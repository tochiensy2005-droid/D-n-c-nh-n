from pathlib import Path
import io
import os
import sys
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms, datasets


BASE_DIR = Path(__file__).resolve().parent.parent

# Ensure we can import RAG package
rag_dir = BASE_DIR / "RAG"
if str(rag_dir) not in sys.path:
    sys.path.insert(0, str(rag_dir))

try:
    from app_internet import InternetRAGChatbot
except Exception as e:
    InternetRAGChatbot = None


app = FastAPI(title="Hanoi Tourism AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    place_name: Optional[str] = None


class ChatResponse(BaseModel):
    status: str
    answer: str
    num_sources: int = 0


class PredictResponse(BaseModel):
    status: str
    place_name: str
    confidence: float
    info: Optional[ChatResponse] = None


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

DATASET_DIR = BASE_DIR / "archive" / "dataset"
TRAIN_DIR = DATASET_DIR / "train"
MODEL_PATH = DATASET_DIR / "tourism_model.pth"


train_dataset = datasets.ImageFolder(str(TRAIN_DIR))
classes = train_dataset.classes
num_classes = len(classes)

model = models.efficientnet_b0(weights=None)
model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model = model.to(device)
model.eval()

transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ]
)


chatbot: Optional[InternetRAGChatbot] = None
if InternetRAGChatbot is not None:
    try:
        chatbot = InternetRAGChatbot()
    except Exception:
        chatbot = None


def predict_image(image: Image.Image):
    img = image.convert("RGB")
    img = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(img)
        probs = F.softmax(outputs, dim=1)
    _, predicted = torch.max(probs, 1)
    top1_class = classes[predicted.item()]
    top1_conf = float(probs[0][predicted.item()])
    return top1_class, top1_conf


@app.get("/")
def read_root():
    return {"message": "Hanoi Tourism AI Backend is running"}


@app.post("/predict-location", response_model=PredictResponse)
async def predict_location(image: UploadFile = File(...)):
    if image.content_type not in ["image/png", "image/jpeg", "image/jpg", "image/bmp", "image/tiff"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    content = await image.read()
    try:
        pil_img = Image.open(io.BytesIO(content))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    place_name, confidence = predict_image(pil_img)

    info = None
    if chatbot is not None:
        try:
            query = f"Du lịch {place_name} Hà Nội"
            result = chatbot.query(query)
            info = ChatResponse(
                status=result.get("status", "success"),
                answer=result.get("answer", "Không tìm thấy thông tin"),
                num_sources=result.get("num_sources", 0),
            )
        except Exception:
            info = None

    return PredictResponse(
        status="success",
        place_name=place_name,
        confidence=confidence,
        info=info,
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if chatbot is None:
        raise HTTPException(status_code=500, detail="Chatbot is not available")

    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question must not be empty")

    if request.place_name:
        full_question = f"Địa điểm là {request.place_name}. {question}"
    else:
        full_question = question

    try:
        result = chatbot.query(full_question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ChatResponse(
        status=result.get("status", "success"),
        answer=result.get("answer", "Không có câu trả lời"),
        num_sources=result.get("num_sources", 0),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)


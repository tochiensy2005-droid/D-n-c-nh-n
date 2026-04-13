from pathlib import Path
import io
import os
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

app = FastAPI(title="Hanoi Tourism AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictResponse(BaseModel):
    status: str
    place_name: str
    confidence: float


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

DATASET_DIR = BASE_DIR / "archive" / "dataset"
TRAIN_DIR = DATASET_DIR / "train"
MODEL_PATH = DATASET_DIR / "tourism_model.pth"


train_dataset = datasets.ImageFolder(str(TRAIN_DIR))
classes = train_dataset.classes
num_classes = len(classes)

model = models.efficientnet_b0(weights=None)
model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=True))
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

    return PredictResponse(
        status="success",
        place_name=place_name,
        confidence=confidence,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)


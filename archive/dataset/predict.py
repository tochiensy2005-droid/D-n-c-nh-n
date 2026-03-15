import logging
import warnings

# Giảm log/Warning không cần thiết để đầu ra chỉ chứa dự đoán và thông tin
logging.basicConfig(level=logging.ERROR)
logging.getLogger("web_search").setLevel(logging.ERROR)
logging.getLogger("app_internet").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=FutureWarning)

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms, datasets
from PIL import Image
import os
import sys
from pathlib import Path

# =========================
# DEVICE
# =========================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =========================
# LOAD DATASET (ĐỂ LẤY CLASS ĐÚNG THỨ TỰ)
# =========================
train_dataset = datasets.ImageFolder("train")
classes = train_dataset.classes
num_classes = len(classes)

# =========================
# LOAD MODEL
# =========================
model = models.efficientnet_b0(weights=None)
model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)

model.load_state_dict(torch.load("tourism_model.pth", map_location=device))
model = model.to(device)
model.eval()

# =========================
# TRANSFORM (PHẢI GIỐNG LÚC TRAIN)
# =========================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

# =========================
# PREDICT ALL IMAGES IN TEST FOLDER
# =========================
test_folder = "Test"

if not os.path.exists(test_folder):
    print("Test folder not found!")
    exit()

for filename in os.listdir(test_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        image_path = os.path.join(test_folder, filename)
        
        try:
            img = Image.open(image_path).convert("RGB")
            img = transform(img).unsqueeze(0).to(device)
            
            # =========================
            # PREDICTION
            # =========================
            with torch.no_grad():
                outputs = model(img)
                probs = F.softmax(outputs, dim=1)
            
            # Top 1
            _, predicted = torch.max(probs, 1)
            top1_class = classes[predicted.item()]
            top1_conf = float(probs[0][predicted.item()])
            
            # Chỉ hiển thị dự đoán chính
            print(f"\n✅ Dự đoán: {top1_class} ({top1_conf:.4f})")
            
            # Tự động tìm thông tin từ internet về địa điểm dự đoán
            print(f"\n🔍 Tìm thông tin về địa điểm: {top1_class}")
            
            # Chuyển đến thư mục RAG để import
            rag_dir = Path(__file__).resolve().parent.parent.parent / "RAG"
            sys.path.insert(0, str(rag_dir))
            os.chdir(rag_dir)
            
            try:
                from app_internet import InternetRAGChatbot
                
                chatbot = InternetRAGChatbot()
                
                # Tìm kiếm thông tin
                query = f"Du lịch {top1_class}"
                result = chatbot.query(query)
                
                print("\n" + "="*60)
                print(f"📍 THÔNG TIN VỀ {top1_class.upper()}")
                print("="*60)
                print(result.get("answer", "Không tìm thấy thông tin"))
                
                if result.get("sources"):
                    print(f"\n🌐 Nguồn tham khảo ({result.get('num_sources', 0)}):")
                    for source in result["sources"]:
                        print(f"  • {source['title']}")
                        print(f"    URL: {source['url']}")
                
                print("="*60)
            
            except Exception as e:
                print(f"❌ Lỗi khi tìm kiếm thông tin: {e}")
                print("💡 Đảm bảo các thư viện cần thiết đã được cài đặt và API key đã được cấu hình.")
            
            # Chuyển lại thư mục dataset để tiếp tục xử lý ảnh khác
            os.chdir(Path(__file__).resolve().parent)
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("\nAll images processed!")

# =========================
# Hỏi người dùng có thêm câu hỏi không
# =========================
print("\n" + "="*60)
print("Bạn có thêm câu hỏi nào không?")
print("(y/n để vào chế độ chatbot, hoặc exit để thoát)")
print("="*60)

while True:
    user_input = input("👤 Bạn: ").strip().lower()
    if user_input == 'y' or user_input == 'yes':
        print("\n" + "="*60)
        print("💬 CHẾ ĐỘ CHATBOT AI AGENT")
        print("Bạn có thể hỏi thêm về du lịch hoặc bất kỳ chủ đề nào!")
        print("(Nhập 'exit' để thoát)")
        print("="*60)
        # Chuyển đến RAG và khởi tạo chatbot
        rag_dir = Path(__file__).resolve().parent.parent.parent / "RAG"
        os.chdir(rag_dir)
        try:
            from app_internet import InternetRAGChatbot
            chatbot = InternetRAGChatbot()
            chatbot.interactive_chat()
        except Exception as e:
            print(f"❌ Lỗi khởi tạo chatbot: {e}")
        break
    elif user_input == 'n' or user_input == 'no' or user_input == 'exit':
        print("👋 Cảm ơn! Chúc bạn có chuyến đi vui vẻ!")
        break
    else:
        print("Vui lòng nhập 'y', 'n', hoặc 'exit'")
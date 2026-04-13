# 📱 Du Lịch Hà Nội AI - Mobile App

Ứng dụng di động nhận diện địa điểm du lịch Hà Nội sử dụng camera và AI.

## ✨ Tính năng

- 📷 **Chụp ảnh địa điểm**: Sử dụng camera để chụp ảnh các điểm du lịch
- 🧠 **Nhận diện AI**: Gửi ảnh lên server để phân tích bằng AI
- 💬 **Chatbot thông minh**: Hỏi đáp về địa điểm đã nhận diện
- 🌐 **Web App**: Chạy trên trình duyệt mobile, không cần cài đặt
- 📱 **PWA Support**: Có thể cài đặt như app native

## 🚀 Cách chạy (Dễ nhất)

### Double-click file `run_app.bat`

File này sẽ tự động:
1. Khởi động backend API server
2. Khởi động mobile app server trên port 3000

### Hoặc chạy thủ công:

```bash
# Terminal 1: Backend (phải dùng virtual environment)
cd d:\dean-main
.venv\Scripts\activate
cd backend
python main.py

# Terminal 2: Mobile App
cd d:\dean-main\mobile-app
python -m http.server 3000
```

## 📱 Truy cập từ điện thoại

### Cách 1: Cùng mạng WiFi
- Máy tính và điện thoại cùng kết nối WiFi
- Tìm IP của máy tính: `ipconfig` (Windows) hoặc `ifconfig` (Linux/Mac)
- Trên điện thoại: `http://[IP_MAY_TINH]:3000`

### Cách 2: USB Debugging (Android)
- Kết nối điện thoại qua USB
- Bật USB debugging trong Developer Options
- Forward port: `adb reverse tcp:3000 tcp:3000`
- Truy cập: `http://localhost:3000`

### Cách 3: Trên máy tính (Test)
- Truy cập: `http://localhost:3000`
- Sử dụng camera của máy tính

## 📋 Hướng dẫn sử dụng

1. **Mở app** trên điện thoại
2. **Cho phép truy cập camera** khi được hỏi
3. **Chụp ảnh** địa điểm du lịch Hà Nội
4. **Nhấn "Phân tích"** để AI nhận diện
5. **Xem thông tin chi tiết** về địa điểm
6. **Hỏi thêm** qua chatbot tích hợp

## 🏗️ Kiến trúc hệ thống

```
Mobile App (Web + PWA)
    ↓ HTTP requests
Backend API (FastAPI - localhost:8000)
    ↓ Image processing
AI Model (PyTorch EfficientNet-B0)
    ↓ Place recognition
Dataset (14 địa điểm Hà Nội)
    ↓ Information retrieval
RAG Chatbot (Gemini AI)
```

## 📋 Địa điểm hỗ trợ

| Địa điểm | Độ chính xác | Mô tả |
|----------|-------------|--------|
| Hồ Hoàn Kiếm | ⭐⭐⭐⭐⭐ | Biểu tượng Hà Nội |
| Văn Miếu | ⭐⭐⭐⭐⭐ | Trường đại học đầu tiên VN |
| Chùa Một Cột | ⭐⭐⭐⭐⭐ | Kiến trúc độc đáo |
| Lăng Bác Hồ | ⭐⭐⭐⭐⭐ | Di tích quốc gia |
| Cầu Long Biên | ⭐⭐⭐⭐⭐ | Cầu sắt lịch sử |
| Phố Cổ Hà Nội | ⭐⭐⭐⭐⭐ | Khu thương mại cổ |
| Nhà hát Lớn | ⭐⭐⭐⭐⭐ | Kiến trúc Pháp |
| Đền Ngọc Sơn | ⭐⭐⭐⭐⭐ | Đền trên đảo |
| Tháp Bút | ⭐⭐⭐⭐⭐ | Tháp Văn Miếu |
| Và nhiều địa điểm khác... | ⭐⭐⭐⭐ | |

## 🔧 Yêu cầu kỹ thuật

### Backend Server
- Python 3.8+
- PyTorch + Torchvision
- FastAPI + Uvicorn
- PIL (Pillow)

### Mobile App
- Trình duyệt hiện đại hỗ trợ:
  - HTML5 Camera API
  - ES6+ JavaScript
  - CSS Grid/Flexbox
  - Service Worker (PWA)

### Camera
- Camera sau (recommended) cho chụp cảnh quan
- Độ phân giải tối thiểu 720p
- Hỗ trợ autofocus

## 🚀 Tính năng nâng cao

- [x] **PWA Support**: Cài đặt như app native
- [x] **Camera Switching**: Chuyển đổi camera trước/sau
- [x] **Real-time Chat**: Hỏi đáp về địa điểm
- [ ] **Offline Mode**: Cache dữ liệu địa điểm
- [ ] **GPS Integration**: Gợi ý địa điểm gần nhất
- [ ] **AR Overlays**: Hiển thị thông tin AR
- [ ] **Social Sharing**: Chia sẻ kết quả
- [ ] **Multi-language**: Hỗ trợ tiếng Anh

## 🐛 Xử lý sự cố

### Lỗi "Cannot access camera"
- Đảm bảo HTTPS hoặc localhost
- Cho phép quyền camera trong browser settings
- Thử refresh trang

### Lỗi "Cannot connect to backend"
- Kiểm tra backend server đang chạy: `http://localhost:8000`
- Đảm bảo firewall không chặn port 3000
- Kiểm tra IP address khi truy cập từ mobile

### Lỗi "Model not found"
- Đảm bảo file `tourism_model.pth` tồn tại
- Kiểm tra đường dẫn trong `main.py`

### Độ chính xác thấp
- Chụp ảnh rõ ràng, đủ sáng
- Đảm bảo địa điểm trong khung hình
- Thử chụp từ nhiều góc độ

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Mở Developer Tools (F12) để xem console errors
2. Kiểm tra Network tab xem API calls
3. Đảm bảo backend và mobile app cùng chạy
4. Thử restart cả hai server

## 🎯 Mục tiêu phát triển

- **Phase 1** ✅: Core camera + AI recognition
- **Phase 2** 🔄: PWA + offline support
- **Phase 3** 📋: GPS + AR features
- **Phase 4** 🚀: Multi-platform deployment

---

**🎉 Chúc bạn có trải nghiệm tuyệt vời khi khám phá Hà Nội với AI!**
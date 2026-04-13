# 🚀 HƯỚNG DẪN NHANH - Du Lịch Hà Nội AI Mobile App

## ⚡ Khởi động nhanh (1 click)

**Double-click file:** `start_mobile_app.bat`

Script này sẽ tự động khởi động:
- ✅ Backend API Server (port 8000)
- ✅ Mobile App Server (port 3000)

## 📱 Truy cập từ điện thoại

### Bước 1: Tìm IP máy tính
```cmd
ipconfig
```
Tìm **IPv4 Address** (ví dụ: 192.168.1.100)

### Bước 2: Mở trình duyệt trên điện thoại
```
http://[IP_MAY_TINH]:3000
```

### Bước 3: Cho phép camera
- App sẽ yêu cầu truy cập camera
- Chọn **"Allow"**

## 🎯 Cách sử dụng

1. **Chụp ảnh** địa điểm du lịch Hà Nội
2. **Nhấn "Phân tích"** để AI nhận diện
3. **Xem thông tin** chi tiết về địa điểm
4. **Hỏi thêm** qua chatbot

## 🛠️ Troubleshooting

### ❌ "Cannot connect to backend"
- Đảm bảo backend server đang chạy
- Kiểm tra firewall không chặn port 8000/3000

### ❌ "Camera not accessible"
- Đảm bảo HTTPS hoặc localhost
- Cho phép camera permissions
- Thử refresh trang

### ❌ "Model not found"
- Kiểm tra file `tourism_model.pth` tồn tại
- Đảm bảo đúng đường dẫn trong code

## 📞 Cần hỗ trợ?

1. Mở Developer Tools (F12)
2. Kiểm tra Console tab xem lỗi
3. Kiểm tra Network tab xem API calls

---

**🎉 Chúc bạn khám phá Hà Nội vui vẻ!**
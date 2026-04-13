# 🔧 TROUBLESHOOTING - Du Lịch Hà Nội AI Mobile App

## ❌ Lỗi thường gặp và cách sửa

### 1. **"Form data requires python-multipart"**

**Nguyên nhân:** Thiếu package python-multipart trong virtual environment

**Giải pháp:**
```bash
cd d:\dean-main
.venv\Scripts\activate
pip install python-multipart
```

### 2. **"Cannot import torch" hoặc lỗi multiprocessing**

**Nguyên nhân:** Chạy backend không dùng virtual environment

**Giải pháp:**
```bash
cd d:\dean-main
.venv\Scripts\activate
cd backend
python main.py
```

### 3. **FutureWarning về torch.load**

**Nguyên nhân:** Cần cập nhật code để tương thích với PyTorch mới

**Giải pháp:** Đã được sửa trong `main.py` (thêm `weights_only=True`)

### 4. **Mobile app không kết nối được backend**

**Nguyên nhân:** IP address hoặc port không đúng

**Giải pháp:**
- Kiểm tra backend chạy trên port 8000
- Tìm IP máy tính: `ipconfig` → IPv4 Address
- Truy cập: `http://[IP]:3000`

### 5. **Camera không hoạt động trên mobile**

**Nguyên nhân:** Browser không hỗ trợ hoặc thiếu HTTPS

**Giải pháp:**
- Sử dụng Chrome/Safari trên mobile
- Đảm bảo HTTP (localhost) hoặc HTTPS
- Cho phép camera permissions khi được hỏi

### 6. **"Model not found" hoặc "File not found"**

**Nguyên nhân:** Đường dẫn file model không đúng

**Giải pháp:**
- Kiểm tra file `tourism_model.pth` tồn tại trong `archive/dataset/`
- Đảm bảo đường dẫn trong `main.py` đúng

## 🧪 Cách test từng thành phần

### Test Backend API:
```powershell
# Health check
Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing

# Docs API
start http://localhost:8000/docs
```

### Test Mobile App:
```bash
cd d:\dean-main\mobile-app
python -m http.server 3000
# Truy cập: http://localhost:3000
```

### Test Camera:
- Mở app trên mobile
- Nhấn "Chụp ảnh"
- Kiểm tra camera bật lên

### Test AI Recognition:
- Chụp ảnh địa điểm Hà Nội
- Nhấn "Phân tích"
- Kiểm tra console browser (F12) xem có lỗi API call

## 📊 Logs và Debug

### Xem logs backend:
- Mở terminal chạy backend
- Nhìn vào output để tìm lỗi

### Debug mobile app:
- Mở Developer Tools (F12)
- Tab Console: xem lỗi JavaScript
- Tab Network: xem API calls

### Test API endpoints:
```bash
# Test chat endpoint
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "Hồ Hoàn Kiếm ở đâu?", "place_name": "Hồ Hoàn Kiếm"}'
```

## 🚀 Performance Tips

### Backend:
- Sử dụng GPU nếu có: đảm bảo CUDA installed
- Giảm batch size nếu memory thấp
- Cache model sau lần load đầu

### Mobile App:
- Nén ảnh trước khi upload (đã implement)
- Sử dụng Service Worker để cache
- Tối ưu hình ảnh và CSS

### Network:
- Sử dụng cùng WiFi network
- Tránh firewall chặn ports
- Sử dụng HTTPS nếu deploy production

## 📞 Cần hỗ trợ thêm?

1. **Check logs** - Xem terminal output
2. **Browser console** - F12 để debug
3. **Network tab** - Kiểm tra API calls
4. **Restart servers** - Đôi khi cần restart

---

**💡 Tip:** Luôn chạy backend với virtual environment để tránh conflicts!**

# ✅ UPDATE - Du Lịch Hà Nội AI Mobile App

## 🔧 Những thay đổi vừa làm

### 1. **Sửa năm 2024 → 2026** ✅
   - File: `index.html` (footer)
   - Từ: `© 2024 Du Lịch Hà Nội AI`
   - Thành: `© 2026 Du Lịch Hà Nội AI`

### 2. **Cải thiện xử lý lỗi Camera** ✅
   - **Kiểm tra hỗ trợ trình duyệt**: Xác nhận `navigator.mediaDevices` có sẵn
   - **Chi tiết lỗi**: Phân loại lỗi (NotAllowedError, NotFoundError, etc.)
   - **Hướng dẫn người dùng**: Hiển thị lỗi cụ thể cho mỗi tình huống
   - **Fallback**: Gợi ý tải ảnh từ thư viện khi camera không hoạt động

### 3. **Thêm tính năng Upload ảnh từ Thư viện** ✅
   - **UI**: Nút "Tư thư viện" bên cạnh nút chụp ảnh
   - **Functionality**: 
     - Click button → Mở file picker
     - Chọn ảnh từ device
     - Hiển thị preview before analyze
   - **Validation**:
     - Kiểm tra file type (chỉ image)
     - Giới hạn kích thước (max 5MB)
     - Error messages rõ ràng
   - **Code**: 
     - Method `handleFileUpload()` trong `app.js`
     - File input element trong `index.html`

### 4. **Cải thiện CSS & UX** ✅
   - **Responsive buttons**: `flex-wrap` cho camera controls
   - **Button states**: Disable khi camera không available
   - **Hover effects**: Transform & shadow effects
   - **Active states**: Visual feedback khi click

---

## 🚀 Cách sử dụng app ngay

### Camera:
1. Mở app từ điện thoại
2. Cho phép camera permissions
3. Chụp ảnh hoặc tải từ thư viện
4. Nhấn "Phân tích"

### Upload từ Thư viện:
1. Mở app
2. Nhấn "Tư thư viện"
3. Chọn ảnh từ device
4. Nhấn "Phân tích"

---

## 📋 File đã sửa

| File | Thay đổi |
|------|----------|
| `index.html` | ✅ Thêm nút upload, sửa năm 2024→2026 |
| `app.js` | ✅ Cải thiện camera, thêm file upload handler |
| `styles.css` | ✅ Update responsive design, button states |

---

## 🔍 Kiểm tra lỗi Camera

**Nếu camera vẫn không hoạt động:**

1. **Kiểm tra trình duyệt**: Sử dụng Chrome, Firefox, Safari
2. **Cho phép permissions**: Browser sẽ hỏi khi mở app lần đầu
3. **Check console**: F12 → Console tab để xem chi tiết lỗi
4. **Thử upload**: Dùng "Tư thư viện" thay thế
5. **Khởi động lại**: Reload trang một lần nữa

---

## 🎯 Ưu điểm của bản cập nhật

✅ **Khiến hệ thống linh hoạt hơn**: Có thể dùng camera hoặc upload từ file  
✅ **User-friendly errors**: Người dùng biết được lỗi gì và cách fix  
✅ **Better UX**: Nút được disable khi không khả dụng  
✅ **Fallback option**: Luôn có cách khác để hoạt động  

---

## 🖼️ Screenshot áp dụng

Ứng dụng giờ đây hiển thị:
- ✅ Nút "Chụp ảnh" (camera)
- ✅ Nút "Tư thư viện" (upload)
- ✅ Nút "Đổi camera" (front/back)
- ✅ Footer với năm 2026
- ✅ Tốt hơn messages & error handling

---

**🎉 App đã được cập nhật! Bạn có thể reload trang để thấy thay đổi!**
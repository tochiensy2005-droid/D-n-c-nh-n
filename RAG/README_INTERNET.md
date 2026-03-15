# 🚀 Hướng dẫn - Chuyển sang Tìm kiếm Internet

## 📋 Tóm tắt Thay đổi

Đã triển khai 3 bước đầu tiên:

### ✅ Bước 1: Nghiên cứu và Chọn API Web Search
- **API được chọn**: `DuckDuckGo Search` (không cần API key)
- **Lýlý do**:
  - Miễn phí và không giới hạn
  - Không cần đăng ký API key
  - Hỗ trợ tìm kiếm đa ngôn ngữ
  - Có sẵn thư viện `duckduckgo-search`

### ✅ Bước 2: Tạo Mô-đun Web Search
**File mới**: `web_search.py`
- Lớp `WebSearcher`: Tìm kiếm web + cạo nội dung từ URL
- Lớp `WebContentProcessor`: Xử lý và chunking nội dung web
- Hỗ trợ cạo HTML và trích xuất text

### ✅ Bước 3: Sửa Đổi Các Mô-đun Hiện Có
- **requirements.txt**: Thêm dependencies
  - `duckduckgo-search==3.9.10`
  - `requests==2.31.0`
  - `beautifulsoup4==4.12.2`

- **config.py**: Thêm cấu hình web search
  - `MODE`: Chọn 'internet' hoặc 'pdf'
  - `WEB_SEARCH_TIMEOUT`, `WEB_SEARCH_NUM_RESULTS`

- **app_internet.py** (tệp mới): Chatbot dùng web search
  - Giữ lại app.py cũ để sử dụng PDF nếu cần

## 📦 Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

Hoặc cài riêng:
```bash
pip install duckduckgo-search requests beautifulsoup4
```

## 🎯 Cách Sử dụng

### Sử dụng Chatbot Tìm kiếm Internet (Mới)

```bash
python app_internet.py
```

**Ví dụ**:
```
👤 Bạn: Thông tin về du lịch Hà Nội
🤖 Chatbot: [Trả lời dựa trên thông tin từ Internet]

🌐 Nguồn tham khảo:
  • Vietnam - The Hanoi Travel Guide
    URL: https://example.com/hanoi
```

### Sử dụng Chatbot Cũ (PDF)

```bash
python app.py
```

## 📊 So Sánh

| Tính năng | PDF (Cũ) | Internet (Mới) |
|----------|----------|----------------|
| Dữ liệu | Cục bộ, tĩnh | Internet, động |
| Cập nhật | Thủ công | Tự động mới nhất |
| Tốc độ | Nhanh | Phụ thuộc mạng |
| API Key | Không cần | Không cần (DuckDuckGo) |
| Kích thước | ~150MB index | Không cần lưu |
| Độ tin cậy | Cao (dữ liệu xác định) | Phụ thuộc khả dụng web |

## 🔧 Cấu hình

### .env file

Đảm bảo có:
```env
GEMINI_API_KEY=your_key_here
RAG_MODE=internet
```

### Tùy chỉnh trong config.py

```python
WEB_SEARCH_TIMEOUT = 10  # Timeout khi cạo
WEB_SEARCH_NUM_RESULTS = 5  # Số trang cạo
WEB_SEARCH_REGION = 'vn'  # Ưu tiên Việt Nam
```

## 🐛 Xử lý Lỗi

**Lỗi**: "Timeout khi cạo trang web"
- Giảm `WEB_SEARCH_TIMEOUT` hoặc tăng nó lên

**Lỗi**: "Không tìm thấy kết quả"
- Thử với từ khóa khác
- Kiểm tra kết nối internet

**Lỗi**: "GEMINI_API_KEY chưa được thiết lập"
- Kiểm tra file `.env`
- Đảm bảo có API key hợp lệ

## ✨ Cải thiện tiêm theo

### Tiếp theo (Bước 4, 5, 6)
1. **Bước 4**: Tối ưu hóa retrieval
   - Thêm caching
   - Lọc kết quả không liên quan
   - Ranking theo độ liên quan

2. **Bước 5**: Kiểm thử
   - Test với nhiều query
   - So sánh kết quả PDF vs Internet

3. **Bước 6**: Error handling và logging
   - Thêm retry logic
   - Logging chi tiết

## 📚 Cấu trúc File

```
RAG/
├── app.py                 # Chatbot cũ (PDF)
├── app_internet.py        # Chatbot mới (Web Search)
├── web_search.py          # Module tìm kiếm web
├── config.py              # Cấu hình
├── embedding_service.py   # Embedding service
├── vector_store.py        # FAISS store
├── gemini_rag.py         # RAG logic
├── requirements.txt       # Dependencies
└── README.md             # Bạn đây
```

---

**Trạng thái**: ✅ Hoàn thành bước 1-3
**Tiếp theo**: Bước 4-6 (tối ưu, test, error handling)

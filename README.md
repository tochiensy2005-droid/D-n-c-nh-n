🌏 RAG CHATBOT – TRỢ LÝ DU LỊCH VIỆT NAM (INTERNET)
Dự án này xây dựng một trợ lý du lịch Việt Nam sử dụng:
- 🌐 Tìm kiếm thông tin du lịch **trực tiếp từ Internet**
- 🧠 Mô hình ngôn ngữ **Google Gemini**
- 🔎 Cơ chế RAG: truy xuất thông tin từ web → tổng hợp câu trả lời tự nhiên, dễ hiểu
---
## 📚 Công Nghệ Sử Dụng
| Thành phần           | Công nghệ / Mô tả                                                                 |
|----------------------|------------------------------------------------------------------------------------|
| Web Search           | **SerpApi (Google Search)** – tìm kiếm kết quả liên quan đến câu hỏi              |
| Web Scraping         | **requests + BeautifulSoup4** – cào và làm sạch nội dung HTML                     |
| Semantic Chunking    | Cắt nhỏ nội dung web theo đoạn, giới hạn độ dài để Gemini xử lý tốt               |
| LLM                  | **Google Gemini (models/gemini-2.5-flash)** – sinh câu trả lời                    |
| RAG Pipeline         | Tìm kiếm → trích xuất nội dung → xây dựng ngữ cảnh → gọi Gemini                  |
| Caching              | Lưu cache kết quả tìm kiếm vào `search_cache.json` để giảm số lần gọi SerpApi     |
| Cấu hình             | `config.py` – quản lý API key, timeout, số kết quả, vùng tìm kiếm, v.v.          |
---
## ⚙️ Cấu hình chính
File `RAG/config.py`:
- **Chế độ hoạt động**  
  ```python
  MODE = os.getenv("RAG_MODE", "internet")  # hiện tại dùng internet
Web Search
WEB_SEARCH_TIMEOUT = 10        # timeout cào nội dung (giây)
WEB_SEARCH_NUM_RESULTS = 5     # số kết quả web sẽ cào
WEB_SEARCH_REGION = 'vn'       # ưu tiên kết quả Việt Nam
Gemini
GEMINI_MODEL = "models/gemini-2.5-flash"
GEMINI_TEMPERATURE = 0.3
GEMINI_MAX_TOKENS = 2048
📦 Cài Đặt
Trong thư mục RAG/:

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
requirements.txt (rút gọn các gói chính):

google-generativeai
serpapi
requests
beautifulsoup4
python-dotenv
(các gói khác có thể dùng cho mở rộng sau)
🔑 Thiết lập biến môi trường
Tạo file .env trong thư mục RAG:

GEMINI_API_KEY=your_gemini_key_here
SERPAPI_API_KEY=your_serpapi_key_here
RAG_MODE=internet
🚀 Chạy Chatbot Internet
Trong thư mục RAG:

venv\Scripts\activate
python app_internet.py
Gõ câu hỏi trực tiếp trong terminal, ví dụ:

👤 Bạn: Gợi ý lịch trình 3 ngày du lịch Hà Nội
Chatbot sẽ:

Gọi SerpApi để tìm các trang web liên quan
Cào và tóm tắt nội dung
Gọi Gemini để sinh câu trả lời
In kèm danh sách nguồn tham khảo (URL, tiêu đề, snippet)

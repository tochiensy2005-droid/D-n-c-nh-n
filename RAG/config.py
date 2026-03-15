import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ==================== CHẾ ĐỘ HOẠT ĐỘNG ====================
# Chọn 'pdf' để sử dụng PDF cục bộ, 'internet' để tìm kiếm trên web
MODE = os.getenv("RAG_MODE", "internet")  # Mặc định: internet

# ==================== ĐƯỜNG DẪN PDF ====================
PDF_FILE_1 = r"D:\dean-main\archive (1)\Đề án.pdf"  # 536 trang
PDF_FILE_2 = r"D:\dean-main\archive (1)\vietnam_tourism_data.pdf"  # 2807 trang

# ==================== CÀI ĐẶT CHUNK ====================
CHUNK_SIZE = 1500  # ký tự
CHUNK_OVERLAP = 150  # 10% của 1500
SEMANTIC_CHUNKING = True

# ==================== CÀI ĐẶT EMBEDDING ====================
# Sử dụng mô hình công khai từ sentence-transformers
EMBEDDING_MODEL = "intfloat/multilingual-e5-base"
EMBEDDING_DIMENSION = 768

# ==================== CÀI ĐẶT VECTOR DB ====================
# Lưu trữ chỉ mục trong đường dẫn tương đối với thư mục dự án (tránh mã hóa cứng
# một ký tự ổ đĩa có thể không tồn tại trên máy hiện tại).
# Kho vector sẽ tự động tạo các thư mục cha khi lưu.
BASE_DIR = Path(__file__).parent
FAISS_INDEX_PATH = str(BASE_DIR / "data" / "faiss_index" / "index.faiss")
FAISS_METADATA_PATH = str(BASE_DIR / "data" / "faiss_metadata.pkl")

# ==================== CÀI ĐẶT TÌM KIẾM SEMANTIC ====================
TOP_K = 5  # Số lượng kết quả hàng đầu để truy xuất
SIMILARITY_THRESHOLD = 0.45  # Ngưỡng cân bằng để lọc ra kết quả không liên quan
USE_SIMILARITY_THRESHOLD = False  # Boolean bật/tắt

# ==================== CÀI ĐẶT WEB SEARCH ====================
WEB_SEARCH_TIMEOUT = 10  # Timeout khi cạo trang web (giây)
WEB_SEARCH_NUM_RESULTS = TOP_K  # Số lượng kết quả cạo từ web
WEB_SEARCH_REGION = 'vn'  # Ưu tiên kết quả từ Việt Nam

# ==================== CÀI ĐẶT GEMINI ====================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "models/gemini-2.5-flash"  # cập nhật thành mô hình khả dụng (<list_models>)
GEMINI_TEMPERATURE = 0.3
GEMINI_MAX_TOKENS = 2048

# ==================== CÀI ĐẶT RAG ====================
CHAIN_TYPE = "stuff"  # Loại chuỗi Q&A
VERBOSE = True

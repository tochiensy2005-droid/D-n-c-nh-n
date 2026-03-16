"""
Web Search Module - Tìm kiếm thông tin từ Internet
Sử dụng DuckDuckGo để tìm kiếm và Beautiful Soup để cạo nội dung
"""

import logging
import requests
import time
from bs4 import BeautifulSoup
from typing import List, Dict
from config import TOP_K
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSearcher:
    """Lớp tìm kiếm web và trích xuất nội dung"""

    last_search_time = 0  # Thời gian tìm kiếm cuối cùng
    min_interval = 300  # 5 phút giữa các tìm kiếm

    def __init__(self):
        self.requests_timeout = 10  # Timeout 10 giây
        self.max_results = TOP_K * 2  # Lấy nhiều hơn để lọc
        self.cache_file = 'search_cache.json'
        self.cache = self.load_cache()
        self.cache_expiry = 3600  # 1 giờ

        logger.info("✅ WebSearcher khởi tạo thành công")

    def load_cache(self) -> Dict:
        """Load cache từ file"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_cache(self):
        """Lưu cache vào file"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"⚠️ Lỗi lưu cache: {e}")

    def get_cached_result(self, query: str) -> List[Dict]:
        """Lấy kết quả từ cache nếu còn hạn"""
        if query in self.cache:
            cached = self.cache[query]
            if time.time() - cached['timestamp'] < self.cache_expiry:
                logger.info("✅ Sử dụng kết quả từ cache")
                return cached['results']
            else:
                # Xóa cache hết hạn
                del self.cache[query]
                self.save_cache()
        return []

    def search_web(self, query: str) -> List[Dict]:
        """
        Tìm kiếm trên web.

        Phiên bản hiện tại đã được đơn giản hóa để KHÔNG
        sử dụng SerpApi hay bất kỳ dịch vụ tìm kiếm trả phí nào.
        Hàm này trả về danh sách rỗng, và phần gọi Gemini sẽ
        chịu trách nhiệm trả lời trực tiếp dựa trên kiến thức
        của mô hình thay vì dữ liệu cào từ web.

        Args:
            query: Câu hỏi/từ khóa tìm kiếm

        Returns:
            Danh sách kết quả tìm kiếm với metadata
        """
        logger.info(f"🔍 (BỎ SERPAPI) Bỏ qua tìm kiếm web thực, sẽ để Gemini trả lời trực tiếp cho truy vấn: '{query}'")
        return []

    def extract_content(self, url: str) -> str:
        """
        Cạo nội dung từ URL

        Args:
            url: Đường dẫn web cần cạo

        Returns:
            Nội dung text từ trang web
        """
        try:
            logger.info(f"  📄 Đang load: {url[:60]}...")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=self.requests_timeout)
            response.encoding = 'utf-8'

            if response.status_code != 200:
                logger.warning(f"     ⚠️ HTTP {response.status_code}")
                return ""

            soup = BeautifulSoup(response.content, 'html.parser')

            # Loại bỏ script, style, nav
            for script in soup(["script", "style", "nav", "noscript"]):
                script.decompose()

            # Lấy text
            text = soup.get_text(separator='\n', strip=True)

            # Làm sạch
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            content = '\n'.join(lines[:200])  # Giới hạn 200 dòng

            logger.info(f"     ✅ Extracted {len(content)} chars")
            return content

        except requests.Timeout:
            logger.warning(f"     ⏱️ Timeout {self.requests_timeout}s")
            return ""
        except Exception as e:
            logger.warning(f"     ⚠️ Lỗi cạo: {str(e)[:50]}")
            return ""

    def search_and_extract(self, query: str, num_results: int = TOP_K) -> List[Dict]:
        """
        Tìm kiếm web và trích xuất nội dung từ kết quả

        Args:
            query: Câu hỏi/từ khóa
            num_results: Số lượng kết quả cần lấy

        Returns:
            Danh sách documents với nội dung đầy đủ
        """
        # Tìm kiếm
        search_results = self.search_web(query)

        if not search_results:
            logger.warning("❌ Không tìm thấy kết quả")
            return []

        documents = []

        logger.info(f"📥 Đang cạo {min(len(search_results), num_results)} trang...")

        for i, result in enumerate(search_results[:num_results]):
            try:
                url = result.get('href', '')
                title = result.get('title', 'Không rõ')
                snippet = result.get('body', '')

                if not url:
                    continue

                # Cạo nội dung đầy đủ
                content = self.extract_content(url)

                # Nếu không cạo được nội dung, dùng snippet
                if not content:
                    content = snippet

                doc = {
                    'content': content,
                    'metadata': {
                        'source': url,
                        'title': title,
                        'snippet': snippet[:200]
                    }
                }

                documents.append(doc)

            except Exception as e:
                logger.warning(f"   ⚠️ Lỗi xử lý result {i+1}: {str(e)[:50]}")
                continue

        logger.info(f"✅ Trích xuất thành công: {len(documents)} trang\n")
        return documents


class WebContentProcessor:
    """Xử lý nội dung web tương tự như PDF chunking"""

    def __init__(self, chunk_size: int = 1500, chunk_overlap: int = 150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        logger.info(f"✅ WebContentProcessor khởi tạo (chunk_size={chunk_size})")

    def chunk_content(self, content: str, metadata: dict) -> List[Dict]:
        """
        Chia nội dung web thành chunks

        Args:
            content: Nội dung text
            metadata: Metadata (source, title, etc.)

        Returns:
            Danh sách chunks
        """
        chunks = []

        # Chia theo đoạn văn
        paragraphs = content.split('\n\n')

        current_chunk = ""

        for para in paragraphs:
            # Nếu thêm đoạn này vào vượt quá kích thước, tạo chunk mới
            if len(current_chunk) + len(para) > self.chunk_size:
                if current_chunk:  # Lưu chunk hiện tại
                    chunks.append({
                        'content': current_chunk,
                        'metadata': metadata
                    })
                current_chunk = para
            else:
                if current_chunk:
                    current_chunk += '\n\n' + para
                else:
                    current_chunk = para

        # Thêm chunk cuối cùng
        if current_chunk:
            chunks.append({
                'content': current_chunk,
                'metadata': metadata
            })

        return chunks

    def process_documents(self, documents: List[Dict]) -> List[Dict]:
        """
        Xử lý danh sách documents web thành chunks

        Args:
            documents: Danh sách documents từ web_search_and_extract()

        Returns:
            Danh sách chunks đã xử lý
        """
        logger.info("🔪 BẮT ĐẦU XỬ LÝ NỘI DUNG WEB")

        all_chunks = []

        for doc in documents:
            chunks = self.chunk_content(doc['content'], doc['metadata'])
            all_chunks.extend(chunks)

        logger.info(f"✅ Tạo thành công: {len(all_chunks)} chunks")
        logger.info("=" * 60 + "\n")

        return all_chunks

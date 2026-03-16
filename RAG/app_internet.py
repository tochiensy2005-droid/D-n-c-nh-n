"""
RAG CHATBOT - Ứng dụng tìm kiếm thông tin từ Internet
Sử dụng Gemini + Web Search
"""

import logging
import sys
from pathlib import Path
from config import GEMINI_API_KEY, GEMINI_MODEL
from web_search import WebSearcher, WebContentProcessor
import google.generativeai as genai

# ==================== GHI LOG ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)   
logger = logging.getLogger(__name__)

class InternetRAGChatbot:
    """Chatbot sử dụng Web Search thay vì PDF cục bộ"""
    
    def __init__(self):
        logger.info("\n" + "="*60)
        logger.info("🚀 KHỞI TẠO INTERNET RAG CHATBOT")
        logger.info("="*60)
        
        if not GEMINI_API_KEY:
            raise ValueError("❌ GEMINI_API_KEY chưa được thiết lập!")
        
        # Khởi tạo các thành phần
        logger.info("\n🔄 Khởi tạo hệ thống...")
        
        logger.info("  1️⃣  Khởi tạo Web Searcher...")
        self.web_searcher = WebSearcher()
        
        logger.info("  2️⃣  Khởi tạo Web Content Processor...")
        self.content_processor = WebContentProcessor()
        
        logger.info("  3️⃣  Cấu hình Gemini...")
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        
        logger.info("\n✅ Hệ thống sẵn sàng!\n")
    
    def _build_context_from_web(self, documents: list) -> str:
        """Xây dựng ngữ cảnh từ tài liệu web"""
        context = "=== THÔNG TIN TỪ INTERNET ===\n\n"
        
        for i, doc in enumerate(documents[:5], 1):  # Giới hạn 5 nguồn
            title = doc['metadata'].get('title', 'Không rõ')
            url = doc['metadata'].get('source', '')
            snippet = doc['metadata'].get('snippet', '')
            
            context += f"[{i}] {title}\n"
            context += f"Nguồn: {url}\n"
            context += f"Tóm tắt: {snippet}\n"
            context += f"Nội dung: {doc['content'][:1000]}...\n\n"
        
        return context
    
    def _build_prompt_internet(self, context: str, query: str) -> str:
        """Xây dựng prompt cho Gemini (với dữ liệu web)"""
        prompt = f"""VAI TRÒ: Bạn là một trợ lý AI thông minh, trả lời dựa trên thông tin từ Internet.

THÔNG TIN THAM KHẢO:
{context}

Câu hỏi: {query}

YÊU CẦU:
- Trả lời dựa trên thông tin được cung cấp từ Internet
- Nếu có thông tin liên quan, hãy tóm tắt chi tiết
- Luôn ghi rõ nguồn thông tin (URL hoặc tên trang web)
- Nếu không tìm thấy thông tin phù hợp, hãy thừa nhận
- Trả lời bằng tiếng Việt, rõ ràng và hữu ích
- Nếu cần, cung cấp thêm thông tin liên quan"""
        
        return prompt
    
    def query(self, question: str) -> dict:
        """
        Trả lời câu hỏi bằng cách tìm kiếm trên web
        """
        logger.info("\n" + "="*60)
        logger.info("❓ CÂU HỎI: " + question)
        logger.info("="*60)
        
        try:
            # 1. Tìm kiếm web (đã được cấu hình bỏ SerpApi, có thể trả về rỗng)
            logger.info("🌐 (TÙY CHỌN) Tìm kiếm trên Internet...")
            web_docs = self.web_searcher.search_and_extract(question, num_results=3)
            
            sources = []
            context = ""
            
            if web_docs:
                logger.info(f"✅ Tìm thấy {len(web_docs)} nguồn tham khảo:")
                for doc in web_docs:
                    logger.info(f"   - {doc['metadata']['title'][:50]}")
                
                # Xây dựng context từ web nếu có
                context = self._build_context_from_web(web_docs)
                sources = [
                    {
                        "title": doc['metadata'].get('title', 'Không rõ'),
                        "url": doc['metadata'].get('source', ''),
                        "snippet": doc['metadata'].get('snippet', '')
                    }
                    for doc in web_docs
                ]
                prompt = self._build_prompt_internet(context, question)
            else:
                logger.warning("⚠️ Không sử dụng được dữ liệu web, sẽ để Gemini trả lời trực tiếp từ kiến thức của mô hình.")
                # Prompt đơn giản cho trường hợp không có web context
                prompt = f"""Bạn là một trợ lý AI thông minh, trả lời bằng tiếng Việt.

Câu hỏi của người dùng:
{question}

Hãy trả lời chi tiết, dễ hiểu, tập trung vào bối cảnh du lịch và địa điểm nếu câu hỏi liên quan đến địa danh."""
            
            logger.info(f"📝 Prompt length: {len(prompt)} chars")
            
            # 2. Gọi Gemini
            logger.info("🤖 Gọi Gemini để sinh câu trả lời...")
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=2048
                )
            )
            
            answer = response.text
            logger.info("✅ Sinh câu trả lời thành công\n")
            
            return {
                "status": "success",
                "question": question,
                "answer": answer,
                "sources": sources,
                "num_sources": len(sources)
            }
        
        except Exception as e:
            logger.error(f"❌ Lỗi: {str(e)}")
            return {
                "status": "error",
                "question": question,
                "error": str(e)
            }
    
    def interactive_chat(self):
        """Chế độ chat tương tác"""
        logger.info("\n" + "="*60)
        logger.info("💬 CHẾ ĐỘ TƯƠNG TÁC (WEB SEARCH)")
        logger.info("(Nhập 'exit' để thoát)")
        logger.info("="*60 + "\n")
        
        while True:
            try:
                question = input("👤 Bạn: ").strip()
                
                if question.lower() == 'exit':
                    logger.info("👋 Tạm biệt!")
                    break
                
                if not question:
                    continue
                
                result = self.query(question)
                
                print("\n" + "="*60)
                print("🤖 Chatbot:")
                print("="*60)
                print(result.get("answer", "Không có câu trả lời"))
                print("\n" + "-"*60)
                print(f"📊 Số nguồn tham khảo: {result.get('num_sources', 0)}")
                
                if result.get("sources"):
                    print("\n🌐 Nguồn tham khảo:")
                    for source in result["sources"]:
                        print(f"  • {source['title']}")
                        print(f"    URL: {source['url']}")
                
                print("="*60 + "\n")
            
            except KeyboardInterrupt:
                logger.info("\n👋 Tạm biệt!")
                break
            except Exception as e:
                logger.error(f"❌ Lỗi: {str(e)}\n")

def main():
    try:
        chatbot = InternetRAGChatbot()
        chatbot.interactive_chat()
    
    except Exception as e:
        logger.error(f"❌ Lỗi khởi tạo: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

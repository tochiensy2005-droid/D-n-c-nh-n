from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL, EMBEDDING_DIMENSION
import logging
import numpy as np
import torch

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        logger.info("🧠 KHỞI TẠO DỊCH VỤ EMBEDDING")
        logger.info(f"   Mô hình: {EMBEDDING_MODEL}")
        
        # Thiết lập thiết bị GPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"   Thiết bị: {self.device}")
        
        try:
            self.model = SentenceTransformer(EMBEDDING_MODEL)
            self.model = self.model.to(self.device)
            logger.info(f"   Kích thước: {EMBEDDING_DIMENSION}")
            logger.info("✅ Tải mô hình thành công - GPU sẵn sàng\n")
        except Exception as e:
            logger.error(f"❌ Lỗi tải mô hình: {str(e)}")
            raise
    
    def embed_documents(self, texts: list) -> np.ndarray:
        """Embedding hàng loạt tài liệu với tăng tốc GPU"""
        logger.info(f"📊 Embedding {len(texts)} đoạn (tăng tốc GPU)...")
        
        try:
            embeddings = self.model.encode(
                texts,
                batch_size=32,
                show_progress_bar=True,
                convert_to_numpy=True,
                normalize_embeddings=True,
                device=self.device
            )
            logger.info(f"✅ Embedding thành công: hình dạng {embeddings.shape}\n")
            return embeddings
        
        except Exception as e:
            logger.error(f"❌ Lỗi embedding: {str(e)}")
            raise
    
    def embed_query(self, query: str) -> np.ndarray:
        """Embedding một truy vấn với tăng tốc GPU"""
        try:
            embedding = self.model.encode(
                query,
                convert_to_numpy=True,
                normalize_embeddings=True,
                device=self.device
            )
            return embedding
        except Exception as e:
            logger.error(f"❌ Lỗi embedding query: {str(e)}")
            raise

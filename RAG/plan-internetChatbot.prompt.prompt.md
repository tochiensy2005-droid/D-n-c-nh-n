# Kế hoạch Sửa đổi Chatbot để Lấy Thông tin từ Internet

## Phân tích Triển khai Hiện tại
- Chatbot hiện tại sử dụng RAG (Retrieval-Augmented Generation) với tài liệu PDF cục bộ
- Các thành phần: Tải PDF, phân đoạn ngữ nghĩa, nhúng, kho vector FAISS, truy xuất và tạo LLM
- Các tệp liên quan: pdf_loader.py, semantic_chunker.py, embedding_service.py, vector_store.py, app.py

## Các Thay đổi Đề xuất
1. **Thay thế Tải PDF bằng Tìm kiếm Web**
   - Loại bỏ phụ thuộc pdf_loader.py
   - Triển khai chức năng tìm kiếm web bằng API (Google Custom Search, Bing Search, hoặc tương tự)
   - Thêm khả năng cạo web cho các trang liên quan

2. **Sửa đổi Hệ thống Truy xuất**
   - Cập nhật vector_store.py để xử lý nội dung từ web thay vì PDF cục bộ
   - Triển khai tìm kiếm web thời gian thực cho mỗi truy vấn
   - Thêm cơ chế lưu trữ đệm cho thông tin được truy cập thường xuyên

3. **Cập nhật Pipeline Xử lý Dữ liệu**
   - Sửa đổi semantic_chunker.py để xử lý nội dung web
   - Đảm bảo nhúng hoạt động với dữ liệu web động
   - Thêm lọc nội dung và chấm điểm liên quan

4. **Cải thiện Logic Ứng dụng**
   - Cập nhật app.py để tích hợp tìm kiếm web trước khi truy xuất
   - Thêm xử lý lỗi cho các yêu cầu mạng
   - Triển khai cơ chế dự phòng

5. **Thêm Phụ thuộc Mới**
   - Thư viện API tìm kiếm web (requests, beautifulsoup, v.v.)
   - Cấu hình khóa API công cụ tìm kiếm
   - Quản lý giới hạn tốc độ và hạn ngạch API

## Các Bước Triển khai
1. Nghiên cứu và chọn API tìm kiếm web phù hợp
2. Tạo mô-đun web_search.py mới
3. Sửa đổi các mô-đun hiện có để sử dụng dữ liệu web
4. Cập nhật tệp cấu hình
5. Kiểm tra với các truy vấn mẫu
6. Thêm xử lý lỗi và ghi nhật ký

## Các Thách thức Tiềm ẩn
- Giới hạn tốc độ và chi phí API
- Độ tươi mới nội dung so với độ tin cậy dữ liệu cục bộ
- Xử lý các định dạng nội dung web đa dạng
- Đảm bảo độ chính xác và liên quan của thông tin
- Cân nhắc về quyền riêng tư và sử dụng dữ liệu

## Các Bước Tiếp theo
- Thu thập yêu cầu cho các API tìm kiếm cụ thể
- Tạo nguyên mẫu tích hợp tìm kiếm web
- Kiểm tra hiệu suất và độ chính xác
- Tinh chỉnh dựa trên phản hồi của người dùng
- Prototype web search integration
- Test performance and accuracy
- Refine based on user feedback

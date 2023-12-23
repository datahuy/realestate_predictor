# Bất động sản Crawler và Dự đoán ứng dụng

## Mục đích
Thư mục code này chứa các thành phần chính để thu thập dữ liệu từ các trang web bất động sản, xây dựng mô hình dự đoán, và tạo một ứng dụng giao diện người dùng (GUI) để demo kết quả.

## Các File Chính

1. **crawl_bds.py**: 
   - File này chứa mã nguồn để thu thập dữ liệu từ các trang web bất động sản. Có thể có các hàm để crawl thông tin như giá, diện tích, vị trí, v.v.

2. **model_bds.py**:
   - File này chứa mã nguồn để xây dựng mô hình dự đoán. Có thể sử dụng các thuật toán máy học hoặc học sâu để dự đoán giá bất động sản dựa trên dữ liệu thu thập được.

3. **app_prediction.py**:
   - File này là ứng dụng chính có giao diện người dùng sử dụng thư viện Streamlit. Cho phép người dùng nhập dữ liệu và xem dự đoán của mô hình thông qua giao diện đơn giản.

## Cách Sử Dụng

1. **Thu thập Dữ liệu (crawl_bds.py)**:
   - Chắc chắn đã cài đặt các thư viện cần thiết.
   - Chạy `crawl_bds.py` để bắt đầu quá trình thu thập dữ liệu từ các trang web bất động sản.

2. **Xây Dựng Mô Hình (model_bds.py)**:
   - Chắc chắn đã cài đặt các thư viện học máy và học sâu.
   - Chạy `model_bds.py` để xây dựng mô hình dự đoán dựa trên dữ liệu đã thu thập.

3. **Chạy Ứng Dụng Giao Diện (app_prediction.py)**:
   - Chắc chắn đã cài đặt Streamlit (`pip install streamlit`).
   - Chạy `app_prediction.py` và mở trình duyệt tại địa chỉ được hiển thị để sử dụng ứng dụng giao diện.

## Yêu Cầu Hệ Thống
- Python 3.x
- Các thư viện được liệt kê trong `requirements.txt`

## Lưu Ý
- Để đảm bảo hiệu suất tốt, cần kiểm tra và cập nhật định dạng dữ liệu đầu vào cho mô hình và ứng dụng giao diện.


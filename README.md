# CS336.J21-Music-Search-Engine
Xây dựng 1 search engine đơn giản dựa trên mô hình BOW bằng python3

Dữ liệu được crawl về từ BXH 100 bài hát của trang nhaccuatui.com

Code editor sử dụng cho đồ án này là Visual studio Code

Các phương thức crawl dữ liệu trình bày ở file crawl.py

Các phương thức xây dựng, xử lí dữ liệu trình bày ở file indexing.py

Các phương thức xây dựng GUI, truy vấn, xếp hạng kết quả trình bày ở file main.py

---------------------------------------------------------------------------------------------------------

Để chạy được chương trình cần cài đặt các packpage sau bằng cách mở cmd, nhập lần lượt các dòng lệnh dưới đây:

pip install requests

pip install beautifulsoup4

pip install selenium

pip install underthesea

pip install PyQt5


---------Các bước sử dụng---------

B1: crawl dữ liệu: (Nếu xài dữ liệu đã crawl sẵn thì bỏ qua bước này, còn không phải update lại file crawl.py vì trang web được crawl thay đổi theo thời gian dẫn đến cú pháp crawl cũ không còn chính xác)
mở cmd nhập lệnh sau: python crawl.py 

khi hoàn thành vào thư mục crawl và copy thư mục data ra ngoài.


B2: Build Data, inverted_index:

mở cmd trong thư mục nhập lệnh sau: python indexing.py
(nếu sử dụng data có sẵn thì bỏ qua bước này)

B3: truy vấn

mở cmd trong thư mục nhập lệnh sau: python main.py

sau đó nhập câu truy vấn

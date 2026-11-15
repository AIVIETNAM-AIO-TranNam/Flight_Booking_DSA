# Tài liệu Kiến trúc & Cấu trúc Dự án: Hệ thống Đặt vé Máy bay (DSA)

Tài liệu này tổng hợp cấu trúc thư mục, chức năng của các khối xử lý (Modules) và vai trò của từng hàm trong hệ thống đặt vé máy bay chạy trên Terminal bằng Python thuần túy.

---

## 1. Cấu trúc Thư mục Dự án (`Folder Structure`)

Dự án được tổ chức theo kiến trúc mô-đun hóa (Modular Architecture), tách biệt phần lưu trữ dữ liệu, cấu trúc dữ liệu lõi và các nghiệp vụ xử lý:

```text
FlightBookingDSA/
│
├── data/                      # Thư mục lưu trữ dữ liệu dạng văn bản (Database giả lập)
│   ├── users.txt              # Lưu tài khoản người dùng (username, password, role)
│   ├── flights.txt            # Lưu danh sách chuyến bay và số ghế trống
│   └── bookings.txt           # Lưu lịch sử giao dịch và mã vé đã xuất
│
├── src/                       # Thư mục chứa mã nguồn chính của hệ thống
│   ├── __init__.py            # Đánh dấu thư mục src là một Python package
│   ├── models.py              # Cài đặt từ đầu các cấu trúc dữ liệu (DSA Core)
│   ├── user_manager.py        # Khối 1: Quản lý người dùng & xác thực
│   ├── flight_manager.py      # Khối 2: Quản lý chuyến bay, tìm kiếm & sắp xếp
│   ├── booking_engine.py      # Khối 3: Xử lý hàng đợi đặt vé & danh sách chờ ưu tiên
│   ├── payment_module.py      # Khối 4: Thanh toán giả lập & sinh mã vé điện tử
│   └── history_module.py      # Khối 5: Quản lý lịch sử đặt vé & tra cứu
│
├── main.py                    # Giao diện dòng lệnh (Terminal CLI) điều phối toàn hệ thống
└── pipeline.drawio # Sơ đồ luồng xử lý trực quan
```

### Giải thích chi tiết từng tệp tin:
* **`data/*.txt`**: Đóng vai trò lưu trữ bền vững (Persistence). Khi khởi động chương trình, dữ liệu từ các file này được nạp vào các cấu trúc dữ liệu trong bộ nhớ RAM; khi có thay đổi, hệ thống ghi nối tiếp vào file.
* **`src/models.py`**: Tệp quan trọng nhất về mặt thuật toán. Chứa các class tự cài đặt hoàn toàn không dùng thư viện ngoài: `Node`, `SinglyLinkedList`, `HashTable`, `Queue`, và `PriorityQueue` (dựa trên Binary Heap).
* **`main.py`**: Điểm khởi chạy (`Entry point`) của ứng dụng. Hiển thị menu trên Terminal, nhận thao tác nhập từ bàn phím và gọi các hàm tương ứng từ 5 khối chức năng trong thư mục `src/`.

---

## 2. Chi tiết các Khối chức năng & Các hàm cốt lõi

Hệ thống được chia làm 5 khối chức năng độc lập nhưng liên kết chặt chẽ theo luồng nghiệp vụ:

### Khối 1: `UserManagerModule` (`src/user_manager.py`)
* **Tác dụng chung:** Quản lý thông tin tài khoản, đăng ký, đăng nhập và phân quyền người dùng. Sử dụng `HashTable` để tối ưu tốc độ tra cứu tài khoản về mức $O(1)$.
* **Các hàm chính:**
  * `load_users_from_file(filepath)`: Đọc dữ liệu từ `users.txt` và nạp vào `HashTable`.
  * `register_user(username, password, role)`: Kiểm tra trùng lặp tên đăng nhập; nếu hợp lệ thì thêm vào `HashTable` và lưu vào file.
  * `authenticate_user(username, password)`: Đối chiếu thông tin đăng nhập, nếu khớp sẽ lưu trạng thái phiên làm việc hiện tại (`current_user`).

### Khối 2: `FlightManagementModule` (`src/flight_manager.py`)
* **Tác dụng chung:** Lưu trữ kho chuyến bay bằng `SinglyLinkedList`, cung cấp tính năng tra cứu và tự cài đặt thuật toán sắp xếp `MergeSort`.
* **Các hàm chính:**
  * `load_flights_from_file(filepath)`: Nạp danh sách chuyến bay từ `flights.txt` vào danh sách liên kết đơn.
  * `add_flight(...)`: Tạo một đối tượng chuyến bay mới, thêm vào `SinglyLinkedList` và ghi xuống file (dành cho Admin).
  * `search_flights(origin, destination, date)`: Duyệt qua danh sách liên kết để lọc ra các chuyến bay khớp với điểm đi, điểm đến và ngày bay.
  * `sort_flights_by_price(flights)`: Chia nhỏ danh sách chuyến bay theo chiến lược Chia để trị (Divide and Conquer) để sắp xếp giá vé tăng dần.
  * `_merge_price(left, right)`: Hàm bổ trợ gộp hai danh sách con đã sắp xếp thành một danh sách hoàn chỉnh.

### Khối 3: `BookingEngineModule` (`src/booking_engine.py`)
* **Tác dụng chung:** Điều phối quy trình chọn ghế, xử lý đồng thời các yêu cầu đặt vé theo cơ chế FIFO (`Queue`) và quản lý danh sách chờ cho khách ưu tiên (`PriorityQueue`).
* **Các hàm chính:**
  * `select_seat(flight_code, seat_number, username)`: Tạo một yêu cầu đặt vé ở trạng thái chờ (`Pending`) và đẩy vào hàng đợi `Queue`.
  * `add_to_waitlist(username, flight_code, priority_score)`: Đưa hành khách vào danh sách chờ khi hết vé, sắp xếp thứ tự phục vụ dựa trên điểm ưu tiên (hạng thương gia/VIP) thông qua cấu trúc Max-Heap.
  * `process_booking_queue()`: Lấy tuần tự từng yêu cầu ra khỏi `Queue` để xác nhận giữ chỗ (`Confirmed`) trước khi chuyển sang bước thanh toán.

### Khối 4: `PaymentAndTicketModule` (`src/payment_module.py`)
* **Tác dụng chung:** Xử lý giao dịch thanh toán giả lập và cấp phát mã định danh vé điện tử duy nhất (tương tự mã PNR trong thực tế).
* **Các hàm chính:**
  * `process_payment(booking_info, amount)`: Kiểm tra tính hợp lệ của số tiền thanh toán; nếu thành công sẽ kích hoạt hàm tạo mã vé.
  * `generate_ticket_code()`: Tự sinh chuỗi mã vé ngẫu nhiên gồm 6 ký tự chữ và số (ví dụ: `TKT-A9X20B`) mà không cần dùng thư viện `uuid`.

### Khối 5: `HistoryAndManagementModule` (`src/history_module.py`)
* **Tác dụng chung:** Lưu vết toàn bộ lịch sử đặt vé của hệ thống vào `SinglyLinkedList` và hỗ trợ người dùng xem lại các vé đã đặt.
* **Các hàm chính:**
  * `add_booking_to_history(username, ticket_info)`: Ghi nhận thông tin vé vừa thanh toán thành công vào danh sách liên kết lịch sử và lưu bền vững vào `bookings.txt`.
  * `view_user_bookings(username)`: Duyệt qua `SinglyLinkedList` lịch sử để trích xuất và hiển thị toàn bộ vé thuộc về tài khoản đang đăng nhập.
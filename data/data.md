# FLIGHTS.CSV
## 1, flight_id: "airline_code" + "flight_code"
example: VN123: Chuyến bay mã 123 của Vietnam Airlines (Ta giải sử flight_id là duy nhất, key của từng chuyến bay)
## 2, origin
cần tạo 1 list ánh xạ tên viết tắt với tên đầy đủ của origin và destination
## 3, destination
## 4, depart_time:
Format: "YYYY-MM-DD HH:MM" (Theo chuẩn ISO)
<!-- 
from dataclasses import dataclass
from datetime import datetime 
-->
## 5, arrive_time:
Tương tự depart_time
## 6, price:
## 7, available_seats:
## 8, total_seats:

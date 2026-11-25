# 15/11:
    Nam: đã tạo baseline cấu trúc file/thư mục dự án và một số hàm cơ bản
# 18/11:
    Nam: đề xuất ý tưởng giải quyết tình huống đổi chuyển bay với các tình huống sau:
        - 1, Do khách hành muốn đổi chuyến:
            + 1.1, Nếu yêu cầu đổi chuyến bay trước thời gian quy định (Ví dụ: Tối thiểu 12h trước thời gian chuyến bay khởi hành (cần viết hàm tính khoảng thời gian giữa 2 thời điểm (giờ - ngày - tháng - năm))):
                ++Mất phí đổi cố định (Change Fee): Tùy thuộc vào hạng vé bạn đã mua. (có 4 loại vé: promotional < economy < flexible < business)
                ++Bù thêm phần chênh lệch giá vé (Fare Difference):
	                • Nếu chuyến bay mới có giá cao hơn vé cũ, phải trả thêm phần tiền chênh lệch này.
	                • Nếu chuyến bay mới rẻ hơn, hãng hàng không sẽ không hoàn lại số tiền thừa cho bạn.
            + 1.2, Yêu cầu đổi chuyến trong khoảng thời gian cận giờ bay (Ví dụ: Dưới 12 tiếng trước giờ khởi hành)
                ++Phí đổi cận giờ (Last-minute Change Fee): Thường cao hơn đáng kể (hoặc tính theo tỷ lệ phần trăm cao hơn) so với đổi trước 12h, phụ thuộc vào từng hạng vé (promotional, economy, flexible, business).
                ++Bù chênh lệch giá vé (Fare Difference): Vẫn áp dụng nguyên tắc:
                    Chuyến mới cao hơn: Khách trả thêm tiền chênh lệch.
                    Chuyến mới rẻ hơn: Không hoàn lại tiền thừa.

            + 1.3, đổi chuyến sau khi chuyến bay đã khởi hành (No-show / Đổi vé quá giờ)
                ++Hạng vé promotional & economy: Vé bị tính là No-show, không hỗ trợ đổi và mất toàn bộ giá trị vé.
                ++Hạng vé flexible & business: Cho phép đổi sang chuyến bay tiếp theo trong ngày với phí phạt No-show cố định (thường là mức phí cao nhất) + tiền chênh lệch giá vé (nếu có).
        - 2, Do hãng hàng không đổi chuyến bay vì sự cố (...):
            + Đổi sang chuyến bay mới miễn phí (chuyến bay kế tiếp) (nếu khách hàng ACCEPT)
            + Được hoàn tiền toàn bộ vé: Nếu giờ bay mới không phù hợp với kế hoạch cá nhân (REFUSE)
            + Bảo lưu giá trị vé (KEEP FOR FUTURE)
# 19/11:
    Nam: đề xuất build 1 module về quản lí và liên kết các sân bay trong nước và quốc tế (giả sử mỗi nước có 1 sân bay). Để giải quyết 1 số tình huống sau:
        - Khách hàng muốn bay nhiều chuyến nối nhau vì ko có chuyến bay trực tiếp từ sân bay A đến C nên phải từ A->B rồi B->C(quá cảnh) => liên kết hệ thống các sân bay để có thể đặt vé B->C (in advance) từ sân bay A (giảm thời gian chờ)
        - Hãng hàng không thông báo đổi địa điểm hạ cánh TRƯỚC GIỜ BAY (vì lý do thời tiết xấu, an toàn do dọa đánh bom hoặc hệ thống quản lí máy bay ở sân bay muốn đến ban đầu đang bị quá tải, ko đủ không gian cho các máy bay khác đến trong thời gian dự kiến sắp tới)
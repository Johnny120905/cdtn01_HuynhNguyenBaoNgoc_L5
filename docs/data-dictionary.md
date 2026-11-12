# DATA DICTIONARY (TỪ ĐIỂN DỮ LIỆU) — MEKONG MOBILE (LUỒNG 05)
## Hệ thống Smart CRM – Phân hệ Quản lý Kho linh kiện thay thế (`L5-WH-890`)
### Học phần: Chuyên đề tốt nghiệp 1 (CDTN01) — Track: Software Engineering (SE)
### Sinh viên: Huỳnh Nguyễn Bảo Ngọc — MSSV: 2374802010339

---

## 1. Tổng quan cơ sở dữ liệu
Hệ thống sử dụng cơ sở dữ liệu NoSQL **MongoDB 7.0**, database name: `mekong_mobile_l5`. Dữ liệu được tổ chức thành 5 collections chuẩn hóa nhằm phục vụ tối ưu các truy vấn quản lý kho, theo dõi nhật ký giao dịch bất biến và phân quyền người dùng đa chi nhánh.

---

## 2. Chi tiết cấu trúc các Collections

### 2.1. Collection `parts` (Danh mục linh kiện thay thế)
Lưu trữ thông tin định danh và đặc tính kỹ thuật của từng loại linh kiện trong hệ thống.

| Tên trường (Field) | Kiểu dữ liệu | Bắt buộc | Ràng buộc & Quy tắc nghiệp vụ | Mô tả chi tiết |
| :--- | :--- | :---: | :--- | :--- |
| `_id` | ObjectId | Có | Khóa chính tự sinh MongoDB | Định danh tài liệu nội bộ |
| `part_code` | String | Có | Duy nhất (Unique Index), Unique code | Mã định danh linh kiện (VD: `IP13-SCR-01`) |
| `name` | String | Có | Max 150 ký tự | Tên linh kiện hiển thị (VD: Màn hình OLED iPhone 13) |
| `category` | String | Có | Thuộc enum: `SCREEN`, `BATTERY`, `CAMERA`, `SPEAKER`, `BACK_GLASS`, `CHARGING_PORT` | Danh mục chủng loại linh kiện |
| `model` | String | Có | Chuỗi không rỗng | Tên dòng thiết bị áp dụng (VD: iPhone 13 Pro Max) |
| `cost_price` | Float | Có | $> 0$ | Giá vốn nhập kho (VNĐ) |
| `selling_price`| Float | Có | $\ge cost\_price$ | Đơn giá xuất bán / thay thế niêm yết (VNĐ) |
| `compatible_models` | Array[String] | Không | Danh sách chuỗi | Các dòng máy tương thích |
| `status` | String | Có | Enum: `ACTIVE`, `INACTIVE` | Trạng thái kinh doanh linh kiện |
| `created_at` | DateTime | Có | UTC Timestamp | Thời điểm tạo bản ghi |
| `updated_at` | DateTime | Có | UTC Timestamp | Thời điểm cập nhật cuối |

---

### 2.2. Collection `inventory` / `part_stock` (Quản lý tồn kho chi nhánh)
Theo dõi số lượng tồn kho khả dụng thời gian thực tại từng chi nhánh trung tâm bảo hành, tích hợp cơ chế khóa lạc quan (Optimistic Concurrency Control).

| Tên trường (Field) | Kiểu dữ liệu | Bắt buộc | Ràng buộc & Quy tắc nghiệp vụ | Mô tả chi tiết |
| :--- | :--- | :---: | :--- | :--- |
| `_id` | ObjectId | Có | Khóa chính tự sinh MongoDB | Định danh bản ghi |
| `center_id` | String | Có | Khóa ngoại logic -> `service_center` | Mã trung tâm dịch vụ (VD: `L5-WH-890`) |
| `part_code` | String | Có | Khóa ngoại logic -> `parts.part_code` | Mã linh kiện quản lý tồn kho |
| `quantity` | Integer | Có | $\ge 0$ (BR-01 Chống tồn âm) | Số lượng tồn kho vật lý khả dụng hiện tại |
| `min_threshold` | Integer | Có | $\ge 0$, mặc định: 5 | Ngưỡng an toàn tối thiểu quy định cho linh kiện |
| `status_flag` | String | Có | Enum: `NORMAL`, `WARNING` (BR-05) | Cờ cảnh báo tự động: `WARNING` khi $quantity \le min\_threshold$ |
| `version` | Integer | Có | $\ge 1$, tăng 1 mỗi lần cập nhật | Phiên bản dùng cho Optimistic Concurrency Control (HTTP 409) |
| `last_updated` | DateTime | Có | UTC Timestamp | Thời điểm biến động kho gần nhất |

> **Index:** `Compound Index: (center_id, part_code)` duy nhất.

---

### 2.3. Collection `transactions` / `part_transaction` (Sổ cái giao dịch kho)
Lưu vết toàn bộ lịch sử xuất, nhập, hoàn trả linh kiện. Được thiết kế theo nguyên lý bất biến (**Insert-Only Ledger**), không cho phép sửa hoặc xóa lịch sử.

| Tên trường (Field) | Kiểu dữ liệu | Bắt buộc | Ràng buộc & Quy tắc nghiệp vụ | Mô tả chi tiết |
| :--- | :--- | :---: | :--- | :--- |
| `_id` | ObjectId | Có | Khóa chính tự sinh MongoDB | Định danh tài liệu giao dịch |
| `transaction_id`| String | Có | Unique UUID | Mã định danh duy nhất của giao dịch kho |
| `center_id` | String | Có | Mã chi nhánh thực hiện | Chi nhánh diễn ra giao dịch |
| `part_code` | String | Có | Khóa ngoại -> `parts.part_code` | Linh kiện giao dịch |
| `type` | String | Có | Enum: `IN` (Nhập), `OUT` (Xuất), `RETURN` (Hoàn kho) | Loại nghiệp vụ giao dịch |
| `quantity` | Integer | Có | $> 0$ | Số lượng linh kiện xuất/nhập |
| `ticket_id` | String | Tùy loại | Bắt buộc khi `OUT` hoặc `RETURN` (BR-02) | Mã phiếu tiếp nhận bảo hành / sửa chữa liên kết |
| `staff_email` | String | Có | Khóa ngoại -> `users.email` | Nhân sự chịu trách nhiệm thực hiện thao tác |
| `notes` | String | Không | Max 500 ký tự | Ghi chú lý do xuất nhập |
| `timestamp` | DateTime | Có | UTC Timestamp hệ thống | Thời điểm xác nhận giao dịch |

---

### 2.4. Collection `users` (Tài khoản & Phân quyền RBAC)
Lưu trữ thông tin nhân sự và cơ chế bảo mật xác thực phân quyền 3 vai trò.

| Tên trường (Field) | Kiểu dữ liệu | Bắt buộc | Ràng buộc & Quy tắc nghiệp vụ | Mô tả chi tiết |
| :--- | :--- | :---: | :--- | :--- |
| `_id` | ObjectId | Có | Khóa chính tự sinh MongoDB | Định danh tài khoản |
| `email` | String | Có | Duy nhất (Unique Index), Định dạng email chuẩn | Tên đăng nhập và kênh nhận diện nhân sự |
| `full_name` | String | Có | Max 100 ký tự | Họ tên đầy đủ nhân viên |
| `password_hash`| String | Có | Chuỗi băm Bcrypt 12 rounds, cấm Plaintext | Mật khẩu băm an toàn theo tiêu chuẩn OWASP |
| `role` | String | Có | Enum: `MANAGER`, `MATERIAL_STAFF`, `TECH_STAFF` | Vai trò tác nghiệp trong hệ thống (RBAC) |
| `center_id` | String | Có | Mã trung tâm dịch vụ | Chi nhánh công tác của nhân sự |
| `status` | String | Có | Enum: `ACTIVE`, `OFF_SHIFT`, `TERMINATED` | Trạng thái công tác (khóa 403 nếu `TERMINATED`) |
| `created_at` | DateTime | Có | UTC Timestamp | Thời điểm tạo tài khoản |

---

### 2.5. Collection `warranty_tickets` / `ticket` (Phiếu bảo hành dịch vụ)
Liên kết giữa quy trình bảo hành của Kỹ thuật viên và việc xuất linh kiện thay thế.

| Tên trường (Field) | Kiểu dữ liệu | Bắt buộc | Ràng buộc & Quy tắc nghiệp vụ | Mô tả chi tiết |
| :--- | :--- | :---: | :--- | :--- |
| `_id` | ObjectId | Có | Khóa chính tự sinh MongoDB | Định danh phiếu bảo hành |
| `ticket_id` | String | Có | Duy nhất (Unique Index), VD: `TK-2026-001` | Mã số phiếu bảo hành tiếp nhận sửa chữa |
| `customer_name`| String | Có | Max 100 ký tự | Tên khách hàng mang máy đến bảo hành |
| `device_model` | String | Có | Chuỗi không rỗng | Dòng máy tiếp nhận sửa chữa |
| `fault_description`| String | Có | Mô tả lỗi | Hiện trạng hỏng hóc cần thay thế linh kiện |
| `status` | String | Có | Enum: `OPEN`, `IN_PROGRESS`, `COMPLETED`, `CANCELLED` | Chỉ cho phép xuất linh kiện khi status là `OPEN`/`IN_PROGRESS` |
| `created_at` | DateTime | Có | UTC Timestamp | Thời điểm mở phiếu |


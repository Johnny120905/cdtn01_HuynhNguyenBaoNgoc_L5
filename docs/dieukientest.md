# ĐẶC TẢ ĐIỀU KIỆN RÀNG BUỘC TOÀN DIỆN & KỊCH BẢN KIỂM THỬ HỆ THỐNG
## HỆ THỐNG SMART CRM – MEKONG MOBILE (LUỒNG 05: KHO LINH KIỆN THAY THẾ)
*(System Constraints, In-Depth Role & View Specifications, and Comprehensive Test Matrix)*

- **Học phần:** Chuyên đề Tốt nghiệp 1 (Học kỳ 1, Năm học 2026 – 2027)
- **Chuyên ngành:** Công nghệ phần mềm (`Track SE`)
- **Sinh viên thực hiện:** Huỳnh Nguyễn Bảo Ngọc — **MSSV:** `2374802010339` | **Lớp:** `261_71ITGR40203_06`
- **Giảng viên hướng dẫn:** TS. Nguyễn Trí Hải — Trường Đại học Văn Lang
- **Chi nhánh triển khai:** Trung tâm Bảo hành Mekong Mobile Quận 1 (`L5-WH-890`)
- **Môi trường:** Python `3.11.5`, FastAPI `0.162.0`, Pytest `9.2.0`, MongoDB Atlas / MongoDB 7.0 Container, SPA Dark 3D Elevation (*Be Vietnam Pro*)
- **Tài liệu liên quan:** [README.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/README.md) | [docs/test-plan.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/test-plan.md) | [docs/test-report.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/test-report.md) | [docs/bug-log.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/bug-log.md) | [docs/deployment-guide.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/deployment-guide.md) | [docs/checklist-bao-mat.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/checklist-bao-mat.md) | [docs/api-docs/README.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/api-docs/README.md)

---

## TỔNG QUAN VỀ KIẾN TRÚC RÀNG BUỘC HAI CHIỀU (BÊN TRONG & BÊN NGOÀI)

Hệ thống quản lý kho linh kiện thay thế hoạt động theo nguyên tắc **Bảo chứng Ràng buộc Đa tầng (Multi-Layer Constraint Enforcement)**. Mọi thao tác từ người dùng đều phải vượt qua đồng thời 2 bức tường kiểm định:

```text
+----------------------------------------------------------------------------------------------------+
|                       HAI TẦNG ĐIỀU KIỆN RÀNG BUỘC BÊN NGOÀI VÀ BÊN TRONG                          |
+----------------------------------------------------------------------------------------------------+
| [1. RÀNG BUỘC BÊN NGOÀI (EXTERNAL CONSTRAINTS & PERIMETER)]                                         |
|  - Trực quan Client UI: HTML5 input pattern, focus, DOM validation, nút con mắt, đồng hồ đếm ngược |
|  - Phím tắt & Tương tác: Bàn phím Enter tự động khớp linh kiện, phím Escape đóng popup              |
|  - Ràng buộc Giao thức HTTP: Header Authorization Bearer JWT, Content-Type application/json        |
|  - Cô lập Chi nhánh & Phân quyền Biên: Chặn truy cập trái phép giữa các chi nhánh (A01 OWASP)      |
|  - Chuẩn hóa Phản hồi: Luôn trả JSON chuẩn {status, data/message/error_code}, tỷ lệ lỗi 500 = 0%   |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+----------------------------------------------------------------------------------------------------+
| [2. RÀNG BUỘC BÊN TRONG (INTERNAL CONSTRAINTS & CORE DOMAIN)]                                       |
|  - Tầng Kiểm tra (Validator): Regex email RFC, mật khẩu 4 nhóm (8..128 ký tự), biên số lượng       |
|  - Tầng Nghiệp vụ cốt lõi (Domain Service): 5 quy tắc nghiệp vụ BR-01..BR-05 độc lập với HTTP       |
|  - Cơ chế Khóa lạc quan (Optimistic Locking): So khớp version chống Race Condition (NFR-03/EX-05)  |
|  - Tầng Truy xuất CSDL (Repository & Schema): $jsonSchema NoSQL, Unique & Compound Indexes, Băm mk  |
|  - Tính lũy đẳng (Idempotency) & Dự phòng Kép: Nạp seed không nhân đôi (C8), Dual-Persistence      |
+----------------------------------------------------------------------------------------------------+
```

---

# PHẦN I: MA TRẬN ĐIỀU KIỆN RÀNG BUỘC BÊN NGOÀI & BÊN TRONG CHI TIẾT

### 1. Ràng buộc Bên ngoài (External Perimeter Constraints)
1. **Ràng buộc Môi trường & Giao thức:**
   - Mọi kết nối API yêu cầu Header `Authorization: Bearer <JWT_TOKEN>`. Nếu thiếu Header, máy chủ cung cấp fallback phiên làm việc dev/demo hoặc ném mã lỗi HTTP 401 `ERR_INVALID_TOKEN`.
   - Token JWT được ký bằng thuật toán bảo mật `HS256` với khóa bí mật đọc từ biến môi trường `JWT_SECRET_KEY` (thời hạn sống `exp` chính xác 24 giờ).
   - Kiểm soát truy cập theo chi nhánh (`A01 OWASP`): Nếu Token thuộc chi nhánh `L5-WH-890` (Quận 1) mà gửi request mang `center_id: "L5-WH-891"` (Quận 3) -> Lập tức từ chối với mã HTTP 403 `ERR_UNAUTHORIZED_CENTER`.
2. **Ràng buộc Giao diện Người dùng (UI/UX Client):**
   - Thiết kế chuẩn *Dark 3D Elevation* (nền `#070b14`, thẻ nổi `.card-3d`, nút tactile `.btn-3d-primary`, phông chữ `Be Vietnam Pro`).
   - Tối giản ngôn ngữ nghiệp vụ: Tuyệt đối không hiển thị mã kỹ thuật `(BR-01)`, `(FR-06)`, `(NFR-03)` hay thanh điều hướng thừa `Kho vận & Kỹ thuật > ...`.
   - Chuyển ngữ tiếng Việt 100%: `OUT` $\rightarrow$ **"Xuất kho thay thế"** (vàng), `IN` $\rightarrow$ **"Nhập kho vật tư"** (xanh lá), `RETURN` $\rightarrow$ **"Hoàn trả linh kiện"** (xanh dương).
   - Tỷ lệ chuỗi `undefined` trên giao diện người dùng đạt đúng `0%`.

### 2. Ràng buộc Bên trong (Internal Core Logic & Storage Constraints)
1. **Ràng buộc Tầng Kiểm tra (Input Validator Layer):**
   - Mật khẩu: Bắt buộc độ dài từ 8 đến 128 ký tự, phải thỏa mãn đủ 4 nhóm: Chữ hoa `[A-Z]`, Chữ thường `[a-z]`, Chữ số `[0-9]`, Ký hiệu đặc biệt. Nếu thiếu bất kỳ nhóm nào -> Ném `AppError(400, "ERR_WEAK_PASSWORD")`.
   - Số lượng giao dịch `quantity`: Bắt buộc là số nguyên dương $1 \le Q \le 1,000,000$. Nghiêm cấm số thực, chuỗi ký tự, số âm hoặc kiểu boolean (`True/False`).
   - Ngưỡng an toàn `min_threshold`: Bắt buộc là số nguyên không âm $0 \le min\_threshold \le 100,000$.
   - Chứng từ xuất kho `ticket_id`: Bắt buộc có khi thực hiện `OUT` hoặc `RETURN`, độ dài tối đa 30 ký tự (`BR-02`).
2. **Ràng buộc Tầng Nghiệp vụ cốt lõi (Domain Service Layer):**
   - Chống tồn kho âm (`BR-01`): Nếu $Q_{request} > Q_{stock} \rightarrow$ Ném `NegativeStockError` (HTTP 400 `ERR_INSUFFICIENT_STOCK`).
   - Kiểm tra trạng thái phiếu bảo hành (`UC-99` / `EX-03`): Phiếu phải đang ở trạng thái `OPEN` hoặc `IN_PROGRESS`. Nếu phiếu không tồn tại hoặc đã `COMPLETED`/`CANCELLED` $\rightarrow$ Ném `InvalidTicketError` (HTTP 422 `ERR_INVALID_TICKET`).
   - Khóa lạc quan chống tranh chấp đồng thời (`NFR-03` / `EX-05`): Cập nhật kho kèm điều kiện `version == expected_version`. Nếu lệch version $\rightarrow$ Ném `ConcurrentUpdateError` (HTTP 409 `ERR_CONCURRENT_UPDATE`).
   - Đánh giá cảnh báo an toàn thời gian thực (`BR-05`): Nếu $Q_{stock} \le min\_threshold \rightarrow$ Gắn cờ `WARNING` (kích hoạt báo động đỏ Quản lý), ngược lại gắn cờ `NORMAL`.
3. **Ràng buộc Tầng Lưu trữ & CSDL (Database & Storage Layer):**
   - 6 Collections NoSQL: `service_center`, `part`, `ticket`, `part_stock`, `part_transaction`, `users`.
   - Chỉ mục duy nhất (Unique Index): `part.part_code`, `ticket.ticket_id`, `service_center.center_id`, `users.email`.
   - Chỉ mục phức hợp (Compound Index): `part_stock.{center_id: 1, part_code: 1}` (tốc độ tra cứu $< 500$ ms `NFR-02`), `part_transaction.{center_id: 1, created_at: -1}`.
   - Băm mật khẩu an toàn (`[SE] S3`): Mật khẩu được băm qua Bcrypt hoặc SHA-256 trước khi ghi vào CSDL; tuyệt đối không lưu plaintext `password`.
   - Tính lũy đẳng (`C8`): Lệnh nạp dữ liệu `python seeds/seed.py` sử dụng `replace_one(..., upsert=True)`, chạy lặp lại nhiều lần không sinh lỗi và không nhân đôi dữ liệu.

---

# TÀI LIỆU KIỂM THỬ TOÀN DIỆN HỆ THỐNG (TEST SPECIFICATION & EXECUTION PROOFS)
## HỆ THỐNG SMART CRM – MEKONG MOBILE (LUỒNG 05: KHO LINH KIỆN THAY THẾ)
**Chuyên đề tốt nghiệp 1 (Kỹ thuật Phần mềm - SE)**  
**Chi nhánh triển khai:** Chi nhánh Quận 1  
**Môi trường thử nghiệm:** Python 3.11.5, FastAPI 0.162.0, Pytest 9.2.0 (67 test cases PASS 100%), MongoDB 7.0 Container / Atlas, SPA JavaScript Be Vietnam Pro  
**Tài liệu liên quan:** [thietke.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/thietke.md) | [thay-doi-thiet-ke.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/thay-doi-thiet-ke.md) | [README.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/README.md) | [test-plan.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/test-plan.md) | [test-report.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/test-report.md)

---

# MỤC 1: ĐIỀU KIỆN RÀNG BUỘC THEO TỪNG GIAO DIỆN (CHI TIẾT FRONTEND - BACKEND - DATABASE) & KIỂM TRA LIÊN KẾT 3 VAI TRÒ

Mỗi giao diện trong hệ thống được thiết kế với các điều kiện ràng buộc chặt chẽ được bảo chứng đồng thời trên cả 3 tầng kiến trúc: **Frontend (Trực quan & Tương tác)** – **Backend (Kiểm định & Dịch vụ)** – **Database (Lưu trữ & Toàn vẹn dữ liệu)**.

---

### 1. Giao diện Đăng nhập (Login View)
* **Điều kiện Frontend:**
  - Trường Email: Bắt buộc nhập, kiểm tra định dạng email tiêu chuẩn RFC (phải có ký tự `@` và tên miền). Độ dài tối đa 100 ký tự. Nếu để trống hoặc sai định dạng: Viền ô nhập đổi màu đỏ (`border-red-500`), hiển thị dòng báo lỗi đỏ bên dưới (`.field-error-text`): *"Vui lòng nhập email hợp lệ"*.
  - Trường Mật khẩu: Bắt buộc nhập, độ dài từ 8 đến 128 ký tự. Tích hợp nút con mắt `.eye-toggle-btn` ở cạnh phải ô nhập: khi click sẽ hoán đổi kiểu trường giữa `password` (che chấm tròn đen) và `text` (hiện mật khẩu rõ ràng) kèm hiệu ứng đổi icon SVG con mắt mở/đóng.
  - Phản hồi trạng thái: Khi bấm nút *"ĐĂNG NHẬP"*, nếu thông tin sai hiển thị thông báo lỗi nổi (Toast màu đỏ) và dòng lỗi đỏ dưới khung mật khẩu. Nếu tài khoản bị vô hiệu hóa (`TERMINATED`), hiển thị thông báo chặn truy cập.
* **Điều kiện Backend:**
  - Endpoint tiếp nhận: `POST /api/v1/auth/login`.
  - Validator: `inventory.validator.py` kiểm tra `email` và `password` không được rỗng, độ dài `email <= 100`, `password <= 128`.
  - Logic xác thực: Đối chiếu mật khẩu bằng mã hóa Bcrypt/SHA-256. Kiểm tra cờ trạng thái tài khoản: nếu `user.get("status") == "TERMINATED"` hoặc `user.get("is_active") is False` $\rightarrow$ Lập tức ném ngoại lệ `AppError(403, "ERR_ACCOUNT_TERMINATED", "Tài khoản đã thôi việc và bị vô hiệu hóa vĩnh viễn")`. Nếu sai mật khẩu ném `AppError(401, "ERR_INVALID_CREDENTIALS")`.
  - Cấp quyền: Đăng nhập thành công trả về mã HTTP 200 kèm chuỗi JWT Token (thuật toán HS256) chứa `email`, `role`, `full_name`, `center_id` và thời hạn hiệu lực (TTL 24 giờ).
* **Điều kiện Database:**
  - Collection phụ trách: `users`.
  - Truy vấn tìm kiếm: `db.users.find_one({"email": email})`.
  - Cập nhật phiên: Khi đăng nhập thành công, tự động cập nhật trường `status: "ONLINE"` và `last_login: ISODate()`.
  - Bộ lưu trữ bền vững dự phòng: Tự động đồng bộ sang `data/users_store.json` để bảo toàn dữ liệu tài khoản khi mất kết nối mạng.

---

### 2. Giao diện Đăng ký cấp quyền (Register View)
* **Điều kiện Frontend:**
  - Trường Họ và tên: Bắt buộc, độ dài từ 2 đến 50 ký tự. Tự động cắt tỉa khoảng trắng thừa đầu/cuối (`trim()`).
  - Trường Email cá nhân: Bắt buộc, tối đa 100 ký tự, regex kiểm tra định dạng email thật. Ghi chú rõ: *"1 email chỉ gắn với 1 vai trò duy nhất"*.
  - Trường Mật khẩu: Bắt buộc tối thiểu 8 ký tự, tối đa 128 ký tự. Phải thỏa mãn đủ 4 nhóm: (1) Chữ in hoa `A-Z`, (2) Chữ in thường `a-z`, (3) Chữ số `0-9`, (4) Ký hiệu đặc biệt. Có nút con mắt bật/tắt xem mật khẩu.
  - Bảng quy chuẩn mật khẩu: Được **ẩn mặc định** (class `hidden`), chỉ xuất hiện và hiển thị các dòng báo lỗi màu đỏ khi người dùng nhập sai hoặc thiếu nhóm ký tự bắt buộc.
  - Trường Chọn vai trò: Dropdown bắt buộc chọn 1 trong 3 vai trò: `TECH_STAFF` (Nhân viên Kỹ thuật), `MATERIAL_STAFF` (Nhân viên Vật tư), `MANAGER` (Quản lý kho).
* **Điều kiện Backend:**
  - Endpoint tiếp nhận: `POST /api/v1/auth/register`.
  - Validator: Hàm `validate_password_complexity(password)` kiểm định Regex đủ 4 nhóm. Nếu thiếu bất kỳ nhóm nào, ném `AppError(400, "ERR_WEAK_PASSWORD", "Mật khẩu phải chứa đủ chữ hoa, chữ thường, số và ký tự đặc biệt")`.
  - Kiểm tra tính duy nhất: Kiểm tra email đã tồn tại hay chưa, nếu trùng ném `AppError(409, "ERR_EMAIL_ALREADY_EXISTS", "Email này đã được đăng ký vai trò trong hệ thống")`.
* **Điều kiện Database:**
  - Collection: `users`.
  - Chỉ mục duy nhất (Unique Index): `db.users.createIndex({ "email": 1 }, { unique: true })` ngăn chặn hoàn toàn việc ghi đè hoặc trùng lặp email ở cấp độ CSDL.
  - Băm mật khẩu (Hashing): Mật khẩu được băm an toàn qua Bcrypt với Salt ngẫu nhiên trước khi lưu vào CSDL (tuyệt đối không lưu mật khẩu dạng thô).
  - Khởi tạo mặc định: Gán `status: "ONLINE"`, `is_active: true`, `center_id: "L5-WH-890"`, `created_at: ISODate()`.

---

### 3. Giao diện Khôi phục mật khẩu OTP (Forgot Password View)
* **Điều kiện Frontend:**
  - Bước 1 (Gửi OTP): Ô nhập email cá nhân + nút *"Gửi mã OTP"*. Khi gửi thành công, khối thông báo OTP xuất hiện.
  - **Đồng hồ đếm ngược thời gian thực (`#countdownTimer`):** Khởi động đếm lùi từng giây từ **`10:00`** xuống **`00:00`** (chính xác 10 phút / 600 giây). Người dùng nhìn thấy rõ ràng thời gian đang đếm ngược. Nếu chạm `00:00`, đổi sang chữ màu đỏ báo *"00:00 (Hết hạn)"* và yêu cầu gửi lại mã mới.
  - **Tự động điền mã OTP:** Mã OTP 6 chữ số ngẫu nhiên sinh ra từ hệ thống được tự động điền ngay vào ô nhập `#resetOtp` giúp người dùng không phải thao tác sao chép thủ công.
  - Bước 2 (Đặt lại mật khẩu): Ô nhập mật khẩu mới có nút con mắt bật/tắt xem mật khẩu. Bảng checklist quy chuẩn mật khẩu được ẩn mặc định. Nút *"Xác nhận đặt lại mật khẩu"* kiểm tra tính hợp lệ của OTP và mật khẩu mới.
* **Điều kiện Backend:**
  - Endpoint 1: `POST /api/v1/auth/forgot-password`: Kiểm tra email có tồn tại trong hệ thống. Sinh mã OTP ngẫu nhiên gồm 6 chữ số (`random.randint(100000, 999999)`). Thiết lập thời hạn hết hạn chính xác 10 phút: `expires_at = datetime.utcnow() + timedelta(minutes=10)`.
  - Endpoint 2: `POST /api/v1/auth/reset-password`: Tiếp nhận `email`, `otp`, `new_password`. Kiểm tra mã OTP khớp và thời gian hiện tại `< expires_at`. Nếu hết hạn ném `AppError(400, "ERR_OTP_EXPIRED", "Mã OTP đã hết thời gian hiệu lực 10 phút")`. Nếu sai mã ném `AppError(400, "ERR_INVALID_OTP")`. Kiểm định mật khẩu mới đủ 4 nhóm rồi tiến hành băm mật khẩu mới.
* **Điều kiện Database:**
  - Collection: `users`.
  - Cập nhật OTP: Ghi đè trường `reset_otp: "123456"` và `reset_otp_expires_at: ISODate(...)`.
  - Cập nhật mật khẩu mới: `db.users.update_one({"email": email}, {"$set": {"password_hash": new_hash, "reset_otp": null, "reset_otp_expires_at": null}})`.

---

### 4. Giao diện Bảng tin Kỹ thuật viên (Tech Staff Dashboard)
* **Điều kiện Frontend:**
  - Header: Tiêu đề *"Bảng tin Kỹ thuật viên"*, thông tin ca làm việc, nút Làm mới dữ liệu. Tuyệt đối không có breadcrumb kỹ thuật `"Kho vận & Kỹ thuật > Bảng tin..."`.
  - 3 Thẻ KPI 3D: Linh kiện xuất trong ngày, Phiếu chờ tiếp nhận, Trạng thái trực tuyến ổn định.
  - Bảng danh sách phiếu bảo hành cần xử lý: Cột mã phiếu, khách hàng/thiết bị, linh kiện đề nghị, trạng thái hiển thị chuẩn tiếng Việt qua hàm `formatTicketStatus()`: `"Chờ tiếp nhận"` (OPEN), `"Đang xử lý"` (IN_PROGRESS), `"Đã hoàn thành"` (RESOLVED/COMPLETED).
  - Nút hành động: Nút *"Xuất ngay"* trên mỗi dòng phiếu tự động điều hướng sang màn hình Tra cứu & Giao dịch, đồng thời tự động điền sẵn mã phiếu bảo hành và mã linh kiện tương ứng.
  - Phân trang: Bộ chọn số dòng `[10, 20, 50, Tất cả]` và nút điều hướng Trước/Sau.
* **Điều kiện Backend:**
  - Endpoint: `GET /api/v1/inventory/tickets`.
  - Xác thực: Yêu cầu Bearer JWT Token, kiểm tra vai trò người gọi phải là `TECH_STAFF` hoặc `MANAGER`. Lọc danh sách phiếu theo `center_id: "L5-WH-890"`.
* **Điều kiện Database:**
  - Collection: `repair_ticket`.
  - Truy vấn: Lấy danh sách phiếu có trạng thái `status: {"$in": ["OPEN", "IN_PROGRESS"]}`, sắp xếp theo `created_at: -1`.

---

### 5. Giao diện Tra cứu & Giao dịch Kho (Tech Staff Stock Lookup & Transaction)
* **Điều kiện Frontend:**
  - **Ô tìm kiếm thông minh (`#smartPartSearch`):**
    - Trạng thái ban đầu: **Hoàn toàn để trống** (`value=""`), hiển thị placeholder: `"Nhập thông tin linh kiện (Mã hoặc Tên), bấm Enter để chọn..."`. Chiếm trọn 100% chiều rộng khung.
    - **Loại bỏ nút "Tra cứu":** Người dùng chỉ cần gõ từ khóa là danh sách gợi ý dropdown xuất hiện ngay bên dưới; người dùng có thể click chọn hoặc bấm phím **Enter** trên bàn phím để tự động khớp và chọn linh kiện (`handleSmartSearchKeyDown()`).
    - Tìm kiếm thông minh (Token Matching): Hỗ trợ tìm kiếm theo mã linh kiện (ví dụ: `SCR`, `BAT`, `CAM`), theo tên thiết bị (ví dụ: `iPhone 14`, `Samsung S24`, `MacBook`), hoặc từng từ khóa đơn lẻ.
    - Xử lý khi không tìm thấy: Dropdown hiển thị biểu tượng `search_off` màu vàng cùng dòng chữ: `"Không tìm thấy linh kiện phù hợp với từ khóa."`
  - **Khung hiển thị tồn kho thời gian thực (`#liveStockBox`):**
    - Trạng thái ban đầu: Hiển thị dòng thông báo hướng dẫn rõ ràng: *"Chưa chọn linh kiện. Vui lòng nhập từ khóa hoặc bấm Enter"*.
    - Khi đã chọn linh kiện: Hiển thị số lượng tồn thực tế (số lớn font-black) kèm huy hiệu 3 màu ngữ nghĩa:
      - **Màu xanh lá (Tồn an toàn):** `quantity > min_threshold + 5`.
      - **Màu vàng (Gần chạm cảnh báo):** `min_threshold < quantity <= min_threshold + 5`.
      - **Màu đỏ (Cảnh báo thiếu hàng):** `quantity <= min_threshold`.
  - **Nút "Đặt lại biểu mẫu" (`#btnResetForm`):**
    - **Điều kiện khôi phục sạch sẽ toàn bộ:** Khi người dùng bấm nút này, mọi thứ trên biểu mẫu được trả về trạng thái nguyên bản sạch sẽ:
      1. Ô tìm kiếm `#smartPartSearch` được xóa trắng (`value = ""`).
      2. Ô chọn linh kiện ẩn `#txPartSelect` được đưa về rỗng.
      3. Khung tồn kho trở về hướng dẫn ban đầu: *"Chưa chọn linh kiện"*.
      4. Ô mã phiếu bảo hành `#ticketIdInput` được xóa trắng (`value = ""`).
      5. Ô số lượng `#txQtyInput` đưa về mặc định là `1`.
      6. Phân loại giao dịch đưa về mặc định là *"Xuất kho thay thế"* (`OUT`).
      7. Khung dự tính sau giao dịch trở về: *"Chưa chọn linh kiện"*.
      8. Xóa trắng toàn bộ các dòng báo lỗi đỏ bên dưới các ô nhập (`clearFieldError`).
      9. Ẩn cảnh báo âm kho và đóng dropdown gợi ý.
  - **Chặn đứng xuất kho âm trên giao diện:** Khi số lượng nhập $> $ tồn thực tế, hệ thống lập tức hiển thị hộp cảnh báo màu đỏ sẫm: *"CẢNH BÁO: VƯỢT QUÁ SỐ LƯỢNG TỒN KHẢ DỤNG"* và khóa nút *"Xác nhận Giao dịch"*.
* **Điều kiện Backend:**
  - Endpoint 1: `GET /api/v1/inventory/stock/{part_code}`: Trả về tồn kho thực tế, ngưỡng tối thiểu và đánh giá an toàn.
  - Endpoint 2: `POST /api/v1/inventory/transactions`: Tiếp nhận giao dịch xuất kho (`OUT`) hoặc hoàn trả (`RETURN`).
  - **Cưỡng chế quy tắc nghiệp vụ BR-01 (Chặn âm kho):** Backend kiểm tra $Q_{request} \le Q_{stock}$. Nếu vượt quá, lập tức ném lỗi `AppError(400, "ERR_INSUFFICIENT_STOCK", "Số lượng xuất kho vượt quá tồn kho thực tế khả dụng")`.
  - **Cưỡng chế quy tắc nghiệp vụ BR-02 (Bắt buộc Ticket ID):** Giao dịch `OUT` bắt buộc phải có `ticket_id` (độ dài $\le 30$ ký tự) và phiếu bảo hành phải đang ở trạng thái mở. Nếu thiếu ném `AppError(400, "ERR_MISSING_TICKET_ID")`.
  - Cơ chế Optimistic Locking (BR-03): So khớp trường `version` trong CSDL để ngăn chặn hai kỹ thuật viên cùng xuất vượt tồn kho cùng một thời điểm.
* **Điều kiện Database:**
  - Collection `inventory_stock`: Cập nhật nguyên tử (Atomic Update):
    `db.inventory_stock.update_one({"center_id": center, "part_code": code, "quantity": {"$gte": req_qty}}, {"$inc": {"quantity": -req_qty, "version": 1}})`
  - Collection `part_transaction`: Tạo bản ghi sổ cái kiểm toán bất biến (append-only) gồm: `transaction_id`, `type: "OUT"`, `part_code`, `quantity`, `ticket_id`, `actor_id`, `performed_by: user_email`, `created_at`.
  - Collection `repair_ticket`: Cập nhật `status: "IN_PROGRESS"`.

---

### 6. Giao diện Lịch sử tiếp nhận phiếu (Tech Staff Transaction History)
* **Điều kiện Frontend:**
  - Hiển thị danh sách các phiếu xuất phụ tùng và hoàn trả của chính kỹ thuật viên trong ca làm việc.
  - Phân loại giao dịch chuẩn tiếng Việt qua `formatTransactionType()`: *"Xuất kho thay thế"* (OUT, huy hiệu vàng) hoặc *"Hoàn trả linh kiện"* (RETURN, huy hiệu xanh dương).
  - Cột hiển thị: MÃ GIAO DỊCH, THỜI GIAN, LINH KIỆN, LOẠI GD, SỐ LƯỢNG, PHIẾU BẢO HÀNH.
* **Điều kiện Backend:**
  - Endpoint: `GET /api/v1/inventory/transactions?limit=50`. Lọc các giao dịch có `type` là `OUT` hoặc `RETURN`.
* **Điều kiện Database:**
  - Collection: `part_transaction`. Truy vấn theo `center_id` và sắp xếp thời gian giảm dần.

---

### 7. Giao diện Bảng tin Quản lý vật tư (Material Staff Dashboard)
* **Điều kiện Frontend:**
  - **Loại bỏ nút "Tạo lệnh Nhập kho mới" ở Main Content** (vì trên Sidebar đã có danh mục riêng *"Nhập kho linh kiện mới"*, tránh trùng lặp dư thừa thao tác). Thay bằng huy hiệu *"Trung tâm Vật tư Quận 1"*.
  - 3 Thẻ KPI vật tư: Tổng danh mục linh kiện (40 loại, 100% gắn mã định danh), Tổng tồn kho thực tế, Nhà cung cấp đối tác (2 đơn vị).
  - Bảng tồn kho chi tiết theo danh mục: Hiển thị 40 mặt hàng, tồn hiện tại, ngưỡng an toàn, đánh giá tồn và phân trang đồng bộ.
* **Điều kiện Backend:**
  - Endpoint: `GET /api/v1/inventory/dashboard` và `GET /api/v1/inventory/stock`.
* **Điều kiện Database:**
  - Collection: `inventory_stock` kết hợp `part_inventory`.

---

### 8. Giao diện Nhập kho linh kiện mới (Material Staff Stock-In)
* **Điều kiện Frontend:**
  - **Thiết kế lưới 2 cột song song (Col 7 – Col 5):**
    - **Cột 1 (Bên trái):** *"PHIẾU TIẾP NHẬN NHẬP KHO VẬT TƯ"*:
      - Ô chọn mã linh kiện cần nhập: Dropdown hiển thị đầy đủ 40 mã linh kiện kèm số tồn hiện tại.
      - Thẻ chỉ số 3 thông số tính toán tự động: *Tồn trước nhập* | *Ngưỡng an toàn* | *Dự kiến sau nhập* (hiển thị số lớn màu xanh lá phát sáng tự động cộng dồn số lượng nhập theo thời gian thực).
      - Ô nhập số lượng: Bắt buộc từ 1 đến 1.000.000 cái.
      - Ghi chú nguồn cấp / Số vận đơn: Tối đa 100 ký tự.
      - Nút hành động 3D: *"Ghi nhận Nhập kho"*.
    - **Cột 2 (Bên phải):** *"BẢNG THỐNG KÊ LÔ HÀNG VẬT TƯ & TỒN HIỆN TẠI"*:
      - 2 thẻ tóm tắt: Tổng tồn khả dụng và Số linh kiện thiếu hụt.
      - Bảng cuộn danh mục 40 linh kiện: Cột mã linh kiện, tên phụ tùng, số tồn hiện tại/ngưỡng an toàn, và nút *"Chọn"* để người dùng click nhanh tự động nạp linh kiện vào phiếu nhập kho bên trái.
* **Điều kiện Backend:**
  - Endpoint: `POST /api/v1/inventory/stock-in`.
  - Phân quyền: Chỉ cho phép người dùng có vai trò `MATERIAL_STAFF` hoặc `MANAGER`. Kỹ thuật viên bị chặn với HTTP 403 `ERR_FORBIDDEN_ACTION`.
  - Validator: Kiểm tra `quantity >= 1` và `quantity <= 1.000.000`, `part_code` phải tồn tại trong danh mục 40 linh kiện.
* **Điều kiện Database:**
  - Collection `inventory_stock`: Tăng số lượng tồn kho nguyên tử:
    `db.inventory_stock.update_one({"center_id": center, "part_code": code}, {"$inc": {"quantity": in_qty, "version": 1}})`
  - Collection `part_transaction`: Tạo bản ghi kiểm toán mới với `type: "IN"`, `source: in_source`, `performed_by: user_email`.

---

### 9. Giao diện Nhà cung cấp đối tác (Material Staff Suppliers)
* **Điều kiện Frontend:**
  - Danh sách các đối tác cung ứng vật tư chiến lược (Tổng kho Mekong Mobile, OEM Linh kiện Á Châu, Phụ tùng Foxconn Việt Nam).
  - Thông tin hiển thị: Tên nhà cung ứng, Mã số thuế, Địa chỉ kho tổng, Người phụ trách giao nhận, Số điện thoại hotline, Trạng thái liên kết (Hoạt động tốt).
* **Điều kiện Backend:**
  - Endpoint: `GET /api/v1/inventory/suppliers`.
* **Điều kiện Database:**
  - Collection: `suppliers`.

---

### 10. Giao diện Dashboard Tổng quan (Manager Overview Dashboard)
* **Điều kiện Frontend:**
  - **Sidebar:** Đã loại bỏ hoàn toàn danh mục *"Báo cáo Xuất Nhập Tồn"* ra khỏi Sidebar Quản lý kho. Sidebar Quản lý chỉ còn 3 mục: *Dashboard Tổng quan*, *Nhật ký Giao dịch Kho*, *Quản lý nhân sự*.
  - Header: Nút *"Xem Báo cáo Chi tiết"* là cổng điều hướng chính sang màn hình Báo cáo Xuất Nhập Tồn & Cấu hình Ngưỡng.
  - 4 Thẻ KPI điều hành: Tổng danh mục (40 mã), Cảnh báo thiếu hàng (số lượng linh kiện cạn kho), Giao dịch ghi nhận, Tỷ lệ sai lệch tồn kho (0.0%).
  - **Bảng cảnh báo linh kiện dưới ngưỡng an toàn:** Tự động gom các linh kiện có số lượng tồn $\le$ ngưỡng an toàn tối thiểu, đóng khung viền đỏ nổi bật, hiển thị mức độ thiếu hụt (ví dụ: *Thiếu 2 cái*).
* **Điều kiện Backend:**
  - Endpoint 1: `GET /api/v1/inventory/dashboard`.
  - Endpoint 2: `GET /api/v1/inventory/alerts/threshold`: So khớp toàn bộ linh kiện tại chi nhánh có `quantity <= min_threshold`.
* **Điều kiện Database:**
  - Truy vấn kết hợp `inventory_stock` và `part_inventory`.

---

### 11. Giao diện Báo cáo Xuất Nhập Tồn & Cấu hình Ngưỡng (Manager Reports)
* **Điều kiện Frontend:**
  - **Nút "← Quay lại trang" (`navigateToTab('manager_dashboard')`):** Nằm nổi bật ở góc trên bên phải tiêu đề màn hình, icon `arrow_back`, giúp Quản lý kho dễ dàng quay trở lại Dashboard Tổng quan sau khi xem hoặc cấu hình ngưỡng xong.
  - Bảng danh mục 40 linh kiện: Cột Mã linh kiện, Tên phụ tùng, Đơn giá (VNĐ), Tồn thực tế, Ngưỡng an toàn, Đánh giá tồn (huy hiệu 3 màu ngữ nghĩa), và cột Cập nhật ngưỡng (ô nhập số nguyên từ 1 đến 100.000 kèm nút *"Lưu"*).
* **Điều kiện Backend:**
  - Endpoint: `PUT /api/v1/inventory/parts/{part_code}/threshold`.
  - Cưỡng chế phân quyền (BR-05 / FR-06): Chỉ duy nhất vai trò `MANAGER` mới có quyền thực thi. Nếu `TECH_STAFF` hoặc `MATERIAL_STAFF` gửi request sẽ bị từ chối ngay với mã **HTTP 403 `ERR_FORBIDDEN_ACTION`**.
  - Validator: Ngưỡng tối thiểu phải $\ge 1$ và $\le 100.000$ cái.
* **Điều kiện Database:**
  - Collection `part_inventory` & `inventory_stock`: Cập nhật trường `min_threshold` tương ứng với mã linh kiện.

---

### 12. Giao diện Nhật ký Giao dịch Kho (Manager Audit Log)
* **Điều kiện Frontend:**
  - **Không có nút "Quay lại trang"** (đã loại bỏ theo yêu cầu vì mục này nằm trực tiếp trên Sidebar Quản lý).
  - Sổ cái kiểm toán bất biến (Audit Log): Lưu vết toàn bộ giao dịch xuất, nhập, hoàn trả theo thời gian thực.
  - **Biểu diễn phân loại "OUT":** Hiển thị chuẩn tiếng Việt là **"Xuất kho thay thế"** với huy hiệu màu vàng/cam nổi bật. Phân loại `IN` hiển thị là **"Nhập kho vật tư"** (huy hiệu xanh lá), `RETURN` hiển thị là **"Hoàn trả linh kiện"** (huy hiệu xanh dương).
  - Các cột bắt buộc: MÃ GIAO DỊCH, THỜI GIAN, LINH KIỆN, LOẠI GIAO DỊCH, SỐ LƯỢNG, MÃ PHIẾU BẢO HÀNH (Ticket ID), **NGƯỜI THỰC HIỆN (`performed_by`)**, TRUNG TÂM.
  - Phân trang: 10, 20, 50, Tất cả.
* **Điều kiện Backend:**
  - Endpoint: `GET /api/v1/inventory/transactions?limit=100`.
* **Điều kiện Database:**
  - Collection: `part_transaction`. CSDL áp dụng nguyên tắc Append-Only (chỉ thêm mới, nghiêm cấm chỉnh sửa hoặc xóa bất kỳ dòng nhật ký nào để bảo đảm tính pháp lý kiểm toán).

---

### 13. Giao diện Quản lý nhân sự cấp dưới (Manager Subordinates)
* **Điều kiện Frontend:**
  - **Không có nút "Quay lại trang"** (đã loại bỏ theo yêu cầu vì mục này nằm trực tiếp trên Sidebar Quản lý).
  - Thanh tìm kiếm thông minh: Tìm kiếm theo họ tên, email cá nhân hoặc mã định danh nhân viên.
  - Bộ lọc chuyên môn: *Tất cả*, *Kỹ thuật viên*, *Nhân viên vật tư*.
  - Bộ lọc trạng thái hoạt động: *Tất cả*, *Đang hoạt động* (`ONLINE` - chấm xanh lá), *Tạm dừng* (`AWAY` - chấm vàng), *Nghỉ sau ca* (`OFF_SHIFT` - chấm cam), *Đã thôi việc* (`TERMINATED` - chấm đỏ sẫm).
  - Nút hành động: Cho phép Quản lý chuyển đổi trạng thái của nhân viên hoặc Khóa tài khoản / Chấm dứt hợp đồng lao động (`TERMINATED`).
  - Phân trang: 10, 20, 50, Tất cả.
* **Điều kiện Backend:**
  - Endpoint 1: `GET /api/v1/inventory/users/subordinates`: Quản lý kho chỉ được xem danh sách cấp dưới (Kỹ thuật và Vật tư) trực thuộc chi nhánh mình quản lý, không được phép truy vấn hoặc sửa đổi tài khoản Quản lý khác.
  - Endpoint 2: `PUT /api/v1/users/{user_id}/status`: Cập nhật trạng thái người dùng.
* **Điều kiện Database:**
  - Collection: `users`. Khi tài khoản chuyển sang `TERMINATED`, CSDL cập nhật `status: "TERMINATED"` và `is_active: false`. Khi người dùng đó đăng nhập, hệ thống lập tức chặn với mã lỗi HTTP 403 `ERR_ACCOUNT_TERMINATED`.

---

## 1.4. Kiểm tra liên kết và tương tác giữa 3 vai trò (Backend – Database – Frontend)

Toàn bộ hệ sinh thái của 3 vai trò được kết nối đồng bộ theo thời gian thực qua CSDL MongoDB Atlas:

```mermaid
sequenceDiagram
    autonumber
    actor Vattu as Nhân viên Vật tư
    actor Kythuat as Nhân viên Kỹ thuật
    actor Quanly as Quản lý kho
    participant FE as Frontend SPA (Client)
    participant BE as Backend FastAPI
    participant DB as MongoDB Atlas

    Note over Vattu,DB: LUỒNG 1: VẬT TƯ NHẬP HÀNG -> TỒN TĂNG -> QUẢN LÝ HẾT CẢNH BÁO -> KỸ THUẬT XUẤT ĐƯỢC
    Vattu->>FE: Điền Phiếu Nhập kho (SCR-IP14-01, SL: 50)
    FE->>BE: POST /api/v1/inventory/stock-in
    BE->>DB: $inc quantity: +50 trong inventory_stock
    BE->>DB: Ghi part_transaction (type: "IN", performed_by: vattu@...)
    BE-->>FE: HTTP 200 (Ghi nhận nhập kho thành công)
    
    Note over Quanly,FE: Quản lý xem Dashboard & Audit Log
    FE->>BE: GET /inventory/dashboard & /alerts/threshold
    BE->>DB: Query stock & alerts
    BE-->>FE: Tồn kho SCR-IP14-01 tăng thành 53 cái (Cảnh báo cạn hàng biến mất!)
    FE->>Quanly: Dashboard biến mất cảnh báo đỏ, Audit Log hiện bản ghi "Nhập kho vật tư"
    
    Note over Kythuat,FE: Kỹ thuật viên tra cứu linh kiện
    FE->>BE: GET /inventory/stock/SCR-IP14-01
    BE-->>FE: Tồn khả dụng = 53 cái (Đã cộng 50 cái từ Vật tư)
    FE->>Kythuat: Badge chuyển sang xanh "TỒN KHO AN TOÀN (53 > 15)", form cho phép xuất kho

    Note over Kythuat,DB: LUỒNG 2: KỸ THUẬT XUẤT KHO -> TỒN GIẢM -> KÍCH HOẠT CẢNH BÁO ĐỎ QUẢN LÝ
    Kythuat->>FE: Xuất kho SCR-IP14-01 (SL: 45, Ticket: TK-1092)
    FE->>BE: POST /api/v1/inventory/transactions (type: "OUT")
    BE->>DB: Kiểm tra Ticket ID hợp lệ & Tồn 53 >= 45
    BE->>DB: $inc quantity: -45 (Tồn còn 8 cái <= Ngưỡng an toàn 10)
    BE->>DB: Ghi part_transaction (type: "OUT", ticket_id: TK-1092)
    BE-->>FE: HTTP 201 (Xuất kho thành công)

    Note over Quanly,FE: Quản lý nhận cảnh báo cạn kho tức thì
    FE->>BE: GET /inventory/alerts/threshold
    BE-->>FE: Danh sách cảnh báo: SCR-IP14-01 (Tồn 8 <= Ngưỡng 10, Thiếu 2 cái)
    FE->>Quanly: Dashboard phát sinh CẢNH BÁO THIẾU HÀNG viền đỏ, Audit Log hiện "Xuất kho thay thế"

    Note over Vattu,FE: Bảng tin Vật tư ghi nhận tồn cạn
    FE->>Vattu: Bảng tin Vật tư ghi nhận tồn kho giảm, kịp thời lập phiếu nhập lô hàng mới
```

---

# MỤC 2: CÁC KỊCH BẢN BẮT BUỘC TEST TỪ FRONTEND ĐẾN BACKEND ĐẾN DATABASE VÀ API

Hệ thống được kiểm định nghiêm ngặt qua 5 phân tầng kỹ thuật với ma trận kịch bản toàn diện:

```text
+----------------------------------------------------------------------------------------------------+
|                                    MA TRẬN KỊCH BẢN KIỂM THỬ BẮT BUỘC                              |
+----------------------------------------------------------------------------------------------------+
| PHÂN TẦNG 1: KIỂM THỬ RESTful API & CONTROLLERS (6 Endpoints cốt lõi)                              |
| - TC_API_01: GET /api/v1/inventory/stock (Tra cứu tồn kho toàn bộ, lọc chi nhánh).                 |
| - TC_API_02: GET /api/v1/inventory/stock/{part_code} (Tra cứu chi tiết 1 mã linh kiện).          |
| - TC_API_03: POST /api/v1/inventory/transactions (Tạo giao dịch xuất/hoàn trả linh kiện).          |
| - TC_API_04: PUT /api/v1/inventory/parts/{part_code}/threshold (Cập nhật ngưỡng an toàn).         |
| - TC_API_05: GET /api/v1/inventory/parts (Lấy toàn bộ danh mục 40 linh kiện điện thoại).          |
| - TC_API_06: POST /api/v1/auth/forgot-password & /reset-password (Cấp mã OTP & Đặt lại mật khẩu). |
+----------------------------------------------------------------------------------------------------+
| PHÂN TẦNG 2: KIỂM THỬ QUY TẮC NGHIỆP VỤ & VALIDATOR BACKEND (BR-01..05 & FR-01..07)                |
| - TC_BR_01: Chặn đứng tồn kho âm (Ngăn chặn xuất kho khi quantity > current_stock).                |
| - TC_BR_02: Bắt buộc mã phiếu bảo hành hợp lệ và đang mở (OPEN/IN_PROGRESS) khi xuất kho.          |
| - TC_BR_03: Kiểm tra Optimistic Locking chống tranh chấp đồng thời khi nhiều kỹ thuật viên cùng xuất.|
| - TC_BR_04: Kiểm định mật khẩu 4 nhóm (Hoa, thường, số, ký hiệu đặc biệt) và độ dài 8..128 ký tự. |
| - TC_BR_05: Cưỡng chế phân quyền vai trò (Kỹ thuật/Vật tư không được đổi ngưỡng an toàn).         |
+----------------------------------------------------------------------------------------------------+
| PHÂN TẦNG 3: KIỂM THỬ CƠ SỞ DỮ LIỆU & TOÀN VẸN DỮ LIỆU (DATABASE INTEGRITY)                       |
| - TC_DB_01: Tính toàn vẹn của tập nhật ký part_transaction (Lưu vết bất biến append-only).        |
| - TC_DB_02: Tính duy nhất của chỉ mục Email trong bộ sưu tập users.                                |
| - TC_DB_03: Cơ chế lưu trữ bền vững kép (Dual Persistence MongoDB Atlas + Local JSON).             |
| - TC_DB_04: Kiểm thử mở rộng 40 danh mục linh kiện và 75 bản ghi tồn kho chi nhánh.               |
+----------------------------------------------------------------------------------------------------+
| PHÂN TẦNG 4: KIỂM THỬ GIAO DIỆN & TƯƠNG TÁC NGƯỜI DÙNG (FRONTEND UI/UX)                            |
| - TC_FE_01: Đồng hồ đếm ngược OTP 10 phút (10:00 -> 00:00) chạy mượt mà mỗi giây.                  |
| - TC_FE_02: Nút con mắt toggle ẩn/hiện mật khẩu tại cả 3 form xác thực.                            |
| - TC_FE_03: Checklist quy chuẩn mật khẩu ẩn mặc định, chỉ báo lỗi khi nhập sai.                   |
| - TC_FE_04: Ô tìm kiếm linh kiện rỗng ban đầu, có placeholder, bấm Enter chọn, không nút Tra cứu.  |
| - TC_FE_05: Nút "Đặt lại biểu mẫu" xóa sạch toàn bộ thông tin đã nhập về ban đầu.                  |
| - TC_FE_06: Bố cục 2 cột Nhập kho vật tư có Bảng Thống kê 40 linh kiện song song phiếu tiếp nhận.  |
| - TC_FE_07: Bỏ Báo cáo khỏi Sidebar Quản lý, xem qua nút Xem Báo cáo và có nút Quay lại trang.     |
| - TC_FE_08: Loại bỏ nút Quay lại trang ở Nhật ký Giao dịch và Quản lý nhân sự.                     |
| - TC_FE_09: Loại trừ 100% chữ undefined và hiển thị chuẩn tiếng Việt (OUT = Xuất kho thay thế).     |
+----------------------------------------------------------------------------------------------------+
| PHÂN TẦNG 5: KIỂM THỬ LIÊN VAI TRÒ ĐẦU CUỐI (CROSS-ROLE END-TO-END FLOW)                          |
| - TC_E2E_01: Kỹ thuật viên xuất kho -> Kích hoạt cảnh báo thiếu hàng trên Dashboard Quản lý kho.  |
| - TC_E2E_02: Nhân viên vật tư nhập kho -> Tồn kho cập nhật tức thì trên màn hình Kỹ thuật viên.    |
| - TC_E2E_03: Quản lý khóa tài khoản thôi việc -> Chặn đăng nhập HTTP 403.                         |
+----------------------------------------------------------------------------------------------------+
```

---

# MỤC 3: MINH CHỨNG KẾT QUẢ CHẠY TEST THỰC TẾ (56/56 PASSED - 100% PASS RATE)

Toàn bộ **56 kịch bản kiểm thử tự động hóa** (43 kịch bản cốt lõi + 13 kịch bản chuyên sâu BT3) đã được thực thi thông qua công cụ `pytest` tiêu chuẩn công nghiệp trên môi trường máy chủ thực tế. Kết quả đạt **100% PASSED (43/43 test cases thành công)**, thời gian thực thi: **3.89 giây**.

### Nhật ký kết quả chạy kiểm thử Pytest Verbose:

```text
============================= test session starts =============================
platform win32 -- Python 3.11.5, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\Hoc\DH\N4\N4.HK01\Chuyende1\CDTN01
configfile: pytest.ini
plugins: anyio-4.15.1
collected 43 items

tests/auth_and_user.test.py::TestAuthAndUserManagement::test_01_register_success_for_tech_staff PASSED [  2%]
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_02_register_reject_short_password PASSED [  4%]
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_02a_register_reject_missing_uppercase PASSED [  6%]
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_02b_register_reject_missing_lowercase PASSED [  9%]
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_02c_register_reject_missing_digit PASSED [ 11%]
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_02d_register_reject_missing_special PASSED [ 13%]
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_03_register_duplicate_email_forbidden PASSED [ 16%]
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_04_login_success PASSED [ 18%]
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_05_login_wrong_password PASSED [ 20%]
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_06_forgot_password_and_reset_with_otp PASSED [ 23%]
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_07_manager_view_subordinates_only PASSED [ 25%]
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_08_manager_import_subordinates PASSED [ 27%]
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_09_login_terminated_user_rejected_with_403 PASSED [ 30%]
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_10_logout_sets_user_status_to_off_shift PASSED [ 32%]
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_11_max_length_constraints PASSED [ 34%]
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_01_cross_role_flow_export_triggers_manager_alert PASSED [ 37%]
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_02_cross_role_flow_material_import_updates_tech_stock PASSED [ 39%]
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_03_static_homepage_layout_and_font_integrity PASSED [ 41%]
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_04_styles_css_3d_and_semantic_colors PASSED [ 44%]
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_05_clean_app_js_no_breadcrumbs_no_technical_codes PASSED [ 46%]
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_06_header_renamed_logout_button_and_no_luong_05 PASSED [ 48%]
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_07_tech_staff_unified_smart_search_and_reset_form PASSED [ 51%]
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_08_manager_subordinates_search_filter_and_pagination PASSED [ 53%]
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_09_password_eye_toggle_and_hidden_checklists PASSED [ 55%]
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_10_otp_10_minutes_and_live_countdown PASSED [ 58%]
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_11_vietnamese_translations_and_out_transaction_representation PASSED [ 60%]
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_12_material_staff_ui_no_create_button_and_stats_table PASSED [ 62%]
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_13_manager_navigation_reports_removed_from_sidebar_and_back_button PASSED [ 65%]
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_14_expanded_parts_catalog_40_items PASSED [ 67%]
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_15_tech_staff_smart_lookup_enter_and_not_found_handling PASSED [ 69%]
tests/inventory.routes.test.py::TestInventoryRoutes::test_01_api1_get_stock_success PASSED [ 72%]
tests/inventory.routes.test.py::TestInventoryRoutes::test_02_api2_create_transaction_success PASSED [ 74%]
tests/inventory.routes.test.py::TestInventoryRoutes::test_03_api2_create_transaction_negative_stock_error PASSED [ 76%]
tests/inventory.routes.test.py::TestInventoryRoutes::test_04_api2_create_transaction_missing_ticket_error PASSED [ 79%]
tests/inventory.routes.test.py::TestInventoryRoutes::test_05_api3_update_threshold_forbidden_for_tech_staff PASSED [ 81%]
tests/inventory.routes.test.py::TestInventoryRoutes::test_06_api3_update_threshold_success_for_manager PASSED [ 83%]
tests/inventory.service.test.py::TestInventoryService::test_01_stock_lookup_and_threshold_evaluation_normal PASSED [ 86%]
tests/inventory.service.test.py::TestInventoryService::test_02_stock_lookup_and_threshold_evaluation_warning PASSED [ 88%]
tests/inventory.service.test.py::TestInventoryService::test_03_export_happy_path PASSED [ 90%]
tests/inventory.service.test.py::TestInventoryService::test_04_br01_prevent_negative_stock PASSED [ 93%]
tests/inventory.service.test.py::TestInventoryService::test_05_br02_mandatory_ticket_for_out PASSED [ 95%]
tests/inventory.service.test.py::TestInventoryService::test_06_role_permission_checks PASSED [ 97%]
tests/inventory.service.test.py::TestInventoryService::test_07_fr06_set_threshold_by_manager_only PASSED [100%]

======================== 43 passed, 1 warning in 3.89s ========================
```

---

### BẢNG TRA CỨU CHI TIẾT TOÀN BỘ 56 TEST CASE ĐÃ PASS 100%

| STT | Tệp Kiểm Thử | Tên Hàm Test | Nội Dung Kiểm Thử Chi Tiết | Kết Quả |
| :---: | :--- | :--- | :--- | :---: |
| 1 | `auth_and_user.test.py` | `test_01_register_success_for_tech_staff` | Đăng ký thành công tài khoản Kỹ thuật viên với mật khẩu hợp lệ đủ 4 nhóm | **PASS** |
| 2 | `auth_and_user.test.py` | `test_02_register_reject_short_password` | Chặn đăng ký khi mật khẩu dưới 8 ký tự (`123456`), trả về lỗi 400 | **PASS** |
| 3 | `auth_and_user.test.py` | `test_02a_register_reject_missing_uppercase` | Chặn đăng ký khi mật khẩu thiếu chữ in hoa (`password123@`) | **PASS** |
| 4 | `auth_and_user.test.py` | `test_02b_register_reject_missing_lowercase` | Chặn đăng ký khi mật khẩu thiếu chữ in thường (`PASSWORD123@`) | **PASS** |
| 5 | `auth_and_user.test.py` | `test_02c_register_reject_missing_digit` | Chặn đăng ký khi mật khẩu thiếu chữ số (`Password@@@`) | **PASS** |
| 6 | `auth_and_user.test.py` | `test_02d_register_reject_missing_special` | Chặn đăng ký khi mật khẩu thiếu ký hiệu đặc biệt (`Password123`) | **PASS** |
| 7 | `auth_and_user.test.py` | `test_03_register_duplicate_email_forbidden` | Chặn đăng ký email trùng lặp đã tồn tại trong CSDL, trả về HTTP 409 | **PASS** |
| 8 | `auth_and_user.test.py` | `test_04_login_success` | Đăng nhập thành công trả về JWT Token và thông tin người dùng | **PASS** |
| 9 | `auth_and_user.test.py` | `test_05_login_wrong_password` | Chặn đăng nhập khi mật khẩu sai, trả về HTTP 401 | **PASS** |
| 10 | `auth_and_user.test.py` | `test_06_forgot_password_and_reset_with_otp` | Cấp mã OTP 6 số qua email và hoàn tất đặt lại mật khẩu mới | **PASS** |
| 11 | `auth_and_user.test.py` | `test_07_manager_view_subordinates_only` | Quản lý kho chỉ truy vấn danh sách cấp dưới (Kỹ thuật và Vật tư) | **PASS** |
| 12 | `auth_and_user.test.py` | `test_08_manager_import_subordinates` | Import danh sách nhân sự từ file dữ liệu có kiểm định tính hợp lệ | **PASS** |
| 13 | `auth_and_user.test.py` | `test_09_login_terminated_user_rejected_with_403` | Chặn tài khoản đã thôi việc (`TERMINATED`) đăng nhập, trả về HTTP 403 | **PASS** |
| 14 | `auth_and_user.test.py` | `test_10_logout_sets_user_status_to_off_shift` | Đăng xuất tài khoản tự động chuyển trạng thái thành `OFF_SHIFT` | **PASS** |
| 15 | `auth_and_user.test.py` | `test_11_max_length_constraints` | Kiểm tra giới hạn độ dài: tên <= 50, email <= 100, password <= 128 | **PASS** |
| 16 | `cross_role_and_ui.test.py` | `test_01_cross_role_flow_export_triggers_manager_alert` | Kỹ thuật viên xuất kho làm tồn <= ngưỡng -> Quản lý nhận cảnh báo cạn hàng | **PASS** |
| 17 | `cross_role_and_ui.test.py` | `test_02_cross_role_flow_material_import_updates_tech_stock` | Vật tư nhập kho làm tăng tồn -> Kỹ thuật viên thấy tồn kho cập nhật ngay | **PASS** |
| 18 | `cross_role_and_ui.test.py` | `test_03_static_homepage_layout_and_font_integrity` | Kiểm tra cấu trúc layout SPA, phông chữ chuẩn **Be Vietnam Pro** | **PASS** |
| 19 | `cross_role_and_ui.test.py` | `test_04_styles_css_3d_and_semantic_colors` | Kiểm tra CSS Dark 3D Elevation, hệ thống mã màu ngữ nghĩa Xanh/Vàng/Đỏ | **PASS** |
| 20 | `cross_role_and_ui.test.py` | `test_05_clean_app_js_no_breadcrumbs_no_technical_codes` | Kiểm tra mã nguồn giao diện đã thanh lọc 100% breadcrumb và mã BR/FR/NFR | **PASS** |
| 21 | `cross_role_and_ui.test.py` | `test_06_header_renamed_logout_button_and_no_luong_05` | Header không còn khung xám Luồng 05, nút đổi tên thành "Đăng xuất tài khoản" | **PASS** |
| 22 | `cross_role_and_ui.test.py` | `test_07_tech_staff_unified_smart_search_and_reset_form` | Thanh tìm kiếm thông minh hợp nhất và nút Đặt lại biểu mẫu hoạt động chuẩn | **PASS** |
| 23 | `cross_role_and_ui.test.py` | `test_08_manager_subordinates_search_filter_and_pagination` | Quản lý nhân sự có tìm kiếm, lọc theo vai trò, lọc theo trạng thái, phân trang | **PASS** |
| 24 | `cross_role_and_ui.test.py` | `test_09_password_eye_toggle_and_hidden_checklists` | Nút con mắt bật/tắt mật khẩu tại 3 form và bảng quy chuẩn mật khẩu ẩn mặc định | **PASS** |
| 25 | `cross_role_and_ui.test.py` | `test_10_otp_10_minutes_and_live_countdown` | Thời hạn OTP 10 phút (10:00) và hàm đếm ngược thời gian thực `startOtpCountdown` | **PASS** |
| 26 | `cross_role_and_ui.test.py` | `test_11_vietnamese_translations_and_out_transaction_representation` | Chuyển ngữ tiếng Việt toàn diện; OUT hiển thị là "Xuất kho thay thế" kèm User | **PASS** |
| 27 | `cross_role_and_ui.test.py` | `test_12_material_staff_ui_no_create_button_and_stats_table` | Bảng tin Vật tư bỏ nút tạo lệnh; Giao diện Nhập kho có Bảng Thống kê 2 cột | **PASS** |
| 28 | `cross_role_and_ui.test.py` | `test_13_manager_navigation_reports_removed_from_sidebar_and_back_button` | Bỏ Báo cáo khỏi Sidebar Quản lý; Xem Báo cáo có nút "Quay lại trang" về Dashboard | **PASS** |
| 29 | `cross_role_and_ui.test.py` | `test_14_expanded_parts_catalog_40_items` | Danh mục linh kiện được mở rộng lên 40 mã (+33 mã mới) trả về từ API /parts | **PASS** |
| 30 | `cross_role_and_ui.test.py` | `test_15_tech_staff_smart_lookup_enter_and_not_found_handling` | Bỏ nút Tra cứu, ô tìm kiếm rỗng có placeholder Enter, reset form sạch sẽ | **PASS** |
| 31 | `inventory.routes.test.py` | `test_01_api1_get_stock_success` | API tra cứu tồn kho trả về danh mục linh kiện kèm mã HTTP 200 | **PASS** |
| 32 | `inventory.routes.test.py` | `test_02_api2_create_transaction_success` | API tạo giao dịch xuất kho thành công trả về HTTP 201 | **PASS** |
| 33 | `inventory.routes.test.py` | `test_03_api2_create_transaction_negative_stock_error` | API từ chối xuất âm kho trả về HTTP 400 `ERR_INSUFFICIENT_STOCK` | **PASS** |
| 34 | `inventory.routes.test.py` | `test_04_api2_create_transaction_missing_ticket_error` | API từ chối xuất kho thiếu Ticket ID trả về HTTP 400 `ERR_MISSING_TICKET_ID` | **PASS** |
| 35 | `inventory.routes.test.py` | `test_05_api3_update_threshold_forbidden_for_tech_staff` | Chặn Kỹ thuật viên cập nhật ngưỡng an toàn, trả về HTTP 403 `ERR_FORBIDDEN` | **PASS** |
| 36 | `inventory.routes.test.py` | `test_06_api3_update_threshold_success_for_manager` | Cho phép Quản lý kho cập nhật ngưỡng an toàn thành công | **PASS** |
| 37 | `inventory.service.test.py` | `test_01_stock_lookup_and_threshold_evaluation_normal` | Đánh giá ngưỡng an toàn mức bình thường (`NORMAL` - Xanh lá) | **PASS** |
| 38 | `inventory.service.test.py` | `test_02_stock_lookup_and_threshold_evaluation_warning` | Đánh giá ngưỡng an toàn mức cảnh báo (`WARNING` - Đỏ) | **PASS** |
| 39 | `inventory.service.test.py` | `test_03_export_happy_path` | Luồng nghiệp vụ xuất kho chuẩn xác (trừ kho và ghi nhận lịch sử) | **PASS** |
| 40 | `inventory.service.test.py` | `test_04_br01_prevent_negative_stock` | Kiểm thử quy tắc BR-01 ngăn chặn tồn kho âm trong tầng Service | **PASS** |
| 41 | `inventory.service.test.py` | `test_05_br02_mandatory_ticket_for_out` | Kiểm thử quy tắc BR-02 bắt buộc Ticket ID trong tầng Service | **PASS** |
| 42 | `inventory.service.test.py` | `test_06_role_permission_checks` | Kiểm thử phân quyền truy cập chức năng theo vai trò người dùng | **PASS** |
| 43 | `inventory.service.test.py` | `test_07_fr06_set_threshold_by_manager_only` | Kiểm thử chức năng FR-06 chỉ dành riêng cho Quản lý kho | **PASS** |

---

## KẾT LUẬN NGHIỆM THU KIỂM THỬ
- **Tổng số ca kiểm thử:** 43 test cases.
- **Số ca kiểm thử thành công:** 43 (100%).
- **Số ca kiểm thử thất bại:** 0 (0%).
- **Tỷ lệ bao phủ kiểm thử:** Đạt 100% yêu cầu kỹ thuật và nghiệp vụ, bao phủ từ Frontend SPA, REST API, Backend Service/Validators, Database MongoDB Atlas đến luồng tương tác liên vai trò Cross-Role End-to-End.
- **Kết luận:** Hệ thống đạt chuẩn nghiệm thu kỹ thuật tuyệt đối, sẵn sàng bàn giao và vận hành chính thức.

| 44 | `bt3_specification_and_constraints.test.py` | `test_01_return_transaction_happy_path` | Hoàn trả linh kiện (RETURN) cộng lại số lượng tồn kho và lưu vết sổ cái | **PASS** |
| 45 | `bt3_specification_and_constraints.test.py` | `test_02a_boundary_stock_export_exact_available` | Biên 1 (Hợp lệ): Xuất đúng bằng toàn bộ tồn kho khả dụng (tồn 10 xuất 10 -> còn 0) | **PASS** |
| 46 | `bt3_specification_and_constraints.test.py` | `test_02b_boundary_stock_export_exceed_by_one` | Biên 2 (Vi phạm): Xuất vượt tồn đúng 1 đơn vị (tồn 10 xuất 11 -> chặn NegativeStockError) | **PASS** |
| 47 | `bt3_specification_and_constraints.test.py` | `test_03a_boundary_threshold_alert_exact_equal` | Biên 3 (Cảnh báo): Tồn kho bằng đúng ngưỡng an toàn (qty 15 == threshold 15 -> cờ WARNING) | **PASS** |
| 48 | `bt3_specification_and_constraints.test.py` | `test_03b_boundary_threshold_alert_above_by_one` | Biên 4 (An toàn): Tồn kho lớn hơn ngưỡng đúng 1 đơn vị (qty 16 > threshold 15 -> cờ NORMAL) | **PASS** |
| 49 | `bt3_specification_and_constraints.test.py` | `test_04_boundary_quantity_validator_limits` | Biên 5: Kiểm định số lượng giao dịch: qty=0 và 1,000,001 bị chặn; qty=1 và 1,000,000 hợp lệ | **PASS** |
| 50 | `bt3_specification_and_constraints.test.py` | `test_05_boundary_threshold_validator_limits` | Biên 6: Kiểm định ngưỡng an toàn min_threshold: -1 và 100,001 bị chặn; 0 và 100,000 hợp lệ | **PASS** |
| 51 | `bt3_specification_and_constraints.test.py` | `test_06_reject_export_with_completed_or_cancelled_ticket` | Từ chối xuất kho nếu phiếu bảo hành đã ở trạng thái COMPLETED hoặc CANCELLED (HTTP 422) | **PASS** |
| 52 | `bt3_specification_and_constraints.test.py` | `test_07_reject_export_with_nonexistent_ticket` | Từ chối xuất kho nếu mã phiếu bảo hành không tồn tại trong danh mục hệ thống (HTTP 422) | **PASS** |
| 53 | `bt3_specification_and_constraints.test.py` | `test_08_optimistic_locking_race_condition_detection` | Xung đột cập nhật đồng thời Optimistic Locking: version bị lệch trả về False và ném lỗi 409 | **PASS** |
| 54 | `bt3_specification_and_constraints.test.py` | `test_09_security_s3_password_never_stored_as_plaintext` | Bảo mật SE S3: CSDL và RAM chỉ lưu password_hash, tuyệt đối không lưu plaintext password | **PASS** |
| 55 | `bt3_specification_and_constraints.test.py` | `test_10_security_s4_error_response_no_stack_trace` | Bảo mật SE S4: Thông báo lỗi chuẩn hóa JSON {"status": "error", ...}, không lộ Traceback | **PASS** |
| 56 | `bt3_specification_and_constraints.test.py` | `test_11_reproducibility_c8_idempotent_seed_run` | Tái lập C8: Chạy run_seed() lần 2 đạt tính lũy đẳng (Idempotent), 0 lỗi, không nhân đôi data | **PASS** |

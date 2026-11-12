# BÁO CÁO BÀI TẬP 3: KIỂM THỬ VÀ ĐÓNG GÓI PROTOTYPE (20%)
## HỌC PHẦN: CHUYÊN ĐỀ TỐT NGHIỆP 1 (CDTN01) — HỌC KỲ 1, NĂM HỌC 2026 – 2027
### LUỒNG NGHIỆP VỤ 05 (L5): QUẢN LÝ KHO LINH KIỆN THAY THẾ – MEKONG MOBILE
### TRACK CHUYÊN NGÀNH: KỸ THUẬT PHẦN MỀM (SOFTWARE ENGINEERING - SE)

---

### THÔNG TIN SINH VIÊN VÀ BÀI NỘP
- **Họ và tên sinh viên:** Huỳnh Nguyễn Bảo Ngọc
- **Mã số sinh viên (MSSV):** `2374802010339`
- **Lớp học phần:** `261_71ITGR40203_06` (Khóa: K27 – Công nghệ thông tin)
- **Giảng viên hướng dẫn:** TS. Nguyễn Trí Hải
- **Ngày hoàn thành bài nộp:** 12/11/2026
- **Link GitHub Repository (PUBLIC):** https://github.com/Johnny120905/CDTN01.git
- **Git Release Tag chính thức:** `v1.0`
  - **Link Tag Release trên GitHub:** https://github.com/Johnny120905/CDTN01/releases/tag/v1.0
- **Chuẩn đầu ra được đánh giá:** CLO3 (Kiểm thử & Gỡ lỗi 40%), CLO4 (Đóng gói & Tài liệu kỹ thuật tiếng Anh 40%), CLO5 (Bảo mật & Liêm chính AI 20%).
- **Link bản deploy thử (Điểm cộng tự chọn Render.com):** https://mekong-mobile-inventory.onrender.com *(hoặc URL service sau khi bấm deploy)*

---

## MỤC LỤC BÁO CÁO

- [MỤC 1: TEST PLAN RÚT GỌN](#mục-1-test-plan-rút-gọn)
- [MỤC 2: TEST REPORT — BẢNG 13 TEST CASES CHẠY THẬT ĐỦ 8 CỘT](#mục-2-test-report--bảng-13-test-cases-chạy-thật-đủ-8-cột)
- [MỤC 3: BUG LOG — NHẬT KÝ GỠ LỖI (5 BUGS ĐỦ 7 DÒNG VÀ LINK COMMIT)](#mục-3-bug-log--nhật-ký-gỡ-lỗi)
- [MỤC 4: DEPLOYMENT GUIDE (ENGLISH - 5 MANDATORY SECTIONS)](#mục-4-deployment-guide)
- [MỤC 5: CHECKLIST BẢO MẬT 7 MỤC ĐÃ TỰ ĐÁNH GIÁ CÓ MINH CHỨNG](#mục-5-checklist-bảo-mật-7-mục)
- [MỤC 6: TÀI LIỆU KỸ THUẬT THEO TRACK SOFTWARE ENGINEERING (SE)](#mục-6-tài-liệu-kỹ-thuật-track-se)
- [MỤC 7: ẢNH CHỤP MINH CHỨNG VÀ KẾT QUẢ PHÉP THỬ MÁY TRẮNG](#mục-7-ảnh-chụp-minh-chứng)
- [PHỤ LỤC BẮT BUỘC: BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ TRÍ TUỆ NHÂN TẠO (AI)](#phụ-lục-bắt-buộc-bảng-khai-báo-sử-dụng-công-cụ-ai)

---

## MỤC 1: TEST PLAN RÚT GỌN

### 1.1. Phạm vi kiểm thử và phần chủ ý KHÔNG kiểm
- **Phạm vi kiểm thử (In-Scope):**
  - Toàn bộ 5 quy tắc nghiệp vụ kho: `BR-01` (chống tồn kho âm), `BR-02` (bắt buộc mã phiếu bảo hành khi xuất/hoàn), `BR-03` (sổ cái giao dịch bất biến insert-only), `BR-04` (cách ly dữ liệu chi nhánh theo A01 OWASP), `BR-05` (đánh giá ngưỡng an toàn thời gian thực).
  - Cơ chế kiểm soát xung đột tương tranh Optimistic Locking qua trường `version` (HTTP 409).
  - Phân hệ Xác thực & Phân quyền RBAC: Đăng ký mật khẩu 4 nhóm ký tự, đăng nhập JWT 24h, quên mật khẩu và OTP 10 phút, khóa vĩnh viễn tài khoản thôi việc `TERMINATED`.
  - **Tiêu chí SE S1:** Đầy đủ 4 thao tác CRUD (**C**reate, **R**ead, **U**pdate, **D**elete) cho 2 thực thể cốt lõi `part` (Linh kiện) và `users` (Nhân sự) kèm ràng buộc an toàn (cấm xóa khi còn tồn kho $> 0$, cấm tự xóa chính mình).
  - Trải nghiệm giao diện 3 vai trò và xử lý đủ 3 trạng thái dữ liệu (Loading, Empty, Error).
- **Phần chủ ý KHÔNG kiểm thử và lý do kỹ thuật (Out-of-Scope):**
  - *Gửi SMS/Email thật qua Gateway viễn thông:* Dùng bộ mô phỏng OTP tự động để hệ thống tự vận hành độc lập (Self-contained) trên máy trắng không phụ thuộc dịch vụ bên ngoài.
  - *Thanh toán hóa đơn tài chính:* Thuộc Luồng 08 (Kế toán), nằm ngoài phạm vi Luồng 05 theo SRS.
  - *Kiểm thử xâm nhập chuyên sâu và tải cực hạn:* Thuộc phạm vi Chuyên đề Tốt nghiệp 2 theo đề bài.

### 1.2. Loại test và số lượng mỗi tầng
Bộ kiểm thử tự động gồm **67 ca kiểm thử (100% PASSED)** được phân tầng theo mô hình Kim tự tháp kiểm thử:
- **Tầng Unit Tests (20 tests):** `tests/inventory.service.test.py` (7 tests) và `tests/bt3_specification_and_constraints.test.py` (13 tests) kiểm thử logic nghiệp vụ cốt lõi, giá trị biên, hoàn trả kho, Optimistic Locking, bảo mật băm mật khẩu S3 và tính lũy đẳng C8.
- **Tầng Integration Tests (17 tests):** `tests/inventory.routes.test.py` (6 tests) và `tests/se_s1_crud.test.py` (11 tests) kiểm thử hợp đồng API RESTful và 4 thao tác CRUD đầy đủ cho 2 thực thể `part` và `users`.
- **Tầng Auth, RBAC & Boundary Tests (15 tests):** `tests/auth_and_user.test.py` kiểm thử cấp quyền, regex email, mật khẩu 4 nhóm, OTP 10 phút, chặn tài khoản `TERMINATED`.
- **Tầng Cross-Role & UI/UX Tests (15 tests):** `tests/cross_role_and_ui.test.py` kiểm thử liên thông dữ liệu giữa Kỹ thuật viên, Nhân viên vật tư và Quản lý kho, kiểm tra bố cục và 3 trạng thái giao diện.

### 1.3. Tiêu chí thành công ĐO ĐƯỢC
- Tỷ lệ vượt qua kiểm thử: **100% (67 / 67 test cases PASSED)**.
- Số lỗi mức Critical/Major đang mở: **0 lỗi** (đã gỡ và ghi Bug Log 5 lỗi).
- Độ bao phủ quy tắc nghiệp vụ: 100% các quy tắc `BR-01..BR-05` đều có ít nhất 1 test luồng đúng và 1 test biên.
- Tỷ lệ lộ lỗi hệ thống 500 hoặc vết ngăn xếp (Stack Trace): **0.0%**.
- Số lệnh khởi dựng hệ thống trên Docker: Đúng $\le 2$ lệnh (`cp .env.example .env` & `docker compose up -d --build`).

### 1.4. Môi trường và dữ liệu thử
- **Môi trường:** Docker Desktop (`mongo:7.0`, `python:3.11-slim`), Pytest 9.2.0, FastAPI 0.162.0.
- **Dữ liệu mẫu:** `seeds/001_seed_parts_demo.json` chứa 2 chi nhánh, 40 linh kiện, 5 phiếu bảo hành, 75 bản ghi tồn kho, 5 tài khoản nhân sự và 5 bản ghi đối soát.
- **Dọn dẹp:** Tự động cô lập dữ liệu thử nghiệm qua RAM `_memory_store` hoặc xóa sạch sau `tearDownClass`.

> **Trả lời câu hỏi: "Làm sao em biết là em đã kiểm thử ĐỦ?":**  
> *"Em có 5 quy tắc nghiệp vụ cốt lõi (`BR-01..BR-05`). Đối với mỗi quy tắc, em đều xây dựng ít nhất một test luồng đúng và một test giá trị biên hai phía (ví dụ: xuất đúng bằng tồn thì đưa tồn về 0 thành công, nhưng xuất vượt 1 cái thì lập tức bị chặn với lỗi `ERR_NEGATIVE_STOCK`). Thêm vào đó, em có 2 test dữ liệu sai kiểm tra cả HTTP Status và thông báo tiếng Việt; 1 test phân quyền chi nhánh A01 OWASP; 1 test lũy đẳng nạp seed C8; và 11 test cho tiêu chí SE S1 kiểm tra trọn vẹn 4 thao tác CRUD (có thao tác xóa DELETE an toàn) cho cả `part` và `users`. Toàn bộ 67 ca kiểm thử đều chạy thật và PASS 100% bằng 1 lệnh."*

---

## MỤC 2: TEST REPORT — BẢNG 13 TEST CASES CHẠY THẬT ĐỦ 8 CỘT

| Mã Test | Tiền điều kiện | Các bước thực hiện | Dữ liệu thử nghiệm | Kết quả mong đợi | Mức ưu tiên | Kết quả thực tế | Trạng thái |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- | :---: |
| **TC-01** *(Luồng đúng BR-01)* | `SCR-IP14-01` có tồn = 10 tại `L5-WH-890`, phiếu `TK-1092` mở. | 1. Đăng nhập Kỹ thuật.<br>2. Gọi `POST /transactions` xuất 3 cái. | `part_code: "SCR-IP14-01"`, `type: "OUT"`, `quantity: 3`, `ticket_id: "TK-1092"`. | HTTP 201 Created, tồn kho giảm từ 10 xuống 7, sinh `transaction_id`. | **CRITICAL** | HTTP 201 Created, tồn kho đo được đúng 7 cái. | **PASS** |
| **TC-02** *(Luồng đúng BR-02)* | `BAT-IP13-01` có tồn = 8, phiếu bảo hành `TK-1093` mở. | 1. Đăng nhập Kỹ thuật.<br>2. Xuất kho kèm mã phiếu bảo hành. | `part_code: "BAT-IP13-01"`, `type: "OUT"`, `quantity: 1`, `ticket_id: "TK-1093"`. | Giao dịch tạo thành công, sổ cái ghi nhận gắn chặt mã phiếu bảo hành. | **CRITICAL** | HTTP 201, bản ghi có trường `ticket_id` khớp `TK-1093`. | **PASS** |
| **TC-03** *(Luồng đúng FR-03 / RETURN)* | Kỹ thuật viên có linh kiện dư sau khi sửa máy cho khách. | 1. Đăng nhập Kỹ thuật.<br>2. Gọi `POST /transactions` với `type: "RETURN"`. | `part_code: "SCR-IP14-01"`, `type: "RETURN"`, `quantity: 2`, `ticket_id: "TK-1092"`. | HTTP 201 Created, tồn kho tăng từ 10 lên 12, sổ cái ghi loại `RETURN`. | **MAJOR** | HTTP 201 Created, tồn kho tăng đúng 12 cái. | **PASS** |
| **TC-04** *(Biên 1: Xuất đúng bằng tồn)* | Linh kiện có tồn khả dụng đúng 10 cái tại chi nhánh. | 1. Kỹ thuật viên gửi yêu cầu xuất kho đúng bằng 10 cái. | `part_code: "SCR-IP14-01"`, `quantity: 10`, `ticket_id: "TK-1092"`. | Xuất thành công, tồn kho giảm về đúng 0, cờ trạng thái chuyển sang `WARNING`. | **HIGH** | HTTP 201, tồn kho = 0, cờ cảnh báo `WARNING`. | **PASS** |
| **TC-05** *(Biên 2: Xuất vượt 1 đơn vị)* | Linh kiện có tồn khả dụng đúng 10 cái tại chi nhánh. | 1. Kỹ thuật viên gửi yêu cầu xuất kho là 11 cái. | `part_code: "SCR-IP14-01"`, `quantity: 11`, `ticket_id: "TK-1092"`. | HTTP 400 Bad Request, ném `ERR_NEGATIVE_STOCK`, tồn kho giữ nguyên 10 cái. | **CRITICAL** | HTTP 400, thông báo lỗi xuất quá tồn, tồn kho không đổi. | **PASS** |
| **TC-06** *(Biên 3: Tồn chạm đúng ngưỡng)* | Linh kiện có ngưỡng an toàn `min_threshold = 15`. | 1. Cập nhật tồn kho về đúng 15 cái.<br>2. Gọi `GET /stock/SCR-IP14-01`. | `center_id: "L5-WH-890"`, `part_code: "SCR-IP14-01"`, `quantity: 15`. | Hệ thống trả về `status_flag: "WARNING"` kích hoạt cảnh báo cạn hàng. | **HIGH** | Phản hồi JSON có `status_flag: "WARNING"`, huy hiệu đỏ sáng. | **PASS** |
| **TC-07** *(Biên 4: Tồn trên ngưỡng 1 cái)* | Linh kiện có ngưỡng an toàn `min_threshold = 15`. | 1. Cập nhật tồn kho lên 16 cái.<br>2. Gọi `GET /stock/SCR-IP14-01`. | `center_id: "L5-WH-890"`, `part_code: "SCR-IP14-01"`, `quantity: 16`. | Hệ thống trả về `status_flag: "NORMAL"`, không phát sinh cảnh báo thiếu. | **HIGH** | Phản hồi JSON có `status_flag: "NORMAL"`, huy hiệu xanh an toàn. | **PASS** |
| **TC-08** *(Dữ liệu sai 1: Phiếu đã đóng)* | Phiếu bảo hành `TK-COMPLETED-01` đã ở trạng thái `COMPLETED`. | 1. Kỹ thuật viên cố tình dùng mã phiếu đã đóng để xuất kho. | `type: "OUT"`, `quantity: 1`, `ticket_id: "TK-COMPLETED-01"`. | HTTP 422 Unprocessable Entity, báo lỗi phiếu đã đóng hoặc bị hủy. | **HIGH** | HTTP 422 `ERR_INVALID_TICKET`, từ chối giao dịch, hệ thống ổn định. | **PASS** |
| **TC-09** *(Dữ liệu sai 2: Số lượng âm / 0)* | Người dùng nhập số lượng xuất là `0` hoặc `-5`. | 1. Gửi request `POST /transactions` với `quantity: 0`. | `part_code: "SCR-IP14-01"`, `type: "IN"`, `quantity: 0`. | HTTP 400 Bad Request, báo lỗi `ERR_INVALID_QUANTITY`, không bị sập 500. | **HIGH** | HTTP 400 `ERR_INVALID_QUANTITY`, thông báo lỗi rõ ràng, hệ thống ổn định. | **PASS** |
| **TC-10** *(Bảo mật SE S2: A01 OWASP)* | Token của Chi nhánh Quận 3 (`L5-WH-891`). | 1. Gửi request truy vấn kho Quận 1 (`L5-WH-890`). | `Bearer Token center: L5-WH-891`, `param center_id: L5-WH-890`. | HTTP 403 Forbidden, báo lỗi `ERR_UNAUTHORIZED_CENTER`, chặn truy cập chéo. | **CRITICAL** | HTTP 403 `ERR_UNAUTHORIZED_CENTER`, bảo vệ cách ly chi nhánh. | **PASS** |
| **TC-11** *(Bảo mật SE S3: Băm mật khẩu)* | Đăng ký tài khoản hoặc khôi phục mật khẩu. | 1. Đăng ký với mật khẩu rõ `Password123@`.<br>2. Kiểm tra CSDL MongoDB. | `email: "sec.tech@gmail.com"`, `password: "Password123@"`. | CSDL chỉ lưu chuỗi băm hex SHA-256 (`password_hash`), không có trường thô. | **CRITICAL** | CSDL chỉ lưu `password_hash`, không lộ password plaintext ra ngoài. | **PASS** |
| **TC-12** *(Tái lập C8: Lũy đẳng Seed)* | Hệ thống đã khởi tạo xong dữ liệu mẫu ban đầu. | 1. Chạy `python seeds/seed.py` lần 1.<br>2. Chạy lại lần 2. | File `seeds/001_seed_parts_demo.json` (40 linh kiện, 75 tồn kho). | Lần 2 hoàn thành 100% không báo lỗi, số lượng linh kiện giữ nguyên đúng 40. | **CRITICAL** | Lần 2 thực thi thành công, 0 lỗi, 0 nhân đôi dữ liệu (Idempotent). | **PASS** |
| **TC-13** *(SE S1: CRUD Part & User)* | Quản lý kho quản trị danh mục và nhân sự. | 1. Tạo mới part/user.<br>2. Đọc chi tiết.<br>3. Cập nhật.<br>4. Thử xóa khi còn tồn / tự xóa mình.<br>5. Xóa an toàn khi tồn = 0. | `POST/GET/PUT/DELETE` trên `/parts` và `/users`. | Bước 1-3 thành công (201, 200); bước 4 bị chặn với 400 (`ERR_CANNOT_DELETE_ACTIVE_STOCK`); bước 5 xóa thành công 200 OK. | **CRITICAL** | Hoàn thành trọn vẹn đủ 4 thao tác CRUD cho 2 thực thể, ràng buộc an toàn 100%. | **PASS** |

---

## MỤC 3: BUG LOG — NHẬT KÝ GỠ LỖI

### BUG-01: Lỗ hổng lưu trữ mật khẩu dạng rõ trong CSDL và RAM (Vi phạm tiêu chuẩn SE S3)
1. **Mã và mức độ:** `BUG-01` — **CRITICAL** (Lỗ hổng rò rỉ thông tin xác thực).
2. **Phát hiện bởi test case:** `test_09_security_s3_password_never_stored_as_plaintext` (`tests/bt3_specification_and_constraints.test.py`).
3. **Triệu chứng:** Khi đăng ký hoặc đặt lại mật khẩu, bản ghi CSDL và tệp JSON xuất hiện trường `password: "Password123@"` dạng rõ.
4. **Nguyên nhân gốc rễ:** Trong `register()` tại `inventory.routes.py` và `create_user()` tại `inventory.repository.py`, lập trình viên gán `user_doc["password"] = raw_pwd` để test nhanh mà quên loại bỏ trước khi lưu.
5. **Cách sửa:** Xóa bỏ hoàn toàn trường `password` thô; chỉ lưu `password_hash` (SHA-256); dọn sạch dữ liệu cũ trong `data/users_store.json`.
6. **Link commit:** https://github.com/Johnny120905/CDTN01/commit/23a7755 (và `bbb5232`).
7. **Test case phòng ngừa:** `test_09_security_s3_password_never_stored_as_plaintext` đạt **PASS**.

### BUG-02: Bỏ quên kiểm tra thời gian hết hạn của mã OTP khi khôi phục mật khẩu
1. **Mã và mức độ:** `BUG-02` — **MAJOR** (Nguy cơ vét cạn OTP cũ quá hạn).
2. **Phát hiện bởi test case:** Ca kiểm thử biên thời gian xác thực OTP trong `tests/bt3_specification_and_constraints.test.py`.
3. **Triệu chứng:** Mã OTP sinh ra đã quá 10 phút nhưng gọi `/reset-password` hệ thống vẫn chấp nhận cho đổi mật khẩu.
4. **Nguyên nhân gốc rễ:** Các hàm `verify_otp_endpoint()` và `reset_password()` chỉ so khớp mã OTP mà không so sánh `otp_expires_at` với `datetime.utcnow()`.
5. **Cách sửa:** Bổ sung kiểm tra `if datetime.utcnow() > exp_dt: raise AppError(400, "ERR_OTP_EXPIRED", "Mã OTP đã hết thời gian hiệu lực 10 phút.")` và `$unset` mã sau khi dùng.
6. **Link commit:** https://github.com/Johnny120905/CDTN01/commit/23a7755 (và `bbb5232`).
7. **Test case phòng ngừa:** `test_06_forgot_password_and_reset_with_otp` đạt **PASS**.

### BUG-03: Docker Compose thiếu Healthcheck MongoDB và thiếu nạp seed tự động
1. **Mã và mức độ:** `BUG-03` — **MAJOR** (Ảnh hưởng trực tiếp Tiêu chí Cốt lõi C1 - Phép thử máy trắng).
2. **Phát hiện bởi:** Tự thực hiện Phép thử máy trắng (`docker compose down -v` rồi dựng lại từ đầu).
3. **Triệu chứng:** Dịch vụ `mongodb` không hiển thị `(healthy)`; CSDL bị trống trơn nếu không chạy script seed thủ công.
4. **Nguyên nhân gốc rễ:** `docker-compose.yml` thiếu khối `healthcheck:` cho `mongodb` và `Dockerfile` chưa gọi script seed khi khởi động.
5. **Cách sửa:** Thêm healthcheck `mongosh --eval 'db.adminCommand("ping")'`; đổi CMD Dockerfile thành `python seeds/seed.py || true; uvicorn src.app:app ...`.
6. **Link commit:** https://github.com/Johnny120905/CDTN01/commit/23f1563 (và `bbb5232`).
7. **Xác nhận:** `docker compose ps` hiển thị cả 2 container đều `Up ... (healthy)`, truy vấn API có đủ 40 linh kiện ngay.

### BUG-04: Cột Tồn kho hiển thị `undefined` trên Bảng cảnh báo thiếu hàng của Quản lý kho
1. **Mã và mức độ:** `BUG-04` — **MAJOR** (Lỗi hiển thị dữ liệu sai lệch trên UI).
2. **Phát hiện bởi test case:** `test_01_cross_role_flow_export_triggers_manager_alert` (`tests/cross_role_and_ui.test.py`).
3. **Triệu chứng:** Dashboard Quản lý kho hiển thị dòng chữ: *"Tồn hiện tại: undefined / Ngưỡng: 15"*.
4. **Nguyên nhân gốc rễ:** Dòng 1848 `src/static/app.js` truy cập thuộc tính `a.current_stock`, trong khi API trả về tên trường chuẩn là `quantity`.
5. **Cách sửa:** Sửa thành toán tử nullish coalescing: `const currentQty = a.quantity ?? a.current_stock ?? 0;`.
6. **Link commit:** https://github.com/Johnny120905/CDTN01/commit/23f1563.
7. **Xác nhận:** Giao diện hiển thị sắc nét *"Tồn hiện tại: 8 / Ngưỡng: 10"*, tỷ lệ chữ `undefined` bằng 0%.

### BUG-05: Hệ thống thiếu hoàn toàn thao tác Xóa (DELETE), không đạt tiêu chí SE S1
1. **Mã và mức độ:** `BUG-05` — **CRITICAL** (Không thỏa mãn tiêu chí kỹ thuật tối thiểu [SE] S1 theo Bảng 4.2).
2. **Phát hiện bởi:** Nhận xét phản hồi trực tiếp của Giảng viên hướng dẫn về Bài tập 2.
3. **Triệu chứng:** Hệ thống không có endpoint `DELETE` nào; khi gọi `DELETE /api/v1/inventory/parts/{code}` bị trả về HTTP 405.
4. **Nguyên nhân gốc rễ:** Chưa hiện thực hóa đủ 4 thao tác CRUD cho 2 thực thể cốt lõi `part` và `users`.
5. **Cách sửa:** Hiện thực đủ CRUD và thao tác `DELETE` có ràng buộc an toàn (cấm xóa khi còn tồn kho $> 0$; cấm tự xóa chính mình) tại cả 4 tầng; viết test suite `tests/se_s1_crud.test.py` (11 tests).
6. **Link commit:** https://github.com/Johnny120905/CDTN01/commit/04a015b.
7. **Test case phòng ngừa:** 11/11 tests trong `tests/se_s1_crud.test.py` đạt **PASS 100%**.

---

## MỤC 4: DEPLOYMENT GUIDE (ENGLISH - 5 MANDATORY SECTIONS)

### 4.1. Prerequisites
- **Operating System:** Windows 10/11 64-bit, macOS 12+, or Ubuntu 20.04+ LTS.
- **Container Engine:** Docker Desktop `4.25+` / Docker Compose `v2.24+`.
- **Python (Optional for local dev):** Python `3.11.x` (`3.11.5` tested).
- **RAM & Ports:** Minimum `4.0 GB` RAM; Ports `8000` (App & REST API) and `27017` (MongoDB) must be free.

### 4.2. Clone & Environment Configuration
```bash
git clone https://github.com/Johnny120905/CDTN01.git
cd CDTN01
cp .env.example .env
```

### 4.3. Launch Instructions (<= 2 Commands)
```bash
# Command 1 (Environment setup):
cp .env.example .env

# Command 2 (Single-command launch):
docker compose up -d --build
```

### 4.4. Verification Steps (Sanity Checks)
1. **Container Health:** Run `docker compose ps` $\rightarrow$ both `mekong_crm_l5_app` and `mekong_crm_l5_mongodb` must show `Up ... (healthy)`.
2. **Web Application:** Open `http://localhost:8000` in browser $\rightarrow$ Dark 3D SPA Portal loads immediately.
3. **API Documentation:** Open `http://localhost:8000/docs` $\rightarrow$ Swagger UI loads with 22 operational endpoints.
4. **Run Automated Test Suite:**
   ```bash
   docker compose exec mekong-l5-app pytest tests/ -v
   # Or locally: pytest tests/ -v
   # Result: 67 passed, 100% PASS in ~3.0 seconds
   ```
5. **Pre-seeded Accounts (RBAC):**
   - Inventory Manager (`MANAGER`): `lethithuyngan985@gmail.com` / Password: `Le090805!`
   - Material Specialist (`MATERIAL_STAFF`): `huynhnguyenbaongoc2k5@gmail.com` / Password: `Huynh120905!`
   - Technical Staff (`TECH_STAFF`): `vuthelong1009@gmail.com` / Password: `Vu100905!`

### 4.5. Troubleshooting & Rollback
- *Port 8000 already in use:* Edit `API_PORT=8080` in `.env` and `docker-compose.yml`.
- *Database reset:* Run `docker compose down -v && docker compose up -d --build` to re-seed clean data.

---

## MỤC 5: CHECKLIST BẢO MẬT 7 MỤC ĐÃ TỰ ĐÁNH GIÁ CÓ MINH CHỨNG

| STT | Mục Kiểm Tra Bảo Mật | Trạng Thái | Dòng Minh Chứng Cụ Thể |
| :-: | :--- | :---: | :--- |
| **1** | **Không có secret nào trong repo** | **ĐÃ LÀM** | `git grep -i "mongodb+srv://"` trả về 0 kết quả; `.gitignore` chặn triệt để `.env`; `.env.example` chỉ chứa chuỗi mẫu `localhost:27017`. |
| **2** | **Dữ liệu vào được kiểm ở tầng ứng dụng** | **ĐÃ LÀM** | `src/validators/inventory.validator.py` kiểm định regex email, mật khẩu 4 nhóm ký tự, biên số lượng $1 \le Q \le 1,000,000$, bắt buộc `ticket_id` theo `BR-02`. |
| **3** | **Kiểm soát truy cập theo chủ sở hữu (A01 OWASP)** | **ĐÃ LÀM** | `src/routes/inventory.routes.py` trích xuất `center_id` từ JWT; request can thiệp chi nhánh khác bị ném `UnauthorizedCenterError` (HTTP 403); `test_10` đạt **PASS**. |
| **4** | **Mật khẩu và dữ liệu nhạy cảm được băm** | **ĐÃ LÀM** | `src/repositories/inventory.repository.py` chỉ lưu chuỗi băm `password_hash` (SHA-256), xóa bỏ 100% mật khẩu thô trong CSDL và RAM; `test_09` đạt **PASS**. |
| **5** | **Thông báo lỗi không lộ cấu trúc bên trong** | **ĐÃ LÀM** | `custom_app_error_handler` trong `src/app.py` chuẩn hóa 100% lỗi thành `AppError` JSON; tỷ lệ lộ lỗi 500 hay Traceback là `0.0%`; `test_10` đạt **PASS**. |
| **6** | **Nhật ký không ghi dữ liệu nhạy cảm** | **ĐÃ LÀM** | Collection `part_transaction` chỉ lưu vết nghiệp vụ (`transaction_id, center_id, part_code, type, quantity, ticket_id`), không ghi mật khẩu hay token. |
| **7** | **Phụ thuộc được ghim phiên bản chặt chẽ** | **ĐÃ LÀM** | `requirements.txt` ghim 100% phiên bản bằng dấu `==` (`fastapi==0.162.0`, `pymongo==4.19.0`, `pyjwt==2.15.1`, `pytest==9.2.0`); không có cảnh báo lỗ hổng High/Critical. |

---

## MỤC 6: TÀI LIỆU KỸ THUẬT THEO TRACK SOFTWARE ENGINEERING (SE)

Hệ thống đáp ứng trọn vẹn 4 tiêu chí chuyên ngành Software Engineering (`SE`):

1. **Tiêu chí `[SE] S1`: Hợp đồng API và Tài liệu Kỹ thuật đầy đủ mọi Endpoint**
   - Tài liệu kỹ thuật chuẩn OpenAPI 3.0 xuất tại [docs/api-docs/openapi.json](file:///d:/Hoc/DH/N4/N4.HK01\CDTN01\docs\api-docs\openapi.json) gồm đủ **22 endpoints**.
   - Cẩm nang tra cứu [docs/api-docs/README.md](file:///d:/Hoc/DH/N4/N4.HK01\CDTN01\docs\api-docs\README.md) mô tả chi tiết đủ 7 mục cho từng endpoint (Method, Path, Business Description, Auth, Request Body, Success Response JSON thật, Error Table và Limits).
   - Đầy đủ 4 thao tác CRUD (**C**reate, **R**ead, **U**pdate, **D**elete) cho 2 thực thể cốt lõi `part` và `users`.
2. **Tiêu chí `[SE] S2`: Kiểm thử Phân quyền Kiểm soát Truy cập theo Chủ sở hữu (A01 OWASP)**
   - Hiện thực tại `src/routes/inventory.routes.py`: Chặn mọi truy cập chéo chi nhánh giữa `L5-WH-890` (Quận 1) và `L5-WH-891` (Quận 3) với mã HTTP 403 `ERR_UNAUTHORIZED_CENTER`.
   - Kiểm chứng tự động qua ca test `test_10_security_s2_center_isolation` đạt **PASS 100%**.
3. **Tiêu chí `[SE] S3`: Mật khẩu trong CSDL là Chuỗi Băm, Tuyệt đối Không Lưu Dạng Rõ**
   - 100% mật khẩu người dùng được băm qua thuật toán mật mã SHA-256 / Bcrypt; không có trường `password` thô nào trong MongoDB hay tệp JSON.
   - Kiểm chứng tự động qua ca test `test_09_security_s3_password_never_stored_as_plaintext` đạt **PASS 100%**.
4. **Tiêu chí `[SE] S4`: Phản hồi Lỗi Không Lộ Vết Ngăn Xếp (Stack Trace)**
   - Toàn bộ ngoại lệ hệ thống được bắt tập trung tại `custom_app_error_handler` (`src/app.py`), trả về JSON chuẩn `{"status": "error", "error_code", "message"}` bằng tiếng Việt thân thiện, không bao giờ lộ Traceback hay tên bảng CSDL.
   - Kiểm chứng tự động qua ca test `test_10_security_s4_error_response_no_stack_trace` đạt **PASS 100%**.

---

## MỤC 7: ẢNH CHỤP MINH CHỨNG VÀ KẾT QUẢ PHÉP THỬ MÁY TRẮNG

1. **Minh chứng 1: Toàn bộ 67 Ca Kiểm thử Tự động PASS 100% bằng 1 Lệnh:**
   - Lệnh thực thi: `python -m pytest tests/ -v` (thời gian chạy: 3.09 giây).
   - Ảnh chụp minh chứng: [docs/screenshots/test_pytest_pass.png](file:///d:/Hoc/DH/N4/N4.HK01\CDTN01\docs\screenshots\test_pytest_pass.png).
2. **Minh chứng 2: Khởi dựng Thành công từ Máy Trắng bằng Docker Compose:**
   - Lệnh thực thi: `docker compose up -d --build` (Cả 2 container đều đạt trạng thái `healthy`).
   - Ảnh chụp minh chứng: [docs/screenshots/docker_compose_up.png](file:///d:/Hoc/DH/N4/N4.HK01\CDTN01\docs\screenshots\docker_compose_up.png).
3. **Minh chứng 3: Ba Trạng thái Giao diện Chuẩn mực (Loading, Empty, Error):**
   - Đang tải (Loading): [docs/screenshots/ui_loading_state.png](file:///d:/Hoc/DH/N4/N4.HK01\CDTN01\docs\screenshots\ui_loading_state.png).
   - Rỗng (Empty): [docs/screenshots/ui_empty_state.png](file:///d:/Hoc/DH/N4/N4.HK01\CDTN01\docs\screenshots\ui_empty_state.png).
   - Lỗi (Error): [docs/screenshots/ui_error_state.png](file:///d:/Hoc/DH/N4/N4.HK01\CDTN01\docs\screenshots\ui_error_state.png).

---

## PHỤ LỤC BẮT BUỘC: BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ TRÍ TUỆ NHÂN TẠO (AI)

*(Tuân thủ theo Mục 3.1 & Tiêu chí C8 Đề bài BT3)*

| STT | Công cụ AI sử dụng | Mục đích sử dụng cụ thể | Phạm vi kết quả do AI tạo ra | Đánh giá, hiệu chỉnh và kiểm chứng của sinh viên |
| :-: | :--- | :--- | :--- | :--- |
| 1 | **Antigravity AI (Google DeepMind)** | Hỗ trợ phân tích mã nguồn, sinh khung test suite Pytest đa tầng, cấu hình Docker Compose và gỡ lỗi hiển thị UI. | Khung kiểm thử tự động ban đầu, cấu hình healthcheck container và gợi ý logic toán tử nullish coalescing. | Sinh viên trực tiếp đọc hiểu 100% mã nguồn, tự tay viết các hàm kiểm thử biên hai phía, kiểm chứng tính đúng đắn trên terminal đạt kết quả 67/67 tests PASS và xác thực trạng thái container healthy. |
| 2 | **ChatGPT (OpenAI GPT-4o)** | Tham khảo cú pháp kiểm thử phân quyền theo chuẩn OWASP Top 10 A01 và kỹ thuật băm mật khẩu bảo mật S3. | Gợi ý cấu trúc request header mô phỏng truy cập chéo chi nhánh và đoạn mã băm SHA-256 an toàn. | Sinh viên kiểm tra tính tương thích với PyMongo và FastAPI, tự viết các test case bảo mật trong `bt3_specification_and_constraints.test.py` và chạy xác minh thực tế 100% PASS. |
| 3 | **Claude (Anthropic 3.5 Sonnet)** | Hỗ trợ soát lỗi chính tả và chuẩn hóa văn phong tiếng Anh kỹ thuật cho Deployment Guide và API Documentation. | Bản nháp tiếng Anh của 5 mục trong `deployment-guide.md` và tài liệu hợp đồng API. | Sinh viên tự tay rà soát đối chiếu từng tham số, đảm bảo các câu lệnh sao chép được và hoạt động chính xác trên cả Windows lẫn Linux. |

**Cam đoan của sinh viên:** Tôi xin cam đoan toàn bộ nội dung khai báo sử dụng công cụ Trí tuệ Nhân tạo (AI) nêu trên là hoàn toàn trung thực. Toàn bộ mã nguồn, cấu hình hệ thống và dữ liệu kiểm thử đã được tôi trực tiếp kiểm tra, tinh chỉnh và chạy kiểm thử thành công trên môi trường thực tế.

*TP. Hồ Chí Minh, ngày 12 tháng 11 năm 2026*  
**Sinh viên thực hiện**  
*(Đã ký)*  
**Huỳnh Nguyễn Bảo Ngọc**


# NHẬT KÝ THEO DÕI VÀ GỠ LỖI (BUG LOG) — BÀI TẬP 3
*(Defect Tracking & Resolution Log: >= 3 Bugs with 7 Required Fields & Commit Links)*

- **Hệ thống:** Smart CRM – Mekong Mobile | **Luồng 05:** Kho linh kiện thay thế
- **Sinh viên:** Huỳnh Nguyễn Bảo Ngọc — **MSSV:** `2374802010339` | **Track:** Software Engineering (`SE`)
- **Kho mã nguồn:** https://github.com/Johnny120905/CDTN01.git

---

## 1. Bảng Tổng hợp Danh mục Lỗi đã Gỡ

| Mã Lỗi | Mức độ | Tóm tắt sự cố kỹ thuật | Tệp mã nguồn liên quan | Trạng thái |
| :---: | :---: | :--- | :--- | :---: |
| **BUG-01** | **CRITICAL** | Lưu trữ mật khẩu dạng rõ (*Plaintext*) trong CSDL và RAM khi Đăng ký và Đặt lại mật khẩu. | `src/routes/inventory.routes.py`, `src/repositories/inventory.repository.py` | **ĐÃ SỬA TRIỆT ĐỂ** |
| **BUG-02** | **MAJOR** | Lỗ hổng bỏ quên kiểm tra thời hạn hiệu lực 10 phút của mã OTP xác thực khôi phục mật khẩu. | `src/routes/inventory.routes.py` (`verify_otp_endpoint`, `reset_password`) | **ĐÃ SỬA TRIỆT ĐỂ** |
| **BUG-03** | **MAJOR** | Docker Compose thiếu Healthcheck cho dịch vụ MongoDB và thiếu tự động nạp seed khi khởi dựng máy trắng. | `docker-compose.yml`, `Dockerfile` | **ĐÃ SỬA TRIỆT ĐỂ** |
| **BUG-04** | **MAJOR** | Bảng cảnh báo thiếu hàng của Quản lý kho hiển thị `undefined` ở cột tồn kho do đọc sai tên thuộc tính. | `src/static/app.js` (`renderManagerDashboard`) | **ĐÃ SỬA TRIỆT ĐỂ** |
| **BUG-05** | **CRITICAL** | API chưa đủ 4 thao tác CRUD (thiếu hoàn toàn thao tác xóa DELETE), không đạt tiêu chí SE S1. | `src/repositories/inventory.repository.py`, `src/services/inventory.service.py`, `src/routes/inventory.routes.py` | **ĐÃ SỬA TRIỆT ĐỂ** |

---

## 2. Chi tiết Từng Lỗi đã Gỡ (Đủ 7 Dòng Quy Chuẩn Mục 2.3)

### BUG-01: Lỗ hổng lưu trữ mật khẩu dạng rõ trong CSDL và RAM (Vi phạm tiêu chuẩn SE S3)
1. **Mã và mức độ:** `BUG-01` — **CRITICAL** (Lỗ hổng bảo mật rò rỉ thông tin xác thực người dùng).
2. **Phát hiện bởi test case nào:** Phát hiện qua ca kiểm thử `test_09_security_s3_password_never_stored_as_plaintext` trong tệp [tests/bt3_specification_and_constraints.test.py](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/tests/bt3_specification_and_constraints.test.py).
3. **Triệu chứng:** Khi người dùng thực hiện Đăng ký tài khoản (`POST /api/v1/auth/register`) hoặc Đặt lại mật khẩu (`POST /api/v1/auth/reset-password`), bản ghi người dùng trong CSDL MongoDB và tệp dự phòng `data/users_store.json` xuất hiện trường `password: "Password123@"` dạng rõ, có thể đọc được bằng mắt thường.
4. **Cách tái lập:**
   - Bước 1: Gửi request `POST /api/v1/auth/register` với mật khẩu `"Password123@"`.
   - Bước 2: Mở MongoDB Compass hoặc tệp `data/users_store.json` kiểm tra tài khoản vừa tạo.
   - Kết quả: Thấy trường `"password": "Password123@"` nằm song song với `"password_hash"`.
5. **Nguyên nhân:** Trong hàm `register()` tại [src/routes/inventory.routes.py](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/src/routes/inventory.routes.py) và hàm `create_user()`, `update_user_password()` tại [src/repositories/inventory.repository.py](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/src/repositories/inventory.repository.py), lập trình viên đã gán trực tiếp tham số mật khẩu thô vào tài liệu lưu trữ (`user_doc["password"] = raw_pwd`) để phục vụ kiểm thử nhanh ban đầu mà quên loại bỏ trước khi ghi xuống đĩa.
6. **Cách sửa:**
   - Xóa bỏ hoàn toàn thuộc tính `"password"` khỏi từ điển `user_doc` trước khi gọi `create_user()`.
   - Cập nhật hàm `create_user()` và `update_user_password()` trong Repository chỉ tiếp nhận và lưu duy nhất chuỗi băm an toàn `password_hash`.
   - Viết script quét sạch toàn bộ các trường `password` dạng rõ còn sót lại trong `data/users_store.json`.
7. **Link commit và xác nhận:**
   - Commit: `23a7755` & `e6698d5` (và commit hoàn thiện BT3).
   - Xác nhận: Chạy `pytest tests/bt3_specification_and_constraints.test.py -k test_09` đạt kết quả **PASSED**. Kiểm tra tệp JSON xác nhận không còn bất kỳ mật khẩu dạng rõ nào.

---

### BUG-02: Bỏ quên kiểm tra thời gian hết hạn của mã OTP xác thực khôi phục mật khẩu
1. **Mã và mức độ:** `BUG-02` — **MAJOR** (Lỗi logic xác thực người dùng, nguy cơ tấn công vét cạn OTP cũ).
2. **Phát hiện bởi test case nào:** Phát hiện qua ca kiểm thử biên thời gian xác thực OTP trong [tests/bt3_specification_and_constraints.test.py](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/tests/bt3_specification_and_constraints.test.py).
3. **Triệu chứng:** Mã OTP sinh ra đã quá 10 phút (thậm chí qua ngày hôm sau) nhưng khi người dùng gửi request `POST /api/v1/auth/verify-otp` hoặc `/reset-password` thì hệ thống vẫn chấp nhận và cho phép đặt lại mật khẩu mới thành công thay vì báo lỗi hết hạn.
4. **Cách tái lập:**
   - Bước 1: Yêu cầu cấp OTP qua `POST /api/v1/auth/forgot-password`.
   - Bước 2: Chỉnh sửa thời gian trường `otp_expires_at` trong CSDL lùi về 1 giờ trước (`datetime.utcnow() - timedelta(hours=1)`).
   - Bước 3: Gửi `POST /api/v1/auth/reset-password` với mã OTP cũ.
   - Kết quả: API trả về HTTP 200 thành công thay vì ném lỗi HTTP 400 `ERR_OTP_EXPIRED`.
5. **Nguyên nhân:** Trong cả hai hàm `verify_otp_endpoint()` và `reset_password()` tại [src/routes/inventory.routes.py](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/src/routes/inventory.routes.py), mã nguồn chỉ so sánh chuỗi `if not stored_otp or stored_otp != otp:` mà hoàn toàn không so sánh trường thời gian `user.get("otp_expires_at")` với thời điểm hiện tại `datetime.utcnow()`.
6. **Cách sửa:**
   - Bổ sung đoạn mã trích xuất `otp_expires_at`, chuyển đổi sang đối tượng `datetime` và kiểm tra điều kiện `if datetime.utcnow() > exp_dt: raise AppError(400, "ERR_OTP_EXPIRED", "Mã OTP đã hết thời gian hiệu lực 10 phút.")`.
   - Sau khi đặt lại mật khẩu thành công, lập tức gọi `$unset` xóa sạch cả `otp_code` và `otp_expires_at` để ngăn chặn việc tái sử dụng mã một lần.
7. **Link commit và xác nhận:**
   - Commit: `23a7755` (và commit hoàn thiện BT3).
   - Xác nhận: Kiểm thử tự động với mốc thời gian quá hạn $t = 10m01s$ trả về đúng mã lỗi `400 ERR_OTP_EXPIRED`.

---

### BUG-03: Docker Compose thiếu Healthcheck cho MongoDB và thiếu tự động nạp hạt giống khi dựng máy trắng
1. **Mã và mức độ:** `BUG-03` — **MAJOR** (Ảnh hưởng trực tiếp đến Tiêu chí Cốt lõi C1 - Phép thử máy trắng).
2. **Phát hiện bởi test case nào:** Phát hiện khi tự thực hiện Phép thử máy trắng (Mục 2.4 Đề bài BT3) bằng lệnh `docker compose up -d --build` từ thư mục sạch.
3. **Triệu chứng:** Khi chạy `docker compose ps`, dịch vụ `mongodb` không hiển thị trạng thái `(healthy)`. Đồng thời do chuỗi `MONGO_URI` trong `.env.example` mặc định là `localhost:27017`, container ứng dụng `mekong-l5-app` không thể kết nối tới `mongodb` qua mạng Docker Bridge và CSDL MongoDB bị trống trơn nếu không chạy script seed thủ công.
4. **Cách tái lập:**
   - Bước 1: Xóa sạch container và volume bằng `docker compose down -v`.
   - Bước 2: Sao chép `cp .env.example .env` và chạy `docker compose up -d --build`.
   - Bước 3: Chạy `docker compose ps` kiểm tra trạng thái dịch vụ.
   - Kết quả: `mongodb` chỉ hiện `Up` (không có `healthy`), CSDL chưa có sẵn 40 linh kiện mẫu.
5. **Nguyên nhân:** Tệp [docker-compose.yml](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docker-compose.yml) ban đầu chưa khai báo khối `healthcheck:` cho service `mongodb`, chưa cấu hình `depends_on: mongodb: condition: service_healthy`, và chuỗi kết nối trong container mạng nội bộ cần trỏ tới hostname `mongodb` thay vì `localhost`.
6. **Cách sửa:**
   - Bổ sung `healthcheck:` vào service `mongodb` sử dụng lệnh `mongosh --eval 'db.adminCommand("ping")'`.
   - Cấu hình biến `MONGO_URI=mongodb://mongodb:27017/${DB_NAME:-mekong_mobile_l5}` trực tiếp trong `environment` của `mekong-l5-app`.
   - Cập nhật lệnh khởi động của [Dockerfile](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/Dockerfile) thành: `CMD ["sh", "-c", "python seeds/seed.py || true; uvicorn src.app:app --host 0.0.0.0 --port 8000"]` để tự động nạp đủ 40 linh kiện ngay khi container khởi động lần đầu.
7. **Link commit và xác nhận:**
   - Commit: `23f1563` & `23a7755` (và commit hoàn thiện BT3).
   - Xác nhận: Chạy `docker compose ps` thấy cả 2 container đều đạt trạng thái `Up ... (healthy)`, truy vấn `GET /api/v1/inventory/parts` có đủ 40 linh kiện ngay lập tức.

---

### BUG-04: Cột Tồn kho hiển thị `undefined` trên Bảng cảnh báo thiếu hàng của Quản lý kho
1. **Mã và mức độ:** `BUG-04` — **MAJOR** (Lỗi hiển thị dữ liệu sai lệch trên giao diện người dùng).
2. **Phát hiện bởi test case nào:** Phát hiện khi chạy giao diện thực tế tại `http://localhost:8000/` và đối chiếu với ca kiểm thử `test_01_cross_role_flow_export_triggers_manager_alert` trong [tests/cross_role_and_ui.test.py](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/tests/cross_role_and_ui.test.py).
3. **Triệu chứng:** Khi linh kiện bị xuất dưới ngưỡng an toàn, Dashboard của Quản lý kho hiển thị bảng viền đỏ thông báo linh kiện thiếu hụt, nhưng tại cột số lượng lại hiển thị dòng chữ: *"Tồn hiện tại: undefined / Ngưỡng: 15"*.
4. **Cách tái lập:**
   - Bước 1: Đăng nhập vai trò `MANAGER`.
   - Bước 2: Quan sát khối "CẢNH BÁO LINH KIỆN DƯỚI NGƯỠNG AN TOÀN" trên Dashboard.
   - Kết quả: Thấy xuất hiện chữ `undefined` tại vị trí số tồn kho.
5. **Nguyên nhân:** Trong hàm `renderManagerDashboard()` tại dòng 1848 của [src/static/app.js](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/src/static/app.js), đoạn mã JavaScript cố tình truy cập vào thuộc tính `a.current_stock`, trong khi API Backend `/api/v1/inventory/alerts/threshold` và hàm `get_low_stock_alerts()` trả về đối tượng với tên trường chuẩn hóa là `quantity`.
6. **Cách sửa:** Sửa dòng 1848 thành toán tử nullish coalescing đa tầng: `const currentQty = a.quantity ?? a.current_stock ?? 0;` đồng thời đồng bộ sửa trên cả [frontend/public/app.js](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/frontend/public/app.js) và [backend/src/static/app.js](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/backend/src/static/app.js).
7. **Link commit và xác nhận:**
   - Commit: `23f1563` (Thông điệp: `docs(readme): hoan thien README goc doi chieu BT1-BT2-BT3, sua hien thi canh bao kho va cap nhat ho so (v0.2)`).
   - Xác nhận: Kiểm tra giao diện Dashboard Quản lý kho hiển thị số tồn kho sắc nét (ví dụ: *"Tồn hiện tại: 8 / Ngưỡng: 10"*), tỷ lệ chữ `undefined` trên toàn hệ thống bằng đúng `0%`.

---

### BUG-05: Hệ thống thiếu hoàn toàn thao tác Xóa (DELETE), không đạt tiêu chí SE S1 trong Bảng 4.2 BT2
1. **Mã và mức độ:** `BUG-05` — **CRITICAL** (Không thỏa mãn tiêu chí kỹ thuật tối thiểu chuyên ngành [SE] S1 theo Bảng 4.2).
2. **Phát hiện bởi test case nào:** Phát hiện qua phản hồi nhận xét trực tiếp của Giảng viên hướng dẫn (TS. Nguyễn Trí Hải) tại Bài tập 2: *"API chưa đủ bốn thao tác CRUD (không có xoá). Mục kiểm chứng (bảng 4.2) chưa đạt: S1"*.
3. **Triệu chứng:** Hệ thống chỉ có các phương thức `GET` và `POST`/`PUT` cập nhật ngưỡng; không có bất kỳ endpoint `DELETE` nào để gỡ bỏ linh kiện hư hại lỗi thời hoặc xóa tài khoản nhân sự nghỉ việc. Khi gọi `DELETE /api/v1/inventory/parts/{part_code}` hoặc `DELETE /api/v1/inventory/users/{email}`, máy chủ trả về mã HTTP `405 Method Not Allowed`.
4. **Cách tái lập:**
   - Bước 1: Gửi request `DELETE /api/v1/inventory/parts/PRT-IP15-SCR` kèm Bearer Token Quản lý kho.
   - Bước 2: Quan sát mã trạng thái phản hồi.
   - Kết quả: Máy chủ trả về HTTP 405 Method Not Allowed do chưa khai báo Route tiếp nhận.
5. **Nguyên nhân:** Khi hiện thực hóa Sprint 2 ở BT2, nhóm phát triển ưu tiên luồng giao dịch xuất nhập kho nên chỉ hiện thực thao tác Read/Update ngưỡng và Import nhân sự mà chưa xây dựng đầy đủ 4 thao tác CRUD chuẩn hóa cho 2 thực thể cốt lõi `part` và `users`.
6. **Cách sửa:**
   - Tại `src/repositories/inventory.repository.py`: Bổ sung `create_part()`, `update_part()`, `delete_part()`, `update_user_profile()`, `delete_user()`.
   - Tại `src/services/inventory.service.py`: Tích hợp các ràng buộc an toàn: Không cho phép xóa linh kiện nếu còn tồn kho thực tế $> 0$ (`ERR_CANNOT_DELETE_ACTIVE_STOCK`); cấm Quản lý tự xóa tài khoản của chính mình (`ERR_CANNOT_DELETE_SELF`).
   - Tại `src/routes/inventory.routes.py`: Khai báo đủ 8 endpoints CRUD mới cho `parts` và `users`.
   - Viết bộ kiểm thử chuyên biệt `tests/se_s1_crud.test.py` với 11 test cases kiểm thử tự động toàn diện.
7. **Link commit và xác nhận:**
   - Commit: `04a015b` (Thông điệp: `fix(bt2): khac phuc toan dien nhan xet BT2 - bo sung CRUD S1 (thao tac xoa cho part va users), bao cao chuan 7 muc 8 trang, giu tag v0.2 ban nop 29/10`).
   - Xác nhận: 11/11 ca kiểm thử trong `tests/se_s1_crud.test.py` đạt **100% PASSED**. Đạt chuẩn tiêu chí `[SE] S1` trong Bảng 4.2.

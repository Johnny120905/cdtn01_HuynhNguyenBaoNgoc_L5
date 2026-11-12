# KẾ HOẠCH KIỂM THỬ RÚT GỌN (TEST PLAN) — BÀI TẬP 3
*(Short Test Plan: Scope, Layers, Quantifiable Criteria & Test Data)*

- **Học phần:** Chuyên đề Tốt nghiệp 1 (Học kỳ 1, Năm học 2026 – 2027)
- **Hệ thống:** Smart CRM – Mekong Mobile | **Phân hệ:** Luồng 05 (`L5`) – Quản lý Kho linh kiện thay thế
- **Chuyên ngành:** Công nghệ phần mềm (`Track SE`)
- **Sinh viên:** Huỳnh Nguyễn Bảo Ngọc — **MSSV:** `2374802010339` | **Lớp:** `261_71ITGR40203_06`
- **Giảng viên hướng dẫn:** TS. Nguyễn Trí Hải
- **Mã nguồn GitHub:** https://github.com/Johnny120905/cdtn01_HuynhNguyenBaoNgoc_L5.git (Tag `v1.0`)

---

## 1. Phạm vi kiểm thử và phần chủ ý KHÔNG kiểm

### 1.1. Phạm vi ĐƯỢC kiểm thử (In-Scope)
- **Toàn bộ 5 quy tắc nghiệp vụ cốt lõi:**
  - `BR-01`: Chống tồn kho âm ($Q_{request} \le Q_{stock}$).
  - `BR-02`: Bắt buộc chứng từ phiếu bảo hành hợp lệ và đang mở (`OPEN`, `IN_PROGRESS`) khi xuất/hoàn kho (`UC-99`).
  - `BR-03`: Sổ cái giao dịch bất biến (*Immutable Append-Only Audit Log*), không có API sửa/xóa giao dịch.
  - `BR-04`: Phân mảnh dữ liệu theo trung tâm (*Center Isolation* `L5-WH-890` vs `L5-WH-891` theo chuẩn `A01 OWASP`).
  - `BR-05`: Tự động đánh giá cờ cảnh báo an toàn thời gian thực (`NORMAL` khi $Q > Q_{min}$, `WARNING` khi $Q \le Q_{min}$).
- **Cơ chế kiểm soát tranh chấp đồng thời:** Khóa lạc quan (*Optimistic Locking* kiểm tra trường `version` trong CSDL NoSQL chống Race Condition `NFR-03` / `EX-05`).
- **Phân hệ Xác thực & Phân quyền RBAC:** Đăng ký cấp quyền (mật khẩu 8 ký tự, 4 nhóm), Đăng nhập cấp JWT (24h), Quên mật khẩu OTP (10 phút có đồng hồ đếm ngược), Khóa vĩnh viễn tài khoản thôi việc (`TERMINATED` HTTP 403).
- **Trải nghiệm giao diện UI/UX:** 13 màn hình SPA Dark 3D Elevation, phông chữ *Be Vietnam Pro*, chuyển ngữ 100% tiếng Việt, tìm kiếm thông minh có gợi ý dropdown và phím Enter, xóa sạch form bằng nút Đặt lại biểu mẫu.
- **Tiêu chuẩn đóng gói Container:** Khởi dựng toàn bộ hệ thống bằng $\le 2$ lệnh qua Docker Compose kèm Healthcheck tự động và nạp hạt giống Idempotent.

### 1.2. Phần chủ ý KHÔNG kiểm thử và Lý do kỹ thuật (Out-of-Scope)
| Thành phần chủ ý KHÔNG kiểm | Lý do kỹ thuật & Căn cứ phạm vi |
| :--- | :--- |
| **Gửi email / SMS OTP thật qua Gateway viễn thông** | Hệ thống sử dụng chế độ mô phỏng OTP trực quan (`otp_demo` tự động điền và đồng hồ 10:00) nhằm đảm bảo bài kiểm thử chạy độc lập hoàn toàn (*Self-contained*), không phụ thuộc vào kết nối mạng Internet bên ngoài hay tài khoản dịch vụ trả phí bên thứ ba (Twilio/SendGrid). |
| **Thanh toán tiền mặt / Hóa đơn tài chính VAT** | Thuộc phân hệ Kế toán – Tài chính (Luồng 08), nằm ngoài ranh giới xác lập của Luồng 05 (Quản lý Kho linh kiện thay thế) đã được quy định trong Bản SRS (`docs/srs.md` - Mục 1.2 `WON'T HAVE`). |
| **Tự động đặt hàng NCC khi cạn kho** | Phân hệ chỉ cung cấp danh bạ nhà cung cấp đối tác và cảnh báo thiếu hàng; quyết định ký hợp đồng đặt hàng là nghiệp vụ quản trị chuỗi cung ứng ngoài đời thực, không tự động hóa bằng code. |
| **Kiểm thử xâm nhập chuyên sâu (Penetration Testing) & Tải cực lớn (Stress Testing)** | Đề bài Bài tập 3 quy định rõ các hạng mục này thuộc phạm vi Chuyên đề Tốt nghiệp 2. Ở BT3 tập trung kiểm thử chức năng, biên, ngoại lệ, bảo mật ứng dụng cơ bản (`A01 OWASP`, băm mật khẩu, che giấu lỗi hệ thống) và đóng gói tái lập. |

---

## 2. Loại test và số lượng mỗi tầng

Hệ thống được kiểm thử tự động hóa đa tầng theo mô hình kim tự tháp kiểm thử (*Test Pyramid*):

```text
       /\
      /  \      15 ca E2E & UI Integration Tests (cross_role_and_ui.test.py)
     /    \     -----------------------------------------------------------
    /      \    15 ca Auth, RBAC & Boundary Tests (auth_and_user.test.py)
   /        \   -----------------------------------------------------------
  /          \  11 ca SE S1 CRUD Tests (se_s1_crud.test.py)
 /            \ -----------------------------------------------------------
/              \ 06 ca RESTful API Integration Tests (inventory.routes.test.py)
/                \ ---------------------------------------------------------
/                  \ 20 ca Unit & BT3 Constraint Tests (service & bt3 tests)
=============================================================================
TỔNG CỘNG: 67 TEST CASES TỰ ĐỘNG CHẠY PASS 100% (Bao gồm 11 ca SE S1 CRUD)
```

1. **Tầng Unit Test (Lớp Domain Service & Nghiệp vụ cốt lõi):**
   - **07 ca** trong `tests/inventory.service.test.py`: Ép lỗi xuất âm kho, thiếu ticket, phân quyền vai trò, cập nhật ngưỡng an toàn.
   - **07 ca** trong `tests/bt3_specification_and_constraints.test.py`: Kiểm thử luồng hoàn trả `RETURN`, 4 ca giá trị biên (tồn kho, ngưỡng an toàn), 2 ca ngoại lệ ticket đóng/hủy.
2. **Tầng Integration Test (Lớp Controller, API Routes & Database):**
   - **06 ca** trong `tests/inventory.routes.test.py`: Kiểm thử hợp đồng API (`GET /stock`, `POST /transactions`, `PUT /threshold`).
   - **06 ca** trong `tests/bt3_specification_and_constraints.test.py`: Xung đột Optimistic Locking (HTTP 409), bảo mật phân quyền chi nhánh A01 OWASP (HTTP 403), băm mật khẩu trong CSDL (S3), che giấu vết ngăn xếp (S4), tính lũy đẳng khi chạy seed lần 2 (C8).
   - **11 ca** trong `tests/se_s1_crud.test.py`: Kiểm thử toàn diện 4 thao tác CRUD (Create, Read, Update, Delete) cho cả 2 thực thể `part` và `users`, ràng buộc cấm xóa tồn kho > 0 và cấm tự xóa chính mình.
3. **Tầng Xác thực & Quản trị Nhân sự (Auth & User Management):**
   - **15 ca** trong `tests/auth_and_user.test.py`: Đăng ký, đăng nhập, quên mật khẩu OTP, kiểm định độ phức tạp mật khẩu 4 nhóm ký tự, giới hạn độ dài biên, khóa vĩnh viễn tài khoản `TERMINATED`.
4. **Tầng Giao diện & Luồng liên vai trò (Cross-Role Flow & UI/UX):**
   - **15 ca** trong `tests/cross_role_and_ui.test.py`: Liên thông 3 vai trò (Kỹ thuật xuất kho kích hoạt cảnh báo Quản lý, Vật tư nhập kho tăng tồn Kỹ thuật), bố cục 3D, loại bỏ breadcrumb và mã kỹ thuật, kiểm tra bộ lọc và phân trang.

---

## 3. Tiêu chí thành công ĐO ĐƯỢC (Quantifiable Success Criteria)

Hệ thống được coi là hoàn thành kiểm thử Giai đoạn 3 khi đạt đồng thời các chỉ số định lượng sau:

| Chỉ số kỹ thuật | Ngưỡng cam kết (Target) | Kết quả thực tế đo được | Đánh giá |
| :--- | :---: | :---: | :---: |
| **Tỷ lệ vượt qua kiểm thử (Test Pass Rate)** | **100%** | **67 / 67 PASSED (100%)** | **ĐẠT** |
| **Số lượng lỗi nghiêm trọng (Critical Bugs) đang mở** | **0 lỗi** | **0 lỗi (Đã sửa và ghi Bug Log 5 bug)** | **ĐẠT** |
| **Số lượng lỗi lớn (Major Bugs) đang mở** | **0 lỗi** | **0 lỗi** | **ĐẠT** |
| **Độ bao phủ quy tắc nghiệp vụ cốt lõi (`BR-01..BR-05`)** | **100%** | Mỗi quy tắc có ít nhất 1 test luồng đúng và 1 test biên | **ĐẠT** |
| **Tỷ lệ lộ mã lỗi thô 500 hoặc vết ngăn xếp (*Stack Trace*)** | **0.0%** | **0.0% (100% lỗi qua AppError Handler)** | **ĐẠT** |
| **Số lượng lệnh khởi dựng hệ thống sạch trên Docker** | $\le \mathbf{2}$ **lệnh** | Đúng **2 lệnh** (`cp .env.example .env` & `docker compose up -d --build`) | **ĐẠT** |
| **Trạng thái sức khỏe container sau khởi chạy** | `healthy` | 100% container `mekong-l5-app` và `mongodb` đều `healthy` | **ĐẠT** |
| **Tính lũy đẳng nạp dữ liệu mẫu (*Idempotency*)** | **0 duplicate** | Chạy `python seeds/seed.py` lặp lại 2 lần: dữ liệu không bị nhân đôi | **ĐẠT** |

---

## 4. Môi trường và dữ liệu thử (Test Environment & Fixtures)

- **Môi trường thực thi:**
  - Python `3.11.5`, Pytest `9.2.0`, AnyIO `4.15.1`, FastAPI `0.162.0`, Uvicorn `0.54.0`, PyMongo `4.19.0`.
  - Docker Desktop Container Engine (`mongo:7.0` & `python:3.11-slim`).
  - Hệ điều hành: Windows 11 64-bit / Linux Alpine / Ubuntu 22.04 LTS.
- **Nguồn dữ liệu thử nghiệm:**
  - Bộ dữ liệu hạt giống tại `seeds/001_seed_parts_demo.json` chứa đầy đủ: 2 chi nhánh (`service_center`), 40 linh kiện (`part`), 5 phiếu bảo hành (`ticket`), 75 bản ghi tồn kho (`part_stock`), 5 tài khoản nhân sự chuẩn (`users`) và 5 bản ghi đối soát mẫu (`part_transaction`).
- **Cơ chế cách ly và dọn dẹp dữ liệu thử:**
  - Khi chạy Unit Tests: Lớp `InventoryRepository(connect=False)` khởi tạo dữ liệu trong RAM độc lập (`_memory_store`), hoàn toàn không ghi đè vào CSDL thật.
  - Khi chạy Integration Tests: Các hàm `@classmethod setUpClass` và `tearDownClass` tự động xóa sạch các tài khoản/giao dịch thử nghiệm bằng email tiền tố `test.*`, khôi phục trạng thái CSDL nguyên bản 100% trước và sau mỗi phiên chạy.

---

## Câu trả lời chuẩn mực: "Làm sao em biết là em đã kiểm thử ĐỦ?"

> *"Em có năm quy tắc nghiệp vụ cốt lõi đã hiện thực hóa (`BR-01` đến `BR-05`). Đối với mỗi quy tắc, em đều xây dựng ít nhất một kịch bản kiểm thử luồng đúng (Happy Path) và một kịch bản kiểm thử giá trị biên ở hai bên ranh giới (ví dụ: xuất đúng bằng tồn kho thì thành công đưa tồn về 0, nhưng xuất vượt đúng 1 đơn vị thì lập tức bị chặn với lỗi `NegativeStockError`). Thêm vào đó, em xây dựng các kịch bản kiểm thử dữ liệu sai để xác thực hệ thống phản hồi đúng mã HTTP 400/403/409/422 kèm mã lỗi nghiệp vụ mà không bao giờ bị sập hay lộ vết ngăn xếp; kiểm thử cơ chế Khóa lạc quan chống Race Condition khi có xung đột phiên bản; kiểm thử bảo mật phân quyền chi nhánh theo chuẩn A01 OWASP; kiểm thử tiêu chí chuyên ngành SE S1 với đầy đủ 11 ca kiểm thử CRUD và thao tác XÓA an toàn; và kiểm thử tính lũy đẳng khi nạp hạt giống lặp lại. Toàn bộ 67 kịch bản kiểm thử tự động đều tự dựng và tự dọn dữ liệu sạch sẽ, chạy đạt kết quả tuyệt đối 100% PASSED. Em chủ ý không kiểm thử việc gửi email thật ra Internet vì hệ thống đã có bộ mô phỏng OTP tự động nhằm bảo đảm tính độc lập khi người khác dựng lại từ máy trắng — em đã ghi rõ điều này tại Mục 1 của Test Plan."*

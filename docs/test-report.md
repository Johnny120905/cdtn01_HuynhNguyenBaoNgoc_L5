# BÁO CÁO KẾT QUẢ KIỂM THỬ THỰC TẾ (TEST REPORT) — BÀI TẬP 3
*(Test Execution Report: 13 Core Test Cases with 8 Required Columns)*

- **Hệ thống:** Smart CRM – Mekong Mobile | **Luồng 05:** Kho linh kiện thay thế
- **Chuyên ngành:** Công nghệ phần mềm (`Track SE`)
- **Sinh viên:** Huỳnh Nguyễn Bảo Ngọc — **MSSV:** `2374802010339` | **Lớp:** `261_71ITGR40203_06`
- **Công cụ thực thi:** `pytest 9.2.0` trên nền `Python 3.11.5`
- **Tổng số ca kiểm thử:** 13 ca kiểm thử đại diện chạy thật đủ 8 cột (trích xuất từ bộ 67 ca kiểm thử tự động toàn diện)
- **Tỷ lệ đạt:** **13 / 13 PASSED (100%)** | Toàn bộ suite: **67 / 67 PASSED (100%)**

---

## Bảng Báo cáo 13 Test Case đã Chạy Thật Đủ 8 Cột Chuẩn Mục 2.2

| Mã Test | Tiền điều kiện | Các bước thực hiện | Dữ liệu thử nghiệm | Kết quả mong đợi | Mức ưu tiên | Kết quả thực tế | Trạng thái |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- | :---: |
| **TC-01** *(Luồng đúng BR-01)* | Linh kiện `SCR-IP14-01` có tồn kho = 10 tại `L5-WH-890`, phiếu `TK-1092` trạng thái `OPEN`. | 1. Đăng nhập Kỹ thuật viên.<br>2. Gọi `POST /transactions` với `type: OUT`. | `part_code: "SCR-IP14-01"`, `quantity: 3`, `ticket_id: "TK-1092"`. | HTTP 201 Created, trả về `transaction_id`, tồn kho giảm từ 10 xuống 7. | **CRITICAL** | HTTP 201, `transaction_id` sinh mới, tồn kho đo được đúng 7 cái. | **PASS** |
| **TC-02** *(Luồng đúng BR-02)* | Linh kiện `BAT-IP13-01` có tồn kho = 8, phiếu bảo hành `TK-1093` mở. | 1. Đăng nhập Kỹ thuật viên.<br>2. Xuất kho linh kiện pin kèm mã phiếu. | `part_code: "BAT-IP13-01"`, `type: "OUT"`, `quantity: 1`, `ticket_id: "TK-1093"`. | Ghi nhận giao dịch thành công, bản ghi có gắn chặt mã phiếu bảo hành. | **CRITICAL** | Giao dịch tạo thành công, trường `ticket_id` khớp `TK-1093`. | **PASS** |
| **TC-03** *(Luồng đúng FR-03 / RETURN)* | Linh kiện `SCR-IP14-01` có tồn = 10, Kỹ thuật viên có linh kiện dư sau sửa chữa. | 1. Đăng nhập Kỹ thuật viên.<br>2. Lập lệnh hoàn trả `RETURN` kèm mã phiếu `TK-1092`. | `part_code: "SCR-IP14-01"`, `type: "RETURN"`, `quantity: 2`, `ticket_id: "TK-1092"`. | HTTP 201 Created, tồn kho tăng từ 10 lên 12, sổ cái ghi nhận loại `RETURN`. | **MAJOR** | HTTP 201, tồn tăng chính xác 12, sổ cái lưu vết phân loại `RETURN`. | **PASS** |
| **TC-04** *(Biên 1: Xuất đúng bằng tồn)* | Linh kiện có tồn kho thực tế khả dụng đúng 10 cái tại chi nhánh. | 1. Kỹ thuật viên gửi yêu cầu xuất kho với số lượng đúng bằng 10. | `part_code: "SCR-IP14-01"`, `quantity: 10`, `ticket_id: "TK-1092"`. | Giao dịch thành công, tồn kho giảm về đúng 0, cờ trạng thái chuyển sang `WARNING`. | **HIGH** | Xuất kho thành công, tồn kho còn đúng 0, cờ cảnh báo `WARNING`. | **PASS** |
| **TC-05** *(Biên 2: Xuất vượt 1 đơn vị)* | Linh kiện có tồn kho thực tế khả dụng đúng 10 cái tại chi nhánh. | 1. Kỹ thuật viên gửi yêu cầu xuất kho với số lượng là 11 cái. | `part_code: "SCR-IP14-01"`, `quantity: 11`, `ticket_id: "TK-1092"`. | Hệ thống từ chối, ném `NegativeStockError`, tồn giữ nguyên 10 cái. | **CRITICAL** | Ném lỗi `ERR_INSUFFICIENT_STOCK`, tồn kho không đổi (10 cái). | **PASS** |
| **TC-06** *(Biên 3: Tồn chạm đúng ngưỡng)* | Linh kiện có ngưỡng an toàn `min_threshold = 15`. | 1. Cập nhật số dư tồn kho về đúng 15 cái.<br>2. Gọi `GET /stock/SCR-IP14-01`. | `center_id: "L5-WH-890"`, `part_code: "SCR-IP14-01"`, `quantity: 15`. | Hệ thống trả về `status_flag: "WARNING"` kích hoạt cờ cảnh báo thiếu hàng. | **HIGH** | Phản hồi JSON có `status_flag: "WARNING"`, huy hiệu đỏ sáng. | **PASS** |
| **TC-07** *(Biên 4: Tồn trên ngưỡng 1 cái)* | Linh kiện có ngưỡng an toàn `min_threshold = 15`. | 1. Cập nhật số dư tồn kho lên 16 cái.<br>2. Gọi `GET /stock/SCR-IP14-01`. | `center_id: "L5-WH-890"`, `part_code: "SCR-IP14-01"`, `quantity: 16`. | Hệ thống trả về `status_flag: "NORMAL"`, không phát sinh cảnh báo thiếu hàng. | **HIGH** | Phản hồi JSON có `status_flag: "NORMAL"`, huy hiệu xanh an toàn. | **PASS** |
| **TC-08** *(Dữ liệu sai 1: Phiếu đã đóng)* | Phiếu bảo hành `TK-COMPLETED-01` đã ở trạng thái `COMPLETED`. | 1. Kỹ thuật viên cố tình dùng mã phiếu đã đóng để xuất kho. | `type: "OUT"`, `quantity: 1`, `ticket_id: "TK-COMPLETED-01"`. | HTTP 422, từ chối giao dịch, báo lỗi phiếu đã kết thúc hoặc bị hủy. | **HIGH** | HTTP 422 `ERR_INVALID_TICKET`, thông báo: *"Phiếu bảo hành hiện đã kết thúc..."*. | **PASS** |
| **TC-09** *(Dữ liệu sai 2: Số lượng âm / 0)* | Nhân viên nhập số lượng xuất là `0` hoặc `-5` vào ô nhập. | 1. Gửi request `POST /transactions` với `quantity: 0`. | `part_code: "SCR-IP14-01"`, `type: "IN"`, `quantity: 0`. | HTTP 400 Bad Request, báo lỗi `ERR_INVALID_QUANTITY`, hệ thống không sập. | **HIGH** | HTTP 400 `ERR_INVALID_QUANTITY`, thông báo lỗi rõ ràng, hệ thống ổn định. | **PASS** |
| **TC-10** *(Bảo mật SE - S2: A01 OWASP)* | Tài khoản đăng nhập mang Token của Chi nhánh Quận 3 (`L5-WH-891`). | 1. Người dùng gửi request kèm `center_id: "L5-WH-890"` để truy vấn kho khác. | `Header Bearer Token center: L5-WH-891`, `body center_id: L5-WH-890`. | HTTP 403 Forbidden, báo lỗi `ERR_UNAUTHORIZED_CENTER`, chặn truy cập chéo. | **CRITICAL** | HTTP 403 `ERR_UNAUTHORIZED_CENTER`, từ chối truy cập ngoài trung tâm. | **PASS** |
| **TC-11** *(Bảo mật SE - S3: Băm mật khẩu)* | Đăng ký tài khoản mới hoặc yêu cầu khôi phục mật khẩu. | 1. Đăng ký tài khoản với mật khẩu dạng rõ `Password123@`.<br>2. Kiểm tra bản ghi CSDL. | `email: "sec.tech@gmail.com"`, `password: "Password123@"`. | Trong CSDL chỉ có trường `password_hash` (chuỗi băm Bcrypt 12 rounds an toàn `$2b$12$...`), không có trường `password`. | **CRITICAL** | CSDL chỉ lưu `password_hash`, không lưu plaintext `password`, API không lộ mật khẩu. | **PASS** |
| **TC-12** *(Tái lập C8: Lũy đẳng Seed)* | Hệ thống đã khởi tạo xong dữ liệu mẫu ban đầu qua script seed. | 1. Chạy lệnh `python seeds/seed.py` lần 1.<br>2. Chạy lại `python seeds/seed.py` lần 2. | File `seeds/001_seed_parts_demo.json` (40 linh kiện, 75 tồn kho). | Lần 2 hoàn thành 100% không báo lỗi, tổng số linh kiện giữ nguyên đúng 40 loại, không nhân đôi. | **CRITICAL** | Lần 2 thực thi thành công, số lượng bản ghi giữ nguyên tuyệt đối (Idempotent). | **PASS** |
| **TC-13** *(SE - S1: CRUD Part & User)* | Quản lý kho có quyền quản trị danh mục và tài khoản nhân sự. | 1. Tạo mới part/user.<br>2. Đọc chi tiết.<br>3. Cập nhật thông tin.<br>4. Thử xóa khi còn tồn kho / tự xóa chính mình.<br>5. Xóa an toàn khi tồn kho = 0. | `POST`, `GET`, `PUT`, `DELETE` trên `/api/v1/inventory/parts` và `/api/v1/inventory/users`. | Bước 1-3 thành công (201, 200); bước 4 bị chặn an toàn với HTTP 400 (`ERR_CANNOT_DELETE_ACTIVE_STOCK` / `ERR_CANNOT_DELETE_SELF`); bước 5 xóa thành công 200 OK. | **CRITICAL** | Hoàn thành trọn vẹn đủ 4 thao tác CRUD cho 2 thực thể, ràng buộc bảo vệ hoạt động chính xác 100%. | **PASS** |

---

## Minh chứng Lệnh Chạy Thực tế trên Terminal

```text
============================= test session starts =============================
platform win32 -- Python 3.11.5, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\Hoc\DH\N4\N4.HK01\Chuyende1\CDTN01
configfile: pytest.ini
plugins: anyio-4.15.1
collected 67 items

tests/auth_and_user.test.py::TestAuthAndUserManagement (15 tests) ............... PASSED [ 22%]
tests/bt3_specification_and_constraints.test.py::TestBT3SpecificationAndConstraints (13 tests) ............. PASSED [ 41%]
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI (15 tests) ............... PASSED [ 64%]
tests/inventory.routes.test.py::TestInventoryRoutes (6 tests) ...... PASSED [ 73%]
tests/inventory.service.test.py::TestInventoryService (7 tests) ....... PASSED [ 83%]
tests/se_s1_crud.test.py::TestSES1CRUD (11 tests) ........... PASSED [100%]

======================== 67 passed, 1 warning in 3.09s ========================
```

import os

readme_content = r"""# HỆ THỐNG SMART CRM – MEKONG MOBILE
## BÁO CÁO ĐỒ ÁN CHUYÊN ĐỀ TỐT NGHIỆP 1 (HỌC KỲ 1, NĂM HỌC 2026 – 2027)
**Chuyên ngành:** Kỹ thuật Phần mềm (Software Engineering - SE)  
**Phân hệ thực hiện:** Luồng 05 – Quản lý Kho linh kiện thay thế  
**Chi nhánh triển khai:** Chi nhánh Quận 1  
**Sinh viên thực hiện:** Huỳnh Nguyễn Bảo Ngọc — **MSSV:** 2374802010339  
**Lớp học phần:** 261_71ITGR40203_06  
**Giảng viên hướng dẫn:** TS. Nguyễn Trí Hải  
**Repository GitHub:** [https://github.com/Johnny120905/cdtn01_HuynhNguyenBaoNgoc_L5.git](https://github.com/Johnny120905/cdtn01_HuynhNguyenBaoNgoc_L5.git)  
**Tài liệu kỹ thuật liên quan:**
- [docs/thietke.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/thietke.md) — Đặc tả Layout & Prompt Stitch tái tạo giao diện 3D chi tiết
- [docs/thaydoithietke.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/thaydoithietke.md) — Nhật ký chi tiết toàn bộ các thay đổi Backend - Database - Frontend
- [docs/test.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/test.md) — Đặc tả điều kiện ràng buộc 13 giao diện & Bằng chứng 43 ca kiểm thử tự động
- [docs/BT2.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/BT2.md) — Báo cáo kết quả Bài tập 2 (Sprint 2) nộp học phần
- [docs/api-contract.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/api-contract.md) — Đặc tả hợp đồng API RESTful chuẩn JSON
- [docs/srs.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/srs.md) — Tài liệu đặc tả yêu cầu phần mềm (Software Requirements Specification)

---

> [!IMPORTANT]
> **CAM KẾT TÁI TẠO CƠ CẤU TUYỆT ĐỐI (100% REPRODUCTION GUARANTEE):**  
> Tài liệu này được biên soạn với tiêu chuẩn: **Bất kỳ ai, dù không có chuyên môn sâu về lập trình hay công nghệ thông tin, chỉ cần đọc và làm theo từng bước hướng dẫn bên dưới là chắc chắn 100% tái tạo và vận hành thành công toàn bộ hệ thống website đúng y hệt kết quả tác giả đã xây dựng từ Backend - Database - Frontend.**

---

# MỤC 1: HƯỚNG DẪN TÁI TẠO CƠ CẤU HỆ THỐNG TOÀN DIỆN (DATABASE — BACKEND — FRONTEND)

Hệ thống được thiết kế theo kiến trúc 3 tầng (3-Tier Architecture) đồng bộ và hoàn chỉnh:

```
+-----------------------------------------------------------------------------------+
|                        KIẾN TRÚC TÁI TẠO CƠ CẤU TOÀN DIỆN                         |
+-----------------------------------------------------------------------------------+
| 1. DATABASE (CƠ SỞ DỮ LIỆU):                                                      |
|    - CSDL Đám mây MongoDB Atlas (Cluster huynhnguyenbaongoc2k5, mekong_mobile_l5) |
|    - Cơ chế lưu trữ kép Dual-Persistence dự phòng đĩa: data/users_store.json      |
|    - 40 mã linh kiện mẫu (seeds/001_seed_parts_demo.json) & 75 bản ghi tồn kho    |
|                                         ▲▼                                        |
| 2. BACKEND (MÁY CHỦ API FASTAPI):                                                 |
|    - Python 3.11, FastAPI RESTful API, PyMongo, PyJWT, Bcrypt, Pytest             |
|    - Cưỡng chế quy tắc nghiệp vụ BR-01 (Chặn âm kho), BR-02 (Bắt buộc Ticket ID)  |
|    - Cổng phục vụ API & Swagger UI: http://localhost:8000/docs                    |
|                                         ▲▼                                        |
| 3. FRONTEND (GIAO DIỆN NGƯỜI DÙNG SPA DARK 3D ELEVATION):                         |
|    - Single Page Application (HTML5, Vanilla JS, Dark 3D Elevation CSS)           |
|    - Phông chữ Be Vietnam Pro, màu ngữ nghĩa xanh/vàng/đỏ, nút tactile 3D         |
|    - Tự động gợi ý Dropdown + phím Enter (bỏ nút Tra cứu), nút Đặt lại sạch sẽ    |
|    - Đếm ngược OTP 10 phút, bỏ nút Quay lại trang ở Sổ cái và Quản lý nhân sự     |
|    - Địa chỉ truy cập trực tiếp: http://localhost:8000/                            |
+-----------------------------------------------------------------------------------+
```

---

## 1. TÁI TẠO CƠ CẤU DATABASE (CƠ SỞ DỮ LIỆU)

### 1.1. Cấu hình Chuỗi kết nối MongoDB Atlas
Hệ thống sử dụng cơ sở dữ liệu MongoDB Atlas Cloud. Chuỗi kết nối đã được cấu hình sẵn trong tệp [.env](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/.env):
```env
MONGO_URI=mongodb+srv://<db_username>:<db_password>@<ten-cluster>.mongodb.net/?retryWrites=true&w=majority
DB_NAME=mekong_mobile_l5
ENVIRONMENT=development
PORT=8000
JWT_SECRET=supersecretkey_mekong_mobile_2026_jwt_token_secure_flow05
CENTER_ID=L5-WH-890
```

### 1.2. Danh mục 6 Collections và Nhiệm vụ
Hệ thống quản lý 6 bộ sưu tập (collections) chính:
1. **`users`**: Lưu trữ hồ sơ nhân viên, mật khẩu đã băm Bcrypt, vai trò (`TECH_STAFF`, `MATERIAL_STAFF`, `MANAGER`), trạng thái (`ONLINE`, `AWAY`, `OFF_SHIFT`, `TERMINATED`), mã OTP và thời hạn hiệu lực OTP.
2. **`part_inventory`**: Danh mục 40 loại linh kiện chuẩn hóa (Mã linh kiện, Tên, Thiết bị áp dụng, Đơn giá VNĐ, Nhà cung cấp).
3. **`inventory_stock`**: Quản lý số lượng tồn kho khả dụng thực tế, ngưỡng cảnh báo an toàn (`min_threshold`), phiên bản giao dịch (`version` phục vụ Optimistic Locking).
4. **`part_transaction`**: Sổ cái kiểm toán bất biến (Audit Log) ghi nhận toàn bộ các thao tác `OUT` (Xuất kho thay thế), `IN` (Nhập kho vật tư), `RETURN` (Hoàn trả linh kiện) gắn kèm `ticket_id` và `performed_by`.
5. **`repair_ticket`**: Danh mục phiếu sửa chữa tiếp nhận từ khách hàng tại quầy bảo hành.
6. **`suppliers`**: Danh sách các đơn vị cung ứng vật tư chiến lược.

### 1.3. Nạp dữ liệu hạt giống (Seed Data 40 Linh kiện)
Dữ liệu mẫu chuẩn hóa gồm 40 mã linh kiện và các bản ghi tồn kho được lưu tại [seeds/001_seed_parts_demo.json](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/seeds/001_seed_parts_demo.json).
Khi khởi động hệ thống, Backend sẽ tự động kiểm tra và nạp dữ liệu vào MongoDB Atlas nếu chưa có. Nếu bạn muốn nạp cưỡng bức lại từ đầu, hãy chạy lệnh:
```powershell
python scripts/seed_database.py
```

### 1.4. Cơ chế lưu trữ kép Dual-Persistence dự phòng
Để đảm bảo hệ thống không bao giờ bị gián đoạn hay mất dữ liệu khi mất kết nối mạng Internet với MongoDB Atlas, tầng dữ liệu tích hợp bộ lưu trữ bền vững dự phòng tại [data/users_store.json](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/data/users_store.json). Mọi thao tác cập nhật người dùng, đổi mật khẩu, cấp OTP đều được đồng bộ đồng thời vào tệp này.

---

## 2. TÁI TẠO CƠ CẤU BACKEND (MÁY CHỦ API FASTAPI)

### 2.1. Yêu cầu Môi trường
- **Hệ điều hành:** Windows 10/11, macOS, hoặc Linux (Ubuntu 20.04+).
- **Python:** Phiên bản Python 3.10 hoặc Python 3.11 (Khuyến nghị 3.11.5).

### 2.2. Các bước cài đặt và khởi động Backend
Mở cửa sổ PowerShell (hoặc Terminal) và thực hiện tuần tự các lệnh sau:

1. **Di chuyển vào thư mục dự án:**
   ```powershell
   cd D:\Hoc\DH\N4\N4.HK01\Chuyende1\CDTN01
   ```

2. **Tạo và kích hoạt môi trường ảo (Virtual Environment):**
   - Trên **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
     .\venv\Scripts\Activate.ps1
     ```
     *(Khi thành công, đầu dòng nhắc lệnh sẽ hiện chữ `(venv)` màu xanh).*
   - Trên **macOS / Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Cài đặt toàn bộ thư viện phụ thuộc:**
   ```powershell
   pip install -r requirements.txt
   ```
   *Các thư viện được cài đặt bao gồm: `fastapi`, `uvicorn[standard]`, `pymongo[srv]`, `dnspython`, `pydantic`, `pytest`, `httpx`, `bcrypt`, `pyjwt`, `python-dotenv`.*

4. **Khởi chạy máy chủ Backend API:**
   ```powershell
   python src/app.py
   ```
   *Màn hình hiển thị thông báo:*
   ```text
   INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
   [Repository] Connected to MongoDB: mekong_mobile_l5 at mongodb+srv://<db_username>:<db_password>@<ten-cluster>.mongodb.net/?retryWrites=true&w=majority
   ```

5. **Kiểm tra tài liệu API tương tác trực quan (Swagger UI):**
   Mở trình duyệt truy cập:
   👉 **`http://localhost:8000/docs`** (hoặc `http://127.0.0.1:8000/docs`)
   Tại đây bạn có thể trực tiếp gửi request và thử nghiệm toàn bộ các endpoint xác thực, kho linh kiện, giao dịch, và quản lý nhân sự.

---

## 3. TÁI TẠO CƠ CẤU FRONTEND (GIAO DIỆN NGƯỜI DÙNG SPA 3D)

### 3.1. Truy cập Website trực tiếp
Giao diện người dùng được tích hợp trực tiếp vào máy chủ FastAPI thông qua cơ chế Mount Static Files. Do đó, bạn không cần cài thêm Node.js hay chạy server web riêng:
👉 Mở trình duyệt web (Chrome, Edge, Firefox, Safari) và truy cập: **`http://localhost:8000/`**

*(Nếu muốn chạy qua Vite Dev Server ở cổng 3000, bạn có thể gõ `cd frontend && npm install && npm run dev`).*

### 3.2. Danh sách Tài khoản mẫu theo từng vai trò
Hệ thống cung cấp sẵn các tài khoản có đầy đủ phân quyền và trạng thái mẫu:

| Vai trò Nghiệp vụ | Email Đăng nhập | Mật khẩu mặc định | Giao diện và Quyền hạn đặc trưng |
| :--- | :--- | :--- | :--- |
| **Nhân viên Kỹ thuật (`TECH_STAFF`)** | `kythuat.quan1@mekongmobile.vn`<br>*(hoặc `kythuat.test@gmail.com`)* | `Tech@123456`<br>*(hoặc `123456`)* | - **Bảng tin Kỹ thuật viên:** Danh sách phiếu bảo hành, trạng thái tiếng Việt ("Chờ tiếp nhận", "Đang xử lý", "Đã hoàn thành").<br>- **Tra cứu & Giao dịch:** Ô tìm kiếm tự động gợi ý dropdown, bấm phím `Enter` tự động chọn linh kiện (không cần nút "Tra cứu"); Nút "Đặt lại biểu mẫu" khôi phục toàn bộ về trạng thái ban đầu sạch sẽ; Cảnh báo âm kho tự động khóa nút khi vượt tồn.<br>- **Lịch sử tiếp nhận:** Sổ nhật ký xuất kho và hoàn trả cá nhân. |
| **Nhân viên Vật tư (`MATERIAL_STAFF`)** | `vattu.quan1@mekongmobile.vn`<br>*(hoặc `vattu.test@gmail.com`)* | `Mat@123456`<br>*(hoặc `123456`)* | - **Bảng tin Quản lý vật tư:** Đã loại bỏ nút "Tạo lệnh Nhập kho mới" thừa ở Main Content, thay bằng huy hiệu trung tâm vật tư.<br>- **Nhập kho linh kiện mới:** Thiết kế lưới 2 cột song song (Form nhập kho bên trái, Bảng thống kê tồn 40 linh kiện bên phải kèm nút "Chọn" nhanh).<br>- **Nhà cung cấp:** Danh bạ đối tác cung ứng vật tư. |
| **Quản lý Kho chi nhánh (`MANAGER`)** | `quanly.quan1@mekongmobile.vn`<br>*(hoặc `quanlykho.test@gmail.com`)* | `Manager@123456`<br>*(hoặc `123456`)* | - **Dashboard Tổng quan:** 4 thẻ KPI, bảng cảnh báo cạn kho viền đỏ, nút "Xem Báo cáo Chi tiết".<br>- **Báo cáo Xuất Nhập Tồn:** Cấu hình ngưỡng an toàn `min_threshold` kèm nút **"Quay lại trang"**.<br>- **Nhật ký Giao dịch Kho (Audit Log):** Sổ cái lưu vết giao dịch "Xuất kho thay thế" (OUT) gắn kèm Ticket ID và Người thực hiện (Không có nút "Quay lại trang").<br>- **Quản lý nhân sự:** Tìm kiếm, lọc theo vai trò, lọc theo 4 trạng thái, khóa tài khoản thôi việc (Không có nút "Quay lại trang"). |
| **Tài khoản Đã thôi việc (`TERMINATED`)** | `anhpham712002@gmail.com` | `Anhpham712002@` | - **Kiểm tra an ninh:** Đăng nhập bị chặn lập tức với mã lỗi HTTP 403 `ERR_ACCOUNT_TERMINATED`. |

### 3.3. Các tính năng giao diện người dùng nổi bật
1. **Quy chuẩn mật khẩu an toàn:** 8 ký tự (đủ 4 nhóm hoa, thường, số, ký tự đặc biệt). Bảng checklist được ẩn mặc định và chỉ báo đỏ khi người dùng nhập sai quy chuẩn.
2. **Nút con mắt xem mật khẩu (`.eye-toggle-btn`):** Tích hợp tại tất cả các ô nhập mật khẩu của 3 màn hình Đăng nhập, Đăng ký và Quên mật khẩu.
3. **Đồng hồ đếm ngược OTP 10 phút thời gian thực (`#countdownTimer`):** Khung Quên mật khẩu đếm ngược từng giây từ `10:00` xuống `00:00`, tự động điền mã OTP 6 số sinh ra từ hệ thống.
4. **Loại bỏ triệt để chuỗi `undefined`:** Áp dụng cơ chế dự phòng an toàn 100% bằng tiếng Việt chuẩn cho mọi trường dữ liệu trên giao diện.

---

## 4. CHẠY BỘ KIỂM THỬ TỰ ĐỘNG HÓA (AUTOMATED TEST VERIFICATION)

Hệ thống được bảo vệ bởi bộ kiểm thử tự động hóa toàn diện gồm **43 ca kiểm thử (Test Cases)** bao phủ đầy đủ các tầng Routes, Services, Validators, CSDL và Giao diện UI/UX.

### Lệnh chạy toàn bộ kiểm thử:
Tại cửa sổ PowerShell trong môi trường ảo, gõ lệnh:
```powershell
pytest tests/ -v
```

### Kết quả chạy kiểm thử thực tế (Bảo chứng 100% PASS):
```text
============================= test session starts =============================
platform win32 -- Python 3.11.5, pytest-9.1.1, pluggy-1.6.0 -- python.exe
rootdir: D:\Hoc\DH\N4\N4.HK01\Chuyende1\CDTN01
configfile: pytest.ini
collected 43 items

tests/auth_and_user.test.py::TestAuthAndUserManagement::test_01_register_success_for_tech_staff PASSED
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_02_register_reject_short_password PASSED
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_02a_register_reject_missing_uppercase PASSED
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_02b_register_reject_missing_lowercase PASSED
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_02c_register_reject_missing_digit PASSED
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_02d_register_reject_missing_special PASSED
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_03_register_duplicate_email_forbidden PASSED
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_04_login_success PASSED
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_05_login_wrong_password PASSED
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_06_forgot_password_and_reset_with_otp PASSED
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_07_manager_view_subordinates_only PASSED
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_08_manager_import_subordinates PASSED
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_09_login_terminated_user_rejected_with_403 PASSED
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_10_logout_sets_user_status_to_off_shift PASSED
tests/auth_and_user.test.py::TestAuthAndUserManagement::test_11_max_length_constraints PASSED
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_01_cross_role_flow_export_triggers_manager_alert PASSED
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_02_cross_role_flow_material_import_updates_tech_stock PASSED
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_03_static_homepage_layout_and_font_integrity PASSED
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_04_styles_css_3d_and_semantic_colors PASSED
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_05_clean_app_js_no_breadcrumbs_no_technical_codes PASSED
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_06_header_renamed_logout_button_and_no_luong_05 PASSED
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_07_tech_staff_unified_smart_search_and_reset_form PASSED
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_08_manager_subordinates_search_filter_and_pagination PASSED
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_09_password_eye_toggle_and_hidden_checklists PASSED
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_10_otp_10_minutes_and_live_countdown PASSED
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_11_vietnamese_translations_and_out_transaction_representation PASSED
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_12_material_staff_ui_no_create_button_and_stats_table PASSED
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_13_manager_navigation_reports_removed_from_sidebar_and_back_button PASSED
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_14_expanded_parts_catalog_40_items PASSED
tests/cross_role_and_ui.test.py::TestCrossRoleAndUI::test_15_tech_staff_smart_lookup_enter_and_not_found_handling PASSED
tests/inventory.routes.test.py::TestInventoryRoutes::test_01_api1_get_stock_success PASSED
tests/inventory.routes.test.py::TestInventoryRoutes::test_02_api2_create_transaction_success PASSED
tests/inventory.routes.test.py::TestInventoryRoutes::test_03_api2_create_transaction_negative_stock_error PASSED
tests/inventory.routes.test.py::TestInventoryRoutes::test_04_api2_create_transaction_missing_ticket_error PASSED
tests/inventory.routes.test.py::TestInventoryRoutes::test_05_api3_update_threshold_forbidden_for_tech_staff PASSED
tests/inventory.routes.test.py::TestInventoryRoutes::test_06_api3_update_threshold_success_for_manager PASSED
tests/inventory.service.test.py::TestInventoryService::test_01_stock_lookup_and_threshold_evaluation_normal PASSED
tests/inventory.service.test.py::TestInventoryService::test_02_stock_lookup_and_threshold_evaluation_warning PASSED
tests/inventory.service.test.py::TestInventoryService::test_03_export_happy_path PASSED
tests/inventory.service.test.py::TestInventoryService::test_04_br01_prevent_negative_stock PASSED
tests/inventory.service.test.py::TestInventoryService::test_05_br02_mandatory_ticket_for_out PASSED
tests/inventory.service.test.py::TestInventoryService::test_06_role_permission_checks PASSED
tests/inventory.service.test.py::TestInventoryService::test_07_fr06_set_threshold_by_manager_only PASSED

======================== 43 passed, 1 warning in 3.42s ========================
```

---

## 5. THƯ MỤC TÀI LIỆU DỰ ÁN TRONG THƯ MỤC `/docs`

Toàn bộ các tài liệu đặc tả, kiểm thử và nhật ký thay đổi của hệ thống được quy hoạch gọn gàng trong thư mục [docs/](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs):
- [docs/test.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/test.md): Tài liệu kiểm thử chi tiết điều kiện ràng buộc Backend - Database - Frontend cho toàn bộ 13 giao diện hệ thống.
- [docs/thaydoithietke.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/thaydoithietke.md): Báo cáo nhật ký thay đổi thiết kế qua 5 lần nâng cấp.
- [docs/thietke.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/thietke.md): Đặc tả thiết kế hệ thống và cấu trúc giao diện 3D.
- [docs/BT2.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/BT2.md): Báo cáo kết quả Bài tập 2 học phần Chuyên đề tốt nghiệp 1.
- [docs/api-contract.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/api-contract.md): Hợp đồng API RESTful chuẩn JSON.
- [docs/srs.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/srs.md): Đặc tả yêu cầu phần mềm.
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print("Updated README.md with comprehensive Reproduction Guide!")

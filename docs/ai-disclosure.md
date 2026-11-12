# PHỤ LỤC BẮT BUỘC: HỒ SƠ TÍCH LŨY KHAI BÁO SỬ DỤNG CÔNG CỤ TRÍ TUỆ NHÂN TẠO (`BT1` · `BT2` · `BT3`)
*(Mandatory Appendix: Cumulative AI Usage Declaration Across Assignments 1, 2 & 3)*

- **Học phần:** Chuyên đề Tốt nghiệp 1 (Học kỳ 1, Năm học 2026 – 2027)
- **Dự án:** Hệ thống Smart CRM – Mekong Mobile | **Phân hệ:** Luồng 05 (`L5`) – Quản lý Kho linh kiện thay thế
- **Chuyên ngành:** Công nghệ phần mềm (`Track SE`)
- **Sinh viên thực hiện:** Huỳnh Nguyễn Bảo Ngọc — **MSSV:** `2374802010339`
- **Lớp học phần:** `261_71ITGR40203_06`
- **Giảng viên hướng dẫn:** TS. Nguyễn Trí Hải
- **Kho mã nguồn GitHub:** https://github.com/Johnny120905/cdtn01_HuynhNguyenBaoNgoc_L5.git

---

## Cam kết Chung về Liêm chính Học thuật

Tôi xin cam đoan toàn bộ hồ sơ khai báo sử dụng công cụ Trí tuệ Nhân tạo (AI) tích lũy xuyên suốt 3 giai đoạn của học phần (**Bài tập 1: Phân tích & Thiết kế** → **Bài tập 2: Hiện thực hóa Module cốt lõi** → **Bài tập 3: Kiểm thử & Đóng gói Prototype**) dưới đây là hoàn toàn trung thực, minh bạch và tuân thủ nghiêm ngặt quy định liêm chính học thuật của Khoa Công nghệ Thông tin – Trường Đại học Văn Lang. Mọi công cụ AI chỉ được sử dụng với vai trò trợ lý hỗ trợ chuẩn hóa văn phong, gợi ý cú pháp khung mẫu, rà soát lỗi và kiểm tra tài liệu; toàn bộ quyết định nghiệp vụ, thiết kế kiến trúc, mã nguồn, kịch bản kiểm thử và cấu hình đóng gói đều do tôi trực tiếp đọc hiểu từng dòng, tự tay kiểm chứng thực nghiệm và hoàn toàn chịu trách nhiệm giải trình trước Giảng viên hướng dẫn.

---

## PHẦN I: KHAI BÁO SỬ DỤNG CÔNG CỤ AI — BÀI TẬP 1 (`BT1`: PHÂN TÍCH VÀ THIẾT KẾ)

**Cam kết cá nhân Giai đoạn 1 (`BT1`):**
> *"Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp. Huỳnh Nguyễn Bảo Ngọc, 2374802010339, Ngày 08/10/2026"*

**Bảng kê khai chi tiết mức độ sử dụng AI ở Bài tập 1:**

| STT | Tên công cụ AI | Nhiệm vụ / Mục đích sử dụng | Thành phần áp dụng trong Bài tập | Cách sinh viên kiểm chứng & Chịu trách nhiệm |
| :-: | :--- | :--- | :--- | :--- |
| 1 | **Google Gemini** | Tinh chỉnh văn phong học thuật (SRS, Đặc tả Use Case); cấu trúc hóa các Yêu cầu phi chức năng (NFR) có ngưỡng số; sinh mã code PlantUML; gợi ý câu từ cho phần Lập luận kiến trúc và viết Prompt thiết kế UI. | Thành phần 1, 2, 3, 4 & 5 *(`docs/srs.md`, `docs/api-contract.md`)*. | Sinh viên cung cấp dữ liệu thô ban đầu. Sau khi AI trả kết quả, sinh viên tự đối chiếu lại 100% với Barem chấm điểm và ràng buộc của Luồng L5 để cắt bỏ các chi tiết thừa/sai lệch. |
| 2 | **Draw.io (qua Text-to-Code PlantUML)** | Render tự động các bản vẽ kỹ thuật (Use Case, Kiến trúc, ERD) dựa trên đoạn mã do Gemini cung cấp để đảm bảo tính thẩm mỹ và chuẩn hóa cấu trúc. | Thành phần 2 (Use Case), Thành phần 3 (Kiến trúc) & Thành phần 4 (ERD) *(`docs/usecase.drawio`, `docs/architecture.drawio`, `docs/erd.drawio`)*. | Sinh viên tự xác định danh sách bảng, khóa ngoại và luồng quan hệ. Sau khi Render, sinh viên rà soát lại các ký pháp (Crow's foot, Include/Extend, mũi tên một chiều) trước khi xuất ảnh. |
| 3 | **Stitch** | Sinh hình ảnh phác thảo giao diện (Wireframes) cho 3 màn hình cốt lõi dựa trên các câu lệnh (Prompt) mô tả cấu trúc Layout và trường dữ liệu. | Thành phần 5 (Wireframe 3 màn hình) *(`docs/thietke.md`)*. | Sinh viên tự thiết kế cấu trúc Form, sau khi Stitch sinh ảnh, sinh viên tiến hành đối chiếu chéo thủ công từng trường nhập liệu trên ảnh với bảng ERD để đảm bảo tính "đóng vòng" dữ liệu. |
| 4 | **— Không dùng AI (Tự làm hoàn toàn) —** | Xác lập ranh giới phạm vi Trong/Ngoài phạm vi (`WON'T HAVE`) của Luồng 05; phân tích quyền hạn 3 vai trò (`ACT-01..03`), định nghĩa 5 quy tắc nghiệp vụ cốt lõi (`BR-01..BR-05`), ấn định ngưỡng đo lường định lượng cho 4 `NFR`, đặc tả luồng ngoại lệ `EX-02..EX-05` của `UC-02` và khép kín Ma trận truy vết yêu cầu (`RTM`). | Thành phần 1 & Thành phần 2 *(`docs/srs.md` – Mục 1, Mục 2, Mục 5, Mục 6 & Đặc tả `UC-02`)*. | Không áp dụng AI. Tự đối chiếu trực tiếp với đề bài Case Study Smart CRM – Mekong Mobile (Bảng 9.1) và Checklist 11 mục kiểm chứng kỹ thuật tối thiểu của Đề bài Bài tập 1 để đảm bảo không có ô trống và thống nhất 100% bảng thuật ngữ. |

---

## PHẦN II: KHAI BÁO SỬ DỤNG CÔNG CỤ AI — BÀI TẬP 2 (`BT2`: HIỆN THỰC HÓA MODULE CỐT LÕI – TAG `v0.2`)

**Cam kết cá nhân Giai đoạn 2 (`BT2`):**
> *"Tôi tên là: Huỳnh Nguyễn Bảo Ngọc _ 2374802010339 — Ngành: SE — Ngày 29/10/2026. Tôi xin cam đoan toàn bộ nội dung khai báo sử dụng công cụ Trí tuệ Nhân tạo (AI) nêu trên là hoàn toàn trung thực, minh bạch và đúng quy định của Khoa Công nghệ Thông tin – Trường Đại học Văn Lang. Tôi hiểu rõ từng dòng mã nguồn, từng quy tắc nghiệp vụ, giải thuật Khóa lạc quan (Optimistic Locking), cấu trúc dữ liệu NoSQL và toàn bộ 43 kịch bản kiểm thử tự động trong kho mã nguồn của mình, đồng thời hoàn toàn chịu trách nhiệm học thuật và sẵn sàng giải trình trực tiếp trước Giảng viên hướng dẫn."*

**Bảng kê khai chi tiết mức độ sử dụng AI & Kiểm chứng mã nguồn ở Bài tập 2:**

| STT | Công cụ | Dùng vào việc gì | Áp dụng ở tệp / hàm nào | Em đã kiểm chứng thế nào |
| :-: | :--- | :--- | :--- | :--- |
| 1 | **— Không dùng AI (Tự làm hoàn toàn) —** | Thiết kế luồng nghiệp vụ cốt lõi 6 bước xử lý giao dịch kho, lập luận giải thuật Khóa lạc quan (*Optimistic Locking* đối chiếu trường `version`), quy tắc chặn âm kho (`BR-01` / `EX-04`), bắt buộc chứng từ bảo hành (`BR-02` / `UC-99` / `EX-03`), sổ cái bất biến (`BR-03`), cô lập dữ liệu chi nhánh (`BR-04` / `EX-02`), phân quyền cấu hình ngưỡng (`FR-06`) và cơ chế lưu trữ kép (*Dual-Persistence Fallback*). | - `src/services/inventory.service.py` → `InventoryService.process_transaction()`, `get_stock()`, `get_low_stock_alerts()`, `set_part_threshold()`<br>- `src/repositories/inventory.repository.py` → `update_stock_optimistic()`, `insert_transaction()`, `update_part_threshold()`<br>- `src/errors/AppError.py` → `AppError` & 6 lớp ngoại lệ nghiệp vụ (`EX-02..EX-05`) | Tự viết mã nguồn và trực tiếp xây dựng 07 ca Unit Tests độc lập trong `tests/inventory.service.test.py` (chạy cô lập trên RAM không cần HTTP) để ép lỗi xuất vượt tồn kho (`NegativeStockError`), thiếu mã phiếu (`InvalidTicketError`) và sai quyền vai trò (`UnauthorizedRoleError`), xác nhận số dư tồn kho tuyệt đối không bao giờ bị trừ âm. |
| 2 | **Google Gemini / Antigravity IDE** | Hỗ trợ gợi ý cú pháp FastAPI Global Exception Handler, biểu thức chính quy (Regex) kiểm tra độ phức tạp mật khẩu 4 nhóm ký tự và kỹ thuật nạp mô-đun động `importlib` cho các tệp đặt tên có dấu chấm (`inventory.*.py`). | - `src/app.py` → `custom_app_error_handler()`<br>- `src/validators/inventory.validator.py` → `validate_password_complexity()`, `validate_transaction_payload()`, `validate_threshold_payload()`<br>- `src/routes/__init__.py`, `src/validators/__init__.py`, `src/services/__init__.py`, `src/repositories/__init__.py` | Rà soát thủ công từng nhánh điều kiện (bổ sung chặn kiểu `bool` giả dạng `int` trong Python); viết các ca kiểm thử biên `test_02..test_02d` trong `tests/auth_and_user.test.py` và 06 ca Integration Tests trong `tests/inventory.routes.test.py` để xác nhận API trả đúng mã HTTP `400`/`403`/`422` và tỷ lệ lộ lỗi thô `500` bằng `0%`. |
| 3 | **Google Gemini / Antigravity IDE** | Hỗ trợ chuẩn hóa cú pháp `$jsonSchema` trong script Migration MongoDB, sinh dữ liệu mẫu 40 linh kiện, cấu hình đóng gói `Dockerfile` / `docker-compose.yml` và gợi ý cấu trúc hàm API Client tập trung kèm xử lý 3 trạng thái giao diện (`Loading`, `Empty`, `Error`). | - `migrations/001_create_collections.js`, `migrations/002_create_indexes.js`<br>- `seeds/001_seed_parts_demo.json`, `seeds/seed.py` → `run_seed()`<br>- `Dockerfile`, `docker-compose.yml`<br>- `src/static/app.js` → `apiCall()`, `renderCurrentView()` | Chạy lệnh `python seeds/seed.py` liên tiếp 2 lần để kiểm chứng tính *Idempotent* của `replace_one(..., upsert=True)` (`0` lỗi, `0` bản ghi trùng lặp); khởi dựng container bằng `docker compose up -d --build` và chạy lệnh `python -m pytest tests/ -v` đạt kết quả tuyệt đối **43/43 PASSED (100%)**. |
| 4 | **Google Stitch & Draw.io** | Hỗ trợ xây dựng hệ thống Design Tokens *Dark 3D Elevation* và chuẩn hóa bộ sơ đồ kỹ thuật (`layered clean architecture.drawio`, `usecase.drawio`, `erd.drawio`, `architecture.drawio`) cùng nhật ký thay đổi thiết kế. | - `src/static/index.html`, `src/static/styles.css`<br>- `docs/thietke.md`, `docs/thaydoithietke.md`<br>- `docs/layered clean architecture.drawio`, `docs/erd.drawio`, `docs/usecase.drawio` | Đối chiếu thủ công 100% trường nhập liệu và huy hiệu trên 13 màn hình với 6 collections MongoDB cùng toàn bộ mã truy vết `ACT`, `US`, `FR`, `UC`, `BR`, `EX` của BT1; kiểm chứng tự động cấu trúc HTML/CSS/JS qua 15 ca kiểm thử trong `tests/cross_role_and_ui.test.py`. |

---

## PHẦN III: KHAI BÁO SỬ DỤNG CÔNG CỤ AI — BÀI TẬP 3 (`BT3`: KIỂM THỬ VÀ ĐÓNG GÓI PROTOTYPE)

*(Hạng mục đã thực hiện cho phần Kiểm thử tự động 43 ca, Sửa lỗi giao diện/bảo mật, Đóng gói Docker `<= 2` lệnh & Cẩm nang Tái lập môi trường sạch; tiếp tục được cập nhật bổ sung đến thời điểm đóng nhãn `v1.0` của Bài tập 3)*

**Cam kết cá nhân Giai đoạn 3 (`BT3`):**
> *"Tôi xác nhận đã đọc, hiểu rõ từng kịch bản kiểm thử (Test Case), từng nguyên nhân gốc rễ khi gỡ lỗi (Bug Root Cause), từng dòng cấu hình đóng gói Container (`Dockerfile`, `docker-compose.yml`) và từng bước trong tài liệu hướng dẫn dựng lại hệ thống, đồng thời chịu trách nhiệm hoàn toàn về tính trung thực và khả năng tái lập của sản phẩm bàn giao. Huỳnh Nguyễn Bảo Ngọc, 2374802010339, Ngày 30/10/2026"*

**Bảng kê khai chi tiết mức độ sử dụng AI cho công tác Kiểm thử, Gỡ lỗi & Đóng gói (`BT3`):**

| STT | Công cụ | Dùng vào việc gì | Áp dụng ở tệp / hàm nào | Em đã kiểm chứng thế nào |
| :-: | :--- | :--- | :--- | :--- |
| 1 | **— Không dùng AI (Tự làm hoàn toàn) —** | Lập tiêu chí bao phủ kiểm thử theo 5 quy tắc nghiệp vụ (`BR-01..BR-05`), phân tích nguyên nhân gốc rễ và trực tiếp sửa lỗi hiển thị thiếu trường tồn kho trên bảng cảnh báo Quản lý kho (`a.quantity ?? a.current_stock`), kiểm thử phân quyền truy cập theo vai trò & chi nhánh (`A01 OWASP`), và rà soát loại bỏ triệt để chuỗi kết nối nhạy cảm khỏi kho mã nguồn. | - `src/static/app.js` (dòng `1847–1851`: hàm `renderManagerDashboard()`, dòng `1270–1276`: `handleTechTransactionSubmit()`)<br>- `tests/inventory.service.test.py`, `tests/inventory.routes.test.py`<br>- `.env.example`, `.gitignore`, `scripts/generate_readme.py` | Tự tái lập lỗi trên trình duyệt tại `http://localhost:8000/`, sửa mã nguồn đồng bộ trên `src/static/app.js` và `frontend/public/app.js`; chạy quét chuỗi `mongodb+srv://` trên toàn bộ các tệp được Git theo dõi để xác nhận `0` secret lộ lọt (đạt tiêu chí `C7` của BT3). |
| 2 | **Google Gemini / Antigravity IDE** | Hỗ trợ mở rộng bộ kịch bản kiểm thử liên thông 3 vai trò (End-to-End), kiểm thử biên mật khẩu 4 nhóm, OTP 10 phút, khóa vĩnh viễn tài khoản thôi việc (`TERMINATED`) và cấu trúc hóa báo cáo kế hoạch/kết quả kiểm thử. | - `tests/auth_and_user.test.py` (15 ca kiểm thử)<br>- `tests/cross_role_and_ui.test.py` (15 ca kiểm thử)<br>- `pytest.ini`, `docs/test.md` | Trực tiếp chạy thật toàn bộ 43 ca kiểm thử bằng lệnh đơn `python -m pytest tests/ -v`, kiểm tra độc lập từng hàm `setUpClass` / `tearDownClass` đảm bảo dữ liệu kiểm thử tự dựng và tự dọn sạch 100%, không phụ thuộc dữ liệu riêng trên máy cá nhân (đạt tiêu chí cốt lõi `C2`, `C3` của BT3). |
| 3 | **Google Gemini / Antigravity IDE** | Hỗ trợ tối ưu hóa kịch bản đóng gói `Dockerfile` (`python:3.11-slim` + `HEALTHCHECK`), điều phối `docker-compose.yml` (2 container App + MongoDB 7.0 tự nạp seed khi khởi động) và biên soạn cẩm nang tái tạo hệ thống từ máy trắng + đối chiếu cấu trúc thư mục `BT1` · `BT2` · `BT3`. | - `Dockerfile`, `docker-compose.yml`, `.dockerignore`<br>- `README.md` (Phần 1 đến Phần 8)<br>- `docs/api-contract.md` | Tự thực hiện "Phép thử máy trắng": xóa container/volume cũ (`docker compose down -v`), dựng mới bằng đúng 2 lệnh (`cp .env.example .env` & `docker compose up -d --build`), kiểm tra trạng thái `healthy` tại `GET /health` và chạy lặp `python seeds/seed.py` lần 2 không lỗi, không nhân đôi dữ liệu (đạt tiêu chí cốt lõi `C1`, `C8` của BT3). |

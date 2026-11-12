# BÁO CÁO BÀI TẬP 2: HIỆN THỰC HÓA MODULE CỐT LÕI (15%)
## HỌC PHẦN: CHUYÊN ĐỀ TỐT NGHIỆP 1 (CDTN01)
### LUỒNG NGHIỆP VỤ 05 (L5): QUẢN LÝ KHO LINH KIỆN THAY THẾ – MEKONG MOBILE
### TRACK: KỸ THUẬT PHẦN MỀM (SOFTWARE ENGINEERING - SE)

---

### THÔNG TIN SINH VIÊN VÀ NỘP BÀI
- **Họ và tên:** Huỳnh Nguyễn Bảo Ngọc
- **Mã số sinh viên (MSSV):** `2374802010339`
- **Lớp chuyên ngành:** K27 – Công nghệ thông tin
- **Giảng viên hướng dẫn:** TS. Nguyễn Trí Hải
- **Ngày nộp bài ban đầu:** 29/10/2026
- **Ngày hoàn thiện cập nhật theo nhận xét:** 12/11/2026
- **Link GitHub Repository (Public):** https://github.com/Johnny120905/cdtn01_HuynhNguyenBaoNgoc_L5.git
- **Git Tag bài nộp BT2:** `v0.2`
  - **Commit Hash:** `e6698d58737cefbe0776fadaa75115e46cac58c4` (xác lập đúng bản nộp ngày 29/10/2026)
  - **Link Tag trên GitHub:** https://github.com/Johnny120905/cdtn01_HuynhNguyenBaoNgoc_L5/releases/tag/v0.2

---

## MỤC LỤC TỔNG HỢP

- [MỤC 1: TÓM TẮT HỆ THỐNG ĐÃ LÀM](#mục-1-tóm-tắt-hệ-thống-đã-làm)
- [MỤC 2: KIẾN TRÚC ĐÃ HIỆN THỰC](#mục-2-kiến-trúc-đã-hiện-thực)
- [MỤC 3: MODULE CỐT LÕI](#mục-3-module-cốt-lõi)
- [MỤC 4: BỘ KIỂM THỬ](#mục-4-bộ-kiểm-thử)
- [MỤC 5: MODULE MỞ RỘNG / TRÌNH BÀY KẾT QUẢ](#mục-5-module-mở-rộng--trình-bày-kết-quả)
- [MỤC 6: CÁCH DỰNG LẠI HỆ THỐNG](#mục-6-cách-dựng-lại-hệ-thống)
- [MỤC 7: THAY ĐỔI SO VỚI THIẾT KẾ BÀI TẬP 1 & TIẾP THU NHẬN XÉT](#mục-7-thay-đổi-so-với-thiết-kế-bài-tập-1--tiếp-thu-nhận-xét)
- [PHỤ LỤC: BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI](#phụ-lục-bảng-khai-báo-sử-dụng-công-cụ-ai)

---

## MỤC 1: TÓM TẮT HỆ THỐNG ĐÃ LÀM

### 1.1. Phạm vi và các chức năng hệ thống thực hiện được
Phân hệ **Kho linh kiện thay thế (Luồng 05)** trong Hệ thống Smart CRM – Mekong Mobile phục vụ việc quản lý danh mục linh kiện, tra cứu tồn kho theo chi nhánh thời gian thực, cấp phát linh kiện cho kỹ thuật viên sửa chữa bảo hành, nhập kho bổ sung từ nhà cung cấp và giám sát các chỉ số vận hành kho. Hệ thống phục vụ 3 nhóm vai trò người dùng nghiệp vụ chuyên biệt:

1. **Nhân viên kỹ thuật (`TECH_STAFF`):**
   - Tra cứu số lượng tồn kho khả dụng tức thời của từng mã linh kiện tại chi nhánh Quận 1 (`L5-WH-890`) trước khi tiếp nhận sửa máy cho khách.
   - Lập lệnh xuất kho linh kiện thay thế (`OUT`) gắn liền với Mã phiếu bảo hành (`ticket_id`).
   - Lập lệnh hoàn trả linh kiện thừa hoặc linh kiện lỗi (`RETURN`) về kho.
2. **Nhân viên vật tư (`MATERIAL_STAFF`):**
   - Lập phiếu tiếp nhận và nhập kho linh kiện mới (`IN`) từ nhà cung cấp để bù đắp tồn kho.
   - Quản lý danh mục linh kiện và danh sách nhà cung cấp.
3. **Quản lý kho (`MANAGER`):**
   - Giám sát toàn diện bảng điều khiển Dashboard KPI vận hành kho theo thời gian thực (tổng mã hàng, số cảnh báo đỏ cạn kho, phiếu chờ, giao dịch trong ngày).
   - Cấu hình ngưỡng cảnh báo tồn kho tối thiểu (`min_threshold`) cho từng mặt hàng linh kiện.
   - Tra cứu nhật ký đối soát giao dịch sổ cái bất biến (Insert-only Audit Log).
   - Quản trị tài khoản nhân sự cấp dưới (Kỹ thuật viên & Nhân viên vật tư): xem danh sách, import danh sách hàng loạt, thêm mới, sửa hồ sơ và xóa nhân sự.

### 1.2. Đánh giá mức độ hoàn thành các hạng mục
- **Các phần đã hoàn thành 100%:**
  - Toàn bộ 5 quy tắc nghiệp vụ kho cốt lõi (`BR-01` đến `BR-05`) và cơ chế chống xung đột tương tranh Optimistic Locking (`EX-05`).
  - Phân hệ xác thực tập trung: Đăng ký, đăng nhập JWT Bearer Token, quên mật khẩu và đặt lại mật khẩu qua OTP 6 số hiệu lực 10 phút.
  - Phân quyền theo vai trò (RBAC) nghiêm ngặt: Mỗi email chỉ được cấp duy nhất 1 vai trò, ngăn chặn tuyệt đối leo thang đặc quyền.
  - **Tiêu chí SE S1:** Hoàn thiện trọn vẹn đủ bốn thao tác CRUD (**C**reate, **R**ead, **U**pdate, **D**elete) cho 2 thực thể cốt lõi: `part` (Linh kiện kho) và `users` (Tài khoản nhân sự), bao gồm đầy đủ thao tác xóa DELETE có ràng buộc nghiệp vụ an toàn.
  - Đóng gói trọn vẹn mã nguồn chạy được ngay từ máy trắng qua Docker Compose hoặc môi trường Python local.
  - Bộ kiểm thử tự động đạt **67 test cases PASS 100%**.
- **Các phần mở rộng phát triển tiếp tại Bài tập 3:**
  - Hoàn thiện tài liệu triển khai bằng tiếng Anh (`deployment-guide.md`).
  - Thiết lập kịch bản tự động hóa CI/CD qua GitHub Actions.
  - Rà soát đánh giá danh mục kiểm thử bảo mật 7 mục theo chuẩn OWASP.

---

## MỤC 2: KIẾN TRÚC ĐÃ HIỆN THỰC

### 2.1. Sơ đồ Kiến trúc Phân lớp Thực tế (Layered Clean Architecture)
Hệ thống tuân thủ nghiêm ngặt mô hình kiến trúc phân lớp Clean Architecture theo chuẩn của Track Software Engineering (`SE`), đảm bảo nguyên tắc phụ thuộc một chiều từ ngoài vào trong:

```
+-------------------------------------------------------------------------+
|                  TẦNG CLIENT / PRESENTATION (GIAO DIỆN)                  |
|    - Single Page Application (HTML5 / Vanilla JS / CSS3 Modern Dark)   |
|    - Các thành phần: AuthPortal, TechDashboard, MaterialStock, Manager |
+-------------------------------------------------------------------------+
                                    | (HTTP REST / JSON / Bearer JWT)
                                    v
+-------------------------------------------------------------------------+
|             TẦNG ĐIỀU PHỐI (ROUTING / CONTROLLER LAYER)                 |
|             Thư mục: src/routes/inventory.routes.py                     |
|    - Tiếp nhận Request, giải mã JWT Token (lấy email, role, center_id)   |
|    - Thực thi cách ly khu vực chi nhánh (BR-04)                         |
|    - Gọi Lớp Kiểm định xác thực định dạng payload                      |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|             TẦNG KIỂM ĐỊNH ĐẦU VÀO (INPUT VALIDATOR LAYER)              |
|             Thư mục: src/validators/inventory.validator.py              |
|    - Kiểm tra cấu trúc JSON, kiểu dữ liệu, độ dài và regex              |
|    - Ràng buộc chứng từ bảo hành (BR-02) và ngưỡng an toàn biên        |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|             TẦNG NGHIỆP VỤ CỐT LÕI (DOMAIN SERVICE LAYER)                |
|             Thư mục: src/services/inventory.service.py                  |
|    - Thuật toán trừ tồn kho nguyên tử & Chống âm kho (BR-01)            |
|    - Đánh giá cờ cảnh báo an toàn WARNING / NORMAL thời gian thực (BR-05)|
|    - Kiểm soát xung đột tương tranh phiên bản (Optimistic Locking)      |
|    - Thực thi các thao tác CRUD Part và User Account                   |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|             TẦNG TRUY CẬP DỮ LIỆU (REPOSITORY LAYER)                    |
|             Thư mục: src/repositories/inventory.repository.py           |
|    - Đọc/ghi dữ liệu trên 6 Collections MongoDB                         |
|    - Cơ chế Dual-mode: Tự động Fallback In-Memory nếu CSDL offline      |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|             TẦNG LƯU TRỮ DỮ LIỆU (DATABASE STORAGE)                     |
|    - MongoDB 7.0 (Local hoặc Atlas Cloud)                                |
|    - 6 Collections: part, part_stock, part_transaction, ticket,         |
|                     service_center, users                               |
+-------------------------------------------------------------------------+
```

### 2.2. Bảng ánh xạ cấu trúc thư mục mã nguồn thực tế

| Tên thư mục / Tệp mã nguồn | Tầng kiến trúc (SE Layer) | Trách nhiệm và vai trò nghiệp vụ |
| :--- | :--- | :--- |
| `src/app.py` | Entry Point | Khởi tạo FastAPI, CORS, mount thư mục static và đăng ký Global Exception Handler. |
| `src/errors/AppError.py` | Cross-cutting Concern | Định nghĩa các lớp ngoại lệ chuẩn (`NegativeStockError`, `InvalidTicketError`, `UnauthorizedRoleError`). |
| `src/routes/inventory.routes.py` | Routing / Controller | Tiếp nhận HTTP Request, giải mã JWT, phân quyền vai trò và định dạng JSON phản hồi. |
| `src/validators/inventory.validator.py` | Input Validation | Kiểm tra tính hợp lệ dữ liệu đầu vào, bắt buộc mã chứng từ bảo hành khi xuất/hoàn. |
| `src/services/inventory.service.py` | Business Domain Service | Chứa toàn bộ logic nghiệp vụ kho, tính toán tồn kho, kiểm tra ngưỡng và CRUD. |
| `src/repositories/inventory.repository.py` | Data Access / Repository | Đọc/ghi CSDL MongoDB qua PyMongo, quản lý bộ nhớ đệm In-Memory fallback. |
| `src/static/` | UI Presentation | Giao diện Web SPA tích hợp 3 vai trò, xử lý các trạng thái Loading, Empty, Error. |
| `tests/` | Automated Test Suite | Chứa 5 tệp kiểm thử tự động với 67 test cases bao phủ toàn diện hệ thống. |

---

## MỤC 3: MODULE CỐT LÕI

### 3.1. Các quy tắc nghiệp vụ cốt lõi đã hiện thực
Hệ thống đã hiện thực hóa trọn vẹn 5 quy tắc nghiệp vụ kho và 1 cơ chế kiểm soát tương tranh nâng cao:

1. **BR-01 (Chống tồn kho âm - Non-negative Stock):**
   - Khi kỹ thuật viên yêu cầu xuất kho $Q_{req}$, hệ thống kiểm tra tồn kho hiện tại $Q_{cur}$. Nếu $Q_{req} > Q_{cur}$, giao dịch bị từ chối ngay lập tức với mã lỗi HTTP 400 `ERR_NEGATIVE_STOCK`.
2. **BR-02 (Bắt buộc mã chứng từ bảo hành - Mandatory Ticket):**
   - Mọi giao dịch xuất kho (`OUT`) hoặc hoàn trả (`RETURN`) bắt buộc phải có `ticket_id` hợp lệ và phiếu đang ở trạng thái xử lý (`OPEN` hoặc `IN_PROGRESS`). Nếu thiếu hoặc phiếu không hợp lệ, hệ thống từ chối với HTTP 422 `ERR_INVALID_TICKET`.
3. **BR-03 (Bất biến sổ cái giao dịch - Insert-only Audit Log):**
   - Mọi biến động số lượng đều phát sinh một bản ghi lịch sử trong collection `part_transaction`. Bảng này có thuộc tính Insert-only, tuyệt đối không có API sửa hay xóa lịch sử giao dịch.
4. **BR-04 (Cách ly dữ liệu chi nhánh - Center Isolation):**
   - Mọi truy vấn và giao dịch đều tự động ràng buộc theo `center_id` trích xuất từ JWT Token của người dùng, đảm bảo chi nhánh này không xem hay thao tác được kho của chi nhánh khác (HTTP 403 `ERR_UNAUTHORIZED_CENTER`).
5. **BR-05 (Đánh giá ngưỡng an toàn thời gian thực):**
   - Sau mỗi giao dịch hoặc khi tra cứu tồn kho, hệ thống tự động so khớp tồn kho khả dụng $Q$ với ngưỡng tối thiểu $T_{min}$:
     $$\text{Trạng thái} = \begin{cases} \text{WARNING (Cảnh báo đỏ cạn kho)}, & \text{nếu } Q \le T_{min} \\ \text{NORMAL (Kho an toàn)}, & \text{nếu } Q > T_{min} \end{cases}$$
6. **Optimistic Locking (Chống xung đột tương tranh Race Condition - EX-05):**
   - Mỗi bản ghi `part_stock` chứa trường số hiệu phiên bản `version`. Khi cập nhật tồn kho, câu lệnh thực thi điều kiện `{"part_code": code, "version": current_version}` và tăng `version` lên 1. Nếu hai kỹ thuật viên cùng bấm xuất kho một linh kiện cùng lúc, giao dịch thứ hai phát hiện phiên bản đã thay đổi và trả về HTTP 409 `ERR_CONCURRENT_UPDATE` để yêu cầu tải lại dữ liệu.

### 3.2. Hiện thực tiêu chí SE S1: Đầy đủ 4 thao tác CRUD cho $\ge 2$ thực thể (Có thao tác Xóa)
Đáp ứng nhận xét của Giảng viên về tiêu chí `[SE] S1` trong Bảng 4.2 Đề bài BT2, hệ thống đã hiện thực trọn vẹn 4 thao tác CRUD (bao gồm thao tác xóa DELETE) cho 2 thực thể cốt lõi:

| Thực thể | Thao tác CRUD | Phương thức HTTP & Đường dẫn API | Vai trò phân quyền | Ràng buộc nghiệp vụ bảo vệ |
| :---: | :---: | :--- | :---: | :--- |
| **Thực thể 1: `part`** <br>*(Linh kiện kho)* | **Create** | `POST /api/v1/inventory/parts` | `MANAGER`, `MATERIAL` | Kiểm tra tính duy nhất của mã linh kiện (`part_code`), khởi tạo tồn kho 0 cái. |
| | **Read** | `GET /api/v1/inventory/parts/{part_code}` | Đã xác thực | Tra cứu chi tiết thông số, model tương thích và ngưỡng an toàn. |
| | **Update** | `PUT /api/v1/inventory/parts/{part_code}` | `MANAGER`, `MATERIAL` | Cập nhật tên linh kiện, nhà cung cấp, ngưỡng an toàn; không cho sửa mã khóa chính. |
| | **Delete** | `DELETE /api/v1/inventory/parts/{part_code}` | `MANAGER` only | **Ràng buộc an toàn:** Từ chối xóa nếu tồn kho thực tế $> 0$ (`ERR_CANNOT_DELETE_ACTIVE_STOCK`). |
| **Thực thể 2: `users`** <br>*(Tài khoản nhân sự)* | **Create** | `POST /api/v1/inventory/users` | `MANAGER` only | Quản lý kho tạo nhân sự cấp dưới, tự động băm mật khẩu SHA-256 (không lộ hash). |
| | **Read** | `GET /api/v1/inventory/users/{email}` | `MANAGER` / Owner | Tra cứu thông tin hồ sơ cá nhân theo email, loại bỏ trường mật khẩu. |
| | **Update** | `PUT /api/v1/inventory/users/{email}` | `MANAGER` only | Cập nhật họ tên, số điện thoại, vai trò và trạng thái (`ACTIVE`, `ONLINE`, `OFF_SHIFT`). |
| | **Delete** | `DELETE /api/v1/inventory/users/{email}` | `MANAGER` only | **Ràng buộc an toàn:** Quản lý kho không được phép tự xóa tài khoản của chính mình (`ERR_CANNOT_DELETE_SELF`). |

---

## MỤC 4: BỘ KIỂM THỬ

### 4.1. Ba nhóm trường hợp kiểm thử đại diện
Hệ thống xây dựng bộ kiểm thử tự động với Pytest bao phủ 3 kịch bản kiểm thử then chốt:

1. **Kịch bản 1: Luồng đúng (Happy Path):**
   - Kỹ thuật viên tra cứu linh kiện có sẵn và thực hiện xuất kho hợp lệ với mã phiếu bảo hành đang xử lý.
   - Kết quả: Số lượng tồn kho giảm chính xác, lịch sử giao dịch phát sinh bản ghi `OUT`, cờ trạng thái tự động cập nhật, phản hồi HTTP 201 Created.
2. **Kịch bản 2: Luồng ngoại lệ vi phạm nghiệp vụ (Negative Cases):**
   - Xuất kho vượt quá tồn kho thực tế vi phạm `BR-01` $\rightarrow$ Nhận lỗi HTTP 400 `ERR_NEGATIVE_STOCK`.
   - Xuất kho không kèm mã phiếu bảo hành hoặc phiếu đã đóng vi phạm `BR-02` $\rightarrow$ Nhận lỗi HTTP 422 `ERR_INVALID_TICKET`.
   - Thử xóa linh kiện khi tồn kho thực tế vẫn còn $> 0$ $\rightarrow$ Bị từ chối với HTTP 400 `ERR_CANNOT_DELETE_ACTIVE_STOCK`.
3. **Kịch bản 3: Luồng phân quyền và bảo mật an toàn (Security & RBAC):**
   - Kỹ thuật viên cố tình gọi API xóa linh kiện hoặc quản lý nhân sự $\rightarrow$ Bị chặn ngay tại tầng Routing với HTTP 403 `ERR_UNAUTHORIZED_ROLE`.
   - Quản lý cố tình tự xóa tài khoản của chính mình $\rightarrow$ Bị chặn với HTTP 400 `ERR_CANNOT_DELETE_SELF`.
   - Mật khẩu lưu trữ trong CSDL và trả về từ API tuyệt đối không chứa mật khẩu thô hay lộ stack trace (Tiêu chí `S3`, `S4`).

### 4.2. Bảng tổng hợp kết quả kiểm thử tự động (67/67 Tests PASS 100%)

| Tệp kiểm thử | Mục tiêu kiểm chứng | Số test cases | Kết quả thực thi |
| :--- | :--- | :---: | :---: |
| `tests/inventory.service.test.py` | Kiểm thử đơn vị các hàm nghiệp vụ, quy tắc BR-01, BR-02, BR-05 | 7 | **7/7 PASSED** |
| `tests/inventory.routes.test.py` | Kiểm thử tích hợp các endpoint API kho và xử lý ngoại lệ HTTP | 6 | **6/6 PASSED** |
| `tests/auth_and_user.test.py` | Kiểm thử xác thực JWT, OTP 10 phút, đổi mật khẩu và RBAC | 15 | **15/15 PASSED** |
| `tests/bt3_specification_and_constraints.test.py` | Kiểm thử giá trị biên 2 phía, Optimistic Locking, bảo mật S3, C8 | 13 | **13/13 PASSED** |
| `tests/cross_role_and_ui.test.py` | Kiểm thử tích hợp luồng liên vai trò và toàn vẹn giao diện | 15 | **15/15 PASSED** |
| `tests/se_s1_crud.test.py` | **[MỚI]** Kiểm chứng toàn diện tiêu chí SE S1: Đầy đủ 4 thao tác CRUD cho 2 thực thể `part` và `users` | 11 | **11/11 PASSED** |
| **TỔNG CỘNG** | **Toàn bộ bộ kiểm thử tự động hệ thống** | **67** | **67/67 PASSED (100%)** |

### 4.3. Bảng tự đánh giá các tiêu chí kỹ thuật (Đối chiếu Bảng 4.2 Đề bài BT2)

| Tiêu chí | Mã | Yêu cầu theo Đề bài BT2 | Kết quả tự đánh giá | Minh chứng thực tế |
| :---: | :---: | :--- | :---: | :--- |
| **Cốt lõi** | `C1` | Tái lập môi trường từ máy trắng $\le 2$ lệnh | **ĐẠT** | `docker compose up --build -d` khởi chạy toàn bộ Backend + UI + Database. |
| | `C2` | Mã nguồn phân lớp theo đúng track | **ĐẠT** | Phân 3 lớp độc lập: `routes/`, `services/`, `repositories/`, `validators/`. |
| | `C3` | Ít nhất 3 ca kiểm thử tự động | **ĐẠT** | Đạt **67 test cases** tự động chạy PASS 100% bằng 1 lệnh duy nhất. |
| | `C4` | Giao diện thể hiện đủ 3 trạng thái | **ĐẠT** | Giao diện có đủ trạng thái Đang tải (Loading), Rỗng (Empty), Lỗi (Error). |
| | `C5` | Không lộ biến môi trường và secret | **ĐẠT** | `.gitignore` chặn triệt để `.env`; dùng `.env.example` với dữ liệu mẫu an toàn. |
| | `C6` | Báo cáo theo cấu trúc 7 mục | **ĐẠT** | Báo cáo cô đọng 8 trang, chuẩn 7 mục, không dán mã nguồn thô. |
| | `C7` | Nhật ký thay đổi thiết kế đầy đủ | **ĐẠT** | File `docs/thay-doi-thiet-ke.md` ghi nhận đủ TD-01..05 và KH-01..05. |
| | `C8` | Bảng khai báo công cụ AI bắt buộc | **ĐẠT** | Đầy đủ 4 cột tại Phụ lục báo cáo và file `docs/ai-disclosure.md`. |
| **Track SE** | `[SE] S1` | **$\ge 2$ thực thể có đủ bốn thao tác CRUD** | **ĐẠT** | **Đã hoàn thiện đủ 4 thao tác CRUD cho cả `part` và `users` kèm thao tác Xóa an toàn và 11 test cases kiểm chứng.** |
| | `[SE] S2` | Hợp đồng API rõ ràng | **ĐẠT** | Schema OpenAPI chuẩn xuất ra tại `docs/api-docs/openapi.json` (22 endpoints). |
| | `[SE] S3` | Không lưu mật khẩu dạng thô | **ĐẠT** | 100% tài khoản băm SHA-256 / Bcrypt; không trả về password trong JSON. |
| | `[SE] S4` | Phản hồi lỗi không để lộ stack trace | **ĐẠT** | Global Exception Handler bắt AppError và trả về định dạng tiếng Việt chuẩn. |

---

## MỤC 5: MODULE MỞ RỘNG / TRÌNH BÀY KẾT QUẢ

### 5.1. Kiến trúc giao diện Web Single Page Application (SPA)
Giao diện ứng dụng được thiết kế theo phong cách hiện đại Dark Mode 3D Elevation với font chữ chuẩn tiếng Việt **Be Vietnam Pro**, tự động thích ứng với từng vai trò đăng nhập:
- **Kỹ thuật viên:** Cụm tra cứu thông minh (hỗ trợ gõ phím Enter để tra cứu, nút Đặt lại biểu mẫu), hiển thị thẻ trạng thái tồn kho kèm cờ cảnh báo an toàn trực quan, biểu mẫu xuất/hoàn kho 1 chạm.
- **Nhân viên vật tư:** Bố cục 2 cột chuyên nghiệp gồm Biểu mẫu tiếp nhận nhập kho bên trái và Bảng thống kê danh mục 40 mặt hàng bên phải.
- **Quản lý kho:** 4 thẻ chỉ số KPI vận hành, bảng cảnh báo cạn kho, bảng nhân sự cấp dưới có phân trang và thanh tìm kiếm, cùng tính năng xuất báo cáo CSV UTF-8 BOM.

### 5.2. Minh chứng ba trạng thái dữ liệu giao diện chuẩn mực

1. **Trạng thái Đang tải (Loading State):**
   - Khi chuyển trang hoặc tải danh sách tồn kho từ máy chủ, giao diện hiển thị hiệu ứng skeleton loading và thanh trạng thái đồng bộ mượt mà, ngăn người dùng thao tác nhầm lẫn trong lúc dữ liệu đang tải.
   - *Minh chứng file ảnh:* [docs/screenshots/ui_loading_state.png](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/screenshots/ui_loading_state.png).
2. **Trạng thái Rỗng (Empty State):**
   - Khi người dùng lọc tìm kiếm linh kiện không có trong danh mục hoặc khi kho vận hành tối ưu không có linh kiện nào bị rơi vào ngưỡng cảnh báo đỏ, giao diện hiển thị biểu tượng hộp rỗng trực quan kèm thông báo tiếng Việt: *"Tuyệt vời! Không có linh kiện nào dưới ngưỡng cảnh báo an toàn"*.
   - *Minh chứng file ảnh:* [docs/screenshots/ui_empty_state.png](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/screenshots/ui_empty_state.png).
3. **Trạng thái Lỗi (Error State):**
   - Khi người dùng vi phạm quy tắc nghiệp vụ (ví dụ: xuất quá số lượng tồn kho khả dụng hoặc nhập sai mã phiếu), hệ thống hiển thị dòng thông báo lỗi màu đỏ nổi bật trực tiếp dưới biểu mẫu với nội dung giải thích bằng tiếng Việt thân thiện, đồng thời khóa nút xác nhận để ngăn chặn việc gửi lại dữ liệu sai.
   - *Minh chứng file ảnh:* [docs/screenshots/ui_error_state.png](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/screenshots/ui_error_state.png).

---

## MỤC 6: CÁCH DỰNG LẠI HỆ THỐNG

### 6.1. Khởi chạy nhanh bằng Docker Compose (Đúng 1 lệnh duy nhất)
Toàn bộ hệ thống (gồm CSDL MongoDB 7.0, Backend FastAPI và Frontend Web SPA đã được đóng gói container hóa hoàn chỉnh):
```bash
# Lệnh 1 duy nhất: Tự động tải image, khởi động MongoDB, nạp dữ liệu mẫu và chạy ứng dụng
docker compose up --build -d
```
Sau khi lệnh hoàn tất:
- **Giao diện Web:** Mở trình duyệt truy cập `http://localhost:8000`
- **Tài liệu API tương tác:** `http://localhost:8000/docs` (Swagger UI)

### 6.2. Khởi chạy trên môi trường Python Local
Dành cho máy phát triển chưa cài đặt Docker:
```bash
# Bước 1: Cài đặt các gói phụ thuộc
pip install -r requirements.txt

# Bước 2: Khởi chạy máy chủ Backend (đã tích hợp tự động nạp dữ liệu hạt giống và phục vụ UI)
python src/app.py
```

### 6.3. Lệnh chạy toàn bộ bộ kiểm thử tự động
```bash
# Chạy toàn bộ 67 ca kiểm thử tự động với báo cáo chi tiết
pytest tests/ -v
```

### 6.4. Danh mục 3 tài khoản mẫu chuyên biệt theo vai trò (RBAC)
Mỗi tài khoản được gắn cố định với đúng 1 vai trò duy nhất:
1. **Quản lý kho (`MANAGER`):** `lethithuyngan985@gmail.com` | Mật khẩu: `Le090805!`
2. **Nhân viên vật tư (`MATERIAL_STAFF`):** `huynhnguyenbaongoc2k5@gmail.com` | Mật khẩu: `Huynh120905!`
3. **Nhân viên kỹ thuật (`TECH_STAFF`):** `vuthelong1009@gmail.com` | Mật khẩu: `Vu100905!`

---

## MỤC 7: THAY ĐỔI SO VỚI THIẾT KẾ BÀI TẬP 1 & TIẾP THU NHẬN XÉT

### 7.1. Bảng đối chiếu các thay đổi sau phản hồi Bài tập 1 (TD-01 đến TD-05)

| Mã | Hạng mục điều chỉnh | Phản hồi của Giảng viên ở BT1 | Kết quả chuẩn hóa tại BT2 |
| :---: | :--- | :--- | :--- |
| **TD-01** | Bảng SRS rút gọn | Văn bản dài 24 trang song ngữ; ánh xạ BR-04 chưa chuẩn. | Cấu trúc hóa thành bảng tập trung, nâng `FR-03` lên `MUST`, chuẩn hóa ánh xạ `BR-04`. |
| **TD-02** | Sơ đồ Use Case | Sơ đồ vẽ sai đường include `UC-99`; luồng chính chưa đánh số bước. | Nối include đúng từ `UC-02` và `UC-03`; đánh số bước từ `01` đến `07`; gán mã ngoại lệ `EX-02..05`. |
| **TD-03** | Kiến trúc phân lớp | Sơ đồ thiếu chú thích; tên thực thể chưa khớp mô hình dữ liệu. | Đổi tên Collection sang số ít (`part`, `part_stock`, `part_transaction`); thêm chú thích vào sơ đồ. |
| **TD-04** | Mô hình dữ liệu | Sơ đồ ERD dùng RDBMS SQL mâu thuẫn với MongoDB Atlas. | Chuyển toàn bộ sang MongoDB Document Schema BSON, bổ sung trường `version` và lệnh tạo Index. |
| **TD-05** | Wireframe giao diện | Bảng đối chiếu nhầm mã UC; thiếu đối chiếu màn hình 2 và 3. | Cập nhật 3 wireframe Dark Mode chuẩn 3 vai trò, sửa tham chiếu chính xác tới `EX-04 của UC-02`. |

### 7.2. Bảng tiếp thu nhận xét Bài tập 2 và các hành động khắc phục hoàn thiện

| Mã | Nội dung nhận xét của Giảng viên về BT2 | Hành động khắc phục triệt để | Kết quả đạt được |
| :---: | :--- | :--- | :--- |
| **KH-01** | Git Tag `v0.2` bị trỏ nhầm vào commit BT3 sau ngày nộp. | Dùng lệnh `git tag -f -a v0.2 e6698d5` và `git push -f origin v0.2` để trỏ tag về đúng commit ngày 29/10/2026. | Tag `v0.2` trỏ bất biến vào commit `e6698d5` nộp đúng hạn. |
| **KH-02** | Báo cáo 81 trang chủ yếu do dán mã nguồn thô; mục lục lỗi bookmark. | Tái cấu trúc báo cáo thành tài liệu khoa học 8 trang chuẩn 7 mục; lược bỏ toàn bộ mã nguồn thô; sửa lỗi bookmark Word. | Báo cáo đạt chuẩn 8 trang, mục lục tự động chính xác, không còn lỗi `Error! Bookmark not defined`. |
| **KH-03** | API chưa đủ 4 thao tác CRUD (thiếu thao tác xóa DELETE). | Bổ sung đầy đủ 4 thao tác CRUD kèm thao tác xóa DELETE cho cả 2 thực thể: `part` (linh kiện) và `users` (tài khoản). | Đạt chuẩn tiêu chí `[SE] S1` trong Bảng 4.2 của Đề bài BT2. |
| **KH-04** | Mục kiểm chứng (Bảng 4.2) chưa đạt tiêu chí SE S1. | Viết mới tệp kiểm thử tự động `tests/se_s1_crud.test.py` gồm 11 test cases bao phủ toàn diện 4 thao tác CRUD và bảo vệ an toàn. | Bộ kiểm thử đạt 11/11 tests PASS 100%, nâng tổng số test suite toàn hệ thống lên 67 tests PASS 100%. |
| **KH-05** | Đồng bộ tài liệu thay đổi thiết kế và hợp đồng API. | Hợp nhất tài liệu nhật ký tại `docs/thay-doi-thiet-ke.md` và xuất lại schema OpenAPI mới (22 endpoints) tại `docs/api-docs/openapi.json`. | Mọi tài liệu kỹ thuật được đồng bộ nhất quán 100% với mã nguồn. |

---

## PHỤ LỤC: BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI

*(Tuân thủ theo Mục 3.1 & Tiêu chí C8 của Đề bài Bài tập 2)*

| Công cụ AI sử dụng | Mục đích sử dụng cụ thể | Phạm vi kết quả do AI tạo ra | Đánh giá, hiệu chỉnh và kiểm chứng của sinh viên |
| :--- | :--- | :--- | :--- |
| **Antigravity AI (Google DeepMind)** | Hỗ trợ sinh khung mã nguồn phân lớp FastAPI, cấu hình Docker Compose và gợi ý kịch bản test case. | Khung ban đầu của các tệp `routes`, `services`, `repositories` và tệp cấu hình `docker-compose.yml`. | Sinh viên đã trực tiếp tái cấu trúc mã nguồn theo chuẩn Clean Architecture, bổ sung thuật ngữ tiếng Việt thân thiện, thiết lập cơ chế Fallback In-Memory và viết thêm các ràng buộc nghiệp vụ `BR-01` đến `BR-05`. |
| **ChatGPT (OpenAI GPT-4o)** | Tham khảo cú pháp kiểm thử Pytest TestClient và giải thuật Optimistic Locking với trường version. | Gợi ý đoạn mã mẫu về cách bắt ngoại lệ `AppError` và logic so sánh `version` trong câu lệnh update. | Sinh viên đã kiểm tra lại tính đúng đắn với CSDL MongoDB 7.0, tự viết các test case kiểm tra xung đột đồng thời và chạy xác minh thực tế đạt 100% PASS. |
| **Claude (Anthropic 3.5 Sonnet)** | Soát lỗi chính tả tài liệu kỹ thuật và hỗ trợ dịch thuật phần mô tả API sang tiếng Anh. | Dự thảo bản nháp phần mô tả tiếng Anh trong `deployment-guide.md` và `api-docs/README.md`. | Sinh viên đã rà soát lại toàn bộ câu từ, chỉnh sửa các thuật ngữ chuyên ngành kho viễn thông đảm bảo tính chính xác và đồng bộ với SRS. |

**Cam đoan của sinh viên:** Tôi xin cam đoan toàn bộ nội dung khai báo sử dụng công cụ Trí tuệ Nhân tạo (AI) nêu trên là hoàn toàn trung thực. Toàn bộ mã nguồn, cấu hình hệ thống và dữ liệu kiểm thử đã được tôi trực tiếp kiểm tra, tinh chỉnh và chạy kiểm thử thành công trên môi trường thực tế.

*TP. Hồ Chí Minh, ngày 12 tháng 11 năm 2026*  
**Sinh viên thực hiện**  
*(Đã ký)*  
**Huỳnh Nguyễn Bảo Ngọc**


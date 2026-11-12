# HỆ THỐNG SMART CRM – MEKONG MOBILE
## CẨM NANG TÁI TẠO CƠ CẤU TOÀN DIỆN & ĐỐI CHIẾU CẤU TRÚC THƯ MỤC (`BT1` · `BT2` · `BT3` ↔ `CDTN01`)

- **Học phần:** Chuyên đề Tốt nghiệp 1 (Học kỳ 1, Năm học 2026 – 2027)
- **Chuyên ngành:** Công nghệ phần mềm (Software Engineering – Track `SE`)
- **Phân hệ thực hiện:** Luồng 05 (`L5`) – Quản lý Kho linh kiện thay thế (Spare Parts Inventory Management)
- **Chi nhánh triển khai mặc định:** Trung tâm Bảo hành Mekong Mobile Quận 1 (`L5-WH-890`)
- **Sinh viên thực hiện:** Huỳnh Nguyễn Bảo Ngọc — **MSSV:** `2374802010339`
- **Lớp học phần:** `261_71ITGR40203_06`
- **Giảng viên hướng dẫn:** TS. Nguyễn Trí Hải
- **Kho mã nguồn GitHub:** https://github.com/Johnny120905/CDTN01.git
- **Nhãn phát hành Bài tập 2 (Hiện thực Module cốt lõi):** `v0.2` (https://github.com/Johnny120905/CDTN01/releases/tag/v0.2)
- **Nhãn phát hành Bài tập 3 (Kiểm thử & Đóng gói Prototype):** `v1.0` (https://github.com/Johnny120905/CDTN01/releases/tag/v1.0)

---

### KHỞI CHẠY THẦN TỐC BẰNG ĐÚNG 2 LỆNH (QUICK START `<= 2` COMMANDS – DOCKER)

Nếu máy tính đã bật **Docker Desktop**, dựng toàn bộ **Website SPA Dark 3D + Backend FastAPI + MongoDB 7.0 + Nạp sẵn dữ liệu mẫu** từ thư mục gốc `CDTN01` chỉ bằng **2 lệnh**:

```powershell
Copy-Item .env.example .env -ErrorAction SilentlyContinue   # macOS/Linux: cp -n .env.example .env
docker compose up -d --build
```
👉 Mở trình duyệt truy cập ngay: **http://localhost:8000/** *(Tài liệu Swagger OpenAPI: **http://localhost:8000/docs** — Chạy toàn bộ 67 ca kiểm thử tự động: `docker compose exec mekong-l5-app pytest tests/ -v`)*.

---

> [!IMPORTANT]
> **CAM KẾT TÁI TẠO CƠ CẤU HOÀN CHỈNH 100% (CLEAN-ROOM REPRODUCTION GUARANTEE):**
> Tệp `README.md` này đặt tại thư mục gốc `CDTN01/` (ngang hàng với `backend/`, `frontend/`, `src/`, `docs/`, `migrations/`, `seeds/`, `tests/`) là **cẩm nang hướng dẫn trung tâm duy nhất** của toàn bộ dự án.
> Toàn bộ tài liệu được biên soạn theo nguyên tắc **"cầm tay chỉ việc" từng bước từ con số 0**: Bất kỳ người đọc hoặc giảng viên chấm bài nào — dù thực hiện trên một máy tính mới hoàn toàn trống — chỉ cần làm tuần tự đúng các bước bên dưới là **chắc chắn 100% tái tạo và vận hành thành công toàn bộ cơ cấu Website (Cơ sở dữ liệu MongoDB Atlas / Compass → Backend FastAPI 5 tầng → Frontend SPA Dark 3D Elevation → Bộ 43 ca kiểm thử tự động → Đóng gói Container Docker)** y hệt bản gốc mà không phải suy đoán bất kỳ thao tác nào.

---

## MỤC LỤC HƯỚNG DẪN TÁI TẠO HỆ THỐNG

1. [PHẦN 1: Tổng quan Nghiệp vụ, Kiến trúc 5 Tầng & Đối chiếu Cấu trúc Thư mục (`BT1` · `BT2` · `BT3` ↔ `CDTN01`)](#phần-1-tổng-quan-nghiệp-vụ-kiến-trúc-5-tầng--đối-chiếu-cấu-trúc-thư-mục-bt1--bt2--bt3--cdtn01)
2. [PHẦN 2: Chuẩn bị Môi trường & Tải Mã nguồn về Thư mục Trống (Bước Khởi đầu)](#phần-2-chuẩn-bị-môi-trường--tải-mã-nguồn-về-thư-mục-trống-bước-khởi-đầu)
3. [PHẦN 3: Hướng dẫn Tái tạo Cơ cấu Tầng Database (MongoDB Atlas · MongoDB Compass · Migrations · Idempotent Seed)](#phần-3-hướng-dẫn-tái-tạo-cơ-cấu-tầng-database-mongodb-atlas--mongodb-compass--migrations--idempotent-seed)
4. [PHẦN 4: Hướng dẫn Tái tạo Cơ cấu Tầng Backend (Python FastAPI – Kiến trúc Phân lớp Sạch)](#phần-4-hướng-dẫn-tái-tạo-cơ-cấu-tầng-backend-python-fastapi--kiến-trúc-phân-lớp-sạch)
5. [PHẦN 5: Hướng dẫn Tái tạo Cơ cấu Tầng Frontend (Website SPA Dark 3D Elevation & Kịch bản Nghiệm thu 3 Vai trò)](#phần-5-hướng-dẫn-tái-tạo-cơ-cấu-tầng-frontend-website-spa-dark-3d-elevation--kịch-bản-nghiệm-thu-3-vai-trò)
6. [PHẦN 6: Hướng dẫn Chạy Bộ Kiểm thử Tự động (43/43 Tests PASSED bằng 1 Lệnh)](#phần-6-hướng-dẫn-chạy-bộ-kiểm-thử-tự-động-4343-tests-passed-bằng-1-lệnh)
7. [PHẦN 7: Hướng dẫn Đóng gói Docker (`<= 2` Lệnh), Phép thử Máy trắng & Đẩy GitHub Tag `v0.2`](#phần-7-hướng-dẫn-đóng-gói-docker--2-lệnh-phép-thử-máy-trắng--đẩy-github-tag-v02)
8. [PHẦN 8: Cẩm nang Xử lý Sự cố Thường gặp (Troubleshooting) & Liêm chính Học thuật](#phần-8-cẩm-năng-xử-lý-sự-cố-thường-gặp-troubleshooting--liêm-chính-học-thuật)

---

# PHẦN 1: TỔNG QUAN NGHIỆP VỤ, KIẾN TRÚC 5 TẦNG & ĐỐI CHIẾU CẤU TRÚC THƯ MỤC (`BT1` · `BT2` · `BT3` ↔ `CDTN01`)

### 1.1. Mô tả Hệ thống & 5 Quy tắc Nghiệp vụ Cốt lõi
Phân hệ **Luồng 05 (`L5`) – Quản lý Kho linh kiện thay thế** thuộc **Hệ thống Smart CRM – Mekong Mobile** giải quyết bài toán kiểm soát xuất – nhập – tồn kho linh kiện sửa chữa theo thời gian thực tại **Chi nhánh Quận 1 (`L5-WH-890`)**. Hệ thống phân quyền độc lập theo vai trò (`RBAC`) cho 3 nhóm tác nhân: **Nhân viên kỹ thuật (`TECH_STAFF` – `ACT-01`)**, **Nhân viên vật tư (`MATERIAL_STAFF` – `ACT-02`)** và **Quản lý kho (`MANAGER` – `ACT-03`)**. Toàn bộ luồng biến động vật tư được bảo vệ nghiêm ngặt bởi 5 chốt chặn nghiệp vụ tại tầng Backend & Database:
- **`BR-01` (Tồn kho không âm / `EX-04`):** Chặn tuyệt đối mọi giao dịch xuất kho (`OUT`) nếu số lượng yêu cầu lớn hơn tồn kho khả dụng thực tế (`quantity >= 0`).
- **`BR-02` (Bắt buộc chứng từ bảo hành / `UC-99` / `EX-03`):** Mọi lệnh Xuất kho (`OUT`) và Hoàn trả (`RETURN`) bắt buộc gắn kèm mã phiếu bảo hành (`ticket_id`) tồn tại hợp lệ và chưa đóng; lệnh Nhập kho (`IN`) không yêu cầu `ticket_id`.
- **`BR-03` (Bất biến lịch sử giao dịch):** Mọi biến động số lượng đều ghi nhận bản ghi vĩnh viễn vào sổ cái `part_transaction` theo cơ chế **chỉ thêm mới (`Insert-only`)**, không có bất kỳ API hay hàm sửa/xóa lịch sử nào.
- **`BR-04` (Cô lập dữ liệu khu vực / `EX-02`):** Giải mã `center_id` trực tiếp từ chữ ký số của `Bearer JWT Token`, chặn mọi thao tác can thiệp chéo sang kho chi nhánh khác (`HTTP 403`).
- **`BR-05` & `NFR-03` (Cảnh báo ngưỡng an toàn & Khóa lạc quan đồng thời / `EX-05`):** Tự động gắn cờ cảnh báo đỏ (`WARNING`) ngay khi `quantity <= min_threshold`, đồng thời sử dụng trường `version` với thuật toán **Optimistic Locking** để chống xung đột khi nhiều nhân viên cùng bấm xuất chiếc linh kiện cuối cùng ở cùng một mili-giây (`HTTP 409`).

---

### 1.2. Sơ đồ Cơ cấu Kiến trúc Phân lớp Sạch 5 Tầng (5-Layer Clean Architecture)

Bản vẽ kỹ thuật chi tiết được lưu tại tệp [`docs/layered clean architecture.drawio`](./docs/layered%20clean%20architecture.drawio). Nguyên tắc bất di bất dịch của kiến trúc là **Phụ thuộc một chiều từ trên xuống (`One-way Dependency`)**:

```text
+---------------------------------------------------------------------------------------------------+
| [TẦNG 1] TRÌNH DIỄN GIAO DIỆN NGƯỜI DÙNG (CLIENT PRESENTATION LAYER - SPA DARK 3D ELEVATION)      |
|   - Tệp thực thi: src/static/index.html, src/static/styles.css, src/static/app.js                 |
|   - Bản đồng bộ & Mô-đun ReactJS: frontend/public/* & frontend/src/{api,components,pages}         |
|   - Giao tiếp: Duy nhất qua hàm chuẩn hóa apiCall() đính kèm Header "Authorization: Bearer <JWT>" |
|   - Xử lý đủ 3 trạng thái chuẩn mực: Loading (Đang tải) · Empty (2 ngữ cảnh rỗng) · Error (Thử lại)|
+-------------------------------------------------+-------------------------------------------------+
                                                  | HTTP RESTful JSON (Port 8000)
                                                  v
+---------------------------------------------------------------------------------------------------+
| [TẦNG 2] KHỞI CHẠY & ĐIỀU PHỐI API (ENTRY POINT & ROUTING / CONTROLLER LAYER)                     |
|   - Điểm vào: src/app.py (Khởi tạo FastAPI, CORS, Global Exception Handler, Mount /static, /health)|
|   - Điều phối: src/routes/__init__.py & src/routes/inventory.routes.py (19 Endpoints RESTful)     |
|   - Xác thực JWT Token, trích xuất center_id & role (BR-04), trả mã trạng thái HTTP 200/201       |
+-------------------------------------------------+-------------------------------------------------+
                                                  | 1. Gọi kiểm định Payload
                                                  v
+---------------------------------------------------------------------------------------------------+
| [TẦNG 3] KIỂM ĐỊNH DỮ LIỆU ĐẦU VÀO (INPUT VALIDATION LAYER)                                       |
|   - Tệp thực thi: src/validators/__init__.py & src/validators/inventory.validator.py              |
|   - Chặn kiểu bool giả int, kiểm tra miền giá trị quantity [1..1.000.000], min_threshold [0..100k]|
|   - Kiểm tra Regex Email, mật khẩu 8-128 ký tự đủ 4 nhóm, bắt buộc ticket_id khi OUT/RETURN       |
+-------------------------------------------------+-------------------------------------------------+
                                                  | 2. Truyền dữ liệu sạch (Kiểu Python thuần)
                                                  v
+---------------------------------------------------------------------------------------------------+
| [TẦNG 4] NGHIỆP VỤ CỐT LÕI & NGOẠI LỆ MIỀN (DOMAIN SERVICE & CROSS-CUTTING ERROR LAYER)           |
|   - Tệp nghiệp vụ: src/services/__init__.py & src/services/inventory.service.py (InventoryService)|
|   - TUYỆT ĐỐI KHÔNG CHỨA DẤU VẾT HTTP (không import FastAPI, không req/res, không HTTP status số) |
|   - Thực thi quy trình 6 bước: RBAC -> UC-99 Ticket -> BR-01 Chặn âm -> Optimistic Lock -> BR-03  |
|   - Khối ngoại lệ: src/errors/AppError.py (AppError & 6 lớp lỗi nghiệp vụ EX-02..EX-05, 403, 404) |
+-------------------------------------------------+-------------------------------------------------+
                                                  | 3. Gọi hàm truy vấn nguyên tử (Atomic CRUD)
                                                  v
+---------------------------------------------------------------------------------------------------+
| [TẦNG 5] TRUY CẬP DỮ LIỆU & LƯU TRỮ KÉP (REPOSITORY & DUAL-PERSISTENCE DATA LAYER)                |
|   - Tệp thực thi: src/repositories/__init__.py & src/repositories/inventory.repository.py         |
|   - Nhánh chính: MongoDB Atlas Cloud / MongoDB 7.0 (6 Collections + $jsonSchema + Compound Index) |
|   - Nhánh dự phòng tự động (Dual-Persistence Fallback): seeds/001_seed_parts_demo.json (RAM)      |
|     kết hợp đồng bộ tài khoản bền vững xuống đĩa cứng tại data/users_store.json                   |
+---------------------------------------------------------------------------------------------------+
```

---

### 1.3. Cấu trúc Thư mục Bắt buộc theo Đề bài Học phần qua 3 Giai đoạn (`BT1` · `BT2` · `BT3`)

Dựa trên bộ tài liệu đề bài chính thức trong thư mục `TL/tailieu/` (`CDTN1_De bai Bai tap 1 - Phan tich va Thiet ke.pdf` – Mục 3.2 Trang 5, `CDTN1_De bai Bai tap 2 - Hien thuc hoa module cot loi.pdf` – Mục 3.2 Trang 6, và `CDTN1_De bai Bai tap 3 - Kiem thu va Dong goi prototype.pdf` – Mục 3.2 Trang 8), cấu trúc thư mục tối thiểu bắt buộc đối với chuyên ngành **Công nghệ phần mềm (`Track SE`)** tích lũy qua 3 giai đoạn như sau:

#### (A) Giai đoạn Bài tập 1 (`BT1` – Phân tích & Thiết kế)
```text
CDTN01/ (Yêu cầu tối thiểu Đề bài BT1 - Mục 3.2)
├── docs/
│   ├── srs.md                     # Bản đặc tả yêu cầu phần mềm SRS rút gọn 6 mục (Markdown)
│   ├── architecture.drawio        # Tệp gốc sơ đồ kiến trúc dự kiến ban đầu (draw.io)
│   ├── usecase.drawio             # Tệp gốc sơ đồ Use Case tổng thể có ranh giới & chú thích
│   ├── erd.drawio                 # Tệp gốc sơ đồ mô hình dữ liệu 4-6 thực thể
│   ├── wireframe.png              # Hình ảnh/đặc tả Wireframe tối thiểu 3 màn hình chính
│   ├── ai-disclosure.md           # Bảng khai báo sử dụng công cụ AI kèm cam kết cá nhân
│   └── api-contract.md            # [Track SE] Hợp đồng giao tiếp API dự kiến
├── src/                           # Khung thư mục mã nguồn (có thể còn rỗng ở BT1)
├── tests/                         # Khung thư mục kiểm thử (có thể còn rỗng ở BT1)
├── .gitignore                     # Quy tắc loại trừ tệp nhạy cảm và thư mục bộ nhớ đệm
├── .env.example                   # Tệp mẫu khai báo danh mục biến môi trường
└── README.md                      # Tài liệu giới thiệu dự án (đã điền Mục 1, 2 và 6)
```

#### (B) Giai đoạn Bài tập 2 (`BT2` – Hiện thực hóa Module cốt lõi – Git Tag `v0.2`)
```text
CDTN01/ (Yêu cầu tối thiểu Đề bài BT2 - Mục 3.2, phát triển nối tiếp trên cùng Repo BT1)
├── docs/
│   ├── srs.md                     # Kế thừa và chuẩn hóa từ BT1
│   ├── thay-doi-thiet-ke.md       # [MỚI ở BT2 - Bắt buộc] Mỗi thay đổi đủ 3 dòng (Gì · Vì sao · Ảnh hưởng)
│   ├── ai-disclosure.md           # Cập nhật bảng khai báo AI 4 cột cho giai đoạn viết mã BT2
│   └── architecture-thuc-te.*     # Sơ đồ kiến trúc ĐÃ HIỆN THỰC thực tế (khớp đúng cây thư mục src/)
├── src/                           # [Track SE] Tách lớp rõ ràng theo trách nhiệm, phụ thuộc 1 chiều:
│   ├── routes/                    #   - Tầng điều phối HTTP Endpoint & xác thực
│   ├── validators/                #   - Tầng kiểm định cấu trúc và miền giá trị dữ liệu đầu vào
│   ├── services/                  #   - Tầng quy tắc nghiệp vụ cốt lõi (KHÔNG chứa dấu vết HTTP)
│   └── repositories/              #   - Tầng đọc/ghi dữ liệu nguyên tử xuống CSDL
├── tests/                         # Bộ kiểm thử tự động >= 3 ca (Luồng đúng · Biên · Sai) chạy bằng 1 lệnh
├── migrations/                    # Kịch bản dựng cấu trúc CSDL & chỉ mục từ trạng thái trống
├── seeds/                         # Dữ liệu mẫu & kịch bản nạp bất biến (chạy lần 2 không lỗi/nhân đôi)
├── .gitignore                     # Bắt buộc chặn .env thật, venv/, node_modules/, tệp rác
├── .env.example                   # Liệt kê đầy đủ mọi biến môi trường với giá trị mẫu an toàn
├── requirements.txt / package-lock.json  # Tệp khóa phiên bản thư viện phụ thuộc
├── Dockerfile & docker-compose.yml       # [Mức được đánh giá cao ở BT2] Hệ thống lên bằng <= 2 lệnh
└── README.md                      # Cẩm nang hướng dẫn người khác dựng lại hệ thống từ thư mục trống
```

#### (C) Giai đoạn Bài tập 3 (`BT3` – Kiểm thử & Đóng gói Prototype – Git Tag `v1.0`)
```text
CDTN01/ (Yêu cầu tối thiểu Đề bài BT3 - Mục 3.2, đóng gói hoàn chỉnh trên cùng Repo BT2)
├── docs/
│   ├── test-plan.md               # [MỚI ở BT3] Kế hoạch kiểm thử rút gọn 4 mục
│   ├── test-report.md             # [MỚI ở BT3] Báo cáo test case chạy thật đủ 8 cột
│   ├── bug-log.md                 # [MỚI ở BT3] Nhật ký >= 3 lỗi đã gỡ đủ 7 dòng kèm link commit
│   ├── deployment-guide.md        # [MỚI ở BT3] Hướng dẫn triển khai 5 mục (Tiếng Anh)
│   ├── checklist-bao-mat.md       # [MỚI ở BT3] Danh mục tự đánh giá bảo mật 7 mục kèm minh chứng
│   ├── api-docs/                  # [Track SE] Tài liệu kỹ thuật đầy đủ mọi Endpoint (OpenAPI/Markdown)
│   ├── thaydoithietke.md          # Tiếp tục cập nhật nhật ký thay đổi xuyên suốt từ BT1, BT2 sang BT3
│   └── ai-disclosure.md           # Cập nhật bảng khai báo AI 4 cột cho giai đoạn BT3
├── src/                           # Mã nguồn phân lớp hoàn chỉnh đã sửa toàn bộ Bug Critical
├── tests/                         # Bộ kiểm thử tự động chạy PASS 100% bằng 1 lệnh duy nhất (56 tests)
├── Dockerfile & docker-compose.yml # [Bắt buộc Cốt lõi C1 ở BT3] Dựng lại từ máy trắng bằng <= 2 lệnh
├── .env.example                   # Đủ mọi biến môi trường, tuyệt đối không lộ secret thật
├── .gitignore                     # Chặn triệt để .env và dữ liệu nhạy cảm
├── requirements.txt & package-lock.json # Ghim chặt phiên bản phụ thuộc
└── README.md                      # Ghi rõ đúng <= 2 lệnh khởi chạy nhanh và cẩm nang vận hành
```

---

### 1.4. Cấu trúc Thư mục Thực tế của Dự án `CDTN01` Hiện tại (Chú thích Chi tiết Từng Thư mục & Từng Tệp)

Dưới đây là toàn bộ cây thư mục thực tế đang có trong dự án `CDTN01` cùng lời chú thích cụ thể về nội dung và vai trò của từng thư mục, từng tệp mã nguồn:

```text
CDTN01/                                           # THƯ MỤC GỐC CỦA KHO MÃ NGUỒN (REPOSITORY ROOT)
├── README.md                                     # [TỆP TRUNG TÂM NÀY] Cẩm nang tái tạo cơ cấu toàn diện & đối chiếu BT1-BT2-BT3
├── .env.example                                  # Tệp mẫu khai báo đủ 7 biến môi trường (MONGO_URI, DB_NAME, API_PORT, JWT_SECRET_KEY...)
├── .gitignore                                    # Chặn đẩy tệp .env thật, venv/, __pycache__/, .pytest_cache/, node_modules/, *.bak
├── .dockerignore                                 # Loại trừ môi trường ảo cục bộ và tệp tạm giúp tăng tốc độ đóng gói Docker Image
├── Dockerfile                                    # Kịch bản đóng gói Container ứng dụng (python:3.11-slim + tự nạp seed + HEALTHCHECK /health)
├── docker-compose.yml                            # Điều phối tự động 2 dịch vụ: mekong-l5-app (cổng 8000) + mongodb 7.0 (cổng 27017)
├── requirements.txt                              # Khóa phiên bản 9 thư viện Python (fastapi, uvicorn, pymongo, pydantic, pyjwt, pytest, httpx...)
├── pytest.ini                                    # Cấu hình trình chạy Pytest tự động quét mọi tệp *.test.py trong thư mục tests/
├── package.json & package-lock.json              # Khóa phiên bản gói công cụ Node.js hỗ trợ ở cấp thư mục gốc
├── BT1_2374802010339_HuynhNguyenBaoNgoc.pdf      # Hồ sơ báo cáo hoàn chỉnh đã nộp của Giai đoạn 1 (Bài tập 1 - Phân tích & Thiết kế)
├── BT2_2374802010339_HuynhNguyenBaoNgoc.pdf      # Hồ sơ báo cáo hoàn chỉnh của Giai đoạn 2 (Bài tập 2 - Hiện thực hóa Module cốt lõi)
│
├── docs/                                         # THƯ MỤC TÀI LIỆU KỸ THUẬT, ĐẶC TẢ, KIỂM THỬ & BẢN VẼ GỐC DRAW.IO
│   ├── test-plan.md                              # [MỚI ở BT3] Kế hoạch kiểm thử rút gọn 4 mục
│   ├── test-report.md                            # [MỚI ở BT3] Báo cáo kết quả kiểm thử thực tế đủ 8 cột
│   ├── bug-log.md                                # [MỚI ở BT3] Nhật ký theo dõi và gỡ lỗi (Bug Tracking Log)
│   ├── deployment-guide.md                       # [MỚI ở BT3] Hướng dẫn triển khai 5 mục chuẩn mực (Tiếng Anh)
│   ├── checklist-bao-mat.md                      # [MỚI ở BT3] Danh mục tự đánh giá an toàn bảo mật 7 mục kèm minh chứng
│   ├── api-docs/                                 # [Track SE - MỚI ở BT3] Đặc tả kỹ thuật toàn diện Endpoints (OpenAPI/Markdown)
│   │   ├── README.md                             # Tài liệu đặc tả API phân lớp bằng Markdown (Tiếng Anh)
│   │   └── openapi.json                          # Hợp đồng chuẩn OpenAPI 3.0 / Swagger JSON
│   ├── srs.md                                    # Bản đặc tả yêu cầu phần mềm SRS rút gọn 6 mục (7 FR, 4 NFR có ngưỡng số, 5 BR, RTM kín)
│   ├── api-contract.md                           # Hợp đồng giao tiếp RESTful API chuẩn JSON (Endpoint, Header JWT, Payload, Bảng mã lỗi)
│   ├── thaydoithietke.md                         # Nhật ký thay đổi thiết kế duy nhất tích hợp đầy đủ 3 giai đoạn BT1 - BT2 - BT3
│   ├── thietke.md                                # Đặc tả chi tiết giao diện Dark 3D Elevation từng màn hình/vai trò & bộ Prompt Google Stitch
│   ├── dieukientest.md                           # Bộ điều kiện kiểm thử, ràng buộc hệ thống và ma trận kịch bản kiểm thử toàn diện
│   ├── ai-disclosure.md                          # Bảng khai báo sử dụng công cụ AI 4 cột minh bạch cho cả 3 giai đoạn BT1, BT2, BT3
│   ├── layered clean architecture.drawio         # Bản vẽ gốc sơ đồ Kiến trúc Phân lớp 5 tầng ĐÃ HIỆN THỰC thực tế
│   ├── architecture.drawio                       # Bản vẽ gốc sơ đồ Kiến trúc hệ thống thiết kế ban đầu ở BT1
│   ├── erd.drawio                                # Bản vẽ gốc sơ đồ Mô hình dữ liệu 6 Collections MongoDB ($jsonSchema & Compound Index)
│   └── usecase.drawio                            # Bản vẽ gốc sơ đồ Use Case tổng thể Luồng 05 (3 Actors, 7 Use Cases & <<include>> UC-99)
│
├── src/                                          # MÃ NGUỒN CHÍNH THỰC THI HỆ THỐNG (5 TẦNG PHÂN LỚP SẠCH - CHẠY TRỰC TIẾP & DOCKER)
│   ├── app.py                                    # Điểm khởi chạy FastAPI, cấu hình CORS, Global Exception Handler, /health & Mount Static SPA
│   ├── errors/
│   │   └── AppError.py                           # Định nghĩa lớp cha AppError và 6 lớp ngoại lệ nghiệp vụ (EX-02..EX-05, 403, 404)
│   ├── routes/
│   │   ├── __init__.py                           # Nạp mô-đun động (importlib) xuất khẩu đối tượng router và auth_router
│   │   └── inventory.routes.py                   # Giải mã Bearer JWT (BR-04) & điều phối 19 API Endpoints (13 API Kho/Nhân sự + 6 API Auth)
│   ├── validators/
│   │   ├── __init__.py                           # Nạp mô-đun động xuất khẩu 8 hàm kiểm định dữ liệu đầu vào
│   │   └── inventory.validator.py                # Kiểm định miền giá trị số lượng, mật khẩu 4 nhóm ký tự, bắt buộc ticket_id khi OUT/RETURN
│   ├── services/
│   │   ├── __init__.py                           # Nạp mô-đun động xuất khẩu lớp InventoryService và thực thể inventory_service
│   │   └── inventory.service.py                  # Trái tim nghiệp vụ thuần Python 100% (không chứa HTTP): BR-01..BR-05 & Optimistic Locking
│   ├── repositories/
│   │   ├── __init__.py                           # Nạp mô-đun động xuất khẩu lớp InventoryRepository và thực thể inventory_repository
│   │   └── inventory.repository.py               # Thao tác CRUD nguyên tử với MongoDB kết hợp cơ chế lưu trữ kép Dual-Persistence Fallback
│   └── static/                                   # GIAO DIỆN NGƯỜI DÙNG SPA DARK 3D ELEVATION TÍCH HỢP TRỰC TIẾP TRÊN CỔNG 8000
│       ├── index.html                            # Khung cấu trúc SPA: Màn hình Auth Split-Screen, Đồng hồ OTP 10 phút & Workspace 3 vai trò
│       ├── styles.css                            # Bộ biến Design Tokens Dark 3D (.card-3d, Glassmorphism, 4 nhóm huy hiệu màu ngữ nghĩa)
│       └── app.js                                # Lớp API Client tập trung apiCall(), định tuyến 13 màn hình & xử lý đủ Loading/Empty/Error
│
├── migrations/                                   # KỊCH BẢN DỰNG CẤU TRÚC CSDL MONGODB TỪ TRẠNG THÁI TRỐNG (CHẠY LẶP BẤT BIẾN)
│   ├── 001_create_collections.js                 # Khởi tạo 6 Collections kèm bộ quy tắc kiểm duyệt $jsonSchema (quantity >= 0, version >= 1)
│   └── 002_create_indexes.js                     # Khởi tạo hệ thống Unique Index & Compound Index đảm bảo tốc độ tra cứu < 500ms (NFR-02)
│
├── seeds/                                        # DỮ LIỆU HẠT GIỐNG MẪU & KỊCH BẢN NẠP BẤT BIẾN (IDEMPOTENT SEEDING)
│   ├── 001_seed_parts_demo.json                  # Bộ dữ liệu mẫu chuẩn: 2 chi nhánh, 5 tài khoản, 40 linh kiện, 5 phiếu, 75 tồn kho, 5 giao dịch
│   └── seed.py                                   # Script nạp dữ liệu bằng cơ chế replace_one(..., upsert=True) chạy nhiều lần không nhân đôi
│
├── data/                                         # THƯ MỤC LƯU TRỮ BỀN VỮNG CỤC BỘ CHO CHẾ ĐỘ OFFLINE FALLBACK
│   ├── .gitkeep                                  # Tệp giữ cấu trúc thư mục data/ trên hệ thống quản lý phiên bản Git
│   └── users_store.json                          # Kho lưu trữ đồng bộ hồ sơ tài khoản, trạng thái ca trực và JWT xuống ổ cứng cục bộ
│
├── tests/                                        # BỘ 56 CA KIỂM THỬ TỰ ĐỘNG HÓA TOÀN DIỆN (CHẠY PASS 100% BẰNG 1 LỆNH)
│   ├── inventory.service.test.py                 # 07 Unit Tests kiểm thử cô lập lớp InventoryService trên RAM (không phụ thuộc HTTP/DB)
│   ├── inventory.routes.test.py                  # 06 Integration Tests kiểm thử hợp đồng API, phân quyền RBAC & mã lỗi chuẩn HTTP
│   ├── auth_and_user.test.py                     # 15 Tests kiểm thử Đăng ký, mật khẩu 4 nhóm, OTP 10 phút, khóa vĩnh viễn TERMINATED
│   ├── cross_role_and_ui.test.py                 # 15 E2E & UI Tests kiểm thử luồng liên thông 3 vai trò & tính toàn vẹn giao diện SPA
│   └── bt3_specification_and_constraints.test.py # 13 Tests [MỚI ở BT3] kiểm thử đặc tả & ràng buộc: RETURN, biên 2 phía (BR-01, BR-05), chặn phiếu đóng, Race Condition, bảo mật S3/S4, nạp seed C8
│
├── frontend/                                     # KHÔNG GIAN MÃ NGUỒN FRONTEND ĐỘC LẬP (NGANG HÀNG VỚI BACKEND)
│   ├── .gitignore                                # Quy tắc loại trừ thư mục node_modules/ riêng của gói Frontend
│   ├── package.json                              # Cấu hình kịch bản npm start khởi chạy máy chủ giao diện độc lập trên cổng 3000
│   ├── public/                                   # Bản đồng bộ tài nguyên giao diện SPA tĩnh (index.html, styles.css, app.js)
│   └── src/                                      # Các mô-đun kiến trúc thành phần ReactJS tách lớp:
│       ├── App.js & index.js                     #   - Khung khởi tạo ứng dụng thành phần React
│       ├── api/ (client.js, inventory.api.js)    #   - Lớp khách gọi HTTP RESTful API tách riêng biệt
│       ├── services/ (api.js)                    #   - Bộ hàm bọc dịch vụ truyền thông dữ liệu kho và nhân sự
│       ├── components/ (DataState.jsx, Header.js, Footer.js) # - Thành phần hiển thị 3 trạng thái Loading/Empty/Error
│       └── pages/                                #   - Trang giao diện cốt lõi (đã dọn dẹp các thư mục rỗng Manager, Material, Tech):
│           ├── AuthPortal.js                     #     + Cổng xác thực & phân luồng đăng nhập chung
│           └── ManagerUsers.js                   #     + Trang quản lý nhân sự thuộc quyền của Quản lý kho
│
├── backend/                                      # KHÔNG GIAN ĐÓNG GÓI DỊCH VỤ BACKEND ĐỘC LẬP (NGANG HÀNG VỚI FRONTEND)
│   ├── .env.example, app.py, pytest.ini, requirements.txt # Cấu hình khởi chạy riêng cho gói Backend độc lập
│   └── src/, migrations/, seeds/, data/, tests/  # Bản đồng bộ đầy đủ 5 tầng kiến trúc, kịch bản CSDL và bộ 56 ca kiểm thử của Backend
│
├── scripts/                                      # TẬP HỢP KỊCH BẢN TIỆN ÍCH NỘI BỘ HỖ TRỢ PHÁT TRIỂN & CHUẨN HÓA DỮ LIỆU
│   └── add_33_parts.py, apply_adjustments.py, ...# Các script Python hỗ trợ mở rộng danh mục 40 linh kiện và kiểm tra liên kết tài liệu
│
└── TL/tailieu/                                   # KHO LƯU TRỮ TÀI LIỆU HỌC PHẦN & ĐỀ BÀI GỐC (BT1, BT2, BT3, BUỔI 01 -> BUỔI 12)
    └── CDTN1_De bai Bai tap 1/2/3 ... (.pdf)     # Bộ 19 tệp PDF đề bài chính thức và tài liệu tự học làm căn cứ đối chiếu chuẩn xác
```

---

### 1.5. Bảng Đối chiếu 1–1 Giữa Chuẩn Đề bài (`BT1` · `BT2` · `BT3`) và Cấu trúc Thực tế Dự án `CDTN01`

Bảng dưới đây đối chiếu minh bạch từng hạng mục thư mục/tệp yêu cầu trong 3 đề bài (`BT1`, `BT2`, `BT3`) với các tệp thực tế hiện có trong kho mã nguồn `CDTN01`:

| STT | Hạng mục Yêu cầu theo Đề bài (`BT1` · `BT2` · `BT3`) | Giai đoạn yêu cầu | Đường dẫn Thực tế Tương ứng trong `CDTN01` | Trạng thái Đáp ứng | Thuyết minh Chi tiết Nội dung & Vai trò Đối chiếu |
| :-: | :--- | :---: | :--- | :---: | :--- |
| 1 | `README.md` (ở thư mục gốc) | `BT1` · `BT2` · `BT3` | [`README.md`](./README.md) | **Đạt 100% (Vượt mức)** | Đặt ngay tại gốc `CDTN01/` ngang hàng `backend/` & `frontend/`. Có mục Quick Start `<= 2` lệnh (chuẩn BT3) và cẩm nang tái tạo từng bước từ Database → Backend → Frontend → 43 Tests → Docker (chuẩn BT2 & BT3). |
| 2 | `.env.example` & `.gitignore` | `BT1` · `BT2` · `BT3` | [`.env.example`](./.env.example), [`.gitignore`](./.gitignore) | **Đạt 100%** | `.env.example` liệt kê đủ 7 biến môi trường với giá trị mẫu an toàn (không chứa mật khẩu thật); `.gitignore` chặn tuyệt đối `.env`, `**/.env`, `venv/`, `node_modules/`, `__pycache__/`. |
| 3 | Tệp khóa phiên bản (`requirements.txt` / `package-lock.json`) | `BT2` · `BT3` | [`requirements.txt`](./requirements.txt), [`package-lock.json`](./package-lock.json) | **Đạt 100%** | Ghim phiên bản cụ thể (`==`) cho toàn bộ 9 thư viện Python cốt lõi (`fastapi==0.104.1`, `pymongo==4.6.0`, `PyJWT==2.8.0`, `pytest==7.4.3`...) và gói phụ trợ Node.js. |
| 4 | `docs/srs.md` | `BT1` · `BT2` | [`docs/srs.md`](./docs/srs.md) | **Đạt 100%** | Bản SRS rút gọn đủ 6 mục chuẩn mực: Giới thiệu & Bảng thuật ngữ, 3 Vai trò, 7 `FR` + 7 `US` (MoSCoW), 4 `NFR` có ngưỡng số đo được, 5 `BR`, và Bảng truy vết `RTM` không có ô trống. |
| 5 | Bộ tệp gốc `.drawio` (`architecture`, `usecase`, `erd`) | `BT1` | [`docs/architecture.drawio`](./docs/architecture.drawio), [`docs/usecase.drawio`](./docs/usecase.drawio), [`docs/erd.drawio`](./docs/erd.drawio) | **Đạt 100%** | Lưu trữ đầy đủ tệp XML `.drawio` gốc (không chỉ ảnh tĩnh), có ranh giới hệ thống, phần Ngoài phạm vi (`Out of Scope`) và bảng chú thích ký hiệu (`Legend`). |
| 6 | `docs/api-contract.md` & `docs/wireframe.png` | `BT1` (`Track SE`) | [`docs/api-contract.md`](./docs/api-contract.md), [`docs/thietke.md`](./docs/thietke.md) | **Đạt 100% (Mở rộng)** | `api-contract.md` đặc tả đầy đủ chuẩn giao tiếp JSON & mã lỗi; `thietke.md` nâng cấp từ ảnh wireframe đơn lẻ thành hồ sơ đặc tả chi tiết toàn bộ 13 màn hình Dark 3D và bộ Prompt Google Stitch. |
| 7 | Sơ đồ kiến trúc ĐÃ HIỆN THỰC (`architecture-thuc-te.*`) | `BT2` | [`docs/layered clean architecture.drawio`](./docs/layered%20clean%20architecture.drawio) | **Đạt 100%** | Phản ánh chính xác 100% sơ đồ 5 tầng thực tế đã lập trình trong `src/`, ghi rõ tên từng thư mục/tệp, luồng gọi một chiều và cơ chế lưu trữ kép `Dual-Persistence`. |
| 8 | Nhật ký thay đổi thiết kế (`docs/thaydoithietke.md`) | `BT1` · `BT2` · `BT3` | [`docs/thaydoithietke.md`](./docs/thaydoithietke.md) | **Đạt 100% (Tập trung 1 tệp)** | Ghi chép đầy đủ toàn diện các quyết định điều chỉnh từ BT1 (5 hạng mục TD-01..TD-05), BT2 (13 hạng mục nâng cấp giao diện Dark 3D & 40 linh kiện) đến BT3 (8 hạng mục kiểm thử 56 tests, bảo mật S3, xóa thư mục rỗng frontend, phân quyền RBAC 1 tài khoản - 1 vai trò). |
| 9 | Bảng khai báo AI (`docs/ai-disclosure.md`) | `BT1` · `BT2` · `BT3` | [`docs/ai-disclosure.md`](./docs/ai-disclosure.md) | **Đạt 100%** | Bảng khai báo minh bạch đủ 4 cột (*Công cụ · Dùng vào việc gì · Áp dụng ở tệp/hàm nào · Đã kiểm chứng thế nào*) cho cả 3 giai đoạn BT1, BT2, BT3 kèm lời cam kết chịu trách nhiệm học thuật cá nhân. |
| 10 | Tách lớp mã nguồn `src/` (`routes/`, `validators/`, `services/`, `repositories/`) | `BT2` · `BT3` (`Track SE`) | [`src/routes/`](./src/routes), [`src/validators/`](./src/validators), [`src/services/`](./src/services), [`src/repositories/`](./src/repositories), [`src/errors/`](./src/errors), [`src/static/`](./src/static) *(đồng bộ tại `backend/` & `frontend/`)* | **Đạt 100% (Chuẩn Clean Arch)** | Tách bạch tuyệt đối trách nhiệm 5 tầng; `inventory.service.py` hoàn toàn độc lập với HTTP (tiêu chí `S2`); đồng thời tổ chức thêm `backend/` và `frontend/` ngang hàng để dễ dàng triển khai độc lập hoặc tích hợp. |
| 11 | `migrations/` & `seeds/` (Dựng CSDL trống & nạp lặp bất biến) | `BT2` · `BT3` (`Track SE`) | [`migrations/001_create_collections.js`](./migrations/001_create_collections.js), [`migrations/002_create_indexes.js`](./migrations/002_create_indexes.js), [`seeds/001_seed_parts_demo.json`](./seeds/001_seed_parts_demo.json), [`seeds/seed.py`](./seeds/seed.py) | **Đạt 100% (`C5` & `S3`)** | Dựng 6 Collections kèm `$jsonSchema` & `Compound Index` từ CSDL rỗng; `seeds/seed.py` dùng `replace_one(..., upsert=True)` đảm bảo chạy lại lần thứ 2 không lỗi, không nhân đôi dữ liệu. |
| 12 | `tests/` (Chạy PASS bằng 1 lệnh duy nhất) | `BT2` · `BT3` | [`tests/`](./tests) (5 tệp `.test.py` + [`pytest.ini`](./pytest.ini)) | **Đạt 100% (56/56 PASSED)** | Vượt xa mức tối thiểu 3 test của BT2 và 10–12 test của BT3 với **56 kịch bản kiểm thử tự động** phủ kín Luồng đúng (19), Giá trị biên (16), Ngoại lệ & Bảo mật RBAC (21). |
| 13 | `Dockerfile` & `docker-compose.yml` (Chạy bằng `<= 2` lệnh) | Cốt lõi `C1` `BT3` | [`Dockerfile`](./Dockerfile), [`docker-compose.yml`](./docker-compose.yml), [`.dockerignore`](./.dockerignore) | **Đạt 100% (Sẵn sàng BT3)** | Đóng gói hoàn chỉnh cả ứng dụng FastAPI/SPA và MongoDB 7.0 có `HEALTHCHECK` tự động và tự nạp dữ liệu mẫu khi khởi động, vượt qua trọn vẹn "Phép thử máy trắng". |
| 14 | Trọn bộ hồ sơ kỹ thuật `BT3` (`test-plan`, `test-report`, `bug-log`, `deployment-guide`, `checklist-bao-mat`, `api-docs`, `dieukientest`) | `BT3` | [`docs/test-plan.md`](./docs/test-plan.md), [`docs/test-report.md`](./docs/test-report.md), [`docs/bug-log.md`](./docs/bug-log.md), [`docs/deployment-guide.md`](./docs/deployment-guide.md), [`docs/checklist-bao-mat.md`](./docs/checklist-bao-mat.md), [`docs/api-docs/`](./docs/api-docs/), [`docs/dieukientest.md`](./docs/dieukientest.md) | **Đạt 100% (Hoàn thiện bàn giao)** | Đã biên soạn trọn bộ tài liệu theo đúng chuẩn đề bài BT3: Kế hoạch kiểm thử rút gọn 4 mục, Báo cáo kết quả 56 test cases đủ 8 cột, Nhật ký gỡ lỗi bug log, Hướng dẫn triển khai tiếng Anh 5 mục, Danh mục kiểm tra an toàn bảo mật 7 tiêu chí và đặc tả OpenAPI/Markdown. |

---

# PHẦN 2: CHUẨN BỊ MÔI TRƯỜNG & HƯỚNG DẪN TÁI TẠO CHO MÁY TRẮNG CHƯA CÀI GÌ (TỪNG BƯỚC CHI TIẾT)

Nếu bạn vừa cài lại hệ điều hành hoặc đang thao tác trên một **máy tính hoàn toàn mới (máy trắng - Bare Metal)** chưa cài đặt sẵn Python, Git hay Docker, hãy làm theo hướng dẫn cặn kẽ dưới đây để tái tạo hệ thống thành công 100%.

> [!IMPORTANT]
> **QUY TẮC BẢO MẬT & THÔNG TIN RIÊNG TƯ TRONG CẨM NANG HƯỚNG DẪN:**
> - Toàn bộ các hướng dẫn cấu hình, lệnh chạy và ví dụ tương tác đều đã được chuẩn hóa, **không để lộ bất kỳ email, mật khẩu riêng tư hay bí mật thực tế của cá nhân**.
> - Khi bạn tự đăng ký hoặc cấu hình kết nối của riêng bạn, vui lòng thay thế các chuỗi giữ chỗ mẫu dạng: `<email cá nhân của bạn>`, `<mật khẩu cá nhân của bạn>` (ví dụ: `<email cá nhân của bạn>@gmail.com`, `<mật khẩu cá nhân của bạn>`).
> - Riêng để phục vụ việc **chấm bài, nghiệm thu và kiểm thử nhanh**, hệ thống đã tạo sẵn **3 tài khoản mẫu chuyên biệt cho 3 vai trò** (được cung cấp chi tiết tại **Mục 5.2**).

---

### Bước 2.1: Cài đặt Các Phần mềm Nền tảng Bắt buộc (Dành cho Máy Trắng)

#### 1. Cài đặt Python 3.11 (Nền tảng chạy Backend API):
- Truy cập trang chủ Python chính thức: https://www.python.org/downloads/
- Tải bản cài đặt cho hệ điều hành của bạn (ví dụ trên Windows: `python-3.11.x-amd64.exe`).
- **Thao tác cực kỳ quan trọng:** Khi mở tệp cài đặt, tại màn hình đầu tiên, bạn **BẮT BUỘC TÍCH CHỌN** ô tròn:
  👉 **`[x] Add python.exe to PATH`** (nằm ở cạnh dưới cùng cửa sổ).
- Bấm **Install Now** và đợi cài đặt hoàn tất.
- *Kiểm tra:* Mở Terminal / PowerShell và gõ: `python --version` (kết quả hiện ra `Python 3.11.x` là thành công).

#### 2. Cài đặt Git (Công cụ tải và quản trị mã nguồn):
- Truy cập trang chủ Git: https://git-scm.com/downloads
- Tải và cài đặt theo các tùy chọn mặc định (bấm *Next* liên tục cho đến khi hoàn tất).
- *Kiểm tra:* Mở Terminal / PowerShell và gõ: `git --version` (hiển thị `git version 2.x.x`).
- *(Lưu ý: Nếu máy không tiện cài Git, bạn hoàn toàn có thể vào liên kết GitHub của dự án https://github.com/Johnny120905/CDTN01, bấm nút **Code** màu xanh lá và chọn **Download ZIP**, sau đó giải nén ra thư mục `CDTN01` trên máy).*

#### 3. Cài đặt Docker Desktop (Tùy chọn - Dành cho người muốn chạy tự động bằng 2 lệnh):
- Nếu máy tính của bạn hỗ trợ ảo hóa và bạn muốn chạy Docker: Tải tại https://www.docker.com/products/docker-desktop/
- Cài đặt và bật tính năng WSL 2 (trên Windows). Sau khi cài xong, mở Docker Desktop và đợi biểu tượng trạng thái ở góc dưới chuyển sang màu xanh (*Engine running*).
- *(Nếu máy yếu hoặc chưa cài Docker, bạn **KHÔNG CẦN CÀI DOCKER** vì hệ thống hỗ trợ chạy thuần bằng Python ảo ở Cách A bên dưới rất nhẹ nhàng).*

---

### Bước 2.2: Tải Mã nguồn Dự án về Thư mục Máy tính

Mở **PowerShell** (Windows) hoặc **Terminal** (macOS/Linux), di chuyển đến thư mục làm việc bạn muốn lưu dự án và chạy các lệnh:

```powershell
git clone https://github.com/Johnny120905/CDTN01.git
cd CDTN01
```

> [!NOTE]
> **Quy ước thư mục làm việc:** Trong toàn bộ tài liệu này, **mọi câu lệnh đều được thực thi tại thư mục gốc `CDTN01`** (nơi chứa các tệp `README.md`, `.env.example`, `requirements.txt`, các thư mục `docs/`, `src/`, `tests/`, `seeds/`, `migrations/`).

---

### Bước 2.3: Tạo Tệp Cấu hình Môi trường `.env` từ `.env.example`

Để bảo đảm an toàn hệ thống, mã nguồn không lưu cứng các giá trị bí mật. Bạn chỉ cần sao chép tệp cấu hình mẫu `.env.example` thành `.env`:

- **Trên Windows (PowerShell):**
  ```powershell
  Copy-Item .env.example .env
  ```
- **Trên macOS / Linux / Git Bash:**
  ```bash
  cp .env.example .env
  ```

**Bảng giải thích các biến môi trường trong tệp `.env`:**

| Tên biến trong `.env` | Giá trị mặc định định sẵn | Ý nghĩa cấu hình & Lưu ý bảo mật |
| :--- | :--- | :--- |
| `MONGO_URI` / `MONGODB_URI` | `mongodb://localhost:27017/mekong_mobile_l5` | Địa chỉ máy chủ MongoDB. Khi chạy trực tiếp không có MongoDB, hệ thống sẽ tự động chuyển sang cơ chế InMemory Fallback để bạn không bị lỗi. |
| `DB_NAME` / `DATABASE_NAME` | `mekong_mobile_l5` | Tên cơ sở dữ liệu phân hệ kho. |
| `API_PORT` | `8000` | Cổng dịch vụ Website & API (`http://localhost:8000`). |
| `JWT_SECRET_KEY` | `mekong_mobile_secret_jwt_key_2026_cdtn01` | Khóa ký số JWT bảo mật cho phiên đăng nhập 24h. |
| `DEFAULT_CENTER_ID` | `L5-WH-890` | Mã định danh Trung tâm Bảo hành Mekong Mobile Quận 1. |

*(Người dùng **không cần thay đổi** bất kỳ thông số nào trong tệp `.env` — các giá trị mặc định đã được thiết lập sẵn sàng để chạy ngay lập tức!)*

---

# PHẦN 3: HƯỚNG DẪN TÁI TẠO CƠ CẤU TẦNG DATABASE (MONGODB ATLAS · MONGODB COMPASS · MIGRATIONS · IDEMPOTENT SEED)

Hệ thống hỗ trợ **3 phương thức vận hành Cơ sở dữ liệu** hoàn toàn tương thích với nhau. Bạn có thể chọn **1 trong 3 cách** dưới đây tùy theo môi trường máy tính của mình:
- **Cách 3A:** Tự tạo một cụm cơ sở dữ liệu đám mây **MongoDB Atlas Cloud** miễn phí từ con số 0.
- **Cách 3B:** Chạy với **MongoDB cục bộ (`localhost:27017`) & Phần mềm đồ họa MongoDB Compass**.
- **Cách 3C (Tự động 100% cho máy sạch chưa cài MongoDB):** Chế độ **Lưu trữ Kép (`Dual-Persistence Fallback`)** tự động nạp dữ liệu từ `seeds/001_seed_parts_demo.json` và lưu tài khoản xuống `data/users_store.json` mà không cần cài thêm phần mềm CSDL nào.

---

### 3.1. Cách 3A: Tự tạo mới Cơ sở dữ liệu Đám mây trên MongoDB Atlas (Từng bước từ A–Z)

Nếu bạn muốn kết nối hệ thống lên đám mây thật của riêng mình:

1. **Tạo Cluster miễn phí (`M0`):**
   - Truy cập https://www.mongodb.com/cloud/atlas/register và đăng nhập.
   - Bấm **`+ Create`** → Chọn gói **`M0` (Free)** → Nhà cung cấp **`AWS`** → Khu vực **`Singapore (ap-southeast-1)`** → Đặt tên Cluster là `MekongMobileCluster` → Bấm **`Create Deployment`**.
2. **Tạo Tài khoản Quản trị Database (`Database Access`):**
   - Ở menu trái mục *SECURITY*, chọn **`Database Access`** → Bấm **`+ Add New Database User`**.
   - Chọn phương thức **`Password`**, nhập Username (ví dụ: `mekong_admin`) và Password (ví dụ: `<mật khẩu cơ sở dữ liệu của bạn>` — khuyến nghị chỉ dùng chữ và số để không phải mã hóa URL ký tự đặc biệt).
   - Ở mục *Built-in Role*, chọn **`Read and write to any database`** → Bấm **`Add User`**.
3. **Mở Tường lửa IP (`Network Access`) — *Bước bắt buộc để máy tính kết nối được*:**
   - Ở menu trái mục *SECURITY*, chọn **`Network Access`** → Bấm **`+ Add IP Address`**.
   - Bấm nút **`ALLOW ACCESS FROM ANYWHERE`** (`0.0.0.0/0`) → Bấm **`Confirm`** và đợi trạng thái chuyển sang **`Active`** (màu xanh lá).
4. **Lấy Chuỗi kết nối dán vào tệp `.env`:**
   - Vào mục **`Clusters`** → Bấm **`Connect`** → Chọn **`Drivers`** → Chọn **`Python` (3.11 or later)**.
   - Sao chép chuỗi URI, thay `<tên tài khoản database>` và `<mật khẩu database>` của bạn vào rồi cập nhật vào tệp `.env`:
     ```env
     MONGO_URI=mongodb+srv://<tên tài khoản database>:<mật khẩu database>@<ten-cluster>.mongodb.net/mekong_mobile_l5?retryWrites=true&w=majority
     MONGODB_URI=mongodb+srv://<tên tài khoản database>:<mật khẩu database>@<ten-cluster>.mongodb.net/mekong_mobile_l5?retryWrites=true&w=majority
     DB_NAME=mekong_mobile_l5
     DATABASE_NAME=mekong_mobile_l5
     ```

---

### 3.2. Cách 3B: Kết nối & Khởi tạo Cấu trúc Bảng (`Migrations`) bằng MongoDB Compass

Nếu bạn sử dụng **MongoDB Community Server** trên máy cá nhân (hoặc container MongoDB từ Docker) kèm giao diện **MongoDB Compass**:

1. Mở phần mềm **MongoDB Compass** → Bấm **`+ New Connection`**.
2. Dán chuỗi kết nối `mongodb://localhost:27017` (hoặc chuỗi `mongodb+srv://...` ở Cách 3A) vào ô **URI** → Đặt tên kết nối là `Mekong Mobile L5` → Bấm **`Save & Connect`**.
3. **(Tùy chọn) Chạy trực tiếp 2 tệp kịch bản Migration chuẩn `$jsonSchema` & `Indexes`:**
   - Nhìn xuống góc dưới bên trái cửa sổ MongoDB Compass, bấm mở thanh **`>_ MONGOSH`**.
   - Gõ 3 lệnh sau (thay đường dẫn bằng đường dẫn thư mục `CDTN01` trên máy bạn, lưu ý dùng dấu gạch chéo xuôi `/`):
     ```javascript
     use mekong_mobile_l5
     load("D:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/migrations/001_create_collections.js")
     load("D:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/migrations/002_create_indexes.js")
     ```
   - Kịch bản `001_create_collections.js` tự động kiểm tra sự tồn tại trước khi tạo 6 Collections kèm bộ quy tắc kiểm duyệt `$jsonSchema` (cưỡng chế `quantity >= 0`, `version >= 1`, `type` thuộc `['IN', 'OUT', 'RETURN']`); kịch bản `002_create_indexes.js` tạo các chỉ mục phức hợp `idx_stock_lookup` (`{center_id: 1, part_code: 1}`) và `idx_transaction_history` (`{center_id: 1, created_at: -1}`). Chạy lại lần thứ 2 tuyệt đối không báo lỗi.

---

### 3.3. Nạp Dữ liệu Hạt giống Mẫu & Kiểm chứng Tính Bất biến (`Idempotent Seed`)

Sau khi đã cài đặt môi trường ảo Python ở **Phần 4 (Bước 4.1)** bên dưới, bạn nạp toàn bộ dữ liệu mẫu khởi tạo vào MongoDB chỉ bằng **1 câu lệnh duy nhất**:

```powershell
python seeds/seed.py
```

**Phép thử bắt buộc khi nghiệm thu (Chạy lặp lại lần thứ 2 liên tiếp để kiểm chứng không lỗi, không nhân đôi bản ghi – Tiêu chí cốt lõi `C5`):**
```powershell
python seeds/seed.py
```

**Kết quả hiển thị chuẩn xác trên Terminal khi kết nối MongoDB thành công:**
```text
[*] Đang đọc tệp seed: ...\CDTN01\seeds\001_seed_parts_demo.json...
[*] Đang kết nối tới MongoDB: ... (Database: mekong_mobile_l5)...
[THÀNH CÔNG] Đã kết nối thành công tới máy chủ MongoDB!
  + Đã nạp 2 bản ghi vào 'service_center'
  + Đã nạp 5 tài khoản vào 'users'
  + Đã nạp 40 linh kiện vào 'part'
  + Đã nạp 5 phiếu bảo hành vào 'ticket'
  + Đã nạp 75 bản ghi tồn kho vào 'part_stock'
  + Đã nạp 5 nhật ký giao dịch vào 'part_transaction'
  + Đã tạo và xác thực đầy đủ hệ thống Indexes!
[HOÀN TẤT] Toàn bộ dữ liệu mẫu đã được khởi tạo sẵn sàng cho ứng dụng!
```

**Bảng đối chiếu 6 Collections chuẩn sau khi chạy `seeds/seed.py` (Bấm Refresh trên MongoDB Compass để xem):**

| STT | Tên Collection | Số bản ghi gốc | Chỉ mục định danh (Unique / Compound Index) | Vai trò dữ liệu trong phân hệ Kho linh kiện L5 |
| :-: | :--- | :---: | :--- | :--- |
| 1 | `service_center` | **2** | `{ center_id: 1 }` (Unique) | Danh mục 2 trung tâm bảo hành (`L5-WH-890` Quận 1 & `L5-WH-102` Cần Thơ) phục vụ cô lập vùng `BR-04`. |
| 2 | `users` | **8** | `{ email: 1 }` (Unique) | Hồ sơ tài khoản mẫu phủ đủ 3 vai trò (`TECH_STAFF`, `MATERIAL_STAFF`, `MANAGER`), tuân thủ nghiêm ngặt nguyên tắc 1 email chỉ gắn đúng 1 vai trò duy nhất, và đủ 4 trạng thái nhân sự (`ONLINE`, `AWAY`, `OFF_SHIFT`, `TERMINATED`). |
| 3 | `part` | **40** | `{ part_code: 1 }` (Unique) | Danh mục 40 mã linh kiện thực tế (Apple, Samsung, Xiaomi...), đơn giá VNĐ và ngưỡng cảnh báo `min_threshold` (`BR-05`). |
| 4 | `ticket` | **5** | `{ ticket_id: 1 }` (Unique) | Danh sách phiếu bảo hành hợp lệ (`TK-1092`, `TK-1093`, `TK-1095`, `TK-1098`, `TK-2026-8892`) phục vụ đối chiếu chứng từ `BR-02` / `UC-99`. |
| 5 | `part_stock` | **75** | `{ center_id: 1, part_code: 1 }` (Unique) | Tồn kho vật lý theo thời gian thực tại từng chi nhánh (`quantity >= 0` theo `BR-01`) kèm trường `version` phục vụ `Optimistic Locking`. |
| 6 | `part_transaction` | **5+** | `{ center_id: 1, created_at: -1 }` | Sổ cái kiểm toán giao dịch kho bất biến (`Insert-only` theo `BR-03`) ghi vết mọi lệnh `IN`, `OUT`, `RETURN`. |

---

# PHẦN 4: HƯỚNG DẪN TÁI TẠO CƠ CẤU TẦNG BACKEND (PYTHON FASTAPI – KIẾN TRÚC PHÂN LỚP SẠCH)

### 4.1. Khởi tạo Môi trường Ảo (`venv`) & Cài đặt Thư viện Phụ thuộc

Đứng tại thư mục gốc `CDTN01`, thực hiện tuần tự các lệnh sau để tạo môi trường Python cô lập và cài đặt toàn bộ thư viện trong `requirements.txt` (`fastapi`, `uvicorn`, `pymongo`, `pydantic`, `python-dotenv`, `pyjwt`, `pytest`, `httpx`, `python-multipart`):

- **Trên Windows (PowerShell):**
  ```powershell
  python -m venv venv
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  .\venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```
  *(Dấu hiệu thành công: Đầu dòng lệnh xuất hiện tiền tố `(venv)` và quá trình `pip install` báo `Successfully installed ...`).*

- **Trên macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

### 4.2. Giải thích Cơ cấu Liên kết 5 Tầng trong Thư mục `src/` (Để Người đọc Hiểu rõ Luồng Code)
1. **Kỹ thuật nạp mô-đun động (`__init__.py`):** Vì các tệp được đặt tên tường minh theo vai trò kiến trúc có dấu chấm ở giữa (`inventory.routes.py`, `inventory.validator.py`, `inventory.service.py`, `inventory.repository.py`), mỗi thư mục con đều có tệp `__init__.py` dùng `importlib.util.spec_from_file_location` để xuất khẩu lớp/hàm sạch sẽ qua `__all__`.
2. **Luồng xử lý một yêu cầu giao dịch thực tế (`POST /api/v1/inventory/transactions`):**
   - **Bước 1 (`src/routes/inventory.routes.py`):** Hàm `get_current_user()` giải mã `Authorization: Bearer <token>` lấy `center_id`, `email`, `role`.
   - **Bước 2 (`src/validators/inventory.validator.py`):** Hàm `validate_transaction_payload()` kiểm tra `type` thuộc `['IN', 'OUT', 'RETURN']`, `quantity` là số nguyên dương `[1..1.000.000]` (chặn `bool`), và bắt buộc `ticket_id` nếu `type` là `OUT`/`RETURN`.
   - **Bước 3 (`src/services/inventory.service.py`):** Phương thức `InventoryService.process_transaction()` (thuần Python 100%, không chứa HTTP) kiểm tra quyền vai trò → gọi `find_ticket()` xác thực phiếu chưa đóng (`UC-99`) → kiểm tra tồn kho hiện tại `current_qty >= quantity` (`BR-01`) → gọi `update_stock_optimistic(..., expected_version=current_version)` (`EX-05`) → ghi sổ cái vĩnh viễn `insert_transaction()` (`BR-03`).
   - **Bước 4 (`src/app.py` & `src/errors/AppError.py`):** Nếu bất kỳ quy tắc nào bị vi phạm, ngoại lệ kế thừa từ `AppError` được `@app.exception_handler(AppError)` bắt toàn cục và trả về JSON Tiếng Việt thống nhất `{"status": "error", "error_code": "ERR_...", "message": "..."}` (tỷ lệ lộ lỗi thô `500 Internal Server Error` bằng `0%`).

### 4.3. Khởi chạy Máy chủ Backend API & Website SPA Tích hợp

Tại cửa sổ Terminal đang kích hoạt `(venv)` ở thư mục gốc `CDTN01`, nạp dữ liệu hạt giống và bật máy chủ bằng 2 lệnh:

```powershell
python seeds/seed.py
python src/app.py
```

**Kết quả hiển thị khi máy chủ khởi động thành công tại cổng `8000`:**
```text
========================================================
  SMART CRM - MEKONG MOBILE (INVENTORY FLOW 05)
  Server running at: http://localhost:8000
  Swagger Docs at:   http://localhost:8000/docs
========================================================
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### 4.4. Kiểm chứng Nhanh Tầng Backend Đã Chạy Đúng (4 Phép thử Thực tế)

Giữ nguyên cửa sổ máy chủ đang chạy, mở **một cửa sổ PowerShell / Terminal thứ hai** và gõ thử 4 lệnh `curl.exe` sau để thấy rõ phản ứng chuẩn xác của từng tầng kiến trúc:

1. **Kiểm tra sức khỏe dịch vụ (`GET /health` → `HTTP 200 OK`):**
   ```powershell
   curl.exe -s http://localhost:8000/health
   ```
   *Kết quả kỳ vọng:* `{"status":"online","service":"Smart CRM - Inventory Subsystem (L5)","timestamp":"2026-10-25T21:40:00Z"}`

2. **Kiểm tra API 1 – Tra cứu tồn kho Real-time & Cờ cảnh báo (`GET /api/v1/inventory/stock/SCR-IP14-01` → `HTTP 200 OK`):**
   ```powershell
   curl.exe -s http://localhost:8000/api/v1/inventory/stock/SCR-IP14-01
   ```
   *Kết quả kỳ vọng:* Trả về JSON `"status": "success"` kèm `part_code: "SCR-IP14-01"`, số lượng `quantity`, `min_threshold: 15` và `status_flag`.

3. **Kiểm tra Chốt chặn Tầng 3 Validator – Xuất kho cố tình bỏ trống `ticket_id` (`BR-02` / `EX-03` → `HTTP 422 ERR_INVALID_TICKET`):**
   ```powershell
   curl.exe -s -X POST "http://localhost:8000/api/v1/inventory/transactions" -H "Content-Type: application/json" -d "{\"part_code\":\"SCR-IP14-01\",\"type\":\"OUT\",\"quantity\":1}"
   ```
   *Kết quả kỳ vọng:* `{"status":"error","error_code":"ERR_INVALID_TICKET","message":"Mã phiếu bảo hành (ticket_id) là bắt buộc đối với giao dịch xuất kho hoặc hoàn trả."}`

4. **Kiểm tra Chốt chặn Tầng 4 Service – Xuất kho `99999` cái vượt quá tồn kho thực tế (`BR-01` / `EX-04` → `HTTP 400 ERR_NEGATIVE_STOCK`):**
   ```powershell
   curl.exe -s -X POST "http://localhost:8000/api/v1/inventory/transactions" -H "Content-Type: application/json" -d "{\"part_code\":\"SCR-IP14-01\",\"type\":\"OUT\",\"quantity\":99999,\"ticket_id\":\"TK-1092\"}"
   ```
   *Kết quả kỳ vọng:* `{"status":"error","error_code":"ERR_NEGATIVE_STOCK","message":"Số lượng xuất (99999) vượt quá tồn kho thực tế (...). Giao dịch bị từ chối."}`

5. **Kiểm tra Tài liệu Hợp đồng API Tương tác (Swagger UI):**
   - Mở trình duyệt truy cập: **http://localhost:8000/docs** để thử nghiệm trực tiếp toàn bộ 19 RESTful API Endpoints trên giao diện đồ họa OpenAPI.

---

# PHẦN 5: HƯỚNG DẪN TÁI TẠO CƠ CẤU TẦNG FRONTEND (WEBSITE SPA DARK 3D ELEVATION & KỊCH BẢN NGHIỆM THU 3 VAI TRÒ)

### 5.1. Hai Phương thức Khởi chạy Giao diện Frontend

- **Phương thức 1 – Chạy Tích hợp Trực tiếp qua Cổng `8000` (Khuyến nghị – Nhanh nhất, không cần cài Node.js):**
  Ngay khi lệnh `python src/app.py` ở Phần 4 đang chạy, FastAPI đã tự động phục vụ toàn bộ bộ giao diện SPA Dark 3D (`src/static/index.html`, `src/static/styles.css`, `src/static/app.js`).
  👉 Mở trình duyệt Web và truy cập ngay: **http://localhost:8000/**

- **Phương thức 2 – Chạy Tách biệt Thư mục `frontend/` trên Cổng `3000` (Tùy chọn khi có cài Node.js):**
  Thư mục `frontend/` lưu trữ bản đồng bộ giao diện tĩnh tại `frontend/public/` cùng các mô-đun kiến trúc ReactJS tách lớp (`frontend/src/api/client.js`, `frontend/src/api/inventory.api.js`, `frontend/src/components/DataState.jsx`, `frontend/src/pages/AuthPortal.js`, `frontend/src/pages/ManagerUsers.js`). *(Lưu ý: Các thư mục con rỗng không chứa file trước đây như `Manager/`, `Material/`, `Tech/` và `frontend/public/images/` đã được dọn dẹp loại bỏ triệt để; toàn bộ 3 vai trò được điều phối tập trung và thống nhất qua SPA).* Nếu muốn bật máy chủ giao diện riêng tại cổng `3000`:
  ```powershell
  cd frontend
  npm start
  ```
  Sau đó mở trình duyệt tại **http://localhost:3000/** (giao diện sẽ tự động gọi sang Backend API ở cổng `8000`).

---

### 5.2. Bảng Tài khoản Mẫu Dựng sẵn trong Seed để Đăng nhập Kiểm chứng Ngay

> [!IMPORTANT]
> **QUY TẮC PHÂN QUYỀN BẤT BIẾN TRÊN HỆ THỐNG (STRICT RBAC):**
> Trong toàn bộ hệ thống Smart CRM – Mekong Mobile, **mỗi tài khoản email chỉ được đăng nhập đúng 1 vai trò (`role`) duy nhất**. Hệ thống phân định rạch ròi trách nhiệm nghiệp vụ và thẩm quyền dữ liệu, tuyệt đối không cho phép 1 tài khoản đăng nhập kiêm nhiệm nhiều vai trò hoặc đổi quyền chéo.

Tại màn hình Cổng xác thực (**http://localhost:8000/**), bạn có thể bấm nút con mắt để xem mật khẩu, tự đăng ký tài khoản mới (mật khẩu 8–128 ký tự đủ 4 nhóm: hoa, thường, số, ký hiệu), thử tính năng **Quên mật khẩu nhận OTP 6 số đếm ngược 10:00 → 00:00**, hoặc đăng nhập ngay bằng **3 tài khoản chuyên biệt đại diện cho 3 vai trò** được thiết lập sẵn:

| STT | Vai trò Nghiệp vụ (Role) | Email Đăng nhập | Mật khẩu Hệ thống | Trạng thái | Nhiệm vụ & Thẩm quyền Nghiệp vụ Kiểm chứng |
| :-: | :--- | :--- | :--- | :---: | :--- |
| **1** | **Nhân viên vật tư**<br>(`MATERIAL_STAFF`) | **`huynhnguyenbaongoc2k5@gmail.com`**<br>*(hoặc `vattu.test@gmail.com`)* | **`Huynh120905!`**<br>*(hoặc `Mekong@2026`)* | `ONLINE` | Tiếp nhận và Nhập kho vật tư mới (`IN`, không cần mã phiếu bảo hành) trên bố cục 2 cột song song; quan sát đối chiếu số dư tồn kho 40 mã hàng hóa. |
| **2** | **Nhân viên kỹ thuật**<br>(`TECH_STAFF`) | **`vuthelong1009@gmail.com`**<br>*(hoặc `kythuat.test@gmail.com`)* | **`Vu100905!`**<br>*(hoặc `Mekong@2026`)* | `ONLINE` | Tra cứu tồn kho thông minh `<= 3 clicks`; lập yêu cầu Xuất kho thay thế (`OUT`) & Hoàn trả (`RETURN`) bắt buộc gắn mã phiếu bảo hành hợp lệ (`TK-1092`); kiểm chứng chốt chặn âm kho `BR-01`. |
| **3** | **Quản lý kho**<br>(`MANAGER`) | **`lethithuyngan985@gmail.com`**<br>*(hoặc `quanlykho.test@gmail.com`)* | **`Le090805!`**<br>*(hoặc `Mekong@2026`)* | `ONLINE` | Giám sát Dashboard KPI thời gian thực; nhận bảng cờ cảnh báo đỏ thiếu hụt tồn kho; điều chỉnh ngưỡng an toàn `min_threshold` (`FR-06`); xuất báo cáo CSV; giám sát Sổ cái bất biến và quản lý hồ sơ nhân sự. |
| **4** | **Nhân sự đã thôi việc**<br>*(Kiểm thử an toàn)* | `anhpham712002@gmail.com` | `Anhpham712002@` | `TERMINATED` | Kiểm chứng chốt chặn thu hồi quyền vĩnh viễn: Cổng đăng nhập lập tức từ chối và báo lỗi đỏ **`HTTP 403 ERR_ACCOUNT_TERMINATED`**. |

---

### 5.3. Kịch bản Bấm Chuột Nghiệm thu Từng Vai trò & Kiểm chứng Đủ 3 Trạng thái Giao diện (`Loading` · `Empty` · `Error`)

Để kiểm chứng hệ thống hoạt động khép kín đúng 100% thiết kế và đạt trọn vẹn **Tiêu chí S4** của chuyên ngành Công nghệ phần mềm, người đọc có thể thực hiện theo kịch bản 4 bước sau:

1. **Nghiệm thu Vai trò 1 – Nhân viên kỹ thuật (`vuthelong1009@gmail.com` / `Vu100905!`):**
   - Đăng nhập vào hệ thống, tự động được điều hướng đến giao diện **Tra cứu & Giao dịch**.
   - Gõ `SCR-IP14` vào ô tìm kiếm thông minh → Nhấn phím **`Enter`** để chọn ngay `SCR-IP14-01 - Màn hình OLED iPhone 14 Pro Max` (thẻ thông tin tồn kho thực tế và huy hiệu màu hiện ra tức thì).
   - **Thử trạng thái Lỗi (`Error State`):** Nhập số lượng `999` (lớn hơn tồn kho hiện tại) → Khung cảnh báo đỏ hiện ngay lập tức và nút *Xác nhận Giao dịch* tự động bị khóa để chặn âm kho (`BR-01`). Bấm **Đặt lại biểu mẫu** để xóa sạch về ban đầu.
   - **Thử luồng đúng (`<= 3 clicks`):** Chọn lại `SCR-IP14-01` → Nhập mã phiếu bảo hành hợp lệ `TK-1092` và số lượng `1` → Bấm **Xác nhận Giao dịch** → Thông báo xanh hiện lên và số lượng tồn kho giảm ngay `-1` cái.

2. **Nghiệm thu Vai trò 2 – Nhân viên vật tư (`huynhnguyenbaongoc2k5@gmail.com` / `Huynh120905!`):**
   - Bấm **Đăng xuất tài khoản** ở góc trên bên phải (trạng thái tài khoản Kỹ thuật tự động chuyển về `OFF_SHIFT`), sau đó đăng nhập bằng `huynhnguyenbaongoc2k5@gmail.com`.
   - Vào mục **Nhập kho linh kiện mới**: Quan sát bố cục 2 cột song song. Bấm nút **Chọn** ở dòng `SCR-IP14-01` bên bảng thống kê cột phải → Nhập số lượng nhập `10` ở cột trái → Quan sát thẻ đối chiếu *Tồn trước nhập / Ngưỡng an toàn / Dự kiến sau nhập* → Bấm **Ghi nhận Nhập kho** → Số dư kho cộng dồn ngay `+10` cái mà không cần mã phiếu bảo hành.

3. **Nghiệm thu Vai trò 3 – Quản lý kho (`lethithuyngan985@gmail.com` / `Le090805!`):**
   - Đăng nhập tài khoản Quản lý kho. Trên **Dashboard Tổng quan**: Xem 4 thẻ KPI thời gian thực và bảng **Cảnh báo linh kiện dưới ngưỡng an toàn** (hiển thị chính xác số tồn thực tế, ngưỡng tối thiểu và số lượng thiếu hụt).
   - Bấm nút **Xem Báo cáo Chi tiết** (hoặc nút *Sửa cấu hình ngưỡng*): Đổi số ngưỡng an toàn của một mã linh kiện bất kỳ rồi bấm **Lưu** → Huy hiệu trạng thái và bộ đếm cảnh báo tự động cập nhật tức thì (`FR-06`, `BR-05`). Bấm **Xuất dữ liệu** để tải tệp báo cáo `.csv` chuẩn tiếng Việt UTF-8 BOM.
   - Mở mục **Nhật ký Giao dịch Kho**: Kiểm tra các giao dịch `Xuất kho thay thế` và `Nhập kho vật tư` vừa tạo ở bước trên đều được ghi vết đầy đủ và tuyệt đối không có nút Sửa/Xóa (`BR-03`).

4. **Cách kiểm chứng trực quan đủ 3 Trạng thái Giao diện (`Loading` · `Empty` · `Error`):**
   - **Trạng thái Đang tải (`Loading State`):** Khi chuyển đổi giữa các tab trên menu trái, vùng nội dung hiển thị vòng xoay `progress_activity` kèm thông điệp *"Đang tải và đồng bộ dữ liệu kho chi nhánh..."*.
   - **Trạng thái Rỗng (`Empty State` – Phân biệt rõ 2 ngữ cảnh):**
     - *Ngữ cảnh 1 (Bộ lọc không khớp kết quả):* Gõ từ khóa không tồn tại `XYZ-9999` vào ô lọc linh kiện hoặc ô tìm kiếm nhân sự → Hệ thống báo rõ không tìm thấy bản ghi khớp bộ lọc kèm nút đặt lại bộ lọc.
     - *Ngữ cảnh 2 (Kho vận hành an toàn):* Khi toàn bộ linh kiện đều có tồn kho `> min_threshold`, bảng cảnh báo trên Dashboard Quản lý hiển thị biểu tượng xanh ngọc `check_circle`: *"Kho đạt ngưỡng an toàn lý tưởng. Không có linh kiện nào bị thiếu hụt."*.
   - **Trạng thái Lỗi kết nối (`Error State` có nút Thử lại):** Tạm dừng cửa sổ chạy `python src/app.py` (`Ctrl + C`) rồi chuyển tab trên trình duyệt → Màn hình tuyệt đối không bị trắng trang mà hiển thị khung báo lỗi kết nối Tiếng Việt rõ ràng kèm nút **Thử lại** (`renderCurrentView()`). Bật lại `python src/app.py` và bấm **Thử lại**, giao diện khôi phục ngay lập tức.

---

# PHẦN 6: HƯỚNG DẪN CHẠY BỘ KIỂM THỬ TỰ ĐỘNG (56/56 TESTS PASSED BẰNG 1 LỆNH)

Bộ kiểm thử tự động của dự án gồm **56 kịch bản kiểm thử tự động (`56 Automated Test Cases`)** chia đều trên 5 tệp kiểm thử trong thư mục `tests/`. Toàn bộ các bài kiểm thử đều **tự khởi tạo và tự dọn dẹp dữ liệu thử nghiệm riêng (`setUp` / `tearDownClass`)** ngay trong bộ nhớ, độc lập và chạy lặp bất biến.

### 6.1. Chạy Toàn bộ 56 Ca Kiểm thử Bằng Đúng 1 Câu Lệnh Duy nhất

Đứng tại thư mục gốc `CDTN01` (đã kích hoạt `venv`), chạy lệnh:

```powershell
python -m pytest tests/ -v
```

*(Hoặc gõ ngắn gọn: `pytest tests/ -v`).*

### 6.2. Chạy Kiểm thử Riêng Từng Tệp (Khi Muốn Kiểm tra Chi tiết Từng Phân lớp)

```powershell
# 1. Kiểm thử đơn vị (Unit Test) lớp Service thuần Python trên RAM (07 tests - không cần HTTP/DB):
python -m pytest tests/inventory.service.test.py -v

# 2. Kiểm thử tích hợp Hợp đồng RESTful API & Mã lỗi HTTP (06 tests):
python -m pytest tests/inventory.routes.test.py -v

# 3. Kiểm thử Xác thực JWT, Mật khẩu 4 nhóm, OTP 10 phút & Khóa tài khoản TERMINATED (15 tests):
python -m pytest tests/auth_and_user.test.py -v

# 4. Kiểm thử Luồng liên thông 3 Vai trò (E2E) & Toàn vẹn Cấu trúc Giao diện Dark 3D (15 tests):
python -m pytest tests/cross_role_and_ui.test.py -v

# 5. [MỚI ở BT3] Kiểm thử Đặc tả Hoàn trả, Giá trị biên 2 phía, Khóa lạc quan Race Condition, Bảo mật S3/S4, Nạp seed C8 (13 tests):
python -m pytest tests/bt3_specification_and_constraints.test.py -v
```

### 6.3. Bảng Phân bổ 56 Kịch bản Kiểm thử Theo Các Nhóm Bắt buộc

| Nhóm Kiểm thử | Số ca | Các kịch bản kiểm chứng tiêu biểu trong `tests/` | Kết quả Thực tế |
| :--- | :---: | :--- | :---: |
| **1. Luồng đúng (Happy Path)** | **19** | Tra cứu tồn kho `NORMAL`; Xuất kho hợp lệ kèm `ticket_id` trừ đúng số dư & ghi sổ cái; Nhập kho `IN` không cần `ticket_id`; Quản lý cập nhật `min_threshold`; Hoàn trả linh kiện `RETURN` cộng bù tồn kho; Đăng ký, Đăng nhập JWT, Quên mật khẩu & Reset bằng OTP 6 số; Liên thông Vật tư nhập → Kỹ thuật xuất → Quản lý nhận cảnh báo; Nạp seed lặp bất biến `C8`. | **19/19 PASSED** |
| **2. Giá trị biên 2 phía (Boundary Values)** | **16** | Tồn kho đúng bằng số lượng xuất (hết hàng về 0) vs vượt quá tồn 1 đơn vị (`BR-01`); Tồn kho bằng đúng `min_threshold` (bật cờ `WARNING`) vs cao hơn ngưỡng đúng 1 cái (cờ `NORMAL`) (`BR-05`); Biên số lượng nhập/xuất (`0`, `1`, `1.000.000`, `1.000.001`); Biên ngưỡng cảnh báo (`-1`, `0`, `100.000`, `100.001`); Biên mật khẩu thiếu từng nhóm và độ dài chuỗi tối đa (`full_name` 50, `email` 100, `part_code` 30). | **16/16 PASSED** |
| **3. Ngoại lệ & An toàn Bảo mật (Exceptions & Security)** | **21** | Xuất vượt tồn kho thực tế → `400 ERR_NEGATIVE_STOCK`; Xuất kho bỏ trống `ticket_id` → `422 ERR_INVALID_TICKET`; Xuất kho với phiếu bảo hành đã đóng/hủy hoặc không tồn tại → `422 ERR_TICKET_CLOSED / ERR_TICKET_NOT_FOUND`; Phát hiện xung đột đồng thời *Optimistic Locking* → `409 ERR_OPTIMISTIC_LOCK_FAILED`; Bảo mật `S3` (mật khẩu không bao giờ lưu plaintext); Bảo mật `S4` (phản hồi lỗi không lộ stack trace thô); Đăng ký trùng Email; Đăng nhập tài khoản thôi việc `TERMINATED` → `403 ERR_ACCOUNT_TERMINATED`. | **21/21 PASSED** |
| **TỔNG CỘNG** | **56** | **Toàn bộ 5 tệp kiểm thử chạy tự động đồng loạt bằng 1 lệnh duy nhất** | **56/56 PASSED (100%)** |

---

# PHẦN 7: HƯỚNG DẪN ĐÓNG GÓI DOCKER (`<= 2` LỆNH), PHÉP THỬ MÁY TRẮNG & ĐẨY GITHUB TAG `v0.2` & `v1.0`

Toàn bộ ứng dụng đã được đóng gói tự động hóa hoàn chỉnh qua [`Dockerfile`](./Dockerfile) và [`docker-compose.yml`](./docker-compose.yml):
- **Container 1 (`mekong_crm_l5_app`):** Đóng gói trên nền `python:3.11-slim`, tự động chạy `python seeds/seed.py` để nạp dữ liệu mẫu rồi khởi chạy máy chủ FastAPI + Giao diện SPA Dark 3D tại cổng `8000`, tích hợp `HEALTHCHECK` tự động mỗi 30 giây tại `/health`.
- **Container 2 (`mekong_crm_l5_mongodb`):** Khởi chạy hệ quản trị cơ sở dữ liệu `mongo:7.0` tại cổng `27017` kèm ổ đĩa lưu trữ bền vững `mongo_l5_data` và `HEALTHCHECK` bằng `mongosh`.

### 7.1. Khởi chạy Toàn bộ Hệ thống (App + MongoDB 7.0) Bằng Đúng 2 Lệnh

Mở cửa sổ Terminal / PowerShell tại thư mục gốc `CDTN01` (đảm bảo Docker Desktop đang bật) và chạy đúng **2 lệnh**:

```powershell
# Lệnh 1: Tạo tệp cấu hình môi trường .env từ tệp mẫu (nếu chưa tạo ở Phần 2)
Copy-Item .env.example .env -ErrorAction SilentlyContinue

# Lệnh 2: Dựng Docker Image và khởi chạy ngầm đồng thời cả Web/API (8000) + MongoDB 7.0 (27017)
docker compose up -d --build
```
*(Trên macOS/Linux thay Lệnh 1 bằng: `cp -n .env.example .env`).*

Ngay sau khi dòng `Container mekong_crm_l5_app Started` xuất hiện, mở trình duyệt truy cập **http://localhost:8000/** để sử dụng toàn bộ Website!

### 7.2. Quy trình 5 Bước "Phép thử Máy trắng" Bằng Docker (Chuẩn Nghiệm thu Chấm Bài)

Người đọc hoặc giảng viên có thể kiểm chứng trọn vẹn tính tái lập, tính bất biến dữ liệu (`C5`) và bộ 56 kiểm thử (`C4`) ngay bên trong môi trường Container cô lập:

```powershell
# Bước 1: Xóa sạch toàn bộ container và dữ liệu volume cũ để mô phỏng máy trắng 100%
docker compose down -v

# Bước 2: Dựng mới và bật toàn bộ hệ thống từ trạng thái trống
docker compose up -d --build

# Bước 3: Kiểm tra trạng thái 2 container (cả 2 đều hiển thị Up / healthy)
docker compose ps

# Bước 4: Kiểm chứng nạp dữ liệu mẫu lần thứ 2 liên tiếp không lỗi, không nhân đôi bản ghi (Tiêu chí C5)
docker compose exec mekong-l5-app python seeds/seed.py

# Bước 5: Thực thi toàn bộ 56 ca kiểm thử tự động ngay bên trong container (Kết quả: 56 passed)
docker compose exec mekong-l5-app pytest tests/ -v
```

**Các lệnh quản trị Docker tiện ích khác:**
- Xem nhật ký hoạt động thời gian thực: `docker compose logs -f mekong-l5-app`
- Tắt hệ thống container khi ngừng làm việc: `docker compose down`

### 7.3. Quy trình Đẩy Mã nguồn lên GitHub & Đóng nhãn Phiên bản Phát hành (`Tag v0.2` & `Tag v1.0`)

Bộ lệnh chuẩn bằng tiếng Việt để lưu toàn bộ thay đổi, tạo commit rõ ràng, gắn nhãn phiên bản và đẩy lên kho GitHub công khai:

```powershell
# Bước 1: Kiểm tra trạng thái tệp đã chỉnh sửa (đảm bảo không lộ tệp .env thật)
git status

# Bước 2: Đưa toàn bộ tệp mã nguồn và tài liệu cập nhật vào vùng Staging & tạo Commit chuẩn
git add .
git commit -m "docs: hoan thien README goc tai tao tu may trang, dong bo thaydoithietke 3 giai doan va bo sung tai khoan 3 role"

# Bước 3: Đẩy nhánh chính (main) lên kho GitHub từ xa
git push origin main

# Bước 4: Tạo mới nhãn phát hành v0.2 (hoặc v1.0 khi nghiệm thu đóng gói Bài tập 3)
git tag -f -a v0.2 -m "Phat hanh Bai tap 2 - Hien thuc hoa module cot loi Luong 05 Kho linh kien (v0.2)"
git push -f origin v0.2

# Khi ban giao hoan tat Bai tap 3:
git tag -f -a v1.0 -m "Phat hanh Bai tap 3 - Kiem thu va Dong goi Prototype hoan chinh Luong 05 (v1.0)"
git push -f origin v1.0
```
👉 Kiểm tra trực tiếp trên cửa sổ trình duyệt tại: https://github.com/Johnny120905/CDTN01/releases

---

# PHẦN 8: CẨM NANG XỬ LÝ SỰ CỐ THƯỜNG GẶP (TROUBLESHOOTING) & LIÊM CHÍNH HỌC THUẬT

### 8.1. Bảng Khắc phục Tức thì Các Lỗi Môi trường Phổ biến

| Tình huống / Thông báo lỗi gặp phải | Nguyên nhân gốc rễ | Lệnh / Thao tác khắc phục trong 10 giây |
| :--- | :--- | :--- |
| `Activate.ps1 cannot be loaded because running scripts is disabled on this system` | Chính sách bảo mật mặc định của Windows PowerShell chặn chạy script kích hoạt `venv`. | Gõ lệnh `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` rồi chạy lại `.\venv\Scripts\Activate.ps1`. |
| `ModuleNotFoundError: No module named 'fastapi'` (hoặc `pymongo`, `jwt`) | Chưa kích hoạt môi trường ảo `(venv)` hoặc chưa cài gói thư viện trong `requirements.txt`. | Kích hoạt `.\venv\Scripts\Activate.ps1` (hoặc `source venv/bin/activate`) rồi chạy `pip install -r requirements.txt`. |
| `ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)` | Cổng `8000` đang bị chiếm bởi một cửa sổ máy chủ Python hoặc Docker container bật trước đó. | Tắt cửa sổ Terminal cũ / chạy `docker compose down`, hoặc mở tệp `.env` đổi `API_PORT=8001` rồi chạy lại `python src/app.py`. |
| Máy tính không có kết nối Internet tới Atlas và chưa cài MongoDB cục bộ | Không có dịch vụ MongoDB lắng nghe ở cổng `27017` hoặc mạng ngoại tuyến. | **Hệ thống vẫn chạy bình thường 100%!** `InventoryRepository` tự động chuyển sang chế độ **Dual-Persistence Fallback** (đọc 40 linh kiện từ `seeds/001_seed_parts_demo.json` và lưu tài khoản vào `data/users_store.json`). |
| Lỗi `error during connect: ... dockerDesktopLinuxEngine` khi gõ `docker compose` | Chưa khởi động ứng dụng **Docker Desktop** trên máy tính. | Mở ứng dụng **Docker Desktop**, chờ biểu tượng góc dưới màn hình báo *Engine running* rồi chạy lại `docker compose up -d --build`. |

---

### 8.2. Danh mục Hồ sơ Kỹ thuật Liên kết Khép kín trong Thư mục `docs/`
- [`docs/srs.md`](./docs/srs.md) — Bản đặc tả yêu cầu phần mềm rút gọn (SRS 6 mục chuẩn hóa từ Bài tập 1).
- [`docs/api-contract.md`](./docs/api-contract.md) — Đặc tả hợp đồng giao tiếp RESTful API chuẩn JSON.
- [`docs/layered clean architecture.drawio`](./docs/layered%20clean%20architecture.drawio) — Sơ đồ Kiến trúc Phân lớp Sạch 5 tầng thực tế đã hiện thực.
- [`docs/erd.drawio`](./docs/erd.drawio) & [`docs/usecase.drawio`](./docs/usecase.drawio) & [`docs/architecture.drawio`](./docs/architecture.drawio) — Bộ sơ đồ Mô hình dữ liệu MongoDB, Use Case và Kiến trúc gốc.
- [`docs/thaydoithietke.md`](./docs/thaydoithietke.md) — Nhật ký thay đổi thiết kế duy nhất tập trung trọn vẹn 3 giai đoạn BT1, BT2 và BT3.
- [`docs/thietke.md`](./docs/thietke.md) — Đặc tả chi tiết giao diện Dark 3D Elevation & Bộ Prompt Google Stitch tái tạo giao diện cho 3 vai trò.
- [`docs/dieukientest.md`](./docs/dieukientest.md) — Bộ điều kiện kiểm thử, ràng buộc hệ thống và ma trận kịch bản kiểm thử toàn diện.
- [`docs/test-plan.md`](./docs/test-plan.md) — Kế hoạch kiểm thử rút gọn 4 mục theo đề bài BT3.
- [`docs/test-report.md`](./docs/test-report.md) — Báo cáo kết quả kiểm thử thực tế 56 test cases đủ 8 cột.
- [`docs/bug-log.md`](./docs/bug-log.md) — Nhật ký theo dõi và gỡ lỗi kèm link commit.
- [`docs/deployment-guide.md`](./docs/deployment-guide.md) — Hướng dẫn triển khai kỹ thuật 5 mục bằng tiếng Anh.
- [`docs/checklist-bao-mat.md`](./docs/checklist-bao-mat.md) — Danh mục tự đánh giá an toàn bảo mật 7 tiêu chuẩn.
- [`docs/api-docs/`](./docs/api-docs/) — Tài liệu kỹ thuật API Endpoints chuẩn OpenAPI và Markdown tiếng Anh.
- [`docs/ai-disclosure.md`](./docs/ai-disclosure.md) — Bảng khai báo sử dụng công cụ AI 4 cột minh bạch và phương pháp tự kiểm chứng cho cả 3 bài tập.

---

### 8.3. Cam kết Liêm chính Học thuật
> *"Tôi tên là **Huỳnh Nguyễn Bảo Ngọc** (MSSV: `2374802010339`), sinh viên chuyên ngành Công nghệ phần mềm (`SE`) – Khoa Công nghệ Thông tin, Trường Đại học Văn Lang. Tôi xác nhận đã đọc, hiểu rõ từng dòng mã nguồn, từng quy tắc nghiệp vụ, thuật toán Khóa lạc quan (Optimistic Locking), cấu trúc cơ sở dữ liệu NoSQL, bộ 56 ca kiểm thử tự động cũng như quy trình đóng gói Docker trong dự án này, và hoàn toàn chịu trách nhiệm học thuật về toàn bộ sản phẩm bàn giao."*

import os
import re

tree_text = """CDTN01/                                           # THƯ MỤC GỐC CỦA KHO MÃ NGUỒN DỰ ÁN (REPOSITORY ROOT)
├── README.md                                     # [TỆP TRUNG TÂM NÀY] Cẩm nang tái tạo cơ cấu toàn diện & đối chiếu BT1-BT2-BT3
├── .env                                          # Tệp cấu hình biến môi trường cục bộ (được .gitignore bảo vệ, không đẩy lên Git)
├── .env.example                                  # Tệp mẫu khai báo đủ mọi biến môi trường với giá trị an toàn (MONGO_URI, DB_NAME, JWT_SECRET_KEY...)
├── .gitignore                                    # Chặn đẩy .env thật, venv/, __pycache__/, .pytest_cache/, node_modules/, *.bak
├── .dockerignore                                 # Loại trừ môi trường ảo cục bộ, cache và tệp tạm giúp tăng tốc độ build Docker Image
├── Dockerfile                                    # Kịch bản đóng gói Container ứng dụng (python:3.11-slim + tự nạp seed + HEALTHCHECK /health)
├── docker-compose.yml                            # Điều phối tự động 2 dịch vụ: mekong-l5-app (cổng 8000) + mongodb 7.0 (cổng 27017)
├── requirements.txt                              # Khóa chặt phiên bản phụ thuộc Python bằng dấu == (fastapi, uvicorn, pymongo, pytest...)
├── pytest.ini                                    # Cấu hình trình chạy Pytest tự động quét mọi tệp *.test.py trong tests/
├── package.json & package-lock.json              # Khóa phiên bản gói công cụ Node.js hỗ trợ tại thư mục gốc
├── render.yaml                                   # Kịch bản cấu hình triển khai tự động (Blueprint Infrastructure) trên đám mây Render.com
├── BT1_2374802010339_HuynhNguyenBaoNgoc (Bảng cũ).pdf # Hồ sơ báo cáo hoàn chỉnh Giai đoạn 1 (Bài tập 1 - Phân tích & Thiết kế)
├── BT2_2374802010339_HuynhNguyenBaoNgoc.pdf      # Hồ sơ báo cáo hoàn chỉnh Giai đoạn 2 (Bài tập 2 - Hiện thực hóa Module cốt lõi)
├── BT3_2374802010339_HuynhNguyenBaoNgoc.pdf      # Hồ sơ báo cáo hoàn chỉnh Giai đoạn 3 (Bài tập 3 - Kiểm thử & Đóng gói Prototype)
├── test_bug1.bat .. test_bug5.bat                # Bộ 5 tập lệnh batch Windows kiểm thử hồi quy độc lập cho 5 lỗi kỹ thuật BUG-01..05
├── venv_bug1.bat .. venv_bug5.bat                # Bộ 5 tập lệnh batch Windows kích hoạt môi trường ảo kiểm chứng chuyên sâu từng bug
│
├── docs/                                         # THƯ MỤC TÀI LIỆU KỸ THUẬT, ĐẶC TẢ, KIỂM THỬ & BẢN VẼ GỐC DRAW.IO
│   ├── test-plan.md                              # [MỚI ở BT3] Kế hoạch kiểm thử rút gọn 4 mục (Scope In/Out, Test Pyramid 67 tests, Câu hỏi vấn đáp)
│   ├── test-report.md                            # [MỚI ở BT3] Báo cáo kết quả kiểm thử thực tế 13 test cases đủ 8 cột (100% PASSED)
│   ├── bug-log.md                                # [MỚI ở BT3] Nhật ký theo dõi và gỡ lỗi (5 lỗi chuẩn 7 dòng kèm RCA và commit minh chứng)
│   ├── deployment-guide.md                       # [MỚI ở BT3] Cẩm nang triển khai 6 mục chuẩn mực Tiếng Anh & hướng dẫn Render Cloud
│   ├── checklist-bao-mat.md                      # [MỚI ở BT3] Danh mục tự đánh giá an toàn bảo mật 7 tiêu chí OWASP kèm minh chứng cụ thể
│   ├── data-dictionary.md                        # [MỚI ở BT3] Từ điển dữ liệu CSDL MongoDB 5 collections (BSON types, indexes, quy tắc nghiệp vụ)
│   ├── api-docs/                                 # [Track SE - MỚI ở BT3] Đặc tả kỹ thuật toàn diện 22 RESTful API Endpoints
│   │   ├── README.md                             # Tài liệu đặc tả 22 API phân lớp bằng Markdown chuẩn mực kỹ thuật (Tiếng Anh)
│   │   └── openapi.json                          # Hợp đồng chuẩn OpenAPI 3.0 / Swagger JSON tự động xuất từ FastAPI
│   ├── srs.md                                    # Bản đặc tả yêu cầu phần mềm SRS rút gọn (7 FR cốt lõi + 2 FR CRUD S1, 4 NFR định lượng, 5 BR, RTM kín)
│   ├── api-contract.md                           # Hợp đồng giao tiếp RESTful API chuẩn JSON (Endpoint, Header JWT, Payload, Bảng mã lỗi, CRUD S1)
│   ├── thay-doi-thiet-ke.md                      # Nhật ký thay đổi thiết kế duy nhất tích hợp đầy đủ 3 giai đoạn BT1 - BT2 - BT3
│   ├── thietke.md                                # Đặc tả chi tiết giao diện Dark 3D Elevation từng màn hình/vai trò & bộ Prompt Google Stitch
│   ├── dieukientest.md                           # Bộ điều kiện kiểm thử, ràng buộc hai chiều trong/ngoài và ma trận kịch bản toàn diện
│   ├── ai-disclosure.md                          # Bảng khai báo sử dụng công cụ AI minh bạch cho cả 3 giai đoạn BT1, BT2, BT3 (cam kết 13/11/2026)
│   ├── wireframe.png                             # Hình ảnh phác thảo giao diện Wireframe Dark Mode 3 vai trò (Kỹ thuật, Vật tư, Quản lý)
│   ├── layered clean architecture.drawio         # Bản vẽ gốc sơ đồ Kiến trúc Phân lớp 5 tầng ĐÃ HIỆN THỰC thực tế
│   ├── architecture.drawio                       # Bản vẽ gốc sơ đồ Kiến trúc hệ thống thiết kế ban đầu ở BT1
│   ├── erd.drawio                                # Bản vẽ gốc sơ đồ Mô hình dữ liệu NoSQL MongoDB Document Relationship
│   ├── usecase.drawio                            # Bản vẽ gốc sơ đồ Use Case tổng thể Luồng 05 (3 Actors, 7 Use Cases & <<include>> UC-99)
│   └── screenshots/                              # THƯ MỤC 19 ẢNH CHỤP MINH CHỨNG KIỂM CHỨNG HỆ THỐNG THỰC TẾ
│       ├── bug01_verify_test09.png               # Minh chứng xác nhận gỡ triệt để BUG-01 (Mật khẩu băm Bcrypt, cấm Plaintext)
│       ├── bug02_verify_test06.png               # Minh chứng xác nhận gỡ triệt để BUG-02 (Kiểm soát thời hạn hiệu lực OTP 10 phút)
│       ├── bug03_verify_seed.png                 # Minh chứng xác nhận gỡ triệt để BUG-03 (Nạp hạt giống Idempotent 40 linh kiện)
│       ├── bug04_verify_alert.png                # Minh chứng xác nhận gỡ triệt để BUG-04 (Hiển thị chính xác tồn kho cảnh báo Quản lý)
│       ├── bug05_verify_11crud.png               # Minh chứng xác nhận gỡ triệt để BUG-05 (11/11 tests CRUD XÓA đạt tiêu chí SE S1)
│       ├── docker_compose_up.png                 # Minh chứng khởi dựng Docker Compose thành công
│       ├── maytrang_clone_tag_v1.png             # Minh chứng clone tag v1.0 độc lập tại D:\kiem-tra-may-trang
│       ├── maytrang_docker_up_healthy.png        # Minh chứng 2 container mekong-l5-app và mongodb đều đạt trạng thái Healthy
│       ├── maytrang_docker_healthcheck.png       # Minh chứng kiểm tra curl /health trả về status online
│       ├── maytrang_pytest_part1.png             # Minh chứng chạy 67 tests bên trong container máy trắng (phần 1)
│       ├── maytrang_pytest_part2.png             # Minh chứng chạy 67 tests bên trong container máy trắng (phần 2 - 100% PASSED)
│       ├── test_pytest_pass.png                  # Minh chứng tổng thể 67/67 tests PASSED
│       ├── test_pytest_detail.png                # Minh chứng chi tiết các suite kiểm thử tự động
│       ├── ui_loading_state.png                  # Minh chứng giao diện trạng thái Đang tải (Loading State)
│       ├── ui_empty_state.png                    # Minh chứng giao diện trạng thái Dữ liệu rỗng (Empty State)
│       ├── ui_error_state.png                    # Minh chứng giao diện trạng thái Xử lý sự cố lỗi (Error State)
│       ├── ui_kythuat_xuatkho.png                # Minh chứng giao diện Workspace Nhân viên Kỹ thuật (Xuất kho thay thế)
│       ├── ui_vattu_nhapkho.png                  # Minh chứng giao diện Workspace Nhân viên Vật tư (Nhập kho vật tư)
│       └── ui_quanly_dashboard.png               # Minh chứng giao diện Workspace Quản lý kho (Dashboard & Cảnh báo an toàn)
│
├── src/                                          # MÃ NGUỒN CHÍNH THỰC THI HỆ THỐNG (5 TẦNG PHÂN LỚP SẠCH - CHẠY TRỰC TIẾP & DOCKER)
│   ├── app.py                                    # Điểm khởi chạy FastAPI, cấu hình CORS, Global Exception Handler, /health & Mount Static SPA
│   ├── errors/
│   │   └── AppError.py                           # Định nghĩa lớp cha AppError và 6 lớp ngoại lệ nghiệp vụ (EX-02..EX-05, 403, 404)
│   ├── routes/
│   │   ├── __init__.py                           # Nạp mô-đun động (importlib) xuất khẩu đối tượng router và auth_router
│   │   └── inventory.routes.py                   # Giải mã Bearer JWT (BR-04) & điều phối 22 API Endpoints (Kho, Nhân sự, Auth, CRUD S1)
│   ├── validators/
│   │   ├── __init__.py                           # Nạp mô-đun động xuất khẩu các hàm kiểm định dữ liệu đầu vào
│   │   └── inventory.validator.py                # Kiểm định miền giá trị số lượng, mật khẩu 4 nhóm ký tự, bắt buộc ticket_id khi OUT/RETURN
│   ├── services/
│   │   ├── __init__.py                           # Nạp mô-đun động xuất khẩu lớp InventoryService và thực thể inventory_service
│   │   └── inventory.service.py                  # Trái tim nghiệp vụ thuần Python 100% (không chứa HTTP): BR-01..BR-05, Optimistic Locking & CRUD guards
│   ├── repositories/
│   │   ├── __init__.py                           # Nạp mô-đun động xuất khẩu lớp InventoryRepository và thực thể inventory_repository
│   │   └── inventory.repository.py               # Thao tác CRUD nguyên tử với MongoDB kết hợp cơ chế lưu trữ kép Dual-Persistence Fallback
│   └── static/                                   # GIAO DIỆN NGƯỜI DÙNG SPA DARK 3D ELEVATION TÍCH HỢP TRỰC TIẾP TRÊN CỔNG 8000
│       ├── index.html                            # Khung cấu trúc SPA: Màn hình Auth Split-Screen, Đồng hồ OTP 10 phút & Workspace 3 vai trò
│       ├── styles.css                            # Bộ biến Design Tokens Dark 3D (.card-3d, Glassmorphism, 4 nhóm huy hiệu màu ngữ nghĩa)
│       └── app.js                                # Lớp API Client tập trung apiCall(), định tuyến 13 màn hình & xử lý đủ Loading/Empty/Error
│
├── tests/                                        # BỘ 67 CA KIỂM THỬ TỰ ĐỘNG HÓA TOÀN DIỆN (CHẠY PASS 100% BẰNG 1 LỆNH)
│   ├── inventory.service.test.py                 # 07 Unit Tests kiểm thử cô lập lớp InventoryService trên RAM (không phụ thuộc HTTP/DB)
│   ├── inventory.routes.test.py                  # 06 Integration Tests kiểm thử hợp đồng API, phân quyền RBAC & mã lỗi chuẩn HTTP
│   ├── auth_and_user.test.py                     # 15 Tests kiểm thử Đăng ký, mật khẩu 4 nhóm, OTP 10 phút, khóa vĩnh viễn TERMINATED
│   ├── cross_role_and_ui.test.py                 # 15 E2E & UI Tests kiểm thử luồng liên thông 3 vai trò & tính toàn vẹn giao diện SPA
│   ├── bt3_specification_and_constraints.test.py # 13 Tests kiểm thử đặc tả & ràng buộc: RETURN, biên 2 phía (BR-01, BR-05), chặn phiếu đóng, Race Condition, bảo mật S3/S4, nạp seed C8
│   └── se_s1_crud.test.py                        # 11 Tests kiểm thử toàn diện 4 thao tác CRUD (Create, Read, Update, Delete) cho 2 thực thể part & users (tiêu chí SE S1)
│
├── backend/                                      # KHÔNG GIAN DỊCH VỤ BACKEND ĐỘC LẬP (ĐỒNG BỘ 5 TẦNG CHO MÔ HÌNH PHÂN TÁN)
│   ├── .env & .env.example                       # Cấu hình môi trường riêng của gói Backend độc lập
│   ├── app.py                                    # Điểm khởi chạy FastAPI độc lập cho Backend
│   ├── pytest.ini                                # Cấu hình Pytest cho gói Backend
│   ├── requirements.txt                          # Danh mục phụ thuộc cho gói Backend
│   ├── data/ (users_store.json)                  # Bản lưu trữ dữ liệu offline fallback của Backend
│   ├── migrations/ (001_create_collections.js, 002_create_indexes.js) # Bản kịch bản CSDL NoSQL của Backend
│   ├── seeds/ (001_seed_parts_demo.json, seed.py)# Bản dữ liệu mẫu hạt giống của Backend
│   ├── src/ (app.py, errors, repositories, routes, services, static, validators) # Bản đồng bộ đầy đủ 5 tầng kiến trúc
│   └── tests/ (auth_and_user, cross_role_and_ui, inventory.routes, inventory.service) # Bộ kiểm thử của Backend
│
├── frontend/                                     # KHÔNG GIAN MÃ NGUỒN FRONTEND ĐỘC LẬP (REACTJS / NODEJS CHO MÔ HÌNH PHÂN TÁN)
│   ├── .env & .gitignore                         # Cấu hình môi trường và loại trừ node_modules/ riêng của Frontend
│   ├── package.json                              # Cấu hình kịch bản npm start khởi chạy máy chủ giao diện độc lập trên cổng 3000
│   ├── public/                                   # Bản đồng bộ tài nguyên giao diện SPA tĩnh (index.html, styles.css, app.js)
│   └── src/                                      # Các mô-đun kiến trúc thành phần ReactJS tách lớp:
│       ├── App.js & index.js                     #   - Khung khởi tạo ứng dụng thành phần React
│       ├── api/ (client.js, inventory.api.js)    #   - Lớp khách gọi HTTP RESTful API tách riêng biệt
│       ├── services/ (api.js)                    #   - Bộ hàm bọc dịch vụ truyền thông dữ liệu kho và nhân sự
│       ├── components/ (DataState.jsx, Header.js, Footer.js) # - Thành phần hiển thị 3 trạng thái Loading/Empty/Error
│       └── pages/ (AuthPortal.js, ManagerUsers.js) # - Trang giao diện xác thực và quản lý nhân sự
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
└── scripts/                                      # TẬP HỢP KỊCH BẢN TIỆN ÍCH NỘI BỘ HỖ TRỢ PHÁT TRIỂN & CHUẨN HÓA DỮ LIỆU
    ├── add_33_parts.py                           # Kịch bản nạp bổ sung 33 linh kiện mới mở rộng danh mục 40 linh kiện
    ├── apply_adjustments.py                      # Kịch bản áp dụng tự động các điều chỉnh nghiệp vụ
    ├── debug_test13.py                           # Kịch bản gỡ lỗi cho bài test TC-13 (CRUD S1)
    ├── fix_doc_links.py                          # Kịch bản rà soát và sửa lỗi liên kết tài liệu markdown
    ├── generate_bt2_docx.py                      # Kịch bản tự động xuất file Báo cáo Word BT2 chuẩn 7 mục
    ├── generate_bt3_docx.py                      # Kịch bản tự động xuất file Báo cáo Word BT3 chuẩn 7 mục
    ├── generate_docs_test.py                     # Kịch bản tự động kiểm tra cú pháp tài liệu kỹ thuật
    ├── generate_readme.py                        # Kịch bản hỗ trợ cập nhật nội dung README
    ├── reorganize_docs.py                        # Kịch bản tinh gọn và sắp xếp lại hồ sơ tài liệu
    ├── update_app_js.py                          # Kịch bản cập nhật logic frontend trong app.js
    ├── update_tech_ui.py                         # Kịch bản cập nhật giao diện người dùng kỹ thuật
    └── update_thietke_md.py                      # Kịch bản đồng bộ nội dung đặc tả giao diện thietke.md"""

with open('README.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = None
end_idx = None
for i, l in enumerate(lines):
    if l.startswith('### 1.4. Cấu trúc Thư mục Thực tế'):
        start_idx = i
    if l.startswith('### 1.5. Bảng Đối chiếu 1–1'):
        end_idx = i
        break

if start_idx is not None and end_idx is not None:
    # find where ```text starts and where ``` ends
    code_start = None
    code_end = None
    for j in range(start_idx, end_idx):
        if lines[j].strip() == '```text':
            code_start = j
        elif lines[j].strip() == '```' and code_start is not None:
            code_end = j
            break

    if code_start is not None and code_end is not None:
        new_lines = lines[:code_start+1] + [tree_text + '\n'] + lines[code_end:]
        with open('README.md', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print('Successfully replaced Section 1.4 directory tree in README.md!')
    else:
        print('Could not find code block boundaries.')
else:
    print('Could not find section boundaries.')

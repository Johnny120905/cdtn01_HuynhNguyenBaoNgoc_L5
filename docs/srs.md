# TÀI LIỆU ĐẶC TẢ YÊU CẦU PHẦN MỀM (SRS) RÚT GỌN
**Dự án:** Smart CRM – Mekong Mobile  
**Phân hệ:** Luồng 05 (`L5`) – Quản lý Kho linh kiện thay thế  
**Chi nhánh triển khai:** Trung tâm Bảo hành Mekong Mobile Quận 1 (`L5-WH-890`)

---

## Mục 1: Giới thiệu & Phạm vi

> **Bối cảnh & Phát biểu phạm vi dự án:**
> Hệ thống Smart CRM phân hệ L5 được xây dựng nhằm số hóa quy trình quản lý kho linh kiện thay thế tại các trung tâm bảo hành Mekong Mobile. Mục tiêu là triệt tiêu độ trễ thông tin, kiểm soát chặt chẽ tồn kho vật lý theo thời gian thực và đảm bảo tính minh bạch, bất biến trong luồng luân chuyển vật tư.

**1. Các hạng mục Trong phạm vi (In-Scope)**
- Quản lý danh mục linh kiện (`part`) và thiết lập ngưỡng tồn kho an toàn (`min_threshold`).
- Ghi nhận giao dịch nhập kho (`IN`), xuất kho (`OUT`) và hoàn trả kho (`RETURN`) theo thời gian thực.
- Tra cứu tồn kho Real-time và cảnh báo tự động (`WARNING`) khi chạm hoặc thấp hơn ngưỡng an toàn.
- Phân quyền theo 3 vai trò (`ACT-01`, `ACT-02`, `ACT-03`) và cô lập dữ liệu độc lập theo từng trung tâm bảo hành (`center_id`).

**2. Các hạng mục Ngoài phạm vi (Out-of-Scope / WON'T HAVE)**
- Quản lý quy trình Lễ tân tiếp nhận thiết bị của khách hàng.
- Tích hợp API đồng bộ dữ liệu với hệ thống Kế toán – Tài chính / Hóa đơn VAT (FIFO/LIFO).
- Tự động gửi Email đặt hàng (PO) tới Nhà cung cấp ngoài hoặc theo dõi vận chuyển (Logistics) từ Tổng công ty về chi nhánh.

**3. Bảng thuật ngữ nghiệp vụ (Business Glossary)**
- **Phiếu bảo hành (`Ticket` / `ticket_id`):** Chứng từ nghiệp vụ ghi nhận yêu cầu sửa chữa hợp lệ của khách hàng (`OPEN`), bắt buộc đính kèm khi xuất hoặc hoàn kho.
- **Linh kiện (`Part` / `part_code`):** Đơn vị vật tư thay thế chuẩn hóa phục vụ sửa chữa thiết bị.
- **Tồn kho Real-time (`Stock` / `quantity`):** Số lượng vật lý khả dụng thực tế của một linh kiện tại một trung tâm bảo hành cụ thể (`center_id`).
- **Giao dịch kho (`Transaction`):** Bản ghi nhật ký bất biến (`Insert-only`) phản ánh biến động tồn kho (`IN`, `OUT`, `RETURN`).
- **Ngưỡng an toàn (`Min_threshold` / `min_threshold`):** Mức tồn kho tối thiểu do Quản lý kho cấu hình để kích hoạt cờ cảnh báo thiếu hàng.

---

## Mục 2: Các bên liên quan & Vai trò (Stakeholders & Actors)

| Mã Tác nhân | Tên Vai trò (Role) | Mã Phân quyền Hệ thống | Nhóm nghiệp vụ & Trách nhiệm chính |
| :---: | :--- | :---: | :--- |
| **`ACT-01`** | **Nhân viên kỹ thuật** (*Technical Staff*) | `TECH_STAFF` | **Nhóm Nhập liệu (*Data Entry*):** Trực tiếp sửa chữa thiết bị; có quyền tra cứu tồn kho Real-time (`UC-04`), xuất kho kèm mã phiếu (`UC-02`) và hoàn trả linh kiện dư (`UC-03`). |
| **`ACT-02`** | **Nhân viên vật tư** (*Material Specialist*) | `MATERIAL_STAFF` | **Nhóm Nhập liệu (*Data Entry*):** Tiếp nhận lô hàng linh kiện mới từ Tổng công ty/Nhà cung cấp và thực hiện nghiệp vụ nhập kho (`UC-01`). |
| **`ACT-03`** | **Quản lý kho** (*Inventory Manager*) | `MANAGER` | **Nhóm Giám sát (*Data Monitor*):** Giám sát tồn kho tổng thể, xem nhật ký giao dịch đối soát (`UC-05`), thiết lập ngưỡng an toàn (`UC-06`) và theo dõi cảnh báo thiếu hàng (`UC-07`). |

---

## Mục 3: Yêu cầu chức năng (Functional Requirements - FR)

| Mã FR | Tên Yêu cầu Chức năng | Tác nhân chính | Mô tả nghiệp vụ cốt lõi | Mức ưu tiên (MoSCoW) |
| :---: | :--- | :---: | :--- | :---: |
| **`FR-01`** | **Nhập kho linh kiện** | `ACT-02` (`MATERIAL_STAFF`) | Ghi nhận giao dịch nhập lô linh kiện mới (`type = 'IN'`), cộng dồn số lượng tồn kho tại chi nhánh và lưu nhật ký giao dịch. | **`MUST`** |
| **`FR-02`** | **Xuất kho hợp lệ** | `ACT-01` (`TECH_STAFF`) | Ghi nhận giao dịch xuất linh kiện sửa chữa (`type = 'OUT'`) bắt buộc đính kèm `ticket_id` hợp lệ (`UC-99`), trừ tồn kho nguyên tử và chặn âm kho. | **`MUST`** |
| **`FR-03`** | **Hoàn trả kho (Return)** | `ACT-01` (`TECH_STAFF`) | Ghi nhận giao dịch hoàn trả linh kiện dư/không sử dụng (`type = 'RETURN'`) gắn với `ticket_id` hợp lệ (`UC-99`) để cộng bù trừ lại tồn kho. | **`MUST`** |
| **`FR-04`** | **Tra cứu tồn kho Real-time** | `ACT-01` (`TECH_STAFF`) | Tra cứu tức thời số lượng tồn kho vật lý, đơn giá, ngưỡng an toàn và cờ trạng thái (`NORMAL`/`WARNING`) theo `part_code` tại chi nhánh. | **`MUST`** |
| **`FR-05`** | **Xem nhật ký giao dịch (Audit Log)** | `ACT-03` (`MANAGER`) | Truy xuất lịch sử giao dịch bất biến (`IN`/`OUT`/`RETURN`) sắp xếp giảm dần theo thời gian thực để phục vụ hậu kiểm và đối soát. | **`SHOULD`** |
| **`FR-06`** | **Thiết lập ngưỡng an toàn** | `ACT-03` (`MANAGER`) | Cho phép duy nhất Quản lý kho cấu hình giá trị `min_threshold` (`>= 0`) cho từng mã linh kiện trong danh mục `part`. | **`MUST`** |
| **`FR-07`** | **Hiển thị cảnh báo thiếu hàng** | `ACT-03` (`MANAGER`) | Tự động đánh giá và hiển thị danh sách linh kiện có tồn kho chạm hoặc thấp hơn ngưỡng an toàn (`quantity <= min_threshold`). | **`SHOULD`** |
| **`FR-08`** | **Quản lý danh mục linh kiện (CRUD Part)** | `ACT-03` (`MANAGER`) | Đầy đủ 4 thao tác Create, Read, Update, Delete linh kiện; chặn xóa linh kiện nếu còn tồn kho $> 0$ (Tiêu chí `[SE] S1`). | **`MUST`** |
| **`FR-09`** | **Quản trị tài khoản nhân sự (CRUD User)** | `ACT-03` (`MANAGER`) | Đầy đủ 4 thao tác Create, Read, Update, Delete nhân sự; chặn Quản lý tự xóa chính mình (Tiêu chí `[SE] S1`). | **`MUST`** |

---

## Mục 4: Yêu cầu Phi chức năng (Non-Functional Requirements - NFR)

| Mã NFR | Thuộc tính chất lượng | Chỉ số đo lường & Ngưỡng nghiệm thu kỹ thuật |
| :---: | :--- | :--- |
| **`NFR-01`** | **Tính Tái lập & Triển khai (*Deployability*)** | Hệ thống phải được dựng và khởi chạy thành công từ môi trường sạch bằng tối đa **2 câu lệnh (`<= 2 commands`)** trên Terminal (hoặc 1 lệnh `docker compose up -d --build`). **100%** biến cấu hình nhạy cảm đọc từ `.env`, không hardcode secret trong mã nguồn. |
| **`NFR-02`** | **Hiệu năng & Thời gian phản hồi (*Performance*)** | Thời gian phản hồi của các API tra cứu tồn kho và giao dịch cốt lõi đạt mức **`< 500ms`** ở tải trọng `10.000` bản ghi nhờ đánh chỉ mục phức hợp (`idx_stock_lookup` trên `{center_id: 1, part_code: 1}` và `idx_transaction_history` trên `{center_id: 1, created_at: -1}`). |
| **`NFR-03`** | **Tính Toàn vẹn Dữ liệu Đồng thời (*Concurrency & Integrity*)** | Sai lệch số lượng tồn kho bằng **`0`** (`quantity >= 0` tuyệt đối) ngay cả khi có **`>= 50` requests** xuất kho đồng thời nhờ cơ chế Khóa lạc quan (*Optimistic Locking* qua trường `version`). Lịch sử giao dịch tuân thủ `Insert-only` với **`0%`** quyền sửa/xóa. |
| **`NFR-04`** | **Tính Khả dụng & Trải nghiệm (*Usability*)** | Kỹ thuật viên hoàn thành thao tác Tra cứu & Xuất kho trong tối đa **3 thao tác (`<= 3 clicks`)**; thông báo lỗi Tiếng Việt trực quan, tỷ lệ phơi bày lỗi thô `500 Internal Server Error` ra giao diện người dùng bằng **`0%`**. |

---

## Mục 5: Ràng buộc và Quy tắc nghiệp vụ (Business Rules - BR)

| Mã BR | Tên Quy tắc Nghiệp vụ | Nội dung ràng buộc kỹ thuật | Yêu cầu phục vụ trực tiếp |
| :---: | :--- | :--- | :--- |
| **`BR-01`** | **Tồn kho không âm (*Non-negative Stock*)** | Hệ thống tự động đánh chặn mọi giao dịch xuất kho nếu số lượng yêu cầu vượt quá tồn kho thực tế (`quantity_out > current_stock` → HTTP `400` / `EX-04`). | Phục vụ trực tiếp cho `FR-02` và `NFR-04`. |
| **`BR-02`** | **Bắt buộc chứng từ (*Ticket Reference Mandate*)** | Mọi giao dịch Xuất kho (`OUT`) hoặc Hoàn trả (`RETURN`) bắt buộc phải gắn với một mã phiếu bảo hành (`ticket_id`) tồn tại và đang mở (`OPEN`); giao dịch Nhập kho (`IN`) không yêu cầu `ticket_id` (`EX-03` → HTTP `422`). | Phục vụ trực tiếp cho `FR-02` và `FR-03`. |
| **`BR-03`** | **Bất biến lịch sử (*Transaction Immutability*)** | Mọi biến động kho đều sinh bản ghi nhật ký vĩnh viễn (`Insert-only`). Tuyệt đối không có API cập nhật hay xóa giao dịch; nếu xuất nhầm phải lập giao dịch `RETURN` để bù trừ. | Phục vụ trực tiếp cho `FR-05` và `NFR-03`. |
| **`BR-04`** | **Dữ liệu khu vực (*Center Isolation*)** | Tài khoản đăng nhập thuộc chi nhánh nào (`center_id` giải mã từ Bearer JWT Token) chỉ được phép xem tồn kho và thực hiện giao dịch tại đúng chi nhánh đó (`EX-02` → HTTP `403`). | Phục vụ trực tiếp cho Chính sách Phân quyền và Bảo mật hệ thống (*Security*). |
| **`BR-05`** | **Đánh giá ngưỡng an toàn (*Threshold Evaluation*)** | Ngay khi `quantity <= min_threshold`, hệ thống lập tức gắn cờ cảnh báo đỏ (`status_flag = "WARNING"`) theo thời gian thực mà không có ngoại lệ. | Phục vụ trực tiếp cho `FR-06`, `FR-07` và `NFR-04`. |

---

## Mục 6: Ma trận Truy vết Yêu cầu (Requirements Traceability Matrix - RTM)

| Mã Yêu cầu Chức năng (FR) | Mã User Story (US) | Mã Use Case (UC) | Quy tắc & Ngoại lệ liên quan | Mức độ ưu tiên (MoSCoW) |
| :--- | :---: | :--- | :---: | :---: |
| **FR-01:** Nhập kho linh kiện | `US-01` | `UC-01` | `BR-03`, `BR-04`, `EX-02` | **`MUST`** |
| **FR-02:** Xuất kho hợp lệ | `US-02` | `UC-02` (`<<include>>` `UC-99`) | `BR-01`..`BR-05`, `EX-02`..`EX-05` | **`MUST`** |
| **FR-03:** Hoàn trả kho (Return) | `US-03` | `UC-03` (`<<include>>` `UC-99`) | `BR-02`, `BR-03`, `BR-04`, `EX-02`, `EX-03` | **`MUST`** |
| **FR-04:** Tra cứu Tồn kho Real-time | `US-04` | `UC-04` | `BR-04`, `BR-05`, `EX-02` | **`MUST`** |
| **FR-05:** Xem Nhật ký Giao dịch | `US-05` | `UC-05` | `BR-03`, `BR-04` | **`SHOULD`** |
| **FR-06:** Thiết lập Ngưỡng an toàn | `US-06` | `UC-06` | `BR-05` | **`MUST`** |
| **FR-07:** Hiển thị Cảnh báo | `US-07` | `UC-07` | `BR-04`, `BR-05` | **`SHOULD`** |
| **FR-08:** Quản lý Danh mục Linh kiện (CRUD) | `US-08` | `UC-08` | `BR-01` (Chặn xóa tồn > 0) | **`MUST`** |
| **FR-09:** Quản trị Tài khoản Nhân sự (CRUD) | `US-09` | `UC-09` | RBAC, Chặn tự xóa chính mình | **`MUST`** |

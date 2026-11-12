# NHẬT KÝ THAY ĐỔI THIẾT KẾ (DESIGN CHANGE LOG)

- **Dự án:** Hệ thống Smart CRM – Mekong Mobile
- **Luồng nghiệp vụ:** Luồng 05 (L5) – Kho linh kiện thay thế
- **Chi nhánh triển khai:** Trung tâm Bảo hành Mekong Mobile Quận 1 (`L5-WH-890`)
- **Track:** Công nghệ phần mềm (SE)
- **Sinh viên thực hiện:** Huỳnh Nguyễn Bảo Ngọc – `2374802010339`
- **Giảng viên hướng dẫn:** TS. Nguyễn Trí Hải
- **Tài liệu liên quan:** [srs.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/srs.md) | [thietke.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/thietke.md) | [api-contract.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/api-contract.md) | [BT2.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/BT2.md) | [test.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/test.md) | [README.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/README.md)

---

## PHẦN I: Tổng hợp các điều chỉnh từ Bản cũ sang Bản mới (Sau phản hồi Bài tập 1)

Phần này ghi nhận đầy đủ kết quả đối chiếu giữa **Bản Bài tập 1 cũ (trước khi nhận phản hồi/feedback)** và **Bản Bài tập 1 mới (sau khi tiếp thu phản hồi của Giảng viên hướng dẫn TS. Nguyễn Trí Hải và chỉnh sửa hoàn thiện)**.

### Bảng tóm tắt 5 hạng mục điều chỉnh Bài tập 1 (Sau phản hồi của Giảng viên)

| Mã thay đổi | Hạng mục & Vị trí điều chỉnh | Tóm tắt phản hồi của Giảng viên | Quyết định | Kết quả chuẩn hóa ở Bản mới |
| :---: | :--- | :--- | :---: | :--- |
| **TD-01** | **Thành phần 1 (Bản SRS rút gọn)** – Mục 3 (`FR`), Mục 4 (`NFR`), Mục 5 (`BR`) | Bài dài 24 trang với nhiều tiêu đề song ngữ rườm rà; `BR-04` ghi phục vụ *"NFR-04 Bảo mật"* trong khi `NFR-04` thực tế là Usability. | **SỬA** | Cấu trúc hóa Mục 3, 4, 5 thành Bảng tập trung; nâng `FR-03` từ `SHOULD` lên `MUST`; sửa ánh xạ `BR-04` về *Chính sách Phân quyền & Bảo mật (Security)* và bổ sung `BR-01`, `BR-05` phục vụ `NFR-04`. |
| **TD-02** | **Thành phần 2 (Use Case)** – Mục 1 (Sơ đồ tổng thể) & Mục 2 (Đặc tả `UC-02`) | Sơ đồ thiếu bảng chú thích; vẽ `<<include>>` `UC-99` từ `UC-03` & `UC-04` lệch với văn bản (`UC-02` & `UC-03`); luồng chính chưa đánh số bước khi ngoại lệ tham chiếu 2a, 3a, 4a, 5a. | **SỬA** | Sửa `<<include>>` tới `UC-99` từ `UC-02` và `UC-03`; thêm bảng chú thích vào [usecase.drawio](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/usecase.drawio); đánh số bước `01`–`07` chuẩn NoSQL và đồng bộ mã ngoại lệ `EX-02`, `EX-03`, `EX-04`, `EX-05`. |
| **TD-03** | **Thành phần 3 (Thiết kế kiến trúc)** – Mục 1 (Sơ đồ phân lớp) & Mục 2 (Lập luận) | Sơ đồ kiến trúc thiếu khung chú thích ký hiệu; tên thực thể lưu trữ chưa đồng bộ với mô hình dữ liệu. | **SỬA** | Đổi tên Collection từ số nhiều sang số ít (`part`, `part_stock`, `part_transaction`); thêm bảng chú thích vào [architecture.drawio](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/architecture.drawio); bổ sung lập luận khởi tạo bằng MongoDB Shell JS & driver `PyMongo`/`Motor`. |
| **TD-04** | **Thành phần 4 (Mô hình dữ liệu)** – Mục 1 (Sơ đồ ERD) & Mục 2 (Schema mã nguồn) | Sơ đồ ERD thiếu chú thích; bản cũ dùng RDBMS 3NF và SQL `CREATE TABLE` (PostgreSQL) mâu thuẫn với MongoDB Atlas ở Thành phần 3. | **SỬA** | Chuyển toàn bộ sang *MongoDB Document Relationship* (kiểu BSON, thêm bảng chú thích vào [erd.drawio](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/erd.drawio)); thay SQL DDL bằng `db.createCollection` (`$jsonSchema`), bổ sung trường `version` (*Optimistic Locking*) và lệnh `createIndex`. |
| **TD-05** | **Thành phần 5 (Wireframe 3 màn hình)** – Mục 1 (Phác thảo & Đối chiếu ERD) | Bảng đối chiếu Màn hình 1 ghi lỗi xuất quá tồn kho thuộc `UC-04` thay vì `UC-02`; cần đồng bộ tên 3 vai trò và thuật ngữ thao tác NoSQL. | **SỬA** | Cập nhật 3 ảnh Wireframe Dark Mode chuẩn 3 vai trò; sửa lỗi xuất quá tồn thành **`Ngoại lệ EX-04 của UC-02 (Vi phạm BR-01)`**; bổ sung đối chiếu Màn hình 2 & 3 và đổi thuật ngữ sang `collection part`. |

---

### TD-01: Cấu trúc hóa bảng biểu và chuẩn hóa ánh xạ BR-04 tại Bản SRS rút gọn
* **Vị trí thay đổi:** Thành phần 1 (Bản SRS rút gọn) – Mục 3 (Yêu cầu chức năng), Mục 4 (Yêu cầu phi chức năng) và Mục 5 (Ràng buộc & Quy tắc nghiệp vụ).
* **Phản hồi của giảng viên:** Bài dài 24 trang với nhiều tiêu đề song ngữ rườm rà; quy tắc `BR-04` ghi phục vụ "NFR-04 Bảo mật" trong khi `NFR-04` thực tế là Usability.
* **Quyết định:** **SỬA**.
* **Chi tiết trước và sau khi chỉnh sửa:**
  * **Tại Mục 3, 4, 5:** Chuyển đổi toàn bộ cách trình bày từ dạng danh sách gạch đầu dòng rời rạc ở bản cũ sang **dạng Bảng (Table) tập trung**, lược bỏ các tiêu đề phụ song ngữ dài dòng để cô đọng tài liệu.
  * **Tại Mục 3 (`FR-03`):** Nâng mức độ ưu tiên MoSCoW của `FR-03` (Hoàn trả kho) trong bảng đặc tả từ `SHOULD` lên `MUST` để đảm bảo tính khép kín của nghiệp vụ bù trừ kho.
  * **Tại Mục 5 (Ánh xạ `BR`):**
    * **`BR-04` (Dữ liệu khu vực):** Bản cũ ghi *"Phục vụ cho NFR-04 (Bảo mật và Phân quyền)"* → Bản mới sửa thành *"Phục vụ trực tiếp cho Chính sách Phân quyền và Bảo mật hệ thống (Security)"*.
    * **`BR-01` & `BR-05`:** Bổ sung ánh xạ phục vụ trực tiếp thêm cho `NFR-04` (hiển thị cờ cảnh báo và thông báo lỗi trực quan trên UI).

---

### TD-02: Chuẩn hóa Sơ đồ Use Case, đánh số bước Luồng chính và đồng bộ Mã ngoại lệ
* **Vị trí thay đổi:** Thành phần 2 (Use Case) – Mục 1 (Sơ đồ Use Case Tổng thể) và Mục 2 (Đặc tả Chi tiết Use Case `UC-02`).
* **Phản hồi của giảng viên:** Sơ đồ thiếu khung chú thích ký hiệu; sơ đồ vẽ `<<include>>` `UC-99` từ `UC-03` và `UC-04` nhưng văn bản nói `UC-02` và `UC-03`; luồng chính `UC-02` chưa đánh số bước trong khi ngoại lệ tham chiếu bước 2a, 3a, 4a, 5a.
* **Quyết định:** **SỬA**.
* **Chi tiết trước và sau khi chỉnh sửa:**
  * **Tại Mục 1 (Sơ đồ Use Case & Tác nhân):**
    * Sửa lại đường nối `<<include>>` tới `UC-99` (Xác thực mã phiếu) xuất phát đúng từ **`UC-02` (Xuất kho hợp lệ)** và **`UC-03` (Hoàn trả kho)**, xóa bỏ đường nối sai từ `UC-04` (Tra cứu tồn kho).
    * Bổ sung **Bảng chú thích: Sơ đồ Use Case** trực tiếp bên cạnh sơ đồ ([usecase.drawio](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/usecase.drawio)).
    * Đồng bộ mô tả vị trí Tác nhân tại Tiểu mục 1: Bản cũ ghi Quản lý kho ở "Bên phải" trong khi hình vẽ nằm bên trái → Bản mới chuẩn hóa thành *"Được bố trí dọc theo phía bên trái của ranh giới hệ thống, phân thành 2 nhóm vai trò chính"*.
  * **Tại Mục 2 – Tiểu mục 1 (Luồng sự kiện chính - Happy Path):**
    * Chuyển từ dạng gạch đầu dòng không đánh số sang **bảng đánh số bước tuần tự từ `01` đến `07`**.
    * Thay thế thuật ngữ bảng SQL cũ (`part_stocks`, `part_transactions`) thành thuật ngữ chuẩn NoSQL (`collection part_stock`, `collection part_transaction`) tại bước `04`, `05`, `06`.
  * **Tại Mục 2 – Tiểu mục 2 (Luồng ngoại lệ - Exception Flow):**
    * Chuyển sang định dạng bảng gồm 4 cột (`Mã ngoại lệ`, `Bước liên quan`, `Điều kiện xảy ra lỗi`, `Mô tả cách xử lý & Kết quả`).
    * Đồng bộ lại toàn bộ mã ngoại lệ theo đúng số bước của luồng chính:
      * Bước `02` → **`EX-02`** (Vi phạm vùng dữ liệu khu vực - HTTP 403).
      * Bước `03` → Đổi từ `EX-01` (bản cũ) thành **`EX-03`** (Sai mã phiếu bảo hành - HTTP 422).
      * Bước `04` → Gán mã **`EX-04`** cho ngoại lệ 4a (Số lượng yêu cầu > tồn kho thực tế, vi phạm `BR-01` - HTTP 400).
      * Bước `05` → Đổi từ `EX-03` (bản cũ) thành **`EX-05`** (Xung đột dữ liệu đồng thời Race Condition - HTTP 409).

---

### TD-03: Đồng bộ tên Collection trên Sơ đồ Kiến trúc và bổ sung Lập luận NoSQL
* **Vị trí thay đổi:** Thành phần 3 (Thiết kế kiến trúc) – Mục 1 (Sơ đồ Kiến trúc Phân lớp) và Mục 2 (Lập luận Kiến trúc).
* **Phản hồi của giảng viên:** Sơ đồ kiến trúc thiếu khung chú thích ký hiệu; cần đồng bộ tên thực thể giữa sơ đồ kiến trúc và mô hình dữ liệu.
* **Quyết định:** **SỬA**.
* **Chi tiết trước và sau khi chỉnh sửa:**
  * **Tại Mục 1 (Sơ đồ Kiến trúc Phân lớp):**
    * Đổi tên 3 khối lưu trữ ở tầng dưới cùng (MongoDB Atlas Cloud) từ dạng số nhiều ở bản cũ (`parts`, `part_stocks`, `part_transactions`) sang **dạng số ít chuẩn xác (`part`, `part_stock`, `part_transaction`)** để khớp 100% với Sơ đồ ERD ở Thành phần 4.
    * Bổ sung **Bảng chú thích: Sơ đồ Kiến trúc phân lớp** trực tiếp vào bản vẽ ([architecture.drawio](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/architecture.drawio)).
  * **Tại Mục 2 (Lập luận Kiến trúc – Lập luận 3):** Bổ sung chi tiết kỹ thuật khởi tạo cấu trúc Collection bằng script độc lập qua cú pháp JavaScript của MongoDB Shell ([migrations/001_create_collections.js](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/migrations/001_create_collections.js), [migrations/002_create_indexes.js](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/migrations/002_create_indexes.js)) và kết nối Backend Python qua thư viện driver (`PyMongo`/`Motor`) thay vì chỉ nêu chung chung như bản cũ.

---

### TD-04: Chuyển đổi Mô hình dữ liệu từ RDBMS (SQL 3NF) sang NoSQL (MongoDB Schema)
* **Vị trí thay đổi:** Thành phần 4 (Mô hình dữ liệu) – Mục 1 (Sơ đồ Mô hình Dữ liệu) và Mục 2 (Cấu trúc Dữ liệu Mã nguồn).
* **Phản hồi của giảng viên & Yêu cầu đồng bộ Stack:** Sơ đồ ERD thiếu khung chú thích ký hiệu; bản cũ đang dùng sơ đồ RDBMS 3NF và mã lệnh SQL `CREATE TABLE` (PostgreSQL) gây mâu thuẫn với Lớp Lưu trữ MongoDB Atlas đã chọn ở Thành phần 3.
* **Quyết định:** **SỬA**.
* **Chi tiết trước và sau khi chỉnh sửa:**
  * **Tại Mục 1 (Sơ đồ Mô hình Dữ liệu):**
    * Đổi tiêu đề và nội dung từ *"Sơ đồ Mô hình Dữ liệu (ERD - Chuẩn 3NF)"* sang *"Sơ đồ Mô hình Dữ liệu (MongoDB Document Relationship)"* với 5 Collection độc lập.
    * Cập nhật kiểu dữ liệu trên sơ đồ từ kiểu SQL (`VARCHAR`, `DECIMAL`, `BIGSERIAL`, `TIMESTAMPTZ`) sang kiểu BSON/NoSQL (`ObjectId`, `String`, `Float`, `Integer`, `Long`, `ISODate`) và bổ sung khóa chính `_id : ObjectId «PK»` cho `part_stock`.
    * Bổ sung **Bảng chú thích sơ đồ ERD chi tiết** ngay dưới sơ đồ ([erd.drawio](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/erd.drawio)).
  * **Tại Mục 2 (Cấu trúc Dữ liệu Mã nguồn):**
    * Thay thế toàn bộ mã lệnh SQL DDL (`CREATE TABLE ... CHECK ...`) ở bản cũ bằng mã nguồn **MongoDB Schema & Indexes Skeleton (`db.createCollection` với bộ kiểm duyệt `\$jsonSchema`)**.
    * Bổ sung trường **`version` (`bsonType: "int"`)** vào danh sách trường bắt buộc (`required`) của collection `part_stock` để hiện thực hóa thuật toán *Optimistic Locking* chặn Race Condition (`EX-05` / `NFR-03`).
    * Chuyển lệnh tạo Index từ cú pháp SQL sang `db.part_stock.createIndex({ center_id: 1, part_code: 1 }, { unique: true, name: "idx_stock_lookup" })` và `db.part_transaction.createIndex({ center_id: 1, created_at: -1 }, { name: "idx_transaction_history" })`.

---

### TD-05: Cập nhật Giao diện Wireframe và sửa lỗi truy vết tại Bảng đối chiếu
* **Vị trí thay đổi:** Thành phần 5 (Wireframe 3 màn hình) – Mục 1 (Bản phác thảo Giao diện & Đối chiếu ERD) ở cả 3 màn hình.
* **Phản hồi của giảng viên:** Bảng đối chiếu Wireframe màn hình 1 ghi lỗi xuất quá tồn kho thuộc `UC-04` thay vì `UC-02`; cần đồng bộ thuật ngữ vai trò và thao tác NoSQL.
* **Quyết định:** **SỬA**.
* **Chi tiết trước và sau khi chỉnh sửa:**
  * **Cập nhật hình ảnh 3 màn hình Wireframe (Dark Mode UI):** Thay thế 3 ảnh wireframe cũ bằng bộ giao diện mới trực quan ([wireframe.png](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/wireframe.png)), hiển thị đúng tên và đúng 3 vai trò chuẩn của hệ thống: `Lê Văn Kỹ Thuật - Nhân viên Kỹ thuật` (Màn hình 1), `Nguyễn Thị Vật Tư - Nhân viên Vật tư` (Màn hình 2), và `Trần Văn Quản Lý - Quản lý Kho` (Màn hình 3).
  * **Tại Tiểu mục 1 – Bảng đối chiếu dữ liệu (Màn hình 1 - Nhân viên kỹ thuật):**
    * Sửa cột *Nguồn Use Case (UC) & FR* của dòng Cảnh báo đỏ *"Lỗi: Số lượng xuất vượt quá tồn kho..."* từ `Ngoại lệ UC-04 (Vi phạm BR-01)` (bản cũ) thành **`Ngoại lệ EX-04 của UC-02 (Vi phạm BR-01)`**.
  * **Tại Tiểu mục 2 – Bảng đối chiếu dữ liệu (Màn hình 2 - Nhân viên vật tư):**
    * Bổ sung thêm dòng đối chiếu: **Hiển thị thông số "Tồn trước nhập" & "Ngưỡng an toàn"** → Ánh xạ vào `part_stock.quantity & part.min_threshold` → Nguồn `UC-01, UC-07`.
  * **Tại Tiểu mục 3 – Bảng đối chiếu dữ liệu (Màn hình 3 - Quản lý kho):**
    * Bổ sung đầy đủ các trường đọc từ `part_transaction` (`created_at, type, part_code, quantity, ticket_id, created_by`) và gắn rõ mã quy tắc `BR-05`, `BR-03` vào cột nguồn Use Case.
    * Sửa mô tả hành động của nút *"Lưu cấu hình"* từ thuật ngữ SQL (`cập nhật cột min_threshold vào bảng part`) sang thuật ngữ NoSQL chuẩn xác (**`cập nhật trường min_threshold vào collection part`**).

---

## PHẦN II: Nhật ký thay đổi và cải tiến thiết kế trong giai đoạn hiện thực hóa Bài tập 2 (Sprint 2)

Sau khi hoàn tất chỉnh sửa thiết kế Bài tập 1 theo phản hồi của Giảng viên (Phần I), trong quá trình hiện thực hóa mã nguồn thực tế ở **Bài tập 2 (Sprint 2 – Release `v0.2`)**, hệ thống tiếp tục được tối ưu hóa qua các vòng lặp cải tiến thực nghiệm nhằm hoàn thiện trải nghiệm người dùng và độ bền vững của dữ liệu.

### 1. Lịch trình 4 đợt cải tiến trong quá trình hiện thực hóa hệ thống

```text
+----------------------------------------------------------------------------------------------------+
|                                    LỊCH TRÌNH 4 LẦN THAY ĐỔI HỆ THỐNG                              |
+----------------------------------------------------------------------------------------------------+
| LẦN 1 (Sprint 1 - Bài tập 1 & Chuẩn hóa sau Feedback GV):                                          |
| - Hoàn thiện tài liệu SRS, Use Case, Kiến trúc 4 tầng Clean Architecture và MongoDB Schema NoSQL.  |
| - Bản dựng khởi đầu có giao diện cơ bản, còn breadcrumb, lộ mã kỹ thuật (BR, FR, NFR), 7 linh kiện.|
|                                                  ▼                                                 |
| LẦN 2 (Sprint 2 - Đợt 1):                                                                          |
| - Chuyển đổi toàn diện sang Giao diện Dark 3D Elevation, phông chữ Be Vietnam Pro.                 |
| - Loại bỏ khung xám Luồng 05 trên Header, đổi tên nút thành "Đăng xuất tài khoản".                 |
| - Xóa bỏ 100% breadcrumbs và mã kỹ thuật lộ thiên trên giao diện người dùng.                       |
| - Chuẩn hóa 4 trạng thái nhân sự (ONLINE, AWAY, OFF_SHIFT, TERMINATED) và bộ lọc quản lý nhân sự.  |
|                                                  ▼                                                 |
| LẦN 3 (Sprint 2 - Đợt 2):                                                                          |
| - Thêm nút con mắt bật/tắt xem mật khẩu tại 3 biểu mẫu (Đăng nhập, Đăng ký, Quên mật khẩu).        |
| - Bảng quy chuẩn mật khẩu được ẩn mặc định (chỉ báo đỏ khi làm sai).                               |
| - Phục hồi CSDL người dùng và hoàn thiện luồng Quên mật khẩu OTP tự động điền.                     |
|                                                  ▼                                                 |
| LẦN 4 (Sprint 2 - Đợt 3 - Hoàn thiện tối ưu theo phản hồi thực nghiệm):                            |
| 1. Quên mật khẩu: Điều chỉnh thời gian OTP từ 15 xuống 10 phút, tích hợp đồng hồ đếm ngược (10:00).|
| 2. Chuyển ngữ tiếng Việt toàn diện: Chuyển toàn bộ mã tiếng Anh (OUT, IN, RETURN, IN_PROGRESS,     |
|    OPEN, RESOLVED) sang tiếng Việt chuẩn. OUT hiển thị là "Xuất kho thay thế" kèm Ticket ID & User.|
| 3. Vật tư Dashboard: Bỏ nút "Tạo lệnh Nhập kho mới" dư thừa ở Main Content.                        |
| 4. Vật tư Nhập kho: Bố cục 2 cột kèm BẢNG THỐNG KÊ LÔ HÀNG VẬT TƯ & TỒN HIỆN TẠI.                  |
| 5. Quản lý kho: Bỏ "Báo cáo Xuất Nhập Tồn" khỏi Sidebar; nút "Xem Báo cáo Chi tiết" dẫn sang       |
|    Báo cáo có thêm nút "Quay lại trang" về Dashboard.                                              |
| 6. Kỹ thuật viên: Sửa ô tìm kiếm thông minh (ban đầu rỗng, bấm Enter chọn ngay, Đặt lại sạch 100%).|
| 7. CSDL: Mở rộng danh mục từ 7 lên 40 mã linh kiện (+33 linh kiện mới Apple, Samsung, Xiaomi,...). |
+----------------------------------------------------------------------------------------------------+
```

---

### 2. Bảng so sánh chi tiết từng nội dung cải tiến ở Sprint 2 (Bài tập 2)

| STT | Thành Phần / Giao Diện | Trạng Thái Thiết Kế Cũ (Trước Cải Tiến) | Trạng Thái Hiện Thực Mới (Sau Hoàn Thiện `v0.2`) | Tác Động Tới Hệ Thống |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Khung Quên mật khẩu** | Hiển thị thời gian tĩnh `15:00`, người dùng không biết thời gian đang chạy hay dừng. | - Điều chỉnh xuống **10 phút** (`10:00`).<br>- Tích hợp **đồng hồ đếm ngược trực quan từng giây** (`#countdownTimer`).<br>- Khi hết giờ, tự động đổi màu đỏ báo hết hạn và yêu cầu lấy mã mới. | Cải thiện trải nghiệm xác thực an toàn, minh bạch thời gian thực cho người dùng. |
| **2** | **Ngôn từ & Biểu diễn `OUT`** | Giao diện còn hiển thị mã kỹ thuật tiếng Anh (`OUT`, `IN`, `RETURN`, `IN_PROGRESS`, `OPEN`, `RESOLVED`). | - `OUT` → **"Xuất kho thay thế"** (Huy hiệu vàng/cam).<br>- `IN` → **"Nhập kho vật tư"** (Huy hiệu xanh lá).<br>- `RETURN` → **"Hoàn trả linh kiện"** (Huy hiệu xanh dương).<br>- `OPEN` → **"Chờ tiếp nhận"**.<br>- `IN_PROGRESS` → **"Đang xử lý"**.<br>- `RESOLVED` → **"Đã hoàn thành"**.<br>- Sổ cái kiểm toán Audit Log hiển thị rõ phân loại "Xuất kho thay thế", gắn kèm **Ticket ID** và **Người thực hiện**. | Thân thiện người dùng Việt Nam 100%, rõ ràng trách nhiệm kiểm toán. |
| **3** | **Bảng tin Quản lý vật tư** | Main Content có nút *"Tạo lệnh Nhập kho mới"* gây trùng lặp với danh mục trên Sidebar. | Loại bỏ hoàn toàn nút bấm thừa trên Main Content; thay bằng huy hiệu *"Trung tâm Vật tư Quận 1"*. Sidebar giữ danh mục *"Nhập kho linh kiện mới"*. | Giao diện gọn gàng, tránh dư thừa thao tác điều hướng. |
| **4** | **Giao diện Nhập kho mới** | Chỉ có 1 khối form đơn độc chiếm toàn bộ chiều ngang, không nhìn thấy tồn kho hiện tại. | Thiết kế lại **bố cục 2 cột song song (Col 7 - Col 5)**:<br>- Cột trái: Form *"PHIẾU TIẾP NHẬN NHẬP KHO VẬT TƯ"*.<br>- Cột phải: *"BẢNG THỐNG KÊ LÔ HÀNG VẬT TƯ & TỒN HIỆN TẠI"* với danh mục 40 linh kiện và nút *"Chọn"* nhập nhanh. | Nhân viên vật tư vừa nhập vừa đối chiếu số dư tồn kho trực tiếp. |
| **5** | **Sidebar Quản lý kho** | Menu Sidebar có mục *"Báo cáo Xuất Nhập Tồn"*, trong khi Main Dashboard cũng có nút *"Xem Báo cáo Chi tiết"*. | - **Loại bỏ mục Báo cáo Xuất Nhập Tồn khỏi Sidebar** (Sidebar Quản lý chỉ còn: Dashboard, Sổ cái, Nhân sự).<br>- Khi bấm *"Xem Báo cáo Chi tiết"* trên Dashboard sẽ mở giao diện Báo cáo.<br>- Giao diện Báo cáo được bổ sung nút **"Quay lại trang"** (icon `arrow_back`) để trở về Dashboard. | Tối ưu hóa luồng điều hướng nghiệp vụ của cấp Quản lý theo chuẩn Master-Detail. |
| **6** | **Tra cứu & Giao dịch Kỹ thuật** | - Ô tìm kiếm điền sẵn nội dung gây lỗi không tìm thấy khi click/focus.<br>- Khung tồn kho điền sẵn số liệu mặc định.<br>- Không hỗ trợ phím Enter. | - Ô tìm kiếm ban đầu **rỗng**, placeholder hướng dẫn rõ ràng.<br>- Khung tồn kho ban đầu hiển thị: *"Chưa chọn linh kiện..."*.<br>- Dropdown hiển thị *"Không tìm thấy linh kiện phù hợp với từ khóa."* khi không khớp.<br>- **Hỗ trợ phím `Enter`** trên ô tìm kiếm để chọn nhanh. | Khắc phục triệt để vướng mắc thao tác tra cứu trong ca trực thực tế. |
| **7** | **Quy mô Danh mục linh kiện** | Chỉ có 7 linh kiện cơ bản thuộc iPhone 13/14. | Mở rộng lên **40 loại linh kiện** thuộc các dòng: iPhone 13, 14, 15 Pro Max, iPad Pro/Air, MacBook Air/Pro M1/M2/M3, Samsung Galaxy S23/S24/Z Fold, Xiaomi 13/14. | Dữ liệu đa dạng, tiệm cận mô hình chuỗi trung tâm bảo hành thực tế. |
| **8** | **Header Top Bar** | Khung xám `LUỒNG 05: KHO LINH KIỆN`, mã `(L5-WH-890)`, nút "Đăng xuất khỏi hệ thống". | - Loại bỏ khung xám và mã kỹ thuật lộ thiên.<br>- Logo 3D `L5` + `SMART CRM — MEKONG MOBILE` + `Chi nhánh: Quận 1`.<br>- Nút đổi thành **"Đăng xuất tài khoản"**. | Nhận diện thương hiệu sang trọng, đúng ngôn ngữ người dùng cuối. |
| **9** | **Trạng thái Người dùng** | Trạng thái sơ sài, người đăng xuất bị hiểu nhầm là thôi việc. | Phân định rạch ròi 4 trạng thái:<br>- `ONLINE` (Xanh lá)<br>- `AWAY` (Vàng)<br>- `OFF_SHIFT` (Cam - Đăng xuất sau ca, mai làm lại)<br>- `TERMINATED` (Đỏ sẫm - Đã thôi việc vĩnh viễn, khóa HTTP 403). | Quản trị nhân sự chặt chẽ, an toàn bảo mật phân quyền cấp cao. |
| **10** | **Quy chuẩn Mật khẩu** | Bảng checklist 4 tiêu chí hiện thô trên màn hình gây rối mắt. | Ẩn mặc định (class `hidden`), chỉ xuất hiện dòng báo lỗi đỏ khi người dùng nhập sai quy chuẩn 8 ký tự (Hoa, thường, số, ký hiệu). Thêm nút con mắt bật/tắt mật khẩu. | Giao diện hiện đại, tinh tế, chuẩn UX công nghiệp. |
| **11** | **Tối giản nút Tra cứu & Nút Đặt lại biểu mẫu** | Phải bấm nút "Tra cứu" thủ công; khi bấm "Đặt lại biểu mẫu" vẫn còn lưu thông tin cũ. | - **Loại bỏ hoàn toàn nút "Tra cứu"** khỏi form xuất linh kiện; gõ từ khóa hiện gợi ý và bấm `Enter` chọn ngay.<br>- **Nút "Đặt lại biểu mẫu" khôi phục sạch sẽ 100%:** Xóa trắng ô tìm kiếm, đưa khung tồn kho về *"Chưa chọn linh kiện"*, xóa mã phiếu, đưa số lượng về `1` và xóa toàn bộ dòng báo lỗi đỏ. | Thao tác mượt mà, tối giản hành vi người dùng, biểu mẫu luôn minh bạch. |
| **12** | **Tinh gọn nút Quay lại trang ở Sổ cái & Nhân sự** | Giao diện Sổ cái Nhật ký và Quản lý nhân sự có nút "Quay lại trang" dư thừa vì đã nằm sẵn trên Sidebar. | - **Loại bỏ nút "Quay lại trang"** ở cả hai giao diện Nhật ký Giao dịch Kho và Quản lý nhân sự.<br>- Chỉ duy trì duy nhất nút "Quay lại trang" tại **Báo cáo Xuất Nhập Tồn** để Quản lý kho quay về Dashboard Tổng quan. | Cấu trúc điều hướng nhất quán, không trùng lặp lối đi. |
| **13** | **Loại trừ triệt để chuỗi `undefined`** | Một số thuộc tính thiếu giá trị có nguy cơ hiển thị chuỗi `undefined` trên giao diện người dùng. | Tích hợp cơ chế Fallback an toàn 100% bằng tiếng Việt chuẩn cho tất cả các trường dữ liệu (`Mã LK`, `Linh kiện thay thế`, `Họ tên`,...). | Giao diện chuyên nghiệp, sạch sẽ, không có lỗi hiển thị thô. |

---

### 3. Chi tiết thay đổi theo từng tầng kiến trúc mã nguồn

#### A. Tầng Frontend (SPA JavaScript & Dark 3D CSS)
- **[src/static/app.js](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/src/static/app.js):**
  - Thêm biến toàn cục `otpCountdownInterval` và hàm `startOtpCountdown(600)` đếm ngược từng giây từ `10:00` về `00:00`.
  - Hiện thực 2 hàm tiện ích chuyển ngữ tiếng Việt: `formatTicketStatus()` và `formatTransactionType()`.
  - Cập nhật `renderMaterialDashboard()`: Bỏ nút *"Tạo lệnh Nhập kho mới"* trùng lặp.
  - Cập nhật `renderMaterialStockIn()`: Tái cấu trúc thành lưới 2 cột song song, bổ sung hàm `selectPartForStockIn()`.
  - Cập nhật `renderSidebarNav()`: Loại bỏ `manager_reports` khỏi menu `MANAGER`.
  - Cập nhật `renderManagerReports()`: Thêm nút `<button onclick="navigateToTab('manager_dashboard')">Quay lại trang</button>`.
  - Cập nhật `renderTechTransaction()`: Khởi tạo ô tìm kiếm rỗng, xử lý `handleSmartSearchKeyDown()`, `executeSmartLookup()`, `selectPartForTransaction()` và `resetTechTransactionForm()`.
- **[src/static/index.html](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/src/static/index.html):**
  - Cập nhật nhãn đếm ngược `#countdownTimer` thành `10:00`.
  - Tích hợp nút con mắt `.eye-toggle-btn` tại cả 3 biểu mẫu xác thực (`Login`, `Register`, `Reset Password`).
- **[src/static/styles.css](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/src/static/styles.css):**
  - Bổ sung hệ thống Design Tokens Dark 3D (`.card-3d`, `.btn-3d-primary`), hiệu ứng viền phát sáng và 4 lớp huy hiệu trạng thái ngữ nghĩa.

#### B. Tầng Backend (Python FastAPI)
- **[src/routes/inventory.routes.py](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/src/routes/inventory.routes.py):**
  - Endpoint `POST /api/v1/auth/forgot-password`: Đặt thời hạn OTP chuẩn `timedelta(minutes=10)`.
  - Endpoint `POST /api/v1/auth/login` & `POST /api/v1/auth/logout`: Chặn tài khoản `TERMINATED` (HTTP 403 `ERR_ACCOUNT_TERMINATED`) và chuyển trạng thái `OFF_SHIFT` khi đăng xuất an toàn.
  - Endpoint `GET /api/v1/inventory/parts` & `POST /api/v1/inventory/transactions`: Phục vụ danh mục 40 linh kiện và xử lý giao dịch Nhập/Xuất/Hoàn kho nguyên tử.
- **[src/validators/inventory.validator.py](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/src/validators/inventory.validator.py):**
  - Kiểm định bắt buộc `ticket_id` khi `OUT`/`RETURN` (`BR-02`), giới hạn biên dữ liệu và độ phức tạp mật khẩu 4 nhóm ký tự.

#### C. Tầng Database & Đóng gói Hệ thống (MongoDB Atlas, Data Seeds & Docker)
- **[migrations/001_create_collections.js](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/migrations/001_create_collections.js) & [migrations/002_create_indexes.js](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/migrations/002_create_indexes.js):**
  - Đồng bộ 100% cấu trúc 6 Collections NoSQL (`service_center`, `part`, `ticket`, `part_stock`, `part_transaction`, `users`) kèm `$jsonSchema` và Compound Indexes (`idx_stock_lookup`, `idx_transaction_history`).
- **[seeds/001_seed_parts_demo.json](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/seeds/001_seed_parts_demo.json) & [data/users_store.json](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/data/users_store.json):**
  - Mở rộng lên 40 linh kiện và 75 bản ghi tồn kho chi nhánh; duy trì bền vững 4 trạng thái tài khoản nhân sự.
- **[Dockerfile](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/Dockerfile) & [docker-compose.yml](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docker-compose.yml):**
  - Đóng gói trọn vẹn ứng dụng Backend + Frontend SPA + MongoDB 7.0 giúp tái tạo hệ thống tức thì bằng 1 lệnh duy nhất (`NFR-01`).

---

## 4. Kết luận và đánh giá tính toàn vẹn sau thay đổi
Toàn bộ **5 hạng mục điều chỉnh thiết kế Bài tập 1 sau phản hồi của Giảng viên (`TD-01` → `TD-05`)** và **các cải tiến thực nghiệm trong Bài tập 2 (Sprint 2)** đã được đồng bộ xuyên suốt từ tài liệu đặc tả ([srs.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/srs.md), [thietke.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/thietke.md), [api-contract.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/api-contract.md), sơ đồ `.drawio`) đến mã nguồn thực thi và bộ kiểm thử tự động (**43/43 Test Cases PASSED 100%**, không phát sinh lỗi hồi quy).


---

## PHẦN III: Nhật ký thay đổi và hoàn thiện hệ thống ở Bài tập 3 (Kiểm thử, Bảo mật & Đóng gói)

Giai đoạn Bài tập 3 tập trung vào việc biến hệ thống từ mức hiện thực hóa ở Bài tập 2 thành sản phẩm bàn giao hoàn chỉnh đạt chuẩn kiểm chứng thực tế và đóng gói tái lập:

### Bảng tóm tắt các cải tiến kỹ thuật trong Bài tập 3:

| STT | Hạng mục cải tiến | Trạng thái ở BT2 | Cải tiến hoàn thiện ở BT3 | Căn cứ đánh giá BT3 |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **Bảo mật lưu trữ mật khẩu (S3)** | Tài khoản đăng ký còn lưu trường `password` dạng thô trong CSDL và RAM. | Loại bỏ 100% trường `password` thô; chỉ lưu duy nhất `password_hash` (Bcrypt / SHA-256); xóa sạch secret khỏi kho mã nguồn. | Tiêu chí kỹ thuật `[SE] S3` & Checklist bảo mật mục 4. |
| **2** | **Xác thực thời hạn OTP** | API Backend chưa kiểm tra thời hạn `otp_expires_at` của OTP khi gọi `/verify-otp`. | Bổ sung kiểm tra `datetime.utcnow() > exp_dt` ném mã lỗi HTTP 400 `ERR_OTP_EXPIRED`. | Tiêu chí kỹ thuật `S2` & Luồng khôi phục an toàn. |
| **3** | **Đóng gói Docker Compose (C1)** | MongoDB container thiếu healthcheck; chưa tự động chạy seed khi dựng từ máy trắng. | Bổ sung healthcheck `mongosh --eval 'db.adminCommand("ping")'`, tự động chạy `seeds/seed.py` khi khởi động container; hệ thống lên bằng đúng $\le 2$ lệnh. | Tiêu chí Cốt lõi `C1` & Phép thử máy trắng. |
| **4** | **Kiểm thử tự động đa tầng (C2, C3)** | Có 43 test cases tập trung vào luồng chính và giao diện. | Mở rộng lên **56 test cases** tự động; bổ sung đầy đủ test biên 2 bên ranh giới (`BR-01`, `BR-05`), test hoàn trả (`RETURN`), test xung đột đồng thời (*Optimistic Locking*), test lũy đẳng nạp seed (`C8`). | Tiêu chí Cốt lõi `C2, C3` & Rubric 4.2. |
| **5** | **Ghim phiên bản phụ thuộc** | Tệp `requirements.txt` dùng toán tử `>=`. | Ghim chặt 100% phiên bản thư viện bằng toán tử `==` (`fastapi==0.162.0`, `pymongo==4.19.0`, v.v.). | Mục 3.2 Đề bài BT3 & Checklist bảo mật mục 7. |
| **6** | **Tài liệu bàn giao tiếng Anh** | Tài liệu chủ yếu bằng tiếng Việt. | Biên soạn trọn bộ `deployment-guide.md` và `api-docs/README.md` bằng tiếng Anh chuẩn mực kỹ thuật. | Tiêu chí CLO4 & Mục 2.5, 2.6 BT3. |
| **7** | **Dọn dẹp và tinh gọn thư mục Frontend** | Tồn tại các thư mục con rỗng `frontend/src/pages/Manager`, `Material`, `Tech` và `frontend/public/images` gây nhầm lẫn về cấu trúc phân quyền và vị trí file. | Xóa bỏ hoàn toàn các thư mục con rỗng thừa; đưa trực tiếp `AuthPortal.js` và `ManagerUsers.js` ra `frontend/src/pages/`. Toàn bộ giao diện 3 vai trò chạy tập trung và đồng bộ qua kiến trúc SPA (`src/static/app.js` và `frontend/public/app.js`). | Chuẩn hóa cấu trúc thư mục sạch, loại bỏ mã thừa, tăng tính bảo trì dự án. |
| **8** | **Nguyên tắc 1 tài khoản - 1 vai trò duy nhất (RBAC)** | Tài khoản thử nghiệm dùng chung hoặc thiếu tài khoản chuyên biệt cho từng vai trò riêng biệt. | Thiết lập quy định bất biến: Mỗi tài khoản email chỉ được cấp đúng 1 vai trò duy nhất (`MATERIAL_STAFF`, `TECH_STAFF`, hoặc `MANAGER`). Nạp sẵn 3 tài khoản chuẩn mực độc lập tương ứng với 3 vai trò vào CSDL và hệ thống seed. | Bảo mật phân quyền RBAC, kiểm toán trách nhiệm pháp lý và truy vết giao dịch. |

---

## PHẦN IV: Phản hồi của Giảng viên về Bài tập 2 & Các hành động khắc phục hoàn thiện

### 1. Chi tiết nhận xét đánh giá Bài tập 2 từ Giảng viên hướng dẫn (TS. Nguyễn Trí Hải)
- **Sinh viên:** Huỳnh Nguyễn Bảo Ngọc – MSSV: `2374802010339`
- **Luồng:** Luồng 05 – Kho linh kiện thay thế | **Track:** Software Engineering (`SE`)
- **Điểm mạnh ghi nhận:**
  - Kiến trúc FastAPI tách 3 lớp rõ ràng (Routes, Services, Repositories).
  - Hiện thực nhiều quy tắc nghiệp vụ kho chặt chẽ: Bắt buộc chứng từ phiếu bảo hành khi xuất kho (`BR-02`), ngưỡng an toàn (`BR-05`), giao dịch nguyên tử, nhật ký đối soát bất biến insert-only (`BR-03`).
  - Toàn bộ kiểm thử tự động PASS 100%.
  - Giao diện có đầy đủ 3 trạng thái dữ liệu (Loading, Empty, Error) kèm ảnh chụp minh chứng.
  - Đóng gói Docker Compose chạy được ngay từ máy trắng.
- **Các điểm cần khắc phục & Mục kiểm chứng chưa đạt:**
  1. *Báo cáo 81 trang chủ yếu là dán mã nguồn, không theo cấu trúc 7 mục (gợi ý 6–9 trang), mục lục còn lỗi "Error! Bookmark not defined".*
  2. *Tag `v0.2` đang trỏ vào commit BT3 làm sau ngày nộp (lần này thầy chấp nhận chấm theo main) — lần sau tag phải giữ đúng bản đã nộp.*
  3. *API chưa đủ bốn thao tác CRUD (không có thao tác xóa DELETE).*
  4. *Mục kiểm chứng (Bảng 4.2) chưa đạt: Tiêu chí `[SE] S1` ("$\ge 2$ thực thể có đủ bốn thao tác CRUD").*

---

### 2. Kế hoạch & Kết quả khắc phục toàn diện

| STT | Vấn đề phản hồi | Hành động khắc phục chi tiết | Kết quả & Minh chứng kỹ thuật |
| :---: | :--- | :--- | :--- |
| **KH-01** | **Git Tag `v0.2` trỏ sai commit** | Điều chỉnh con trỏ git tag `v0.2` quay về đúng commit nộp thực tế ngày 29/10/2026: `e6698d5` (`feat(bt2): complete core module, layered clean architecture, docs, docker & 43 automated tests (v0.2)`). | Thực thi lệnh `git tag -f -a v0.2 e6698d5 -m "..."` và `git push -f origin v0.2`. Kiểm chứng bằng `git show v0.2` xác nhận trỏ đúng commit ngày 29/10/2026. Tag được giữ bất biến. |
| **KH-02** | **Thiếu CRUD & Thao tác Xóa (Tiêu chí `[SE] S1`)** | Hiện thực đầy đủ cả 4 thao tác CRUD (**C**reate, **R**ead, **U**pdate, **D**elete) cho **2 thực thể cốt lõi**: <br>1. Thực thể `part` (Linh kiện kho)<br>2. Thực thể `users` (Tài khoản nhân sự). | - `part`: `POST /parts`, `GET /parts/{code}`, `PUT /parts/{code}`, `DELETE /parts/{code}`.<br>- `users`: `POST /users`, `GET /users/{email}`, `PUT /users/{email}`, `DELETE /users/{email}`.<br>- Bổ sung đầy đủ ràng buộc an toàn (không xóa khi còn tồn kho > 0, không tự xóa tài khoản của chính mình). |
| **KH-03** | **Kiểm chứng tự động cho Tiêu chí S1** | Xây dựng bộ test suite mới `tests/se_s1_crud.test.py` gồm 11 test cases kiểm thử tự động toàn diện cho cả 2 thực thể. | Kiểm thử tự động 11/11 tests PASS 100%. Nâng tổng bộ kiểm thử toàn hệ thống lên **67 test cases PASS 100%** bằng 1 lệnh `pytest tests/ -v`. |
| **KH-04** | **Báo cáo BT2 quá dài (81 trang) và lỗi mục lục** | Tái cấu trúc toàn bộ Báo cáo BT2 thành tài liệu khoa học cô đọng chuẩn 7 mục (khuyến nghị 6–9 trang theo Mục 3.1 Đề bài BT2). Lược bỏ toàn bộ mã nguồn thô; thay thế bằng sơ đồ, bảng biểu đối chiếu và trích đoạn giải thuật ngắn gọn. Sửa triệt để lỗi Word `Error! Bookmark not defined`. | Báo cáo đạt chuẩn 8 trang, mục lục cập nhật đúng số trang tự động, đầy đủ trang bìa, 7 mục chuẩn và Phụ lục AI. Lưu tại `docs/BT2_BaoCao_Chuan7Muc.md` và file Word `.docx` tương ứng. |
| **KH-05** | **Đồng bộ OpenAPI & Tài liệu API** | Tự động xuất schema OpenAPI mới nhất ra [docs/api-docs/openapi.json](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/api-docs/openapi.json) (22 endpoints) và cập nhật bảng tra cứu trong [docs/api-docs/README.md](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/api-docs/README.md). | Swagger UI (`/docs`) và OpenAPI JSON phản ánh chính xác các endpoints CRUD mới bổ sung. |


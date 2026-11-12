# RESTFUL API SPECIFICATION & TECHNICAL DOCUMENTATION
## SMART CRM – MEKONG MOBILE (FLOW 05: SPARE PARTS INVENTORY)
### Track: Software Engineering (`SE`) — Assignment 3 Deliverable

- **API Base URL:** `http://localhost:8000/api/v1`
- **Interactive OpenAPI Documentation:** `http://localhost:8000/docs` (Swagger UI) & `http://localhost:8000/redoc` (ReDoc)
- **JSON Specification File:** [docs/api-docs/openapi.json](file:///d:/Hoc/DH/N4/N4.HK01/Chuyende1/CDTN01/docs/api-docs/openapi.json)
- **Repository:** https://github.com/Johnny120905/cdtn01_HuynhNguyenBaoNgoc_L5.git

---

## 1. Authentication & Security Architecture
All protected endpoints require an HTTP `Authorization` header containing a valid Bearer JSON Web Token (JWT):
```http
Authorization: Bearer <JWT_TOKEN>
```
The token payload encapsulates `email`, `role` (`TECH_STAFF` | `MATERIAL_STAFF` | `MANAGER`), `center_id` (`L5-WH-890`), and expiration time `exp` (24 hours).

---

## 2. Comprehensive Endpoint Index

| Method | Path | Summary & Business Role | Required Role |
| :---: | :--- | :--- | :---: |
| `POST` | `/api/v1/auth/register` | Register new user account and assign professional role | Public |
| `POST` | `/api/v1/auth/login` | Authenticate user, verify password hash, issue JWT | Public |
| `POST` | `/api/v1/auth/logout` | Terminate session, update status to `OFF_SHIFT` | Authenticated |
| `POST` | `/api/v1/auth/forgot-password` | Generate 6-digit OTP with 10-minute expiry | Public |
| `POST` | `/api/v1/auth/verify-otp` | Verify 6-digit OTP code against expiry timestamp | Public |
| `POST` | `/api/v1/auth/reset-password` | Reset account password with validated OTP | Public |
| `GET` | `/api/v1/inventory/stock/{part_code}` | Query real-time physical stock and threshold flag | `TECH_STAFF`, `MANAGER` |
| `GET` | `/api/v1/inventory/stock` | Query entire stock catalog for current branch | Authenticated |
| `POST` | `/api/v1/inventory/transactions` | Execute atomic stock transaction (`OUT`, `IN`, `RETURN`) | Role-specific |
| `PUT` | `/api/v1/inventory/parts/{part_code}/threshold` | Configure safety threshold `min_threshold` | `MANAGER` only |
| `GET` | `/api/v1/inventory/parts` | Retrieve spare parts catalog metadata (CRUD: Read All) | Authenticated |
| `POST` | `/api/v1/inventory/parts` | [SE S1] Create new spare part entry (CRUD: Create) | `MANAGER`, `MATERIAL` |
| `GET` | `/api/v1/inventory/parts/{part_code}` | [SE S1] Retrieve spare part details by code (CRUD: Read Detail) | Authenticated |
| `PUT` | `/api/v1/inventory/parts/{part_code}` | [SE S1] Update spare part metadata (CRUD: Update) | `MANAGER`, `MATERIAL` |
| `DELETE` | `/api/v1/inventory/parts/{part_code}` | [SE S1] Delete spare part entry (CRUD: Delete, Guard: Stock=0) | `MANAGER` only |
| `GET` | `/api/v1/inventory/users` | Retrieve all personnel records | `MANAGER` only |
| `POST` | `/api/v1/inventory/users` | [SE S1] Create new personnel account (CRUD: Create) | `MANAGER` only |
| `GET` | `/api/v1/inventory/users/{email}` | [SE S1] Retrieve personnel profile by email (CRUD: Read Detail) | `MANAGER` / Owner |
| `PUT` | `/api/v1/inventory/users/{email}` | [SE S1] Update personnel profile (CRUD: Update) | `MANAGER` only |
| `DELETE` | `/api/v1/inventory/users/{email}` | [SE S1] Delete personnel account (CRUD: Delete, Guard: Not Self) | `MANAGER` only |
| `GET` | `/api/v1/inventory/alerts/threshold` | List spare parts below minimum safety threshold | `MANAGER`, `MATERIAL` |
| `GET` | `/api/v1/inventory/transactions` | Query immutable audit log records (limit=50) | `MANAGER`, `TECH` |
| `GET` | `/api/v1/inventory/tickets` | Query active repair tickets (`OPEN`, `IN_PROGRESS`) | Authenticated |
| `GET` | `/api/v1/inventory/dashboard` | Aggregated KPI metrics for branch management | Authenticated |
| `GET` | `/api/v1/inventory/users/subordinates` | List branch technical and material staff | `MANAGER` only |
| `POST` | `/api/v1/inventory/users/import` | Bulk import subordinate personnel from JSON/CSV | `MANAGER` only |

---

## 3. Detailed Endpoint Specifications (7 Mandatory Sections Per Endpoint)

### 3.1. GET `/api/v1/inventory/stock/{part_code}`
1. **Method & Path:** `GET /api/v1/inventory/stock/{part_code}`
2. **Business Description:** Retrieves the instantaneous physical inventory quantity of a spare part for the user's assigned branch (`BR-04`), evaluating real-time safety threshold status (`BR-05`).
3. **Authentication:** Bearer JWT required.
4. **Parameters:**
   - Path parameter: `part_code` (string, max 30 chars, required). Example: `SCR-IP14-01`.
5. **Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "center_id": "L5-WH-890",
    "part_code": "SCR-IP14-01",
    "part_name": "Màn hình OLED iPhone 14 Pro Max",
    "category": "Màn hình",
    "price": 3200000.0,
    "quantity": 12,
    "min_threshold": 15,
    "status_flag": "WARNING"
  }
}
```
6. **Error Codes Table:**
   - `400 ERR_INVALID_INPUT`: Part code is empty or malformed.
   - `401 ERR_INVALID_TOKEN`: Missing or expired Bearer token.
   - `403 ERR_UNAUTHORIZED_CENTER`: User attempting to query cross-center data (`A01 OWASP`).
   - `404 ERR_RESOURCE_NOT_FOUND`: Part code does not exist in master catalog.
7. **Constraints & Limits:** Indexed via `{center_id: 1, part_code: 1}` ensuring response time $< 500$ ms (`NFR-02`).

---

### 3.2. POST `/api/v1/inventory/transactions`
1. **Method & Path:** `POST /api/v1/inventory/transactions`
2. **Business Description:** Records an atomic inventory transaction (`OUT` for repair, `IN` for restocking, `RETURN` for spare returns). Implements non-negative stock deduction (`BR-01`), mandatory ticket enforcement (`BR-02`), immutable audit logging (`BR-03`), and Optimistic Locking concurrency protection (`NFR-03` / `EX-05`).
3. **Authentication:** Bearer JWT required.
4. **Request Body:**
```json
{
  "part_code": "SCR-IP14-01",
  "type": "OUT",
  "quantity": 1,
  "ticket_id": "TK-1092"
}
```
5. **Success Response (201 Created):**
```json
{
  "status": "success",
  "message": "Giao dịch thành công, số dư kho đã được cập nhật.",
  "data": {
    "transaction_id": 884920,
    "created_at": "2026-10-30T00:15:22.105Z"
  }
}
```
6. **Error Codes Table:**
   - `400 ERR_INSUFFICIENT_STOCK`: Requested quantity exceeds available physical stock (`BR-01`).
   - `400 ERR_INVALID_QUANTITY`: Quantity is $\le 0$ or non-integer.
   - `403 ERR_FORBIDDEN_ACTION`: Material staff attempting `OUT` or Tech staff attempting `IN`.
   - `409 ERR_CONCURRENT_UPDATE`: Optimistic locking version conflict detected (`EX-05`).
   - `422 ERR_INVALID_TICKET`: Missing ticket or ticket is in `COMPLETED`/`CANCELLED` state (`BR-02` / `UC-99`).
7. **Constraints & Limits:** Quantity limit: $1 \le Q \le 1,000,000$. Ticket ID max length: 30 chars.

---

### 3.3. PUT `/api/v1/inventory/parts/{part_code}/threshold`
1. **Method & Path:** `PUT /api/v1/inventory/parts/{part_code}/threshold`
2. **Business Description:** Modifies the minimum safety threshold level (`min_threshold`) for an inventory item. Restricted strictly to Inventory Managers (`MANAGER`).
3. **Authentication:** Bearer JWT required (Role must be `MANAGER`).
4. **Request Body:**
```json
{
  "min_threshold": 20
}
```
5. **Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Đã cập nhật ngưỡng an toàn thành 20 cái."
}
```
6. **Error Codes Table:**
   - `400 ERR_INVALID_THRESHOLD`: Threshold is $< 0$ or $> 100,000$.
   - `403 ERR_UNAUTHORIZED_ROLE`: Non-manager role attempting modification.
   - `404 ERR_RESOURCE_NOT_FOUND`: Part code does not exist.
7. **Constraints & Limits:** $0 \le min\_threshold \le 100,000$.

---

### 3.4. [SE S1] Spare Parts Catalog CRUD (`/api/v1/inventory/parts`)
1. **POST `/api/v1/inventory/parts` (Create):** Thêm mới linh kiện vào danh mục. Yêu cầu quyền `MANAGER` hoặc `MATERIAL_STAFF`.
   - Body: `{"part_code": "PRT-...", "part_name": "...", "min_threshold": 10, ...}`
   - Trả về 201 Created kèm dữ liệu linh kiện mới tạo.
2. **GET `/api/v1/inventory/parts/{part_code}` (Read Detail):** Tra cứu thông tin linh kiện theo mã. Trả về 200 OK hoặc 404.
3. **PUT `/api/v1/inventory/parts/{part_code}` (Update):** Cập nhật tên, danh mục, model tương thích, nhà cung cấp, ngưỡng an toàn. Yêu cầu quyền `MANAGER` hoặc `MATERIAL_STAFF`.
   - Trả về 200 OK kèm thông tin đã cập nhật.
4. **DELETE `/api/v1/inventory/parts/{part_code}` (Delete):** Xóa linh kiện khỏi danh mục. Yêu cầu quyền `MANAGER`.
   - Ràng buộc an toàn: Nếu linh kiện vẫn còn tồn kho thực tế > 0 thì từ chối với lỗi 400 `ERR_CANNOT_DELETE_ACTIVE_STOCK`.
   - Trả về 200 OK sau khi xóa thành công.

---

### 3.5. [SE S1] Personnel Accounts CRUD (`/api/v1/inventory/users`)
1. **POST `/api/v1/inventory/users` (Create):** Quản lý kho tạo mới tài khoản nhân sự cấp dưới. Yêu cầu quyền `MANAGER`.
   - Body: `{"full_name": "...", "email": "...", "password": "...", "role": "TECH_STAFF"|"MATERIAL_STAFF"}`
   - Trả về 201 Created (tự động băm SHA-256 mật khẩu, không trả về password_hash - Tiêu chí S3).
2. **GET `/api/v1/inventory/users/{email}` (Read Detail):** Tra cứu hồ sơ nhân sự theo email. Yêu cầu quyền `MANAGER` hoặc chủ tài khoản. Trả về 200 OK.
3. **PUT `/api/v1/inventory/users/{email}` (Update):** Cập nhật thông tin nhân sự (`full_name`, `phone`, `role`, `status`). Yêu cầu quyền `MANAGER`. Trả về 200 OK.
4. **DELETE `/api/v1/inventory/users/{email}` (Delete):** Xóa tài khoản nhân sự. Yêu cầu quyền `MANAGER`.
   - Ràng buộc an toàn: Quản lý không được phép tự xóa tài khoản của chính mình (lỗi 400 `ERR_CANNOT_DELETE_SELF`).
   - Trả về 200 OK sau khi xóa thành công.


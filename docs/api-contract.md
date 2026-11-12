# TÀI LIỆU ĐẶC TẢ API (API CONTRACT)
**Dự án:** Smart CRM - Mekong Mobile 
**Phân hệ:** Luồng L5 - Quản lý Kho linh kiện
**Phiên bản:** 1.0.0

---

## 1. Cấu hình chung (General Configuration)
- **Base URL:** `https://api.mekongmobile.vn/api/v1/inventory`
- **Authentication:** Yêu cầu gửi kèm header `Authorization: Bearer <JWT_Token>` trong mọi request. Token chứa thông tin `user_id`, `role`, và `center_id` (Phân mảnh dữ liệu theo BR-04).
- **Định dạng dữ liệu:** `application/json`
- **Yêu cầu hiệu năng:** Mọi API truy vấn phải trả về kết quả trong thời gian `< 500ms` (Tuân thủ NFR-02).

---

## 2. Danh sách API cốt lõi

### API 1: Tra cứu Tồn kho Linh kiện
- **Mô tả:** Lấy thông tin số lượng tồn kho thực tế của một linh kiện tại trung tâm hiện tại (Phục vụ FR-04 & UC-04).
- **Method:** `GET`
- **Endpoint:** `/stock/{part_code}`
- **Path Variables:**
  - `part_code` (string): Mã linh kiện (VD: `SCR-IP14-01`).

**Response - Thành công (200 OK):**
```json
{
  "status": "success",
  "data": {
    "center_id": "L5-WH-890",
    "part_code": "SCR-IP14-01",
    "part_name": "Màn hình iPhone 14 Pro Max",
    "quantity": 12,
    "min_threshold": 15,
    "status_flag": "WARNING" 
  }
}
```
*(Ghi chú: Trả về `status_flag` là WARNING do quantity <= min_threshold, kích hoạt tính năng cảnh báo FR-07).*

---

### API 2: Ghi nhận Giao dịch Kho (Xuất / Nhập / Hoàn trả)
- **Mô tả:** Tạo một giao dịch làm biến động số lượng tồn kho (Phục vụ FR-01, FR-02, FR-03).
- **Method:** `POST`
- **Endpoint:** `/transactions`
- **Request Body:**
```json
{
  "part_code": "SCR-IP14-01",
  "type": "OUT",
  "quantity": 1,
  "ticket_id": "TK-2026-8892"
}
```
- **Ràng buộc Dữ liệu (Payload Constraints):**
  - `type`: Chỉ chấp nhận các giá trị `IN`, `OUT`, `RETURN`.
  - `quantity`: Phải là số nguyên dương `> 0`.
  - `ticket_id`: Bắt buộc nếu `type` là `OUT` hoặc `RETURN` (Tuân thủ BR-02).

**Response - Thành công (201 Created):**
```json
{
  "status": "success",
  "message": "Giao dịch thành công, số dư kho đã được cập nhật.",
  "data": {
    "transaction_id": 884920,
    "created_at": "2026-10-27T10:42:15Z"
  }
}
```

**Response - Lỗi Ngoại lệ (400 Bad Request):**
```json
{
  "error_code": "ERR_NEGATIVE_STOCK",
  "message": "Số lượng xuất vượt quá tồn kho thực tế. Giao dịch bị từ chối."
}
```
*(Ghi chú: Đánh chặn theo quy tắc nghiệp vụ BR-01: Tồn kho không âm).*

**Response - Lỗi Ngoại lệ (422 Unprocessable Entity):**
```json
{
  "error_code": "ERR_INVALID_TICKET",
  "message": "Mã phiếu bảo hành không tồn tại hoặc đã đóng."
}
```

---

### API 3: Cập nhật Ngưỡng An toàn
- **Mô tả:** Thiết lập lại số lượng tối thiểu trước khi báo động đỏ cho một linh kiện (Phục vụ FR-06). Quyền này chỉ dành cho Quản lý kho (ACT-03).
- **Method:** `PUT`
- **Endpoint:** `/parts/{part_code}/threshold`
- **Request Body:**
```json
{
  "min_threshold": 10
}
```

**Response - Thành công (200 OK):**
```json
{
  "status": "success",
  "message": "Đã cập nhật ngưỡng an toàn thành 10 cái."
}
```

**Response - Lỗi Phân quyền (403 Forbidden):**
```json
{
  "error_code": "ERR_UNAUTHORIZED_ROLE",
  "message": "Tài khoản của bạn không có quyền sửa đổi thông số này."
}
```

---

### API 4: Xác thực & Cấp quyền (Auth Endpoints)
- **Mô tả:** Đăng ký, Đăng nhập cấp Bearer JWT Token 24h, Quên mật khẩu và Đặt lại mật khẩu bằng mã OTP 10 phút.

#### 4.1. Đăng nhập hệ thống (Login)
- **Method:** `POST`
- **Endpoint:** `/auth/login`
- **Request Body:**
```json
{
  "email": "kythuat.test@gmail.com",
  "password": "Password123@"
}
```
- **Response - Thành công (200 OK):**
```json
{
  "status": "success",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "email": "kythuat.test@gmail.com",
    "full_name": "Kỹ thuật viên Test",
    "role": "TECH_STAFF",
    "center_id": "L5-WH-890"
  }
}
```

#### 4.2. Quên mật khẩu & Gửi mã OTP (Forgot Password)
- **Method:** `POST`
- **Endpoint:** `/auth/forgot-password`
- **Request Body:** `{"email": "kythuat.test@gmail.com"}`
- **Response (200 OK):** `{"status": "success", "message": "Mã OTP đã được tạo, hiệu lực trong 10 phút."}`

#### 4.3. Đặt lại mật khẩu với OTP (Reset Password)
- **Method:** `POST`
- **Endpoint:** `/auth/reset-password`
- **Request Body:**
```json
{
  "email": "kythuat.test@gmail.com",
  "otp": "123456",
  "new_password": "NewPassword123@"
}
```
- **Response (200 OK):** `{"status": "success", "message": "Mật khẩu đã được cập nhật thành công."}`
- **Lỗi hết hạn OTP (400 Bad Request):** `{"error_code": "ERR_OTP_EXPIRED", "message": "Mã OTP đã hết thời gian hiệu lực 10 phút."}`

---

### API 5: Quản lý Danh mục Linh kiện (CRUD Part — Tiêu chí [SE] S1)
- **Mô tả:** Đáp ứng đầy đủ 4 thao tác CRUD (**C**reate, **R**ead, **U**pdate, **D**elete) cho thực thể `part` với ràng buộc an toàn: Không cho phép xóa linh kiện nếu còn tồn kho $> 0$.

| Thao tác | Method | Endpoint Path | Quyền (RBAC) | Mô tả & Ràng buộc bảo vệ |
| :---: | :---: | :--- | :---: | :--- |
| **Create** | `POST` | `/parts` | `MANAGER`, `MATERIAL` | Tạo linh kiện mới vào danh mục (`part_code` duy nhất, `cost_price > 0`). |
| **Read (All)** | `GET` | `/parts` | Mọi vai trò | Lấy toàn bộ danh mục 40 linh kiện kèm thông tin danh mục, đơn giá. |
| **Read (Detail)**| `GET` | `/parts/{part_code}` | Mọi vai trò | Xem chi tiết 1 linh kiện theo mã `part_code`. |
| **Update** | `PUT` | `/parts/{part_code}` | `MANAGER`, `MATERIAL` | Cập nhật thông tin linh kiện (tên, giá bán, danh mục, trạng thái). |
| **Delete** | `DELETE`| `/parts/{part_code}` | `MANAGER` | **Xóa an toàn:** Bị chặn với HTTP 400 `ERR_CANNOT_DELETE_ACTIVE_STOCK` nếu tồn kho $> 0$; chỉ xóa khi tồn kho $= 0$. |

---

### API 6: Quản trị Tài khoản Nhân sự (CRUD User — Tiêu chí [SE] S1)
- **Mô tả:** Đáp ứng đầy đủ 4 thao tác CRUD cho thực thể `users` với ràng buộc an toàn: Quản lý không được phép tự xóa tài khoản của chính mình.

| Thao tác | Method | Endpoint Path | Quyền (RBAC) | Mô tả & Ràng buộc bảo vệ |
| :---: | :---: | :--- | :---: | :--- |
| **Create** | `POST` | `/users` | `MANAGER` | Tạo tài khoản nhân sự mới (`email` duy nhất, mật khẩu 4 nhóm ký tự băm Bcrypt). |
| **Read (All)** | `GET` | `/users` | `MANAGER` | Xem danh sách toàn bộ nhân sự trong chi nhánh. |
| **Read (Detail)**| `GET` | `/users/{email}` | `MANAGER` / Chính chủ | Xem hồ sơ chi tiết người dùng. |
| **Update** | `PUT` | `/users/{email}` | `MANAGER` | Cập nhật thông tin nhân viên (họ tên, vai trò, trạng thái `ACTIVE`/`OFF_SHIFT`/`TERMINATED`). |
| **Delete** | `DELETE`| `/users/{email}` | `MANAGER` | **Xóa an toàn:** Bị chặn với HTTP 400 `ERR_CANNOT_DELETE_SELF` nếu email trùng người đang đăng nhập. |

---

### API 7: Báo cáo & Cảnh báo Ngưỡng Tồn kho (Low Stock Alerts)
- **Method:** `GET`
- **Endpoint:** `/alerts/threshold`
- **Mô tả:** Trả về danh sách tất cả các linh kiện có số lượng tồn kho khả dụng chạm hoặc dưới ngưỡng an toàn tối thiểu ($quantity \le min\_threshold$) kèm cờ `WARNING` phục vụ Dashboard Quản lý kho.
- **Response - Thành công (200 OK):**
```json
{
  "status": "success",
  "alerts_count": 3,
  "data": [
    {
      "center_id": "L5-WH-890",
      "part_code": "SCR-IP14-01",
      "part_name": "Màn hình OLED iPhone 14 Pro Max",
      "quantity": 8,
      "min_threshold": 15,
      "status_flag": "WARNING"
    }
  ]
}
```
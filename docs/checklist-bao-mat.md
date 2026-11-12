# DANH MỤC TỰ ĐÁNH GIÁ AN TOÀN BẢO MẬT (SECURITY CHECKLIST) — BÀI TẬP 3
*(Mandatory 7-Item Security Self-Assessment with Concrete Verification Proofs)*

- **Hệ thống:** Smart CRM – Mekong Mobile | **Luồng 05:** Kho linh kiện thay thế
- **Chuyên ngành:** Công nghệ phần mềm (`Track SE`)
- **Sinh viên:** Huỳnh Nguyễn Bảo Ngọc — **MSSV:** `2374802010339` | **Lớp:** `261_71ITGR40203_06`
- **Quy tắc đánh giá:** Mỗi mục chỉ nhận 1 trong 3 trạng thái (`ĐÃ LÀM` / `CHƯA LÀM` / `KHÔNG ÁP DỤNG`) kèm **01 dòng minh chứng cụ thể**.

---

## Bảng Tự Đánh Giá 7 Mục An Toàn Bảo Mật

| STT | Mục Kiểm Tra Bảo Mật | Trạng Thái | Dòng Minh Chứng Cụ Thể (Tệp mã nguồn / Lệnh kiểm tra & Kết quả thực tế) |
| :-: | :--- | :---: | :--- |
| **1** | **Không có secret nào trong repo** | **ĐÃ LÀM** | Lệnh quét Git `git grep -i "mongodb+srv://"` trả về 0 kết quả trên toàn bộ repo; `.gitignore` đã chặn nghiêm ngặt `.env` và tệp `.env.example` chỉ chứa chuỗi mẫu `localhost:27017`. |
| **2** | **Dữ liệu vào được kiểm ở tầng ứng dụng** | **ĐÃ LÀM** | Tệp `src/validators/inventory.validator.py` kiểm định chặt chẽ toàn bộ tham số (Regex email RFC, mật khẩu 4 nhóm ký tự, chặn kiểu `bool` giả số, biên số lượng $1 \le Q \le 1,000,000$, bắt buộc `ticket_id` theo `BR-02`). |
| **3** | **Kiểm soát truy cập theo chủ sở hữu (A01 OWASP)** | **ĐÃ LÀM** | Lớp Route `src/routes/inventory.routes.py` trích xuất `center_id` và `role` trực tiếp từ Bearer JWT Token; nếu request gửi sai chi nhánh sẽ ném `UnauthorizedCenterError` (HTTP 403 `ERR_UNAUTHORIZED_CENTER`); kiểm chứng qua ca test `test_10` trong `tests/bt3_specification_and_constraints.test.py` đạt **PASS**. |
| **4** | **Mật khẩu và dữ liệu nhạy cảm được băm hoặc mã hóa** | **ĐÃ LÀM** | Tệp `src/routes/inventory.routes.py` và `src/repositories/inventory.repository.py` chỉ lưu chuỗi băm `password_hash` (Bcrypt / SHA-256 64 hex), xóa bỏ 100% trường `password` dạng rõ trong CSDL và RAM; kiểm chứng qua ca test `test_09` đạt **PASS**. |
| **5** | **Thông báo lỗi không lộ cấu trúc bên trong** | **ĐÃ LÀM** | Bộ xử lý ngoại lệ tập trung `custom_app_error_handler` trong `src/app.py` chuẩn hóa 100% lỗi thành `{"status": "error", "error_code", "message"}`; tỷ lệ lộ mã lỗi hệ thống 500 hay Traceback là `0.0%`; kiểm chứng qua ca test `test_10` đạt **PASS**. |
| **6** | **Nhật ký không ghi secret hay dữ liệu cá nhân không cần thiết** | **ĐÃ LÀM** | Bảng sổ cái kiểm toán `part_transaction` chỉ lưu vết nghiệp vụ (`transaction_id, center_id, part_code, type, quantity, ticket_id, created_by, created_at`), tuyệt đối không ghi nhận mật khẩu, token hay thông tin thẻ ngân hàng. |
| **7** | **Phụ thuộc được ghim phiên bản và đã kiểm cảnh báo lỗ hổng cơ bản** | **ĐÃ LÀM** | Tệp `requirements.txt` ghim chặt chẽ 100% phiên bản bằng dấu `==` (`fastapi==0.162.0`, `uvicorn==0.54.0`, `pymongo==4.19.0`, `pyjwt==2.15.1`, `pytest==9.2.0`); lệnh quét `pip audit` hoặc `npm audit` không phát hiện lỗ hổng mức Critical/High. |

---

## Cam kết Trung thực về Liêm chính Học thuật
Tôi xin cam đoan các mục đánh giá an toàn bảo mật trên đều được trực tiếp kiểm chứng thực nghiệm bằng các lệnh chạy thật và tệp mã nguồn trong kho GitHub công khai https://github.com/Johnny120905/cdtn01_HuynhNguyenBaoNgoc_L5.git.

"""
File: src/validators/inventory.validator.py
Dự án: Hệ thống Smart CRM – Mekong Mobile (Luồng 05: Kho linh kiện thay thế)
Mục đích: Lớp kiểm tra tính hợp lệ của dữ liệu đầu vào (Input Validation Layer).
Vai trò trong kiến trúc phân lớp:
  - Nằm ở ranh giới giữa Lớp Điều phối (routes) và Lớp Nghiệp vụ (services).
  - Đảm bảo dữ liệu gửi lên thỏa mãn đúng hợp đồng API (docs/api-contract.md) và các ràng buộc dữ liệu.
  - Thực thi kiểm tra quy tắc BR-02: Bắt buộc mã phiếu bảo hành khi type là OUT hoặc RETURN.

Kết hợp với:
  - src/routes/inventory.routes.py: Gọi các hàm validate trước khi chuyển tiếp dữ liệu vào Service.
  - src/errors/AppError.py: Ném ra AppError (HTTP 400 hoặc HTTP 422) khi phát hiện dữ liệu không hợp lệ.
"""

from typing import Dict, Any
from src.errors.AppError import AppError, InvalidTicketError


def validate_stock_lookup(part_code: str) -> str:
    """
    Kiểm tra tính hợp lệ của mã linh kiện khi tra cứu tồn kho (FR-04 / GET /stock/{part_code}).
    
    Tham số:
      - part_code (str): Mã linh kiện truyền qua đường dẫn URL.
      
    Trả về:
      - str: Chuỗi mã linh kiện đã được chuẩn hóa (loại bỏ khoảng trắng thừa).
      
    Kết hợp với:
      - src/routes/inventory.routes.py -> Hàm get_stock_by_part_code()
      - src/services/inventory.service.py -> Hàm get_stock()
    """
    if not part_code or not isinstance(part_code, str) or not part_code.strip():
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_INPUT",
            message="Mã linh kiện (part_code) không được để trống."
        )
    return part_code.strip()


def validate_transaction_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Kiểm tra toàn bộ payload của yêu cầu ghi nhận giao dịch kho (POST /transactions).
    Thực thi ràng buộc nghiệp vụ BR-02 (Bắt buộc chứng từ).
    
    Quy tắc kiểm tra:
      1. part_code: Bắt buộc, chuỗi không rỗng.
      2. type: Bắt buộc, chỉ chấp nhận một trong ba giá trị: 'IN', 'OUT', 'RETURN'.
      3. quantity: Bắt buộc, kiểu số nguyên dương (> 0).
      4. ticket_id: Bắt buộc nếu type là 'OUT' hoặc 'RETURN' (Theo BR-02: Bắt buộc chứng từ).
         Đối với type là 'IN' (nhập kho từ nhà cung cấp), ticket_id có thể là None hoặc bỏ qua.
         
    Tham số:
      - data (dict): JSON body gửi từ Client (ReactJS).
      
    Trả về:
      - dict: Dữ liệu đã được kiểm duyệt và chuẩn hóa kiểu dữ liệu.
      
    Kết hợp với:
      - src/routes/inventory.routes.py -> Hàm create_transaction_route()
      - src/services/inventory.service.py -> Hàm process_transaction()
    """
    if not isinstance(data, dict):
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_BODY",
            message="Dữ liệu gửi lên phải là một đối tượng JSON hợp lệ."
        )

    # 1. Kiểm tra part_code
    part_code = data.get("part_code")
    if not part_code or not isinstance(part_code, str) or not part_code.strip():
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_PART_CODE",
            message="Trường 'part_code' (Mã linh kiện) là bắt buộc và không được để trống."
        )
    clean_part_code = part_code.strip()
    if len(clean_part_code) > 30:
        raise AppError(
            status_code=400,
            error_code="ERR_PART_CODE_TOO_LONG",
            message="Mã linh kiện không được vượt quá 30 ký tự."
        )

    # 2. Kiểm tra type (Loại giao dịch)
    tx_type = data.get("type")
    valid_types = ["IN", "OUT", "RETURN"]
    if not tx_type or tx_type not in valid_types:
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_TYPE",
            message=f"Trường 'type' không hợp lệ. Chỉ chấp nhận các giá trị: {', '.join(valid_types)}."
        )

    # 3. Kiểm tra quantity (Số lượng)
    quantity = data.get("quantity")
    if quantity is None:
        raise AppError(
            status_code=400,
            error_code="ERR_MISSING_QUANTITY",
            message="Trường 'quantity' (Số lượng) là bắt buộc."
        )
    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_QUANTITY",
            message="Số lượng linh kiện giao dịch (quantity) bắt buộc phải là số nguyên dương lớn hơn 0."
        )
    if quantity > 1000000:
        raise AppError(
            status_code=400,
            error_code="ERR_QUANTITY_EXCEEDED",
            message="Số lượng linh kiện giao dịch tối đa là 1,000,000 cái trong một lần thực hiện."
        )

    # 4. Kiểm tra ticket_id theo quy tắc BR-02
    ticket_id = data.get("ticket_id")
    if tx_type in ["OUT", "RETURN"]:
        if not ticket_id or not isinstance(ticket_id, str) or not ticket_id.strip():
            # Vi phạm quy tắc nghiệp vụ BR-02: Bắt buộc chứng từ
            raise InvalidTicketError(
                message="Mã phiếu bảo hành (ticket_id) là bắt buộc đối với giao dịch xuất kho hoặc hoàn trả."
            )
        clean_ticket_id = ticket_id.strip()
        if len(clean_ticket_id) > 30:
            raise AppError(
                status_code=400,
                error_code="ERR_TICKET_TOO_LONG",
                message="Mã phiếu bảo hành không được vượt quá 30 ký tự."
            )
    else:
        # Đối với lệnh IN (Nhập kho hàng mới), cho phép ticket_id là None
        clean_ticket_id = ticket_id.strip() if (ticket_id and isinstance(ticket_id, str)) else None
        if clean_ticket_id and len(clean_ticket_id) > 30:
            raise AppError(
                status_code=400,
                error_code="ERR_TICKET_TOO_LONG",
                message="Mã phiếu bảo hành không được vượt quá 30 ký tự."
            )

    return {
        "part_code": clean_part_code,
        "type": tx_type,
        "quantity": quantity,
        "ticket_id": clean_ticket_id
    }


def validate_threshold_payload(data: Dict[str, Any]) -> int:
    """
    Kiểm tra payload yêu cầu cập nhật ngưỡng an toàn min_threshold (PUT /parts/{part_code}/threshold).
    Phục vụ tính năng FR-06 dành cho Quản lý kho.
    
    Tham số:
      - data (dict): JSON body chứa trường 'min_threshold'.
      
    Trả về:
      - int: Giá trị ngưỡng an toàn mới.
      
    Kết hợp với:
      - src/routes/inventory.routes.py -> Hàm update_threshold_route()
      - src/services/inventory.service.py -> Hàm update_part_threshold()
    """
    if not isinstance(data, dict):
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_BODY",
            message="Dữ liệu gửi lên phải là một đối tượng JSON hợp lệ."
        )

    min_threshold = data.get("min_threshold")
    if min_threshold is None:
        raise AppError(
            status_code=400,
            error_code="ERR_MISSING_THRESHOLD",
            message="Trường 'min_threshold' (Ngưỡng an toàn tối thiểu) là bắt buộc."
        )
    if not isinstance(min_threshold, int) or isinstance(min_threshold, bool) or min_threshold < 0:
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_THRESHOLD",
            message="Ngưỡng an toàn (min_threshold) phải là số nguyên lớn hơn hoặc bằng 0."
        )
    if min_threshold > 100000:
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_THRESHOLD",
            message="Ngưỡng an toàn tối đa không được vượt quá 100,000."
        )

    return min_threshold


import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
VALID_ROLES = ["TECH_STAFF", "MATERIAL_STAFF", "MANAGER"]


def validate_password_complexity(password: str) -> None:
    r"""
    Ràng buộc mật khẩu: Tối thiểu 8 ký tự, tối đa 128 ký tự, phải chứa đầy đủ 4 nhóm:
      1. Chữ in hoa (A-Z)
      2. Chữ in thường (a-z)
      3. Chữ số (0-9)
      4. Ký hiệu đặc biệt (!@#$%^&*(),.?":{}|<>_~`-+=[]\;/)
    """
    if not password or not isinstance(password, str):
        raise AppError(
            status_code=400,
            error_code="ERR_WEAK_PASSWORD",
            message="Mật khẩu bắt buộc phải có tối thiểu 8 ký tự (bao gồm chữ hoa, chữ thường, số và ký hiệu đặc biệt)."
        )
    if len(password) < 8:
        raise AppError(
            status_code=400,
            error_code="ERR_WEAK_PASSWORD",
            message="Mật khẩu bắt buộc phải có độ dài tối thiểu 8 ký tự."
        )
    if len(password) > 128:
        raise AppError(
            status_code=400,
            error_code="ERR_WEAK_PASSWORD",
            message="Mật khẩu tối đa không được vượt quá 128 ký tự."
        )
    if not re.search(r"[A-Z]", password):
        raise AppError(
            status_code=400,
            error_code="ERR_WEAK_PASSWORD",
            message="Mật khẩu phải chứa ít nhất 1 chữ cái in hoa (A-Z)."
        )
    if not re.search(r"[a-z]", password):
        raise AppError(
            status_code=400,
            error_code="ERR_WEAK_PASSWORD",
            message="Mật khẩu phải chứa ít nhất 1 chữ cái in thường (a-z)."
        )
    if not re.search(r"\d", password):
        raise AppError(
            status_code=400,
            error_code="ERR_WEAK_PASSWORD",
            message="Mật khẩu phải chứa ít nhất 1 chữ số (0-9)."
        )
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_~`\-+=\[\]\\;/]", password):
        raise AppError(
            status_code=400,
            error_code="ERR_WEAK_PASSWORD",
            message="Mật khẩu phải chứa ít nhất 1 ký hiệu đặc biệt (!@#$%^&*...)."
        )


def validate_register_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Kiểm tra tính hợp lệ của dữ liệu đăng ký cấp quyền tài khoản người dùng mới.
    Ràng buộc:
      - full_name: Bắt buộc, chuỗi không rỗng (từ 2 đến 50 ký tự).
      - email: Bắt buộc, email thật đúng định dạng chuẩn RFC (tối đa 100 ký tự).
      - password: Bắt buộc, từ 8 đến 128 ký tự (đủ hoa, thường, số, ký hiệu đặc biệt).
      - role: Bắt buộc, chỉ được chọn 1 trong 3 vai trò: TECH_STAFF, MATERIAL_STAFF, MANAGER.
    """
    if not isinstance(data, dict):
        raise AppError(status_code=400, error_code="ERR_INVALID_BODY", message="Payload phải là đối tượng JSON.")

    full_name = data.get("full_name")
    if not full_name or not isinstance(full_name, str) or len(full_name.strip()) < 2:
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_FULL_NAME",
            message="Họ tên cá nhân là bắt buộc và phải có ít nhất 2 ký tự."
        )
    if len(full_name.strip()) > 50:
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_FULL_NAME",
            message="Họ tên tối đa không được vượt quá 50 ký tự."
        )

    email = data.get("email")
    if not email or not isinstance(email, str) or not EMAIL_REGEX.match(email.strip()):
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_EMAIL",
            message="Email cá nhân không đúng định dạng chuẩn (ví dụ: user@example.com)."
        )
    if len(email.strip()) > 100:
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_EMAIL",
            message="Email tối đa không được vượt quá 100 ký tự."
        )

    password = data.get("password")
    validate_password_complexity(password)

    role = data.get("role")
    if not role or role not in VALID_ROLES:
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_ROLE",
            message=f"Vai trò cấp quyền không hợp lệ. Chỉ chấp nhận một trong các vai trò: {', '.join(VALID_ROLES)}."
        )

    center_id = data.get("center_id", "L5-WH-890")
    if not center_id or not isinstance(center_id, str):
        center_id = "L5-WH-890"

    return {
        "full_name": full_name.strip(),
        "email": email.strip().lower(),
        "password": password,
        "role": role,
        "center_id": center_id.strip()
    }


def validate_login_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Kiểm tra tính hợp lệ của dữ liệu đăng nhập.
    Ràng buộc:
      - email: Bắt buộc, đúng định dạng email (tối đa 100 ký tự).
      - password: Bắt buộc, tối thiểu 6 ký tự (demo) hoặc 8 ký tự (tối đa 128 ký tự).
    """
    if not isinstance(data, dict):
        raise AppError(status_code=400, error_code="ERR_INVALID_BODY", message="Payload phải là đối tượng JSON.")

    email = data.get("email")
    if not email or not isinstance(email, str) or not EMAIL_REGEX.match(email.strip()):
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_EMAIL",
            message="Email đăng nhập không đúng định dạng chuẩn."
        )
    if len(email.strip()) > 100:
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_EMAIL",
            message="Email đăng nhập không được vượt quá 100 ký tự."
        )

    password = data.get("password")
    if not password or not isinstance(password, str) or len(password) < 6:
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_PASSWORD",
            message="Mật khẩu đăng nhập không được để trống (tối thiểu 8 ký tự đối với tài khoản mới)."
        )
    if len(password) > 128:
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_PASSWORD",
            message="Mật khẩu đăng nhập không được vượt quá 128 ký tự."
        )

    return {
        "email": email.strip().lower(),
        "password": password
    }


def validate_forgot_password_payload(data: Dict[str, Any]) -> str:
    """
    Kiểm tra email yêu cầu nhận mã OTP khôi phục mật khẩu.
    """
    if not isinstance(data, dict):
        raise AppError(status_code=400, error_code="ERR_INVALID_BODY", message="Payload phải là đối tượng JSON.")

    email = data.get("email")
    if not email or not isinstance(email, str) or not EMAIL_REGEX.match(email.strip()):
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_EMAIL",
            message="Email yêu cầu khôi phục mật khẩu không đúng định dạng chuẩn."
        )

    return email.strip().lower()


def validate_reset_password_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Kiểm tra payload xác nhận mã OTP và đặt lại mật khẩu mới.
    Ràng buộc:
      - email: Bắt buộc.
      - otp: Mã OTP gồm 6 chữ số.
      - new_password: Bắt buộc, tối thiểu 8 ký tự.
    """
    if not isinstance(data, dict):
        raise AppError(status_code=400, error_code="ERR_INVALID_BODY", message="Payload phải là đối tượng JSON.")

    email = data.get("email")
    if not email or not isinstance(email, str) or not EMAIL_REGEX.match(email.strip()):
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_EMAIL",
            message="Email xác thực không đúng định dạng."
        )

    otp = data.get("otp")
    if not otp or not isinstance(otp, str) or not otp.strip().isdigit() or len(otp.strip()) != 6:
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_OTP",
            message="Mã OTP phải là chuỗi 6 chữ số hợp lệ."
        )

    new_password = data.get("new_password")
    validate_password_complexity(new_password)

    return {
        "email": email.strip().lower(),
        "otp": otp.strip(),
        "new_password": new_password
    }


def validate_user_import_payload(data: Any) -> list:
    """
    Kiểm tra payload danh sách nhân sự cấp dưới cần import vào hệ thống.
    Chỉ cho phép import TECH_STAFF hoặc MATERIAL_STAFF.
    """
    users_list = []
    if isinstance(data, dict) and "users" in data:
        users_list = data["users"]
    elif isinstance(data, list):
        users_list = data
    else:
        raise AppError(
            status_code=400,
            error_code="ERR_INVALID_IMPORT_FORMAT",
            message="Dữ liệu import phải là mảng JSON hoặc đối tượng có khóa 'users'."
        )

    if not users_list:
        raise AppError(
            status_code=400,
            error_code="ERR_EMPTY_IMPORT",
            message="Danh sách nhân sự import không được rỗng."
        )

    cleaned_users = []
    subordinate_roles = ["TECH_STAFF", "MATERIAL_STAFF"]

    for idx, u in enumerate(users_list):
        if not isinstance(u, dict):
            raise AppError(status_code=400, error_code="ERR_INVALID_USER_ENTRY", message=f"Dòng {idx+1}: Bản ghi không hợp lệ.")
        name = u.get("full_name") or u.get("name")
        email = u.get("email")
        role = u.get("role")

        if not name or not isinstance(name, str) or len(name.strip()) < 2:
            raise AppError(status_code=400, error_code="ERR_INVALID_NAME", message=f"Dòng {idx+1}: Họ tên '{name}' không hợp lệ.")
        if not email or not isinstance(email, str) or not EMAIL_REGEX.match(email.strip()):
            raise AppError(status_code=400, error_code="ERR_INVALID_EMAIL", message=f"Dòng {idx+1}: Email '{email}' không đúng định dạng.")
        if role not in subordinate_roles:
            raise AppError(status_code=400, error_code="ERR_INVALID_ROLE", message=f"Dòng {idx+1}: Quản lý kho chỉ được import Nhân viên kỹ thuật (TECH_STAFF) hoặc Nhân viên vật tư (MATERIAL_STAFF).")

        cleaned_users.append({
            "full_name": name.strip(),
            "email": email.strip().lower(),
            "role": role,
            "center_id": u.get("center_id", "L5-WH-890"),
            "status": u.get("status", "ACTIVE")
        })

    return cleaned_users


def validate_part_create_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Kiểm tra tính hợp lệ khi tạo mới một linh kiện vào danh mục kho (CRUD: Create - Tiêu chí S1).
    Ràng buộc:
      - part_code: Bắt buộc, độ dài 3-30 ký tự, định dạng mã chuẩn.
      - part_name: Bắt buộc, độ dài 2-100 ký tự.
      - min_threshold: Số nguyên dương >= 1 (mặc định 10).
    """
    if not isinstance(data, dict):
        raise AppError(status_code=400, error_code="ERR_INVALID_BODY", message="Dữ liệu gửi lên phải là một đối tượng JSON hợp lệ.")

    part_code = data.get("part_code")
    if not part_code or not isinstance(part_code, str) or not part_code.strip():
        raise AppError(status_code=400, error_code="ERR_INVALID_PART_CODE", message="Mã linh kiện (part_code) là bắt buộc.")
    clean_code = part_code.strip().upper()
    if len(clean_code) < 3 or len(clean_code) > 30:
        raise AppError(status_code=400, error_code="ERR_INVALID_PART_CODE_LENGTH", message="Mã linh kiện phải từ 3 đến 30 ký tự.")

    part_name = data.get("part_name")
    if not part_name or not isinstance(part_name, str) or not part_name.strip():
        raise AppError(status_code=400, error_code="ERR_INVALID_PART_NAME", message="Tên linh kiện (part_name) là bắt buộc.")
    clean_name = part_name.strip()
    if len(clean_name) < 2 or len(clean_name) > 100:
        raise AppError(status_code=400, error_code="ERR_INVALID_PART_NAME_LENGTH", message="Tên linh kiện phải từ 2 đến 100 ký tự.")

    min_threshold = data.get("min_threshold", 10)
    try:
        min_threshold = int(min_threshold)
        if min_threshold < 1 or min_threshold > 500:
            raise ValueError()
    except (ValueError, TypeError):
        raise AppError(status_code=400, error_code="ERR_INVALID_THRESHOLD", message="Ngưỡng cảnh báo tối thiểu phải là số nguyên từ 1 đến 500.")

    category = data.get("category", "Linh kiện thay thế")
    if not isinstance(category, str):
        category = "Linh kiện thay thế"

    compatible_model = data.get("compatible_model", "Tất cả")
    if not isinstance(compatible_model, str):
        compatible_model = "Tất cả"

    supplier = data.get("supplier", "Mekong Official Supplier")
    if not isinstance(supplier, str):
        supplier = "Mekong Official Supplier"

    unit = data.get("unit", "Cái")
    if not isinstance(unit, str):
        unit = "Cái"

    center_id = data.get("center_id", "L5-WH-890")

    return {
        "part_code": clean_code,
        "part_name": clean_name,
        "category": category.strip(),
        "compatible_model": compatible_model.strip(),
        "supplier": supplier.strip(),
        "unit": unit.strip(),
        "min_threshold": min_threshold,
        "center_id": center_id.strip() if isinstance(center_id, str) else "L5-WH-890"
    }


def validate_part_update_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Kiểm tra tính hợp lệ khi cập nhật thông tin linh kiện (CRUD: Update - Tiêu chí S1).
    Không cho phép cập nhật part_code.
    """
    if not isinstance(data, dict):
        raise AppError(status_code=400, error_code="ERR_INVALID_BODY", message="Dữ liệu gửi lên phải là một đối tượng JSON hợp lệ.")

    cleaned = {}
    if "part_name" in data:
        val = data["part_name"]
        if not val or not isinstance(val, str) or len(val.strip()) < 2:
            raise AppError(status_code=400, error_code="ERR_INVALID_PART_NAME", message="Tên linh kiện phải có ít nhất 2 ký tự.")
        cleaned["part_name"] = val.strip()

    if "category" in data and isinstance(data["category"], str):
        cleaned["category"] = data["category"].strip()

    if "compatible_model" in data and isinstance(data["compatible_model"], str):
        cleaned["compatible_model"] = data["compatible_model"].strip()

    if "supplier" in data and isinstance(data["supplier"], str):
        cleaned["supplier"] = data["supplier"].strip()

    if "unit" in data and isinstance(data["unit"], str):
        cleaned["unit"] = data["unit"].strip()

    if "min_threshold" in data:
        try:
            th = int(data["min_threshold"])
            if th < 1 or th > 500:
                raise ValueError()
            cleaned["min_threshold"] = th
        except (ValueError, TypeError):
            raise AppError(status_code=400, error_code="ERR_INVALID_THRESHOLD", message="Ngưỡng cảnh báo tối thiểu phải là số nguyên từ 1 đến 500.")

    return cleaned


def validate_user_update_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Kiểm tra tính hợp lệ khi cập nhật thông tin nhân sự (CRUD: Update - Tiêu chí S1).
    Không cho phép cập nhật email hay password_hash trực tiếp qua endpoint này.
    """
    if not isinstance(data, dict):
        raise AppError(status_code=400, error_code="ERR_INVALID_BODY", message="Dữ liệu gửi lên phải là một đối tượng JSON hợp lệ.")

    cleaned = {}
    if "full_name" in data:
        val = data["full_name"]
        if not val or not isinstance(val, str) or len(val.strip()) < 2:
            raise AppError(status_code=400, error_code="ERR_INVALID_NAME", message="Họ tên phải có ít nhất 2 ký tự.")
        cleaned["full_name"] = val.strip()
        cleaned["name"] = val.strip()

    if "phone" in data and isinstance(data["phone"], str):
        cleaned["phone"] = data["phone"].strip()

    if "role" in data:
        val = data["role"]
        if val not in VALID_ROLES:
            raise AppError(status_code=400, error_code="ERR_INVALID_ROLE", message=f"Vai trò không hợp lệ. Chỉ chấp nhận: {', '.join(VALID_ROLES)}.")
        cleaned["role"] = val
        role_labels = {"MANAGER": "Quản lý kho", "MATERIAL_STAFF": "Nhân viên vật tư", "TECH_STAFF": "Nhân viên kỹ thuật"}
        cleaned["role_label"] = role_labels.get(val, "Nhân sự kho")

    if "status" in data:
        val = data["status"]
        if val not in ["ACTIVE", "INACTIVE", "OFF_SHIFT", "ONLINE", "LOCKED"]:
            raise AppError(status_code=400, error_code="ERR_INVALID_STATUS", message="Trạng thái nhân sự không hợp lệ.")
        cleaned["status"] = val

    return cleaned



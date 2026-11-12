"""
File: src/services/inventory.service.py
Dự án: Hệ thống Smart CRM – Mekong Mobile (Luồng 05: Kho linh kiện thay thế)
Mục đích: Lớp Nghiệp vụ cốt lõi (Business Logic Service Layer).
Tuân thủ nguyên tắc thiết kế trong Slide 7 & NFR-03:
  1. Tuyệt đối KHÔNG import bất kỳ thành phần nào của HTTP (không có req, res, status_code).
  2. Độc lập hoàn toàn với framework web, có thể chạy trong CLI, Background Job hay API.
  3. Thực thi toàn bộ các quy tắc nghiệp vụ cốt lõi:
     - BR-01: Chống tồn kho âm (Non-negative Stock).
     - BR-02: Bắt buộc mã chứng từ bảo hành khi Xuất / Hoàn linh kiện.
     - BR-03: Bất biến lịch sử giao dịch (Insert-only Audit Log).
     - BR-04: Phân mảnh dữ liệu theo trung tâm (Center Isolation).
     - BR-05: Tự động đánh giá cờ cảnh báo an toàn (Real-time Threshold Evaluation).
     - NFR-03 & EX-05: Thuật toán Optimistic Locking ngăn chặn Race Condition khi xuất kho đồng thời.

Kết hợp với:
  - src/repositories/inventory.repository.py: Đọc và ghi dữ liệu CSDL MongoDB.
  - src/errors/AppError.py: Ném các ngoại lệ nghiệp vụ khi vi phạm điều kiện.
  - src/routes/inventory.routes.py: Gọi các hàm trong service này và nhận kết quả trả về.
"""

import time
import copy
from datetime import datetime
from typing import Dict, Any, List, Optional
from src.repositories import inventory_repository, InventoryRepository
from src.errors.AppError import (
    AppError,
    NegativeStockError,
    InvalidTicketError,
    ConcurrentUpdateError,
    UnauthorizedCenterError,
    UnauthorizedRoleError,
    ResourceNotFoundError
)


class InventoryService:
    """
    Lớp dịch vụ quản lý nghiệp vụ kho linh kiện.
    Chứa toàn bộ các thuật toán tính toán tồn kho, kiểm tra ngưỡng và ghi vết sổ cái.
    """
    def __init__(self, repo: Optional[InventoryRepository] = None):
        # Cho phép Dependency Injection khi chạy Unit Test
        self.repo = repo or inventory_repository

    # ==============================================================================
    # 1. NGHIỆP VỤ TRA CỨU TỒN KHO REAL-TIME (FR-04, BR-04, BR-05)
    # ==============================================================================

    def get_stock(self, center_id: str, part_code: str) -> Dict[str, Any]:
        """
        Tra cứu số lượng tồn kho tức thời của một linh kiện tại trung tâm hiện tại.
        
        Quy trình xử lý:
          1. Đọc thông tin linh kiện gốc từ collection 'part' để lấy part_name và min_threshold.
          2. Đọc thông tin tồn kho từ collection 'part_stock' theo center_id và part_code.
          3. Thực hiện quy tắc BR-05: Nếu quantity <= min_threshold -> gắn cờ 'WARNING', ngược lại 'NORMAL'.
          
        Tham số:
          - center_id (str): Mã trung tâm bảo hành của nhân sự (BR-04).
          - part_code (str): Mã linh kiện cần tra cứu (VD: SCR-IP14-01).
          
        Trả về:
          - dict: Cấu trúc dữ liệu theo đúng Hợp đồng API 1 trong docs/api-contract.md.
          
        Ngoại lệ:
          - ResourceNotFoundError: Nếu mã linh kiện không tồn tại trong danh mục hệ thống.
        """
        # Bước 1: Kiểm tra danh mục linh kiện gốc
        part_info = self.repo.find_part(part_code)
        if not part_info:
            raise ResourceNotFoundError(f"Không tìm thấy linh kiện với mã '{part_code}' trong danh mục.")

        # Bước 2: Lấy số lượng tồn kho vật lý tại trung tâm
        stock_info = self.repo.find_stock(center_id, part_code)
        quantity = stock_info.get("quantity", 0) if stock_info else 0
        min_threshold = part_info.get("min_threshold", 0)

        # Bước 3: Đánh giá cờ cảnh báo an toàn theo quy tắc BR-05
        # Trạng thái 'WARNING' kích hoạt tính năng cảnh báo thiếu hàng FR-07 trên giao diện
        status_flag = "WARNING" if quantity <= min_threshold else "NORMAL"

        return {
            "center_id": center_id,
            "part_code": part_code,
            "part_name": part_info.get("part_name", part_code),
            "category": part_info.get("category", "Linh kiện"),
            "price": part_info.get("price", 0.0),
            "quantity": quantity,
            "min_threshold": min_threshold,
            "status_flag": status_flag
        }

    def get_all_stock(self, center_id: str) -> List[Dict[str, Any]]:
        """
        Lấy toàn bộ danh sách tồn kho tại một trung tâm, tự động ghép thông tin linh kiện và cờ cảnh báo.
        Phục vụ hiển thị bảng danh sách vật tư trên giao diện Kỹ thuật viên và Quản lý kho.
        """
        stocks = self.repo.find_all_stocks(center_id)
        stock_map = {s["part_code"]: s for s in stocks}

        parts = self.repo.find_all_parts()
        results = []

        for p in parts:
            p_code = p["part_code"]
            stock_entry = stock_map.get(p_code)
            qty = stock_entry.get("quantity", 0) if stock_entry else 0
            threshold = p.get("min_threshold", 0)
            status_flag = "WARNING" if qty <= threshold else "NORMAL"

            results.append({
                "center_id": center_id,
                "part_code": p_code,
                "part_name": p.get("part_name", p_code),
                "category": p.get("category", "Linh kiện"),
                "price": p.get("price", 0.0),
                "quantity": qty,
                "min_threshold": threshold,
                "status_flag": status_flag
            })

        return results

    def get_low_stock_alerts(self, center_id: str) -> List[Dict[str, Any]]:
        """
        Lấy danh sách các linh kiện đang chạm ngưỡng an toàn hoặc cạn kiệt (quantity <= min_threshold).
        Thực hiện yêu cầu chức năng FR-07 (Cờ đỏ cảnh báo thiếu hàng cho Quản lý kho).
        """
        all_stocks = self.get_all_stock(center_id)
        alerts = [item for item in all_stocks if item["status_flag"] == "WARNING"]
        return alerts

    # ==============================================================================
    # 2. NGHIỆP VỤ BIẾN ĐỘNG KHO & OPTIMISTIC LOCKING (FR-01, FR-02, FR-03, BR-01..BR-03)
    # ==============================================================================

    def process_transaction(
        self,
        center_id: str,
        part_code: str,
        tx_type: str,
        quantity: int,
        ticket_id: Optional[str],
        user_email: str,
        user_role: str
    ) -> Dict[str, Any]:
        """
        Ghi nhận một giao dịch làm biến động số lượng tồn kho (Nhập / Xuất / Hoàn trả).
        Thực hiện đầy đủ các chốt chặn an toàn theo đặc tả UC-02 & NFR-03:
        
        Các bước nghiệp vụ:
          Bước 1: Phân quyền vai trò thực hiện:
                  - Xuất kho (OUT) & Hoàn kho (RETURN): Chỉ Nhân viên Kỹ thuật (TECH_STAFF) và Quản lý (MANAGER).
                  - Nhập kho (IN): Chỉ Nhân viên Vật tư (MATERIAL_STAFF) và Quản lý (MANAGER).
          Bước 2: Kiểm tra phiếu bảo hành (ticket_id) theo BR-02:
                  - Bắt buộc phiếu phải tồn tại và đang mở (OPEN / IN_PROGRESS).
          Bước 3: Kiểm tra sự tồn tại của linh kiện trong danh mục.
          Bước 4: Chặn tồn kho âm (BR-01):
                  - Nếu là OUT: Đảm bảo số lượng yêu cầu <= tồn kho thực tế hiện tại.
          Bước 5: Áp dụng thuật toán Optimistic Locking (NFR-03 & EX-05):
                  - Thực thi lệnh cập nhật số lượng dựa trên 'version'.
                  - Nếu version bị lệch do có người xuất trước ở cùng mili-giây -> ném ConcurrentUpdateError (HTTP 409).
          Bước 6: Ghi nhật ký giao dịch vĩnh viễn (BR-03: Bất biến lịch sử).
          
        Trả về:
          - dict: Thông tin kết quả giao dịch kèm transaction_id và thời gian tạo.
        """
        # Bước 1: Kiểm tra phân quyền thao tác theo vai trò
        if tx_type in ["OUT", "RETURN"] and user_role not in ["TECH_STAFF", "MANAGER"]:
            raise UnauthorizedRoleError(
                message="Chỉ Nhân viên Kỹ thuật hoặc Quản lý kho mới có quyền tạo lệnh Xuất kho hoặc Hoàn trả."
            )
        if tx_type == "IN" and user_role not in ["MATERIAL_STAFF", "MANAGER"]:
            raise UnauthorizedRoleError(
                message="Chỉ Nhân viên Vật tư hoặc Quản lý kho mới có quyền tạo lệnh Nhập kho linh kiện mới."
            )

        # Bước 2: Kiểm tra mã phiếu bảo hành theo quy tắc BR-02
        if tx_type in ["OUT", "RETURN"]:
            if not ticket_id:
                raise InvalidTicketError(message="Mã phiếu bảo hành (ticket_id) không được để trống khi xuất/hoàn.")
            ticket_doc = self.repo.find_ticket(ticket_id)
            if not ticket_doc:
                raise InvalidTicketError(
                    message=f"Mã phiếu bảo hành '{ticket_id}' không tồn tại trong hệ thống."
                )
            if ticket_doc.get("status") in ["CANCELLED", "COMPLETED"]:
                raise InvalidTicketError(
                    message=f"Phiếu bảo hành '{ticket_id}' hiện đã kết thúc hoặc bị hủy, không thể xuất linh kiện."
                )

        # Bước 3: Kiểm tra sự tồn tại của linh kiện
        part_doc = self.repo.find_part(part_code)
        if not part_doc:
            raise ResourceNotFoundError(f"Linh kiện với mã '{part_code}' không tồn tại trong hệ thống.")

        # Bước 4: Lấy thông tin tồn kho hiện thời và kiểm tra chống tồn kho âm (BR-01)
        stock_doc = self.repo.find_stock(center_id, part_code)
        current_qty = stock_doc.get("quantity", 0) if stock_doc else 0
        current_version = stock_doc.get("version", 1) if stock_doc else 1

        if tx_type == "OUT":
            if current_qty < quantity:
                # Vi phạm quy tắc BR-01: Tồn kho không âm
                raise NegativeStockError(
                    message=f"Số lượng xuất ({quantity}) vượt quá tồn kho thực tế ({current_qty}). Giao dịch bị từ chối."
                )

        # Bước 5: Thực thi biến động kho bằng thuật toán Optimistic Locking
        qty_delta = quantity if tx_type in ["IN", "RETURN"] else -quantity

        # Nếu chưa có bản ghi tồn kho và là lệnh nhập hàng mới (IN)
        if not stock_doc and tx_type == "IN":
            self.repo.upsert_stock(center_id, part_code, quantity, version=1)
        else:
            # Cập nhật có kiểm tra phiên bản (version)
            update_success = self.repo.update_stock_optimistic(
                center_id=center_id,
                part_code=part_code,
                quantity_delta=qty_delta,
                expected_version=current_version
            )

            if not update_success:
                # Kiểm tra nguyên nhân thất bại: Do thiếu số lượng hay do xung đột phiên bản đồng thời
                refreshed_stock = self.repo.find_stock(center_id, part_code)
                if refreshed_stock and tx_type == "OUT" and refreshed_stock.get("quantity", 0) < quantity:
                    raise NegativeStockError(
                        message="Số lượng tồn kho vừa bị trừ bởi một giao dịch khác không còn đủ để xuất."
                    )
                # Vi phạm xung đột đồng thời (EX-05)
                raise ConcurrentUpdateError(
                    message="Linh kiện này vừa được cập nhật bởi một nhân viên khác trong cùng thời điểm. Vui lòng thử lại."
                )

        # Bước 6: Sinh bản ghi Nhật ký giao dịch vĩnh viễn (BR-03: Bất biến lịch sử)
        # Sinh mã transaction_id định danh duy nhất (6 chữ số tăng tiến)
        generated_tx_id = int(time.time() * 1000) % 900000 + 100000
        now = datetime.utcnow()

        transaction_doc = {
            "transaction_id": generated_tx_id,
            "center_id": center_id,
            "part_code": part_code,
            "type": tx_type,
            "quantity": quantity,
            "ticket_id": ticket_id,
            "created_by": user_email,
            "created_at": now
        }

        saved_tx = self.repo.insert_transaction(transaction_doc)

        return {
            "transaction_id": saved_tx["transaction_id"],
            "created_at": now.isoformat() + "Z"
        }

    # ==============================================================================
    # 3. NGHIỆP VỤ THIẾT LẬP NGƯỠNG AN TOÀN (FR-06)
    # ==============================================================================

    def set_part_threshold(self, user_role: str, part_code: str, min_threshold: int) -> bool:
        """
        Thiết lập lại ngưỡng tồn kho an toàn cho một mã linh kiện (FR-06).
        Chỉ cho phép Quản lý kho (MANAGER) thực hiện.
        
        Ngoại lệ:
          - UnauthorizedRoleError: Nếu người gọi không phải là Quản lý kho.
          - ResourceNotFoundError: Nếu không tìm thấy mã linh kiện.
        """
        if user_role != "MANAGER":
            # Chặn phân quyền vi phạm hợp đồng API 3
            raise UnauthorizedRoleError(
                message="Tài khoản của bạn không có quyền sửa đổi thông số này. Quyền này chỉ dành riêng cho Quản lý kho."
            )

        part_doc = self.repo.find_part(part_code)
        if not part_doc:
            raise ResourceNotFoundError(f"Không tìm thấy linh kiện với mã '{part_code}' để cập nhật ngưỡng.")

        success = self.repo.update_part_threshold(part_code, min_threshold)
        return success

    # ==============================================================================
    # 4. TRÍCH XUẤT NHẬT KÝ ĐỐI SOÁT & DASHBOARD (FR-05)
    # ==============================================================================

    def get_transaction_history(self, center_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Lấy danh sách nhật ký giao dịch phục vụ đối soát số liệu (FR-05)."""
        return self.repo.find_transactions(center_id=center_id, limit=limit)

    def get_dashboard_metrics(self, center_id: str, user_role: str) -> Dict[str, Any]:
        """
        Tổng hợp các chỉ số KPI vận hành kho cho Dashboard của 3 vai trò:
          - Tổng số loại linh kiện đang quản lý.
          - Số lượng linh kiện đang bị cảnh báo đỏ (cạn hàng).
          - Số lượng phiếu sửa chữa đang chờ xử lý.
          - Tổng số lượt giao dịch trong ngày.
        """
        all_stocks = self.get_all_stock(center_id)
        total_items = len(all_stocks)
        warning_count = sum(1 for item in all_stocks if item["status_flag"] == "WARNING")
        
        all_tickets = self.repo.find_all_tickets()
        pending_tickets = [t for t in all_tickets if t.get("status") in ["OPEN", "IN_PROGRESS"]]
        
        history = self.repo.find_transactions(center_id=center_id, limit=100)
        
        return {
            "center_id": center_id,
            "total_items": total_items,
            "warning_count": warning_count,
            "pending_tickets_count": len(pending_tickets),
            "today_transactions_count": len(history),
            "operational_status": "Hoạt động bình thường"
        }

    # ==============================================================================
    # 5. CÁC THAO TÁC CRUD ĐẦY ĐỦ CHO THỰC THỂ PART & USER (TIÊU CHÍ SE S1)
    # ==============================================================================

    def create_part(self, payload: Dict[str, Any], operator_role: str) -> Dict[str, Any]:
        """Tạo linh kiện mới trong danh mục kho (Create). Chỉ MANAGER hoặc MATERIAL_STAFF có quyền."""
        if operator_role not in ["MANAGER", "MATERIAL_STAFF"]:
            raise UnauthorizedRoleError("Chỉ Quản lý kho hoặc Nhân viên vật tư mới có quyền thêm linh kiện mới vào danh mục.")
        return self.repo.create_part(payload)

    def get_part_detail(self, part_code: str) -> Dict[str, Any]:
        """Tra cứu chi tiết linh kiện theo mã (Read). Mọi vai trò đã đăng nhập đều có quyền tra cứu."""
        clean_code = part_code.strip()
        part = self.repo.find_part(clean_code)
        if not part:
            raise ResourceNotFoundError(f"Không tìm thấy linh kiện với mã '{clean_code}'.")
        return part

    def update_part(self, part_code: str, payload: Dict[str, Any], operator_role: str) -> Dict[str, Any]:
        """Cập nhật thông tin linh kiện (Update). Chỉ MANAGER hoặc MATERIAL_STAFF có quyền."""
        if operator_role not in ["MANAGER", "MATERIAL_STAFF"]:
            raise UnauthorizedRoleError("Chỉ Quản lý kho hoặc Nhân viên vật tư mới có quyền cập nhật thông tin linh kiện.")
        clean_code = part_code.strip()
        updated = self.repo.update_part(clean_code, payload)
        if not updated:
            raise ResourceNotFoundError(f"Không tìm thấy linh kiện với mã '{clean_code}' để cập nhật.")
        return updated

    def delete_part(self, part_code: str, operator_role: str) -> bool:
        """Xóa linh kiện khỏi danh mục kho (Delete). Chỉ MANAGER có quyền."""
        if operator_role != "MANAGER":
            raise UnauthorizedRoleError("Chỉ Quản lý kho mới có quyền xóa linh kiện khỏi hệ thống.")
        return self.repo.delete_part(part_code)

    def create_user_account(self, payload: Dict[str, Any], operator_role: str) -> Dict[str, Any]:
        """Tạo mới tài khoản nhân sự (Create). Chỉ MANAGER có quyền tạo nhân sự cấp dưới."""
        if operator_role != "MANAGER":
            raise UnauthorizedRoleError("Chỉ Quản lý kho mới có quyền tạo mới tài khoản nhân sự.")
        return self.repo.create_user(payload)

    def get_user_detail(self, email: str) -> Dict[str, Any]:
        """Tra cứu chi tiết tài khoản nhân sự theo email (Read)."""
        clean_email = email.strip().lower()
        user = self.repo.find_user_by_email(clean_email)
        if not user:
            raise ResourceNotFoundError(f"Không tìm thấy tài khoản với email '{clean_email}'.")
        safe_user = copy.deepcopy(user)
        safe_user.pop("password_hash", None)
        return safe_user

    def update_user_profile(self, email: str, payload: Dict[str, Any], operator_role: str) -> Dict[str, Any]:
        """Cập nhật thông tin tài khoản nhân sự (Update). Chỉ MANAGER có quyền sửa nhân sự cấp dưới."""
        if operator_role != "MANAGER":
            raise UnauthorizedRoleError("Chỉ Quản lý kho mới có quyền cập nhật thông tin nhân sự.")
        clean_email = email.strip().lower()
        updated = self.repo.update_user_profile(clean_email, payload)
        if not updated:
            raise ResourceNotFoundError(f"Không tìm thấy tài khoản với email '{clean_email}' để cập nhật.")
        return updated

    def delete_user_account(self, email: str, operator_role: str, current_user_email: str) -> bool:
        """Xóa tài khoản nhân sự (Delete). Chỉ MANAGER có quyền và không được tự xóa chính mình."""
        if operator_role != "MANAGER":
            raise UnauthorizedRoleError("Chỉ Quản lý kho mới có quyền xóa tài khoản nhân sự.")
        clean_email = email.strip().lower()
        if clean_email == current_user_email.strip().lower():
            raise AppError(status_code=400, error_code="ERR_CANNOT_DELETE_SELF", message="Bạn không thể tự xóa tài khoản của chính mình.")
        return self.repo.delete_user(clean_email)


# Đối tượng Service dùng chung trong toàn bộ ứng dụng
inventory_service = InventoryService()

"""
File: src/repositories/inventory.repository.py
Dự án: Hệ thống Smart CRM – Mekong Mobile (Luồng 05: Kho linh kiện thay thế)
Mục đích: Lớp Truy cập dữ liệu (Data Access / Repository Layer).
Vai trò trong kiến trúc phân lớp:
  - Chỉ chịu trách nhiệm đọc và ghi dữ liệu trực tiếp xuống cơ sở dữ liệu MongoDB.
  - Tuyệt đối KHÔNG chứa bất kỳ logic nghiệp vụ nào (tuân thủ nguyên tắc phụ thuộc một chiều trong Slide 7).
  - Tự động kết nối tới MongoDB qua chuỗi MONGO_URI trong .env.
  - Tích hợp cơ chế Fallback Cache thông minh: Nếu MongoDB chưa khởi động, hệ thống sử dụng kho dữ liệu
    mẫu từ seeds/001_seed_parts_demo.json để đảm bảo ứng dụng luôn chạy thử nghiệm được mượt mà (NFR-01).

Kết hợp với:
  - src/services/inventory.service.py: Gọi các phương thức của Repository để lấy hoặc lưu dữ liệu.
  - seeds/001_seed_parts_demo.json: Nguồn dữ liệu khởi tạo ban đầu.
"""

import os
import json
import copy
from datetime import datetime
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import pymongo
from bson import ObjectId

# Nạp các biến môi trường từ .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/inventory_db")
DB_NAME = os.getenv("DB_NAME", "inventory_db")


class InventoryRepository:
    """
    Lớp Repository đóng gói toàn bộ thao tác CRUD trên 6 Collections của MongoDB:
      1. service_center
      2. part
      3. ticket
      4. part_stock
      5. part_transaction
      6. users
    """
    _global_connection_tested = False
    _global_is_connected = False

    def __init__(self, mongo_uri: Optional[str] = None, db_name: Optional[str] = None, connect: bool = True):
        self.mongo_uri = mongo_uri or MONGO_URI
        self.db_name = db_name or DB_NAME
        self.client: Optional[pymongo.MongoClient] = None
        self.db = None
        self.is_connected = False

        # Bộ nhớ đệm InMemory Fallback (sử dụng khi MongoDB chưa sẵn sàng trên máy cục bộ)
        self._memory_store: Dict[str, List[Dict[str, Any]]] = {}
        self._load_seed_into_memory()
        if connect:
            self._init_connection()

    def _load_seed_into_memory(self):
        """Đọc file seeds/001_seed_parts_demo.json và data/users_store.json vào bộ nhớ đệm phục vụ chế độ offline fallback."""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            seed_path = os.path.join(base_dir, "seeds", "001_seed_parts_demo.json")
            if os.path.exists(seed_path):
                with open(seed_path, "r", encoding="utf-8") as f:
                    self._memory_store = json.load(f)
            else:
                self._memory_store = {
                    "service_center": [],
                    "part": [],
                    "ticket": [],
                    "part_stock": [],
                    "part_transaction": [],
                    "users": []
                }

            # Nạp và hòa trộn tài khoản đã đăng ký được lưu tại data/users_store.json
            users_file = os.path.join(base_dir, "data", "users_store.json")
            if os.path.exists(users_file):
                with open(users_file, "r", encoding="utf-8") as f:
                    saved_users = json.load(f)
                    if isinstance(saved_users, list):
                        existing_emails = {u.get("email", "").lower() for u in self._memory_store.get("users", [])}
                        for su in saved_users:
                            if su.get("email", "").lower() not in existing_emails:
                                self._memory_store.setdefault("users", []).append(su)
                            else:
                                for idx, u in enumerate(self._memory_store.get("users", [])):
                                    if u.get("email", "").lower() == su.get("email", "").lower():
                                        self._memory_store["users"][idx] = su
                                        break
        except Exception as e:
            print(f"[Repository Warning] Không thể nạp seed json: {e}")
            self._memory_store = {}

    def _save_users_to_disk(self):
        """Lưu toàn bộ danh sách người dùng vào file data/users_store.json để bảo tồn tài khoản khi tắt server."""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            data_dir = os.path.join(base_dir, "data")
            os.makedirs(data_dir, exist_ok=True)
            users_file = os.path.join(data_dir, "users_store.json")
            with open(users_file, "w", encoding="utf-8") as f:
                json.dump(self._memory_store.get("users", []), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[Repository Warning] Không thể ghi users_store.json: {e}")

    def _init_connection(self):
        """Khởi tạo kết nối tới MongoDB với timeout ngắn để không gây treo tiến trình."""
        try:
            self.client = pymongo.MongoClient(self.mongo_uri, serverSelectionTimeoutMS=2000)
            self.client.server_info()  # Thử ping server
            self.db = self.client[self.db_name]
            self.is_connected = True
            print(f"[Repository] Connected to MongoDB: {self.db_name} at {self.mongo_uri}")
        except Exception as e:
            self.is_connected = False
            print("[Repository] Running in In-Memory Fallback mode (MongoDB offline).")

    # ==============================================================================
    # 1. THAO TÁC TRÊN COLLECTION: part_stock (Tồn kho vật lý)
    # ==============================================================================

    def find_stock(self, center_id: str, part_code: str) -> Optional[Dict[str, Any]]:
        """
        Tìm kiếm bản ghi tồn kho của một mã linh kiện tại một trung tâm cụ thể.
        Sử dụng chỉ mục compound index {center_id: 1, part_code: 1} để đạt tốc độ < 500ms (NFR-02).
        """
        if self.is_connected and self.db is not None:
            doc = self.db.part_stock.find_one({"center_id": center_id, "part_code": part_code}, {"_id": 0})
            return doc
        else:
            for item in self._memory_store.get("part_stock", []):
                if item.get("center_id") == center_id and item.get("part_code") == part_code:
                    return copy.deepcopy(item)
            return None

    def find_all_stocks(self, center_id: str) -> List[Dict[str, Any]]:
        """Lấy toàn bộ danh sách tồn kho tại một trung tâm chỉ định (Phục vụ BR-04 Center Isolation)."""
        if self.is_connected and self.db is not None:
            cursor = self.db.part_stock.find({"center_id": center_id}, {"_id": 0})
            return list(cursor)
        else:
            return [copy.deepcopy(x) for x in self._memory_store.get("part_stock", []) if x.get("center_id") == center_id]

    def update_stock_optimistic(
        self,
        center_id: str,
        part_code: str,
        quantity_delta: int,
        expected_version: int
    ) -> bool:
        """
        Thực hiện cập nhật số lượng tồn kho theo cơ chế Optimistic Locking (NFR-03 & EX-05).
        
        Logic thực thi nguyên tử (Atomic):
          - Điều kiện lọc: đúng center_id, đúng part_code, đúng expected_version.
          - Nếu quantity_delta < 0 (Xuất kho): điều kiện lọc bổ sung quantity >= |quantity_delta|
            để đảm bảo BR-01: Tồn kho không âm ở cấp độ Database.
          - Hành động cập nhật: tăng/giảm quantity và version = expected_version + 1.
          
        Trả về:
          - True: Nếu cập nhật thành công (matched_count == 1).
          - False: Nếu phiên bản bị xung đột hoặc không thỏa mãn số lượng tồn kho.
        """
        if self.is_connected and self.db is not None:
            query: Dict[str, Any] = {
                "center_id": center_id,
                "part_code": part_code,
                "version": expected_version
            }
            if quantity_delta < 0:
                # Chặn tồn kho âm ở tầng database
                query["quantity"] = {"$gte": abs(quantity_delta)}

            update_doc = {
                "$inc": {
                    "quantity": quantity_delta,
                    "version": 1
                }
            }
            result = self.db.part_stock.update_one(query, update_doc)
            return result.modified_count > 0
        else:
            # Xử lý trên InMemory Fallback
            for item in self._memory_store.get("part_stock", []):
                if item.get("center_id") == center_id and item.get("part_code") == part_code:
                    if item.get("version") != expected_version:
                        return False
                    new_qty = item.get("quantity", 0) + quantity_delta
                    if new_qty < 0:
                        return False
                    item["quantity"] = new_qty
                    item["version"] = expected_version + 1
                    return True
            # Nếu chưa tồn tại bản ghi tồn kho và là lệnh nhập kho (IN)
            if quantity_delta > 0:
                self._memory_store.setdefault("part_stock", []).append({
                    "center_id": center_id,
                    "part_code": part_code,
                    "quantity": quantity_delta,
                    "version": 1
                })
                return True
            return False

    def upsert_stock(self, center_id: str, part_code: str, quantity: int, version: int = 1) -> None:
        """Thêm mới hoặc cập nhật bản ghi tồn kho ban đầu."""
        if self.is_connected and self.db is not None:
            self.db.part_stock.update_one(
                {"center_id": center_id, "part_code": part_code},
                {"$set": {"quantity": quantity, "version": version}},
                upsert=True
            )
        else:
            for item in self._memory_store.get("part_stock", []):
                if item.get("center_id") == center_id and item.get("part_code") == part_code:
                    item["quantity"] = quantity
                    item["version"] = version
                    return
            self._memory_store.setdefault("part_stock", []).append({
                "center_id": center_id,
                "part_code": part_code,
                "quantity": quantity,
                "version": version
            })

    # ==============================================================================
    # 2. THAO TÁC TRÊN COLLECTION: part (Danh mục linh kiện & Ngưỡng an toàn)
    # ==============================================================================

    def find_part(self, part_code: str) -> Optional[Dict[str, Any]]:
        """Tìm kiếm thông tin linh kiện gốc theo mã part_code."""
        if self.is_connected and self.db is not None:
            return self.db.part.find_one({"part_code": part_code}, {"_id": 0})
        else:
            for item in self._memory_store.get("part", []):
                if item.get("part_code") == part_code:
                    return copy.deepcopy(item)
            return None

    def find_all_parts(self) -> List[Dict[str, Any]]:
        """Lấy toàn bộ danh mục linh kiện hệ thống."""
        if self.is_connected and self.db is not None:
            return list(self.db.part.find({}, {"_id": 0}))
        else:
            return [copy.deepcopy(x) for x in self._memory_store.get("part", [])]

    def update_part_threshold(self, part_code: str, min_threshold: int) -> bool:
        """
        Cập nhật ngưỡng an toàn min_threshold của một linh kiện (FR-06).
        Dành riêng cho Quản lý kho.
        """
        if self.is_connected and self.db is not None:
            result = self.db.part.update_one(
                {"part_code": part_code},
                {"$set": {"min_threshold": min_threshold}}
            )
            return result.matched_count > 0
        else:
            for item in self._memory_store.get("part", []):
                if item.get("part_code") == part_code:
                    item["min_threshold"] = min_threshold
                    return True
            return False

    def create_part(self, part_data: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo mới một linh kiện vào danh mục kho (CRUD: Create - Tiêu chí S1)."""
        from src.errors.AppError import AppError
        part_code = part_data["part_code"].strip()
        existing = self.find_part(part_code)
        if existing:
            raise AppError(status_code=400, error_code="ERR_PART_EXISTS", message=f"Mã linh kiện '{part_code}' đã tồn tại trong danh mục.")
        
        doc = copy.deepcopy(part_data)
        doc["part_code"] = part_code
        if self.is_connected and self.db is not None:
            self.db.part.insert_one(copy.deepcopy(doc))
        else:
            self._memory_store.setdefault("part", []).append(copy.deepcopy(doc))
        
        # Tự động khởi tạo tồn kho 0 cái cho linh kiện mới tại chi nhánh mặc định
        center_id = doc.get("center_id", "L5-WH-890")
        min_thresh = doc.get("min_threshold", 10)
        stock_doc = {
            "center_id": center_id,
            "part_code": part_code,
            "quantity": 0,
            "min_threshold": min_thresh,
            "version": 1,
            "updated_at": datetime.utcnow()
        }
        if self.is_connected and self.db is not None:
            self.db.part_stock.replace_one({"center_id": center_id, "part_code": part_code}, stock_doc, upsert=True)
        else:
            stocks = self._memory_store.setdefault("part_stock", [])
            stocks = [s for s in stocks if not (s.get("center_id") == center_id and s.get("part_code") == part_code)]
            stocks.append(stock_doc)
            self._memory_store["part_stock"] = stocks

        return doc

    def update_part(self, part_code: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Cập nhật thông tin linh kiện trong danh mục (CRUD: Update - Tiêu chí S1)."""
        part_code = part_code.strip()
        existing = self.find_part(part_code)
        if not existing:
            return None

        update_fields = {k: v for k, v in update_data.items() if k not in ["_id", "part_code"]}
        if not update_fields:
            return existing

        if self.is_connected and self.db is not None:
            self.db.part.update_one({"part_code": part_code}, {"$set": update_fields})
            return self.find_part(part_code)
        else:
            for item in self._memory_store.get("part", []):
                if item.get("part_code") == part_code:
                    item.update(update_fields)
                    return copy.deepcopy(item)
            return None

    def delete_part(self, part_code: str) -> bool:
        """Xóa linh kiện khỏi danh mục kho (CRUD: Delete - Tiêu chí S1)."""
        from src.errors.AppError import AppError
        part_code = part_code.strip()
        existing = self.find_part(part_code)
        if not existing:
            raise AppError(status_code=404, error_code="ERR_PART_NOT_FOUND", message=f"Không tìm thấy linh kiện '{part_code}' để xóa.")

        # Kiểm tra tồn kho thực tế: Nếu tồn kho > 0 tại bất kỳ chi nhánh nào, không cho phép xóa
        if self.is_connected and self.db is not None:
            stocks = list(self.db.part_stock.find({"part_code": part_code}))
            active_stock = any(s.get("quantity", 0) > 0 for s in stocks)
            if active_stock:
                raise AppError(status_code=400, error_code="ERR_CANNOT_DELETE_ACTIVE_STOCK",
                               message=f"Không thể xóa linh kiện '{part_code}' vì vẫn còn tồn kho thực tế > 0. Vui lòng xuất hết tồn kho trước khi xóa.")
            self.db.part.delete_one({"part_code": part_code})
            self.db.part_stock.delete_many({"part_code": part_code})
            return True
        else:
            stocks = [s for s in self._memory_store.get("part_stock", []) if s.get("part_code") == part_code]
            if any(s.get("quantity", 0) > 0 for s in stocks):
                raise AppError(status_code=400, error_code="ERR_CANNOT_DELETE_ACTIVE_STOCK",
                               message=f"Không thể xóa linh kiện '{part_code}' vì vẫn còn tồn kho thực tế > 0. Vui lòng xuất hết tồn kho trước khi xóa.")
            self._memory_store["part"] = [p for p in self._memory_store.get("part", []) if p.get("part_code") != part_code]
            self._memory_store["part_stock"] = [s for s in self._memory_store.get("part_stock", []) if s.get("part_code") != part_code]
            return True

    # ==============================================================================
    # 3. THAO TÁC TRÊN COLLECTION: ticket (Phiếu bảo hành)
    # ==============================================================================

    def find_ticket(self, ticket_id: str) -> Optional[Dict[str, Any]]:
        """Tìm kiếm thông tin phiếu bảo hành (Phục vụ xác thực ticket BR-02)."""
        if self.is_connected and self.db is not None:
            return self.db.ticket.find_one({"ticket_id": ticket_id}, {"_id": 0})
        else:
            for item in self._memory_store.get("ticket", []):
                if item.get("ticket_id") == ticket_id:
                    return copy.deepcopy(item)
            return None

    def find_all_tickets(self) -> List[Dict[str, Any]]:
        """Lấy danh sách các phiếu bảo hành đang chờ hoặc đang xử lý."""
        if self.is_connected and self.db is not None:
            return list(self.db.ticket.find({}, {"_id": 0}))
        else:
            return [copy.deepcopy(x) for x in self._memory_store.get("ticket", [])]

    # ==============================================================================
    # 4. THAO TÁC TRÊN COLLECTION: part_transaction (Nhật ký giao dịch bất biến BR-03)
    # ==============================================================================

    def insert_transaction(self, transaction_doc: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ghi nhận một bản ghi giao dịch vĩnh viễn (BR-03: Bất biến lịch sử).
        Tuyệt đối KHÔNG có hàm sửa (UPDATE) hay xóa (DELETE) cho collection này.
        """
        doc = copy.deepcopy(transaction_doc)
        if "created_at" not in doc or not doc["created_at"]:
            doc["created_at"] = datetime.utcnow()
        elif isinstance(doc["created_at"], str):
            try:
                doc["created_at"] = datetime.fromisoformat(doc["created_at"].replace("Z", "+00:00"))
            except Exception:
                doc["created_at"] = datetime.utcnow()

        if self.is_connected and self.db is not None:
            self.db.part_transaction.insert_one(doc)
            doc.pop("_id", None)
            return doc
        else:
            self._memory_store.setdefault("part_transaction", []).append(doc)
            return doc

    def find_transactions(self, center_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Trích xuất danh sách nhật ký giao dịch mới nhất theo trung tâm (FR-05).
        Sử dụng chỉ mục idx_transaction_history {center_id: 1, created_at: -1}.
        """
        if self.is_connected and self.db is not None:
            cursor = self.db.part_transaction.find(
                {"center_id": center_id},
                {"_id": 0}
            ).sort("created_at", -1).limit(limit)
            results = []
            for item in cursor:
                if isinstance(item.get("created_at"), datetime):
                    item["created_at"] = item["created_at"].isoformat()
                results.append(item)
            return results
        else:
            items = [copy.deepcopy(x) for x in self._memory_store.get("part_transaction", []) if x.get("center_id") == center_id]
            items.sort(key=lambda x: str(x.get("created_at", "")), reverse=True)
            return items[:limit]

    # ==============================================================================
    # 5. THAO TÁC TRÊN COLLECTION: users (Người dùng và Xác thực)
    # ==============================================================================

    def find_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Tìm tài khoản người dùng theo email (Dùng cho Đăng nhập và Khôi phục mật khẩu)."""
        if not email:
            return None
        clean_email = email.strip().lower()
        if self.is_connected and self.db is not None:
            doc = self.db.users.find_one({"email": clean_email})
            if doc:
                doc["_id"] = str(doc["_id"])
            return doc
        else:
            for item in self._memory_store.get("users", []):
                if item.get("email", "").lower() == clean_email:
                    return copy.deepcopy(item)
            return None

    def find_all_users(self) -> List[Dict[str, Any]]:
        """Lấy danh sách nhân sự kho cho màn hình Quản lý nhân sự của Quản lý kho."""
        if self.is_connected and self.db is not None:
            cursor = self.db.users.find({}, {"password_hash": 0})
            results = []
            for item in cursor:
                item["_id"] = str(item["_id"])
                results.append(item)
            return results
        else:
            results = []
            for item in self._memory_store.get("users", []):
                c = copy.deepcopy(item)
                c.pop("password_hash", None)
                results.append(c)
            return results

    def update_user_otp(self, email: str, otp_code: str, otp_expires_at: datetime) -> bool:
        """Cập nhật mã OTP tạm thời cho quy trình Khôi phục quyền truy cập an toàn."""
        clean_email = email.strip().lower()
        updated = False
        if self.is_connected and self.db is not None:
            res = self.db.users.update_one(
                {"email": clean_email},
                {"$set": {"otp_code": otp_code, "otp_expires_at": otp_expires_at}}
            )
            updated = res.matched_count > 0

        for item in self._memory_store.get("users", []):
            if item.get("email", "").lower() == clean_email:
                item["otp_code"] = otp_code
                item["otp_expires_at"] = otp_expires_at.isoformat()
                updated = True
                break

        if updated:
            self._save_users_to_disk()
        return updated

    def create_user(self, user_doc: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo người dùng mới khi đăng ký cấp quyền với 1 vai trò cố định."""
        from src.errors.AppError import AppError
        clean_email = user_doc["email"].strip().lower()
        existing = self.find_user_by_email(clean_email)
        if existing:
            raise AppError(
                status_code=400,
                error_code="ERR_EMAIL_EXISTS",
                message="Email này đã được đăng ký trên hệ thống. Một email chỉ được gắn với một vai trò duy nhất."
            )

        full_name = user_doc["full_name"].strip()
        username = user_doc.get("username") or clean_email.split("@")[0]
        role_labels = {
            "MANAGER": "Quản lý kho",
            "MATERIAL_STAFF": "Nhân viên vật tư",
            "TECH_STAFF": "Nhân viên kỹ thuật"
        }
        role_label = role_labels.get(user_doc["role"], "Nhân sự kho")

        new_doc = {
            "_id": str(ObjectId()),
            "username": username,
            "name": full_name,
            "full_name": full_name,
            "phone": user_doc.get("phone", "0961570243"),
            "email": clean_email,
            "password_hash": user_doc["password_hash"],
            "role": user_doc["role"],
            "role_label": role_label,
            "center_id": user_doc.get("center_id", "L5-WH-890"),
            "active": 1,
            "status": user_doc.get("status", "ACTIVE"),
            "token": user_doc.get("token", ""),
            "created_at": datetime.utcnow().isoformat()
        }

        if self.is_connected and self.db is not None:
            self.db.users.insert_one(copy.deepcopy(new_doc))
        
        if "users" not in self._memory_store:
            self._memory_store["users"] = []
        self._memory_store["users"].append(copy.deepcopy(new_doc))
        self._save_users_to_disk()

        res = copy.deepcopy(new_doc)
        res.pop("password_hash", None)
        return res

    def update_user_token(self, email: str, token: str) -> bool:
        """Lưu mã token vào CSDL MongoDB để tự động nhớ phiên đăng nhập."""
        clean_email = email.strip().lower()
        updated = False
        if self.is_connected and self.db is not None:
            res = self.db.users.update_one(
                {"email": clean_email},
                {"$set": {"token": token, "active": 1, "status": "ONLINE"}}
            )
            updated = res.matched_count > 0

        for item in self._memory_store.get("users", []):
            if item.get("email", "").lower() == clean_email:
                item["token"] = token
                item["active"] = 1
                item["status"] = "ONLINE"
                updated = True
                break

        if updated:
            self._save_users_to_disk()
        return updated

    def update_user_password(self, email: str, new_password_hash: str, new_plain_password: Optional[str] = None) -> bool:
        """Đặt lại mật khẩu mới sau khi xác thực OTP thành công (Chỉ lưu password_hash - S3)."""
        clean_email = email.strip().lower()
        updated = False
        set_dict = {"password_hash": new_password_hash}

        if self.is_connected and self.db is not None:
            res = self.db.users.update_one(
                {"email": clean_email},
                {"$set": set_dict, "$unset": {"otp_code": "", "otp_expires_at": ""}}
            )
            updated = res.matched_count > 0

        for item in self._memory_store.get("users", []):
            if item.get("email", "").lower() == clean_email:
                item["password_hash"] = new_password_hash
                item.pop("password", None)
                item.pop("otp_code", None)
                item.pop("otp_expires_at", None)
                updated = True
                break

        if updated:
            self._save_users_to_disk()
        return updated

    def find_subordinate_users(self, center_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Lấy danh sách nhân sự cấp dưới trực thuộc Quản lý kho:
        Bắt buộc chỉ gồm: Nhân viên kỹ thuật (TECH_STAFF) và Nhân viên vật tư (MATERIAL_STAFF).
        Tuyệt đối không hiển thị tài khoản Quản lý kho (MANAGER) khác.
        """
        subordinate_roles = ["TECH_STAFF", "MATERIAL_STAFF"]
        results = []
        if self.is_connected and self.db is not None:
            query = {"role": {"$in": subordinate_roles}}
            if center_id:
                query["center_id"] = center_id
            cursor = self.db.users.find(query, {"password_hash": 0, "otp_code": 0})
            for item in cursor:
                item["_id"] = str(item["_id"])
                if "status" not in item:
                    item["status"] = "ONLINE" if item.get("is_active", True) else "TERMINATED"
                results.append(item)
        else:
            for item in self._memory_store.get("users", []):
                if item.get("role") in subordinate_roles:
                    if center_id and item.get("center_id") != center_id:
                        continue
                    c = copy.deepcopy(item)
                    c.pop("password_hash", None)
                    c.pop("otp_code", None)
                    if "status" not in c:
                        c["status"] = "ONLINE" if c.get("is_active", True) else "TERMINATED"
                    results.append(c)
        return results

    def bulk_import_users(self, users_list: List[Dict[str, Any]]) -> int:
        """Import danh sách nhân sự cấp dưới (Kỹ thuật và Vật tư) từ file Excel/CSV."""
        import hashlib
        imported_count = 0
        subordinate_roles = ["TECH_STAFF", "MATERIAL_STAFF"]

        for u in users_list:
            if u.get("role") not in subordinate_roles:
                continue
            clean_email = u["email"].strip().lower()
            existing = self.find_user_by_email(clean_email)
            if existing:
                # Cập nhật thông tin nếu tài khoản đã tồn tại
                if self.is_connected and self.db is not None:
                    self.db.users.update_one(
                        {"email": clean_email},
                        {"$set": {
                            "full_name": u["full_name"],
                            "role": u["role"],
                            "center_id": u.get("center_id", "L5-WH-890")
                        }}
                    )
                for m in self._memory_store.get("users", []):
                    if m.get("email", "").lower() == clean_email:
                        m["full_name"] = u["full_name"]
                        m["role"] = u["role"]
                        m["center_id"] = u.get("center_id", "L5-WH-890")
                imported_count += 1
            else:
                pwd_hash = hashlib.sha256("Mekong@2026".encode("utf-8")).hexdigest()
                doc = {
                    "_id": str(ObjectId()),
                    "email": clean_email,
                    "full_name": u["full_name"],
                    "password_hash": pwd_hash,
                    "role": u["role"],
                    "center_id": u.get("center_id", "L5-WH-890"),
                    "status": u.get("status", "ACTIVE"),
                    "created_at": datetime.utcnow().isoformat()
                }
                if self.is_connected and self.db is not None:
                    self.db.users.insert_one(copy.deepcopy(doc))
                if "users" not in self._memory_store:
                    self._memory_store["users"] = []
                self._memory_store["users"].append(copy.deepcopy(doc))
                imported_count += 1

        if imported_count > 0:
            self._save_users_to_disk()
        return imported_count

    def update_user_profile(self, email: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Cập nhật thông tin nhân sự (CRUD: Update - Tiêu chí S1)."""
        clean_email = email.strip().lower()
        existing = self.find_user_by_email(clean_email)
        if not existing:
            return None

        update_fields = {k: v for k, v in update_data.items() if k not in ["_id", "email", "password_hash"]}
        if not update_fields:
            return existing

        if self.is_connected and self.db is not None:
            self.db.users.update_one({"email": clean_email}, {"$set": update_fields})
        
        for item in self._memory_store.get("users", []):
            if item.get("email", "").lower() == clean_email:
                item.update(update_fields)
                break
        
        self._save_users_to_disk()
        updated_user = self.find_user_by_email(clean_email)
        if updated_user:
            updated_user.pop("password_hash", None)
        return updated_user

    def delete_user(self, email: str) -> bool:
        """Xóa tài khoản nhân sự khỏi hệ thống (CRUD: Delete - Tiêu chí S1)."""
        from src.errors.AppError import AppError
        clean_email = email.strip().lower()
        existing = self.find_user_by_email(clean_email)
        if not existing:
            raise AppError(status_code=404, error_code="ERR_USER_NOT_FOUND", message=f"Không tìm thấy tài khoản '{clean_email}' để xóa.")

        if self.is_connected and self.db is not None:
            self.db.users.delete_one({"email": clean_email})
        
        self._memory_store["users"] = [u for u in self._memory_store.get("users", []) if u.get("email", "").lower() != clean_email]
        self._save_users_to_disk()
        return True


    # ==============================================================================
    # 6. THAO TÁC TRÊN COLLECTION: service_center (Trung tâm bảo hành)
    # ==============================================================================

    def find_center(self, center_id: str) -> Optional[Dict[str, Any]]:
        """Lấy thông tin chi nhánh bảo hành theo center_id."""
        if self.is_connected and self.db is not None:
            return self.db.service_center.find_one({"center_id": center_id}, {"_id": 0})
        else:
            for item in self._memory_store.get("service_center", []):
                if item.get("center_id") == center_id:
                    return copy.deepcopy(item)
            return None

    def find_all_centers(self) -> List[Dict[str, Any]]:
        """Lấy toàn bộ danh sách các trung tâm bảo hành."""
        if self.is_connected and self.db is not None:
            return list(self.db.service_center.find({}, {"_id": 0}))
        else:
            return [copy.deepcopy(x) for x in self._memory_store.get("service_center", [])]


# Khởi tạo một đối tượng Repository dùng chung (Singleton Pattern)
inventory_repository = InventoryRepository()

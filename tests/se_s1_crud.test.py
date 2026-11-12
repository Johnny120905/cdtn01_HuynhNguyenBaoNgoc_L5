"""
File: tests/se_s1_crud.test.py
Dự án: Hệ thống Smart CRM – Mekong Mobile (Luồng 05: Kho linh kiện thay thế)
Mục đích: Kiểm chứng toàn diện Tiêu chí SE S1 (Bảng 4.2 Đề bài BT2):
  - [SE] S1: >= 2 thực thể có đủ bốn thao tác CRUD (Create, Read, Update, Delete).
  - Thực thể 1: part (Linh kiện kho)
      + C: POST   /api/v1/inventory/parts
      + R: GET    /api/v1/inventory/parts/{part_code} (và GET /parts)
      + U: PUT    /api/v1/inventory/parts/{part_code}
      + D: DELETE /api/v1/inventory/parts/{part_code}
  - Thực thể 2: users (Tài khoản nhân sự)
      + C: POST   /api/v1/inventory/users
      + R: GET    /api/v1/inventory/users/{email} (và GET /users)
      + U: PUT    /api/v1/inventory/users/{email}
      + D: DELETE /api/v1/inventory/users/{email}
"""

import os
import sys
import unittest
from datetime import datetime, timedelta
import jwt

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fastapi.testclient import TestClient
from src.app import app
from src.repositories import inventory_repository

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "mekong_mobile_secret_jwt_key_2026_cdtn01")
JWT_ALGORITHM = "HS256"


class TestSES1CRUD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        
        # Sinh Token Quản lý kho
        mgr_payload = {
            "email": "lethithuyngan985@gmail.com",
            "role": "MANAGER",
            "center_id": "L5-WH-890",
            "exp": datetime.utcnow() + timedelta(hours=2)
        }
        cls.manager_token = jwt.encode(mgr_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        cls.manager_headers = {"Authorization": f"Bearer {cls.manager_token}"}

        # Sinh Token Kỹ thuật viên (để kiểm tra phân quyền bảo vệ CRUD)
        tech_payload = {
            "email": "vuthelong1009@gmail.com",
            "role": "TECH_STAFF",
            "center_id": "L5-WH-890",
            "exp": datetime.utcnow() + timedelta(hours=2)
        }
        cls.tech_token = jwt.encode(tech_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        cls.tech_headers = {"Authorization": f"Bearer {cls.tech_token}"}

    def setUp(self):
        # Dọn dẹp dữ liệu test mẫu nếu còn tồn đọng
        test_part_code = "PRT-TEST-S1-01"
        test_user_email = "nv.test.crud@gmail.com"
        
        if inventory_repository.is_connected and inventory_repository.db is not None:
            inventory_repository.db.part.delete_one({"part_code": test_part_code})
            inventory_repository.db.part_stock.delete_many({"part_code": test_part_code})
            inventory_repository.db.users.delete_one({"email": test_user_email})
        
        if "part" in inventory_repository._memory_store:
            inventory_repository._memory_store["part"] = [
                p for p in inventory_repository._memory_store["part"] if p.get("part_code") != test_part_code
            ]
        if "part_stock" in inventory_repository._memory_store:
            inventory_repository._memory_store["part_stock"] = [
                s for s in inventory_repository._memory_store["part_stock"] if s.get("part_code") != test_part_code
            ]
        if "users" in inventory_repository._memory_store:
            inventory_repository._memory_store["users"] = [
                u for u in inventory_repository._memory_store["users"] if u.get("email") != test_user_email
            ]

    # ==============================================================================
    # 1. KIỂM THỬ ĐẦY ĐỦ 4 THAO TÁC CRUD CHO THỰC THỂ 1: PART (LINH KIỆN KHO)
    # ==============================================================================

    def test_01_crud_part_c_create_success(self):
        """[S1 - Part - CREATE]: Thêm mới một linh kiện vào danh mục kho."""
        payload = {
            "part_code": "PRT-TEST-S1-01",
            "part_name": "Màn hình OLED Test S1 CRUD",
            "category": "Màn hình",
            "compatible_model": "iPhone 15 Pro Max",
            "supplier": "Foxconn VN",
            "unit": "Bộ",
            "min_threshold": 12,
            "center_id": "L5-WH-890"
        }
        res = self.client.post("/api/v1/inventory/parts", json=payload, headers=self.manager_headers)
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["part_code"], "PRT-TEST-S1-01")
        self.assertEqual(data["data"]["min_threshold"], 12)

    def test_02_crud_part_r_read_detail_success(self):
        """[S1 - Part - READ]: Tra cứu chi tiết một linh kiện theo mã."""
        # Tạo trước bản ghi
        self.test_01_crud_part_c_create_success()

        res = self.client.get("/api/v1/inventory/parts/PRT-TEST-S1-01", headers=self.manager_headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["part_code"], "PRT-TEST-S1-01")
        self.assertEqual(data["data"]["part_name"], "Màn hình OLED Test S1 CRUD")

    def test_03_crud_part_u_update_success(self):
        """[S1 - Part - UPDATE]: Cập nhật thông tin linh kiện."""
        # Tạo trước bản ghi
        self.test_01_crud_part_c_create_success()

        update_payload = {
            "part_name": "Màn hình OLED Test S1 (Đã nâng cấp gen 2)",
            "min_threshold": 18,
            "supplier": "Foxconn Global"
        }
        res = self.client.put("/api/v1/inventory/parts/PRT-TEST-S1-01", json=update_payload, headers=self.manager_headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["part_name"], "Màn hình OLED Test S1 (Đã nâng cấp gen 2)")
        self.assertEqual(data["data"]["min_threshold"], 18)
        self.assertEqual(data["data"]["supplier"], "Foxconn Global")

    def test_04_crud_part_d_delete_safety_guard_reject_active_stock(self):
        """[S1 - Part - DELETE Ràng buộc an toàn]: Từ chối xóa linh kiện nếu tồn kho thực tế > 0."""
        # Tạo linh kiện có tồn kho thực tế (nhập 5 cái)
        self.test_01_crud_part_c_create_success()
        stock_doc = {
            "center_id": "L5-WH-890",
            "part_code": "PRT-TEST-S1-01",
            "quantity": 5,
            "min_threshold": 12,
            "version": 1
        }
        if inventory_repository.is_connected and inventory_repository.db is not None:
            inventory_repository.db.part_stock.replace_one({"center_id": "L5-WH-890", "part_code": "PRT-TEST-S1-01"}, stock_doc, upsert=True)
        else:
            stocks = [s for s in inventory_repository._memory_store.get("part_stock", []) if not (s.get("center_id") == "L5-WH-890" and s.get("part_code") == "PRT-TEST-S1-01")]
            stocks.append(stock_doc)
            inventory_repository._memory_store["part_stock"] = stocks

        # Thử xóa khi tồn kho > 0 -> Bị từ chối với lỗi 400
        res = self.client.delete("/api/v1/inventory/parts/PRT-TEST-S1-01", headers=self.manager_headers)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["error_code"], "ERR_CANNOT_DELETE_ACTIVE_STOCK")

    def test_05_crud_part_d_delete_success(self):
        """[S1 - Part - DELETE]: Xóa thành công linh kiện khi tồn kho = 0."""
        self.test_01_crud_part_c_create_success()

        res = self.client.delete("/api/v1/inventory/parts/PRT-TEST-S1-01", headers=self.manager_headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "success")

        # Kiểm chứng sau khi xóa: Tra cứu lại phải trả về 404
        check_res = self.client.get("/api/v1/inventory/parts/PRT-TEST-S1-01", headers=self.manager_headers)
        self.assertEqual(check_res.status_code, 404)

    # ==============================================================================
    # 2. KIỂM THỬ ĐẦY ĐỦ 4 THAO TÁC CRUD CHO THỰC THỂ 2: USERS (NHÂN SỰ KHO)
    # ==============================================================================

    def test_06_crud_user_c_create_success(self):
        """[S1 - User - CREATE]: Quản lý kho tạo mới tài khoản nhân sự cấp dưới."""
        payload = {
            "full_name": "Nguyễn Văn Test CRUD",
            "email": "nv.test.crud@gmail.com",
            "password": "Password123@",
            "role": "TECH_STAFF",
            "center_id": "L5-WH-890"
        }
        res = self.client.post("/api/v1/inventory/users", json=payload, headers=self.manager_headers)
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["email"], "nv.test.crud@gmail.com")
        self.assertEqual(data["data"]["role"], "TECH_STAFF")
        self.assertNotIn("password_hash", data["data"])  # Tiêu chí S3: Không lộ hash

    def test_07_crud_user_r_read_detail_success(self):
        """[S1 - User - READ]: Tra cứu chi tiết tài khoản nhân sự theo email."""
        self.test_06_crud_user_c_create_success()

        res = self.client.get("/api/v1/inventory/users/nv.test.crud@gmail.com", headers=self.manager_headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["email"], "nv.test.crud@gmail.com")
        self.assertEqual(data["data"]["full_name"], "Nguyễn Văn Test CRUD")
        self.assertNotIn("password_hash", data["data"])

    def test_08_crud_user_u_update_success(self):
        """[S1 - User - UPDATE]: Cập nhật thông tin hồ sơ nhân sự (họ tên, sđt, trạng thái)."""
        self.test_06_crud_user_c_create_success()

        update_payload = {
            "full_name": "Nguyễn Văn Test CRUD (Đã Cập Nhật)",
            "phone": "0988776655",
            "status": "ONLINE"
        }
        res = self.client.put("/api/v1/inventory/users/nv.test.crud@gmail.com", json=update_payload, headers=self.manager_headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["full_name"], "Nguyễn Văn Test CRUD (Đã Cập Nhật)")
        self.assertEqual(data["data"]["phone"], "0988776655")
        self.assertEqual(data["data"]["status"], "ONLINE")

    def test_09_crud_user_d_delete_self_guard_rejected(self):
        """[S1 - User - DELETE Ràng buộc an toàn]: Không được phép tự xóa tài khoản của chính mình."""
        res = self.client.delete("/api/v1/inventory/users/lethithuyngan985@gmail.com", headers=self.manager_headers)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["error_code"], "ERR_CANNOT_DELETE_SELF")

    def test_10_crud_user_d_delete_success(self):
        """[S1 - User - DELETE]: Xóa thành công tài khoản nhân sự cấp dưới."""
        self.test_06_crud_user_c_create_success()

        res = self.client.delete("/api/v1/inventory/users/nv.test.crud@gmail.com", headers=self.manager_headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "success")

        # Kiểm chứng sau khi xóa: Tra cứu lại phải trả về 404
        check_res = self.client.get("/api/v1/inventory/users/nv.test.crud@gmail.com", headers=self.manager_headers)
        self.assertEqual(check_res.status_code, 404)

    def test_11_crud_role_protection_for_tech_staff(self):
        """[S1 - Phân quyền]: Kỹ thuật viên không có quyền xóa linh kiện hoặc quản lý nhân sự."""
        # Thử xóa linh kiện -> Bị từ chối 403
        res = self.client.delete("/api/v1/inventory/parts/PRT-IP15-SCR", headers=self.tech_headers)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json()["error_code"], "ERR_UNAUTHORIZED_ROLE")

        # Thử thêm nhân sự -> Bị từ chối 403
        payload = {
            "full_name": "Hacker Tech",
            "email": "hacker@gmail.com",
            "password": "Password123@",
            "role": "TECH_STAFF"
        }
        res2 = self.client.post("/api/v1/inventory/users", json=payload, headers=self.tech_headers)
        self.assertEqual(res2.status_code, 403)
        self.assertEqual(res2.json()["error_code"], "ERR_UNAUTHORIZED_ROLE")


if __name__ == "__main__":
    unittest.main()

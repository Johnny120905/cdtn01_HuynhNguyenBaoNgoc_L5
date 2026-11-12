"""
File: tests/auth_and_user.test.py
Mục đích: Kiểm thử tự động các tính năng Xác thực và Quản lý nhân sự mới:
  1. Đăng ký cấp quyền (Họ tên, email chuẩn, password >= 8 ký tự, role: TECH_STAFF, MATERIAL_STAFF, MANAGER).
  2. Ràng buộc 1 email chỉ được cấp 1 vai trò duy nhất.
  3. Đăng nhập thành công và chặn đăng nhập sai mật khẩu.
  4. Quên mật khẩu & cấp mã OTP 6 số, đặt lại mật khẩu mới >= 8 ký tự.
  5. Quản lý kho xem nhân sự cấp dưới (chỉ thấy TECH_STAFF và MATERIAL_STAFF).
  6. Quản lý kho import danh sách nhân sự cấp dưới.
"""

import os
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fastapi.testclient import TestClient
from src.app import app
from src.repositories import inventory_repository



class TestAuthAndUserManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_emails = {"test.kythuat.new@gmail.com", "kt2.import@gmail.com", "vt2.import@gmail.com"}
        if inventory_repository.is_connected and inventory_repository.db is not None:
            inventory_repository.db.users.delete_many({"email": {"$in": list(test_emails)}})
        if "users" in inventory_repository._memory_store:
            inventory_repository._memory_store["users"] = [
                u for u in inventory_repository._memory_store["users"] if u.get("email") not in test_emails
            ]
            inventory_repository._save_users_to_disk()

    @classmethod
    def tearDownClass(cls):
        test_emails = {"test.kythuat.new@gmail.com", "kt2.import@gmail.com", "vt2.import@gmail.com"}
        if inventory_repository.is_connected and inventory_repository.db is not None:
            inventory_repository.db.users.delete_many({"email": {"$in": list(test_emails)}})
        if "users" in inventory_repository._memory_store:
            inventory_repository._memory_store["users"] = [
                u for u in inventory_repository._memory_store["users"] if u.get("email") not in test_emails
            ]
            inventory_repository._save_users_to_disk()

    def setUp(self):
        self.client = TestClient(app)

    def test_01_register_success_for_tech_staff(self):
        """Đăng ký tài khoản kỹ thuật viên mới với email hợp lệ và mật khẩu >= 8 ký tự."""
        payload = {
            "full_name": "Nguyễn Văn Test Kỹ Thuật",
            "email": "test.kythuat.new@gmail.com",
            "password": "Password123@",
            "role": "TECH_STAFF",
            "center_id": "L5-WH-890"
        }
        res = self.client.post("/api/v1/auth/register", json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("token", data)
        self.assertEqual(data["user"]["role"], "TECH_STAFF")
        self.assertEqual(data["user"]["email"], "test.kythuat.new@gmail.com")

    def test_02_register_reject_short_password(self):
        """Từ chối đăng ký khi mật khẩu dưới 8 ký tự."""
        payload = {
            "full_name": "Trần Văn Ngắn",
            "email": "test.short@gmail.com",
            "password": "123",  # < 8 ký tự
            "role": "TECH_STAFF"
        }
        res = self.client.post("/api/v1/auth/register", json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertIn("ERR_WEAK_PASSWORD", res.json()["error_code"])

    def test_02a_register_reject_missing_uppercase(self):
        """Từ chối đăng ký khi mật khẩu thiếu chữ in hoa."""
        payload = {
            "full_name": "Trần Văn Thiếu Hoa",
            "email": "test.no_upper@gmail.com",
            "password": "password123@",  # thiếu chữ in hoa
            "role": "TECH_STAFF"
        }
        res = self.client.post("/api/v1/auth/register", json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertIn("ERR_WEAK_PASSWORD", res.json()["error_code"])

    def test_02b_register_reject_missing_lowercase(self):
        """Từ chối đăng ký khi mật khẩu thiếu chữ in thường."""
        payload = {
            "full_name": "Trần Văn Thiếu Thường",
            "email": "test.no_lower@gmail.com",
            "password": "PASSWORD123@",  # thiếu chữ in thường
            "role": "TECH_STAFF"
        }
        res = self.client.post("/api/v1/auth/register", json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertIn("ERR_WEAK_PASSWORD", res.json()["error_code"])

    def test_02c_register_reject_missing_digit(self):
        """Từ chối đăng ký khi mật khẩu thiếu chữ số."""
        payload = {
            "full_name": "Trần Văn Thiếu Số",
            "email": "test.no_digit@gmail.com",
            "password": "Password@@@@",  # thiếu chữ số
            "role": "TECH_STAFF"
        }
        res = self.client.post("/api/v1/auth/register", json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertIn("ERR_WEAK_PASSWORD", res.json()["error_code"])

    def test_02d_register_reject_missing_special(self):
        """Từ chối đăng ký khi mật khẩu thiếu ký hiệu đặc biệt."""
        payload = {
            "full_name": "Trần Văn Thiếu Ký Tự",
            "email": "test.no_special@gmail.com",
            "password": "Password123",  # thiếu ký hiệu đặc biệt
            "role": "TECH_STAFF"
        }
        res = self.client.post("/api/v1/auth/register", json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertIn("ERR_WEAK_PASSWORD", res.json()["error_code"])

    def test_03_register_duplicate_email_forbidden(self):
        """Từ chối đăng ký lại một email đã tồn tại (1 email = 1 role)."""
        payload = {
            "full_name": "Nguyễn Văn Trùng",
            "email": "test.kythuat.new@gmail.com",
            "password": "Password123@",
            "role": "MATERIAL_STAFF"
        }
        res = self.client.post("/api/v1/auth/register", json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["error_code"], "ERR_EMAIL_EXISTS")

    def test_04_login_success(self):
        """Đăng nhập thành công với tài khoản vừa tạo."""
        payload = {
            "email": "test.kythuat.new@gmail.com",
            "password": "Password123@"
        }
        res = self.client.post("/api/v1/auth/login", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("token", data)
        self.assertEqual(data["user"]["role"], "TECH_STAFF")

    def test_05_login_wrong_password(self):
        """Đăng nhập thất bại khi sai mật khẩu."""
        payload = {
            "email": "test.kythuat.new@gmail.com",
            "password": "WrongPassword123@"
        }
        res = self.client.post("/api/v1/auth/login", json=payload)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json()["error_code"], "ERR_WRONG_PASSWORD")

    def test_06_forgot_password_and_reset_with_otp(self):
        """Quy trình quên mật khẩu: nhận mã OTP 6 số và đặt lại mật khẩu mới >= 8 ký tự."""
        # 0. Đảm bảo tài khoản tồn tại (tiền điều kiện độc lập cho test case)
        self.client.post("/api/v1/auth/register", json={
            "full_name": "Kỹ thuật viên Test OTP",
            "email": "test.kythuat.new@gmail.com",
            "password": "Password123@",
            "role": "TECH_STAFF",
            "center_id": "L5-WH-890"
        })
        # 1. Gửi yêu cầu quên mật khẩu
        forgot_res = self.client.post("/api/v1/auth/forgot-password", json={"email": "test.kythuat.new@gmail.com"})
        self.assertEqual(forgot_res.status_code, 200)
        otp = forgot_res.json()["otp_demo"]
        self.assertEqual(len(otp), 6)

        # 2. Xác thực OTP và đặt lại mật khẩu mới
        reset_res = self.client.post("/api/v1/auth/reset-password", json={
            "email": "test.kythuat.new@gmail.com",
            "otp": otp,
            "new_password": "NewSecretPassword2026@"
        })
        self.assertEqual(reset_res.status_code, 200)

        # 3. Đăng nhập lại với mật khẩu mới
        login_new = self.client.post("/api/v1/auth/login", json={
            "email": "test.kythuat.new@gmail.com",
            "password": "NewSecretPassword2026@"
        })
        self.assertEqual(login_new.status_code, 200)

    def test_07_manager_view_subordinates_only(self):
        """Quản lý kho xem nhân sự cấp dưới: chỉ thấy TECH_STAFF và MATERIAL_STAFF."""
        # Lấy token của Manager
        login_mgr = self.client.post("/api/v1/auth/login", json={
            "email": "quanlykho.test@gmail.com",
            "password": "123456"
        })
        mgr_token = login_mgr.json()["token"]

        res = self.client.get("/api/v1/inventory/users/subordinates", headers={"Authorization": f"Bearer {mgr_token}"})
        self.assertEqual(res.status_code, 200)
        subordinates = res.json()["data"]
        self.assertGreater(len(subordinates), 0)
        for s in subordinates:
            self.assertIn(s["role"], ["TECH_STAFF", "MATERIAL_STAFF"])
            self.assertNotEqual(s["role"], "MANAGER")

    def test_08_manager_import_subordinates(self):
        """Quản lý kho tải file lên import danh sách nhân viên kỹ thuật và vật tư."""
        login_mgr = self.client.post("/api/v1/auth/login", json={
            "email": "quanlykho.test@gmail.com",
            "password": "123456"
        })
        mgr_token = login_mgr.json()["token"]

        import_payload = [
            {"full_name": "Phạm Văn Kỹ Thuật 2", "email": "kt2.import@gmail.com", "role": "TECH_STAFF"},
            {"full_name": "Hoàng Thị Vật Tư 2", "email": "vt2.import@gmail.com", "role": "MATERIAL_STAFF"}
        ]

        res = self.client.post(
            "/api/v1/inventory/users/import",
            json=import_payload,
            headers={"Authorization": f"Bearer {mgr_token}"}
        )
        self.assertEqual(res.status_code, 200)
    def test_09_login_terminated_user_rejected_with_403(self):
        """Từ chối đăng nhập đối với tài khoản đã thôi việc (TERMINATED) với mã lỗi 403."""
        # Tài khoản anhpham712002@gmail.com đã thôi việc (status=TERMINATED, is_active=false)
        res = self.client.post("/api/v1/auth/login", json={
            "email": "anhpham712002@gmail.com",
            "password": "Anhpham712002@"
        })
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json()["error_code"], "ERR_ACCOUNT_TERMINATED")

    def test_10_logout_sets_user_status_to_off_shift(self):
        """Đăng xuất tài khoản cập nhật trạng thái người dùng thành OFF_SHIFT (Nghỉ sau ca làm)."""
        res = self.client.post("/api/v1/auth/logout", json={
            "email": "test.kythuat.new@gmail.com",
            "reason": "OFF_SHIFT"
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "success")

    def test_11_max_length_constraints(self):
        """Kiểm tra các ràng buộc độ dài tối đa (Họ tên <= 50, Email <= 100, Mật khẩu <= 128)."""
        # Họ tên vượt quá 50 ký tự
        res_name = self.client.post("/api/v1/auth/register", json={
            "full_name": "A" * 51,
            "email": "valid.length@gmail.com",
            "password": "Password123@",
            "role": "TECH_STAFF"
        })
        self.assertEqual(res_name.status_code, 400)
        self.assertEqual(res_name.json()["error_code"], "ERR_INVALID_FULL_NAME")

        # Email vượt quá 100 ký tự (105 ký tự)
        long_email = ("b" * 95) + "@gmail.com"
        res_email = self.client.post("/api/v1/auth/register", json={
            "full_name": "Nguyen Van B",
            "email": long_email,
            "password": "Password123@",
            "role": "TECH_STAFF"
        })
        self.assertEqual(res_email.status_code, 400)
        self.assertEqual(res_email.json()["error_code"], "ERR_INVALID_EMAIL")


if __name__ == "__main__":
    unittest.main()


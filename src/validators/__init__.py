"""
File: src/validators/__init__.py
Mục đích: Module export cho Lớp Kiểm tra Dữ liệu (Validators).
Tải động tệp inventory.validator.py để Python có thể import trực tiếp.
"""

import os
import importlib.util

_file_path = os.path.join(os.path.dirname(__file__), "inventory.validator.py")
_spec = importlib.util.spec_from_file_location("inventory_validator_mod", _file_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

validate_stock_lookup = getattr(_mod, "validate_stock_lookup")
validate_transaction_payload = getattr(_mod, "validate_transaction_payload")
validate_threshold_payload = getattr(_mod, "validate_threshold_payload")
validate_register_payload = getattr(_mod, "validate_register_payload")
validate_login_payload = getattr(_mod, "validate_login_payload")
validate_forgot_password_payload = getattr(_mod, "validate_forgot_password_payload")
validate_reset_password_payload = getattr(_mod, "validate_reset_password_payload")
validate_user_import_payload = getattr(_mod, "validate_user_import_payload",
    "validate_password_complexity")
validate_part_create_payload = getattr(_mod, "validate_part_create_payload")
validate_part_update_payload = getattr(_mod, "validate_part_update_payload")
validate_user_update_payload = getattr(_mod, "validate_user_update_payload")
validate_password_complexity = getattr(_mod, "validate_password_complexity")

__all__ = [
    "validate_stock_lookup",
    "validate_transaction_payload",
    "validate_threshold_payload",
    "validate_register_payload",
    "validate_login_payload",
    "validate_forgot_password_payload",
    "validate_reset_password_payload",
    "validate_user_import_payload",
    "validate_password_complexity",
    "validate_part_create_payload",
    "validate_part_update_payload",
    "validate_user_update_payload"
]


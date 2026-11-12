@echo off
docker exec mekong_crm_l5_app pytest tests/cross_role_and_ui.test.py -k test_01 -v

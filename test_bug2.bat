@echo off
docker exec mekong_crm_l5_app pytest tests/auth_and_user.test.py -k test_06 -v

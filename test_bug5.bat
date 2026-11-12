@echo off
docker exec mekong_crm_l5_app pytest tests/se_s1_crud.test.py -v

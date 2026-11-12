@echo off
docker exec mekong_crm_l5_app pytest tests/bt3_specification_and_constraints.test.py -k test_09 -v

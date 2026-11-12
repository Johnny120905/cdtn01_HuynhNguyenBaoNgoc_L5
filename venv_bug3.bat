@echo off
python -m seeds.seed
python -m pytest tests/bt3_specification_and_constraints.test.py -k test_11 -v

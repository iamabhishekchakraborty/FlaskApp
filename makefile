help:
	@echo "    test_pytest"
	@echo "        Run unit tests (pytest) on the application"
    @echo "    test_unittest"
	@echo "        Run unit tests (unittest) on the application"

test_pytest:
    python3 -m pytest -vv

test_unittest:
    python3 unittest_flaskapp.py

include .env
.PHONY: pylint isort activeblack format check prepare-commit

#* Python Rules
run:
	python -m src.main

#* Git Rules
isort:
	isort --settings-path=$(MAKE_CONFIG_FILE) $(FORMAT_CHECK_SRC)

pylint:
	pylint --rcfile=$(PYLINT_CONFIG_FILE) $(FORMAT_CHECK_SRC)

activeblack:
	black $(FORMAT_CHECK_SRC)

format: activeblack isort

check: pylint isort

prepare-commit: format check
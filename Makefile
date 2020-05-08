
clean:
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf ./.cache .mypy_cache ./schema/.mypy_cache .coverage

PROJECT = widark
COVFILE ?= .coverage

coverage:
	mypy widark && pytest --cov-branch --cov=$(PROJECT) tests/ \
	--cov-report term-missing -x -s -vv -W ignore::DeprecationWarning

PART ?= patch

version:
	bump2version $(PART) $(PROJECT)/__init__.py --tag --commit

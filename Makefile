
clean:
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf ./.cache .mypy_cache ./schema/.mypy_cache .coverage

PROJECT = widark
COVFILE ?= .coverage

test:
	mypy widark && pytest tests/
	
coverage:
	mypy widark && pytest --cov-branch --cov=$(PROJECT) tests/ \
	--cov-report term-missing -vv

PART ?= patch

version:
	bump2version $(PART) pyproject.toml widark/__init__.py --tag --commit

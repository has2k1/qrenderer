.PHONY: clean-pyc clean-build doc clean visualize-tests build

clean: clean-build clean-cache clean-test

# Use uv (if it is installed) to run all python related commands,
# and prefere the active environment over .venv in a parent folder
ifeq ($(OS),Windows_NT)
  HAS_UV := $(if $(shell where uv 2>NUL),true,false)
else
  HAS_UV := $(if $(shell command -v uv 2>/dev/null),true,false)
endif

ifeq ($(HAS_UV),true)
  PYTHON ?= uv run --active python
  PIP ?= uv pip
  UVRUN ?= uv run --active
else
  PYTHON ?= python
  PIP ?= pip
  UVRUN ?=
endif

clean-build:
	rm -fr build/
	rm -fr dist/
	find . -name '*.egg-info' -exec rm -fr {} +

clean-cache:
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -f .coverage
	rm -f coverage.xml
	rm -fr htmlcov/

ruff:
	$(UVRUN) ruff check . $(args)

format:
	$(UVRUN) ruff format . --check

format-fix:
	$(UVRUN) ruff format .

lint: ruff

lint-fix:
	make lint args="--fix"

fix: format-fix lint-fix

typecheck:
	$(UVRUN) pyright

test: clean-test
	$(UVRUN) pytest

coverage:
	$(UVRUN) coverage report -m
	$(UVRUN) coverage html
	$(BROWSER) htmlcov/index.html

install: clean
	$(PIP) install "."

develop: clean-cache
	$(PIP) install -e ".[all]"

develop-update: clean-cache
	$(PIP) install --upgrade -e ".[all]"
	$(UVRUN) pre-commit autoupdate

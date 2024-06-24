.PHONY: clean-pyc clean-build doc clean visualize-tests build

clean: clean-build clean-cache clean-test

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
	ruff . $(args)

format:
	ruff format . --check

format-fix:
	ruff format .

lint: ruff

lint-fix:
	make lint args="--fix"

fix: format-fix lint-fix

typecheck:
	pyright

test: clean-test
	pytest

coverage:
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

install: clean
	pip install ".[extra]"

develop: clean-cache
	pip install -e ".[all]"

develop-update: clean-cache
	pip install --upgrade -e ".[all]"
	pre-commit autoupdate

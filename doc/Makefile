.PHONY: help Makefile
.DEFAULT_GOAL := help

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

define PRINT_HELP_PYSCRIPT
import re
import sys

target_pattern = re.compile(r"^([a-zA-Z1-9_-]+):.*?## (.*)$$")
for line in sys.stdin:
    match = target_pattern.match(line)
    if match:
        target, help = match.groups()
        print(f"{target:<20} {help}")
endef
export PRINT_HELP_PYSCRIPT


help:
	@$(PYTHON) -m  -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean:  ## Remove build artefacts
	rm -rf .quarto
	rm -rf reference/
	rm -rf _site/
	rm -rf _inv/

install-filters:  ## Install required pandoc filters
	$(UVRUN) quarto add --no-prompt has2k1/issuey
	$(UVRUN) quarto add --no-prompt has2k1/interlinks

install-stylesheets:  ## Install qrenderer stylesheet(s)
	$(PYTHON) -m qrenderer.stylesheets.install $(CURDIR)

install-all: install-filters install-stylesheets  ## Install All Dependencies

interlink:  ## Gather interlinks
	$(UVRUN) quartodoc interlinks

docstrings:   ## Generate qmd files from the docstrings
	$(UVRUN) quartodoc build --config _quarto.yml

html: docstrings  ## Build html site
	$(UVRUN) quarto render

doc: clean interlink html  ## Build html documentation from a clean slate

preview:  ## Preview html website
	$(UVRUN) quarto preview --port 42100 --no-browser

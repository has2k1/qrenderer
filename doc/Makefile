.PHONY: help Makefile
.DEFAULT_GOAL := help

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
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean:  ## Remove build artefacts
	rm -rf .quarto
	rm -rf reference/
	rm -rf _site/
	rm -rf _inv/

install-filters:  ## Install required pandoc filters
	quarto add --no-prompt has2k1/issuey
	quarto add --no-prompt has2k1/interlinks

interlink:  ## Gather interlinks
	quartodoc interlinks

docstrings:   ## Generate qmd files from the docstrings
	quartodoc build --config _quarto.yml

html: docstrings  ## Build html site
	quarto render

doc: clean interlink html  ## Build html documentation from a clean slate

preview:  ## Preview html website
	quarto preview --port 42100 --no-browser

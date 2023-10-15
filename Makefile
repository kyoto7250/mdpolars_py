SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help


style: ## format and lint
	poetry run black mdpolars/ tests/
	poetry run isort mdpolars/ tests/
	poetry run ruff  mdpolars/ tests/

test: ## exec pytest
	poetry run pytest --doctest-modules

build: ## build a dist
	poetry build


help: ## display this help screen
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


%:
	@echo 'command "$@" is not found.'
	@$(MAKE) help
	@exit 2

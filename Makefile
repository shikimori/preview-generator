
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(patsubst %/,%,$(dir $(mkfile_path)))

include .env
export $(shell sed 's/=.*//' .env)

help: ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

# ========== Poetry stuff ========== #
shell: ## Activate Poetry shell
	poetry shell

install_poetry: ## Install Poetry
	curl -sSL https://install.python-poetry.org | python3 -

version: ## Check Poetry version
	poetry --version

config: ## Poetry config token
	poetry config pypi-token.pypi $$PYPI

publish: ## Poetry build and publish
	poetry publish --build

# ========== Build ========== #
build: ## Build package
	poetry build

# ========== Utils ========== #
clear: ## Clear output folder
	rm -rf "output"
	mkdir -p "output"

# ========== Fetch ========== #

fetch_single_anime: clear ## Fetch "Cowboy Bebop" anime
	pgen fetch 1 --app-name $$APPLICATION_NAME

fetch_single_manga: clear ## Fetch "Monster" manga
	pgen fetch -m 1 --app-name $$APPLICATION_NAME

fetch_many_anime: clear ## Fetch 3 animes
	pgen fetch -M "1,5,8" --app-name $$APPLICATION_NAME

fetch_many_manga: clear ## Fetch 2 mangas
	pgen fetch -mM "1,8" --app-name $$APPLICATION_NAME

fetch_to_custom_file: clear ## Fetch to custom file
	pgen fetch -M "1,5,8" --app-name $$APPLICATION_NAME --save-path "output/custom.json"

# ========== Make preview ========== #
preview_animes: fetch_to_custom_file ## Fetch to custom file and then make preview with example config file
	mkdir -p "output/preview"
	pgen make-preview "output/custom.json" \
		--output-folder "output/preview/" \
		--config "config.example.yaml" \
		--app-name $$APPLICATION_NAME


preview_30: clear ## Fetch 30 animes and preview in parallel
	pgen fetch -M \
		"1,5,6,7,8,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,43,44,45,46,47,48"\
		--app-name $$APPLICATION_NAME \
		--save-path "output/custom.json"
	mkdir -p "output/preview"
	pgen make-preview -P "output/custom.json" \
		--output-folder "output/preview/" \
		--config "config.example.yaml" \
		--app-name $$APPLICATION_NAME



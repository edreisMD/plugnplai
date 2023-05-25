autoformat:
	set -e
	isort .
	black --config pyproject.toml .
	flake8

lint:
	set -e
	isort -c .
	black --check --config pyproject.toml .
	flake8

dev-lint:
	pip install --upgrade black==22.8.0 coverage isort flake8 flake8-bugbear flake8-comprehensions pre-commit pooch

build-docs:
	set -e
	mkdir -p docs/source/_static
	rm -rf docs/build
	rm -rf docs/source/generated
	cd docs && make html

all: autoformat build-docs
# Docs
watch-docs: ## Build and watch documentation
	sphinx-autobuild doc/ doc/_build/html --open-browser --watch $(GIT_ROOT)/plugnplai
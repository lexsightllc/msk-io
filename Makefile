# SPDX-License-Identifier: MPL-2.0
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c

PYTHON ?= python3
VENV ?= .venv
ifeq ($(OS),Windows_NT)
	VENV_BIN := $(VENV)/Scripts
else
	VENV_BIN := $(VENV)/bin
endif
PYTHON_BIN := $(VENV_BIN)/python
PIP_BIN := $(PYTHON_BIN) -m pip

PACKAGE := msk_io
PYTEST := $(PYTHON_BIN) -m pytest
RUFF := $(PYTHON_BIN) -m ruff
BLACK := $(PYTHON_BIN) -m black
ISORT := $(PYTHON_BIN) -m isort
MYPY := $(PYTHON_BIN) -m mypy

PORT ?= 8000
MSK_ARGS ?=
MSK_FIX ?=
FIX_FLAG := $(if $(filter 1,$(MSK_FIX) $(FIX)),--fix,)

.PHONY: bootstrap dev lint fmt typecheck test e2e coverage build package release update-deps security-scan sbom gen-docs migrate clean check help

bootstrap:
	$(PYTHON) -m venv $(VENV)
	$(PYTHON_BIN) -m pip install --upgrade pip
	$(PIP_BIN) install -e .[dev]
	$(PIP_BIN) install build pip-tools pip-audit bandit detect-secrets cyclonedx-bom
	$(PYTHON_BIN) -m pre_commit install --install-hooks
	$(PYTHON_BIN) -m pre_commit install --hook-type commit-msg
	git config commit.template configs/git-commit-template.txt

# Launch local API server with auto-reload
dev:
	UVICORN_CMD="$(PYTHON_BIN) -m uvicorn msk_io.api:app --reload --host 0.0.0.0 --port $${PORT}"; \
		echo "Starting development server: $$UVICORN_CMD"; \
		exec $$UVICORN_CMD

lint:
	$(RUFF) check $(FIX_FLAG) src tests
	$(BLACK) --check src tests
	$(ISORT) --check-only src tests

fmt:
	$(BLACK) src tests
	$(ISORT) src tests
	$(RUFF) format src tests

typecheck:
	$(MYPY) src

pytest-common:
	$(PYTEST) $(MSK_ARGS)

unit-tests:
	$(PYTEST) tests/unit $(MSK_ARGS)

integration-tests:
	@if [ -d tests/integration ] && [ "$(shell ls -A tests/integration)" ]; then \
		$(PYTEST) tests/integration $(MSK_ARGS); \
	else \
		echo "No integration tests discovered"; \
	fi

test: unit-tests integration-tests

# Run pytest against end-to-end scenarios if present
E2E_DIR := tests/e2e

e2e:
	@if [ -d $(E2E_DIR) ] && [ "$(shell ls -A $(E2E_DIR))" ]; then \
		$(PYTEST) $(E2E_DIR) $(MSK_ARGS); \
	else \
		echo "No e2e tests discovered"; \
	fi

coverage:
	$(PYTEST) --cov=$(PACKAGE) --cov-report=term-missing --cov-report=xml $(MSK_ARGS)

build:
	$(PYTHON_BIN) -m build

package: build
	@echo "Package artifacts available in dist/"

release: build
	$(PIP_BIN) install twine
	$(PYTHON_BIN) -m twine check dist/*
	@echo "Release candidate built. Push tags and upload with twine as needed."

update-deps:
	$(PIP_BIN) install pip-tools
	$(PYTHON_BIN) -m piptools compile pyproject.toml -o configs/python/requirements-lock.txt

security-scan:
	$(PIP_BIN) install pip-audit bandit detect-secrets
	$(PYTHON_BIN) -m bandit -q -r src
	$(PYTHON_BIN) -m pip_audit --progress-spinner=off --format json --output sbom/pip-audit.json || (echo "pip-audit failed" && exit 1)
	detect-secrets scan --all-files > sbom/secret-scan.json

sbom:
	$(PIP_BIN) install pip-audit
	$(PYTHON_BIN) -m pip_audit --format cyclonedx-json --output sbom/sbom.json || (echo "pip-audit SBOM generation failed" && exit 1)

GEN_DOCS_DIR := docs/api

gen-docs:
	$(PIP_BIN) install pdoc
	$(PYTHON_BIN) -m pdoc src/msk_io --output-directory $(GEN_DOCS_DIR)

migrate:
	@if [ -d migrations ]; then \
		echo "Running migrations via alembic"; \
		$(PYTHON_BIN) -m alembic upgrade head; \
	else \
		echo "No migrations directory present; skipping."; \
	fi

clean:
	rm -rf $(VENV) build dist .pytest_cache .mypy_cache .ruff_cache .coverage coverage.xml sbom/*.json docs/api
	find src tests -name "__pycache__" -type d -prune -exec rm -rf {} +

check:
	$(MAKE) lint
	$(MAKE) typecheck
	$(MAKE) test
	$(MAKE) coverage
	$(MAKE) security-scan

help:
	@grep -E '^[a-zA-Z_-]+:' Makefile | cut -d':' -f1

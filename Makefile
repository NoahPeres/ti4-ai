SHELL := bash
.SHELLFLAGS := -euo pipefail -c

.PHONY: all help install test lint lint-fix format type-check check-all clean dev-setup strict-check security-check runtime-check quality-gate pre-commit-install pre-commit-autoupdate format-check

all: quality-gate

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies with uv
	uv sync --dev

dev-setup: install pre-commit-install ## Set up development environment with uv
	@echo "Development environment set up!"
	@echo "Activate with: source .venv/bin/activate"
	@echo "Or run commands with: uv run <command>"

test: ## Run tests with coverage
	uv run pytest --cov=src/ti4 --cov-report=term-missing --cov-report=html

lint: ## Run linting checks
	uv run ruff check src tests --show-fixes

lint-fix: ## Run linting checks and automatically fix issues
	uv run ruff check src tests --fix --show-fixes
	uv run ruff format src tests

format: ## Format code with ruff
	uv run ruff format src tests

format-check: ## Check code formatting without making changes
	uv run ruff format --check src tests

type-check: ## Run type checking with mypy
	@echo "Running mypy with strict checking for src/ and standard checking for tests/..."
	@echo "Checking src/ with strict mode..."
	uv run mypy src --show-error-codes --strict --warn-unused-ignores
	@echo "Checking tests/ with standard mode (errors are informational only)..."
	-uv run mypy tests --show-error-codes
	@echo "✅ Type checking complete. Production code (src/) passes strict checks."

strict-check: ## Run mypy with strictest settings (no type ignores allowed)
	@echo "Running mypy with enhanced strict settings on all code..."
	uv run mypy src tests --show-error-codes --strict --warn-unused-ignores

security-check: ## Run security analysis with bandit
	@echo "Running security analysis..."
	uvx bandit -r src/ -f json -ll -ii

runtime-check: ## Run tests with runtime type checking enabled
	@echo "Running tests with runtime type checking..."
	PYTHONPATH=src uv run pytest tests/ -v --tb=short

pre-commit-install: ## Install pre-commit hooks
	uvx pre-commit install
	uvx pre-commit install --hook-type commit-msg

pre-commit-autoupdate: ## Update pre-commit hooks to latest versions
	uvx pre-commit autoupdate

check-all: lint type-check format-check ## Run all quality checks (lint, format-check, type-check)
	@echo "All basic quality checks passed!"

quality-gate: lint strict-check security-check test runtime-check format-check ## Run the complete quality gate (all checks + tests)
	@echo "🎉 All quality gate checks passed! Code is ready for production."

clean: ## Clean up build artifacts
	@rm -rf build/ dist/ *.egg-info/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/ .ruff_cache/
	@find . -type d -name __pycache__ -delete
	@find . -type f -name "*.pyc" -delete

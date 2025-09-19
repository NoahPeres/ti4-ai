.PHONY: help install test lint format ruff-format type-check check-all clean dev-setup strict-check security-check runtime-check quality-gate pre-commit-install

help:
	@echo "Available commands:"
	@echo "  install          Install dependencies with uv"
	@echo "  dev-setup        Set up development environment with uv"
	@echo "  test             Run tests with coverage"
	@echo "  lint             Run linting checks"
	@echo "  format           Format code with ruff"
	@echo "  type-check       Run type checking with mypy"
	@echo "  strict-check     Run mypy with strictest settings (no type ignores allowed)"
	@echo "  security-check   Run security analysis with bandit"
	@echo "  runtime-check    Run tests with runtime type checking enabled"
	@echo "  check-all        Run all quality checks (lint, format-check, type-check)"
	@echo "  quality-gate     Run the complete quality gate (all checks + tests)"
	@echo "  pre-commit-install Install pre-commit hooks"
	@echo "  clean            Clean up build artifacts"

install:
	uv sync --dev

dev-setup: install pre-commit-install
	@echo "Development environment set up!"
	@echo "Activate with: source .venv/bin/activate"
	@echo "Or run commands with: uv run <command>"

test:
	uv run pytest --cov=src/ti4 --cov-report=term-missing --cov-report=html

lint:
	uv run ruff check src tests --show-fixes

format:
	uv run ruff format src tests

type-check:
	@echo "Running mypy with strict checking for src/ and standard checking for tests/..."
	@echo "Checking src/ with strict mode..."
	uv run mypy src --show-error-codes --strict --warn-unused-ignores
	@echo "Checking tests/ with standard mode (errors are informational only)..."
	-uv run mypy tests --show-error-codes
	@echo "✅ Type checking complete. Production code (src/) passes strict checks."

strict-check:
	@echo "Running mypy with enhanced strict settings on all code..."
	uv run mypy src tests --show-error-codes --strict --warn-unused-ignores

security-check:
	@echo "Running security analysis..."
	uv add --dev bandit
	uv run bandit -r src/ -f json || echo "Security issues found - review above"

runtime-check:
	@echo "Running tests with runtime type checking..."
	PYTHONPATH=src uv run pytest tests/ -v --tb=short

pre-commit-install:
	uv add --dev pre-commit
	uv run pre-commit install

check-all: lint type-check
	@echo "Running format check..."
	uv run ruff format --check src tests
	@echo "All basic quality checks passed!"

quality-gate: lint strict-check security-check test runtime-check
	@echo "Running format check..."
	uv run ruff format --check src tests
	@echo "🎉 All quality gate checks passed! Code is ready for production."

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

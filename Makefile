.PHONY: help install test lint format type-check clean dev-setup

help:
	@echo "Available commands:"
	@echo "  install     Install dependencies with uv"
	@echo "  dev-setup   Set up development environment with uv"
	@echo "  test        Run tests with coverage"
	@echo "  lint        Run linting checks"
	@echo "  format      Format code with black"
	@echo "  type-check  Run type checking with mypy"
	@echo "  clean       Clean up build artifacts"

install:
	uv sync --dev

dev-setup:
	uv sync --dev
	@echo "Development environment set up!"
	@echo "Activate with: source .venv/bin/activate"
	@echo "Or run commands with: uv run <command>"

test:
	uv run pytest --cov=src/ti4 --cov-report=term-missing --cov-report=html

lint:
	uv run ruff check src tests

format:
	uv run black src tests

type-check:
	uv run mypy src

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
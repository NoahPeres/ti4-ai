# TI4 Game Framework

A comprehensive framework for Twilight Imperium 4th Edition that tracks legal game states, validates moves, and provides interfaces for both human and AI players.

## Features

- Accurate game state tracking and validation
- Legal move generation and validation
- Support for both human and AI players
- Modular and extensible architecture
- Comprehensive test coverage

## Installation

### Development Setup

1. Clone the repository
2. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you haven't already
3. Create virtual environment and install dependencies:
   ```bash
   uv sync --dev
   ```
4. Activate the virtual environment:
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

### Alternative: Using uv run

You can also run commands directly with uv without activating the virtual environment:
```bash
uv run pytest
uv run black src tests
uv run mypy src
```

## Development

This project follows strict **Test-Driven Development (TDD)** practices. See `.kiro/steering/tdd-practices.md` for detailed guidelines that all contributors must follow.

### Running Tests

```bash
uv run pytest
```

### Code Formatting

```bash
# Format with ruff (recommended)
uv run ruff format src tests

# Format with both ruff and black
make format

# Or format with black only
uv run black src tests
```

### Type Checking

```bash
uv run mypy src
```

### Linting

```bash
# Check for linting issues
uv run ruff check src tests

# Auto-fix linting issues where possible
uv run ruff check --fix src tests
```

### Quality Checks

```bash
# Run all quality checks (recommended before committing)
make check-all

# Or run individual checks:
make lint        # Linting with ruff
make type-check  # Type checking with mypy
make format      # Format code
```

## Project Structure

```
src/
├── ti4/
│   ├── core/          # Core game components and state management
│   ├── actions/       # Action system and validation
│   ├── players/       # Player interfaces and implementations
│   └── rules/         # Game rules and validation engine
tests/                 # Test suite
docs/                  # Documentation
```

## License

MIT License
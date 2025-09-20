# TI4 Game Framework

A comprehensive, enterprise-grade framework for Twilight Imperium 4th Edition that provides advanced game state management, AI integration capabilities, and robust testing infrastructure. Built with modern design patterns and optimized for both competitive play and AI research.

## Features

### Core Functionality
- **Accurate Game State Management**: Immutable game states with comprehensive validation
- **Legal Move Generation**: Optimized legal move calculation with caching
- **Multi-Player Support**: Robust support for 3-8 player games
- **Faction-Specific Rules**: Complete implementation of all faction abilities
- **Technology Integration**: Full technology tree with upgrade mechanics

### Advanced Architecture (Phase 2)
- **Command Pattern**: Full undo/redo support with command history and replay
- **Observer Pattern**: Event-driven architecture for real-time monitoring and AI integration
- **State Machine**: Robust game phase management with transition validation
- **Builder Pattern**: Fluent interfaces for complex test scenario creation
- **Performance Layer**: Caching, concurrent game support, and resource management

### AI & Research Features
- **Event Streams**: Rich event data for machine learning algorithms
- **Command History**: Complete game replay capabilities for AI training
- **Statistics Collection**: Real-time game analytics and performance metrics
- **Concurrent Games**: Support for multiple simultaneous game instances
- **Diagnostic Tools**: Comprehensive debugging and analysis utilities

### Quality & Performance
- **Test Coverage**: 87% test coverage with 1053+ comprehensive tests
- **Performance Optimized**: Caching layer with 40-60% improvement in critical operations
- **Thread Safe**: Full concurrent game support with proper isolation
- **Memory Managed**: Automatic resource cleanup for long-running sessions
- **Error Recovery**: Graceful degradation with comprehensive error context

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

## Architecture Overview

The TI4 framework implements advanced design patterns for robust, scalable game management:

```
┌─────────────────────────────────────────────────────────────┐
│                    Player Interfaces                        │
│         (Human UI, AI API, Network Interface)               │
├─────────────────────────────────────────────────────────────┤
│                  Game Controller                            │
│              (Enhanced with State Machine)                  │
├─────────────────────────────────────────────────────────────┤
│     Command System        │        Event System             │
│  (Action Commands with    │    (Observer Pattern for        │
│   Execute/Undo/Replay)    │     Game Event Notifications)   │
├─────────────────────────────────────────────────────────────┤
│                    Action Engine                            │
│         (Move Validation, State Transitions)                │
├─────────────────────────────────────────────────────────────┤
│                     Game State                              │
│            (Board, Players, Cards, Resources)               │
├─────────────────────────────────────────────────────────────┤
│      Rule Engine          │      Performance Layer          │
│  (Game Rules, Victory     │   (Caching, Optimization,       │
│   Conditions)             │    Resource Management)         │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
src/
├── ti4/
│   ├── core/              # Core game components and state management
│   │   ├── game_state.py      # Immutable game state with validation
│   │   ├── game_controller.py # Main game flow controller
│   │   ├── game_state_machine.py # Phase management state machine
│   │   ├── events.py          # Event system and event definitions
│   │   ├── observers.py       # Event observers (logging, stats, AI)
│   │   ├── exceptions.py      # Enhanced exception hierarchy
│   │   ├── logging.py         # Structured game logging
│   │   └── diagnostics.py     # Debugging and analysis tools
│   ├── commands/          # Command pattern implementation
│   │   ├── base.py            # GameCommand interface and manager
│   │   ├── manager.py         # Command execution and history
│   │   └── movement.py        # Movement command implementation
│   ├── actions/           # Action system and validation
│   │   ├── action.py          # Base action interfaces
│   │   ├── legal_moves.py     # Legal move generation
│   │   └── validation.py      # Action validation engine
│   ├── performance/       # Performance optimization layer
│   │   ├── cache.py           # Caching for expensive operations
│   │   ├── concurrent.py      # Concurrent game management
│   │   └── monitoring.py      # Resource and performance monitoring
│   ├── testing/           # Test utilities and scenario builders
│   │   ├── scenario_builder.py # Fluent test scenario creation
│   │   └── test_utilities.py   # Common test helpers
│   ├── players/           # Player interfaces and implementations
│   └── rules/             # Game rules and validation engine
tests/                     # Comprehensive test suite (1053+ tests)
docs/                      # Documentation and examples
├── API_DOCUMENTATION.md       # Complete API reference
├── USAGE_EXAMPLES.md          # Practical usage examples
├── ARCHITECTURAL_CHANGES.md   # Detailed architecture documentation
└── PERFORMANCE_CHARACTERISTICS.md # Performance analysis and benchmarks
```

## Quick Start

### Basic Game Setup

```python
from ti4.testing.scenario_builder import GameScenarioBuilder
from ti4.commands.manager import CommandManager
from ti4.core.events import GameEventBus
from ti4.core.observers import LoggingObserver

# Create a game scenario
game_state = (GameScenarioBuilder()
    .with_players(("alice", "sol"), ("bob", "xxcha"))
    .with_galaxy("standard_6p")
    .in_phase("action")
    .build())

# Set up command management and event handling
command_manager = CommandManager()
event_bus = GameEventBus()
logger = LoggingObserver()

event_bus.subscribe("unit_moved", logger.handle_event)

# Execute commands with full undo support
from ti4.commands.movement import MovementCommand

move_command = MovementCommand(
    unit_id="cruiser_1",
    from_system="home_system",
    to_system="mecatol_rex",
    player_id="alice",
    event_bus=event_bus
)

# Execute and automatically log/track
new_state = command_manager.execute_command(move_command, game_state)

# Undo if needed
previous_state = command_manager.undo_last_command(new_state)
```

### AI Integration Example

```python
from ti4.core.observers import AITrainingDataCollector

# Set up AI data collection
ai_collector = AITrainingDataCollector()
event_bus.subscribe("unit_moved", ai_collector.handle_event)
event_bus.subscribe("combat_resolved", ai_collector.handle_event)

# Play through game and collect training data
# ... execute many commands ...

# Export training data for machine learning
training_data = ai_collector.export_training_data()
```

## Documentation

- **[API Documentation](API_DOCUMENTATION.md)**: Complete API reference with examples
- **[Usage Examples](USAGE_EXAMPLES.md)**: Practical examples for all major features
- **[Architectural Changes](ARCHITECTURAL_CHANGES.md)**: Detailed architecture documentation
- **[Performance Characteristics](PERFORMANCE_CHARACTERISTICS.md)**: Performance analysis and benchmarks

## License

MIT License

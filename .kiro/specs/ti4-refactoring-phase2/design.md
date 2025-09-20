# Design Document

## Overview

The TI4 Refactoring Phase 2 design focuses on implementing advanced design patterns and architectural improvements to create a more robust, maintainable, and extensible framework. This phase builds upon the successful first refactoring that addressed unit statistics and movement rules.

The design emphasizes fixing existing test failures, implementing proven design patterns (Command, Observer, Builder, State Machine), and establishing solid foundations for AI integration and performance optimization. All changes will maintain backward compatibility while improving code quality and system reliability.

## Architecture

### Enhanced Architecture with Design Patterns

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

### Key Design Patterns Integration

1. **Command Pattern**: All game actions become undoable commands
2. **Observer Pattern**: Event-driven architecture for loose coupling
3. **State Machine Pattern**: Robust game phase management
4. **Builder Pattern**: Fluent test scenario construction
5. **Strategy Pattern**: Enhanced rule engine flexibility
6. **Factory Pattern**: Improved object creation consistency

## Components and Interfaces

### 1. Command System Architecture

#### Command Interface
```python
from abc import ABC, abstractmethod
from typing import Any, Dict

class GameCommand(ABC):
    """Base interface for all game commands."""

    @abstractmethod
    def execute(self, game_state: GameState) -> GameState:
        """Execute the command and return new game state."""
        pass

    @abstractmethod
    def undo(self, game_state: GameState) -> GameState:
        """Undo the command and return previous game state."""
        pass

    @abstractmethod
    def get_undo_data(self) -> Dict[str, Any]:
        """Get data needed for undo operation."""
        pass

    @abstractmethod
    def can_execute(self, game_state: GameState) -> bool:
        """Check if command can be executed in current state."""
        pass
```

#### Command Manager
```python
class CommandManager:
    """Manages command execution, undo, and replay functionality."""

    def __init__(self):
        self._command_history: List[GameCommand] = []
        self._undo_stack: List[Dict[str, Any]] = []

    def execute_command(self, command: GameCommand, game_state: GameState) -> GameState:
        """Execute command and store for potential undo."""
        pass

    def undo_last_command(self, game_state: GameState) -> GameState:
        """Undo the most recent command."""
        pass

    def replay_commands(self, initial_state: GameState) -> GameState:
        """Replay all commands from initial state."""
        pass
```

### 2. Event System Architecture

#### Event Bus
```python
from typing import Callable, List, Any

class GameEventBus:
    """Central event bus for game event notifications."""

    def __init__(self):
        self._observers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, observer: Callable) -> None:
        """Subscribe to specific event types."""
        pass

    def unsubscribe(self, event_type: str, observer: Callable) -> None:
        """Unsubscribe from event types."""
        pass

    def publish(self, event: GameEvent) -> None:
        """Publish event to all subscribers."""
        pass
```

#### Game Events
```python
@dataclass(frozen=True)
class GameEvent:
    """Base class for all game events."""
    event_type: str
    timestamp: float
    game_id: str
    data: Dict[str, Any]

@dataclass(frozen=True)
class UnitMovedEvent(GameEvent):
    """Event fired when a unit moves."""
    unit_id: str
    from_system: str
    to_system: str
    player_id: str

@dataclass(frozen=True)
class CombatStartedEvent(GameEvent):
    """Event fired when combat begins."""
    system_id: str
    participants: List[str]
```

### 3. State Machine for Game Phases

#### Phase State Machine
```python
from enum import Enum
from typing import Set, Optional

class GamePhaseState(Enum):
    SETUP = "setup"
    STRATEGY = "strategy"
    ACTION = "action"
    STATUS = "status"
    AGENDA = "agenda"

class GameStateMachine:
    """Manages game phase transitions with validation."""

    def __init__(self):
        self._current_phase = GamePhaseState.SETUP
        self._valid_transitions = self._build_transition_map()

    def can_transition_to(self, new_phase: GamePhaseState) -> bool:
        """Check if transition to new phase is valid."""
        pass

    def transition_to(self, new_phase: GamePhaseState) -> None:
        """Transition to new phase if valid."""
        pass

    def get_valid_transitions(self) -> Set[GamePhaseState]:
        """Get all valid transitions from current phase."""
        pass
```

### 4. Test Scenario Builder

#### Game Scenario Builder
```python
class GameScenarioBuilder:
    """Fluent builder for creating complex test scenarios."""

    def __init__(self):
        self._players: List[Player] = []
        self._galaxy: Optional[Galaxy] = None
        self._phase: GamePhaseState = GamePhaseState.SETUP
        self._custom_setup: Dict[str, Any] = {}

    def with_players(self, *player_configs) -> 'GameScenarioBuilder':
        """Add players to the scenario."""
        return self

    def with_galaxy(self, galaxy_config) -> 'GameScenarioBuilder':
        """Set galaxy configuration."""
        return self

    def in_phase(self, phase: GamePhaseState) -> 'GameScenarioBuilder':
        """Set the game phase."""
        return self

    def with_units(self, unit_placements) -> 'GameScenarioBuilder':
        """Place units on the board."""
        return self

    def build(self) -> GameState:
        """Build the final game state."""
        pass
```

## Data Models

### Enhanced Error Handling

#### Comprehensive Exception Hierarchy
```python
class TI4Error(Exception):
    """Base exception with enhanced context."""
    def __init__(self, message: str, context: Dict[str, Any] = None):
        super().__init__(message)
        self.context = context or {}
        self.timestamp = time.time()

class CommandExecutionError(TI4Error):
    """Raised when command execution fails."""
    def __init__(self, command: GameCommand, reason: str, context: Dict[str, Any] = None):
        super().__init__(f"Command execution failed: {reason}", context)
        self.command = command

class PhaseTransitionError(TI4Error):
    """Raised when invalid phase transition is attempted."""
    def __init__(self, from_phase: GamePhaseState, to_phase: GamePhaseState):
        super().__init__(f"Invalid transition from {from_phase} to {to_phase}")
        self.from_phase = from_phase
        self.to_phase = to_phase
```

### Performance Optimization Models

#### Caching Layer
```python
from functools import lru_cache
from typing import Hashable

class GameStateCache:
    """Caches expensive computations for game states."""

    def __init__(self, max_size: int = 1000):
        self._cache_size = max_size

    @lru_cache(maxsize=1000)
    def get_legal_moves(self, state_hash: Hashable, player_id: str) -> List[GameCommand]:
        """Cache legal moves for game state."""
        pass

    def invalidate_cache(self, state_hash: Hashable) -> None:
        """Invalidate cache entries for specific state."""
        pass
```

## Error Handling

### Multi-Layer Error Recovery

#### Error Recovery Strategy
1. **Command Level**: Commands validate before execution and provide rollback
2. **System Level**: Event bus continues operation even if observers fail
3. **State Level**: Game state validation prevents corruption
4. **Application Level**: Graceful degradation for non-critical failures

#### Enhanced Logging System
```python
import logging
from typing import Any, Dict

class GameLogger:
    """Enhanced logging with structured data."""

    def __init__(self, game_id: str):
        self.game_id = game_id
        self.logger = logging.getLogger(f"ti4.game.{game_id}")

    def log_command(self, command: GameCommand, result: str, context: Dict[str, Any] = None):
        """Log command execution with context."""
        pass

    def log_event(self, event: GameEvent):
        """Log game events."""
        pass

    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Log errors with full context."""
        pass
```

## Testing Strategy

### Test Failure Resolution Plan

#### Priority 1: Fix Existing Test Failures
1. **Game Controller Exception Test**: Update test to expect `InvalidPlayerError` instead of `ValueError`
2. **Movement Validation Tests**: Fix movement validator logic to properly handle adjacent system validation
3. **Integration Test Failures**: Resolve unit statistics and faction ability issues
4. **Faction-Specific Tests**: Ensure proper unit stat calculation with faction modifiers

#### Enhanced Test Architecture
```python
class TestScenarioManager:
    """Manages complex test scenarios with builder pattern."""

    @staticmethod
    def create_basic_game() -> GameScenarioBuilder:
        """Create basic 2-player game scenario."""
        return (GameScenarioBuilder()
                .with_players(("player1", "sol"), ("player2", "xxcha"))
                .with_galaxy("standard_6p")
                .in_phase(GamePhaseState.ACTION))

    @staticmethod
    def create_combat_scenario() -> GameScenarioBuilder:
        """Create scenario with units ready for combat."""
        pass
```

### Property-Based Testing Enhancement
```python
from hypothesis import given, strategies as st

class GameStateInvariants:
    """Property-based tests for game state invariants."""

    @given(st.lists(st.text(), min_size=2, max_size=6))
    def test_player_uniqueness(self, player_ids):
        """Test that all players have unique IDs."""
        pass

    @given(st.integers(min_value=0, max_value=10))
    def test_resource_non_negative(self, resource_amount):
        """Test that resources never go negative."""
        pass
```

## Implementation Phases

### Phase 1: Test Failure Resolution (Priority)
- Fix all existing test failures
- Ensure consistent exception handling
- Resolve movement validation issues
- Fix faction-specific unit statistics

### Phase 2: Command Pattern Implementation
- Implement base command interface
- Convert existing actions to commands
- Add undo/redo functionality
- Implement command history and replay

### Phase 3: Event System Implementation
- Create event bus architecture
- Define core game events
- Implement observer registration
- Add event-driven notifications

### Phase 4: State Machine Enhancement
- Implement game phase state machine
- Add phase transition validation
- Enhance phase-specific rule enforcement
- Improve phase progression logic

### Phase 5: Builder Pattern for Tests
- Create game scenario builder
- Implement fluent interface
- Add complex scenario support
- Enhance test readability

### Phase 6: Performance Optimization
- Implement caching layer
- Add performance monitoring
- Optimize critical paths
- Add resource management

### Phase 7: Enhanced Error Handling
- Implement comprehensive logging
- Add structured error context
- Improve error recovery
- Add debugging capabilities

## Success Metrics

### Code Quality Metrics
- **Test Coverage**: Maintain >85% coverage
- **Cyclomatic Complexity**: Keep methods under 10 complexity
- **Code Duplication**: Reduce duplication by 50%
- **Error Handling**: 100% custom exceptions in core modules

### Performance Metrics
- **Command Execution**: <1ms for simple commands
- **State Transitions**: <5ms for complex transitions
- **Memory Usage**: Stable memory usage over long runs
- **Concurrent Games**: Support 10+ simultaneous games

### Maintainability Metrics
- **Test Failures**: Zero failing tests
- **Documentation**: 100% public API documented
- **Code Review**: All changes peer reviewed
- **Refactoring Safety**: All refactoring preserves behavior

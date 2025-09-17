# TI4 Framework API Documentation

## Overview

This document provides comprehensive API documentation for the TI4 framework's new design patterns and architectural improvements implemented in Phase 2 refactoring.

## Command Pattern Implementation

### GameCommand Interface

```python
from abc import ABC, abstractmethod
from typing import Any, Dict
from ..core.game_state import GameState

class GameCommand(ABC):
    """Base interface for all game commands with undo support."""
    
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

### CommandManager

```python
class CommandManager:
    """Manages command execution, undo, and replay functionality."""
    
    def execute_command(self, command: GameCommand, game_state: GameState) -> GameState:
        """Execute command and store for potential undo."""
        
    def undo_last_command(self, game_state: GameState) -> GameState:
        """Undo the most recent command."""
        
    def replay_commands(self, initial_state: GameState) -> GameState:
        """Replay all commands from initial state."""
```

### Usage Example

```python
# Create a movement command
move_command = MovementCommand(
    unit_id="unit_1",
    from_system="sys_a",
    to_system="sys_b",
    player_id="player_1"
)

# Execute the command
new_state = command_manager.execute_command(move_command, current_state)

# Undo if needed
previous_state = command_manager.undo_last_command(new_state)
```

## Observer Pattern Implementation

### GameEventBus

```python
class GameEventBus:
    """Central event bus for game event notifications."""
    
    def subscribe(self, event_type: str, observer: Callable) -> None:
        """Subscribe to specific event types."""
        
    def unsubscribe(self, event_type: str, observer: Callable) -> None:
        """Unsubscribe from event types."""
        
    def publish(self, event: GameEvent) -> None:
        """Publish event to all subscribers."""
```

### Game Events

```python
@dataclass(frozen=True)
class UnitMovedEvent:
    """Event fired when a unit moves."""
    game_id: str
    unit_id: str
    from_system: str
    to_system: str
    player_id: str
    timestamp: float = None

@dataclass(frozen=True)
class CombatStartedEvent:
    """Event fired when combat begins."""
    game_id: str
    system_id: str
    participants: List[str]
    timestamp: float = None

@dataclass(frozen=True)
class PhaseChangedEvent:
    """Event fired when game phase changes."""
    game_id: str
    from_phase: GamePhase
    to_phase: GamePhase
    timestamp: float = None
```

### Event Observers

```python
class LoggingObserver(EventObserver):
    """Observer that logs game events."""
    
    def handle_event(self, event: GameEvent) -> None:
        """Log game events with appropriate detail level."""

class StatisticsCollector(EventObserver):
    """Observer that collects game statistics."""
    
    def handle_event(self, event: GameEvent) -> None:
        """Collect statistics from game events."""

class AITrainingDataCollector(EventObserver):
    """Observer that collects data for AI training."""
    
    def handle_event(self, event: GameEvent) -> None:
        """Collect training data from game events."""
```

### Usage Example

```python
# Create event bus and observers
event_bus = GameEventBus()
logger = LoggingObserver()
stats_collector = StatisticsCollector()

# Subscribe observers
event_bus.subscribe("unit_moved", logger.handle_event)
event_bus.subscribe("unit_moved", stats_collector.handle_event)

# Publish events
event = UnitMovedEvent(
    game_id="game_1",
    unit_id="unit_1",
    from_system="sys_a",
    to_system="sys_b",
    player_id="player_1"
)
event_bus.publish(event)
```

## State Machine Pattern Implementation

### GameStateMachine

```python
class GameStateMachine:
    """Manages game phase transitions with validation."""
    
    def can_transition_to(self, new_phase: GamePhaseState) -> bool:
        """Check if transition to new phase is valid."""
        
    def transition_to(self, new_phase: GamePhaseState) -> None:
        """Transition to new phase if valid."""
        
    def get_valid_transitions(self) -> Set[GamePhaseState]:
        """Get all valid transitions from current phase."""
```

### Usage Example

```python
# Create state machine
state_machine = GameStateMachine()

# Check valid transitions
if state_machine.can_transition_to(GamePhaseState.ACTION):
    state_machine.transition_to(GamePhaseState.ACTION)
else:
    print("Invalid phase transition")
```

## Builder Pattern Implementation

### GameScenarioBuilder

```python
class GameScenarioBuilder:
    """Fluent builder for creating complex test scenarios."""
    
    def with_players(self, *player_configs) -> 'GameScenarioBuilder':
        """Add players to the scenario."""
        
    def with_galaxy(self, galaxy_config) -> 'GameScenarioBuilder':
        """Set galaxy configuration."""
        
    def in_phase(self, phase: GamePhaseState) -> 'GameScenarioBuilder':
        """Set the game phase."""
        
    def with_units(self, unit_placements) -> 'GameScenarioBuilder':
        """Place units on the board."""
        
    def build(self) -> GameState:
        """Build the final game state."""
```

### Usage Example

```python
# Build a complex game scenario
game_state = (GameScenarioBuilder()
    .with_players(
        ("player1", "sol"),
        ("player2", "xxcha")
    )
    .with_galaxy("standard_6p")
    .in_phase(GamePhaseState.ACTION)
    .with_units({
        "sys_1": [("cruiser", "player1")],
        "sys_2": [("destroyer", "player2")]
    })
    .build())
```

## Performance Optimization Layer

### GameStateCache

```python
class GameStateCache:
    """Caches expensive computations for game states."""
    
    def get_legal_moves(self, game_state: GameState, player_id: str) -> List[GameCommand]:
        """Get legal moves for a player, using cache if available."""
        
    def invalidate_cache(self, state_hash: Hashable) -> None:
        """Invalidate cache entries for specific state."""
```

### ConcurrentGameManager

```python
class ConcurrentGameManager:
    """Manages multiple concurrent game instances safely."""
    
    def create_game(self, game_id: str, initial_state: GameState) -> None:
        """Create a new game instance."""
        
    def get_game(self, game_id: str) -> Optional[GameState]:
        """Get current state of a game."""
        
    def execute_game_operation(self, game_id: str, operation: Callable) -> Any:
        """Execute operation on specific game with thread safety."""
```

## Enhanced Error Handling

### Exception Hierarchy

```python
class TI4GameError(Exception):
    """Base exception with enhanced context."""
    
    def __init__(self, message: str, context: Dict[str, Any] = None):
        super().__init__(message)
        self.context = context or {}
        self.timestamp = time.time()

class CommandExecutionError(TI4GameError):
    """Raised when command execution fails."""

class PhaseTransitionError(TI4GameError):
    """Raised when invalid phase transition is attempted."""
```

### GameLogger

```python
class GameLogger:
    """Enhanced logging with structured data."""
    
    def log_command(self, command: GameCommand, result: str, context: Dict[str, Any] = None):
        """Log command execution with context."""
        
    def log_event(self, event: GameEvent):
        """Log game events."""
        
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Log errors with full context."""
```

## Integration Examples

### Complete Game Setup

```python
# Initialize all components
event_bus = GameEventBus()
command_manager = CommandManager()
state_machine = GameStateMachine()
cache = GameStateCache()
logger = GameLogger("game_1")

# Set up observers
logging_observer = LoggingObserver()
stats_collector = StatisticsCollector()

event_bus.subscribe("unit_moved", logging_observer.handle_event)
event_bus.subscribe("unit_moved", stats_collector.handle_event)

# Create game scenario
initial_state = (GameScenarioBuilder()
    .with_players(("player1", "sol"), ("player2", "xxcha"))
    .with_galaxy("standard_6p")
    .in_phase(GamePhaseState.SETUP)
    .build())

# Execute commands with full integration
move_command = MovementCommand(
    unit_id="unit_1",
    from_system="sys_a",
    to_system="sys_b",
    player_id="player1",
    event_bus=event_bus  # Commands publish events
)

new_state = command_manager.execute_command(move_command, initial_state)
```

### Error Handling Integration

```python
try:
    # Execute risky operation
    result = command_manager.execute_command(command, state)
except CommandExecutionError as e:
    logger.log_error(e, {"command": command, "state": state})
    # Handle error appropriately
except PhaseTransitionError as e:
    logger.log_error(e, {"current_phase": state_machine.current_phase})
    # Handle phase error
```

## Best Practices

### Command Pattern
- Always implement both `execute` and `undo` methods
- Store minimal undo data for efficiency
- Validate commands before execution
- Use command serialization for persistence

### Observer Pattern
- Keep observers lightweight and fast
- Handle observer failures gracefully
- Use specific event types for better performance
- Unsubscribe observers when no longer needed

### State Machine
- Define all valid transitions explicitly
- Validate transitions before executing
- Log phase changes for debugging
- Use state machine for complex game flow control

### Builder Pattern
- Use fluent interface for readability
- Validate configuration before building
- Provide sensible defaults
- Support both simple and complex scenarios

### Performance
- Use caching for expensive operations
- Monitor memory usage in long-running games
- Implement proper cleanup strategies
- Profile performance-critical paths

This API documentation provides the foundation for using the TI4 framework's enhanced architecture with confidence and efficiency.
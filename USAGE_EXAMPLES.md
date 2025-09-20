# TI4 Framework Usage Examples

## Overview

This document provides practical usage examples for the new design patterns and architectural improvements in the TI4 framework.

## Command Pattern Examples

### Basic Command Usage

```python
from ti4.commands.movement import MovementCommand
from ti4.commands.manager import CommandManager
from ti4.core.game_state import GameState

# Create a game state and command manager
game_state = GameState()
command_manager = CommandManager()

# Create and execute a movement command
move_command = MovementCommand(
    unit_id="cruiser_1",
    from_system="mecatol_rex",
    to_system="adjacent_system",
    player_id="player_1"
)

# Execute the command
if move_command.can_execute(game_state):
    new_state = command_manager.execute_command(move_command, game_state)
    print(f"Unit moved successfully")
else:
    print("Invalid move")
```

### Undo/Redo Operations

```python
# Execute multiple commands
move1 = MovementCommand(unit_id="unit_1", from_system="sys_a", to_system="sys_b", player_id="player_1")
move2 = MovementCommand(unit_id="unit_2", from_system="sys_c", to_system="sys_d", player_id="player_2")

state1 = command_manager.execute_command(move1, initial_state)
state2 = command_manager.execute_command(move2, state1)

# Undo the last command
state_after_undo = command_manager.undo_last_command(state2)
print("Last command undone")

# Replay all commands from initial state
final_state = command_manager.replay_commands(initial_state)
print("All commands replayed")
```

### Custom Command Implementation

```python
from ti4.commands.base import GameCommand
from typing import Dict, Any

class BuildStructureCommand(GameCommand):
    def __init__(self, structure_type: str, system_id: str, player_id: str):
        self.structure_type = structure_type
        self.system_id = system_id
        self.player_id = player_id
        self._undo_data = {}

    def can_execute(self, game_state: GameState) -> bool:
        # Check if player has resources and system is controlled
        return self._validate_resources(game_state) and self._validate_control(game_state)

    def execute(self, game_state: GameState) -> GameState:
        # Store undo data
        self._undo_data = {
            'previous_resources': game_state.get_player_resources(self.player_id),
            'previous_structures': game_state.get_system_structures(self.system_id)
        }

        # Execute the build
        new_state = game_state.copy()
        new_state.add_structure(self.system_id, self.structure_type, self.player_id)
        new_state.deduct_resources(self.player_id, self._get_cost())

        return new_state

    def undo(self, game_state: GameState) -> GameState:
        # Restore previous state using undo data
        restored_state = game_state.copy()
        restored_state.set_player_resources(self.player_id, self._undo_data['previous_resources'])
        restored_state.set_system_structures(self.system_id, self._undo_data['previous_structures'])

        return restored_state

    def get_undo_data(self) -> Dict[str, Any]:
        return self._undo_data
```

## Observer Pattern Examples

### Basic Event Handling

```python
from ti4.core.events import GameEventBus, UnitMovedEvent
from ti4.core.observers import LoggingObserver, StatisticsCollector

# Set up event bus and observers
event_bus = GameEventBus()
logger = LoggingObserver()
stats = StatisticsCollector()

# Subscribe observers to events
event_bus.subscribe("unit_moved", logger.handle_event)
event_bus.subscribe("unit_moved", stats.handle_event)
event_bus.subscribe("combat_started", logger.handle_event)

# Publish an event
event = UnitMovedEvent(
    game_id="game_123",
    unit_id="cruiser_1",
    from_system="home_system",
    to_system="mecatol_rex",
    player_id="player_1"
)

event_bus.publish(event)
print("Event published to all subscribers")
```

### Custom Observer Implementation

```python
from ti4.core.observers import EventObserver
from ti4.core.events import GameEvent

class VictoryConditionObserver(EventObserver):
    def __init__(self):
        self.victory_points = {}
        self.objectives_completed = {}

    def handle_event(self, event: GameEvent) -> None:
        if event.event_type == "objective_completed":
            self._handle_objective_completion(event)
        elif event.event_type == "planet_controlled":
            self._handle_planet_control(event)

        # Check for victory after each relevant event
        self._check_victory_conditions(event.game_id)

    def _handle_objective_completion(self, event: GameEvent) -> None:
        player_id = event.data['player_id']
        objective_id = event.data['objective_id']
        points = event.data['points']

        if player_id not in self.victory_points:
            self.victory_points[player_id] = 0

        self.victory_points[player_id] += points
        print(f"Player {player_id} scored {points} points")

    def _check_victory_conditions(self, game_id: str) -> None:
        for player_id, points in self.victory_points.items():
            if points >= 10:  # Victory condition
                victory_event = GameEvent(
                    event_type="game_won",
                    game_id=game_id,
                    data={'winner': player_id, 'points': points}
                )
                # Could publish this event to notify other observers
                print(f"Player {player_id} wins with {points} points!")

# Use the custom observer
victory_observer = VictoryConditionObserver()
event_bus.subscribe("objective_completed", victory_observer.handle_event)
event_bus.subscribe("planet_controlled", victory_observer.handle_event)
```

### Event-Driven Game Flow

```python
class GameFlowController:
    def __init__(self, event_bus: GameEventBus):
        self.event_bus = event_bus
        self.event_bus.subscribe("phase_changed", self.handle_phase_change)
        self.event_bus.subscribe("all_players_passed", self.handle_all_passed)

    def handle_phase_change(self, event: GameEvent) -> None:
        new_phase = event.data['to_phase']
        game_id = event.game_id

        if new_phase == "action":
            self._setup_action_phase(game_id)
        elif new_phase == "status":
            self._setup_status_phase(game_id)

    def handle_all_passed(self, event: GameEvent) -> None:
        # Automatically advance to next phase
        next_phase_event = PhaseChangedEvent(
            game_id=event.game_id,
            from_phase=event.data['current_phase'],
            to_phase=self._get_next_phase(event.data['current_phase'])
        )
        self.event_bus.publish(next_phase_event)
```

## State Machine Examples

### Basic Phase Management

```python
from ti4.core.game_state_machine import GameStateMachine, GamePhaseState

# Create and use state machine
state_machine = GameStateMachine()

# Check current phase
print(f"Current phase: {state_machine.current_phase}")

# Get valid transitions
valid_transitions = state_machine.get_valid_transitions()
print(f"Valid transitions: {valid_transitions}")

# Attempt phase transition
if state_machine.can_transition_to(GamePhaseState.STRATEGY):
    state_machine.transition_to(GamePhaseState.STRATEGY)
    print("Transitioned to strategy phase")
else:
    print("Invalid transition")
```

### Phase-Specific Action Validation

```python
class PhaseAwareActionValidator:
    def __init__(self, state_machine: GameStateMachine):
        self.state_machine = state_machine

    def validate_action(self, action: GameCommand, game_state: GameState) -> bool:
        current_phase = self.state_machine.current_phase

        # Phase-specific validation
        if current_phase == GamePhaseState.STRATEGY:
            return self._validate_strategy_action(action, game_state)
        elif current_phase == GamePhaseState.ACTION:
            return self._validate_action_phase_action(action, game_state)
        elif current_phase == GamePhaseState.STATUS:
            return self._validate_status_action(action, game_state)

        return False

    def _validate_strategy_action(self, action: GameCommand, game_state: GameState) -> bool:
        # Only allow strategy card selection in strategy phase
        return isinstance(action, StrategyCardSelectionCommand)

    def _validate_action_phase_action(self, action: GameCommand, game_state: GameState) -> bool:
        # Allow movement, combat, etc. in action phase
        allowed_actions = [MovementCommand, CombatCommand, BuildCommand]
        return any(isinstance(action, action_type) for action_type in allowed_actions)
```

## Builder Pattern Examples

### Simple Game Setup

```python
from ti4.testing.scenario_builder import GameScenarioBuilder
from ti4.core.game_phase import GamePhaseState

# Create a simple 2-player game
game_state = (GameScenarioBuilder()
    .with_players(
        ("alice", "sol"),
        ("bob", "xxcha")
    )
    .with_galaxy("standard_6p")
    .in_phase(GamePhaseState.SETUP)
    .build())

print("Simple game created")
```

### Complex Test Scenario

```python
# Create a complex mid-game scenario
complex_scenario = (GameScenarioBuilder()
    .with_players(
        ("player1", "sol"),
        ("player2", "xxcha"),
        ("player3", "hacan"),
        ("player4", "jol_nar")
    )
    .with_galaxy("custom_layout")
    .in_phase(GamePhaseState.ACTION)
    .with_units({
        "mecatol_rex": [
            ("cruiser", "player1"),
            ("destroyer", "player2")
        ],
        "home_system_1": [
            ("dreadnought", "player1"),
            ("carrier", "player1"),
            ("fighter", "player1"),
            ("fighter", "player1")
        ]
    })
    .with_resources({
        "player1": {"trade_goods": 5, "command_tokens": 3},
        "player2": {"trade_goods": 3, "command_tokens": 4}
    })
    .with_technologies({
        "player1": ["gravity_drive", "plasma_scoring"],
        "player2": ["antimass_deflectors", "sarween_tools"]
    })
    .build())

print("Complex scenario created")
```

### Custom Builder Extension

```python
class CombatScenarioBuilder(GameScenarioBuilder):
    def with_opposing_fleets(self, system_id: str, fleet1: dict, fleet2: dict) -> 'CombatScenarioBuilder':
        """Add opposing fleets in the same system for combat testing."""
        units = []

        # Add fleet 1 units
        for unit_type, count in fleet1.items():
            for _ in range(count):
                units.append((unit_type, fleet1.get('player', 'player1')))

        # Add fleet 2 units
        for unit_type, count in fleet2.items():
            for _ in range(count):
                units.append((unit_type, fleet2.get('player', 'player2')))

        return self.with_units({system_id: units})

    def ready_for_combat(self) -> 'CombatScenarioBuilder':
        """Set up the scenario ready for combat resolution."""
        return self.in_phase(GamePhaseState.ACTION)

# Use the custom builder
combat_scenario = (CombatScenarioBuilder()
    .with_players(("attacker", "sol"), ("defender", "xxcha"))
    .with_opposing_fleets(
        "contested_system",
        fleet1={"cruiser": 2, "destroyer": 1, "player": "attacker"},
        fleet2={"dreadnought": 1, "fighter": 3, "player": "defender"}
    )
    .ready_for_combat()
    .build())
```

## Performance Optimization Examples

### Caching Usage

```python
from ti4.performance.cache import GameStateCache

# Create cache with custom size
cache = GameStateCache(max_size=500)

# Use cache for expensive operations
def get_legal_moves_cached(game_state: GameState, player_id: str):
    # Cache automatically handles hit/miss logic
    return cache.get_legal_moves(game_state, player_id)

# Manual cache management
def update_game_state(game_state: GameState, command: GameCommand):
    new_state = command.execute(game_state)

    # Invalidate cache for the old state
    cache.invalidate_cache(hash(game_state))

    return new_state
```

### Concurrent Game Management

```python
from ti4.performance.concurrent import ConcurrentGameManager

# Create concurrent game manager
game_manager = ConcurrentGameManager(max_concurrent_games=10)

# Create multiple games
for i in range(5):
    initial_state = create_initial_game_state(f"game_{i}")
    game_manager.create_game(f"game_{i}", initial_state)

# Execute operations on specific games
def execute_move_on_game(game_id: str, move_command: MovementCommand):
    def move_operation():
        current_state = game_manager.get_game(game_id)
        return move_command.execute(current_state)

    return game_manager.execute_game_operation(game_id, move_operation)

# Execute moves on different games concurrently
import threading

threads = []
for i in range(5):
    move_cmd = create_move_command(f"game_{i}")
    thread = threading.Thread(
        target=execute_move_on_game,
        args=(f"game_{i}", move_cmd)
    )
    threads.append(thread)
    thread.start()

# Wait for all operations to complete
for thread in threads:
    thread.join()

print("All concurrent operations completed")
```

## Integration Example: Complete Game Session

```python
from ti4.core.events import GameEventBus
from ti4.commands.manager import CommandManager
from ti4.core.game_state_machine import GameStateMachine
from ti4.performance.cache import GameStateCache
from ti4.core.logging import GameLogger

class TI4GameSession:
    def __init__(self, game_id: str):
        self.game_id = game_id

        # Initialize all components
        self.event_bus = GameEventBus()
        self.command_manager = CommandManager()
        self.state_machine = GameStateMachine()
        self.cache = GameStateCache()
        self.logger = GameLogger(game_id)

        # Set up observers
        self._setup_observers()

        # Create initial game state
        self.current_state = self._create_initial_state()

    def _setup_observers(self):
        # Add logging observer
        logging_observer = LoggingObserver()
        self.event_bus.subscribe("unit_moved", logging_observer.handle_event)
        self.event_bus.subscribe("combat_started", logging_observer.handle_event)
        self.event_bus.subscribe("phase_changed", logging_observer.handle_event)

        # Add statistics collector
        stats_collector = StatisticsCollector()
        self.event_bus.subscribe("unit_moved", stats_collector.handle_event)
        self.event_bus.subscribe("combat_resolved", stats_collector.handle_event)

    def _create_initial_state(self):
        return (GameScenarioBuilder()
            .with_players(
                ("player1", "sol"),
                ("player2", "xxcha"),
                ("player3", "hacan")
            )
            .with_galaxy("standard_6p")
            .in_phase(GamePhaseState.SETUP)
            .build())

    def execute_command(self, command: GameCommand) -> bool:
        try:
            # Validate command can be executed
            if not command.can_execute(self.current_state):
                self.logger.log_error(
                    CommandExecutionError("Command validation failed", {"command": command}),
                    {"game_state": self.current_state}
                )
                return False

            # Execute command
            self.current_state = self.command_manager.execute_command(command, self.current_state)

            # Log successful execution
            self.logger.log_command(command, "success")

            return True

        except Exception as e:
            self.logger.log_error(e, {"command": command, "game_state": self.current_state})
            return False

    def undo_last_command(self) -> bool:
        try:
            self.current_state = self.command_manager.undo_last_command(self.current_state)
            self.logger.log_command(None, "undo_success")
            return True
        except Exception as e:
            self.logger.log_error(e, {"operation": "undo"})
            return False

    def advance_phase(self, new_phase: GamePhaseState) -> bool:
        if self.state_machine.can_transition_to(new_phase):
            old_phase = self.state_machine.current_phase
            self.state_machine.transition_to(new_phase)

            # Publish phase change event
            phase_event = PhaseChangedEvent(
                game_id=self.game_id,
                from_phase=old_phase,
                to_phase=new_phase
            )
            self.event_bus.publish(phase_event)

            return True
        return False

# Usage
game = TI4GameSession("epic_game_001")

# Execute some commands
move_command = MovementCommand(
    unit_id="cruiser_1",
    from_system="home_system",
    to_system="mecatol_rex",
    player_id="player1",
    event_bus=game.event_bus
)

if game.execute_command(move_command):
    print("Move executed successfully")

# Advance game phase
if game.advance_phase(GamePhaseState.STRATEGY):
    print("Advanced to strategy phase")

# Undo if needed
if game.undo_last_command():
    print("Last command undone")
```

These examples demonstrate the practical usage of all the new design patterns and architectural improvements, showing how they work together to create a robust, maintainable, and extensible TI4 framework.

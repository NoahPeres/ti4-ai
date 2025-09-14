# Design Document

## Overview

The TI4 Game Framework will be implemented in Python, leveraging object-oriented design principles to model the complex interactions between game components. The architecture follows a layered approach with clear separation between game state management, rule enforcement, and player interfaces.

The system is designed around the concept of immutable game states with validated transitions, ensuring that every game action produces a new valid state or is rejected with clear reasoning. This approach supports both deterministic replay and robust AI training scenarios.

## Architecture

### Core Architecture Layers

```
┌─────────────────────────────────────────┐
│           Player Interfaces             │
│  (Human UI, AI API, Network Interface)  │
├─────────────────────────────────────────┤
│            Game Controller              │
│     (Turn Management, Phase Control)    │
├─────────────────────────────────────────┤
│             Action Engine               │
│    (Move Validation, State Transitions) │
├─────────────────────────────────────────┤
│             Game State                  │
│   (Board, Players, Cards, Resources)    │
├─────────────────────────────────────────┤
│             Rule Engine                 │
│     (Game Rules, Victory Conditions)    │
└─────────────────────────────────────────┘
```

### Key Design Principles

1. **Immutable State**: Game states are immutable objects; actions create new states
2. **Command Pattern**: All player actions are represented as command objects
3. **Strategy Pattern**: Different game phases and mechanics use pluggable strategies
4. **Observer Pattern**: State changes notify interested components (UI, logging, AI)
5. **Factory Pattern**: Complex object creation (galaxy setup, faction initialization)

## Components and Interfaces

### GameState Concept
The central state container will hold all game information in an immutable structure. The specific fields and organization will emerge through TDD, starting with minimal requirements and expanding as features are implemented.

### Action System
All player actions inherit from a base Action class:

```python
class Action(ABC):
    @abstractmethod
    def is_legal(self, state: GameState, player_id: PlayerId) -> bool
    
    @abstractmethod
    def execute(self, state: GameState, player_id: PlayerId) -> GameState
    
    @abstractmethod
    def get_description(self) -> str
```

### Player Interface
Abstract interface that both AI and human players implement:

```python
class Player(ABC):
    @abstractmethod
    def choose_action(self, state: GameState, legal_actions: List[Action]) -> Action
    
    @abstractmethod
    def make_choice(self, state: GameState, choice_context: ChoiceContext) -> Any
```

### Game Controller
Manages game flow and coordinates between components:

```python
class GameController:
    def __init__(self, players: List[Player], settings: GameSettings):
        self.state = self._initialize_game(players, settings)
        self.players = {p.id: p for p in players}
        self.action_engine = ActionEngine()
        self.rule_engine = RuleEngine()
    
    def play_game(self) -> GameResult:
        while not self._is_game_over():
            self._execute_turn()
        return self._determine_winner()
```

## Data Models

### Design Philosophy for Data Structures

Following TDD principles, the specific data structures will emerge organically through implementing and testing individual features. The design emphasizes:

- **Flexibility**: Data models will evolve as we implement and test each component
- **Immutability**: Core principle for reliable state management
- **Extensibility**: Structure should accommodate both base game and Prophecy of Kings expansion

### Initial Conceptual Models

These represent initial thinking that will be refined through implementation:

#### Core Game Concepts
- **Galaxy**: Hex-based map with systems containing planets and units
- **Players**: Faction-specific state including resources, technologies, and cards  
- **Units**: Game pieces with type-specific abilities and current status
- **Actions**: Player decisions that transition game state

#### Key Considerations for Implementation
- **Planets**: Must track controlling player AND which units are present (by type and owner)
- **Unit Abilities**: Abstract concept covering sustain damage, anti-fighter barrage, space cannon, etc.
- **Expansion Compatibility**: Design should accommodate Prophecy of Kings components as secondary requirement

#### Iterative Development Approach
Rather than defining rigid class structures upfront, we'll:
1. Start with minimal viable representations
2. Add complexity only as tests require it
3. Refactor structures as patterns emerge
4. Maintain backward compatibility where possible

## Error Handling

### Validation Strategy
The system uses a multi-layered validation approach:

1. **Syntax Validation**: Ensure action parameters are well-formed
2. **Precondition Validation**: Check if action prerequisites are met
3. **Rule Validation**: Verify action complies with current game rules
4. **State Validation**: Confirm resulting state is valid

### Error Types
```python
class TI4Error(Exception):
    """Base exception for all TI4 framework errors"""
    pass

class InvalidActionError(TI4Error):
    """Raised when an action cannot be performed"""
    def __init__(self, action: Action, reason: str):
        self.action = action
        self.reason = reason

class GameStateError(TI4Error):
    """Raised when game state becomes invalid"""
    pass

class RuleViolationError(TI4Error):
    """Raised when a rule is violated"""
    def __init__(self, rule: str, context: str):
        self.rule = rule
        self.context = context
```

## Testing Strategy

### Test-Driven Development Approach

#### Unit Tests
- **Rule Engine Tests**: Verify individual rule implementations
- **Action Tests**: Test each action type's validation and execution
- **State Tests**: Ensure state transitions maintain invariants
- **Component Tests**: Test individual game components in isolation

#### Integration Tests
- **Game Flow Tests**: Test complete turn sequences
- **Phase Transition Tests**: Verify correct phase changes
- **Multi-Player Interaction Tests**: Test player interaction scenarios
- **Victory Condition Tests**: Test all paths to victory

#### Property-Based Tests
Using hypothesis library to generate random game states and verify:
- State invariants are maintained
- Actions are reversible where appropriate
- Rule consistency across different scenarios

#### AI Training Tests
- **Deterministic Replay**: Ensure games can be replayed exactly
- **Performance Tests**: Verify system can handle rapid AI decision-making
- **Concurrent Game Tests**: Test multiple simultaneous games

### Test Structure
```python
class TestGameState(unittest.TestCase):
    def setUp(self):
        self.initial_state = create_test_game_state()
    
    def test_action_validation(self):
        # Test that invalid actions are rejected
        pass
    
    def test_state_transitions(self):
        # Test that valid actions produce correct new states
        pass

class TestIntegration(unittest.TestCase):
    def test_complete_turn_sequence(self):
        # Test full turn from strategy phase to status phase
        pass
```

### Mocking Strategy
- **Dice Rolling**: Mock random elements for deterministic testing
- **Player Decisions**: Mock player choices to test game flow
- **Time-Dependent Actions**: Mock timing for phase transitions

## Implementation Phases

### Phase 1: Core Infrastructure
- Basic game state representation
- Action framework and validation
- Simple turn management
- Basic unit tests

### Phase 2: Essential Game Mechanics
- Movement and fleet management
- Basic combat system
- Resource management (trade goods, commodities)
- Technology acquisition

### Phase 3: Advanced Systems
- Political phase and agenda system
- Strategy cards and their effects
- Action cards and timing windows
- Victory point tracking

### Phase 4: Complete Game Implementation
- All faction abilities
- All technology trees
- All strategy card effects
- Complete rule set implementation

### Phase 5: AI Interface and Optimization
- Optimized state representation for AI
- Batch action processing
- Performance profiling and optimization
- Training data export capabilities

### Phase 6: Expansion Integration (Secondary Priority)
- Prophecy of Kings faction abilities
- New unit types and mechanics
- Additional agenda and objective cards
- Expanded technology trees and strategy cards
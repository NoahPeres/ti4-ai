# Design Document

## Overview

The Rule 83: STRATEGY CARD implementation will create a lightweight, integration-focused system that leverages our existing robust implementations. Rather than building a monolithic new system, this design emphasizes extending and connecting our proven components: Rule 82 (Strategic Action), Rule 91 (Technology Strategy Card), and the game state management system.

The core philosophy is to create minimal, focused components that integrate seamlessly with existing systems to form one cohesive strategy card framework.

## Architecture

### Integration-First Design

The strategy card system will be built as a thin coordination layer that connects existing systems:

```
┌─────────────────────────────────────────────────────────────┐
│                    Rule 83: Strategy Card System            │
├─────────────────────────────────────────────────────────────┤
│  StrategyCardCoordinator (NEW - Lightweight)               │
│  ├── Card Selection & Assignment                           │
│  ├── Initiative Order Calculation                          │
│  └── State Coordination                                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Existing Systems (REUSE)                 │
├─────────────────────────────────────────────────────────────┤
│  Rule 82: StrategicActionManager                           │
│  ├── Primary/Secondary ability resolution                   │
│  ├── Player participation tracking                          │
│  └── Action workflow management                             │
│                                                             │
│  Rule 91: TechnologyStrategyCard (Example Implementation)   │
│  ├── Concrete strategy card abilities                       │
│  ├── Primary/secondary ability patterns                     │
│  └── Integration with game state                            │
│                                                             │
│  Game State System                                          │
│  ├── Player management                                      │
│  ├── Phase tracking                                         │
│  └── State persistence                                      │
└─────────────────────────────────────────────────────────────┘
```

### Leveraging Existing Constants

We already have `StrategyCardType` enum in `constants.py` with all eight strategy cards defined. The design will use this existing foundation rather than recreating card definitions.

## Components and Interfaces

### 1. StrategyCardCoordinator (NEW - Minimal)

A lightweight coordinator that manages card assignments and integrates with existing systems:

```python
class StrategyCardCoordinator:
    """Lightweight coordinator for strategy card system integration."""

    def __init__(self, strategic_action_manager: StrategicActionManager):
        self._strategic_action_manager = strategic_action_manager
        self._card_assignments: Dict[str, StrategyCardType] = {}
        self._exhausted_cards: Set[StrategyCardType] = set()

    # Card selection (integrates with game state)
    def assign_strategy_card(self, player_id: str, card: StrategyCardType) -> Result
    def get_available_cards(self) -> List[StrategyCardType]

    # Initiative order (pure calculation, no state)
    def calculate_initiative_order(self, player_assignments: Dict[str, StrategyCardType]) -> List[str]

    # Integration points
    def integrate_with_strategic_actions(self) -> None
```

### 2. Enhanced StrategicActionManager (EXTEND EXISTING)

Extend our existing Rule 82 implementation to work with the strategy card coordinator:

```python
# Existing StrategicActionManager gets minimal extensions
class StrategicActionManager:
    # Existing methods remain unchanged

    # NEW: Integration method
    def set_strategy_card_coordinator(self, coordinator: StrategyCardCoordinator) -> None

    # ENHANCED: Use coordinator for card state
    def execute_strategic_action(self, player_id: str) -> StrategicActionResult:
        # Leverage coordinator for card validation and state management
```

### 3. Strategy Card Registry (REUSE EXISTING PATTERN)

Follow the pattern established by Rule 91 (Technology Strategy Card) for individual strategy card implementations:

```python
# Each strategy card follows the TechnologyStrategyCard pattern
class LeadershipStrategyCard(BaseStrategyCard):
    """Follows exact pattern from TechnologyStrategyCard implementation."""

class DiplomacyStrategyCard(BaseStrategyCard):
    """Follows exact pattern from TechnologyStrategyCard implementation."""

# etc. for all 8 cards
```

### 4. Game State Integration (EXTEND EXISTING)

Minimal extensions to existing game state to track strategy card assignments:

```python
# GameState gets minimal strategy card tracking
@dataclass
class GameState:
    # Existing fields remain unchanged
    strategy_card_assignments: Dict[str, StrategyCardType] = field(default_factory=dict)
    exhausted_strategy_cards: Set[StrategyCardType] = field(default_factory=set)
```

## Data Models

### Reuse Existing Models

The design leverages existing data structures:

- `StrategyCardType` enum (already exists in constants.py)
- `StrategicActionResult` (from Rule 82)
- `GameState` (existing, minimal extension)
- Player management (existing system)

### New Minimal Models

Only add what's absolutely necessary:

```python
@dataclass
class StrategyCardAssignment:
    """Lightweight assignment tracking."""
    player_id: str
    strategy_card: StrategyCardType
    is_exhausted: bool = False

@dataclass
class InitiativeOrder:
    """Initiative calculation result."""
    ordered_players: List[str]
    card_assignments: Dict[str, StrategyCardType]
```

## Error Handling

### Leverage Existing Patterns

Follow the error handling patterns established in Rules 82 and 91:

- Use existing `Result` types and error classes
- Integrate with existing validation frameworks
- Reuse error message patterns and logging

### Strategy Card Specific Validation

```python
class StrategyCardValidationError(GameValidationError):
    """Extends existing validation error hierarchy."""
    pass

def validate_card_selection(player_id: str, card: StrategyCardType,
                          available_cards: Set[StrategyCardType]) -> ValidationResult:
    """Follows existing validation patterns."""
```

## Testing Strategy

### Integration Testing Focus

Since this design emphasizes integration, testing will focus on:

1. **Integration with Rule 82**: Verify strategic actions work with strategy card coordinator
2. **Integration with Rule 91**: Ensure technology strategy card continues working
3. **Integration with Game State**: Verify state management works seamlessly
4. **Cross-System Workflows**: Test complete card selection → strategic action → exhaustion cycles

### Minimal Unit Testing

Only test new, isolated functionality:
- Initiative order calculation logic
- Card assignment validation
- Coordinator state management

### Reuse Existing Test Patterns

Follow the TDD patterns established in Rules 82 and 91:
- Same test structure and naming conventions
- Same assertion patterns and helper methods
- Same coverage expectations

## Implementation Phases

### Phase 1: Core Integration (Minimal New Code)

1. Create `StrategyCardCoordinator` with basic assignment tracking
2. Extend `StrategicActionManager` with coordinator integration
3. Add minimal game state extensions
4. Implement initiative order calculation

### Phase 2: Strategy Card Registry (Follow Existing Pattern)

1. Create `BaseStrategyCard` following `TechnologyStrategyCard` pattern
2. Implement all 8 strategy cards using established patterns
3. Register cards with coordinator

### Phase 3: System Integration (Connect Everything)

1. Integrate coordinator with game state management
2. Connect with existing phase management
3. Ensure seamless operation with Rules 82 and 91
4. Add comprehensive integration tests

## Design Decisions and Rationales

### 1. Coordinator Pattern Over Monolithic Manager

**Decision**: Use a lightweight coordinator that orchestrates existing systems rather than a large new manager.

**Rationale**: Leverages proven Rule 82 and Rule 91 implementations, reduces code duplication, maintains system boundaries.

### 2. Extend Rather Than Replace

**Decision**: Extend existing `StrategicActionManager` rather than creating a new action system.

**Rationale**: Rule 82 is already proven and tested. Extension maintains backward compatibility and reuses robust workflows.

### 3. Follow Rule 91 Pattern for Individual Cards

**Decision**: Each strategy card implementation follows the exact pattern established by `TechnologyStrategyCard`.

**Rationale**: Rule 91 provides a proven template for strategy card implementation with proper integration points.

### 4. Minimal Game State Changes

**Decision**: Add only essential fields to `GameState` for strategy card tracking.

**Rationale**: Preserves existing game state architecture while enabling necessary functionality.

### 5. Pure Function Initiative Calculation

**Decision**: Initiative order calculation is a pure function with no side effects.

**Rationale**: Easier to test, reason about, and integrate. Follows functional programming principles for deterministic operations.

This design ensures we build on our solid foundation rather than reinventing systems, creating a cohesive strategy card framework through intelligent integration of existing robust components.

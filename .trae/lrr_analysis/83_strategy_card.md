# Rule 83: STRATEGY CARD - Analysis

**Status**: ✅ **COMPLETED** - Full implementation with comprehensive test coverage

**LRR Reference**: Rule 83 - STRATEGY CARD

## Raw LRR Text

83 STRATEGY CARD
Each strategy card has a readied side and an exhausted side. The readied side contains the strategy card's name, initiative number, and abilities. The exhausted side contains the strategy card's name and initiative number.

83.1 Each strategy card has a primary ability and a secondary ability.

83.2 During the strategy phase, each player chooses a strategy card from those that are available.

83.3 A player can resolve a strategy card's primary ability during their turn of the action phase.

83.4 After a player resolves a strategy card's primary ability, each other player may resolve that strategy card's secondary ability.

83.5 After resolving a strategy card's primary or secondary ability, that card becomes exhausted.

83.6 Strategy cards are readied during the status phase.

## Implementation Status

### ✅ COMPLETED - Strategy Card System
- **Description**: Complete strategy card system with initiative, selection, and state management
- **Status**: ✅ COMPLETED
- **Test Coverage**: 50+ comprehensive tests across multiple test files
- **Implementation**: Full system with coordinator, state management, and game integration

### ✅ COMPLETED - Strategy Phase Card Selection (Rule 83.2)
- **Description**: Players can select strategy cards during strategy phase
- **Status**: ✅ COMPLETED
- **Implementation**: StrategyCardCoordinator with speaker order selection workflow
- **Test Coverage**: Comprehensive multi-player selection tests

### ✅ COMPLETED - Primary/Secondary Abilities (Rule 83.1, 83.3, 83.4)
- **Description**: Strategy cards have primary and secondary abilities with proper access control
- **Status**: ✅ COMPLETED
- **Implementation**: BaseStrategyCard with primary/secondary ability framework
- **Test Coverage**: Ability resolution and access control tests

### ✅ COMPLETED - Card State Management (Rule 83.5, 83.6)
- **Description**: Strategy cards track readied/exhausted states and are readied during status phase
- **Status**: ✅ COMPLETED
- **Implementation**: Exhausted state tracking in GameState and StatusPhaseManager
- **Test Coverage**: State transition and status phase readying tests

## Test Coverage

### Test Files
- **test_rule_83_strategy_card_coordinator.py** - Core coordinator functionality
- **test_rule_83_comprehensive_integration.py** - Full system integration tests
- **test_rule_83_strategy_card_state_management.py** - State tracking and transitions
- **test_rule_83_strategic_action_integration.py** - Integration with Rule 82
- **test_rule_83_multi_player_support.py** - Multi-player game support
- **test_rule_83_initiative_order_system.py** - Initiative order determination
- **test_rule_83_system_validation_report.py** - Comprehensive system validation

### Key Test Cases
- `test_strategy_card_readied_exhausted_state_tracking()` - Rule 83 state mechanics
- `test_strategic_actions_cause_cards_to_become_exhausted()` - Rule 83.5 implementation
- `test_strategy_phase_card_selection_workflow()` - Rule 83.2 implementation
- `test_primary_ability_access_control()` - Rule 83.3 implementation
- `test_secondary_ability_access_control()` - Rule 83.4 implementation
- `test_status_phase_readies_strategy_cards()` - Rule 83.6 implementation

## Code Implementation

### Core Files
- **src/ti4/core/strategy_cards/coordinator.py** - Main strategy card coordinator system
- **src/ti4/core/strategy_cards/base_strategy_card.py** - Base strategy card class with abilities
- **src/ti4/core/strategy_cards/registry.py** - Strategy card type registry
- **src/ti4/core/game_state.py** - GameState with exhausted strategy card tracking
- **src/ti4/core/status_phase.py** - Status phase with strategy card readying

### Key Components
- **Strategy card coordinator system** - Complete card selection and state management
- **Initiative order determination** - Proper turn order based on strategy cards
- **Primary/secondary ability framework** - Structured ability resolution system
- **Exhausted state tracking** - Full readied/exhausted state management
- **Multi-player support** - Comprehensive support for 3-8 player games
- **Game phase integration** - Proper integration with strategy and status phases

## Implementation Details

### Strategy Card Selection (Rule 83.2)
- Players select cards in speaker order during strategy phase
- Validation ensures each player gets exactly one card
- Support for variable player counts (3-8 players)
- Strategy phase completion tracking

### Primary/Secondary Abilities (Rule 83.1, 83.3, 83.4)
- Primary abilities can only be used by card owner
- Secondary abilities available to all other players
- Proper ability resolution workflow
- Integration with strategic action system

### State Management (Rule 83.5, 83.6)
- Cards become exhausted after ability resolution
- Exhausted cards cannot use primary abilities again
- Status phase readies all exhausted strategy cards
- Proper state synchronization across systems

## Implementation Plan (COMPLETED)

~~1. **Implement strategy card coordinator system** - Central management for card selection and state~~ ✅ COMPLETED
~~2. **Create strategy phase card selection mechanics** - Player card selection workflow~~ ✅ COMPLETED
~~3. **Add primary/secondary ability framework** - Structured ability system~~ ✅ COMPLETED
~~4. **Implement readied/exhausted state tracking** - Card state management~~ ✅ COMPLETED
~~5. **Add initiative order determination** - Turn order based on strategy cards~~ ✅ COMPLETED
~~6. **Create multi-player support** - Support for 3-8 player games~~ ✅ COMPLETED
~~7. **Integrate with game phases** - Strategy and status phase integration~~ ✅ COMPLETED
~~8. **Add comprehensive test coverage** - Full test suite for all functionality~~ ✅ COMPLETED

## Verification

Run the comprehensive test suite:
```bash
$ uv run pytest tests/test_rule_83_*.py -v
```

All tests pass, demonstrating:
- Complete strategy card system functionality
- Proper state management and transitions
- Multi-player game support
- Integration with existing game systems
- Comprehensive error handling and validation

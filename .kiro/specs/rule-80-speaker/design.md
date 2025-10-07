# Design Document

## Overview

This design document outlines the implementation of Rule 80: SPEAKER for the TI4 AI system. The speaker system is a core game mechanic that manages initiative order, tie-breaking authority, and agenda phase responsibilities. The implementation will build upon the existing `SpeakerManager` class in `src/ti4/core/speaker.py` and integrate with existing systems including the agenda phase, Politics strategy card, and game state management.

## Architecture

### Core Components

#### SpeakerManager (Enhanced)
The existing `SpeakerManager` class will be enhanced to provide comprehensive speaker functionality:

- **Speaker Assignment**: Track and manage the current speaker
- **Initiative Order**: Calculate turn order with speaker first
- **Tie Breaking**: Resolve ties using speaker authority
- **Token Passing**: Handle speaker token transfers during agenda phase
- **Politics Integration**: Support speaker token claiming via Politics strategy card

#### SpeakerSystem Integration
The existing `SpeakerSystem` class in the agenda phase will be integrated with the enhanced `SpeakerManager` to ensure consistency across the codebase.

#### Game State Integration
The speaker system will integrate with the existing game state management to ensure speaker information is properly tracked and persisted.

## Components and Interfaces

### Enhanced SpeakerManager Interface

```python
class SpeakerManager:
    """Enhanced manager for Rule 80: SPEAKER functionality."""

    # Core speaker management
    def assign_speaker(self, game_state: GameState, player_id: str) -> GameState
    def get_current_speaker(self, game_state: GameState) -> str | None
    def is_speaker(self, game_state: GameState, player_id: str) -> bool

    # Initiative order (Rule 80.1)
    def get_initiative_order(self, game_state: GameState) -> list[str]
    def calculate_turn_order(self, game_state: GameState, players: list[str]) -> list[str]

    # Tie breaking (Rule 80.2)
    def break_tie(self, game_state: GameState, tied_players: list[str]) -> str
    def resolve_voting_tie(self, game_state: GameState, vote_tally: dict[str, int], chosen_outcome: str) -> VotingTieResult

    # Token passing (Rule 80.3)
    def pass_speaker_token(self, game_state: GameState, new_speaker_id: str) -> GameState
    def can_pass_speaker_token(self, game_state: GameState, current_speaker: str, target_player: str) -> bool

    # Politics strategy card integration (Rule 80.4)
    def claim_speaker_via_politics(self, game_state: GameState, player_id: str) -> GameState
    def can_claim_speaker_via_politics(self, game_state: GameState, player_id: str) -> bool

    # Agenda phase integration
    def get_voting_order(self, game_state: GameState, players: list[str]) -> list[str]
    def should_reveal_agenda(self, game_state: GameState, player_id: str) -> bool
```

### Supporting Data Classes

```python
@dataclass
class VotingTieResult:
    """Result of speaker tie-breaking in voting."""
    winning_outcome: str
    resolved_by_speaker: bool
    speaker_id: str
    original_tally: dict[str, int]

@dataclass
class SpeakerTransition:
    """Result of speaker token passing."""
    success: bool
    previous_speaker: str | None
    new_speaker: str
    transition_reason: str  # "agenda_phase", "politics_card", "game_start"
    error_message: str | None = None
```

### Integration Points

#### Game State Integration
- Extend `GameState` to include speaker tracking methods
- Ensure speaker information is included in game state serialization
- Provide speaker change notifications to other game systems

#### Agenda Phase Integration
- Integrate with existing `AgendaPhase` and `SpeakerSystem` classes
- Ensure speaker reveals agenda cards
- Implement speaker-last voting order
- Handle speaker tie-breaking in agenda resolution

#### Politics Strategy Card Integration
- Enhance `PoliticsStrategyCard` to support speaker token claiming
- Provide alternative to action card drawing when claiming speaker token
- Validate Politics card holder can claim speaker token

#### Initiative System Integration
- Create initiative order calculation that places speaker first
- Handle initiative ties with speaker authority
- Integrate with existing strategy card selection systems

## Data Models

### Speaker State
The speaker state will be managed through the existing game state system with the following additions:

```python
# In GameState class
speaker_id: str | None  # Current speaker player ID
speaker_history: list[SpeakerTransition]  # History of speaker changes
```

### Speaker Events
Speaker-related events will be tracked for game history and debugging:

```python
@dataclass
class SpeakerEvent:
    """Event representing a speaker-related action."""
    event_type: str  # "assigned", "passed", "claimed_via_politics", "tie_broken"
    player_id: str
    previous_speaker: str | None
    timestamp: datetime
    context: dict[str, Any]  # Additional context (e.g., agenda name for tie-breaking)
```

## Error Handling

### Validation Errors
- **Invalid Player**: Attempting to assign speaker to non-existent player
- **Invalid Token Pass**: Attempting to pass token to invalid target
- **Politics Card Validation**: Attempting to claim speaker without Politics card
- **Agenda Phase Validation**: Invalid speaker actions during agenda phase

### Error Recovery
- Graceful handling of speaker assignment failures
- Fallback mechanisms for tie-breaking when speaker is unavailable
- Validation of speaker state consistency across game components

### Error Types
```python
class SpeakerError(Exception):
    """Base exception for speaker-related errors."""
    pass

class InvalidSpeakerAssignmentError(SpeakerError):
    """Raised when attempting to assign invalid speaker."""
    pass

class SpeakerTokenPassError(SpeakerError):
    """Raised when speaker token passing fails."""
    pass

class SpeakerAuthorityError(SpeakerError):
    """Raised when speaker authority is misused."""
    pass
```

## Testing Strategy

### Unit Tests
- **Speaker Assignment**: Test basic speaker assignment and retrieval
- **Initiative Order**: Verify speaker-first initiative calculation
- **Tie Breaking**: Test speaker tie-breaking authority
- **Token Passing**: Validate speaker token transfer mechanics
- **Politics Integration**: Test speaker claiming via Politics strategy card
- **Validation**: Test error handling and input validation

### Integration Tests
- **Agenda Phase Integration**: Test speaker role in agenda resolution
- **Game State Integration**: Verify speaker state persistence
- **Strategy Card Integration**: Test Politics card speaker claiming
- **Multi-Player Scenarios**: Test speaker functionality with multiple players

### Edge Case Tests
- **No Speaker Scenarios**: Handle games without assigned speaker
- **Speaker Elimination**: Handle speaker player elimination
- **Concurrent Operations**: Test thread safety of speaker operations
- **State Consistency**: Verify speaker state remains consistent across operations

### Test Structure
```python
class TestSpeakerManager:
    """Test suite for SpeakerManager functionality."""

    # Basic functionality tests
    def test_assign_speaker_success(self)
    def test_assign_speaker_invalid_player(self)
    def test_get_current_speaker(self)
    def test_is_speaker_check(self)

    # Initiative order tests (Rule 80.1)
    def test_initiative_order_speaker_first(self)
    def test_initiative_order_no_speaker(self)
    def test_calculate_turn_order_with_strategy_cards(self)

    # Tie breaking tests (Rule 80.2)
    def test_break_tie_speaker_wins(self)
    def test_break_tie_speaker_not_tied(self)
    def test_resolve_voting_tie(self)

    # Token passing tests (Rule 80.3)
    def test_pass_speaker_token_success(self)
    def test_pass_speaker_token_invalid_target(self)
    def test_can_pass_speaker_token_validation(self)

    # Politics integration tests (Rule 80.4)
    def test_claim_speaker_via_politics_success(self)
    def test_claim_speaker_via_politics_no_card(self)
    def test_can_claim_speaker_via_politics(self)

    # Agenda phase integration tests
    def test_get_voting_order_speaker_last(self)
    def test_should_reveal_agenda_speaker_only(self)

    # Error handling tests
    def test_invalid_player_assignment_error(self)
    def test_speaker_token_pass_error(self)
    def test_speaker_authority_error(self)
```

## Implementation Plan

### Phase 1: Core Speaker Management
1. Enhance existing `SpeakerManager` class with comprehensive functionality
2. Implement speaker assignment and retrieval methods
3. Add input validation and error handling
4. Create basic unit tests for core functionality

### Phase 2: Initiative Order Implementation
1. Implement `get_initiative_order` method with speaker-first logic
2. Add `calculate_turn_order` method for strategy card integration
3. Create tie-breaking logic for initiative conflicts
4. Add comprehensive tests for initiative order scenarios

### Phase 3: Tie Breaking System
1. Implement `break_tie` method for general tie resolution
2. Add `resolve_voting_tie` method for agenda phase integration
3. Create tie-breaking validation and error handling
4. Add tests for various tie-breaking scenarios

### Phase 4: Token Passing Mechanics
1. Implement `pass_speaker_token` method for agenda phase
2. Add validation for token passing operations
3. Create speaker transition tracking and history
4. Add tests for token passing scenarios

### Phase 5: Politics Strategy Card Integration
1. Implement `claim_speaker_via_politics` method
2. Add validation for Politics card holder requirements
3. Integrate with existing `PoliticsStrategyCard` implementation
4. Add tests for Politics card speaker claiming

### Phase 6: Agenda Phase Integration
1. Integrate with existing `AgendaPhase` and `SpeakerSystem` classes
2. Implement speaker-specific agenda phase methods
3. Add voting order calculation with speaker-last logic
4. Add comprehensive integration tests

### Phase 7: Game State Integration
1. Extend `GameState` with speaker tracking capabilities
2. Implement speaker state serialization and persistence
3. Add speaker change notifications to other systems
4. Add tests for game state integration

### Phase 8: Comprehensive Testing and Validation
1. Create comprehensive test suite covering all functionality
2. Add integration tests with existing game systems
3. Perform edge case testing and error scenario validation
4. Add performance testing for speaker operations

## Dependencies

### Existing Systems
- **Game State Management**: Core game state tracking and persistence
- **Agenda Phase**: Existing agenda resolution and voting systems
- **Politics Strategy Card**: Existing strategy card implementation
- **Player Management**: Player tracking and validation systems

### New Dependencies
- **Speaker Event System**: For tracking speaker-related events
- **Initiative Order System**: For calculating turn order with speaker priority
- **Tie Breaking System**: For resolving conflicts using speaker authority

## Performance Considerations

### Optimization Strategies
- **Caching**: Cache initiative order calculations when speaker doesn't change
- **Lazy Loading**: Load speaker history only when needed
- **Efficient Lookups**: Use efficient data structures for player validation
- **Minimal State Changes**: Only update game state when speaker actually changes

### Scalability
- **Multi-Player Support**: Ensure speaker system scales to maximum player count
- **Concurrent Access**: Handle concurrent speaker operations safely
- **Memory Usage**: Minimize memory footprint of speaker tracking
- **Performance Monitoring**: Track speaker operation performance metrics

## Security and Validation

### Input Validation
- **Player ID Validation**: Ensure all player IDs are valid and exist
- **Speaker Authority Validation**: Verify speaker has authority for requested actions
- **Token Passing Validation**: Validate token passing follows game rules
- **Politics Card Validation**: Verify Politics card holder can claim speaker token

### State Consistency
- **Speaker State Integrity**: Ensure speaker state remains consistent across operations
- **Cross-System Consistency**: Maintain consistency between speaker systems
- **Transaction Safety**: Ensure speaker operations are atomic and safe
- **Rollback Capability**: Support rollback of failed speaker operations

This design provides a comprehensive foundation for implementing Rule 80: SPEAKER while integrating seamlessly with existing TI4 AI systems and maintaining high code quality standards.

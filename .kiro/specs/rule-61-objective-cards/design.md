# Design Document - Rule 61: OBJECTIVE CARDS Completion

## Overview

This design completes the implementation of Rule 61: OBJECTIVE CARDS by building upon the existing ~85% complete foundation. The current system has comprehensive test coverage for core mechanics but lacks critical components for a fully functional objective system. This design addresses the remaining gaps while maintaining backward compatibility with existing implementations.

## Architecture

### Current System Analysis

The existing objective system has these components:
- **Core Framework**: `src/ti4/core/objective.py` - Basic objective structure
- **Public Objectives**: `src/ti4/core/public_objectives.py` - Partial public objective implementations
- **Game State Integration**: Victory point tracking and objective completion in `GameState`
- **Test Coverage**: 63 comprehensive tests across multiple test files

### Missing Components

1. **Public Objective Setup System**: Stage I/II progression and revelation mechanics
2. **Home System Control Validation**: Rule 61.16 compliance checking
3. **Concrete Objective Cards**: All 80 official objective implementations
4. **Victory Point Scoreboard Integration**: Complete integration with victory tracking

## Components and Interfaces

### 1. Public Objective Setup System

```python
@dataclass
class PublicObjectiveSetup:
    """Manages the setup and progression of public objectives."""
    stage_i_objectives: List[ObjectiveCard]
    stage_ii_objectives: List[ObjectiveCard]
    revealed_objectives: List[ObjectiveCard]
    current_stage: Literal["stage_i", "stage_ii", "complete"]

class PublicObjectiveManager:
    """Manages public objective revelation and progression."""

    def setup_objectives(self, game_state: GameState) -> None:
        """Set up 5 Stage I and 5 Stage II objectives face-down."""

    def reveal_next_objective(self, speaker_id: str) -> ObjectiveCard:
        """Reveal the next public objective during status phase."""

    def check_game_end_condition(self) -> bool:
        """Check if all objectives are revealed (triggers game end)."""

    def get_available_objectives_for_scoring(self) -> List[ObjectiveCard]:
        """Get currently revealed objectives available for scoring."""
```

### 2. Home System Control Validator

```python
class HomeSystemControlValidator:
    """Validates home system control for public objective eligibility."""

    def validate_home_system_control(self, player_id: str, game_state: GameState) -> ValidationResult:
        """Validate that player controls all planets in their home system."""

    def get_home_system_planets(self, player_id: str, game_state: GameState) -> List[Planet]:
        """Get all planets in player's home system."""

    def check_planet_control(self, planet: Planet, player_id: str) -> bool:
        """Check if player controls a specific planet."""
```

### 3. Concrete Objective Card System

```python
class ObjectiveCardFactory:
    """Factory for creating concrete objective card instances."""

    @staticmethod
    def create_all_objectives() -> Dict[str, ObjectiveCard]:
        """Create all 80 official TI4 objective cards."""

    @staticmethod
    def create_stage_i_objectives() -> List[ObjectiveCard]:
        """Create all 20 Stage I public objectives."""

    @staticmethod
    def create_stage_ii_objectives() -> List[ObjectiveCard]:
        """Create all 20 Stage II public objectives."""

    @staticmethod
    def create_secret_objectives() -> List[ObjectiveCard]:
        """Create all 40 secret objectives."""

class ConcreteObjectiveRequirements:
    """Implementations of specific objective requirement validators."""

    def validate_corner_the_market(self, player_id: str, game_state: GameState) -> bool:
        """Control 4 planets that each have the same planet trait."""

    def validate_develop_weaponry(self, player_id: str, game_state: GameState) -> bool:
        """Own 2 unit upgrade technologies."""

    def validate_diversify_research(self, player_id: str, game_state: GameState) -> bool:
        """Own 2 technologies in each of 2 colors."""

    # ... implementations for all 80 objectives
```

### 4. Enhanced Objective Completion Detection

```python
class ObjectiveEligibilityTracker:
    """Tracks and detects objective eligibility for players."""

    def check_all_objective_eligibility(self, player_id: str, game_state: GameState) -> Dict[str, bool]:
        """Check eligibility for all objectives for a player."""

    def get_newly_eligible_objectives(self, player_id: str, game_state: GameState) -> List[ObjectiveCard]:
        """Get objectives that became newly eligible since last check."""

    def update_eligibility_cache(self, game_state: GameState) -> None:
        """Update cached eligibility data for performance."""
```

### 5. Victory Point Scoreboard Integration

```python
class VictoryPointScoreboard:
    """Manages victory point tracking and scoreboard display."""

    def score_objective(self, player_id: str, objective: ObjectiveCard, game_state: GameState) -> None:
        """Score an objective and update victory points."""

    def place_control_token(self, player_id: str, objective: ObjectiveCard) -> None:
        """Place player's control token on objective card."""

    def advance_victory_track(self, player_id: str, points: int) -> None:
        """Advance player's position on victory point track."""

    def check_victory_condition(self, game_state: GameState) -> Optional[str]:
        """Check if any player has reached victory point threshold."""

    def get_victory_standings(self, game_state: GameState) -> List[PlayerStanding]:
        """Get current victory point standings with tie-breaking."""
```

## Data Models

### Enhanced Objective Card Model

```python
@dataclass
class ObjectiveCard:
    """Enhanced objective card with complete metadata."""
    id: str
    name: str
    condition: str
    points: int
    expansion: Expansion
    phase: Phase
    type: ObjectiveType
    requirement_validator: Callable[[str, GameState], bool]
    category: ObjectiveCategory  # NEW: For grouping similar objectives
    dependencies: List[str]      # NEW: System dependencies (e.g., "technology", "planets")

@dataclass
class ObjectiveRequirement:
    """Detailed requirement specification."""
    description: str
    validator_function: str
    required_systems: List[str]
    validation_complexity: Literal["simple", "moderate", "complex"]

@dataclass
class PlayerStanding:
    """Player victory point standing."""
    player_id: str
    victory_points: int
    scored_objectives: List[ObjectiveCard]
    initiative_order: int
```

### Public Objective Setup Data

```python
@dataclass
class ObjectiveSetupConfiguration:
    """Configuration for objective setup."""
    stage_i_count: int = 5
    stage_ii_count: int = 5
    include_expansions: List[Expansion] = field(default_factory=lambda: [Expansion.BASE])
    random_seed: Optional[int] = None

@dataclass
class ObjectiveRevealState:
    """Current state of objective revelation."""
    revealed_stage_i: List[ObjectiveCard]
    revealed_stage_ii: List[ObjectiveCard]
    remaining_stage_i: List[ObjectiveCard]
    remaining_stage_ii: List[ObjectiveCard]
    current_stage: Literal["stage_i", "stage_ii", "complete"]
```

## Error Handling

### Custom Exception Types

```python
class ObjectiveSystemError(Exception):
    """Base exception for objective system errors."""
    pass

class HomeSystemControlError(ObjectiveSystemError):
    """Raised when player doesn't control home system for public objectives."""
    pass

class ObjectiveAlreadyScoredError(ObjectiveSystemError):
    """Raised when attempting to score an already-scored objective."""
    pass

class ObjectiveNotEligibleError(ObjectiveSystemError):
    """Raised when attempting to score an objective without meeting requirements."""
    pass

class InvalidObjectivePhaseError(ObjectiveSystemError):
    """Raised when attempting to score objective in wrong phase."""
    pass

class AllObjectivesRevealedError(ObjectiveSystemError):
    """Raised when game should end due to all objectives being revealed."""
    pass
```

### Error Recovery Strategies

1. **Validation Failures**: Provide specific feedback about missing requirements
2. **Home System Control**: Clear messaging about which planets need to be controlled
3. **Phase Restrictions**: Guidance on when objectives can be scored
4. **System Integration**: Graceful degradation when dependent systems are unavailable

## Testing Strategy

### Unit Testing Approach

1. **Objective Card Factory Tests**: Verify all 80 objectives are created correctly
2. **Requirement Validator Tests**: Test each objective's requirement validation logic
3. **Public Objective Setup Tests**: Test Stage I/II progression and revelation
4. **Home System Control Tests**: Test validation logic for various home system configurations
5. **Victory Point Integration Tests**: Test scoreboard updates and victory detection

### Integration Testing

1. **End-to-End Objective Scoring**: Complete flow from eligibility to victory points
2. **Game State Integration**: Verify objective system works with existing game state
3. **Phase Integration**: Test objective scoring during different game phases
4. **Multi-Player Scenarios**: Test objective competition and tie-breaking

### Performance Testing

1. **Eligibility Checking**: Ensure sub-50ms validation for all objectives
2. **Batch Operations**: Test performance with multiple simultaneous objective checks
3. **Memory Usage**: Monitor memory consumption with full objective card set
4. **Caching Effectiveness**: Verify eligibility caching improves performance

## Implementation Phases

### Phase 1: Public Objective Setup System
- Implement `PublicObjectiveManager` with Stage I/II progression
- Add objective revelation mechanics during status phase
- Implement game end condition checking
- Create comprehensive tests for setup and revelation

### Phase 2: Home System Control Validation
- Implement `HomeSystemControlValidator` with planet control checking
- Integrate with existing planet control system
- Add validation to public objective scoring flow
- Create tests for various home system configurations

### Phase 3: Concrete Objective Card Implementation
- Implement `ObjectiveCardFactory` with all 80 official objectives
- Create requirement validators for each objective type
- Integrate with existing objective requirement framework
- Add comprehensive tests for each objective's validation logic

### Phase 4: Enhanced Completion Detection
- Implement `ObjectiveEligibilityTracker` with caching
- Add automatic eligibility detection on game state changes
- Optimize performance for real-time eligibility checking
- Create tests for eligibility tracking and caching

### Phase 5: Victory Point Scoreboard Integration
- Implement `VictoryPointScoreboard` with complete victory tracking
- Integrate with existing victory point system
- Add victory condition checking and tie-breaking
- Create tests for victory detection and scoreboard display

### Phase 6: System Integration and Polish
- Integrate all components with existing game systems
- Add comprehensive error handling and recovery
- Optimize performance and memory usage
- Create end-to-end integration tests

## Backward Compatibility

### Existing System Preservation
- All existing objective tests must continue passing
- Current objective scoring API remains unchanged
- Existing victory point tracking continues to work
- No breaking changes to public interfaces

### Migration Strategy
- New components extend existing interfaces
- Gradual replacement of placeholder implementations
- Feature flags for enabling new functionality
- Comprehensive regression testing

## Performance Considerations

### Optimization Strategies
1. **Requirement Validation Caching**: Cache expensive validation results
2. **Lazy Loading**: Load objective cards only when needed
3. **Batch Operations**: Process multiple objectives efficiently
4. **Memory Management**: Efficient storage of objective metadata

### Scalability Targets
- Support for 6-8 player games without performance degradation
- Sub-50ms objective validation for typical game states
- Minimal memory overhead for objective tracking
- Efficient handling of simultaneous objective eligibility checks

This design provides a comprehensive approach to completing the Rule 61: OBJECTIVE CARDS implementation while maintaining the high quality and test coverage standards established in the existing codebase.

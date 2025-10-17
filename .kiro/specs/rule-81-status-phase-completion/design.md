# Rule 81: Status Phase Completion - Design Document

## Overview

This design document outlines the completion of Rule 81 (Status Phase) implementation for the TI4 AI system. The design builds upon the existing 30% implementation (agent readying functionality) and adds the missing 7 core status phase steps to achieve complete round management functionality.

**Design Goals:**
- Complete all 8 LRR-defined status phase steps
- Integrate seamlessly with existing game systems
- Maintain high performance and code quality standards
- Enable proper round progression and phase transitions

## Architecture

### High-Level Architecture

```
StatusPhaseManager (Enhanced)
├── StatusPhaseOrchestrator (New)
│   ├── Step1Handler: ScoreObjectivesStep
│   ├── Step2Handler: RevealObjectiveStep  
│   ├── Step3Handler: DrawActionCardsStep
│   ├── Step4Handler: RemoveCommandTokensStep
│   ├── Step5Handler: GainRedistributeTokensStep
│   ├── Step6Handler: ReadyCardsStep (Enhanced)
│   ├── Step7Handler: RepairUnitsStep
│   └── Step8Handler: ReturnStrategyCardsStep
├── StatusPhaseValidator (New)
├── RoundTransitionManager (New)
└── Existing: ready_all_cards() method
```

### Integration Points

```
StatusPhaseManager
├── ObjectiveSystem (Rule 61) - For scoring and revealing
├── ActionCardSystem (Rule 2) - For drawing cards
├── CommandTokenSystem (Rule 20) - For token management
├── StrategyCardSystem (Rule 83) - For card return
├── LeaderSystem (Rule 51) - For agent readying (existing)
├── UnitSystem - For unit repair
└── GameStateManager - For phase transitions
```

## Components and Interfaces

### 1. StatusPhaseOrchestrator (New)

**Purpose:** Coordinates execution of all 8 status phase steps in proper sequence.

```python
class StatusPhaseOrchestrator:
    """Orchestrates the complete 8-step status phase sequence."""
    
    def execute_complete_status_phase(self, game_state: GameState) -> StatusPhaseResult:
        """Execute all 8 status phase steps in LRR order."""
        
    def execute_step(self, step_number: int, game_state: GameState) -> StepResult:
        """Execute a specific status phase step."""
        
    def validate_step_prerequisites(self, step_number: int, game_state: GameState) -> bool:
        """Validate that prerequisites for a step are met."""
        
    def get_step_handler(self, step_number: int) -> StatusPhaseStepHandler:
        """Get the appropriate handler for a status phase step."""
```

### 2. StatusPhaseStepHandler (Abstract Base)

**Purpose:** Abstract base class for all status phase step implementations.

```python
@dataclass
class StepResult:
    """Result of executing a status phase step."""
    success: bool
    step_name: str
    error_message: str = ""
    players_processed: list[str] = field(default_factory=list)
    actions_taken: list[str] = field(default_factory=list)

class StatusPhaseStepHandler(ABC):
    """Abstract base for status phase step handlers."""
    
    @abstractmethod
    def execute(self, game_state: GameState) -> tuple[StepResult, GameState]:
        """Execute this status phase step."""
        
    @abstractmethod
    def validate_prerequisites(self, game_state: GameState) -> bool:
        """Validate prerequisites for this step."""
        
    @abstractmethod
    def get_step_name(self) -> str:
        """Get the name of this step."""
```

### 3. Step-Specific Handlers

#### ScoreObjectivesStep (Step 1)

```python
class ScoreObjectivesStep(StatusPhaseStepHandler):
    """Handles Step 1: Score Objectives in initiative order."""
    
    def execute(self, game_state: GameState) -> tuple[StepResult, GameState]:
        """Allow each player to score up to 1 public + 1 secret objective."""
        
    def process_player_objective_scoring(
        self, player_id: str, game_state: GameState
    ) -> tuple[int, GameState]:
        """Process objective scoring for a single player."""
        
    def get_scorable_objectives(
        self, player_id: str, game_state: GameState
    ) -> tuple[list[ObjectiveCard], list[ObjectiveCard]]:
        """Get public and secret objectives the player can score."""
```

#### RevealObjectiveStep (Step 2)

```python
class RevealObjectiveStep(StatusPhaseStepHandler):
    """Handles Step 2: Speaker reveals next public objective."""
    
    def execute(self, game_state: GameState) -> tuple[StepResult, GameState]:
        """Speaker reveals the next unrevealed public objective."""
        
    def get_next_unrevealed_objective(self, game_state: GameState) -> ObjectiveCard | None:
        """Get the next objective to reveal."""
        
    def reveal_objective(
        self, objective: ObjectiveCard, game_state: GameState
    ) -> GameState:
        """Reveal a public objective."""
```

#### DrawActionCardsStep (Step 3)

```python
class DrawActionCardsStep(StatusPhaseStepHandler):
    """Handles Step 3: Each player draws one action card."""
    
    def execute(self, game_state: GameState) -> tuple[StepResult, GameState]:
        """Each player draws one action card in initiative order."""
        
    def draw_card_for_player(
        self, player_id: str, game_state: GameState
    ) -> tuple[bool, GameState]:
        """Draw one action card for a specific player."""
```

#### Command Token Management Steps (Steps 4-5)

```python
class RemoveCommandTokensStep(StatusPhaseStepHandler):
    """Handles Step 4: Remove all command tokens from game board."""
    
    def execute(self, game_state: GameState) -> tuple[StepResult, GameState]:
        """Remove all command tokens from board for all players."""

class GainRedistributeTokensStep(StatusPhaseStepHandler):
    """Handles Step 5: Gain 2 tokens and redistribute."""
    
    def execute(self, game_state: GameState) -> tuple[StepResult, GameState]:
        """Give each player 2 tokens and allow redistribution."""
        
    def redistribute_tokens_for_player(
        self, player_id: str, game_state: GameState
    ) -> GameState:
        """Handle token redistribution for a single player."""
```

#### RepairUnitsStep (Step 7)

```python
class RepairUnitsStep(StatusPhaseStepHandler):
    """Handles Step 7: Repair all damaged units."""
    
    def execute(self, game_state: GameState) -> tuple[StepResult, GameState]:
        """Repair all damaged units for all players."""
        
    def repair_player_units(
        self, player_id: str, game_state: GameState
    ) -> tuple[int, GameState]:
        """Repair all damaged units for a specific player."""
```

#### ReturnStrategyCardsStep (Step 8)

```python
class ReturnStrategyCardsStep(StatusPhaseStepHandler):
    """Handles Step 8: Return strategy cards to common area."""
    
    def execute(self, game_state: GameState) -> tuple[StepResult, GameState]:
        """Return all strategy cards to common area."""
        
    def return_player_strategy_card(
        self, player_id: str, game_state: GameState
    ) -> GameState:
        """Return a specific player's strategy card."""
```

### 4. StatusPhaseValidator (New)

**Purpose:** Validates status phase operations and prerequisites.

```python
class StatusPhaseValidator:
    """Validates status phase operations and state."""
    
    def validate_game_state_for_status_phase(self, game_state: GameState) -> bool:
        """Validate that game state is ready for status phase."""
        
    def validate_step_prerequisites(
        self, step_number: int, game_state: GameState
    ) -> tuple[bool, str]:
        """Validate prerequisites for a specific step."""
        
    def validate_objective_scoring(
        self, player_id: str, objective: ObjectiveCard, game_state: GameState
    ) -> bool:
        """Validate that a player can score a specific objective."""
        
    def validate_token_redistribution(
        self, player_id: str, distribution: dict[str, int], game_state: GameState
    ) -> bool:
        """Validate command token redistribution."""
```

### 5. RoundTransitionManager (New)

**Purpose:** Manages transitions between phases after status phase completion.

```python
class RoundTransitionManager:
    """Manages phase transitions after status phase."""
    
    def determine_next_phase(self, game_state: GameState) -> str:
        """Determine the next phase after status phase."""
        
    def transition_to_agenda_phase(self, game_state: GameState) -> GameState:
        """Transition to agenda phase if custodians token removed."""
        
    def transition_to_new_round(self, game_state: GameState) -> GameState:
        """Start new round with strategy phase."""
        
    def update_round_counter(self, game_state: GameState) -> GameState:
        """Update round counter and related state."""
```

## Data Models

### StatusPhaseResult

```python
@dataclass
class StatusPhaseResult:
    """Result of complete status phase execution."""
    success: bool
    steps_completed: list[str]
    step_results: dict[int, StepResult]
    total_execution_time: float
    next_phase: str
    error_message: str = ""
    
    def get_step_result(self, step_number: int) -> StepResult | None:
        """Get result for a specific step."""
        
    def was_step_successful(self, step_number: int) -> bool:
        """Check if a specific step was successful."""
```

### Enhanced StatusPhaseManager

```python
class StatusPhaseManager:
    """Enhanced status phase manager with complete functionality."""
    
    def __init__(self):
        self.orchestrator = StatusPhaseOrchestrator()
        self.validator = StatusPhaseValidator()
        self.transition_manager = RoundTransitionManager()
    
    def execute_complete_status_phase(self, game_state: GameState) -> tuple[StatusPhaseResult, GameState]:
        """Execute complete status phase with all 8 steps."""
        
    def execute_single_step(
        self, step_number: int, game_state: GameState
    ) -> tuple[StepResult, GameState]:
        """Execute a single status phase step."""
        
    # Existing method - enhanced
    def ready_all_cards(self, game_state: GameState) -> GameState:
        """Ready all exhausted cards (Step 6) - existing implementation."""
```

## Error Handling

### Error Categories

1. **Validation Errors**: Prerequisites not met, invalid game state
2. **Integration Errors**: Failures in system integration points
3. **Resource Errors**: Missing objectives, empty action card deck
4. **State Errors**: Inconsistent game state during execution

### Error Handling Strategy

```python
class StatusPhaseError(Exception):
    """Base exception for status phase errors."""
    
class StepValidationError(StatusPhaseError):
    """Raised when step prerequisites are not met."""
    
class SystemIntegrationError(StatusPhaseError):
    """Raised when integration with other systems fails."""
    
class GameStateError(StatusPhaseError):
    """Raised when game state is invalid for status phase."""
```

### Recovery Mechanisms

- **Graceful Degradation**: Skip optional steps if they fail
- **State Rollback**: Revert to previous state on critical failures
- **Partial Execution**: Complete successful steps, report failures
- **Retry Logic**: Retry failed operations with exponential backoff

## Testing Strategy

### Unit Testing

1. **Step Handler Tests**: Each step handler tested in isolation
2. **Orchestrator Tests**: Complete sequence execution testing
3. **Validator Tests**: All validation logic thoroughly tested
4. **Integration Tests**: System integration points validated

### Test Categories

```python
class TestStatusPhaseOrchestrator:
    """Test complete status phase orchestration."""
    
    def test_complete_status_phase_execution(self):
        """Test all 8 steps execute in correct order."""
        
    def test_step_failure_handling(self):
        """Test handling of individual step failures."""

class TestScoreObjectivesStep:
    """Test Step 1: Score Objectives."""
    
    def test_initiative_order_processing(self):
        """Test players processed in initiative order."""
        
    def test_objective_scoring_limits(self):
        """Test 1 public + 1 secret objective limit."""

class TestIntegrationPoints:
    """Test integration with existing systems."""
    
    def test_objective_system_integration(self):
        """Test integration with objective scoring system."""
        
    def test_command_token_system_integration(self):
        """Test integration with command token management."""
```

### Performance Testing

- **Complete Status Phase**: <500ms execution time
- **Individual Steps**: <100ms execution time each
- **Memory Usage**: Minimal memory allocation during execution
- **Concurrent Access**: Thread-safe operation validation

### Integration Testing

```python
class TestStatusPhaseIntegration:
    """Test status phase integration with game flow."""
    
    def test_end_to_end_round_progression(self):
        """Test complete round from action phase through status phase."""
        
    def test_agenda_phase_transition(self):
        """Test transition to agenda phase when custodians token removed."""
        
    def test_new_round_transition(self):
        """Test transition to new round when no agenda phase."""
```

## Implementation Plan

### Phase 1: Core Infrastructure (Week 1)

1. **StatusPhaseOrchestrator**: Complete step coordination
2. **StatusPhaseStepHandler**: Abstract base class
3. **StatusPhaseResult**: Data models and result handling
4. **StatusPhaseValidator**: Basic validation framework

### Phase 2: Step Implementations (Week 1-2)

1. **Steps 1-3**: Score objectives, reveal objectives, draw action cards
2. **Steps 4-5**: Command token management
3. **Step 6**: Enhance existing ready cards functionality
4. **Steps 7-8**: Repair units, return strategy cards

### Phase 3: Integration and Testing (Week 2)

1. **System Integration**: Connect with existing game systems
2. **RoundTransitionManager**: Phase transition logic
3. **Comprehensive Testing**: Unit, integration, and performance tests
4. **Error Handling**: Complete error handling and recovery

### Success Criteria

- ✅ All 8 status phase steps implemented and tested
- ✅ Complete integration with existing game systems
- ✅ 95%+ test coverage achieved
- ✅ Performance benchmarks met (<500ms total execution)
- ✅ Round progression functional (status → agenda/strategy phase)
- ✅ Backward compatibility maintained with existing code

This design provides a comprehensive, maintainable, and performant solution for completing Rule 81 (Status Phase) implementation while building on the existing foundation and integrating seamlessly with the broader TI4 AI system.
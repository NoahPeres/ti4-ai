# Design Document: Rule 7 - AGENDA CARDS

## Overview

This design document outlines the implementation of Rule 7: AGENDA CARDS for the TI4 AI system. The implementation will build upon the existing agenda phase infrastructure while providing a comprehensive agenda card system that includes all base game agenda cards from the ability compendium, proper deck management, law persistence, and integration with the voting system.

## Architecture

### System Components

```
AgendaCardSystem
├── AgendaDeck (deck management)
├── AgendaCardRegistry (card registry and factory)
├── LawManager (persistent law effects)
├── AgendaEffectResolver (effect execution)
├── base/
│   ├── BaseAgendaCard (abstract base)
│   ├── LawCard (persistent effects)
│   └── DirectiveCard (immediate effects)
└── concrete/
    ├── AntiIntellectualRevolution
    ├── ClassifiedDocumentLeaks
    ├── CommitteeFormation
    └── ... (individual card implementations)
```

### Integration Points

- **Existing AgendaPhase**: Extends current agenda phase with proper card management
- **VotingSystem**: Integrates with existing voting mechanics
- **GameState**: Tracks active laws and agenda deck state
- **Technology Card Framework**: Follows established patterns for card implementations

## Components and Interfaces

### Core Data Models

#### Enhanced AgendaCard

```python
@dataclass
class AgendaCard:
    """Enhanced agenda card with complete game data."""

    name: str
    agenda_type: AgendaType  # LAW or DIRECTIVE
    outcomes: list[str]  # Voting outcomes (For/Against, Elect, etc.)

    # Effect descriptions
    for_effect: str | None = None
    against_effect: str | None = None
    elect_effect: str | None = None

    # Timing and conditions
    play_timing: str | None = None  # When card effects trigger
    play_timing_2: str | None = None  # Secondary timing

    # Game metadata
    expansion: str = "Base"
    flavor_text: str | None = None

    # Computed properties
    def get_voting_outcomes(self) -> list[str]:
        """Get all possible voting outcomes for this agenda."""

    def is_law(self) -> bool:
        """Check if this is a law (persistent effect)."""

    def is_directive(self) -> bool:
        """Check if this is a directive (immediate effect)."""
```

#### Law Tracking

```python
@dataclass
class ActiveLaw:
    """Represents a law currently in effect."""

    agenda_card: AgendaCard
    enacted_round: int
    elected_target: str | None = None  # For laws with election outcomes
    effect_description: str = ""

    def applies_to_context(self, context: GameContext) -> bool:
        """Check if this law applies to the given game context."""
```

#### Agenda Deck Management

```python
class AgendaDeck:
    """Manages the agenda deck with proper shuffling and drawing."""

    def __init__(self, cards: list[AgendaCard]):
        self._deck: list[AgendaCard] = []
        self._discard_pile: list[AgendaCard] = []
        self._removed_cards: list[AgendaCard] = []

    def shuffle(self) -> None:
        """Shuffle the deck."""

    def draw_top_card(self) -> AgendaCard:
        """Draw the top card, reshuffling if needed."""

    def discard_card(self, card: AgendaCard) -> None:
        """Add card to discard pile."""

    def remove_from_game(self, card: AgendaCard) -> None:
        """Permanently remove card from game."""

    def reshuffle_if_needed(self) -> None:
        """Reshuffle discard pile into deck if deck is empty."""
```

### Agenda Card Framework

#### Base Agenda Card Classes

```python
from abc import ABC, abstractmethod

class BaseAgendaCard(ABC):
    """Abstract base class for all agenda cards."""

    @abstractmethod
    def get_name(self) -> str:
        """Get the card name."""

    @abstractmethod
    def get_agenda_type(self) -> AgendaType:
        """Get the agenda type (LAW or DIRECTIVE)."""

    @abstractmethod
    def get_voting_outcomes(self) -> list[str]:
        """Get possible voting outcomes."""

    @abstractmethod
    def resolve_outcome(
        self,
        outcome: str,
        vote_result: VoteResult,
        game_state: GameState
    ) -> AgendaResolutionResult:
        """Resolve the agenda based on voting outcome."""

    def get_flavor_text(self) -> str:
        """Get flavor text for the card."""
        return ""

class LawCard(BaseAgendaCard):
    """Base class for law cards (persistent effects)."""

    def get_agenda_type(self) -> AgendaType:
        return AgendaType.LAW

    @abstractmethod
    def create_active_law(
        self,
        outcome: str,
        elected_target: str | None = None
    ) -> ActiveLaw:
        """Create an active law instance."""

class DirectiveCard(BaseAgendaCard):
    """Base class for directive cards (immediate effects)."""

    def get_agenda_type(self) -> AgendaType:
        return AgendaType.DIRECTIVE

    @abstractmethod
    def execute_immediate_effect(
        self,
        outcome: str,
        vote_result: VoteResult,
        game_state: GameState
    ) -> None:
        """Execute the immediate directive effect."""
```

#### AgendaCardRegistry

```python
class AgendaCardRegistry:
    """Registry of all agenda card implementations."""

    def __init__(self):
        self._cards: dict[str, type[BaseAgendaCard]] = {}
        self._instances: dict[str, BaseAgendaCard] = {}

    def register_card_class(self, card_class: type[BaseAgendaCard]) -> None:
        """Register an agenda card class."""

    def create_card(self, name: str) -> BaseAgendaCard:
        """Create an instance of the specified agenda card."""

    def get_all_card_names(self) -> list[str]:
        """Get names of all registered cards."""

    def get_cards_by_type(self, agenda_type: AgendaType) -> list[BaseAgendaCard]:
        """Get all cards of a specific type."""
```

### Law Management System

#### LawManager

```python
class LawManager:
    """Manages active laws and their persistent effects."""

    def __init__(self):
        self._active_laws: list[ActiveLaw] = []

    def enact_law(self, agenda_card: AgendaCard, elected_target: str | None = None) -> None:
        """Enact a new law."""

    def get_active_laws(self) -> list[ActiveLaw]:
        """Get all currently active laws."""

    def get_laws_affecting_context(self, context: GameContext) -> list[ActiveLaw]:
        """Get laws that affect a specific game context."""

    def remove_law(self, law_name: str) -> bool:
        """Remove a law from play (e.g., via Repeal Law action card)."""

    def check_law_conflicts(self, new_law: AgendaCard) -> list[ActiveLaw]:
        """Check for laws that would be replaced by the new law."""
```

### Effect Resolution System

#### AgendaEffectResolver

```python
class AgendaEffectResolver:
    """Resolves agenda card effects based on voting outcomes."""

    def resolve_agenda_outcome(
        self,
        agenda: AgendaCard,
        vote_result: VoteResult,
        game_state: GameState
    ) -> AgendaResolutionResult:
        """Resolve agenda based on voting outcome."""

    def apply_law_effect(
        self,
        agenda: AgendaCard,
        elected_target: str | None,
        game_state: GameState
    ) -> None:
        """Apply persistent law effect to game state."""

    def execute_directive_effect(
        self,
        agenda: AgendaCard,
        vote_result: VoteResult,
        game_state: GameState
    ) -> None:
        """Execute immediate directive effect."""

    def handle_election_outcome(
        self,
        agenda: AgendaCard,
        elected_target: str,
        game_state: GameState
    ) -> None:
        """Handle election-based agenda outcomes."""
```

### Concrete Agenda Card Implementations

#### Example Law Card Implementation

```python
class AntiIntellectualRevolution(LawCard):
    """Anti-Intellectual Revolution agenda card.

    FOR: After a player researches a technology, they must destroy 1 of their non-fighter ships.
    AGAINST: At the start of the next strategy phase, each player chooses and exhausts 1 planet for each technology they own.
    """

    def get_name(self) -> str:
        return "Anti-Intellectual Revolution"

    def get_voting_outcomes(self) -> list[str]:
        return ["For", "Against"]

    def resolve_outcome(
        self,
        outcome: str,
        vote_result: VoteResult,
        game_state: GameState
    ) -> AgendaResolutionResult:
        if outcome == "For":
            law = self.create_active_law("For")
            game_state.law_manager.enact_law(law)
            return AgendaResolutionResult(
                success=True,
                law_enacted=True,
                description="Anti-Intellectual Revolution enacted: Players must destroy ships when researching"
            )
        else:  # Against
            # Execute immediate effect
            self._exhaust_planets_for_technologies(game_state)
            return AgendaResolutionResult(
                success=True,
                directive_executed=True,
                description="Anti-Intellectual Revolution rejected: Players exhaust planets for technologies"
            )

    def create_active_law(self, outcome: str, elected_target: str | None = None) -> ActiveLaw:
        return ActiveLaw(
            agenda_card=self,
            effect_description="After a player researches a technology, they must destroy 1 of their non-fighter ships",
            trigger_condition="after_technology_research"
        )
```

#### Example Directive Card Implementation

```python
class ClassifiedDocumentLeaks(DirectiveCard):
    """Classified Document Leaks agenda card.

    When revealed: If no scored secret objectives, discard and reveal another.
    Elect Scored Secret Objective: The elected secret objective becomes public.
    """

    def get_name(self) -> str:
        return "Classified Document Leaks"

    def get_voting_outcomes(self) -> list[str]:
        return ["Elect Scored Secret Objective"]

    def should_discard_on_reveal(self, game_state: GameState) -> bool:
        """Check if card should be discarded when revealed."""
        return len(game_state.get_scored_secret_objectives()) == 0

    def resolve_outcome(
        self,
        outcome: str,
        vote_result: VoteResult,
        game_state: GameState
    ) -> AgendaResolutionResult:
        if outcome.startswith("Elect"):
            elected_objective = vote_result.elected_target
            self._make_objective_public(elected_objective, game_state)
            return AgendaResolutionResult(
                success=True,
                directive_executed=True,
                description=f"Secret objective '{elected_objective}' is now public"
            )
```

## Data Models

### Agenda Card Types and Outcomes

Based on the CSV analysis, agenda cards have several patterns:

#### Law Cards (Persistent Effects)
- **For/Against Laws**: Standard voting with persistent effects
- **Election Laws**: Elect a player/planet, then apply persistent effect
- **Minister Cards**: Elect a player who gains ongoing abilities

#### Directive Cards (Immediate Effects)
- **For/Against Directives**: Immediate effects based on vote outcome
- **Election Directives**: Elect target, apply immediate effect
- **Special Directives**: Unique mechanics (e.g., Committee Formation)

#### Voting Outcome Patterns
```python
class VotingOutcomes:
    FOR_AGAINST = ["For", "Against"]
    ELECT_PLAYER = ["Elect Player"]
    ELECT_PLANET_CULTURAL = ["Elect Cultural Planet"]
    ELECT_PLANET_INDUSTRIAL = ["Elect Industrial Planet"]
    ELECT_PLANET_HAZARDOUS = ["Elect Hazardous Planet"]
    ELECT_SECRET_OBJECTIVE = ["Elect Scored Secret Objective"]
```

### Effect Parsing Strategy

The CSV contains complex effect text that needs parsing:

```python
def parse_agenda_effects(effect_text: str) -> dict[str, str]:
    """Parse agenda effect text into structured outcomes.

    Examples:
    - "FOR : Effect text\nAGAINST : Other effect"
    - "Elect Player\nEffect description"
    - "When condition, effect description"
    """
```

## Error Handling

### Validation Strategy

```python
class AgendaCardValidationError(Exception):
    """Raised when agenda card data is invalid."""

class AgendaDeckEmptyError(Exception):
    """Raised when trying to draw from empty deck with no discard pile."""

class LawConflictError(Exception):
    """Raised when laws conflict in unexpected ways."""
```

### Error Recovery

- **Missing Card Data**: Log warning, create placeholder card
- **Invalid Effects**: Use fallback generic effects
- **Deck Management**: Auto-reshuffle when needed
- **Law Conflicts**: Provide clear conflict resolution

## Testing Strategy

### Unit Tests
- AgendaCard creation and validation
- Deck management (shuffle, draw, discard)
- Law persistence and tracking
- Effect resolution for all outcome types
- CSV data loading and parsing

### Integration Tests
- Full agenda phase with real cards
- Law effects during gameplay
- Voting integration with agenda outcomes
- Game state persistence with active laws

### Data Validation Tests
- All CSV agenda cards load correctly
- Effect parsing handles all card types
- Voting outcomes match card specifications

## Implementation Phases

### Phase 1: Core Infrastructure
1. Enhanced AgendaCard data model
2. AgendaDeck management system
3. Basic CSV loading functionality
4. Integration with existing AgendaPhase

### Phase 2: Effect System
1. AgendaEffectResolver implementation
2. LawManager for persistent effects
3. Voting outcome handling
4. Election mechanics

### Phase 3: Complete Card Implementation
1. Implement all base game agenda cards as individual classes
2. Create concrete card implementations following the framework
3. Law conflict resolution
4. Advanced election mechanics

### Phase 4: Integration and Polish
1. Full game state integration
2. Comprehensive error handling
3. Performance optimization
4. Documentation and examples

## Success Criteria

- All base game agenda cards implemented as individual classes
- Complete law persistence system
- Full integration with existing voting mechanics
- Comprehensive test coverage (95%+)
- All agenda effects properly implemented following the framework pattern
- Robust error handling and validation
- Performance meets benchmarks (<100ms per operation)
- Framework ready for POK agenda card expansion

## Future Considerations

- **Prophecy of Kings Expansion**: Framework ready for POK agenda cards
- **Custom Agendas**: Support for user-defined agenda cards
- **Advanced Effects**: Complex timing and interaction handling
- **AI Integration**: Agenda evaluation for AI decision-making

# Agenda Card Framework Developer Guide

## Overview

The Agenda Card Framework provides a comprehensive, type-safe system for implementing all TI4 agenda cards. This guide covers everything you need to know to implement new agenda cards, understand the framework's architecture, and integrate with the existing agenda phase system.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Framework Architecture](#framework-architecture)
3. [Base Classes](#base-classes)
4. [Implementing Agenda Cards](#implementing-agenda-cards)
5. [Law Management System](#law-management-system)
6. [Effect Resolution](#effect-resolution)
7. [Integration Points](#integration-points)
8. [Testing Guidelines](#testing-guidelines)
9. [Examples](#examples)
10. [Troubleshooting](#troubleshooting)

## Quick Start

To implement a new agenda card:

1. **Determine card type** (Law or Directive)
2. **Choose appropriate base class** (`LawCard`, `DirectiveCard`, or `PlanetAttachableCard`)
3. **Create concrete implementation** in `src/ti4/core/agenda_cards/concrete/`
4. **Register with the system** using `AgendaCardRegistry`
5. **Write comprehensive tests**
6. **Update documentation**

## Framework Architecture

The framework follows a clear separation of concerns with distinct layers:

- **Base Classes**: Abstract base classes for different agenda card types
- **Registry System**: Manages agenda card registration and lookup
- **Deck Management**: Handles agenda deck shuffling, drawing, and state
- **Law Management**: Persistent law tracking and effect application
- **Effect Resolution**: Resolves agenda outcomes and applies effects
- **Planet Attachment**: System for cards that attach to planets
- **Validation Framework**: Comprehensive validation for all operations
- **Concrete Implementations**: All specific agenda card implementations

### Design Principles

1. **Type Safety**: Strong typing throughout the framework
2. **Clear Separation**: Laws vs Directives have distinct behaviors
3. **Extensibility**: Easy to add new agenda cards and mechanics
4. **Integration**: Seamless integration with existing game systems
5. **Persistence**: Laws persist across game rounds
6. **Validation**: Comprehensive validation at all levels

## Base Classes

The framework provides several base classes for different agenda card types:

### BaseAgendaCard

Abstract base class for all agenda cards:

```python
class BaseAgendaCard(ABC):
    """Abstract base class for all agenda card implementations."""

    def __init__(self, name: str) -> None:
        self._name = name.strip()

    @property
    def name(self) -> str:
        """Display name of the agenda card."""
        return self._name

    @abstractmethod
    def get_agenda_type(self) -> AgendaType:
        """Get the agenda type (LAW or DIRECTIVE)."""
        ...

    def get_voting_outcomes(self) -> list[str]:
        """Get possible voting outcomes for this agenda."""
        return ["For", "Against"]

    @abstractmethod
    def resolve_outcome(self, outcome: str, vote_result: Any, game_state: Any) -> Any:
        """Resolve the agenda based on voting outcome."""
        ...
```

### LawCard

Base class for law cards (persistent effects):

```python
class LawCard(BaseAgendaCard):
    """Base class for law cards with persistent effects."""

    def get_agenda_type(self) -> AgendaType:
        return AgendaType.LAW

    @abstractmethod
    def create_active_law(
        self, outcome: str, elected_target: str | None = None
    ) -> ActiveLaw:
        """Create an active law instance for persistent tracking."""
        ...

    def get_law_effects(self) -> list[str]:
        """Get list of game mechanics this law affects."""
        return []

    def conflicts_with_law(self, other_law: "ActiveLaw") -> bool:
        """Check if this law conflicts with another active law."""
        return False
```

### DirectiveCard

Base class for directive cards (immediate effects):

```python
class DirectiveCard(BaseAgendaCard):
    """Base class for directive cards with immediate effects."""

    def get_agenda_type(self) -> AgendaType:
        return AgendaType.DIRECTIVE

    @abstractmethod
    def execute_immediate_effect(
        self, outcome: str, vote_result: "VoteResult", game_state: "GameState"
    ) -> None:
        """Execute the immediate directive effect."""
        ...

    def should_discard_on_reveal(self, game_state: "GameState") -> bool:
        """Check if card should be discarded when revealed."""
        return False
```

### PlanetAttachableCard

Base class for agenda cards that attach to planets:

```python
class PlanetAttachableCard(DirectiveCard):
    """Base class for agenda cards that attach to planets."""

    @abstractmethod
    def get_attachment_type(self) -> PlanetAttachmentType:
        """Get the type of planet attachment."""
        ...

    @abstractmethod
    def get_planet_effects(self) -> dict[str, Any]:
        """Get the effects this attachment provides to the planet."""
        ...

    def can_attach_to_planet(self, planet: "Planet") -> bool:
        """Check if this card can attach to the given planet."""
        return True
```

## Implementing Agenda Cards

### Step 1: Determine Card Type

First, determine what type of agenda card you're implementing:

- **Law Card**: Has persistent effects that remain in play (e.g., Fleet Regulations)
- **Directive Card**: Has immediate effects that resolve once (e.g., Classified Document Leaks)
- **Planet Attachable Card**: Attaches to planets with ongoing effects (e.g., Core Mining)

### Step 2: Create Concrete Implementation

Create your implementation in the concrete agenda cards directory:

```python
# Example law card implementation
"""
Example Law agenda card implementation.

This module implements an example law card showing the standard patterns.
"""

from typing import TYPE_CHECKING

from ti4.core.agenda_cards.base.law_card import LawCard
from ti4.core.agenda_cards.effect_resolver import AgendaResolutionResult
from ti4.core.agenda_cards.law_manager import ActiveLaw

if TYPE_CHECKING:
    from ti4.core.agenda_phase import VoteResult
    from ti4.core.game_state import GameState


class ExampleLaw(LawCard):
    """
    Example Law agenda card.

    FOR: [Description of FOR effect]
    AGAINST: [Description of AGAINST effect]
    """

    def __init__(self) -> None:
        """Initialize the Example Law card."""
        super().__init__("Example Law")

    def get_voting_outcomes(self) -> list[str]:
        """Get possible voting outcomes for this agenda."""
        return ["For", "Against"]

    def resolve_outcome(
        self,
        outcome: str,
        vote_result: "VoteResult",
        game_state: "GameState",
    ) -> AgendaResolutionResult:
        """Resolve the agenda based on voting outcome."""
        if outcome not in self.get_voting_outcomes():
            raise ValueError(f"Invalid outcome '{outcome}' for {self.name}")

        if outcome == "For":
            # FOR: Enact law with persistent effect
            return AgendaResolutionResult(
                success=True,
                law_enacted=True,
                description="Example Law enacted: [effect description]",
            )
        else:  # Against
            # AGAINST: Execute immediate directive effect
            return AgendaResolutionResult(
                success=True,
                directive_executed=True,
                description="Example Law rejected: [immediate effect description]",
            )

    def create_active_law(
        self, outcome: str, elected_target: str | None = None
    ) -> ActiveLaw:
        """Create an active law instance for the FOR outcome."""
        if outcome != "For":
            raise ValueError("Can only create active law for 'For' outcome")

        return ActiveLaw(
            agenda_card=self,
            enacted_round=1,  # Set by game state
            effect_description="[Persistent effect description]",
            elected_target=elected_target,
        )
```

### Step 3: Handle Different Voting Patterns

The framework supports various voting patterns:

#### For/Against Voting

```python
def get_voting_outcomes(self) -> list[str]:
    return ["For", "Against"]
```

#### Election Voting

```python
def get_voting_outcomes(self) -> list[str]:
    return ["Elect Player"]  # or "Elect Cultural Planet", etc.
```

#### Mixed Voting

```python
def get_voting_outcomes(self) -> list[str]:
    return ["For", "Against", "Elect Player"]
```

### Step 4: Register the Card

Register your card with the system:

```python
# In the concrete module's __init__.py
from .example_law import ExampleLaw

# The registry will automatically discover and register cards
```

### Step 5: Write Tests

Create comprehensive tests:

```python
# Example test structure
import pytest
from ti4.core.agenda_cards.concrete.example_law import ExampleLaw
from ti4.core.constants import AgendaType


class TestExampleLaw:
    """Test Example Law implementation."""

    def test_basic_properties(self):
        """Test basic agenda card properties."""
        card = ExampleLaw()
        assert card.name == "Example Law"
        assert card.get_agenda_type() == AgendaType.LAW
        assert card.get_voting_outcomes() == ["For", "Against"]

    def test_for_outcome_resolution(self):
        """Test FOR outcome creates active law."""
        card = ExampleLaw()
        # Mock vote_result and game_state
        result = card.resolve_outcome("For", mock_vote_result, mock_game_state)
        assert result.success
        assert result.law_enacted
        assert "enacted" in result.description.lower()

    def test_against_outcome_resolution(self):
        """Test AGAINST outcome executes directive."""
        card = ExampleLaw()
        result = card.resolve_outcome("Against", mock_vote_result, mock_game_state)
        assert result.success
        assert result.directive_executed
        assert "rejected" in result.description.lower()

    def test_create_active_law(self):
        """Test active law creation."""
        card = ExampleLaw()
        active_law = card.create_active_law("For")
        assert active_law.agenda_card == card
        assert active_law.effect_description
        assert active_law.enacted_round == 1

    def test_invalid_outcome_raises_error(self):
        """Test invalid outcomes raise appropriate errors."""
        card = ExampleLaw()
        with pytest.raises(ValueError, match="Invalid outcome"):
            card.resolve_outcome("Invalid", mock_vote_result, mock_game_state)
```

## Law Management System

The `LawManager` handles persistent law effects:

### ActiveLaw

Represents a law currently in effect:

```python
@dataclass
class ActiveLaw:
    """Represents a law currently in effect."""
    agenda_card: BaseAgendaCard
    enacted_round: int
    effect_description: str
    elected_target: str | None = None

    def applies_to_context(self, context: GameContext) -> bool:
        """Check if this law applies to the given game context."""
        # Implementation depends on the specific law
        return True
```

### LawManager Usage

```python
# Get the law manager from game state
law_manager = game_state.law_manager

# Enact a new law
law_manager.enact_law(active_law)

# Check active laws
active_laws = law_manager.get_active_laws()

# Get laws affecting a specific context
relevant_laws = law_manager.get_laws_affecting_context(context)

# Remove a law (e.g., via Repeal Law action card)
law_manager.remove_law("Fleet Regulations")
```

## Effect Resolution

The `AgendaEffectResolver` handles agenda outcome resolution:

### AgendaResolutionResult

```python
@dataclass
class AgendaResolutionResult:
    """Result of agenda resolution."""
    success: bool
    law_enacted: bool = False
    directive_executed: bool = False
    description: str = ""
    elected_target: str | None = None
    errors: list[str] = field(default_factory=list)
```

### Using the Effect Resolver

```python
resolver = AgendaEffectResolver()
result = resolver.resolve_agenda_outcome(agenda_card, vote_result, game_state)

if result.success:
    if result.law_enacted:
        # Law was enacted and is now active
        print(f"Law enacted: {result.description}")
    elif result.directive_executed:
        # Directive effect was executed
        print(f"Directive executed: {result.description}")
else:
    # Handle errors
    for error in result.errors:
        print(f"Error: {error}")
```

## Integration Points

The framework integrates with several existing systems:

### Agenda Phase Integration

```python
# In agenda_phase.py
def reveal_agenda_card(self) -> BaseAgendaCard:
    """Reveal the next agenda card from the deck."""
    card = self.agenda_deck.draw_top_card()

    # Check if card should be discarded on reveal
    if isinstance(card, DirectiveCard) and card.should_discard_on_reveal(self.game_state):
        self.agenda_deck.discard_card(card)
        return self.reveal_agenda_card()  # Reveal another

    return card
```

### Voting System Integration

```python
# Voting validates against agenda card outcomes
def validate_vote_outcome(self, agenda_card: BaseAgendaCard, outcome: str) -> bool:
    """Validate that the outcome is valid for this agenda card."""
    return outcome in agenda_card.get_voting_outcomes()
```

### Game State Integration

```python
# Game state tracks active laws and agenda deck
@dataclass
class GameState:
    law_manager: LawManager
    agenda_deck: AgendaDeck
    # ... other fields
```

## Testing Guidelines

### Test Structure

Follow this structure for agenda card tests:

```python
class TestAgendaCardName:
    """Test [Agenda Card Name] implementation."""

    def test_basic_properties(self):
        """Test basic agenda card properties."""

    def test_voting_outcomes(self):
        """Test voting outcome validation."""

    def test_outcome_resolution(self):
        """Test all outcome resolution paths."""

    def test_law_creation(self):  # For law cards
        """Test active law creation."""

    def test_immediate_effects(self):  # For directive cards
        """Test immediate effect execution."""

    def test_edge_cases(self):
        """Test edge cases and error conditions."""

    def test_integration(self):
        """Test integration with game systems."""
```

### Test Coverage Requirements

- **Basic Properties**: Name, type, voting outcomes
- **All Outcomes**: Test every possible voting outcome
- **Law Persistence**: For law cards, test active law creation
- **Immediate Effects**: For directive cards, test effect execution
- **Edge Cases**: Invalid inputs, error conditions
- **Integration**: Integration with agenda phase and voting

### Test Utilities

The framework provides test utilities:

```python
# In test files
from tests.test_utilities import create_mock_game_state, create_mock_vote_result

def test_agenda_card():
    game_state = create_mock_game_state()
    vote_result = create_mock_vote_result(outcome="For", elected_target=None)
    # Use in tests...
```

## Examples

### Anti-Intellectual Revolution (Law Card)

A law card with For/Against outcomes:

```python
class AntiIntellectualRevolution(LawCard):
    """
    Anti-Intellectual Revolution agenda card.

    FOR: After a player researches a technology, they must destroy 1 of their non-fighter ships.
    AGAINST: At the start of the next strategy phase, each player chooses and exhausts 1 planet for each technology they own.
    """

    def get_voting_outcomes(self) -> list[str]:
        return ["For", "Against"]

    def resolve_outcome(self, outcome: str, vote_result: "VoteResult", game_state: "GameState") -> AgendaResolutionResult:
        if outcome == "For":
            return AgendaResolutionResult(
                success=True,
                law_enacted=True,
                description="Anti-Intellectual Revolution enacted: Players must destroy ships when researching",
            )
        else:  # Against
            return AgendaResolutionResult(
                success=True,
                directive_executed=True,
                description="Anti-Intellectual Revolution rejected: Players exhaust planets for technologies",
            )
```

### Classified Document Leaks (Directive Card)

A directive card with election mechanics:

```python
class ClassifiedDocumentLeaks(DirectiveCard):
    """
    Classified Document Leaks directive card.

    When revealed: If no scored secret objectives, discard and reveal another.
    Elect Scored Secret Objective: The elected secret objective becomes public.
    """

    def get_voting_outcomes(self) -> list[str]:
        return ["Elect Scored Secret Objective"]

    def should_discard_on_reveal(self, game_state: "GameState") -> bool:
        """Check if card should be discarded when revealed."""
        # Check if any player has scored secret objectives
        return not any(game_state.completed_objectives.values())

    def resolve_outcome(self, outcome: str, vote_result: "VoteResult", game_state: "GameState") -> AgendaResolutionResult:
        elected_objective = vote_result.elected_target
        return AgendaResolutionResult(
            success=True,
            directive_executed=True,
            description=f"Secret objective '{elected_objective}' is now public",
            elected_target=elected_objective,
        )
```

### Core Mining (Planet Attachable Card)

A directive card that attaches to planets:

```python
class CoreMining(PlanetAttachableCard):
    """
    Core Mining agenda card.

    Elect Industrial Planet: Attach this card to the elected planet.
    The planet's resource value is increased by 2.
    """

    def get_voting_outcomes(self) -> list[str]:
        return ["Elect Industrial Planet"]

    def get_attachment_type(self) -> PlanetAttachmentType:
        return PlanetAttachmentType.RESOURCE_ENHANCEMENT

    def get_planet_effects(self) -> dict[str, Any]:
        return {"resource_bonus": 2}

    def can_attach_to_planet(self, planet: "Planet") -> bool:
        return planet.planet_type == PlanetType.INDUSTRIAL
```

## Troubleshooting

### Common Issues

#### 1. AgendaCardValidationError

**Problem**: Getting validation errors when creating agenda cards
**Solution**: Check that all required fields are provided and valid

#### 2. Invalid Voting Outcomes

**Problem**: Voting system rejects outcomes
**Solution**: Ensure `get_voting_outcomes()` returns all valid outcomes for the card

#### 3. Law Conflicts

**Problem**: Multiple laws conflicting with each other
**Solution**: Implement `conflicts_with_law()` method to detect and resolve conflicts

#### 4. Missing Integration

**Problem**: Agenda effects not applying to game mechanics
**Solution**: Check integration points in agenda phase and game state

### Debugging Tips

1. **Check Card Registration**: Ensure card is registered with `AgendaCardRegistry`
2. **Verify Outcomes**: Make sure all voting outcomes are handled
3. **Test Integration**: Test each integration point separately
4. **Use Examples**: Compare with existing implementations

### Getting Help

1. **Check Examples**: Look at Anti-Intellectual Revolution and Classified Document Leaks
2. **Read Tests**: Test files show expected behavior patterns
3. **Check Integration**: Look at agenda phase integration
4. **Review Documentation**: This guide covers all common patterns

## Best Practices

### Implementation

1. **Clear naming**: Use descriptive names for methods and variables
2. **Comprehensive validation**: Validate all inputs and state
3. **Error handling**: Provide clear error messages
4. **Documentation**: Document all public methods and complex logic
5. **Type safety**: Use proper type hints throughout

### Code Quality

1. **Single responsibility**: Each method should do one thing well
2. **Immutability**: Prefer immutable data structures where possible
3. **Defensive programming**: Check preconditions and handle edge cases
4. **Consistent patterns**: Follow established patterns from existing cards

### Testing

1. **TDD approach**: Write tests first, then implement
2. **Comprehensive coverage**: Test all code paths and outcomes
3. **Edge cases**: Test error conditions and boundary cases
4. **Integration tests**: Test system interactions

This guide provides everything you need to implement agenda cards in the TI4 framework. The framework is designed to be extensible and maintainable, making it easy to add new agenda cards while maintaining consistency and reliability.

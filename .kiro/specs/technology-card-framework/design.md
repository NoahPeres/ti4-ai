# Design Document

## Overview

The Technology Card Framework provides a comprehensive, extensible system for implementing all TI4 technology cards. The framework establishes clear patterns for concrete technology implementations, seamless integration with existing game systems (abilities, unit stats, exhaustion mechanics), and a protocol that ensures consistency across all technology implementations.

Based on analysis of the TI4 ability compendium, technology cards exhibit several key patterns:
- **Timing-based abilities**: ACTION, "After you activate", "When you research", etc.
- **Exhaustible abilities**: Cards that can be exhausted for one-time effects
- **Passive abilities**: Continuous effects that don't require exhaustion
- **Unit upgrades**: Technologies that modify unit statistics
- **Prerequisite systems**: Color-based prerequisites for research
- **Faction restrictions**: Some technologies are faction-specific

## Architecture

### Enum-First Design Philosophy

Following your excellent suggestion, the framework adopts an enum-first approach for all game concepts to provide:
- **Type Safety**: Compile-time checking of all game references
- **Discoverability**: IDE autocomplete for all game elements
- **Centralized Registry**: Single source of truth for all game data
- **Clear Mapping**: Direct mapping from specifications to game behavior

```python
# Comprehensive enum system
class Expansion(Enum):
    BASE = "base"
    PROPHECY_OF_KINGS = "prophecy_of_kings"
    CODEX_I = "codex_i"
    CODEX_II = "codex_ii"
    CODEX_III = "codex_iii"

class AbilityTrigger(Enum):
    ACTION = "action"
    AFTER_ACTIVATE_SYSTEM = "after_activate_system"
    AFTER_TACTICAL_ACTION = "after_tactical_action"
    WHEN_RESEARCH_TECHNOLOGY = "when_research_technology"
    START_OF_TURN = "start_of_turn"
    END_OF_TURN = "end_of_turn"
    # ... all triggers from compendium analysis

class AbilityEffectType(Enum):
    EXPLORE_FRONTIER_TOKEN = "explore_frontier_token"
    ALLOW_RETREAT_TO_EMPTY_ADJACENT = "allow_retreat_to_empty_adjacent"
    MODIFY_UNIT_STATS = "modify_unit_stats"
    GAIN_TRADE_GOODS = "gain_trade_goods"
    # ... all effect types from compendium analysis

class AbilityCondition(Enum):
    HAS_SHIPS_IN_SYSTEM = "has_ships_in_system"
    CONTROL_PLANET = "control_planet"
    SYSTEM_CONTAINS_FRONTIER = "system_contains_frontier"
    # ... all conditions from compendium analysis
```

### Core Components

```
src/ti4/
├── core/
│   ├── technology.py              # Existing abstract system
│   └── technology_cards/          # NEW: Concrete implementations
│       ├── __init__.py
│       ├── base/                  # Base technology classes
│       │   ├── __init__.py
│       │   ├── technology_card.py # Abstract base for all tech cards
│       │   ├── exhaustible_tech.py # Base for exhaustible technologies
│       │   ├── passive_tech.py    # Base for passive technologies
│       │   └── unit_upgrade_tech.py # Base for unit upgrade technologies
│       ├── concrete/              # Concrete technology implementations
│       │   ├── __init__.py
│       │   ├── dark_energy_tap.py # First implementation
│       │   └── gravity_drive.py   # Refactored existing implementation
│       └── registry.py            # Technology card registry
```

### Integration Points

The framework integrates with existing systems through well-defined interfaces:

1. **Abilities System Integration** (`src/ti4/core/abilities.py`)
   - Technology cards register abilities with the AbilityManager
   - Timing windows (ACTION, AFTER, WHEN) map to TimingWindow enum
   - Ability costs integrate with AbilityCostManager

2. **Unit Stats Integration** (`src/ti4/core/unit_stats.py`)
   - Unit upgrade technologies register modifications with UnitStatsProvider
   - Technology effects on unit stats are applied automatically

3. **Exhaustion Integration** (`src/ti4/core/technology.py`)
   - Exhaustible technologies use existing TechnologyCard exhaustion mechanics
   - Ready/exhaust state tracking is handled by the base system

4. **Game State Integration**
   - Technology ownership tracked by TechnologyManager
   - Prerequisites validated through existing color system
   - Faction restrictions enforced through existing faction technology system

## Components and Interfaces

### Base Technology Card Interface

```python
from typing import Protocol, Optional, List, Dict, Any
from ti4.core.abilities import Ability, AbilityManager
from ti4.core.constants import Technology, TechnologyColor, UnitType, Faction

class TechnologyCardProtocol(Protocol):
    """Protocol that all technology cards must implement"""

    @property
    def technology_enum(self) -> Technology:
        """The Technology enum value for this card"""
        ...

    @property
    def name(self) -> str:
        """Display name of the technology"""
        ...

    @property
    def color(self) -> Optional[TechnologyColor]:
        """Technology color (None for unit upgrades)"""
        ...

    @property
    def prerequisites(self) -> List[TechnologyColor]:
        """Required prerequisite colors"""
        ...

    @property
    def faction_restriction(self) -> Optional[Faction]:
        """Faction restriction (None if available to all)"""
        ...

    def get_abilities(self) -> List[Ability]:
        """Get all abilities provided by this technology"""
        ...

    def register_with_systems(self, ability_manager: AbilityManager,
                            unit_stats_provider: Any) -> None:
        """Register this technology with game systems"""
        ...
```

### Exhaustible Technology Base

```python
from typing import Protocol, Optional

class ExhaustibleTechnologyProtocol(Protocol):
    """Protocol for technologies that can be exhausted"""

    def is_exhausted(self) -> bool:
        """Check if this technology is exhausted"""
        ...

    def exhaust(self) -> None:
        """Exhaust this technology"""
        ...

    def ready(self) -> None:
        """Ready this technology"""
        ...

    def get_action_ability(self) -> Optional[Ability]:
        """Get the ACTION ability that exhausts this card"""
        ...

class ExhaustibleTechnologyCard:
    """Base implementation for exhaustible technologies"""

    def __init__(self):
        self._exhausted = False

    def is_exhausted(self) -> bool:
        return self._exhausted

    def exhaust(self) -> None:
        if self._exhausted:
            raise ValueError("Technology is already exhausted")
        self._exhausted = True

    def ready(self) -> None:
        self._exhausted = False
```

### Unit Upgrade Technology Base

```python
from typing import Protocol, Optional, Dict, Any

class UnitUpgradeTechnologyProtocol(Protocol):
    """Protocol for unit upgrade technologies"""

    @property
    def upgraded_unit_type(self) -> UnitType:
        """The unit type this technology upgrades"""
        ...

    def get_unit_stat_modifications(self) -> Dict[str, Any]:
        """Get the stat modifications this upgrade provides"""
        ...

class UnitUpgradeTechnologyCard:
    """Base implementation for unit upgrade technologies"""

    @property
    def color(self) -> Optional[TechnologyColor]:
        # Unit upgrades have no color
        return None
```

### Technology Registry

```python
class TechnologyCardRegistry:
    """Registry for all concrete technology card implementations"""

    def __init__(self):
        self._cards: Dict[Technology, TechnologyCardProtocol] = {}

    def register_card(self, card: TechnologyCardProtocol) -> None:
        """Register a technology card implementation"""
        self._cards[card.technology_enum] = card

    def get_card(self, technology: Technology) -> Optional[TechnologyCardProtocol]:
        """Get a technology card implementation"""
        return self._cards.get(technology)

    def get_all_cards(self) -> List[TechnologyCardProtocol]:
        """Get all registered technology cards"""
        return list(self._cards.values())
```

## Data Models

### Dark Energy Tap Specification

Based on user confirmation and TI4 ability compendium analysis:

```python
# Dark Energy Tap Technology Specification - CONFIRMED BY USER
{
    "name": "Dark Energy Tap",
    "technology_enum": Technology.DARK_ENERGY_TAP,
    "color": TechnologyColor.BLUE,  # CONFIRMED: Blue technology
    "prerequisites": [],  # CONFIRMED: No prerequisites (Level 0 technology)
    "faction_restriction": None,  # Available to all factions
    "expansion": "Prophecy of Kings",
    "abilities": [
        {
            "name": "Frontier Exploration",
            "timing": TimingWindow.AFTER,
            "trigger": "tactical_action_in_frontier_system",
            "effect": {
                "type": "explore_frontier_token",
                "conditions": ["has_ships_in_system"]
            },
            "mandatory": True
        },
        {
            "name": "Enhanced Retreat",
            "timing": TimingWindow.WHEN,
            "trigger": "retreat_declared",
            "effect": {
                "type": "allow_retreat_to_empty_adjacent"
            },
            "passive": True
        }
    ]
}
```

### Technology Attribute Categories

From compendium analysis, technologies require support for:

1. **Basic Attributes** (All Enum-Based)
   - Name, color (TechnologyColor), prerequisites (List[TechnologyColor])
   - Faction restrictions (Optional[Faction])
   - Expansion source (Expansion enum)

2. **Ability Patterns** (All Enum-Based)
   - ACTION abilities (AbilityTrigger.ACTION)
   - Triggered abilities (AbilityTrigger.AFTER_*, WHEN_*, BEFORE_*)
   - Passive abilities (continuous effects with no trigger)
   - Conditional abilities (AbilityCondition enums for IF/THEN logic)

3. **Cost Patterns** (Enum-Based)
   - Resource costs, trade good costs (AbilityCostType enum)
   - Command token costs, influence costs
   - Multi-resource costs (List[AbilityCost])

4. **Timing Patterns** (Enum-Based)
   - Phase-specific (GamePhase enum integration)
   - Event-specific (AbilityTrigger enum)
   - Turn-specific (TurnTiming enum)

5. **Unit Upgrade Patterns** (Enum-Based)
   - Stat modifications (UnitStatModification enum)
   - Ability additions (UnitAbility enum for SUSTAIN_DAMAGE, BOMBARDMENT, etc.)
   - Special unit abilities (UnitSpecialAbility enum)

### Enum Registry System

```python
class TechnologySpecificationRegistry:
    """Centralized registry mapping enums to game behavior"""

    # Technology specifications using only enums
    SPECIFICATIONS = {
        Technology.DARK_ENERGY_TAP: TechnologySpecification(
            name="Dark Energy Tap",
            color=TechnologyColor.BLUE,
            prerequisites=[],  # No prerequisites
            faction_restriction=None,
            expansion=Expansion.PROPHECY_OF_KINGS,
            abilities=[
                AbilitySpecification(
                    trigger=AbilityTrigger.AFTER_TACTICAL_ACTION,
                    effect=AbilityEffectType.EXPLORE_FRONTIER_TOKEN,
                    conditions=[AbilityCondition.HAS_SHIPS_IN_SYSTEM,
                               AbilityCondition.SYSTEM_CONTAINS_FRONTIER],
                    mandatory=True
                ),
                AbilitySpecification(
                    trigger=AbilityTrigger.WHEN_RETREAT_DECLARED,
                    effect=AbilityEffectType.ALLOW_RETREAT_TO_EMPTY_ADJACENT,
                    passive=True
                )
            ]
        )
    }
```

## Error Handling

### Manual Confirmation Protocol

The framework enforces the manual confirmation protocol for all technology specifications:

```python
class TechnologySpecificationError(Exception):
    """Raised when technology specifications are not confirmed"""
    pass

def require_confirmation(technology: Technology, attribute: str) -> None:
    """Enforce manual confirmation for technology attributes"""
    confirmed_technologies = get_confirmed_technologies()
    if technology not in confirmed_technologies:
        raise TechnologySpecificationError(
            f"Technology {technology} {attribute} not confirmed. "
            f"Please ask user for specification."
        )
```

### Validation Framework

```python
class TechnologyCardValidator:
    """Validates technology card implementations"""

    def validate_card(self, card: TechnologyCardProtocol) -> List[str]:
        """Validate a technology card implementation"""
        errors = []

        # Validate required attributes
        if not card.name:
            errors.append("Technology name is required")

        # Validate color consistency
        if card.color is None and not isinstance(card, UnitUpgradeTechnologyCard):
            errors.append("Non-unit-upgrade technologies must have a color")

        # Validate abilities
        abilities = card.get_abilities()
        for ability in abilities:
            if not ability.name:
                errors.append("All abilities must have names")

        return errors
```

## Testing Strategy

### Unit Testing Approach

1. **Base Class Testing**
   - Test abstract interfaces and base functionality
   - Test exhaustion mechanics for exhaustible technologies
   - Test unit stat integration for upgrade technologies

2. **Concrete Implementation Testing**
   - Test Dark Energy Tap frontier exploration ability
   - Test Dark Energy Tap retreat enhancement ability
   - Test integration with Rule 35 exploration system

3. **Integration Testing**
   - Test technology card registration with game systems
   - Test ability triggering through AbilityManager
   - Test unit stat modifications through UnitStatsProvider

4. **Validation Testing**
   - Test manual confirmation protocol enforcement
   - Test technology card validation
   - Test error handling for unconfirmed specifications

### Test Structure

```python
class TestTechnologyCardFramework:
    """Test the technology card framework"""

    def test_dark_energy_tap_frontier_exploration(self):
        """Test Dark Energy Tap enables frontier exploration"""
        # Test Rule 35.4 integration
        pass

    def test_technology_card_registration(self):
        """Test technology cards register with game systems"""
        pass

    def test_manual_confirmation_protocol(self):
        """Test manual confirmation is enforced"""
        pass

class TestDarkEnergyTap:
    """Test Dark Energy Tap implementation"""

    def test_frontier_exploration_ability(self):
        """Test frontier exploration ability triggers correctly"""
        pass

    def test_retreat_enhancement_ability(self):
        """Test retreat enhancement works correctly"""
        pass
```

### Mock and Test Data

```python
# Test data for Dark Energy Tap
DARK_ENERGY_TAP_TEST_DATA = {
    "confirmed_specifications": {
        Technology.DARK_ENERGY_TAP: {
            "color": TechnologyColor.BLUE,
            "prerequisites": [TechnologyColor.BLUE],
            "faction_restriction": None
        }
    }
}
```

## Implementation Plan Integration

The framework design supports the implementation plan by:

1. **Clear File Structure**: Organized directory structure makes it easy to find and add technology implementations

2. **Consistent Interfaces**: All technology cards implement the same protocol, ensuring consistency

3. **System Integration**: Clear integration points with existing systems (abilities, unit stats, exhaustion)

4. **Validation Framework**: Built-in validation ensures implementations follow the protocol

5. **Manual Confirmation**: Enforces the manual confirmation protocol to prevent assumptions

6. **Extensibility**: Framework supports all technology patterns found in the compendium

The design provides a solid foundation for implementing Dark Energy Tap as the first concrete example and establishing patterns for all future technology implementations.

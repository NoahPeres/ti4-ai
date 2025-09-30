# Technology Card Framework Developer Guide

## Overview

The Technology Card Framework provides a comprehensive, type-safe system for implementing all TI4 technology cards. This guide covers everything you need to know to implement new technology cards and understand the framework's architecture.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Framework Architecture](#framework-architecture)
3. [Enum System](#enum-system)
4. [Base Classes](#base-classes)
5. [Implementing Technology Cards](#implementing-technology-cards)
6. [Integration Points](#integration-points)
7. [Manual Confirmation Protocol](#manual-confirmation-protocol)
8. [Testing Guidelines](#testing-guidelines)
9. [Examples](#examples)
10. [Troubleshooting](#troubleshooting)

## Quick Start

To implement a new technology card:

1. **Add the technology to the enum system** in `src/ti4/core/constants.py`
2. **Get user confirmation** for all specifications (mandatory)
3. **Add specification** to `TechnologySpecificationRegistry`
4. **Create concrete implementation** in `src/ti4/core/technology_cards/concrete/`
5. **Register with systems** using the registry
6. **Write comprehensive tests**

## Framework Architecture

The framework follows an enum-first design philosophy with clear separation of concerns:

```
src/ti4/core/technology_cards/
├── __init__.py                 # Public API exports
├── protocols.py                # Protocol definitions
├── specifications.py           # Enum-based specifications
├── registry.py                 # Technology card registry
├── confirmation.py             # Manual confirmation protocol
├── exceptions.py               # Framework exceptions
├── abilities_integration.py    # Abilities system integration
├── unit_stats_integration.py   # Unit stats system integration
├── base/                       # Base implementations
│   ├── technology_card.py      # Abstract base class
│   ├── exhaustible_tech.py     # Exhaustible technologies
│   ├── passive_tech.py         # Passive technologies
│   └── unit_upgrade_tech.py    # Unit upgrade technologies
└── concrete/                   # Concrete implementations
    ├── dark_energy_tap.py      # Reference implementation
    └── gravity_drive.py        # Refactored implementation
```

### Design Principles

1. **Enum-First**: All game concepts are represented as enums for type safety
2. **Protocol-Based**: Clear interfaces ensure consistency across implementations
3. **Manual Confirmation**: All specifications must be user-confirmed
4. **System Integration**: Seamless integration with existing game systems
5. **Test-Driven**: Comprehensive testing ensures reliability

## Enum System

The framework uses comprehensive enums to represent all game concepts:

### Core Technology Enums

```python
# In src/ti4/core/constants.py

class Technology(Enum):
    """All TI4 technologies"""
    DARK_ENERGY_TAP = "dark_energy_tap"
    GRAVITY_DRIVE = "gravity_drive"
    # ... add new technologies here

class Expansion(Enum):
    """TI4 expansions"""
    BASE = "base"
    PROPHECY_OF_KINGS = "prophecy_of_kings"
    CODEX_I = "codex_i"
    # ... etc

class AbilityTrigger(Enum):
    """When abilities trigger"""
    ACTION = "action"
    AFTER_TACTICAL_ACTION = "after_tactical_action"
    WHEN_RETREAT_DECLARED = "when_retreat_declared"
    # ... all timing patterns

class AbilityEffectType(Enum):
    """What abilities do"""
    EXPLORE_FRONTIER_TOKEN = "explore_frontier_token"
    MODIFY_UNIT_STATS = "modify_unit_stats"
    GAIN_TRADE_GOODS = "gain_trade_goods"
    # ... all effect types

class AbilityCondition(Enum):
    """Conditions for abilities"""
    HAS_SHIPS_IN_SYSTEM = "has_ships_in_system"
    SYSTEM_CONTAINS_FRONTIER = "system_contains_frontier"
    # ... all conditions
```

### Benefits of Enum System

- **Type Safety**: IDE autocomplete and compile-time checking
- **Discoverability**: Easy to find all available options
- **Centralized**: Single source of truth for all game data
- **Validation**: Automatic validation of enum values

## Base Classes

The framework provides several base classes for different technology types:

### BaseTechnologyCard

Abstract base class for all technology cards:

```python
class BaseTechnologyCard:
    """Base class for all technology cards"""

    def __init__(self, technology_enum: Technology, name: str):
        self.technology_enum = technology_enum
        self.name = name

    # Abstract methods that subclasses must implement
    @property
    def color(self) -> Optional[TechnologyColor]: ...
    @property
    def prerequisites(self) -> list[TechnologyColor]: ...
    @property
    def faction_restriction(self) -> Optional[Faction]: ...
    def get_abilities(self) -> list[Ability]: ...
```

### ExhaustibleTechnologyCard

For technologies with abilities that exhaust the card when used (including ACTION abilities, triggered abilities, and others):

```python
class ExhaustibleTechnologyCard(BaseTechnologyCard):
    """Base for technologies that can be exhausted"""

    def is_exhausted(self) -> bool: ...
    def exhaust(self) -> None: ...
    def ready(self) -> None: ...
    def get_exhaustible_abilities(self) -> list[Ability]: ...
    def get_action_ability(self) -> Optional[Ability]: ...
```

**Important**: `ExhaustibleTechnologyCard` supports **any** type of ability that exhausts the card, not just ACTION abilities. This includes:

- **ACTION abilities**: Traditional exhaustible cards activated during the action phase
- **Triggered abilities**: Like AI Development Algorithm's "When you research..." abilities
- **Other timing windows**: WHEN, AFTER, BEFORE, etc.

**Example - AI Development Algorithm** (non-ACTION exhaustible abilities):

```python
class AIDevelopmentAlgorithm(ExhaustibleTechnologyCard):
    def get_exhaustible_abilities(self) -> list[Ability]:
        return [
            # WHEN ability (not ACTION) that exhausts the card
            Ability(
                name="Research Enhancement",
                timing=TimingWindow.WHEN,
                trigger="research_unit_upgrade_technology",
                effect=AbilityEffect(type="ignore_prerequisite", value=1),
                mandatory=False
            ),
            # Another WHEN ability that exhausts the card
            Ability(
                name="Production Cost Reduction",
                timing=TimingWindow.WHEN,
                trigger="units_use_production",
                effect=AbilityEffect(type="reduce_production_cost", value="unit_upgrade_count"),
                mandatory=False
            )
        ]
```

### PassiveTechnologyCard

For technologies with passive abilities:

```python
class PassiveTechnologyCard(BaseTechnologyCard):
    """Base for technologies with passive abilities"""

    # Provides default implementations for passive technologies
```

### UnitUpgradeTechnologyCard

For unit upgrade technologies:

```python
class UnitUpgradeTechnologyCard(BaseTechnologyCard):
    """Base for unit upgrade technologies"""

    @property
    def upgraded_unit_type(self) -> UnitType: ...
    def get_unit_stat_modifications(self) -> dict[str, Any]: ...
```

## Implementing Technology Cards

### Step 1: Add Technology Enum

First, add your technology to the `Technology` enum in `constants.py`:

```python
class Technology(Enum):
    # Existing technologies...
    YOUR_NEW_TECH = "your_new_tech"
```

### Step 2: Get User Confirmation (MANDATORY)

**CRITICAL**: You must get user confirmation for all specifications before implementing:

```python
# NEVER assume specifications - always ask the user:
# "I need to implement [Technology Name]. Before proceeding, I need confirmation:
# - What color is this technology?
# - What are its prerequisites?
# - What abilities does it have?
# - Is it faction-specific?"
```

### Step 3: Add Specification

Add the confirmed specification to `TechnologySpecificationRegistry`:

```python
# In specifications.py
self._specifications[Technology.YOUR_NEW_TECH] = TechnologySpecification(
    technology=Technology.YOUR_NEW_TECH,
    name="Your New Tech",
    color=TechnologyColor.BLUE,  # CONFIRMED by user
    prerequisites=[TechnologyColor.BLUE],  # CONFIRMED by user
    faction_restriction=None,  # CONFIRMED by user
    expansion=Expansion.BASE,  # CONFIRMED by user
    abilities=[
        AbilitySpecification(
            trigger=AbilityTrigger.ACTION,  # CONFIRMED by user
            effect=AbilityEffectType.GAIN_TRADE_GOODS,  # CONFIRMED by user
            conditions=[],  # CONFIRMED by user
            mandatory=True,  # CONFIRMED by user
            passive=False,  # CONFIRMED by user
        ),
    ],
)
```

### Step 4: Create Concrete Implementation

Create your implementation in `src/ti4/core/technology_cards/concrete/`:

```python
# your_new_tech.py
"""
Your New Tech technology implementation.

CONFIRMED SPECIFICATIONS - DO NOT MODIFY WITHOUT USER APPROVAL:
- Color: Blue technology
- Prerequisites: 1 Blue
- Abilities: ACTION - Gain 2 trade goods
"""

from typing import Optional
from ti4.core.constants import Faction, Technology
from ti4.core.technology import TechnologyColor
from ti4.core.technology_cards.base.exhaustible_tech import ExhaustibleTechnologyCard

class YourNewTech(ExhaustibleTechnologyCard):
    """Your New Tech implementation."""

    def __init__(self) -> None:
        super().__init__(Technology.YOUR_NEW_TECH, "Your New Tech")

    @property
    def color(self) -> Optional[TechnologyColor]:
        return TechnologyColor.BLUE

    @property
    def prerequisites(self) -> list[TechnologyColor]:
        return [TechnologyColor.BLUE]

    @property
    def faction_restriction(self) -> Optional[Faction]:
        return None

    def get_abilities(self) -> list[Ability]:
        return [self._create_action_ability()]

    def _create_action_ability(self) -> Ability:
        # Implementation details...
        pass
```

### Step 5: Write Tests

Create comprehensive tests for your implementation:

```python
# test_your_new_tech.py
class TestYourNewTech:
    def test_basic_properties(self):
        tech = YourNewTech()
        assert tech.technology_enum == Technology.YOUR_NEW_TECH
        assert tech.name == "Your New Tech"
        assert tech.color == TechnologyColor.BLUE
        assert tech.prerequisites == [TechnologyColor.BLUE]
        assert tech.faction_restriction is None

    def test_abilities(self):
        tech = YourNewTech()
        abilities = tech.get_abilities()
        assert len(abilities) == 1
        # Test ability details...

    def test_exhaustion_mechanics(self):
        tech = YourNewTech()
        assert not tech.is_exhausted()
        tech.exhaust()
        assert tech.is_exhausted()
        tech.ready()
        assert not tech.is_exhausted()
```

## Integration Points

The framework integrates with several existing systems:

### Abilities System Integration

Technology abilities are automatically registered with the `AbilityManager`:

```python
# abilities_integration.py provides mapping functions
def map_trigger_to_timing(trigger: AbilityTrigger) -> TimingWindow:
    """Maps AbilityTrigger enums to TimingWindow enums"""

def create_ability_from_specification(spec: AbilitySpecification) -> Ability:
    """Creates Ability objects from specifications"""
```

### Unit Stats Integration

Unit upgrade technologies integrate with the `UnitStatsProvider`:

```python
# unit_stats_integration.py
class UnitStatsIntegration:
    def register_technology_modifications(self, tech: UnitUpgradeTechnologyCard):
        """Registers unit stat modifications from technology"""
```

### Exploration System Integration

Technologies like Dark Energy Tap integrate with Rule 35 exploration:

```python
# In exploration.py
def can_explore_frontier_token(self, player, system):
    """Check if player can explore frontier token (includes tech check)"""
    if player.has_technology(Technology.DARK_ENERGY_TAP):
        return True  # Dark Energy Tap enables frontier exploration
```

## Manual Confirmation Protocol

**CRITICAL**: The framework enforces manual confirmation for all technology specifications.

### Why Manual Confirmation?

- Prevents incorrect assumptions about game rules
- Ensures accuracy of implementations
- Maintains consistency across the codebase
- Provides clear audit trail of confirmed specifications

### How It Works

```python
# confirmation.py
def require_confirmation(technology: Technology, attribute: str) -> None:
    """Enforce manual confirmation for technology attributes"""
    confirmed_technologies = get_confirmed_technologies()
    if technology not in confirmed_technologies:
        raise TechnologySpecificationError(
            f"Technology {technology} {attribute} not confirmed. "
            f"Please ask user for specification."
        )
```

### Confirmed Technologies

Currently confirmed technologies:
- **Dark Energy Tap**: Blue, no prerequisites, Prophecy of Kings
- **Gravity Drive**: Blue, 1 Blue prerequisite, Base game

### Adding New Confirmations

To add a new confirmed technology:

1. Get explicit user confirmation for all attributes
2. Add to `CONFIRMED_TECHNOLOGIES` in `confirmation.py`
3. Document the confirmation in code comments
4. Add specification to `TechnologySpecificationRegistry`

## Testing Guidelines

### Test Structure

Follow this structure for technology card tests:

```python
class TestTechnologyName:
    """Test [Technology Name] implementation"""

    def test_basic_properties(self):
        """Test basic technology properties"""

    def test_abilities(self):
        """Test technology abilities"""

    def test_system_integration(self):
        """Test integration with game systems"""

    def test_edge_cases(self):
        """Test edge cases and error conditions"""
```

### Test Coverage Requirements

- **Basic Properties**: Name, color, prerequisites, faction restriction
- **Abilities**: All abilities and their effects
- **System Integration**: Integration with abilities, unit stats, etc.
- **Edge Cases**: Error conditions, invalid states
- **Manual Confirmation**: Confirmation protocol enforcement

### Test Utilities

The framework provides test utilities:

```python
# In test files
from ti4.core.technology_cards.concrete.dark_energy_tap import DarkEnergyTap

def test_dark_energy_tap_reference():
    """Use Dark Energy Tap as reference for testing patterns"""
    tech = DarkEnergyTap()
    # Test implementation patterns...
```

## Examples

### Dark Energy Tap (Reference Implementation)

Dark Energy Tap serves as the reference implementation showing all framework capabilities:

```python
class DarkEnergyTap(PassiveTechnologyCard):
    """
    Dark Energy Tap technology implementation.

    CONFIRMED SPECIFICATIONS:
    - Color: Blue technology
    - Prerequisites: None (Level 0 technology)
    - Expansion: Prophecy of Kings
    - Abilities: Frontier exploration + retreat enhancement
    """

    def __init__(self) -> None:
        super().__init__(Technology.DARK_ENERGY_TAP, "Dark Energy Tap")

    @property
    def color(self) -> Optional[TechnologyColor]:
        return TechnologyColor.BLUE

    @property
    def prerequisites(self) -> list[TechnologyColor]:
        return []  # No prerequisites

    @property
    def faction_restriction(self) -> Optional[Faction]:
        return None  # Available to all factions

    def get_abilities(self) -> list[Ability]:
        return [
            self._create_frontier_exploration_ability(),
            self._create_retreat_enhancement_ability(),
        ]
```

Key features demonstrated:
- **Passive Technology**: Uses `PassiveTechnologyCard` base
- **Multiple Abilities**: Two different abilities with different triggers
- **System Integration**: Integrates with exploration and combat systems
- **Enum Usage**: Uses all enum types for type safety
- **Documentation**: Clear documentation of confirmed specifications

### Gravity Drive (Refactored Implementation)

Gravity Drive shows how existing technologies are refactored to the new framework:

```python
class GravityDrive(PassiveTechnologyCard):
    """
    Gravity Drive technology implementation.

    CONFIRMED SPECIFICATIONS:
    - Color: Blue technology
    - Prerequisites: 1 Blue
    - Abilities: Movement enhancement after system activation
    """

    # Similar structure to Dark Energy Tap but with different abilities
```

## Troubleshooting

### Common Issues

#### 1. TechnologySpecificationError

**Problem**: Getting `TechnologySpecificationError` when accessing technology
**Solution**: Technology needs user confirmation - ask user for specifications

#### 2. Missing Enum Values

**Problem**: Need to add new trigger/effect/condition types
**Solution**: Add to appropriate enum in `constants.py`

#### 3. Integration Issues

**Problem**: Technology not working with game systems
**Solution**: Check integration points in `abilities_integration.py` and `unit_stats_integration.py`

#### 4. Test Failures

**Problem**: Tests failing after implementation
**Solution**: Follow TDD practices - write tests first, then implement

### Debugging Tips

1. **Check Confirmations**: Ensure technology is in `CONFIRMED_TECHNOLOGIES`
2. **Verify Enums**: Make sure all enum values are defined
3. **Test Integration**: Test each integration point separately
4. **Use Reference**: Compare with Dark Energy Tap implementation

### Getting Help

1. **Check Examples**: Look at Dark Energy Tap and Gravity Drive
2. **Read Tests**: Test files show expected behavior
3. **Check Integration**: Look at integration modules for system connections
4. **Ask for Confirmation**: When in doubt, ask user for specifications

## Best Practices

### Implementation

1. **Always get user confirmation** before implementing
2. **Use enum types** for all game concepts
3. **Follow naming conventions** from existing implementations
4. **Write comprehensive tests** before implementing
5. **Document confirmed specifications** in code comments

### Code Quality

1. **Type hints**: Use proper type hints for all methods
2. **Docstrings**: Document all public methods and classes
3. **Error handling**: Handle edge cases and invalid inputs
4. **Validation**: Validate inputs and state transitions

### Testing

1. **TDD approach**: Write tests first, then implement
2. **Comprehensive coverage**: Test all code paths
3. **Edge cases**: Test error conditions and boundary cases
4. **Integration tests**: Test system interactions

This guide provides everything you need to implement technology cards in the TI4 framework. Remember: when in doubt, ask for user confirmation rather than making assumptions!

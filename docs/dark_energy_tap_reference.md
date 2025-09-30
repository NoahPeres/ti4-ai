# Dark Energy Tap Reference Implementation

## Overview

Dark Energy Tap serves as the reference implementation for the Technology Card Framework, demonstrating all framework capabilities and best practices. This document provides a comprehensive walkthrough of the implementation.

## Technology Overview

**Dark Energy Tap** is a blue technology from Prophecy of Kings that provides two abilities:
1. **Frontier Exploration**: After tactical action in frontier system, explore frontier token
2. **Retreat Enhancement**: When retreat declared, allow retreat to empty adjacent systems

### Confirmed Specifications

```
CONFIRMED SPECIFICATIONS - DO NOT MODIFY WITHOUT USER APPROVAL:
- Color: Blue technology
- Prerequisites: None (Level 0 technology)
- Expansion: Prophecy of Kings
- Available to all factions
- Abilities: Frontier exploration + retreat enhancement
```

## Implementation Structure

### File Organization

```
src/ti4/core/technology_cards/concrete/dark_energy_tap.py
tests/test_dark_energy_tap.py
tests/test_dark_energy_tap_abilities_integration.py
```

### Class Hierarchy

```
BaseTechnologyCard
└── PassiveTechnologyCard
    └── DarkEnergyTap
```

Dark Energy Tap uses `PassiveTechnologyCard` because its abilities are passive (don't require exhaustion).

## Complete Implementation

### Core Implementation

```python
"""
Dark Energy Tap technology implementation.

This module implements the Dark Energy Tap technology card from Prophecy of Kings,
which enables frontier exploration and enhanced retreat capabilities.

CONFIRMED SPECIFICATIONS - DO NOT MODIFY WITHOUT USER APPROVAL:
- Color: Blue technology
- Prerequisites: None (Level 0 technology)
- Expansion: Prophecy of Kings
- Available to all factions
"""

from typing import Optional

from ti4.core.abilities import Ability, AbilityEffect, TimingWindow
from ti4.core.constants import Faction, Technology
from ti4.core.technology import TechnologyColor
from ti4.core.technology_cards.base.passive_tech import PassiveTechnologyCard


class DarkEnergyTap(PassiveTechnologyCard):
    """
    Dark Energy Tap technology implementation.

    This technology provides two abilities:
    1. Frontier Exploration: After tactical action in frontier system, explore frontier token
    2. Retreat Enhancement: When retreat declared, allow retreat to empty adjacent systems

    LRR References:
    - Rule 35.4: Frontier exploration mechanics
    - Retreat rules for enhanced retreat capabilities
    """

    def __init__(self) -> None:
        """Initialize Dark Energy Tap technology."""
        super().__init__(Technology.DARK_ENERGY_TAP, "Dark Energy Tap")

    @property
    def color(self) -> Optional[TechnologyColor]:
        """Technology color (Blue)."""
        return TechnologyColor.BLUE

    @property
    def prerequisites(self) -> list[TechnologyColor]:
        """Required prerequisite colors (none)."""
        return []

    @property
    def faction_restriction(self) -> Optional[Faction]:
        """Faction restriction (available to all)."""
        return None

    def get_abilities(self) -> list[Ability]:
        """Get all abilities provided by Dark Energy Tap."""
        return [
            self._create_frontier_exploration_ability(),
            self._create_retreat_enhancement_ability(),
        ]

    def _create_frontier_exploration_ability(self) -> Ability:
        """Create the frontier exploration ability."""
        from ti4.core.constants import AbilityCondition
        from ti4.core.technology_cards.abilities_integration import EnhancedAbility

        ability = EnhancedAbility(
            name="Frontier Exploration",
            timing=TimingWindow.AFTER,
            trigger="tactical_action_in_frontier_system",
            effect=AbilityEffect(
                type="explore_frontier_token",
                value=True,
                conditions=[
                    {"type": "has_ships_in_system", "value": True},
                    {"type": "system_contains_frontier", "value": True},
                ]
            ),
            mandatory=True,
            conditions=[
                AbilityCondition.HAS_SHIPS_IN_SYSTEM,
                AbilityCondition.SYSTEM_CONTAINS_FRONTIER,
            ]
        )
        # Add source identifier for tracking
        ability.source = "Dark Energy Tap"
        return ability

    def _create_retreat_enhancement_ability(self) -> Ability:
        """Create the retreat enhancement ability."""
        from ti4.core.technology_cards.abilities_integration import EnhancedAbility

        ability = EnhancedAbility(
            name="Enhanced Retreat",
            timing=TimingWindow.WHEN,
            trigger="retreat_declared",
            effect=AbilityEffect(
                type="allow_retreat_to_empty_adjacent",
                value=True,
            ),
            mandatory=False,
            conditions=[]  # No conditions for retreat enhancement
        )
        # Add source identifier for tracking
        ability.source = "Dark Energy Tap"
        return ability
```

## Key Implementation Patterns

### 1. Base Class Selection

```python
class DarkEnergyTap(PassiveTechnologyCard):
```

**Why PassiveTechnologyCard?**
- Dark Energy Tap has no ACTION abilities that exhaust the card
- Both abilities are passive/triggered abilities
- No exhaustion mechanics needed

**Alternative base classes:**
- `ExhaustibleTechnologyCard`: For ACTION abilities that exhaust
- `UnitUpgradeTechnologyCard`: For unit upgrades

### 2. Property Implementation

```python
@property
def color(self) -> Optional[TechnologyColor]:
    """Technology color (Blue)."""
    return TechnologyColor.BLUE

@property
def prerequisites(self) -> list[TechnologyColor]:
    """Required prerequisite colors (none)."""
    return []  # Level 0 technology - no prerequisites

@property
def faction_restriction(self) -> Optional[Faction]:
    """Faction restriction (available to all)."""
    return None  # Available to all factions
```

**Key patterns:**
- **Type hints**: All properties have proper type hints
- **Docstrings**: Clear documentation of what each property returns
- **Enum usage**: Uses `TechnologyColor` and `Faction` enums
- **Confirmed values**: All values are user-confirmed

### 3. Ability Creation

```python
def get_abilities(self) -> list[Ability]:
    """Get all abilities provided by Dark Energy Tap."""
    return [
        self._create_frontier_exploration_ability(),
        self._create_retreat_enhancement_ability(),
    ]
```

**Pattern benefits:**
- **Separation of concerns**: Each ability has its own creation method
- **Maintainability**: Easy to modify individual abilities
- **Testability**: Can test each ability creation separately
- **Readability**: Clear structure showing all abilities

### 4. Enhanced Ability Usage

```python
def _create_frontier_exploration_ability(self) -> Ability:
    """Create the frontier exploration ability."""
    from ti4.core.constants import AbilityCondition
    from ti4.core.technology_cards.abilities_integration import EnhancedAbility

    ability = EnhancedAbility(
        name="Frontier Exploration",
        timing=TimingWindow.AFTER,
        trigger="tactical_action_in_frontier_system",
        effect=AbilityEffect(
            type="explore_frontier_token",
            value=True,
            conditions=[
                {"type": "has_ships_in_system", "value": True},
                {"type": "system_contains_frontier", "value": True},
            ]
        ),
        mandatory=True,
        conditions=[
            AbilityCondition.HAS_SHIPS_IN_SYSTEM,
            AbilityCondition.SYSTEM_CONTAINS_FRONTIER,
        ]
    )
    # Add source identifier for tracking
    ability.source = "Dark Energy Tap"
    return ability
```

**Key features:**
- **EnhancedAbility**: Uses framework's enhanced ability class
- **Enum conditions**: Uses `AbilityCondition` enums for type safety
- **Source tracking**: Adds source identifier for debugging
- **Condition validation**: Both effect conditions and enum conditions

## Specification Integration

### Registry Entry

```python
# In specifications.py
self._specifications[Technology.DARK_ENERGY_TAP] = TechnologySpecification(
    technology=Technology.DARK_ENERGY_TAP,
    name="Dark Energy Tap",
    color=TechnologyColor.BLUE,
    prerequisites=[],  # CONFIRMED: No prerequisites
    faction_restriction=None,
    expansion=Expansion.PROPHECY_OF_KINGS,
    abilities=[
        AbilitySpecification(
            trigger=AbilityTrigger.AFTER_TACTICAL_ACTION,
            effect=AbilityEffectType.EXPLORE_FRONTIER_TOKEN,
            conditions=[
                AbilityCondition.HAS_SHIPS_IN_SYSTEM,
                AbilityCondition.SYSTEM_CONTAINS_FRONTIER,
            ],
            mandatory=True,
            passive=False,
        ),
        AbilitySpecification(
            trigger=AbilityTrigger.WHEN_RETREAT_DECLARED,
            effect=AbilityEffectType.ALLOW_RETREAT_TO_EMPTY_ADJACENT,
            conditions=[],
            mandatory=False,
            passive=True,
        ),
    ],
)
```

**Specification features:**
- **Enum-based**: All values use appropriate enums
- **User-confirmed**: All specifications confirmed by user
- **Complete**: Covers all aspects of the technology
- **Validated**: Passes all validation checks

## System Integration Examples

### 1. Exploration System Integration

```python
# In exploration.py
def can_explore_frontier_token(self, player, system):
    """Check if player can explore frontier token."""
    # Standard Rule 35.4 check
    if not system.has_frontier_token():
        return False

    # Dark Energy Tap integration
    if player.has_technology(Technology.DARK_ENERGY_TAP):
        if player.has_ships_in_system(system):
            return True  # Dark Energy Tap enables exploration

    return False
```

### 2. Abilities System Integration

```python
# Abilities are automatically registered through the framework
ability_manager = AbilityManager()
dark_energy_tap = DarkEnergyTap()

# Register abilities
for ability in dark_energy_tap.get_abilities():
    ability_manager.register_ability(ability)

# Abilities can now trigger through the standard system
```

### 3. Manual Confirmation Integration

```python
# Confirmation is enforced automatically
from ti4.core.technology_cards.confirmation import require_confirmation

def get_dark_energy_tap_specification():
    # This will pass because Dark Energy Tap is confirmed
    require_confirmation(Technology.DARK_ENERGY_TAP, "specification")
    return registry.get_specification(Technology.DARK_ENERGY_TAP)
```

## Testing Patterns

### Basic Property Tests

```python
class TestDarkEnergyTap:
    """Test Dark Energy Tap implementation."""

    def test_basic_properties(self):
        """Test basic technology properties."""
        tech = DarkEnergyTap()

        assert tech.technology_enum == Technology.DARK_ENERGY_TAP
        assert tech.name == "Dark Energy Tap"
        assert tech.color == TechnologyColor.BLUE
        assert tech.prerequisites == []
        assert tech.faction_restriction is None

    def test_abilities_count(self):
        """Test that Dark Energy Tap has exactly 2 abilities."""
        tech = DarkEnergyTap()
        abilities = tech.get_abilities()

        assert len(abilities) == 2

        # Check ability names
        ability_names = [ability.name for ability in abilities]
        assert "Frontier Exploration" in ability_names
        assert "Enhanced Retreat" in ability_names
```

### Ability-Specific Tests

```python
def test_frontier_exploration_ability(self):
    """Test frontier exploration ability details."""
    tech = DarkEnergyTap()
    abilities = tech.get_abilities()

    frontier_ability = next(
        ability for ability in abilities
        if ability.name == "Frontier Exploration"
    )

    assert frontier_ability.timing == TimingWindow.AFTER
    assert frontier_ability.trigger == "tactical_action_in_frontier_system"
    assert frontier_ability.effect.type == "explore_frontier_token"
    assert frontier_ability.source == "Dark Energy Tap"

def test_retreat_enhancement_ability(self):
    """Test retreat enhancement ability details."""
    tech = DarkEnergyTap()
    abilities = tech.get_abilities()

    retreat_ability = next(
        ability for ability in abilities
        if ability.name == "Enhanced Retreat"
    )

    assert retreat_ability.timing == TimingWindow.WHEN
    assert retreat_ability.trigger == "retreat_declared"
    assert retreat_ability.effect.type == "allow_retreat_to_empty_adjacent"
    assert retreat_ability.source == "Dark Energy Tap"
```

### Integration Tests

```python
def test_exploration_integration(self):
    """Test integration with exploration system."""
    # Test that Dark Energy Tap enables frontier exploration
    player = create_test_player()
    system = create_frontier_system()

    # Without Dark Energy Tap
    assert not can_explore_frontier_token(player, system)

    # With Dark Energy Tap
    player.add_technology(Technology.DARK_ENERGY_TAP)
    player.add_ships_to_system(system, [UnitType.CRUISER])
    assert can_explore_frontier_token(player, system)

def test_abilities_registration(self):
    """Test that abilities register correctly with AbilityManager."""
    ability_manager = AbilityManager()
    tech = DarkEnergyTap()

    # Register abilities
    tech.register_with_systems(ability_manager, None)

    # Check abilities are registered
    registered_abilities = ability_manager.get_abilities_by_source("Dark Energy Tap")
    assert len(registered_abilities) == 2
```

## Common Usage Patterns

### 1. Creating and Using Dark Energy Tap

```python
# Create instance
dark_energy_tap = DarkEnergyTap()

# Check properties
assert dark_energy_tap.color == TechnologyColor.BLUE
assert dark_energy_tap.prerequisites == []

# Get abilities
abilities = dark_energy_tap.get_abilities()
for ability in abilities:
    print(f"Ability: {ability.name}")
    print(f"Timing: {ability.timing}")
    print(f"Effect: {ability.effect.type}")
```

### 2. Registry Integration

```python
# Register with technology card registry
registry = TechnologyCardRegistry()
registry.register_card(DarkEnergyTap())

# Retrieve from registry
tech_card = registry.get_card(Technology.DARK_ENERGY_TAP)
assert isinstance(tech_card, DarkEnergyTap)
```

### 3. Player Integration

```python
# Add to player's technologies
player.add_technology(Technology.DARK_ENERGY_TAP)

# Check if player has technology
if player.has_technology(Technology.DARK_ENERGY_TAP):
    # Player can use Dark Energy Tap abilities
    pass
```

## Lessons Learned

### 1. Base Class Selection Matters

Choosing `PassiveTechnologyCard` was correct because:
- No ACTION abilities that exhaust
- Both abilities are passive/triggered
- Simpler implementation without exhaustion mechanics

### 2. Enum Usage is Critical

Using enums throughout provides:
- Type safety at compile time
- IDE autocomplete support
- Clear validation and error messages
- Centralized data management

### 3. Ability Creation Patterns

Separating ability creation into individual methods:
- Makes code more maintainable
- Enables focused testing
- Improves readability
- Follows single responsibility principle

### 4. Integration Points

Clear integration with existing systems:
- Exploration system for frontier tokens
- Abilities system for ability registration
- Combat system for retreat enhancement
- Manual confirmation for specifications

## Best Practices Demonstrated

### 1. Documentation

- **Confirmed specifications** clearly documented
- **LRR references** for rule connections
- **Comprehensive docstrings** for all methods
- **Type hints** for all parameters and returns

### 2. Error Handling

- **Type validation** in ability creation
- **Source tracking** for debugging
- **Condition validation** for ability triggering
- **Manual confirmation** enforcement

### 3. Testing

- **Comprehensive coverage** of all functionality
- **Integration tests** with other systems
- **Edge case testing** for error conditions
- **Clear test organization** by functionality

### 4. Code Organization

- **Single responsibility** methods
- **Clear naming** conventions
- **Proper imports** and dependencies
- **Consistent patterns** throughout

## Using as a Template

When implementing new technology cards, use Dark Energy Tap as a template:

1. **Copy the file structure** and naming patterns
2. **Follow the same property implementation** patterns
3. **Use the same ability creation** approach
4. **Include the same level of documentation**
5. **Write similar comprehensive tests**

### Template Checklist

- [ ] Confirmed specifications documented
- [ ] Appropriate base class selected
- [ ] All properties implemented with type hints
- [ ] Abilities created using EnhancedAbility
- [ ] Source tracking added to abilities
- [ ] Comprehensive tests written
- [ ] Integration tests included
- [ ] Registry integration tested
- [ ] Manual confirmation enforced

Dark Energy Tap demonstrates all framework capabilities and serves as the gold standard for technology card implementations. Use it as your reference when implementing new technologies!

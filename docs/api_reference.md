# Technology Card Framework API Reference

## Overview

This document provides a comprehensive API reference for the Technology Card Framework, including all classes, methods, and interfaces.

## Table of Contents

1. [Core Protocols](#core-protocols)
2. [Base Classes](#base-classes)
3. [Registry Classes](#registry-classes)
4. [Specification System](#specification-system)
5. [Integration Classes](#integration-classes)
6. [Exception Classes](#exception-classes)
7. [Utility Functions](#utility-functions)
8. [Enum Types](#enum-types)

## Core Protocols

### TechnologyCardProtocol

**File**: `src/ti4/core/technology_cards/protocols.py`

Protocol that all technology cards must implement.

```python
class TechnologyCardProtocol(Protocol):
    """Protocol that all technology cards must implement."""
```

#### Properties

##### technology_enum
```python
@property
def technology_enum(self) -> Technology:
    """The Technology enum value for this card."""
```

**Returns**: `Technology` - The enum value identifying this technology

##### name
```python
@property
def name(self) -> str:
    """Display name of the technology."""
```

**Returns**: `str` - Human-readable name of the technology

##### color
```python
@property
def color(self) -> Optional[TechnologyColor]:
    """Technology color (None for unit upgrades)."""
```

**Returns**: `Optional[TechnologyColor]` - Color of the technology, or None for unit upgrades

##### prerequisites
```python
@property
def prerequisites(self) -> list[TechnologyColor]:
    """Required prerequisite colors."""
```

**Returns**: `list[TechnologyColor]` - List of required prerequisite colors

##### faction_restriction
```python
@property
def faction_restriction(self) -> Optional[Faction]:
    """Faction restriction (None if available to all)."""
```

**Returns**: `Optional[Faction]` - Faction restriction, or None if available to all factions

#### Methods

##### get_abilities
```python
def get_abilities(self) -> list[Ability]:
    """Get all abilities provided by this technology."""
```

**Returns**: `list[Ability]` - List of all abilities this technology provides

##### register_with_systems
```python
def register_with_systems(self, ability_manager: Any, unit_stats_provider: Any) -> None:
    """Register this technology with game systems."""
```

**Parameters**:
- `ability_manager: Any` - The ability manager to register abilities with
- `unit_stats_provider: Any` - The unit stats provider for unit modifications

### ExhaustibleTechnologyProtocol

**File**: `src/ti4/core/technology_cards/protocols.py`

Protocol for technologies that can be exhausted.

```python
class ExhaustibleTechnologyProtocol(Protocol):
    """Protocol for technologies that can be exhausted."""
```

#### Methods

##### is_exhausted
```python
def is_exhausted(self) -> bool:
    """Check if this technology is exhausted."""
```

**Returns**: `bool` - True if the technology is exhausted

##### exhaust
```python
def exhaust(self) -> None:
    """Exhaust this technology."""
```

**Raises**: `ValueError` - If the technology is already exhausted

##### ready
```python
def ready(self) -> None:
    """Ready this technology."""
```

##### get_action_ability
```python
def get_action_ability(self) -> Optional[Ability]:
    """Get the ACTION ability that exhausts this card."""
```

**Returns**: `Optional[Ability]` - The ACTION ability, or None if no ACTION ability exists

### UnitUpgradeTechnologyProtocol

**File**: `src/ti4/core/technology_cards/protocols.py`

Protocol for unit upgrade technologies.

```python
class UnitUpgradeTechnologyProtocol(Protocol):
    """Protocol for unit upgrade technologies."""
```

#### Properties

##### upgraded_unit_type
```python
@property
def upgraded_unit_type(self) -> UnitType:
    """The unit type this technology upgrades."""
```

**Returns**: `UnitType` - The unit type that this technology upgrades

#### Methods

##### get_unit_stat_modifications
```python
def get_unit_stat_modifications(self) -> dict[str, Any]:
    """Get the stat modifications this upgrade provides."""
```

**Returns**: `dict[str, Any]` - Dictionary mapping stat names to their new values

## Base Classes

### BaseTechnologyCard

**File**: `src/ti4/core/technology_cards/base/technology_card.py`

Abstract base class for all technology cards.

```python
class BaseTechnologyCard:
    """Base class for all technology cards."""
```

#### Constructor

```python
def __init__(self, technology_enum: Technology, name: str) -> None:
    """Initialize the base technology card."""
```

**Parameters**:
- `technology_enum: Technology` - The Technology enum value for this card
- `name: str` - Display name of the technology

#### Properties

All properties from `TechnologyCardProtocol` (abstract - must be implemented by subclasses)

#### Methods

##### register_with_systems
```python
def register_with_systems(self, ability_manager: Any, unit_stats_provider: Any) -> None:
    """Register this technology with game systems."""
```

Default implementation that registers abilities with the ability manager.

### ExhaustibleTechnologyCard

**File**: `src/ti4/core/technology_cards/base/exhaustible_tech.py`

Base implementation for exhaustible technology cards.

```python
class ExhaustibleTechnologyCard(BaseTechnologyCard):
    """Base implementation for exhaustible technology cards."""
```

#### Constructor

```python
def __init__(self, technology_enum: Technology, name: str) -> None:
    """Initialize the exhaustible technology card."""
```

#### Properties

Inherits all properties from `BaseTechnologyCard`

#### Methods

##### is_exhausted
```python
def is_exhausted(self) -> bool:
    """Check if this technology is exhausted."""
```

##### exhaust
```python
def exhaust(self) -> None:
    """Exhaust this technology."""
```

**Raises**: `ValueError` - If the technology is already exhausted

##### ready
```python
def ready(self) -> None:
    """Ready this technology."""
```

##### get_action_ability
```python
def get_action_ability(self) -> Optional[Ability]:
    """Get the ACTION ability that exhausts this card."""
```

Default implementation returns None. Override in subclasses with ACTION abilities.

### PassiveTechnologyCard

**File**: `src/ti4/core/technology_cards/base/passive_tech.py`

Base implementation for passive technology cards.

```python
class PassiveTechnologyCard(BaseTechnologyCard):
    """Base implementation for passive technology cards."""
```

Provides default implementations suitable for technologies with passive abilities.

### UnitUpgradeTechnologyCard

**File**: `src/ti4/core/technology_cards/base/unit_upgrade_tech.py`

Base implementation for unit upgrade technology cards.

```python
class UnitUpgradeTechnologyCard(BaseTechnologyCard):
    """Base implementation for unit upgrade technology cards."""
```

#### Properties

##### color
```python
@property
def color(self) -> Optional[TechnologyColor]:
    """Technology color (always None for unit upgrades)."""
```

**Returns**: `None` - Unit upgrades have no color

#### Methods

##### register_with_systems
```python
def register_with_systems(self, ability_manager: Any, unit_stats_provider: Any) -> None:
    """Register unit stat modifications with the unit stats provider."""
```

Registers unit stat modifications in addition to abilities.

## Registry Classes

### TechnologyCardRegistry

**File**: `src/ti4/core/technology_cards/registry.py`

Registry for managing concrete technology card implementations.

```python
class TechnologyCardRegistry:
    """Registry for all concrete technology card implementations."""
```

#### Constructor

```python
def __init__(self) -> None:
    """Initialize the technology card registry."""
```

#### Methods

##### register_card
```python
def register_card(self, card: TechnologyCardProtocol) -> None:
    """Register a technology card implementation."""
```

**Parameters**:
- `card: TechnologyCardProtocol` - The technology card to register

**Raises**: `ValueError` - If a card is already registered for this technology

##### get_card
```python
def get_card(self, technology: Technology) -> Optional[TechnologyCardProtocol]:
    """Get a technology card implementation."""
```

**Parameters**:
- `technology: Technology` - The technology to get the card for

**Returns**: `Optional[TechnologyCardProtocol]` - The card implementation, or None if not registered

##### get_all_cards
```python
def get_all_cards(self) -> list[TechnologyCardProtocol]:
    """Get all registered technology cards."""
```

**Returns**: `list[TechnologyCardProtocol]` - List of all registered cards

##### is_registered
```python
def is_registered(self, technology: Technology) -> bool:
    """Check if a technology card is registered."""
```

**Parameters**:
- `technology: Technology` - The technology to check

**Returns**: `bool` - True if the card is registered

##### unregister_card
```python
def unregister_card(self, technology: Technology) -> bool:
    """Unregister a technology card."""
```

**Parameters**:
- `technology: Technology` - The technology to unregister

**Returns**: `bool` - True if the card was unregistered, False if it wasn't registered

##### clear
```python
def clear(self) -> None:
    """Clear all registered technology cards."""
```

##### get_card_with_confirmation
```python
def get_card_with_confirmation(self, technology: Technology) -> TechnologyCardProtocol:
    """Get a technology card with manual confirmation enforcement."""
```

**Parameters**:
- `technology: Technology` - The technology to get the card for

**Returns**: `TechnologyCardProtocol` - The card implementation

**Raises**:
- `TechnologySpecificationError` - If technology is not confirmed
- `ValueError` - If technology card is not registered

## Specification System

### TechnologySpecification

**File**: `src/ti4/core/technology_cards/specifications.py`

Complete specification for a technology card using only enum types.

```python
@dataclass(frozen=True)
class TechnologySpecification:
    """Complete specification for a technology card using only enum types."""
```

#### Fields

- `technology: Technology` - The Technology enum value
- `name: str` - Display name of the technology
- `color: Optional[TechnologyColor]` - Technology color (None for unit upgrades)
- `prerequisites: list[TechnologyColor]` - Required prerequisite colors
- `faction_restriction: Optional[Faction]` - Faction restriction (None if available to all)
- `expansion: Expansion` - Source expansion
- `abilities: list[AbilitySpecification]` - All abilities

### AbilitySpecification

**File**: `src/ti4/core/technology_cards/specifications.py`

Specification for a technology ability using only enum types.

```python
@dataclass(frozen=True)
class AbilitySpecification:
    """Specification for a technology ability using only enum types."""
```

#### Fields

- `trigger: AbilityTrigger` - When the ability triggers
- `effect: AbilityEffectType` - What the ability does
- `conditions: list[AbilityCondition]` - Required conditions
- `mandatory: bool` - Whether the ability must be used if triggered
- `passive: bool` - Whether the ability is passive

### TechnologySpecificationRegistry

**File**: `src/ti4/core/technology_cards/specifications.py`

Registry for all technology specifications using enum-based data.

```python
class TechnologySpecificationRegistry:
    """Registry for all technology specifications using enum-based data."""
```

#### Constructor

```python
def __init__(self):
    """Initialize the registry with confirmed technology specifications."""
```

#### Methods

##### get_specification
```python
def get_specification(self, technology: Technology) -> Optional[TechnologySpecification]:
    """Get a technology specification by Technology enum."""
```

**Parameters**:
- `technology: Technology` - The Technology enum to get specification for

**Returns**: `Optional[TechnologySpecification]` - The specification if found, None otherwise

**Raises**: `TypeError` - If technology is not a Technology enum

##### has_specification
```python
def has_specification(self, technology: Technology) -> bool:
    """Check if a technology specification exists."""
```

**Parameters**:
- `technology: Technology` - The Technology enum to check

**Returns**: `bool` - True if specification exists

**Raises**: `TypeError` - If technology is not a Technology enum

##### get_all_specifications
```python
def get_all_specifications(self) -> list[TechnologySpecification]:
    """Get all technology specifications."""
```

**Returns**: `list[TechnologySpecification]` - List of all specifications

##### get_specifications_by_color
```python
def get_specifications_by_color(self, color: TechnologyColor) -> list[TechnologySpecification]:
    """Get all specifications for a specific color."""
```

**Parameters**:
- `color: TechnologyColor` - The color to filter by

**Returns**: `list[TechnologySpecification]` - List of matching specifications

**Raises**: `TypeError` - If color is not a TechnologyColor enum

##### get_specifications_by_expansion
```python
def get_specifications_by_expansion(self, expansion: Expansion) -> list[TechnologySpecification]:
    """Get all specifications for a specific expansion."""
```

**Parameters**:
- `expansion: Expansion` - The expansion to filter by

**Returns**: `list[TechnologySpecification]` - List of matching specifications

**Raises**: `TypeError` - If expansion is not an Expansion enum

##### get_specification_with_confirmation
```python
def get_specification_with_confirmation(self, technology: Technology) -> TechnologySpecification:
    """Get a technology specification with manual confirmation enforcement."""
```

**Parameters**:
- `technology: Technology` - The Technology enum to get specification for

**Returns**: `TechnologySpecification` - The specification

**Raises**:
- `TechnologySpecificationError` - If technology is not confirmed
- `TypeError` - If technology is not a Technology enum

## Integration Classes

### EnhancedAbility

**File**: `src/ti4/core/technology_cards/abilities_integration.py`

Enhanced Ability class with condition validation support.

```python
class EnhancedAbility(Ability):
    """Enhanced Ability class with condition validation support."""
```

#### Constructor

```python
def __init__(self, conditions=None, **kwargs):
    """Initialize enhanced ability with conditions."""
```

**Parameters**:
- `conditions: Optional[list[AbilityCondition]]` - List of conditions for the ability
- `**kwargs` - Additional arguments passed to base Ability class

#### Methods

##### can_trigger
```python
def can_trigger(self, event: str, context: Optional[dict] = None) -> bool:
    """Check if ability can trigger, including condition validation."""
```

**Parameters**:
- `event: str` - The event that might trigger the ability
- `context: Optional[dict]` - Context information for validation

**Returns**: `bool` - True if the ability can trigger

### UnitStatsIntegration

**File**: `src/ti4/core/technology_cards/unit_stats_integration.py`

Integration between technology cards and unit stats system.

```python
class UnitStatsIntegration:
    """Integration between technology cards and unit stats system."""
```

#### Constructor

```python
def __init__(self, unit_stats_provider):
    """Initialize unit stats integration."""
```

**Parameters**:
- `unit_stats_provider` - The unit stats provider to integrate with

#### Methods

##### register_technology_modifications
```python
def register_technology_modifications(self, tech: UnitUpgradeTechnologyCard) -> None:
    """Register unit stat modifications from a technology."""
```

**Parameters**:
- `tech: UnitUpgradeTechnologyCard` - The unit upgrade technology to register

##### unregister_technology_modifications
```python
def unregister_technology_modifications(self, technology: Technology) -> bool:
    """Unregister unit stat modifications for a technology."""
```

**Parameters**:
- `technology: Technology` - The technology to unregister

**Returns**: `bool` - True if modifications were unregistered

## Exception Classes

### TechnologySpecificationError

**File**: `src/ti4/core/technology_cards/exceptions.py`

Raised when technology specifications are not confirmed.

```python
class TechnologySpecificationError(Exception):
    """Raised when technology specifications are not confirmed."""
```

## Utility Functions

### Mapping Functions

**File**: `src/ti4/core/technology_cards/abilities_integration.py`

#### map_trigger_to_timing
```python
def map_trigger_to_timing(trigger: AbilityTrigger) -> TimingWindow:
    """Map AbilityTrigger enum to TimingWindow enum."""
```

**Parameters**:
- `trigger: AbilityTrigger` - The trigger to map

**Returns**: `TimingWindow` - The corresponding timing window

**Raises**:
- `TypeError` - If trigger is not an AbilityTrigger enum
- `ValueError` - If trigger cannot be mapped

#### map_effect_to_handler
```python
def map_effect_to_handler(effect_type: AbilityEffectType) -> Callable:
    """Map AbilityEffectType enum to actual game effect handler."""
```

**Parameters**:
- `effect_type: AbilityEffectType` - The effect type to map

**Returns**: `Callable` - Handler function for the effect

**Raises**:
- `TypeError` - If effect_type is not an AbilityEffectType enum
- `ValueError` - If effect_type cannot be mapped

#### create_ability_from_specification
```python
def create_ability_from_specification(spec: AbilitySpecification) -> Ability:
    """Create an Ability object from an AbilitySpecification."""
```

**Parameters**:
- `spec: AbilitySpecification` - The specification to convert

**Returns**: `Ability` - The created ability object

**Raises**:
- `TypeError` - If spec is not an AbilitySpecification
- `ValueError` - If specification cannot be converted

### Validation Functions

**File**: `src/ti4/core/technology_cards/specifications.py`

#### validate_specification
```python
def validate_specification(spec: TechnologySpecification) -> list[str]:
    """Validate a technology specification for consistency and completeness."""
```

**Parameters**:
- `spec: TechnologySpecification` - The specification to validate

**Returns**: `list[str]` - List of validation error messages (empty if valid)

**Raises**: `TypeError` - If spec is not a TechnologySpecification

### Confirmation Functions

**File**: `src/ti4/core/technology_cards/confirmation.py`

#### require_confirmation
```python
def require_confirmation(technology: Technology, attribute: str) -> None:
    """Enforce manual confirmation for technology attributes."""
```

**Parameters**:
- `technology: Technology` - The technology to check
- `attribute: str` - The attribute being accessed

**Raises**: `TechnologySpecificationError` - If technology is not confirmed

#### get_confirmed_technologies
```python
def get_confirmed_technologies() -> set[Technology]:
    """Get set of confirmed technologies."""
```

**Returns**: `set[Technology]` - Set of confirmed technologies

## Enum Types

### Technology

**File**: `src/ti4/core/technology_cards/specifications.py`

Enumeration of all TI4 technologies.

```python
class Technology(Enum):
    """Enumeration of TI4 technologies."""

    DARK_ENERGY_TAP = "dark_energy_tap"
    GRAVITY_DRIVE = "gravity_drive"
    # ... all technologies
```

### Expansion

**File**: `src/ti4/core/technology_cards/specifications.py`

Enumeration of TI4 expansions.

```python
class Expansion(Enum):
    """Enumeration of TI4 expansions for technology framework."""

    BASE = "base"
    PROPHECY_OF_KINGS = "prophecy_of_kings"
    # ... all expansions
```

### AbilityTrigger

**File**: `src/ti4/core/technology_cards/specifications.py`

Enumeration of ability triggers.

```python
class AbilityTrigger(Enum):
    """Enumeration of ability triggers for technology framework."""

    ACTION = "action"
    AFTER_TACTICAL_ACTION = "after_tactical_action"
    # ... all triggers
```

### AbilityEffectType

**File**: `src/ti4/core/technology_cards/specifications.py`

Enumeration of ability effect types.

```python
class AbilityEffectType(Enum):
    """Enumeration of ability effect types for technology framework."""

    EXPLORE_FRONTIER_TOKEN = "explore_frontier_token"
    MODIFY_UNIT_STATS = "modify_unit_stats"
    # ... all effect types
```

### AbilityCondition

**File**: `src/ti4/core/technology_cards/specifications.py`

Enumeration of ability conditions.

```python
class AbilityCondition(Enum):
    """Enumeration of ability conditions for technology framework."""

    HAS_SHIPS_IN_SYSTEM = "has_ships_in_system"
    SYSTEM_CONTAINS_FRONTIER = "system_contains_frontier"
    # ... all conditions
```

### UnitStatModification

**File**: `src/ti4/core/technology_cards/specifications.py`

Enumeration of unit stat modification types.

```python
class UnitStatModification(Enum):
    """Enumeration of unit stat modification types for technology framework."""

    COST = "cost"
    COMBAT_VALUE = "combat_value"
    MOVEMENT = "movement"
    # ... all stat modifications
```

## Usage Examples

### Basic Technology Implementation

```python
from ti4.core.technology_cards.base.passive_tech import PassiveTechnologyCard
from ti4.core.constants import Technology, Faction
from ti4.core.technology import TechnologyColor

class MyTechnology(PassiveTechnologyCard):
    def __init__(self):
        super().__init__(Technology.MY_TECH, "My Technology")

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
        return []  # Implement abilities
```

### Registry Usage

```python
# Create registry
registry = TechnologyCardRegistry()

# Register technology
registry.register_card(MyTechnology())

# Get technology
tech = registry.get_card(Technology.MY_TECH)
```

### Specification Usage

```python
# Create specification registry
spec_registry = TechnologySpecificationRegistry()

# Get specification
spec = spec_registry.get_specification(Technology.DARK_ENERGY_TAP)

# Filter by color
blue_specs = spec_registry.get_specifications_by_color(TechnologyColor.BLUE)
```

This API reference provides comprehensive documentation for all classes, methods, and interfaces in the Technology Card Framework.

# Technology Card Framework Enum Systems Reference

## Overview

The Technology Card Framework uses comprehensive enum systems to represent all game concepts with type safety and centralized data management. This reference documents all enum systems and their usage patterns.

## Core Design Philosophy

### Enum-First Approach

All game concepts are represented as enums to provide:

- **Type Safety**: Compile-time checking of all game references
- **Discoverability**: IDE autocomplete for all game elements
- **Centralized Registry**: Single source of truth for all game data
- **Clear Mapping**: Direct mapping from specifications to game behavior

### Benefits

1. **No Magic Strings**: All game concepts are strongly typed
2. **IDE Support**: Full autocomplete and refactoring support
3. **Validation**: Automatic validation of enum values
4. **Documentation**: Self-documenting code with clear enum names

## Technology Enums

### Technology

Represents all TI4 technologies in the game.

```python
class Technology(Enum):
    """Enumeration of TI4 technologies."""

    # Movement technologies
    GRAVITY_DRIVE = "gravity_drive"
    FLEET_LOGISTICS = "fleet_logistics"
    LIGHT_WAVE_DEFLECTOR = "light_wave_deflector"
    ANTIMASS_DEFLECTORS = "antimass_deflectors"

    # Unit upgrade technologies
    CRUISER_II = "cruiser_ii"
    DREADNOUGHT_II = "dreadnought_ii"
    CARRIER_II = "carrier_ii"
    DESTROYER_II = "destroyer_ii"
    FIGHTER_II = "fighter_ii"

    # Faction-specific technologies (manually confirmed)
    SPEC_OPS_II = "spec_ops_ii"  # Sol faction tech
    QUANTUM_DATAHUB_NODE = "quantum_datahub_node"  # Hacan faction tech

    # Prophecy of Kings technologies
    DARK_ENERGY_TAP = "dark_energy_tap"  # CONFIRMED: Blue, no prereqs
```

**Usage:**
```python
# Correct - type safe
tech = Technology.DARK_ENERGY_TAP

# Incorrect - would cause type error
tech = "dark_energy_tap"  # Don't use strings!
```

### Expansion

Represents TI4 expansions and content sources.

```python
class Expansion(Enum):
    """Enumeration of TI4 expansions for technology framework."""

    BASE = "base"
    PROPHECY_OF_KINGS = "prophecy_of_kings"
    CODEX_I = "codex_i"
    CODEX_II = "codex_ii"
    CODEX_III = "codex_iii"
```

**Usage:**
```python
# Filter technologies by expansion
pok_techs = registry.get_specifications_by_expansion(Expansion.PROPHECY_OF_KINGS)
```

## Ability System Enums

### AbilityTrigger

Represents when technology abilities trigger.

```python
class AbilityTrigger(Enum):
    """Enumeration of ability triggers for technology framework."""

    # Basic timing
    ACTION = "action"
    START_OF_TURN = "start_of_turn"
    END_OF_TURN = "end_of_turn"
    START_OF_PHASE = "start_of_phase"
    END_OF_PHASE = "end_of_phase"

    # Tactical action timing
    AFTER_ACTIVATE_SYSTEM = "after_activate_system"
    AFTER_TACTICAL_ACTION = "after_tactical_action"

    # Technology timing
    WHEN_RESEARCH_TECHNOLOGY = "when_research_technology"

    # Combat timing
    WHEN_RETREAT_DECLARED = "when_retreat_declared"
    BEFORE_COMBAT = "before_combat"
    AFTER_COMBAT = "after_combat"

    # Production timing
    WHEN_PRODUCING_UNITS = "when_producing_units"
```

**Usage:**
```python
# Create ability specification
ability_spec = AbilitySpecification(
    trigger=AbilityTrigger.AFTER_TACTICAL_ACTION,  # Type safe
    effect=AbilityEffectType.EXPLORE_FRONTIER_TOKEN,
    conditions=[AbilityCondition.HAS_SHIPS_IN_SYSTEM],
    mandatory=True,
    passive=False
)
```

**Mapping to TimingWindow:**
```python
# abilities_integration.py provides mapping
def map_trigger_to_timing(trigger: AbilityTrigger) -> TimingWindow:
    mapping = {
        AbilityTrigger.ACTION: TimingWindow.ACTION,
        AbilityTrigger.AFTER_TACTICAL_ACTION: TimingWindow.AFTER,
        AbilityTrigger.WHEN_RETREAT_DECLARED: TimingWindow.WHEN,
        # ... complete mapping
    }
    return mapping[trigger]
```

### AbilityEffectType

Represents what technology abilities do.

```python
class AbilityEffectType(Enum):
    """Enumeration of ability effect types for technology framework."""

    # Exploration effects
    EXPLORE_FRONTIER_TOKEN = "explore_frontier_token"

    # Combat effects
    ALLOW_RETREAT_TO_EMPTY_ADJACENT = "allow_retreat_to_empty_adjacent"
    MODIFY_COMBAT_VALUE = "modify_combat_value"

    # Unit effects
    MODIFY_UNIT_STATS = "modify_unit_stats"
    MODIFY_MOVEMENT = "modify_movement"
    MODIFY_CAPACITY = "modify_capacity"

    # Resource effects
    GAIN_TRADE_GOODS = "gain_trade_goods"
    GAIN_RESOURCES = "gain_resources"
    GAIN_INFLUENCE = "gain_influence"
    GAIN_COMMAND_TOKENS = "gain_command_tokens"

    # Card effects
    DRAW_ACTION_CARDS = "draw_action_cards"
    RESEARCH_TECHNOLOGY = "research_technology"
```

**Usage:**
```python
# Map effect types to handlers
def map_effect_to_handler(effect_type: AbilityEffectType) -> Callable:
    mapping = {
        AbilityEffectType.EXPLORE_FRONTIER_TOKEN: explore_frontier_handler,
        AbilityEffectType.GAIN_TRADE_GOODS: gain_trade_goods_handler,
        # ... complete mapping
    }
    return mapping[effect_type]
```

### AbilityCondition

Represents conditions that must be met for abilities to trigger.

```python
class AbilityCondition(Enum):
    """Enumeration of ability conditions for technology framework."""

    # System conditions
    HAS_SHIPS_IN_SYSTEM = "has_ships_in_system"
    SYSTEM_CONTAINS_FRONTIER = "system_contains_frontier"
    SYSTEM_CONTAINS_WORMHOLE = "system_contains_wormhole"
    ADJACENT_TO_MECATOL_REX = "adjacent_to_mecatol_rex"

    # Planet conditions
    CONTROL_PLANET = "control_planet"
    HAS_GROUND_FORCES_ON_PLANET = "has_ground_forces_on_planet"
    CONTROLS_LEGENDARY_PLANET = "controls_legendary_planet"

    # Game state conditions
    DURING_COMBAT = "during_combat"
    DURING_TACTICAL_ACTION = "during_tactical_action"
    HAS_TECHNOLOGY_OF_COLOR = "has_technology_of_color"
```

**Usage:**
```python
# Validate conditions in enhanced abilities
class EnhancedAbility(Ability):
    def _validate_conditions(self, context: dict) -> bool:
        for condition in self.conditions:
            if condition == AbilityCondition.HAS_SHIPS_IN_SYSTEM:
                if not context.get("has_ships", False):
                    return False
            elif condition == AbilityCondition.SYSTEM_CONTAINS_FRONTIER:
                if not context.get("has_frontier_token", False):
                    return False
        return True
```

## Unit System Enums

### UnitStatModification

Represents modifications that can be made to unit statistics.

```python
class UnitStatModification(Enum):
    """Enumeration of unit stat modification types for technology framework."""

    # Fundamental unit properties
    COST = "cost"
    COMBAT_VALUE = "combat_value"
    COMBAT_DICE = "combat_dice"
    MOVEMENT = "movement"
    CAPACITY = "capacity"
    PRODUCTION = "production"

    # Unit abilities
    SUSTAIN_DAMAGE = "sustain_damage"
    ANTI_FIGHTER_BARRAGE = "anti_fighter_barrage"
    BOMBARDMENT = "bombardment"
    BOMBARDMENT_VALUE = "bombardment_value"
    BOMBARDMENT_DICE = "bombardment_dice"
    DEPLOY = "deploy"
    PLANETARY_SHIELD = "planetary_shield"
    SPACE_CANNON = "space_cannon"
    SPACE_CANNON_VALUE = "space_cannon_value"
    SPACE_CANNON_DICE = "space_cannon_dice"
    HAS_PRODUCTION = "has_production"
```

**Usage:**
```python
# Unit upgrade technology example
class CruiserII(UnitUpgradeTechnologyCard):
    def get_unit_stat_modifications(self) -> dict[str, Any]:
        return {
            UnitStatModification.COMBAT_VALUE.value: 6,  # Improved combat
            UnitStatModification.CAPACITY.value: 1,      # Gains capacity
            UnitStatModification.COST.value: 2,          # Same cost
        }
```

## Faction and Game Enums

### Faction

Represents TI4 factions for faction-specific technologies.

```python
class Faction(Enum):
    """Enumeration of TI4 factions."""

    SOL = "sol"
    HACAN = "hacan"
    XXCHA = "xxcha"
    JORD = "jord"
    YSSARIL = "yssaril"
    NAALU = "naalu"
    BARONY = "barony"
    SAAR = "saar"
    MUAAT = "muaat"
    ARBOREC = "arborec"
    L1Z1X = "l1z1x"
    WINNU = "winnu"
```

**Usage:**
```python
# Faction-specific technology
spec = TechnologySpecification(
    technology=Technology.SPEC_OPS_II,
    faction_restriction=Faction.SOL,  # Only Sol can research
    # ... other attributes
)
```

### UnitType

Represents unit types for unit upgrade technologies.

```python
class UnitType(Enum):
    """Enumeration of unit types."""

    CARRIER = "carrier"
    CRUISER = "cruiser"
    CRUISER_II = "cruiser_ii"
    DREADNOUGHT = "dreadnought"
    DESTROYER = "destroyer"
    FIGHTER = "fighter"
    FLAGSHIP = "flagship"
    INFANTRY = "infantry"
    MECH = "mech"
    PDS = "pds"
    SPACE_DOCK = "space_dock"
    WAR_SUN = "war_sun"
```

**Usage:**
```python
# Unit upgrade technology
class CruiserII(UnitUpgradeTechnologyCard):
    @property
    def upgraded_unit_type(self) -> UnitType:
        return UnitType.CRUISER  # Upgrades Cruiser units
```

## Specification System

### TechnologySpecification

Uses enums to define complete technology specifications:

```python
@dataclass(frozen=True)
class TechnologySpecification:
    """Complete specification for a technology card using only enum types."""

    technology: Technology              # Which technology
    name: str                          # Display name
    color: Optional[TechnologyColor]   # Technology color (None for unit upgrades)
    prerequisites: list[TechnologyColor]  # Required colors
    faction_restriction: Optional[Faction]  # Faction restriction
    expansion: Expansion               # Source expansion
    abilities: list[AbilitySpecification]  # All abilities
```

### AbilitySpecification

Uses enums to define ability specifications:

```python
@dataclass(frozen=True)
class AbilitySpecification:
    """Specification for a technology ability using only enum types."""

    trigger: AbilityTrigger           # When it triggers
    effect: AbilityEffectType         # What it does
    conditions: list[AbilityCondition]  # Required conditions
    mandatory: bool                   # Must be used if triggered
    passive: bool                     # Passive vs active ability
```

## Usage Patterns

### Creating Specifications

```python
# Complete technology specification using only enums
dark_energy_tap_spec = TechnologySpecification(
    technology=Technology.DARK_ENERGY_TAP,
    name="Dark Energy Tap",
    color=TechnologyColor.BLUE,
    prerequisites=[],  # No prerequisites
    faction_restriction=None,  # Available to all
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

### Registry Operations

```python
# Type-safe registry operations
registry = TechnologySpecificationRegistry()

# Get specification (type-safe)
spec = registry.get_specification(Technology.DARK_ENERGY_TAP)

# Filter by color (type-safe)
blue_techs = registry.get_specifications_by_color(TechnologyColor.BLUE)

# Filter by expansion (type-safe)
pok_techs = registry.get_specifications_by_expansion(Expansion.PROPHECY_OF_KINGS)
```

### Validation

```python
# Enum-based validation
def validate_specification(spec: TechnologySpecification) -> list[str]:
    errors = []

    # Validate unit upgrade color consistency
    if spec.technology in UNIT_UPGRADE_TECHNOLOGIES and spec.color is not None:
        errors.append(f"Unit upgrade {spec.technology} should not have color")

    # Validate abilities use proper enums
    for ability in spec.abilities:
        if not isinstance(ability.trigger, AbilityTrigger):
            errors.append(f"Invalid trigger type: {type(ability.trigger)}")

    return errors
```

## Adding New Enum Values

### Process

1. **Identify Need**: Determine what new enum value is needed
2. **Add to Enum**: Add the new value to the appropriate enum
3. **Update Mappings**: Update any mapping functions that use the enum
4. **Add Tests**: Test the new enum value
5. **Document**: Update this reference documentation

### Example: Adding New Ability Trigger

```python
# 1. Add to enum
class AbilityTrigger(Enum):
    # Existing values...
    WHEN_PLANET_EXHAUSTED = "when_planet_exhausted"  # New trigger

# 2. Update mapping
def map_trigger_to_timing(trigger: AbilityTrigger) -> TimingWindow:
    mapping = {
        # Existing mappings...
        AbilityTrigger.WHEN_PLANET_EXHAUSTED: TimingWindow.WHEN,  # New mapping
    }
    return mapping[trigger]

# 3. Add tests
def test_new_trigger_mapping():
    timing = map_trigger_to_timing(AbilityTrigger.WHEN_PLANET_EXHAUSTED)
    assert timing == TimingWindow.WHEN
```

## Best Practices

### Naming Conventions

1. **Enum Names**: Use descriptive, clear names
2. **Values**: Use snake_case strings that match the enum name
3. **Consistency**: Follow existing patterns in the codebase

### Type Safety

1. **Always Use Enums**: Never use string literals for game concepts
2. **Type Hints**: Use proper type hints with enum types
3. **Validation**: Validate enum types in functions that accept them

### Documentation

1. **Docstrings**: Document all enum classes and their purpose
2. **Comments**: Add comments for complex or non-obvious enum values
3. **Examples**: Provide usage examples in docstrings

### Error Handling

```python
# Good: Type-safe with proper error handling
def process_technology(tech: Technology) -> None:
    if not isinstance(tech, Technology):
        raise TypeError(f"Expected Technology enum, got {type(tech)}")

    spec = registry.get_specification(tech)
    if spec is None:
        raise ValueError(f"No specification found for {tech}")

# Bad: Using strings without validation
def process_technology(tech_name: str) -> None:  # Don't do this!
    # No type safety, prone to typos
    if tech_name == "dark_energy_tap":  # Magic string!
        # ...
```

## Migration Guide

### From Strings to Enums

If you have existing code using strings, migrate to enums:

```python
# Old way (don't do this)
tech_name = "dark_energy_tap"
if tech_name == "dark_energy_tap":
    # ...

# New way (type-safe)
tech = Technology.DARK_ENERGY_TAP
if tech == Technology.DARK_ENERGY_TAP:
    # ...
```

### Adding New Technologies

When adding new technologies:

1. Add to `Technology` enum
2. Get user confirmation for specifications
3. Add to `TechnologySpecificationRegistry`
4. Create concrete implementation
5. Add comprehensive tests

This enum system provides the foundation for type-safe, maintainable technology card implementations. Always use enums instead of strings for game concepts!

# Technology Card Framework Integration Points Guide

## Overview

The Technology Card Framework integrates seamlessly with existing TI4 game systems. This guide documents all integration points and provides examples of how technology cards interact with other game components.

## Integration Architecture

```text
Technology Card Framework
├── Abilities System Integration
├── Unit Stats System Integration
├── Exploration System Integration
├── Combat System Integration
├── Game State Integration
├── Manual Confirmation Integration
└── Registry System Integration
```

## Abilities System Integration

### Overview

Technology cards register their abilities with the `AbilityManager` to participate in the game's ability system.

### Integration Module

**File**: `src/ti4/core/technology_cards/abilities_integration.py`

### Key Components

#### 1. Trigger Mapping

Maps technology ability triggers to the existing timing system:

```python
def map_trigger_to_timing(trigger: AbilityTrigger) -> TimingWindow:
    """Map AbilityTrigger enum to TimingWindow enum."""
    mapping = {
        AbilityTrigger.ACTION: TimingWindow.ACTION,
        AbilityTrigger.AFTER_ACTIVATE_SYSTEM: TimingWindow.AFTER,
        AbilityTrigger.AFTER_TACTICAL_ACTION: TimingWindow.AFTER,
        AbilityTrigger.WHEN_RESEARCH_TECHNOLOGY: TimingWindow.WHEN,
        AbilityTrigger.START_OF_TURN: TimingWindow.START_OF_TURN,
        AbilityTrigger.END_OF_TURN: TimingWindow.END_OF_TURN,
        AbilityTrigger.WHEN_RETREAT_DECLARED: TimingWindow.WHEN,
        AbilityTrigger.BEFORE_COMBAT: TimingWindow.BEFORE,
        AbilityTrigger.AFTER_COMBAT: TimingWindow.AFTER,
        # ... complete mapping
    }
    return mapping[trigger]
```

#### 2. Effect Mapping

Maps technology effects to actual game handlers:

```python
def map_effect_to_handler(effect_type: AbilityEffectType) -> Callable:
    """Map AbilityEffectType enum to actual game effect handler."""
    mapping = {
        AbilityEffectType.EXPLORE_FRONTIER_TOKEN: explore_frontier_token_handler,
        AbilityEffectType.ALLOW_RETREAT_TO_EMPTY_ADJACENT: allow_retreat_handler,
        AbilityEffectType.MODIFY_UNIT_STATS: modify_unit_stats_handler,
        AbilityEffectType.GAIN_TRADE_GOODS: gain_trade_goods_handler,
        # ... complete mapping
    }
    return mapping[effect_type]
```

#### 3. Enhanced Ability Class

Extends the base `Ability` class with technology-specific features:

```python
class EnhancedAbility(Ability):
    """Enhanced Ability class with condition validation support."""

    def __init__(self, conditions=None, **kwargs):
        super().__init__(**kwargs)
        self.conditions = conditions or []
        self._validate_condition_types()

    def can_trigger(self, event: str, context: Optional[dict] = None) -> bool:
        """Check if ability can trigger, including condition validation."""
        if not super().can_trigger(event, context):
            return False

        if context and self.conditions:
            return self._validate_conditions(context)

        return True

    def _validate_conditions(self, context: dict) -> bool:
        """Validate all conditions are met in the given context."""
        for condition in self.conditions:
            if condition == AbilityCondition.HAS_SHIPS_IN_SYSTEM:
                if not context.get("has_ships", False):
                    return False
            elif condition == AbilityCondition.SYSTEM_CONTAINS_FRONTIER:
                if not context.get("has_frontier_token", False):
                    return False
            # ... more condition validations
        return True
```

### Usage Example

```python
# Technology creates enhanced abilities
class DarkEnergyTap(PassiveTechnologyCard):
    def _create_frontier_exploration_ability(self) -> Ability:
        ability = EnhancedAbility(
            name="Frontier Exploration",
            timing=TimingWindow.AFTER,
            trigger="tactical_action_in_frontier_system",
            effect=AbilityEffect(
                type="explore_frontier_token",
                value=True,
            ),
            conditions=[
                AbilityCondition.HAS_SHIPS_IN_SYSTEM,
                AbilityCondition.SYSTEM_CONTAINS_FRONTIER,
            ]
        )
        ability.source = "Dark Energy Tap"
        return ability

# Abilities are registered with the system
def register_with_systems(self, ability_manager: AbilityManager, unit_stats_provider: Any):
    for ability in self.get_abilities():
        ability_manager.register_ability(ability)
```

### Integration Benefits

- **Automatic Registration**: Technology abilities participate in the standard ability system
- **Condition Validation**: Enhanced abilities validate technology-specific conditions
- **Source Tracking**: Abilities track their technology source for debugging
- **Type Safety**: All mappings use enum types for safety

## Unit Stats System Integration

### Overview

Unit upgrade technologies integrate with the `UnitStatsProvider` to modify unit statistics.

### Integration Module

**File**: `src/ti4/core/technology_cards/unit_stats_integration.py`

### Key Components

#### 1. Unit Stats Integration Class

```python
class UnitStatsIntegration:
    """Integration between technology cards and unit stats system."""

    def __init__(self, unit_stats_provider):
        self.unit_stats_provider = unit_stats_provider
        self._registered_modifications = {}

    def register_technology_modifications(self, tech: UnitUpgradeTechnologyCard) -> None:
        """Register unit stat modifications from a technology."""
        modifications = tech.get_unit_stat_modifications()
        unit_type = tech.upgraded_unit_type

        # Register with unit stats provider
        for stat_type, value in modifications.items():
            self.unit_stats_provider.register_modification(
                unit_type=unit_type,
                stat_type=stat_type,
                value=value,
                source=tech.name
            )

        # Track for unregistration
        self._registered_modifications[tech.technology_enum] = {
            'unit_type': unit_type,
            'modifications': modifications
        }
```

#### 2. Stat Modification Mapping

```python
def map_stat_modification(modification: UnitStatModification, value: Any) -> dict:
    """Map UnitStatModification enum to actual stat changes."""
    mapping = {
        UnitStatModification.COST: {'cost': value},
        UnitStatModification.COMBAT_VALUE: {'combat_value': value},
        UnitStatModification.MOVEMENT: {'movement': value},
        UnitStatModification.CAPACITY: {'capacity': value},
        UnitStatModification.SUSTAIN_DAMAGE: {'sustain_damage': value},
        # ... complete mapping
    }
    return mapping.get(modification, {})
```

### Usage Example

```python
# Unit upgrade technology
class CruiserII(UnitUpgradeTechnologyCard):
    @property
    def upgraded_unit_type(self) -> UnitType:
        return UnitType.CRUISER

    def get_unit_stat_modifications(self) -> dict[str, Any]:
        return {
            UnitStatModification.COMBAT_VALUE.value: 6,  # Improved combat
            UnitStatModification.CAPACITY.value: 1,      # Gains capacity
            UnitStatModification.COST.value: 2,          # Same cost
        }

# Integration with unit stats system
unit_stats_integration = UnitStatsIntegration(unit_stats_provider)
cruiser_ii = CruiserII()
unit_stats_integration.register_technology_modifications(cruiser_ii)

# Now Cruiser units have improved stats when player has Cruiser II
```

### Integration Benefits

- **Automatic Registration**: Unit upgrades automatically modify unit stats
- **Source Tracking**: Modifications track their technology source
- **Enum Safety**: All stat types use enum values
- **Reversible**: Modifications can be unregistered if needed

## Exploration System Integration

### Overview

Technologies like Dark Energy Tap integrate with Rule 35 exploration mechanics.

### Integration Points

#### 1. Frontier Token Exploration

```python
# In exploration.py
def can_explore_frontier_token(self, player, system):
    """Check if player can explore frontier token."""
    if not system.has_frontier_token():
        return False

    # Standard Rule 35.4 check
    if self._meets_standard_exploration_requirements(player, system):
        return True

    # Dark Energy Tap integration
    if player.has_technology(Technology.DARK_ENERGY_TAP):
        if player.has_ships_in_system(system):
            return True  # Dark Energy Tap enables exploration

    return False
```

#### 2. Exploration Validation

```python
def validate_exploration_action(self, player, system, exploration_type):
    """Validate exploration action including technology effects."""
    # Base validation
    if not self._base_exploration_validation(player, system, exploration_type):
        return False

    # Technology-specific validation
    if exploration_type == "frontier_token":
        return self._validate_frontier_exploration(player, system)

    return True

def _validate_frontier_exploration(self, player, system):
    """Validate frontier token exploration with technology support."""
    # Check for Dark Energy Tap
    if player.has_technology(Technology.DARK_ENERGY_TAP):
        return player.has_ships_in_system(system)

    # Standard Rule 35.4 requirements
    return self._meets_standard_exploration_requirements(player, system)
```

### Usage Example

```python
# Player with Dark Energy Tap can explore frontier tokens
player = create_test_player()
player.add_technology(Technology.DARK_ENERGY_TAP)

system = create_frontier_system()
player.add_ships_to_system(system, [UnitType.CRUISER])

# This will return True due to Dark Energy Tap
can_explore = exploration_manager.can_explore_frontier_token(player, system)
assert can_explore == True
```

## Combat System Integration

### Overview

Technologies can modify combat mechanics, such as retreat options.

### Integration Points

#### 1. Retreat Enhancement

```python
# In combat.py
def get_valid_retreat_systems(self, player, current_system):
    """Get valid systems for retreat, including technology enhancements."""
    valid_systems = []

    # Standard retreat rules
    adjacent_systems = self.galaxy.get_adjacent_systems(current_system)
    for system in adjacent_systems:
        if self._is_valid_standard_retreat(player, system):
            valid_systems.append(system)

    # Dark Energy Tap enhancement
    if player.has_technology(Technology.DARK_ENERGY_TAP):
        for system in adjacent_systems:
            if self._is_empty_system(system):
                valid_systems.append(system)  # Can retreat to empty adjacent

    return list(set(valid_systems))  # Remove duplicates
```

#### 2. Combat Ability Integration

```python
def process_combat_abilities(self, player, combat_context):
    """Process combat-related technology abilities."""
    abilities = self.ability_manager.get_abilities_by_timing(TimingWindow.DURING_COMBAT)

    for ability in abilities:
        if ability.source in player.technologies:
            if ability.can_trigger("combat", combat_context):
                self._execute_ability(ability, combat_context)
```

## Game State Integration

### Overview

Technology cards integrate with the overall game state management system.

### Integration Points

#### 1. Technology Manager Integration

```python
# In game_technology_manager.py
class GameTechnologyManager:
    def __init__(self):
        self.technology_registry = TechnologyCardRegistry()
        self.specification_registry = TechnologySpecificationRegistry()

    def research_technology(self, player, technology: Technology):
        """Research a technology for a player."""
        # Validate prerequisites
        spec = self.specification_registry.get_specification(technology)
        if not self._validate_prerequisites(player, spec.prerequisites):
            raise ValueError("Prerequisites not met")

        # Add to player
        player.add_technology(technology)

        # Register abilities and modifications
        tech_card = self.technology_registry.get_card(technology)
        if tech_card:
            tech_card.register_with_systems(
                self.ability_manager,
                self.unit_stats_provider
            )
```

#### 2. Player Technology Tracking

```python
# In player.py
class Player:
    def __init__(self):
        self.technologies = set()
        self.technology_cards = {}

    def add_technology(self, technology: Technology):
        """Add a technology to the player."""
        self.technologies.add(technology)

        # Get technology card instance
        tech_card = technology_registry.get_card(technology)
        if tech_card:
            self.technology_cards[technology] = tech_card

    def has_technology(self, technology: Technology) -> bool:
        """Check if player has a technology."""
        return technology in self.technologies

    def get_technology_abilities(self) -> list[Ability]:
        """Get all abilities from player's technologies."""
        abilities = []
        for tech_card in self.technology_cards.values():
            abilities.extend(tech_card.get_abilities())
        return abilities
```

## Manual Confirmation Integration

### Overview

The manual confirmation protocol is enforced throughout the framework.

### Integration Module

**File**: `src/ti4/core/technology_cards/confirmation.py`

### Key Components

#### 1. Confirmation Enforcement

```python
def require_confirmation(technology: Technology, attribute: str) -> None:
    """Enforce manual confirmation for technology attributes."""
    confirmed_technologies = get_confirmed_technologies()
    if technology not in confirmed_technologies:
        raise TechnologySpecificationError(
            f"Technology {technology} {attribute} not confirmed. "
            f"Please ask user for specification."
        )

def get_confirmed_technologies() -> set[Technology]:
    """Get set of confirmed technologies."""
    return {
        Technology.DARK_ENERGY_TAP,  # CONFIRMED: Blue, no prereqs, PoK
        Technology.GRAVITY_DRIVE,    # CONFIRMED: Blue, 1 Blue prereq, Base
        # Add more as they are confirmed
    }
```

#### 2. Registry Integration

```python
# In registry.py
def get_card_with_confirmation(self, technology: Technology) -> TechnologyCardProtocol:
    """Get technology card with confirmation enforcement."""
    require_confirmation(technology, "card")

    card = self.get_card(technology)
    if card is None:
        raise ValueError(f"Technology card {technology} is not registered")

    return card

# In specifications.py
def get_specification_with_confirmation(self, technology: Technology) -> TechnologySpecification:
    """Get specification with confirmation enforcement."""
    require_confirmation(technology, "specification")
    return self.get_specification(technology)
```

### Usage Example

```python
# This will work - Dark Energy Tap is confirmed
spec = registry.get_specification_with_confirmation(Technology.DARK_ENERGY_TAP)

# This will raise TechnologySpecificationError - not confirmed
try:
    spec = registry.get_specification_with_confirmation(Technology.SOME_NEW_TECH)
except TechnologySpecificationError as e:
    print(f"Error: {e}")
    # Must ask user for confirmation before proceeding
```

## Registry System Integration

### Overview

The registry system provides centralized management of technology cards and specifications.

### Key Components

#### 1. Technology Card Registry

```python
class TechnologyCardRegistry:
    """Registry for concrete technology card implementations."""

    def register_card(self, card: TechnologyCardProtocol) -> None:
        """Register a technology card implementation."""
        if card.technology_enum in self._cards:
            raise ValueError(f"Technology {card.technology_enum} already registered")
        self._cards[card.technology_enum] = card

    def get_card(self, technology: Technology) -> Optional[TechnologyCardProtocol]:
        """Get a technology card implementation."""
        return self._cards.get(technology)
```

#### 2. Specification Registry

```python
class TechnologySpecificationRegistry:
    """Registry for technology specifications using enum-based data."""

    def get_specifications_by_color(self, color: TechnologyColor) -> list[TechnologySpecification]:
        """Get all specifications for a specific color."""
        return [spec for spec in self._specifications.values() if spec.color == color]

    def get_specifications_by_expansion(self, expansion: Expansion) -> list[TechnologySpecification]:
        """Get all specifications for a specific expansion."""
        return [spec for spec in self._specifications.values() if spec.expansion == expansion]
```

### Usage Example

```python
# Initialize registries
card_registry = TechnologyCardRegistry()
spec_registry = TechnologySpecificationRegistry()

# Register technology cards
card_registry.register_card(DarkEnergyTap())
card_registry.register_card(GravityDrive())

# Query by color
blue_specs = spec_registry.get_specifications_by_color(TechnologyColor.BLUE)
print(f"Found {len(blue_specs)} blue technologies")

# Query by expansion
pok_specs = spec_registry.get_specifications_by_expansion(Expansion.PROPHECY_OF_KINGS)
print(f"Found {len(pok_specs)} Prophecy of Kings technologies")
```

## Integration Testing

### Testing Integration Points

```python
class TestTechnologyIntegration:
    """Test technology framework integration with game systems."""

    def test_abilities_integration(self):
        """Test technology abilities integrate with AbilityManager."""
        ability_manager = AbilityManager()
        tech = DarkEnergyTap()

        # Register abilities
        tech.register_with_systems(ability_manager, None)

        # Check abilities are registered
        abilities = ability_manager.get_abilities_by_source("Dark Energy Tap")
        assert len(abilities) == 2

    def test_exploration_integration(self):
        """Test Dark Energy Tap integrates with exploration system."""
        player = create_test_player()
        system = create_frontier_system()
        exploration_manager = ExplorationManager()

        # Without Dark Energy Tap
        assert not exploration_manager.can_explore_frontier_token(player, system)

        # With Dark Energy Tap
        player.add_technology(Technology.DARK_ENERGY_TAP)
        player.add_ships_to_system(system, [UnitType.CRUISER])
        assert exploration_manager.can_explore_frontier_token(player, system)

    def test_unit_stats_integration(self):
        """Test unit upgrade technologies integrate with unit stats."""
        unit_stats_provider = UnitStatsProvider()
        unit_stats_integration = UnitStatsIntegration(unit_stats_provider)

        # Register Cruiser II
        cruiser_ii = CruiserII()
        unit_stats_integration.register_technology_modifications(cruiser_ii)

        # Check modifications are applied
        cruiser_stats = unit_stats_provider.get_unit_stats(UnitType.CRUISER)
        assert cruiser_stats.combat_value == 6  # Improved by Cruiser II
```

## Best Practices

### 1. Integration Design

- **Clear Interfaces**: Define clear integration points between systems
- **Enum Usage**: Use enums for all integration mappings
- **Error Handling**: Handle integration failures gracefully
- **Testing**: Test all integration points thoroughly

### 2. System Coupling

- **Loose Coupling**: Keep systems loosely coupled through interfaces
- **Dependency Injection**: Use dependency injection for system references
- **Event-Driven**: Use events for system communication where appropriate
- **Validation**: Validate integration data at system boundaries

### 3. Documentation

- **Integration Points**: Document all integration points clearly
- **Usage Examples**: Provide examples of integration usage
- **Error Scenarios**: Document error scenarios and handling
- **Testing Patterns**: Document testing patterns for integration

The Technology Card Framework's integration architecture ensures seamless interaction with all existing game systems while maintaining clear separation of concerns and type safety throughout.

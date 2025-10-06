# Leader Implementation Guidelines

## Overview

This document provides comprehensive guidelines for implementing new faction leaders in the TI4 AI system. It covers patterns for implementing different types of leader abilities, unlock conditions, validation requirements, and integration with game systems.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Leader Type Patterns](#leader-type-patterns)
3. [Ability Implementation Patterns](#ability-implementation-patterns)
4. [Unlock Condition Patterns](#unlock-condition-patterns)
5. [Validation Framework](#validation-framework)
6. [Integration Guidelines](#integration-guidelines)
7. [Testing Requirements](#testing-requirements)
8. [Examples by Complexity](#examples-by-complexity)
9. [Best Practices](#best-practices)
10. [Common Pitfalls](#common-pitfalls)

## Architecture Overview

The leader system is built on a hierarchical architecture with clear separation of concerns:

```
BaseLeader (Abstract)
├── Agent (Ready/Exhaust mechanics)
├── Commander (Unlock mechanics)
└── Hero (Unlock + Purge mechanics)

Supporting Systems:
├── LeaderManager (Lifecycle management)
├── LeaderRegistry (Factory and definitions)
├── LeaderAbilityValidator (Validation framework)
└── LeaderSheet (Player integration)
```

### Core Components

- **BaseLeader**: Abstract base class defining the leader interface
- **Leader Types**: Agent, Commander, Hero with type-specific mechanics
- **LeaderManager**: Coordinates leader operations and lifecycle
- **LeaderRegistry**: Factory for creating faction-specific leaders
- **LeaderAbilityValidator**: Comprehensive validation framework
- **LeaderSheet**: Integration with player data structures

## Leader Type Patterns

### Agent Pattern

Agents are the most frequently used leaders with ready/exhaust mechanics.

```python
class FactionAgent(Agent):
    def get_name(self) -> str:
        return "Faction Agent Name"

    def get_unlock_conditions(self) -> list[str]:
        return []  # Agents start unlocked

    def check_unlock_conditions(self, game_state: GameState) -> bool:
        return True  # Always unlocked

    def execute_ability(self, game_state: GameState, **kwargs: Any) -> LeaderAbilityResult:
        # Validate state (handled by framework)
        if not self.can_use_ability():
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message=f"Agent {self.get_name()} cannot use ability in current state"
            )

        # Implement ability logic
        effects = ["Agent ability effect"]
        game_state_changes = {"ability_used": self.get_name()}

        return LeaderAbilityResult(
            success=True,
            effects=effects,
            game_state_changes=game_state_changes
        )
```

**Key Characteristics:**
- Start unlocked and readied
- Exhaust after ability use
- Ready during status phase
- Can be used repeatedly throughout the game

### Commander Pattern

Commanders provide ongoing abilities after meeting unlock conditions.

```python
class FactionCommander(Commander):
    def get_name(self) -> str:
        return "Faction Commander Name"

    def get_unlock_conditions(self) -> list[str]:
        return ["Specific unlock condition 1", "Specific unlock condition 2"]

    def check_unlock_conditions(self, game_state: GameState) -> bool:
        # Get player from game state
        player = self._get_player_from_game_state(game_state, self.player_id)
        if not player:
            return False

        # Check all conditions must be met
        condition1_met = self._check_condition_1(player, game_state)
        condition2_met = self._check_condition_2(player, game_state)

        return condition1_met and condition2_met

    def execute_ability(self, game_state: GameState, **kwargs: Any) -> LeaderAbilityResult:
        if not self.can_use_ability():
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message=f"Commander {self.get_name()} is not unlocked"
            )

        # Commanders typically provide ongoing effects
        effects = ["Ongoing commander effect"]
        game_state_changes = {"ongoing_effect": "commander_bonus"}

        return LeaderAbilityResult(
            success=True,
            effects=effects,
            game_state_changes=game_state_changes
        )
```

**Key Characteristics:**
- Start locked, unlock when conditions are met
- No exhaustion mechanics
- Provide ongoing abilities or passive benefits
- Remain unlocked for the rest of the game

### Hero Pattern

Heroes provide powerful one-time abilities and are then purged.

```python
class FactionHero(Hero):
    def get_name(self) -> str:
        return "Faction Hero Name"

    def get_unlock_conditions(self) -> list[str]:
        return ["Complex unlock condition 1", "Complex unlock condition 2", "Complex unlock condition 3"]

    def check_unlock_conditions(self, game_state: GameState) -> bool:
        # Heroes typically have more complex unlock conditions
        player = self._get_player_from_game_state(game_state, self.player_id)
        if not player:
            return False

        # All conditions must be met
        return (
            self._check_complex_condition_1(player, game_state) and
            self._check_complex_condition_2(player, game_state) and
            self._check_complex_condition_3(player, game_state)
        )

    def execute_ability(self, game_state: GameState, **kwargs: Any) -> LeaderAbilityResult:
        if not self.can_use_ability():
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message=f"Hero {self.get_name()} cannot use ability in current state"
            )

        # Heroes have powerful, game-changing effects
        effects = [
            "Powerful effect 1",
            "Powerful effect 2",
            "Powerful effect 3"
        ]
        game_state_changes = {
            "major_effect_1": True,
            "major_effect_2": "significant_value",
            "hero_purged": True
        }

        # Hero is automatically purged after ability use (handled by LeaderManager)
        return LeaderAbilityResult(
            success=True,
            effects=effects,
            game_state_changes=game_state_changes
        )
```

**Key Characteristics:**
- Start locked with complex unlock conditions
- Provide powerful one-time effects
- Automatically purged after ability use
- Cannot be used again once purged

## Ability Implementation Patterns

### Simple Effect Pattern

For straightforward abilities with no conditions or targeting.

```python
def execute_ability(self, game_state: GameState, **kwargs: Any) -> LeaderAbilityResult:
    """Simple resource generation or bonus effect."""
    if not self.can_use_ability():
        return self._create_state_error()

    # Direct effect with no validation needed
    effects = ["Generated 2 trade goods"]
    game_state_changes = {"trade_goods_gained": 2}

    return LeaderAbilityResult(
        success=True,
        effects=effects,
        game_state_changes=game_state_changes
    )
```

### Conditional Effect Pattern

For abilities that require specific game conditions.

```python
def execute_ability(self, game_state: GameState, **kwargs: Any) -> LeaderAbilityResult:
    """Conditional ability based on game state."""
    if not self.can_use_ability():
        return self._create_state_error()

    # Check game conditions
    player = self._get_player_from_game_state(game_state, self.player_id)
    if not player:
        return self._create_error("Player not found")

    # Validate conditions
    if player.controlled_planets < 3:
        return self._create_error("Must control at least 3 planets to use this ability")

    # Apply conditional effect
    bonus_amount = min(player.controlled_planets, 5)  # Cap at 5
    effects = [f"Gained {bonus_amount} resources based on controlled planets"]
    game_state_changes = {"resources_gained": bonus_amount}

    return LeaderAbilityResult(
        success=True,
        effects=effects,
        game_state_changes=game_state_changes
    )
```

### Targeting Pattern

For abilities that require target selection and validation.

```python
def execute_ability(self, game_state: GameState, **kwargs: Any) -> LeaderAbilityResult:
    """Targeting ability with validation."""
    if not self.can_use_ability():
        return self._create_state_error()

    # Validate required target parameter
    target = kwargs.get("target")
    if not target:
        return self._create_error("Target parameter is required")

    # Validate target type and format
    if not isinstance(target, str) or not target.strip():
        return self._create_error("Target must be a non-empty string")

    target = target.strip()

    # Validate target exists and is legal
    valid_targets = self._get_valid_targets(game_state)
    if target not in valid_targets:
        return self._create_error(
            f"Invalid target '{target}'. Valid targets: {', '.join(valid_targets)}"
        )

    # Apply targeted effect
    effects = [f"Applied effect to {target}"]
    game_state_changes = {"target_affected": target, "effect_type": "targeted_bonus"}

    return LeaderAbilityResult(
        success=True,
        effects=effects,
        game_state_changes=game_state_changes
    )
```

### Multi-System Integration Pattern

For abilities that interact with multiple game systems.

```python
def execute_ability(self, game_state: GameState, **kwargs: Any) -> LeaderAbilityResult:
    """Complex ability integrating with multiple systems."""
    if not self.can_use_ability():
        return self._create_state_error()

    effects = []
    game_state_changes = {}

    # Combat system integration
    if kwargs.get("combat_context"):
        combat_bonus = self._calculate_combat_bonus(game_state)
        effects.append(f"All ships gain +{combat_bonus} combat value")
        game_state_changes["combat_bonus"] = combat_bonus

    # Movement system integration
    if kwargs.get("movement_context"):
        movement_bonus = self._calculate_movement_bonus(game_state)
        effects.append(f"All ships gain +{movement_bonus} movement")
        game_state_changes["movement_bonus"] = movement_bonus

    # Resource system integration
    resource_gain = self._calculate_resource_gain(game_state)
    effects.append(f"Gained {resource_gain} resources")
    game_state_changes["resources_gained"] = resource_gain

    return LeaderAbilityResult(
        success=True,
        effects=effects,
        game_state_changes=game_state_changes
    )
```

## Unlock Condition Patterns

### Simple Condition Pattern

For straightforward unlock requirements.

```python
def check_unlock_conditions(self, game_state: GameState) -> bool:
    """Simple unlock condition: control X planets."""
    player = self._get_player_from_game_state(game_state, self.player_id)
    if not player:
        return False

    return player.controlled_planets >= 3
```

### Multiple Conditions Pattern

For unlock requirements with multiple criteria (all must be met).

```python
def check_unlock_conditions(self, game_state: GameState) -> bool:
    """Multiple unlock conditions (AND logic)."""
    player = self._get_player_from_game_state(game_state, self.player_id)
    if not player:
        return False

    # All conditions must be met
    has_enough_planets = player.controlled_planets >= 3
    has_enough_resources = player.trade_goods >= 5
    has_technology = self._check_technology_requirement(player, "ADVANCED_TECH")

    return has_enough_planets and has_enough_resources and has_technology
```

### Complex Condition Pattern

For unlock requirements with complex game state analysis.

```python
def check_unlock_conditions(self, game_state: GameState) -> bool:
    """Complex unlock conditions with game state analysis."""
    player = self._get_player_from_game_state(game_state, self.player_id)
    if not player:
        return False

    # Check victory point threshold
    if player.victory_points < 8:
        return False

    # Check control of specific systems
    if not self._controls_mecatol_rex(player, game_state):
        return False

    # Check completed objectives
    completed_objectives = self._count_completed_objectives(player, game_state)
    if completed_objectives < 2:
        return False

    # Check faction-specific condition
    if not self._check_faction_specific_condition(player, game_state):
        return False

    return True
```

### Alternative Conditions Pattern

For unlock requirements with multiple paths (OR logic).

```python
def check_unlock_conditions(self, game_state: GameState) -> bool:
    """Alternative unlock conditions (OR logic)."""
    player = self._get_player_from_game_state(game_state, self.player_id)
    if not player:
        return False

    # Any one of these conditions can unlock the leader
    path1 = player.controlled_planets >= 6
    path2 = player.victory_points >= 10
    path3 = self._controls_mecatol_rex(player, game_state) and player.trade_goods >= 8

    return path1 or path2 or path3
```

## Validation Framework

### Using the Validation Framework

The `LeaderAbilityValidator` provides comprehensive validation for leader abilities:

```python
def execute_ability(self, game_state: GameState, **kwargs: Any) -> LeaderAbilityResult:
    """Example using validation framework."""
    # The framework automatically validates:
    # - Leader state (locked/unlocked, readied/exhausted)
    # - Game phase and timing
    # - Resource requirements
    # - Target validation

    # Custom validation can be added for specific requirements
    custom_error = self._validate_custom_requirements(game_state, **kwargs)
    if custom_error:
        return LeaderAbilityResult(
            success=False,
            effects=[],
            error_message=custom_error
        )

    # Proceed with ability execution
    return self._execute_ability_logic(game_state, **kwargs)
```

### Custom Validation Patterns

```python
def _validate_custom_requirements(self, game_state: GameState, **kwargs: Any) -> str | None:
    """Custom validation for specific ability requirements."""

    # Phase-specific validation
    if kwargs.get("requires_action_phase"):
        current_phase = getattr(game_state, "current_phase", None)
        if current_phase != "action":
            return "This ability can only be used during the action phase"

    # Resource cost validation
    resource_cost = kwargs.get("resource_cost", 0)
    if resource_cost > 0:
        player = self._get_player_from_game_state(game_state, self.player_id)
        if player and player.trade_goods < resource_cost:
            return f"Insufficient resources: need {resource_cost}, have {player.trade_goods}"

    # System availability validation
    if kwargs.get("requires_combat_system"):
        combat_manager = getattr(game_state, "combat_manager", None)
        if not combat_manager:
            return "Combat system unavailable for this ability"

    return None
```

## Integration Guidelines

### Combat System Integration

```python
def _integrate_with_combat_system(self, game_state: GameState, **kwargs: Any) -> dict[str, Any]:
    """Integrate leader ability with combat system."""
    combat_effects = {}

    # Check if combat is active
    combat_manager = getattr(game_state, "combat_manager", None)
    if combat_manager:
        # Apply combat modifiers
        combat_effects["combat_bonus"] = 1
        combat_effects["applies_to"] = "all_ships"

        # Register with combat system
        if hasattr(combat_manager, "register_leader_effect"):
            combat_manager.register_leader_effect(self.player_id, combat_effects)

    return combat_effects
```

### Resource System Integration

```python
def _integrate_with_resource_system(self, game_state: GameState, **kwargs: Any) -> dict[str, Any]:
    """Integrate leader ability with resource system."""
    resource_effects = {}

    # Check resource system availability
    resource_manager = getattr(game_state, "resource_manager", None)
    if resource_manager and hasattr(resource_manager, "process_effect"):
        try:
            # Process resource changes through the system
            resource_manager.process_effect("generate_trade_goods", 2)
            resource_effects["trade_goods_gained"] = 2
        except Exception as e:
            # Fallback to direct effect
            resource_effects["trade_goods_gained"] = 2
            resource_effects["system_error"] = str(e)
    else:
        # Direct resource effect
        resource_effects["trade_goods_gained"] = 2

    return resource_effects
```

### Movement System Integration

```python
def _integrate_with_movement_system(self, game_state: GameState, **kwargs: Any) -> dict[str, Any]:
    """Integrate leader ability with movement system."""
    movement_effects = {}

    # Get movement context
    if kwargs.get("movement_context"):
        target_fleet = kwargs.get("target_fleet", [])

        # Apply movement bonuses
        movement_effects["movement_bonus"] = 1
        movement_effects["affected_ships"] = len(target_fleet)

        # Check for special movement abilities
        if kwargs.get("ignore_anomalies"):
            movement_effects["special_movement"] = "anomaly_immunity"

    return movement_effects
```

## Testing Requirements

### Unit Test Structure

```python
class TestFactionLeader:
    """Test structure for faction leader implementation."""

    def test_leader_initialization(self):
        """Test leader initializes with correct properties."""
        leader = FactionLeader(faction=Faction.FACTION_NAME, player_id="test_player")

        assert leader.get_leader_type() == LeaderType.AGENT  # or COMMANDER/HERO
        assert leader.get_name() == "Expected Leader Name"
        assert leader.faction == Faction.FACTION_NAME
        assert leader.player_id == "test_player"

    def test_unlock_conditions(self):
        """Test unlock condition checking."""
        leader = FactionLeader(faction=Faction.FACTION_NAME, player_id="test_player")
        game_state = MockGameState()

        # Test conditions not met
        game_state.add_player("test_player", **insufficient_conditions)
        assert leader.check_unlock_conditions(game_state) is False

        # Test conditions met
        game_state.add_player("test_player", **sufficient_conditions)
        assert leader.check_unlock_conditions(game_state) is True

    def test_ability_execution_success(self):
        """Test successful ability execution."""
        leader = FactionLeader(faction=Faction.FACTION_NAME, player_id="test_player")
        game_state = MockGameState()

        # Ensure leader can use ability
        if isinstance(leader, Commander) or isinstance(leader, Hero):
            leader.unlock()

        result = leader.execute_ability(game_state, **valid_parameters)

        assert result.success is True
        assert len(result.effects) > 0
        assert result.error_message is None
        assert result.game_state_changes is not None

    def test_ability_execution_failure(self):
        """Test ability execution failure scenarios."""
        leader = FactionLeader(faction=Faction.FACTION_NAME, player_id="test_player")
        game_state = MockGameState()

        # Test with invalid state
        if isinstance(leader, Agent):
            leader.exhaust()

        result = leader.execute_ability(game_state)

        assert result.success is False
        assert result.effects == []
        assert result.error_message is not None

    def test_integration_scenarios(self):
        """Test integration with other game systems."""
        leader = FactionLeader(faction=Faction.FACTION_NAME, player_id="test_player")
        game_state = MockGameState()

        # Test combat integration
        result = leader.execute_ability(game_state, combat_context=True)
        assert "combat" in str(result.effects).lower()

        # Test resource integration
        result = leader.execute_ability(game_state, resource_context=True)
        assert "resource" in str(result.effects).lower() or "trade" in str(result.effects).lower()
```

### Integration Test Patterns

```python
def test_leader_with_game_systems(self):
    """Test leader integration with actual game systems."""
    # Create real game state with systems
    game_state = GameState()
    player = Player(id="test_player", faction=Faction.FACTION_NAME)
    game_state.add_player(player)

    # Initialize leader through proper channels
    initialize_player_leaders(player)
    leader = player.leader_sheet.get_leader_by_name("Leader Name")

    # Test with LeaderManager
    manager = LeaderManager(game_state)
    result = manager.execute_leader_ability("test_player", "Leader Name")

    assert result.success is True
```

## Examples by Complexity

### Level 1: Simple Resource Generation

```python
class SimpleAgent(Agent):
    """Simplest leader pattern: generate resources."""

    def get_name(self) -> str:
        return "Resource Generator"

    def execute_ability(self, game_state: GameState, **kwargs: Any) -> LeaderAbilityResult:
        if not self.can_use_ability():
            return self._create_state_error()

        return LeaderAbilityResult(
            success=True,
            effects=["Generated 1 trade good"],
            game_state_changes={"trade_goods_gained": 1}
        )
```

### Level 2: Conditional Bonus

```python
class ConditionalCommander(Commander):
    """Medium complexity: conditional ongoing bonus."""

    def get_name(self) -> str:
        return "Conditional Bonus Commander"

    def get_unlock_conditions(self) -> list[str]:
        return ["Control 3 planets"]

    def check_unlock_conditions(self, game_state: GameState) -> bool:
        player = self._get_player_from_game_state(game_state, self.player_id)
        return player and player.controlled_planets >= 3

    def execute_ability(self, game_state: GameState, **kwargs: Any) -> LeaderAbilityResult:
        if not self.can_use_ability():
            return self._create_state_error()

        player = self._get_player_from_game_state(game_state, self.player_id)
        bonus = min(player.controlled_planets, 5)  # Cap at 5

        return LeaderAbilityResult(
            success=True,
            effects=[f"Planets produce +{bonus} resources"],
            game_state_changes={"resource_bonus": bonus}
        )
```

### Level 3: Complex Multi-System

```python
class ComplexHero(Hero):
    """High complexity: multi-system interaction with targeting."""

    def get_name(self) -> str:
        return "Complex Multi-System Hero"

    def get_unlock_conditions(self) -> list[str]:
        return ["Control Mecatol Rex", "Have 8+ victory points", "Complete 2 objectives"]

    def check_unlock_conditions(self, game_state: GameState) -> bool:
        player = self._get_player_from_game_state(game_state, self.player_id)
        if not player:
            return False

        return (
            self._controls_mecatol_rex(player, game_state) and
            player.victory_points >= 8 and
            self._count_completed_objectives(player, game_state) >= 2
        )

    def execute_ability(self, game_state: GameState, **kwargs: Any) -> LeaderAbilityResult:
        if not self.can_use_ability():
            return self._create_state_error()

        # Validate target system
        target_system = kwargs.get("target_system")
        if not target_system:
            return self._create_error("Must specify target system")

        # Validate system exists and is reachable
        if not self._validate_system_target(target_system, game_state):
            return self._create_error(f"Invalid target system: {target_system}")

        effects = []
        game_state_changes = {}

        # Multi-system effects
        # 1. Movement system: instant fleet movement
        fleet_moved = self._move_fleet_to_system(target_system, game_state)
        effects.append(f"Moved fleet to {target_system}")
        game_state_changes["fleet_movement"] = {"target": target_system, "ships": fleet_moved}

        # 2. Combat system: combat bonus
        combat_bonus = 2
        effects.append(f"Fleet gains +{combat_bonus} combat for this round")
        game_state_changes["combat_bonus"] = combat_bonus

        # 3. Resource system: resource generation
        resources_gained = 3
        effects.append(f"Gained {resources_gained} trade goods")
        game_state_changes["trade_goods_gained"] = resources_gained

        # 4. Command system: command token generation
        command_tokens = 2
        effects.append(f"Gained {command_tokens} command tokens")
        game_state_changes["command_tokens_gained"] = command_tokens

        return LeaderAbilityResult(
            success=True,
            effects=effects,
            game_state_changes=game_state_changes
        )
```

## Best Practices

### Code Organization

1. **Separate Concerns**: Keep unlock logic separate from ability logic
2. **Use Helper Methods**: Break complex logic into smaller, testable methods
3. **Consistent Naming**: Follow naming conventions for methods and variables
4. **Error Handling**: Provide clear, actionable error messages
5. **Documentation**: Include docstrings with LRR references

### Performance Considerations

1. **Lazy Evaluation**: Only compute expensive operations when needed
2. **Caching**: Cache expensive calculations where appropriate
3. **Early Returns**: Fail fast on validation errors
4. **Minimal State Changes**: Only modify game state when necessary

### Maintainability

1. **Single Responsibility**: Each method should have one clear purpose
2. **DRY Principle**: Extract common patterns into helper methods
3. **Testability**: Design for easy unit testing
4. **Extensibility**: Consider future requirements and variations

### Integration

1. **System Boundaries**: Respect boundaries between game systems
2. **Error Propagation**: Handle system unavailability gracefully
3. **Backward Compatibility**: Maintain compatibility with existing systems
4. **Event Integration**: Use event system for cross-system communication

## Common Pitfalls

### Implementation Pitfalls

1. **Hardcoded Values**: Avoid hardcoding game values that might change
2. **Missing Validation**: Always validate inputs and game state
3. **State Mutation**: Be careful about when and how you modify game state
4. **Circular Dependencies**: Avoid circular imports between modules

### Design Pitfalls

1. **Overly Complex Abilities**: Keep abilities focused and understandable
2. **Tight Coupling**: Avoid tight coupling between leaders and specific systems
3. **Missing Edge Cases**: Consider all possible game states and scenarios
4. **Inconsistent Patterns**: Follow established patterns for similar abilities

### Testing Pitfalls

1. **Insufficient Coverage**: Test all code paths and edge cases
2. **Brittle Tests**: Avoid tests that break with minor changes
3. **Missing Integration Tests**: Test interaction with real game systems
4. **Unrealistic Mocks**: Ensure mocks accurately represent real behavior

### Documentation Pitfalls

1. **Outdated Documentation**: Keep documentation current with code changes
2. **Missing LRR References**: Always reference relevant LRR rules
3. **Unclear Examples**: Provide clear, working examples
4. **Missing Context**: Explain why decisions were made, not just what was done

## Conclusion

This guide provides the foundation for implementing faction leaders in the TI4 AI system. By following these patterns and guidelines, you can create leaders that are:

- **Consistent** with the established architecture
- **Testable** and maintainable
- **Integrated** properly with game systems
- **Validated** comprehensively for correctness
- **Documented** clearly for future developers

Remember to always reference the official TI4 rules and compendium when implementing specific faction abilities, and use the placeholder leaders as architectural examples only.

For questions or clarifications about leader implementation, refer to the existing codebase examples and test suites, or consult the development team.

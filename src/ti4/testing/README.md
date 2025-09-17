# TI4 Testing Framework

This module provides a comprehensive testing framework for the TI4 game engine, featuring a fluent Builder pattern for creating complex game scenarios.

## GameScenarioBuilder

The `GameScenarioBuilder` class provides a fluent interface for constructing game states for testing purposes.

### Basic Usage

```python
from src.ti4.testing.scenario_builder import GameScenarioBuilder
from src.ti4.core.game_phase import GamePhase

# Create a basic game scenario
game_state = (GameScenarioBuilder()
              .with_players(("player1", "sol"), ("player2", "xxcha"))
              .with_galaxy("standard_6p")
              .in_phase(GamePhase.ACTION)
              .build())
```

### Advanced Features

#### Unit Placement
```python
game_state = (GameScenarioBuilder()
              .with_players(("player1", "sol"), ("player2", "xxcha"))
              .with_galaxy("standard_6p")
              .with_units([
                  ("player1", "cruiser", "system1", "space"),
                  ("player2", "carrier", "system2", "space"),
                  ("player2", "fighter", "system2", "space")
              ])
              .build())
```

#### Resource Configuration
```python
game_state = (GameScenarioBuilder()
              .with_players(("player1", "sol"))
              .with_player_resources("player1", trade_goods=10, command_tokens=16)
              .with_player_technologies("player1", ["cruiser_ii", "fighter_ii"])
              .build())
```

## Preset Scenarios

The builder provides several preset scenarios for common testing needs:

### Basic Scenarios
- `create_basic_2_player_game()`: Simple 2-player setup
- `create_early_game_scenario()`: Early game with starting units
- `create_mid_game_scenario()`: Mid-game with advanced units
- `create_late_game_scenario()`: Late game with war suns and flagships
- `create_combat_scenario()`: Units positioned for combat testing

### Faction-Specific Scenarios
```python
# Test Sol faction abilities
game_state = GameScenarioBuilder.create_faction_specific_scenario("sol")

# Test Xxcha faction abilities  
game_state = GameScenarioBuilder.create_faction_specific_scenario("xxcha")
```

### Edge Case Scenarios
```python
# Test maximum unit capacity
game_state = GameScenarioBuilder.create_edge_case_scenario("max_units")

# Test empty galaxy
game_state = GameScenarioBuilder.create_edge_case_scenario("empty_systems")

# Test resource overflow
game_state = GameScenarioBuilder.create_edge_case_scenario("resource_overflow")
```

### Multi-Player Scenarios
```python
# Create 6-player game
game_state = GameScenarioBuilder.create_multi_player_scenario(6)

# Create 3-player game
game_state = GameScenarioBuilder.create_multi_player_scenario(3)
```

## Test Utilities

The `TestUtilities` class provides helper methods for common testing patterns:

### Verification Methods
```python
from src.ti4.testing.test_utilities import TestUtilities

# Verify unit placement
expected_placements = {
    "system1": ["cruiser", "fighter"],
    "system2": ["carrier", "fighter", "fighter"]
}
assert TestUtilities.verify_unit_placement(game_state, expected_placements)

# Count units by owner
counts = TestUtilities.count_units_by_owner(system)
assert counts["player1"] == 3

# Get units by type
fighters = TestUtilities.get_units_by_type(system, "fighter")
assert len(fighters) == 2
```

### Quick Scenario Creation
```python
# Simple 2-player game
game_state = TestUtilities.create_simple_2_player_game()

# Adjacent systems for movement testing
game_state = TestUtilities.create_game_with_adjacent_systems()

# Fleet capacity testing scenario
game_state = TestUtilities.create_fleet_capacity_test_scenario()
```

## Validation

The builder includes comprehensive validation:

- **Player Validation**: Ensures unique player IDs and valid factions
- **Configuration Consistency**: Validates that all configurations are consistent
- **Resource Validation**: Ensures resource values are valid
- **Unit Placement**: Validates unit placement rules

## Error Handling

The builder provides clear error messages for invalid configurations:

```python
# This will raise ValueError: "At least one player must be configured"
GameScenarioBuilder().build()

# This will raise ValueError: "Player ID cannot be empty"
GameScenarioBuilder().with_players(("", "sol")).build()

# This will raise ValueError: "Duplicate player ID: player1"
GameScenarioBuilder().with_players(("player1", "sol"), ("player1", "xxcha")).build()
```

## Best Practices

### Test Organization
1. Use preset scenarios for common test cases
2. Create custom scenarios for specific test requirements
3. Use test utilities for verification and assertions
4. Group related tests using scenario themes

### Performance Considerations
1. Reuse scenarios when possible to avoid repeated setup
2. Use minimal scenarios for unit tests
3. Reserve complex scenarios for integration tests
4. Cache expensive scenario creation when appropriate

### Maintainability
1. Use descriptive scenario names
2. Document custom scenarios with clear comments
3. Keep scenarios focused on specific test requirements
4. Avoid overly complex scenarios that test multiple concerns

## Examples

### Testing Combat System
```python
def test_combat_detection():
    game_state = GameScenarioBuilder.create_combat_scenario()
    combat_system = game_state.systems["combat_system"]
    
    detector = CombatDetector()
    assert detector.should_initiate_combat(combat_system) is True
```

### Testing Movement Rules
```python
def test_movement_validation():
    game_state = TestUtilities.create_game_with_adjacent_systems()
    
    # Test movement between adjacent systems
    movement = MovementOperation(
        unit=game_state.systems["system_a"].space_units[0],
        from_system_id="system_a",
        to_system_id="system_b",
        player_id="player1"
    )
    
    validator = MovementValidator(game_state.galaxy)
    assert validator.is_valid_movement(movement) is True
```

### Testing Fleet Capacity
```python
def test_fleet_capacity_rules():
    game_state = TestUtilities.create_fleet_capacity_test_scenario()
    test_system = game_state.systems["test_system"]
    
    fleet = Fleet(owner="player1", system_id="test_system")
    for unit in test_system.space_units:
        fleet.add_unit(unit)
    
    validator = FleetCapacityValidator()
    assert validator.is_fleet_capacity_valid(fleet) is True
```

This testing framework provides a robust foundation for testing all aspects of the TI4 game engine while maintaining clean, readable, and maintainable test code.
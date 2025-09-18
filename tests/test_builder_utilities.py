"""Tests for builder utilities and test patterns."""

from src.ti4.core.game_phase import GamePhase
from src.ti4.testing.scenario_builder import GameScenarioBuilder
from src.ti4.testing.test_utilities import TestUtilities


def test_early_game_scenario() -> None:
    """Test early game scenario preset."""
    game_state = GameScenarioBuilder.create_early_game_scenario()

    assert len(game_state.players) == 2
    assert game_state.phase == GamePhase.STRATEGY

    # Verify both players have home systems with starting units
    home_system_1 = game_state.systems["home_system_1"]
    home_system_2 = game_state.systems["home_system_2"]

    assert len(home_system_1.space_units) == 3  # 1 carrier + 2 fighters
    assert len(home_system_2.space_units) == 3  # 1 carrier + 2 fighters

    # Verify resources
    assert game_state.player_resources["player1"]["trade_goods"] == 3
    assert game_state.player_resources["player2"]["command_tokens"] == 8


def test_mid_game_scenario() -> None:
    """Test mid-game scenario preset."""
    game_state = GameScenarioBuilder.create_mid_game_scenario()

    assert len(game_state.players) == 2
    assert game_state.phase == GamePhase.ACTION

    # Verify advanced units are present
    systems = game_state.systems
    all_units = []
    for system in systems.values():
        all_units.extend(system.space_units)

    unit_types = [unit.unit_type for unit in all_units]
    assert "dreadnought" in unit_types
    assert "war_sun" in unit_types

    # Verify technologies
    assert "dreadnought_ii" in game_state.player_technologies["player1"]
    assert "war_sun" in game_state.player_technologies["player2"]


def test_test_utilities_simple_game() -> None:
    """Test TestUtilities simple game creation."""
    game_state = TestUtilities.create_simple_2_player_game()

    assert len(game_state.players) == 2
    assert game_state.phase == GamePhase.ACTION


def test_test_utilities_adjacent_systems() -> None:
    """Test TestUtilities adjacent systems scenario."""
    game_state = TestUtilities.create_game_with_adjacent_systems()

    assert len(game_state.systems) == 2
    assert "system_a" in game_state.systems
    assert "system_b" in game_state.systems

    system_a = game_state.systems["system_a"]
    system_b = game_state.systems["system_b"]

    assert len(system_a.space_units) == 1
    assert len(system_b.space_units) == 1
    assert system_a.space_units[0].unit_type == "cruiser"
    assert system_b.space_units[0].unit_type == "destroyer"


def test_test_utilities_fleet_capacity() -> None:
    """Test TestUtilities fleet capacity scenario."""
    game_state = TestUtilities.create_fleet_capacity_test_scenario()

    test_system = game_state.systems["test_system"]
    assert len(test_system.space_units) == 6  # 1 carrier + 4 fighters + 1 infantry

    # Verify unit types
    unit_types = [unit.unit_type for unit in test_system.space_units]
    assert unit_types.count("fighter") == 4
    assert unit_types.count("carrier") == 1
    assert unit_types.count("infantry") == 1


def test_test_utilities_verification_methods() -> None:
    """Test TestUtilities verification methods."""
    game_state = TestUtilities.create_fleet_capacity_test_scenario()
    test_system = game_state.systems["test_system"]

    # Test unit counting
    counts = TestUtilities.count_units_by_owner(test_system)
    assert counts["player1"] == 6

    # Test unit filtering by type
    fighters = TestUtilities.get_units_by_type(test_system, "fighter")
    assert len(fighters) == 4

    carriers = TestUtilities.get_units_by_type(test_system, "carrier")
    assert len(carriers) == 1

    # Test placement verification
    expected_placements = {
        "test_system": [
            "carrier",
            "fighter",
            "fighter",
            "fighter",
            "fighter",
            "infantry",
        ]
    }
    assert TestUtilities.verify_unit_placement(game_state, expected_placements) is True

    # Test with wrong expectations
    wrong_expectations = {"test_system": ["dreadnought", "fighter"]}
    assert TestUtilities.verify_unit_placement(game_state, wrong_expectations) is False

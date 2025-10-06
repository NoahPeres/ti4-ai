"""Tests for GameScenarioBuilder pattern."""

import pytest

from ti4.core.constants import Faction, Technology, UnitType
from ti4.core.game_phase import GamePhase
from ti4.testing.scenario_builder import GameScenarioBuilder


def test_game_scenario_builder_creation() -> None:
    """Test that GameScenarioBuilder can be created."""
    builder = GameScenarioBuilder()
    assert builder is not None


def test_builder_with_players_fluent_interface() -> None:
    """Test that with_players returns builder for fluent interface."""
    builder = GameScenarioBuilder()
    result = builder.with_players(("player1", Faction.SOL), ("player2", Faction.XXCHA))
    assert result is builder  # Should return self for fluent interface


def test_builder_with_galaxy_fluent_interface() -> None:
    """Test that with_galaxy returns builder for fluent interface."""
    builder = GameScenarioBuilder()
    result = builder.with_galaxy("standard_6p")
    assert result is builder


def test_builder_in_phase_fluent_interface() -> None:
    """Test that in_phase returns builder for fluent interface."""
    builder = GameScenarioBuilder()
    result = builder.in_phase(GamePhase.ACTION)
    assert result is builder


def test_builder_build_creates_game_state() -> None:
    """Test that build() creates a GameState with configured components."""
    builder = GameScenarioBuilder()
    game_state = (
        builder.with_players(("player1", Faction.SOL), ("player2", Faction.XXCHA))
        .with_galaxy("standard_6p")
        .in_phase(GamePhase.ACTION)
        .build()
    )

    assert game_state is not None
    assert hasattr(game_state, "players")
    assert hasattr(game_state, "galaxy")
    assert hasattr(game_state, "phase")
    assert len(game_state.players) == 2
    assert game_state.phase == GamePhase.ACTION


def test_builder_validates_configuration_consistency() -> None:
    """Test that builder validates configuration consistency."""
    builder = GameScenarioBuilder()

    # Test empty players validation
    with pytest.raises(ValueError, match="players cannot be empty"):
        builder.build()

    # Test invalid player config
    with pytest.raises(ValueError, match="player_id cannot be empty or None"):
        builder.with_players(("", Faction.SOL)).build()

    # Test that we can't pass invalid faction types (this would be caught at type checking level)
    # For now, we'll skip the empty faction test since it requires a valid Faction enum


def test_builder_validates_duplicate_player_ids() -> None:
    """Test that builder prevents duplicate player IDs."""
    builder = GameScenarioBuilder()

    with pytest.raises(ValueError, match="Duplicate item in players"):
        builder.with_players(
            ("player1", Faction.SOL), ("player1", Faction.XXCHA)
        ).build()


def test_builder_with_units_placement() -> None:
    """Test that builder can place units in systems."""

    builder = GameScenarioBuilder()
    game_state = (
        builder.with_players(("player1", Faction.SOL), ("player2", Faction.XXCHA))
        .with_galaxy("standard_6p")
        .with_units(
            [
                ("player1", UnitType.CRUISER, "system1", "space"),
                ("player2", UnitType.CARRIER, "system2", "space"),
                ("player2", UnitType.FIGHTER, "system2", "space"),
            ]
        )
        .in_phase(GamePhase.ACTION)
        .build()
    )

    assert game_state is not None
    assert hasattr(game_state, "systems")

    # Check that units were placed correctly
    system1 = game_state.systems.get("system1")
    system2 = game_state.systems.get("system2")

    assert system1 is not None
    assert system2 is not None
    assert len(system1.space_units) == 1
    assert len(system2.space_units) == 2

    # Check unit ownership
    assert system1.space_units[0].owner == "player1"
    assert system1.space_units[0].unit_type == UnitType.CRUISER
    assert system2.space_units[0].owner == "player2"
    assert system2.space_units[1].owner == "player2"


def test_builder_with_resources_and_technologies() -> None:
    """Test builder with resource and technology configuration."""
    builder = GameScenarioBuilder()
    game_state = (
        builder.with_players(("player1", Faction.SOL), ("player2", Faction.XXCHA))
        .with_galaxy("standard_6p")
        # with_player_resources call removed - incorrect implementation
        # Resources should be tracked on planets, not as player pools
        .with_player_technologies(
            "player1", [Technology.CRUISER_II, Technology.FIGHTER_II]
        )
        .in_phase(GamePhase.ACTION)
        .build()
    )

    assert game_state is not None
    # Player resource verification removed - incorrect implementation
    # Resources should be tracked on planets, not as player pools
    assert hasattr(game_state, "player_technologies")

    # Check technologies
    player1_techs = game_state.player_technologies.get("player1")
    assert player1_techs is not None
    assert Technology.CRUISER_II in player1_techs
    assert Technology.FIGHTER_II in player1_techs


def test_builder_preset_scenarios() -> None:
    """Test that builder provides preset scenario factory methods."""
    # Test basic 2-player scenario
    game_state = GameScenarioBuilder.create_basic_2_player_game()
    assert game_state is not None
    assert len(game_state.players) == 2
    assert game_state.phase == GamePhase.ACTION

    # Test combat scenario
    game_state = GameScenarioBuilder.create_combat_scenario()
    assert game_state is not None
    assert hasattr(game_state, "systems")
    # Should have units ready for combat
    combat_system = None
    for system in game_state.systems.values():
        if len(system.space_units) >= 2:
            owners = {unit.owner for unit in system.space_units}
            if len(owners) >= 2:  # Multiple players in same system
                combat_system = system
                break
    assert combat_system is not None

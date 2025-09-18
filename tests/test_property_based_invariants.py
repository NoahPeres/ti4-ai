"""Property-based tests for TI4 game invariants using hypothesis."""

import pytest
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.strategies import composite

from src.ti4.core.game_phase import GamePhase
from src.ti4.core.game_state import GameState
from src.ti4.core.hex_coordinate import HexCoordinate
from src.ti4.core.player import Player


# GREEN Phase: Basic property-based test to verify hypothesis is working
@given(st.text())
def test_property_based_testing_setup(text_value) -> None:
    """Test that property-based testing infrastructure is working."""
    # This should pass to demonstrate hypothesis is working
    assert isinstance(text_value, str)


# REFACTOR Phase: Use proper hypothesis strategies
@composite
def valid_player_strategy(draw) -> None:
    """Generate a valid Player instance using hypothesis."""
    player_id = draw(st.text(min_size=1, max_size=50).filter(lambda x: x.strip()))
    faction = draw(st.text(min_size=1, max_size=50).filter(lambda x: x.strip()))
    return Player(id=player_id, faction=faction)


@given(valid_player_strategy())
def test_player_generator_creates_valid_players(player) -> None:
    """Test that we can generate valid Player instances."""
    assert isinstance(player, Player)
    assert player.is_valid()
    assert len(player.id.strip()) > 0
    assert len(player.faction.strip()) > 0


# GREEN Phase: Minimal hex coordinate generator
@composite
def valid_hex_coordinate_strategy(draw) -> None:
    """Generate a valid HexCoordinate instance using hypothesis."""
    q = draw(st.integers(min_value=-10, max_value=10))
    r = draw(st.integers(min_value=-10, max_value=10))
    return HexCoordinate(q, r)


@given(valid_hex_coordinate_strategy())
def test_hex_coordinate_generator_creates_valid_coordinates(coord) -> None:
    """Test that we can generate valid HexCoordinate instances."""
    assert isinstance(coord, HexCoordinate)
    assert isinstance(coord.q, int)
    assert isinstance(coord.r, int)


# REFACTOR Phase: Fix game state generator to ensure unique player IDs
@composite
def valid_game_state_strategy(draw) -> None:
    """Generate a valid GameState instance using hypothesis."""
    num_players = draw(st.integers(min_value=2, max_value=6))

    # Generate unique player IDs
    player_ids = draw(
        st.lists(
            st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
            min_size=num_players,
            max_size=num_players,
            unique=True,
        )
    )

    # Generate players with unique IDs
    players = []
    for player_id in player_ids:
        faction = draw(st.text(min_size=1, max_size=50).filter(lambda x: x.strip()))
        players.append(Player(id=player_id, faction=faction))

    phase = draw(st.sampled_from(list(GamePhase)))
    return GameState(players=players, phase=phase)


@given(valid_game_state_strategy())
def test_game_state_invariants_always_hold(state) -> None:
    """Test that game state invariants always hold regardless of input."""
    # Test basic invariants
    assert state.is_valid()
    assert isinstance(state.game_id, str)
    assert len(state.game_id) > 0
    assert len(state.players) >= 2
    assert len(state.players) <= 6
    assert isinstance(state.phase, GamePhase)


@given(valid_hex_coordinate_strategy(), valid_hex_coordinate_strategy())
def test_hex_coordinate_distance_is_symmetric(coord1, coord2) -> None:
    """Test that hex coordinate distance calculation is symmetric."""
    # Distance from A to B should equal distance from B to A
    distance_ab = coord1.distance_to(coord2)
    distance_ba = coord2.distance_to(coord1)
    assert distance_ab == distance_ba
    assert distance_ab >= 0  # Distance should never be negative


@given(valid_hex_coordinate_strategy())
def test_hex_coordinate_distance_to_self_is_zero(coord) -> None:
    """Test that distance from a coordinate to itself is always zero."""
    assert coord.distance_to(coord) == 0


@given(
    valid_hex_coordinate_strategy(),
    valid_hex_coordinate_strategy(),
    valid_hex_coordinate_strategy(),
)
def test_hex_coordinate_triangle_inequality(coord1, coord2, coord3) -> None:
    """Test that hex coordinate distances satisfy triangle inequality."""
    # For any three points A, B, C: distance(A,C) <= distance(A,B) + distance(B,C)
    distance_ac = coord1.distance_to(coord3)
    distance_ab = coord1.distance_to(coord2)
    distance_bc = coord2.distance_to(coord3)

    assert distance_ac <= distance_ab + distance_bc


@given(valid_game_state_strategy())
def test_game_state_players_have_unique_ids(state) -> None:
    """Test that all players in a game state have unique IDs."""
    player_ids = [player.id for player in state.players]
    assert len(player_ids) == len(set(player_ids)), "Player IDs must be unique"


@given(valid_game_state_strategy())
def test_game_state_immutability_preserved(state) -> None:
    """Test that game state immutability is preserved."""
    # Should not be able to modify the state after creation
    with pytest.raises(AttributeError):
        state.new_field = "value"

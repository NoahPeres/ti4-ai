"""Tests for Player class."""

from src.ti4.core.constants import Faction
from src.ti4.core.player import Player


def test_player_has_unique_identification() -> None:
    """Test that Player has unique identification."""
    player = Player(id="player1", faction=Faction.SOL)
    assert player.id == "player1"


def test_player_equality() -> None:
    """Test that Player instances with same data are equal."""
    player1 = Player(id="player1", faction=Faction.SOL)
    player2 = Player(id="player1", faction=Faction.SOL)

    assert player1 == player2


def test_player_validation() -> None:
    """Test that Player has validation methods."""
    player = Player(id="player1", faction=Faction.SOL)

    # Should have a validation method
    assert hasattr(player, "is_valid")
    assert callable(player.is_valid)

    # Valid player should return True
    assert player.is_valid() is True


def test_multiple_players_in_game_state() -> None:
    """Test that multiple players can be created with different IDs."""
    player1 = Player(id="player1", faction=Faction.SOL)
    player2 = Player(id="player2", faction=Faction.HACAN)

    # Players should have different IDs
    assert player1.id != player2.id

    # Players should be different objects
    assert player1 != player2

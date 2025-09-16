"""Tests for GameController class."""

import pytest

from src.ti4.core.exceptions import InvalidPlayerError
from src.ti4.core.game_controller import GameController
from src.ti4.core.player import Player


def test_game_controller_creation():
    """Test that GameController can be created with players."""
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
    ]
    controller = GameController(players)
    assert controller is not None


def test_turn_order_determination():
    """Test that GameController determines initial turn order."""
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
        Player(id="player3", faction="xxcha"),
    ]
    controller = GameController(players)

    # Should have a method to get turn order
    turn_order = controller.get_turn_order()
    assert len(turn_order) == 3
    assert all(player.id in ["player1", "player2", "player3"] for player in turn_order)


def test_current_player_tracking():
    """Test that GameController tracks the current active player."""
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
    ]
    controller = GameController(players)

    # Should start with first player
    current_player = controller.get_current_player()
    assert current_player.id == "player1"


def test_turn_progression():
    """Test that GameController can advance to the next player."""
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
        Player(id="player3", faction="xxcha"),
    ]
    controller = GameController(players)

    # Should start with first player
    assert controller.get_current_player().id == "player1"

    # Advance to next player
    controller.advance_turn()
    assert controller.get_current_player().id == "player2"

    # Advance again
    controller.advance_turn()
    assert controller.get_current_player().id == "player3"


def test_turn_wrapping():
    """Test that turn order wraps around to first player."""
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
    ]
    controller = GameController(players)

    # Advance through all players and wrap around
    controller.advance_turn()  # player2
    controller.advance_turn()  # back to player1
    assert controller.get_current_player().id == "player1"


def test_empty_players_list_raises_error():
    """Test that GameController raises error with empty players list."""
    with pytest.raises(ValueError, match="At least one player is required"):
        GameController([])


def test_player_activation_status():
    """Test that GameController tracks which player is currently activated."""
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
    ]
    controller = GameController(players)

    # First player should be activated
    assert controller.is_player_activated("player1") is True
    assert controller.is_player_activated("player2") is False

    # After advancing turn
    controller.advance_turn()
    assert controller.is_player_activated("player1") is False
    assert controller.is_player_activated("player2") is True


def test_player_activation_invalid_player():
    """Test that checking activation for non-existent player raises error."""
    players = [Player(id="player1", faction="sol")]
    controller = GameController(players)

    with pytest.raises(InvalidPlayerError, match="Player 'invalid' not found in game"):
        controller.is_player_activated("invalid")


def test_player_pass_turn():
    """Test that a player can pass their turn."""
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
    ]
    controller = GameController(players)

    # Player 1 is active
    assert controller.get_current_player().id == "player1"

    # Player 1 passes turn
    controller.pass_turn("player1")

    # Should advance to player 2
    assert controller.get_current_player().id == "player2"


def test_inactive_player_cannot_pass():
    """Test that inactive player cannot pass turn."""
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
    ]
    controller = GameController(players)

    # Player 1 is active, player 2 tries to pass
    with pytest.raises(ValueError, match="Player 'player2' is not currently active"):
        controller.pass_turn("player2")


def test_strategy_phase_initialization():
    """Test that GameController can enter strategy phase."""
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
    ]
    controller = GameController(players)

    # Should be able to start strategy phase
    controller.start_strategy_phase()

    # Should have strategy cards available for selection
    available_cards = controller.get_available_strategy_cards()
    assert len(available_cards) > 0


def test_strategy_card_selection():
    """Test that players can select strategy cards."""
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
    ]
    controller = GameController(players)
    controller.start_strategy_phase()

    # Player 1 should be able to select a strategy card
    available_cards = controller.get_available_strategy_cards()
    leadership_card = next(
        card for card in available_cards if card.name == "Leadership"
    )

    controller.select_strategy_card("player1", leadership_card.id)

    # Card should no longer be available
    remaining_cards = controller.get_available_strategy_cards()
    assert leadership_card not in remaining_cards

    # Player should have the selected card
    player_card = controller.get_player_strategy_card("player1")
    assert player_card == leadership_card


def test_strategy_phase_turn_order():
    """Test that turn order is determined by strategy card initiative."""
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
        Player(id="player3", faction="xxcha"),
    ]
    controller = GameController(players)
    controller.start_strategy_phase()

    # Players select cards with different initiatives
    controller.select_strategy_card("player1", 8)  # Imperial (initiative 8)
    controller.select_strategy_card("player2", 1)  # Leadership (initiative 1)
    controller.select_strategy_card("player3", 4)  # Construction (initiative 4)

    # Turn order should be based on initiative (lowest first)
    turn_order = controller.get_strategy_phase_turn_order()
    assert turn_order[0].id == "player2"  # Leadership (1)
    assert turn_order[1].id == "player3"  # Construction (4)
    assert turn_order[2].id == "player1"  # Imperial (8)


def test_strategy_phase_completion():
    """Test that strategy phase can be completed when all players have cards."""
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
    ]
    controller = GameController(players)
    controller.start_strategy_phase()

    # Initially not complete
    assert controller.is_strategy_phase_complete() is False

    # After one player selects
    controller.select_strategy_card("player1", 1)
    assert controller.is_strategy_phase_complete() is False

    # After all players select
    controller.select_strategy_card("player2", 2)
    assert controller.is_strategy_phase_complete() is True


def test_action_phase_initialization():
    """Test that GameController can enter action phase."""
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
    ]
    controller = GameController(players)

    # Should be able to start action phase
    controller.start_action_phase()

    # Should track that we're in action phase
    assert controller.get_current_phase() == "action"


def test_action_phase_turn_management():
    """Test that action phase manages turns properly."""
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
    ]
    controller = GameController(players)
    controller.start_action_phase()

    # Should start with first player in initiative order
    assert controller.get_current_player().id == "player1"

    # Player can take an action
    controller.take_tactical_action("player1", "some_action_data")

    # Should advance to next player
    assert controller.get_current_player().id == "player2"


def test_strategic_action():
    """Test that players can take strategic actions."""
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
    ]
    controller = GameController(players)
    controller.start_action_phase()

    # Player can take a strategic action
    controller.take_strategic_action("player1", "leadership_primary")

    # Should advance to next player
    assert controller.get_current_player().id == "player2"


def test_action_phase_passing():
    """Test that players can pass in action phase."""
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
    ]
    controller = GameController(players)
    controller.start_action_phase()

    # Player can pass their turn
    controller.pass_action_phase_turn("player1")

    # Should advance to next player
    assert controller.get_current_player().id == "player2"


def test_action_phase_completion():
    """Test that action phase can be completed."""
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
    ]
    controller = GameController(players)
    controller.start_action_phase()

    # Initially not complete
    assert controller.is_action_phase_complete() is False

    # After all players pass consecutively, phase should be complete
    controller.pass_action_phase_turn("player1")
    controller.pass_action_phase_turn("player2")

    # Should be complete after all players pass
    assert controller.is_action_phase_complete() is True

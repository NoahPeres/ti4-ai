"""Tests for GameController class."""

import pytest

from src.ti4.core.exceptions import InvalidPlayerError
from src.ti4.core.game_controller import GameController
from src.ti4.core.game_phase import GamePhase
from src.ti4.core.player import Player


def create_test_players(count=3) -> list[Player]:
    """Create test players for GameController tests."""
    factions = ["sol", "hacan", "xxcha", "yssaril", "naalu", "barony", "saar", "muaat"]
    return [
        Player(id=f"player{i + 1}", faction=factions[i])
        for i in range(min(count, len(factions)))
    ]


def test_game_controller_creation() -> None:
    """Test that GameController can be created with players."""
    players = create_test_players(3)
    controller = GameController(players)
    assert controller is not None


def test_turn_order_determination() -> None:
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


def test_current_player_tracking() -> None:
    """Test that GameController tracks the current active player."""
    players = create_test_players(3)
    controller = GameController(players)

    # Should start with first player
    current_player = controller.get_current_player()
    assert current_player.id == "player1"


def test_turn_progression() -> None:
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


def test_turn_wrapping() -> None:
    """Test that turn order wraps around to first player."""
    players = create_test_players(3)
    controller = GameController(players)

    # Advance through all players and wrap around
    controller.advance_turn()  # player2
    controller.advance_turn()  # player3
    controller.advance_turn()  # back to player1
    assert controller.get_current_player().id == "player1"


def test_empty_players_list_raises_error() -> None:
    """Test that GameController raises error with empty players list."""
    with pytest.raises(ValueError, match="At least one player is required"):
        GameController([])


def test_insufficient_players_raises_error() -> None:
    """Test that GameController raises error with fewer than 3 players."""
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
    ]
    with pytest.raises(ValueError, match="At least 3 players are required for TI4"):
        GameController(players)


def test_player_activation_status() -> None:
    """Test that GameController tracks which player is currently activated."""
    players = create_test_players(3)
    controller = GameController(players)

    # First player should be activated
    assert controller.is_player_activated("player1") is True
    assert controller.is_player_activated("player2") is False

    # After advancing turn
    controller.advance_turn()
    assert controller.is_player_activated("player1") is False
    assert controller.is_player_activated("player2") is True


def test_player_activation_invalid_player() -> None:
    """Test that checking activation for non-existent player raises error."""
    players = create_test_players(3)
    controller = GameController(players)

    with pytest.raises(InvalidPlayerError, match="Player 'invalid' not found in game"):
        controller.is_player_activated("invalid")


def test_player_pass_turn() -> None:
    """Test that a player can pass their turn."""
    players = create_test_players(3)
    controller = GameController(players)

    # Player 1 is active
    assert controller.get_current_player().id == "player1"

    # Player 1 passes turn
    controller.pass_turn("player1")

    # Should advance to player 2
    assert controller.get_current_player().id == "player2"


def test_inactive_player_cannot_pass() -> None:
    """Test that inactive player cannot pass turn."""
    players = create_test_players(3)
    controller = GameController(players)

    # Player 1 is active, player 2 tries to pass
    with pytest.raises(ValueError, match="Player 'player2' is not currently active"):
        controller.pass_turn("player2")


def test_strategy_phase_initialization() -> None:
    """Test that GameController can enter strategy phase."""
    players = create_test_players(3)
    controller = GameController(players)

    # Should be able to start strategy phase
    controller.start_strategy_phase()

    # Should have strategy cards available for selection
    available_cards = controller.get_available_strategy_cards()
    assert len(available_cards) > 0


def test_strategy_card_selection() -> None:
    """Test that players can select strategy cards."""
    players = create_test_players(3)
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
    player_cards = controller.get_player_strategy_cards("player1")
    assert len(player_cards) == 1
    assert player_cards[0] == leadership_card


def test_strategy_phase_turn_order() -> None:
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


def test_strategy_phase_completion() -> None:
    """Test that strategy phase can be completed when all players have cards."""
    # Use 8 players (each gets 1 card) for simplicity
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
        Player(id="player3", faction="xxcha"),
        Player(id="player4", faction="yssaril"),
        Player(id="player5", faction="naalu"),
        Player(id="player6", faction="barony"),
        Player(id="player7", faction="saar"),
        Player(id="player8", faction="muaat"),
    ]
    controller = GameController(players)
    controller.start_strategy_phase()

    # Initially not complete
    assert controller.is_strategy_phase_complete() is False

    # After some players select (but not all)
    controller.select_strategy_card("player1", 1)
    controller.select_strategy_card("player2", 2)
    assert controller.is_strategy_phase_complete() is False

    # After all players select their one card each
    controller.select_strategy_card("player3", 3)
    controller.select_strategy_card("player4", 4)
    controller.select_strategy_card("player5", 5)
    controller.select_strategy_card("player6", 6)
    controller.select_strategy_card("player7", 7)
    controller.select_strategy_card("player8", 8)
    assert controller.is_strategy_phase_complete() is True


def test_action_phase_initialization() -> None:
    """Test that GameController can enter action phase."""
    players = create_test_players(3)
    controller = GameController(players)

    # Should be able to start action phase
    controller.start_action_phase()

    # Should track that we're in action phase
    assert controller.get_current_phase() == GamePhase.ACTION


def test_action_phase_turn_management() -> None:
    """Test that action phase manages turns properly."""
    players = create_test_players(3)
    controller = GameController(players)
    controller.start_action_phase()

    # Should start with first player in initiative order
    assert controller.get_current_player().id == "player1"

    # Player can take an action
    controller.take_tactical_action("player1", "some_action_data")

    # Should advance to next player
    assert controller.get_current_player().id == "player2"


def test_strategic_action() -> None:
    """Test that players can take strategic actions."""
    players = create_test_players(3)
    controller = GameController(players)
    controller.start_action_phase()

    # Player can take a strategic action
    controller.take_strategic_action("player1", "leadership_primary")

    # Should advance to next player
    assert controller.get_current_player().id == "player2"


def test_action_phase_passing() -> None:
    """Test that players can pass in action phase."""
    players = create_test_players(3)
    controller = GameController(players)
    controller.start_action_phase()

    # Player can pass their turn
    controller.pass_action_phase_turn("player1")

    # Should advance to next player
    assert controller.get_current_player().id == "player2"


def test_action_phase_completion() -> None:
    """Test that action phase can be completed."""
    players = create_test_players(3)
    controller = GameController(players)
    controller.start_action_phase()

    # Initially not complete
    assert controller.is_action_phase_complete() is False

    # After all players pass consecutively, phase should be complete
    controller.pass_action_phase_turn("player1")
    controller.pass_action_phase_turn("player2")
    controller.pass_action_phase_turn("player3")

    # Should be complete after all players pass
    assert controller.is_action_phase_complete() is True


def test_player_can_select_multiple_strategy_cards() -> None:
    """Test that a player can select multiple strategy cards (for games with fewer than 6 players)."""
    # 4 players = 2 cards each (8 total cards / 4 players)
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
        Player(id="player3", faction="xxcha"),
        Player(id="player4", faction="yssaril"),
    ]
    controller = GameController(players)
    controller.start_strategy_phase()

    # Player 1 selects first card in round 1
    controller.select_strategy_card("player1", 1)  # Leadership
    # Skip other players for this test...
    # Player 1 selects second card in round 2
    controller.select_strategy_card("player1", 5)  # Trade

    # Player should have both cards
    player_cards = controller.get_player_strategy_cards("player1")
    assert len(player_cards) == 2
    assert any(card.id == 1 for card in player_cards)  # Leadership
    assert any(card.id == 5 for card in player_cards)  # Trade


def test_multiple_strategy_cards_turn_order() -> None:
    """Test that turn order uses lowest initiative when player has multiple cards."""
    players = create_test_players(3)
    controller = GameController(players)
    controller.start_strategy_phase()

    # Player 1 gets cards with initiatives 4 and 8
    controller.select_strategy_card("player1", 4)  # Construction (initiative 4)
    controller.select_strategy_card("player1", 8)  # Imperial (initiative 8)

    # Player 2 gets card with initiative 2
    controller.select_strategy_card("player2", 2)  # Diplomacy (initiative 2)

    # Player 3 gets card with initiative 6
    controller.select_strategy_card("player3", 6)  # Warfare (initiative 6)

    # Turn order should use lowest initiative for each player
    turn_order = controller.get_strategy_phase_turn_order()
    assert turn_order[0].id == "player2"  # Diplomacy (2)
    assert turn_order[1].id == "player1"  # Construction (4) - lowest of player1's cards
    assert turn_order[2].id == "player3"  # Warfare (6)


def test_strategy_phase_completion_with_multiple_cards() -> None:
    """Test strategy phase completion when players have multiple cards."""
    # 4 players = 2 cards each (8 total cards / 4 players)
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
        Player(id="player3", faction="xxcha"),
        Player(id="player4", faction="yssaril"),
    ]
    controller = GameController(players)
    controller.start_strategy_phase()

    # Initially not complete
    assert controller.is_strategy_phase_complete() is False

    # Round 1: Each player selects one card in table order
    controller.select_strategy_card("player1", 1)  # Leadership
    controller.select_strategy_card("player2", 2)  # Diplomacy
    controller.select_strategy_card("player3", 3)  # Politics
    controller.select_strategy_card("player4", 4)  # Construction

    # Still not complete - each player needs 2 cards total
    assert controller.is_strategy_phase_complete() is False

    # Round 2: Each player selects their second card in table order
    controller.select_strategy_card("player1", 5)  # Trade
    controller.select_strategy_card("player2", 6)  # Warfare
    controller.select_strategy_card("player3", 7)  # Technology
    controller.select_strategy_card("player4", 8)  # Imperial

    # Now complete - all players have exactly 2 cards each
    assert controller.is_strategy_phase_complete() is True


def test_cannot_select_already_taken_strategy_card() -> None:
    """Test that a strategy card cannot be selected by multiple players."""
    players = create_test_players(3)
    controller = GameController(players)
    controller.start_strategy_phase()

    # Player 1 selects Leadership
    controller.select_strategy_card("player1", 1)

    # Player 2 cannot select the same card
    with pytest.raises(ValueError, match="Strategy card with id 1 is not available"):
        controller.select_strategy_card("player2", 1)


def test_get_player_strategy_cards_empty() -> None:
    """Test getting strategy cards for player who hasn't selected any."""
    players = create_test_players(3)
    controller = GameController(players)
    controller.start_strategy_phase()

    # Player has no cards initially
    player_cards = controller.get_player_strategy_cards("player1")
    assert player_cards == []


def test_strategy_phase_requires_equal_card_distribution() -> None:
    """Test that strategy phase requires equal number of cards per player."""
    # 3 players = 2 cards each, 2 cards left over (8 total cards / 3 players = 2 remainder 2)
    # In TI4, remaining cards are not distributed
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
        Player(id="player3", faction="xxcha"),
    ]
    controller = GameController(players)
    controller.start_strategy_phase()

    # Each player gets 2 cards (6 total), 2 cards remain unused
    expected_cards_per_player = 8 // 3  # 2 cards per player

    # Round 1: Each player selects one card
    controller.select_strategy_card("player1", 1)
    controller.select_strategy_card("player2", 2)
    controller.select_strategy_card("player3", 3)

    # Not complete yet
    assert controller.is_strategy_phase_complete() is False

    # Round 2: Each player selects their second card
    controller.select_strategy_card("player1", 4)
    controller.select_strategy_card("player2", 5)
    controller.select_strategy_card("player3", 6)

    # Now complete - each player has exactly 2 cards
    assert controller.is_strategy_phase_complete() is True

    # Verify each player has the expected number of cards
    for player in players:
        player_cards = controller.get_player_strategy_cards(player.id)
        assert len(player_cards) == expected_cards_per_player


def test_backward_compatibility_get_player_strategy_card() -> None:
    """Test that the old singular method still works for backward compatibility."""
    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
        Player(id="player3", faction="xxcha"),
    ]
    controller = GameController(players)
    controller.start_strategy_phase()

    # Player selects one card
    controller.select_strategy_card("player1", 1)

    # Old method should return the first/only card
    player_card = controller.get_player_strategy_card("player1")
    assert player_card is not None
    assert player_card.id == 1

    # Player selects a second card
    controller.select_strategy_card("player1", 4)

    # Old method should still return the first card (for backward compatibility)
    player_card = controller.get_player_strategy_card("player1")
    assert player_card is not None
    assert player_card.id == 1  # Should return first card selected

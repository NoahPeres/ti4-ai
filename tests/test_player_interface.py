"""Tests for player interface abstractions."""

from abc import ABC
from typing import Any

import pytest

from src.ti4.actions.action import Action
from src.ti4.core.game_state import GameState


def test_player_interface_exists():
    """Test that PlayerInterface abstract base class exists."""
    from src.ti4.core.player_interface import PlayerInterface

    # Should be an abstract base class
    assert issubclass(PlayerInterface, ABC)


def test_player_interface_has_choose_action_method():
    """Test that PlayerInterface has choose_action method."""
    from src.ti4.core.player_interface import PlayerInterface

    # Should have choose_action method
    assert hasattr(PlayerInterface, "choose_action")

    # Method should be abstract
    assert getattr(PlayerInterface.choose_action, "__isabstractmethod__", False)


def test_player_interface_has_make_choice_method():
    """Test that PlayerInterface has make_choice method."""
    from src.ti4.core.player_interface import PlayerInterface

    # Should have make_choice method
    assert hasattr(PlayerInterface, "make_choice")

    # Method should be abstract
    assert getattr(PlayerInterface.make_choice, "__isabstractmethod__", False)


def test_basic_ai_player_exists():
    """Test that BasicAIPlayer exists and implements PlayerInterface."""
    from src.ti4.core.player_interface import BasicAIPlayer, PlayerInterface

    # Should be a subclass of PlayerInterface
    assert issubclass(BasicAIPlayer, PlayerInterface)


def test_basic_ai_player_can_be_instantiated():
    """Test that BasicAIPlayer can be instantiated."""
    from src.ti4.core.player_interface import BasicAIPlayer

    ai_player = BasicAIPlayer(player_id="ai1")
    assert ai_player.player_id == "ai1"


def test_basic_ai_player_implements_choose_action():
    """Test that BasicAIPlayer implements choose_action method."""
    from src.ti4.core.player_interface import BasicAIPlayer

    # Create a mock action for testing
    class MockAction(Action):
        def is_legal(self, state: Any, player_id: Any) -> bool:
            return True

        def execute(self, state: Any, player_id: Any) -> Any:
            return state

        def get_description(self) -> str:
            return "Mock action"

    ai_player = BasicAIPlayer(player_id="ai1")
    game_state = GameState()
    legal_actions: list[Action] = [MockAction()]

    chosen_action = ai_player.choose_action(game_state, legal_actions)
    assert chosen_action == legal_actions[0]


def test_basic_ai_player_implements_make_choice():
    """Test that BasicAIPlayer implements make_choice method."""
    from src.ti4.core.player_interface import BasicAIPlayer

    ai_player = BasicAIPlayer(player_id="ai1")
    game_state = GameState()
    choice_context = {"type": "combat_roll"}

    choice = ai_player.make_choice(game_state, choice_context)
    # Basic implementation returns None
    assert choice is None


def test_basic_ai_player_handles_no_legal_actions():
    """Test that BasicAIPlayer raises error when no legal actions available."""
    from src.ti4.core.player_interface import BasicAIPlayer

    ai_player = BasicAIPlayer(player_id="ai1")
    game_state = GameState()
    legal_actions: list[Action] = []

    with pytest.raises(ValueError, match="No legal actions available"):
        ai_player.choose_action(game_state, legal_actions)


def test_player_state_view_exists():
    """Test that PlayerStateView class exists."""
    from src.ti4.core.player_interface import PlayerStateView

    # Should be a class that can be instantiated
    assert PlayerStateView is not None


def test_player_state_view_can_be_created():
    """Test that PlayerStateView can be created from game state."""
    from src.ti4.core.player import Player
    from src.ti4.core.player_interface import PlayerStateView

    game_state = GameState(players=[Player(id="player1", faction="sol")])
    player_view = PlayerStateView.create_for_player(game_state, "player1")

    assert player_view.player_id == "player1"


def test_player_state_view_has_get_legal_actions_method():
    """Test that PlayerStateView has get_legal_actions method."""
    from src.ti4.core.player import Player
    from src.ti4.core.player_interface import PlayerStateView

    game_state = GameState(players=[Player(id="player1", faction="sol")])
    player_view = PlayerStateView.create_for_player(game_state, "player1")

    # Should have get_legal_actions method
    assert hasattr(player_view, "get_legal_actions")
    assert callable(player_view.get_legal_actions)


def test_player_state_view_get_legal_actions_returns_list():
    """Test that get_legal_actions returns a list of actions."""
    from src.ti4.core.player import Player
    from src.ti4.core.player_interface import PlayerStateView

    game_state = GameState(players=[Player(id="player1", faction="sol")])
    player_view = PlayerStateView.create_for_player(game_state, "player1")

    legal_actions = player_view.get_legal_actions()
    assert isinstance(legal_actions, list)


def test_player_state_view_has_get_visible_information_method():
    """Test that PlayerStateView has get_visible_information method."""
    from src.ti4.core.player import Player
    from src.ti4.core.player_interface import PlayerStateView

    game_state = GameState(players=[Player(id="player1", faction="sol")])
    player_view = PlayerStateView.create_for_player(game_state, "player1")

    # Should have get_visible_information method
    assert hasattr(player_view, "get_visible_information")
    assert callable(player_view.get_visible_information)


def test_player_state_view_get_visible_information_returns_dict():
    """Test that get_visible_information returns a dictionary."""
    from src.ti4.core.player import Player
    from src.ti4.core.player_interface import PlayerStateView

    game_state = GameState(players=[Player(id="player1", faction="sol")])
    player_view = PlayerStateView.create_for_player(game_state, "player1")

    visible_info = player_view.get_visible_information()
    assert isinstance(visible_info, dict)


def test_player_state_view_information_visibility():
    """Test that PlayerStateView provides appropriate information visibility."""
    from src.ti4.core.game_phase import GamePhase
    from src.ti4.core.player import Player
    from src.ti4.core.player_interface import PlayerStateView

    players = [
        Player(id="player1", faction="sol"),
        Player(id="player2", faction="hacan"),
    ]
    game_state = GameState(players=players, phase=GamePhase.ACTION)
    player_view = PlayerStateView.create_for_player(game_state, "player1")

    visible_info = player_view.get_visible_information()

    # Should include player's own ID
    assert visible_info["player_id"] == "player1"

    # Should include current game phase
    assert visible_info["game_phase"] == GamePhase.ACTION

    # Should include list of all player IDs
    assert "player1" in visible_info["players"]
    assert "player2" in visible_info["players"]

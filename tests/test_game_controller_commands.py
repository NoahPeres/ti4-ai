"""Tests for GameController command integration."""

from unittest.mock import Mock

from src.ti4.core.game_controller import GameController
from src.ti4.core.game_state import GameState
from src.ti4.core.player import Player


def test_game_controller_has_command_manager():
    """Test that GameController has a CommandManager."""
    # Create test players
    players = [
        Player(id="player1", faction="faction1"),
        Player(id="player2", faction="faction2"),
        Player(id="player3", faction="faction3"),
    ]

    # RED: This will fail because GameController doesn't have CommandManager yet
    controller = GameController(players)

    # Check that controller has command manager
    assert hasattr(controller, "_command_manager")
    assert hasattr(controller, "undo_last_action")
    assert hasattr(controller, "redo_last_action")
    assert hasattr(controller, "get_action_history")


def test_game_controller_undo_functionality():
    """Test that GameController can undo actions."""
    from src.ti4.commands.movement import MovementCommand

    # Create test players
    players = [
        Player(id="player1", faction="faction1"),
        Player(id="player2", faction="faction2"),
        Player(id="player3", faction="faction3"),
    ]
    controller = GameController(players)

    # Create a mock movement command
    unit = Mock()
    unit.unit_type = "destroyer"

    command = MovementCommand(
        unit=unit, from_system_id="system1", to_system_id="system2", player_id="player1"
    )

    # Set up initial game state and execute command through controller
    initial_state = GameState()
    controller.set_current_game_state(initial_state)
    controller.execute_command(command, initial_state)

    # Verify command was executed
    assert len(controller.get_action_history()) == 1

    # RED: Test undo functionality
    undo_success = controller.undo_last_action()

    assert undo_success is True
    assert len(controller.get_action_history()) == 0


def test_game_controller_undo_empty_history():
    """Test that GameController handles undo with no history gracefully."""
    # Create test players
    players = [
        Player(id="player1", faction="faction1"),
        Player(id="player2", faction="faction2"),
        Player(id="player3", faction="faction3"),
    ]
    controller = GameController(players)

    # RED: Test undo with empty history
    undo_success = controller.undo_last_action()

    assert undo_success is False
    assert len(controller.get_action_history()) == 0


def test_game_controller_redo_not_implemented():
    """Test that GameController redo returns False (not implemented yet)."""
    # Create test players
    players = [
        Player(id="player1", faction="faction1"),
        Player(id="player2", faction="faction2"),
        Player(id="player3", faction="faction3"),
    ]
    controller = GameController(players)

    # RED: Test redo functionality (should return False for now)
    redo_success = controller.redo_last_action()

    assert redo_success is False

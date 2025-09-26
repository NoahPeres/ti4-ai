"""Tests for movement command implementation."""

from unittest.mock import Mock

from ti4.core.constants import LocationType, UnitType
from ti4.core.game_state import GameState


def test_movement_command_exists() -> None:
    """Test that MovementCommand can be imported and implements GameCommand."""
    from ti4.commands.base import GameCommand
    from ti4.commands.movement import MovementCommand

    # Check that it's a subclass of GameCommand
    assert issubclass(MovementCommand, GameCommand)

    # Check that it has the required methods
    assert hasattr(MovementCommand, "execute")
    assert hasattr(MovementCommand, "undo")
    assert hasattr(MovementCommand, "can_execute")
    assert hasattr(MovementCommand, "get_undo_data")


def test_movement_command_creation() -> None:
    """Test that MovementCommand can be created with required parameters."""
    from ti4.commands.movement import MovementCommand

    # Create a mock unit
    unit = Mock()
    unit.unit_type = UnitType.DESTROYER.value

    # Create MovementCommand directly
    command = MovementCommand(
        unit=unit,
        from_system_id="system1",
        to_system_id="system2",
        player_id="player1",
        from_location="planet1",
        to_location=LocationType.SPACE.value,
    )

    assert command.unit == unit
    assert command.from_system_id == "system1"
    assert command.to_system_id == "system2"
    assert command.player_id == "player1"
    assert command.from_location == "planet1"
    assert command.to_location == LocationType.SPACE.value


def test_movement_command_execute_and_undo_data() -> None:
    """Test that MovementCommand collects undo data during execution."""
    from ti4.commands.movement import MovementCommand

    # Create a mock unit
    unit = Mock()
    unit.unit_type = UnitType.DESTROYER.value

    command = MovementCommand(
        unit=unit,
        from_system_id="system1",
        to_system_id="system2",
        player_id="player1",
        from_location="planet1",
        to_location="space",
    )

    initial_state = GameState()

    # RED: Test execution and undo data collection
    result_state = command.execute(initial_state)

    # Check that undo data was collected
    undo_data = command.get_undo_data()
    assert undo_data["unit"] == unit
    assert undo_data["from_system_id"] == "system1"
    assert undo_data["to_system_id"] == "system2"
    assert undo_data["from_location"] == "planet1"
    assert undo_data["to_location"] == "space"

    # For now, state should be unchanged
    assert result_state == initial_state


def test_movement_command_execute_undo_cycle() -> None:
    """Test that MovementCommand can execute and then undo properly."""
    from ti4.commands.manager import CommandManager
    from ti4.commands.movement import MovementCommand

    # Create a mock unit
    unit = Mock()
    unit.unit_type = UnitType.DESTROYER.value

    command = MovementCommand(
        unit=unit,
        from_system_id="system1",
        to_system_id="system2",
        player_id="player1",
    )

    manager = CommandManager()
    initial_state = GameState()

    # RED: Test execute/undo cycle through command manager
    # Execute command
    result_state = manager.execute_command(command, initial_state)
    assert len(manager.get_command_history()) == 1

    # Undo command
    restored_state = manager.undo_last_command(result_state)
    assert len(manager.get_command_history()) == 0

    # States should be equivalent (for now, they're the same object)
    assert restored_state == initial_state

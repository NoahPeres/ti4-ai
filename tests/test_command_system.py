"""Tests for the command system implementation."""

import pytest
from unittest.mock import Mock

from src.ti4.core.game_state import GameState


def test_game_command_interface_exists():
    """Test that GameCommand interface can be imported."""
    from src.ti4.commands.base import GameCommand
    
    # Basic interface check
    assert hasattr(GameCommand, 'execute')
    assert hasattr(GameCommand, 'undo')
    assert hasattr(GameCommand, 'can_execute')
    assert hasattr(GameCommand, 'get_undo_data')


def test_command_manager_exists():
    """Test that CommandManager class can be imported and instantiated."""
    from src.ti4.commands.manager import CommandManager
    
    manager = CommandManager()
    assert manager is not None
    assert hasattr(manager, 'execute_command')
    assert hasattr(manager, 'undo_last_command')
    assert hasattr(manager, 'get_command_history')


def test_command_manager_execute_command():
    """Test that CommandManager can execute a command."""
    from src.ti4.commands.manager import CommandManager
    from src.ti4.commands.base import GameCommand
    
    # Create a mock command
    class MockCommand(GameCommand):
        def __init__(self):
            self.executed = False
            
        def execute(self, game_state):
            self.executed = True
            return game_state
            
        def undo(self, game_state):
            self.executed = False
            return game_state
            
        def can_execute(self, game_state):
            return True
            
        def get_undo_data(self):
            return {"executed": self.executed}
            
        def serialize(self):
            return {"command_type": "MockCommand", "data": {"executed": self.executed}}
    
    manager = CommandManager()
    command = MockCommand()
    initial_state = GameState()
    
    # RED: This will fail because we need to test the actual execution
    result_state = manager.execute_command(command, initial_state)
    
    assert command.executed is True
    assert result_state is initial_state
    assert len(manager.get_command_history()) == 1


def test_command_manager_undo_command():
    """Test that CommandManager can undo a command."""
    from src.ti4.commands.manager import CommandManager
    from src.ti4.commands.base import GameCommand
    
    # Create a mock command
    class MockCommand(GameCommand):
        def __init__(self):
            self.executed = False
            
        def execute(self, game_state):
            self.executed = True
            return game_state
            
        def undo(self, game_state):
            self.executed = False
            return game_state
            
        def can_execute(self, game_state):
            return True
            
        def get_undo_data(self):
            return {"executed": self.executed}
            
        def serialize(self):
            return {"command_type": "MockCommand", "data": {"executed": self.executed}}
    
    manager = CommandManager()
    command = MockCommand()
    initial_state = GameState()
    
    # Execute then undo
    manager.execute_command(command, initial_state)
    assert command.executed is True
    
    # RED: Test undo functionality
    result_state = manager.undo_last_command(initial_state)
    
    assert command.executed is False
    assert result_state is initial_state
    assert len(manager.get_command_history()) == 0

def test_command_manager_rejects_invalid_command():
    """Test that CommandManager rejects commands that cannot be executed."""
    from src.ti4.commands.manager import CommandManager
    from src.ti4.commands.base import GameCommand
    
    # Create a command that cannot be executed
    class InvalidCommand(GameCommand):
        def execute(self, game_state):
            return game_state
            
        def undo(self, game_state):
            return game_state
            
        def can_execute(self, game_state):
            return False  # Always invalid
            
        def get_undo_data(self):
            return {}
            
        def serialize(self):
            return {"command_type": "InvalidCommand", "data": {}}
    
    manager = CommandManager()
    command = InvalidCommand()
    initial_state = GameState()
    
    # RED: This should raise an exception
    with pytest.raises(ValueError, match="Command cannot be executed"):
        manager.execute_command(command, initial_state)


def test_command_manager_undo_empty_history():
    """Test that CommandManager raises error when undoing with empty history."""
    from src.ti4.commands.manager import CommandManager
    
    manager = CommandManager()
    initial_state = GameState()
    
    # RED: This should raise an exception
    with pytest.raises(ValueError, match="No commands to undo"):
        manager.undo_last_command(initial_state)


def test_command_validation_interface():
    """Test that command validation interface works correctly."""
    from src.ti4.commands.base import GameCommand
    
    class TestCommand(GameCommand):
        def __init__(self, can_exec=True):
            self._can_exec = can_exec
            
        def execute(self, game_state):
            return game_state
            
        def undo(self, game_state):
            return game_state
            
        def can_execute(self, game_state):
            return self._can_exec
            
        def get_undo_data(self):
            return {"test": "data"}
            
        def serialize(self):
            return {"command_type": "TestCommand", "data": {"can_exec": self._can_exec}}
    
    # Test valid command
    valid_command = TestCommand(can_exec=True)
    state = GameState()
    assert valid_command.can_execute(state) is True
    
    # Test invalid command
    invalid_command = TestCommand(can_exec=False)
    assert invalid_command.can_execute(state) is False
    
    # Test undo data
    assert valid_command.get_undo_data() == {"test": "data"}
def test_command_manager_replay_from_initial_state():
    """Test that CommandManager can replay commands from initial state."""
    from src.ti4.commands.manager import CommandManager
    from src.ti4.commands.base import GameCommand
    
    # Create mock commands
    class MockCommand(GameCommand):
        def __init__(self, name):
            self.name = name
            self.executed = False
            
        def execute(self, game_state):
            self.executed = True
            return game_state
            
        def undo(self, game_state):
            self.executed = False
            return game_state
            
        def can_execute(self, game_state):
            return True
            
        def get_undo_data(self):
            return {"name": self.name}
            
        def serialize(self):
            return {"command_type": "MockCommand", "data": {"name": self.name}}
    
    manager = CommandManager()
    initial_state = GameState()
    
    # Execute multiple commands
    cmd1 = MockCommand("command1")
    cmd2 = MockCommand("command2")
    
    manager.execute_command(cmd1, initial_state)
    manager.execute_command(cmd2, initial_state)
    
    # RED: Test replay functionality
    replay_state = manager.replay_from_initial_state(initial_state)
    
    # Both commands should have been executed during replay
    assert cmd1.executed is True
    assert cmd2.executed is True
    assert replay_state == initial_state  # For now, state is unchanged


def test_command_serialization():
    """Test that commands can be serialized for persistence."""
    from src.ti4.commands.manager import CommandManager
    from src.ti4.commands.movement import MovementCommand
    from unittest.mock import Mock
    
    # Create a movement command
    unit = Mock()
    unit.unit_type = "destroyer"
    
    command = MovementCommand(
        unit=unit,
        from_system_id="system1",
        to_system_id="system2",
        player_id="player1"
    )
    
    manager = CommandManager()
    initial_state = GameState()
    
    # Execute command
    manager.execute_command(command, initial_state)
    
    # RED: Test serialization functionality
    serialized_commands = manager.serialize_commands()
    
    # Should return a list of serializable data
    assert isinstance(serialized_commands, list)
    assert len(serialized_commands) == 1
    
    # First command should be serializable
    cmd_data = serialized_commands[0]
    assert isinstance(cmd_data, dict)
    assert "command_type" in cmd_data
    assert "data" in cmd_data
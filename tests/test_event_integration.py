"""Test event integration with commands."""

from unittest.mock import Mock

from ti4.commands.movement import MovementCommand
from ti4.core.constants import Faction
from ti4.core.events import GameEventBus, PhaseChangedEvent, UnitMovedEvent
from ti4.core.game_controller import GameController
from ti4.core.game_phase import GamePhase
from ti4.core.game_state import GameState
from ti4.core.player import Player
from ti4.core.unit import Unit


class TestMovementEventIntegration:
    """Test event publishing in movement commands."""

    def test_movement_command_publishes_unit_moved_event(self) -> None:
        """Test that movement commands publish unit moved events."""
        event_bus = GameEventBus()
        observer = Mock()
        event_bus.subscribe("unit_moved", observer)

        unit = Unit("destroyer", "player_1")
        command = MovementCommand(
            unit=unit,
            from_system_id="system_1",
            to_system_id="system_2",
            player_id="player_1",
        )

        game_state = GameState()

        # Execute command with event bus
        command.execute_with_events(game_state, event_bus)

        # Verify event was published
        observer.assert_called_once()
        published_event = observer.call_args[0][0]
        assert isinstance(published_event, UnitMovedEvent)
        assert published_event.unit_id == unit.id
        assert published_event.from_system == "system_1"
        assert published_event.to_system == "system_2"
        assert published_event.player_id == "player_1"

    def test_movement_command_without_event_bus_still_works(self) -> None:
        """Test that movement commands work without event bus for backward compatibility."""
        unit = Unit("destroyer", "player_1")
        command = MovementCommand(
            unit=unit,
            from_system_id="system_1",
            to_system_id="system_2",
            player_id="player_1",
        )

        game_state = GameState()

        # Should not raise exception
        result = command.execute(game_state)
        assert result is not None


class TestGameControllerEventIntegration:
    """Test event publishing in game controller."""

    def test_game_controller_publishes_phase_changed_event(self) -> None:
        """Test that changing game phase publishes a PhaseChangedEvent."""
        # Setup
        players = [
            Player("player_1", Faction.SOL),
            Player("player_2", Faction.XXCHA),
            Player("player_3", Faction.HACAN),
        ]
        controller = GameController(players)

        event_bus = GameEventBus()
        observer = Mock()
        event_bus.subscribe("phase_changed", observer)

        # Set event bus on controller
        controller.set_event_bus(event_bus)

        # Change phase
        controller.advance_to_phase(GamePhase.STRATEGY)

        # Verify event was published
        observer.assert_called_once()
        published_event = observer.call_args[0][0]
        assert isinstance(published_event, PhaseChangedEvent)
        assert published_event.from_phase == "setup"
        assert published_event.to_phase == "strategy"

    def test_game_controller_without_event_bus_still_works(self) -> None:
        """Test that game controller works without event bus for backward compatibility."""
        players = [
            Player("player_1", Faction.SOL),
            Player("player_2", Faction.XXCHA),
            Player("player_3", Faction.HACAN),
        ]
        controller = GameController(players)

        # Should not raise exception
        controller.advance_to_phase(GamePhase.STRATEGY)
        assert controller.get_current_phase() == GamePhase.STRATEGY


class TestEventBusIntegration:
    """Test integration scenarios with event bus."""

    def test_multiple_actions_publish_multiple_events(self) -> None:
        """Test that multiple actions publish their respective events."""
        event_bus = GameEventBus()
        all_events = []

        def capture_event(event) -> None:
            all_events.append(event)

        event_bus.subscribe("unit_moved", capture_event)
        event_bus.subscribe("phase_changed", capture_event)

        # Setup game controller
        players = [
            Player("player_1", Faction.SOL),
            Player("player_2", Faction.XXCHA),
            Player("player_3", Faction.HACAN),
        ]
        controller = GameController(players)
        controller.set_event_bus(event_bus)

        # Setup movement command
        unit = Unit("destroyer", "player_1")
        command = MovementCommand(
            unit=unit,
            from_system_id="system_1",
            to_system_id="system_2",
            player_id="player_1",
        )

        game_state = GameState()

        # Execute actions
        controller.advance_to_phase(GamePhase.STRATEGY)
        command.execute_with_events(game_state, event_bus)

        # Verify both events were published
        assert len(all_events) == 2
        assert any(isinstance(event, PhaseChangedEvent) for event in all_events)
        assert any(isinstance(event, UnitMovedEvent) for event in all_events)

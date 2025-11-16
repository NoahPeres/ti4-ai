"""Test for Rule 89.2b: Player may choose to not move any ships."""

from ti4.actions.movement_engine import MovementPlan, MovementStep
from ti4.core.constants import UnitType
from ti4.core.game_state import GameState
from ti4.core.system import System
from ti4.core.unit import Unit


class TestRule89_2b_EmptyMovement:
    """Test Rule 89.2b: Player may choose to not move any ships."""

    def test_empty_movement_plan_should_execute(self) -> None:
        """Test that MovementStep executes even with empty movement plan (Rule 89.2b)."""
        # Create a movement step
        movement_step = MovementStep()

        # Create game state with a simple system
        game_state = GameState()
        system = System(system_id="test_system")
        game_state.systems["test_system"] = system

        # Create context with empty movement plan
        context = {
            "movement_plan": MovementPlan(),  # Empty plan - no movements
            "player_id": "player1",
        }

        # Verify the step can execute with empty plan
        assert movement_step.can_execute(game_state, context) is True

        # Execute the step - should not raise any errors
        result_state = movement_step.execute(game_state, context)

        # State should remain unchanged
        assert result_state is game_state
        assert len(game_state.systems["test_system"].space_units) == 0

    def test_no_movement_plan_should_execute(self) -> None:
        """Test that MovementStep executes even when no movement plan is provided (Rule 89.2b)."""
        # Create a movement step
        movement_step = MovementStep()

        # Create game state with a simple system
        game_state = GameState()
        system = System(system_id="test_system")
        game_state.systems["test_system"] = system

        # Create context with no movement plan
        context = {
            "player_id": "player1"
            # No movement_plan key
        }

        # Verify the step can execute without plan
        assert movement_step.can_execute(game_state, context) is True

        # Execute the step - should not raise any errors
        result_state = movement_step.execute(game_state, context)

        # State should remain unchanged
        assert result_state is game_state
        assert len(game_state.systems["test_system"].space_units) == 0

    def test_movement_step_name(self) -> None:
        """Test that MovementStep has correct name for debugging/logging."""
        movement_step = MovementStep()
        assert movement_step.get_step_name() == "Movement"

    def test_empty_plan_with_systems_present(self) -> None:
        """Test that empty movement plan works correctly when systems have units."""

        # Create a movement step
        movement_step = MovementStep()

        # Create game state with systems containing units
        game_state = GameState()

        # Source system with a ship
        source_system = System(system_id="source")
        source_system.place_unit_in_space(
            Unit(unit_type=UnitType.CARRIER, owner="player1")
        )
        game_state.systems["source"] = source_system

        # Target system (empty)
        target_system = System(system_id="target")
        game_state.systems["target"] = target_system

        # Create empty movement plan
        empty_plan = MovementPlan()
        context = {"movement_plan": empty_plan, "player_id": "player1"}

        # Verify the step can execute
        assert movement_step.can_execute(game_state, context) is True

        # Execute the step
        result_state = movement_step.execute(game_state, context)

        # Verify no units were moved
        assert len(result_state.systems["source"].space_units) == 1
        assert len(result_state.systems["target"].space_units) == 0
        assert (
            result_state.systems["source"].space_units[0].unit_type == UnitType.CARRIER
        )

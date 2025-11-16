"""Test Rule 89.2b: Player may choose to not move any ships (empty movement plan validation).

This test demonstrates that the current implementation should handle empty movement plans
where a player activates a system but chooses not to move any ships. According to LRR Rule 89.2b,
a player may choose to not move any ships during the movement step.

The test should pass initially, showing that empty movement plans are already supported.
"""

from ti4.actions.movement_engine import MovementPlan
from ti4.core.constants import UnitType
from ti4.core.galaxy import Galaxy
from ti4.core.game_state import GameState
from ti4.core.hex_coordinate import HexCoordinate
from ti4.core.system import System
from ti4.core.tactical_action_coordinator import TacticalActionCoordinator
from ti4.core.unit import Unit


class TestRule89_2bEmptyMovementPlan:
    """Test empty movement plan validation for Rule 89.2b."""

    def test_player_may_choose_not_to_move_any_ships(self) -> None:
        """A player should be able to activate a system without moving any ships."""
        galaxy = Galaxy()
        active_system = System("active")

        # Place system
        galaxy.place_system(HexCoordinate(0, 0), active_system.system_id)
        galaxy.register_system(active_system)

        # Create a ship in an adjacent system (but don't move it)
        adjacent_system = System("adjacent")
        galaxy.place_system(HexCoordinate(1, 0), adjacent_system.system_id)
        galaxy.register_system(adjacent_system)

        ship = Unit(unit_type=UnitType.CRUISER, owner="player1")
        adjacent_system.place_unit_in_space(ship)

        # Create empty movement plan (no movements)
        plan = MovementPlan()
        # Intentionally not adding any movements to test empty plan

        game_state = GameState(
            galaxy=galaxy,
            systems={
                active_system.system_id: active_system,
                adjacent_system.system_id: adjacent_system,
            },
        )

        coordinator = TacticalActionCoordinator()
        results = coordinator.validate_and_execute_tactical_action(
            active_system,
            "player1",
            galaxy,
            movement_plan=plan,
            game_state=game_state,
        )

        # Movement should be considered executed (even if no units moved)
        assert results.get("movement_executed") is True

        # Ship should still be in adjacent system (not moved)
        adjacent_space_units = adjacent_system.get_units_in_space()
        assert ship in adjacent_space_units

        # Ship should not be in active system
        active_space_units = active_system.get_units_in_space()
        assert ship not in active_space_units

    def test_empty_movement_plan_with_units_present(self) -> None:
        """Player can choose not to move even when units are present and could move."""
        galaxy = Galaxy()
        active_system = System("active")
        source_system = System("source")

        # Place systems adjacent to each other
        galaxy.place_system(HexCoordinate(0, 0), active_system.system_id)
        galaxy.place_system(HexCoordinate(1, 0), source_system.system_id)
        galaxy.register_system(active_system)
        galaxy.register_system(source_system)

        # Create multiple ships that could move but don't
        ships = [
            Unit(unit_type=UnitType.CRUISER, owner="player1"),
            Unit(unit_type=UnitType.CARRIER, owner="player1"),
            Unit(unit_type=UnitType.DESTROYER, owner="player1"),
        ]

        # Place all ships in source system
        for ship in ships:
            source_system.place_unit_in_space(ship)

        # Create empty movement plan (deliberately not moving any ships)
        plan = MovementPlan()
        # No movements added - this tests the "may choose not to move" rule

        game_state = GameState(
            galaxy=galaxy,
            systems={
                active_system.system_id: active_system,
                source_system.system_id: source_system,
            },
        )

        coordinator = TacticalActionCoordinator()
        results = coordinator.validate_and_execute_tactical_action(
            active_system,
            "player1",
            galaxy,
            movement_plan=plan,
            game_state=game_state,
        )

        # Movement step should complete successfully with no movements
        assert results.get("movement_executed") is True

        # All ships should remain in source system
        source_space_units = source_system.get_units_in_space()
        for ship in ships:
            assert ship in source_space_units

        # No ships should be in active system
        active_space_units = active_system.get_units_in_space()
        assert len(active_space_units) == 0

    def test_no_movement_plan_defaults_to_empty_movement(self) -> None:
        """When no movement plan is provided, it should be treated as choosing not to move."""
        galaxy = Galaxy()
        active_system = System("active")

        # Place system
        galaxy.place_system(HexCoordinate(0, 0), active_system.system_id)
        galaxy.register_system(active_system)

        # Create a ship in the system
        ship = Unit(unit_type=UnitType.CRUISER, owner="player1")
        active_system.place_unit_in_space(ship)

        game_state = GameState(
            galaxy=galaxy,
            systems={
                active_system.system_id: active_system,
            },
        )

        coordinator = TacticalActionCoordinator()
        results = coordinator.validate_and_execute_tactical_action(
            active_system,
            "player1",
            galaxy,
            # No movement_plan parameter provided
            game_state=game_state,
        )

        # Movement step should complete successfully
        assert results.get("movement_executed") is True

        # Ship should remain in the active system
        active_space_units = active_system.get_units_in_space()
        assert ship in active_space_units

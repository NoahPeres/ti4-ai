"""Test for Rule 89.5a: Production abilities execution during tactical action."""

from ti4.actions.movement_engine import MovementPlan
from ti4.core.constants import UnitType
from ti4.core.system import System
from ti4.core.tactical_action_coordinator import TacticalActionCoordinator
from ti4.core.unit import Unit


class TestRule89_5a_ProductionAbilitiesExecution:
    """Test Rule 89.5a: Production abilities should be resolved when units have production capability."""

    def test_production_abilities_should_be_executed_when_units_have_production(
        self,
    ) -> None:
        """Test that production abilities are executed when units have production capability (Rule 89.5a)."""
        # Create a system with a unit that has production ability
        active_system = System("active_system")

        # Add a unit with production ability (e.g., Space Dock)
        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="active_player")
        active_system.space_units = [space_dock]

        # Create a simple galaxy for the test
        from ti4.core.galaxy import Galaxy

        galaxy = Galaxy()

        # Create tactical action coordinator
        coordinator = TacticalActionCoordinator()

        # Execute tactical action
        results = coordinator.validate_and_execute_tactical_action(
            active_system=active_system,
            player="active_player",
            galaxy=galaxy,
            movement_plan=MovementPlan(),
        )

        # Verify results indicate production was executed
        assert results["production_executed"] is True
        assert results["production_result"]["production_executed"] is True
        assert results["production_result"]["units_with_production"] == 1
        assert "SPACE_DOCK" in results["production_result"]["production_units"]

    def test_no_production_when_no_units_with_production_abilities(self) -> None:
        """Test that no production occurs when no units have production capability (Rule 89.5a)."""
        # Create a system with units that have no production ability
        active_system = System("active_system")

        # Add units without production ability (e.g., ships without production)
        carrier = Unit(unit_type=UnitType.CARRIER, owner="active_player")
        fighter = Unit(unit_type=UnitType.FIGHTER, owner="active_player")
        active_system.space_units = [carrier, fighter]

        # Create a simple galaxy for the test
        from ti4.core.galaxy import Galaxy

        galaxy = Galaxy()

        # Create tactical action coordinator
        coordinator = TacticalActionCoordinator()

        # Execute tactical action
        results = coordinator.validate_and_execute_tactical_action(
            active_system=active_system,
            player="active_player",
            galaxy=galaxy,
            movement_plan=MovementPlan(),
        )

        # Verify results indicate no production
        assert results.get("production_executed", False) is False

    def test_production_with_multiple_units_having_production_abilities(self) -> None:
        """Test that production abilities are executed when multiple units have production capability (Rule 89.5a)."""
        # Create a system with multiple units that have production ability
        active_system = System("active_system")

        # Add multiple units with production ability
        space_dock1 = Unit(unit_type=UnitType.SPACE_DOCK, owner="active_player")
        space_dock2 = Unit(unit_type=UnitType.SPACE_DOCK, owner="active_player")
        active_system.space_units = [space_dock1, space_dock2]

        # Create a simple galaxy for the test
        from ti4.core.galaxy import Galaxy

        galaxy = Galaxy()

        # Create tactical action coordinator
        coordinator = TacticalActionCoordinator()

        # Execute tactical action
        results = coordinator.validate_and_execute_tactical_action(
            active_system=active_system,
            player="active_player",
            galaxy=galaxy,
            movement_plan=MovementPlan(),
        )

        # Verify results indicate production was executed
        assert results["production_executed"] is True
        assert results["production_result"]["production_executed"] is True
        assert results["production_result"]["units_with_production"] == 2
        assert "SPACE_DOCK" in results["production_result"]["production_units"]

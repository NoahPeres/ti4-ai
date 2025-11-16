"""Test for Rule 89.4b: Ground force landing mechanics during invasion step."""

from unittest.mock import Mock, patch

from ti4.actions.movement_engine import MovementPlan
from ti4.core.constants import UnitType
from ti4.core.system import System
from ti4.core.tactical_action_coordinator import TacticalActionCoordinator
from ti4.core.unit import Unit


class TestRule89_4b_GroundForceLanding:
    """Test Rule 89.4b: Units should be able to land on planets during invasion step."""

    def test_ground_forces_should_land_on_planets_when_committed(self) -> None:
        """Test that ground forces can be committed to land on planets (Rule 89.4b)."""
        # Create a system with a planet and ground forces in space
        active_system = System("active_system")

        # Add a planet (no enemy units initially)
        from ti4.core.planet import Planet

        planet = Planet("test_planet", resources=1, influence=1)
        planet.units = []  # No units on planet initially
        active_system.planets = [planet]

        # Add ground forces (Infantry) in space area
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="active_player")
        active_system.space_units = [infantry]

        # Create a simple galaxy for the test
        from ti4.core.galaxy import Galaxy

        galaxy = Galaxy()

        # Create tactical action coordinator
        coordinator = TacticalActionCoordinator()

        # Mock the invasion system to verify ground forces are committed
        with patch("ti4.core.invasion.InvasionController") as mock_invasion_class:
            mock_invasion_system = Mock()
            mock_invasion_class.return_value = mock_invasion_system

            # Execute tactical action
            coordinator.validate_and_execute_tactical_action(
                active_system=active_system,
                player="active_player",
                galaxy=galaxy,
                movement_plan=MovementPlan(),
            )

            # Verify invasion system was created (since ground forces can land)
            mock_invasion_class.assert_called_once()

            # Verify ground forces were committed to land
            mock_invasion_system.commit_ground_forces_step.assert_called_once()

    def test_no_ground_forces_available_should_not_trigger_landing(self) -> None:
        """Test that no landing occurs when no ground forces are in space."""
        # Create a system with a planet but no ground forces in space
        active_system = System("active_system")

        # Add a planet
        from ti4.core.planet import Planet

        planet = Planet("test_planet", resources=1, influence=1)
        planet.units = []
        active_system.planets = [planet]

        # Add only ships (no ground forces) in space area
        carrier = Unit(unit_type=UnitType.CARRIER, owner="active_player")
        active_system.space_units = [carrier]

        # Create a simple galaxy for the test
        from ti4.core.galaxy import Galaxy

        galaxy = Galaxy()

        # Create tactical action coordinator
        coordinator = TacticalActionCoordinator()

        # Mock the invasion system to verify it's NOT called
        with patch("ti4.core.invasion.InvasionController") as mock_invasion_class:
            mock_invasion_system = Mock()
            mock_invasion_class.return_value = mock_invasion_system

            # Execute tactical action
            coordinator.validate_and_execute_tactical_action(
                active_system=active_system,
                player="active_player",
                galaxy=galaxy,
                movement_plan=MovementPlan(),
            )

            # Verify invasion system was NOT created or called
            mock_invasion_class.assert_not_called()
            mock_invasion_system.commit_ground_forces_step.assert_not_called()

    def test_no_planets_available_should_not_trigger_landing(self) -> None:
        """Test that no landing occurs when there are no planets to land on."""
        # Create a system with ground forces but no planets
        active_system = System("active_system")

        # No planets
        active_system.planets = []

        # Add ground forces (Infantry) in space area
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="active_player")
        active_system.space_units = [infantry]

        # Create a simple galaxy for the test
        from ti4.core.galaxy import Galaxy

        galaxy = Galaxy()

        # Create tactical action coordinator
        coordinator = TacticalActionCoordinator()

        # Mock the invasion system to verify it's NOT called
        with patch("ti4.core.invasion.InvasionController") as mock_invasion_class:
            mock_invasion_system = Mock()
            mock_invasion_class.return_value = mock_invasion_system

            # Execute tactical action
            coordinator.validate_and_execute_tactical_action(
                active_system=active_system,
                player="active_player",
                galaxy=galaxy,
                movement_plan=MovementPlan(),
            )

            # Verify invasion system was NOT created or called
            mock_invasion_class.assert_not_called()
            mock_invasion_system.commit_ground_forces_step.assert_not_called()

"""Test for Rule 89.4c: Ground combat resolution during invasion step."""

from unittest.mock import Mock, patch

from ti4.actions.movement_engine import MovementPlan
from ti4.core.constants import UnitType
from ti4.core.system import System
from ti4.core.tactical_action_coordinator import TacticalActionCoordinator
from ti4.core.unit import Unit


class TestRule89_4c_GroundCombatResolution:
    """Test Rule 89.4c: Ground combat should be resolved when opposing ground forces are present."""

    def test_ground_combat_should_be_resolved_when_opposing_forces_present(
        self,
    ) -> None:
        """Test that ground combat is resolved when both players have ground forces on a planet (Rule 89.4c)."""
        # Create a system with a planet that has ground forces from both players
        active_system = System("active_system")

        # Add a planet with ground forces from both players
        from ti4.core.planet import Planet

        planet = Planet("test_planet", resources=1, influence=1)

        # Active player's ground forces
        active_infantry = Unit(unit_type=UnitType.INFANTRY, owner="active_player")
        # Opponent's ground forces
        opponent_infantry = Unit(unit_type=UnitType.INFANTRY, owner="opponent_player")

        planet.units = [active_infantry, opponent_infantry]
        active_system.planets = [planet]

        # Add ground forces in space for the active player (to simulate landing)
        space_infantry = Unit(unit_type=UnitType.INFANTRY, owner="active_player")
        active_system.space_units = [space_infantry]

        # Create a simple galaxy for the test
        from ti4.core.galaxy import Galaxy

        galaxy = Galaxy()

        # Create tactical action coordinator
        coordinator = TacticalActionCoordinator()

        # Mock the invasion system to verify ground combat is resolved
        with patch("ti4.core.invasion.InvasionController") as mock_invasion_class:
            mock_invasion_system = Mock()
            mock_invasion_class.return_value = mock_invasion_system

            # Mock the ground combat resolution to return combat occurred
            mock_invasion_system.resolve_ground_combat.return_value = {
                "combat_resolved": True,
                "winner": "active_player",
                "remaining_units": [active_infantry],
            }

            # Execute tactical action
            results = coordinator.validate_and_execute_tactical_action(
                active_system=active_system,
                player="active_player",
                galaxy=galaxy,
                movement_plan=MovementPlan(),
            )

            # Verify invasion system was created
            mock_invasion_class.assert_called_once()

            # Verify ground combat was resolved
            mock_invasion_system.resolve_ground_combat.assert_called_once()

            # Verify results indicate combat was resolved
            assert results["ground_combat_resolved"] is True
            assert results["ground_combat_result"]["combat_resolved"] is True

    def test_no_ground_combat_when_only_active_player_forces_present(self) -> None:
        """Test that ground combat is not resolved when only active player has ground forces (Rule 89.4c)."""
        # Create a system with a planet that only has active player's ground forces
        active_system = System("active_system")

        # Add a planet with only active player's ground forces
        from ti4.core.planet import Planet

        planet = Planet("test_planet", resources=1, influence=1)

        # Only active player's ground forces
        active_infantry = Unit(unit_type=UnitType.INFANTRY, owner="active_player")
        planet.units = [active_infantry]
        active_system.planets = [planet]

        # Add ground forces in space for the active player
        space_infantry = Unit(unit_type=UnitType.INFANTRY, owner="active_player")
        active_system.space_units = [space_infantry]

        # Create a simple galaxy for the test
        from ti4.core.galaxy import Galaxy

        galaxy = Galaxy()

        # Create tactical action coordinator
        coordinator = TacticalActionCoordinator()

        # Mock the invasion system to verify ground combat is NOT called
        with patch("ti4.core.invasion.InvasionController") as mock_invasion_class:
            mock_invasion_system = Mock()
            mock_invasion_class.return_value = mock_invasion_system

            # Mock the ground combat resolution to return no combat
            mock_invasion_system.resolve_ground_combat.return_value = {
                "combat_resolved": False,
                "reason": "no_opposing_forces",
            }

            # Execute tactical action
            results = coordinator.validate_and_execute_tactical_action(
                active_system=active_system,
                player="active_player",
                galaxy=galaxy,
                movement_plan=MovementPlan(),
            )

            # Verify invasion system was created
            mock_invasion_class.assert_called_once()

            # Verify ground combat was still called (coordinator tries to resolve)
            mock_invasion_system.resolve_ground_combat.assert_called_once()

            # Verify results indicate no combat occurred
            assert results["ground_combat_resolved"] is False

    def test_no_ground_combat_when_no_planets_available(self) -> None:
        """Test that ground combat is not attempted when there are no planets (Rule 89.4c)."""
        # Create a system with ground forces but no planets
        active_system = System("active_system")

        # No planets
        active_system.planets = []

        # Add ground forces in space
        space_infantry = Unit(unit_type=UnitType.INFANTRY, owner="active_player")
        active_system.space_units = [space_infantry]

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
            results = coordinator.validate_and_execute_tactical_action(
                active_system=active_system,
                player="active_player",
                galaxy=galaxy,
                movement_plan=MovementPlan(),
            )

            # Verify invasion system was NOT created or called
            mock_invasion_class.assert_not_called()
            mock_invasion_system.resolve_ground_combat.assert_not_called()

            # Verify results indicate no ground combat
            assert results["ground_combat_resolved"] is False

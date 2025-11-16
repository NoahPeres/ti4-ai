"""Test for Rule 89.4a: Bombardment abilities execution during invasion step."""

from unittest.mock import Mock, patch

from ti4.actions.movement_engine import MovementPlan
from ti4.core.constants import UnitType
from ti4.core.system import System
from ti4.core.tactical_action_coordinator import TacticalActionCoordinator
from ti4.core.unit import Unit
from ti4.core.unit_stats import UnitStats


class TestRule89_4a_BombardmentExecution:
    """Test Rule 89.4a: Bombardment abilities should be executed during invasion step."""

    def test_bombardment_should_execute_when_possible(self) -> None:
        """Test that bombardment is executed when bombardment-capable ships are present (Rule 89.4a)."""
        # Create a system with a planet and bombardment-capable ships
        active_system = System("active_system")

        # Add a planet with enemy ground forces
        from ti4.core.planet import Planet

        planet = Planet("test_planet", resources=1, influence=1)
        planet.units = [Unit(unit_type=UnitType.INFANTRY, owner="enemy_player")]
        active_system.planets = [planet]

        # Add bombardment-capable ship (War Sun) in space
        war_sun = Unit(unit_type=UnitType.WAR_SUN, owner="active_player")
        # Mock get_stats to return a UnitStats with bombardment=True
        with patch.object(
            war_sun,
            "get_stats",
            return_value=UnitStats(
                bombardment=True, bombardment_value=3, bombardment_dice=1
            ),
        ):
            active_system.space_units = [war_sun]
            # Create a simple galaxy for the test
            from ti4.core.galaxy import Galaxy

            galaxy = Galaxy()
            # Create tactical action coordinator
            coordinator = TacticalActionCoordinator()
            # Mock the bombardment system to verify it's called
            with patch(
                "ti4.core.tactical_action_coordinator.BombardmentSystem"
            ) as mock_bombardment_class:
                mock_bombardment_system = Mock()
                mock_bombardment_class.return_value = mock_bombardment_system
                # Execute tactical action
                coordinator.validate_and_execute_tactical_action(
                    active_system=active_system,
                    player="active_player",
                    galaxy=galaxy,
                    movement_plan=MovementPlan(),
                )
                # Verify bombardment system was created and called
                mock_bombardment_class.assert_called_once()
                # Verify execute_bombardment was called with correct parameters
                expected_planet_targets = {
                    "test_planet": [war_sun]  # War Sun should target the planet
                }
                mock_bombardment_system.execute_bombardment.assert_called_once_with(
                    system=active_system,
                    attacking_player="active_player",
                    planet_targets=expected_planet_targets,
                    player_faction=None,
                    player_technologies=None,
                )
        active_system.space_units = [war_sun]

        # Create a simple galaxy for the test
        from ti4.core.galaxy import Galaxy

        galaxy = Galaxy()

        # Create tactical action coordinator
        coordinator = TacticalActionCoordinator()

        # Mock the bombardment system to verify it's called
        with patch(
            "ti4.core.tactical_action_coordinator.BombardmentSystem"
        ) as mock_bombardment_class:
            mock_bombardment_system = Mock()
            mock_bombardment_class.return_value = mock_bombardment_system

            # Execute tactical action
            coordinator.validate_and_execute_tactical_action(
                active_system=active_system,
                player="active_player",
                galaxy=galaxy,
                movement_plan=MovementPlan(),
            )

            # Verify bombardment system was created and called
            mock_bombardment_class.assert_called_once()

            # Verify execute_bombardment was called with correct parameters
            expected_planet_targets = {
                "test_planet": [war_sun]  # War Sun should target the planet
            }
            mock_bombardment_system.execute_bombardment.assert_called_once_with(
                system=active_system,
                attacking_player="active_player",
                planet_targets=expected_planet_targets,
                player_faction=None,
                player_technologies=None,
            )

    def test_bombardment_not_executed_when_no_bombardment_ships(self) -> None:
        """Test that bombardment is not executed when no bombardment-capable ships are present."""
        # Create a system with a planet but no bombardment-capable ships
        active_system = System("active_system")

        # Add a planet with enemy ground forces
        from ti4.core.planet import Planet

        planet = Planet("test_planet", resources=1, influence=1)
        planet.units = [Unit(unit_type=UnitType.INFANTRY, owner="enemy_player")]
        active_system.planets = [planet]

        # Add non-bombardment ship (Carrier) in space
        carrier = Unit(unit_type=UnitType.CARRIER, owner="active_player")
        active_system.space_units = [carrier]

        # Create a simple galaxy for the test
        from ti4.core.galaxy import Galaxy

        galaxy = Galaxy()

        # Create tactical action coordinator
        coordinator = TacticalActionCoordinator()

        # Mock the bombardment system to verify it's NOT called
        with patch("ti4.core.bombardment.BombardmentSystem") as mock_bombardment_class:
            mock_bombardment_system = Mock()
            mock_bombardment_class.return_value = mock_bombardment_system

            # Execute tactical action
            coordinator.validate_and_execute_tactical_action(
                active_system=active_system,
                player="active_player",
                galaxy=galaxy,
                movement_plan=MovementPlan(),
            )

            # Verify bombardment system was NOT created or called
            mock_bombardment_class.assert_not_called()
            mock_bombardment_system.execute_bombardment.assert_not_called()

    def test_bombardment_not_executed_when_no_planets(self) -> None:
        """Test that bombardment is not executed when there are no planets to bombard."""
        # Create a system with bombardment-capable ships but no planets
        active_system = System("active_system")

        # No planets
        active_system.planets = []

        # Add bombardment-capable ship (War Sun) in space
        war_sun = Unit(unit_type=UnitType.WAR_SUN, owner="active_player")
        active_system.space_units = [war_sun]

        # Create a simple galaxy for the test
        from ti4.core.galaxy import Galaxy

        galaxy = Galaxy()

        # Create tactical action coordinator
        coordinator = TacticalActionCoordinator()

        # Mock the bombardment system to verify it's NOT called
        with patch("ti4.core.bombardment.BombardmentSystem") as mock_bombardment_class:
            mock_bombardment_system = Mock()
            mock_bombardment_class.return_value = mock_bombardment_system

            # Execute tactical action
            coordinator.validate_and_execute_tactical_action(
                active_system=active_system,
                player="active_player",
                galaxy=galaxy,
                movement_plan=MovementPlan(),
            )

            # Verify bombardment system was NOT created or called
            mock_bombardment_class.assert_not_called()
            mock_bombardment_system.execute_bombardment.assert_not_called()

"""Integration tests demonstrating the refactored TI4 system."""

from typing import Any, Optional

from src.ti4.core.combat import CombatDetector, CombatInitiator
from src.ti4.core.fleet import Fleet, FleetCapacityValidator
from src.ti4.core.galaxy import Galaxy
from src.ti4.core.hex_coordinate import HexCoordinate
from src.ti4.core.movement import MovementOperation, MovementValidator
from src.ti4.core.player import Player
from src.ti4.core.system import System
from src.ti4.core.unit import Unit
from src.ti4.core.unit_stats import UnitStats, UnitStatsProvider


class TestTI4Integration:
    def debug_test_failure(
        self, test_name: str, expected: Any, actual: Any, context: Optional[dict[Any, Any]] = None
    ) -> None:
        """Helper method to provide debugging output for failed test scenarios."""
        print(f"\n=== DEBUG INFO FOR FAILED TEST: {test_name} ===")
        print(f"Expected: {expected}")
        print(f"Actual: {actual}")
        if context:
            print("Context:")
            for key, value in context.items():
                print(f"  {key}: {value}")
        print("=" * 50)

    def test_complete_game_scenario(self):
        """Test a complete scenario using all refactored systems."""
        # Setup game with players
        player1 = Player(id="player1", faction="sol")
        player2 = Player(id="player2", faction="hacan")

        # Setup galaxy
        galaxy = Galaxy()
        system1 = System(system_id="system1")
        system2 = System(system_id="system2")

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)  # Adjacent

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        # Create units with proper stats
        sol_cruiser = Unit(
            unit_type="cruiser", owner=player1.id, faction=player1.faction
        )
        hacan_carrier = Unit(
            unit_type="carrier", owner=player2.id, faction=player2.faction
        )
        hacan_fighter = Unit(
            unit_type="fighter", owner=player2.id, faction=player2.faction
        )

        # Verify unit stats
        assert sol_cruiser.get_capacity() == 0  # Base cruiser has no capacity
        assert sol_cruiser.get_movement() == 2
        assert hacan_carrier.get_capacity() == 4
        assert hacan_fighter.get_capacity() == 0

        # Create fleets
        sol_fleet = Fleet(owner=player1.id, system_id="system1")
        hacan_fleet = Fleet(owner=player2.id, system_id="system2")

        sol_fleet.add_unit(sol_cruiser)
        hacan_fleet.add_unit(hacan_carrier)
        hacan_fleet.add_unit(hacan_fighter)

        # Validate fleet capacity
        validator = FleetCapacityValidator()
        assert validator.is_fleet_capacity_valid(sol_fleet) is True
        assert (
            validator.is_fleet_capacity_valid(hacan_fleet) is True
        )  # Fighter fits in carrier

        # Place units in systems
        system1.place_unit_in_space(sol_cruiser)
        system2.place_unit_in_space(hacan_carrier)
        system2.place_unit_in_space(hacan_fighter)

        # Test movement
        movement_validator = MovementValidator(galaxy)
        movement = MovementOperation(
            unit=sol_cruiser,
            from_system_id="system1",
            to_system_id="system2",
            player_id=player1.id,
        )

        # Movement should be valid (adjacent systems, cruiser has movement 2)
        assert movement_validator.is_valid_movement(movement) is True

        # Execute movement (sol cruiser moves to system2)
        system1.remove_unit_from_space(sol_cruiser)
        system2.place_unit_in_space(sol_cruiser)

        # Now both players have units in system2 - combat should be detected
        combat_detector = CombatDetector()
        assert combat_detector.should_initiate_combat(system2) is True

        # Get combat participants
        combat_initiator = CombatInitiator()
        participants = combat_initiator.get_combat_participants(system2)

        assert len(participants) == 2
        assert player1.id in participants
        assert player2.id in participants
        assert len(participants[player1.id]) == 1  # Sol cruiser
        assert len(participants[player2.id]) == 2  # Hacan carrier + fighter

    def test_technology_upgrade_scenario(self):
        """Test scenario with technology upgrades."""
        # Create stats provider with technology
        stats_provider = UnitStatsProvider()

        # Register Cruiser II technology
        stats_provider.register_technology_modifier(
            "cruiser_ii", "cruiser", UnitStats(capacity=1, combat_value=6)
        )

        # Create base cruiser
        base_cruiser = Unit(unit_type="cruiser", owner="player1")
        assert base_cruiser.get_capacity() == 0
        assert base_cruiser.get_combat_value() == 7

        # Create upgraded cruiser
        upgraded_cruiser = Unit(
            unit_type="cruiser",
            owner="player1",
            technologies={"cruiser_ii"},
            stats_provider=stats_provider,
        )

        # Verify upgrade effects
        assert upgraded_cruiser.get_capacity() == 1  # Now has capacity
        assert upgraded_cruiser.get_combat_value() == 6  # Better combat

        # Test fleet with upgraded cruiser
        fleet = Fleet(owner="player1", system_id="system1")
        fleet.add_unit(upgraded_cruiser)

        # Add infantry that can be carried
        infantry = Unit(unit_type="infantry", owner="player1")
        fleet.add_unit(infantry)

        # Fleet should be valid (infantry fits in cruiser capacity)
        validator = FleetCapacityValidator()
        assert validator.is_fleet_capacity_valid(fleet) is True

    def test_faction_specific_abilities(self):
        """Test faction-specific unit modifications."""
        # Create stats provider with faction modifiers
        stats_provider = UnitStatsProvider()

        # Sol faction gets better infantry (Spec Ops)
        stats_provider.register_faction_modifier(
            "sol", "infantry", UnitStats(combat_value=7, movement=0, capacity=0, cost=0)
        )

        # Create Sol infantry (Spec Ops)
        sol_infantry = Unit(
            unit_type="infantry",
            owner="player1",
            faction="sol",
            stats_provider=stats_provider,
        )

        # Create regular infantry
        regular_infantry = Unit(unit_type="infantry", owner="player2")

        # Verify faction bonus
        assert sol_infantry.get_combat_value() == 7  # Improved (Spec Ops)
        assert regular_infantry.get_combat_value() == 8  # Default

        # Both should have same movement and capacity
        assert sol_infantry.get_movement() == regular_infantry.get_movement()
        assert sol_infantry.get_capacity() == regular_infantry.get_capacity()

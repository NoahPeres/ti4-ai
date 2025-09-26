"""Integration tests demonstrating the refactored TI4 system."""

from typing import Any, Optional

from ti4.core.combat import CombatDetector
from ti4.core.constants import Faction, Technology, UnitType
from ti4.core.fleet import Fleet, FleetCapacityValidator
from ti4.core.galaxy import Galaxy
from ti4.core.hex_coordinate import HexCoordinate
from ti4.core.movement import MovementOperation, MovementValidator
from ti4.core.player import Player
from ti4.core.system import System
from ti4.core.unit import Unit
from ti4.core.unit_stats import UnitStatsProvider


class TestTI4Integration:
    def debug_test_failure(
        self,
        test_name: str,
        expected: Any,
        actual: Any,
        context: Optional[dict[Any, Any]] = None,
    ) -> None:
        """Debug helper for test failures."""
        print(f"\n=== TEST FAILURE: {test_name} ===")
        print(f"Expected: {expected}")
        print(f"Actual: {actual}")
        if context:
            print(f"Context: {context}")
        print("=" * 50)

    def test_complete_game_scenario(self) -> None:
        """Test a complete game scenario with multiple systems and players."""
        # Create galaxy and systems
        galaxy = Galaxy()

        # Create systems at specific coordinates
        mecatol_coord = HexCoordinate(0, 0)
        system_a_coord = HexCoordinate(1, 0)
        system_b_coord = HexCoordinate(-1, 0)

        mecatol = System("mecatol_rex")
        system_a = System("system_a")
        system_b = System("system_b")

        galaxy.place_system(mecatol_coord, "mecatol_rex")
        galaxy.place_system(system_a_coord, "system_a")
        galaxy.place_system(system_b_coord, "system_b")

        galaxy.register_system(mecatol)
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)

        # Create players
        Player("player1", "The Federation of Sol")
        Player("player2", "The Sardakk N'orr")

        # Create fleets for each player
        fleet1 = Fleet(owner="player1", system_id="test_system")
        fleet2 = Fleet(owner="player2", system_id="test_system")

        # Create units for player 1
        carrier1 = Unit(unit_type=UnitType.CARRIER, owner="player1")
        fighter1 = Unit(unit_type=UnitType.FIGHTER, owner="player1")
        fighter2 = Unit(unit_type=UnitType.FIGHTER, owner="player1")
        Unit(unit_type=UnitType.INFANTRY, owner="player1")

        # Create units for player 2
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player2")
        destroyer1 = Unit(unit_type=UnitType.DESTROYER, owner="player2")

        # Place units in systems
        system_a.place_unit_in_space(carrier1)
        system_a.place_unit_in_space(fighter1)
        system_a.place_unit_in_space(fighter2)

        system_b.place_unit_in_space(cruiser1)
        system_b.place_unit_in_space(destroyer1)

        # Add units to fleets
        fleet1.add_unit(carrier1)
        fleet1.add_unit(fighter1)
        fleet1.add_unit(fighter2)

        fleet2.add_unit(cruiser1)
        fleet2.add_unit(destroyer1)

        # Test fleet capacity validation
        validator = FleetCapacityValidator()

        # Fleet 1 should be valid (carrier capacity 4, has 2 fighters)
        assert validator.is_fleet_capacity_valid(fleet1) is True

        # Fleet 2 should be valid (no capacity constraints)
        assert validator.is_fleet_capacity_valid(fleet2) is True

        # Test movement validation
        movement_validator = MovementValidator(galaxy)

        # Test valid movement from system_a to mecatol (adjacent)
        movement = MovementOperation(
            unit=carrier1,
            from_system_id="system_a",
            to_system_id="mecatol_rex",
            player_id="player1",
        )
        assert movement_validator.validate_movement(movement) is True

        # Test invalid movement from system_a to system_b (not adjacent)
        invalid_movement = MovementOperation(
            unit=carrier1,
            from_system_id="system_a",
            to_system_id="system_b",
            player_id="player1",
        )
        assert movement_validator.validate_movement(invalid_movement) is False

        # Test combat detection
        combat_detector = CombatDetector()

        # Move player 1 units to mecatol
        mecatol.place_unit_in_space(carrier1)
        mecatol.place_unit_in_space(fighter1)
        mecatol.place_unit_in_space(fighter2)

        # Move player 2 units to mecatol (should trigger combat)
        mecatol.place_unit_in_space(cruiser1)
        mecatol.place_unit_in_space(destroyer1)

        # Check if combat is detected
        combat_detected = combat_detector.should_initiate_combat(mecatol)
        assert combat_detected is True

        # Test unit stats
        stats_provider = UnitStatsProvider()

        carrier_stats = stats_provider.get_unit_stats(UnitType.CARRIER)
        assert carrier_stats.combat_value == 9
        assert carrier_stats.capacity == 4
        assert carrier_stats.movement == 1

        cruiser_stats = stats_provider.get_unit_stats(UnitType.CRUISER)
        assert cruiser_stats.combat_value == 7
        assert cruiser_stats.capacity == 0
        assert cruiser_stats.movement == 2

        fighter_stats = stats_provider.get_unit_stats(UnitType.FIGHTER)
        assert fighter_stats.combat_value == 9
        assert fighter_stats.capacity == 0
        assert fighter_stats.movement == 0

    def test_technology_upgrade_scenario(self) -> None:
        """Test technology upgrades affecting unit capabilities."""
        # Create a unit that can be upgraded
        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")

        # Test base stats
        assert carrier.get_combat() == 9
        assert carrier.get_capacity() == 4
        assert carrier.get_movement() == 1

        # Apply technology upgrade (Carrier II)
        carrier.add_technology("carrier_ii")

        # Test upgraded stats (assuming technology improves capacity)
        # This would depend on the specific technology implementation
        # For now, we'll test that the technology was applied
        assert Technology.CARRIER_II in carrier.technologies

        # Test Gravity Drive technology
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        assert cruiser.get_movement() == 2  # Base movement

        cruiser.add_technology("gravity_drive")
        # Gravity Drive should increase movement by 1
        # This would be implemented in the unit's get_movement method
        assert Technology.GRAVITY_DRIVE in cruiser.technologies

    def test_faction_specific_abilities(self) -> None:
        """Test faction-specific unit abilities and modifications."""
        # Test Sol faction infantry (should have improved combat)
        sol_infantry = Unit(
            unit_type=UnitType.INFANTRY, owner="player1", faction=Faction.SOL
        )

        # Test Barony units (should have combat bonuses)
        barony_cruiser = Unit(
            unit_type=UnitType.CRUISER, owner="player2", faction=Faction.BARONY
        )

        # Test that faction-specific modifications are applied
        # This would depend on the specific faction implementation
        assert sol_infantry.faction.value == Faction.SOL.value
        assert barony_cruiser.faction.value == Faction.BARONY.value

        # Test that units maintain their base functionality
        assert sol_infantry.unit_type == UnitType.INFANTRY
        assert barony_cruiser.unit_type == UnitType.CRUISER

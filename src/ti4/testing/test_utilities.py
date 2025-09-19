"""Test utilities for common testing patterns."""

from src.ti4.core.constants import Faction, UnitType
from src.ti4.core.game_state import GameState
from src.ti4.core.system import System
from src.ti4.core.unit import Unit

from .scenario_builder import GameScenarioBuilder


class TestUtilities:
    """Utility methods for common test patterns."""

    @staticmethod
    def create_simple_2_player_game() -> GameState:
        """Create a simple 2-player game for basic testing.

        Returns:
            GameState with minimal setup for testing
        """
        return GameScenarioBuilder.create_basic_2_player_game()

    @staticmethod
    def create_game_with_adjacent_systems() -> GameState:
        """Create a game with units in adjacent systems for movement testing.

        Returns:
            GameState with units positioned for movement tests
        """
        return (
            GameScenarioBuilder()
            .with_players(("player1", Faction.SOL), ("player2", Faction.XXCHA))
            .with_galaxy("standard_6p")
            .with_units(
                [
                    ("player1", "cruiser", "system_a", "space"),
                    ("player2", "destroyer", "system_b", "space"),
                ]
            )
            .build()
        )

    @staticmethod
    def create_fleet_capacity_test_scenario() -> GameState:
        """Create a scenario for testing fleet capacity rules.

        Returns:
            GameState with units that test capacity limits
        """
        return (
            GameScenarioBuilder()
            .with_players(("player1", Faction.SOL))
            .with_galaxy("standard_6p")
            .with_units(
                [
                    ("player1", "carrier", "test_system", "space"),
                    ("player1", "fighter", "test_system", "space"),
                    ("player1", "fighter", "test_system", "space"),
                    ("player1", "fighter", "test_system", "space"),
                    ("player1", "fighter", "test_system", "space"),
                    (
                        "player1",
                        "infantry",
                        "test_system",
                        "space",
                    ),  # Should fit in carrier
                ]
            )
            .build()
        )

    @staticmethod
    def verify_unit_placement(
        game_state: GameState, expected_placements: dict[str, list[str]]
    ) -> bool:
        """Verify that units are placed as expected.

        Args:
            game_state: The game state to verify
            expected_placements: Dict mapping system_id to list of expected unit types

        Returns:
            True if all placements match expectations
        """
        for system_id, expected_units in expected_placements.items():
            if system_id not in game_state.systems:
                return False

            system = game_state.systems[system_id]
            # Convert enum values to strings for comparison
            actual_units = [unit.unit_type.value for unit in system.space_units]

            if sorted(actual_units) != sorted(expected_units):
                return False

        return True

    @staticmethod
    def count_units_by_owner(system: System) -> dict[str, int]:
        """Count units in a system by owner.

        Args:
            system: The system to analyze

        Returns:
            Dict mapping owner_id to unit count
        """
        counts: dict[str, int] = {}
        for unit in system.space_units:
            counts[unit.owner] = counts.get(unit.owner, 0) + 1
        return counts

    @staticmethod
    def get_units_by_type(system: System, unit_type: UnitType) -> list[Unit]:
        """Get all units of a specific type from a system.

        Args:
            system: The system to search
            unit_type: The type of unit to find

        Returns:
            List of units matching the type
        """
        return [
            unit for unit in system.space_units if unit.unit_type == unit_type
        ]

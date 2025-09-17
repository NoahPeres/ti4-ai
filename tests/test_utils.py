"""Test utilities for TI4 game framework tests."""

from typing import Optional

from src.ti4.core.constants import FactionConstants, UnitType
from src.ti4.core.fleet import Fleet
from src.ti4.core.galaxy import Galaxy
from src.ti4.core.hex_coordinate import HexCoordinate
from src.ti4.core.player import Player
from src.ti4.core.system import System
from src.ti4.core.unit import Unit
from src.ti4.core.unit_stats import UnitStatsProvider


class TestDataFactory:
    """Factory for creating test data objects."""

    @staticmethod
    def create_player(
        player_id: str = "test_player", faction: str = FactionConstants.SOL
    ) -> Player:
        """Create a test player."""
        return Player(id=player_id, faction=faction)

    @staticmethod
    def create_unit(
        unit_type: str = UnitType.CRUISER.value,
        owner: str = "test_player",
        faction: Optional[str] = None,
        technologies: Optional[set[str]] = None,
    ) -> Unit:
        """Create a test unit."""
        return Unit(
            unit_type=unit_type,
            owner=owner,
            faction=faction,
            technologies=technologies or set(),
        )

    @staticmethod
    def create_fleet(
        owner: str = "test_player",
        system_id: str = "test_system",
        units: Optional[list[Unit]] = None,
    ) -> Fleet:
        """Create a test fleet."""
        fleet = Fleet(owner=owner, system_id=system_id)
        for unit in units or []:
            fleet.add_unit(unit)
        return fleet

    @staticmethod
    def create_system(system_id: str = "test_system") -> System:
        """Create a test system."""
        return System(system_id=system_id)

    @staticmethod
    def create_galaxy_with_systems(
        system_configs: list[tuple[str, int, int]],
    ) -> Galaxy:
        """Create a galaxy with systems at specified coordinates.

        Args:
            system_configs: List of (system_id, q, r) tuples
        """
        galaxy = Galaxy()
        for system_id, q, r in system_configs:
            coord = HexCoordinate(q, r)
            galaxy.place_system(coord, system_id)
        return galaxy

    @staticmethod
    def create_adjacent_systems() -> tuple[Galaxy, System, System]:
        """Create two adjacent systems in a galaxy."""
        galaxy = Galaxy()
        system1 = System("system1")
        system2 = System("system2")

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)  # Adjacent

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")

        return galaxy, system1, system2


class TestAssertions:
    """Custom assertions for TI4 tests."""

    @staticmethod
    def assert_fleet_capacity_valid(fleet: Fleet) -> None:
        """Assert that a fleet's capacity is valid."""
        carried = fleet.get_carried_units_count()
        capacity = fleet.get_total_capacity()
        assert carried <= capacity, f"Fleet capacity exceeded: {carried} > {capacity}"

    @staticmethod
    def assert_units_in_system(system: System, expected_units: list[Unit]) -> None:
        """Assert that specific units are in a system."""
        for unit in expected_units:
            assert unit in system.space_units, (
                f"Unit {unit.unit_type} not found in system"
            )

    @staticmethod
    def assert_combat_participants(
        participants: dict, expected_players: list[str]
    ) -> None:
        """Assert that combat participants match expected players."""
        assert set(participants.keys()) == set(expected_players), (
            f"Participants {list(participants.keys())} != expected {expected_players}"
        )


class MockStatsProvider(UnitStatsProvider):
    """Mock stats provider for testing."""

    def __init__(self, custom_stats: Optional[dict] = None):
        """Initialize with optional custom stats."""
        super().__init__()
        self.custom_stats = custom_stats or {}

    def get_unit_stats(self, unit_type: str, faction=None, technologies=None):
        """Get stats, using custom stats if provided."""
        if unit_type in self.custom_stats:
            return self.custom_stats[unit_type]
        return super().get_unit_stats(unit_type, faction, technologies)

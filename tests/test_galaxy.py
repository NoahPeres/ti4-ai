"""Tests for galaxy structure."""

from ti4.core.galaxy import Galaxy
from ti4.core.hex_coordinate import HexCoordinate


class TestGalaxy:
    def test_galaxy_creation(self) -> None:
        """Test that a galaxy can be created."""
        galaxy = Galaxy()
        assert galaxy is not None

    def test_galaxy_has_systems_dict(self) -> None:
        """Test that galaxy has a system_coordinates dictionary."""
        galaxy = Galaxy()
        assert hasattr(galaxy, "system_coordinates")
        assert isinstance(galaxy.system_coordinates, dict)

    def test_place_system_at_coordinate(self) -> None:
        """Test placing a system at a hex coordinate."""
        galaxy = Galaxy()
        coord = HexCoordinate(q=0, r=0)
        system_id = "test_system"
        galaxy.place_system(coord, system_id)
        assert system_id in galaxy.system_coordinates
        assert galaxy.system_coordinates[system_id] == coord

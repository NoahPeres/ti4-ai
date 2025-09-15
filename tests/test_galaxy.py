"""Tests for galaxy structure."""

import pytest
from src.ti4.core.galaxy import Galaxy
from src.ti4.core.hex_coordinate import HexCoordinate


class TestGalaxy:
    def test_galaxy_creation(self):
        """Test that a galaxy can be created."""
        galaxy = Galaxy()
        assert galaxy is not None

    def test_galaxy_has_systems_dict(self):
        """Test that galaxy has a systems dictionary."""
        galaxy = Galaxy()
        assert hasattr(galaxy, "systems")
        assert isinstance(galaxy.systems, dict)

    def test_place_system_at_coordinate(self):
        """Test placing a system at a hex coordinate."""
        galaxy = Galaxy()
        coord = HexCoordinate(q=0, r=0)
        system_id = "test_system"
        galaxy.place_system(coord, system_id)
        assert coord in galaxy.systems
        assert galaxy.systems[coord] == system_id

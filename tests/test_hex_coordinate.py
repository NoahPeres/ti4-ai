"""Tests for hex coordinate system."""

import pytest
from src.ti4.core.hex_coordinate import HexCoordinate


class TestHexCoordinate:
    def test_hex_coordinate_creation(self):
        """Test that a hex coordinate can be created with q and r values."""
        coord = HexCoordinate(q=1, r=2)
        assert coord.q == 1
        assert coord.r == 2
    
    def test_distance_calculation(self):
        """Test distance calculation between two hex coordinates."""
        coord1 = HexCoordinate(q=0, r=0)
        coord2 = HexCoordinate(q=1, r=1)
        assert coord1.distance_to(coord2) == 2
    
    def test_get_neighbors(self):
        """Test getting all adjacent hex coordinates."""
        coord = HexCoordinate(q=0, r=0)
        neighbors = coord.get_neighbors()
        assert len(neighbors) == 6
        # Check that all neighbors are distance 1 away
        for neighbor in neighbors:
            assert coord.distance_to(neighbor) == 1
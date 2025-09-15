"""Tests for unit structure."""

import pytest
from src.ti4.core.unit import Unit


class TestUnit:
    def test_unit_creation(self):
        """Test that a unit can be created with type and owner."""
        unit = Unit(unit_type="fighter", owner="player1")
        assert unit.unit_type == "fighter"
        assert unit.owner == "player1"
"""Tests for planet structure."""

import pytest
from src.ti4.core.planet import Planet
from src.ti4.core.unit import Unit


class TestPlanet:
    def test_planet_creation(self):
        """Test that a planet can be created with basic properties."""
        planet = Planet(name="Test Planet", resources=2, influence=1)
        assert planet.name == "Test Planet"
        assert planet.resources == 2
        assert planet.influence == 1
    
    def test_planet_has_control_tracking(self):
        """Test that planet has control tracking."""
        planet = Planet(name="Test Planet", resources=2, influence=1)
        assert hasattr(planet, 'controlled_by')
        assert planet.controlled_by is None
    
    def test_planet_control_changes(self):
        """Test that planet control can be changed."""
        planet = Planet(name="Test Planet", resources=2, influence=1)
        player_id = "player1"
        planet.set_control(player_id)
        assert planet.controlled_by == player_id
    
    def test_planet_has_units_list(self):
        """Test that planet has a units list for ground forces."""
        planet = Planet(name="Test Planet", resources=2, influence=1)
        assert hasattr(planet, 'units')
        assert isinstance(planet.units, list)
        assert len(planet.units) == 0
    
    def test_place_unit_on_planet(self):
        """Test placing a ground unit on a planet."""
        planet = Planet(name="Test Planet", resources=2, influence=1)
        unit = Unit(unit_type="infantry", owner="player1")
        planet.place_unit(unit)
        assert unit in planet.units
        assert len(planet.units) == 1
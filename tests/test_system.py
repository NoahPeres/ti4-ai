"""Tests for system structure."""

import pytest
from src.ti4.core.system import System
from src.ti4.core.planet import Planet
from src.ti4.core.unit import Unit


class TestSystem:
    def test_system_creation(self):
        """Test that a system can be created with an ID."""
        system = System(system_id="test_system")
        assert system.system_id == "test_system"
    
    def test_system_has_planets_list(self):
        """Test that system has a planets list."""
        system = System(system_id="test_system")
        assert hasattr(system, 'planets')
        assert isinstance(system.planets, list)
    
    def test_system_has_space_units_tracking(self):
        """Test that system has space unit tracking."""
        system = System(system_id="test_system")
        assert hasattr(system, 'space_units')
        assert isinstance(system.space_units, list)
    
    def test_place_unit_in_space(self):
        """Test placing a unit in the space area of a system."""
        system = System(system_id="test_system")
        unit = Unit(unit_type="fighter", owner="player1")
        system.place_unit_in_space(unit)
        assert unit in system.space_units
        assert len(system.space_units) == 1
    
    def test_remove_unit_from_space(self):
        """Test removing a unit from the space area of a system."""
        system = System(system_id="test_system")
        unit = Unit(unit_type="fighter", owner="player1")
        system.place_unit_in_space(unit)
        system.remove_unit_from_space(unit)
        assert unit not in system.space_units
        assert len(system.space_units) == 0
    
    def test_place_unit_on_planet_in_system(self):
        """Test placing a unit on a planet within a system."""
        system = System(system_id="test_system")
        planet = Planet(name="Test Planet", resources=2, influence=1)
        system.add_planet(planet)
        unit = Unit(unit_type="infantry", owner="player1")
        system.place_unit_on_planet(unit, "Test Planet")
        assert unit in planet.units
        assert len(planet.units) == 1
    
    def test_space_and_planet_units_are_separate(self):
        """Test that space units and planet units are tracked separately."""
        system = System(system_id="test_system")
        planet = Planet(name="Test Planet", resources=2, influence=1)
        system.add_planet(planet)
        
        # Place a space unit
        space_unit = Unit(unit_type="fighter", owner="player1")
        system.place_unit_in_space(space_unit)
        
        # Place a ground unit on planet
        ground_unit = Unit(unit_type="infantry", owner="player1")
        system.place_unit_on_planet(ground_unit, "Test Planet")
        
        # Verify they are tracked separately
        assert space_unit in system.space_units
        assert space_unit not in planet.units
        assert ground_unit in planet.units
        assert ground_unit not in system.space_units
        assert len(system.space_units) == 1
        assert len(planet.units) == 1
"""Tests for planet structure."""

from ti4.core.constants import UnitType
from ti4.core.planet import Planet
from ti4.core.unit import Unit


class TestPlanet:
    def test_planet_creation(self) -> None:
        """Test that a planet can be created with basic properties."""
        planet = Planet(name="Test Planet", resources=2, influence=1)
        assert planet.name == "Test Planet"
        assert planet.resources == 2
        assert planet.influence == 1

    def test_planet_has_control_tracking(self) -> None:
        """Test that planet tracks which player controls it."""
        planet = Planet(name="Test Planet", resources=2, influence=1)
        assert hasattr(planet, "controlled_by")
        assert planet.controlled_by is None  # Initially uncontrolled

    def test_planet_control_changes(self) -> None:
        """Test that planet control can be changed."""
        planet = Planet(name="Test Planet", resources=2, influence=1)
        planet.controlled_by = "player1"
        assert planet.controlled_by == "player1"

    def test_planet_has_units_list(self) -> None:
        """Test that planet has a units list for ground forces."""
        planet = Planet(name="Test Planet", resources=2, influence=1)
        assert hasattr(planet, "units")
        assert isinstance(planet.units, list)

    def test_place_unit_on_planet(self) -> None:
        """Test placing a ground unit on a planet."""
        planet = Planet(name="Test Planet", resources=2, influence=1)
        unit = Unit(unit_type=UnitType.INFANTRY, owner="player1")

        planet.place_unit(unit)
        assert unit in planet.units

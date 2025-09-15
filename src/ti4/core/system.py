"""System structure for TI4 game board."""

from typing import TYPE_CHECKING, Optional

from .unit import Unit

if TYPE_CHECKING:
    from .planet import Planet


class System:
    """Represents a star system containing planets."""

    def __init__(self, system_id: str):
        self.system_id = system_id
        self.planets: list[Planet] = []
        self.space_units: list[Unit] = []  # Units in the space area of the system

    def place_unit_in_space(self, unit: Unit) -> None:
        """Place a unit in the space area of this system."""
        self.space_units.append(unit)

    def remove_unit_from_space(self, unit: Unit) -> None:
        """Remove a unit from the space area of this system."""
        self.space_units.remove(unit)

    def place_unit_on_planet(self, unit: Unit, planet_name: str) -> None:
        """Place a unit on a specific planet in this system."""
        planet = self.get_planet_by_name(planet_name)
        if planet:
            planet.place_unit(unit)

    def remove_unit_from_planet(self, unit: Unit, planet_name: str) -> None:
        """Remove a unit from a specific planet in this system."""
        planet = self.get_planet_by_name(planet_name)
        if planet:
            planet.remove_unit(unit)

    def get_planet_by_name(self, planet_name: str) -> Optional["Planet"]:
        """Get a planet by name from this system."""
        for planet in self.planets:
            if planet.name == planet_name:
                return planet
        return None

    def add_planet(self, planet: "Planet") -> None:
        """Add a planet to this system."""
        self.planets.append(planet)

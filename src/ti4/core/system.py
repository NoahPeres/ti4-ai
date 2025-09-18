"""System structure for TI4 game board."""

from typing import TYPE_CHECKING, Optional

from .unit import Unit

if TYPE_CHECKING:
    from .fleet import Fleet
    from .planet import Planet


class System:
    """Represents a star system containing planets."""

    def __init__(self, system_id: str) -> None:
        self.system_id = system_id
        self.planets: list[Planet] = []
        self.space_units: list[Unit] = []  # Units in the space area of the system
        self.wormholes: list[str] = []  # List of wormhole types in this system
        self.fleets: list[Fleet] = []  # Fleets in this system

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

    def add_fleet(self, fleet: "Fleet") -> None:
        """Add a fleet to this system."""
        self.fleets.append(fleet)

    def add_wormhole(self, wormhole_type: str) -> None:
        """
        Add a wormhole of the specified type to this system.

        Implements support for LRR 101 wormhole adjacency rules.
        Valid wormhole types: alpha, beta, gamma, delta

        Args:
            wormhole_type: Type of wormhole to add (alpha, beta, gamma, delta)

        Raises:
            ValueError: If wormhole_type is invalid
        """
        if not wormhole_type:
            raise ValueError("Wormhole type cannot be empty")

        valid_types = {"alpha", "beta", "gamma", "delta"}
        if wormhole_type not in valid_types:
            raise ValueError(
                f"Invalid wormhole type: {wormhole_type}. Valid types: {valid_types}"
            )

        # Avoid duplicates
        if wormhole_type not in self.wormholes:
            self.wormholes.append(wormhole_type)

    def has_wormhole(self, wormhole_type: str) -> bool:
        """
        Check if this system has a wormhole of the specified type.

        Args:
            wormhole_type: Type of wormhole to check for

        Returns:
            True if system contains the specified wormhole type, False otherwise
        """
        return wormhole_type in self.wormholes

    def get_wormhole_types(self) -> list[str]:
        """
        Get all wormhole types present in this system.

        Returns:
            List of wormhole types in this system (copy to prevent external modification)
        """
        return self.wormholes.copy()

    def remove_wormhole(self, wormhole_type: str) -> bool:
        """
        Remove a wormhole of the specified type from this system.

        Args:
            wormhole_type: Type of wormhole to remove

        Returns:
            True if wormhole was removed, False if it wasn't present
        """
        if wormhole_type in self.wormholes:
            self.wormholes.remove(wormhole_type)
            return True
        return False

    def get_units_in_space(self) -> list[Unit]:
        """Get all units in the space area of this system."""
        return self.space_units.copy()

    def get_units_on_planet(self, planet_name: str) -> list[Unit]:
        """Get all units on a specific planet in this system."""
        planet = self.get_planet_by_name(planet_name)
        if planet:
            return planet.units.copy()
        return []

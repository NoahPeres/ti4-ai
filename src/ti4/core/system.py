"""System structure for TI4 game board."""

from __future__ import annotations

from typing import TYPE_CHECKING

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
        self.command_tokens: dict[str, bool] = {}  # Player ID -> has command token

    def place_command_token(self, player_id: str) -> None:
        """Place a command token for a player in this system (Rule 20.4)."""
        self.command_tokens[player_id] = True

    def remove_command_token(self, player_id: str) -> None:
        """Remove a command token for a player from this system."""
        self.command_tokens.pop(player_id, None)

    def has_command_token(self, player_id: str) -> bool:
        """Check if a player has a command token in this system."""
        return self.command_tokens.get(player_id, False)

    def get_players_with_command_tokens(self) -> list[str]:
        """Get list of players who have command tokens in this system."""
        return [
            player_id
            for player_id, has_token in self.command_tokens.items()
            if has_token
        ]

    def has_enemy_ships(self, player_id: str) -> bool:
        """Check if this system contains enemy movement-blocking ships (Rule 58.4b).

        Fighters are intentionally excluded: they do not block movement.
        For combat detection, use the combat-related API instead.
        """
        from .constants import GameConstants

        # Use NON_FIGHTER_SHIP_TYPES for movement blocking rules
        ship_types = GameConstants.NON_FIGHTER_SHIP_TYPES

        for unit in self.space_units:
            if unit.owner != player_id and unit.unit_type in ship_types:
                return True
        return False

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

    def get_planet_by_name(self, planet_name: str) -> Planet | None:
        """Get a planet by name from this system."""
        for planet in self.planets:
            if planet.name == planet_name:
                return planet
        return None

    def add_planet(self, planet: Planet) -> None:
        """Add a planet to this system."""
        self.planets.append(planet)

    def add_fleet(self, fleet: Fleet) -> None:
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

    def get_ground_forces_on_planet(self, planet_name: str) -> list[Unit]:
        """Get all ground force units on a specific planet in this system."""
        from .constants import GameConstants

        planet = self.get_planet_by_name(planet_name)
        if planet:
            # Filter for ground force units (infantry, mechs, etc.)
            return [
                unit
                for unit in planet.units
                if unit.unit_type in GameConstants.GROUND_FORCE_TYPES
            ]
        return []

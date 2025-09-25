"""Galaxy structure for TI4 game board."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .hex_coordinate import HexCoordinate
from .system import System

if TYPE_CHECKING:
    from .planet import Planet
    from .unit import Unit


class Galaxy:
    """Represents the hex-based galaxy game board."""

    def __init__(self) -> None:
        """Initialize an empty galaxy."""
        self.system_coordinates: dict[str, HexCoordinate] = {}
        self.system_objects: dict[str, System] = {}
        self.hyperlane_connections: set[tuple[str, str]] = set()

    def place_system(self, coordinate: HexCoordinate, system_id: str) -> None:
        """Place a system at the given coordinate."""
        self.system_coordinates[system_id] = coordinate

    def register_system(self, system: System) -> None:
        """Register a system object in the galaxy."""
        self.system_objects[system.system_id] = system

    def get_system_coordinate(self, system_id: str) -> HexCoordinate | None:
        """Get the coordinate of a system by its ID."""
        return self.system_coordinates.get(system_id)

    def get_system(self, system_id: str) -> System | None:
        """Get a system object by its ID."""
        return self.system_objects.get(system_id)

    def are_systems_adjacent(self, system_id1: str, system_id2: str) -> bool:
        """
        Check if two systems are adjacent according to LRR Rules 6 and 101.

        Systems are adjacent if:
        1. They are physically adjacent (distance = 1)
        2. They share at least one wormhole type (Rule 101)

        Args:
            system_id1: ID of the first system
            system_id2: ID of the second system

        Returns:
            True if systems are adjacent, False otherwise
        """
        coord1 = self.get_system_coordinate(system_id1)
        coord2 = self.get_system_coordinate(system_id2)

        if coord1 is None or coord2 is None:
            return False

        # Check physical adjacency (Rule 6)
        if coord1.distance_to(coord2) == 1:
            return True

        # Check wormhole adjacency (Rule 101)
        if self._check_wormhole_adjacency(system_id1, system_id2):
            return True

        # Check for hyperlane adjacency
        if self._check_hyperlane_adjacency(system_id1, system_id2):
            return True

        return False

    def _check_wormhole_adjacency(self, system_id1: str, system_id2: str) -> bool:
        """
        Check if two systems are adjacent via wormholes (Rule 101).

        Systems are wormhole-adjacent if they share at least one wormhole type.
        This implements LRR 101: "A system that contains a wormhole is adjacent
        to all other systems that contain a wormhole of the same type."

        Args:
            system_id1: ID of the first system
            system_id2: ID of the second system

        Returns:
            True if systems share any wormhole type, False otherwise
        """
        system1 = self.get_system(system_id1)
        system2 = self.get_system(system_id2)

        if system1 is None or system2 is None:
            return False

        # Check if systems share any wormhole types
        return self._systems_share_wormhole_type(system1, system2)

    def _systems_share_wormhole_type(self, system1: System, system2: System) -> bool:
        """
        Check if two systems share at least one wormhole type.

        Args:
            system1: First system to check
            system2: Second system to check

        Returns:
            True if systems share any wormhole type, False otherwise
        """
        for wormhole_type in system1.wormholes:
            if system2.has_wormhole(wormhole_type):
                return True

        return False

    def _check_hyperlane_adjacency(self, system_id1: str, system_id2: str) -> bool:
        """
        Check if two systems are adjacent via hyperlanes (Rule 6.4).

        Systems are hyperlane-adjacent if they are connected by hyperlane tiles.
        This implements LRR 6.4: "Systems that are connected by lines drawn
        across one or more hyperlane tiles are adjacent for all purposes."

        Args:
            system_id1: ID of the first system
            system_id2: ID of the second system

        Returns:
            True if systems are connected by hyperlanes, False otherwise
        """
        # Check if there's a direct hyperlane connection
        connection1 = (system_id1, system_id2)
        connection2 = (system_id2, system_id1)

        return (
            connection1 in self.hyperlane_connections
            or connection2 in self.hyperlane_connections
        )

    def add_hyperlane_connection(self, system_id1: str, system_id2: str) -> None:
        """
        Add a hyperlane connection between two systems.

        Args:
            system_id1: ID of the first system
            system_id2: ID of the second system
        """
        # Store both directions for easier lookup
        self.hyperlane_connections.add((system_id1, system_id2))
        self.hyperlane_connections.add((system_id2, system_id1))

    def is_unit_adjacent_to_system(self, unit: Unit, target_system_id: str) -> bool:
        """
        Check if a unit is adjacent to a target system according to LRR Rule 6.2.

        A unit is adjacent to all system tiles that are adjacent to the system tile
        that contains that unit. A system is not adjacent to itself (Rule 6.2a).

        Args:
            unit: The unit to check adjacency for
            target_system_id: ID of the target system

        Returns:
            True if unit is adjacent to target system, False otherwise
        """
        # Find which system contains this unit
        containing_system_id = self._find_unit_system(unit)
        if containing_system_id is None:
            return False

        # Rule 6.2a: A system is not adjacent to itself
        if containing_system_id == target_system_id:
            return False

        # Check if the containing system is adjacent to the target system
        return self.are_systems_adjacent(containing_system_id, target_system_id)

    def is_planet_adjacent_to_system(
        self, planet: Planet, target_system_id: str
    ) -> bool:
        """
        Check if a planet is adjacent to a target system according to LRR Rules 6.2 and 6.3.

        Rule 6.2: A planet is adjacent to all system tiles that are adjacent to the
        system tile that contains that planet.
        Rule 6.3: A planet is treated as being adjacent to the system that contains that planet.

        Args:
            planet: The planet to check adjacency for
            target_system_id: ID of the target system

        Returns:
            True if planet is adjacent to target system, False otherwise
        """
        # Find which system contains this planet
        containing_system_id = self._find_planet_system(planet)
        if containing_system_id is None:
            return False

        # Rule 6.3: Planet is adjacent to its containing system
        if containing_system_id == target_system_id:
            return True

        # Rule 6.2: Planet is adjacent to systems adjacent to its containing system
        return self.are_systems_adjacent(containing_system_id, target_system_id)

    def _find_unit_system(self, unit: Unit) -> str | None:
        """
        Find which system contains the given unit.

        Args:
            unit: The unit to locate

        Returns:
            System ID containing the unit, or None if not found
        """
        for system_id, system in self.system_objects.items():
            # Check space units
            if unit in system.space_units:
                return system_id

            # Check planet units
            for planet in system.planets:
                if unit in planet.units:
                    return system_id

        return None

    def _find_planet_system(self, planet: Planet) -> str | None:
        """
        Find which system contains the given planet.

        Args:
            planet: The planet to locate

        Returns:
            System ID containing the planet, or None if not found
        """
        for system_id, system in self.system_objects.items():
            if planet in system.planets:
                return system_id

        return None

    def are_players_neighbors(self, player_id1: str, player_id2: str) -> bool:
        """
        Check if two players are neighbors according to LRR Rule 60.

        Players are neighbors if they both have a unit or control a planet
        in the same system or in systems that are adjacent to each other.
        """
        # Get all systems where each player has presence
        player1_systems = self._get_player_systems(player_id1)
        player2_systems = self._get_player_systems(player_id2)

        # Check if players share any systems
        shared_systems = player1_systems.intersection(player2_systems)
        if shared_systems:
            return True

        # Check if any of player1's systems are adjacent to any of player2's systems
        for system1_id in player1_systems:
            for system2_id in player2_systems:
                if self.are_systems_adjacent(system1_id, system2_id):
                    return True

        return False

    def _get_player_systems(self, player_id: str) -> set[str]:
        """
        Get all system IDs where a player has units or controls planets.

        Returns a set of system IDs where the player has presence.
        """
        player_systems = set()

        # Check all registered systems for player presence
        for system_id, system in self.system_objects.items():
            # Check space units
            for unit in system.space_units:
                if unit.owner == player_id:
                    player_systems.add(system_id)
                    break

            # Check planet units and control
            for planet in system.planets:
                # Check units on planet
                for unit in planet.units:
                    if unit.owner == player_id:
                        player_systems.add(system_id)
                        break

                # Check planet control
                if planet.controlled_by == player_id:
                    player_systems.add(system_id)
                    break

        return player_systems

    def find_path(
        self, start_system_id: str, end_system_id: str, max_distance: int = 10
    ) -> list[str]:
        """
        Find a path between two systems using BFS.

        Args:
            start_system_id: Starting system ID
            end_system_id: Destination system ID
            max_distance: Maximum path length to search

        Returns:
            List of system IDs representing the path, empty if no path found
        """
        if start_system_id == end_system_id:
            return [start_system_id]

        # Quick check for direct adjacency (common case optimization)
        if self.are_systems_adjacent(start_system_id, end_system_id):
            return [start_system_id, end_system_id]

        from collections import deque

        queue = deque([(start_system_id, [start_system_id])])
        visited = {start_system_id}

        while queue:
            current_system, path = queue.popleft()

            if len(path) > max_distance:
                continue

            # Check all systems for adjacency
            for system_id in self.system_objects.keys():
                if system_id not in visited and self.are_systems_adjacent(
                    current_system, system_id
                ):
                    new_path = path + [system_id]

                    if system_id == end_system_id:
                        return new_path

                    if len(new_path) < max_distance:
                        queue.append((system_id, new_path))
                        visited.add(system_id)

        return []  # No path found

    def find_planets_controlled_by_player(self, player_id: str) -> list[Planet]:
        """Find all planets controlled by a specific player.

        Args:
            player_id: The player ID to search for

        Returns:
            List of planets controlled by the player
        """
        controlled_planets = []
        for system in self.system_objects.values():
            for planet in system.planets:
                if planet.controlled_by == player_id:
                    controlled_planets.append(planet)
        return controlled_planets

    def find_exhausted_planets_controlled_by_player(
        self, player_id: str
    ) -> list[Planet]:
        """Find all exhausted planets controlled by a specific player.

        Args:
            player_id: The player ID to search for

        Returns:
            List of exhausted planets controlled by the player
        """
        exhausted_planets = []
        for system in self.system_objects.values():
            for planet in system.planets:
                if planet.controlled_by == player_id and planet.is_exhausted():
                    exhausted_planets.append(planet)
        return exhausted_planets

    def find_planet_by_name(
        self, planet_name: str, player_id: str | None = None
    ) -> Planet | None:
        """Find a planet by name, optionally filtered by controlling player.

        Args:
            planet_name: The name of the planet to find
            player_id: Optional player ID to filter by controlling player

        Returns:
            The planet if found, None otherwise
        """
        for system in self.system_objects.values():
            for planet in system.planets:
                if planet.name == planet_name:
                    if player_id is None or planet.controlled_by == player_id:
                        return planet
        return None

"""Galaxy structure for TI4 game board."""

from typing import Optional

from .hex_coordinate import HexCoordinate
from .system import System


class Galaxy:
    """Represents the hex-based galaxy game board."""

    def __init__(self) -> None:
        self.systems: dict[HexCoordinate, str] = {}
        self.system_objects: dict[str, System] = {}  # Registry of system objects

    def place_system(self, coordinate: HexCoordinate, system_id: str) -> None:
        """Place a system at the given hex coordinate."""
        self.systems[coordinate] = system_id

    def register_system(self, system: System) -> None:
        """Register a system object in the galaxy."""
        self.system_objects[system.system_id] = system

    def get_system_coordinate(self, system_id: str) -> Optional[HexCoordinate]:
        """Get the coordinate of a system by its ID."""
        for coord, sid in self.systems.items():
            if sid == system_id:
                return coord
        return None

    def get_system(self, system_id: str) -> Optional[System]:
        """Get a system object by its ID."""
        return self.system_objects.get(system_id)

    def are_systems_adjacent(self, system_id1: str, system_id2: str) -> bool:
        """Check if two systems are adjacent to each other."""
        # Check physical adjacency first
        coord1 = self.get_system_coordinate(system_id1)
        coord2 = self.get_system_coordinate(system_id2)

        if coord1 is None or coord2 is None:
            return False

        # Physical adjacency
        if coord1.distance_to(coord2) == 1:
            return True

        # Check wormhole adjacency (stub implementation - always returns False for now)
        # This will be the focus of our RED phase test
        return self._check_wormhole_adjacency(system_id1, system_id2)

    def _check_wormhole_adjacency(self, system_id1: str, system_id2: str) -> bool:
        """Check if two systems are adjacent via wormholes."""
        system1 = self.get_system(system_id1)
        system2 = self.get_system(system_id2)
        
        if system1 is None or system2 is None:
            return False
        
        # Check if systems share any wormhole types
        for wormhole_type in system1.wormholes:
            if system2.has_wormhole(wormhole_type):
                return True
        
        return False

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
                if hasattr(planet, 'controller') and planet.controller == player_id:
                    player_systems.add(system_id)
                    break
        
        return player_systems

"""Blockade system for TI4 Rule 14: BLOCKADED.

This module implements Rule 14: BLOCKADED mechanics according to the TI4 LRR.
Handles blockade detection, production restrictions, unit return, and capture prevention.
"""

from typing import TYPE_CHECKING, Optional

from .constants import UnitType

if TYPE_CHECKING:
    from .capture import CaptureManager
    from .galaxy import Galaxy
    from .system import System
    from .unit import Unit


class BlockadeManager:
    """Manages blockade mechanics according to Rule 14.

    Handles:
    - Blockade detection (Rule 14.0)
    - Production restrictions (Rule 14.1)
    - Unit return mechanism (Rule 14.2)
    - Capture prevention during blockade (Rule 14.2a)
    """

    def __init__(
        self,
        galaxy: Optional["Galaxy"] = None,
        capture_manager: Optional["CaptureManager"] = None,
    ):
        """Initialize the blockade manager.

        Args:
            galaxy: The galaxy instance for system queries
            capture_manager: The capture manager for unit return mechanics
        """
        self._galaxy = galaxy
        self._capture_manager = capture_manager

    def is_unit_blockaded(self, unit: "Unit") -> bool:
        """Check if a unit is blockaded according to Rule 14.0.

        Args:
            unit: The unit to check for blockade status

        Returns:
            True if the unit is blockaded, False otherwise

        Raises:
            ValueError: If unit is None
        """
        if unit is None:
            raise ValueError("Unit cannot be None")

        # Rule 14.0: Only units with "Production" can be blockaded
        if not self._has_production_ability(unit):
            return False

        # If unit is not in galaxy, it cannot be blockaded
        if self._galaxy is None:
            return False

        # Find the system containing this unit
        unit_system = self._find_unit_system(unit)
        if unit_system is None:
            return False

        # Rule 14.0: Blockaded if system contains enemy ships but no friendly ships
        has_friendly_ships = self._system_has_friendly_ships(unit_system, unit.owner)
        has_enemy_ships = self._system_has_enemy_ships(unit_system, unit.owner)

        return has_enemy_ships and not has_friendly_ships

    def can_produce_ships(self, unit: "Unit") -> bool:
        """Check if a unit can produce ships according to Rule 14.1.

        Args:
            unit: The production unit to check

        Returns:
            True if the unit can produce ships, False if blockaded
        """
        # Rule 14.1: Blockaded units cannot produce ships
        return not self.is_unit_blockaded(unit)

    def can_produce_ground_forces(self, unit: "Unit") -> bool:
        """Check if a unit can produce ground forces according to Rule 14.1.

        Args:
            unit: The production unit to check

        Returns:
            True if the unit can produce ground forces (always True per Rule 14.1)
        """
        # Rule 14.1: Blockaded units can still produce ground forces
        return True

    def apply_blockade_effects(self, unit: "Unit") -> None:
        """Apply blockade effects including unit return according to Rule 14.2.

        Args:
            unit: The blockaded unit
        """
        if not self.is_unit_blockaded(unit):
            return

        if self._capture_manager is None:
            return

        # Rule 14.2: Return captured units from blockading players
        blockading_players = self.get_blockading_players(unit)
        for blockading_player in blockading_players:
            self._return_captured_units_from_player(unit.owner, blockading_player)

    def can_capture_unit(self, target_unit: "Unit", capturing_player: str) -> bool:
        """Check if a unit can be captured according to Rule 14.2a.

        Args:
            target_unit: The unit to potentially capture
            capturing_player: The player attempting the capture

        Returns:
            True if capture is allowed, False if prevented by blockade
        """
        # Rule 14.2a: Blockaded player cannot capture blockading player's units
        if self._galaxy is None:
            return True

        # Find systems where capturing player has blockaded production units
        blockaded_systems = self._find_blockaded_systems_for_player(capturing_player)

        for system in blockaded_systems:
            # Check if target unit's owner is blockading this system
            if self._is_player_blockading_system(
                target_unit.owner, system, capturing_player
            ):
                return False

        return True

    def get_blockading_players(self, unit: "Unit") -> set[str]:
        """Get the set of players blockading the given unit.

        Args:
            unit: The potentially blockaded unit

        Returns:
            Set of player IDs who are blockading the unit
        """
        if not self.is_unit_blockaded(unit):
            return set()

        if self._galaxy is None:
            return set()

        unit_system = self._find_unit_system(unit)
        if unit_system is None:
            return set()

        # Find all enemy players with ships in the system
        blockading_players = set()
        for space_unit in unit_system.space_units:
            if space_unit.owner != unit.owner:
                blockading_players.add(space_unit.owner)

        return blockading_players

    def _has_production_ability(self, unit: "Unit") -> bool:
        """Check if a unit has production ability.

        Args:
            unit: The unit to check

        Returns:
            True if unit has production ability
        """
        # Space docks have production ability
        return unit.unit_type == UnitType.SPACE_DOCK

    def _find_unit_system(self, unit: "Unit") -> Optional["System"]:
        """Find the system containing the given unit.

        Args:
            unit: The unit to locate

        Returns:
            The system containing the unit, or None if not found
        """
        if self._galaxy is None:
            return None

        # Search all systems for the unit
        for _system_id, system in self._galaxy.system_objects.items():
            # Check space units
            if unit in system.space_units:
                return system

            # Check planet units
            for planet in system.planets:
                if unit in planet.units:
                    return system

        return None

    def _system_has_friendly_ships(self, system: "System", player_id: str) -> bool:
        """Check if system has friendly ships.

        Args:
            system: The system to check
            player_id: The player to check for

        Returns:
            True if system has friendly ships
        """
        for unit in system.space_units:
            if unit.owner == player_id and self._is_ship(unit):
                return True
        return False

    def _system_has_enemy_ships(self, system: "System", player_id: str) -> bool:
        """Check if system has enemy ships.

        Args:
            system: The system to check
            player_id: The player to check against

        Returns:
            True if system has enemy ships
        """
        for unit in system.space_units:
            if unit.owner != player_id and self._is_ship(unit):
                return True
        return False

    def _is_ship(self, unit: "Unit") -> bool:
        """Check if a unit is a ship.

        Args:
            unit: The unit to check

        Returns:
            True if unit is a ship
        """
        ship_types = {
            UnitType.CARRIER,
            UnitType.CRUISER,
            UnitType.DESTROYER,
            UnitType.DREADNOUGHT,
            UnitType.FIGHTER,
            UnitType.FLAGSHIP,
            UnitType.WAR_SUN,
        }
        return unit.unit_type in ship_types

    def _return_captured_units_from_player(
        self, capturing_player: str, original_owner: str
    ) -> None:
        """Return captured units from a specific player.

        Args:
            capturing_player: The player who captured the units
            original_owner: The original owner of the units to return
        """
        if self._capture_manager is None:
            return

        # Get captured units belonging to original_owner held by capturing_player
        captured_units = self._capture_manager.get_captured_units_by_owner(
            original_owner, capturing_player
        )

        # Return each captured unit
        for unit in captured_units:
            self._capture_manager.return_unit(unit, capturing_player)

    def _find_blockaded_systems_for_player(self, player_id: str) -> list["System"]:
        """Find systems where player has blockaded production units.

        Args:
            player_id: The player to check

        Returns:
            List of systems with blockaded production units
        """
        if self._galaxy is None:
            return []

        blockaded_systems = []
        for _system_id, system in self._galaxy.system_objects.items():
            # Check for player's production units in this system
            for planet in system.planets:
                for unit in planet.units:
                    if (
                        unit.owner == player_id
                        and self._has_production_ability(unit)
                        and self.is_unit_blockaded(unit)
                    ):
                        blockaded_systems.append(system)
                        break

        return blockaded_systems

    def _is_player_blockading_system(
        self, potential_blockader: str, system: "System", blockaded_player: str
    ) -> bool:
        """Check if a player is blockading a system.

        Args:
            potential_blockader: The player who might be blockading
            system: The system to check
            blockaded_player: The player being blockaded

        Returns:
            True if potential_blockader is blockading the system
        """
        # Check if potential_blockader has ships in the system
        has_blockader_ships = False
        for unit in system.space_units:
            if unit.owner == potential_blockader and self._is_ship(unit):
                has_blockader_ships = True
                break

        if not has_blockader_ships:
            return False

        # Check if blockaded_player has no ships in the system
        has_blockaded_ships = False
        for unit in system.space_units:
            if unit.owner == blockaded_player and self._is_ship(unit):
                has_blockaded_ships = True
                break

        return not has_blockaded_ships

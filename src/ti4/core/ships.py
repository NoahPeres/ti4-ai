"""Ship system for TI4 Rule 76: SHIPS.

This module implements Rule 76: SHIPS mechanics according to the TI4 LRR.
Handles ship identification, fleet pool limits, placement validation, and ship attributes.
"""

from typing import TYPE_CHECKING

from .constants import UnitType

if TYPE_CHECKING:
    from .fleet import Fleet
    from .planet import Planet
    from .system import System
    from .unit import Unit


class ShipManager:
    """Manages ship mechanics according to Rule 76.

    Handles:
    - Ship type identification (Rule 76.0)
    - Ship placement validation (Rule 76.1)
    - Fleet pool limits (Rule 76.2)
    - Ship attributes (Rule 76.3)
    """

    def __init__(self) -> None:
        """Initialize the ship manager."""
        pass

    def is_ship(self, unit: "Unit") -> bool:
        """Check if a unit is a ship.

        Args:
            unit: The unit to check

        Returns:
            True if the unit is a ship, False otherwise

        LRR Reference: Rule 76.0 - Ship definition
        """
        # Rule 76.0: Ships are carriers, cruisers, dreadnoughts, destroyers, fighters, war suns, flagships
        ship_types = {
            UnitType.CARRIER,
            UnitType.CRUISER,
            UnitType.DREADNOUGHT,
            UnitType.DESTROYER,
            UnitType.FIGHTER,
            UnitType.WAR_SUN,
            UnitType.FLAGSHIP,
        }
        return unit.unit_type in ship_types

    def can_place_ship_in_space(self, unit: "Unit", system: "System") -> bool:
        """Check if a ship can be placed in space.

        Args:
            unit: The ship unit to place
            system: The system to place the ship in

        Returns:
            True if the ship can be placed in space

        LRR Reference: Rule 76.1 - Ships are always placed in space
        """
        # Rule 76.1: Ships are always placed in space
        return self.is_ship(unit)

    def can_place_ship_on_planet(self, unit: "Unit", planet: "Planet") -> bool:
        """Check if a ship can be placed on a planet.

        Args:
            unit: The ship unit to place
            planet: The planet to place the ship on

        Returns:
            False - ships cannot be placed on planets

        LRR Reference: Rule 76.1 - Ships are always placed in space
        """
        # Rule 76.1: Ships are always placed in space (not on planets)
        return False

    def can_add_ship_to_system(
        self, unit: "Unit", system: "System", player_id: str, fleet_pool_size: int
    ) -> bool:
        """Check if a ship can be added to a system based on fleet pool limits.

        Args:
            unit: The ship unit to add
            system: The system to add the ship to
            player_id: The player adding the ship
            fleet_pool_size: The number of command tokens in the player's fleet pool

        Returns:
            True if the ship can be added without exceeding fleet pool limits

        LRR Reference: Rule 76.2 - Fleet pool limits
        """
        if not self.is_ship(unit):
            return False

        # Rule 76.2a: Fighters don't count toward fleet pool limit
        if unit.unit_type == UnitType.FIGHTER:
            return True

        # Count current non-fighter ships in system
        current_ships = self.count_non_fighter_ships_in_system(system, player_id)

        # Rule 76.2: Can have ships equal to or less than fleet pool size
        return current_ships < fleet_pool_size

    def count_non_fighter_ships_in_system(
        self, system: "System", player_id: str
    ) -> int:
        """Count non-fighter ships in a system for a player.

        Args:
            system: The system to count ships in
            player_id: The player whose ships to count

        Returns:
            The number of non-fighter ships in the system

        LRR Reference: Rule 76.2a - Fighters don't count toward fleet pool limit
        """
        count = 0
        for unit in system.space_units:
            if (
                unit.owner == player_id
                and self.is_ship(unit)
                and unit.unit_type != UnitType.FIGHTER
            ):
                count += 1
        return count

    def ship_has_cost_attribute(self, unit: "Unit") -> bool:
        """Check if a ship has a cost attribute.

        Args:
            unit: The ship unit to check

        Returns:
            True if the ship has a cost attribute

        LRR Reference: Rule 76.3 - Ship attributes
        """
        if not self.is_ship(unit):
            return False

        # Rule 76.3: Ships can have cost attribute
        return unit.get_cost() > 0

    def ship_has_combat_attribute(self, unit: "Unit") -> bool:
        """Check if a ship has a combat attribute.

        Args:
            unit: The ship unit to check

        Returns:
            True if the ship has a combat attribute

        LRR Reference: Rule 76.3 - Ship attributes
        """
        if not self.is_ship(unit):
            return False

        # Rule 76.3: Ships can have combat attribute
        return unit.get_combat_dice() > 0

    def ship_has_move_attribute(self, unit: "Unit") -> bool:
        """Check if a ship has a move attribute.

        Args:
            unit: The ship unit to check

        Returns:
            True if the ship has a move attribute

        LRR Reference: Rule 76.3 - Ship attributes
        """
        if not self.is_ship(unit):
            return False

        # Rule 76.3: Ships can have move attribute
        return unit.get_movement() > 0

    def ship_has_capacity_attribute(self, unit: "Unit") -> bool:
        """Check if a ship has a capacity attribute.

        Args:
            unit: The ship unit to check

        Returns:
            True if the ship has a capacity attribute

        LRR Reference: Rule 76.3 - Ship attributes
        """
        if not self.is_ship(unit):
            return False

        # Rule 76.3: Ships can have capacity attribute
        return unit.get_capacity() > 0

    def validate_fleet_pool_limits(
        self, fleets: list["Fleet"], fleet_pool_size: int
    ) -> bool:
        """Validate that fleets don't exceed fleet pool limits.

        Args:
            fleets: List of fleets to validate
            fleet_pool_size: The number of command tokens in the player's fleet pool

        Returns:
            True if fleet pool limits are respected

        LRR Reference: Rule 76.2 - Fleet pool limits

        Note: This integrates with existing FleetCapacityValidator for consistency.
        """
        from .fleet import FleetCapacityValidator

        validator = FleetCapacityValidator()
        return validator.is_fleet_supply_valid(fleets, fleet_pool_size)

    def can_add_ship_to_fleet(
        self, unit: "Unit", fleet: "Fleet", fleet_pool_size: int
    ) -> bool:
        """Check if a ship can be added to a fleet based on fleet pool limits.

        Args:
            unit: The ship unit to add
            fleet: The fleet to add the ship to
            fleet_pool_size: The number of command tokens in the player's fleet pool

        Returns:
            True if the ship can be added without exceeding fleet pool limits

        LRR Reference: Rule 76.2 - Fleet pool limits

        Note: This method integrates with existing Fleet class for consistency.
        """
        if not self.is_ship(unit):
            return False

        # Rule 76.2a: Fighters don't count toward fleet pool limit
        if unit.unit_type == UnitType.FIGHTER:
            return True

        # Use existing Fleet class logic for counting ships requiring fleet supply
        current_ships_requiring_supply = len(fleet.get_ships_requiring_fleet_supply())

        # Rule 76.2: Can have ships equal to or less than fleet pool size
        return current_ships_requiring_supply < fleet_pool_size

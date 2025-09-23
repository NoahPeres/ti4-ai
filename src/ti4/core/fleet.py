"""Fleet management for TI4 game framework."""

from __future__ import annotations

from .constants import UnitType
from .unit import Unit


class Fleet:
    """Represents all units belonging to one player in one system's space area.

    In TI4, there's no explicit 'fleet' concept, but this class represents
    the collection of all ships and ground forces that a player has in the
    space area of a specific system. Each player can have at most one Fleet
    per system.

    Fleet supply (command tokens in fleet pool) limits how many systems
    can contain fleets with non-fighter ships.
    """

    def __init__(self, owner: str, system_id: str) -> None:
        """Initialize a fleet for a player in a specific system."""
        self.owner = owner
        self.system_id = system_id
        self.units: list[Unit] = []

    def add_unit(self, unit: Unit) -> None:
        """Add a unit to the fleet."""
        self.units.append(unit)

    def get_total_capacity(self) -> int:
        """Get the total capacity of all capacity‑providing units in the fleet."""
        total_capacity = 0
        for unit in self.units:
            cap = unit.get_capacity()
            if cap > 0:
                total_capacity += cap
        return total_capacity

    def get_carried_units_count(self) -> int:
        """Get the count of units that need to be carried (fighters and infantry)."""
        # Use unit stats to determine if unit needs to be carried
        return sum(1 for unit in self.units if self._unit_needs_capacity(unit))

    def _unit_needs_capacity(self, unit: Unit) -> bool:
        """Check if a unit needs to be carried (no independent movement)."""
        stats = unit.get_stats()
        # Fighters and infantry need capacity unless they have independent movement
        # Fighter II has movement > 0 and doesn't need capacity
        if unit.unit_type == UnitType.FIGHTER:
            return stats.movement == 0  # Base fighters need capacity, Fighter II don't
        elif unit.unit_type == UnitType.INFANTRY:
            return True  # Infantry always need capacity (no independent space movement)
        else:
            return False  # Ships don't need capacity

    def get_ships_with_capacity(self) -> list[Unit]:
        """Get all ships that provide capacity."""
        return [unit for unit in self.units if unit.get_capacity() > 0]

    def get_ships_requiring_fleet_supply(self) -> list[Unit]:
        """Get all ships that require fleet supply (non-fighter ships + Fighter II)."""
        ships_requiring_supply = []
        for unit in self.units:
            stats = unit.get_stats()
            # Ships with independent movement require fleet supply
            if stats.movement > 0:
                # This includes all ships (cruiser, carrier, etc.) and Fighter II
                ships_requiring_supply.append(unit)
        return ships_requiring_supply

    def requires_fleet_supply(self) -> bool:
        """Check if this fleet requires fleet supply (has ships with independent movement)."""
        return len(self.get_ships_requiring_fleet_supply()) > 0


class FleetCapacityValidator:
    """Validates fleet capacity rules."""

    def __init__(self) -> None:
        """Initialize the fleet capacity validator."""
        pass

    def is_fleet_capacity_valid(self, fleet: Fleet) -> bool:
        """Check if a fleet's capacity is valid."""
        total_capacity = fleet.get_total_capacity()
        carried_units = fleet.get_carried_units_count()

        return carried_units <= total_capacity

    def is_fleet_supply_valid(self, fleets: list[Fleet], fleet_tokens: int) -> bool:
        """Check if the number of fleets with non-fighter ships is within fleet pool token limits."""
        # Only count fleets that contain ships requiring fleet supply
        fleets_requiring_supply = sum(
            1 for fleet in fleets if fleet.requires_fleet_supply()
        )
        return fleets_requiring_supply <= fleet_tokens


class FleetCapacityEnforcer:
    """Enforces fleet capacity rules with player choice for excess unit removal.

    LRR Reference: Rule 16.3a - A player can choose which of their excess units to remove.
    """

    def __init__(self) -> None:
        """Initialize the fleet capacity enforcer."""
        pass

    def remove_excess_units_with_choice(
        self, fleet: Fleet, chosen_units_to_remove: list[Unit]
    ) -> list[Unit]:
        """Remove excess units from fleet based on player choice.

        Args:
            fleet: The fleet to enforce capacity on
            chosen_units_to_remove: Units the player chooses to remove

        Returns:
            List of units that were actually removed

        Raises:
            FleetCapacityError: If player choice is invalid or insufficient

        LRR Reference: Rule 16.3a - A player can choose which of their excess units to remove.
        """
        from .exceptions import FleetCapacityError

        # Check if fleet is within capacity - no removal needed
        total_capacity = fleet.get_total_capacity()
        carried_units = fleet.get_carried_units_count()

        if carried_units <= total_capacity:
            return []  # No excess units to remove

        excess_count = carried_units - total_capacity

        # Validate that all chosen units are in the fleet
        for unit in chosen_units_to_remove:
            if unit not in fleet.units:
                raise FleetCapacityError(
                    f"Cannot remove unit not in fleet: {unit.unit_type}"
                )

        # Filter to only units that count against capacity
        valid_units_to_remove = [
            unit for unit in chosen_units_to_remove if fleet._unit_needs_capacity(unit)
        ]

        # Reject duplicate selections among valid units
        if len({id(u) for u in valid_units_to_remove}) != len(valid_units_to_remove):
            raise FleetCapacityError("Duplicate units selected for removal.")

        if len(valid_units_to_remove) < excess_count:
            raise FleetCapacityError(
                f"Insufficient units chosen for removal. Need to remove {excess_count}, "
                f"but only {len(valid_units_to_remove)} chosen."
            )

        # Consider only the exact number needed; ignore any extra provided
        units_to_remove = valid_units_to_remove[:excess_count]

        # Remove the chosen units (only the exact number needed)
        removed_units: list[Unit] = []

        for unit in units_to_remove:
            fleet.units.remove(unit)
            removed_units.append(unit)

        return removed_units

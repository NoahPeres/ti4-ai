"""Production system for TI4 Rule 67: PRODUCING UNITS.

This module implements Rule 67: PRODUCING UNITS mechanics according to the TI4 LRR.
Handles unit production, cost validation, reinforcement limits, and production restrictions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .constants import UnitType
from .unit_stats import UnitStatsProvider

if TYPE_CHECKING:
    from .blockade import BlockadeManager
    from .system import System
    from .unit import Unit


class ProductionManager:
    """Manages unit production mechanics according to Rule 67.

    Handles:
    - Unit cost validation (Rule 67.1)
    - Dual unit production (Rule 67.2)
    - Tactical action production (Rule 67.3)
    - Non-tactical production (Rule 67.4)
    - Reinforcement limits (Rule 67.5)
    - Ship production restrictions (Rule 67.6)
    """

    def __init__(self) -> None:
        """Initialize the production manager."""
        self._stats_provider = UnitStatsProvider()

    def can_afford_unit(self, unit_type: UnitType, available_resources: int) -> bool:
        """Check if a player can afford to produce a unit.

        Args:
            unit_type: The type of unit to produce
            available_resources: The resources available to the player

        Returns:
            True if the player can afford the unit, False otherwise

        LRR Reference: Rule 67.1 - Must spend resources equal to or greater than cost
        """
        unit_stats = self._stats_provider.get_unit_stats(unit_type)
        unit_cost = unit_stats.cost

        # Rule 67.1: Must spend resources equal to or greater than cost
        return available_resources >= unit_cost

    def get_units_produced_for_cost(self, unit_type: UnitType) -> int:
        """Get the number of units produced for the cost of one unit.

        Args:
            unit_type: The type of unit to check

        Returns:
            Number of units produced for the cost (2 for fighters/infantry, 1 for others)

        LRR Reference: Rule 67.2 - Cost with two icons (fighters/infantry) produces two units
        """
        # Rule 67.2: Fighters and infantry produce two units for their cost
        if unit_type in {UnitType.FIGHTER, UnitType.INFANTRY}:
            return 2
        else:
            return 1

    def can_produce_ships_in_system(self, system: System, player_id: str) -> bool:
        """Check if a player can produce ships in a system.

        Args:
            system: The system to check for ship production
            player_id: The player attempting to produce ships

        Returns:
            True if ships can be produced, False if restricted by enemy ships

        LRR Reference: Rule 67.6 - Cannot produce ships in system containing other players' ships
        """
        # Rule 67.6: Cannot produce ships in system containing other players' ships
        for unit in system.space_units:
            if unit.owner != player_id and self._is_ship(unit):
                return False
        return True

    def _is_ship(self, unit: Unit) -> bool:
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

    def can_produce_from_reinforcements(
        self, unit_type: UnitType, available_reinforcements: int, units_to_produce: int
    ) -> bool:
        """Check if units can be produced from available reinforcements.

        Args:
            unit_type: The type of unit to produce
            available_reinforcements: Number of units available in reinforcements
            units_to_produce: Number of production actions (not final unit count)

        Returns:
            True if sufficient reinforcements are available

        LRR Reference: Rule 67.5 - Players limited by units in reinforcements
        """
        # Calculate total units that would be produced
        units_per_production = self.get_units_produced_for_cost(unit_type)
        total_units_needed = units_to_produce * units_per_production

        # Rule 67.5: Must have sufficient units in reinforcements
        return available_reinforcements >= total_units_needed

    def can_produce_ships_with_blockade_check(
        self, unit: Unit, blockade_manager: BlockadeManager
    ) -> bool:
        """Check if a unit can produce ships considering blockade restrictions.

        Args:
            unit: The production unit to check
            blockade_manager: The blockade manager for checking restrictions

        Returns:
            True if ships can be produced, False if restricted by blockade

        LRR Reference: Rule 67.6 + Rule 14.1 - Production restrictions with blockade integration
        """
        # Rule 67.6 + Rule 14.1: Blockaded units cannot produce ships
        return blockade_manager.can_produce_ships(unit)

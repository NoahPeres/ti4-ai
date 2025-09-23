"""Production ability system for TI4 Rule 68: PRODUCTION (UNIT ABILITY).

This module implements Rule 68: PRODUCTION (UNIT ABILITY) mechanics according to the TI4 LRR.
Handles production values, combined production, placement rules, and special cases.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .constants import Faction, GameConstants, UnitType

if TYPE_CHECKING:
    from .blockade import BlockadeManager
    from .planet import Planet
    from .system import System
    from .unit import Unit


class ProductionAbilityManager:
    """Manages production ability mechanics according to Rule 68.

    Handles:
    - Production values and limits (Rule 68.1)
    - Combined production calculations (Rule 68.1a)
    - Fighter/infantry counting (Rule 68.1b)
    - Partial production (Rule 68.1c)
    - Arborec restrictions (Rule 68.1d)
    - Ship placement rules (Rule 68.2)
    - Ground force placement rules (Rule 68.3)
    - Space area production (Rule 68.4)
    """

    def __init__(self) -> None:
        """Initialize the production ability manager."""
        pass

    def get_production_value(self, unit: Unit, planet: Planet | None = None) -> int:
        """Get the production value of a unit.

        Args:
            unit: The unit to check
            planet: The planet the unit is on (required for space docks)

        Returns:
            The production value of the unit

        LRR Reference: Rule 68.1 - Production ability value
        """
        # Rule 68.1: Production ability followed by value
        if unit.unit_type == UnitType.SPACE_DOCK:
            if planet is None:
                # Cannot determine space dock production without planet
                return 0
            # Space Dock I: PRODUCTION = RESOURCES + 2
            return planet.resources + 2
        # War suns do not have production ability in base game
        # Other units with production will be added via faction-specific mechanics
        return 0

    def get_combined_production_in_system(self, system: System, player: str) -> int:
        """Get the combined production value for a player in a system.

        Args:
            system: The system to check
            player: The player whose production to calculate

        Returns:
            The combined production value

        LRR Reference: Rule 68.1a - Combined production values
        """
        # Rule 68.1a: Combined total of units' production values in system
        total_production = 0

        # Check planets for production units
        for planet in system.planets:
            for unit in planet.units:
                if unit.owner == player:
                    total_production += self.get_production_value(unit, planet)

        # Check space area for production units (no planet context)
        for unit in system.space_units:
            if unit.owner == player:
                total_production += self.get_production_value(unit)

        return total_production

    def calculate_production_used(self, units_to_produce: list[UnitType]) -> int:
        """Calculate production capacity used by units to produce.

        Args:
            units_to_produce: List of unit types to produce

        Returns:
            The production capacity used

        LRR Reference: Rule 68.1b - Individual unit counting
        """
        # Rule 68.1b: Each individual unit counts toward production limit
        production_used = 0

        for unit_type in units_to_produce:
            if unit_type in [UnitType.FIGHTER, UnitType.INFANTRY]:
                # Fighters and infantry count individually
                production_used += 1
            else:
                # Other units count as their cost (typically 1 for most ships)
                production_used += 1

        return production_used

    def can_produce_units(
        self,
        producing_unit: Unit,
        units_to_produce: list[UnitType],
        planet: Planet | None = None,
    ) -> bool:
        """Check if a unit can produce the specified units.

        Args:
            producing_unit: The unit doing the production
            units_to_produce: List of unit types to produce
            planet: The planet the unit is on (required for space docks)

        Returns:
            True if the units can be produced

        LRR Reference: Rule 68.1 + 68.1d - Production limits and restrictions
        """
        # Check Arborec space dock infantry restriction
        if (
            producing_unit.unit_type == UnitType.SPACE_DOCK
            and producing_unit.faction == Faction.ARBOREC
            and UnitType.INFANTRY in units_to_produce
        ):
            # Rule 68.1d: Arborec space docks cannot produce infantry
            return False

        # Check production capacity
        production_capacity = self.get_production_value(producing_unit, planet)
        production_used = self.calculate_production_used(units_to_produce)

        return production_used <= production_capacity

    def can_produce_partial_fighters(self, count: int) -> bool:
        """Check if partial fighters can be produced.

        Args:
            count: Number of fighters to produce

        Returns:
            True if partial fighters can be produced

        LRR Reference: Rule 68.1c - Partial production
        """
        # Rule 68.1c: Can choose to produce one fighter for full cost
        return count >= 1

    def get_partial_fighter_cost(self, count: int) -> int:
        """Get the cost for partial fighter production.

        Args:
            count: Number of fighters to produce

        Returns:
            The resource cost

        LRR Reference: Rule 68.1c - Full cost for partial production
        """
        # Rule 68.1c: Must still pay the entire cost
        # Fighters cost 0.5 each, so 2 fighters cost 1 resource
        # Even for 1 fighter, must pay full cost of 1 resource
        return 1

    def can_produce_partial_infantry(self, count: int) -> bool:
        """Check if partial infantry can be produced.

        Args:
            count: Number of infantry to produce

        Returns:
            True if partial infantry can be produced

        LRR Reference: Rule 68.1c - Partial production
        """
        # Rule 68.1c: Can choose to produce one infantry for full cost
        return count >= 1

    def get_partial_infantry_cost(self, count: int) -> int:
        """Get the cost for partial infantry production.

        Args:
            count: Number of infantry to produce

        Returns:
            The resource cost

        LRR Reference: Rule 68.1c - Full cost for partial production
        """
        # Rule 68.1c: Must still pay the entire cost
        # Infantry cost 0.5 each, so 2 infantry cost 1 resource
        # Even for 1 infantry, must pay full cost of 1 resource
        return 1

    def can_place_produced_ships_in_system(
        self, ships: list[UnitType], target_system: System, active_system: System
    ) -> bool:
        """Check if produced ships can be placed in target system.

        Args:
            ships: List of ship types to place
            target_system: System where ships would be placed
            active_system: The active system

        Returns:
            True if ships can be placed in target system

        LRR Reference: Rule 68.2 - Ship placement in active system
        """
        # Rule 68.2: Ships must be placed in the active system
        return target_system == active_system

    def are_units_ships(self, units: list[UnitType]) -> bool:
        """Check if units are ships.

        Args:
            units: List of unit types to check

        Returns:
            True if all units are ships

        LRR Reference: Rule 68.2 - Ship identification
        """
        return all(unit_type in GameConstants.SHIP_TYPES for unit_type in units)

    def can_place_produced_ground_forces_on_planet(
        self, ground_forces: list[UnitType], planet: Planet
    ) -> bool:
        """Check if produced ground forces can be placed on planet.

        Args:
            ground_forces: List of ground force types to place
            planet: Planet where ground forces would be placed

        Returns:
            True if ground forces can be placed on planet

        LRR Reference: Rule 68.3 - Ground force placement on production planets
        """
        # Rule 68.3: Ground forces must be placed on planets with production units
        for unit in planet.units:
            if self.get_production_value(unit, planet) > 0:
                return True
        return False

    def are_units_ground_forces(self, units: list[UnitType]) -> bool:
        """Check if all units are ground forces (infantry or mechs)."""

        return all(unit_type in GameConstants.GROUND_FORCE_TYPES for unit_type in units)

    def can_space_production_place_ground_forces_on_planet(
        self, ground_forces: list[UnitType], planet: Planet, player: str
    ) -> bool:
        """Check if space-based production can place ground forces on planet.

        Args:
            ground_forces: List of ground force types to place
            planet: Planet where ground forces would be placed
            player: The player producing the units

        Returns:
            True if ground forces can be placed on planet

        LRR Reference: Rule 68.4 - Space production planet placement
        """
        # Rule 68.4: Can place on planet the player controls
        return planet.controlled_by == player

    def can_space_production_place_ground_forces_in_space(
        self, ground_forces: list[UnitType], system: System
    ) -> bool:
        """Check if space-based production can place ground forces in space.

        Args:
            ground_forces: List of ground force types to place
            system: System where ground forces would be placed

        Returns:
            True if ground forces can be placed in space

        LRR Reference: Rule 68.4 - Space production space placement
        """
        # Rule 68.4: Can place in space area of system
        return True

    def can_use_production_in_tactical_action(
        self, system: System, player: str
    ) -> bool:
        """Check if player can use production in tactical action.

        Args:
            system: The active system
            player: The player attempting production

        Returns:
            True if production can be used

        LRR Reference: Rule 68.0 - Production during tactical action
        """
        # Rule 68.0: Can resolve production ability during tactical action production step
        return self.get_combined_production_in_system(system, player) > 0

    def is_production_blockaded(
        self, unit: Unit, blockade_manager: BlockadeManager
    ) -> bool:
        """Check if production unit is blockaded.

        Args:
            unit: The production unit to check
            blockade_manager: The blockade manager

        Returns:
            True if production is blockaded

        LRR Reference: Rule 68 + Rule 14 - Production and blockade integration
        """
        # Production integrates with blockade system
        return blockade_manager.is_unit_blockaded(unit)

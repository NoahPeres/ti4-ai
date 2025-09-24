"""Unit destruction system for TI4 Rule 31: DESTROYED.

This module implements unit destruction mechanics according to the TI4 LRR.
Handles the distinction between destroyed and removed units, and manages destruction effects.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from .constants import UnitType

if TYPE_CHECKING:
    from .reinforcements import ReinforcementPool
    from .system import System
    from .unit import Unit


@dataclass
class DestructionEvent:
    """Event representing unit destruction or removal.

    LRR Reference: Rule 31.2 - Distinction between destroyed and removed units.
    """

    unit: Unit
    was_destroyed: bool  # True if destroyed, False if removed
    trigger_effects: bool  # Whether to trigger destruction effects
    system_id: str


class UnitDestructionManager:
    """Manages unit destruction and removal according to Rule 31.

    LRR Reference:
    - Rule 31: When a unit is destroyed, it returns to reinforcements
    - Rule 31.2: Removed units are not treated as destroyed
    """

    def __init__(self) -> None:
        """Initialize the destruction manager."""
        self._destruction_effects: dict[UnitType, list[Callable[[Unit], None]]] = {}

    def register_destruction_effect(
        self, unit_type: UnitType, effect: Callable[[Unit], None]
    ) -> None:
        """Register an effect that triggers when a unit is destroyed.

        Args:
            unit_type: The type of unit this effect applies to
            effect: Function to call when unit is destroyed
        """
        if unit_type not in self._destruction_effects:
            self._destruction_effects[unit_type] = []
        self._destruction_effects[unit_type].append(effect)

    def destroy_unit(
        self,
        unit: Unit,
        system: System,
        reinforcements: ReinforcementPool | None = None,
    ) -> DestructionEvent:
        """Destroy a unit according to Rule 31.

        Args:
            unit: The unit to destroy
            system: The system containing the unit
            reinforcements: Optional reinforcement pool to return unit to

        Returns:
            DestructionEvent describing what happened

        Raises:
            ValueError: If unit is not found in system

        LRR Reference: Rule 31 - Destroyed units return to reinforcements
        """
        # Verify unit is in system
        unit_found = False
        if unit in system.space_units:
            unit_found = True
        else:
            # Check all planets in the system
            for planet in system.planets:
                if unit in planet.units:
                    unit_found = True
                    break

        if not unit_found:
            raise ValueError(f"Unit not found in system {system.system_id}")

        # Remove unit from system
        if unit in system.space_units:
            system.remove_unit_from_space(unit)
        else:
            # Find and remove from planet
            for planet in system.planets:
                if unit in planet.units:
                    system.remove_unit_from_planet(unit, planet.name)
                    break

        # Return to reinforcements if provided
        if reinforcements is not None:
            reinforcements.return_destroyed_unit(unit.unit_type)

        # Trigger destruction effects
        self._trigger_destruction_effects(unit)

        return DestructionEvent(
            unit=unit,
            was_destroyed=True,
            trigger_effects=True,
            system_id=system.system_id,
        )

    def remove_unit(
        self,
        unit: Unit,
        system: System,
        reinforcements: ReinforcementPool | None = None,
    ) -> DestructionEvent:
        """Remove a unit without triggering destruction effects (Rule 31.2).

        Args:
            unit: The unit to remove
            system: The system containing the unit
            reinforcements: Optional reinforcement pool to return unit to

        Returns:
            DestructionEvent describing what happened

        LRR Reference: Rule 31.2 - Removed units don't trigger destruction effects
        """
        # Remove unit from system (same as destruction)
        if unit in system.space_units:
            system.remove_unit_from_space(unit)
        else:
            # Find and remove from planet
            for planet in system.planets:
                if unit in planet.units:
                    system.remove_unit_from_planet(unit, planet.name)
                    break

        # Return to reinforcements if provided
        if reinforcements is not None:
            reinforcements.return_destroyed_unit(unit.unit_type)

        # Do NOT trigger destruction effects (Rule 31.2)

        return DestructionEvent(
            unit=unit,
            was_destroyed=False,
            trigger_effects=False,
            system_id=system.system_id,
        )

    def destroy_units(
        self,
        units: list[Unit],
        system: System,
        reinforcements: ReinforcementPool | None = None,
    ) -> list[DestructionEvent]:
        """Destroy multiple units simultaneously.

        Args:
            units: List of units to destroy
            system: The system containing the units
            reinforcements: Optional reinforcement pool to return units to

        Returns:
            List of DestructionEvents for each unit
        """
        events = []
        for unit in units:
            event = self.destroy_unit(unit, system, reinforcements)
            events.append(event)
        return events

    def destroy_unit_in_combat(
        self,
        unit: Unit,
        system: System,
        reinforcements: ReinforcementPool | None = None,
    ) -> DestructionEvent:
        """Destroy a unit specifically in combat (triggers all effects).

        Args:
            unit: The unit to destroy
            system: The system containing the unit
            reinforcements: Optional reinforcement pool to return unit to

        Returns:
            DestructionEvent describing what happened
        """
        return self.destroy_unit(unit, system, reinforcements)

    def remove_unit_for_fleet_pool(
        self,
        unit: Unit,
        system: System,
        reinforcements: ReinforcementPool | None = None,
    ) -> DestructionEvent:
        """Remove a unit due to fleet pool limits (does not trigger effects).

        Args:
            unit: The unit to remove
            system: The system containing the unit
            reinforcements: Optional reinforcement pool to return unit to

        Returns:
            DestructionEvent describing what happened

        LRR Reference: Rule 31.2 - Fleet pool removal is not destruction
        """
        return self.remove_unit(unit, system, reinforcements)

    def _trigger_destruction_effects(self, unit: Unit) -> None:
        """Trigger all registered destruction effects for a unit type.

        Args:
            unit: The unit that was destroyed
        """
        effects = self._destruction_effects.get(unit.unit_type, [])
        for effect in effects:
            effect(unit)

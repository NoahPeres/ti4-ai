"""
Transport system for TI4 Rule 95: TRANSPORT

Implements Rule 95: TRANSPORT mechanics according to the TI4 LRR.
Handles unit transport capacity, pickup restrictions, movement constraints, and invasion integration.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .constants import UnitType

if TYPE_CHECKING:
    from .unit import Unit

# Rule 95.0: Only fighters and ground forces can be transported
TRANSPORTABLE_UNIT_TYPES = {UnitType.FIGHTER, UnitType.INFANTRY, UnitType.MECH}


@dataclass
class TransportState:
    """Represents the current transport state of units.

    Tracks which units are being transported by which ship during movement.

    LRR Reference: Rule 95.2 - Transported units move with ship
    """

    transport_ship: Unit
    transported_units: list[Unit]
    origin_system_id: str
    player_id: str

    def get_remaining_capacity(self) -> int:
        """Get remaining transport capacity.

        Returns:
            The remaining capacity available for additional units
        """
        ship_capacity = self.transport_ship.get_capacity()
        used_capacity = len(self.transported_units)
        return ship_capacity - used_capacity

    def can_add_unit(self, unit: Unit) -> bool:
        """Check if unit can be added to transport.

        Args:
            unit: The unit to check

        Returns:
            True if the unit can be added within capacity limits

        Raises:
            ValueError: If unit parameter is invalid
        """
        if unit is None:
            raise ValueError("Unit cannot be None")

        # Check if unit type is transportable
        if unit.unit_type not in TRANSPORTABLE_UNIT_TYPES:
            return False

        return self.get_remaining_capacity() > 0


class TransportManager:
    """Manages unit transport operations according to Rule 95.

    Handles:
    - Transport capacity validation (Rule 95.0)
    - Unit pickup during movement (Rule 95.1)
    - Transport movement constraints (Rule 95.2)
    - Command token pickup restrictions (Rule 95.3)
    - Ground force landing integration (Rule 95.4)
    """

    # Reference to module-level constant for transportable unit types

    def __init__(self) -> None:
        """Initialize the transport manager."""
        pass

    def can_transport_units(self, ship: Unit, units: list[Unit]) -> bool:
        """Check if a ship can transport the given units.

        Args:
            ship: The transport ship
            units: List of units to transport

        Returns:
            True if the ship can transport all units within capacity limits

        Raises:
            ValueError: If ship or units parameters are invalid

        LRR Reference: Rule 95.0 - Transport capacity limits
        """
        # Input validation
        if ship is None:
            raise ValueError("Ship cannot be None")
        if units is None:
            raise ValueError("Units list cannot be None")

        # Get ship's transport capacity
        ship_capacity = ship.get_capacity()

        # Ships with no capacity cannot transport units
        if ship_capacity == 0:
            return False

        # Check if all units can be transported (only fighters and ground forces)
        for unit in units:
            if unit.unit_type not in TRANSPORTABLE_UNIT_TYPES:
                return False

        # Calculate total capacity needed for units
        # For now, assume each unit takes 1 capacity
        units_capacity_needed = len(units)

        # Check if ship has enough capacity
        return units_capacity_needed <= ship_capacity

    def load_units(
        self, ship: Unit, units: list[Unit], system_id: str
    ) -> TransportState:
        """Load units onto a transport ship.

        Args:
            ship: The transport ship
            units: List of units to load
            system_id: The system where loading occurs

        Returns:
            TransportState tracking the loaded units

        Raises:
            ValueError: If transport operation is invalid

        LRR Reference: Rule 95.0 - Transport capacity limits
        """
        # Validate the transport operation first
        if not self.can_transport_units(ship, units):
            raise ValueError(
                "Cannot transport units - capacity or type restrictions violated"
            )

        # Determine player ID from ship owner
        player_id = ship.owner

        # Create and return transport state
        return TransportState(
            transport_ship=ship,
            transported_units=units.copy(),  # Copy to avoid external modifications
            origin_system_id=system_id,
            player_id=player_id,
        )

    def unload_units(
        self, transport_state: TransportState, destination_system_id: str
    ) -> list[Unit]:
        """Unload units from a transport ship.

        Args:
            transport_state: The current transport state
            destination_system_id: The system where units are being unloaded

        Returns:
            List of units that were unloaded

        Raises:
            ValueError: If transport state is invalid

        LRR Reference: Rule 95.4 - Ground forces can land during invasion
        """
        # Input validation
        if transport_state is None:
            raise ValueError("Transport state cannot be None")
        if destination_system_id is None:
            raise ValueError("Destination system ID cannot be None")

        # Get the units to unload
        unloaded_units = transport_state.transported_units.copy()

        # Clear the transport state
        # TODO: Consider making TransportState immutable in future refactoring
        # to prevent unintended side effects from direct mutation
        transport_state.transported_units.clear()

        return unloaded_units

    def can_pickup_from_system(
        self,
        system_id: str,
        player_id: str,
        has_player_command_token: bool,
        is_active_system: bool,
    ) -> bool:
        """Check if units can be picked up from a system based on command token restrictions.

        Args:
            system_id: The system to check
            player_id: The player attempting pickup
            has_player_command_token: Whether the system has the player's command token
            is_active_system: Whether this is the active system

        Returns:
            True if pickup is allowed, False otherwise

        LRR Reference: Rule 95.3 - Command token pickup restrictions
        """
        # Input validation
        if system_id is None:
            raise ValueError("System ID cannot be None")
        if player_id is None:
            raise ValueError("Player ID cannot be None")

        # Rule 95.3: Cannot pickup from systems with own command tokens, except active system
        if has_player_command_token and not is_active_system:
            return False

        # All other cases allow pickup
        return True

    def validate_pickup_during_movement(
        self,
        pickup_system_id: str,
        starting_system_id: str,
        active_system_id: str,
        intermediate_systems: list[str],
        has_command_token: bool,
    ) -> bool:
        """Validate if units can be picked up during movement based on system location.

        Args:
            pickup_system_id: The system where pickup is attempted
            starting_system_id: The system where movement started
            active_system_id: The active system (destination)
            intermediate_systems: List of systems passed through during movement
            has_command_token: Whether the pickup system has the player's command token

        Returns:
            True if pickup is allowed, False otherwise

        Raises:
            ValueError: If any system ID is invalid

        LRR Reference: Rule 95.3 - Pickup restrictions during movement
        """
        # Input validation
        if pickup_system_id is None:
            raise ValueError("Pickup system ID cannot be None")
        if starting_system_id is None:
            raise ValueError("Starting system ID cannot be None")
        if active_system_id is None:
            raise ValueError("Active system ID cannot be None")
        if intermediate_systems is None:
            raise ValueError("Intermediate systems list cannot be None")

        # Pickup from starting system is always allowed
        if pickup_system_id == starting_system_id:
            return True

        # Pickup from active system is always allowed (even with command token)
        if pickup_system_id == active_system_id:
            return True

        # For intermediate systems, use the existing command token logic
        # Note: is_active_system is False here since we already handled active system above
        return self.can_pickup_from_system(
            pickup_system_id,
            "",  # Empty string is acceptable - player_id validation only checks for None
            has_command_token,
            False,  # Not active system (already handled above)
        )


class TransportRules:
    """Handles transport movement rules and constraints according to Rule 95.2.

    Manages transport movement validation, space area tracking, and movement constraints.
    """

    def __init__(self) -> None:
        """Initialize the transport rules handler."""
        pass

    def validate_movement_constraints(
        self, transport_state: TransportState, from_system_id: str, to_system_id: str
    ) -> bool:
        """Validate movement constraints for transported units.

        Args:
            transport_state: The current transport state
            from_system_id: The system being moved from
            to_system_id: The system being moved to

        Returns:
            True if movement is valid, False otherwise

        Raises:
            ValueError: If parameters are invalid

        LRR Reference: Rule 95.2 - Transported units move with ship
        """
        # Input validation
        if transport_state is None:
            raise ValueError("Transport state cannot be None")
        if from_system_id is None:
            raise ValueError("From system ID cannot be None")
        if to_system_id is None:
            raise ValueError("To system ID cannot be None")

        # Basic validation - transported units always move with their ship
        # More complex validation can be added later
        return True

    def get_units_in_space_area(self, transport_state: TransportState) -> list[Unit]:
        """Get units that are in the space area during transport.

        Args:
            transport_state: The current transport state

        Returns:
            List of units in the space area

        Raises:
            ValueError: If transport state is invalid

        LRR Reference: Rule 95.2 - Transported units remain in space
        """
        # Input validation
        if transport_state is None:
            raise ValueError("Transport state cannot be None")

        # Transported units remain in space area
        return transport_state.transported_units.copy()

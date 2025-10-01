"""
Transport system for TI4 Rule 95: TRANSPORT

Implements Rule 95: TRANSPORT mechanics according to the TI4 LRR.
Handles unit transport capacity, pickup restrictions, movement constraints, and invasion integration.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from .constants import UnitType
from .exceptions import TI4Error

if TYPE_CHECKING:
    from .fleet import Fleet
    from .unit import Unit


# Transport Exception Hierarchy
class TransportError(TI4Error):
    """Base exception for all transport-related errors.

    LRR Reference: Rule 95 - TRANSPORT
    Requirements: 8.3 - Integrate with existing exception handling patterns
    """

    pass


class TransportCapacityError(TransportError):
    """Raised when transport capacity limits are exceeded.

    LRR Reference: Rule 95.0 - Transport capacity limits
    Requirements: 8.1, 8.2 - Comprehensive error messages with context
    """

    def __init__(
        self,
        message: str,
        ship_type: str | None = None,
        ship_capacity: int | None = None,
        units_requested: int | None = None,
    ):
        super().__init__(message)
        self.ship_type = ship_type
        self.ship_capacity = ship_capacity
        self.units_requested = units_requested


class TransportPickupError(TransportError):
    """Raised when unit pickup is restricted by command tokens or other rules.

    LRR Reference: Rule 95.3 - Command token pickup restrictions
    Requirements: 8.1, 8.2 - Comprehensive error messages with context
    """

    def __init__(
        self,
        message: str,
        system_id: str | None = None,
        has_command_token: bool | None = None,
        is_active_system: bool | None = None,
    ):
        super().__init__(message)
        self.system_id = system_id
        self.has_command_token = has_command_token
        self.is_active_system = is_active_system


class TransportMovementError(TransportError):
    """Raised when transport movement constraints are violated.

    LRR Reference: Rule 95.2 - Transport movement constraints
    Requirements: 8.1, 8.2 - Comprehensive error messages with context
    """

    def __init__(
        self,
        message: str,
        from_system: str | None = None,
        to_system: str | None = None,
        transport_ship_id: str | None = None,
    ):
        super().__init__(message)
        self.from_system = from_system
        self.to_system = to_system
        self.transport_ship_id = transport_ship_id


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

        Note: Currently assumes each unit occupies 1 capacity slot.

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

        # Check unit ownership - cannot transport enemy units
        if unit.owner != self.player_id:
            return False

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
    TRANSPORTABLE_UNIT_TYPES = TRANSPORTABLE_UNIT_TYPES

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

        # Empty list is valid but trivially true
        if not units:
            return True

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
        # Each unit takes 1 capacity slot
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
            TransportCapacityError: If transport capacity is exceeded
            ValueError: If transport operation is invalid

        LRR Reference: Rule 95.0 - Transport capacity limits
        """
        # Input validation
        if system_id is None:
            raise ValueError("System ID cannot be None")

        # Validate the transport operation first
        if not self.can_transport_units(ship, units):
            # Check specific failure reason for better error message
            ship_capacity = ship.get_capacity()
            units_requested = len(units)

            if units_requested > ship_capacity:
                raise TransportCapacityError(
                    f"Cannot transport {units_requested} units: ship capacity is {ship_capacity}",
                    ship_type=ship.unit_type.name,
                    ship_capacity=ship_capacity,
                    units_requested=units_requested,
                )
            else:
                # Other validation failure (e.g., invalid unit types)
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

        # TODO: Use destination_system_id for invasion integration (Rule 95.4)

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
        has_command_token: bool,
    ) -> bool:
        """Validate if units can be picked up during movement based on system location.

        Args:
            pickup_system_id: The system where pickup is attempted
            starting_system_id: The system where movement started
            active_system_id: The active system (destination)
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

    def validate_pickup_with_exception(
        self,
        system_id: str,
        player_id: str,
        has_player_command_token: bool,
        is_active_system: bool,
    ) -> bool:
        """Validate pickup with exception raising for error handling tests.

        Args:
            system_id: The system to check
            player_id: The player attempting pickup
            has_player_command_token: Whether the system has the player's command token
            is_active_system: Whether this is the active system

        Returns:
            True if pickup is allowed

        Raises:
            TransportPickupError: If pickup is restricted

        LRR Reference: Rule 95.3 - Command token pickup restrictions
        Requirements: 8.1, 8.2 - Comprehensive error messages with context
        """
        if not self.can_pickup_from_system(
            system_id, player_id, has_player_command_token, is_active_system
        ):
            raise TransportPickupError(
                f"Cannot pickup from {system_id}: command token restriction",
                system_id=system_id,
                has_command_token=has_player_command_token,
                is_active_system=is_active_system,
            )
        return True


class TransportRules:
    """Handles transport movement rules and constraints according to Rule 95.2.

    Manages transport movement validation, space area tracking, and movement constraints.
    """

    def _validate_transport_state(
        self, transport_state: TransportState, method_name: str
    ) -> None:
        """Validate transport state for transport operations.

        Args:
            transport_state: The transport state to validate
            method_name: Name of the calling method for error context

        Raises:
            ValueError: If transport state is invalid
        """
        if transport_state is None:
            raise ValueError(f"Transport state cannot be None in {method_name}")

        # Additional validation could be added here in the future
        # e.g., validate transport_ship is not None, transported_units is a list, etc.

    def validate_movement_constraints(
        self, transport_state: TransportState, from_system_id: str, to_system_id: str
    ) -> bool:
        """Validate movement constraints for transported units.

        Note: Current implementation always returns True. Additional validation
        will be added as movement rules are integrated.

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
        self._validate_transport_state(transport_state, "validate_movement_constraints")
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
        self._validate_transport_state(transport_state, "get_units_in_space_area")

        # Transported units remain in space area
        return transport_state.transported_units.copy()

    def handle_transport_ship_destruction(
        self, transport_state: TransportState
    ) -> list[Unit]:
        """Handle destruction of transport ship and transported units.

        Args:
            transport_state: The current transport state

        Returns:
            List of all units that are destroyed (ship + transported units)

        Raises:
            ValueError: If transport state is invalid

        LRR Reference: Rule 95.2 - Transported units are destroyed with ship
        """
        # Input validation
        self._validate_transport_state(
            transport_state, "handle_transport_ship_destruction"
        )

        # All transported units are destroyed along with the transport ship
        destroyed_units = [transport_state.transport_ship]
        destroyed_units.extend(transport_state.transported_units)

        return destroyed_units

    def can_transported_units_retreat_separately(
        self, transport_state: TransportState
    ) -> bool:
        """Check if transported units can retreat separately from their transport ship.

        Args:
            transport_state: The current transport state

        Returns:
            False - transported units cannot retreat separately

        Raises:
            ValueError: If transport state is invalid

        LRR Reference: Rule 95.2 - Transported units move with ship
        """
        # Input validation
        self._validate_transport_state(
            transport_state, "can_transported_units_retreat_separately"
        )

        # Transported units cannot retreat separately from their transport ship
        return False

    def validate_movement_with_exception(
        self, transport_state: TransportState, from_system_id: str, to_system_id: str
    ) -> bool:
        """Validate movement with exception raising for error handling tests.

        Args:
            transport_state: The current transport state
            from_system_id: The system being moved from
            to_system_id: The system being moved to

        Returns:
            True if movement is valid

        Raises:
            TransportMovementError: If movement is invalid

        LRR Reference: Rule 95.2 - Transport movement constraints
        Requirements: 8.1, 8.2 - Comprehensive error messages with context
        """
        # Check for invalid transport state
        if transport_state.transport_ship is None:
            raise TransportMovementError(
                f"Invalid transport movement from {from_system_id} to {to_system_id}",
                from_system=from_system_id,
                to_system=to_system_id,
                transport_ship_id=None,
            )

        # Use existing validation logic
        return self.validate_movement_constraints(
            transport_state, from_system_id, to_system_id
        )


class FleetTransportManager:
    """Manages transport operations across multiple ships in a fleet.

    Coordinates transport capacity calculation and unit distribution
    across multiple ships according to Requirements 7.1-7.4.
    """

    def get_total_transport_capacity(self, fleet: Fleet) -> int:
        """Get total transport capacity across all ships in the fleet.

        Args:
            fleet: The fleet to calculate capacity for

        Returns:
            Total transport capacity of all ships in the fleet

        Raises:
            ValueError: If fleet is None
        """
        if fleet is None:
            raise ValueError("Fleet cannot be None")
        return fleet.get_total_capacity()

    def can_transport_units(self, fleet: Fleet, units: list[Unit]) -> bool:
        """Check if fleet can transport the given units.

        Args:
            fleet: The fleet to check
            units: List of units to transport

        Returns:
            True if fleet has sufficient capacity for all units

        Raises:
            ValueError: If fleet or units is None
        """
        if fleet is None:
            raise ValueError("Fleet cannot be None")
        if units is None:
            raise ValueError("Units list cannot be None")

        total_capacity = self.get_total_transport_capacity(fleet)
        return len(units) <= total_capacity

    def create_transport_distribution(
        self, fleet: Fleet, units: list[Unit]
    ) -> list[TransportState]:
        """Create transport distribution across multiple ships.

        Args:
            fleet: The fleet to distribute units across
            units: List of units to distribute

        Returns:
            List of TransportState objects for each ship

        Raises:
            ValueError: If fleet or units is None
        """
        if fleet is None:
            raise ValueError("Fleet cannot be None")
        if units is None:
            raise ValueError("Units list cannot be None")

        return self._create_distribution_with_strategy(
            fleet, units, simple_distribution=True
        )

    def _create_distribution_with_strategy(
        self, fleet: Fleet, units: list[Unit], simple_distribution: bool = True
    ) -> list[TransportState]:
        """Create transport distribution using specified strategy.

        Args:
            fleet: The fleet to distribute units across
            units: List of units to distribute
            simple_distribution: If True, use simple first-fit strategy

        Returns:
            List of TransportState objects for each ship
        """
        transport_states = []
        ships_with_capacity = fleet.get_ships_with_capacity()

        # Distribute units among ships
        units_remaining = units.copy()

        for ship in ships_with_capacity:
            ship_capacity = ship.get_capacity()
            units_for_ship = units_remaining[:ship_capacity]
            units_remaining = units_remaining[ship_capacity:]

            transport_state = TransportState(
                transport_ship=ship,
                transported_units=units_for_ship,
                origin_system_id=fleet.system_id,
                player_id=fleet.owner,
            )
            transport_states.append(transport_state)

            if not units_remaining:
                break

        if units_remaining:
            total_capacity = fleet.get_total_capacity()
            raise TransportCapacityError(
                f"Cannot distribute {len(units)} units across fleet capacity {total_capacity}",
                ship_type=None,
                ship_capacity=total_capacity,
                units_requested=len(units),
            )

        # Add empty transport states for remaining ships
        self._add_empty_transport_states(transport_states, ships_with_capacity, fleet)

        return transport_states

    def _add_empty_transport_states(
        self,
        transport_states: list[TransportState],
        ships_with_capacity: list[Unit],
        fleet: Fleet,
    ) -> None:
        """Add empty transport states for ships not yet included.

        Args:
            transport_states: Current list of transport states
            ships_with_capacity: All ships with capacity in the fleet
            fleet: The fleet being processed
        """
        for ship in ships_with_capacity:
            if not any(ts.transport_ship == ship for ts in transport_states):
                transport_state = TransportState(
                    transport_ship=ship,
                    transported_units=[],
                    origin_system_id=fleet.system_id,
                    player_id=fleet.owner,
                )
                transport_states.append(transport_state)


class TransportOptimizer:
    """Optimizes unit distribution among transport ships."""

    def optimize_transport_distribution(
        self, fleet: Fleet, units: list[Unit]
    ) -> list[TransportState]:
        """Create optimal distribution of units among ships.

        Args:
            fleet: The fleet to optimize distribution for
            units: List of units to distribute

        Returns:
            List of TransportState objects with optimal distribution

        Raises:
            ValueError: If fleet or units is None
        """
        if fleet is None:
            raise ValueError("Fleet cannot be None")
        if units is None:
            raise ValueError("Units list cannot be None")

        return self._create_optimal_distribution(fleet, units)

    def _create_optimal_distribution(
        self, fleet: Fleet, units: list[Unit]
    ) -> list[TransportState]:
        """Create optimal distribution using capacity-first strategy.

        Args:
            fleet: The fleet to optimize distribution for
            units: List of units to distribute

        Returns:
            List of TransportState objects with optimal distribution
        """
        transport_states = []
        ships_with_capacity = fleet.get_ships_with_capacity()

        # Sort ships by capacity (highest first) for optimal distribution
        ships_sorted = sorted(
            ships_with_capacity, key=lambda s: s.get_capacity(), reverse=True
        )

        units_remaining = units.copy()

        for ship in ships_sorted:
            ship_capacity = ship.get_capacity()
            units_for_ship = units_remaining[:ship_capacity]
            units_remaining = units_remaining[ship_capacity:]

            transport_state = TransportState(
                transport_ship=ship,
                transported_units=units_for_ship,
                origin_system_id=fleet.system_id,
                player_id=fleet.owner,
            )
            transport_states.append(transport_state)

            if not units_remaining:
                break

        if units_remaining:
            total_capacity = fleet.get_total_capacity()
            raise TransportCapacityError(
                f"Cannot distribute {len(units)} units across fleet capacity {total_capacity}",
                ship_type=None,
                ship_capacity=total_capacity,
                units_requested=len(units),
            )

        return transport_states


class FleetTransportValidator:
    """Validates fleet transport operations."""

    def validate_fleet_transport_operation(
        self, fleet: Fleet, units: list[Unit]
    ) -> bool:
        """Validate if fleet can perform transport operation.

        Args:
            fleet: The fleet to validate
            units: List of units to transport

        Returns:
            True if operation is valid, False otherwise

        Raises:
            ValueError: If fleet or units is None
        """
        if fleet is None:
            raise ValueError("Fleet cannot be None")
        if units is None:
            raise ValueError("Units list cannot be None")

        return self._validate_capacity_and_unit_types(fleet, units)

    def _validate_capacity_and_unit_types(
        self, fleet: Fleet, units: list[Unit]
    ) -> bool:
        """Validate both capacity limits and unit types.

        Args:
            fleet: The fleet to validate
            units: List of units to transport

        Returns:
            True if validation passes, False otherwise
        """
        # Check capacity limits
        total_capacity = fleet.get_total_capacity()
        if len(units) > total_capacity:
            return False

        # Check unit types (only fighters and ground forces can be transported)
        for unit in units:
            if unit.unit_type not in TRANSPORTABLE_UNIT_TYPES:
                return False

        return True


@dataclass
class TransportAssignment:
    """Represents assignment of units to a specific transport ship."""

    transport_ship: Unit
    units: list[Unit]


@dataclass
class TransportPlan:
    """Represents a comprehensive transport plan for a fleet."""

    transport_assignments: list[TransportAssignment]


class TransportPlanningUtilities:
    """Utilities for creating comprehensive transport plans."""

    def create_transport_plan(self, fleet: Fleet, units: list[Unit]) -> TransportPlan:
        """Create comprehensive transport plan for fleet.

        Args:
            fleet: The fleet to create plan for
            units: List of units to transport

        Returns:
            TransportPlan with assignments for all ships

        Raises:
            ValueError: If fleet or units is None
        """
        if fleet is None:
            raise ValueError("Fleet cannot be None")
        if units is None:
            raise ValueError("Units list cannot be None")

        return self._create_comprehensive_plan(fleet, units)

    def _create_comprehensive_plan(
        self, fleet: Fleet, units: list[Unit]
    ) -> TransportPlan:
        """Create comprehensive transport plan with assignments for all ships.

        Args:
            fleet: The fleet to create plan for
            units: List of units to transport

        Returns:
            TransportPlan with assignments for all ships
        """
        assignments = []
        ships_with_capacity = fleet.get_ships_with_capacity()

        units_remaining = units.copy()

        # Create assignments for all ships with capacity
        for ship in ships_with_capacity:
            ship_capacity = ship.get_capacity()
            units_for_ship = units_remaining[:ship_capacity]
            units_remaining = units_remaining[ship_capacity:]

            assignment = TransportAssignment(transport_ship=ship, units=units_for_ship)
            assignments.append(assignment)

        if units_remaining:
            total_capacity = fleet.get_total_capacity()
            raise TransportCapacityError(
                f"Cannot distribute {len(units)} units across fleet capacity {total_capacity}",
                ship_type=None,
                ship_capacity=total_capacity,
                units_requested=len(units),
            )

        return TransportPlan(transport_assignments=assignments)


# Validation Layer Classes
class TransportValidationLayer:
    """Validation layer for transport operations.

    Provides pre-transport, movement, and landing validation layers with
    state consistency validation and error recovery mechanisms.
    Requirements: 8.1-8.4
    """

    def __init__(self) -> None:
        self.transport_manager = TransportManager()

    def validate_pre_transport(self, ship: Unit, units: list[Unit]) -> None:
        """Validate transport operation before loading units.

        Args:
            ship: The transport ship
            units: List of units to transport

        Raises:
            TransportCapacityError: If transport capacity is exceeded

        Requirements: 8.1, 8.4 - Pre-transport validation
        """
        if not self.transport_manager.can_transport_units(ship, units):
            ship_capacity = ship.get_capacity()
            units_requested = len(units)

            invalid_types = [
                unit.unit_type.name
                for unit in units
                if unit.unit_type not in TRANSPORTABLE_UNIT_TYPES
            ]

            if units_requested > ship_capacity:
                raise TransportCapacityError(
                    f"Pre-transport validation failed: Cannot transport {units_requested} units with ship capacity {ship_capacity}",
                    ship_type=ship.unit_type.name,
                    ship_capacity=ship_capacity,
                    units_requested=units_requested,
                )

            if invalid_types:
                raise TransportCapacityError(
                    "Pre-transport validation failed: only fighters, infantry, and mechs may be transported",
                    ship_type=ship.unit_type.name,
                    ship_capacity=ship_capacity,
                    units_requested=units_requested,
                )

            raise TransportCapacityError(
                "Pre-transport validation failed: transport manager rejected the requested units",
                ship_type=ship.unit_type.name,
                ship_capacity=ship_capacity,
                units_requested=units_requested,
            )

    def validate_movement(
        self, transport_state: TransportState, from_system_id: str, to_system_id: str
    ) -> None:
        """Validate transport movement operation.

        Args:
            transport_state: The current transport state
            from_system_id: The system being moved from
            to_system_id: The system being moved to

        Raises:
            TransportMovementError: If movement is invalid

        Requirements: 8.1, 8.4 - Movement validation
        """
        transport_rules = TransportRules()
        if not transport_rules.validate_movement_constraints(
            transport_state, from_system_id, to_system_id
        ):
            raise TransportMovementError(
                f"Movement validation failed: Invalid transport movement from {from_system_id} to {to_system_id}",
                from_system=from_system_id,
                to_system=to_system_id,
                transport_ship_id=str(transport_state.transport_ship.unit_type)
                if transport_state.transport_ship
                else None,
            )

    def validate_landing(
        self, transport_state: TransportState, planet_name: str
    ) -> list[Unit]:
        """Validate and identify units that can land during invasion.

        Args:
            transport_state: The current transport state
            planet_name: The planet where units are landing

        Returns:
            List of units that can land (ground forces only)

        Requirements: 8.1, 8.4 - Landing validation
        """
        landable_units = []

        for unit in transport_state.transported_units:
            # Only ground forces can land, fighters remain in space
            if unit.unit_type in {UnitType.INFANTRY, UnitType.MECH}:
                landable_units.append(unit)

        return landable_units

    def validate_state_consistency(self, transport_state: TransportState) -> None:
        """Validate transport state consistency.

        Args:
            transport_state: The transport state to validate

        Raises:
            TransportMovementError: If state is inconsistent

        Requirements: 8.1, 8.4 - State consistency validation
        """
        # Check that all transported units belong to the same player
        for unit in transport_state.transported_units:
            if unit.owner != transport_state.player_id:
                raise TransportMovementError(
                    f"State consistency validation failed: Unit ownership mismatch - unit belongs to {unit.owner}, transport belongs to {transport_state.player_id}",
                    transport_ship_id=str(transport_state.transport_ship.unit_type)
                    if transport_state.transport_ship
                    else None,
                )


@dataclass
class TransportErrorRecoveryResult:
    """Result of transport error recovery attempt."""

    success: bool
    error_type: str
    suggested_fix: str


class TransportErrorRecovery:
    """Error recovery mechanisms for transport validation failures.

    Requirements: 8.4 - Validation error recovery mechanisms
    """

    def attempt_with_recovery(
        self, operation_func: Callable[[], None]
    ) -> TransportErrorRecoveryResult:
        """Attempt operation with error recovery.

        Args:
            operation_func: The operation function to attempt

        Returns:
            TransportErrorRecoveryResult with recovery information
        """
        try:
            operation_func()
            return TransportErrorRecoveryResult(
                success=True,
                error_type="None",
                suggested_fix="Operation completed successfully",
            )
        except TransportCapacityError as e:
            return TransportErrorRecoveryResult(
                success=False,
                error_type="TransportCapacityError",
                suggested_fix=f"Reduce number of units or use ship with higher capacity. Current issue: {str(e)}",
            )
        except TransportPickupError as e:
            return TransportErrorRecoveryResult(
                success=False,
                error_type="TransportPickupError",
                suggested_fix=f"Remove command token or choose different pickup location. Current issue: {str(e)}",
            )
        except TransportMovementError as e:
            return TransportErrorRecoveryResult(
                success=False,
                error_type="TransportMovementError",
                suggested_fix=f"Fix transport state or movement parameters. Current issue: {str(e)}",
            )
        except Exception as e:
            return TransportErrorRecoveryResult(
                success=False,
                error_type=type(e).__name__,
                suggested_fix=f"Unexpected error occurred: {str(e)}",
            )

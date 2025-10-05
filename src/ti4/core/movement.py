"""Movement system for TI4 units."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from .constants import GameConstants, LocationType, Technology, UnitType
from .galaxy import Galaxy
from .movement_rules import MovementContext, MovementRuleEngine
from .system import System
from .unit import Unit

if TYPE_CHECKING:
    from .movement_validation import MovementValidationResult
    from .transport import TransportManager, TransportState


def _check_path_requires_alpha_or_beta_wormholes(
    galaxy: Galaxy, movement: MovementOperation
) -> bool:
    """Check if movement would only be possible via alpha or beta wormholes.

    This implements the Enforced Travel Ban rule: "Alpha and beta wormholes
    have no effect during movement."

    Args:
        galaxy: Galaxy instance for path finding
        movement: The movement operation to check

    Returns:
        True if movement requires alpha or beta wormholes, False otherwise
    """
    path = galaxy.find_path(movement.from_system_id, movement.to_system_id)
    if not path:
        return False

    for i in range(len(path) - 1):
        current_id = path[i]
        next_id = path[i + 1]
        current_coord = galaxy.get_system_coordinate(current_id)
        next_coord = galaxy.get_system_coordinate(next_id)

        if current_coord and next_coord and current_coord.distance_to(next_coord) == 1:
            continue  # physical adjacency, no wormhole needed

        current_system = galaxy.get_system(current_id)
        next_system = galaxy.get_system(next_id)
        if not current_system or not next_system:
            continue

        shared = set(current_system.get_wormhole_types()).intersection(
            next_system.get_wormhole_types()
        )
        if {"alpha", "beta"}.intersection(shared):
            return True

    return False


@dataclass
class MovementOperation:
    """Represents a unit movement operation (internal game logic).

    Note: This is NOT a TI4 Action - it's an internal operation for moving units.
    TI4 Actions are handled by the TacticalAction class.

    Enhanced to support Rule 95: TRANSPORT with comprehensive transport state tracking.
    """

    unit: Unit
    from_system_id: str
    to_system_id: str
    player_id: str
    from_location: str = "space"  # "space" or planet name
    to_location: str = "space"  # "space" or planet name
    player_technologies: set[Technology] | None = None
    transport_ship: Unit | None = None  # For ground force transport (legacy)
    transport_state: TransportState | None = None  # Enhanced Rule 95 transport state
    active_system_id: str | None = None  # For nebula movement validation


def _is_space_location(location: str) -> bool:
    """Check if a location string represents space."""
    return location == LocationType.SPACE.value


class MovementValidator:
    """Validates unit movement actions."""

    def __init__(
        self, galaxy: Galaxy, rule_engine: MovementRuleEngine | None = None
    ) -> None:
        """Initialize the movement validator with a galaxy."""
        self._galaxy = galaxy
        self._rule_engine = rule_engine or MovementRuleEngine()

    def is_valid_movement(self, movement: MovementOperation) -> bool:
        """Check if a movement action is valid according to TI4 rules."""
        # First check TI4-specific rules
        if not self._validate_ti4_movement_rules(movement):
            return False

        # Then check distance/range validation
        tech_key = (
            frozenset(tech.value for tech in movement.player_technologies)
            if movement.player_technologies
            else frozenset()
        )
        return self._is_valid_movement_cached(
            UnitType(movement.unit.unit_type),
            movement.from_system_id,
            movement.to_system_id,
            tech_key,
        )

    def _validate_ti4_movement_rules(self, movement: MovementOperation) -> bool:
        """Validate TI4-specific movement rules."""
        from_system = self._galaxy.get_system(movement.from_system_id)
        to_system = self._galaxy.get_system(movement.to_system_id)

        if not from_system or not to_system:
            return False

        # Rule 58.4c: Cannot move from system with own command token
        if from_system.has_command_token(movement.player_id):
            return False

        # Rule 58.4b: Cannot move through systems with enemy ships
        # Find the path and check each intermediate system
        path = self._galaxy.find_path(movement.from_system_id, movement.to_system_id)

        if not path:
            return False  # No path exists

        # Check intermediate systems (exclude start and end)
        for i in range(1, len(path) - 1):
            intermediate_system_id = path[i]
            intermediate_system = self._galaxy.get_system(intermediate_system_id)

            if intermediate_system and intermediate_system.has_enemy_ships(
                movement.player_id
            ):
                return False  # Blocked by enemy ships in intermediate system

        # Rule 58.4d: Can move through systems with own command tokens
        # This is implicitly allowed by not blocking it

        return True

    def validate_movement(self, movement: MovementOperation) -> bool:
        """Validate a movement operation (alias for is_valid_movement)."""
        return self.is_valid_movement(movement)

    def _is_valid_movement_cached(
        self,
        unit_type: UnitType,
        from_system_id: str,
        to_system_id: str,
        technologies: frozenset[str],
    ) -> bool:
        """Cached movement validation."""
        from_coord = self._galaxy.get_system_coordinate(from_system_id)
        to_coord = self._galaxy.get_system_coordinate(to_system_id)

        if from_coord is None or to_coord is None:
            return False

        # Create a mock unit for validation (since we only need the type)
        mock_unit = Unit(unit_type=unit_type, owner="temp")

        # Create movement context
        context = MovementContext(
            unit=mock_unit,
            from_coordinate=from_coord,
            to_coordinate=to_coord,
            player_technologies={Technology(tech) for tech in technologies},
            galaxy=self._galaxy,
        )

        # Use rule engine to validate movement
        return self._rule_engine.can_move(context)

    def is_valid_movement_with_law_effects(
        self, movement: MovementOperation, law_effects: list[Any]
    ) -> bool:
        """Check if a movement action is valid considering active law effects.

        Args:
            movement: The movement operation to validate
            law_effects: List of active laws that might affect movement

        Returns:
            True if movement is valid considering law effects
        """
        # First check standard movement validation
        if not self.is_valid_movement(movement):
            return False

        # Check law effects
        for law_effect in law_effects:
            if (
                law_effect.agenda_card
                and law_effect.agenda_card.get_name() == "Enforced Travel Ban"
            ):
                # Enforced Travel Ban: Alpha and beta wormholes have no effect during movement
                if self._movement_requires_alpha_or_beta_wormholes(movement):
                    return False  # Movement blocked by Enforced Travel Ban

        return True

    def _movement_requires_alpha_or_beta_wormholes(
        self, movement: MovementOperation
    ) -> bool:
        """Check if movement would only be possible via alpha or beta wormholes."""
        return _check_path_requires_alpha_or_beta_wormholes(self._galaxy, movement)

    def validate_movement_with_transport(self, movement: MovementOperation) -> bool:
        """Validate movement operation that includes transport state.

        Performs comprehensive validation for movement with transported units:
        - Standard movement validation
        - Transport capacity and unit type validation
        - Transport state consistency validation

        Args:
            movement: Movement operation with optional transport state

        Returns:
            True if movement with transport is valid, False otherwise

        Raises:
            ValueError: If movement operation is None

        LRR Reference: Rule 95.0, 95.2 - Transport validation during movement
        """
        if movement is None:
            raise ValueError("Movement operation cannot be None")

        # If no transport state, use standard validation
        if movement.transport_state is None:
            return self.is_valid_movement(movement)

        # Validate transport state consistency
        transport_state = movement.transport_state
        if transport_state.transport_ship != movement.unit:
            return False  # Transport ship must match movement unit

        if transport_state.player_id != movement.player_id:
            return False  # Player must match

        # Validate transport capacity and unit types using TransportValidator
        from .transport import TransportManager

        transport_manager = TransportManager()
        if not transport_manager.can_transport_units(
            transport_state.transport_ship, transport_state.transported_units
        ):
            return False

        # Validate standard movement rules
        return self.is_valid_movement(movement)

    def validate_movement_path_through_anomalies(
        self, movement: MovementOperation
    ) -> bool:
        """Validate movement path checking anomaly restrictions for all systems.

        Args:
            movement: The movement operation to validate

        Returns:
            True if movement path is valid, False if blocked by anomalies

        LRR References:
        - Rule 58: Movement integration with all anomaly types
        - Requirement 8.1: Check anomaly restrictions for all systems in path
        """
        from .constants import AnomalyType

        active_system_id = movement.active_system_id or movement.to_system_id

        # Get the movement path
        path = self._galaxy.find_path(movement.from_system_id, movement.to_system_id)
        if not path:
            return False

        # Check each system in the path for anomaly restrictions
        for system_id in path:
            system = self._galaxy.get_system(system_id)
            if not system:
                continue

            # Skip the starting system (movement from is allowed)
            if system_id == movement.from_system_id:
                continue

            # Check for movement-blocking anomalies
            anomaly_types = system.get_anomaly_types()
            for anomaly_type in anomaly_types:
                if anomaly_type in {AnomalyType.ASTEROID_FIELD, AnomalyType.SUPERNOVA}:
                    return False
                elif anomaly_type == AnomalyType.NEBULA:
                    # Nebula blocks movement unless it's the active system
                    if system_id != active_system_id:
                        return False

        return True

    def get_movement_validation_error(self, movement: MovementOperation) -> str | None:
        """Get detailed error message for movement validation failure.

        Args:
            movement: The movement operation to validate

        Returns:
            Error message if movement is invalid, None if valid

        LRR References:
        - Requirement 8.4: Specific error messages indicating which anomaly caused failure
        """
        from .constants import AnomalyType

        active_system_id = movement.active_system_id or movement.to_system_id

        # Get the movement path
        path = self._galaxy.find_path(movement.from_system_id, movement.to_system_id)
        if not path:
            return "No valid path found between systems"

        # Check each system in the path for anomaly restrictions
        for system_id in path:
            system = self._galaxy.get_system(system_id)
            if not system:
                continue

            # Skip the starting system
            if system_id == movement.from_system_id:
                continue

            # Check for movement-blocking anomalies
            anomaly_types = system.get_anomaly_types()
            for anomaly_type in anomaly_types:
                if anomaly_type == AnomalyType.ASTEROID_FIELD:
                    return f"Movement blocked by asteroid field in system {system_id}"
                elif anomaly_type == AnomalyType.SUPERNOVA:
                    return f"Movement blocked by supernova in system {system_id}"
                elif anomaly_type == AnomalyType.NEBULA:
                    if system_id != active_system_id:
                        return f"Movement blocked by nebula in system {system_id} - nebula must be the active system"

        return None

    def calculate_effective_movement_range(self, movement: MovementOperation) -> int:
        """Calculate effective movement range with anomaly effects applied.

        Args:
            movement: The movement operation to analyze

        Returns:
            Effective movement range considering anomaly effects

        LRR References:
        - Requirement 8.3: Calculate movement costs with anomaly effects applied
        """
        from .constants import AnomalyType

        base_movement = movement.unit.get_movement()

        # Get starting system to check for nebula penalty
        from_system = self._galaxy.get_system(movement.from_system_id)
        if from_system and from_system.has_anomaly_type(AnomalyType.NEBULA):
            # Nebula sets move value to 1
            return 1

        # Check for gravity rift bonus when exiting from gravity rift system
        gravity_rift_bonuses = 0
        if from_system and from_system.has_anomaly_type(AnomalyType.GRAVITY_RIFT):
            gravity_rift_bonuses += 1

        # Check for gravity rift bonuses in intermediate systems of the path
        path = self._galaxy.find_path(movement.from_system_id, movement.to_system_id)
        if path and len(path) > 2:  # Only check intermediate systems
            for system_id in path[1:-1]:  # Skip start and end systems
                system = self._galaxy.get_system(system_id)
                if system and system.has_anomaly_type(AnomalyType.GRAVITY_RIFT):
                    gravity_rift_bonuses += 1

        return base_movement + gravity_rift_bonuses

    def validate_movement_with_anomaly_effects(
        self, movement: MovementOperation
    ) -> MovementValidationResult:
        """Validate movement with comprehensive anomaly effects analysis.

        Args:
            movement: The movement operation to validate

        Returns:
            Comprehensive validation result with error details

        LRR References:
        - Requirement 8.2: Movement path includes blocked anomalies
        """
        from .movement_validation import MovementValidationResult

        # Check if movement is valid
        is_valid = self.validate_movement_path_through_anomalies(movement)

        # Get error message if invalid
        error_message = ""
        blocked_systems = []
        if not is_valid:
            error_message = (
                self.get_movement_validation_error(movement)
                or "Movement blocked by anomaly"
            )
            # Extract blocked system from error message
            if "system " in error_message:
                system_part = error_message.split("system ")[1].split()[0]
                blocked_systems.append(system_part)

        # Calculate effective movement range
        effective_range = self.calculate_effective_movement_range(movement)

        # Identify anomaly effects applied
        anomaly_effects = []
        from_system = self._galaxy.get_system(movement.from_system_id)
        if from_system:
            from .constants import AnomalyType

            if from_system.has_anomaly_type(AnomalyType.NEBULA):
                anomaly_effects.append("nebula_move_penalty")
            if from_system.has_anomaly_type(AnomalyType.GRAVITY_RIFT):
                anomaly_effects.append("gravity_rift_exit_bonus")

        return MovementValidationResult(
            is_valid=is_valid,
            error_message=error_message,
            blocked_systems=blocked_systems,
            effective_movement_range=effective_range,
            anomaly_effects_applied=anomaly_effects,
        )


class MovementExecutor:
    """Executes unit movement actions."""

    def __init__(self, galaxy: Galaxy, systems: dict[str, System]) -> None:
        """Initialize the movement executor."""
        self._galaxy = galaxy
        self._systems = systems

    def execute_movement(self, movement: MovementOperation) -> bool:
        """Execute a movement action."""
        from_system = self._systems.get(movement.from_system_id)
        to_system = self._systems.get(movement.to_system_id)

        if from_system is None or to_system is None:
            from .exceptions import InvalidSystemError

            raise InvalidSystemError("Invalid system ID in movement")

        # Check for invalid direct planet-to-planet movement
        if not _is_space_location(movement.from_location) and not _is_space_location(
            movement.to_location
        ):
            # Direct planet-to-planet movement is not allowed
            return False

        # Handle different movement types
        self._remove_unit_from_location(
            from_system, movement.unit, movement.from_location
        )
        self._place_unit_at_location(to_system, movement.unit, movement.to_location)

        return True

    def _remove_unit_from_location(
        self, system: System, unit: Unit, location: str
    ) -> None:
        """Remove unit from specified location (space or planet)."""
        if _is_space_location(location):
            system.remove_unit_from_space(unit)
        else:
            # Remove from planet
            system.remove_unit_from_planet(unit, location)

    def _place_unit_at_location(
        self, system: System, unit: Unit, location: str
    ) -> None:
        """Place unit at specified location (space or planet)."""
        if _is_space_location(location):
            system.place_unit_in_space(unit)
        else:
            # Place on planet
            system.place_unit_on_planet(unit, location)

    def execute_movement_with_transport(self, movement: MovementOperation) -> bool:
        """Execute movement operation that includes transport state.

        Handles movement of transport ship and all transported units together.
        Transported units move with their transport ship according to Rule 95.2.

        Args:
            movement: Movement operation with transport state

        Returns:
            True if movement was executed successfully, False otherwise

        Raises:
            ValueError: If movement operation is invalid

        LRR Reference: Rule 95.2 - Transported units move with ship
        """
        if movement is None:
            raise ValueError("Movement operation cannot be None")

        # If no transport state, use standard execution
        if movement.transport_state is None:
            return self.execute_movement(movement)

        from_system = self._systems.get(movement.from_system_id)
        to_system = self._systems.get(movement.to_system_id)

        if from_system is None or to_system is None:
            from .exceptions import InvalidSystemError

            raise InvalidSystemError("Invalid system ID in movement with transport")

        transport_state = movement.transport_state

        # Move the transport ship
        self._remove_unit_from_location(
            from_system, transport_state.transport_ship, movement.from_location
        )
        self._place_unit_at_location(
            to_system, transport_state.transport_ship, movement.to_location
        )

        # Move all transported units with the ship
        for transported_unit in transport_state.transported_units:
            # Remove from source system (guard against missing units)
            if transported_unit in from_system.get_units_in_space():
                from_system.remove_unit_from_space(transported_unit)
            # Place in destination system (transported units remain in space)
            to_system.place_unit_in_space(transported_unit)

        return True


@dataclass
class TransportOperation:
    """Represents transporting ground forces with ships (internal operation)."""

    transport_ship: Unit
    ground_forces: list[Unit]
    from_system_id: str
    to_system_id: str
    from_location: str = "space"  # Where ground forces start
    to_location: str = "space"  # Where ground forces end up
    player_id: str = ""


class TransportValidator:
    """Validates transport actions for fighters and ground forces.

    Enhanced to support Rule 95: TRANSPORT compliance.
    Integrates with existing movement validation while adding Rule 95 specific checks.
    """

    def __init__(self, galaxy: Galaxy) -> None:
        """Initialize transport validator with galaxy reference.

        Args:
            galaxy: Galaxy instance for coordinate and system lookups

        Raises:
            ValueError: If galaxy is None
        """
        if galaxy is None:
            raise ValueError("Galaxy cannot be None")

        self._galaxy = galaxy
        # Lazy import to avoid circular dependencies
        self._transport_manager: TransportManager | None = None

    def _get_transport_manager(self) -> TransportManager:
        """Get transport manager instance (lazy initialization).

        Returns:
            TransportManager instance for Rule 95 validation
        """
        if self._transport_manager is None:
            from .transport import TransportManager

            self._transport_manager = TransportManager()
        return self._transport_manager

    def is_valid_transport(self, transport: TransportOperation) -> bool:
        """Check if a transport action is valid according to Rule 95.

        Performs comprehensive validation including:
        - Rule 95.0: Transport capacity limits
        - Rule 95.0: Only fighters and ground forces can be transported
        - Movement distance validation (existing functionality)
        - System coordinate validation

        Args:
            transport: The transport operation to validate

        Returns:
            True if transport is valid, False otherwise

        Raises:
            ValueError: If transport operation is None or invalid

        LRR Reference: Rule 95.0 - Transport capacity and unit type restrictions
        """
        if transport is None:
            raise ValueError("Transport operation cannot be None")

        # Rule 95.0: Check transport capacity and unit types using enhanced manager
        transport_manager = self._get_transport_manager()
        if not transport_manager.can_transport_units(
            transport.transport_ship, transport.ground_forces
        ):
            return False

        # Validate system coordinates exist
        from_coord = self._galaxy.get_system_coordinate(transport.from_system_id)
        to_coord = self._galaxy.get_system_coordinate(transport.to_system_id)

        if from_coord is None or to_coord is None:
            return False

        # Validate movement distance (existing functionality)
        max_movement = transport.transport_ship.get_movement()
        actual_distance = from_coord.distance_to(to_coord)

        return actual_distance <= max_movement

    def validate_pickup_restrictions(
        self,
        pickup_system_id: str,
        player_id: str,
        has_command_token: bool,
        is_active_system: bool,
    ) -> bool:
        """Validate pickup restrictions according to Rule 95.3.

        Args:
            pickup_system_id: System where pickup is attempted
            player_id: Player attempting pickup
            has_command_token: Whether system has player's command token
            is_active_system: Whether this is the active system

        Returns:
            True if pickup is allowed, False otherwise

        Raises:
            ValueError: If required parameters are None or invalid

        LRR Reference: Rule 95.3 - Command token pickup restrictions
        """
        if pickup_system_id is None:
            raise ValueError("Pickup system ID cannot be None")
        if player_id is None:
            raise ValueError("Player ID cannot be None")

        transport_manager = self._get_transport_manager()
        return transport_manager.can_pickup_from_system(
            pickup_system_id, player_id, has_command_token, is_active_system
        )

    def validate_movement_pickup(
        self,
        pickup_system_id: str,
        starting_system_id: str,
        active_system_id: str,
        has_command_token: bool,
    ) -> bool:
        """Validate pickup during movement according to Rule 95.3.

        Validates pickup restrictions for different movement scenarios:
        - Pickup from starting system (always allowed)
        - Pickup from active system (always allowed)
        - Pickup from intermediate systems (subject to command token restrictions)

        Args:
            pickup_system_id: System where pickup is attempted
            starting_system_id: Starting system of movement
            active_system_id: Active system (destination)
            has_command_token: Whether pickup system has player's command token

        Returns:
            True if pickup is allowed, False otherwise

        Raises:
            ValueError: If required system IDs are None

        LRR Reference: Rule 95.3 - Pickup restrictions during movement
        """
        if pickup_system_id is None:
            raise ValueError("Pickup system ID cannot be None")
        if starting_system_id is None:
            raise ValueError("Starting system ID cannot be None")
        if active_system_id is None:
            raise ValueError("Active system ID cannot be None")

        transport_manager = self._get_transport_manager()
        return transport_manager.validate_pickup_during_movement(
            pickup_system_id, starting_system_id, active_system_id, has_command_token
        )

    def is_valid_movement_with_law_effects(
        self, movement: MovementOperation, law_effects: list[Any]
    ) -> bool:
        """Check if a movement action is valid considering active law effects.

        Args:
            movement: The movement operation to validate
            law_effects: List of active laws that might affect movement

        Returns:
            True if movement is valid considering law effects
        """
        # Create a transport operation from the movement for validation
        transport = TransportOperation(
            transport_ship=movement.unit,
            ground_forces=[],
            from_system_id=movement.from_system_id,
            to_system_id=movement.to_system_id,
            player_id=movement.player_id,
        )

        # First check standard transport validation
        if not self.is_valid_transport(transport):
            return False

        # Check law effects
        for law_effect in law_effects:
            if (
                law_effect.agenda_card
                and law_effect.agenda_card.get_name() == "Enforced Travel Ban"
            ):
                # Enforced Travel Ban: Alpha and beta wormholes have no effect during movement
                if self._movement_requires_alpha_or_beta_wormholes(movement):
                    return False  # Movement blocked by Enforced Travel Ban

        return True

    def _movement_requires_alpha_or_beta_wormholes(
        self, movement: MovementOperation
    ) -> bool:
        """Check if movement would only be possible via alpha or beta wormholes."""
        return _check_path_requires_alpha_or_beta_wormholes(self._galaxy, movement)


class TransportExecutor:
    """Executes transport actions."""

    def __init__(self, systems: dict[str, System]) -> None:
        """Initialize transport executor."""
        self._systems = systems

    def execute_transport(self, transport: TransportOperation) -> None:
        """Execute a transport action."""
        from_system = self._systems.get(transport.from_system_id)
        to_system = self._systems.get(transport.to_system_id)

        if from_system is None or to_system is None:
            from .exceptions import InvalidSystemError

            raise InvalidSystemError("Invalid system ID in transport")

        # Move transport ship
        if transport.from_system_id != transport.to_system_id:
            from_system.remove_unit_from_space(transport.transport_ship)
            to_system.place_unit_in_space(transport.transport_ship)

        # Move ground forces
        for unit in transport.ground_forces:
            self._move_ground_force(
                from_system,
                to_system,
                unit,
                transport.from_location,
                transport.to_location,
            )

    def _move_ground_force(
        self,
        from_system: System,
        to_system: System,
        unit: Unit,
        from_location: str,
        to_location: str,
    ) -> None:
        """Move a single ground force unit."""
        # Remove from source
        if _is_space_location(from_location):
            from_system.remove_unit_from_space(unit)
        else:
            from_system.remove_unit_from_planet(unit, from_location)

        # Place at destination
        if _is_space_location(to_location):
            to_system.place_unit_in_space(unit)
        else:
            to_system.place_unit_on_planet(unit, to_location)

    def can_transport_units(self, carrier: Unit, units: list[Unit]) -> bool:
        """Check if a carrier can transport the given units."""

        # Only infantry and mechs can be transported
        transportable_types = GameConstants.GROUND_FORCE_TYPES
        for unit in units:
            if unit.unit_type not in transportable_types:
                return False

        # Check capacity using explicit per-unit costs
        cost_by_type = {
            UnitType.FIGHTER: GameConstants.FIGHTER_CAPACITY_COST,
            UnitType.INFANTRY: GameConstants.INFANTRY_CAPACITY_COST,
            UnitType.MECH: GameConstants.MECH_CAPACITY_COST,
        }
        used = 0
        for u in units:
            used += cost_by_type.get(u.unit_type, 1)
        return used <= carrier.get_capacity()

    def get_transportable_units(self, system: System, player: str) -> list[Unit]:
        """Get all units that can be transported by this player."""
        from .constants import GameConstants

        transportable_units = []
        for planet in system.planets:
            for unit in planet.units:
                if (
                    unit.owner == player
                    and unit.unit_type in GameConstants.GROUND_FORCE_TYPES
                ):
                    transportable_units.append(unit)
        return transportable_units

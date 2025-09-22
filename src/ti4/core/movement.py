"""Movement system for TI4 units."""

from dataclasses import dataclass
from typing import Optional

from .constants import LocationType, Technology, UnitType
from .galaxy import Galaxy
from .movement_rules import MovementContext, MovementRuleEngine
from .system import System
from .unit import Unit


@dataclass
class MovementOperation:
    """Represents a unit movement operation (internal game logic).

    Note: This is NOT a TI4 Action - it's an internal operation for moving units.
    TI4 Actions are handled by the TacticalAction class.
    """

    unit: Unit
    from_system_id: str
    to_system_id: str
    player_id: str
    from_location: str = "space"  # "space" or planet name
    to_location: str = "space"  # "space" or planet name
    player_technologies: Optional[set[Technology]] = None
    transport_ship: Optional[Unit] = None  # For ground force transport


def _is_space_location(location: str) -> bool:
    """Check if a location string represents space."""
    return location == LocationType.SPACE.value


class MovementValidator:
    """Validates unit movement actions."""

    def __init__(
        self, galaxy: Galaxy, rule_engine: Optional[MovementRuleEngine] = None
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
    """Validates transport actions for ground forces."""

    def __init__(self, galaxy: Galaxy) -> None:
        """Initialize transport validator."""
        self._galaxy = galaxy

    def is_valid_transport(self, transport: TransportOperation) -> bool:
        """Check if a transport action is valid."""
        # Check if transport ship has capacity
        ship_capacity = transport.transport_ship.get_capacity()
        ground_force_count = len(transport.ground_forces)

        if ground_force_count > ship_capacity:
            return False

        # Check if all units are ground forces that can be transported
        from .constants import GameConstants

        transportable_types = GameConstants.GROUND_FORCE_TYPES
        for unit in transport.ground_forces:
            if unit.unit_type not in transportable_types:
                return False

        # Check if transport ship can move between systems
        from_coord = self._galaxy.get_system_coordinate(transport.from_system_id)
        to_coord = self._galaxy.get_system_coordinate(transport.to_system_id)

        if from_coord is None or to_coord is None:
            return False

        # Basic adjacency check (could be enhanced with movement rules)
        return (
            from_coord.distance_to(to_coord) <= transport.transport_ship.get_movement()
        )


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

    def can_transport_units(self, carrier: "Unit", units: list["Unit"]) -> bool:
        """Check if a carrier can transport the given units."""
        from .constants import GameConstants

        # Only infantry and mechs can be transported
        transportable_types = GameConstants.GROUND_FORCE_TYPES
        for unit in units:
            if unit.unit_type not in transportable_types:
                return False

        # Check capacity
        return len(units) <= carrier.get_capacity()

    def get_transportable_units(self, system: "System", player: str) -> list["Unit"]:
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

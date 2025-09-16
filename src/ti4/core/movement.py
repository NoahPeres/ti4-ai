"""Movement system for TI4 units."""

from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from .galaxy import Galaxy
from .movement_rules import MovementContext, MovementRuleEngine
from .system import System
from .unit import Unit


@dataclass
class MovementAction:
    """Represents a unit movement action."""

    unit: Unit
    from_system_id: str
    to_system_id: str
    player_id: str
    from_location: str = "space"  # "space" or planet name
    to_location: str = "space"  # "space" or planet name
    player_technologies: Optional[set[str]] = None
    transport_ship: Optional[Unit] = None  # For ground force transport


class MovementValidator:
    """Validates unit movement actions."""

    def __init__(
        self, galaxy: Galaxy, rule_engine: Optional[MovementRuleEngine] = None
    ):
        """Initialize the movement validator with a galaxy."""
        self._galaxy = galaxy
        self._rule_engine = rule_engine or MovementRuleEngine()

    def is_valid_movement(self, movement: MovementAction) -> bool:
        """Check if a movement action is valid."""
        # Use cached validation for performance
        tech_key = (
            frozenset(movement.player_technologies)
            if movement.player_technologies
            else frozenset()
        )
        return self._is_valid_movement_cached(
            movement.unit.unit_type,
            movement.from_system_id,
            movement.to_system_id,
            tech_key,
        )

    @lru_cache(maxsize=1000)
    def _is_valid_movement_cached(
        self,
        unit_type: str,
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
            player_technologies=set(technologies),
            galaxy=self._galaxy,
        )

        # Use rule engine to validate movement
        return self._rule_engine.can_move(context)


class MovementExecutor:
    """Executes unit movement actions."""

    def __init__(self, galaxy: Galaxy, systems: dict[str, System]):
        """Initialize the movement executor."""
        self._galaxy = galaxy
        self._systems = systems

    def execute_movement(self, movement: MovementAction) -> None:
        """Execute a movement action."""
        from_system = self._systems.get(movement.from_system_id)
        to_system = self._systems.get(movement.to_system_id)

        if from_system is None or to_system is None:
            from .exceptions import InvalidSystemError

            raise InvalidSystemError("Invalid system ID in movement")

        # Handle different movement types
        self._remove_unit_from_location(
            from_system, movement.unit, movement.from_location
        )
        self._place_unit_at_location(to_system, movement.unit, movement.to_location)

    def _remove_unit_from_location(
        self, system: System, unit: Unit, location: str
    ) -> None:
        """Remove unit from specified location (space or planet)."""
        if location == "space":
            system.remove_unit_from_space(unit)
        else:
            # Remove from planet
            system.remove_unit_from_planet(unit, location)

    def _place_unit_at_location(
        self, system: System, unit: Unit, location: str
    ) -> None:
        """Place unit at specified location (space or planet)."""
        if location == "space":
            system.place_unit_in_space(unit)
        else:
            # Place on planet
            system.place_unit_on_planet(unit, location)


@dataclass
class TransportAction:
    """Represents transporting ground forces with ships."""

    transport_ship: Unit
    ground_forces: list[Unit]
    from_system_id: str
    to_system_id: str
    from_location: str = "space"  # Where ground forces start
    to_location: str = "space"  # Where ground forces end up
    player_id: str = ""


class TransportValidator:
    """Validates transport actions for ground forces."""

    def __init__(self, galaxy: Galaxy):
        """Initialize transport validator."""
        self._galaxy = galaxy

    def is_valid_transport(self, transport: TransportAction) -> bool:
        """Check if a transport action is valid."""
        # Check if transport ship has capacity
        ship_capacity = transport.transport_ship.get_capacity()
        ground_force_count = len(transport.ground_forces)

        if ground_force_count > ship_capacity:
            return False

        # Check if all units are ground forces that can be transported
        transportable_types = {"infantry", "mech"}
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

    def __init__(self, systems: dict[str, System]):
        """Initialize transport executor."""
        self._systems = systems

    def execute_transport(self, transport: TransportAction) -> None:
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
        if from_location == "space":
            from_system.remove_unit_from_space(unit)
        else:
            from_system.remove_unit_from_planet(unit, from_location)

        # Place at destination
        if to_location == "space":
            to_system.place_unit_in_space(unit)
        else:
            to_system.place_unit_on_planet(unit, to_location)

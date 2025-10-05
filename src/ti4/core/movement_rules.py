"""Advanced movement rules for TI4."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .constants import Technology
from .dice import roll_dice
from .galaxy import Galaxy
from .hex_coordinate import HexCoordinate
from .unit import Unit

if TYPE_CHECKING:
    from .system import System


@dataclass
class GravityRiftDestructionResult:
    """Result of gravity rift destruction rolls."""

    units_destroyed: list[Unit]
    dice_results: list[int]
    surviving_units: list[Unit]


@dataclass
class MovementContext:
    """Context for movement validation including technologies and abilities."""

    unit: Unit
    from_coordinate: HexCoordinate
    to_coordinate: HexCoordinate
    player_technologies: set[Technology]
    galaxy: Galaxy
    path: list[HexCoordinate] | None = None
    active_system_coordinate: HexCoordinate | None = None


class MovementRule(ABC):
    """Abstract base class for movement rules."""

    @abstractmethod
    def can_move(self, context: MovementContext) -> bool:
        """Check if movement is allowed under this rule."""
        pass

    @abstractmethod
    def get_movement_range(self, unit: Unit, technologies: set[Technology]) -> int:
        """Get the movement range for a unit."""
        pass


class BasicMovementRule(MovementRule):
    """Basic movement rule - units can move up to their movement value."""

    def can_move(self, context: MovementContext) -> bool:
        """Check if movement is within basic movement range."""
        distance = context.from_coordinate.distance_to(context.to_coordinate)
        max_range = self.get_movement_range(context.unit, context.player_technologies)
        return distance <= max_range

    def get_movement_range(self, unit: Unit, technologies: set[Technology]) -> int:
        """Get basic movement range."""
        return unit.get_movement()


class GravityDriveRule(MovementRule):
    """Gravity Drive technology rule - increases movement by +1."""

    def can_move(self, context: MovementContext) -> bool:
        """Check if gravity drive allows this movement."""
        distance = context.from_coordinate.distance_to(context.to_coordinate)
        max_range = self.get_movement_range(context.unit, context.player_technologies)
        return distance <= max_range

    def get_movement_range(self, unit: Unit, technologies: set[Technology]) -> int:
        """Gravity drive adds +1 to movement range."""
        base_movement = unit.get_movement()
        if Technology.GRAVITY_DRIVE in technologies:
            return base_movement + 1
        return base_movement


class AnomalyRule(MovementRule):
    """Rule for handling movement through/around anomalies.

    Implements Rule 9: ANOMALIES movement restrictions:
    - Rule 11: Asteroid fields block all movement
    - Rule 86: Supernovas block all movement

    LRR References:
    - Rule 9: ANOMALIES - Core anomaly system
    - Rule 11: Asteroid Field - Movement blocking
    - Rule 86: Supernova - Movement blocking
    """

    def can_move(self, context: MovementContext) -> bool:
        """Check if movement is blocked by anomalies.

        Args:
            context: Movement context containing unit, coordinates, and galaxy

        Returns:
            False if movement is blocked by anomalies, True otherwise

        LRR References:
        - Rule 11: Ships cannot move into or through asteroid field systems
        - Rule 86: Ships cannot move into or through supernova systems
        - Rule 59.1: Ships can only move into nebula if it's the active system
        """
        # Check if destination system blocks movement
        if self._system_blocks_movement(context.to_coordinate, context.galaxy):
            return False

        # Check nebula movement restrictions (Rule 59.1)
        if self._system_has_nebula_restriction(
            context.to_coordinate, context.galaxy, context.active_system_coordinate
        ):
            return False

        # Check if any system in the path blocks movement
        if context.path:
            for coordinate in context.path:
                # Skip the starting coordinate (movement from is allowed)
                if coordinate == context.from_coordinate:
                    continue
                if self._system_blocks_movement(coordinate, context.galaxy):
                    return False
                # Check nebula restrictions for path systems
                if self._system_has_nebula_restriction(
                    coordinate, context.galaxy, context.active_system_coordinate
                ):
                    return False

        return True

    def _system_blocks_movement(
        self, coordinate: HexCoordinate, galaxy: Galaxy
    ) -> bool:
        """Check if a system at the given coordinate blocks movement.

        Args:
            coordinate: Coordinate to check
            galaxy: Galaxy containing the systems

        Returns:
            True if system blocks movement, False otherwise
        """
        # Find system at this coordinate
        for system_id, system_coord in galaxy.system_coordinates.items():
            if system_coord == coordinate:
                system = galaxy.get_system(system_id)
                if system:
                    return self._system_has_blocking_anomaly(system)
        return False

    def _system_has_blocking_anomaly(self, system: System) -> bool:
        """Check if a system has anomalies that block movement.

        Args:
            system: System to check for blocking anomalies

        Returns:
            True if system has blocking anomalies, False otherwise

        LRR References:
        - Rule 11: Asteroid fields block movement
        - Rule 86: Supernovas block movement
        """
        from .constants import AnomalyType

        # Check for movement-blocking anomaly types
        blocking_anomalies = {AnomalyType.ASTEROID_FIELD, AnomalyType.SUPERNOVA}

        for anomaly_type in system.get_anomaly_types():
            if anomaly_type in blocking_anomalies:
                return True

        return False

    def get_movement_range(self, unit: Unit, technologies: set[Technology]) -> int:
        """Anomalies don't change movement range."""
        return unit.get_movement()

    def get_movement_range_from_system(
        self, unit: Unit, technologies: set[Technology], system: System
    ) -> int:
        """Get movement range considering anomaly effects from starting system.

        Args:
            unit: The unit to get movement range for
            technologies: Player's technologies
            system: The system the unit is starting from

        Returns:
            Movement range considering anomaly effects

        LRR References:
        - Rule 59.2: Ships in nebula have move value 1
        """
        from .constants import AnomalyType

        # Check if starting from nebula system (Rule 59.2)
        if system.has_anomaly_type(AnomalyType.NEBULA):
            return 1

        return unit.get_movement()

    def _system_has_nebula_restriction(
        self,
        coordinate: HexCoordinate,
        galaxy: Galaxy,
        active_system_coordinate: HexCoordinate | None,
    ) -> bool:
        """Check if a system has nebula that restricts movement.

        Args:
            coordinate: Coordinate to check
            galaxy: Galaxy containing the systems
            active_system_coordinate: Coordinate of the active system (if any)

        Returns:
            True if system has nebula that blocks movement, False otherwise

        LRR References:
        - Rule 59.1: Ships can only move into nebula if it's the active system
        """
        from .constants import AnomalyType

        # Find system at this coordinate
        for system_id, system_coord in galaxy.system_coordinates.items():
            if system_coord == coordinate:
                system = galaxy.get_system(system_id)
                if system and system.has_anomaly_type(AnomalyType.NEBULA):
                    # Nebula blocks movement unless it's the active system
                    return coordinate != active_system_coordinate
        return False

    def get_movement_range_with_gravity_rift_bonus(
        self, unit: Unit, technologies: set[Technology], system: System
    ) -> int:
        """Get movement range with gravity rift bonus when exiting system.

        Args:
            unit: The unit to get movement range for
            technologies: Player's technologies
            system: The system the unit is exiting from

        Returns:
            Movement range with gravity rift bonus applied

        LRR References:
        - Rule 41: Gravity Rift - Movement bonuses when exiting
        """
        from .constants import AnomalyType

        base_movement = unit.get_movement()

        # Apply gravity rift bonus if exiting from gravity rift system
        if system.has_anomaly_type(AnomalyType.GRAVITY_RIFT):
            return base_movement + 1

        return base_movement

    def get_effective_movement_range_for_path(self, context: MovementContext) -> int:
        """Get effective movement range considering gravity rift bonuses in path.

        Args:
            context: Movement context containing path information

        Returns:
            Effective movement range with all gravity rift bonuses applied

        LRR References:
        - Rule 41: Gravity Rift - Movement bonuses when passing through
        """
        from .constants import AnomalyType

        base_movement = context.unit.get_movement()
        gravity_rift_bonuses = 0

        if context.path:
            # Count gravity rifts in the path (excluding destination)
            for coordinate in context.path[:-1]:  # Exclude destination
                for (
                    system_id,
                    system_coord,
                ) in context.galaxy.system_coordinates.items():
                    if system_coord == coordinate:
                        system = context.galaxy.get_system(system_id)
                        if system and system.has_anomaly_type(AnomalyType.GRAVITY_RIFT):
                            gravity_rift_bonuses += 1
                        break

        return base_movement + gravity_rift_bonuses

    def check_gravity_rift_destruction(self, unit: Unit, roll_value: int) -> bool:
        """Check if a unit is destroyed by gravity rift based on dice roll.

        Args:
            unit: The unit to check for destruction
            roll_value: The dice roll result (1-10)

        Returns:
            True if unit is destroyed, False if it survives

        Raises:
            ValueError: If roll_value is not in valid range (1-10)

        LRR References:
        - Rule 41: Gravity Rift - Destruction on rolls 1-3, survival on 4-10
        """
        # Normalize roll_value from 0-9 range to 1-10 range
        normalized_roll = roll_value if roll_value != 0 else 10

        if not 1 <= normalized_roll <= 10:
            raise ValueError(
                f"Invalid dice roll value: {normalized_roll}. Must be between 1 and 10."
            )

        return normalized_roll <= 3

    def apply_gravity_rift_destruction(
        self, context: MovementContext
    ) -> GravityRiftDestructionResult:
        """Apply gravity rift destruction rolls for movement.

        Args:
            context: Movement context containing unit and path information

        Returns:
            Result containing destroyed units and dice results

        LRR References:
        - Rule 41: Gravity Rift - Destruction rolls when exiting/passing through
        """
        from .constants import AnomalyType

        units_to_roll = [context.unit]
        gravity_rift_count = 0

        # Count gravity rifts that affect this movement
        if context.path:
            # Check each system in path for gravity rifts
            for coordinate in context.path:
                # Skip the starting coordinate (no roll for entering)
                if coordinate == context.from_coordinate:
                    continue

                for (
                    system_id,
                    system_coord,
                ) in context.galaxy.system_coordinates.items():
                    if system_coord == coordinate:
                        system = context.galaxy.get_system(system_id)
                        if system and system.has_anomaly_type(AnomalyType.GRAVITY_RIFT):
                            gravity_rift_count += 1
                        break
        else:
            # Direct movement - check if exiting from gravity rift
            for system_id, system_coord in context.galaxy.system_coordinates.items():
                if system_coord == context.from_coordinate:
                    system = context.galaxy.get_system(system_id)
                    if system and system.has_anomaly_type(AnomalyType.GRAVITY_RIFT):
                        gravity_rift_count += 1
                    break

        # Roll dice for each gravity rift effect
        dice_results = roll_dice(gravity_rift_count)
        units_destroyed = []
        surviving_units = []

        for unit in units_to_roll:
            unit_destroyed = False
            for roll_result in dice_results:
                if self.check_gravity_rift_destruction(unit, roll_result):
                    unit_destroyed = True
                    break

            if unit_destroyed:
                units_destroyed.append(unit)
            else:
                surviving_units.append(unit)

        return GravityRiftDestructionResult(
            units_destroyed=units_destroyed,
            dice_results=dice_results,
            surviving_units=surviving_units,
        )


class MovementRuleEngine:
    """Engine that applies multiple movement rules."""

    def __init__(self) -> None:
        """Initialize with default movement rules."""
        self.rules: list[MovementRule] = [
            BasicMovementRule(),
            GravityDriveRule(),
            AnomalyRule(),
        ]

    def add_rule(self, rule: MovementRule) -> None:
        """Add a custom movement rule."""
        self.rules.append(rule)

    def can_move(self, context: MovementContext) -> bool:
        """Check if movement is valid considering maximum movement range."""
        distance = context.from_coordinate.distance_to(context.to_coordinate)
        max_range = self.get_max_movement_range(
            context.unit, context.player_technologies
        )
        return distance <= max_range

    def get_max_movement_range(self, unit: Unit, technologies: set[Technology]) -> int:
        """Get the maximum movement range considering all rules."""
        # Take the maximum range from all applicable rules
        return max(rule.get_movement_range(unit, technologies) for rule in self.rules)

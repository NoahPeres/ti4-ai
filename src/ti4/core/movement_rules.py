"""Advanced movement rules for TI4."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from .constants import Technology
from .galaxy import Galaxy
from .hex_coordinate import HexCoordinate
from .unit import Unit


@dataclass
class MovementContext:
    """Context for movement validation including technologies and abilities."""

    unit: Unit
    from_coordinate: HexCoordinate
    to_coordinate: HexCoordinate
    player_technologies: set[Technology]
    galaxy: Galaxy
    path: list[HexCoordinate] | None = None


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
    """Rule for handling movement through/around anomalies."""

    def can_move(self, context: MovementContext) -> bool:
        """Check if movement is blocked by anomalies."""
        # This would check for nebulae, asteroid fields, etc.
        # For now, simplified implementation
        return True

    def get_movement_range(self, unit: Unit, technologies: set[Technology]) -> int:
        """Anomalies don't change movement range."""
        return unit.get_movement()


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

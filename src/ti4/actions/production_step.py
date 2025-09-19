"""Production step for tactical actions implementing Rule 67.3.

This module implements the production step that occurs during tactical actions,
following Rule 67.3: Production during tactical action.
"""

from typing import TYPE_CHECKING, Any

from ..core.constants import UnitType
from ..core.production import ProductionManager
from .movement_engine import TacticalActionStep

if TYPE_CHECKING:
    from ..core.system import System
    from ..core.unit import Unit


class ProductionStep(TacticalActionStep):
    """Production step for tactical actions.

    Implements Rule 67.3: Production during tactical action follows Production ability rules
    for placement in active system.
    """

    def __init__(self) -> None:
        """Initialize the production step."""
        self._production_manager = ProductionManager()

    def can_execute(self, game_state: Any, context: dict[str, Any]) -> bool:
        """Check if production can be executed in the current context.

        Args:
            game_state: The current game state
            context: Context containing system and player information

        Returns:
            True if the player has production units in the system

        LRR Reference: Rule 67.3 - Production during tactical action
        """
        system = context.get("system")
        player_id = context.get("player_id")

        if not system or not player_id:
            return False

        # Check if player has any production units in the system
        for planet in system.planets:
            for unit in planet.units:
                if unit.owner == player_id and self._has_production_ability(unit):
                    return True
        return False

    def execute(self, game_state: Any, context: dict[str, Any]) -> Any:
        """Execute the production step.

        Args:
            game_state: The current game state
            context: Context containing system and player information

        Returns:
            The updated game state

        LRR Reference: Rule 67.3 - Production follows Production ability rules
        """
        # In a full implementation, this would:
        # 1. Calculate total production capacity in the system
        # 2. Allow player to spend resources to produce units
        # 3. Place produced units in the system
        # 4. Validate against reinforcement limits
        # 5. Apply blockade restrictions

        # For now, minimal implementation just validates the system has production
        if self.can_execute(game_state, context):
            return game_state
        return game_state

    def get_step_name(self) -> str:
        """Get the name of this step for logging/debugging.

        Returns:
            The name of this step
        """
        return "Production"

    def can_execute_legacy(self, system: "System", player_id: str) -> bool:
        """Legacy method for backward compatibility.

        Args:
            system: The active system for the tactical action
            player_id: The player executing the tactical action

        Returns:
            True if the player has production units in the system
        """
        context = {"system": system, "player_id": player_id}
        return self.can_execute(None, context)

    def _has_production_ability(self, unit: "Unit") -> bool:
        """Check if a unit has production ability.

        Args:
            unit: The unit to check

        Returns:
            True if unit has production ability
        """
        # Space docks have production ability
        return bool(unit.unit_type == UnitType.SPACE_DOCK)

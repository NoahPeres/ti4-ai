"""Basic public objective implementations for TI4."""

from typing import TYPE_CHECKING

from .game_phase import GamePhase
from .objective import CompletableObjective, Objective

if TYPE_CHECKING:
    from .game_state import GameState


class ControlPlanetsObjective(CompletableObjective):
    """Objective for controlling a certain number of planets."""

    def __init__(self) -> None:
        self._objective = Objective(
            id="control_planets",
            name="Control Planets",
            description="Control 6 planets",
            points=1,
            is_public=True,
            scoring_phase=GamePhase.STATUS
        )

    def get_objective(self) -> Objective:
        """Get the underlying Objective data."""
        return self._objective

    def is_completed_by(self, game_state: "GameState", player_id: str) -> bool:
        """Check if this objective is completed by the given player."""
        # For now, return False - we need to implement planet control tracking
        return False


class SpendResourcesObjective(CompletableObjective):
    """Objective for spending resources."""

    def __init__(self) -> None:
        self._objective = Objective(
            id="spend_resources",
            name="Spend Resources",
            description="Spend 8 resources",
            points=1,
            is_public=True,
            scoring_phase=GamePhase.STATUS
        )

    def get_objective(self) -> Objective:
        """Get the underlying Objective data."""
        return self._objective

    def is_completed_by(self, game_state: "GameState", player_id: str) -> bool:
        """Check if this objective is completed by the given player."""
        # For now, return False - we need to implement resource spending tracking
        return False

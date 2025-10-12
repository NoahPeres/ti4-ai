"""
Custodians Token Implementation for TI4 AI

This module implements Rule 27: CUSTODIANS TOKEN mechanics according to the LRR.

Key Components:
- CustodiansToken: Main token entity with state management
- TokenRemovalResult: Result of token removal attempts
- Integration with planet system, influence system, and victory points
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .unit import Unit


@dataclass
class TokenRemovalResult:
    """Result of custodians token removal attempt."""

    success: bool
    error_message: str = ""
    victory_points_awarded: int = 0
    agenda_phase_activated: bool = False


class CustodiansToken:
    """
    Manages the custodians token state and removal mechanics.

    LRR 27: The custodians token begins the game on Mecatol Rex and prevents
    players from landing ground forces on that planet until removed.
    """

    def __init__(self) -> None:
        """Initialize custodians token on Mecatol Rex."""
        self.location = "mecatol_rex"
        self._on_mecatol_rex = True

    def is_on_mecatol_rex(self) -> bool:
        """Check if custodians token is on Mecatol Rex."""
        return self._on_mecatol_rex

    def remove_from_mecatol_rex(self) -> bool:
        """Basic token removal (for backward compatibility)."""
        if self._on_mecatol_rex:
            self._on_mecatol_rex = False
            return True
        return False

    def can_be_removed_by_player(self, player_id: str, game_state: Any) -> bool:
        """
        Check if player can remove custodians token.

        LRR 27.2: A player can remove the custodians token from Mecatol Rex by
        spending six influence while they have one or more ships in the Mecatol Rex system.
        """
        # Check if token is still on Mecatol Rex
        if not self.is_on_mecatol_rex():
            return False

        # Check if player has sufficient influence (6 required)
        available_influence = game_state.get_player_available_influence(player_id)
        if available_influence < 6:
            return False

        # Check if player has ships in Mecatol Rex system
        has_ships = game_state.player_has_ships_in_system(player_id, "mecatol_rex")
        if not has_ships:
            return False

        return True

    def remove_with_ground_force_commitment(
        self, player_id: str, ground_force: Unit | None, game_state: Any
    ) -> TokenRemovalResult:
        """
        Remove custodians token with ground force commitment.

        LRR 27.2a: When a player removes the custodians token, they must commit
        at least one ground force to land on Mecatol Rex.

        LRR 27.3: When a player removes the custodians token, they gain one victory point.

        LRR 27.4: After a player removes the custodians token, the agenda phase
        is added to each game round.
        """
        # Check if token can be removed (Rule 27.2 requirements)
        if not self.can_be_removed_by_player(player_id, game_state):
            return TokenRemovalResult(
                success=False,
                error_message="Player does not meet requirements to remove custodians token",
            )

        # Check ground force commitment requirement (Rule 27.2a)
        if ground_force is None:
            return TokenRemovalResult(
                success=False,
                error_message="Must commit at least one ground force to remove custodians token",
            )

        # Validate ground force ownership
        if ground_force.owner != player_id:
            return TokenRemovalResult(
                success=False, error_message="Ground force must be owned by the player"
            )

        # Remove the token from Mecatol Rex
        self.remove_from_mecatol_rex()

        # Award victory point (Rule 27.3)
        game_state.award_victory_points(player_id, 1)

        # Activate agenda phase (Rule 27.4)
        game_state.activate_agenda_phase()

        return TokenRemovalResult(
            success=True, victory_points_awarded=1, agenda_phase_activated=True
        )

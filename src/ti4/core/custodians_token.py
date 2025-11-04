"""
Custodians Token Implementation for TI4 AI

This module implements Rule 27: CUSTODIANS TOKEN mechanics according to the LRR.

Key Components:
- CustodiansToken: Main token entity with state management
- TokenRemovalResult: Result of token removal attempts
- Integration with planet system, influence system, and victory points
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .unit import Unit


logger = logging.getLogger(__name__)


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

    def remove_from_mecatol_rex(self, player_id: str | None = None) -> bool:
        """Basic token removal (for backward compatibility)."""
        if self._on_mecatol_rex:
            self._on_mecatol_rex = False
            self.location = "removed"  # Update location field for consistency
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
        try:
            available_influence = game_state.get_player_available_influence(player_id)
        except AttributeError:
            # Fallback to ResourceManager if GameState wrapper is missing
            from .resource_management import ResourceManager

            resource_manager = ResourceManager(game_state)
            available_influence = resource_manager.calculate_available_influence(
                player_id, for_voting=False
            )

        if available_influence < 6:
            return False

        # Check if player has ships in Mecatol Rex system
        try:
            from .constants import SystemConstants

            has_ships = game_state.player_has_ships_in_system(
                player_id, SystemConstants.MECATOL_REX_ID
            )
        except AttributeError:
            # Fallback: check directly via system state
            from .constants import SystemConstants
            from .ships import ShipManager

            system = game_state.systems.get(SystemConstants.MECATOL_REX_ID)
            if system is None:
                return False
            ship_manager = ShipManager()
            has_ships = any(
                unit.owner == player_id and ship_manager.is_ship(unit)
                for unit in system.get_units_in_space()
            )

        if not has_ships:
            return False

        return True

    def remove_with_ground_force_commitment(
        self, player_id: str, ground_force: Unit | None, game_state: Any
    ) -> tuple[TokenRemovalResult, Any]:
        """
        Remove custodians token with ground force commitment.

        LRR 27.2a: When a player removes the custodians token, they must commit
        at least one ground force to land on Mecatol Rex.

        LRR 27.3: When a player removes the custodians token, they gain one victory point.

        LRR 27.4: After a player removes the custodians token, the agenda phase
        is added to each game round.

        Returns:
            Tuple of (TokenRemovalResult, updated GameState)
        """
        # Check if token can be removed (Rule 27.2 requirements)
        if not self.can_be_removed_by_player(player_id, game_state):
            return (
                TokenRemovalResult(
                    success=False,
                    error_message="Player does not meet requirements to remove custodians token",
                ),
                game_state,
            )

        # Check ground force commitment requirement (Rule 27.2a)
        if ground_force is None:
            return (
                TokenRemovalResult(
                    success=False,
                    error_message="Must commit at least one ground force to remove custodians token",
                ),
                game_state,
            )

        # Validate ground force ownership
        if ground_force.owner != player_id:
            return (
                TokenRemovalResult(
                    success=False,
                    error_message="Ground force must be owned by the player",
                ),
                game_state,
            )

        # Spend six influence using ResourceManager (planets and trade goods allowed)
        from .constants import SystemConstants
        from .resource_management import ResourceManager

        resource_manager = ResourceManager(game_state)

        # Create spending plan for 6 influence (not a voting context)
        spending_plan = resource_manager.create_spending_plan(
            player_id=player_id, resource_amount=0, influence_amount=6, for_voting=False
        )

        # Validate plan before attempting execution
        if not getattr(spending_plan, "is_valid", False):
            return (
                TokenRemovalResult(
                    success=False,
                    error_message=(
                        getattr(spending_plan, "error_message", None)
                        or "Invalid spending plan: insufficient or unusable influence to remove custodians token (need 6)"
                    ),
                ),
                game_state,
            )

        spending_result = resource_manager.execute_spending_plan(spending_plan)
        if not spending_result.success:
            return (
                TokenRemovalResult(
                    success=False,
                    error_message=(
                        spending_result.error_message
                        or "Failed to spend influence to remove custodians token"
                    ),
                ),
                game_state,
            )

        # Remove the token from Mecatol Rex
        self.remove_from_mecatol_rex()

        # Place the committed ground force on Mecatol Rex (now allowed)
        system = game_state.systems.get(SystemConstants.MECATOL_REX_ID)
        if system is not None:
            try:
                system.place_unit_on_planet(ground_force, "Mecatol Rex")
            except Exception:
                # Non-fatal: landing failure should not rollback token removal or VP
                logger.exception(
                    "Failed to place ground force on Mecatol Rex during custodians token removal"
                )

        # Award victory point (Rule 27.3) and activate agenda phase (Rule 27.4)
        new_state = game_state.award_victory_points(player_id, 1)
        new_state = new_state.activate_agenda_phase()

        # Create and log event for custodians token removal
        try:
            from .events import create_custodians_token_removed_event
            from .logging import GameLogger

            ground_force_id = getattr(ground_force, "id", None)
            removal_event = create_custodians_token_removed_event(
                game_id=new_state.game_id,
                player_id=player_id,
                influence_spent=6,
                system_id=SystemConstants.MECATOL_REX_ID,
                ground_force_id=str(ground_force_id) if ground_force_id else None,
                victory_points_awarded=1,
                agenda_phase_activated=True,
            )
            # Log via GameLogger. If an event bus is used by the controller,
            # observers will also receive PHASE_CHANGED during round transition.
            GameLogger(new_state.game_id).log_event(removal_event.to_game_event())
        except Exception:
            # Defensive: logging should not interfere with game flow
            logger.exception("Failed to log CustodiansTokenRemovedEvent via GameLogger")

        return (
            TokenRemovalResult(
                success=True, victory_points_awarded=1, agenda_phase_activated=True
            ),
            new_state,
        )

"""
Classified Document Leaks directive card implementation.

This module implements the Classified Document Leaks agenda card from the base game.
"""

from typing import TYPE_CHECKING, Any

from ..base.directive_card import DirectiveCard

if TYPE_CHECKING:
    from ...agenda_phase import VoteResult
    from ...game_state import GameState
    from ..effect_resolver import AgendaResolutionResult


class ClassifiedDocumentLeaks(DirectiveCard):
    """
    Classified Document Leaks directive card.

    When revealed: If no scored secret objectives, discard and reveal another.
    Elect Scored Secret Objective: The elected secret objective becomes public.
    """

    def __init__(self) -> None:
        """Initialize the Classified Document Leaks card."""
        super().__init__("Classified Document Leaks")

    def get_voting_outcomes(self) -> list[str]:
        """Get possible voting outcomes for this agenda."""
        return ["Elect Scored Secret Objective"]

    def should_discard_on_reveal(self, game_state: "GameState") -> bool:
        """Check if card should be discarded when revealed."""
        # The card should only be discarded if NO secret objectives have been scored
        # If any secret objectives exist (completed or in hand), keep the card

        # Check completed objectives (scored objectives)
        if (
            hasattr(game_state, "completed_objectives")
            and game_state.completed_objectives
        ):
            # Check if any player has completed any objectives (which could include secret objectives)
            for completed_objectives in game_state.completed_objectives.values():
                if completed_objectives:  # If any player has completed objectives
                    return False

        # Check player secret objectives (objectives in hand that could be scored)
        if (
            hasattr(game_state, "player_secret_objectives")
            and game_state.player_secret_objectives
        ):
            # Check if any player has secret objectives that could be scored
            for secret_objectives in game_state.player_secret_objectives.values():
                secret_objectives_list: Any = secret_objectives  # Type hint for mypy
                if secret_objectives_list:  # If any player has secret objectives
                    return False

        # If no objectives exist (completed or in hand), discard the card
        return True

    def resolve_outcome(
        self, outcome: str, vote_result: "VoteResult", game_state: "GameState"
    ) -> "AgendaResolutionResult":
        """Resolve the agenda based on voting outcome."""
        from ..effect_resolver import AgendaResolutionResult

        # Validate outcome
        if outcome not in self.get_voting_outcomes():
            raise ValueError(f"Invalid voting outcome: {outcome}")

        # Validate elected target
        if vote_result.elected_target is None:
            raise ValueError("No target elected for Classified Document Leaks")

        # Execute the directive effect
        elected_objective = vote_result.elected_target

        # Create resolution result
        return AgendaResolutionResult(
            success=True,
            directive_executed=True,
            description=f"Secret objective '{elected_objective}' is now public",
            elected_target=elected_objective,
        )

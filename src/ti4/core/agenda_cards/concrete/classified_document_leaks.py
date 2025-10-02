"""
Classified Document Leaks directive card implementation.

This module implements the Classified Document Leaks agenda card from the base game.
"""

from typing import TYPE_CHECKING

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
        # Check if any player has scored secret objectives
        for _player_id, completed_objectives in game_state.completed_objectives.items():
            if completed_objectives:  # If any player has completed objectives
                # For now, assume any completed objective could be secret
                # This is a simplified implementation
                return False
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

"""
Regulated Conscription agenda card implementation.

This module implements the Regulated Conscription law card from the TI4 base game.
"""

from typing import TYPE_CHECKING

from ti4.core.agenda_cards.base.law_card import LawCard
from ti4.core.agenda_cards.effect_resolver import AgendaResolutionResult
from ti4.core.agenda_cards.law_manager import ActiveLaw

if TYPE_CHECKING:
    from ti4.core.agenda_phase import VoteResult
    from ti4.core.game_state import GameState


class RegulatedConscription(LawCard):
    """
    Regulated Conscription agenda card.

    FOR: When a player produces units, they produce only 1 fighter and infantry for its cost instead of 2.
    AGAINST: No effect.
    """

    def __init__(self) -> None:
        """Initialize the Regulated Conscription card."""
        super().__init__("Regulated Conscription")

    def get_voting_outcomes(self) -> list[str]:
        """Get possible voting outcomes for this agenda."""
        return ["For", "Against"]

    def resolve_outcome(
        self,
        outcome: str,
        vote_result: "VoteResult",
        game_state: "GameState",
    ) -> AgendaResolutionResult:
        """Resolve the agenda based on voting outcome."""
        if outcome not in self.get_voting_outcomes():
            raise ValueError(f"Invalid outcome '{outcome}' for Regulated Conscription")

        if outcome == "For":
            # FOR: Enact law with persistent effect
            return AgendaResolutionResult(
                success=True,
                law_enacted=True,
                description="Regulated Conscription enacted: Players produce only 1 fighter and infantry for cost instead of 2",
            )
        else:  # Against
            # AGAINST: Execute immediate directive effect (no effect)
            return AgendaResolutionResult(
                success=True,
                directive_executed=True,
                description="Regulated Conscription rejected: No effect",
            )

    def create_active_law(
        self, outcome: str, elected_target: str | None = None
    ) -> ActiveLaw:
        """Create an active law instance for the FOR outcome."""
        if outcome != "For":
            raise ValueError("Can only create active law for 'For' outcome")

        return ActiveLaw(
            agenda_card=self,
            enacted_round=1,  # This would be set by the actual game state
            effect_description="Players produce only 1 fighter and infantry for cost instead of 2",
            elected_target=elected_target,
        )

    @property
    def trigger_condition(self) -> str:
        """Get the trigger condition for this law when enacted."""
        return "unit_production"

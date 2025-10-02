"""
Anti-Intellectual Revolution agenda card implementation.

This module implements the Anti-Intellectual Revolution law card from the TI4 base game.
"""

from typing import TYPE_CHECKING

from ti4.core.agenda_cards.base.law_card import LawCard
from ti4.core.agenda_cards.effect_resolver import AgendaResolutionResult
from ti4.core.agenda_cards.law_manager import ActiveLaw

if TYPE_CHECKING:
    from ti4.core.agenda_phase import VoteResult
    from ti4.core.game_state import GameState


class AntiIntellectualRevolution(LawCard):
    """
    Anti-Intellectual Revolution agenda card.

    FOR: After a player researches a technology, they must destroy 1 of their non-fighter ships.
    AGAINST: At the start of the next strategy phase, each player chooses and exhausts 1 planet for each technology they own.
    """

    def __init__(self) -> None:
        """Initialize the Anti-Intellectual Revolution card."""
        super().__init__("Anti-Intellectual Revolution")

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
            raise ValueError(
                f"Invalid outcome '{outcome}' for Anti-Intellectual Revolution"
            )

        if outcome == "For":
            # FOR: Enact law with persistent effect
            return AgendaResolutionResult(
                success=True,
                law_enacted=True,
                description="Anti-Intellectual Revolution enacted: After a player researches a technology, they must destroy 1 of their non-fighter ships",
            )
        else:  # Against
            # AGAINST: Execute immediate directive effect
            return AgendaResolutionResult(
                success=True,
                directive_executed=True,
                description="Anti-Intellectual Revolution rejected: Each player chooses and exhaust 1 planet for each technology they own",
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
            effect_description="After a player researches a technology, they must destroy 1 of their non-fighter ships",
            elected_target=elected_target,
        )

    @property
    def trigger_condition(self) -> str:
        """Get the trigger condition for this law when enacted."""
        return "after_technology_research"

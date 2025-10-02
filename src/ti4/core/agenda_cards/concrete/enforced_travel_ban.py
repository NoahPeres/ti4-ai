"""
Enforced Travel Ban agenda card implementation.

This module implements the Enforced Travel Ban law card from the TI4 base game.
"""

from typing import TYPE_CHECKING

from ti4.core.agenda_cards.base.law_card import LawCard
from ti4.core.agenda_cards.effect_resolver import AgendaResolutionResult
from ti4.core.agenda_cards.law_manager import ActiveLaw

if TYPE_CHECKING:
    from ti4.core.agenda_phase import VoteResult
    from ti4.core.game_state import GameState


class EnforcedTravelBan(LawCard):
    """
    Enforced Travel Ban agenda card.

    FOR: Alpha and beta wormholes have no effect during movement.
    AGAINST: Each player gains 1 command token in their strategy pool.
    """

    def __init__(self) -> None:
        """Initialize the Enforced Travel Ban card."""
        super().__init__("Enforced Travel Ban")

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
            raise ValueError(f"Invalid outcome '{outcome}' for Enforced Travel Ban")

        if outcome == "For":
            # FOR: Enact law with persistent effect
            return AgendaResolutionResult(
                success=True,
                law_enacted=True,
                description="Enforced Travel Ban enacted: Alpha and beta wormholes have no effect during movement",
            )
        else:  # Against
            # AGAINST: Execute immediate directive effect
            return AgendaResolutionResult(
                success=True,
                directive_executed=True,
                description="Enforced Travel Ban rejected: Each player gains 1 command token in their strategy pool",
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
            effect_description="Alpha and beta wormholes have no effect during movement",
            elected_target=elected_target,
        )

    @property
    def trigger_condition(self) -> str:
        """Get the trigger condition for this law when enacted."""
        return "movement"

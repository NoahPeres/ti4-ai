"""
Wormhole Reconstruction agenda card implementation.

This module implements the Wormhole Reconstruction law card from the TI4 base game.
"""

from typing import TYPE_CHECKING

from ti4.core.agenda_cards.base.law_card import LawCard
from ti4.core.agenda_cards.effect_resolver import AgendaResolutionResult
from ti4.core.agenda_cards.law_manager import ActiveLaw

if TYPE_CHECKING:
    from ti4.core.agenda_phase import VoteResult
    from ti4.core.game_state import GameState


class WormholeReconstruction(LawCard):
    """
    Wormhole Reconstruction agenda card.

    FOR: All systems that contain either an alpha or beta wormhole are adjacent to each other.
    AGAINST: Each player places a command token from their reinforcements in each system that contains a wormhole and 1 or more of their ships.
    """

    def __init__(self) -> None:
        """Initialize the Wormhole Reconstruction card."""
        super().__init__("Wormhole Reconstruction")

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
            raise ValueError(f"Invalid outcome '{outcome}' for Wormhole Reconstruction")

        if outcome == "For":
            # FOR: Enact law with persistent effect
            return AgendaResolutionResult(
                success=True,
                law_enacted=True,
                description="Wormhole Reconstruction enacted: All wormhole systems are adjacent to each other",
            )
        else:  # Against
            # AGAINST: Execute immediate directive effect
            return AgendaResolutionResult(
                success=True,
                directive_executed=True,
                description="Wormhole Reconstruction rejected: Players place command tokens in wormhole systems with ships",
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
            effect_description="All wormhole systems are adjacent to each other",
            elected_target=elected_target,
        )

    @property
    def trigger_condition(self) -> str:
        """Get the trigger condition for this law when enacted."""
        return "wormhole_adjacency"

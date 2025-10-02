"""
Publicize Weapon Schematics agenda card implementation.

This module implements the Publicize Weapon Schematics law card from the TI4 base game.
"""

from typing import TYPE_CHECKING

from ti4.core.agenda_cards.base.law_card import LawCard
from ti4.core.agenda_cards.effect_resolver import AgendaResolutionResult
from ti4.core.agenda_cards.law_manager import ActiveLaw

if TYPE_CHECKING:
    from ti4.core.agenda_phase import VoteResult
    from ti4.core.game_state import GameState


class PublicizeWeaponSchematics(LawCard):
    """
    Publicize Weapon Schematics agenda card.

    FOR: If any player owns a war sun technology, all players may ignore all prerequisites on war sun technologies. All war suns lose SUSTAIN DAMAGE.
    AGAINST: Each player that owns a war sun technology discards all of their action cards.
    """

    def __init__(self) -> None:
        """Initialize the Publicize Weapon Schematics card."""
        super().__init__("Publicize Weapon Schematics")

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
                f"Invalid outcome '{outcome}' for Publicize Weapon Schematics"
            )

        if outcome == "For":
            # FOR: Enact law with persistent effect
            return AgendaResolutionResult(
                success=True,
                law_enacted=True,
                description="Publicize Weapon Schematics enacted: All players may ignore war sun prerequisites, war suns lose sustain damage",
            )
        else:  # Against
            # AGAINST: Execute immediate directive effect
            return AgendaResolutionResult(
                success=True,
                directive_executed=True,
                description="Publicize Weapon Schematics rejected: Players with war sun technology discard all action cards",
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
            effect_description="All players may ignore war sun prerequisites, war suns lose sustain damage",
            elected_target=elected_target,
        )

    @property
    def trigger_condition(self) -> str:
        """Get the trigger condition for this law when enacted."""
        return "war_sun_technology"

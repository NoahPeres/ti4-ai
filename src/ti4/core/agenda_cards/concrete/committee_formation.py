"""
Committee Formation directive card implementation.

This module implements the Committee Formation agenda card from the base game.
"""

from typing import TYPE_CHECKING

from ..base.directive_card import DirectiveCard

if TYPE_CHECKING:
    from ...agenda_phase import VoteResult
    from ...game_state import GameState
    from ..effect_resolver import AgendaResolutionResult


class CommitteeFormation(DirectiveCard):
    """
    Committee Formation directive card.

    Before players vote on an agenda that requires a player to be elected:
    The owner of this card may discard this card to choose a player to be elected.
    Players do not vote on that agenda.
    """

    def __init__(self) -> None:
        """Initialize the Committee Formation card."""
        super().__init__("Committee Formation")
        self._is_discarded = False

    def get_voting_outcomes(self) -> list[str]:
        """Get possible voting outcomes for this agenda."""
        # Committee Formation doesn't have traditional voting outcomes since it bypasses voting
        return []

    def can_bypass_election_agenda(self, outcome: str, game_state: "GameState") -> bool:
        """Check if Committee Formation can bypass election agendas."""
        return self.is_election_outcome(outcome)

    def is_election_outcome(self, outcome: str) -> bool:
        """Check if an outcome is an election outcome."""
        election_outcomes = [
            "Elect Player",
            "Elect Cultural Planet",
            "Elect Industrial Planet",
            "Elect Hazardous Planet",
            "Elect Scored Secret Objective",
        ]
        return outcome in election_outcomes

    def get_trigger_timing(self) -> str:
        """Get the trigger timing for this card."""
        return "before_voting"

    def is_discarded(self) -> bool:
        """Check if the card has been discarded."""
        return self._is_discarded

    def bypass_election_agenda(
        self, chosen_player: str, game_state: "GameState"
    ) -> "AgendaResolutionResult":
        """Bypass election agenda with chosen player."""
        from ..effect_resolver import AgendaResolutionResult

        if chosen_player is None:
            raise ValueError("Cannot elect None player")

        if not chosen_player or chosen_player.strip() == "":
            raise ValueError("Cannot elect empty player name")

        return AgendaResolutionResult(
            success=True,
            directive_executed=True,
            elected_target=chosen_player,
            description=f"Committee Formation: {chosen_player} elected without voting",
        )

    def use_bypass_ability(
        self, chosen_player: str, game_state: "GameState"
    ) -> "AgendaResolutionResult":
        """Use the bypass ability and discard the card."""
        if self._is_discarded:
            raise ValueError("Committee Formation has already been used")

        result = self.bypass_election_agenda(chosen_player, game_state)
        self._is_discarded = True
        return result

    def resolve_outcome(
        self, outcome: str, vote_result: "VoteResult", game_state: "GameState"
    ) -> "AgendaResolutionResult":
        """Resolve the agenda based on voting outcome."""
        # Committee Formation typically bypasses normal resolution
        # This method is here for interface compliance
        from ..effect_resolver import AgendaResolutionResult

        return AgendaResolutionResult(
            success=False,
            directive_executed=False,
            description="Committee Formation should bypass normal voting resolution",
        )

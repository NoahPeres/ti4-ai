"""Crown directive card implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ti4.core.agenda_cards.base.directive_card import DirectiveCard
from ti4.core.constants import AgendaType

if TYPE_CHECKING:
    from ti4.core.game_state import GameState


class Crown(DirectiveCard):
    """Crown directive card.

    LRR Reference: Rule 7 - Agenda Cards
    """

    def __init__(self) -> None:
        """Initialize Crown directive card."""
        super().__init__("Crown")

    def get_agenda_type(self) -> AgendaType:
        """Return the agenda type."""
        return AgendaType.DIRECTIVE

    def get_voting_outcomes(self) -> list[str]:
        """Return valid voting outcomes for this card."""
        return ["For", "Against"]

    def execute_directive_effect(self, game_state: GameState, outcome: str) -> bool:
        """Execute the directive effect.

        Args:
            game_state: Current game state
            outcome: Voting outcome

        Returns:
            True if effect was successfully executed
        """
        # Placeholder implementation - specific effects need user confirmation
        return True

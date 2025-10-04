"""
Law card base implementation.

This module provides the base class for agenda cards with persistent effects (laws).
"""

from typing import TYPE_CHECKING, Any

from ti4.core.constants import AgendaType

from .agenda_card import BaseAgendaCard

if TYPE_CHECKING:
    pass


class LawCard(BaseAgendaCard):
    """
    Base implementation for law agenda cards.

    This class provides a foundation for agenda cards that have
    persistent effects that remain in play after being passed.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize the law card.

        Args:
            name: Display name of the agenda card
        """
        super().__init__(name)
        self._voting_outcomes: list[str] = []

    def get_agenda_type(self) -> AgendaType:
        """Get the agenda type (always LAW for law cards)."""
        return AgendaType.LAW

    def get_voting_outcomes(self) -> list[str]:
        """Get possible voting outcomes for this agenda."""
        if self._voting_outcomes:
            return self._voting_outcomes
        return super().get_voting_outcomes()

    def resolve_outcome(self, outcome: str, vote_result: Any, game_state: Any) -> Any:
        """Resolve the agenda based on voting outcome."""
        # Default implementation - concrete cards should override
        return None

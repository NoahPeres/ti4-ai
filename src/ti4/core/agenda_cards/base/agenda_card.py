"""
Base agenda card implementation.

This module provides the abstract base class for all agenda card implementations.
"""

from abc import ABC, abstractmethod
from typing import Any

from ti4.core.constants import AgendaType


class BaseAgendaCard(ABC):
    """
    Abstract base class for all agenda card implementations.

    This class provides common functionality and enforces the interface
    that all concrete agenda cards must implement.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize the base agenda card.

        Args:
            name: Display name of the agenda card

        Raises:
            ValueError: If name is empty or None
        """
        if not name or not name.strip():
            raise ValueError("Agenda card name cannot be empty")
        self._name = name.strip()

    @property
    def name(self) -> str:
        """Display name of the agenda card."""
        return self._name

    def get_name(self) -> str:
        """Get the agenda card name."""
        return self._name

    @abstractmethod
    def get_agenda_type(self) -> AgendaType:
        """Get the agenda type (LAW or DIRECTIVE)."""
        ...

    def get_voting_outcomes(self) -> list[str]:
        """Get possible voting outcomes for this agenda."""
        # Default implementation - concrete cards should override
        return ["For", "Against"]

    @abstractmethod
    def resolve_outcome(self, outcome: str, vote_result: Any, game_state: Any) -> Any:
        """Resolve the agenda based on voting outcome."""
        ...

    def validate_card_data(self, outcomes: list[str], metadata: dict[str, Any]) -> bool:
        """Validate agenda card data."""
        # Basic validation - concrete cards can override for specific validation
        if not outcomes:
            return False

        # Check that outcomes are valid strings
        if not all(
            isinstance(outcome, str) and outcome.strip() for outcome in outcomes
        ):
            return False

        # Basic metadata validation
        if not isinstance(metadata, dict):
            return False

        return True

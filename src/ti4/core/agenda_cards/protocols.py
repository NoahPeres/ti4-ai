"""
Protocols for agenda card implementations.

This module defines the protocols that agenda cards must implement,
following the technology card framework patterns.
"""

from typing import Any, Protocol, runtime_checkable

from ti4.core.constants import AgendaType


@runtime_checkable
class AgendaCardProtocol(Protocol):
    """Protocol defining the interface that all agenda cards must implement."""

    def get_name(self) -> str:
        """Get the agenda card name."""
        ...

    def get_agenda_type(self) -> AgendaType:
        """Get the agenda type (LAW or DIRECTIVE)."""
        ...

    def get_voting_outcomes(self) -> list[str]:
        """Get possible voting outcomes for this agenda."""
        ...

    def resolve_outcome(self, outcome: str, vote_result: Any, game_state: Any) -> Any:
        """Resolve the agenda based on voting outcome."""
        ...

    def validate_card_data(self, outcomes: list[str], metadata: dict[str, Any]) -> bool:
        """Validate agenda card data."""
        ...

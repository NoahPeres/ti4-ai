"""
Demilitarized Zone agenda card implementation.

This module implements the Demilitarized Zone agenda card that can attach to planets.
"""

from typing import Any

from ti4.core.agenda_cards.base.planet_attachable_card import PlanetAttachableCard


class DemilitarizedZone(PlanetAttachableCard):
    """
    Demilitarized Zone agenda card implementation.

    This card attaches to a planet and prevents ships from moving through
    the system containing that planet.
    """

    def __init__(self) -> None:
        """Initialize the Demilitarized Zone card."""
        super().__init__("Demilitarized Zone")

    def get_voting_outcomes(self) -> list[str]:
        """Get possible voting outcomes for this agenda."""
        return ["Elect Planet"]

    def resolve_outcome(self, outcome: str, vote_result: Any, game_state: Any) -> Any:
        """Resolve the agenda based on voting outcome."""
        from ti4.core.agenda_cards.effect_resolver import AgendaResolutionResult

        # Placeholder implementation
        return AgendaResolutionResult(
            success=True,
            directive_executed=True,
            description="Demilitarized Zone attached to elected planet. Ships cannot move through this system.",
            elected_target=vote_result.elected_target
            if hasattr(vote_result, "elected_target")
            else None,
        )

    def get_attachment_effect_description(self) -> str:
        """Get the description of the effect when attached to a planet."""
        return "Ships cannot move through the system containing this planet"

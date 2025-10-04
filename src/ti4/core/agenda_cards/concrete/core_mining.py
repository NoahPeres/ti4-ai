"""
Core Mining agenda card implementation.

This module implements the Core Mining agenda card that can attach to planets.
"""

from typing import Any

from ti4.core.agenda_cards.base.planet_attachable_card import PlanetAttachableCard


class CoreMining(PlanetAttachableCard):
    """
    Core Mining agenda card implementation.

    This card attaches to a planet and provides additional trade goods
    when the planet is exhausted.
    """

    def __init__(self) -> None:
        """Initialize the Core Mining card."""
        super().__init__("Core Mining")

    def get_voting_outcomes(self) -> list[str]:
        """Get possible voting outcomes for this agenda."""
        return ["Elect Planet"]

    def resolve_outcome(self, outcome: str, vote_result: Any, game_state: Any) -> Any:
        """Resolve the agenda based on voting outcome."""
        # This would be implemented when we have the full voting system
        # For now, just return a placeholder result
        return {
            "success": True,
            "description": "Core Mining attached to elected planet",
        }

    def get_attachment_effect_description(self) -> str:
        """Get the description of the effect when attached to a planet."""
        return "Gain 2 trade goods when this planet is exhausted"

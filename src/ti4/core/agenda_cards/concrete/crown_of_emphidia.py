"""
Crown of Emphidia agenda card implementation.

This module implements the Crown of Emphidia law card that grants victory points
and transfers ownership based on home system planet capture.
"""

from typing import TYPE_CHECKING, Any

from ..base.law_card import LawCard

if TYPE_CHECKING:
    pass


class CrownOfEmphidia(LawCard):
    """
    Implementation of the Crown of Emphidia agenda card.

    Game text: "Elect Player. The elected player gains this card and 1 victory point.
    A player gains this card and 1 victory point after they gain control of a planet
    in the home system of this card's owner. Then, the previous owner of this card
    loses 1 victory point."
    """

    def __init__(self) -> None:
        """Initialize the Crown of Emphidia card."""
        super().__init__("The Crown of Emphidia")
        self._voting_outcomes = ["Elect Player"]

    def get_voting_outcomes(self) -> list[str]:
        """Get possible voting outcomes for this agenda."""
        return self._voting_outcomes

    def resolve_outcome(self, outcome: str, vote_result: Any, game_state: Any) -> Any:
        """Resolve the agenda based on voting outcome."""
        if outcome == "Elect Player":
            # Initial election grants the card and 1 VP to elected player
            elected_player = getattr(vote_result, "elected_target", None)
            if elected_player:
                # Set the initial owner
                if hasattr(game_state, "set_crown_emphidia_owner"):
                    game_state.set_crown_emphidia_owner(elected_player)

                # Grant 1 victory point
                if hasattr(game_state, "adjust_victory_points"):
                    game_state.adjust_victory_points(elected_player, 1)

                return type(
                    "AgendaResult",
                    (),
                    {
                        "description": f"{elected_player} gains the Crown of Emphidia and 1 victory point"
                    },
                )()

        return None

    def handle_home_system_capture(
        self, capturing_player: str, planet: str, game_state: Any
    ) -> None:
        """
        Handle planet capture in the Crown owner's home system.

        Args:
            capturing_player: The player who captured the planet
            planet: The planet that was captured
            game_state: Current game state
        """
        # Get current Crown owner
        current_owner = None
        if hasattr(game_state, "get_crown_emphidia_owner"):
            current_owner = game_state.get_crown_emphidia_owner()

        if current_owner and current_owner != capturing_player:
            # Check if the planet is in the current owner's home system
            is_home_system_planet = False
            if hasattr(game_state, "is_home_system_planet"):
                is_home_system_planet = game_state.is_home_system_planet(
                    planet, current_owner
                )

            if is_home_system_planet:
                # Transfer the Crown to the capturing player
                if hasattr(game_state, "set_crown_emphidia_owner"):
                    game_state.set_crown_emphidia_owner(capturing_player)

                # Capturing player gains 1 VP
                if hasattr(game_state, "adjust_victory_points"):
                    game_state.adjust_victory_points(capturing_player, 1)

                # Previous owner loses 1 VP
                if hasattr(game_state, "adjust_victory_points"):
                    game_state.adjust_victory_points(current_owner, -1)

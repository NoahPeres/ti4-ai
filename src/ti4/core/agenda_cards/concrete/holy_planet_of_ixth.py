"""
Holy Planet of Ixth agenda card implementation.

This module implements the Holy Planet of Ixth law card that attaches to a planet
and grants victory points when gaining or losing control of that planet.
"""

from typing import TYPE_CHECKING, Any

from ..base.law_card import LawCard

if TYPE_CHECKING:
    pass


class HolyPlanetOfIxth(LawCard):
    """
    Implementation of the Holy Planet of Ixth agenda card.

    Game text: "Elect Cultural Planet. Attach this card to the elected planet's card.
    The planet's owner gains 1 victory point. Units on this planet cannot use PRODUCTION.
    When a player gains control of this planet, they gain 1 victory point.
    When a player loses control of this planet, they lose 1 victory point."
    """

    def __init__(self) -> None:
        """Initialize the Holy Planet of Ixth card."""
        super().__init__("Holy Planet of Ixth")
        self._voting_outcomes = ["Elect Cultural Planet"]

    def get_voting_outcomes(self) -> list[str]:
        """Get possible voting outcomes for this agenda."""
        return self._voting_outcomes

    def resolve_outcome(self, outcome: str, vote_result: Any, game_state: Any) -> Any:
        """Resolve the agenda based on voting outcome."""
        if outcome == "Elect Cultural Planet":
            # Attach to elected planet
            elected_planet = getattr(vote_result, "elected_target", None)
            if elected_planet:
                # Attach this card to the planet
                if hasattr(game_state, "attach_agenda_to_planet"):
                    game_state.attach_agenda_to_planet(self.get_name(), elected_planet)

                # Grant 1 VP to current owner of the planet
                planet_owner = None
                if hasattr(game_state, "get_planet_owner"):
                    planet_owner = game_state.get_planet_owner(elected_planet)

                if planet_owner and hasattr(game_state, "adjust_victory_points"):
                    game_state.adjust_victory_points(planet_owner, 1)

                return type(
                    "AgendaResult",
                    (),
                    {
                        "description": f"Holy Planet of Ixth attached to {elected_planet}. {planet_owner} gains 1 victory point."
                    },
                )()

        return None

    def handle_planet_control_gain(
        self, player: str, planet: str, game_state: Any
    ) -> None:
        """
        Handle when a player gains control of the Holy Planet.

        Args:
            player: The player who gained control
            planet: The planet that was gained
            game_state: Current game state
        """
        # Check if this card is attached to the planet
        is_attached = False
        if hasattr(game_state, "is_agenda_attached_to_planet"):
            is_attached = game_state.is_agenda_attached_to_planet(
                self.get_name(), planet
            )

        if is_attached:
            # Player gains 1 VP
            if hasattr(game_state, "adjust_victory_points"):
                game_state.adjust_victory_points(player, 1)

    def handle_planet_control_loss(
        self, player: str, planet: str, game_state: Any
    ) -> None:
        """
        Handle when a player loses control of the Holy Planet.

        Args:
            player: The player who lost control
            planet: The planet that was lost
            game_state: Current game state
        """
        # Check if this card is attached to the planet
        is_attached = False
        if hasattr(game_state, "is_agenda_attached_to_planet"):
            is_attached = game_state.is_agenda_attached_to_planet(
                self.get_name(), planet
            )

        if is_attached:
            # Player loses 1 VP
            if hasattr(game_state, "adjust_victory_points"):
                game_state.adjust_victory_points(player, -1)

    def prevents_production(self, planet: str, game_state: Any) -> bool:
        """
        Check if this card prevents production on the given planet.

        Args:
            planet: The planet to check
            game_state: Current game state

        Returns:
            True if production is prevented on this planet
        """
        # Check if this card is attached to the planet
        if hasattr(game_state, "is_agenda_attached_to_planet"):
            result = game_state.is_agenda_attached_to_planet(self.get_name(), planet)
            return bool(result)

        return False

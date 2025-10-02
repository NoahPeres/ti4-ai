"""
Shard of the Throne agenda card implementation.

This module implements the Shard of the Throne law card that grants victory points
and transfers ownership based on combat victories.
"""

from typing import TYPE_CHECKING, Any

from ..base.law_card import LawCard

if TYPE_CHECKING:
    pass


class ShardOfTheThrone(LawCard):
    """
    Implementation of the Shard of the Throne agenda card.

    Game text: "Elect Player. The elected player gains this card and 1 victory point.
    A player gains this card and 1 victory point when they win a combat against the
    owner of this card. Then, the previous owner of this card loses 1 victory point."
    """

    def __init__(self) -> None:
        """Initialize the Shard of the Throne card."""
        super().__init__("Shard of the Throne")
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
                if hasattr(game_state, "set_shard_owner"):
                    game_state.set_shard_owner(elected_player)

                # Grant 1 victory point
                if hasattr(game_state, "adjust_victory_points"):
                    game_state.adjust_victory_points(elected_player, 1)

                return type(
                    "AgendaResult",
                    (),
                    {
                        "description": f"{elected_player} gains the Shard of the Throne and 1 victory point"
                    },
                )()

        return None

    def handle_combat_victory(self, winner: str, loser: str, game_state: Any) -> None:
        """
        Handle combat victory against the Shard owner.

        Args:
            winner: The player who won the combat
            loser: The player who lost the combat (current Shard owner)
            game_state: Current game state
        """
        # Check if the loser is the current Shard owner
        current_owner = None
        if hasattr(game_state, "get_shard_owner"):
            current_owner = game_state.get_shard_owner()

        if current_owner == loser:
            # Transfer the Shard to the winner
            if hasattr(game_state, "set_shard_owner"):
                game_state.set_shard_owner(winner)

            # Winner gains 1 VP
            if hasattr(game_state, "adjust_victory_points"):
                game_state.adjust_victory_points(winner, 1)

            # Previous owner loses 1 VP
            if hasattr(game_state, "adjust_victory_points"):
                game_state.adjust_victory_points(loser, -1)

"""Status phase management for TI4.

This module implements status phase mechanics including Rule 34.2 ready cards step.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game_state import GameState


class StatusPhaseManager:
    """Manages status phase operations including readying exhausted cards."""

    def ready_all_cards(self, game_state: "GameState") -> "GameState":
        """Ready all exhausted cards for all players.

        LRR Reference: Rule 34.2 - During the 'Ready Cards' step of the status phase,
        each player readies all of their exhausted cards by flipping those cards faceup.

        Args:
            game_state: Current game state

        Returns:
            New game state with all cards readied
        """
        # Start with current state
        new_state = game_state

        # Ready all strategy cards
        new_state = self._ready_all_strategy_cards(new_state)

        # Ready all player cards (planets, technologies)
        new_state = self._ready_all_player_cards(new_state)

        return new_state

    def _ready_all_strategy_cards(self, game_state: "GameState") -> "GameState":
        """Ready all exhausted strategy cards."""
        new_state = game_state

        # Ready each exhausted strategy card
        for strategy_card in list(game_state.exhausted_strategy_cards):
            new_state = new_state.ready_strategy_card(strategy_card)

        return new_state

    def _ready_all_player_cards(self, game_state: "GameState") -> "GameState":
        """Ready all exhausted player cards (planets, technologies)."""
        new_state = game_state

        # Ready all player planets
        new_player_planets = {}
        for player_id, planets in game_state.player_planets.items():
            readied_planets = []
            for planet in planets:
                if planet.is_exhausted():
                    planet.ready()
                readied_planets.append(planet)
            new_player_planets[player_id] = readied_planets

        new_state = new_state._create_new_state(player_planets=new_player_planets)

        # Ready all player technology cards
        new_player_tech_cards = {}
        for player_id, tech_cards in game_state.player_technology_cards.items():
            readied_tech_cards = []
            for tech_card in tech_cards:
                if tech_card.is_exhausted():
                    tech_card.ready()
                readied_tech_cards.append(tech_card)
            new_player_tech_cards[player_id] = readied_tech_cards

        new_state = new_state._create_new_state(
            player_technology_cards=new_player_tech_cards
        )

        return new_state

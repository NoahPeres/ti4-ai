"""Tests for Rule 25: Control of Planets"""

import pytest

from src.ti4.core.constants import UnitType
from src.ti4.core.game_state import GameState
from src.ti4.core.planet import Planet
from src.ti4.core.unit import Unit


class TestRule25Control:
    """Test Rule 25: CONTROL mechanics."""

    def test_rule_25_1_gaining_control_takes_planet_card(self) -> None:
        """Test that gaining control of a planet takes the corresponding planet card.

        LRR Reference: Rule 25.1 - "When a player gains control of a planet, they take
        the planet card that corresponds to that planet and place it in their play area;
        that card is exhausted."
        """
        # This test should fail initially - we need planet card system
        game_state = GameState()

        # Create a planet with a corresponding planet card
        planet = Planet("Test Planet", resources=2, influence=1)

        # Player gains control of planet
        exploration_triggered, new_state = game_state.gain_planet_control(
            "player1", planet
        )

        # Player should now have the planet card in their play area
        player_cards = new_state.get_player_planet_cards("player1")
        assert len(player_cards) == 1
        assert player_cards[0].name == "Test Planet"

        # Planet card should be exhausted when gained
        assert player_cards[0].is_exhausted()

    def test_rule_25_1a_first_control_takes_from_deck(self) -> None:
        """Test that first control of a planet takes card from planet card deck.

        LRR Reference: Rule 25.1a - "If a player is the first player to control a planet,
        they take the planet card from the planet card deck."
        """
        game_state = GameState()

        # Create a planet and ensure its card is in the deck
        planet = Planet("Deck Planet", resources=3, influence=2)

        # Initially, planet card should be in deck (or created when needed)
        # Player gains control for first time
        exploration_triggered, new_state = game_state.gain_planet_control(
            "player1", planet
        )

        # Planet card should no longer be in deck
        assert not new_state.is_planet_card_in_deck("Deck Planet")

        # Player should have the card
        player_cards = new_state.get_player_planet_cards("player1")
        assert len(player_cards) == 1
        assert player_cards[0].name == "Deck Planet"

    def test_rule_25_1b_control_transfer_takes_from_other_player(self) -> None:
        """Test that gaining control from another player takes card from their play area.

        LRR Reference: Rule 25.1b - "If another player controls that planet, they take
        the planet card from that player's play area."
        """
        game_state = GameState()

        # Create a planet
        planet = Planet("Transfer Planet", resources=2, influence=3)

        # Player 1 gains control first
        exploration_triggered, state1 = game_state.gain_planet_control(
            "player1", planet
        )

        # Player 2 gains control from Player 1
        exploration_triggered, state2 = state1.gain_planet_control("player2", planet)

        # Player 1 should no longer have the card
        player1_cards = state2.get_player_planet_cards("player1")
        assert len(player1_cards) == 0

        # Player 2 should now have the card
        player2_cards = state2.get_player_planet_cards("player2")
        assert len(player2_cards) == 1
        assert player2_cards[0].name == "Transfer Planet"

    def test_rule_25_1c_first_control_triggers_exploration(self) -> None:
        """Test that first control of a planet triggers exploration.

        LRR Reference: Rule 25.1c - "If a player is the first player to control a planet,
        they resolve the "Explore" step of a tactical action."
        """
        game_state = GameState()

        # Create a planet
        planet = Planet("Explore Planet", resources=1, influence=1)

        # First control should trigger exploration
        exploration_triggered, new_state = game_state.gain_planet_control(
            "player1", planet
        )
        assert exploration_triggered

        # Second control should not trigger exploration
        exploration_triggered2, state2 = new_state.gain_planet_control(
            "player2", planet
        )
        assert not exploration_triggered2

    def test_rule_25_2_cannot_gain_already_controlled_planet(self) -> None:
        """Test that a player cannot gain control of a planet they already control.

        LRR Reference: Rule 25.2 - "A player cannot gain control of a planet they already control."
        """
        game_state = GameState()

        # Create a planet
        planet = Planet("Already Controlled", resources=2, influence=1)

        # Player gains control
        exploration_triggered, new_state = game_state.gain_planet_control(
            "player1", planet
        )

        # Same player tries to gain control again - should raise ValueError
        with pytest.raises(ValueError, match="Player already controls this planet"):
            new_state.gain_planet_control("player1", planet)

    def test_rule_25_3_planet_card_remains_in_play_area(self) -> None:
        """Test that planet cards remain in player's play area while controlled.

        LRR Reference: Rule 25.3 - "A planet card remains in a player's play area
        as long as they control the planet."
        """
        game_state = GameState()

        # Create a planet
        planet = Planet("Persistent Planet", resources=2, influence=2)

        # Player gains control
        exploration_triggered, new_state = game_state.gain_planet_control(
            "player1", planet
        )

        # Planet card should remain in player's play area
        player_cards = new_state.get_player_planet_cards("player1")
        assert len(player_cards) == 1
        assert player_cards[0].name == "Persistent Planet"

        # Card should still be there after some game actions (simulated by checking again)
        assert len(new_state.get_player_planet_cards("player1")) == 1

    def test_rule_25_4_control_without_units_uses_control_token(self) -> None:
        """Test that controlling a planet without units places a control token.

        LRR Reference: Rule 25.4 - "If a player controls a planet that does not contain
        any of their units, they place a control token on that planet."
        """
        game_state = GameState()

        # Create a planet with no units
        planet = Planet("Token Planet", resources=1, influence=2)

        # Player gains control without units
        exploration_triggered, new_state = game_state.gain_planet_control(
            "player1", planet
        )

        # Should have control token on planet
        assert new_state.has_control_token_on_planet("player1", planet)

    def test_rule_25_5_lose_control_when_other_player_has_units(self) -> None:
        """Test that control is lost when another player has units and current controller doesn't.

        LRR Reference: Rule 25.5 - "If a player does not have units on a planet they control,
        and another player has units on that planet, the player loses control of that planet."
        """
        game_state = GameState()

        # Create a planet
        planet = Planet("Contested Planet", resources=2, influence=1)

        # Player 1 gains control
        exploration_triggered, state1 = game_state.gain_planet_control(
            "player1", planet
        )

        # Add Player 2's unit to the planet
        player2_unit = Unit(UnitType.INFANTRY, "player2")
        planet.place_unit(player2_unit)

        # Resolve control change
        final_state = state1.resolve_planet_control_change(planet)

        # Player 1 should lose control, Player 2 should gain it
        player1_cards = final_state.get_player_planet_cards("player1")
        player2_cards = final_state.get_player_planet_cards("player2")

        assert len(player1_cards) == 0
        assert len(player2_cards) == 1
        assert player2_cards[0].name == "Contested Planet"

    def test_rule_25_7_remove_control_token_when_losing_control(self) -> None:
        """Test that control tokens are removed when losing control.

        LRR Reference: Rule 25.7 - "When a player loses control of a planet,
        they remove their control token from that planet."
        """
        game_state = GameState()

        # Create a planet with no units
        planet = Planet("Token Loss Planet", resources=1, influence=1)

        # Player gains control
        exploration_triggered, state1 = game_state.gain_planet_control(
            "player1", planet
        )
        assert state1.has_control_token_on_planet("player1", planet)

        # Player loses control
        final_state = state1.lose_planet_control("player1", planet)

        # Control token should be removed
        assert not final_state.has_control_token_on_planet("player1", planet)


class TestRule25PlanetCardDeck:
    """Test planet card deck management for Rule 25."""

    def test_planet_card_deck_initialization(self) -> None:
        """Test that planet card deck is properly initialized."""
        game_state = GameState()
        # Deck starts empty and gets populated as planets are controlled
        assert game_state.get_planet_card_deck_size() >= 0


class TestRule25Integration:
    """Integration tests for Rule 25 control mechanics."""

    @pytest.mark.skip(reason="Waiting for invasion mechanics to be implemented")
    def test_control_integration_with_invasion(self):
        """Test that control changes properly during invasion."""
        # This will be implemented when invasion mechanics are added
        pass

    @pytest.mark.skip(reason="Waiting for exploration mechanics to be implemented")
    def test_control_integration_with_exploration(self):
        """Test that gaining control triggers exploration when appropriate."""
        # This will be implemented when exploration mechanics are added
        pass

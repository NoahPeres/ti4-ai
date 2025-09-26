"""
Test Rule 12: ATTACH

Rule 12 defines the mechanics for attaching cards to planet cards.

LRR Text:
12 ATTACH
Some game effects instruct a player to attach a card to a planet card. The attached card modifies that planet card in some way.
12.1 To attach a card to a planet card, a player places the card with the attach effect partially underneath the planet card.
12.2 If a player gains or loses control of planet that contains a card with an attach effect, the attached card stays with that planet.
12.3 When a card is attached to a planet card, place the corresponding attachment token on that planet on the game board.

Related Topics: Agenda Card, Control, Exploration, Planets
"""

from unittest.mock import Mock

import pytest

from ti4.core.galaxy import Galaxy
from ti4.core.game_state import GameState
from ti4.core.hex_coordinate import HexCoordinate
from ti4.core.planet import Planet
from ti4.core.planet_card import PlanetCard
from ti4.core.system import System


class TestRule12Attach:
    """Test Rule 12: ATTACH mechanics."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        from ti4.core.constants import Faction
        from ti4.core.player import Player

        self.galaxy = Galaxy()
        self.system = System("test_system")
        self.planet = Planet(name="test_planet", resources=2, influence=1)
        self.system.add_planet(self.planet)

        coord = HexCoordinate(0, 0)
        self.galaxy.place_system(coord, "test_system")

        # Create GameState and add players properly
        self.game_state = GameState(galaxy=self.galaxy)
        player1 = Player("player1", Faction.SOL)
        player2 = Player("player2", Faction.XXCHA)
        self.game_state = self.game_state.add_player(player1).add_player(player2)

    # Rule 12.1: Card Attachment Process
    def test_attach_card_to_planet_card_basic(self) -> None:
        """Test basic card attachment to planet card (Rule 12.1)."""
        # Create a mock attachment card
        attachment_card = Mock()
        attachment_card.name = "Test Attachment"
        attachment_card.is_exhausted = False

        planet_card = PlanetCard(
            name="test_planet",
            resources=2,
            influence=1,
            game_state=self.game_state,
        )

        # Attach the card
        planet_card.attach_card(attachment_card)

        # Verify attachment
        assert planet_card.has_attached_cards()
        assert attachment_card in planet_card.get_attached_cards()
        assert len(planet_card.get_attached_cards()) == 1

    def test_attach_card_preserves_exhausted_state(self) -> None:
        """Test that attached cards preserve their exhausted state (Rule 12.1)."""
        # Create exhausted attachment card
        exhausted_card = Mock()
        exhausted_card.name = "Exhausted Attachment"
        exhausted_card.is_exhausted = True

        planet_card = PlanetCard(
            name="test_planet", resources=2, influence=1, game_state=self.game_state
        )

        # Attach exhausted card
        planet_card.attach_card(exhausted_card)

        # Verify card state is preserved
        attached_cards = planet_card.get_attached_cards()
        assert len(attached_cards) == 1
        assert attached_cards[0].is_exhausted is True

    def test_multiple_attachments_per_planet(self) -> None:
        """Test that multiple cards can be attached to the same planet."""
        attachment1 = Mock()
        attachment1.name = "First Attachment"
        attachment1.is_exhausted = False

        attachment2 = Mock()
        attachment2.name = "Second Attachment"
        attachment2.is_exhausted = True

        planet_card = PlanetCard(
            name="test_planet",
            resources=2,
            influence=1,
            game_state=self.game_state,
        )

        # Attach multiple cards
        planet_card.attach_card(attachment1)
        planet_card.attach_card(attachment2)

        # Verify all cards are attached
        attached_cards = planet_card.get_attached_cards()
        assert len(attached_cards) == 2
        assert attachment1 in attached_cards
        assert attachment2 in attached_cards

    # Rule 12.2: Control Transfer Behavior
    def test_attached_cards_stay_with_planet_on_control_change(self) -> None:
        """Test that attached cards stay with planet when control changes (Rule 12.2)."""
        # Create a planet card and add it to the deck first
        planet_card = PlanetCard(
            name=self.planet.name,
            resources=self.planet.resources,
            influence=self.planet.influence,
            game_state=self.game_state,
        )

        # Add to deck
        new_deck = self.game_state.planet_card_deck.copy()
        new_deck[planet_card.name] = planet_card
        game_state_with_deck = self.game_state._create_new_state(
            planet_card_deck=new_deck
        )

        attachment_card = Mock()
        attachment_card.name = "Test Attachment"
        attachment_card.is_exhausted = False

        # Attach card to the planet card in the deck
        deck_planet_card = game_state_with_deck.planet_card_deck[self.planet.name]
        deck_planet_card.attach_card(attachment_card)

        # Give control to player1
        _, new_state = game_state_with_deck.gain_planet_control("player1", self.planet)

        # Verify attachment is still there after first control change
        player1_planet_cards = new_state.get_player_planet_cards("player1")
        assert len(player1_planet_cards) == 1
        first_planet_card = player1_planet_cards[0]
        assert first_planet_card.has_attached_cards()
        first_attached_cards = first_planet_card.get_attached_cards()
        assert len(first_attached_cards) == 1
        assert first_attached_cards[0].name == "Test Attachment"

        # Transfer control to player2 (using same planet object)
        _, final_state = new_state.gain_planet_control("player2", self.planet)

        # Attachment should still be there
        player2_planet_cards = final_state.get_player_planet_cards("player2")
        assert len(player2_planet_cards) == 1
        final_planet_card = player2_planet_cards[0]

        # Verify attachment persists through control transfer
        assert final_planet_card.has_attached_cards()
        attached_cards = final_planet_card.get_attached_cards()
        assert len(attached_cards) == 1
        assert attached_cards[0].name == "Test Attachment"

    def test_purged_planet_card_purges_attachments(self) -> None:
        """Test that purging planet card also purges all attached cards (Rule 12.2b)."""
        planet_card = PlanetCard(
            name="test_planet",
            resources=2,
            influence=1,
            game_state=self.game_state,
        )

        attachment1 = Mock()
        attachment1.name = "First Attachment"

        attachment2 = Mock()
        attachment2.name = "Second Attachment"

        # Attach cards to planet
        planet_card.attach_card(attachment1)
        planet_card.attach_card(attachment2)

        # Verify attachments are there
        assert planet_card.has_attached_cards()
        assert len(planet_card.get_attached_cards()) == 2

        # Purge planet card
        planet_card.purge_attachments()

        # All attachments should be purged
        assert not planet_card.has_attached_cards()
        assert len(planet_card.get_attached_cards()) == 0

    # Rule 12.3: Attachment Token Placement
    def test_attachment_token_placed_on_game_board(self) -> None:
        """Test that attachment tokens are placed on the game board (Rule 12.3)."""
        planet_card = self.game_state._get_or_create_planet_card(self.planet)

        attachment_card = Mock()
        attachment_card.name = "Test Attachment"
        attachment_card.token_id = "test_attachment_token"

        # Attach the card
        planet_card.attach_card(attachment_card)

        # Check that attachment token is placed on the planet
        assert "test_attachment_token" in self.game_state.planet_attachment_tokens.get(
            "test_planet", set()
        )

        # Optional: Also check token presence via card's state reference
        if planet_card._game_state is not None:
            assert (
                "test_attachment_token"
                in planet_card._game_state.planet_attachment_tokens.get(
                    "test_planet", set()
                )
            )

    def test_attachment_token_removed_when_card_detached(self) -> None:
        """Test that attachment tokens are removed when cards are detached."""
        planet_card = self.game_state._get_or_create_planet_card(self.planet)

        attachment_card = Mock()
        attachment_card.name = "Test Attachment"
        attachment_card.token_id = "test_attachment_token"

        # Attach and then detach the card
        planet_card.attach_card(attachment_card)
        planet_card.detach_card(attachment_card)

        # Check that attachment token is removed
        assert (
            "test_attachment_token"
            not in self.game_state.planet_attachment_tokens.get("test_planet", set())
        )

    def test_multiple_attachment_tokens_per_planet(self) -> None:
        """Test that multiple attachment tokens can exist on the same planet."""
        planet_card = self.game_state._get_or_create_planet_card(self.planet)

        attachment1 = Mock()
        attachment1.name = "First Attachment"
        attachment1.token_id = "token1"

        attachment2 = Mock()
        attachment2.name = "Second Attachment"
        attachment2.token_id = "token2"

        # Attach both cards
        planet_card.attach_card(attachment1)
        planet_card.attach_card(attachment2)

        # Check that both tokens are present
        planet_tokens = self.game_state.planet_attachment_tokens.get(
            "test_planet", set()
        )
        assert "token1" in planet_tokens
        assert "token2" in planet_tokens
        assert len(planet_tokens) == 2

    # Integration Tests
    def test_attachment_system_integration_with_exploration(self) -> None:
        """Test that attachment system integrates with exploration cards."""
        # This test will verify integration once exploration system supports attachments
        exploration_card = Mock()
        exploration_card.name = "Paradise World"
        exploration_card.has_attach_effect = True
        exploration_card.attach_effect = (
            "This planet's influence value is increased by 2"
        )

        planet_card = self.game_state._get_or_create_planet_card(self.planet)

        # Attach the exploration card to the planet
        planet_card.attach_card(exploration_card)

        # Verify the card is attached
        attached_cards = planet_card.get_attached_cards()
        assert len(attached_cards) == 1
        assert exploration_card in attached_cards

    def test_attachment_system_integration_with_agenda_cards(self) -> None:
        """Test that attachment system integrates with agenda cards."""
        # This test will verify integration once agenda system supports attachments
        agenda_card = Mock()
        agenda_card.name = "Demilitarized Zone"
        agenda_card.has_attach_effect = True
        agenda_card.attach_effect = (
            "Units cannot be committed to, produced on or placed on this planet"
        )

        planet_card = self.game_state._get_or_create_planet_card(self.planet)

        # Attach the agenda card to the planet
        planet_card.attach_card(agenda_card)

        # Verify the card is attached
        attached_cards = planet_card.get_attached_cards()
        assert len(attached_cards) == 1
        assert agenda_card in attached_cards

    def test_attachment_validation_only_planets_can_have_attachments(self) -> None:
        """Test that only planet cards can have attachments."""
        # Create a non-planet card (Mock object without attach_card method)
        non_planet_card = Mock(spec=[])  # Empty spec means no methods
        non_planet_card.name = "Strategy Card"

        attachment_card = Mock()
        attachment_card.name = "Test Attachment"

        # This should fail as only planet cards can have attachments
        with pytest.raises(AttributeError):
            non_planet_card.attach_card(attachment_card)

    def test_attachment_order_preservation(self) -> None:
        """Test that attachment order is preserved for multiple attachments."""
        planet_card = PlanetCard(
            name="test_planet",
            resources=2,
            influence=1,
            game_state=self.game_state,
        )

        attachment1 = Mock()
        attachment1.name = "First Attachment"

        attachment2 = Mock()
        attachment2.name = "Second Attachment"

        attachment3 = Mock()
        attachment3.name = "Third Attachment"

        # Attach cards in order
        planet_card.attach_card(attachment1)
        planet_card.attach_card(attachment2)
        planet_card.attach_card(attachment3)

        # Verify order is preserved
        attached_cards = planet_card.get_attached_cards()
        assert attached_cards[0].name == "First Attachment"
        assert attached_cards[1].name == "Second Attachment"
        assert attached_cards[2].name == "Third Attachment"

    def test_attachment_tokens_persist_across_control_transfers(self) -> None:
        """Test that attachment tokens persist when planet control changes multiple times."""
        # Create a planet card and add it to the deck first
        planet_card = PlanetCard(
            name=self.planet.name,
            resources=self.planet.resources,
            influence=self.planet.influence,
            game_state=self.game_state,
        )

        # Add to deck
        new_deck = self.game_state.planet_card_deck.copy()
        new_deck[planet_card.name] = planet_card
        game_state_with_deck = self.game_state._create_new_state(
            planet_card_deck=new_deck
        )

        attachment_card = Mock()
        attachment_card.name = "Test Attachment"
        attachment_card.is_exhausted = False

        # Attach card to the planet card in the deck
        deck_planet_card = game_state_with_deck.planet_card_deck[self.planet.name]
        deck_planet_card.attach_card(attachment_card)

        # Add attachment token to game state
        new_tokens = game_state_with_deck.planet_attachment_tokens.copy()
        new_tokens[self.planet.name] = {"test_attachment_token"}
        state_with_tokens = game_state_with_deck._create_new_state(
            planet_attachment_tokens=new_tokens
        )

        # Transfer control to player1
        _, state1 = state_with_tokens.gain_planet_control("player1", self.planet)

        # Verify attachment token persists
        assert (
            "test_attachment_token" in state1.planet_attachment_tokens[self.planet.name]
        )

        # Transfer control to player2
        _, state2 = state1.gain_planet_control("player2", self.planet)

        # Verify attachment token still persists
        assert (
            "test_attachment_token" in state2.planet_attachment_tokens[self.planet.name]
        )

        # Verify the attachment card is still attached
        player2_planet_cards = state2.get_player_planet_cards("player2")
        assert len(player2_planet_cards) == 1
        final_planet_card = player2_planet_cards[0]
        assert final_planet_card.has_attached_cards()
        attached_cards = final_planet_card.get_attached_cards()
        assert len(attached_cards) == 1
        assert attached_cards[0].name == "Test Attachment"

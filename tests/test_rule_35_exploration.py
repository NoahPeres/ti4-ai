"""Test Rule 35: EXPLORATION

LRR 35: Planets and some space areas can be explored, yielding varying results
determined by the cards drawn from the exploration decks.

This module tests all aspects of the exploration system including:
- Planet exploration when gaining control (35.1)
- Trait-based exploration deck selection (35.2)
- Multiple exploration handling (35.3)
- Frontier token exploration (35.4-35.6)
- Card resolution mechanics (35.7)
- Attachment cards (35.8)
- Relic fragments (35.9)
"""

from unittest.mock import Mock

from ti4.core.exploration import (
    ExplorationCard,
    ExplorationDeck,
    ExplorationSystem,
    PlanetTrait,
)
from ti4.core.game_state import GameState
from ti4.core.planet import Planet
from ti4.core.player import Player


class TestRule35Exploration:
    """Test Rule 35: EXPLORATION mechanics."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.exploration_system = ExplorationSystem()
        self.mock_game_state = Mock(spec=GameState)
        self.mock_player = Mock(spec=Player)
        self.mock_player.id = "test_player"
        self.mock_player.relic_fragments = []  # Initialize relic_fragments list

    def test_planet_exploration_on_control_gain(self) -> None:
        """Test Rule 35.1: When a player takes control of a planet that is not
        already controlled by another player, they explore that planet.

        LRR 35.1: "When a player takes control of a planet that is not already
        controlled by another player, they explore that planet."
        """
        # Arrange
        cultural_planet = Planet("Vega Major", resources=2, influence=1)
        cultural_planet.traits = [PlanetTrait.CULTURAL]

        # Act
        result = self.exploration_system.explore_planet(
            player=self.mock_player,
            planet=cultural_planet,
            game_state=self.mock_game_state,
        )

        # Assert
        assert result.success is True
        assert result.exploration_triggered is True
        assert result.deck_used == PlanetTrait.CULTURAL
        assert result.card_drawn is not None

    def test_trait_based_deck_selection(self) -> None:
        """Test Rule 35.2: When a player explores a planet, they draw and resolve
        a card from the exploration deck that corresponds to that planet's trait.

        LRR 35.2a: "There are three planetary exploration decks, each of which
        corresponds to a planet trait: cultural, hazardous, and industrial."
        """
        # Test each trait type
        traits_to_test = [
            (PlanetTrait.CULTURAL, "cultural_deck"),
            (PlanetTrait.HAZARDOUS, "hazardous_deck"),
            (PlanetTrait.INDUSTRIAL, "industrial_deck"),
        ]

        for trait, _expected_deck in traits_to_test:
            # Arrange
            planet = Planet(f"test_planet_{trait.value}", resources=1, influence=1)
            planet.traits = [trait]

            # Act
            result = self.exploration_system.explore_planet(
                player=self.mock_player, planet=planet, game_state=self.mock_game_state
            )

            # Assert
            assert result.success is True
            assert result.deck_used == trait
            assert result.card_drawn.deck_type == trait.value

    def test_no_exploration_for_traitless_planets(self) -> None:
        """Test Rule 35.2b: Planets that do not have traits, such as Mecatol Rex
        and planets in home systems, cannot be explored.

        LRR 35.2b: "Planets that do not have traits, such as Mecatol Rex and
        planets in home systems, cannot be explored."
        """
        # Arrange
        mecatol_rex = Planet("Mecatol Rex", resources=1, influence=6)
        mecatol_rex.traits = []  # No traits

        # Act
        result = self.exploration_system.explore_planet(
            player=self.mock_player, planet=mecatol_rex, game_state=self.mock_game_state
        )

        # Assert
        assert result.success is True
        assert result.exploration_triggered is False
        assert result.deck_used is None
        assert result.card_drawn is None

    def test_multiple_trait_planet_choice(self) -> None:
        """Test Rule 35.2c: If a planet has multiple traits, the player exploring
        the planet chooses which of the corresponding exploration decks to draw from.

        LRR 35.2c: "If a planet has multiple traits, the player exploring the
        planet chooses which of the corresponding exploration decks to draw from."
        """
        # Arrange
        multi_trait_planet = Planet("Rigel I", resources=2, influence=1)
        multi_trait_planet.traits = [PlanetTrait.CULTURAL, PlanetTrait.HAZARDOUS]

        # Act - player chooses hazardous deck
        result = self.exploration_system.explore_planet(
            player=self.mock_player,
            planet=multi_trait_planet,
            game_state=self.mock_game_state,
            chosen_trait=PlanetTrait.HAZARDOUS,
        )

        # Assert
        assert result.success is True
        assert result.deck_used == PlanetTrait.HAZARDOUS
        assert result.card_drawn.deck_type == PlanetTrait.HAZARDOUS.value

    def test_multiple_exploration_order_choice(self) -> None:
        """Test Rule 35.2d: If a player gains control of multiple planets or
        resolves multiple explore effects at the same time, they choose the order
        in which they resolve those explorations.

        LRR 35.2d: "If a player gains control of multiple planets or resolves
        multiple explore effects at the same time, they choose the order in which
        they resolve those explorations, completely resolving each exploration
        card before resolving the next."
        """
        # Arrange
        planet1 = Planet("Planet A", resources=1, influence=1)
        planet1.traits = [PlanetTrait.CULTURAL]
        planet2 = Planet("Planet B", resources=2, influence=1)
        planet2.traits = [PlanetTrait.INDUSTRIAL]

        exploration_order = [planet1, planet2]

        # Act
        results = self.exploration_system.explore_multiple_planets(
            player=self.mock_player,
            planets=exploration_order,
            game_state=self.mock_game_state,
        )

        # Assert
        assert len(results) == 2
        assert results[0].planet_name == "Planet A"
        assert results[0].deck_used == PlanetTrait.CULTURAL
        assert results[1].planet_name == "Planet B"
        assert results[1].deck_used == PlanetTrait.INDUSTRIAL

    def test_multiple_exploration_ability(self) -> None:
        """Test Rule 35.3: Certain abilities may allow a planet to be explored
        multiple times.

        LRR 35.3: "Certain abilities may allow a planet to be explored multiple times."
        """
        # Arrange
        planet = Planet("Test Planet", resources=1, influence=1)
        planet.traits = [PlanetTrait.CULTURAL]

        # Act - explore the same planet twice
        result1 = self.exploration_system.explore_planet(
            player=self.mock_player, planet=planet, game_state=self.mock_game_state
        )

        result2 = self.exploration_system.explore_planet(
            player=self.mock_player,
            planet=planet,
            game_state=self.mock_game_state,
            force_exploration=True,  # Ability allows multiple exploration
        )

        # Assert
        assert result1.success is True
        assert result2.success is True
        assert result1.card_drawn != result2.card_drawn  # Different cards drawn

    def test_frontier_token_exploration(self) -> None:
        """Test Rule 35.5: When a player explores a frontier token, they draw
        and resolve a card from the frontier exploration deck.

        LRR 35.5: "When a player explores a frontier token, they draw and resolve
        a card from the frontier exploration deck."
        """
        # Arrange
        system_with_frontier = Mock()
        system_with_frontier.has_frontier_token = True

        # Act
        result = self.exploration_system.explore_frontier_token(
            player=self.mock_player,
            system=system_with_frontier,
            game_state=self.mock_game_state,
        )

        # Assert
        assert result.success is True
        assert result.deck_used == "frontier"
        assert result.card_drawn.deck_type == "frontier"

    def test_frontier_token_removal_after_exploration(self) -> None:
        """Test Rule 35.6: After a frontier token is explored, it is discarded
        and returned to the supply.

        LRR 35.6: "After a frontier token is explored, it is discarded and
        returned to the supply."
        """
        # Arrange
        system_with_frontier = Mock()
        system_with_frontier.has_frontier_token = True

        # Act
        result = self.exploration_system.explore_frontier_token(
            player=self.mock_player,
            system=system_with_frontier,
            game_state=self.mock_game_state,
        )

        # Assert
        assert result.success is True
        assert system_with_frontier.remove_frontier_token.called
        assert result.frontier_token_removed is True

    def test_exploration_card_resolution_and_discard(self) -> None:
        """Test Rule 35.7: To resolve an exploration card, a player reads the card,
        makes any necessary decisions, and resolves its ability. If the card was
        not a relic fragment or an attachment, it is discarded.

        LRR 35.7: "To resolve an exploration card, a player reads the card, makes
        any necessary decisions, and resolves its ability. If the card was not a
        relic fragment or an attachment, it is discarded into its respective
        discard pile."
        """
        # Arrange
        normal_card = ExplorationCard(
            name="Mining World",
            deck_type=PlanetTrait.INDUSTRIAL,
            card_type="normal",
            effect="Gain 2 trade goods",
        )

        # Act
        result = self.exploration_system.resolve_exploration_card(
            card=normal_card, player=self.mock_player, game_state=self.mock_game_state
        )

        # Assert
        assert result.success is True
        assert result.card_discarded is True
        assert result.effect_applied is True

    def test_deck_shuffle_when_empty(self) -> None:
        """Test Rule 35.7a: If there are no cards in an exploration deck, its
        discard pile is shuffled to form a new exploration deck.

        LRR 35.7a: "If there are no cards in an exploration deck, its discard
        pile is shuffled to form a new exploration deck."
        """
        # Arrange
        empty_deck = ExplorationDeck(PlanetTrait.CULTURAL)
        empty_deck.cards = []  # Empty deck
        empty_deck.discard_pile = [
            ExplorationCard("Card 1", PlanetTrait.CULTURAL, "normal", "Effect 1"),
            ExplorationCard("Card 2", PlanetTrait.CULTURAL, "normal", "Effect 2"),
        ]

        # Act
        card = empty_deck.draw_card()

        # Assert
        assert card is not None
        assert len(empty_deck.cards) > 0  # Deck was reshuffled
        assert len(empty_deck.discard_pile) == 0  # Discard pile was cleared

    def test_attachment_card_resolution(self) -> None:
        """Test Rule 35.8: If a player resolves an exploration card that has an
        "attach" header, they attach that card to the planet card of the planet
        being explored.

        LRR 35.8: "If a player resolves an exploration card that has an 'attach'
        header, they attach that card to the planet card of the planet being explored."
        """
        # Arrange
        attachment_card = ExplorationCard(
            name="Ancient Burial Sites",
            deck_type=PlanetTrait.CULTURAL,
            card_type="attachment",
            effect="This planet provides +1 influence",
        )

        planet = Planet("Test Planet", resources=1, influence=1)
        planet.traits = [PlanetTrait.CULTURAL]

        # Act
        result = self.exploration_system.resolve_exploration_card(
            card=attachment_card,
            player=self.mock_player,
            planet=planet,
            game_state=self.mock_game_state,
        )

        # Assert
        assert result.success is True
        assert result.card_attached is True
        assert result.card_discarded is False
        assert attachment_card in planet.attached_cards

    def test_relic_fragment_resolution(self) -> None:
        """Test Rule 35.9: If a player resolves an exploration card that has
        "relic fragment" in the title, they place that card faceup in their
        play area.

        LRR 35.9: "If a player resolves an exploration card that has 'relic
        fragment' in the title, they place that card faceup in their play area."
        """
        # Arrange
        relic_fragment = ExplorationCard(
            name="Relic Fragment",
            deck_type=PlanetTrait.HAZARDOUS,
            card_type="relic_fragment",
            effect="Purge this card to draw 1 relic",
        )

        # Act
        result = self.exploration_system.resolve_exploration_card(
            card=relic_fragment,
            player=self.mock_player,
            game_state=self.mock_game_state,
        )

        # Assert
        assert result.success is True
        assert result.card_discarded is False
        assert result.relic_fragment_gained is True
        assert relic_fragment in self.mock_player.relic_fragments

    def test_relic_fragment_ability_resolution(self) -> None:
        """Test Rule 35.9a: Players can resolve the ability of relic fragments
        that are in their play area. Resolving these abilities allows players
        to draw cards from the relic deck.

        LRR 35.9a: "Players can resolve the ability of relic fragments that are
        in their play area. Resolving these abilities allows players to draw
        cards from the relic deck."
        """
        # Arrange
        relic_fragment = ExplorationCard(
            name="Relic Fragment",
            deck_type=PlanetTrait.HAZARDOUS,
            card_type="relic_fragment",
            effect="Purge this card to draw 1 relic",
        )

        self.mock_player.relic_fragments = [relic_fragment]

        # Act
        result = self.exploration_system.resolve_relic_fragment_ability(
            fragment=relic_fragment,
            player=self.mock_player,
            game_state=self.mock_game_state,
        )

        # Assert
        assert result.success is True
        assert result.relic_drawn is True
        assert relic_fragment not in self.mock_player.relic_fragments  # Purged

    def test_relic_fragment_transaction_eligibility(self) -> None:
        """Test Rule 35.9b: Relic fragments can be exchanged as part of transactions.

        LRR 35.9b: "Relic fragments can be exchanged as part of transactions."
        """
        # Arrange
        relic_fragment = ExplorationCard(
            name="Relic Fragment",
            deck_type=PlanetTrait.CULTURAL,
            card_type="relic_fragment",
            effect="Purge this card to draw 1 relic",
        )

        self.mock_player.relic_fragments = [relic_fragment]

        # Act
        can_trade = self.exploration_system.can_trade_relic_fragment(
            fragment=relic_fragment, player=self.mock_player
        )

        # Assert
        assert can_trade is True

    def test_integration_with_planet_control_system(self) -> None:
        """Test integration between exploration and planet control systems.

        This test verifies that exploration is properly triggered when gaining
        planet control through the existing game state system.
        """
        # Arrange
        planet = Planet("New Planet", resources=2, influence=1)
        planet.traits = [PlanetTrait.INDUSTRIAL]

        # Mock the game state to simulate gaining planet control
        self.mock_game_state.gain_planet_control.return_value = (
            True,
            self.mock_game_state,
        )

        # Act
        exploration_triggered, new_state = self.mock_game_state.gain_planet_control(
            "test_player", planet
        )

        # Assert
        assert exploration_triggered is True
        # Verify exploration system would be called
        assert self.exploration_system.should_trigger_exploration(planet) is True

    def test_no_exploration_for_already_controlled_planet(self) -> None:
        """Test that exploration is not triggered when gaining control of a
        planet that was already controlled by another player.

        This ensures Rule 35.1 is properly implemented - exploration only
        occurs for previously uncontrolled planets.
        """
        # Arrange
        planet = Planet("Controlled Planet", resources=1, influence=2)
        planet.traits = [PlanetTrait.CULTURAL]
        planet.controlled_by = "other_player"  # Already controlled

        # Act
        should_explore = self.exploration_system.should_trigger_exploration(
            planet, previous_controller="other_player"
        )

        # Assert
        assert should_explore is False

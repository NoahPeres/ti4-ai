"""Integration tests for Rule 35 (Exploration) with existing game systems.

These tests verify that the exploration system properly integrates with:
- Planet control mechanics
- Game state management
- Player actions
- Component actions
"""

from unittest.mock import Mock, patch

from ti4.core import component_action
from ti4.core.constants import Faction
from ti4.core.exploration import ExplorationSystem, PlanetTrait
from ti4.core.game_state import GameState
from ti4.core.planet import Planet
from ti4.core.player import Player


class TestExplorationGameStateIntegration:
    """Test exploration integration with game state management."""

    def setup_method(self):
        """Set up test fixtures."""
        self.exploration_system = ExplorationSystem()
        self.player = Player("test_player", Faction.ARBOREC)
        self.game_state = GameState()

        # Create test planet with traits
        self.planet = Planet(name="Test Planet", resources=2, influence=1)
        self.planet.traits = [PlanetTrait.CULTURAL]

    def test_exploration_triggered_on_planet_control_change(self):
        """Test that exploration is triggered when planet control changes from uncontrolled."""
        # Planet starts uncontrolled
        assert self.planet.controlled_by is None

        # Player takes control - should trigger exploration
        result = self.exploration_system.explore_planet(
            self.player, self.planet, self.game_state
        )

        assert result.success
        assert result.exploration_triggered
        assert result.deck_used == PlanetTrait.CULTURAL
        assert result.card_drawn is not None

    def test_no_exploration_when_planet_already_controlled(self):
        """Test that exploration is not triggered when taking planet from another player."""
        # Set planet as controlled by another player
        other_player = Player("other_player", Faction.BARONY)
        self.planet.controlled_by = other_player.id

        # Current player takes control - should NOT trigger exploration
        # (since planet was already controlled)
        # Since the exploration system doesn't track previous state automatically,
        # we need to use the should_trigger_exploration method directly
        should_explore = self.exploration_system.should_trigger_exploration(
            self.planet, previous_controller=other_player.id
        )

        assert not should_explore

    def test_forced_exploration_overrides_control_check(self):
        """Test that forced exploration works even when planet was controlled."""
        # Set planet as controlled by another player
        other_player = Player("other_player", Faction.BARONY)
        self.planet.controlled_by = other_player.id

        # Force exploration should work
        result = self.exploration_system.explore_planet(
            self.player, self.planet, self.game_state, force_exploration=True
        )

        assert result.success
        assert result.exploration_triggered
        assert result.card_drawn is not None

    def test_exploration_with_traitless_planet(self):
        """Test that traitless planets cannot be explored."""
        traitless_planet = Planet(name="Traitless Planet", resources=1, influence=1)
        traitless_planet.traits = []

        result = self.exploration_system.explore_planet(
            self.player, traitless_planet, self.game_state
        )

        assert result.success
        assert not result.exploration_triggered

    def test_multiple_planet_exploration_order(self):
        """Test that multiple planets are explored in the correct order."""
        planets = []

        planet_a = Planet("Planet A", 1, 1)
        planet_a.traits = [PlanetTrait.CULTURAL]
        planets.append(planet_a)

        planet_b = Planet("Planet B", 2, 0)
        planet_b.traits = [PlanetTrait.HAZARDOUS]
        planets.append(planet_b)

        planet_c = Planet("Planet C", 0, 2)
        planet_c.traits = [PlanetTrait.INDUSTRIAL]
        planets.append(planet_c)

        results = self.exploration_system.explore_multiple_planets(
            self.player, planets, self.game_state
        )

        assert len(results) == 3
        assert results[0].planet_name == "Planet A"
        assert results[1].planet_name == "Planet B"
        assert results[2].planet_name == "Planet C"

        # All should have triggered exploration
        for result in results:
            assert result.exploration_triggered
            assert result.card_drawn is not None


class TestExplorationPlayerIntegration:
    """Test exploration integration with player state."""

    def setup_method(self):
        """Set up test fixtures."""
        self.exploration_system = ExplorationSystem()
        self.player = Player("test_player", Faction.ARBOREC)
        self.game_state = GameState()

    def test_relic_fragment_added_to_player(self):
        """Test that relic fragments are properly added to player."""
        # Mock a relic fragment card
        with patch.object(
            self.exploration_system, "_draw_exploration_card"
        ) as mock_draw:
            from ti4.core.exploration import CardType, ExplorationCard

            relic_card = ExplorationCard(
                "Test Relic Fragment",
                PlanetTrait.CULTURAL.value,
                CardType.RELIC_FRAGMENT.value,
                "Test relic fragment",
            )
            mock_draw.return_value = relic_card

            planet = Planet("Test Planet", 1, 1)
            planet.traits = [PlanetTrait.CULTURAL]
            result = self.exploration_system.explore_planet(
                self.player, planet, self.game_state
            )

            assert result.relic_fragment_gained
            assert hasattr(self.player, "relic_fragments")
            assert relic_card in self.player.relic_fragments

    def test_attachment_card_added_to_planet(self):
        """Test that attachment cards are properly attached to planets."""
        with patch.object(
            self.exploration_system, "_draw_exploration_card"
        ) as mock_draw:
            from ti4.core.exploration import CardType, ExplorationCard

            attachment_card = ExplorationCard(
                "Test Attachment",
                PlanetTrait.INDUSTRIAL.value,
                CardType.ATTACHMENT.value,
                "Test attachment effect",
            )
            mock_draw.return_value = attachment_card

            planet = Planet("Test Planet", 2, 0)
            planet.traits = [PlanetTrait.INDUSTRIAL]
            result = self.exploration_system.explore_planet(
                self.player, planet, self.game_state
            )

            assert result.card_attached
            assert hasattr(planet, "attached_cards")
            assert attachment_card in planet.attached_cards

    def test_relic_fragment_ability_resolution(self):
        """Test that relic fragment abilities can be resolved."""
        from ti4.core.exploration import CardType, ExplorationCard

        # Add relic fragment to player
        fragment = ExplorationCard(
            "Test Fragment",
            PlanetTrait.CULTURAL.value,
            CardType.RELIC_FRAGMENT.value,
            "Purge to draw relic",
        )

        if not hasattr(self.player, "relic_fragments"):
            self.player.relic_fragments = []
        self.player.relic_fragments.append(fragment)

        # Resolve the fragment ability
        result = self.exploration_system.resolve_relic_fragment_ability(
            fragment, self.player, self.game_state
        )

        assert result.success
        assert result.relic_drawn
        assert fragment not in self.player.relic_fragments  # Should be purged

    def test_relic_fragment_trading_eligibility(self):
        """Test that relic fragments can be identified for trading."""
        from ti4.core.exploration import CardType, ExplorationCard

        fragment = ExplorationCard(
            "Tradeable Fragment",
            PlanetTrait.HAZARDOUS.value,
            CardType.RELIC_FRAGMENT.value,
            "Test fragment",
        )

        # Fragment not owned - cannot trade
        assert not self.exploration_system.can_trade_relic_fragment(
            fragment, self.player
        )

        # Add fragment to player
        if not hasattr(self.player, "relic_fragments"):
            self.player.relic_fragments = []
        self.player.relic_fragments.append(fragment)

        # Now can trade
        assert self.exploration_system.can_trade_relic_fragment(fragment, self.player)


class TestExplorationFrontierIntegration:
    """Test exploration integration with frontier tokens."""

    def setup_method(self):
        """Set up test fixtures."""
        self.exploration_system = ExplorationSystem()
        self.player = Player("test_player", Faction.ARBOREC)
        self.game_state = GameState()

    def test_frontier_token_exploration(self):
        """Test exploration of frontier tokens."""
        # Mock system with frontier token
        mock_system = Mock()
        mock_system.has_frontier_token = True
        mock_system.remove_frontier_token = Mock()

        result = self.exploration_system.explore_frontier_token(
            self.player, mock_system, self.game_state
        )

        assert result.success
        assert result.exploration_triggered
        assert result.deck_used == "frontier"
        assert result.card_drawn is not None
        assert result.frontier_token_removed
        mock_system.remove_frontier_token.assert_called_once()

    def test_frontier_exploration_without_token(self):
        """Test that systems without frontier tokens cannot be explored."""
        mock_system = Mock()
        mock_system.has_frontier_token = False

        result = self.exploration_system.explore_frontier_token(
            self.player, mock_system, self.game_state
        )

        assert not result.success
        assert not result.exploration_triggered


class TestExplorationComponentActionIntegration:
    """Test exploration integration with component actions."""

    def setup_method(self):
        """Set up test fixtures."""
        self.exploration_system = ExplorationSystem()
        self.player = Player("test_player", Faction.ARBOREC)
        self.game_state = GameState()

    def test_exploration_component_action_constant(self):
        """Test that exploration component action constant exists."""
        # This verifies integration with the component action system
        # The EXPLORATION constant is in ComponentActionType enum
        assert hasattr(component_action.ComponentActionType, "EXPLORATION")
        assert component_action.ComponentActionType.EXPLORATION.value == "exploration"

    def test_exploration_triggered_in_game_state(self):
        """Test that game state can handle exploration triggers."""
        # This tests the existing exploration trigger logic in game_state.py
        planet = Planet("Test Planet", 1, 1)
        planet.traits = [PlanetTrait.CULTURAL]

        # The game state should be able to handle exploration triggers
        # This is a placeholder test for the existing logic in game_state.py
        # that returns (exploration_triggered, new_game_state)

        # In a full integration, this would test the actual game state method
        # For now, we verify the exploration system can work with game state
        result = self.exploration_system.explore_planet(
            self.player, planet, self.game_state
        )

        assert result.success
        assert result.exploration_triggered


class TestExplorationDeckManagement:
    """Test exploration deck management and card cycling."""

    def setup_method(self):
        """Set up test fixtures."""
        self.exploration_system = ExplorationSystem()
        self.player = Player("test_player", Faction.ARBOREC)
        self.game_state = GameState()

    def test_deck_reshuffling_when_empty(self):
        """Test that decks reshuffle when empty."""
        deck = self.exploration_system.decks[PlanetTrait.CULTURAL.value]

        # Draw all cards to empty the deck
        drawn_cards = []
        while deck.cards:
            card = deck.draw_card()
            if card:
                drawn_cards.append(card)
                # Discard normal cards to build discard pile
                if not card.is_attachment and not card.is_relic_fragment:
                    deck.discard_card(card)

        # Deck should be empty, discard pile should have cards
        assert len(deck.cards) == 0
        assert len(deck.discard_pile) > 0

        # Drawing another card should reshuffle
        card = deck.draw_card()
        assert card is not None
        assert (
            len(deck.discard_pile) == 0
        )  # Discard pile should be empty after reshuffle

    def test_multiple_trait_planet_deck_selection(self):
        """Test deck selection for planets with multiple traits."""
        multi_trait_planet = Planet("Multi-Trait Planet", 2, 2)
        multi_trait_planet.traits = [PlanetTrait.CULTURAL, PlanetTrait.HAZARDOUS]

        # Test with chosen trait
        result = self.exploration_system.explore_planet(
            self.player,
            multi_trait_planet,
            self.game_state,
            chosen_trait=PlanetTrait.HAZARDOUS,
        )

        assert result.success
        assert result.exploration_triggered
        assert result.deck_used == PlanetTrait.HAZARDOUS

        # Test default behavior (should use first trait)
        result2 = self.exploration_system.explore_planet(
            self.player, multi_trait_planet, self.game_state
        )

        assert result2.success
        assert result2.exploration_triggered
        assert result2.deck_used == PlanetTrait.CULTURAL  # First trait

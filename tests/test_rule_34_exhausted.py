"""Tests for Rule 34: EXHAUSTED mechanics.

This module tests the exhausted card system according to TI4 LRR Rule 34.
All tests follow strict TDD methodology with RED-GREEN-REFACTOR cycles.

Rule 34 Sub-rules tested:
- 34.0: General exhausted mechanics - cannot resolve abilities or spend resources/influence
- 34.1: Exhausting cards - flip facedown
- 34.2: Status phase ready cards step - readies all exhausted cards
- 34.3: Planet cards exhausted to spend resources/influence
- 34.4: Technology cards exhausted for abilities; cannot exhaust already exhausted
- 34.4a: Passive abilities still work on exhausted cards
- 34.5: Strategy cards exhausted after strategic actions (already implemented)
"""

import pytest

from tests.test_constants import MockPlayer
from ti4.core.planet import Planet


class TestRule34GeneralExhaustedMechanics:
    """Test general exhausted card mechanics (Rule 34.0)."""

    def test_exhausted_card_cannot_spend_resources(self) -> None:
        """Test that exhausted cards cannot spend resources.

        LRR Reference: Rule 34.0 - "A player cannot...spend the resources...of an exhausted card"
        """
        # RED: This will fail until we implement exhausted state for planets
        planet = Planet("Test Planet", resources=3, influence=2)
        planet.set_control(
            MockPlayer.PLAYER_1.value
        )  # Planet must be controlled to spend resources

        # Planet should start readied
        assert not planet.is_exhausted()
        assert planet.can_spend_resources()

        # Exhaust the planet
        planet.exhaust()

        # Should not be able to spend resources when exhausted
        assert planet.is_exhausted()
        assert not planet.can_spend_resources()

    def test_exhausted_card_cannot_spend_influence(self) -> None:
        """Test that exhausted cards cannot spend influence.

        LRR Reference: Rule 34.0 - "A player cannot...spend the...influence of an exhausted card"
        """
        # RED: This will fail until we implement exhausted state for planets
        planet = Planet("Test Planet", resources=3, influence=2)
        planet.set_control(
            MockPlayer.PLAYER_1.value
        )  # Planet must be controlled to spend influence

        # Planet should start readied
        assert not planet.is_exhausted()
        assert planet.can_spend_influence()

        # Exhaust the planet
        planet.exhaust()

        # Should not be able to spend influence when exhausted
        assert planet.is_exhausted()
        assert not planet.can_spend_influence()

    def test_exhausted_card_cannot_resolve_abilities(self) -> None:
        """Test that exhausted cards cannot resolve abilities.

        LRR Reference: Rule 34.0 - "A player cannot resolve abilities...of an exhausted card"
        """
        # RED: This will fail until we implement technology card exhausted state
        from ti4.core.technology import TechnologyCard

        tech_card = TechnologyCard("Test Tech", "Test ability that requires exhaustion")

        # Technology should start readied
        assert not tech_card.is_exhausted()
        assert tech_card.can_resolve_abilities()

        # Exhaust the technology
        tech_card.exhaust()

        # Should not be able to resolve abilities when exhausted
        assert tech_card.is_exhausted()
        assert not tech_card.can_resolve_abilities()


class TestRule34ExhaustingCards:
    """Test card exhaustion mechanics (Rule 34.1)."""

    def test_exhaust_card_flips_facedown(self) -> None:
        """Test that exhausting a card flips it facedown.

        LRR Reference: Rule 34.1 - "To exhaust a card, a player flips the card facedown"
        """
        # RED: This will fail until we implement exhausted state
        planet = Planet("Test Planet", resources=3, influence=2)

        # Planet should start faceup (readied)
        assert planet.is_faceup()
        assert not planet.is_exhausted()

        # Exhaust the planet
        planet.exhaust()

        # Should now be facedown (exhausted)
        assert not planet.is_faceup()
        assert planet.is_exhausted()

    def test_ready_card_flips_faceup(self) -> None:
        """Test that readying a card flips it faceup.

        LRR Reference: Rule 34.2 - "readies all of their exhausted cards by flipping those cards faceup"
        """
        # RED: This will fail until we implement exhausted state
        planet = Planet("Test Planet", resources=3, influence=2)

        # Exhaust the planet first
        planet.exhaust()
        assert not planet.is_faceup()
        assert planet.is_exhausted()

        # Ready the planet
        planet.ready()

        # Should now be faceup (readied)
        assert planet.is_faceup()
        assert not planet.is_exhausted()


class TestRule34StatusPhaseReadyCards:
    """Test status phase ready cards step (Rule 34.2)."""

    def test_status_phase_readies_all_exhausted_cards(self) -> None:
        """Test that status phase readies all exhausted cards.

        LRR Reference: Rule 34.2 - "During the 'Ready Cards' step of the status phase,
        each player readies all of their exhausted cards"
        """
        # RED: This will fail until we implement status phase card readying
        from ti4.core.game_state import GameState
        from ti4.core.status_phase import StatusPhaseManager

        # Create game state with exhausted cards
        game_state = GameState()

        # Add planets to player
        planet1 = Planet("Planet 1", resources=3, influence=2)
        planet2 = Planet("Planet 2", resources=2, influence=3)
        planet1.set_control(MockPlayer.PLAYER_1.value)
        planet2.set_control(MockPlayer.PLAYER_1.value)

        # Exhaust both planets
        planet1.exhaust()
        planet2.exhaust()

        # Add to game state
        game_state = game_state.add_player_planet(MockPlayer.PLAYER_1.value, planet1)
        game_state = game_state.add_player_planet(MockPlayer.PLAYER_1.value, planet2)

        # Both should be exhausted
        assert planet1.is_exhausted()
        assert planet2.is_exhausted()

        # Execute ready cards step
        status_manager = StatusPhaseManager()
        new_game_state = status_manager.ready_all_cards(game_state)

        # All cards should now be readied
        player_planets = new_game_state.get_player_planets(MockPlayer.PLAYER_1.value)
        for planet in player_planets:
            assert not planet.is_exhausted()

    def test_ready_cards_affects_all_card_types(self) -> None:
        """Test that ready cards step affects all card types.

        LRR Reference: Rule 34.2 - "each player readies all of their exhausted cards"
        """
        # RED: This will fail until we implement comprehensive card readying
        from ti4.core.game_state import GameState
        from ti4.core.status_phase import StatusPhaseManager
        from ti4.core.strategic_action import StrategyCardType
        from ti4.core.technology import TechnologyCard

        # Create game state with various exhausted cards
        game_state = GameState()

        # Exhaust planet card
        planet = Planet("Test Planet", resources=3, influence=2)
        planet.set_control(MockPlayer.PLAYER_1.value)
        planet.exhaust()
        game_state = game_state.add_player_planet(MockPlayer.PLAYER_1.value, planet)

        # Exhaust technology card
        tech_card = TechnologyCard("Test Tech", "Test ability")
        tech_card.exhaust()
        game_state = game_state.add_player_technology(
            MockPlayer.PLAYER_1.value, tech_card
        )

        # Exhaust strategy card
        game_state = game_state.exhaust_strategy_card(StrategyCardType.LEADERSHIP)

        # All should be exhausted
        assert planet.is_exhausted()
        assert tech_card.is_exhausted()
        assert StrategyCardType.LEADERSHIP in game_state.exhausted_strategy_cards

        # Execute ready cards step
        status_manager = StatusPhaseManager()
        new_game_state = status_manager.ready_all_cards(game_state)

        # All cards should now be readied
        player_planets = new_game_state.get_player_planets(MockPlayer.PLAYER_1.value)
        player_tech_cards = new_game_state.get_player_technology_cards(
            MockPlayer.PLAYER_1.value
        )

        assert not player_planets[0].is_exhausted()
        assert not player_tech_cards[0].is_exhausted()
        assert (
            StrategyCardType.LEADERSHIP not in new_game_state.exhausted_strategy_cards
        )


class TestRule34PlanetCardExhaustion:
    """Test planet card exhaustion mechanics (Rule 34.3)."""

    def test_player_exhausts_planet_to_spend_resources(self) -> None:
        """Test that players exhaust planet cards to spend resources.

        LRR Reference: Rule 34.3 - "A player exhausts their planet cards to spend either the resources...on that card"
        """
        # RED: This will fail until we implement resource spending
        planet = Planet("Test Planet", resources=3, influence=2)
        planet.set_control(MockPlayer.PLAYER_1.value)

        # Should start readied
        assert not planet.is_exhausted()

        # Spend resources - should exhaust the planet
        resources_spent = planet.spend_resources(2)

        assert resources_spent == 2
        assert planet.is_exhausted()

    def test_player_exhausts_planet_to_spend_influence(self) -> None:
        """Test that players exhaust planet cards to spend influence.

        LRR Reference: Rule 34.3 - "A player exhausts their planet cards to spend either the...influence on that card"
        """
        # RED: This will fail until we implement influence spending
        planet = Planet("Test Planet", resources=3, influence=2)
        planet.set_control(MockPlayer.PLAYER_1.value)

        # Should start readied
        assert not planet.is_exhausted()

        # Spend influence - should exhaust the planet
        influence_spent = planet.spend_influence(1)

        assert influence_spent == 1
        assert planet.is_exhausted()

    def test_cannot_spend_from_exhausted_planet(self) -> None:
        """Test that exhausted planets cannot spend resources or influence.

        LRR Reference: Rule 34.0, 64.9 - "A player cannot spend an exhausted planet's resources or influence"
        """
        # RED: This will fail until we implement exhausted state validation
        planet = Planet("Test Planet", resources=3, influence=2)
        planet.set_control(MockPlayer.PLAYER_1.value)

        # Exhaust the planet
        planet.exhaust()

        # Should not be able to spend resources or influence
        with pytest.raises(ValueError, match="Cannot spend from exhausted planet"):
            planet.spend_resources(1)

        with pytest.raises(ValueError, match="Cannot spend from exhausted planet"):
            planet.spend_influence(1)


class TestRule34TechnologyCardExhaustion:
    """Test technology card exhaustion mechanics (Rule 34.4)."""

    def test_abilities_instruct_player_to_exhaust_card(self) -> None:
        """Test that abilities can instruct players to exhaust cards.

        LRR Reference: Rule 34.4 - "Abilities...may instruct a player to exhaust a card to resolve those abilities"
        """
        # RED: This will fail until we implement technology card exhaustion
        from ti4.core.technology import TechnologyCard

        tech_card = TechnologyCard(
            "Test Tech", "Exhaust this card: Gain 1 command token"
        )

        # Should start readied
        assert not tech_card.is_exhausted()

        # Use ability - should exhaust the card
        result = tech_card.use_ability()

        assert result == "Gained 1 command token"
        assert tech_card.is_exhausted()

    def test_cannot_exhaust_already_exhausted_card(self) -> None:
        """Test that already exhausted cards cannot be exhausted again.

        LRR Reference: Rule 34.4 - "If a card is already exhausted, it cannot be exhausted again"
        """
        # RED: This will fail until we implement exhaustion validation
        from ti4.core.technology import TechnologyCard

        tech_card = TechnologyCard(
            "Test Tech", "Exhaust this card: Gain 1 command token"
        )

        # Exhaust the card
        tech_card.exhaust()
        assert tech_card.is_exhausted()

        # Should not be able to exhaust again
        with pytest.raises(ValueError, match="Card is already exhausted"):
            tech_card.exhaust()

    def test_passive_abilities_work_on_exhausted_cards(self) -> None:
        """Test that passive abilities still work on exhausted cards.

        LRR Reference: Rule 34.4a - "Passive abilities on an exhausted card are still in effect while that card is exhausted"
        """
        # RED: This will fail until we implement passive ability mechanics
        from ti4.core.technology import TechnologyCard

        tech_card = TechnologyCard("Test Tech", "Passive: +1 to all combat rolls")
        tech_card.add_passive_ability("combat_bonus", 1)

        # Should have passive ability when readied
        assert tech_card.get_passive_ability("combat_bonus") == 1

        # Exhaust the card
        tech_card.exhaust()

        # Passive ability should still work
        assert tech_card.get_passive_ability("combat_bonus") == 1


class TestRule34IntegrationWithExistingSystems:
    """Test Rule 34 integration with existing strategy card system."""

    def test_strategy_card_exhaustion_already_implemented(self) -> None:
        """Test that strategy card exhaustion is already working.

        LRR Reference: Rule 34.5 - "After a player performs a strategic action, they exhaust the strategy card"
        """
        # This should pass - strategy card exhaustion is already implemented
        from ti4.core.game_state import GameState
        from ti4.core.strategic_action import StrategyCardType

        game_state = GameState()

        # Should start with no exhausted cards
        assert len(game_state.exhausted_strategy_cards) == 0

        # Exhaust a strategy card
        new_state = game_state.exhaust_strategy_card(StrategyCardType.LEADERSHIP)

        # Should be exhausted
        assert StrategyCardType.LEADERSHIP in new_state.exhausted_strategy_cards

    def test_comprehensive_card_readying_in_status_phase(self) -> None:
        """Test that status phase readies all types of exhausted cards.

        LRR Reference: Rule 34.2 - "each player readies all of their exhausted cards"
        """
        # RED: This will fail until we implement comprehensive status phase readying
        from ti4.core.game_state import GameState
        from ti4.core.status_phase import StatusPhaseManager
        from ti4.core.strategic_action import StrategyCardType
        from ti4.core.technology import TechnologyCard

        # Create game state with all types of exhausted cards
        game_state = GameState()

        # Exhaust planet
        planet = Planet("Test Planet", resources=3, influence=2)
        planet.set_control(MockPlayer.PLAYER_1.value)
        planet.exhaust()
        game_state = game_state.add_player_planet(MockPlayer.PLAYER_1.value, planet)

        # Exhaust technology
        tech = TechnologyCard("Test Tech", "Test ability")
        tech.exhaust()
        game_state = game_state.add_player_technology(MockPlayer.PLAYER_1.value, tech)

        # Exhaust strategy card
        game_state = game_state.exhaust_strategy_card(StrategyCardType.WARFARE)

        # Execute status phase ready cards step
        status_manager = StatusPhaseManager()
        new_state = status_manager.ready_all_cards(game_state)

        # All cards should be readied
        player_planets = new_state.get_player_planets(MockPlayer.PLAYER_1.value)
        player_tech_cards = new_state.get_player_technology_cards(
            MockPlayer.PLAYER_1.value
        )

        assert not player_planets[0].is_exhausted()
        assert not player_tech_cards[0].is_exhausted()
        assert StrategyCardType.WARFARE not in new_state.exhausted_strategy_cards

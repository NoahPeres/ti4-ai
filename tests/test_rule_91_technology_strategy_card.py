"""Tests for Rule 91: TECHNOLOGY (Strategy Card) mechanics.

This module tests the Technology strategy card system according to TI4 LRR Rule 91.
All tests follow strict TDD methodology with RED-GREEN-REFACTOR cycles.

LRR Reference: Rule 91 - TECHNOLOGY (STRATEGY CARD)
"""

from tests.test_constants import MockPlayer
from ti4.core.constants import Technology


class TestRule91TechnologyStrategyCardBasics:
    """Test basic Technology strategy card mechanics (Rule 91.0)."""

    def test_technology_strategy_card_exists(self) -> None:
        """Test that Technology strategy card can be imported and instantiated.

        This is the first RED test - it will fail until we create the system.

        LRR Reference: Rule 91.0 - The "Technology" strategy card allows players to research new technology
        """
        # RED: This will fail until we create TechnologyStrategyCard
        from ti4.core.technology_strategy_card import TechnologyStrategyCard

        card = TechnologyStrategyCard()
        assert card is not None

    def test_technology_strategy_card_has_initiative_seven(self) -> None:
        """Test that Technology strategy card has initiative value 7.

        LRR Reference: Rule 91.0 - This card's initiative value is "7"
        """
        from ti4.core.technology_strategy_card import TechnologyStrategyCard

        card = TechnologyStrategyCard()
        assert card.get_initiative_value() == 7


class TestRule91PrimaryAbility:
    """Test Technology strategy card primary ability (Rule 91.2)."""

    def test_primary_ability_allows_one_free_research(self) -> None:
        """Test that primary ability allows researching one technology for free.

        LRR Reference: Rule 91.2 - The active player can research one technology of their choice
        """
        from ti4.core.technology_strategy_card import TechnologyStrategyCard

        card = TechnologyStrategyCard()

        # RED: This will fail until we implement primary ability
        result = card.execute_primary_ability(
            MockPlayer.PLAYER_1.value, technology=Technology.ANTIMASS_DEFLECTORS
        )
        assert result.success is True
        assert (
            result.additional_data["technology_researched"]
            == Technology.ANTIMASS_DEFLECTORS
        )
        assert result.resources_spent == 0  # First research is free

    def test_primary_ability_allows_second_research_for_six_resources(self) -> None:
        """Test that primary ability allows second research for 6 resources.

        LRR Reference: Rule 91.2 - Then may research one additional technology by spending six resources
        """
        from ti4.core.technology_strategy_card import TechnologyStrategyCard

        card = TechnologyStrategyCard()

        # RED: This will fail until we implement second research option
        result = card.execute_primary_ability_second_research(
            MockPlayer.PLAYER_1.value, Technology.GRAVITY_DRIVE, available_resources=6
        )
        assert result.success is True
        assert result.technology_researched == Technology.GRAVITY_DRIVE
        assert result.resources_spent == 6

    def test_primary_ability_second_research_fails_without_resources(self) -> None:
        """Test that second research fails without sufficient resources.

        LRR Reference: Rule 91.2 - May research additional technology by spending six resources
        """
        from ti4.core.technology_strategy_card import TechnologyStrategyCard

        card = TechnologyStrategyCard()

        # Should fail with insufficient resources
        result = card.execute_primary_ability_second_research(
            MockPlayer.PLAYER_1.value, Technology.GRAVITY_DRIVE, available_resources=5
        )
        assert result.success is False
        assert result.resources_spent == 0


class TestRule91SecondaryAbility:
    """Test Technology strategy card secondary ability (Rule 91.3)."""

    def test_secondary_ability_costs_command_token_and_four_resources(self) -> None:
        """Test that secondary ability costs 1 command token and 4 resources.

        LRR Reference: Rule 91.3 - Each other player may research one technology by spending
        one command token from their strategy pool and four resources
        """
        from ti4.core.technology_strategy_card import TechnologyStrategyCard

        card = TechnologyStrategyCard()

        # RED: This will fail until we implement secondary ability
        result = card.execute_secondary_ability(
            MockPlayer.PLAYER_2.value,
            technology=Technology.ANTIMASS_DEFLECTORS,
            available_command_tokens=2,
            available_resources=4,
        )
        assert result.success is True
        assert (
            result.additional_data["technology_researched"]
            == Technology.ANTIMASS_DEFLECTORS
        )
        assert result.command_tokens_spent == 1
        assert result.resources_spent == 4

    def test_secondary_ability_fails_without_command_token(self) -> None:
        """Test that secondary ability fails without command token.

        LRR Reference: Rule 91.3 - Must spend one command token from strategy pool
        """
        from ti4.core.technology_strategy_card import TechnologyStrategyCard

        card = TechnologyStrategyCard()

        result = card.execute_secondary_ability(
            MockPlayer.PLAYER_2.value,
            technology=Technology.ANTIMASS_DEFLECTORS,
            available_command_tokens=0,  # No command tokens
            available_resources=4,
        )
        assert result.success is False
        assert result.command_tokens_spent == 0
        assert result.resources_spent == 0

    def test_secondary_ability_fails_without_resources(self) -> None:
        """Test that secondary ability fails without sufficient resources.

        LRR Reference: Rule 91.3 - Must spend four resources
        """
        from ti4.core.technology_strategy_card import TechnologyStrategyCard

        card = TechnologyStrategyCard()

        result = card.execute_secondary_ability(
            MockPlayer.PLAYER_2.value,
            technology=Technology.ANTIMASS_DEFLECTORS,
            available_command_tokens=2,
            available_resources=3,  # Insufficient resources
        )
        assert result.success is False
        assert result.command_tokens_spent == 0
        assert result.resources_spent == 0


class TestRule91StrategyCardIntegration:
    """Test Technology strategy card integration with existing systems."""

    def test_integrates_with_strategic_action_system(self) -> None:
        """Test that Technology strategy card integrates with strategic action system.

        LRR Reference: Rule 91.1 - During action phase, active player can perform strategic action
        """
        from ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCard,
            StrategyCardType,
        )

        # Create a strategy card for the technology card
        tech_strategy_card = StrategyCard(
            card_type=StrategyCardType.TECHNOLOGY,
            primary_ability="Research technology",
            secondary_ability="Research technology for cost",
        )

        action_manager = StrategicActionManager()
        action_manager.set_action_phase(True)
        action_manager.set_player_order([MockPlayer.PLAYER_1.value])
        action_manager.assign_strategy_card(
            MockPlayer.PLAYER_1.value, tech_strategy_card
        )

        # Test that we can activate the technology strategy card
        result = action_manager.activate_strategy_card(
            MockPlayer.PLAYER_1.value, StrategyCardType.TECHNOLOGY
        )
        assert result.success is True

    def test_integrates_with_technology_manager(self) -> None:
        """Test that Technology strategy card integrates with technology research system.

        LRR Reference: Rule 91.2/91.3 - Card allows researching technologies
        """
        from ti4.core.technology import TechnologyManager
        from ti4.core.technology_strategy_card import TechnologyStrategyCard

        card = TechnologyStrategyCard()
        tech_manager = TechnologyManager()

        # Should use existing technology research validation
        # RED: This will fail until we integrate systems
        can_research = card.validate_technology_research(
            MockPlayer.PLAYER_1.value, Technology.ANTIMASS_DEFLECTORS, tech_manager
        )
        assert can_research is True

    def test_full_game_state_integration(self) -> None:
        """Test that Technology strategy card integrates with full game state system.

        This tests the complete integration with GameTechnologyManager and game state.
        """
        from ti4.core.game_technology_manager import GameTechnologyManager
        from ti4.core.technology_strategy_card import TechnologyStrategyCard

        # Use the mock game state from technology integration tests
        class MockGameState:
            def __init__(self):
                self.players = {}
                self.player_technologies = {}
                self.round_number = 1
                self.technology_research_history = []

            def add_player(self, player_id, faction=None):
                from tests.test_technology_integration import MockPlayerState

                self.players[player_id] = MockPlayerState(player_id, faction)
                self.player_technologies[player_id] = []

            def get_player_state(self, player_id):
                return self.players.get(player_id)

            def get_technology_research_history(self):
                return self.technology_research_history

            def add_technology_research_event(
                self, player_id, technology, round_number
            ):
                event = {
                    "player_id": player_id,
                    "technology": technology,
                    "round_number": str(round_number),
                }
                self.technology_research_history.append(event)

            def validate_consistency(self):
                return []

        # Create integrated system
        game_state = MockGameState()
        game_state.add_player(MockPlayer.PLAYER_1.value)
        game_tech_manager = GameTechnologyManager(game_state)

        card = TechnologyStrategyCard()

        # Test primary ability with full integration
        result = card.execute_primary_ability(
            MockPlayer.PLAYER_1.value,
            technology=Technology.ANTIMASS_DEFLECTORS,
            game_tech_manager=game_tech_manager,
        )

        assert result.success is True
        assert (
            result.additional_data["technology_researched"]
            == Technology.ANTIMASS_DEFLECTORS
        )
        assert result.resources_spent == 0  # Free research

        # Verify technology was actually added to game state
        player_technologies = game_tech_manager.get_player_technologies(
            MockPlayer.PLAYER_1.value
        )
        assert Technology.ANTIMASS_DEFLECTORS in player_technologies

    def test_prerequisite_validation_with_integration(self) -> None:
        """Test that prerequisite validation works with full integration."""
        from ti4.core.game_technology_manager import GameTechnologyManager
        from ti4.core.technology_strategy_card import TechnologyStrategyCard

        # Use the same mock as above
        class MockGameState:
            def __init__(self):
                self.players = {}
                self.player_technologies = {}
                self.round_number = 1
                self.technology_research_history = []

            def add_player(self, player_id, faction=None):
                from tests.test_technology_integration import MockPlayerState

                self.players[player_id] = MockPlayerState(player_id, faction)
                self.player_technologies[player_id] = []

            def get_player_state(self, player_id):
                return self.players.get(player_id)

            def get_technology_research_history(self):
                return self.technology_research_history

            def add_technology_research_event(
                self, player_id, technology, round_number
            ):
                event = {
                    "player_id": player_id,
                    "technology": technology,
                    "round_number": str(round_number),
                }
                self.technology_research_history.append(event)

            def validate_consistency(self):
                return []

        # Create integrated system
        game_state = MockGameState()
        game_state.add_player(MockPlayer.PLAYER_1.value)
        game_tech_manager = GameTechnologyManager(game_state)

        card = TechnologyStrategyCard()

        # Try to research technology with prerequisites (should fail)
        result = card.execute_primary_ability(
            MockPlayer.PLAYER_1.value,
            technology=Technology.CRUISER_II,  # Requires prerequisites
            game_tech_manager=game_tech_manager,
        )

        assert result.success is False
        assert "prerequisites not met" in result.error_message

    def test_secondary_ability_integration(self) -> None:
        """Test that secondary ability works with full integration."""
        from ti4.core.game_technology_manager import GameTechnologyManager
        from ti4.core.technology_strategy_card import TechnologyStrategyCard

        # Use the same mock as above
        class MockGameState:
            def __init__(self):
                self.players = {}
                self.player_technologies = {}
                self.round_number = 1
                self.technology_research_history = []

            def add_player(self, player_id, faction=None):
                from tests.test_technology_integration import MockPlayerState

                self.players[player_id] = MockPlayerState(player_id, faction)
                self.player_technologies[player_id] = []

            def get_player_state(self, player_id):
                return self.players.get(player_id)

            def get_technology_research_history(self):
                return self.technology_research_history

            def add_technology_research_event(
                self, player_id, technology, round_number
            ):
                event = {
                    "player_id": player_id,
                    "technology": technology,
                    "round_number": str(round_number),
                }
                self.technology_research_history.append(event)

            def validate_consistency(self):
                return []

        # Create integrated system
        game_state = MockGameState()
        game_state.add_player(MockPlayer.PLAYER_2.value)
        game_tech_manager = GameTechnologyManager(game_state)

        card = TechnologyStrategyCard()

        # Test secondary ability with full integration
        result = card.execute_secondary_ability(
            MockPlayer.PLAYER_2.value,
            technology=Technology.ANTIMASS_DEFLECTORS,
            available_command_tokens=2,
            available_resources=4,
            game_tech_manager=game_tech_manager,
        )

        assert result.success is True
        assert (
            result.additional_data["technology_researched"]
            == Technology.ANTIMASS_DEFLECTORS
        )
        assert result.command_tokens_spent == 1
        assert result.resources_spent == 4

        # Verify technology was actually added to game state
        player_technologies = game_tech_manager.get_player_technologies(
            MockPlayer.PLAYER_2.value
        )
        assert Technology.ANTIMASS_DEFLECTORS in player_technologies

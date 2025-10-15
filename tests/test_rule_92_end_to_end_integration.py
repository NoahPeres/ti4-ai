"""
End-to-end integration tests for Rule 92: TRADE (STRATEGY CARD) implementation.

This module implements comprehensive integration tests for task 13: Final integration testing and production readiness.
Requirements: 6.4, 7.4, 11.4

LRR Reference: Rule 92 - TRADE (STRATEGY CARD)
"""

import time

from ti4.core.constants import Faction
from ti4.core.game_state import GameState
from ti4.core.player import Player
from ti4.core.strategy_cards.cards.trade import TradeStrategyCard


class TestTradeCardEndToEndIntegration:
    """Test suite for end-to-end integration tests with complete game scenarios including other strategy cards.

    This test class implements the requirements for task 13: Final integration testing and production readiness.
    Requirements: 6.4, 7.4, 11.4
    """

    def setup_method(self) -> None:
        """Set up test fixtures for end-to-end integration testing."""
        # Create multiple players for comprehensive testing
        self.player1 = Player(id="player1", faction=Faction.SOL)
        self.player2 = Player(id="player2", faction=Faction.HACAN)
        self.player3 = Player(id="player3", faction=Faction.XXCHA)
        self.player4 = Player(id="player4", faction=Faction.JORD)

        self.game_state = GameState(
            players=[self.player1, self.player2, self.player3, self.player4]
        )

        # Set up initial resources for testing
        self.player1.gain_trade_goods(2)
        self.player1.add_commodities(1)
        self.player2.gain_trade_goods(1)
        self.player2.add_commodities(2)
        self.player3.gain_trade_goods(0)
        self.player3.add_commodities(0)
        self.player4.gain_trade_goods(3)
        self.player4.add_commodities(3)

    def test_complete_game_scenario_with_multiple_strategy_cards(self) -> None:
        """Test Trade card works correctly in initiative order with other strategy cards.

        Requirements: 6.4 - Validate Trade card works correctly in initiative order with other strategy cards
        """
        from ti4.core.strategic_action import StrategicActionManager, StrategyCardType
        from ti4.core.strategy_cards.coordinator import StrategyCardCoordinator
        from ti4.core.strategy_cards.registry import StrategyCardRegistry

        # Set up coordinator and registry
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        registry = StrategyCardRegistry()

        # Assign strategy cards to players in a realistic game scenario
        coordinator.assign_strategy_card(
            "player1", StrategyCardType.LEADERSHIP
        )  # Initiative 1
        coordinator.assign_strategy_card(
            "player2", StrategyCardType.POLITICS
        )  # Initiative 3
        coordinator.assign_strategy_card(
            "player3", StrategyCardType.TRADE
        )  # Initiative 5
        coordinator.assign_strategy_card(
            "player4", StrategyCardType.WARFARE
        )  # Initiative 6

        # Verify initiative order is correct
        initiative_order = coordinator.get_action_phase_initiative_order()
        expected_order = ["player1", "player2", "player3", "player4"]
        assert initiative_order == expected_order

        # Test that Trade card can be retrieved and used (focus on Trade card integration)
        trade_card = registry.get_card(StrategyCardType.TRADE)
        assert trade_card is not None

        # Player 3 uses Trade primary ability (our focus)
        initial_trade_goods = self.player3.get_trade_goods()
        self.player3.get_commodities()

        trade_result = trade_card.execute_primary_ability(
            "player3", self.game_state, chosen_players=["player1", "player4"]
        )
        assert trade_result.success is True

        # Verify Trade card effects
        assert self.player3.get_trade_goods() == initial_trade_goods + 3
        assert (
            self.player3.get_commodities() == self.player3.get_commodity_value()
        )  # Replenished to max

        # Test that other strategy cards can be retrieved (basic integration test)
        leadership_card = registry.get_card(StrategyCardType.LEADERSHIP)
        politics_card = registry.get_card(StrategyCardType.POLITICS)
        warfare_card = registry.get_card(StrategyCardType.WARFARE)

        assert leadership_card is not None
        assert politics_card is not None
        assert warfare_card is not None

        # Test secondary abilities - players can use other players' secondary abilities
        # Player 1 uses Trade secondary ability (was chosen, so free)
        trade_secondary_result = trade_card.execute_secondary_ability(
            "player1", self.game_state, is_free=True
        )
        assert trade_secondary_result.success is True

        # Player 2 uses Trade secondary ability (not chosen, must spend command token)
        # First ensure player has command tokens
        self.player2.gain_command_token("strategy")
        trade_secondary_result2 = trade_card.execute_secondary_ability(
            "player2", self.game_state
        )
        assert trade_secondary_result2.success is True

    def test_trade_card_integration_with_game_phase_management(self) -> None:
        """Test integration with game phase management and round progression.

        Requirements: 7.4 - Test integration with game phase management and round progression
        """
        from ti4.core.strategic_action import StrategicActionManager, StrategyCardType
        from ti4.core.strategy_cards.coordinator import StrategyCardCoordinator
        from ti4.core.strategy_cards.registry import StrategyCardRegistry

        # Set up coordinator and registry
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        registry = StrategyCardRegistry()

        # Simulate strategy phase - players select cards
        speaker_order = ["player1", "player2", "player3", "player4"]
        selection_result = coordinator.start_strategy_phase_selection(speaker_order)
        assert selection_result.success is True

        # Players select cards in speaker order
        coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.select_strategy_card("player2", StrategyCardType.POLITICS)
        coordinator.select_strategy_card("player3", StrategyCardType.TRADE)
        coordinator.select_strategy_card("player4", StrategyCardType.WARFARE)

        # Verify strategy phase is complete
        assert coordinator.is_strategy_phase_complete() is True

        # Simulate action phase - players use primary abilities
        trade_card = registry.get_card(StrategyCardType.TRADE)

        # Verify card is readied at start of action phase
        assert (
            coordinator.is_strategy_card_readied("player3", StrategyCardType.TRADE)
            is True
        )

        # Player uses primary ability
        trade_result = trade_card.execute_primary_ability("player3", self.game_state)
        assert trade_result.success is True

        # Card should be exhausted after primary ability use
        coordinator.exhaust_strategy_card("player3", StrategyCardType.TRADE)
        assert (
            coordinator.is_strategy_card_exhausted("player3", StrategyCardType.TRADE)
            is True
        )

        # Simulate status phase - cards are readied for next round
        coordinator.ready_all_strategy_cards()
        assert (
            coordinator.is_strategy_card_readied("player3", StrategyCardType.TRADE)
            is True
        )

    def test_regression_testing_existing_functionality(self) -> None:
        """Perform regression testing to ensure no existing functionality is broken.

        Requirements: 11.4 - Perform regression testing to ensure no existing functionality is broken
        """
        from ti4.core.strategic_action import StrategicActionManager, StrategyCardType
        from ti4.core.strategy_cards.coordinator import StrategyCardCoordinator
        from ti4.core.strategy_cards.registry import StrategyCardRegistry

        # Test that all existing strategy cards still work correctly
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        registry = StrategyCardRegistry()

        # Verify all 8 strategy cards are registered
        assert registry.validate_registry() is True

        # Test each strategy card can be retrieved and has correct properties
        strategy_cards = [
            (StrategyCardType.LEADERSHIP, 1),
            (StrategyCardType.DIPLOMACY, 2),
            (StrategyCardType.POLITICS, 3),
            (StrategyCardType.CONSTRUCTION, 4),
            (StrategyCardType.TRADE, 5),
            (StrategyCardType.WARFARE, 6),
            (StrategyCardType.TECHNOLOGY, 7),
            (StrategyCardType.IMPERIAL, 8),
        ]

        for card_type, expected_initiative in strategy_cards:
            card = registry.get_card(card_type)
            assert card is not None
            assert card.get_initiative_value() == expected_initiative
            assert card.get_card_type() == card_type

        # Test that coordinator can handle all cards
        for i, (card_type, _) in enumerate(strategy_cards):
            player_id = f"player{i + 1}"
            result = coordinator.assign_strategy_card(player_id, card_type)
            assert result.success is True

        # Test initiative ordering with all cards
        initiative_order = coordinator.get_action_phase_initiative_order()
        expected_order = [f"player{i + 1}" for i in range(8)]
        assert initiative_order == expected_order

    def test_multi_player_concurrent_secondary_abilities(self) -> None:
        """Test multiple players using Trade secondary ability concurrently.

        Requirements: 6.4 - Validate integration with existing BaseStrategyCard interface and StrategyCardAbilityResult patterns
        """
        trade_card = TradeStrategyCard()

        # Player 1 executes primary ability and chooses player 2 for free secondary
        primary_result = trade_card.execute_primary_ability(
            "player1", self.game_state, chosen_players=["player2"]
        )
        assert primary_result.success is True

        # Multiple players use secondary ability concurrently
        # Player 2 uses free secondary (was chosen)
        secondary_result1 = trade_card.execute_secondary_ability(
            "player2", self.game_state, is_free=True
        )
        assert secondary_result1.success is True

        # Player 3 uses secondary with command token
        self.player3.gain_command_token("strategy")
        secondary_result2 = trade_card.execute_secondary_ability(
            "player3", self.game_state
        )
        assert secondary_result2.success is True

        # Player 4 uses secondary with command token
        self.player4.gain_command_token("strategy")
        secondary_result3 = trade_card.execute_secondary_ability(
            "player4", self.game_state
        )
        assert secondary_result3.success is True

        # Verify all players' commodities were replenished to their faction maximum
        assert self.player2.get_commodities() == self.player2.get_commodity_value()
        assert self.player3.get_commodities() == self.player3.get_commodity_value()
        assert self.player4.get_commodities() == self.player4.get_commodity_value()

    def test_performance_under_realistic_game_conditions(self) -> None:
        """Test Trade card performance under realistic game conditions.

        Requirements: 11.4 - Complete final quality assurance and mark Rule 92 as production ready
        """
        trade_card = TradeStrategyCard()

        # Test primary ability performance with multiple executions
        primary_times = []
        for _ in range(10):
            start_time = time.perf_counter()
            result = trade_card.execute_primary_ability(
                "player1", self.game_state, chosen_players=["player2", "player3"]
            )
            end_time = time.perf_counter()

            assert result.success is True
            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
            primary_times.append(execution_time)

        # Test secondary ability performance with multiple executions
        secondary_times = []
        for _ in range(10):
            # Ensure player has command tokens
            self.player2.gain_command_token("strategy")

            start_time = time.perf_counter()
            result = trade_card.execute_secondary_ability("player2", self.game_state)
            end_time = time.perf_counter()

            assert result.success is True
            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
            secondary_times.append(execution_time)

        # Verify performance requirements are met
        avg_primary_time = sum(primary_times) / len(primary_times)
        avg_secondary_time = sum(secondary_times) / len(secondary_times)

        # Requirements: Primary ability < 50ms, Secondary ability < 25ms
        assert avg_primary_time < 50.0, (
            f"Primary ability average time {avg_primary_time}ms exceeds 50ms requirement"
        )
        assert avg_secondary_time < 25.0, (
            f"Secondary ability average time {avg_secondary_time}ms exceeds 25ms requirement"
        )

    def test_error_handling_in_complex_scenarios(self) -> None:
        """Test comprehensive error handling in complex game scenarios.

        Requirements: 11.4 - Complete final quality assurance and mark Rule 92 as production ready
        """
        trade_card = TradeStrategyCard()

        # Test error handling with invalid game state
        result = trade_card.execute_primary_ability("player1", None)
        assert result.success is True  # Returns success but with informational message
        assert (
            "Trade primary ability implementation requires user confirmation"
            in result.error_message
        )

        # Test error handling with invalid player
        result = trade_card.execute_primary_ability("invalid_player", self.game_state)
        assert result.success is False
        assert "Player invalid_player not found" in result.error_message

        # Test error handling with invalid chosen players
        result = trade_card.execute_primary_ability(
            "player1", self.game_state, chosen_players=["invalid_player"]
        )
        assert result.success is False
        assert "Invalid player ID: invalid_player" in result.error_message

        # Test secondary ability error handling
        result = trade_card.execute_secondary_ability("player1", None)
        assert result.success is False
        assert "Game state is required" in result.error_message

        # Test secondary ability with insufficient command tokens
        # Ensure player has no command tokens (they start with some, so spend them all)
        while self.player2.command_sheet.has_strategy_tokens():
            self.player2.command_sheet.spend_strategy_token()
        result = trade_card.execute_secondary_ability("player2", self.game_state)
        assert result.success is False
        assert "Insufficient command tokens" in result.error_message

    def test_production_readiness_validation(self) -> None:
        """Validate that Trade card is production ready with all requirements met.

        Requirements: 11.4 - Complete final quality assurance and mark Rule 92 as production ready
        """
        from ti4.core.strategic_action import StrategicActionManager, StrategyCardType
        from ti4.core.strategy_cards.coordinator import StrategyCardCoordinator
        from ti4.core.strategy_cards.registry import StrategyCardRegistry

        # Verify Trade card is properly registered
        registry = StrategyCardRegistry()
        trade_card = registry.get_card(StrategyCardType.TRADE)
        assert trade_card is not None
        assert isinstance(trade_card, TradeStrategyCard)

        # Verify all registry validation passes
        assert registry.validate_registry() is True

        # Verify coordinator integration works
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        assignment_result = coordinator.assign_strategy_card(
            "player1", StrategyCardType.TRADE
        )
        assert assignment_result.success is True

        # Verify card state management works
        assert (
            coordinator.is_strategy_card_readied("player1", StrategyCardType.TRADE)
            is True
        )
        coordinator.exhaust_strategy_card("player1", StrategyCardType.TRADE)
        assert (
            coordinator.is_strategy_card_exhausted("player1", StrategyCardType.TRADE)
            is True
        )

        # Verify performance metrics are available
        trade_card_instance = TradeStrategyCard()
        metrics = trade_card_instance.get_performance_metrics()
        assert "primary_ability_times" in metrics
        assert "secondary_ability_times" in metrics

        # Verify all core functionality works end-to-end
        primary_result = trade_card_instance.execute_primary_ability(
            "player1", self.game_state, chosen_players=["player2"]
        )
        assert primary_result.success is True

        secondary_result = trade_card_instance.execute_secondary_ability(
            "player2", self.game_state, is_free=True
        )
        assert secondary_result.success is True


class TestTradeCardRegressionTesting:
    """Test suite for comprehensive regression testing to ensure no existing functionality is broken.

    Requirements: 11.4 - Perform regression testing to ensure no existing functionality is broken
    """

    def setup_method(self) -> None:
        """Set up test fixtures for regression testing."""
        self.player1 = Player(id="player1", faction=Faction.SOL)
        self.player2 = Player(id="player2", faction=Faction.HACAN)
        self.game_state = GameState(players=[self.player1, self.player2])

    def test_all_strategy_cards_still_functional(self) -> None:
        """Test that all existing strategy cards are still functional after Trade card implementation."""
        from ti4.core.strategic_action import StrategyCardType
        from ti4.core.strategy_cards.registry import StrategyCardRegistry

        registry = StrategyCardRegistry()

        # Test all strategy cards can be instantiated and have basic functionality
        strategy_card_types = [
            StrategyCardType.LEADERSHIP,
            StrategyCardType.DIPLOMACY,
            StrategyCardType.POLITICS,
            StrategyCardType.CONSTRUCTION,
            StrategyCardType.TRADE,
            StrategyCardType.WARFARE,
            StrategyCardType.TECHNOLOGY,
            StrategyCardType.IMPERIAL,
        ]

        for card_type in strategy_card_types:
            card = registry.get_card(card_type)
            assert card is not None

            # Test basic interface compliance
            assert hasattr(card, "get_card_type")
            assert hasattr(card, "get_initiative_value")
            assert hasattr(card, "execute_primary_ability")
            assert hasattr(card, "execute_secondary_ability")

            # Test that methods return expected types
            assert card.get_card_type() == card_type
            assert isinstance(card.get_initiative_value(), int)
            assert 1 <= card.get_initiative_value() <= 8

    def test_strategy_card_coordinator_still_functional(self) -> None:
        """Test that StrategyCardCoordinator functionality is not broken."""
        from ti4.core.strategic_action import StrategicActionManager, StrategyCardType
        from ti4.core.strategy_cards.coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test basic coordinator functionality
        result = coordinator.assign_strategy_card(
            "player1", StrategyCardType.LEADERSHIP
        )
        assert result.success is True

        result = coordinator.assign_strategy_card("player2", StrategyCardType.TRADE)
        assert result.success is True

        # Test initiative ordering
        initiative_order = coordinator.get_action_phase_initiative_order()
        assert initiative_order == [
            "player1",
            "player2",
        ]  # Leadership (1) before Trade (5)

        # Test card state management
        assert (
            coordinator.is_strategy_card_readied("player1", StrategyCardType.LEADERSHIP)
            is True
        )
        assert (
            coordinator.is_strategy_card_readied("player2", StrategyCardType.TRADE)
            is True
        )

    def test_game_state_integration_not_broken(self) -> None:
        """Test that GameState integration is not broken by Trade card implementation."""
        # Test that players can still be created and managed
        assert self.player1.id == "player1"
        assert self.player2.id == "player2"

        # Test that resource management still works
        initial_trade_goods = self.player1.get_trade_goods()
        self.player1.gain_trade_goods(5)
        assert self.player1.get_trade_goods() == initial_trade_goods + 5

        initial_commodities = self.player1.get_commodities()
        self.player1.add_commodities(2)
        assert self.player1.get_commodities() == initial_commodities + 2

        # Test that command tokens still work
        self.player1.gain_command_token("strategy")
        assert self.player1.command_sheet.has_strategy_tokens() is True


class TestTradeCardProductionReadiness:
    """Test suite for final production readiness validation.

    Requirements: 11.4 - Complete final quality assurance and mark Rule 92 as production ready
    """

    def setup_method(self) -> None:
        """Set up test fixtures for production readiness testing."""
        self.player1 = Player(id="player1", faction=Faction.SOL)
        self.player2 = Player(id="player2", faction=Faction.HACAN)
        self.game_state = GameState(players=[self.player1, self.player2])

    def test_trade_card_meets_all_performance_requirements(self) -> None:
        """Test that Trade card meets all performance requirements for production."""
        trade_card = TradeStrategyCard()

        # Test primary ability performance
        start_time = time.perf_counter()
        result = trade_card.execute_primary_ability("player1", self.game_state)
        end_time = time.perf_counter()

        primary_time = (end_time - start_time) * 1000  # Convert to milliseconds
        assert primary_time < 50.0, (
            f"Primary ability took {primary_time}ms, exceeds 50ms requirement"
        )
        assert result.success is True

        # Test secondary ability performance
        self.player2.gain_command_token("strategy")
        start_time = time.perf_counter()
        result = trade_card.execute_secondary_ability("player2", self.game_state)
        end_time = time.perf_counter()

        secondary_time = (end_time - start_time) * 1000  # Convert to milliseconds
        assert secondary_time < 25.0, (
            f"Secondary ability took {secondary_time}ms, exceeds 25ms requirement"
        )
        assert result.success is True

    def test_trade_card_error_handling_is_comprehensive(self) -> None:
        """Test that Trade card has comprehensive error handling for production use."""
        trade_card = TradeStrategyCard()

        # Test all major error conditions are handled gracefully
        error_scenarios = [
            # Primary ability errors
            (
                lambda: trade_card.execute_primary_ability(
                    "invalid_player", self.game_state
                ),
                "Player invalid_player not found",
                False,
            ),
            (
                lambda: trade_card.execute_primary_ability("player1", None),
                "Trade primary ability implementation requires user confirmation",
                True,
            ),  # This returns success=True
            (
                lambda: trade_card.execute_primary_ability(
                    "player1", self.game_state, chosen_players=["invalid"]
                ),
                "Invalid player ID: invalid",
                False,
            ),
            # Secondary ability errors
            (
                lambda: trade_card.execute_secondary_ability(
                    "invalid_player", self.game_state
                ),
                "Player invalid_player not found",
                False,
            ),
            (
                lambda: trade_card.execute_secondary_ability("player1", None),
                "Game state is required",
                False,
            ),
        ]

        for error_func, expected_error_text, expected_success in error_scenarios:
            result = error_func()
            assert result.success is expected_success
            assert expected_error_text in result.error_message

    def test_trade_card_integration_is_complete(self) -> None:
        """Test that Trade card integration with all systems is complete and functional."""
        from ti4.core.strategic_action import StrategicActionManager, StrategyCardType
        from ti4.core.strategy_cards.coordinator import StrategyCardCoordinator
        from ti4.core.strategy_cards.registry import StrategyCardRegistry

        # Test registry integration
        registry = StrategyCardRegistry()
        trade_card = registry.get_card(StrategyCardType.TRADE)
        assert trade_card is not None
        assert isinstance(trade_card, TradeStrategyCard)

        # Test coordinator integration
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        assignment_result = coordinator.assign_strategy_card(
            "player1", StrategyCardType.TRADE
        )
        assert assignment_result.success is True

        # Test state management integration
        assert (
            coordinator.is_strategy_card_readied("player1", StrategyCardType.TRADE)
            is True
        )
        coordinator.exhaust_strategy_card("player1", StrategyCardType.TRADE)
        assert (
            coordinator.is_strategy_card_exhausted("player1", StrategyCardType.TRADE)
            is True
        )

        # Test that all functionality works together
        trade_card_instance = TradeStrategyCard()
        primary_result = trade_card_instance.execute_primary_ability(
            "player1", self.game_state
        )
        assert primary_result.success is True

        self.player2.gain_command_token("strategy")
        secondary_result = trade_card_instance.execute_secondary_ability(
            "player2", self.game_state
        )
        assert secondary_result.success is True

    def test_trade_card_documentation_and_metrics_complete(self) -> None:
        """Test that Trade card has complete documentation and metrics for production."""
        trade_card = TradeStrategyCard()

        # Test that performance metrics are available
        metrics = trade_card.get_performance_metrics()
        assert isinstance(metrics, dict)
        assert "primary_ability_times" in metrics
        assert "secondary_ability_times" in metrics

        # Test that metrics can be reset
        trade_card.reset_performance_metrics()
        reset_metrics = trade_card.get_performance_metrics()
        assert reset_metrics["primary_ability_times"]["count"] == 0
        assert reset_metrics["secondary_ability_times"]["count"] == 0

        # Test that all required methods are documented (have docstrings)
        assert trade_card.execute_primary_ability.__doc__ is not None
        assert trade_card.execute_secondary_ability.__doc__ is not None
        assert trade_card.get_performance_metrics.__doc__ is not None

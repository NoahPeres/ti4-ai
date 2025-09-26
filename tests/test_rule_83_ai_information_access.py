"""Tests for Rule 83: Strategy Card AI Information Access.

Tests the AI-friendly interfaces for strategy card information access,
evaluation, and strategic planning support.

Requirements: 8.1, 8.2, 8.3, 8.4, 8.5
"""

from ti4.core.strategic_action import StrategyCardType
from ti4.core.strategy_card_coordinator import StrategyCardCoordinator


class TestStrategyCardAIInformationAccess:
    """Test AI information access methods for strategy cards."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        from ti4.core.strategic_action import StrategicActionManager

        self.strategic_action_manager = StrategicActionManager()
        self.coordinator = StrategyCardCoordinator(self.strategic_action_manager)

        # Set up a basic game scenario
        self.players = ["player1", "player2", "player3"]
        self.coordinator.start_strategy_phase_selection(self.players)

    def test_get_strategy_card_information_provides_comprehensive_details(self) -> None:
        """Test that AI can get comprehensive strategy card information.

        Requirements: 8.1 - System provides card names, initiative numbers, and current owners
        Requirements: 8.4 - System provides comprehensive card information
        """
        # Assign some cards
        self.coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        self.coordinator.select_strategy_card("player2", StrategyCardType.DIPLOMACY)

        # AI should be able to get comprehensive card information
        card_info = self.coordinator.get_strategy_card_information(
            StrategyCardType.LEADERSHIP
        )

        assert card_info is not None
        assert card_info.card_type == StrategyCardType.LEADERSHIP
        assert card_info.initiative_number == 1
        assert card_info.current_owner == "player1"
        assert card_info.name == "leadership"
        assert card_info.is_exhausted is False

    def test_get_all_strategy_cards_information_for_ai_evaluation(self) -> None:
        """Test that AI can get information about all strategy cards.

        Requirements: 8.2 - AI has access to all available cards and their properties
        """
        # Assign some cards
        self.coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        self.coordinator.select_strategy_card("player2", StrategyCardType.DIPLOMACY)

        # AI should be able to get information about all cards
        all_cards_info = self.coordinator.get_all_strategy_cards_information()

        assert len(all_cards_info) == 8  # All 8 strategy cards

        # Check that assigned cards show ownership
        leadership_info = next(
            info
            for info in all_cards_info
            if info.card_type == StrategyCardType.LEADERSHIP
        )
        assert leadership_info.current_owner == "player1"

        diplomacy_info = next(
            info
            for info in all_cards_info
            if info.card_type == StrategyCardType.DIPLOMACY
        )
        assert diplomacy_info.current_owner == "player2"

        # Check that unassigned cards show no ownership
        politics_info = next(
            info
            for info in all_cards_info
            if info.card_type == StrategyCardType.POLITICS
        )
        assert politics_info.current_owner is None

    def test_get_player_strategy_card_assignments_for_strategic_planning(self) -> None:
        """Test that AI can see which cards other players have selected.

        Requirements: 8.3 - AI knows which cards other players have selected
        """
        # Assign cards to players
        self.coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        self.coordinator.select_strategy_card("player2", StrategyCardType.DIPLOMACY)
        self.coordinator.select_strategy_card("player3", StrategyCardType.POLITICS)

        # AI should be able to see all player assignments
        assignments = self.coordinator.get_player_strategy_card_assignments()

        assert len(assignments) == 3
        assert assignments["player1"] == StrategyCardType.LEADERSHIP
        assert assignments["player2"] == StrategyCardType.DIPLOMACY
        assert assignments["player3"] == StrategyCardType.POLITICS

    def test_get_available_cards_for_ai_selection_evaluation(self) -> None:
        """Test that AI can evaluate available cards for selection.

        Requirements: 8.2 - AI has access to all available cards and their properties
        """
        # Initially all cards should be available
        available_cards = self.coordinator.get_available_cards_for_ai()
        assert len(available_cards) == 8

        # After some selections, fewer should be available
        self.coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        self.coordinator.select_strategy_card("player2", StrategyCardType.DIPLOMACY)

        available_cards = self.coordinator.get_available_cards_for_ai()
        assert len(available_cards) == 6
        assert StrategyCardType.LEADERSHIP not in [
            card.card_type for card in available_cards
        ]
        assert StrategyCardType.DIPLOMACY not in [
            card.card_type for card in available_cards
        ]

    def test_analyze_game_state_for_strategic_planning(self) -> None:
        """Test that AI can analyze game state for strategic planning.

        Requirements: 8.5 - Strategy card assignments are clearly accessible for game state analysis
        """
        # Set up a game state
        self.coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        self.coordinator.select_strategy_card("player2", StrategyCardType.DIPLOMACY)
        self.coordinator.select_strategy_card("player3", StrategyCardType.POLITICS)

        # AI should be able to analyze the strategic situation
        analysis = self.coordinator.analyze_strategy_card_game_state()

        assert analysis is not None
        assert analysis.total_assigned_cards == 3
        assert analysis.total_available_cards == 5
        assert analysis.initiative_order == ["player1", "player2", "player3"]
        assert analysis.lowest_initiative_player == "player1"
        assert analysis.highest_initiative_player == "player3"

    def test_get_strategy_card_evaluation_data_for_ai_decision_making(self) -> None:
        """Test that AI can get evaluation data for decision making.

        Requirements: 8.2, 8.4 - AI has access to card properties and comprehensive information
        """
        # AI should be able to get evaluation data for each card
        evaluation_data = self.coordinator.get_strategy_card_evaluation_data(
            StrategyCardType.LEADERSHIP
        )

        assert evaluation_data is not None
        assert evaluation_data.card_type == StrategyCardType.LEADERSHIP
        assert evaluation_data.initiative_number == 1
        assert evaluation_data.is_available is True
        assert evaluation_data.strategic_value is not None  # Some strategic assessment
        assert evaluation_data.synergy_potential is not None  # Potential synergies

    def test_ai_can_query_initiative_order_implications(self) -> None:
        """Test that AI can understand initiative order implications.

        Requirements: 8.3, 8.5 - AI knows player selections and can analyze game state
        """
        # Set up cards with different initiative values
        self.coordinator.select_strategy_card("player1", StrategyCardType.IMPERIAL)  # 8
        self.coordinator.select_strategy_card(
            "player2", StrategyCardType.LEADERSHIP
        )  # 1
        self.coordinator.select_strategy_card("player3", StrategyCardType.WARFARE)  # 6

        # AI should understand initiative implications
        initiative_analysis = self.coordinator.get_initiative_order_analysis()

        assert initiative_analysis.initiative_order == ["player2", "player3", "player1"]
        assert initiative_analysis.first_player == "player2"
        assert initiative_analysis.last_player == "player1"
        assert len(initiative_analysis.turn_advantages) == 3

    def test_ai_can_evaluate_secondary_ability_opportunities(self) -> None:
        """Test that AI can evaluate secondary ability opportunities.

        Requirements: 8.2, 8.4 - AI has access to comprehensive card information
        """
        # Set up scenario where secondary abilities are relevant
        self.coordinator.select_strategy_card("player1", StrategyCardType.TECHNOLOGY)
        self.coordinator.select_strategy_card("player2", StrategyCardType.WARFARE)

        # AI should be able to evaluate secondary ability opportunities
        secondary_opportunities = self.coordinator.get_secondary_ability_opportunities(
            "player3"
        )

        assert (
            len(secondary_opportunities) == 2
        )  # Can use secondary of both assigned cards
        tech_opportunity = next(
            opp
            for opp in secondary_opportunities
            if opp.card_type == StrategyCardType.TECHNOLOGY
        )
        assert tech_opportunity.can_use is True
        assert tech_opportunity.owner == "player1"

    def test_ai_decision_making_framework_integration(self) -> None:
        """Test that AI information access integrates with decision-making framework.

        Requirements: 8.4 - Integrate with existing AI decision-making frameworks
        """
        from ti4.actions.legal_moves import LegalMoveGenerator
        from ti4.actions.strategy_card_actions import StrategyCardSelectionDecision

        # Create a mock game state with strategy card coordinator
        class MockGameState:
            def __init__(self, coordinator):
                self.strategy_card_coordinator = coordinator

        game_state = MockGameState(self.coordinator)
        legal_move_generator = LegalMoveGenerator()

        # During strategy phase, AI should get legal card selection decisions
        legal_decisions = legal_move_generator.generate_legal_decisions(
            game_state, "player1"
        )

        # Should have 8 strategy card selection decisions (all cards available)
        selection_decisions = [
            decision
            for decision in legal_decisions
            if isinstance(decision, StrategyCardSelectionDecision)
        ]
        assert len(selection_decisions) == 8

        # All strategy cards should be represented
        card_types = {decision.card_type for decision in selection_decisions}
        assert len(card_types) == 8  # All unique strategy cards

    def test_ai_can_access_comprehensive_game_state_information(self) -> None:
        """Test that AI can access all necessary information for strategic planning.

        Requirements: 8.1, 8.2, 8.3, 8.4, 8.5 - Comprehensive AI information access
        """
        # Set up a complex game state
        self.coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        self.coordinator.select_strategy_card("player2", StrategyCardType.DIPLOMACY)
        self.coordinator.select_strategy_card("player3", StrategyCardType.POLITICS)

        # Exhaust some cards
        self.coordinator.exhaust_strategy_card("player1", StrategyCardType.LEADERSHIP)

        # AI should be able to get comprehensive information
        all_info = self.coordinator.get_all_strategy_cards_information()
        assignments = self.coordinator.get_player_strategy_card_assignments()
        analysis = self.coordinator.analyze_strategy_card_game_state()
        available_cards = self.coordinator.get_available_cards_for_ai()

        # Verify comprehensive access
        assert len(all_info) == 8  # All cards
        assert len(assignments) == 3  # Three assignments
        assert analysis.total_assigned_cards == 3
        assert analysis.total_available_cards == 5
        assert len(available_cards) == 5  # Five still available

        # Verify exhaustion status is accessible
        leadership_info = next(
            info for info in all_info if info.card_type == StrategyCardType.LEADERSHIP
        )
        assert leadership_info.is_exhausted is True
        assert leadership_info.current_owner == "player1"

"""Tests for Rule 83: Initiative Order Determination System.

This module tests the initiative order determination system that provides
query methods for action and status phases and integrates with game phase management.

Requirements tested:
- 3.1: Players ordered by strategy card initiative numbers (1-8)
- 3.2: Multiple players sorted from lowest to highest initiative
- 3.3: Initiative order returns player IDs in correct sequence
- 3.4: Players without strategy cards don't appear in initiative order
- 3.5: Initiative order calculated from current card assignments
"""

from src.ti4.core.game_phase import GamePhase
from src.ti4.core.strategic_action import StrategicActionManager, StrategyCardType


class TestRule83InitiativeOrderQueryMethods:
    """Test initiative order query methods for different game phases."""

    def test_get_action_phase_initiative_order(self) -> None:
        """Test getting initiative order for action phase.

        Requirements: 3.3, 3.5 - Initiative order returns player IDs in correct sequence,
        calculated from current card assignments
        """
        # This will fail initially - RED phase
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Assign cards to players
        coordinator.assign_strategy_card("player1", StrategyCardType.IMPERIAL)  # 8
        coordinator.assign_strategy_card("player2", StrategyCardType.LEADERSHIP)  # 1
        coordinator.assign_strategy_card("player3", StrategyCardType.WARFARE)  # 6

        # Get action phase initiative order
        initiative_order = coordinator.get_action_phase_initiative_order()

        # Should be ordered by initiative: Leadership(1), Warfare(6), Imperial(8)
        assert initiative_order == ["player2", "player3", "player1"]

    def test_get_status_phase_initiative_order(self) -> None:
        """Test getting initiative order for status phase.

        Requirements: 3.3, 3.5 - Initiative order returns player IDs in correct sequence,
        calculated from current card assignments
        """
        # This will fail initially - RED phase
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Assign cards to players
        coordinator.assign_strategy_card("player1", StrategyCardType.POLITICS)  # 3
        coordinator.assign_strategy_card("player2", StrategyCardType.TRADE)  # 5
        coordinator.assign_strategy_card("player3", StrategyCardType.DIPLOMACY)  # 2

        # Get status phase initiative order
        initiative_order = coordinator.get_status_phase_initiative_order()

        # Should be ordered by initiative: Diplomacy(2), Politics(3), Trade(5)
        assert initiative_order == ["player3", "player1", "player2"]

    def test_initiative_order_excludes_players_without_cards(self) -> None:
        """Test that players without strategy cards don't appear in initiative order.

        Requirements: 3.4 - Players without strategy cards don't appear in initiative order
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Only assign cards to some players
        coordinator.assign_strategy_card("player1", StrategyCardType.LEADERSHIP)  # 1
        coordinator.assign_strategy_card("player3", StrategyCardType.WARFARE)  # 6
        # player2 has no card

        # Get initiative order
        initiative_order = coordinator.get_action_phase_initiative_order()

        # Should only include players with cards
        assert initiative_order == ["player1", "player3"]
        assert "player2" not in initiative_order

    def test_initiative_order_with_all_eight_cards(self) -> None:
        """Test initiative order with all eight strategy cards assigned.

        Requirements: 3.1, 3.2 - Players ordered by strategy card initiative numbers,
        sorted from lowest to highest
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Assign all cards in random order
        coordinator.assign_strategy_card("player8", StrategyCardType.IMPERIAL)  # 8
        coordinator.assign_strategy_card("player1", StrategyCardType.LEADERSHIP)  # 1
        coordinator.assign_strategy_card("player6", StrategyCardType.WARFARE)  # 6
        coordinator.assign_strategy_card("player3", StrategyCardType.POLITICS)  # 3
        coordinator.assign_strategy_card("player7", StrategyCardType.TECHNOLOGY)  # 7
        coordinator.assign_strategy_card("player2", StrategyCardType.DIPLOMACY)  # 2
        coordinator.assign_strategy_card("player5", StrategyCardType.TRADE)  # 5
        coordinator.assign_strategy_card("player4", StrategyCardType.CONSTRUCTION)  # 4

        # Get initiative order
        initiative_order = coordinator.get_action_phase_initiative_order()

        # Should be ordered 1-8
        expected_order = [
            "player1",
            "player2",
            "player3",
            "player4",
            "player5",
            "player6",
            "player7",
            "player8",
        ]
        assert initiative_order == expected_order


class TestRule83GamePhaseIntegration:
    """Test integration with existing game phase management system."""

    def test_coordinator_integrates_with_game_phase_system(self) -> None:
        """Test that coordinator can integrate with game phase management.

        Requirements: Integration with existing game phase management system
        """
        # This will fail initially - RED phase
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test that coordinator can work with game phases
        coordinator.set_current_game_phase(GamePhase.ACTION)
        assert coordinator.get_current_game_phase() == GamePhase.ACTION

        coordinator.set_current_game_phase(GamePhase.STATUS)
        assert coordinator.get_current_game_phase() == GamePhase.STATUS

    def test_initiative_order_adapts_to_game_phase(self) -> None:
        """Test that initiative order methods work correctly in different game phases.

        Requirements: Integration with existing game phase management system
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Assign cards
        coordinator.assign_strategy_card("player1", StrategyCardType.LEADERSHIP)  # 1
        coordinator.assign_strategy_card("player2", StrategyCardType.WARFARE)  # 6

        # Test in action phase
        coordinator.set_current_game_phase(GamePhase.ACTION)
        action_order = coordinator.get_action_phase_initiative_order()
        assert action_order == ["player1", "player2"]

        # Test in status phase
        coordinator.set_current_game_phase(GamePhase.STATUS)
        status_order = coordinator.get_status_phase_initiative_order()
        assert status_order == ["player1", "player2"]

    def test_initiative_order_validation_for_invalid_phase(self) -> None:
        """Test that initiative order methods validate game phase appropriately.

        Requirements: 9.1, 9.2 - Comprehensive error handling and validation
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Assign cards
        coordinator.assign_strategy_card("player1", StrategyCardType.LEADERSHIP)

        # Test that methods work regardless of phase (they should always return current order)
        coordinator.set_current_game_phase(GamePhase.SETUP)
        setup_order = coordinator.get_action_phase_initiative_order()
        assert setup_order == ["player1"]

        coordinator.set_current_game_phase(GamePhase.STRATEGY)
        strategy_order = coordinator.get_status_phase_initiative_order()
        assert strategy_order == ["player1"]

"""Tests for Rule 83: STRATEGY CARD coordinator system.

This module tests the strategy card coordinator that integrates with existing systems.
All tests follow strict TDD methodology with RED-GREEN-REFACTOR cycles.

Rule 83 requirements tested:
- 1.1, 1.2, 1.3: Strategy card system foundation
- 6.1, 6.2: Integration with strategic action system
"""

import pytest


class TestRule83StrategyCardCoordinatorBasics:
    """Test basic strategy card coordinator functionality."""

    def test_strategy_card_coordinator_exists(self) -> None:
        """Test that strategy card coordinator can be imported and instantiated.

        This is the first RED test - it will fail until we create the coordinator.

        Requirements: 1.1 - System initialization with all eight strategy cards
        """
        # This will fail initially - RED phase
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator
        from src.ti4.core.strategic_action import StrategicActionManager

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        assert coordinator is not None

    def test_coordinator_can_assign_strategy_card(self) -> None:
        """Test that coordinator can assign strategy cards to players.

        Requirements: 1.2 - Card assignment and tracking functionality
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator
        from src.ti4.core.strategic_action import StrategicActionManager, StrategyCardType

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        
        # This will fail initially - RED phase
        result = coordinator.assign_strategy_card("player1", StrategyCardType.WARFARE)
        assert result.success

    def test_coordinator_validates_empty_player_id(self) -> None:
        """Test that coordinator validates empty player ID.

        Requirements: 1.2 - Input validation for card assignment
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator
        from src.ti4.core.strategic_action import StrategicActionManager, StrategyCardType

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        
        result = coordinator.assign_strategy_card("", StrategyCardType.WARFARE)
        assert not result.success
        assert "Player ID cannot be empty" in result.error_message

    def test_coordinator_validates_none_card(self) -> None:
        """Test that coordinator validates None strategy card.

        Requirements: 1.2 - Input validation for card assignment
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator
        from src.ti4.core.strategic_action import StrategicActionManager

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        
        result = coordinator.assign_strategy_card("player1", None)
        assert not result.success
        assert "Strategy card cannot be None" in result.error_message


class TestRule83InitiativeOrderCalculation:
    """Test initiative order calculation functionality."""

    def test_calculate_initiative_order_with_single_player(self) -> None:
        """Test initiative order calculation with single player.

        Requirements: 1.3 - Initiative order calculation as pure function
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator
        from src.ti4.core.strategic_action import StrategicActionManager, StrategyCardType

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        
        # This will fail initially - RED phase
        player_assignments = {"player1": StrategyCardType.WARFARE}
        initiative_order = coordinator.calculate_initiative_order(player_assignments)
        assert initiative_order == ["player1"]

    def test_calculate_initiative_order_with_multiple_players(self) -> None:
        """Test initiative order calculation with multiple players in correct order.

        Requirements: 1.3 - Initiative order calculation as pure function
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator
        from src.ti4.core.strategic_action import StrategicActionManager, StrategyCardType

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        
        # Test with cards in reverse initiative order
        player_assignments = {
            "player1": StrategyCardType.IMPERIAL,    # 8
            "player2": StrategyCardType.LEADERSHIP,  # 1
            "player3": StrategyCardType.WARFARE      # 6
        }
        initiative_order = coordinator.calculate_initiative_order(player_assignments)
        # Should be ordered by initiative: Leadership(1), Warfare(6), Imperial(8)
        assert initiative_order == ["player2", "player3", "player1"]

    def test_calculate_initiative_order_with_empty_assignments(self) -> None:
        """Test initiative order calculation with empty assignments.

        Requirements: 1.3 - Initiative order calculation as pure function
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator
        from src.ti4.core.strategic_action import StrategicActionManager

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        
        initiative_order = coordinator.calculate_initiative_order({})
        assert initiative_order == []


class TestRule83StrategicActionIntegration:
    """Test integration with existing strategic action system."""

    def test_coordinator_integrates_with_strategic_action_manager(self) -> None:
        """Test that coordinator can integrate with strategic action manager.

        Requirements: 6.1, 6.2 - Integration with strategic action system
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator
        from src.ti4.core.strategic_action import StrategicActionManager, StrategyCardType

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        
        # This will fail initially - RED phase
        coordinator.integrate_with_strategic_actions()
        
        # Verify integration was successful
        assert hasattr(strategic_action_manager, '_strategy_card_coordinator')
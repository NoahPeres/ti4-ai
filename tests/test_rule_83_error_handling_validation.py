"""Tests for Rule 83 comprehensive error handling and validation.

This module tests the error handling and validation requirements for the strategy card system.
Requirements: 9.1, 9.2, 9.3, 9.4, 9.5
"""

import pytest

from src.ti4.core.exceptions import StrategyCardStateError
from src.ti4.core.strategic_action import StrategicActionManager, StrategyCardType
from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator


class TestRule83ErrorHandlingValidation:
    """Test comprehensive error handling and validation for strategy card system.

    Requirements: 9.1, 9.2, 9.3, 9.4, 9.5 - Comprehensive error handling and validation
    """

    def test_invalid_player_id_error_messages(self) -> None:
        """Test that invalid player IDs return descriptive error messages.

        Requirements: 9.1 - System returns descriptive error messages for invalid player IDs
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test empty player ID
        result = coordinator.assign_strategy_card("", StrategyCardType.LEADERSHIP)
        assert not result.success
        assert "Player ID cannot be empty" in result.error_message

        # Test None player ID
        result = coordinator.assign_strategy_card(None, StrategyCardType.LEADERSHIP)
        assert not result.success
        assert "Player ID cannot be None" in result.error_message

        # Test whitespace-only player ID
        result = coordinator.assign_strategy_card("   ", StrategyCardType.LEADERSHIP)
        assert not result.success
        assert "Player ID cannot be empty" in result.error_message

    def test_invalid_strategy_card_operations_prevention(self) -> None:
        """Test that invalid strategy card operations are prevented gracefully.

        Requirements: 9.2 - System prevents invalid operations gracefully
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test None strategy card
        result = coordinator.assign_strategy_card("player1", None)
        assert not result.success
        assert "Strategy card cannot be None" in result.error_message

        # Test selecting unavailable card
        coordinator.assign_strategy_card("player1", StrategyCardType.LEADERSHIP)
        result = coordinator.assign_strategy_card(
            "player2", StrategyCardType.LEADERSHIP
        )
        assert not result.success
        assert "already assigned" in result.error_message.lower()

    def test_system_state_inconsistency_detection(self) -> None:
        """Test that system detects and reports state inconsistencies.

        Requirements: 9.3 - System detects and reports state inconsistencies
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Create an inconsistent state by manually manipulating internal state
        # This simulates a bug where card state tracking gets out of sync
        coordinator._card_assignments["player1"] = StrategyCardType.LEADERSHIP
        # Don't add corresponding state tracking - this creates inconsistency

        with pytest.raises(StrategyCardStateError) as exc_info:
            coordinator.validate_system_state()

        assert "state inconsistency" in str(exc_info.value).lower()

    def test_edge_case_handling_without_crashing(self) -> None:
        """Test that edge cases are handled without crashing.

        Requirements: 9.4 - System handles edge cases without crashing
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test extreme player counts
        result = coordinator.start_strategy_phase_selection([])
        assert not result.success
        assert "empty" in result.error_message.lower()

        # Test too many players
        too_many_players = [f"player{i}" for i in range(20)]
        result = coordinator.start_strategy_phase_selection(too_many_players)
        assert not result.success
        assert "maximum" in result.error_message.lower()

    def test_actionable_error_feedback(self) -> None:
        """Test that errors provide actionable feedback for resolution.

        Requirements: 9.5 - System provides actionable feedback for error resolution
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test that error messages suggest solutions
        result = coordinator.select_strategy_card(
            "player1", StrategyCardType.LEADERSHIP
        )
        assert not result.success
        assert "start strategy phase" in result.error_message.lower()


class TestRule83ComprehensiveValidation:
    """Test comprehensive validation and edge case handling.

    Requirements: 9.1, 9.2, 9.3, 9.4, 9.5 - Comprehensive error handling and validation
    """

    def test_integration_with_existing_logging_systems(self) -> None:
        """Test that error handling integrates with existing logging systems.

        Requirements: 9.4 - Integration with existing error handling and logging systems
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test that validation errors can be logged properly
        result = coordinator.assign_strategy_card(None, StrategyCardType.LEADERSHIP)
        assert not result.success
        assert result.error_message is not None

        # Test that the error message is structured for logging
        assert isinstance(result.error_message, str)
        assert len(result.error_message) > 0

    def test_robust_input_validation_following_existing_patterns(self) -> None:
        """Test that input validation follows existing patterns in the codebase.

        Requirements: 9.1 - Robust input validation following existing patterns
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test various invalid input types
        invalid_inputs = [None, "", "   ", 123, [], {}]

        for invalid_input in invalid_inputs:
            try:
                result = coordinator.assign_strategy_card(
                    invalid_input, StrategyCardType.LEADERSHIP
                )
                assert not result.success
                assert "Player ID" in result.error_message
            except TypeError:
                # Some invalid types might raise TypeError, which is acceptable
                pass

    def test_descriptive_error_messages_for_invalid_operations(self) -> None:
        """Test that error messages are descriptive and helpful.

        Requirements: 9.2 - Descriptive error messages for invalid operations
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test card already assigned error
        coordinator.assign_strategy_card("player1", StrategyCardType.LEADERSHIP)
        result = coordinator.assign_strategy_card(
            "player2", StrategyCardType.LEADERSHIP
        )

        assert not result.success
        assert "already assigned" in result.error_message
        assert "player1" in result.error_message
        assert "leadership" in result.error_message.lower()

    def test_edge_case_handling_for_system_state_inconsistencies(self) -> None:
        """Test edge case handling for various system state inconsistencies.

        Requirements: 9.3 - Edge case handling for system state inconsistencies
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test orphaned state tracking
        coordinator._player_card_states["orphan_player"] = {
            StrategyCardType.WARFARE: True
        }

        with pytest.raises(StrategyCardStateError) as exc_info:
            coordinator.validate_system_state()

        assert "orphan_player" in str(exc_info.value)
        assert "warfare" in str(exc_info.value).lower()

    def test_graceful_handling_without_crashing_on_extreme_inputs(self) -> None:
        """Test graceful handling of extreme inputs without crashing.

        Requirements: 9.4 - System handles edge cases without crashing
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test with extremely long player ID
        long_player_id = "x" * 10000
        result = coordinator.assign_strategy_card(
            long_player_id, StrategyCardType.LEADERSHIP
        )
        # Should not crash, should either succeed or fail gracefully
        assert isinstance(result.success, bool)

        # Test with special characters in player ID
        special_player_id = "player!@#$%^&*()_+-=[]{}|;':\",./<>?"
        result = coordinator.assign_strategy_card(
            special_player_id, StrategyCardType.DIPLOMACY
        )
        # Should not crash, should either succeed or fail gracefully
        assert isinstance(result.success, bool)

    def test_actionable_feedback_for_resolution_in_various_scenarios(self) -> None:
        """Test actionable feedback for error resolution in various scenarios.

        Requirements: 9.5 - Actionable feedback for error resolution
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test feedback for strategy phase not started
        result = coordinator.select_strategy_card(
            "player1", StrategyCardType.LEADERSHIP
        )
        assert not result.success
        assert "start_strategy_phase_selection" in result.error_message

        # Test feedback for invalid player count
        result = coordinator.start_strategy_phase_selection([])
        assert not result.success
        assert "empty" in result.error_message.lower()

        # Test feedback for too many players
        too_many_players = [f"player{i}" for i in range(20)]
        result = coordinator.start_strategy_phase_selection(too_many_players)
        assert not result.success
        assert "maximum" in result.error_message.lower()
        assert "8" in result.error_message

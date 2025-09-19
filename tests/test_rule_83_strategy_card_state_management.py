"""Tests for Rule 83: Strategy Card State Management.

This module tests the strategy card state management system that tracks
readied/exhausted states, handles state transitions during strategic actions,
and provides status phase card readying functionality.

Requirements tested:
- 4.1: Strategy cards start in readied state when first assigned
- 4.2: Strategic actions cause strategy cards to become exhausted
- 4.3: Exhausted cards cannot use primary abilities again this round
- 4.4: Status phase readies all strategy cards for next round
- 4.5: System accurately reports readied/exhausted status
"""

from src.ti4.core.strategic_action import StrategicActionManager, StrategyCardType


class TestRule83StrategyCardStateTracking:
    """Test strategy card readied/exhausted state tracking."""

    def test_strategy_card_starts_readied_when_assigned(self) -> None:
        """Test that strategy cards start in readied state when first assigned.

        Requirements: 4.1 - Strategy cards start in readied state when first assigned
        """
        # This will fail initially - RED phase
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Assign a strategy card to a player
        result = coordinator.assign_strategy_card("player1", StrategyCardType.LEADERSHIP)
        assert result.success

        # Card should start in readied state
        assert coordinator.is_strategy_card_readied("player1", StrategyCardType.LEADERSHIP)
        assert not coordinator.is_strategy_card_exhausted("player1", StrategyCardType.LEADERSHIP)

    def test_strategic_action_exhausts_strategy_card(self) -> None:
        """Test that strategic actions cause strategy cards to become exhausted.

        Requirements: 4.2 - Strategic actions cause strategy cards to become exhausted
        """
        # This will fail initially - RED phase
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Assign and integrate
        coordinator.assign_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.integrate_with_strategic_actions()

        # Card should start readied
        assert coordinator.is_strategy_card_readied("player1", StrategyCardType.LEADERSHIP)

        # Perform strategic action
        coordinator.exhaust_strategy_card("player1", StrategyCardType.LEADERSHIP)

        # Card should now be exhausted
        assert coordinator.is_strategy_card_exhausted("player1", StrategyCardType.LEADERSHIP)
        assert not coordinator.is_strategy_card_readied("player1", StrategyCardType.LEADERSHIP)

    def test_exhausted_card_cannot_use_primary_ability(self) -> None:
        """Test that exhausted cards cannot use primary abilities again this round.

        Requirements: 4.3 - Exhausted cards cannot use primary abilities again this round
        """
        # This will fail initially - RED phase
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Assign and integrate
        coordinator.assign_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.integrate_with_strategic_actions()

        # Exhaust the card
        coordinator.exhaust_strategy_card("player1", StrategyCardType.LEADERSHIP)

        # Should not be able to use primary ability
        assert not coordinator.can_use_primary_ability("player1", StrategyCardType.LEADERSHIP)

    def test_readied_card_can_use_primary_ability(self) -> None:
        """Test that readied cards can use primary abilities.

        Requirements: 4.1, 4.3 - Readied cards can use primary abilities
        """
        # This will fail initially - RED phase
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Assign card
        coordinator.assign_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.integrate_with_strategic_actions()

        # Should be able to use primary ability when readied
        assert coordinator.can_use_primary_ability("player1", StrategyCardType.LEADERSHIP)

    def test_status_phase_readies_all_strategy_cards(self) -> None:
        """Test that status phase readies all strategy cards for next round.

        Requirements: 4.4 - Status phase readies all strategy cards for next round
        """
        # This will fail initially - RED phase
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Assign multiple cards to different players
        coordinator.assign_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.assign_strategy_card("player2", StrategyCardType.WARFARE)
        coordinator.assign_strategy_card("player3", StrategyCardType.TECHNOLOGY)
        coordinator.integrate_with_strategic_actions()

        # Exhaust all cards
        coordinator.exhaust_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.exhaust_strategy_card("player2", StrategyCardType.WARFARE)
        coordinator.exhaust_strategy_card("player3", StrategyCardType.TECHNOLOGY)

        # Verify all cards are exhausted
        assert coordinator.is_strategy_card_exhausted("player1", StrategyCardType.LEADERSHIP)
        assert coordinator.is_strategy_card_exhausted("player2", StrategyCardType.WARFARE)
        assert coordinator.is_strategy_card_exhausted("player3", StrategyCardType.TECHNOLOGY)

        # Ready all cards for status phase
        coordinator.ready_all_strategy_cards()

        # All cards should now be readied
        assert coordinator.is_strategy_card_readied("player1", StrategyCardType.LEADERSHIP)
        assert coordinator.is_strategy_card_readied("player2", StrategyCardType.WARFARE)
        assert coordinator.is_strategy_card_readied("player3", StrategyCardType.TECHNOLOGY)

    def test_accurate_state_reporting(self) -> None:
        """Test that system accurately reports readied/exhausted status.

        Requirements: 4.5 - System accurately reports readied/exhausted status
        """
        # This will fail initially - RED phase
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Assign cards
        coordinator.assign_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.assign_strategy_card("player2", StrategyCardType.WARFARE)
        coordinator.integrate_with_strategic_actions()

        # Initially both should be readied
        assert coordinator.is_strategy_card_readied("player1", StrategyCardType.LEADERSHIP)
        assert coordinator.is_strategy_card_readied("player2", StrategyCardType.WARFARE)
        assert not coordinator.is_strategy_card_exhausted("player1", StrategyCardType.LEADERSHIP)
        assert not coordinator.is_strategy_card_exhausted("player2", StrategyCardType.WARFARE)

        # Exhaust one card
        coordinator.exhaust_strategy_card("player1", StrategyCardType.LEADERSHIP)

        # Check mixed states
        assert coordinator.is_strategy_card_exhausted("player1", StrategyCardType.LEADERSHIP)
        assert not coordinator.is_strategy_card_readied("player1", StrategyCardType.LEADERSHIP)
        assert coordinator.is_strategy_card_readied("player2", StrategyCardType.WARFARE)
        assert not coordinator.is_strategy_card_exhausted("player2", StrategyCardType.WARFARE)


class TestRule83StrategicActionManagerIntegration:
    """Test integration with existing StrategicActionManager."""

    def test_coordinator_integrates_with_strategic_action_manager(self) -> None:
        """Test that coordinator integrates with existing StrategicActionManager.

        Requirements: 4.2, 6.1 - Integration with existing StrategicActionManager
        """
        # This will fail initially - RED phase
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Integration should work
        coordinator.integrate_with_strategic_actions()

        # Strategic action manager should have reference to coordinator
        assert strategic_action_manager._strategy_card_coordinator is coordinator

    def test_strategic_action_manager_uses_coordinator_for_state(self) -> None:
        """Test that StrategicActionManager uses coordinator for card state.

        Requirements: 4.2, 6.2 - Strategic action manager uses coordinator for validation
        """
        # This will fail initially - RED phase
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Assign card and integrate
        coordinator.assign_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.integrate_with_strategic_actions()

        # Strategic action manager should be able to check card state through coordinator
        assert strategic_action_manager.can_activate_strategy_card_via_coordinator(
            "player1", StrategyCardType.LEADERSHIP
        )

        # Exhaust card through coordinator
        coordinator.exhaust_strategy_card("player1", StrategyCardType.LEADERSHIP)

        # Strategic action manager should see exhausted state
        assert not strategic_action_manager.can_activate_strategy_card_via_coordinator(
            "player1", StrategyCardType.LEADERSHIP
        )


class TestRule83StateManagementEdgeCases:
    """Test edge cases and error handling for state management."""

    def test_state_queries_for_unassigned_cards(self) -> None:
        """Test state queries for cards not assigned to players.

        Requirements: 4.5, 9.1 - Accurate state reporting and error handling
        """
        # This will fail initially - RED phase
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Query state for unassigned card
        assert not coordinator.is_strategy_card_readied("player1", StrategyCardType.LEADERSHIP)
        assert not coordinator.is_strategy_card_exhausted("player1", StrategyCardType.LEADERSHIP)

    def test_exhaust_unassigned_card_fails_gracefully(self) -> None:
        """Test that exhausting unassigned cards fails gracefully.

        Requirements: 9.1, 9.2 - Error handling and validation
        """
        # This will fail initially - RED phase
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Should not crash when trying to exhaust unassigned card
        coordinator.exhaust_strategy_card("player1", StrategyCardType.LEADERSHIP)

        # State should remain consistent
        assert not coordinator.is_strategy_card_readied("player1", StrategyCardType.LEADERSHIP)
        assert not coordinator.is_strategy_card_exhausted("player1", StrategyCardType.LEADERSHIP)

    def test_ready_unassigned_card_fails_gracefully(self) -> None:
        """Test that readying unassigned cards fails gracefully.

        Requirements: 9.1, 9.2 - Error handling and validation
        """
        # This will fail initially - RED phase
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Should not crash when trying to ready unassigned card
        coordinator.ready_strategy_card("player1", StrategyCardType.LEADERSHIP)

        # State should remain consistent
        assert not coordinator.is_strategy_card_readied("player1", StrategyCardType.LEADERSHIP)
        assert not coordinator.is_strategy_card_exhausted("player1", StrategyCardType.LEADERSHIP)


class TestRule83StateManagementInputValidation:
    """Test input validation and error handling for state management."""

    def test_state_queries_with_none_card(self) -> None:
        """Test state queries with None card parameter.

        Requirements: 9.1, 9.2 - Error handling and validation
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Should handle None card gracefully
        assert not coordinator.is_strategy_card_readied("player1", None)
        assert not coordinator.is_strategy_card_exhausted("player1", None)
        assert not coordinator.can_use_primary_ability("player1", None)

    def test_state_queries_with_empty_player_id(self) -> None:
        """Test state queries with empty player ID.

        Requirements: 9.1, 9.2 - Error handling and validation
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Should handle empty player ID gracefully
        assert not coordinator.is_strategy_card_readied("", StrategyCardType.LEADERSHIP)
        assert not coordinator.is_strategy_card_exhausted("", StrategyCardType.LEADERSHIP)
        assert not coordinator.can_use_primary_ability("", StrategyCardType.LEADERSHIP)

    def test_strategic_action_manager_integration_with_invalid_inputs(self) -> None:
        """Test StrategicActionManager integration with invalid inputs.

        Requirements: 4.2, 6.2, 9.1 - Integration and error handling
        """
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()

        # Test with None inputs
        assert not strategic_action_manager.can_activate_strategy_card_via_coordinator(None, StrategyCardType.LEADERSHIP)
        assert not strategic_action_manager.can_activate_strategy_card_via_coordinator("player1", None)

        # Test with empty player ID
        assert not strategic_action_manager.can_activate_strategy_card_via_coordinator("", StrategyCardType.LEADERSHIP)

        # Test with invalid card string
        assert not strategic_action_manager.can_activate_strategy_card_via_coordinator("player1", "invalid_card")

"""Tests for Rule 83: STRATEGY CARD integration with strategic action system.

This module tests the integration between the strategy card coordinator and
the strategic action manager according to TI4 LRR Rule 83.
All tests follow strict TDD methodology with RED-GREEN-REFACTOR cycles.

Requirements tested:
- 6.1: Integration with existing StrategicActionManager
- 6.2: Strategy card validation in strategic action workflow
- 6.3: Card exhaustion during strategic action resolution
- 6.4: Backward compatibility with existing Rule 82 and Rule 91 implementations
- 6.5: Strategic actions work with strategy card coordinator
"""


class TestRule83StrategicActionIntegration:
    """Test integration between strategy card coordinator and strategic action manager."""

    def test_strategic_action_manager_accepts_coordinator(self) -> None:
        """Test that strategic action manager can be configured with a strategy card coordinator.

        This test verifies the basic integration point between the two systems.

        Requirements: 6.1 - Integration with existing StrategicActionManager
        """
        from ti4.core.strategic_action import StrategicActionManager
        from ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        # Create strategic action manager
        strategic_action_manager = StrategicActionManager()

        # Create strategy card coordinator
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Set up integration
        coordinator.integrate_with_strategic_actions()

        # Verify integration was successful
        assert strategic_action_manager._strategy_card_coordinator is coordinator

    def test_strategic_action_validates_via_coordinator(self) -> None:
        """Test that strategic actions validate strategy card ownership via coordinator.

        This test verifies that the strategic action system uses the coordinator
        to validate that players can only activate their own strategy cards.

        Requirements: 6.2 - Strategy card validation in strategic action workflow
        """
        from ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCardType,
        )
        from ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        # Create and integrate systems
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()

        # Assign strategy card via coordinator
        coordinator.assign_strategy_card("player1", StrategyCardType.WARFARE)

        # Set action phase
        strategic_action_manager.set_action_phase(True)

        # Test validation via coordinator
        assert strategic_action_manager.can_activate_strategy_card_via_coordinator(
            "player1", StrategyCardType.WARFARE
        )

        # Player without the card should not be able to activate it
        assert not strategic_action_manager.can_activate_strategy_card_via_coordinator(
            "player2", StrategyCardType.WARFARE
        )

    def test_strategic_action_exhausts_card_via_coordinator(self) -> None:
        """Test that strategic actions exhaust strategy cards via coordinator.

        This test verifies that when a strategic action is performed, the
        coordinator is notified to exhaust the strategy card.

        Requirements: 6.3 - Card exhaustion during strategic action resolution
        """
        from ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCardType,
        )
        from ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        # Create and integrate systems
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()

        # Assign strategy card via coordinator
        coordinator.assign_strategy_card("player1", StrategyCardType.WARFARE)

        # Set action phase
        strategic_action_manager.set_action_phase(True)

        # Verify card is initially readied
        assert coordinator.is_strategy_card_readied("player1", StrategyCardType.WARFARE)

        # Activate strategy card via coordinator integration
        result = strategic_action_manager.activate_strategy_card_via_coordinator(
            "player1", StrategyCardType.WARFARE
        )

        # Verify activation was successful
        assert result.success

        # Verify card was exhausted via coordinator
        assert coordinator.is_strategy_card_exhausted(
            "player1", StrategyCardType.WARFARE
        )

    def test_backward_compatibility_with_existing_strategic_actions(self) -> None:
        """Test that existing strategic action functionality still works.

        This test verifies that the integration doesn't break existing
        strategic action behavior when no coordinator is present.

        Requirements: 6.4 - Backward compatibility with existing Rule 82 implementations
        """
        from ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCard,
            StrategyCardType,
        )

        # Create strategic action manager without coordinator
        strategic_action_manager = StrategicActionManager()

        # Use existing strategic action functionality
        warfare_card = StrategyCard(
            StrategyCardType.WARFARE,
            primary_ability="Move units",
            secondary_ability="Build units",
        )
        strategic_action_manager.assign_strategy_card("player1", warfare_card)
        strategic_action_manager.set_action_phase(True)

        # Verify existing functionality still works
        assert strategic_action_manager.can_activate_strategy_card(
            "player1", StrategyCardType.WARFARE
        )

        result = strategic_action_manager.activate_strategy_card(
            "player1", StrategyCardType.WARFARE
        )
        assert result.success
        assert result.primary_ability_resolved

    def test_coordinator_integration_with_secondary_abilities(self) -> None:
        """Test that secondary ability resolution works with coordinator integration.

        This test verifies that secondary abilities are still offered to other
        players when using the coordinator integration.

        Requirements: 6.5 - Strategic actions work with strategy card coordinator
        """
        from ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCardType,
        )
        from ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        # Create and integrate systems
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()

        # Set up player order
        strategic_action_manager.set_player_order(["player1", "player2", "player3"])

        # Assign strategy card via coordinator
        coordinator.assign_strategy_card("player1", StrategyCardType.WARFARE)

        # Set action phase
        strategic_action_manager.set_action_phase(True)

        # Activate strategy card via coordinator
        result = strategic_action_manager.activate_strategy_card_via_coordinator(
            "player1", StrategyCardType.WARFARE
        )

        # Verify secondary abilities are offered
        assert result.success
        assert result.secondary_abilities_offered
        expected_order = ["player2", "player3"]
        assert result.secondary_ability_order == expected_order


class TestRule83CoordinatorValidation:
    """Test validation methods in coordinator integration."""

    def test_coordinator_validation_with_invalid_inputs(self) -> None:
        """Test that coordinator validation handles invalid inputs gracefully.

        Requirements: 6.2 - Strategy card validation in strategic action workflow
        """
        from ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCardType,
        )
        from ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        # Create and integrate systems
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()

        # Test with empty player ID
        assert not strategic_action_manager.can_activate_strategy_card_via_coordinator(
            "", StrategyCardType.WARFARE
        )

        # Test with None card
        assert not strategic_action_manager.can_activate_strategy_card_via_coordinator(
            "player1", None
        )

    def test_coordinator_validation_without_coordinator(self) -> None:
        """Test that validation fails gracefully when no coordinator is set.

        Requirements: 6.4 - Backward compatibility with existing implementations
        """
        from ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCardType,
        )

        # Create strategic action manager without coordinator
        strategic_action_manager = StrategicActionManager()

        # Validation should fail gracefully when no coordinator is present
        assert not strategic_action_manager.can_activate_strategy_card_via_coordinator(
            "player1", StrategyCardType.WARFARE
        )

    def test_card_type_conversion_helper(self) -> None:
        """Test the internal card type conversion helper method.

        This test ensures the refactored helper method works correctly.
        """
        from ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCardType,
        )

        strategic_action_manager = StrategicActionManager()

        # Test conversion from enum (should return same enum)
        result = strategic_action_manager._convert_to_strategy_card_type(
            StrategyCardType.WARFARE
        )
        assert result == StrategyCardType.WARFARE

        # Test conversion from string (should return enum)
        result = strategic_action_manager._convert_to_strategy_card_type("warfare")
        assert result == StrategyCardType.WARFARE

        # Test conversion from None (should return None)
        result = strategic_action_manager._convert_to_strategy_card_type(None)
        assert result is None

        # Test conversion from invalid string (should return None)
        result = strategic_action_manager._convert_to_strategy_card_type("invalid_card")
        assert result is None

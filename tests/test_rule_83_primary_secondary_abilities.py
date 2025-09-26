"""Tests for Rule 83: STRATEGY CARD primary and secondary ability framework.

This module tests the primary and secondary ability restrictions and validation
according to TI4 LRR Rule 83. All tests follow strict TDD methodology with RED-GREEN-REFACTOR cycles.

Requirements tested:
- 5.1: Players can use primary ability of their own strategy card
- 5.2: Other players can only access secondary abilities
- 5.3: System rejects attempts to use primary ability of another player's card
- 5.4: Secondary abilities are available to all other players during strategic action
- 5.5: System tracks which players have participated in ability resolution
"""

from ti4.core.strategic_action import StrategicActionManager, StrategyCardType
from ti4.core.strategy_card_coordinator import StrategyCardCoordinator


class TestRule83PrimaryAbilityFramework:
    """Test primary ability access control and restrictions."""

    def test_player_can_use_primary_ability_of_own_card(self) -> None:
        """Test that a player can use the primary ability of their own strategy card.

        Requirements: 5.1 - Players can use primary ability of their own strategy card
        """
        # Create and integrate systems
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()

        # Assign strategy card to player
        coordinator.assign_strategy_card("player1", StrategyCardType.WARFARE)

        # Test primary ability access
        assert coordinator.can_use_primary_ability("player1", StrategyCardType.WARFARE)

    def test_player_cannot_use_primary_ability_of_other_players_card(self) -> None:
        """Test that a player cannot use the primary ability of another player's card.

        Requirements: 5.3 - System rejects attempts to use primary ability of another player's card
        """
        # Create and integrate systems
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()

        # Assign strategy card to player1
        coordinator.assign_strategy_card("player1", StrategyCardType.WARFARE)

        # Test that player2 cannot use player1's primary ability
        assert not coordinator.can_use_primary_ability(
            "player2", StrategyCardType.WARFARE
        )

    def test_exhausted_card_cannot_use_primary_ability(self) -> None:
        """Test that exhausted cards cannot use primary ability again this round.

        Requirements: 5.1 - Primary ability restrictions based on card state
        """
        # Create and integrate systems
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()

        # Assign and exhaust strategy card
        coordinator.assign_strategy_card("player1", StrategyCardType.WARFARE)
        coordinator.exhaust_strategy_card("player1", StrategyCardType.WARFARE)

        # Test that exhausted card cannot use primary ability
        assert not coordinator.can_use_primary_ability(
            "player1", StrategyCardType.WARFARE
        )


class TestRule83SecondaryAbilityFramework:
    """Test secondary ability access control and participant tracking."""

    def test_other_players_can_access_secondary_abilities(self) -> None:
        """Test that other players can access secondary abilities during strategic action.

        Requirements: 5.2, 5.4 - Other players can only access secondary abilities,
        secondary abilities available to all other players
        """
        # Create and integrate systems
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()

        # Assign strategy card to player1
        coordinator.assign_strategy_card("player1", StrategyCardType.WARFARE)

        # Test that other players can access secondary ability
        assert coordinator.can_use_secondary_ability(
            "player2", StrategyCardType.WARFARE
        )
        assert coordinator.can_use_secondary_ability(
            "player3", StrategyCardType.WARFARE
        )

    def test_card_owner_cannot_use_secondary_ability_of_own_card(self) -> None:
        """Test that card owner cannot use secondary ability of their own card.

        Requirements: 5.2 - Other players (not owner) can only access secondary abilities
        """
        # Create and integrate systems
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()

        # Assign strategy card to player1
        coordinator.assign_strategy_card("player1", StrategyCardType.WARFARE)

        # Test that card owner cannot use secondary ability of their own card
        assert not coordinator.can_use_secondary_ability(
            "player1", StrategyCardType.WARFARE
        )

    def test_secondary_ability_participation_tracking(self) -> None:
        """Test that system tracks which players have participated in secondary abilities.

        Requirements: 5.5 - System tracks which players have participated in ability resolution
        """
        # Create and integrate systems
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()

        # Assign strategy card to player1
        coordinator.assign_strategy_card("player1", StrategyCardType.WARFARE)

        # Initially no players have participated
        assert (
            coordinator.get_secondary_ability_participants(StrategyCardType.WARFARE)
            == []
        )

        # Player2 uses secondary ability
        coordinator.use_secondary_ability("player2", StrategyCardType.WARFARE)

        # Verify participation is tracked
        participants = coordinator.get_secondary_ability_participants(
            StrategyCardType.WARFARE
        )
        assert "player2" in participants

    def test_secondary_ability_multiple_participants(self) -> None:
        """Test that multiple players can participate in secondary abilities.

        Requirements: 5.4, 5.5 - Secondary abilities available to all other players,
        system tracks participation
        """
        # Create and integrate systems
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()

        # Assign strategy card to player1
        coordinator.assign_strategy_card("player1", StrategyCardType.WARFARE)

        # Multiple players use secondary ability
        coordinator.use_secondary_ability("player2", StrategyCardType.WARFARE)
        coordinator.use_secondary_ability("player3", StrategyCardType.WARFARE)

        # Verify all participants are tracked
        participants = coordinator.get_secondary_ability_participants(
            StrategyCardType.WARFARE
        )
        assert "player2" in participants
        assert "player3" in participants
        assert len(participants) == 2


class TestRule83AbilityValidation:
    """Test ability validation and error handling."""

    def test_primary_ability_validation_with_invalid_inputs(self) -> None:
        """Test primary ability validation handles invalid inputs gracefully.

        Requirements: 5.3 - System rejects invalid operations
        """
        # Create and integrate systems
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()

        # Test with empty player ID
        assert not coordinator.can_use_primary_ability("", StrategyCardType.WARFARE)

        # Test with None card
        assert not coordinator.can_use_primary_ability("player1", None)

    def test_secondary_ability_validation_with_invalid_inputs(self) -> None:
        """Test secondary ability validation handles invalid inputs gracefully.

        Requirements: 5.3 - System rejects invalid operations
        """
        # Create and integrate systems
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()

        # Test with empty player ID
        assert not coordinator.can_use_secondary_ability("", StrategyCardType.WARFARE)

        # Test with None card
        assert not coordinator.can_use_secondary_ability("player1", None)

    def test_ability_framework_integration_with_strategic_actions(self) -> None:
        """Test that ability framework integrates with existing strategic action patterns.

        Requirements: Integration with existing strategic action participant tracking
        """
        # Create and integrate systems
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()

        # Set up player order for strategic action
        strategic_action_manager.set_player_order(["player1", "player2", "player3"])
        strategic_action_manager.set_action_phase(True)

        # Assign strategy card
        coordinator.assign_strategy_card("player1", StrategyCardType.WARFARE)

        # Activate strategy card via coordinator
        result = strategic_action_manager.activate_strategy_card_via_coordinator(
            "player1", StrategyCardType.WARFARE
        )

        # Verify integration works
        assert result.success
        assert result.primary_ability_resolved

        # Verify secondary abilities are available to other players
        assert coordinator.can_use_secondary_ability(
            "player2", StrategyCardType.WARFARE
        )
        assert coordinator.can_use_secondary_ability(
            "player3", StrategyCardType.WARFARE
        )

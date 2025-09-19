"""Comprehensive integration tests for Rule 83: STRATEGY CARD system.

This module provides comprehensive integration testing to ensure the Rule 83
strategy card system works seamlessly with all existing systems including:
- Rule 82 (Strategic Action) system
- Rule 91 (Technology Strategy Card)
- Game state management
- End-to-end workflows

Requirements tested:
- 6.1: Integration with existing StrategicActionManager
- 6.2: Strategy card validation in strategic action workflow
- 6.3: Card exhaustion during strategic action resolution
- 6.5: Strategic actions work with strategy card coordinator

All tests follow strict TDD methodology with RED-GREEN-REFACTOR cycles.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from src.ti4.core.constants import Technology
from src.ti4.core.game_state import GameState
from src.ti4.core.player import Player
from src.ti4.core.strategic_action import StrategicActionManager, StrategyCardType
from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator


class IntegrationTestHelper:
    """Helper class to eliminate code duplication in integration tests."""

    @staticmethod
    def create_integrated_system() -> tuple[
        StrategicActionManager, StrategyCardCoordinator
    ]:
        """Create and integrate strategic action manager with coordinator.

        Returns:
            Tuple of (strategic_action_manager, coordinator)
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()
        return strategic_action_manager, coordinator

    @staticmethod
    def setup_action_phase(
        strategic_action_manager: StrategicActionManager, players: list[str]
    ) -> None:
        """Set up action phase with player order.

        Args:
            strategic_action_manager: The strategic action manager
            players: List of player IDs
        """
        strategic_action_manager.set_player_order(players)
        strategic_action_manager.set_action_phase(True)

    @staticmethod
    def assign_cards_to_players(
        coordinator: StrategyCardCoordinator,
        assignments: list[tuple[str, StrategyCardType]],
    ) -> None:
        """Assign strategy cards to players.

        Args:
            coordinator: The strategy card coordinator
            assignments: List of (player_id, card_type) tuples
        """
        for player_id, card_type in assignments:
            result = coordinator.assign_strategy_card(player_id, card_type)
            assert result.success, f"Failed to assign {card_type.value} to {player_id}"

    @staticmethod
    def create_game_state_with_players(player_ids: list[str]) -> GameState:
        """Create game state with specified players.

        Args:
            player_ids: List of player IDs to add

        Returns:
            GameState with players added
        """
        game_state = GameState()
        for player_id in player_ids:
            player = Player(player_id, f"Test Player {player_id}")
            game_state = game_state.add_player(player)
        return game_state


class TestRule83Rule82Integration:
    """Test comprehensive integration with Rule 82 (Strategic Action) system."""

    def test_complete_strategic_action_workflow_with_coordinator(self) -> None:
        """Test complete strategic action workflow using strategy card coordinator.

        This test verifies the full integration between Rule 82 and Rule 83 systems
        by executing a complete strategic action workflow.

        Requirements: 6.1, 6.2, 6.3, 6.5 - Complete Rule 82 integration
        """
        # Create integrated system using helper
        strategic_action_manager, coordinator = (
            IntegrationTestHelper.create_integrated_system()
        )

        # Setup multi-player game
        players = ["alice", "bob", "charlie"]
        IntegrationTestHelper.setup_action_phase(strategic_action_manager, players)

        # Strategy phase: assign cards to players
        assignments = [
            ("alice", StrategyCardType.LEADERSHIP),
            ("bob", StrategyCardType.WARFARE),
            ("charlie", StrategyCardType.TECHNOLOGY),
        ]
        IntegrationTestHelper.assign_cards_to_players(coordinator, assignments)

        # Action phase: test initiative order
        initiative_order = coordinator.get_action_phase_initiative_order()
        expected_order = ["alice", "bob", "charlie"]  # Based on card initiative values
        assert initiative_order == expected_order

        # Test strategic action activation via coordinator for each player
        for player_id, card_type in assignments:
            result = strategic_action_manager.activate_strategy_card_via_coordinator(
                player_id, card_type
            )
            assert result.success
            assert result.primary_ability_resolved
            assert result.secondary_abilities_offered

            # Verify card is exhausted via coordinator
            assert coordinator.is_strategy_card_exhausted(player_id, card_type)

    def test_strategic_action_validation_integration(self) -> None:
        """Test that strategic action validation works correctly with coordinator.

        Requirements: 6.2 - Strategy card validation in strategic action workflow
        """
        # Create integrated system using helper
        strategic_action_manager, coordinator = (
            IntegrationTestHelper.create_integrated_system()
        )

        # Setup game
        players = ["player1", "player2"]
        IntegrationTestHelper.setup_action_phase(strategic_action_manager, players)

        # Assign cards using helper
        assignments = [
            ("player1", StrategyCardType.DIPLOMACY),
            ("player2", StrategyCardType.POLITICS),
        ]
        IntegrationTestHelper.assign_cards_to_players(coordinator, assignments)

        # Test validation: player can activate their own card
        assert strategic_action_manager.can_activate_strategy_card_via_coordinator(
            "player1", StrategyCardType.DIPLOMACY
        )

        # Test validation: player cannot activate another player's card
        assert not strategic_action_manager.can_activate_strategy_card_via_coordinator(
            "player1", StrategyCardType.POLITICS
        )

        # Test validation: player cannot activate unassigned card
        assert not strategic_action_manager.can_activate_strategy_card_via_coordinator(
            "player1", StrategyCardType.CONSTRUCTION
        )

    def test_backward_compatibility_preservation(self) -> None:
        """Test that existing Rule 82 functionality is preserved.

        Requirements: 6.1 - Integration preserves existing functionality
        """
        # Test that strategic action manager works without coordinator
        strategic_action_manager = StrategicActionManager()
        strategic_action_manager.set_action_phase(True)

        # Use legacy strategic action functionality
        from src.ti4.core.strategic_action import StrategyCard

        warfare_card = StrategyCard(
            StrategyCardType.WARFARE,
            primary_ability="Move units",
            secondary_ability="Build units",
        )

        strategic_action_manager.assign_strategy_card("player1", warfare_card)

        # Verify legacy functionality still works
        assert strategic_action_manager.can_activate_strategy_card(
            "player1", StrategyCardType.WARFARE
        )

        result = strategic_action_manager.activate_strategy_card(
            "player1", StrategyCardType.WARFARE
        )
        assert result.success


class TestRule83Rule91Integration:
    """Test comprehensive integration with Rule 91 (Technology Strategy Card)."""

    def test_technology_strategy_card_coordinator_integration(self) -> None:
        """Test that Technology strategy card works with coordinator system.

        Requirements: 6.1, 6.5 - Technology strategy card integration
        """
        from src.ti4.core.technology_strategy_card import TechnologyStrategyCard

        # Create integrated system using helper
        strategic_action_manager, coordinator = (
            IntegrationTestHelper.create_integrated_system()
        )

        # Setup game with technology card
        players = ["tech_player", "other_player"]
        IntegrationTestHelper.setup_action_phase(strategic_action_manager, players)

        # Assign cards using helper
        assignments = [
            ("tech_player", StrategyCardType.TECHNOLOGY),
            ("other_player", StrategyCardType.WARFARE),
        ]
        IntegrationTestHelper.assign_cards_to_players(coordinator, assignments)

        # Verify technology card integration
        tech_card = TechnologyStrategyCard()
        assert tech_card.get_initiative_value() == 7

        # Test strategic action activation for technology card
        result = strategic_action_manager.activate_strategy_card_via_coordinator(
            "tech_player", StrategyCardType.TECHNOLOGY
        )
        assert result.success

        # Verify card is exhausted via coordinator
        assert coordinator.is_strategy_card_exhausted(
            "tech_player", StrategyCardType.TECHNOLOGY
        )

    def test_technology_card_abilities_with_coordinator(self) -> None:
        """Test that technology card abilities work with coordinator integration.

        Requirements: 6.3, 6.5 - Card abilities work with coordinator
        """
        from src.ti4.core.technology_strategy_card import TechnologyStrategyCard

        # Create technology card instance
        tech_card = TechnologyStrategyCard()

        # Test primary ability (should work independently)
        result = tech_card.execute_primary_ability(
            "tech_player", technology=Technology.ANTIMASS_DEFLECTORS
        )
        assert result.success
        assert (
            result.additional_data["technology_researched"]
            == Technology.ANTIMASS_DEFLECTORS
        )
        assert result.resources_spent == 0

        # Test secondary ability (should work independently)
        result = tech_card.execute_secondary_ability(
            "other_player",
            technology=Technology.ANTIMASS_DEFLECTORS,
            available_command_tokens=2,
            available_resources=4,
        )
        assert result.success
        assert result.command_tokens_spent == 1
        assert result.resources_spent == 4

    def test_all_strategy_cards_coordinator_compatibility(self) -> None:
        """Test that all strategy cards work with coordinator system.

        Requirements: 6.1 - All strategy cards integrate with coordinator
        """
        # Create integrated system using helper
        strategic_action_manager, coordinator = (
            IntegrationTestHelper.create_integrated_system()
        )

        # Test all 8 strategy cards
        all_cards = list(StrategyCardType)
        players = [f"player{i + 1}" for i in range(len(all_cards))]
        IntegrationTestHelper.setup_action_phase(strategic_action_manager, players)

        # Assign all cards using helper
        assignments = [(players[i], card) for i, card in enumerate(all_cards)]
        IntegrationTestHelper.assign_cards_to_players(coordinator, assignments)

        # Test activation of each card type
        for i, card in enumerate(all_cards):
            result = strategic_action_manager.activate_strategy_card_via_coordinator(
                players[i], card
            )
            assert result.success, f"Failed to activate {card.value}"
            assert coordinator.is_strategy_card_exhausted(players[i], card)


class TestRule83GameStateIntegration:
    """Test comprehensive integration with game state management."""

    def test_game_state_strategy_card_tracking(self) -> None:
        """Test that game state correctly tracks strategy card assignments.

        Requirements: 6.2 - Game state integration for strategy card assignments
        """
        # Create game state with players using helper
        players = ["player1", "player2"]
        IntegrationTestHelper.create_game_state_with_players(players)

        # Create coordinator
        strategic_action_manager, coordinator = (
            IntegrationTestHelper.create_integrated_system()
        )

        # Test strategy card assignment tracking using helper
        assignments = [
            ("player1", StrategyCardType.LEADERSHIP),
            ("player2", StrategyCardType.DIPLOMACY),
        ]
        IntegrationTestHelper.assign_cards_to_players(coordinator, assignments)

        # Verify assignments are tracked
        assert (
            coordinator.get_player_strategy_card("player1")
            == StrategyCardType.LEADERSHIP
        )
        assert (
            coordinator.get_player_strategy_card("player2")
            == StrategyCardType.DIPLOMACY
        )

        # Test card state tracking
        strategic_action_manager.set_action_phase(True)
        strategic_action_manager.set_player_order(["player1", "player2"])
        coordinator.integrate_with_strategic_actions()

        # Activate cards and verify state tracking
        strategic_action_manager.activate_strategy_card_via_coordinator(
            "player1", StrategyCardType.LEADERSHIP
        )
        assert coordinator.is_strategy_card_exhausted(
            "player1", StrategyCardType.LEADERSHIP
        )

    def test_game_state_persistence_across_phases(self) -> None:
        """Test that strategy card state persists across game phases.

        Requirements: 6.2 - Strategy card state persistence
        """
        # Create integrated system using helper
        strategic_action_manager, coordinator = (
            IntegrationTestHelper.create_integrated_system()
        )

        # Strategy phase - assign cards using helper
        players = ["alice", "bob"]
        assignments = [
            ("alice", StrategyCardType.CONSTRUCTION),
            ("bob", StrategyCardType.TRADE),
        ]
        IntegrationTestHelper.assign_cards_to_players(coordinator, assignments)

        # Action phase
        IntegrationTestHelper.setup_action_phase(strategic_action_manager, players)

        # Activate cards
        strategic_action_manager.activate_strategy_card_via_coordinator(
            "alice", StrategyCardType.CONSTRUCTION
        )

        # Verify state persists
        assert (
            coordinator.get_player_strategy_card("alice")
            == StrategyCardType.CONSTRUCTION
        )
        assert coordinator.get_player_strategy_card("bob") == StrategyCardType.TRADE
        assert coordinator.is_strategy_card_exhausted(
            "alice", StrategyCardType.CONSTRUCTION
        )
        assert coordinator.is_strategy_card_readied("bob", StrategyCardType.TRADE)

    def test_multiple_game_rounds_integration(self) -> None:
        """Test strategy card system across multiple game rounds.

        Requirements: 6.2 - Multi-round game state integration
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        players = ["player1", "player2", "player3"]

        # Round 1
        coordinator.start_strategy_phase_selection(players)
        coordinator.select_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.select_strategy_card("player2", StrategyCardType.WARFARE)
        coordinator.select_strategy_card("player3", StrategyCardType.TECHNOLOGY)

        # Activate cards in round 1
        strategic_action_manager.set_action_phase(True)
        strategic_action_manager.set_player_order(players)
        coordinator.integrate_with_strategic_actions()

        for player in players:
            card = coordinator.get_player_strategy_card(player)
            strategic_action_manager.activate_strategy_card_via_coordinator(
                player, card
            )

        # Verify all cards exhausted
        for player in players:
            card = coordinator.get_player_strategy_card(player)
            assert coordinator.is_strategy_card_exhausted(player, card)

        # Status phase - ready cards
        coordinator.ready_all_strategy_cards()

        # Verify cards are readied
        for player in players:
            card = coordinator.get_player_strategy_card(player)
            assert coordinator.is_strategy_card_readied(player, card)

        # Round 2 - reset and new selection
        coordinator.reset_strategy_phase()

        # New card selection for round 2
        coordinator.start_strategy_phase_selection(players)
        coordinator.select_strategy_card("player1", StrategyCardType.DIPLOMACY)
        coordinator.select_strategy_card("player2", StrategyCardType.POLITICS)
        coordinator.select_strategy_card("player3", StrategyCardType.CONSTRUCTION)

        # Verify new assignments
        assert (
            coordinator.get_player_strategy_card("player1")
            == StrategyCardType.DIPLOMACY
        )
        assert (
            coordinator.get_player_strategy_card("player2") == StrategyCardType.POLITICS
        )
        assert (
            coordinator.get_player_strategy_card("player3")
            == StrategyCardType.CONSTRUCTION
        )


class TestRule83EndToEndWorkflows:
    """Test complete end-to-end workflows for strategy card system."""

    def test_complete_game_workflow_three_players(self) -> None:
        """Test complete strategy card workflow for a 3-player game.

        Requirements: 6.1, 6.2, 6.3, 6.5 - Complete end-to-end workflow
        """
        # Setup complete game system
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()

        players = ["alice", "bob", "charlie"]
        strategic_action_manager.set_player_order(players)

        # Phase 1: Strategy Phase - Card Selection
        coordinator.start_strategy_phase_selection(players)

        # Verify initial state
        assert coordinator.get_player_count() == 3
        assert len(coordinator.get_available_cards()) == 8
        assert coordinator.get_expected_unselected_cards_count() == 5

        # Players select cards in speaker order
        coordinator.select_strategy_card("alice", StrategyCardType.LEADERSHIP)
        coordinator.select_strategy_card("bob", StrategyCardType.WARFARE)
        coordinator.select_strategy_card("charlie", StrategyCardType.TECHNOLOGY)

        # Verify strategy phase completion
        assert coordinator.is_strategy_phase_complete()
        assert len(coordinator.get_available_cards()) == 5  # 5 unselected cards

        # Phase 2: Action Phase - Initiative Order and Activation
        strategic_action_manager.set_action_phase(True)

        # Get initiative order
        initiative_order = coordinator.get_action_phase_initiative_order()
        expected_order = [
            "alice",
            "bob",
            "charlie",
        ]  # Leadership(1), Warfare(6), Technology(7)
        assert initiative_order == expected_order

        # Players activate cards in initiative order
        for player in initiative_order:
            player_card = coordinator.get_player_strategy_card(player)

            # Verify can activate
            assert strategic_action_manager.can_activate_strategy_card_via_coordinator(
                player, player_card
            )

            # Activate card
            result = strategic_action_manager.activate_strategy_card_via_coordinator(
                player, player_card
            )
            assert result.success
            assert result.primary_ability_resolved

            # Verify card is exhausted
            assert coordinator.is_strategy_card_exhausted(player, player_card)

        # Phase 3: Status Phase - Ready Cards
        coordinator.ready_all_strategy_cards()

        # Verify all cards are readied
        for player in players:
            player_card = coordinator.get_player_strategy_card(player)
            assert coordinator.is_strategy_card_readied(player, player_card)

        # Phase 4: Next Round - Reset and New Selection
        coordinator.reset_strategy_phase()

        # Verify reset state
        assert coordinator.get_player_count() == 0
        assert len(coordinator.get_available_cards()) == 8
        assert not coordinator.is_strategy_phase_complete()

    def test_complete_game_workflow_eight_players(self) -> None:
        """Test complete strategy card workflow for an 8-player game.

        Requirements: 6.1, 6.2, 6.3, 6.5 - Complete workflow with maximum players
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()

        # 8-player game (maximum)
        players = [f"player{i + 1}" for i in range(8)]
        strategic_action_manager.set_player_order(players)

        # Strategy phase - all cards selected
        coordinator.start_strategy_phase_selection(players)

        assert coordinator.get_player_count() == 8
        assert coordinator.get_expected_unselected_cards_count() == 0

        # Assign all 8 cards
        all_cards = list(StrategyCardType)
        for i, player in enumerate(players):
            coordinator.select_strategy_card(player, all_cards[i])

        # Verify all cards assigned
        assert coordinator.is_strategy_phase_complete()
        assert len(coordinator.get_available_cards()) == 0

        # Action phase - all players activate
        strategic_action_manager.set_action_phase(True)

        initiative_order = coordinator.get_action_phase_initiative_order()
        assert len(initiative_order) == 8

        # All players activate their cards
        for player in initiative_order:
            player_card = coordinator.get_player_strategy_card(player)
            result = strategic_action_manager.activate_strategy_card_via_coordinator(
                player, player_card
            )
            assert result.success

        # Verify all cards exhausted
        for player in players:
            player_card = coordinator.get_player_strategy_card(player)
            assert coordinator.is_strategy_card_exhausted(player, player_card)

    def test_error_handling_in_complete_workflow(self) -> None:
        """Test error handling throughout complete workflow.

        Requirements: 6.2 - Error handling in integrated workflow
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()

        players = ["player1", "player2"]
        strategic_action_manager.set_player_order(players)

        # Test error: activate card before strategy phase (should return failure, not raise)
        result = strategic_action_manager.activate_strategy_card_via_coordinator(
            "player1", StrategyCardType.LEADERSHIP
        )
        assert not result.success

        # Strategy phase
        coordinator.assign_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.assign_strategy_card("player2", StrategyCardType.WARFARE)

        # Test error: assign card that's already assigned to another player
        result = coordinator.assign_strategy_card(
            "player1", StrategyCardType.WARFARE
        )  # Already assigned to player2
        assert not result.success

        # Action phase
        strategic_action_manager.set_action_phase(True)

        # Test error: wrong player activates card
        assert not strategic_action_manager.can_activate_strategy_card_via_coordinator(
            "player1",
            StrategyCardType.WARFARE,  # player2's card
        )

        # Test error: activate already exhausted card
        strategic_action_manager.activate_strategy_card_via_coordinator(
            "player1", StrategyCardType.LEADERSHIP
        )

        # Try to activate again (should fail)
        result = strategic_action_manager.activate_strategy_card_via_coordinator(
            "player1", StrategyCardType.LEADERSHIP
        )
        assert not result.success

    def test_secondary_abilities_complete_workflow(self) -> None:
        """Test secondary abilities in complete workflow.

        Requirements: 6.5 - Secondary abilities work in complete workflow
        """
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        coordinator.integrate_with_strategic_actions()

        players = ["active_player", "secondary_player1", "secondary_player2"]
        strategic_action_manager.set_player_order(players)

        # Strategy phase
        coordinator.start_strategy_phase_selection(players)
        coordinator.select_strategy_card("active_player", StrategyCardType.LEADERSHIP)
        coordinator.select_strategy_card("secondary_player1", StrategyCardType.WARFARE)
        coordinator.select_strategy_card(
            "secondary_player2", StrategyCardType.TECHNOLOGY
        )

        # Action phase
        strategic_action_manager.set_action_phase(True)

        # Active player activates Leadership
        result = strategic_action_manager.activate_strategy_card_via_coordinator(
            "active_player", StrategyCardType.LEADERSHIP
        )

        assert result.success
        assert result.primary_ability_resolved
        assert result.secondary_abilities_offered

        # Verify secondary ability order excludes active player
        expected_secondary_order = ["secondary_player1", "secondary_player2"]
        assert result.secondary_ability_order == expected_secondary_order

        # Verify card is exhausted after primary ability
        assert coordinator.is_strategy_card_exhausted(
            "active_player", StrategyCardType.LEADERSHIP
        )

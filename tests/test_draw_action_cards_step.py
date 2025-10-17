"""Tests for DrawActionCardsStep implementation.

This module tests the Step 3: Draw Action Cards functionality for Rule 81 (Status Phase).
Tests cover initiative order processing, empty deck handling, and integration with
the action card system.

LRR References:
- Rule 81.3: Status Phase Step 3 - Draw Action Cards
- Rule 2: Action Cards - Drawing mechanics and deck management
"""

from unittest.mock import Mock, patch

import pytest

from src.ti4.core.game_state import GameState
from src.ti4.core.player import Player
from src.ti4.core.status_phase import (
    DrawActionCardsStep,
    SystemIntegrationError,
)


class TestDrawActionCardsStep:
    """Test suite for DrawActionCardsStep (Rule 81.3)."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.step = DrawActionCardsStep()

    def test_step_name(self) -> None:
        """Test that step returns correct name."""
        assert self.step.get_step_name() == "Draw Action Cards"

    def test_execute_with_none_game_state(self) -> None:
        """Test execute with None game state returns error."""
        result, state = self.step.execute(None)

        assert not result.success
        assert result.step_name == "Draw Action Cards"
        assert "Game state cannot be None" in result.error_message
        assert result.players_processed == []
        assert result.actions_taken == []
        assert state is None

    def test_validate_prerequisites_with_none_game_state(self) -> None:
        """Test validate_prerequisites with None game state returns False."""
        assert not self.step.validate_prerequisites(None)

    def test_validate_prerequisites_with_valid_game_state(self) -> None:
        """Test validate_prerequisites with valid game state returns True."""
        # Create mock game state with players
        game_state = Mock(spec=GameState)
        game_state.players = [Mock(spec=Player)]

        assert self.step.validate_prerequisites(game_state)

    def test_validate_prerequisites_with_no_players(self) -> None:
        """Test validate_prerequisites with no players returns False."""
        # Create mock game state without players
        game_state = Mock(spec=GameState)
        game_state.players = None

        assert not self.step.validate_prerequisites(game_state)

    def test_execute_initiative_order_processing(self) -> None:
        """Test that players are processed in initiative order."""
        # Create mock game state with players
        player1 = Mock(spec=Player)
        player1.id = "player1"
        player2 = Mock(spec=Player)
        player2.id = "player2"
        player3 = Mock(spec=Player)
        player3.id = "player3"

        game_state = Mock(spec=GameState)
        game_state.players = [player1, player2, player3]

        # Create a chain of mock states for each draw operation
        state_after_player2 = Mock(spec=GameState)
        state_after_player1 = Mock(spec=GameState)
        final_state = Mock(spec=GameState)

        # Set up the chaining: game_state -> state_after_player2 -> state_after_player1 -> final_state
        game_state.draw_action_cards.return_value = state_after_player2
        state_after_player2.draw_action_cards.return_value = state_after_player1
        state_after_player1.draw_action_cards.return_value = final_state

        # Mock strategy card coordinator to return specific initiative order
        with patch(
            "src.ti4.core.strategy_cards.coordinator.StrategyCardCoordinator"
        ) as mock_coordinator_class:
            mock_coordinator = Mock()
            mock_coordinator.get_status_phase_initiative_order.return_value = [
                "player2",
                "player1",
                "player3",
            ]
            mock_coordinator_class.return_value = mock_coordinator

            with patch("src.ti4.core.strategic_action.StrategicActionManager"):
                result, returned_final_state = self.step.execute(game_state)

        # Verify success
        assert result.success
        assert result.step_name == "Draw Action Cards"
        assert result.players_processed == ["player2", "player1", "player3"]
        assert len(result.actions_taken) == 3
        assert "Player player2 drew 1 action card" in result.actions_taken
        assert "Player player1 drew 1 action card" in result.actions_taken
        assert "Player player3 drew 1 action card" in result.actions_taken

        # Verify draw_action_cards was called for each player in correct order
        game_state.draw_action_cards.assert_called_once_with("player2", 1)
        state_after_player2.draw_action_cards.assert_called_once_with("player1", 1)
        state_after_player1.draw_action_cards.assert_called_once_with("player3", 1)

        # Verify final state is returned
        assert returned_final_state == final_state

    def test_execute_with_nonexistent_players_in_initiative_order(self) -> None:
        """Test that nonexistent players in initiative order are filtered out."""
        # Create mock game state with only 2 players
        player1 = Mock(spec=Player)
        player1.id = "player1"
        player2 = Mock(spec=Player)
        player2.id = "player2"

        game_state = Mock(spec=GameState)
        game_state.players = [player1, player2]

        # Create a chain of mock states for each draw operation
        state_after_player1 = Mock(spec=GameState)
        final_state = Mock(spec=GameState)

        # Set up the chaining: game_state -> state_after_player1 -> final_state
        game_state.draw_action_cards.return_value = state_after_player1
        state_after_player1.draw_action_cards.return_value = final_state

        # Mock strategy card coordinator to return initiative order with nonexistent player
        with patch(
            "src.ti4.core.strategy_cards.coordinator.StrategyCardCoordinator"
        ) as mock_coordinator_class:
            mock_coordinator = Mock()
            mock_coordinator.get_status_phase_initiative_order.return_value = [
                "player1",
                "nonexistent_player",
                "player2",
            ]
            mock_coordinator_class.return_value = mock_coordinator

            with patch("src.ti4.core.strategic_action.StrategicActionManager"):
                result, returned_final_state = self.step.execute(game_state)

        # Verify success with only existing players processed
        assert result.success
        assert result.players_processed == ["player1", "player2"]
        assert len(result.actions_taken) == 2

        # Verify draw_action_cards was called only for existing players
        game_state.draw_action_cards.assert_called_once_with("player1", 1)
        state_after_player1.draw_action_cards.assert_called_once_with("player2", 1)

        # Verify final state is returned
        assert returned_final_state == final_state

    def test_execute_with_draw_action_cards_error(self) -> None:
        """Test handling of draw_action_cards method errors."""
        # Create mock game state with players
        player1 = Mock(spec=Player)
        player1.id = "player1"

        game_state = Mock(spec=GameState)
        game_state.players = [player1]

        # Mock draw_action_cards to raise an exception
        game_state.draw_action_cards.side_effect = ValueError("Deck is empty")

        # Mock strategy card coordinator
        with patch(
            "src.ti4.core.strategy_cards.coordinator.StrategyCardCoordinator"
        ) as mock_coordinator_class:
            mock_coordinator = Mock()
            mock_coordinator.get_status_phase_initiative_order.return_value = [
                "player1"
            ]
            mock_coordinator_class.return_value = mock_coordinator

            with patch("src.ti4.core.strategic_action.StrategicActionManager"):
                result, final_state = self.step.execute(game_state)

        # Verify error handling
        assert not result.success
        assert result.step_name == "Draw Action Cards"
        assert (
            "Error drawing cards for player player1: Deck is empty"
            in result.error_message
        )
        assert result.players_processed == []
        assert result.actions_taken == []

    def test_execute_empty_deck_handling(self) -> None:
        """Test graceful handling of empty action card deck."""
        # Create mock game state with players
        player1 = Mock(spec=Player)
        player1.id = "player1"

        game_state = Mock(spec=GameState)
        game_state.players = [player1]

        # Mock draw_action_cards to raise a specific empty deck error
        game_state.draw_action_cards.side_effect = SystemIntegrationError(
            "Action card deck is empty"
        )

        # Mock strategy card coordinator
        with patch(
            "src.ti4.core.strategy_cards.coordinator.StrategyCardCoordinator"
        ) as mock_coordinator_class:
            mock_coordinator = Mock()
            mock_coordinator.get_status_phase_initiative_order.return_value = [
                "player1"
            ]
            mock_coordinator_class.return_value = mock_coordinator

            with patch("src.ti4.core.strategic_action.StrategicActionManager"):
                result, final_state = self.step.execute(game_state)

        # Verify error is properly reported
        assert not result.success
        assert "Action card deck is empty" in result.error_message

    def test_execute_integration_with_action_card_system(self) -> None:
        """Test integration with existing action card system."""
        # Create mock game state with players
        player1 = Mock(spec=Player)
        player1.id = "player1"

        game_state = Mock(spec=GameState)
        game_state.players = [player1]

        # Mock the draw_action_cards method to return new state
        new_state = Mock(spec=GameState)
        game_state.draw_action_cards.return_value = new_state

        # Mock strategy card coordinator
        with patch(
            "src.ti4.core.strategy_cards.coordinator.StrategyCardCoordinator"
        ) as mock_coordinator_class:
            mock_coordinator = Mock()
            mock_coordinator.get_status_phase_initiative_order.return_value = [
                "player1"
            ]
            mock_coordinator_class.return_value = mock_coordinator

            with patch("src.ti4.core.strategic_action.StrategicActionManager"):
                result, final_state = self.step.execute(game_state)

        # Verify integration with action card system
        assert result.success
        game_state.draw_action_cards.assert_called_once_with("player1", 1)
        assert final_state == new_state

    def test_draw_card_for_player_success(self) -> None:
        """Test successful card drawing for a single player."""
        # Create mock game state
        game_state = Mock(spec=GameState)
        new_state = Mock(spec=GameState)
        game_state.draw_action_cards.return_value = new_state

        success, updated_state = self.step.draw_card_for_player("player1", game_state)

        assert success
        assert updated_state == new_state
        game_state.draw_action_cards.assert_called_once_with("player1", 1)

    def test_draw_card_for_player_with_error(self) -> None:
        """Test card drawing with error."""
        # Create mock game state that raises error
        game_state = Mock(spec=GameState)
        game_state.draw_action_cards.side_effect = ValueError("Test error")

        # The method should now raise the exception instead of returning False
        with pytest.raises(ValueError, match="Test error"):
            self.step.draw_card_for_player("player1", game_state)

    def test_draw_card_for_player_with_empty_player_id(self) -> None:
        """Test card drawing with empty player ID."""
        game_state = Mock(spec=GameState)

        success, updated_state = self.step.draw_card_for_player("", game_state)

        assert not success
        assert updated_state == game_state

    def test_draw_card_for_player_with_none_game_state(self) -> None:
        """Test card drawing with None game state."""
        success, updated_state = self.step.draw_card_for_player("player1", None)

        assert not success
        assert updated_state is None

    def test_execute_with_large_number_of_players(self) -> None:
        """Test execute with maximum number of players (8)."""
        # Create mock game state with 8 players
        players = []
        for i in range(1, 9):
            player = Mock(spec=Player)
            player.id = f"player{i}"
            players.append(player)

        game_state = Mock(spec=GameState)
        game_state.players = players

        # Create a chain of mock states for each draw operation
        states = [Mock(spec=GameState) for _ in range(8)]
        current_state = game_state

        # Set up the chaining
        for _i, next_state in enumerate(states):
            current_state.draw_action_cards.return_value = next_state
            current_state = next_state

        # Mock strategy card coordinator with all 8 players
        with patch(
            "src.ti4.core.strategy_cards.coordinator.StrategyCardCoordinator"
        ) as mock_coordinator_class:
            mock_coordinator = Mock()
            mock_coordinator.get_status_phase_initiative_order.return_value = [
                f"player{i}" for i in range(1, 9)
            ]
            mock_coordinator_class.return_value = mock_coordinator

            with patch("src.ti4.core.strategic_action.StrategicActionManager"):
                result, final_state = self.step.execute(game_state)

        # Verify all 8 players were processed
        assert result.success
        assert len(result.players_processed) == 8
        assert len(result.actions_taken) == 8

        # Verify draw_action_cards was called for each player
        game_state.draw_action_cards.assert_called_once_with("player1", 1)
        for i in range(7):
            states[i].draw_action_cards.assert_called_once_with(f"player{i + 2}", 1)

        # Verify final state is returned
        assert final_state == states[-1]

    def test_execute_with_coordinator_creation_error(self) -> None:
        """Test handling of strategy card coordinator creation errors."""
        # Create mock game state with players
        player1 = Mock(spec=Player)
        player1.id = "player1"

        game_state = Mock(spec=GameState)
        game_state.players = [player1]

        # Mock coordinator creation to raise an exception
        with patch(
            "src.ti4.core.strategy_cards.coordinator.StrategyCardCoordinator"
        ) as mock_coordinator_class:
            mock_coordinator_class.side_effect = Exception(
                "Coordinator creation failed"
            )

            result, final_state = self.step.execute(game_state)

        # Verify error handling
        assert not result.success
        assert "Coordinator creation failed" in result.error_message
        assert final_state == game_state

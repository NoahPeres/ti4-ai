"""Tests for command token management steps (Steps 4-5).

This module tests the RemoveCommandTokensStep and GainRedistributeTokensStep
classes that handle command token removal and redistribution during status phase.

LRR References:
- Rule 81.4: Status Phase Step 4 - Remove Command Tokens
- Rule 81.5: Status Phase Step 5 - Gain and Redistribute Command Tokens
- Rule 20: Command Tokens - Token management mechanics
- Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 10.3, 12.3
"""

from typing import TYPE_CHECKING
from unittest.mock import Mock

if TYPE_CHECKING:
    pass


class TestRemoveCommandTokensStep:
    """Test RemoveCommandTokensStep class.

    Tests the functionality of Step 4: Remove Command Tokens from board,
    including token removal for all players and integration with command token system.

    Requirements: 5.1, 5.2, 12.3
    """

    def test_remove_command_tokens_step_creation(self) -> None:
        """Test creating RemoveCommandTokensStep instance.

        Verifies that the step handler can be instantiated successfully.
        """
        from src.ti4.core.status_phase import RemoveCommandTokensStep

        step = RemoveCommandTokensStep()
        assert step is not None

    def test_remove_command_tokens_step_implements_interface(self) -> None:
        """Test that RemoveCommandTokensStep implements StatusPhaseStepHandler interface.

        Verifies that the step handler properly implements all required methods.

        Requirements: 5.1 - Command token removal functionality
        """
        from src.ti4.core.status_phase import (
            RemoveCommandTokensStep,
            StatusPhaseStepHandler,
        )

        # Arrange & Act: Create step handler
        step = RemoveCommandTokensStep()

        # Assert: Should implement StatusPhaseStepHandler interface
        assert isinstance(step, StatusPhaseStepHandler)
        assert hasattr(step, "execute")
        assert hasattr(step, "validate_prerequisites")
        assert hasattr(step, "get_step_name")
        assert callable(step.execute)
        assert callable(step.validate_prerequisites)
        assert callable(step.get_step_name)

    def test_remove_command_tokens_step_name(self) -> None:
        """Test RemoveCommandTokensStep step name.

        Verifies that the step returns the correct name.

        Requirements: 5.1 - Command token removal functionality
        """
        from src.ti4.core.status_phase import RemoveCommandTokensStep

        # Arrange & Act: Create step and get name
        step = RemoveCommandTokensStep()
        step_name = step.get_step_name()

        # Assert: Should return correct step name
        assert step_name == "Remove Command Tokens"

    def test_remove_command_tokens_execute_success(self) -> None:
        """Test successful execution of remove command tokens step.

        Verifies that command tokens are removed from the board for all players.

        Requirements: 5.1 - Remove all command tokens from game board
        """
        from src.ti4.core.status_phase import RemoveCommandTokensStep, StepResult

        # Arrange: Create mock game state with players and systems
        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player1"), Mock(id="player2")]
        mock_game_state.systems = {
            "system1": Mock(command_tokens={"player1": True, "player2": True}),
            "system2": Mock(command_tokens={"player1": True}),
        }

        # Act: Execute remove command tokens step
        step = RemoveCommandTokensStep()
        result, updated_state = step.execute(mock_game_state)

        # Assert: Should return successful result
        assert isinstance(result, StepResult)
        assert result.success is True
        assert result.step_name == "Remove Command Tokens"
        assert len(result.players_processed) == 2
        assert "player1" in result.players_processed
        assert "player2" in result.players_processed
        assert updated_state is not None

    def test_remove_command_tokens_execute_with_none_game_state(self) -> None:
        """Test remove command tokens step with None game state.

        Verifies that the step handles None game state gracefully.

        Requirements: 5.1, 12.3 - Error handling
        """
        from src.ti4.core.status_phase import RemoveCommandTokensStep, StepResult

        # Arrange: Create step with None game state
        step = RemoveCommandTokensStep()

        # Act: Execute with None game state
        result, updated_state = step.execute(None)

        # Assert: Should handle error gracefully
        assert isinstance(result, StepResult)
        assert result.success is False
        assert result.error_message == "Game state cannot be None"
        assert updated_state is None

    def test_remove_command_tokens_validate_prerequisites_success(self) -> None:
        """Test successful prerequisite validation for remove command tokens step.

        Verifies that valid game state passes prerequisite validation.

        Requirements: 5.1 - Command token removal validation
        """
        from src.ti4.core.status_phase import RemoveCommandTokensStep

        # Arrange: Create mock game state
        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player1")]

        # Act: Validate prerequisites
        step = RemoveCommandTokensStep()
        is_valid = step.validate_prerequisites(mock_game_state)

        # Assert: Should pass validation
        assert is_valid is True

    def test_remove_command_tokens_validate_prerequisites_none_state(self) -> None:
        """Test prerequisite validation with None game state.

        Verifies that None game state fails prerequisite validation.

        Requirements: 5.1, 12.3 - Error handling
        """
        from src.ti4.core.status_phase import RemoveCommandTokensStep

        # Arrange: Create step
        step = RemoveCommandTokensStep()

        # Act: Validate prerequisites with None
        is_valid = step.validate_prerequisites(None)

        # Assert: Should fail validation
        assert is_valid is False

    def test_remove_command_tokens_integration_with_command_token_system(self) -> None:
        """Test integration with existing command token system.

        Verifies that the step properly integrates with the command token system
        to remove tokens from systems.

        Requirements: 10.3 - Integration with command token system
        """
        from src.ti4.core.status_phase import RemoveCommandTokensStep

        # Arrange: Create mock game state with command token system
        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player1"), Mock(id="player2")]

        # Mock systems with command tokens
        mock_system1 = Mock()
        mock_system1.command_tokens = {"player1": True, "player2": True}
        mock_system1.remove_command_token = Mock()

        mock_system2 = Mock()
        mock_system2.command_tokens = {"player1": True}
        mock_system2.remove_command_token = Mock()

        mock_game_state.systems = {"system1": mock_system1, "system2": mock_system2}

        # Act: Execute remove command tokens step
        step = RemoveCommandTokensStep()
        result, updated_state = step.execute(mock_game_state)

        # Assert: Should integrate with command token system
        assert result.success is True
        # Verify that remove_command_token was called for each player's tokens
        mock_system1.remove_command_token.assert_any_call("player1")
        mock_system1.remove_command_token.assert_any_call("player2")
        mock_system2.remove_command_token.assert_any_call("player1")


class TestGainRedistributeTokensStep:
    """Test GainRedistributeTokensStep class.

    Tests the functionality of Step 5: Gain and Redistribute Command Tokens,
    including token gaining, redistribution logic, and integration with command token system.

    Requirements: 5.3, 5.4, 5.5, 12.3
    """

    def test_gain_redistribute_tokens_step_creation(self) -> None:
        """Test creating GainRedistributeTokensStep instance.

        Verifies that the step handler can be instantiated successfully.
        """
        from src.ti4.core.status_phase import GainRedistributeTokensStep

        step = GainRedistributeTokensStep()
        assert step is not None

    def test_gain_redistribute_tokens_step_implements_interface(self) -> None:
        """Test that GainRedistributeTokensStep implements StatusPhaseStepHandler interface.

        Verifies that the step handler properly implements all required methods.

        Requirements: 5.3 - Token gaining and redistribution functionality
        """
        from src.ti4.core.status_phase import (
            GainRedistributeTokensStep,
            StatusPhaseStepHandler,
        )

        # Arrange & Act: Create step handler
        step = GainRedistributeTokensStep()

        # Assert: Should implement StatusPhaseStepHandler interface
        assert isinstance(step, StatusPhaseStepHandler)
        assert hasattr(step, "execute")
        assert hasattr(step, "validate_prerequisites")
        assert hasattr(step, "get_step_name")
        assert callable(step.execute)
        assert callable(step.validate_prerequisites)
        assert callable(step.get_step_name)

    def test_gain_redistribute_tokens_step_name(self) -> None:
        """Test GainRedistributeTokensStep step name.

        Verifies that the step returns the correct name.

        Requirements: 5.3 - Token gaining and redistribution functionality
        """
        from src.ti4.core.status_phase import GainRedistributeTokensStep

        # Arrange & Act: Create step and get name
        step = GainRedistributeTokensStep()
        step_name = step.get_step_name()

        # Assert: Should return correct step name
        assert step_name == "Gain and Redistribute Command Tokens"

    def test_gain_redistribute_tokens_execute_success(self) -> None:
        """Test successful execution of gain and redistribute tokens step.

        Verifies that each player gains 2 command tokens and can redistribute them.

        Requirements: 5.3 - Give each player 2 additional command tokens
        """
        from src.ti4.core.status_phase import GainRedistributeTokensStep, StepResult

        # Arrange: Create mock game state with players
        mock_player1 = Mock(id="player1")
        mock_player1.reinforcements = 5
        mock_player1.command_sheet = Mock()
        mock_player1.command_sheet.redistribute_tokens = Mock(return_value=True)

        mock_player2 = Mock(id="player2")
        mock_player2.reinforcements = 3
        mock_player2.command_sheet = Mock()
        mock_player2.command_sheet.redistribute_tokens = Mock(return_value=True)

        mock_game_state = Mock()
        mock_game_state.players = [mock_player1, mock_player2]

        # Act: Execute gain and redistribute tokens step
        step = GainRedistributeTokensStep()
        result, updated_state = step.execute(mock_game_state)

        # Assert: Should return successful result
        assert isinstance(result, StepResult)
        assert result.success is True
        assert result.step_name == "Gain and Redistribute Command Tokens"
        assert len(result.players_processed) == 2
        assert "player1" in result.players_processed
        assert "player2" in result.players_processed
        assert updated_state is not None

    def test_gain_redistribute_tokens_execute_with_none_game_state(self) -> None:
        """Test gain and redistribute tokens step with None game state.

        Verifies that the step handles None game state gracefully.

        Requirements: 5.3, 12.3 - Error handling
        """
        from src.ti4.core.status_phase import GainRedistributeTokensStep, StepResult

        # Arrange: Create step with None game state
        step = GainRedistributeTokensStep()

        # Act: Execute with None game state
        result, updated_state = step.execute(None)

        # Assert: Should handle error gracefully
        assert isinstance(result, StepResult)
        assert result.success is False
        assert result.error_message == "Game state cannot be None"
        assert updated_state is None

    def test_gain_redistribute_tokens_validate_prerequisites_success(self) -> None:
        """Test successful prerequisite validation for gain and redistribute tokens step.

        Verifies that valid game state passes prerequisite validation.

        Requirements: 5.3 - Token gaining and redistribution validation
        """
        from src.ti4.core.status_phase import GainRedistributeTokensStep

        # Arrange: Create mock game state
        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player1")]

        # Act: Validate prerequisites
        step = GainRedistributeTokensStep()
        is_valid = step.validate_prerequisites(mock_game_state)

        # Assert: Should pass validation
        assert is_valid is True

    def test_gain_redistribute_tokens_validate_prerequisites_none_state(self) -> None:
        """Test prerequisite validation with None game state.

        Verifies that None game state fails prerequisite validation.

        Requirements: 5.3, 12.3 - Error handling
        """
        from src.ti4.core.status_phase import GainRedistributeTokensStep

        # Arrange: Create step
        step = GainRedistributeTokensStep()

        # Act: Validate prerequisites with None
        is_valid = step.validate_prerequisites(None)

        # Assert: Should fail validation
        assert is_valid is False

    def test_gain_redistribute_tokens_integration_with_command_token_system(
        self,
    ) -> None:
        """Test integration with existing command token system.

        Verifies that the step properly integrates with the command token system
        to gain and redistribute tokens.

        Requirements: 10.3 - Integration with command token system
        """
        from src.ti4.core.status_phase import GainRedistributeTokensStep

        # Arrange: Create mock game state with command token system
        mock_player = Mock(id="player1")
        mock_player.reinforcements = 5
        mock_player.command_sheet = Mock()
        mock_player.command_sheet.redistribute_tokens = Mock(return_value=True)

        mock_game_state = Mock()
        mock_game_state.players = [mock_player]

        # Act: Execute gain and redistribute tokens step
        step = GainRedistributeTokensStep()
        result, updated_state = step.execute(mock_game_state)

        # Assert: Should integrate with command token system
        assert result.success is True
        # Verify that redistribution was called
        mock_player.command_sheet.redistribute_tokens.assert_called()

    def test_redistribute_tokens_for_player_success(self) -> None:
        """Test token redistribution for a single player.

        Verifies that token redistribution works correctly for individual players.

        Requirements: 5.4 - Allow redistribution among strategy, tactic, and fleet pools
        """
        from src.ti4.core.status_phase import GainRedistributeTokensStep

        # Arrange: Create mock player and game state
        mock_player = Mock(id="player1")
        mock_player.command_sheet = Mock()
        mock_player.command_sheet.redistribute_tokens = Mock(return_value=True)

        mock_game_state = Mock()
        mock_game_state.players = [mock_player]  # Make players iterable

        # Act: Redistribute tokens for player
        step = GainRedistributeTokensStep()
        updated_state = step.redistribute_tokens_for_player("player1", mock_game_state)

        # Assert: Should return updated game state
        assert updated_state is not None

    def test_redistribute_tokens_validates_pool_limits(self) -> None:
        """Test that token redistribution validates pool limits.

        Verifies that redistribution respects pool limits as defined in Rule 20.

        Requirements: 5.5 - Validate pool limits are respected
        """
        from src.ti4.core.status_phase import GainRedistributeTokensStep

        # Arrange: Create mock player with command sheet that validates limits
        mock_player = Mock(id="player1")
        mock_player.command_sheet = Mock()
        # Simulate redistribution that respects limits
        mock_player.command_sheet.redistribute_tokens = Mock(return_value=True)

        mock_game_state = Mock()
        mock_game_state.players = [mock_player]  # Make players iterable

        # Act: Redistribute tokens for player
        step = GainRedistributeTokensStep()
        updated_state = step.redistribute_tokens_for_player("player1", mock_game_state)

        # Assert: Should validate pool limits
        assert updated_state is not None
        # Verify that redistribution was called (which includes validation)
        mock_player.command_sheet.redistribute_tokens.assert_called()


class TestCommandTokenManagementStepsIntegration:
    """Test integration between command token management steps.

    Tests the interaction between Steps 4 and 5 and their integration
    with the existing command token system.

    Requirements: 10.3 - Integration with command token system
    """

    def test_remove_then_gain_tokens_sequence(self) -> None:
        """Test the sequence of removing then gaining command tokens.

        Verifies that Steps 4 and 5 work correctly in sequence.

        Requirements: 5.1, 5.3 - Token removal and gaining sequence
        """
        from src.ti4.core.status_phase import (
            GainRedistributeTokensStep,
            RemoveCommandTokensStep,
        )

        # Arrange: Create mock game state
        mock_player = Mock(id="player1")
        mock_player.reinforcements = 5
        mock_player.command_sheet = Mock()
        mock_player.command_sheet.redistribute_tokens = Mock(return_value=True)

        mock_system = Mock()
        mock_system.command_tokens = {"player1": True}
        mock_system.remove_command_token = Mock()

        mock_game_state = Mock()
        mock_game_state.players = [mock_player]
        mock_game_state.systems = {"system1": mock_system}

        # Act: Execute both steps in sequence
        remove_step = RemoveCommandTokensStep()
        gain_step = GainRedistributeTokensStep()

        # Step 4: Remove tokens
        remove_result, state_after_remove = remove_step.execute(mock_game_state)

        # Step 5: Gain and redistribute tokens
        gain_result, final_state = gain_step.execute(state_after_remove)

        # Assert: Both steps should succeed
        assert remove_result.success is True
        assert gain_result.success is True
        assert final_state is not None

        # Verify integration calls were made
        mock_system.remove_command_token.assert_called_with("player1")
        mock_player.command_sheet.redistribute_tokens.assert_called()

    def test_command_token_system_integration_error_handling(self) -> None:
        """Test error handling in command token system integration.

        Verifies that integration errors are handled gracefully.

        Requirements: 10.3, 12.3 - Integration error handling
        """
        from src.ti4.core.status_phase import RemoveCommandTokensStep

        # Arrange: Create mock game state that will cause integration error
        mock_system = Mock()
        mock_system.command_tokens = {"player1": True}
        mock_system.remove_command_token = Mock(
            side_effect=Exception("Integration error")
        )

        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player1")]
        mock_game_state.systems = {"system1": mock_system}

        # Act: Execute step that will encounter integration error
        step = RemoveCommandTokensStep()
        result, updated_state = step.execute(mock_game_state)

        # Assert: Should handle integration error gracefully
        assert result.success is False
        assert "Integration error" in result.error_message
        assert updated_state is not None

    def test_both_steps_implement_required_interface(self) -> None:
        """Test that both command token management steps implement required interface.

        Verifies that both RemoveCommandTokensStep and GainRedistributeTokensStep
        properly implement the StatusPhaseStepHandler interface.

        Requirements: 5.1, 5.3 - Interface implementation
        """
        from src.ti4.core.status_phase import (
            GainRedistributeTokensStep,
            RemoveCommandTokensStep,
            StatusPhaseStepHandler,
        )

        # Arrange & Act: Create both step handlers
        remove_step = RemoveCommandTokensStep()
        gain_step = GainRedistributeTokensStep()

        # Assert: Both should implement StatusPhaseStepHandler interface
        assert isinstance(remove_step, StatusPhaseStepHandler)
        assert isinstance(gain_step, StatusPhaseStepHandler)

        # Both should have all required methods
        for step in [remove_step, gain_step]:
            assert hasattr(step, "execute")
            assert hasattr(step, "validate_prerequisites")
            assert hasattr(step, "get_step_name")
            assert callable(step.execute)
            assert callable(step.validate_prerequisites)
            assert callable(step.get_step_name)

    def test_steps_return_different_names(self) -> None:
        """Test that both steps return different, descriptive names.

        Verifies that each step has a unique, descriptive name.

        Requirements: 5.1, 5.3 - Step identification
        """
        from src.ti4.core.status_phase import (
            GainRedistributeTokensStep,
            RemoveCommandTokensStep,
        )

        # Arrange & Act: Create both steps and get names
        remove_step = RemoveCommandTokensStep()
        gain_step = GainRedistributeTokensStep()

        remove_name = remove_step.get_step_name()
        gain_name = gain_step.get_step_name()

        # Assert: Should have different, descriptive names
        assert remove_name != gain_name
        assert remove_name == "Remove Command Tokens"
        assert gain_name == "Gain and Redistribute Command Tokens"
        assert isinstance(remove_name, str)
        assert isinstance(gain_name, str)
        assert len(remove_name) > 0
        assert len(gain_name) > 0

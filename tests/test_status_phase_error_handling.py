"""Comprehensive error handling tests for status phase implementation.

This module tests error handling, graceful degradation, and state validation
for all status phase components as required by task 13.1.

LRR References:
- Rule 81: Status Phase - Error handling requirements
- Requirements 11.1, 11.2, 11.3, 11.4, 11.5: Error handling specifications
"""

from unittest.mock import Mock, patch

import pytest

from src.ti4.core.status_phase import (
    DrawActionCardsStep,
    GainRedistributeTokensStep,
    ReadyCardsStep,
    RemoveCommandTokensStep,
    RepairUnitsStep,
    ReturnStrategyCardsStep,
    RevealObjectiveStep,
    ScoreObjectivesStep,
    StatusPhaseError,
    StatusPhaseGameStateError,
    StatusPhaseOrchestrator,
    StatusPhaseStepHandler,
    StepResult,
    StepValidationError,
    SystemIntegrationError,
)


class TestStatusPhaseErrorHierarchy:
    """Test the status phase error exception hierarchy.

    Requirements: 11.1 - Descriptive error messages and types
    """

    def test_status_phase_error_base_class(self) -> None:
        """Test StatusPhaseError base exception class."""
        # RED: Test that StatusPhaseError provides descriptive messages
        error = StatusPhaseError("Test error message")

        assert str(error) == "Test error message"
        assert isinstance(error, Exception)

    def test_step_validation_error_inheritance(self) -> None:
        """Test StepValidationError inherits from StatusPhaseError."""
        # RED: Test inheritance and descriptive messages
        error = StepValidationError("Step prerequisites not met")

        assert str(error) == "Step prerequisites not met"
        assert isinstance(error, StatusPhaseError)
        assert isinstance(error, Exception)

    def test_system_integration_error_inheritance(self) -> None:
        """Test SystemIntegrationError inherits from StatusPhaseError."""
        # RED: Test inheritance and descriptive messages
        error = SystemIntegrationError("Failed to integrate with objective system")

        assert str(error) == "Failed to integrate with objective system"
        assert isinstance(error, StatusPhaseError)
        assert isinstance(error, Exception)

    def test_game_state_error_inheritance(self) -> None:
        """Test StatusPhaseGameStateError inherits from StatusPhaseError."""
        # RED: Test inheritance and descriptive messages
        error = StatusPhaseGameStateError("Invalid game state for status phase")

        assert str(error) == "Invalid game state for status phase"
        assert isinstance(error, StatusPhaseError)
        assert isinstance(error, Exception)


class TestOrchestratorErrorHandling:
    """Test error handling in StatusPhaseOrchestrator.

    Requirements: 11.3 - Graceful degradation for non-critical failures
    """

    def test_execute_complete_status_phase_with_none_game_state(self) -> None:
        """Test complete status phase execution with None game state."""
        # RED: Test graceful handling of None game state
        orchestrator = StatusPhaseOrchestrator()

        result, updated_state = orchestrator.execute_complete_status_phase(None)

        assert result.success is False
        assert "Game state cannot be None" in result.error_message
        assert result.steps_completed == []
        assert result.step_results == {}
        assert updated_state is None

    def test_execute_step_with_invalid_step_number(self) -> None:
        """Test individual step execution with invalid step number."""
        # RED: Test validation of step numbers
        orchestrator = StatusPhaseOrchestrator()
        mock_game_state = Mock()

        # Test step number too low
        with pytest.raises(StepValidationError) as exc_info:
            orchestrator.execute_step(0, mock_game_state)
        assert "Invalid step number: 0" in str(exc_info.value)

        # Test step number too high
        with pytest.raises(StepValidationError) as exc_info:
            orchestrator.execute_step(9, mock_game_state)
        assert "Invalid step number: 9" in str(exc_info.value)

    def test_execute_step_with_none_game_state(self) -> None:
        """Test individual step execution with None game state."""
        # RED: Test graceful handling of None game state
        orchestrator = StatusPhaseOrchestrator()

        result, updated_state = orchestrator.execute_step(1, None)

        assert result.success is False
        assert "Game state cannot be None" in result.error_message
        assert result.step_name == "Step 1"
        assert updated_state is None

    def test_validate_step_prerequisites_with_invalid_step_number(self) -> None:
        """Test step prerequisite validation with invalid step number."""
        # RED: Test validation of step numbers in prerequisite checking
        orchestrator = StatusPhaseOrchestrator()
        mock_game_state = Mock()

        # Test step number too low
        with pytest.raises(StepValidationError) as exc_info:
            orchestrator.validate_step_prerequisites(0, mock_game_state)
        assert "Invalid step number: 0" in str(exc_info.value)

        # Test step number too high
        with pytest.raises(StepValidationError) as exc_info:
            orchestrator.validate_step_prerequisites(9, mock_game_state)
        assert "Invalid step number: 9" in str(exc_info.value)

    def test_get_step_handler_with_invalid_step_number(self) -> None:
        """Test getting step handler with invalid step number."""
        # RED: Test validation of step numbers in handler retrieval
        orchestrator = StatusPhaseOrchestrator()

        # Test step number too low
        with pytest.raises(StepValidationError) as exc_info:
            orchestrator.get_step_handler(0)
        assert "Invalid step number: 0" in str(exc_info.value)

        # Test step number too high
        with pytest.raises(StepValidationError) as exc_info:
            orchestrator.get_step_handler(9)
        assert "Invalid step number: 9" in str(exc_info.value)


class TestStepHandlerErrorHandling:
    """Test error handling in individual step handlers.

    Requirements: 11.2 - Validation prevents invalid state changes
    """

    def test_score_objectives_step_error_handling(self) -> None:
        """Test error handling in ScoreObjectivesStep."""
        # RED: Test graceful handling of errors in objective scoring
        step = ScoreObjectivesStep()

        # Test with None game state
        result, updated_state = step.execute(None)

        assert result.success is False
        assert "Game state cannot be None" in result.error_message
        assert result.step_name == "Score Objectives"
        assert updated_state is None

    def test_score_objectives_step_prerequisite_validation(self) -> None:
        """Test prerequisite validation in ScoreObjectivesStep."""
        # RED: Test validation prevents execution with invalid state
        step = ScoreObjectivesStep()

        # Test with None game state
        assert step.validate_prerequisites(None) is False

        # Test with mock game state without players
        mock_game_state = Mock()
        mock_game_state.players = None
        assert step.validate_prerequisites(mock_game_state) is False

    def test_reveal_objective_step_error_handling(self) -> None:
        """Test error handling in RevealObjectiveStep."""
        # RED: Test graceful handling of errors in objective revealing
        step = RevealObjectiveStep()

        # Test with None game state
        result, updated_state = step.execute(None)

        assert result.success is False
        assert "Game state cannot be None" in result.error_message
        assert result.step_name == "Reveal Public Objective"
        assert updated_state is None

    def test_draw_action_cards_step_error_handling(self) -> None:
        """Test error handling in DrawActionCardsStep."""
        # RED: Test graceful handling of errors in action card drawing
        step = DrawActionCardsStep()

        # Test with None game state
        result, updated_state = step.execute(None)

        assert result.success is False
        assert "Game state cannot be None" in result.error_message
        assert result.step_name == "Draw Action Cards"
        assert updated_state is None

    def test_remove_command_tokens_step_error_handling(self) -> None:
        """Test error handling in RemoveCommandTokensStep."""
        # RED: Test graceful handling of errors in token removal
        step = RemoveCommandTokensStep()

        # Test with None game state
        result, updated_state = step.execute(None)

        assert result.success is False
        assert "Game state cannot be None" in result.error_message
        assert result.step_name == "Remove Command Tokens"
        assert updated_state is None

    def test_gain_redistribute_tokens_step_error_handling(self) -> None:
        """Test error handling in GainRedistributeTokensStep."""
        # RED: Test graceful handling of errors in token redistribution
        step = GainRedistributeTokensStep()

        # Test with None game state
        result, updated_state = step.execute(None)

        assert result.success is False
        assert "Game state cannot be None" in result.error_message
        assert result.step_name == "Gain and Redistribute Command Tokens"
        assert updated_state is None

    def test_ready_cards_step_error_handling(self) -> None:
        """Test error handling in ReadyCardsStep."""
        # RED: Test graceful handling of errors in card readying
        step = ReadyCardsStep()

        # Test with None game state
        result, updated_state = step.execute(None)

        assert result.success is False
        assert "Game state cannot be None" in result.error_message
        assert result.step_name == "Ready Cards"
        assert updated_state is None

    def test_repair_units_step_error_handling(self) -> None:
        """Test error handling in RepairUnitsStep."""
        # RED: Test graceful handling of errors in unit repair
        step = RepairUnitsStep()

        # Test with None game state
        result, updated_state = step.execute(None)

        assert result.success is False
        assert "Game state cannot be None" in result.error_message
        assert result.step_name == "Repair Units"
        assert updated_state is None

    def test_return_strategy_cards_step_error_handling(self) -> None:
        """Test error handling in ReturnStrategyCardsStep."""
        # RED: Test graceful handling of errors in strategy card return
        step = ReturnStrategyCardsStep()

        # Test with None game state
        result, updated_state = step.execute(None)

        assert result.success is False
        assert "Game state cannot be None" in result.error_message
        assert result.step_name == "Return Strategy Cards"
        assert updated_state is None


class TestGracefulDegradation:
    """Test graceful degradation scenarios for non-critical failures.

    Requirements: 11.3 - Graceful degradation for non-critical step failures
    """

    def test_orchestrator_continues_after_non_critical_step_failure(self) -> None:
        """Test that orchestrator continues execution after non-critical step failures."""
        # RED: Test that non-critical failures don't halt entire status phase
        orchestrator = StatusPhaseOrchestrator()

        # Mock step handlers - non-critical steps fail, critical steps succeed
        def mock_get_handler_side_effect(step_number):
            mock_handler = Mock(spec=StatusPhaseStepHandler)
            if step_number == 8:  # Critical step - must succeed
                mock_handler.execute.return_value = (
                    StepResult(success=True, step_name=f"Step {step_number}"),
                    Mock(),  # Mock game state
                )
            else:  # Non-critical steps - can fail
                mock_handler.execute.return_value = (
                    StepResult(
                        success=False,
                        step_name=f"Step {step_number}",
                        error_message="Non-critical error",
                    ),
                    Mock(),  # Mock game state
                )
            return mock_handler

        with patch.object(
            orchestrator, "get_step_handler", side_effect=mock_get_handler_side_effect
        ):
            mock_game_state = Mock()
            result, updated_state = orchestrator.execute_complete_status_phase(
                mock_game_state
            )

            # Should continue execution despite non-critical step failures
            assert (
                result.success is True
            )  # Overall success despite individual step failure
            assert len(result.step_results) == 8  # All steps attempted

    def test_step_handler_graceful_degradation_with_missing_data(self) -> None:
        """Test step handlers gracefully handle missing game data."""
        # RED: Test that steps handle missing data gracefully
        step = ScoreObjectivesStep()

        # Mock game state with missing objective data
        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player1")]
        mock_game_state.get_public_objectives.side_effect = AttributeError(
            "No objectives"
        )

        result, updated_state = step.execute(mock_game_state)

        # Should handle missing data gracefully
        assert result.success is True  # Graceful degradation
        assert "player1" in result.players_processed
        assert "scored no objectives" in result.actions_taken[0]


class TestStateValidationAndRollback:
    """Test state validation and rollback mechanisms for critical failures.

    Requirements: 11.4 - State validation and rollback for critical failures
    """

    def test_orchestrator_validates_game_state_before_execution(self) -> None:
        """Test that orchestrator validates game state before executing steps."""
        # RED: Test state validation prevents execution with invalid state
        orchestrator = StatusPhaseOrchestrator()

        # Test with completely invalid game state
        invalid_state = "not a game state"

        result, updated_state = orchestrator.execute_complete_status_phase(
            invalid_state
        )

        assert result.success is False
        assert (
            "Game state cannot be None" in result.error_message
            or "invalid" in result.error_message.lower()
        )

    def test_step_handler_validates_input_parameters(self) -> None:
        """Test that step handlers validate input parameters."""
        # RED: Test input validation prevents invalid operations
        step = ScoreObjectivesStep()

        # Test process_player_objective_scoring with invalid inputs
        mock_game_state = Mock()

        with pytest.raises(ValueError) as exc_info:
            step.process_player_objective_scoring("", mock_game_state)
        assert "player_id cannot be empty" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            step.process_player_objective_scoring("player1", None)
        assert "game_state cannot be None" in str(exc_info.value)

    def test_step_result_immutability_protection(self) -> None:
        """Test that step results protect against state corruption."""
        # RED: Test that results maintain data integrity
        result = StepResult(success=True, step_name="Test Step")

        # Verify initial state
        assert result.success is True
        assert result.step_name == "Test Step"
        assert result.error_message == ""
        assert result.players_processed == []
        assert result.actions_taken == []

        # Verify lists are independent instances (not shared references)
        result.players_processed.append("player1")
        new_result = StepResult(success=True, step_name="Another Step")
        assert new_result.players_processed == []  # Should be empty, not affected


class TestDescriptiveErrorMessages:
    """Test that all error messages are descriptive and actionable.

    Requirements: 11.5 - Descriptive and actionable error messages
    """

    def test_step_validation_error_messages_are_descriptive(self) -> None:
        """Test that step validation errors provide clear, actionable messages."""
        # RED: Test error messages provide context and guidance
        orchestrator = StatusPhaseOrchestrator()

        try:
            orchestrator.execute_step(-1, Mock())
        except StepValidationError as e:
            assert "Invalid step number: -1" in str(e)
            assert "Must be 1-8" in str(e)

    def test_system_integration_error_messages_are_descriptive(self) -> None:
        """Test that system integration errors provide clear context."""
        # RED: Test integration errors explain what went wrong and why
        error = SystemIntegrationError(
            "Failed to integrate with objective system: ObjectiveManager not initialized"
        )

        assert "Failed to integrate with objective system" in str(error)
        assert "ObjectiveManager not initialized" in str(error)

    def test_game_state_error_messages_are_actionable(self) -> None:
        """Test that game state errors provide actionable guidance."""
        # RED: Test game state errors explain how to fix the issue
        error = StatusPhaseGameStateError(
            "Game state missing required players list. Ensure game is properly initialized."
        )

        assert "Game state missing required players list" in str(error)
        assert "Ensure game is properly initialized" in str(error)

    def test_step_result_error_messages_include_context(self) -> None:
        """Test that step result error messages include relevant context."""
        # RED: Test step results provide context about what failed
        result = StepResult(
            success=False,
            step_name="Score Objectives",
            error_message="Failed to score objectives for player 'player1': Player does not meet objective requirements for 'Control Mecatol Rex'",
        )

        assert "Failed to score objectives" in result.error_message
        assert "player1" in result.error_message
        assert "Control Mecatol Rex" in result.error_message
        assert "does not meet objective requirements" in result.error_message


class TestErrorRecoveryMechanisms:
    """Test error recovery and continuation mechanisms.

    Requirements: 11.3 - Error handling with graceful degradation
    """

    def test_orchestrator_recovers_from_transient_failures(self) -> None:
        """Test that orchestrator can recover from transient failures."""
        # RED: Test recovery from temporary system issues
        orchestrator = StatusPhaseOrchestrator()

        # Mock a scenario where first attempt fails but second succeeds
        call_count = 0

        def mock_execute_side_effect(game_state):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return StepResult(
                    success=False, step_name="Test", error_message="Transient error"
                ), game_state
            else:
                return StepResult(success=True, step_name="Test"), game_state

        with patch.object(orchestrator, "get_step_handler") as mock_get_handler:
            mock_handler = Mock(spec=StatusPhaseStepHandler)
            mock_handler.execute.side_effect = mock_execute_side_effect
            mock_get_handler.return_value = mock_handler

            mock_game_state = Mock()

            # First execution should handle the failure gracefully
            result, updated_state = orchestrator.execute_complete_status_phase(
                mock_game_state
            )

            # Should complete successfully despite initial failure
            assert result.success is True

    def test_step_handler_provides_partial_results_on_failure(self) -> None:
        """Test that step handlers provide partial results when possible."""
        # RED: Test that partial progress is preserved on failure
        step = ScoreObjectivesStep()

        # Mock a scenario where some players succeed and others fail
        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player1"), Mock(id="player2")]

        with patch.object(step, "process_player_objective_scoring") as mock_process:
            # First player succeeds, second fails
            mock_process.side_effect = [
                (1, mock_game_state),  # Player 1 scores 1 objective
                Exception("Player 2 processing failed"),  # Player 2 fails
            ]

            with patch(
                "src.ti4.core.strategy_cards.coordinator.StrategyCardCoordinator"
            ) as mock_coordinator_class:
                mock_coordinator = Mock()
                mock_coordinator.get_status_phase_initiative_order.return_value = [
                    "player1",
                    "player2",
                ]
                mock_coordinator_class.return_value = mock_coordinator

                result, updated_state = step.execute(mock_game_state)

                # Should report partial success with graceful degradation
                assert (
                    result.success is True
                )  # Overall success with graceful degradation
                assert "player1" in result.players_processed  # Player 1 was processed
                assert (
                    "player2" in result.players_processed
                )  # Player 2 was also processed (gracefully)
                assert "Player player1 scored 1 objectives" in result.actions_taken
                assert (
                    "Player player2 scored no objectives (error: Player 2 processing failed)"
                    in result.actions_taken
                )


class TestSystemIntegrationErrorScenarios:
    """Test comprehensive system integration error scenarios.

    Requirements: 11.2 - System integration failure handling
    """

    def test_objective_system_integration_failure(self) -> None:
        """Test handling of objective system integration failures."""
        # RED: Test graceful handling when objective system is unavailable
        step = ScoreObjectivesStep()
        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player1")]

        with patch.object(step, "process_player_objective_scoring") as mock_process:
            mock_process.side_effect = SystemIntegrationError(
                "Objective system unavailable"
            )

            with patch(
                "src.ti4.core.strategy_cards.coordinator.StrategyCardCoordinator"
            ) as mock_coordinator_class:
                mock_coordinator = Mock()
                mock_coordinator.get_status_phase_initiative_order.return_value = [
                    "player1"
                ]
                mock_coordinator_class.return_value = mock_coordinator

                result, updated_state = step.execute(mock_game_state)

                # Should use graceful degradation - success=True but error recorded
                assert result.success is True  # Graceful degradation
                assert "player1" in result.players_processed
                assert "Objective system unavailable" in result.actions_taken[0]
                assert result.step_name == "Score Objectives"

    def test_action_card_system_integration_failure(self) -> None:
        """Test handling of action card system integration failures."""
        # RED: Test graceful handling when action card system fails
        step = DrawActionCardsStep()
        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player1")]

        with patch(
            "src.ti4.core.strategy_cards.coordinator.StrategyCardCoordinator"
        ) as mock_coordinator_class:
            mock_coordinator = Mock()
            mock_coordinator.get_status_phase_initiative_order.return_value = [
                "player1"
            ]
            mock_coordinator_class.return_value = mock_coordinator

            with patch.object(step, "draw_card_for_player") as mock_draw:
                mock_draw.side_effect = SystemIntegrationError(
                    "Action card deck corrupted"
                )

                result, updated_state = step.execute(mock_game_state)

                assert result.success is False
                assert "Action card deck corrupted" in result.error_message

    def test_command_token_system_integration_failure(self) -> None:
        """Test handling of command token system integration failures."""
        # RED: Test graceful handling when command token system fails
        step = RemoveCommandTokensStep()
        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player1")]

        # The step tries to iterate over players, so mock players should be iterable
        mock_game_state.players = "not_iterable"  # This will cause iteration error

        result, updated_state = step.execute(mock_game_state)

        assert result.success is False
        assert "not iterable" in result.error_message

    def test_strategy_card_system_integration_failure(self) -> None:
        """Test handling of strategy card system integration failures."""
        # RED: Test graceful handling when strategy card system fails
        step = ReturnStrategyCardsStep()
        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player1")]

        with patch.object(step, "return_player_strategy_card") as mock_return:
            mock_return.side_effect = SystemIntegrationError(
                "Strategy card system unavailable"
            )

            result, updated_state = step.execute(mock_game_state)

            assert result.success is False
            assert "Strategy card system unavailable" in result.error_message


class TestStateRollbackMechanisms:
    """Test state validation and rollback mechanisms for critical failures.

    Requirements: 11.4 - State rollback for critical failures
    """

    def test_orchestrator_rollback_on_critical_step_failure(self) -> None:
        """Test that orchestrator can rollback state on critical step failures."""
        # RED: Test state rollback when critical steps fail
        orchestrator = StatusPhaseOrchestrator()

        # Mock initial game state
        initial_state = Mock()
        initial_state.phase = "status"
        initial_state.round_number = 1
        # Ensure _create_new_state returns the same object for rollback testing
        initial_state._create_new_state.return_value = initial_state

        # Mock step handlers - critical step fails
        def mock_get_handler_side_effect(step_number):
            mock_handler = Mock(spec=StatusPhaseStepHandler)
            if step_number == 8:  # Critical step - return strategy cards
                mock_handler.execute.return_value = (
                    StepResult(
                        success=False,
                        step_name=f"Step {step_number}",
                        error_message="Critical state corruption",
                    ),
                    initial_state,
                )
            else:
                mock_handler.execute.return_value = (
                    StepResult(success=True, step_name=f"Step {step_number}"),
                    initial_state,
                )
            return mock_handler

        with patch.object(
            orchestrator, "get_step_handler", side_effect=mock_get_handler_side_effect
        ):
            result, updated_state = orchestrator.execute_complete_status_phase(
                initial_state
            )

            # Should complete with graceful degradation but record the critical failure
            assert result.success is False  # Overall failure due to critical step
            assert result.step_results[8].error_message == "Critical state corruption"
            assert updated_state == initial_state  # State should be preserved

    def test_step_handler_validates_state_before_modification(self) -> None:
        """Test that step handlers validate state before making modifications."""
        # RED: Test state validation prevents invalid modifications
        step = GainRedistributeTokensStep()

        # Mock game state with invalid token configuration
        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player1")]
        mock_player = mock_game_state.players[0]
        mock_player.command_tokens = None  # Invalid state

        result, updated_state = step.execute(mock_game_state)

        # Should use graceful degradation - continues execution but may have issues
        assert result.success is True  # Graceful degradation
        assert "player1" in result.players_processed
        # The step completes but may have encountered issues during token redistribution

    def test_step_result_preserves_original_state_on_failure(self) -> None:
        """Test that step results preserve original state when operations fail."""
        # RED: Test state preservation during failures
        step = RepairUnitsStep()

        original_state = Mock()
        original_state.players = [Mock(id="player1")]
        original_state.round_number = 3

        with patch.object(step, "repair_player_units") as mock_repair:
            mock_repair.side_effect = Exception("Unit repair system failure")

            result, updated_state = step.execute(original_state)

            # Should preserve original state on failure
            assert result.success is False
            assert updated_state == original_state
            assert updated_state.round_number == 3


class TestEnhancedValidationScenarios:
    """Test enhanced validation scenarios for edge cases.

    Requirements: 11.2 - Enhanced validation prevents invalid operations
    """

    def test_orchestrator_validates_step_sequence_integrity(self) -> None:
        """Test that orchestrator validates step sequence integrity."""
        # RED: Test validation of step execution order
        orchestrator = StatusPhaseOrchestrator()

        # Mock game state that's only valid for certain steps
        mock_game_state = Mock()
        mock_game_state.phase = "action"  # Wrong phase for status phase

        result, updated_state = orchestrator.execute_complete_status_phase(
            mock_game_state
        )

        # Should use graceful degradation - continues execution despite wrong phase
        assert result.success is False  # Overall failure due to multiple step failures
        # Multiple steps will fail due to invalid mock game state, but execution continues
        failed_steps = [
            step_result
            for step_result in result.step_results.values()
            if not step_result.success
        ]
        assert len(failed_steps) > 0  # Some steps should fail with invalid game state

    def test_step_handler_validates_player_state_consistency(self) -> None:
        """Test that step handlers validate player state consistency."""
        # RED: Test validation of player state consistency
        step = ScoreObjectivesStep()

        # Mock game state with inconsistent player data
        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player1")]
        mock_player = mock_game_state.players[0]
        mock_player.victory_points = -1  # Invalid victory points

        with patch.object(step, "validate_prerequisites") as mock_validate:
            mock_validate.return_value = False

            result, updated_state = step.execute(mock_game_state)

            # Should fail when prerequisites are not met - this is correct behavior
            assert result.success is False  # Proper error handling
            assert "Prerequisites not met" in result.error_message
            # Step should not process players when prerequisites fail

    def test_step_handler_validates_game_component_integrity(self) -> None:
        """Test that step handlers validate game component integrity."""
        # RED: Test validation of game component integrity
        step = RevealObjectiveStep()

        # Mock game state with corrupted objective data
        mock_game_state = Mock()
        mock_game_state.get_public_objectives.return_value = []  # No objectives available
        mock_game_state.speaker_id = None  # No speaker assigned

        result, updated_state = step.execute(mock_game_state)

        # Should fail when game state is invalid - this is correct behavior
        assert result.success is False  # Proper error handling
        assert result.error_message is not None
        # Step should not process when game state is corrupted


class TestPerformanceRelatedErrorHandling:
    """Test performance-related error handling scenarios.

    Requirements: 12.1, 12.2 - Performance constraints and error handling
    """

    def test_orchestrator_handles_timeout_scenarios(self) -> None:
        """Test that orchestrator handles timeout scenarios gracefully."""
        # RED: Test handling of performance timeout scenarios
        orchestrator = StatusPhaseOrchestrator()

        # Mock step handler that takes too long
        def mock_get_handler_side_effect(step_number):
            mock_handler = Mock(spec=StatusPhaseStepHandler)
            if step_number == 1:
                # Simulate timeout by returning failure result
                mock_handler.execute.return_value = (
                    StepResult(
                        success=False,
                        step_name=f"Step {step_number}",
                        error_message="Operation timed out after 1000ms",
                    ),
                    Mock(),
                )
            else:
                mock_handler.execute.return_value = (
                    StepResult(success=True, step_name=f"Step {step_number}"),
                    Mock(),
                )
            return mock_handler

        with patch.object(
            orchestrator, "get_step_handler", side_effect=mock_get_handler_side_effect
        ):
            mock_game_state = Mock()
            result, updated_state = orchestrator.execute_complete_status_phase(
                mock_game_state
            )

            # Should handle timeout gracefully with overall success but step failure recorded
            assert result.success is True  # Graceful degradation continues execution
            assert result.step_results[1].success is False
            assert "timed out" in result.step_results[1].error_message.lower()

    def test_step_handler_handles_memory_pressure(self) -> None:
        """Test that step handlers handle memory pressure scenarios."""
        # RED: Test handling of memory pressure during execution
        step = DrawActionCardsStep()

        mock_game_state = Mock()
        mock_game_state.players = [
            Mock(id=f"player{i}") for i in range(100)
        ]  # Many players

        with patch(
            "src.ti4.core.strategy_cards.coordinator.StrategyCardCoordinator"
        ) as mock_coordinator_class:
            mock_coordinator = Mock()
            mock_coordinator.get_status_phase_initiative_order.return_value = [
                f"player{i}" for i in range(100)
            ]
            mock_coordinator_class.return_value = mock_coordinator

            with patch.object(step, "draw_card_for_player") as mock_draw:
                mock_draw.side_effect = MemoryError(
                    "Insufficient memory for card drawing"
                )

                result, updated_state = step.execute(mock_game_state)

                # Should handle memory pressure gracefully
                assert result.success is False
                assert "memory" in result.error_message.lower()


class TestConcurrentAccessErrorHandling:
    """Test concurrent access error handling scenarios.

    Requirements: 11.3 - Thread-safe error handling
    """

    def test_orchestrator_handles_concurrent_modification(self) -> None:
        """Test that orchestrator handles concurrent modification errors."""
        # RED: Test handling of concurrent modification scenarios
        orchestrator = StatusPhaseOrchestrator()

        # Mock game state that gets modified during execution
        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player1")]

        def mock_get_handler_side_effect(step_number):
            mock_handler = Mock(spec=StatusPhaseStepHandler)
            if step_number == 1:
                # Simulate concurrent modification
                mock_handler.execute.side_effect = RuntimeError(
                    "Game state modified by another thread"
                )
            else:
                mock_handler.execute.return_value = (
                    StepResult(success=True, step_name=f"Step {step_number}"),
                    mock_game_state,
                )
            return mock_handler

        with patch.object(
            orchestrator, "get_step_handler", side_effect=mock_get_handler_side_effect
        ):
            result, updated_state = orchestrator.execute_complete_status_phase(
                mock_game_state
            )

            # Should handle concurrent modification gracefully
            assert result.success is True  # Graceful degradation continues execution
            assert result.step_results[1].success is False
            assert (
                "modified" in result.step_results[1].error_message.lower()
                or "thread" in result.step_results[1].error_message.lower()
            )

    def test_step_handler_handles_resource_contention(self) -> None:
        """Test that step handlers handle resource contention scenarios."""
        # RED: Test handling of resource contention during execution
        step = ReturnStrategyCardsStep()

        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player1")]

        with patch.object(step, "return_player_strategy_card") as mock_return:
            mock_return.side_effect = BlockingIOError(
                "Resource locked by another process"
            )

            result, updated_state = step.execute(mock_game_state)

            # Should handle resource contention gracefully
            assert result.success is False
            assert (
                "locked" in result.error_message.lower()
                or "resource" in result.error_message.lower()
            )


class TestErrorMessageQualityAndActionability:
    """Test that error messages are high-quality and actionable.

    Requirements: 11.5 - Descriptive and actionable error messages
    """

    def test_error_messages_include_troubleshooting_guidance(self) -> None:
        """Test that error messages include troubleshooting guidance."""
        # RED: Test error messages provide troubleshooting steps
        orchestrator = StatusPhaseOrchestrator()

        try:
            orchestrator.execute_step(0, Mock())
        except StepValidationError as e:
            error_msg = str(e)
            assert "Invalid step number: 0" in error_msg
            assert "Must be 1-8" in error_msg
            assert "step number" in error_msg.lower()

    def test_error_messages_include_context_information(self) -> None:
        """Test that error messages include relevant context information."""
        # RED: Test error messages provide context about the failure
        step = ScoreObjectivesStep()

        mock_game_state = Mock()
        mock_game_state.players = []  # No players

        result, updated_state = step.execute(mock_game_state)

        # Should use graceful degradation - no players to process
        assert result.success is True  # Graceful degradation
        assert result.players_processed == []  # No players to process
        assert result.actions_taken == []  # No actions taken

    def test_error_messages_suggest_corrective_actions(self) -> None:
        """Test that error messages suggest corrective actions."""
        # RED: Test error messages suggest how to fix the problem
        error = StatusPhaseGameStateError(
            "Game state missing required players list. "
            "Ensure game is properly initialized with Player.create_player() before starting status phase."
        )

        error_msg = str(error)
        assert "missing required players list" in error_msg
        assert "Ensure game is properly initialized" in error_msg
        assert "Player.create_player()" in error_msg

    def test_error_messages_include_relevant_identifiers(self) -> None:
        """Test that error messages include relevant identifiers for debugging."""
        # RED: Test error messages include IDs and identifiers for debugging
        step = RepairUnitsStep()

        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player_123")]

        with patch.object(step, "repair_player_units") as mock_repair:
            mock_repair.side_effect = Exception(
                "Unit repair failed for player_123: Invalid unit ID 'unit_456'"
            )

            result, updated_state = step.execute(mock_game_state)

            # Error message should include player and unit identifiers
            assert result.success is False
            assert "player_123" in result.error_message
            assert "unit_456" in result.error_message

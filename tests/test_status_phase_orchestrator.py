"""Tests for StatusPhaseOrchestrator step coordination.

This module tests the StatusPhaseOrchestrator class that coordinates
the execution of all 8 status phase steps in proper sequence.

LRR References:
- Rule 81: Status Phase - Complete 8-step sequence
- Requirements: 1.1, 1.2, 1.3, 11.3, 12.3
"""

import time
from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

if TYPE_CHECKING:
    pass


class TestStatusPhaseOrchestrator:
    """Test StatusPhaseOrchestrator class.

    Tests the core functionality of the StatusPhaseOrchestrator including:
    - Complete status phase execution sequence
    - Individual step execution and validation
    - Error handling and graceful degradation scenarios

    Requirements: 1.1, 12.3
    """

    def test_orchestrator_creation(self) -> None:
        """Test creating StatusPhaseOrchestrator instance.

        Verifies that the orchestrator can be instantiated successfully.
        """
        from src.ti4.core.status_phase import StatusPhaseOrchestrator

        orchestrator = StatusPhaseOrchestrator()
        assert orchestrator is not None

    def test_execute_complete_status_phase_success(self) -> None:
        """Test successful execution of complete status phase.

        Verifies that all 8 status phase steps execute successfully
        and return proper results.

        Requirements: 1.1 - Complete status phase orchestration
        """
        from src.ti4.core.status_phase import StatusPhaseOrchestrator, StatusPhaseResult

        # Arrange: Create mock game state with proper structure
        mock_game_state = Mock()
        mock_game_state.players = []
        mock_game_state.systems = {}

        # Act: Execute complete status phase
        orchestrator = StatusPhaseOrchestrator()
        result, updated_state = orchestrator.execute_complete_status_phase(
            mock_game_state
        )

        # Assert: Should return StatusPhaseResult and updated game state
        assert isinstance(result, StatusPhaseResult)
        assert result.success is True
        assert len(result.steps_completed) == 8  # All 8 steps should complete
        assert result.next_phase in ["agenda", "strategy"]  # Valid next phases
        assert updated_state is not None

    def test_execute_complete_status_phase_returns_updated_game_state(self) -> None:
        """Test that complete status phase returns updated game state.

        Verifies that the orchestrator returns both a result and
        an updated game state after execution.

        Requirements: 1.1 - Complete status phase orchestration
        """
        from src.ti4.core.status_phase import StatusPhaseOrchestrator

        # Arrange: Create mock game state
        mock_game_state = Mock()

        # Act: Execute complete status phase
        orchestrator = StatusPhaseOrchestrator()
        result, updated_state = orchestrator.execute_complete_status_phase(
            mock_game_state
        )

        # Assert: Should return both result and updated game state
        assert result is not None
        assert updated_state is not None

    def test_execute_step_valid_step_number(self) -> None:
        """Test executing a valid individual step.

        Verifies that individual steps can be executed successfully
        with valid step numbers (1-8).

        Requirements: 1.2 - Individual step execution
        """
        from src.ti4.core.status_phase import StatusPhaseOrchestrator, StepResult

        # Arrange: Create mock game state with proper structure
        mock_game_state = Mock()
        mock_game_state.players = []
        mock_game_state.systems = {}

        # Act: Execute individual step
        orchestrator = StatusPhaseOrchestrator()
        result, updated_state = orchestrator.execute_step(1, mock_game_state)

        # Assert: Should return StepResult and updated game state
        assert isinstance(result, StepResult)
        assert result.success is True
        assert result.step_name != ""
        assert updated_state is not None

    def test_execute_step_invalid_step_number(self) -> None:
        """Test executing an invalid step number raises error.

        Verifies that invalid step numbers (< 1 or > 8) raise
        appropriate validation errors.

        Requirements: 1.2 - Individual step execution validation
        """
        from src.ti4.core.status_phase import (
            StatusPhaseOrchestrator,
            StepValidationError,
        )

        # Arrange: Create mock game state
        mock_game_state = Mock()
        orchestrator = StatusPhaseOrchestrator()

        # Act & Assert: Invalid step numbers should raise StepValidationError
        with pytest.raises(StepValidationError, match="Invalid step number: 0"):
            orchestrator.execute_step(0, mock_game_state)

        with pytest.raises(StepValidationError, match="Invalid step number: 9"):
            orchestrator.execute_step(9, mock_game_state)

    def test_execute_step_returns_updated_game_state(self) -> None:
        """Test that individual step execution returns updated game state.

        Verifies that step execution returns both result and updated state.

        Requirements: 1.2 - Individual step execution
        """
        from src.ti4.core.status_phase import StatusPhaseOrchestrator

        # Arrange: Create mock game state
        mock_game_state = Mock()

        # Act: Execute individual step
        orchestrator = StatusPhaseOrchestrator()
        result, updated_state = orchestrator.execute_step(1, mock_game_state)

        # Assert: Should return both result and updated game state
        assert result is not None
        assert updated_state is not None

    def test_validate_step_prerequisites_valid_step(self) -> None:
        """Test validating prerequisites for a valid step.

        Verifies that prerequisite validation works for valid steps.

        Requirements: 1.3 - Step validation
        """
        from src.ti4.core.status_phase import StatusPhaseOrchestrator

        # Arrange: Create mock game state
        mock_game_state = Mock()

        # Act: Validate step prerequisites
        orchestrator = StatusPhaseOrchestrator()
        is_valid = orchestrator.validate_step_prerequisites(1, mock_game_state)

        # Assert: Should return boolean
        assert isinstance(is_valid, bool)

    def test_validate_step_prerequisites_invalid_step(self) -> None:
        """Test validating prerequisites for invalid step number.

        Verifies that invalid step numbers raise validation errors.

        Requirements: 1.3 - Step validation
        """
        from src.ti4.core.status_phase import (
            StatusPhaseOrchestrator,
            StepValidationError,
        )

        # Arrange: Create mock game state
        mock_game_state = Mock()
        orchestrator = StatusPhaseOrchestrator()

        # Act & Assert: Invalid step numbers should raise StepValidationError
        with pytest.raises(StepValidationError, match="Invalid step number: 0"):
            orchestrator.validate_step_prerequisites(0, mock_game_state)

    def test_get_step_handler_valid_step(self) -> None:
        """Test getting step handler for valid step number.

        Verifies that step handlers can be retrieved for valid steps.

        Requirements: 1.2 - Individual step execution
        """
        from src.ti4.core.status_phase import (
            StatusPhaseOrchestrator,
            StatusPhaseStepHandler,
        )

        # Arrange & Act: Get step handler
        orchestrator = StatusPhaseOrchestrator()
        handler = orchestrator.get_step_handler(1)

        # Assert: Should return StatusPhaseStepHandler instance
        assert isinstance(handler, StatusPhaseStepHandler)

    def test_get_step_handler_invalid_step(self) -> None:
        """Test getting step handler for invalid step number raises error.

        Verifies that invalid step numbers raise validation errors.

        Requirements: 1.2 - Individual step execution validation
        """
        from src.ti4.core.status_phase import (
            StatusPhaseOrchestrator,
            StepValidationError,
        )

        # Arrange: Create orchestrator
        orchestrator = StatusPhaseOrchestrator()

        # Act & Assert: Invalid step numbers should raise StepValidationError
        with pytest.raises(StepValidationError, match="Invalid step number: 0"):
            orchestrator.get_step_handler(0)

        with pytest.raises(StepValidationError, match="Invalid step number: 9"):
            orchestrator.get_step_handler(9)

    def test_execute_complete_status_phase_step_sequence(self) -> None:
        """Test that complete status phase executes steps in correct sequence.

        Verifies that all 8 steps are executed in the proper LRR order
        and that each step completes successfully.

        Requirements: 1.1 - Complete status phase orchestration
        """
        from src.ti4.core.status_phase import StatusPhaseOrchestrator

        # Arrange: Create mock game state with proper structure
        mock_game_state = Mock()
        mock_game_state.players = []
        mock_game_state.systems = {}
        mock_game_state.exhausted_strategy_cards = []
        mock_game_state.player_planets = {}
        mock_game_state.player_technology_cards = {}
        mock_game_state.ready_strategy_card = Mock(return_value=mock_game_state)
        mock_game_state._create_new_state = Mock(return_value=mock_game_state)

        # Act: Execute complete status phase
        orchestrator = StatusPhaseOrchestrator()
        result, _ = orchestrator.execute_complete_status_phase(mock_game_state)

        # Assert: Should have executed all 8 steps in order
        assert len(result.step_results) == 8
        for step_num in range(1, 9):
            assert step_num in result.step_results
            assert result.step_results[step_num].success is True

    def test_execute_complete_status_phase_error_handling(self) -> None:
        """Test error handling during complete status phase execution.

        Verifies that the orchestrator handles errors gracefully
        and provides meaningful error messages.

        Requirements: 11.3 - Error handling and graceful degradation
        """
        from src.ti4.core.status_phase import StatusPhaseOrchestrator

        # Arrange: Create invalid game state that will cause an error
        invalid_game_state = None

        # Act: Execute complete status phase with invalid state
        orchestrator = StatusPhaseOrchestrator()
        result, updated_state = orchestrator.execute_complete_status_phase(
            invalid_game_state
        )

        # Assert: Should handle error gracefully
        assert result.success is False
        assert result.error_message != ""
        assert result.error_message == "Game state cannot be None"
        assert updated_state is None  # Should return the same None state

    def test_execute_step_error_handling(self) -> None:
        """Test error handling during individual step execution.

        Verifies that individual step execution handles errors gracefully
        and provides meaningful error messages.

        Requirements: 11.3 - Error handling and graceful degradation
        """
        from src.ti4.core.status_phase import StatusPhaseOrchestrator

        # Arrange: Create invalid game state that will cause an error
        invalid_game_state = None

        # Act: Execute individual step with invalid state
        orchestrator = StatusPhaseOrchestrator()
        result, updated_state = orchestrator.execute_step(1, invalid_game_state)

        # Assert: Should handle error gracefully
        assert result.success is False
        assert result.error_message != ""
        assert result.error_message == "Game state cannot be None"
        assert updated_state is None  # Should return the same None state

    def test_execute_complete_status_phase_performance(self) -> None:
        """Test that complete status phase execution meets performance requirements.

        Verifies that the complete status phase executes within the
        required performance threshold of <500ms.

        Requirements: 12.1 - Performance requirements
        """
        from src.ti4.core.status_phase import StatusPhaseOrchestrator

        # Arrange: Create mock game state
        mock_game_state = Mock()

        # Act: Execute complete status phase
        orchestrator = StatusPhaseOrchestrator()
        result, updated_state = orchestrator.execute_complete_status_phase(
            mock_game_state
        )

        # Assert: Should complete within performance requirements (<500ms)
        assert result.total_execution_time < 0.5
        assert updated_state is not None

    def test_execute_step_performance(self) -> None:
        """Test that individual step execution meets performance requirements.

        Verifies that individual steps execute within the
        required performance threshold of <100ms.

        Requirements: 12.2 - Individual step performance
        """
        from src.ti4.core.status_phase import StatusPhaseOrchestrator

        # Arrange: Create mock game state
        mock_game_state = Mock()
        orchestrator = StatusPhaseOrchestrator()

        # Act: Measure execution time for individual step
        start_time = time.perf_counter()
        result, updated_state = orchestrator.execute_step(1, mock_game_state)
        execution_time = time.perf_counter() - start_time

        # Assert: Should complete within performance requirements (<100ms)
        assert execution_time < 0.1
        assert updated_state is not None


class TestStatusPhaseOrchestratorIntegration:
    """Test StatusPhaseOrchestrator integration scenarios.

    Tests integration between the orchestrator and step handlers,
    including graceful degradation scenarios.

    Requirements: 11.3 - Error handling and graceful degradation
    """

    def test_orchestrator_with_step_handlers(self) -> None:
        """Test orchestrator integration with actual step handlers.

        Verifies that the orchestrator can successfully work with
        all step handlers and that they implement the required interface.

        Requirements: 1.2 - Individual step execution
        """
        from src.ti4.core.status_phase import StatusPhaseOrchestrator

        # Arrange: Create orchestrator
        orchestrator = StatusPhaseOrchestrator()

        # Act & Assert: Test that orchestrator can work with step handlers
        for step_num in range(1, 9):
            handler = orchestrator.get_step_handler(step_num)
            assert handler is not None
            assert hasattr(handler, "execute")
            assert hasattr(handler, "validate_prerequisites")
            assert hasattr(handler, "get_step_name")

    def test_orchestrator_graceful_degradation(self) -> None:
        """Test orchestrator graceful degradation on step failures.

        Verifies that the orchestrator handles potential step failures
        gracefully without crashing the system.

        Requirements: 11.3 - Error handling and graceful degradation
        """
        from src.ti4.core.status_phase import StatusPhaseOrchestrator

        # Arrange: Create mock game state
        mock_game_state = Mock()
        orchestrator = StatusPhaseOrchestrator()

        # Act: Execute complete status phase (may have step failures)
        result, updated_state = orchestrator.execute_complete_status_phase(
            mock_game_state
        )

        # Assert: Should still return valid result and state
        assert result is not None
        assert updated_state is not None
        # May not be successful if steps fail, but should not crash
        assert isinstance(result.success, bool)

    def test_all_step_numbers_have_handlers(self) -> None:
        """Test that all 8 status phase steps have handlers.

        Verifies that handlers exist for all required status phase steps.

        Requirements: 1.1 - Complete status phase orchestration
        """
        from src.ti4.core.status_phase import StatusPhaseOrchestrator

        # Arrange: Create orchestrator
        orchestrator = StatusPhaseOrchestrator()

        # Expected step names based on actual implementation
        expected_step_names = {
            1: "Score Objectives",
            2: "Reveal Public Objective",
            3: "Draw Action Cards",
            4: "Remove Command Tokens",
            5: "Gain and Redistribute Command Tokens",
            6: "Ready Cards",
            7: "Repair Units",
            8: "Return Strategy Cards",
        }

        # Act & Assert: All step numbers 1-8 should have handlers
        for step_num in range(1, 9):
            handler = orchestrator.get_step_handler(step_num)
            assert handler is not None
            step_name = handler.get_step_name()
            assert step_name == expected_step_names[step_num]

    def test_step_handlers_implement_required_interface(self) -> None:
        """Test that step handlers implement the required interface.

        Verifies that all step handlers properly implement the
        StatusPhaseStepHandler interface.

        Requirements: 1.2 - Individual step execution
        """
        from src.ti4.core.status_phase import (
            StatusPhaseOrchestrator,
            StatusPhaseStepHandler,
        )

        # Arrange: Create orchestrator and mock game state
        orchestrator = StatusPhaseOrchestrator()
        mock_game_state = Mock()

        # Act & Assert: Test interface implementation for all handlers
        for step_num in range(1, 9):
            handler = orchestrator.get_step_handler(step_num)

            # Should be instance of StatusPhaseStepHandler
            assert isinstance(handler, StatusPhaseStepHandler)

            # Should implement all required methods
            assert callable(handler.execute)
            assert callable(handler.validate_prerequisites)
            assert callable(handler.get_step_name)

            # Methods should work without crashing
            step_name = handler.get_step_name()
            assert isinstance(step_name, str)
            assert step_name != ""

            is_valid = handler.validate_prerequisites(mock_game_state)
            assert isinstance(is_valid, bool)

            result, updated_state = handler.execute(mock_game_state)
            assert result is not None
            assert updated_state is not None

    def test_step_result_helper_methods(self) -> None:
        """Test StatusPhaseResult helper methods.

        Verifies that the StatusPhaseResult class provides
        useful helper methods for accessing step results.

        Requirements: 12.3 - Test coverage
        """
        from src.ti4.core.status_phase import StatusPhaseOrchestrator

        # Arrange: Create mock game state with proper structure
        mock_game_state = Mock()
        mock_game_state.players = []
        mock_game_state.systems = {}
        mock_game_state.exhausted_strategy_cards = []
        mock_game_state.player_planets = {}
        mock_game_state.player_technology_cards = {}
        mock_game_state.ready_strategy_card = Mock(return_value=mock_game_state)
        mock_game_state._create_new_state = Mock(return_value=mock_game_state)

        # Act: Execute complete status phase
        orchestrator = StatusPhaseOrchestrator()
        result, _ = orchestrator.execute_complete_status_phase(mock_game_state)

        # Assert: Test helper methods
        for step_num in range(1, 9):
            step_result = result.get_step_result(step_num)
            assert step_result is not None
            assert result.was_step_successful(step_num) is True

        # Test non-existent step
        assert result.get_step_result(99) is None
        assert result.was_step_successful(99) is False

    def test_step_validation_with_all_step_numbers(self) -> None:
        """Test step validation for all valid step numbers.

        Verifies that prerequisite validation works correctly
        for all 8 status phase steps.

        Requirements: 1.3 - Step validation
        """
        from src.ti4.core.status_phase import StatusPhaseOrchestrator

        # Arrange: Create mock game state and orchestrator
        mock_game_state = Mock()
        orchestrator = StatusPhaseOrchestrator()

        # Act & Assert: Test validation for all steps
        for step_num in range(1, 9):
            is_valid = orchestrator.validate_step_prerequisites(
                step_num, mock_game_state
            )
            assert isinstance(is_valid, bool)
            # With mock game state, should return True
            assert is_valid is True

    def test_orchestrator_with_none_game_state_validation(self) -> None:
        """Test orchestrator validation with None game state.

        Verifies that the orchestrator properly validates
        game state before processing.

        Requirements: 11.3 - Error handling and graceful degradation
        """
        from src.ti4.core.status_phase import StatusPhaseOrchestrator

        # Arrange: Create orchestrator with None game state
        orchestrator = StatusPhaseOrchestrator()

        # Act & Assert: Validation should handle None gracefully
        for step_num in range(1, 9):
            is_valid = orchestrator.validate_step_prerequisites(step_num, None)
            assert is_valid is False

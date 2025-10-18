"""Tests for status phase core infrastructure and data models.

This module tests the core infrastructure components for the complete
status phase implementation including data models, abstract base classes,
and error handling.

LRR References:
- Rule 81: Status Phase
- Requirements: 1.1, 11.1, 11.2, 12.4
"""

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from src.ti4.core.game_state import GameState


class TestStepResult:
    """Test StepResult data class."""

    def test_step_result_creation_with_minimal_fields(self) -> None:
        """Test creating StepResult with minimal required fields."""
        # RED: This will fail until we implement StepResult
        from src.ti4.core.status_phase import StepResult

        result = StepResult(success=True, step_name="Test Step")

        assert result.success is True
        assert result.step_name == "Test Step"
        assert result.error_message == ""
        assert result.players_processed == []
        assert result.actions_taken == []

    def test_step_result_creation_with_all_fields(self) -> None:
        """Test creating StepResult with all fields populated."""
        from src.ti4.core.status_phase import StepResult

        result = StepResult(
            success=False,
            step_name="Score Objectives",
            error_message="Player not found",
            players_processed=["player1", "player2"],
            actions_taken=["scored_public_objective", "scored_secret_objective"],
        )

        assert result.success is False
        assert result.step_name == "Score Objectives"
        assert result.error_message == "Player not found"
        assert result.players_processed == ["player1", "player2"]
        assert result.actions_taken == [
            "scored_public_objective",
            "scored_secret_objective",
        ]


class TestStatusPhaseResult:
    """Test StatusPhaseResult data class."""

    def test_status_phase_result_creation_with_minimal_fields(self) -> None:
        """Test creating StatusPhaseResult with minimal required fields."""
        # RED: This will fail until we implement StatusPhaseResult
        from src.ti4.core.status_phase import StatusPhaseResult

        result = StatusPhaseResult(
            success=True,
            steps_completed=["Step 1", "Step 2"],
            step_results={},
            total_execution_time=0.5,
            next_phase="agenda",
        )

        assert result.success is True
        assert result.steps_completed == ["Step 1", "Step 2"]
        assert result.step_results == {}
        assert result.total_execution_time == 0.5
        assert result.next_phase == "agenda"
        assert result.error_message == ""

    def test_status_phase_result_get_step_result_existing(self) -> None:
        """Test getting an existing step result."""
        from src.ti4.core.status_phase import StatusPhaseResult, StepResult

        step_result = StepResult(success=True, step_name="Test Step")
        result = StatusPhaseResult(
            success=True,
            steps_completed=["Step 1"],
            step_results={1: step_result},
            total_execution_time=0.5,
            next_phase="agenda",
        )

        retrieved = result.get_step_result(1)
        assert retrieved is step_result

    def test_status_phase_result_get_step_result_missing(self) -> None:
        """Test getting a non-existent step result returns None."""
        from src.ti4.core.status_phase import StatusPhaseResult

        result = StatusPhaseResult(
            success=True,
            steps_completed=[],
            step_results={},
            total_execution_time=0.5,
            next_phase="agenda",
        )

        retrieved = result.get_step_result(1)
        assert retrieved is None

    def test_status_phase_result_was_step_successful_true(self) -> None:
        """Test checking if a step was successful when it was."""
        from src.ti4.core.status_phase import StatusPhaseResult, StepResult

        step_result = StepResult(success=True, step_name="Test Step")
        result = StatusPhaseResult(
            success=True,
            steps_completed=["Step 1"],
            step_results={1: step_result},
            total_execution_time=0.5,
            next_phase="agenda",
        )

        assert result.was_step_successful(1) is True

    def test_status_phase_result_was_step_successful_false(self) -> None:
        """Test checking if a step was successful when it failed."""
        from src.ti4.core.status_phase import StatusPhaseResult, StepResult

        step_result = StepResult(success=False, step_name="Test Step")
        result = StatusPhaseResult(
            success=True,
            steps_completed=["Step 1"],
            step_results={1: step_result},
            total_execution_time=0.5,
            next_phase="agenda",
        )

        assert result.was_step_successful(1) is False

    def test_status_phase_result_was_step_successful_missing(self) -> None:
        """Test checking if a non-existent step was successful returns False."""
        from src.ti4.core.status_phase import StatusPhaseResult

        result = StatusPhaseResult(
            success=True,
            steps_completed=[],
            step_results={},
            total_execution_time=0.5,
            next_phase="agenda",
        )

        assert result.was_step_successful(1) is False


class TestStatusPhaseStepHandler:
    """Test StatusPhaseStepHandler abstract base class."""

    def test_status_phase_step_handler_is_abstract(self) -> None:
        """Test that StatusPhaseStepHandler cannot be instantiated directly."""
        # RED: This will fail until we implement StatusPhaseStepHandler
        from src.ti4.core.status_phase import StatusPhaseStepHandler

        # Should not be able to instantiate abstract class
        with pytest.raises(TypeError):
            StatusPhaseStepHandler()

    def test_status_phase_step_handler_subclass_must_implement_methods(self) -> None:
        """Test that subclasses must implement all abstract methods."""
        from src.ti4.core.status_phase import StatusPhaseStepHandler

        # Create incomplete subclass
        class IncompleteHandler(StatusPhaseStepHandler):
            pass

        # Should not be able to instantiate incomplete subclass
        with pytest.raises(TypeError):
            IncompleteHandler()

    def test_status_phase_step_handler_complete_subclass_works(self) -> None:
        """Test that complete subclass can be instantiated."""
        from src.ti4.core.status_phase import StatusPhaseStepHandler, StepResult

        # Create complete subclass
        class CompleteHandler(StatusPhaseStepHandler):
            def execute(
                self, game_state: "GameState"
            ) -> tuple[StepResult, "GameState"]:
                result = StepResult(success=True, step_name="Test")
                return result, game_state

            def validate_prerequisites(self, game_state: "GameState") -> bool:
                return True

            def get_step_name(self) -> str:
                return "Test Step"

        # Should be able to instantiate complete subclass
        handler = CompleteHandler()
        assert handler.get_step_name() == "Test Step"


class TestStatusPhaseErrors:
    """Test StatusPhaseError exception hierarchy."""

    def test_status_phase_error_base_exception(self) -> None:
        """Test StatusPhaseError base exception."""
        # RED: This will fail until we implement StatusPhaseError
        from src.ti4.core.status_phase import StatusPhaseError

        error = StatusPhaseError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)

    def test_step_validation_error(self) -> None:
        """Test StepValidationError exception."""
        from src.ti4.core.status_phase import StepValidationError

        error = StepValidationError("Step validation failed")
        assert str(error) == "Step validation failed"
        assert isinstance(error, Exception)

    def test_system_integration_error(self) -> None:
        """Test SystemIntegrationError exception."""
        from src.ti4.core.status_phase import SystemIntegrationError

        error = SystemIntegrationError("System integration failed")
        assert str(error) == "System integration failed"
        assert isinstance(error, Exception)

    def test_game_state_error_inheritance(self) -> None:
        """Test that GameStateError inherits from StatusPhaseError."""
        from src.ti4.core.status_phase import (
            StatusPhaseError,
            StatusPhaseGameStateError,
        )

        error = StatusPhaseGameStateError("Game state error")
        assert str(error) == "Game state error"
        assert isinstance(error, StatusPhaseError)
        assert isinstance(error, Exception)

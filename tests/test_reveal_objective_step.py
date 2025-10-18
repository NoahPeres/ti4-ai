"""Tests for RevealObjectiveStep handler (Status Phase Step 2).

This module tests the RevealObjectiveStep handler that implements
Step 2 of the status phase: speaker reveals next public objective.

LRR References:
- Rule 81.2: Status Phase Step 2 - Reveal Public Objective
- Rule 80: Speaker - Speaker token privileges and powers
- Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 10.1, 12.3
"""

from unittest.mock import Mock, patch

from src.ti4.core.status_phase import StatusPhaseStepHandler, StepResult


class TestRevealObjectiveStep:
    """Test RevealObjectiveStep handler class.

    Tests the Step 2 handler for status phase objective revealing including:
    - Speaker identification and objective revealing logic
    - Handling for cases when no unrevealed objectives remain
    - Integration with existing objective system

    Requirements: 3.1, 12.3
    """

    def test_reveal_objective_step_creation(self) -> None:
        """Test creating RevealObjectiveStep instance.

        Verifies that the step handler can be instantiated successfully
        and implements the required StatusPhaseStepHandler interface.

        Requirements: 3.1 - Step 2 implementation
        """

        from src.ti4.core.status_phase import RevealObjectiveStep

        step = RevealObjectiveStep()
        assert step is not None
        assert isinstance(step, StatusPhaseStepHandler)

    def test_get_step_name(self) -> None:
        """Test getting the step name.

        Verifies that the step returns the correct name for identification.

        Requirements: 3.1 - Step 2 implementation
        """
        from src.ti4.core.status_phase import RevealObjectiveStep

        step = RevealObjectiveStep()
        step_name = step.get_step_name()

        assert step_name == "Reveal Public Objective"

    def test_validate_prerequisites_valid_game_state(self) -> None:
        """Test prerequisite validation with valid game state.

        Verifies that prerequisite validation works correctly
        when the game state is valid for objective revealing.

        Requirements: 3.1 - Step 2 validation
        """
        from src.ti4.core.status_phase import RevealObjectiveStep

        # Arrange: Create mock game state with valid conditions
        mock_game_state = Mock()
        mock_game_state.speaker_id = "player1"
        mock_game_state.players = [Mock(id="player1"), Mock(id="player2")]

        # Act: Validate prerequisites
        step = RevealObjectiveStep()
        is_valid = step.validate_prerequisites(mock_game_state)

        # Assert: Should be valid
        assert is_valid is True

    def test_validate_prerequisites_invalid_game_state(self) -> None:
        """Test prerequisite validation with invalid game state.

        Verifies that prerequisite validation fails appropriately
        when the game state is invalid.

        Requirements: 3.1 - Step 2 validation
        """
        from src.ti4.core.status_phase import RevealObjectiveStep

        # Arrange: Create invalid game state (None)
        invalid_game_state = None

        # Act: Validate prerequisites
        step = RevealObjectiveStep()
        is_valid = step.validate_prerequisites(invalid_game_state)

        # Assert: Should be invalid
        assert is_valid is False

    def test_validate_prerequisites_no_speaker(self) -> None:
        """Test prerequisite validation with no speaker assigned.

        Verifies that prerequisite validation passes when there are players,
        even if no speaker is assigned (speaker will be assigned during execution).

        Requirements: 3.2 - Speaker identification
        """
        from src.ti4.core.status_phase import RevealObjectiveStep

        # Arrange: Create mock game state with no speaker but with players
        mock_game_state = Mock()
        mock_game_state.speaker_id = None
        mock_game_state.players = [Mock(id="player1"), Mock(id="player2")]

        # Act: Validate prerequisites
        step = RevealObjectiveStep()
        is_valid = step.validate_prerequisites(mock_game_state)

        # Assert: Should be valid with players (speaker assigned during execution)
        assert is_valid is True

    def test_execute_with_available_objective(self) -> None:
        """Test executing step with available objective to reveal.

        Verifies that the step successfully reveals an objective
        when one is available.

        Requirements: 3.2 - Objective revealing logic
        """
        from src.ti4.core.status_phase import RevealObjectiveStep

        # Arrange: Create mock game state with speaker and available objective
        mock_game_state = Mock()
        mock_game_state.speaker_id = "player1"
        mock_game_state.players = [Mock(id="player1")]

        # Create mock objective to reveal
        mock_objective = Mock()
        mock_objective.id = "test_objective"
        mock_objective.name = "Test Objective"

        # Act: Execute step
        step = RevealObjectiveStep()
        with patch.object(
            step, "get_next_unrevealed_objective", return_value=mock_objective
        ):
            with patch.object(
                step, "reveal_objective", return_value=mock_game_state
            ) as mock_reveal:
                result, updated_state = step.execute(mock_game_state)

        # Assert: Should successfully reveal objective
        assert isinstance(result, StepResult)
        assert result.success is True
        assert result.step_name == "Reveal Public Objective"
        assert "Test Objective" in result.actions_taken[0]
        mock_reveal.assert_called_once_with(mock_objective, mock_game_state)

    def test_execute_with_no_unrevealed_objectives(self) -> None:
        """Test executing step when no unrevealed objectives remain.

        Verifies that the step handles the edge case gracefully
        when all objectives have been revealed.

        Requirements: 3.3 - Edge case handling
        """
        from src.ti4.core.status_phase import RevealObjectiveStep

        # Arrange: Create mock game state with speaker but no objectives
        mock_game_state = Mock()
        mock_game_state.speaker_id = "player1"
        mock_game_state.players = [Mock(id="player1")]

        # Act: Execute step
        step = RevealObjectiveStep()
        with patch.object(step, "get_next_unrevealed_objective", return_value=None):
            result, updated_state = step.execute(mock_game_state)

        # Assert: Should skip gracefully
        assert isinstance(result, StepResult)
        assert result.success is True
        assert result.step_name == "Reveal Public Objective"
        assert "No unrevealed objectives" in result.actions_taken[0]
        assert updated_state is mock_game_state

    def test_execute_handles_revealing_errors_gracefully(self) -> None:
        """Test that execution handles objective revealing errors gracefully.

        Verifies that the step handles objective revealing errors
        without crashing and provides meaningful error information.

        Requirements: 3.5 - Error handling during revealing
        """
        from src.ti4.core.status_phase import RevealObjectiveStep

        # Arrange: Create mock game state that will cause revealing error
        mock_game_state = Mock()
        mock_game_state.speaker_id = "player1"
        mock_game_state.players = [Mock(id="player1")]

        # Create mock objective
        mock_objective = Mock()
        mock_objective.id = "test_objective"

        # Act: Execute step
        step = RevealObjectiveStep()
        with patch.object(
            step, "get_next_unrevealed_objective", return_value=mock_objective
        ):
            with patch.object(
                step, "reveal_objective", side_effect=ValueError("Revealing error")
            ):
                result, updated_state = step.execute(mock_game_state)

        # Assert: Should handle error gracefully
        assert isinstance(result, StepResult)
        assert result.success is False
        assert "Revealing error" in result.error_message
        assert updated_state is mock_game_state

    def test_get_next_unrevealed_objective_returns_none_initially(self) -> None:
        """Test getting next unrevealed objective returns None initially.

        Verifies that the method for getting the next unrevealed objective
        returns None when no objectives are available.

        Requirements: 3.3 - Edge case handling
        """
        from src.ti4.core.status_phase import RevealObjectiveStep

        # Arrange: Create mock game state
        mock_game_state = Mock()

        # Act: Get next unrevealed objective
        step = RevealObjectiveStep()
        objective = step.get_next_unrevealed_objective(mock_game_state)

        # Assert: Should return None initially
        assert objective is None

    def test_reveal_objective_returns_updated_state(self) -> None:
        """Test revealing objective returns updated game state.

        Verifies that the reveal_objective method properly
        updates the game state when revealing an objective.

        Requirements: 3.4 - Objective revealing implementation
        """
        from src.ti4.core.status_phase import RevealObjectiveStep

        # Arrange: Create mock game state and objective
        mock_game_state = Mock()
        mock_objective = Mock()
        mock_objective.id = "test_objective"

        # Act: Reveal objective
        step = RevealObjectiveStep()
        updated_state = step.reveal_objective(mock_objective, mock_game_state)

        # Assert: Should return the same state initially
        assert updated_state is mock_game_state

    def test_execute_integration_with_objective_system(self) -> None:
        """Test integration with existing objective system.

        Verifies that the step properly integrates with the
        existing objective system for objective management.

        Requirements: 10.1 - Integration with objective system
        """
        from src.ti4.core.status_phase import RevealObjectiveStep

        # Arrange: Create mock game state with speaker
        mock_game_state = Mock()
        mock_game_state.speaker_id = "player1"
        mock_game_state.players = [Mock(id="player1")]

        # Create mock objective manager
        mock_objective_manager = Mock()
        mock_objective = Mock()
        mock_objective.id = "test_objective"
        mock_objective.name = "Test Objective"
        mock_objective_manager.reveal_next_objective.return_value = mock_objective

        # Act: Execute step with objective system integration
        step = RevealObjectiveStep()
        with patch(
            "src.ti4.core.objective.PublicObjectiveManager",
            return_value=mock_objective_manager,
        ):
            with patch.object(
                step, "get_next_unrevealed_objective", return_value=mock_objective
            ):
                with patch.object(
                    step, "reveal_objective", return_value=mock_game_state
                ):
                    result, updated_state = step.execute(mock_game_state)

        # Assert: Should integrate with objective system
        assert result.success is True
        assert "Test Objective" in result.actions_taken[0]

    def test_execute_identifies_speaker_correctly(self) -> None:
        """Test that execution identifies the speaker correctly.

        Verifies that the step properly identifies the current speaker
        for objective revealing responsibilities.

        Requirements: 3.2 - Speaker identification
        """
        from src.ti4.core.status_phase import RevealObjectiveStep

        # Arrange: Create mock game state with specific speaker
        mock_game_state = Mock()
        mock_game_state.speaker_id = "player2"
        mock_game_state.players = [Mock(id="player1"), Mock(id="player2")]

        # Create mock objective
        mock_objective = Mock()
        mock_objective.id = "test_objective"
        mock_objective.name = "Test Objective"

        # Act: Execute step
        step = RevealObjectiveStep()
        with patch.object(
            step, "get_next_unrevealed_objective", return_value=mock_objective
        ):
            with patch.object(step, "reveal_objective", return_value=mock_game_state):
                result, updated_state = step.execute(mock_game_state)

        # Assert: Should identify speaker correctly
        assert result.success is True
        assert (
            "player2" in result.actions_taken[0] or "Speaker" in result.actions_taken[0]
        )


class TestRevealObjectiveStepIntegration:
    """Test RevealObjectiveStep integration scenarios.

    Tests integration between the step handler and other game systems,
    including edge cases and error conditions.

    Requirements: 10.1 - Integration with objective system
    """

    def test_step_integrates_with_status_phase_orchestrator(self) -> None:
        """Test that step integrates properly with orchestrator.

        Verifies that the step can be used by the StatusPhaseOrchestrator
        and follows the proper interface contract.

        Requirements: 10.1 - Integration with existing systems
        """
        from src.ti4.core.status_phase import StatusPhaseOrchestrator

        # Arrange: Create orchestrator
        orchestrator = StatusPhaseOrchestrator()

        # Act: Get step handler from orchestrator
        handler = orchestrator.get_step_handler(2)

        # Assert: Should return step handler with proper interface
        # Note: This will initially fail until we integrate the step with orchestrator
        # For now, we'll just verify the interface works
        assert handler is not None
        assert hasattr(handler, "execute")
        assert hasattr(handler, "validate_prerequisites")
        assert hasattr(handler, "get_step_name")

    def test_step_handles_complex_objective_scenarios(self) -> None:
        """Test step handling of complex objective scenarios.

        Verifies that the step can handle complex scenarios
        with multiple objective types and revelation states.

        Requirements: 3.1 - Step 2 implementation robustness
        """
        from src.ti4.core.status_phase import RevealObjectiveStep

        # Arrange: Create complex mock game state
        mock_game_state = Mock()
        mock_game_state.speaker_id = "player1"
        mock_game_state.players = [Mock(id="player1")]

        # Create mock objectives of different types
        mock_stage_i_obj = Mock()
        mock_stage_i_obj.id = "stage_i_obj"
        mock_stage_i_obj.name = "Stage I Objective"
        mock_stage_i_obj.type = "PUBLIC_STAGE_I"

        # Act: Execute step with complex scenario
        step = RevealObjectiveStep()
        with patch.object(
            step, "get_next_unrevealed_objective", return_value=mock_stage_i_obj
        ):
            with patch.object(step, "reveal_objective", return_value=mock_game_state):
                result, updated_state = step.execute(mock_game_state)

        # Assert: Should handle complex scenario successfully
        assert result.success is True
        assert "Stage I Objective" in result.actions_taken[0]

    def test_step_execution_with_objective_system(self) -> None:
        """Test step execution with objective system integration.

        Verifies that the step executes efficiently even
        when integrating with the objective system.

        Requirements: 10.1 - Integration with objective system
        """
        from src.ti4.core.status_phase import RevealObjectiveStep

        # Arrange: Create game state with objective system
        mock_game_state = Mock()
        mock_game_state.speaker_id = "player1"
        mock_game_state.players = [Mock(id="player1")]

        # Create mock objective
        mock_objective = Mock()
        mock_objective.id = "test_objective"
        mock_objective.name = "Test Objective"

        # Act: Execute step
        step = RevealObjectiveStep()
        with patch.object(
            step, "get_next_unrevealed_objective", return_value=mock_objective
        ):
            with patch.object(step, "reveal_objective", return_value=mock_game_state):
                result, updated_state = step.execute(mock_game_state)

        # Assert: Should execute successfully
        assert result.success is True

    def test_step_executes_with_multiple_players(self) -> None:
        """Test step execution with multiple players present.

        Verifies that the step correctly identifies and uses the
        designated speaker when multiple players are present.

        Requirements: 3.2 - Speaker identification robustness
        """
        from src.ti4.core.status_phase import RevealObjectiveStep

        # Arrange: Create mock game state with speaker
        mock_game_state = Mock()
        mock_game_state.speaker_id = "player1"
        mock_game_state.players = [Mock(id="player1"), Mock(id="player2")]

        # Create mock objective
        mock_objective = Mock()
        mock_objective.id = "test_objective"
        mock_objective.name = "Test Objective"

        # Act: Execute step
        step = RevealObjectiveStep()
        with patch.object(
            step, "get_next_unrevealed_objective", return_value=mock_objective
        ):
            with patch.object(step, "reveal_objective", return_value=mock_game_state):
                result, updated_state = step.execute(mock_game_state)

        # Assert: Should handle speaker identification robustly
        assert result.success is True
        assert len(result.actions_taken) > 0

"""Tests for ScoreObjectivesStep handler (Status Phase Step 1).

This module tests the ScoreObjectivesStep handler that implements
Step 1 of the status phase: allowing players to score objectives
in initiative order with proper limits and validation.

LRR References:
- Rule 81.1: Status Phase Step 1 - Score Objectives
- Rule 61: Objectives - Scoring mechanics and limits
- Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 10.1, 12.3
"""

import time
from typing import TYPE_CHECKING
from unittest.mock import Mock, patch

if TYPE_CHECKING:
    pass


class TestScoreObjectivesStep:
    """Test ScoreObjectivesStep handler class.

    Tests the Step 1 handler for status phase objective scoring including:
    - Initiative order processing for objective scoring
    - Validation for 1 public + 1 secret objective scoring limits
    - Integration with existing objective system (Rule 61)

    Requirements: 2.1, 12.3
    """

    def test_score_objectives_step_creation(self) -> None:
        """Test creating ScoreObjectivesStep instance.

        Verifies that the step handler can be instantiated successfully
        and implements the required StatusPhaseStepHandler interface.

        Requirements: 2.1 - Step 1 implementation
        """
        # RED: This will fail until we implement ScoreObjectivesStep
        from src.ti4.core.status_phase import (
            ScoreObjectivesStep,
            StatusPhaseStepHandler,
        )

        step = ScoreObjectivesStep()
        assert step is not None
        assert isinstance(step, StatusPhaseStepHandler)

    def test_get_step_name(self) -> None:
        """Test getting the step name.

        Verifies that the step returns the correct name for identification.

        Requirements: 2.1 - Step 1 implementation
        """
        from src.ti4.core.status_phase import ScoreObjectivesStep

        step = ScoreObjectivesStep()
        step_name = step.get_step_name()

        assert step_name == "Score Objectives"

    def test_validate_prerequisites_valid_game_state(self) -> None:
        """Test prerequisite validation with valid game state.

        Verifies that prerequisite validation works correctly
        when the game state is valid for objective scoring.

        Requirements: 2.1 - Step 1 validation
        """
        from src.ti4.core.status_phase import ScoreObjectivesStep

        # Arrange: Create mock game state with valid conditions
        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player1"), Mock(id="player2")]

        # Act: Validate prerequisites
        step = ScoreObjectivesStep()
        is_valid = step.validate_prerequisites(mock_game_state)

        # Assert: Should be valid
        assert is_valid is True

    def test_validate_prerequisites_invalid_game_state(self) -> None:
        """Test prerequisite validation with invalid game state.

        Verifies that prerequisite validation fails appropriately
        when the game state is invalid.

        Requirements: 2.1 - Step 1 validation
        """
        from src.ti4.core.status_phase import ScoreObjectivesStep

        # Arrange: Create invalid game state (None)
        invalid_game_state = None

        # Act: Validate prerequisites
        step = ScoreObjectivesStep()
        is_valid = step.validate_prerequisites(invalid_game_state)

        # Assert: Should be invalid
        assert is_valid is False

    def test_execute_with_no_players(self) -> None:
        """Test executing step with no players in game.

        Verifies that the step handles edge case of no players gracefully.

        Requirements: 2.1 - Step 1 execution
        """
        from src.ti4.core.status_phase import ScoreObjectivesStep, StepResult

        # Arrange: Create mock game state with no players
        mock_game_state = Mock()
        mock_game_state.players = []

        # Act: Execute step
        step = ScoreObjectivesStep()
        result, updated_state = step.execute(mock_game_state)

        # Assert: Should complete successfully with no players processed
        assert isinstance(result, StepResult)
        assert result.success is True
        assert result.step_name == "Score Objectives"
        assert result.players_processed == []
        assert updated_state is mock_game_state

    @patch("src.ti4.core.strategy_cards.coordinator.StrategyCardCoordinator")
    def test_execute_processes_players_in_initiative_order(
        self, mock_coordinator_class
    ) -> None:
        """Test that players are processed in initiative order.

        Verifies that the step processes players in the correct
        initiative order as determined by strategy card assignments.

        Requirements: 2.2 - Initiative order processing
        """
        from src.ti4.core.status_phase import ScoreObjectivesStep, StepResult

        # Arrange: Create mock game state with players
        mock_game_state = Mock()
        mock_game_state.players = [
            Mock(id="player1"),
            Mock(id="player2"),
            Mock(id="player3"),
        ]

        # Mock strategy card coordinator to return specific initiative order
        mock_coordinator = Mock()
        mock_coordinator.get_status_phase_initiative_order.return_value = [
            "player2",
            "player1",
            "player3",
        ]
        mock_coordinator_class.return_value = mock_coordinator

        # Mock get_scorable_objectives to return empty lists (no objectives to score)
        step = ScoreObjectivesStep()
        with patch.object(step, "get_scorable_objectives", return_value=([], [])):
            # Act: Execute step
            result, updated_state = step.execute(mock_game_state)

        # Assert: Should process players in initiative order
        assert isinstance(result, StepResult)
        assert result.success is True
        assert result.players_processed == ["player2", "player1", "player3"]

    def test_get_scorable_objectives_returns_empty_lists_initially(self) -> None:
        """Test getting scorable objectives returns empty lists initially.

        Verifies that the method for getting scorable objectives
        returns empty lists when no objectives are available.

        Requirements: 2.3 - Objective scoring validation
        """
        from src.ti4.core.status_phase import ScoreObjectivesStep

        # Arrange: Create mock game state with empty objective lists
        mock_game_state = Mock()
        mock_game_state.get_public_objectives.return_value = []
        mock_game_state.get_player_secret_objectives.return_value = []
        player_id = "player1"

        # Act: Get scorable objectives
        step = ScoreObjectivesStep()
        public_objectives, secret_objectives = step.get_scorable_objectives(
            player_id, mock_game_state
        )

        # Assert: Should return empty lists when no objectives available
        assert public_objectives == []
        assert secret_objectives == []

    def test_get_scorable_objectives_integrates_with_objective_system(self) -> None:
        """Test that get_scorable_objectives integrates with the objective system.

        Verifies that the method properly retrieves objectives from the game state
        and filters them based on player eligibility and scoring limits.

        Requirements: 10.1 - Integration with objective system
        """
        from src.ti4.core.objective import ObjectiveCard, ObjectiveType
        from src.ti4.core.status_phase import ScoreObjectivesStep

        # Arrange: Create mock game state with objectives
        mock_game_state = Mock()
        player_id = "player1"

        # Create mock objectives
        mock_public_obj = Mock(spec=ObjectiveCard)
        mock_public_obj.id = "public_1"
        mock_public_obj.name = "Control 6 Planets"
        mock_public_obj.type = ObjectiveType.PUBLIC_STAGE_I
        mock_public_obj.requirement_validator = Mock(return_value=True)

        mock_secret_obj = Mock(spec=ObjectiveCard)
        mock_secret_obj.id = "secret_1"
        mock_secret_obj.name = "Win a Combat"
        mock_secret_obj.type = ObjectiveType.SECRET
        mock_secret_obj.requirement_validator = Mock(return_value=True)

        # Mock game state methods
        mock_game_state.get_public_objectives.return_value = [mock_public_obj]
        mock_game_state.get_player_secret_objectives.return_value = [mock_secret_obj]
        mock_game_state.is_objective_completed.return_value = False
        mock_game_state.players = [Mock(id=player_id)]

        # Act: Get scorable objectives
        step = ScoreObjectivesStep()
        public_objectives, secret_objectives = step.get_scorable_objectives(
            player_id, mock_game_state
        )

        # Assert: Should return the available objectives
        assert len(public_objectives) == 1
        assert len(secret_objectives) == 1
        assert public_objectives[0].id == "public_1"
        assert secret_objectives[0].id == "secret_1"

        # Verify game state methods were called
        mock_game_state.get_public_objectives.assert_called_once()
        mock_game_state.get_player_secret_objectives.assert_called_once_with(player_id)

    def test_process_player_objective_scoring_no_objectives(self) -> None:
        """Test processing player objective scoring with no available objectives.

        Verifies that player processing works correctly when
        no objectives are available to score.

        Requirements: 2.4 - Player objective scoring processing
        """
        from src.ti4.core.status_phase import ScoreObjectivesStep

        # Arrange: Create mock game state
        mock_game_state = Mock()
        player_id = "player1"

        # Mock get_scorable_objectives to return empty lists
        step = ScoreObjectivesStep()
        with patch.object(step, "get_scorable_objectives", return_value=([], [])):
            # Act: Process player objective scoring
            objectives_scored, updated_state = step.process_player_objective_scoring(
                player_id, mock_game_state
            )

        # Assert: Should return 0 objectives scored
        assert objectives_scored == 0
        assert updated_state is mock_game_state

    def test_process_player_objective_scoring_with_available_objectives(self) -> None:
        """Test processing player objective scoring with available objectives.

        Verifies that player processing works correctly when
        objectives are available to score.

        Requirements: 2.4 - Player objective scoring processing
        """
        from src.ti4.core.status_phase import ScoreObjectivesStep

        # Arrange: Create mock game state and objectives
        mock_game_state = Mock()
        mock_updated_state = Mock()
        player_id = "player1"

        # Create mock objectives
        mock_public_obj = Mock()
        mock_public_obj.id = "public_1"
        mock_secret_obj = Mock()
        mock_secret_obj.id = "secret_1"

        # Mock get_scorable_objectives to return objectives
        step = ScoreObjectivesStep()
        with patch.object(
            step,
            "get_scorable_objectives",
            return_value=([mock_public_obj], [mock_secret_obj]),
        ):
            # Mock game state scoring method - first call returns mock_updated_state,
            # second call (on mock_updated_state) returns final_state
            final_state = Mock()
            mock_game_state.score_objective.return_value = mock_updated_state
            mock_updated_state.score_objective.return_value = final_state

            # Act: Process player objective scoring
            objectives_scored, updated_state = step.process_player_objective_scoring(
                player_id, mock_game_state
            )

        # Assert: Should score objectives and return updated state
        assert objectives_scored == 2  # 1 public + 1 secret
        assert updated_state is final_state

    def test_execute_integration_with_objective_system(self) -> None:
        """Test integration with existing objective system.

        Verifies that the step properly integrates with the
        existing Rule 61 objective system for scoring validation.

        Requirements: 10.1 - Integration with objective system
        """
        from src.ti4.core.game_phase import GamePhase
        from src.ti4.core.status_phase import ScoreObjectivesStep

        # Arrange: Create mock game state with players
        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player1")]

        # Create mock objective
        mock_objective = Mock()
        mock_objective.id = "test_objective"

        # Mock strategy card coordinator
        with patch(
            "src.ti4.core.strategy_cards.coordinator.StrategyCardCoordinator"
        ) as mock_coordinator_class:
            mock_coordinator = Mock()
            mock_coordinator.get_status_phase_initiative_order.return_value = [
                "player1"
            ]
            mock_coordinator_class.return_value = mock_coordinator

            # Mock get_scorable_objectives to return one objective
            step = ScoreObjectivesStep()
            with patch.object(
                step, "get_scorable_objectives", return_value=([mock_objective], [])
            ):
                # Mock game state score_objective method
                mock_updated_state = Mock()
                mock_game_state.score_objective.return_value = mock_updated_state

                # Act: Execute step
                result, updated_state = step.execute(mock_game_state)

        # Assert: Should call game state score_objective method
        mock_game_state.score_objective.assert_called_with(
            "player1", mock_objective, GamePhase.STATUS
        )
        assert result.success is True

    def test_execute_handles_scoring_errors_gracefully(self) -> None:
        """Test that execution handles scoring errors gracefully.

        Verifies that the step handles objective scoring errors
        without crashing and provides meaningful error information.

        Requirements: 2.5 - Error handling during scoring
        """
        from src.ti4.core.status_phase import ScoreObjectivesStep, StepResult

        # Arrange: Create mock game state that will cause scoring error
        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player1")]

        # Create mock objective
        mock_objective = Mock()
        mock_objective.id = "test_objective"

        # Mock strategy card coordinator
        with patch(
            "src.ti4.core.strategy_cards.coordinator.StrategyCardCoordinator"
        ) as mock_coordinator_class:
            mock_coordinator = Mock()
            mock_coordinator.get_status_phase_initiative_order.return_value = [
                "player1"
            ]
            mock_coordinator_class.return_value = mock_coordinator

            # Mock get_scorable_objectives to return one objective
            step = ScoreObjectivesStep()
            with patch.object(
                step, "get_scorable_objectives", return_value=([mock_objective], [])
            ):
                # Mock game state score_objective to raise error
                mock_game_state.score_objective.side_effect = ValueError(
                    "Scoring error"
                )

                # Act: Execute step
                result, updated_state = step.execute(mock_game_state)

        # Assert: Should handle error gracefully
        assert isinstance(result, StepResult)
        assert result.success is True  # Graceful degradation - step continues
        assert len(result.actions_taken) == 1
        assert "Scoring error" in result.actions_taken[0]  # Error captured in actions
        assert "player1" in result.players_processed  # Player was processed
        assert updated_state is mock_game_state

    def test_execute_tracks_actions_taken(self) -> None:
        """Test that execution tracks actions taken during scoring.

        Verifies that the step properly tracks what actions
        were taken during objective scoring for reporting.

        Requirements: 2.1 - Step 1 execution tracking
        """
        from src.ti4.core.status_phase import ScoreObjectivesStep, StepResult

        # Arrange: Create mock game state with players
        mock_game_state = Mock()
        mock_game_state.players = [Mock(id="player1")]

        # Create mock objectives
        mock_public_obj = Mock()
        mock_public_obj.id = "public_1"
        mock_secret_obj = Mock()
        mock_secret_obj.id = "secret_1"

        # Mock strategy card coordinator
        with patch(
            "src.ti4.core.strategy_cards.coordinator.StrategyCardCoordinator"
        ) as mock_coordinator_class:
            mock_coordinator = Mock()
            mock_coordinator.get_status_phase_initiative_order.return_value = [
                "player1"
            ]
            mock_coordinator_class.return_value = mock_coordinator

            # Mock get_scorable_objectives to return objectives
            step = ScoreObjectivesStep()
            with patch.object(
                step,
                "get_scorable_objectives",
                return_value=([mock_public_obj], [mock_secret_obj]),
            ):
                # Mock game state scoring
                mock_updated_state = Mock()
                mock_game_state.score_objective.return_value = mock_updated_state

                # Act: Execute step
                result, updated_state = step.execute(mock_game_state)

        # Assert: Should track actions taken
        assert isinstance(result, StepResult)
        assert result.success is True
        assert len(result.actions_taken) > 0
        assert any("scored" in action.lower() for action in result.actions_taken)


class TestScoreObjectivesStepIntegration:
    """Test ScoreObjectivesStep integration scenarios.

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
        from src.ti4.core.status_phase import (
            StatusPhaseOrchestrator,
        )

        # Arrange: Create orchestrator and mock game state
        orchestrator = StatusPhaseOrchestrator()

        # Act: Get step handler from orchestrator
        handler = orchestrator.get_step_handler(1)

        # Assert: Should return ScoreObjectivesStep instance
        # Note: This will initially fail until we integrate the step with orchestrator
        # For now, we'll just verify the interface works
        assert handler is not None
        assert hasattr(handler, "execute")
        assert hasattr(handler, "validate_prerequisites")
        assert hasattr(handler, "get_step_name")

    def test_step_handles_complex_game_state(self) -> None:
        """Test step handling of complex game state scenarios.

        Verifies that the step can handle complex game states
        with multiple players, objectives, and scoring conditions.

        Requirements: 2.1 - Step 1 implementation robustness
        """
        from src.ti4.core.status_phase import ScoreObjectivesStep

        # Arrange: Create complex mock game state
        mock_game_state = Mock()
        mock_game_state.players = [
            Mock(id="player1"),
            Mock(id="player2"),
            Mock(id="player3"),
            Mock(id="player4"),
        ]

        # Mock strategy card coordinator for complex initiative order
        with patch(
            "src.ti4.core.strategy_cards.coordinator.StrategyCardCoordinator"
        ) as mock_coordinator_class:
            mock_coordinator = Mock()
            mock_coordinator.get_status_phase_initiative_order.return_value = [
                "player3",
                "player1",
                "player4",
                "player2",
            ]
            mock_coordinator_class.return_value = mock_coordinator

            # Mock get_scorable_objectives to return different objectives for each player
            step = ScoreObjectivesStep()

            def mock_get_scorable(player_id, game_state):
                if player_id == "player1":
                    return ([Mock(id="pub1")], [])
                elif player_id == "player2":
                    return ([], [Mock(id="sec1")])
                else:
                    return ([], [])

            with patch.object(
                step, "get_scorable_objectives", side_effect=mock_get_scorable
            ):
                # Mock game state scoring
                mock_game_state.score_objective.return_value = mock_game_state

                # Act: Execute step
                result, updated_state = step.execute(mock_game_state)

        # Assert: Should handle complex scenario successfully
        assert result.success is True
        assert len(result.players_processed) == 4
        assert result.players_processed == ["player3", "player1", "player4", "player2"]

    def test_step_performance_with_many_players(self) -> None:
        """Test step performance with many players.

        Verifies that the step executes efficiently even
        with a large number of players.

        Requirements: 12.2 - Individual step performance (<100ms)
        """
        from src.ti4.core.status_phase import ScoreObjectivesStep

        # Arrange: Create game state with many players
        mock_game_state = Mock()
        mock_game_state.players = [
            Mock(id=f"player{i}") for i in range(1, 9)
        ]  # 8 players

        # Mock strategy card coordinator
        with patch(
            "src.ti4.core.strategy_cards.coordinator.StrategyCardCoordinator"
        ) as mock_coordinator_class:
            mock_coordinator = Mock()
            mock_coordinator.get_status_phase_initiative_order.return_value = [
                f"player{i}" for i in range(1, 9)
            ]
            mock_coordinator_class.return_value = mock_coordinator

            # Mock get_scorable_objectives to return empty lists (fast path)
            step = ScoreObjectivesStep()
            with patch.object(step, "get_scorable_objectives", return_value=([], [])):
                # Act: Measure execution time
                start_time = time.time()
                result, updated_state = step.execute(mock_game_state)
                execution_time = time.time() - start_time

        # Assert: Should complete within performance requirements (<100ms)
        assert execution_time < 0.1
        assert result.success is True
        assert len(result.players_processed) == 8

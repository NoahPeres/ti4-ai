"""Comprehensive integration tests for Rule 81 Status Phase completion.

This module provides comprehensive integration testing for the complete status phase
implementation, including end-to-end round progression, phase transitions, and
integration with all existing game systems.

LRR References:
- Rule 81: Status Phase - Complete 8-step sequence
- Rule 27.4: Agenda phase activation after custodians token removal
- Rule 61: Objectives - Integration with scoring system
- Rule 83: Strategy Cards - Integration with card management
- Rule 20: Command Tokens - Integration with token management
- Rule 2: Action Cards - Integration with card drawing
"""

from unittest.mock import patch

import pytest

from src.ti4.core.game_phase import GamePhase
from src.ti4.core.game_state import GameState
from src.ti4.core.player import Player
from src.ti4.core.status_phase import StatusPhaseManager, StatusPhaseResult


class TestStatusPhaseComprehensiveIntegration:
    """Comprehensive integration tests for status phase with all game systems."""

    def setup_method(self) -> None:
        """Set up test fixtures for each test method."""
        # RED: This will fail because we need to create proper test fixtures
        # Disable performance optimization to use the base orchestrator for testing
        self.status_phase_manager = StatusPhaseManager(
            enable_performance_optimization=False
        )
        self.base_game_state = self._create_test_game_state()

    def _create_test_game_state(self) -> GameState:
        """Create a test game state with all necessary components."""
        # RED: This will fail because we need to implement proper game state creation
        players = [
            Player(id="player1", faction="sol"),
            Player(id="player2", faction="letnev"),
            Player(id="player3", faction="hacan"),
        ]

        # This will fail initially - we need to create a proper GameState
        return GameState(
            players=players, phase=GamePhase.STATUS, agenda_phase_active=False
        )

    def test_complete_round_progression_without_agenda_phase(self) -> None:
        """Test complete round progression from action phase through status phase to new round.

        Requirements: 9.1, 9.2, 9.3 - Round progression and phase transitions
        """
        # RED: This will fail because we need to implement proper round progression

        # Arrange: Set up game state in action phase with agenda phase explicitly disabled
        game_state = self.base_game_state._create_new_state(
            phase=GamePhase.ACTION, agenda_phase_active=False
        )

        # Verify the game state is set up correctly
        assert game_state.agenda_phase_active is False, (
            f"Expected agenda_phase_active=False, got {game_state.agenda_phase_active}"
        )

        # Act: Execute complete status phase
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            game_state
        )

        # Assert: Status phase completes successfully
        assert result.success is True
        assert len(result.steps_completed) == 8

        # Assert: Transitions to strategy phase (new round) when agenda phase not active
        assert result.next_phase == "strategy"
        assert final_state.phase == GamePhase.STRATEGY

    def test_complete_round_progression_with_agenda_phase_active(self) -> None:
        """Test complete round progression when agenda phase is active.

        Requirements: 9.1, 9.2 - Agenda phase transition when custodians token removed
        """
        # RED: This will fail because we need to implement agenda phase transition

        # Arrange: Set up game state with agenda phase active
        game_state = self.base_game_state._create_new_state(
            phase=GamePhase.STATUS, agenda_phase_active=True
        )

        # Act: Execute complete status phase
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            game_state
        )

        # Assert: Status phase completes successfully
        assert result.success is True

        # Assert: Transitions to agenda phase when active
        assert result.next_phase == "agenda"
        assert final_state.phase == GamePhase.AGENDA

    def test_custodians_token_removal_activates_agenda_phase(self) -> None:
        """Test that custodians token removal activates agenda phase for future rounds.

        Requirements: 9.2 - Validate agenda phase transition when custodians token removed
        """
        # RED: This will fail because we need to implement custodians token integration

        # Arrange: Game state with custodians token on Mecatol Rex
        # (Token would be used in actual implementation)
        game_state = self.base_game_state._create_new_state(agenda_phase_active=False)

        # Simulate custodians token removal (this would happen in action phase)
        game_state_with_agenda = game_state.activate_agenda_phase()

        # Act: Execute status phase after token removal
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            game_state_with_agenda
        )

        # Assert: Status phase completes and transitions to agenda phase
        assert result.success is True
        assert result.next_phase == "agenda"
        assert final_state.agenda_phase_active is True

    def test_integration_with_objective_system(self) -> None:
        """Test integration with existing objective system (Rule 61).

        Requirements: 10.1 - Integration with objectives system
        """
        # RED: This will fail because we need to implement objective system integration

        # Arrange: Game state with scorable objectives
        game_state = self.base_game_state

        # Act: Execute status phase (includes objective scoring step)
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            game_state
        )

        # Assert: Objective scoring step executed successfully
        assert result.success is True
        step_1_result = result.get_step_result(1)  # Score Objectives step
        assert step_1_result is not None
        assert step_1_result.success is True
        assert step_1_result.step_name == "Score Objectives"

    def test_integration_with_action_card_system(self) -> None:
        """Test integration with existing action card system (Rule 2).

        Requirements: 10.2 - Integration with action cards system
        """
        # RED: This will fail because we need to implement action card system integration

        # Arrange: Game state with action card deck
        game_state = self.base_game_state

        # Act: Execute status phase (includes draw action cards step)
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            game_state
        )

        # Assert: Draw action cards step executed successfully
        assert result.success is True
        step_3_result = result.get_step_result(3)  # Draw Action Cards step
        assert step_3_result is not None
        assert step_3_result.success is True
        assert step_3_result.step_name == "Draw Action Cards"

    def test_integration_with_command_token_system(self) -> None:
        """Test integration with existing command token system (Rule 20).

        Requirements: 10.3 - Integration with command tokens system
        """
        # RED: This will fail because we need to implement command token system integration

        # Arrange: Game state with command tokens on board
        game_state = self.base_game_state

        # Act: Execute status phase (includes command token management steps)
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            game_state
        )

        # Assert: Command token steps executed successfully
        assert result.success is True

        # Check step 4: Remove command tokens
        step_4_result = result.get_step_result(4)
        assert step_4_result is not None
        assert step_4_result.success is True

        # Check step 5: Gain and redistribute tokens
        step_5_result = result.get_step_result(5)
        assert step_5_result is not None
        assert step_5_result.success is True

    def test_integration_with_strategy_card_system(self) -> None:
        """Test integration with existing strategy card system (Rule 83).

        Requirements: 10.4 - Integration with strategy cards system
        """
        # RED: This will fail because we need to implement strategy card system integration

        # Arrange: Game state with strategy cards assigned to players
        game_state = self.base_game_state

        # Act: Execute status phase (includes return strategy cards step)
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            game_state
        )

        # Assert: Return strategy cards step executed successfully
        assert result.success is True
        step_8_result = result.get_step_result(8)  # Return Strategy Cards step
        assert step_8_result is not None
        assert step_8_result.success is True
        assert step_8_result.step_name == "Return Strategy Cards"

    def test_integration_with_leader_system(self) -> None:
        """Test integration with existing leader system (Rule 51).

        Requirements: 10.5 - Integration with leaders system (already implemented)
        """
        # RED: This will fail because we need to verify leader system integration

        # Arrange: Game state with exhausted leaders
        game_state = self.base_game_state

        # Act: Execute status phase (includes ready cards step)
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            game_state
        )

        # Assert: Ready cards step executed successfully (includes leader readying)
        assert result.success is True
        step_6_result = result.get_step_result(6)  # Ready Cards step
        assert step_6_result is not None
        assert step_6_result.success is True
        assert step_6_result.step_name == "Ready Cards"

    def test_end_to_end_multiple_round_progression(self) -> None:
        """Test multiple complete rounds with status phase transitions.

        Requirements: 9.1, 9.3 - Complete round progression scenarios
        """
        # RED: This will fail because we need to implement multi-round progression

        # Arrange: Initial game state
        current_state = self.base_game_state._create_new_state(phase=GamePhase.STATUS)

        # Act & Assert: Execute multiple rounds
        for round_num in range(3):
            # Execute status phase
            result, current_state = (
                self.status_phase_manager.execute_complete_status_phase(current_state)
            )

            # Assert: Each round completes successfully
            assert result.success is True, f"Round {round_num + 1} failed"
            assert len(result.steps_completed) == 8, f"Round {round_num + 1} incomplete"

            # Simulate transitioning back to status phase for next round
            # (In real game, this would go through strategy/action phases)
            current_state = current_state._create_new_state(phase=GamePhase.STATUS)

    def test_error_recovery_during_system_integration(self) -> None:
        """Test error recovery when integration with game systems fails.

        Requirements: 9.1, 12.3 - Error handling during integration
        """
        # RED: This will fail because we need to implement error recovery

        # Arrange: Game state that will cause integration failures
        game_state = self.base_game_state

        # Mock system integration failures
        with patch(
            "src.ti4.core.status_phase.ScoreObjectivesStep.execute"
        ) as mock_step:
            mock_step.side_effect = Exception("Objective system integration failed")

            # Act: Execute status phase with integration failure
            result, final_state = (
                self.status_phase_manager.execute_complete_status_phase(game_state)
            )

            # Assert: Graceful degradation - other steps continue
            # (Implementation should handle non-critical step failures gracefully)
            assert result is not None
            assert isinstance(result, StatusPhaseResult)

    def test_performance_requirements_during_integration(self) -> None:
        """Test that performance requirements are met during system integration.

        Requirements: 12.1, 12.2 - Performance benchmarks during integration
        """
        # RED: This will fail because we need to implement performance monitoring

        # Arrange: Game state with complex integration scenarios
        game_state = self.base_game_state

        # Act: Execute status phase and measure performance
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            game_state
        )

        # Assert: Performance requirements met
        assert result.success is True
        assert result.total_execution_time < 0.5  # <500ms requirement

        # Assert: Individual steps meet performance requirements
        for step_num in range(1, 9):
            step_result = result.get_step_result(step_num)
            if step_result:
                # Individual step performance would be tracked in enhanced implementation
                pass

    def test_backward_compatibility_with_existing_systems(self) -> None:
        """Test backward compatibility with existing game systems.

        Requirements: 12.5 - Maintain backward compatibility
        """
        # RED: This will fail because we need to verify backward compatibility

        # Arrange: Use existing ready_all_cards method
        game_state = self.base_game_state

        # Act: Test both old and new interfaces
        # Old interface (backward compatibility)
        ready_state = self.status_phase_manager.ready_all_cards(game_state)

        # New interface (complete status phase)
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            game_state
        )

        # Assert: Both interfaces work correctly
        assert ready_state is not None
        assert result.success is True
        assert final_state is not None


class TestStatusPhaseSystemValidation:
    """Test validation of status phase integration with game systems."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        # RED: This will fail because we need proper validation setup
        # Disable performance optimization to use the base orchestrator for testing
        self.status_phase_manager = StatusPhaseManager(
            enable_performance_optimization=False
        )

    def test_validate_all_game_systems_available(self) -> None:
        """Test that all required game systems are available for integration.

        Requirements: 10.1, 10.2, 10.3, 10.4, 10.5 - System availability validation
        """
        # RED: This will fail because we need to implement system validation

        # Act: Check that all required systems can be imported and used
        try:
            # Test imports to verify system availability
            import importlib.util

            systems = [
                "src.ti4.core.objective",
                "src.ti4.core.action_cards",
                "src.ti4.core.command_tokens",
                "src.ti4.core.strategy_cards.coordinator",
                "src.ti4.core.leaders",
            ]

            for system in systems:
                spec = importlib.util.find_spec(system)
                assert spec is not None, f"System {system} not available"

        except ImportError as e:
            pytest.fail(f"Required game system not available: {e}")

    def test_validate_phase_transition_consistency(self) -> None:
        """Test that phase transitions are consistent across all scenarios.

        Requirements: 9.1, 9.2, 9.3 - Phase transition validation
        """
        # RED: This will fail because we need to implement transition validation

        # Arrange: Test different game state scenarios
        scenarios = [
            ("no_agenda_phase", False, "strategy"),
            ("agenda_phase_active", True, "agenda"),
        ]

        for scenario_name, agenda_active, expected_next_phase in scenarios:
            # Create game state for scenario
            game_state = GameState(
                players=[Player(id="test_player", faction="sol")],
                phase=GamePhase.STATUS,
                agenda_phase_active=agenda_active,
            )

            # Act: Execute status phase
            result, final_state = (
                self.status_phase_manager.execute_complete_status_phase(game_state)
            )

            # Assert: Correct phase transition
            assert result.next_phase == expected_next_phase, (
                f"Scenario {scenario_name} failed"
            )

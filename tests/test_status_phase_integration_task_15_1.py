"""Comprehensive integration tests for Rule 81 Status Phase - Task 15.1 Implementation.

This module implements the specific comprehensive integration tests required by task 15.1:
- Test integration with all existing game systems
- Test complete round progression scenarios
- Test phase transition validation

This complements existing comprehensive integration tests by focusing specifically on
the requirements outlined in task 15.1 of the Rule 81 implementation plan.

LRR References:
- Rule 81: Status Phase - Complete 8-step sequence
- Rule 27.4: Agenda phase activation after custodians token removal
- Rule 61: Objectives - Integration with scoring system
- Rule 83: Strategy Cards - Integration with card management
- Rule 20: Command Tokens - Integration with token management
- Rule 2: Action Cards - Integration with card drawing
- Rule 51: Leaders - Integration with leader system
"""

from unittest.mock import Mock, patch

import pytest

from src.ti4.core.game_phase import GamePhase
from src.ti4.core.game_state import GameState
from src.ti4.core.player import Player
from src.ti4.core.status_phase import StatusPhaseManager, StatusPhaseResult


class TestTask15_1_IntegrationWithAllGameSystems:
    """Test integration with ALL existing game systems as required by task 15.1.

    Requirements: 10.1, 10.2, 10.3, 10.4, 10.5 - Integration with all systems
    """

    def setup_method(self) -> None:
        """Set up test fixtures for each test method."""
        # Use base orchestrator for testing (no performance optimization)
        self.status_phase_manager = StatusPhaseManager(
            enable_performance_optimization=False
        )

    def test_simultaneous_integration_with_all_game_systems(self) -> None:
        """Test that status phase integrates with ALL game systems simultaneously.

        This test validates that all 8 status phase steps can successfully integrate
        with their respective game systems without conflicts or interference.

        Requirements: 10.1, 10.2, 10.3, 10.4, 10.5 - Integration with all systems
        """
        # Arrange: Create game state with all systems represented
        players = [
            Player(id="player1", faction="sol"),
            Player(id="player2", faction="letnev"),
            Player(id="player3", faction="hacan"),
        ]

        game_state = GameState(
            players=players, phase=GamePhase.STATUS, agenda_phase_active=False
        )

        # Act: Execute complete status phase with all system integrations
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            game_state
        )

        # Assert: All steps completed successfully
        assert result.success is True, f"Status phase failed: {result.error_message}"
        assert len(result.steps_completed) == 8, (
            f"Expected 8 steps, got {len(result.steps_completed)}"
        )

        # Assert: Each system integration step completed
        expected_steps = [
            (1, "Score Objectives"),  # Objective system (Rule 61)
            (2, "Reveal Public Objective"),  # Objective system (Rule 61)
            (3, "Draw Action Cards"),  # Action card system (Rule 2)
            (4, "Remove Command Tokens"),  # Command token system (Rule 20)
            (
                5,
                "Gain and Redistribute Command Tokens",
            ),  # Command token system (Rule 20)
            (6, "Ready Cards"),  # Leader system (Rule 51) + others
            (7, "Repair Units"),  # Unit system
            (8, "Return Strategy Cards"),  # Strategy card system (Rule 83)
        ]

        for step_num, expected_name in expected_steps:
            step_result = result.get_step_result(step_num)
            assert step_result is not None, f"Step {step_num} result missing"
            assert step_result.success is True, (
                f"Step {step_num} ({expected_name}) failed: {step_result.error_message}"
            )
            assert step_result.step_name == expected_name, (
                f"Step {step_num} name mismatch: expected '{expected_name}', got '{step_result.step_name}'"
            )

        # Assert: Final state is valid
        assert final_state is not None
        assert hasattr(final_state, "players")
        assert len(final_state.players) == len(players)

    def test_objective_system_integration_edge_cases(self) -> None:
        """Test objective system integration with edge cases.

        Requirements: 10.1 - Integration with objectives system
        """
        # Arrange: Game state with edge case scenarios
        players = [Player(id="player1", faction="sol")]
        game_state = GameState(
            players=players, phase=GamePhase.STATUS, agenda_phase_active=False
        )

        # Act: Execute status phase
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            game_state
        )

        # Assert: Objective steps handle edge cases gracefully
        assert result.success is True

        # Step 1: Score Objectives - should handle no scorable objectives
        score_step = result.get_step_result(1)
        assert score_step is not None
        assert score_step.success is True

        # Step 2: Reveal Objective - should handle no unrevealed objectives
        reveal_step = result.get_step_result(2)
        assert reveal_step is not None
        assert reveal_step.success is True

    def test_action_card_system_integration_edge_cases(self) -> None:
        """Test action card system integration with edge cases.

        Requirements: 10.2 - Integration with action cards system
        """
        # Arrange: Game state with action card edge cases
        players = [Player(id="player1", faction="sol")]
        game_state = GameState(
            players=players, phase=GamePhase.STATUS, agenda_phase_active=False
        )

        # Act: Execute status phase
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            game_state
        )

        # Assert: Action card step handles edge cases gracefully
        assert result.success is True

        # Step 3: Draw Action Cards - should handle empty deck gracefully
        draw_step = result.get_step_result(3)
        assert draw_step is not None
        assert draw_step.success is True

    def test_command_token_system_integration_edge_cases(self) -> None:
        """Test command token system integration with edge cases.

        Requirements: 10.3 - Integration with command tokens system
        """
        # Arrange: Game state with command token edge cases
        players = [Player(id="player1", faction="sol")]
        game_state = GameState(
            players=players, phase=GamePhase.STATUS, agenda_phase_active=False
        )

        # Act: Execute status phase
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            game_state
        )

        # Assert: Command token steps handle edge cases gracefully
        assert result.success is True

        # Step 4: Remove Command Tokens - should handle no tokens on board
        remove_step = result.get_step_result(4)
        assert remove_step is not None
        assert remove_step.success is True

        # Step 5: Gain and Redistribute Tokens - should handle redistribution
        gain_step = result.get_step_result(5)
        assert gain_step is not None
        assert gain_step.success is True

    def test_strategy_card_system_integration_edge_cases(self) -> None:
        """Test strategy card system integration with edge cases.

        Requirements: 10.4 - Integration with strategy cards system
        """
        # Arrange: Game state with strategy card edge cases
        players = [Player(id="player1", faction="sol")]
        game_state = GameState(
            players=players, phase=GamePhase.STATUS, agenda_phase_active=False
        )

        # Act: Execute status phase
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            game_state
        )

        # Assert: Strategy card step handles edge cases gracefully
        assert result.success is True

        # Step 8: Return Strategy Cards - should handle no cards to return
        return_step = result.get_step_result(8)
        assert return_step is not None
        assert return_step.success is True

    def test_leader_system_integration_edge_cases(self) -> None:
        """Test leader system integration with edge cases.

        Requirements: 10.5 - Integration with leaders system
        """
        # Arrange: Game state with leader edge cases
        players = [Player(id="player1", faction="sol")]
        game_state = GameState(
            players=players, phase=GamePhase.STATUS, agenda_phase_active=False
        )

        # Act: Execute status phase
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            game_state
        )

        # Assert: Leader readying step handles edge cases gracefully
        assert result.success is True

        # Step 6: Ready Cards - should handle no exhausted leaders
        ready_step = result.get_step_result(6)
        assert ready_step is not None
        assert ready_step.success is True

    def test_system_integration_failure_recovery(self) -> None:
        """Test recovery when individual system integrations fail.

        Requirements: 12.3 - Error handling during integration
        """
        # Arrange: Game state for testing failure recovery
        players = [Player(id="player1", faction="sol")]
        game_state = GameState(
            players=players, phase=GamePhase.STATUS, agenda_phase_active=False
        )

        # Test each system integration failure independently
        system_failures = [
            (
                "src.ti4.core.status_phase.ScoreObjectivesStep.execute",
                "Objective system failure",
            ),
            (
                "src.ti4.core.status_phase.RevealObjectiveStep.execute",
                "Objective reveal failure",
            ),
            (
                "src.ti4.core.status_phase.DrawActionCardsStep.execute",
                "Action card system failure",
            ),
            (
                "src.ti4.core.status_phase.RemoveCommandTokensStep.execute",
                "Command token removal failure",
            ),
            (
                "src.ti4.core.status_phase.GainRedistributeTokensStep.execute",
                "Token redistribution failure",
            ),
            (
                "src.ti4.core.status_phase.ReadyCardsStep.execute",
                "Card readying failure",
            ),
            (
                "src.ti4.core.status_phase.RepairUnitsStep.execute",
                "Unit repair failure",
            ),
            (
                "src.ti4.core.status_phase.ReturnStrategyCardsStep.execute",
                "Strategy card return failure",
            ),
        ]

        for mock_target, error_message in system_failures:
            with patch(mock_target) as mock_step:
                mock_step.side_effect = Exception(error_message)

                # Act: Execute status phase with system failure
                result, final_state = (
                    self.status_phase_manager.execute_complete_status_phase(game_state)
                )

                # Assert: Graceful handling of system integration failure
                assert result is not None, (
                    f"Result should not be None for {error_message}"
                )
                assert isinstance(result, StatusPhaseResult), (
                    f"Result should be StatusPhaseResult for {error_message}"
                )

                # The implementation should handle failures gracefully
                # Either by continuing with other steps or providing clear error information


class TestTask15_1_CompleteRoundProgressionScenarios:
    """Test complete round progression scenarios as required by task 15.1.

    Requirements: 9.1, 9.2, 9.3 - Complete round progression scenarios
    """

    def setup_method(self) -> None:
        """Set up test fixtures for each test method."""
        self.status_phase_manager = StatusPhaseManager(
            enable_performance_optimization=False
        )

    def test_complete_round_progression_no_agenda_phase(self) -> None:
        """Test complete round progression when agenda phase is not active.

        Requirements: 9.1, 9.3 - Complete round progression scenarios
        """
        # Arrange: Game state at end of action phase, no agenda phase active
        players = [
            Player(id="player1", faction="sol"),
            Player(id="player2", faction="letnev"),
        ]

        # Simulate end of action phase
        action_phase_state = GameState(
            players=players, phase=GamePhase.ACTION, agenda_phase_active=False
        )

        # Transition to status phase (normally done by game controller)
        status_phase_state = action_phase_state._create_new_state(
            phase=GamePhase.STATUS
        )

        # Act: Execute complete status phase
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            status_phase_state
        )

        # Assert: Complete round progression
        assert result.success is True, f"Status phase failed: {result.error_message}"
        assert len(result.steps_completed) == 8, "All 8 steps should complete"

        # Assert: Transitions to strategy phase (new round)
        assert result.next_phase == "strategy", (
            f"Expected strategy phase, got {result.next_phase}"
        )
        assert final_state.phase == GamePhase.STRATEGY, (
            f"Expected STRATEGY phase, got {final_state.phase}"
        )

        # Assert: Game state consistency maintained
        assert len(final_state.players) == len(players)
        assert final_state.agenda_phase_active is False

    def test_complete_round_progression_with_agenda_phase(self) -> None:
        """Test complete round progression when agenda phase is active.

        Requirements: 9.1, 9.2 - Agenda phase transition when custodians token removed
        """
        # Arrange: Game state at end of action phase, agenda phase active
        players = [
            Player(id="player1", faction="sol"),
            Player(id="player2", faction="letnev"),
        ]

        # Simulate end of action phase with agenda phase active (custodians token removed)
        action_phase_state = GameState(
            players=players, phase=GamePhase.ACTION, agenda_phase_active=True
        )

        # Transition to status phase
        status_phase_state = action_phase_state._create_new_state(
            phase=GamePhase.STATUS
        )

        # Act: Execute complete status phase
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            status_phase_state
        )

        # Assert: Complete round progression
        assert result.success is True, f"Status phase failed: {result.error_message}"
        assert len(result.steps_completed) == 8, "All 8 steps should complete"

        # Assert: Transitions to agenda phase
        assert result.next_phase == "agenda", (
            f"Expected agenda phase, got {result.next_phase}"
        )
        assert final_state.phase == GamePhase.AGENDA, (
            f"Expected AGENDA phase, got {final_state.phase}"
        )

        # Assert: Game state consistency maintained
        assert len(final_state.players) == len(players)
        assert final_state.agenda_phase_active is True

    def test_multiple_consecutive_round_progressions(self) -> None:
        """Test multiple consecutive round progressions.

        Requirements: 9.1, 9.3 - Complete round progression scenarios
        """
        # Arrange: Initial game state
        players = [
            Player(id="player1", faction="sol"),
            Player(id="player2", faction="letnev"),
        ]

        current_state = GameState(
            players=players, phase=GamePhase.STATUS, agenda_phase_active=False
        )

        # Act & Assert: Execute multiple consecutive rounds
        for round_num in range(5):  # Test 5 consecutive rounds
            # Execute status phase
            result, current_state = (
                self.status_phase_manager.execute_complete_status_phase(current_state)
            )

            # Assert: Each round completes successfully
            assert result.success is True, (
                f"Round {round_num + 1} failed: {result.error_message}"
            )
            assert len(result.steps_completed) == 8, f"Round {round_num + 1} incomplete"

            # Assert: Proper phase transition
            expected_phase = (
                "agenda" if current_state.agenda_phase_active else "strategy"
            )
            assert result.next_phase == expected_phase, (
                f"Round {round_num + 1} wrong next phase"
            )

            # Assert: Game state consistency
            assert len(current_state.players) == len(players), (
                f"Round {round_num + 1} player count changed"
            )

            # Simulate completing the next phase and returning to status phase
            current_state = current_state._create_new_state(phase=GamePhase.STATUS)

    def test_round_progression_with_custodians_token_activation(self) -> None:
        """Test round progression when custodians token is removed mid-game.

        Requirements: 9.2 - Validate agenda phase transition when custodians token removed
        """
        # Arrange: Initial game state without agenda phase
        players = [Player(id="player1", faction="sol")]

        # Round 1: No agenda phase
        round1_state = GameState(
            players=players, phase=GamePhase.STATUS, agenda_phase_active=False
        )

        # Act: Execute first round
        result1, state_after_round1 = (
            self.status_phase_manager.execute_complete_status_phase(round1_state)
        )

        # Assert: First round transitions to strategy phase
        assert result1.success is True
        assert result1.next_phase == "strategy"
        assert state_after_round1.phase == GamePhase.STRATEGY

        # Simulate custodians token removal (would happen during action phase)
        state_with_agenda = state_after_round1.activate_agenda_phase()
        round2_state = state_with_agenda._create_new_state(phase=GamePhase.STATUS)

        # Act: Execute second round after custodians token removal
        result2, state_after_round2 = (
            self.status_phase_manager.execute_complete_status_phase(round2_state)
        )

        # Assert: Second round transitions to agenda phase
        assert result2.success is True
        assert result2.next_phase == "agenda"
        assert state_after_round2.phase == GamePhase.AGENDA
        assert state_after_round2.agenda_phase_active is True

    def test_round_progression_performance_requirements(self) -> None:
        """Test that round progression meets performance requirements.

        Requirements: 12.1, 12.2 - Performance benchmarks during round progression
        """
        # Arrange: Game state for performance testing
        players = [
            Player(id="player1", faction="sol"),
            Player(id="player2", faction="letnev"),
            Player(id="player3", faction="hacan"),
            Player(id="player4", faction="sardakk"),
        ]

        game_state = GameState(
            players=players, phase=GamePhase.STATUS, agenda_phase_active=False
        )

        # Act: Execute status phase and measure performance
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            game_state
        )

        # Assert: Performance requirements met
        assert result.success is True
        assert result.total_execution_time < 0.5, (
            f"Execution time {result.total_execution_time}s exceeds 500ms limit"
        )

        # Assert: All steps completed within reasonable time
        for step_num in range(1, 9):
            step_result = result.get_step_result(step_num)
            assert step_result is not None, f"Step {step_num} result missing"
            assert step_result.success is True, f"Step {step_num} failed"


class TestTask15_1_PhaseTransitionValidation:
    """Test phase transition validation as required by task 15.1.

    Requirements: 9.1, 9.2, 9.3 - Phase transition validation
    """

    def setup_method(self) -> None:
        """Set up test fixtures for each test method."""
        self.status_phase_manager = StatusPhaseManager(
            enable_performance_optimization=False
        )

    def test_phase_transition_validation_all_scenarios(self) -> None:
        """Test phase transition validation across all possible scenarios.

        Requirements: 9.1, 9.2, 9.3 - Phase transition validation
        """
        # Define comprehensive test scenarios
        scenarios = [
            {
                "name": "no_agenda_single_player",
                "players": [Player(id="player1", faction="sol")],
                "agenda_active": False,
                "expected_next_phase": "strategy",
                "expected_final_phase": GamePhase.STRATEGY,
            },
            {
                "name": "no_agenda_multiple_players",
                "players": [
                    Player(id="player1", faction="sol"),
                    Player(id="player2", faction="letnev"),
                    Player(id="player3", faction="hacan"),
                ],
                "agenda_active": False,
                "expected_next_phase": "strategy",
                "expected_final_phase": GamePhase.STRATEGY,
            },
            {
                "name": "agenda_active_single_player",
                "players": [Player(id="player1", faction="sol")],
                "agenda_active": True,
                "expected_next_phase": "agenda",
                "expected_final_phase": GamePhase.AGENDA,
            },
            {
                "name": "agenda_active_multiple_players",
                "players": [
                    Player(id="player1", faction="sol"),
                    Player(id="player2", faction="letnev"),
                    Player(id="player3", faction="hacan"),
                    Player(id="player4", faction="sardakk"),
                ],
                "agenda_active": True,
                "expected_next_phase": "agenda",
                "expected_final_phase": GamePhase.AGENDA,
            },
        ]

        for scenario in scenarios:
            # Arrange: Create game state for scenario
            game_state = GameState(
                players=scenario["players"],
                phase=GamePhase.STATUS,
                agenda_phase_active=scenario["agenda_active"],
            )

            # Act: Execute status phase
            result, final_state = (
                self.status_phase_manager.execute_complete_status_phase(game_state)
            )

            # Assert: Correct phase transition for scenario
            assert result.success is True, (
                f"Scenario {scenario['name']} failed: {result.error_message}"
            )
            assert result.next_phase == scenario["expected_next_phase"], (
                f"Scenario {scenario['name']}: expected next phase '{scenario['expected_next_phase']}', "
                f"got '{result.next_phase}'"
            )
            assert final_state.phase == scenario["expected_final_phase"], (
                f"Scenario {scenario['name']}: expected final phase '{scenario['expected_final_phase']}', "
                f"got '{final_state.phase}'"
            )

            # Assert: Game state consistency
            assert len(final_state.players) == len(scenario["players"]), (
                f"Scenario {scenario['name']}: player count changed"
            )
            assert final_state.agenda_phase_active == scenario["agenda_active"], (
                f"Scenario {scenario['name']}: agenda phase status changed"
            )

    def test_phase_transition_state_immutability(self) -> None:
        """Test that phase transitions maintain state immutability.

        Requirements: 9.1 - Phase transition validation with immutability
        """
        # Arrange: Initial game state
        players = [
            Player(id="player1", faction="sol"),
            Player(id="player2", faction="letnev"),
        ]

        initial_state = GameState(
            players=players, phase=GamePhase.STATUS, agenda_phase_active=False
        )

        # Store initial state properties for comparison
        initial_player_count = len(initial_state.players)
        initial_player_ids = [p.id for p in initial_state.players]
        initial_agenda_status = initial_state.agenda_phase_active

        # Act: Execute status phase
        result, final_state = self.status_phase_manager.execute_complete_status_phase(
            initial_state
        )

        # Assert: Original state unchanged (immutability)
        assert initial_state.phase == GamePhase.STATUS, (
            "Original state phase should be unchanged"
        )
        assert len(initial_state.players) == initial_player_count, (
            "Original state player count should be unchanged"
        )
        assert initial_state.agenda_phase_active == initial_agenda_status, (
            "Original state agenda status should be unchanged"
        )

        # Assert: New state has correct changes
        assert final_state.phase != initial_state.phase, (
            "Final state should have different phase"
        )
        assert len(final_state.players) == initial_player_count, (
            "Player count should be preserved"
        )

        final_player_ids = [p.id for p in final_state.players]
        assert final_player_ids == initial_player_ids, "Player IDs should be preserved"

    def test_phase_transition_error_handling(self) -> None:
        """Test phase transition error handling.

        Requirements: 9.1 - Phase transition validation with error handling
        """
        # Test with invalid game state
        invalid_states = [
            None,  # Null state
            Mock(),  # Mock object without proper attributes
        ]

        for invalid_state in invalid_states:
            # Act: Attempt phase transition with invalid state
            result, returned_state = (
                self.status_phase_manager.execute_complete_status_phase(invalid_state)
            )

            # Assert: Graceful error handling
            assert result is not None, (
                "Result should not be None even for invalid states"
            )
            assert isinstance(result, StatusPhaseResult), (
                "Result should be StatusPhaseResult"
            )

            # The implementation should handle invalid states gracefully
            # Either by returning an error result or by providing a default transition

    def test_phase_transition_consistency_across_executions(self) -> None:
        """Test that phase transitions are consistent across multiple executions.

        Requirements: 9.1, 9.3 - Phase transition validation consistency
        """
        # Arrange: Identical game states
        players = [Player(id="player1", faction="sol")]

        # Test multiple executions with identical states
        for execution_num in range(10):
            game_state = GameState(
                players=players, phase=GamePhase.STATUS, agenda_phase_active=False
            )

            # Act: Execute status phase
            result, final_state = (
                self.status_phase_manager.execute_complete_status_phase(game_state)
            )

            # Assert: Consistent results across executions
            assert result.success is True, f"Execution {execution_num + 1} failed"
            assert result.next_phase == "strategy", (
                f"Execution {execution_num + 1} inconsistent next phase"
            )
            assert final_state.phase == GamePhase.STRATEGY, (
                f"Execution {execution_num + 1} inconsistent final phase"
            )
            assert len(result.steps_completed) == 8, (
                f"Execution {execution_num + 1} inconsistent step count"
            )

    def test_phase_transition_with_different_player_counts(self) -> None:
        """Test phase transitions work correctly with different player counts.

        Requirements: 9.1 - Phase transition validation with varying player counts
        """
        # Test with different player counts (1-6 players)
        for player_count in range(1, 7):
            # Arrange: Game state with specific player count
            players = [
                Player(id=f"player{i + 1}", faction="sol") for i in range(player_count)
            ]

            game_state = GameState(
                players=players, phase=GamePhase.STATUS, agenda_phase_active=False
            )

            # Act: Execute status phase
            result, final_state = (
                self.status_phase_manager.execute_complete_status_phase(game_state)
            )

            # Assert: Successful execution regardless of player count
            assert result.success is True, (
                f"Failed with {player_count} players: {result.error_message}"
            )
            assert len(result.steps_completed) == 8, (
                f"Incomplete execution with {player_count} players"
            )
            assert result.next_phase == "strategy", (
                f"Wrong next phase with {player_count} players"
            )
            assert final_state.phase == GamePhase.STRATEGY, (
                f"Wrong final phase with {player_count} players"
            )

            # Assert: Player count preserved
            assert len(final_state.players) == player_count, (
                f"Player count changed with {player_count} players"
            )


if __name__ == "__main__":
    # Run task 15.1 comprehensive integration tests when executed directly
    pytest.main([__file__, "-v"])

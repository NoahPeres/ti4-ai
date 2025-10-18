"""Tests for ReadyCardsStep status phase handler.

This module tests the ReadyCardsStep handler that wraps the existing
ready_all_cards functionality and integrates it into the status phase
orchestration system.

LRR References:
- Rule 81.6: Status Phase Step 6 - Ready Cards
- Rule 34.2: Ready Cards step mechanics
- Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 10.5, 12.3
"""

from src.ti4.core.constants import Faction
from src.ti4.core.game_state import GameState
from src.ti4.core.leaders import LeaderReadyStatus, initialize_player_leaders
from src.ti4.core.player import Player
from src.ti4.core.status_phase import ReadyCardsStep, StepResult


def _find_player_by_id(game_state: GameState, player_id: str) -> Player:
    """Helper function to find a player by ID in game state."""
    for player in game_state.players:
        if player.id == player_id:
            return player
    assert False, f"Player {player_id} not found in game state"


class TestReadyCardsStep:
    """Test ReadyCardsStep status phase handler."""

    def test_ready_cards_step_inherits_from_base_handler(self) -> None:
        """Test that ReadyCardsStep inherits from StatusPhaseStepHandler."""
        # RED: This will fail until we implement ReadyCardsStep
        from src.ti4.core.status_phase import StatusPhaseStepHandler

        step = ReadyCardsStep()
        assert isinstance(step, StatusPhaseStepHandler)

    def test_ready_cards_step_get_step_name(self) -> None:
        """Test ReadyCardsStep returns correct step name."""
        # RED: This will fail until we implement ReadyCardsStep
        step = ReadyCardsStep()
        assert step.get_step_name() == "Ready Cards"

    def test_ready_cards_step_validate_prerequisites_valid_state(self) -> None:
        """Test ReadyCardsStep validates prerequisites with valid game state."""
        # RED: This will fail until we implement ReadyCardsStep
        step = ReadyCardsStep()
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        assert step.validate_prerequisites(game_state) is True

    def test_ready_cards_step_validate_prerequisites_none_state(self) -> None:
        """Test ReadyCardsStep validates prerequisites with None game state."""
        # RED: This will fail until we implement ReadyCardsStep
        step = ReadyCardsStep()

        assert step.validate_prerequisites(None) is False

    def test_ready_cards_step_execute_with_valid_state(self) -> None:
        """Test ReadyCardsStep executes successfully with valid game state."""
        # RED: This will fail until we implement ReadyCardsStep
        step = ReadyCardsStep()
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        result, new_state = step.execute(game_state)

        assert isinstance(result, StepResult)
        assert result.success is True
        assert result.step_name == "Ready Cards"
        assert result.error_message == ""
        assert new_state is not None

    def test_ready_cards_step_execute_with_none_state(self) -> None:
        """Test ReadyCardsStep handles None game state gracefully."""
        # RED: This will fail until we implement ReadyCardsStep
        step = ReadyCardsStep()

        result, new_state = step.execute(None)

        assert isinstance(result, StepResult)
        assert result.success is False
        assert result.step_name == "Ready Cards"
        assert "Game state cannot be None" in result.error_message
        assert new_state is None


class TestReadyCardsStepIntegration:
    """Test ReadyCardsStep integration with existing ready_all_cards functionality."""

    def test_ready_cards_step_integrates_with_existing_agent_readying(self) -> None:
        """Test ReadyCardsStep integrates with existing agent readying functionality."""
        # RED: This will fail until we implement ReadyCardsStep integration
        step = ReadyCardsStep()

        # Create game state with player and exhausted agent
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        # Initialize leaders and exhaust agent
        initialize_player_leaders(player)
        agent = player.leader_sheet.agent
        assert agent is not None
        agent.exhaust()
        assert agent.ready_status == LeaderReadyStatus.EXHAUSTED

        # Execute ReadyCardsStep
        result, new_state = step.execute(game_state)

        # Verify step succeeded
        assert result.success is True
        assert result.step_name == "Ready Cards"

        # Verify agent was readied through existing functionality
        updated_player = _find_player_by_id(new_state, "player1")
        updated_agent = updated_player.leader_sheet.agent
        assert updated_agent is not None
        assert updated_agent.ready_status == LeaderReadyStatus.READIED

    def test_ready_cards_step_maintains_backward_compatibility(self) -> None:
        """Test ReadyCardsStep maintains backward compatibility with existing code."""
        # RED: This will fail until we implement ReadyCardsStep
        from src.ti4.core.status_phase import StatusPhaseManager

        # Create game state with exhausted agent
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        initialize_player_leaders(player)
        agent = player.leader_sheet.agent
        assert agent is not None
        agent.exhaust()

        # Test that existing StatusPhaseManager.ready_all_cards still works
        status_manager = StatusPhaseManager()
        old_result = status_manager.ready_all_cards(game_state)

        # Test that new ReadyCardsStep produces same result
        step = ReadyCardsStep()
        step_result, new_result = step.execute(game_state)

        # Both should ready the agent
        old_player = _find_player_by_id(old_result, "player1")
        new_player = _find_player_by_id(new_result, "player1")

        assert old_player.leader_sheet.agent.ready_status == LeaderReadyStatus.READIED
        assert new_player.leader_sheet.agent.ready_status == LeaderReadyStatus.READIED

    def test_ready_cards_step_validates_all_cards_readied(self) -> None:
        """Test ReadyCardsStep validates that all cards are properly readied."""
        # RED: This will fail until we implement ReadyCardsStep validation
        step = ReadyCardsStep()

        # Create game state with multiple exhausted components
        game_state = GameState()
        player1 = Player("player1", Faction.SOL)
        player2 = Player("player2", Faction.HACAN)
        game_state = game_state.add_player(player1).add_player(player2)

        # Initialize leaders and exhaust agents
        initialize_player_leaders(player1)
        initialize_player_leaders(player2)

        agent1 = player1.leader_sheet.agent
        agent2 = player2.leader_sheet.agent
        assert agent1 is not None and agent2 is not None

        agent1.exhaust()
        agent2.exhaust()

        # Execute ReadyCardsStep
        result, new_state = step.execute(game_state)

        # Verify step succeeded and validation passed
        assert result.success is True
        assert result.step_name == "Ready Cards"

        # Verify validation tracked all readied components
        assert len(result.actions_taken) > 0
        assert any("agent" in action.lower() for action in result.actions_taken)

        # Verify all agents are actually readied
        updated_player1 = _find_player_by_id(new_state, "player1")
        updated_player2 = _find_player_by_id(new_state, "player2")

        assert (
            updated_player1.leader_sheet.agent.ready_status == LeaderReadyStatus.READIED
        )
        assert (
            updated_player2.leader_sheet.agent.ready_status == LeaderReadyStatus.READIED
        )

    def test_ready_cards_step_handles_multiple_card_types(self) -> None:
        """Test ReadyCardsStep handles multiple types of cards (strategy, planet, tech, agents)."""
        # RED: This will fail until we implement comprehensive ReadyCardsStep
        step = ReadyCardsStep()

        # Create game state with player
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        # Initialize leaders
        initialize_player_leaders(player)
        agent = player.leader_sheet.agent
        assert agent is not None
        agent.exhaust()

        # Execute ReadyCardsStep
        result, new_state = step.execute(game_state)

        # Verify step succeeded
        assert result.success is True
        assert result.step_name == "Ready Cards"

        # Verify actions were taken for different card types
        # (This test will be enhanced as we add more card type support)
        assert len(result.actions_taken) > 0


class TestReadyCardsStepErrorHandling:
    """Test ReadyCardsStep error handling and edge cases."""

    def test_ready_cards_step_handles_integration_errors_gracefully(self) -> None:
        """Test ReadyCardsStep handles integration errors gracefully."""
        # RED: This will fail until we implement ReadyCardsStep error handling
        step = ReadyCardsStep()

        # Create minimal game state that might cause integration issues
        game_state = GameState()

        # Execute step - should handle gracefully even with minimal state
        result, new_state = step.execute(game_state)

        # Should either succeed or fail gracefully with descriptive error
        assert isinstance(result, StepResult)
        assert result.step_name == "Ready Cards"

        if not result.success:
            assert result.error_message != ""
            assert len(result.error_message) > 0

    def test_ready_cards_step_tracks_players_processed(self) -> None:
        """Test ReadyCardsStep tracks which players were processed."""
        # RED: This will fail until we implement ReadyCardsStep player tracking
        step = ReadyCardsStep()

        # Create game state with multiple players
        game_state = GameState()
        player1 = Player("player1", Faction.SOL)
        player2 = Player("player2", Faction.HACAN)
        game_state = game_state.add_player(player1).add_player(player2)

        # Execute step
        result, new_state = step.execute(game_state)

        # Verify players were tracked
        assert result.success is True
        assert len(result.players_processed) == 2
        assert "player1" in result.players_processed
        assert "player2" in result.players_processed


class TestReadyCardsStepComprehensiveValidation:
    """Test comprehensive card readying validation as required by 6.5."""

    def test_ready_cards_step_validates_strategy_cards_readied(self) -> None:
        """Test ReadyCardsStep validates that strategy cards are readied (Requirement 6.1)."""
        # RED: This will fail until we implement comprehensive strategy card validation
        step = ReadyCardsStep()

        # Create game state with exhausted strategy cards
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        # Execute ReadyCardsStep (strategy card validation will be tested through actions)
        result, new_state = step.execute(game_state)

        # Verify step succeeded and strategy cards were validated
        assert result.success is True
        assert result.step_name == "Ready Cards"

        # Verify strategy card readying was tracked in actions
        strategy_actions = [
            action for action in result.actions_taken if "strategy" in action.lower()
        ]
        assert len(strategy_actions) > 0, (
            "Strategy card readying should be tracked in actions"
        )

    def test_ready_cards_step_validates_planet_cards_readied(self) -> None:
        """Test ReadyCardsStep validates that planet cards are readied (Requirement 6.2)."""
        # RED: This will fail until we implement comprehensive planet card validation
        step = ReadyCardsStep()

        # Create game state with exhausted planet cards
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        # Execute ReadyCardsStep
        result, new_state = step.execute(game_state)

        # Verify step succeeded and planet cards were validated
        assert result.success is True
        assert result.step_name == "Ready Cards"

        # Verify planet card readying was tracked in actions
        planet_actions = [
            action for action in result.actions_taken if "planet" in action.lower()
        ]
        assert len(planet_actions) > 0, (
            "Planet card readying should be tracked in actions"
        )

    def test_ready_cards_step_validates_technology_cards_readied(self) -> None:
        """Test ReadyCardsStep validates that technology cards are readied (Requirement 6.3)."""
        # RED: This will fail until we implement comprehensive technology card validation
        step = ReadyCardsStep()

        # Create game state with exhausted technology cards
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        # Execute ReadyCardsStep
        result, new_state = step.execute(game_state)

        # Verify step succeeded and technology cards were validated
        assert result.success is True
        assert result.step_name == "Ready Cards"

        # Verify technology card readying was tracked in actions
        tech_actions = [
            action for action in result.actions_taken if "technology" in action.lower()
        ]
        assert len(tech_actions) > 0, (
            "Technology card readying should be tracked in actions"
        )

    def test_ready_cards_step_validates_all_cards_in_readied_state(self) -> None:
        """Test ReadyCardsStep verifies all cards are in readied state (Requirement 6.5)."""
        # RED: This will fail until we implement comprehensive readied state validation
        step = ReadyCardsStep()

        # Create game state with multiple exhausted components
        game_state = GameState()
        player1 = Player("player1", Faction.SOL)
        player2 = Player("player2", Faction.HACAN)
        game_state = game_state.add_player(player1).add_player(player2)

        # Initialize leaders and exhaust agents
        initialize_player_leaders(player1)
        initialize_player_leaders(player2)

        agent1 = player1.leader_sheet.agent
        agent2 = player2.leader_sheet.agent
        assert agent1 is not None and agent2 is not None

        agent1.exhaust()
        agent2.exhaust()

        # Execute ReadyCardsStep
        result, new_state = step.execute(game_state)

        # Verify step succeeded
        assert result.success is True
        assert result.step_name == "Ready Cards"

        # Verify comprehensive validation was performed
        assert len(result.actions_taken) >= 4, (
            "Should track strategy, planet, technology, and agent readying"
        )

        # Verify all card types are mentioned in actions
        action_text = " ".join(result.actions_taken).lower()
        assert "strategy" in action_text, "Strategy cards should be validated"
        assert "planet" in action_text, "Planet cards should be validated"
        assert "technology" in action_text, "Technology cards should be validated"
        assert "agent" in action_text, "Agent leaders should be validated"

    def test_ready_cards_step_performance_under_100ms(self) -> None:
        """Test ReadyCardsStep executes in under 100ms (Requirement 12.2)."""
        # RED: This will fail until we optimize ReadyCardsStep performance
        import time

        step = ReadyCardsStep()

        # Create game state with multiple players and exhausted components
        game_state = GameState()
        for i in range(6):  # Test with 6 players (max TI4 players)
            player = Player(f"player{i + 1}", Faction.SOL)
            game_state = game_state.add_player(player)
            initialize_player_leaders(player)
            if player.leader_sheet.agent:
                player.leader_sheet.agent.exhaust()

        # Measure execution time
        start_time = time.perf_counter()
        result, new_state = step.execute(game_state)
        execution_time = time.perf_counter() - start_time

        # Verify step succeeded
        assert result.success is True

        # Verify performance requirement (100ms = 0.1 seconds)
        assert execution_time < 0.1, (
            f"ReadyCardsStep took {execution_time:.3f}s, should be under 0.1s"
        )


class TestReadyCardsStepBackwardCompatibility:
    """Test backward compatibility with existing systems (Requirement 6.5, 12.5)."""

    def test_ready_cards_step_maintains_existing_api_compatibility(self) -> None:
        """Test ReadyCardsStep maintains compatibility with existing StatusPhaseManager API."""
        # RED: This will fail until we ensure complete API compatibility
        from src.ti4.core.status_phase import StatusPhaseManager

        # Create game state with exhausted components
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        initialize_player_leaders(player)
        agent = player.leader_sheet.agent
        assert agent is not None
        agent.exhaust()

        # Test that both old and new APIs work identically
        status_manager = StatusPhaseManager()
        old_result = status_manager.ready_all_cards(game_state)

        step = ReadyCardsStep()
        step_result, new_result = step.execute(game_state)

        # Both should produce equivalent results
        old_player = _find_player_by_id(old_result, "player1")
        new_player = _find_player_by_id(new_result, "player1")

        assert (
            old_player.leader_sheet.agent.ready_status
            == new_player.leader_sheet.agent.ready_status
        )
        assert step_result.success is True

    def test_ready_cards_step_preserves_existing_behavior(self) -> None:
        """Test ReadyCardsStep preserves all existing ready_all_cards behavior."""
        # RED: This will fail until we ensure behavior preservation
        from src.ti4.core.status_phase import StatusPhaseManager

        # Create complex game state to test behavior preservation
        game_state = GameState()

        # Add multiple players with different exhausted components
        for i in range(3):
            player = Player(f"player{i + 1}", Faction.SOL)
            game_state = game_state.add_player(player)
            initialize_player_leaders(player)

            # Exhaust agents for some players
            if i % 2 == 0 and player.leader_sheet.agent:
                player.leader_sheet.agent.exhaust()

        # Test both implementations
        status_manager = StatusPhaseManager()
        old_result = status_manager.ready_all_cards(game_state)

        step = ReadyCardsStep()
        step_result, new_result = step.execute(game_state)

        # Verify new implementation succeeded
        assert step_result.success is True

        # Verify all players have same agent status in both results
        for i in range(3):
            player_id = f"player{i + 1}"
            old_player = _find_player_by_id(old_result, player_id)
            new_player = _find_player_by_id(new_result, player_id)

            if old_player.leader_sheet.agent and new_player.leader_sheet.agent:
                assert (
                    old_player.leader_sheet.agent.ready_status
                    == new_player.leader_sheet.agent.ready_status
                ), f"Agent status mismatch for {player_id}"

    def test_ready_cards_step_integrates_with_status_phase_orchestrator(self) -> None:
        """Test ReadyCardsStep integrates properly with StatusPhaseOrchestrator."""
        # RED: This will fail until we ensure orchestrator integration
        from src.ti4.core.status_phase import StatusPhaseOrchestrator

        # Create game state
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        initialize_player_leaders(player)
        agent = player.leader_sheet.agent
        assert agent is not None
        agent.exhaust()

        # Test integration with orchestrator
        orchestrator = StatusPhaseOrchestrator()

        # Execute step 6 (Ready Cards) through orchestrator
        step_result, new_state = orchestrator.execute_step(6, game_state)

        # Verify step executed successfully
        assert step_result.success is True
        assert step_result.step_name == "Ready Cards"

        # Verify agent was readied
        updated_player = _find_player_by_id(new_state, "player1")
        assert (
            updated_player.leader_sheet.agent.ready_status == LeaderReadyStatus.READIED
        )

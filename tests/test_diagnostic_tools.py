"""Tests for debugging and diagnostic tools."""

import time
from typing import Any
from unittest.mock import Mock

from src.ti4.commands.base import GameCommand
from src.ti4.core.game_state import GameState


class MockCommand(GameCommand):
    """Mock command for testing."""

    def __init__(self, command_type="mock") -> None:
        self.command_type = command_type

    def execute(self, game_state: GameState) -> GameState:
        return game_state

    def undo(self, game_state: GameState) -> GameState:
        return game_state

    def can_execute(self, game_state: GameState) -> bool:
        return True

    def get_undo_data(self) -> dict[str, Any]:
        return {"type": self.command_type}

    def serialize(self) -> dict[str, Any]:
        return {"type": self.command_type, "timestamp": time.time()}

    def _publish_events(self, event_bus: Any, game_state: GameState) -> None:
        pass


class TestGameStateInspector:
    """Test game state inspection utilities."""

    def test_game_state_inspector_creation(self) -> None:
        """Test GameStateInspector creation and basic functionality."""
        # RED: This will fail because GameStateInspector doesn't exist yet
        from src.ti4.core.diagnostics import GameStateInspector

        inspector = GameStateInspector()

        # Mock game state
        game_state = Mock(spec=GameState)
        game_state.players = ["player1", "player2"]
        game_state.current_phase = "action"

        inspection_result = inspector.inspect(game_state)

        assert "players" in inspection_result
        assert "current_phase" in inspection_result
        assert inspection_result["players"] == ["player1", "player2"]
        assert inspection_result["current_phase"] == "action"

    def test_detailed_state_analysis(self) -> None:
        """Test detailed game state analysis."""
        # RED: This will fail because GameStateInspector doesn't exist yet
        from src.ti4.core.diagnostics import GameStateInspector

        inspector = GameStateInspector()

        # Mock complex game state
        game_state = Mock(spec=GameState)
        game_state.players = ["player1", "player2"]
        game_state.current_phase = "action"
        game_state.turn_order = ["player1", "player2"]
        game_state.active_player = "player1"

        detailed_analysis = inspector.analyze_state(game_state)

        assert "summary" in detailed_analysis
        assert "player_count" in detailed_analysis["summary"]
        assert "phase_info" in detailed_analysis
        assert "turn_info" in detailed_analysis
        assert detailed_analysis["summary"]["player_count"] == 2

    def test_state_validation_checks(self) -> None:
        """Test game state validation and consistency checks."""
        # RED: This will fail because GameStateInspector doesn't exist yet
        from src.ti4.core.diagnostics import GameStateInspector

        inspector = GameStateInspector()

        # Mock game state with potential issues
        game_state = Mock(spec=GameState)
        game_state.players = ["player1", "player2"]
        game_state.active_player = "player3"  # Invalid - not in players list

        validation_result = inspector.validate_state(game_state)

        assert "is_valid" in validation_result
        assert "issues" in validation_result
        assert not validation_result["is_valid"]
        assert len(validation_result["issues"]) > 0
        assert any("active_player" in issue for issue in validation_result["issues"])


class TestCommandHistoryAnalyzer:
    """Test command history analysis tools."""

    def test_command_history_analyzer_creation(self) -> None:
        """Test CommandHistoryAnalyzer creation and basic functionality."""
        # RED: This will fail because CommandHistoryAnalyzer doesn't exist yet
        from src.ti4.core.diagnostics import CommandHistoryAnalyzer

        analyzer = CommandHistoryAnalyzer()

        # Mock command history
        commands: list[GameCommand] = [
            MockCommand("move"),
            MockCommand("attack"),
            MockCommand("move"),
        ]

        analysis = analyzer.analyze_commands(commands)

        assert "total_commands" in analysis
        assert "command_types" in analysis
        assert analysis["total_commands"] == 3
        assert analysis["command_types"]["move"] == 2
        assert analysis["command_types"]["attack"] == 1

    def test_command_pattern_detection(self) -> None:
        """Test detection of command patterns and anomalies."""
        # RED: This will fail because CommandHistoryAnalyzer doesn't exist yet
        from src.ti4.core.diagnostics import CommandHistoryAnalyzer

        analyzer = CommandHistoryAnalyzer()

        # Mock command sequence with patterns
        commands: list[GameCommand] = [
            MockCommand("move"),
            MockCommand("move"),
            MockCommand("move"),
            MockCommand("attack"),
            MockCommand("move"),
        ]

        patterns = analyzer.detect_patterns(commands)

        assert "repeated_commands" in patterns
        assert "command_sequences" in patterns
        assert patterns["repeated_commands"]["move"] >= 3

    def test_command_performance_analysis(self) -> None:
        """Test command execution performance analysis."""
        # RED: This will fail because CommandHistoryAnalyzer doesn't exist yet
        from src.ti4.core.diagnostics import CommandHistoryAnalyzer

        analyzer = CommandHistoryAnalyzer()

        # Mock commands with execution times
        command_data = [
            {"command": MockCommand("move"), "execution_time": 0.1},
            {"command": MockCommand("attack"), "execution_time": 0.5},
            {"command": MockCommand("move"), "execution_time": 0.2},
        ]

        performance_analysis = analyzer.analyze_performance(command_data)

        assert "average_execution_time" in performance_analysis
        assert "slowest_commands" in performance_analysis
        assert "command_type_performance" in performance_analysis


class TestPerformanceProfiler:
    """Test performance profiling helpers."""

    def test_performance_profiler_creation(self) -> None:
        """Test PerformanceProfiler creation and basic functionality."""
        # RED: This will fail because PerformanceProfiler doesn't exist yet
        from src.ti4.core.diagnostics import PerformanceProfiler

        profiler = PerformanceProfiler()

        # Test basic profiling
        with profiler.profile("test_operation"):
            time.sleep(0.01)  # Simulate work

        results = profiler.get_results()

        assert "test_operation" in results
        assert results["test_operation"]["call_count"] == 1
        assert results["test_operation"]["total_time"] > 0

    def test_nested_profiling(self) -> None:
        """Test nested operation profiling."""
        # RED: This will fail because PerformanceProfiler doesn't exist yet
        from src.ti4.core.diagnostics import PerformanceProfiler

        profiler = PerformanceProfiler()

        # Test nested profiling
        with profiler.profile("outer_operation"):
            with profiler.profile("inner_operation"):
                time.sleep(0.01)
            time.sleep(0.01)

        results = profiler.get_results()

        assert "outer_operation" in results
        assert "inner_operation" in results
        assert (
            results["outer_operation"]["total_time"]
            > results["inner_operation"]["total_time"]
        )

    def test_profiling_statistics(self) -> None:
        """Test profiling statistics and reporting."""
        # RED: This will fail because PerformanceProfiler doesn't exist yet
        from src.ti4.core.diagnostics import PerformanceProfiler

        profiler = PerformanceProfiler()

        # Profile multiple calls
        for _ in range(3):
            with profiler.profile("repeated_operation"):
                time.sleep(0.01)

        stats = profiler.get_statistics("repeated_operation")

        assert "call_count" in stats
        assert "total_time" in stats
        assert "average_time" in stats
        assert "min_time" in stats
        assert "max_time" in stats
        assert stats["call_count"] == 3

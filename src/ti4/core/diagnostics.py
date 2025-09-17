"""Debugging and diagnostic tools for TI4 game framework."""

import statistics
import time
from collections import Counter, defaultdict
from contextlib import contextmanager
from typing import Any, Callable

from ..commands.base import GameCommand
from .game_state import GameState


class GameStateInspector:
    """Utilities for inspecting and analyzing game state."""

    def __init__(self) -> None:
        self.validation_rules = self._build_validation_rules()

    def _safe_get_attr(self, obj: Any, attr_name: str, default: Any = None) -> Any:
        """Safely get attribute from object with default value."""
        return getattr(obj, attr_name, default) if hasattr(obj, attr_name) else default

    def inspect(self, game_state: GameState) -> dict[str, Any]:
        """Perform basic inspection of game state."""
        inspection = {}

        # Extract basic state information
        attrs_to_extract = ["players", "current_phase", "turn_order", "active_player"]
        for attr in attrs_to_extract:
            value = self._safe_get_attr(game_state, attr)
            if value is not None:
                inspection[attr] = value

        return inspection

    def analyze_state(self, game_state: GameState) -> dict[str, Any]:
        """Perform detailed analysis of game state."""
        basic_info = self.inspect(game_state)

        analysis = {
            "summary": {
                "player_count": len(basic_info.get("players", [])),
                "current_phase": basic_info.get("current_phase"),
                "active_player": basic_info.get("active_player"),
            },
            "phase_info": {
                "current_phase": basic_info.get("current_phase"),
                "phase_valid": self._validate_phase(game_state),
            },
            "turn_info": {
                "turn_order": basic_info.get("turn_order", []),
                "active_player": basic_info.get("active_player"),
                "turn_valid": self._validate_turn_order(game_state),
            },
        }

        return analysis

    def validate_state(self, game_state: GameState) -> dict[str, Any]:
        """Validate game state consistency and identify issues."""
        issues = []

        # Check if active player is in players list
        players = self._safe_get_attr(game_state, "players", [])
        active_player = self._safe_get_attr(game_state, "active_player")
        if active_player and active_player not in players:
            issues.append("active_player is not in players list")

        # Check turn order consistency
        turn_order = self._safe_get_attr(game_state, "turn_order", [])
        if players and turn_order and set(players) != set(turn_order):
            issues.append("turn_order does not match players list")

        # Add more validation rules as needed
        for rule_name, rule_func in self.validation_rules.items():
            try:
                if not rule_func(game_state):
                    issues.append(f"Validation rule failed: {rule_name}")
            except Exception as e:
                issues.append(f"Validation rule error ({rule_name}): {str(e)}")

        return {"is_valid": len(issues) == 0, "issues": issues}

    def _build_validation_rules(self) -> dict[str, Callable[[Any], bool]]:
        """Build dictionary of validation rules."""
        return {
            "has_players": lambda state: hasattr(state, "players")
            and len(getattr(state, "players", [])) > 0,
            "has_phase": lambda state: hasattr(state, "current_phase")
            and state.current_phase is not None,
        }

    def _validate_phase(self, game_state: GameState) -> bool:
        """Validate current phase is valid."""
        if not hasattr(game_state, "current_phase"):
            return False
        return game_state.current_phase is not None

    def _validate_turn_order(self, game_state: GameState) -> bool:
        """Validate turn order consistency."""
        if not hasattr(game_state, "players") or not hasattr(game_state, "turn_order"):
            return True  # Can't validate if data is missing

        return set(game_state.players) == set(game_state.turn_order)


class CommandHistoryAnalyzer:
    """Tools for analyzing command history and patterns."""

    def __init__(self) -> None:
        pass

    def analyze_commands(self, commands: list[GameCommand]) -> dict[str, Any]:
        """Analyze list of commands for patterns and statistics."""
        if not commands:
            return {"total_commands": 0, "command_types": {}}

        # Count command types
        command_types: Counter[str] = Counter()
        for command in commands:
            command_type = self._extract_command_type(command)
            command_types[command_type] += 1

        return {"total_commands": len(commands), "command_types": dict(command_types)}

    def detect_patterns(self, commands: list[GameCommand]) -> dict[str, Any]:
        """Detect patterns in command execution."""
        return self.analyze_command_patterns_and_sequences(commands)

    def analyze_command_patterns_and_sequences(
        self, commands: list[GameCommand]
    ) -> dict[str, Any]:
        """Analyze command patterns and detect sequences in command execution.

        This method examines a list of commands to identify:
        1. Repeated command types and their frequencies
        2. Sequential patterns between consecutive commands

        Args:
            commands: List of game commands to analyze

        Returns:
            Dict containing:
            - repeated_commands: Frequency count of each command type
            - command_sequences: List of command transition patterns
        """
        if not commands:
            return {"repeated_commands": {}, "command_sequences": []}

        # Count repeated commands by type
        command_type_frequencies: Counter[str] = Counter()
        for command in commands:
            command_type = self._extract_command_type(command)
            command_type_frequencies[command_type] += 1

        # Identify command transition sequences
        command_transition_sequences = []
        for i in range(len(commands) - 1):
            current_command_type = self._extract_command_type(commands[i])
            next_command_type = self._extract_command_type(commands[i + 1])
            command_transition_sequences.append(
                f"{current_command_type} -> {next_command_type}"
            )

        return {
            "repeated_commands": dict(command_type_frequencies),
            "command_sequences": command_transition_sequences,
        }

    def analyze_performance(self, command_data: list[dict[str, Any]]) -> dict[str, Any]:
        """Analyze command execution performance."""
        if not command_data:
            return {
                "average_execution_time": 0,
                "slowest_commands": [],
                "command_type_performance": {},
            }

        execution_times = [data["execution_time"] for data in command_data]

        # Group by command type
        type_performance = defaultdict(list)
        for data in command_data:
            command_type = self._extract_command_type(data["command"])
            type_performance[command_type].append(data["execution_time"])

        # Calculate averages per type
        type_averages = {}
        for cmd_type, times in type_performance.items():
            type_averages[cmd_type] = statistics.mean(times)

        # Find slowest commands
        sorted_commands = sorted(
            command_data, key=lambda x: x["execution_time"], reverse=True
        )
        slowest_commands = [
            {
                "command_type": self._extract_command_type(data["command"]),
                "execution_time": data["execution_time"],
            }
            for data in sorted_commands[:5]  # Top 5 slowest
        ]

        return {
            "average_execution_time": statistics.mean(execution_times),
            "slowest_commands": slowest_commands,
            "command_type_performance": type_averages,
        }

    def _extract_command_type(self, command: GameCommand) -> str:
        """Extract the command type identifier from a game command object.

        This method provides a consistent way to get the command type identifier
        from any game command, falling back to the lowercase class name if no
        explicit command_type attribute is available.

        Args:
            command: The game command to extract the type from

        Returns:
            str: The command type identifier or lowercase class name
        """
        if hasattr(command, "command_type"):
            return str(command.command_type)
        return command.__class__.__name__.lower()


class PerformanceProfiler:
    """Performance profiling helpers for operations."""

    def __init__(self) -> None:
        self.results: dict[str, dict[str, Any]] = defaultdict(
            lambda: {"call_count": 0, "total_time": 0.0, "times": []}
        )
        self.active_profiles: dict[str, float] = {}

    @contextmanager
    def profile(self, operation_name: str) -> Any:
        """Context manager for profiling operations."""
        start_time = time.time()
        self.active_profiles[operation_name] = start_time

        try:
            yield
        finally:
            end_time = time.time()
            execution_time = end_time - start_time

            # Record results
            result_entry = self.results[operation_name]
            result_entry["call_count"] += 1
            result_entry["total_time"] += execution_time
            result_entry["times"].append(execution_time)

            # Clean up active profile
            if operation_name in self.active_profiles:
                del self.active_profiles[operation_name]

    def get_results(self) -> dict[str, dict[str, Any]]:
        """Get profiling results for all operations."""
        return dict(self.results)

    def get_statistics(self, operation_name: str) -> dict[str, Any]:
        """Get detailed statistics for specific operation."""
        if operation_name not in self.results:
            return {}

        data = self.results[operation_name]
        times = data["times"]

        if not times:
            return {
                "call_count": 0,
                "total_time": 0.0,
                "average_time": 0.0,
                "min_time": 0.0,
                "max_time": 0.0,
            }

        times_list = list(times)
        return {
            "call_count": data["call_count"],
            "total_time": data["total_time"],
            "average_time": statistics.mean(times_list),
            "min_time": min(times_list),
            "max_time": max(times_list),
        }

    def reset(self) -> None:
        """Reset all profiling data."""
        self.results.clear()
        self.active_profiles.clear()

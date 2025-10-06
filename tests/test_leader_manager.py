"""Tests for LeaderManager class.

This module tests the LeaderManager class which coordinates leader operations,
unlock condition checking, and ability execution.

LRR References:
- Rule 51: LEADERS
- Requirements 8.1, 8.2, 8.3, 9.1, 9.2, 9.3, 9.4, 9.5
"""

import pytest

from src.ti4.core.constants import Faction
from src.ti4.core.game_state import GameState
from src.ti4.core.player import Player


class TestLeaderManager:
    """Test cases for LeaderManager functionality."""

    def test_leader_manager_can_be_imported(self) -> None:
        """Test that LeaderManager can be imported (GREEN phase)."""
        from src.ti4.core.leaders import LeaderManager  # noqa: F401

    def test_leader_manager_initialization(self) -> None:
        """Test LeaderManager initialization with game state."""
        from src.ti4.core.leaders import LeaderManager

        game_state = GameState()
        manager = LeaderManager(game_state)

        assert manager.game_state is game_state

    def test_leader_manager_initialization_with_none_game_state_fails(self) -> None:
        """Test LeaderManager initialization fails with None game state."""
        from src.ti4.core.leaders import LeaderManager

        with pytest.raises(ValueError, match="game_state cannot be None"):
            LeaderManager(None)  # type: ignore

    def test_check_unlock_conditions_with_nonexistent_player_fails(self) -> None:
        """Test that check_unlock_conditions fails with nonexistent player."""
        from src.ti4.core.leaders import LeaderManager, LeaderNotFoundError

        game_state = GameState()
        manager = LeaderManager(game_state)

        # This should fail because player doesn't exist
        with pytest.raises(LeaderNotFoundError, match="Player player1 not found"):
            manager.check_unlock_conditions("player1")

    def test_check_unlock_conditions_with_valid_player(self) -> None:
        """Test that check_unlock_conditions works with valid player."""
        from src.ti4.core.leaders import LeaderManager

        # Create a player with leaders
        player = Player(id="player1", faction=Faction.ARBOREC)
        game_state = GameState(players=[player])
        manager = LeaderManager(game_state)

        # This should work without error
        manager.check_unlock_conditions("player1")

    def test_ready_agents_method_exists(self) -> None:
        """Test that ready_agents method exists."""
        from src.ti4.core.leaders import LeaderManager

        # Create a player with leaders
        player = Player(id="player1", faction=Faction.ARBOREC)
        game_state = GameState(players=[player])
        manager = LeaderManager(game_state)

        # This should work without error
        manager.ready_agents("player1")

    def test_execute_leader_ability_method_exists(self) -> None:
        """Test that execute_leader_ability method exists."""
        from src.ti4.core.leaders import LeaderManager

        # Create a player with leaders
        player = Player(id="player1", faction=Faction.ARBOREC)
        game_state = GameState(players=[player])
        manager = LeaderManager(game_state)

        # This should work now that the method exists
        result = manager.execute_leader_ability("player1", "Agent")

        # Should return a LeaderAbilityResult
        assert hasattr(result, "success")
        assert hasattr(result, "effects")
        assert hasattr(result, "error_message")

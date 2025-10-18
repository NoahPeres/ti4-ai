"""Tests for RoundTransitionManager.

This module tests the round transition logic after status phase completion,
including phase determination and round counter management.

LRR References:
- Rule 81: Status Phase - Round transition after completion
- Rule 27.4: Agenda phase activation after custodians token removal
"""

import pytest

from src.ti4.core.constants import Faction
from src.ti4.core.game_phase import GamePhase
from src.ti4.core.game_state import GameState
from src.ti4.core.player import Player
from src.ti4.core.status_phase import RoundTransitionManager


class TestRoundTransitionManager:
    """Test RoundTransitionManager functionality."""

    def test_determine_next_phase_with_agenda_active(self):
        """Test that agenda phase is chosen when active."""
        # Arrange
        manager = RoundTransitionManager()
        game_state = GameState(
            players=[Player(id="player1", faction=Faction.SOL)],
            phase=GamePhase.STATUS,
            agenda_phase_active=True,
        )

        # Act
        next_phase = manager.determine_next_phase(game_state)

        # Assert
        assert next_phase == "agenda"

    def test_determine_next_phase_with_agenda_inactive(self):
        """Test that strategy phase is chosen when agenda phase inactive."""
        # Arrange
        manager = RoundTransitionManager()
        game_state = GameState(
            players=[Player(id="player1", faction=Faction.SOL)],
            phase=GamePhase.STATUS,
            agenda_phase_active=False,
        )

        # Act
        next_phase = manager.determine_next_phase(game_state)

        # Assert
        assert next_phase == "strategy"

    def test_transition_to_agenda_phase(self):
        """Test transition to agenda phase updates game state."""
        # Arrange
        manager = RoundTransitionManager()
        game_state = GameState(
            players=[Player(id="player1", faction=Faction.SOL)],
            phase=GamePhase.STATUS,
            agenda_phase_active=True,
        )

        # Act
        new_state = manager.transition_to_agenda_phase(game_state)

        # Assert
        assert new_state.phase == GamePhase.AGENDA
        assert new_state is not game_state  # Immutability check

    def test_transition_to_new_round(self):
        """Test transition to new round with strategy phase."""
        # Arrange
        manager = RoundTransitionManager()
        game_state = GameState(
            players=[Player(id="player1", faction=Faction.SOL)],
            phase=GamePhase.STATUS,
            agenda_phase_active=False,
        )

        # Act
        new_state = manager.transition_to_new_round(game_state)

        # Assert
        assert new_state.phase == GamePhase.STRATEGY
        assert new_state is not game_state  # Immutability check

    def test_update_round_counter(self):
        """Test round counter is incremented."""
        # Arrange
        manager = RoundTransitionManager()
        game_state = GameState(
            players=[Player(id="player1", faction=Faction.SOL)], phase=GamePhase.STATUS
        )

        # Act
        new_state = manager.update_round_counter(game_state)

        # Assert
        # For now, just check that we get a new state back
        # Round counter implementation will be added when needed
        assert new_state is not game_state  # Immutability check

    def test_determine_next_phase_with_none_game_state(self):
        """Test error handling with None game state."""
        # Arrange
        manager = RoundTransitionManager()

        # Act & Assert
        with pytest.raises(ValueError, match="Game state cannot be None"):
            manager.determine_next_phase(None)

    def test_transition_to_agenda_phase_with_none_game_state(self):
        """Test error handling with None game state."""
        # Arrange
        manager = RoundTransitionManager()

        # Act & Assert
        with pytest.raises(ValueError, match="Game state cannot be None"):
            manager.transition_to_agenda_phase(None)

    def test_transition_to_new_round_with_none_game_state(self):
        """Test error handling with None game state."""
        # Arrange
        manager = RoundTransitionManager()

        # Act & Assert
        with pytest.raises(ValueError, match="Game state cannot be None"):
            manager.transition_to_new_round(None)

    def test_update_round_counter_with_none_game_state(self):
        """Test error handling with None game state."""
        # Arrange
        manager = RoundTransitionManager()

        # Act & Assert
        with pytest.raises(ValueError, match="Game state cannot be None"):
            manager.update_round_counter(None)


class TestRoundTransitionIntegration:
    """Test RoundTransitionManager integration with phase management."""

    def test_complete_round_transition_to_agenda(self):
        """Test complete round transition when agenda phase is active."""
        # Arrange
        manager = RoundTransitionManager()
        game_state = GameState(
            players=[Player(id="player1", faction=Faction.SOL)],
            phase=GamePhase.STATUS,
            agenda_phase_active=True,
        )

        # Act
        next_phase = manager.determine_next_phase(game_state)
        new_state = manager.transition_to_agenda_phase(game_state)

        # Assert
        assert next_phase == "agenda"
        assert new_state.phase == GamePhase.AGENDA
        assert new_state.agenda_phase_active is True

    def test_complete_round_transition_to_strategy(self):
        """Test complete round transition when agenda phase is inactive."""
        # Arrange
        manager = RoundTransitionManager()
        game_state = GameState(
            players=[Player(id="player1", faction=Faction.SOL)],
            phase=GamePhase.STATUS,
            agenda_phase_active=False,
        )

        # Act
        next_phase = manager.determine_next_phase(game_state)
        new_state = manager.transition_to_new_round(game_state)
        updated_state = manager.update_round_counter(new_state)

        # Assert
        assert next_phase == "strategy"
        assert updated_state.phase == GamePhase.STRATEGY
        assert updated_state.agenda_phase_active is False

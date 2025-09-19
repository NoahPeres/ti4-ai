"""Tests for LegalMoveGenerator class."""

from typing import Any

from src.ti4.actions.action import PlayerDecision
from src.ti4.actions.legal_moves import LegalMoveGenerator
from src.ti4.core.constants import Faction
from src.ti4.core.game_state import GameState
from src.ti4.core.player import Player


def test_legal_move_generator_creation() -> None:
    """Test that LegalMoveGenerator can be created."""
    generator = LegalMoveGenerator()
    assert generator is not None


def test_generate_legal_actions_returns_list() -> None:
    """Test that generate_legal_actions returns a list of actions."""
    generator = LegalMoveGenerator()
    state = GameState()
    player = Player(id="player1", faction=Faction.SOL)

    actions = generator.generate_legal_actions(state, player.id)
    assert isinstance(actions, list)


def test_generate_legal_actions_filters_by_game_phase() -> None:
    """Test that legal actions are filtered by current game phase."""
    from src.ti4.core.game_phase import GamePhase

    generator = LegalMoveGenerator()
    state = GameState()
    player = Player(id="player1", faction=Faction.SOL)

    # Should return different actions for different phases
    setup_actions = generator.generate_legal_actions_for_phase(
        state, player.id, GamePhase.SETUP
    )
    assert isinstance(setup_actions, list)


def test_generate_legal_actions_empty_when_no_legal_moves() -> None:
    """Test that empty list is returned when no legal moves are available."""
    generator = LegalMoveGenerator()
    state = GameState()
    player = Player(id="player1", faction=Faction.SOL)

    # In a basic state with no actions available, should return empty list
    actions = generator.generate_legal_actions(state, player.id)
    assert actions == []


def test_generate_legal_actions_handles_invalid_player_id() -> None:
    """Test that generator handles invalid player IDs gracefully."""
    generator = LegalMoveGenerator()
    state = GameState()

    # Should return empty list for non-existent player
    actions = generator.generate_legal_actions(state, "non_existent_player")
    assert actions == []


def test_generate_legal_actions_integrates_with_validation_engine() -> None:
    """Test that generator uses validation engine to filter legal actions."""

    generator = LegalMoveGenerator()
    state = GameState()
    player = Player(id="player1", faction=Faction.SOL)

    # Create a mock action for testing
    class TestAction(PlayerDecision):
        def __init__(self, is_legal_result: bool = True) -> None:
            self._is_legal_result = is_legal_result

        def is_legal(self, state: Any, player_id: str) -> bool:
            return bool(self._is_legal_result)

        def execute(self, state: Any, player_id: str) -> Any:
            return state

        def get_description(self) -> str:
            return "test action"

    # Test that generator can filter actions based on legality
    legal_action = TestAction(is_legal_result=True)
    illegal_action = TestAction(is_legal_result=False)

    # Generator should be able to work with a list of potential actions
    potential_actions: list[PlayerDecision] = [legal_action, illegal_action]
    legal_actions = generator.filter_legal_actions(potential_actions, state, player.id)

    assert len(legal_actions) == 1
    assert legal_actions[0] == legal_action


def test_filter_legal_actions_handles_empty_list() -> None:
    """Test that filter_legal_actions handles empty input gracefully."""
    generator = LegalMoveGenerator()
    state = GameState()
    player = Player(id="player1", faction=Faction.SOL)

    # Should handle empty list gracefully
    legal_actions = generator.filter_legal_actions([], state, player.id)
    assert legal_actions == []

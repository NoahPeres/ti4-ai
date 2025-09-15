"""Tests for LegalMoveGenerator class."""


from src.ti4.actions.legal_moves import LegalMoveGenerator
from src.ti4.core.game_state import GameState
from src.ti4.core.player import Player


def test_legal_move_generator_creation():
    """Test that LegalMoveGenerator can be created."""
    generator = LegalMoveGenerator()
    assert generator is not None


def test_generate_legal_actions_returns_list():
    """Test that generate_legal_actions returns a list of actions."""
    generator = LegalMoveGenerator()
    state = GameState()
    player = Player(id="player1", faction="sol")

    actions = generator.generate_legal_actions(state, player.id)
    assert isinstance(actions, list)


def test_generate_legal_actions_filters_by_game_phase():
    """Test that legal actions are filtered by current game phase."""
    from src.ti4.core.game_phase import GamePhase

    generator = LegalMoveGenerator()
    state = GameState()
    player = Player(id="player1", faction="sol")

    # Should return different actions for different phases
    setup_actions = generator.generate_legal_actions_for_phase(
        state, player.id, GamePhase.SETUP
    )
    assert isinstance(setup_actions, list)


def test_generate_legal_actions_empty_when_no_legal_moves():
    """Test that empty list is returned when no legal moves are available."""
    generator = LegalMoveGenerator()
    state = GameState()
    player = Player(id="player1", faction="sol")

    # In a basic state with no actions available, should return empty list
    actions = generator.generate_legal_actions(state, player.id)
    assert actions == []


def test_generate_legal_actions_handles_invalid_player_id():
    """Test that generator handles invalid player IDs gracefully."""
    generator = LegalMoveGenerator()
    state = GameState()

    # Should return empty list for non-existent player
    actions = generator.generate_legal_actions(state, "non_existent_player")
    assert actions == []


def test_generate_legal_actions_integrates_with_validation_engine():
    """Test that generator uses validation engine to filter legal actions."""
    from src.ti4.actions.action import Action

    generator = LegalMoveGenerator()
    state = GameState()
    player = Player(id="player1", faction="sol")

    # Create a mock action for testing
    class TestAction(Action):
        def __init__(self, is_legal_result=True):
            self._is_legal_result = is_legal_result

        def is_legal(self, state, player_id) -> bool:
            return self._is_legal_result

        def execute(self, state, player_id):
            return state

        def get_description(self) -> str:
            return "test action"

    # Test that generator can filter actions based on legality
    legal_action = TestAction(is_legal_result=True)
    illegal_action = TestAction(is_legal_result=False)

    # Generator should be able to work with a list of potential actions
    potential_actions = [legal_action, illegal_action]
    legal_actions = generator.filter_legal_actions(potential_actions, state, player.id)

    assert len(legal_actions) == 1
    assert legal_actions[0] == legal_action


def test_filter_legal_actions_handles_empty_list():
    """Test that filter_legal_actions handles empty input gracefully."""
    generator = LegalMoveGenerator()
    state = GameState()
    player = Player(id="player1", faction="sol")

    # Should handle empty list gracefully
    legal_actions = generator.filter_legal_actions([], state, player.id)
    assert legal_actions == []

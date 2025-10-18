"""Tests for StatusPhaseValidator.

This module tests the validation logic for status phase operations,
including game state validation, step prerequisite validation, and
specific validation for objective scoring and token redistribution.

LRR References:
- Rule 81: Status Phase - Validation requirements
- Rule 11: Error Handling and Validation requirements
"""

from unittest.mock import Mock

import pytest

from src.ti4.core.game_state import GameState
from src.ti4.core.objective import ObjectiveCard
from src.ti4.core.player import Player
from src.ti4.core.status_phase import StatusPhaseGameStateError, StatusPhaseValidator


class TestStatusPhaseValidator:
    """Test StatusPhaseValidator validation logic."""

    def setup_method(self):
        """Set up test fixtures."""
        self.validator = StatusPhaseValidator()

        # Create mock game state
        self.mock_game_state = Mock(spec=GameState)
        self.mock_game_state.players = [
            Mock(spec=Player, id="player1"),
            Mock(spec=Player, id="player2"),
        ]
        self.mock_game_state.speaker_id = "player1"
        self.mock_game_state.systems = {}

    def test_validate_game_state_for_status_phase_with_valid_state(self):
        """Test game state validation with valid state."""
        # Act
        result = self.validator.validate_game_state_for_status_phase(
            self.mock_game_state
        )

        # Assert
        assert result is True

    def test_validate_game_state_for_status_phase_with_none_state(self):
        """Test game state validation with None state."""
        # Act & Assert
        with pytest.raises(
            StatusPhaseGameStateError, match="Game state cannot be None"
        ):
            self.validator.validate_game_state_for_status_phase(None)

    def test_validate_game_state_for_status_phase_with_no_players(self):
        """Test game state validation with no players."""
        # Arrange
        self.mock_game_state.players = []

        # Act & Assert
        with pytest.raises(
            StatusPhaseGameStateError, match="Game must have at least one player"
        ):
            self.validator.validate_game_state_for_status_phase(self.mock_game_state)

    def test_validate_step_prerequisites_valid_step_number(self):
        """Test step prerequisite validation with valid step number."""
        # Act
        is_valid, error_message = self.validator.validate_step_prerequisites(
            1, self.mock_game_state
        )

        # Assert
        assert is_valid is True
        assert error_message == ""

    def test_validate_step_prerequisites_invalid_step_number_low(self):
        """Test step prerequisite validation with invalid step number (too low)."""
        # Act
        is_valid, error_message = self.validator.validate_step_prerequisites(
            0, self.mock_game_state
        )

        # Assert
        assert is_valid is False
        assert "Invalid step number: 0" in error_message

    def test_validate_step_prerequisites_invalid_step_number_high(self):
        """Test step prerequisite validation with invalid step number (too high)."""
        # Act
        is_valid, error_message = self.validator.validate_step_prerequisites(
            9, self.mock_game_state
        )

        # Assert
        assert is_valid is False
        assert "Invalid step number: 9" in error_message

    def test_validate_step_prerequisites_step_2_requires_speaker(self):
        """Test step 2 prerequisite validation requires speaker."""
        # Arrange
        self.mock_game_state.speaker_id = None

        # Act
        is_valid, error_message = self.validator.validate_step_prerequisites(
            2, self.mock_game_state
        )

        # Assert
        assert is_valid is False
        assert "Step 2 requires a speaker" in error_message

    def test_validate_objective_scoring_valid_player_and_objective(self):
        """Test objective scoring validation with valid player and objective."""
        # Arrange
        mock_objective = Mock(spec=ObjectiveCard)
        mock_objective.name = "Test Objective"

        # Act
        result = self.validator.validate_objective_scoring(
            "player1", mock_objective, self.mock_game_state
        )

        # Assert
        assert result is True

    def test_validate_objective_scoring_invalid_player_id(self):
        """Test objective scoring validation with invalid player ID."""
        # Arrange
        mock_objective = Mock(spec=ObjectiveCard)

        # Act
        result = self.validator.validate_objective_scoring(
            "invalid_player", mock_objective, self.mock_game_state
        )

        # Assert
        assert result is False

    def test_validate_objective_scoring_none_objective(self):
        """Test objective scoring validation with None objective."""
        # Act
        result = self.validator.validate_objective_scoring(
            "player1", None, self.mock_game_state
        )

        # Assert
        assert result is False

    def test_validate_token_redistribution_valid_distribution(self):
        """Test token redistribution validation with valid distribution."""
        # Arrange
        distribution = {"strategy": 2, "tactic": 3, "fleet": 1}

        # Act
        result = self.validator.validate_token_redistribution(
            "player1", distribution, self.mock_game_state
        )

        # Assert
        assert result is True

    def test_validate_token_redistribution_invalid_player_id(self):
        """Test token redistribution validation with invalid player ID."""
        # Arrange
        distribution = {"strategy": 2, "tactic": 3, "fleet": 1}

        # Act
        result = self.validator.validate_token_redistribution(
            "invalid_player", distribution, self.mock_game_state
        )

        # Assert
        assert result is False

    def test_validate_token_redistribution_negative_tokens(self):
        """Test token redistribution validation with negative tokens."""
        # Arrange
        distribution = {"strategy": -1, "tactic": 3, "fleet": 1}

        # Act
        result = self.validator.validate_token_redistribution(
            "player1", distribution, self.mock_game_state
        )

        # Assert
        assert result is False

    def test_validate_token_redistribution_invalid_pool_name(self):
        """Test token redistribution validation with invalid pool name."""
        # Arrange
        distribution = {"invalid_pool": 2, "tactic": 3, "fleet": 1}

        # Act
        result = self.validator.validate_token_redistribution(
            "player1", distribution, self.mock_game_state
        )

        # Assert
        assert result is False

    def test_validate_token_redistribution_empty_distribution(self):
        """Test token redistribution validation with empty distribution."""
        # Arrange
        distribution = {}

        # Act
        result = self.validator.validate_token_redistribution(
            "player1", distribution, self.mock_game_state
        )

        # Assert
        assert result is True  # Empty distribution should be valid

    def test_validate_token_redistribution_non_integer_values(self):
        """Test token redistribution validation with non-integer values."""
        # Arrange
        distribution = {"strategy": 2.5, "tactic": 3, "fleet": 1}

        # Act
        result = self.validator.validate_token_redistribution(
            "player1", distribution, self.mock_game_state
        )

        # Assert
        assert result is False

    def test_validate_step_prerequisites_all_valid_steps(self):
        """Test step prerequisite validation for all valid step numbers."""
        # Act & Assert
        for step_number in range(1, 9):
            is_valid, error_message = self.validator.validate_step_prerequisites(
                step_number, self.mock_game_state
            )
            assert is_valid is True, f"Step {step_number} should be valid"
            assert error_message == "", (
                f"Step {step_number} should have no error message"
            )

    def test_validate_objective_scoring_empty_player_id(self):
        """Test objective scoring validation with empty player ID."""
        # Arrange
        mock_objective = Mock(spec=ObjectiveCard)

        # Act
        result = self.validator.validate_objective_scoring(
            "", mock_objective, self.mock_game_state
        )

        # Assert
        assert result is False

    def test_validate_objective_scoring_whitespace_player_id(self):
        """Test objective scoring validation with whitespace-only player ID."""
        # Arrange
        mock_objective = Mock(spec=ObjectiveCard)

        # Act
        result = self.validator.validate_objective_scoring(
            "   ", mock_objective, self.mock_game_state
        )

        # Assert
        assert result is False

    def test_validate_token_redistribution_empty_player_id(self):
        """Test token redistribution validation with empty player ID."""
        # Arrange
        distribution = {"strategy": 2, "tactic": 3, "fleet": 1}

        # Act
        result = self.validator.validate_token_redistribution(
            "", distribution, self.mock_game_state
        )

        # Assert
        assert result is False

    def test_validate_token_redistribution_whitespace_player_id(self):
        """Test token redistribution validation with whitespace-only player ID."""
        # Arrange
        distribution = {"strategy": 2, "tactic": 3, "fleet": 1}

        # Act
        result = self.validator.validate_token_redistribution(
            "   ", distribution, self.mock_game_state
        )

        # Assert
        assert result is False

    def test_validator_constants_are_defined(self):
        """Test that validator constants are properly defined."""
        # Assert
        assert hasattr(self.validator, "VALID_STEP_NUMBERS")
        assert hasattr(self.validator, "VALID_TOKEN_POOLS")
        assert self.validator.VALID_STEP_NUMBERS == range(1, 9)
        assert self.validator.VALID_TOKEN_POOLS == {"strategy", "tactic", "fleet"}

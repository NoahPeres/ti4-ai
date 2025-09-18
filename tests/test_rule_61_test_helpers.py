"""Helper functions and fixtures for Rule 61 objective tests."""

import pytest
from typing import Optional

from src.ti4.core.game_phase import GamePhase
from src.ti4.core.game_state import GameState
from src.ti4.core.objective import Objective


class ObjectiveTestHelpers:
    """Helper class for creating common test objectives and game states."""

    @staticmethod
    def create_public_objective(
        obj_id: str, name: str, phase: GamePhase, points: int = 1
    ) -> Objective:
        """Create a public objective for testing."""
        return Objective(
            id=obj_id,
            name=name,
            description=f"{name} description",
            points=points,
            is_public=True,
            scoring_phase=phase,
        )

    @staticmethod
    def create_secret_objective(
        obj_id: str, name: str, phase: GamePhase, points: int = 1
    ) -> Objective:
        """Create a secret objective for testing."""
        return Objective(
            id=obj_id,
            name=name,
            description=f"{name} description",
            points=points,
            is_public=False,
            scoring_phase=phase,
        )

    @staticmethod
    def create_game_state_with_secret_objectives(
        player_id: str, secret_objectives: list[Objective]
    ) -> GameState:
        """Create a game state with secret objectives assigned to a player."""
        game_state = GameState()
        for secret_obj in secret_objectives:
            game_state = game_state.assign_secret_objective(player_id, secret_obj)
        return game_state

    @staticmethod
    def create_standard_objectives() -> dict[str, Objective]:
        """Create a standard set of objectives for testing."""
        return {
            "status_public": ObjectiveTestHelpers.create_public_objective(
                "status_pub", "Status Public", GamePhase.STATUS
            ),
            "status_secret": ObjectiveTestHelpers.create_secret_objective(
                "status_sec", "Status Secret", GamePhase.STATUS
            ),
            "action_public": ObjectiveTestHelpers.create_public_objective(
                "action_pub", "Action Public", GamePhase.ACTION
            ),
            "action_secret": ObjectiveTestHelpers.create_secret_objective(
                "action_sec", "Action Secret", GamePhase.ACTION
            ),
            "agenda_public": ObjectiveTestHelpers.create_public_objective(
                "agenda_pub", "Agenda Public", GamePhase.AGENDA
            ),
            "agenda_secret": ObjectiveTestHelpers.create_secret_objective(
                "agenda_sec", "Agenda Secret", GamePhase.AGENDA
            ),
        }


@pytest.fixture
def game_state():
    """Fixture providing a fresh GameState for each test."""
    return GameState()


@pytest.fixture
def standard_objectives():
    """Fixture providing standard test objectives."""
    return ObjectiveTestHelpers.create_standard_objectives()


@pytest.fixture
def player_with_secrets(game_state, standard_objectives):
    """Fixture providing a game state with secret objectives assigned to player1."""
    secret_objs = [
        standard_objectives["status_secret"],
        standard_objectives["action_secret"],
        standard_objectives["agenda_secret"],
    ]
    return ObjectiveTestHelpers.create_game_state_with_secret_objectives(
        "player1", secret_objs
    )


def assert_objective_scored(
    game_state: GameState,
    player_id: str,
    objective: Objective,
    expected_points: Optional[int] = None,
) -> None:
    """Helper assertion for verifying objective scoring."""
    assert game_state.is_objective_completed(player_id, objective)
    if expected_points is not None:
        assert game_state.get_victory_points(player_id) == expected_points


def assert_scoring_fails(
    game_state: GameState,
    player_id: str,
    objective: Objective,
    phase: GamePhase,
    error_pattern: str,
) -> None:
    """Helper assertion for verifying scoring failures."""
    with pytest.raises(ValueError, match=error_pattern):
        game_state.score_objective(player_id, objective, phase)
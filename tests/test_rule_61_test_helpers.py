"""Test helpers for Rule 61: OBJECTIVE CARDS tests."""

import pytest

from ti4.core.constants import Expansion, Faction
from ti4.core.game_phase import GamePhase
from ti4.core.game_state import GameState
from ti4.core.objective import (
    ObjectiveCard,
    ObjectiveCategory,
    ObjectiveType,
)
from ti4.core.player import Player


class ObjectiveTestHelpers:
    """Helper class for creating common test objectives and game states."""

    @staticmethod
    def create_public_objective(
        obj_id: str, name: str, phase: GamePhase, points=1
    ) -> ObjectiveCard:
        """Create a public objective for testing."""
        return ObjectiveCard(
            id=obj_id,
            name=name,
            condition=f"{name} description",
            points=points,
            expansion=Expansion.BASE,
            phase=phase,
            type=ObjectiveType.PUBLIC_STAGE_I,
            requirement_validator=lambda player_id,
            game_state: True,  # Always pass for tests
            category=ObjectiveCategory.SPECIAL,
            dependencies=[],
        )

    @staticmethod
    def create_secret_objective(
        obj_id: str, name: str, phase: GamePhase, points=1
    ) -> ObjectiveCard:
        """Create a secret objective for testing."""
        return ObjectiveCard(
            id=obj_id,
            name=name,
            condition=f"{name} description",
            points=points,
            expansion=Expansion.BASE,
            phase=phase,
            type=ObjectiveType.SECRET,
            requirement_validator=lambda player_id,
            game_state: True,  # Always pass for tests
            category=ObjectiveCategory.SPECIAL,
            dependencies=[],
        )

    @staticmethod
    def create_game_state_with_secret_objectives(
        player_id: str, secret_objectives: list[ObjectiveCard]
    ) -> GameState:
        """Create a game state with secret objectives assigned to a player."""
        game_state = GameState().add_player(Player(player_id, Faction.SOL))
        for secret_obj in secret_objectives:
            game_state = game_state.assign_secret_objective(player_id, secret_obj)
        return game_state

    @staticmethod
    def create_game_state_with_galaxy_for_public_objectives(
        player_id: str,
    ) -> GameState:
        """Create a game state with galaxy and home system for public objective testing."""
        from ti4.core.galaxy import Galaxy
        from ti4.core.planet import Planet
        from ti4.core.system import System

        player = Player(player_id, Faction.SOL)

        # Create home system with controlled planet
        home_system_id = f"home_system_{player_id.split('player')[-1]}"
        home_system = System(home_system_id)
        home_planet = Planet("Jord", resources=4, influence=2)
        home_planet.set_control(player_id)  # Player controls the planet
        home_system.add_planet(home_planet)

        galaxy = Galaxy()
        galaxy.register_system(home_system)

        return GameState(players=[player], galaxy=galaxy)

    @staticmethod
    def create_standard_objectives() -> dict[str, ObjectiveCard]:
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
def game_state() -> GameState:
    """Fixture providing a fresh GameState for each test."""
    return GameState().add_player(Player("player1", Faction.SOL))


@pytest.fixture
def standard_objectives() -> None:
    """Fixture providing standard test objectives."""
    return ObjectiveTestHelpers.create_standard_objectives()


@pytest.fixture
def player_with_secrets(game_state, standard_objectives) -> None:
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
    objective: ObjectiveCard,
    expected_points: int | None = None,
) -> None:
    """Helper assertion for verifying objective scoring."""
    assert game_state.is_objective_completed(player_id, objective)
    if expected_points is not None:
        assert game_state.get_victory_points(player_id) == expected_points


def assert_scoring_fails(
    game_state: GameState,
    player_id: str,
    objective: ObjectiveCard,
    phase: GamePhase,
    error_pattern: str,
) -> None:
    """Helper assertion for verifying scoring failures."""
    with pytest.raises((ValueError, Exception), match=error_pattern):
        game_state.score_objective(player_id, objective, phase)

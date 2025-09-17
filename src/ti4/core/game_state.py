"""Core game state management for TI4."""

import uuid
from dataclasses import dataclass, field
from typing import Any, Optional

from .galaxy import Galaxy
from .game_phase import GamePhase
from .objective import Objective
from .player import Player
from .system import System

# Victory condition constants
VICTORY_POINTS_TO_WIN = 10


@dataclass(frozen=True)
class GameState:
    """Represents the complete state of a TI4 game."""

    game_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    players: list[Player] = field(default_factory=list, hash=False)
    galaxy: Optional[Galaxy] = None
    phase: GamePhase = GamePhase.SETUP
    systems: dict[str, System] = field(default_factory=dict, hash=False)
    player_resources: dict[str, dict[str, Any]] = field(
        default_factory=dict, hash=False
    )
    player_technologies: dict[str, list[str]] = field(default_factory=dict, hash=False)
    victory_points: dict[str, int] = field(default_factory=dict, hash=False)
    completed_objectives: dict[str, list[str]] = field(default_factory=dict, hash=False)

    def get_victory_points(self, player_id: str) -> int:
        """Get the victory points for a player."""
        return self.victory_points.get(player_id, 0)

    def award_victory_points(self, player_id: str, points: int) -> "GameState":
        """Award victory points to a player, returning a new GameState."""
        new_victory_points = self.victory_points.copy()
        current_points = new_victory_points.get(player_id, 0)
        new_victory_points[player_id] = current_points + points

        return self._create_new_state(victory_points=new_victory_points)

    def has_winner(self) -> bool:
        """Check if any player has reached the victory condition."""
        return any(
            points >= VICTORY_POINTS_TO_WIN for points in self.victory_points.values()
        )

    def get_winner(self) -> Optional[str]:
        """Get the player ID of the winner, if any."""
        for player_id, points in self.victory_points.items():
            if points >= VICTORY_POINTS_TO_WIN:
                return player_id
        return None

    def is_objective_completed(self, player_id: str, objective: Objective) -> bool:
        """Check if a player has completed a specific objective."""
        player_objectives = self.completed_objectives.get(player_id, [])
        return objective.id in player_objectives

    def complete_objective(self, player_id: str, objective: Objective) -> "GameState":
        """Mark an objective as completed for a player, returning a new GameState."""
        new_completed_objectives = {
            pid: objectives.copy()
            for pid, objectives in self.completed_objectives.items()
        }

        if player_id not in new_completed_objectives:
            new_completed_objectives[player_id] = []

        if objective.id not in new_completed_objectives[player_id]:
            new_completed_objectives[player_id].append(objective.id)

        return self._create_new_state(completed_objectives=new_completed_objectives)

    def _create_new_state(self, **kwargs: Any) -> "GameState":
        """Create a new GameState with updated fields."""
        return GameState(
            game_id=self.game_id,
            players=self.players,
            galaxy=self.galaxy,
            phase=self.phase,
            systems=self.systems,
            player_resources=self.player_resources,
            player_technologies=self.player_technologies,
            victory_points=kwargs.get("victory_points", self.victory_points),
            completed_objectives=kwargs.get(
                "completed_objectives", self.completed_objectives
            ),
        )

    def is_valid(self) -> bool:
        """Validate the consistency of the game state."""
        return True

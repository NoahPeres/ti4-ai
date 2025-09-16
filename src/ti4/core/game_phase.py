"""Game phase management for TI4."""

from enum import Enum


class GamePhase(Enum):
    """Represents the different phases of a TI4 game."""

    SETUP = "setup"
    STRATEGY = "strategy"
    ACTION = "action"


def is_valid_transition(from_phase: GamePhase, to_phase: GamePhase) -> bool:
    """Check if a phase transition is valid."""
    # Can't transition to the same phase
    return from_phase != to_phase

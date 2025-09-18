"""Custom exceptions for TI4 game framework."""

import time
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ..commands.base import GameCommand
    from .game_phase import GamePhase


class TI4GameError(Exception):
    """Base exception for TI4 game-related errors with enhanced context."""

    def __init__(
        self,
        message: str,
        context: Optional[dict[str, Any]] = None,
        cause: Optional[Exception] = None,
    ) -> None:
        super().__init__(message)
        self.context = context or {}
        self.timestamp = time.time()

        if cause is not None:
            self.__cause__ = cause


class CommandExecutionError(TI4GameError):
    """Raised when command execution fails."""

    def __init__(
        self,
        command: "GameCommand",
        reason: str,
        context: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(f"Command execution failed: {reason}", context)
        self.command = command


class PhaseTransitionError(TI4GameError):
    """Raised when invalid phase transition is attempted."""

    def __init__(
        self,
        from_phase: "GamePhase",
        to_phase: "GamePhase",
        context: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(f"Invalid transition from {from_phase} to {to_phase}", context)
        self.from_phase = from_phase
        self.to_phase = to_phase


class InvalidPlayerError(TI4GameError):
    """Raised when an invalid player is referenced."""

    pass


class InvalidMovementError(TI4GameError):
    """Raised when an invalid movement is attempted."""

    pass


class InvalidPhaseTransitionError(TI4GameError):
    """Raised when an invalid phase transition is attempted."""

    pass


class FleetCapacityError(TI4GameError):
    """Raised when fleet capacity rules are violated."""

    pass


class FleetSupplyError(TI4GameError):
    """Raised when fleet supply (command token) limits are exceeded."""

    pass


class InvalidUnitTypeError(TI4GameError):
    """Raised when an unknown unit type is referenced."""

    pass


class InvalidSystemError(TI4GameError):
    """Raised when an invalid system is referenced."""

    pass


class CombatError(TI4GameError):
    """Raised when combat-related errors occur."""

    pass

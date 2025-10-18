"""
Core exceptions for the TI4 game system.
"""

import time
from typing import Any

# Re-export ValidationError from the validation module to avoid duplication and API drift
from .validation import ValidationError  # noqa: F401


class TI4Error(Exception):
    """Base exception for all TI4 game errors."""

    pass


class TI4GameError(TI4Error):
    """Legacy alias for TI4Error to maintain compatibility."""

    def __init__(
        self,
        message: str,
        context: dict[str, Any] | None = None,
        cause: Exception | None = None,
    ):
        super().__init__(message)
        self.context = context or {}
        self.timestamp = time.time()
        if cause:
            self.__cause__ = cause


class InvalidPlayerError(TI4Error):
    """Raised when an invalid player is referenced."""

    pass


class InvalidPhaseError(TI4Error):
    """Raised when an action is attempted in the wrong phase."""

    pass


class InvalidActionError(TI4Error):
    """Raised when an invalid action is attempted."""

    pass


class GameStateError(TI4Error):
    """Raised when the game state is invalid."""

    pass


class AbilityError(TI4Error):
    """Base exception for ability-related errors."""

    pass


class InvalidAbilityError(AbilityError):
    """Raised when an ability is invalid or cannot be resolved."""

    pass


class AbilityCostError(AbilityError):
    """Raised when an ability's cost cannot be paid."""

    pass


class AbilityPrecedenceError(AbilityError):
    """Raised when ability precedence rules are violated."""

    pass


class CommandExecutionError(TI4Error):
    """Raised when command execution fails."""

    def __init__(
        self,
        command: Any,
        reason: str,
        context: dict[str, Any] | None = None,
        cause: Exception | None = None,
    ):
        self.command = command
        self.reason = reason
        self.context = context or {}
        self.timestamp = time.time()  # Set timestamp when error occurs
        self.cause = cause  # Store the original exception for chaining

        # Build error message without timestamp for consistency with tests
        message = f"Command execution failed: {reason}"

        # Chain the cause if provided
        super().__init__(message)
        if cause:
            self.__cause__ = cause


class PhaseTransitionError(TI4Error):
    """Raised when a phase transition fails."""

    def __init__(
        self, from_phase: Any, to_phase: Any, context: dict[str, Any] | None = None
    ):
        self.from_phase = from_phase
        self.to_phase = to_phase
        self.context = context or {}
        self.timestamp = time.time()

        # Build simple error message to match test expectations
        message = f"Invalid transition from {from_phase} to {to_phase}"

        super().__init__(message)


class FleetCapacityError(TI4Error):
    """Raised when fleet capacity is exceeded."""

    pass


class StrategyCardStateError(TI4Error):
    """Raised when strategy card state is inconsistent."""

    def __init__(self, message: str, context: dict[str, Any] | None = None):
        super().__init__(message)
        self.context = context or {}


class InvalidSystemError(TI4Error):
    """Raised when an invalid system is referenced."""

    pass


class DeployError(AbilityError):
    """Raised when deploy ability usage fails validation."""

    pass


class ReinforcementError(AbilityError):
    """Raised when reinforcement requirements are not met."""

    pass


# Anomaly-related exceptions
class AnomalyMovementError(TI4Error):
    """Raised when movement is blocked by anomaly rules."""

    pass


class InvalidAnomalyTypeError(TI4Error):
    """Raised when an invalid anomaly type is specified."""

    pass


class GravityRiftDestructionError(TI4Error):
    """Raised when gravity rift destruction occurs."""

    pass


class AnomalyStateConsistencyError(TI4Error):
    """Raised when anomaly system state is inconsistent."""

    pass


# Combat-related exceptions
class InvalidCombatStateError(TI4Error):
    """Raised when combat state is invalid or inconsistent."""

    pass


class InvalidGameStateError(TI4Error):
    """Raised when game state is invalid or corrupted."""

    pass

"""Custom exceptions for TI4 game framework."""


class TI4GameError(Exception):
    """Base exception for TI4 game-related errors."""

    pass


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

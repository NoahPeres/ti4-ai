"""
Agenda card framework for TI4 AI system.

This module provides the complete agenda card system including base classes,
registry, deck management, and concrete implementations for all TI4 agenda cards.
"""

from .base import BaseAgendaCard, DirectiveCard, LawCard
from .deck import AgendaDeck, AgendaDeckEmptyError
from .exceptions import (
    AgendaCardNotFoundError,
    AgendaCardOperationError,
    AgendaCardRegistrationError,
    AgendaCardValidationError,
)
from .law_manager import ActiveLaw, GameContext, LawManager
from .registry import AgendaCardRegistry
from .validation import (
    ActionValidationResult,
    AgendaCardValidator,
    AgendaEffectValidator,
    ValidationResult,
)

__all__ = [
    "BaseAgendaCard",
    "DirectiveCard",
    "LawCard",
    "AgendaCardRegistry",
    "AgendaDeck",
    "AgendaDeckEmptyError",
    "ActiveLaw",
    "GameContext",
    "LawManager",
    "AgendaCardValidationError",
    "AgendaCardOperationError",
    "AgendaCardNotFoundError",
    "AgendaCardRegistrationError",
    "AgendaCardValidator",
    "ValidationResult",
    "AgendaEffectValidator",
    "ActionValidationResult",
]

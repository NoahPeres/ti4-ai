"""Backward compatibility import for strategic action system.

This module maintains backward compatibility for existing imports.
New code should import from src.ti4.core.strategy_cards.strategic_action
"""

# Backward compatibility imports
from .strategy_cards.strategic_action import (
    SecondaryAbilityResult,
    StrategicActionManager,
    StrategicActionResult,
    StrategyCard,
    StrategyCardType,
)

__all__ = [
    "SecondaryAbilityResult",
    "StrategicActionManager",
    "StrategicActionResult",
    "StrategyCard",
    "StrategyCardType",
]

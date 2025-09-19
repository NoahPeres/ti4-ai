"""Backward compatibility import for BaseStrategyCard.

This module maintains backward compatibility for existing imports.
New code should import from src.ti4.core.strategy_cards.base_strategy_card
"""

# Backward compatibility imports
from .strategy_cards.base_strategy_card import (
    BaseStrategyCard,
    StrategyCardAbilityResult,
)

__all__ = ["BaseStrategyCard", "StrategyCardAbilityResult"]

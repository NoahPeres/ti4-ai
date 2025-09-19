"""Backward compatibility import for strategy card actions.

This module maintains backward compatibility for existing imports.
New code should import from src.ti4.core.strategy_cards.actions.strategy_card_actions
"""

# Backward compatibility imports
from src.ti4.core.strategy_cards.actions.strategy_card_actions import (
    SecondaryAbilityDecision,
    StrategyCardActivationDecision,
    StrategyCardSelectionDecision,
)

__all__ = [
    "SecondaryAbilityDecision",
    "StrategyCardActivationDecision",
    "StrategyCardSelectionDecision",
]

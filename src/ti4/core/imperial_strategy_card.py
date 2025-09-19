"""Backward compatibility import for ImperialStrategyCard.

This module maintains backward compatibility for existing imports.
New code should import from src.ti4.core.strategy_cards.cards.imperial
"""

# Backward compatibility imports
from .strategy_cards.cards.imperial import ImperialStrategyCard

__all__ = ["ImperialStrategyCard"]

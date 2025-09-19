"""Backward compatibility import for WarfareStrategyCard.

This module maintains backward compatibility for existing imports.
New code should import from src.ti4.core.strategy_cards.cards.warfare
"""

# Backward compatibility imports
from .strategy_cards.cards.warfare import WarfareStrategyCard

__all__ = ["WarfareStrategyCard"]

"""Backward compatibility import for TradeStrategyCard.

This module maintains backward compatibility for existing imports.
New code should import from src.ti4.core.strategy_cards.cards.trade
"""

# Backward compatibility imports
from .strategy_cards.cards.trade import TradeStrategyCard

__all__ = ["TradeStrategyCard"]

"""Backward compatibility import for PoliticsStrategyCard.

This module maintains backward compatibility for existing imports.
New code should import from src.ti4.core.strategy_cards.cards.politics
"""

# Backward compatibility imports
from .strategy_cards.cards.politics import PoliticsStrategyCard

__all__ = ["PoliticsStrategyCard"]

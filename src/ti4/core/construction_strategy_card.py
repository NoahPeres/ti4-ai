"""Backward compatibility import for ConstructionStrategyCard.

This module maintains backward compatibility for existing imports.
New code should import from src.ti4.core.strategy_cards.cards.construction
"""

# Backward compatibility imports
from .strategy_cards.cards.construction import ConstructionStrategyCard

__all__ = ["ConstructionStrategyCard"]

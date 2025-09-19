"""Backward compatibility import for strategy card registry.

This module maintains backward compatibility for existing imports.
New code should import from src.ti4.core.strategy_cards.registry
"""

# Backward compatibility imports
from .strategy_cards.registry import StrategyCardRegistry

__all__ = ["StrategyCardRegistry"]

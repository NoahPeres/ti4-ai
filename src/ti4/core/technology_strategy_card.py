"""Backward compatibility import for TechnologyStrategyCard.

This module maintains backward compatibility for existing imports.
New code should import from src.ti4.core.strategy_cards.cards.technology
"""

# Backward compatibility imports
from .strategy_cards.cards.technology import TechnologyStrategyCard

__all__ = ["TechnologyStrategyCard"]

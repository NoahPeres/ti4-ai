"""Backward compatibility import for DiplomacyStrategyCard.

This module maintains backward compatibility for existing imports.
New code should import from src.ti4.core.strategy_cards.cards.diplomacy
"""

# Backward compatibility imports
from .strategy_cards.cards.diplomacy import DiplomacyStrategyCard

__all__ = ["DiplomacyStrategyCard"]

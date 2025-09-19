"""Backward compatibility import for LeadershipStrategyCard.

This module maintains backward compatibility for existing imports.
New code should import from src.ti4.core.strategy_cards.cards.leadership
"""

# Backward compatibility imports
from .strategy_cards.cards.leadership import LeadershipStrategyCard

__all__ = ["LeadershipStrategyCard"]

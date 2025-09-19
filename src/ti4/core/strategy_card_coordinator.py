"""Backward compatibility import for strategy card coordinator.

This module maintains backward compatibility for existing imports.
New code should import from src.ti4.core.strategy_cards.coordinator
"""

# Backward compatibility imports
from .strategy_cards.coordinator import (
    SecondaryAbilityOpportunity,
    StrategyCardAssignmentResult,
    StrategyCardCoordinator,
    StrategyCardEvaluationData,
    StrategyCardGameStateAnalysis,
    StrategyCardInformation,
)

__all__ = [
    "StrategyCardCoordinator",
    "StrategyCardInformation",
    "StrategyCardGameStateAnalysis",
    "StrategyCardEvaluationData",
    "SecondaryAbilityOpportunity",
    "StrategyCardAssignmentResult",
]

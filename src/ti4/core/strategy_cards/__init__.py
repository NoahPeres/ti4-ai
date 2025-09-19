"""Strategy card system for TI4.

This module contains all strategy card related functionality including:
- Base strategy card classes
- Individual strategy card implementations
- Strategy card coordinator and registry
- Strategic action management
"""

# Core strategy card components
# Strategy card actions
from .actions.strategy_card_actions import (
    SecondaryAbilityDecision,
    StrategyCardActivationDecision,
    StrategyCardSelectionDecision,
)
from .base_strategy_card import BaseStrategyCard, StrategyCardAbilityResult

# Individual strategy cards
from .cards.construction import ConstructionStrategyCard
from .cards.diplomacy import DiplomacyStrategyCard
from .cards.imperial import ImperialStrategyCard
from .cards.leadership import LeadershipStrategyCard
from .cards.politics import PoliticsStrategyCard
from .cards.technology import TechnologyStrategyCard
from .cards.trade import TradeStrategyCard
from .cards.warfare import WarfareStrategyCard
from .coordinator import StrategyCardCoordinator
from .registry import StrategyCardRegistry
from .strategic_action import (
    StrategicActionManager,
    StrategicActionResult,
    StrategyCard,
    StrategyCardType,
)

__all__ = [
    # Core components
    "BaseStrategyCard",
    "StrategyCardAbilityResult",
    "StrategyCardCoordinator",
    "StrategyCardRegistry",
    "StrategicActionManager",
    "StrategicActionResult",
    "StrategyCard",
    "StrategyCardType",
    # Individual cards
    "ConstructionStrategyCard",
    "DiplomacyStrategyCard",
    "ImperialStrategyCard",
    "LeadershipStrategyCard",
    "PoliticsStrategyCard",
    "TechnologyStrategyCard",
    "TradeStrategyCard",
    "WarfareStrategyCard",
    # Actions
    "SecondaryAbilityDecision",
    "StrategyCardActivationDecision",
    "StrategyCardSelectionDecision",
]

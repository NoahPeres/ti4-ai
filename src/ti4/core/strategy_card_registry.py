"""Strategy card registry system for TI4.

This module implements the registry system for all 8 strategy cards,
following the established patterns and providing centralized access.

LRR Reference: Rule 83 - STRATEGY CARD
"""

from typing import Optional

from .base_strategy_card import BaseStrategyCard
from .strategic_action import StrategyCardType


class StrategyCardRegistry:
    """Registry system for all 8 strategy cards.

    Provides centralized access to strategy card implementations
    following the established patterns.

    Requirements: 5.7 - Strategy card registry system for all 8 cards
    """

    def __init__(self) -> None:
        """Initialize the strategy card registry."""
        self._cards: dict[StrategyCardType, BaseStrategyCard] = {}
        self._initialize_cards()

    def _initialize_cards(self) -> None:
        """Initialize all strategy card implementations."""
        # Import individual strategy cards
        from .construction_strategy_card import ConstructionStrategyCard
        from .diplomacy_strategy_card import DiplomacyStrategyCard
        from .imperial_strategy_card import ImperialStrategyCard
        from .leadership_strategy_card import LeadershipStrategyCard
        from .politics_strategy_card import PoliticsStrategyCard
        from .technology_strategy_card_wrapper import TechnologyStrategyCard
        from .trade_strategy_card import TradeStrategyCard
        from .warfare_strategy_card import WarfareStrategyCard

        # Register all cards
        self._cards[StrategyCardType.LEADERSHIP] = LeadershipStrategyCard()
        self._cards[StrategyCardType.DIPLOMACY] = DiplomacyStrategyCard()
        self._cards[StrategyCardType.POLITICS] = PoliticsStrategyCard()
        self._cards[StrategyCardType.CONSTRUCTION] = ConstructionStrategyCard()
        self._cards[StrategyCardType.TRADE] = TradeStrategyCard()
        self._cards[StrategyCardType.WARFARE] = WarfareStrategyCard()
        self._cards[StrategyCardType.TECHNOLOGY] = TechnologyStrategyCard()
        self._cards[StrategyCardType.IMPERIAL] = ImperialStrategyCard()

    def get_card(self, card_type: StrategyCardType) -> Optional[BaseStrategyCard]:
        """Get a strategy card by type.

        Args:
            card_type: The strategy card type to retrieve

        Returns:
            The strategy card implementation or None if not found

        Requirements: 5.7 - Registry system for card access
        """
        return self._cards.get(card_type)

    def get_all_cards(self) -> list[BaseStrategyCard]:
        """Get all strategy cards.

        Returns:
            List of all strategy card implementations

        Requirements: 5.7 - Registry system for all 8 cards
        """
        return list(self._cards.values())

    def get_cards_by_initiative_order(self) -> list[BaseStrategyCard]:
        """Get all strategy cards ordered by initiative value.

        Returns:
            List of strategy cards ordered by initiative (1-8)
        """
        return sorted(
            self._cards.values(), key=lambda card: card.get_initiative_value()
        )

    def validate_registry(self) -> bool:
        """Validate that all 8 strategy cards are registered.

        Returns:
            True if all cards are properly registered
        """
        expected_types = set(StrategyCardType)
        registered_types = set(self._cards.keys())
        return expected_types == registered_types

"""Tests for BaseStrategyCard implementation pattern.

This module tests the base strategy card implementation that follows the
TechnologyStrategyCard pattern for all 8 strategy cards.
"""

from ti4.core.strategic_action import StrategyCardType


class TestBaseStrategyCardPattern:
    """Test the base strategy card implementation pattern."""

    def test_base_strategy_card_can_be_instantiated(self) -> None:
        """Test that BaseStrategyCard can be instantiated.

        Requirements: 5.1 - Primary and secondary ability framework
        """
        # RED: This will fail until we create BaseStrategyCard
        from ti4.core.base_strategy_card import BaseStrategyCard

        # Create a concrete implementation for testing
        class TestStrategyCard(BaseStrategyCard):
            def __init__(self) -> None:
                pass

            def get_card_type(self) -> StrategyCardType:
                return StrategyCardType.LEADERSHIP

            def get_initiative_value(self) -> int:
                return 1

            def execute_primary_ability(
                self, player_id: str, game_state=None, **kwargs
            ):
                from ti4.core.base_strategy_card import StrategyCardAbilityResult

                return StrategyCardAbilityResult(success=True, player_id=player_id)

            def execute_secondary_ability(
                self, player_id: str, game_state=None, **kwargs
            ):
                from ti4.core.base_strategy_card import StrategyCardAbilityResult

                return StrategyCardAbilityResult(success=True, player_id=player_id)

        card = TestStrategyCard()
        assert card is not None

    def test_base_strategy_card_has_required_abstract_methods(self) -> None:
        """Test that BaseStrategyCard defines required abstract methods.

        Requirements: 5.1, 6.1 - Framework compatibility with strategic action resolution
        """
        from ti4.core.base_strategy_card import BaseStrategyCard

        # Should have abstract methods that concrete cards must implement
        assert hasattr(BaseStrategyCard, "get_card_type")
        assert hasattr(BaseStrategyCard, "get_initiative_value")
        assert hasattr(BaseStrategyCard, "execute_primary_ability")
        assert hasattr(BaseStrategyCard, "execute_secondary_ability")

    def test_base_strategy_card_follows_technology_pattern(self) -> None:
        """Test that BaseStrategyCard follows the TechnologyStrategyCard pattern.

        Requirements: 6.3 - Compatibility with existing strategic action resolution
        """
        from ti4.core.base_strategy_card import BaseStrategyCard

        # Create a concrete implementation
        class TestStrategyCard(BaseStrategyCard):
            def __init__(self) -> None:
                pass

            def get_card_type(self) -> StrategyCardType:
                return StrategyCardType.LEADERSHIP

            def get_initiative_value(self) -> int:
                return 1

            def execute_primary_ability(
                self, player_id: str, game_state=None, **kwargs
            ):
                from ti4.core.base_strategy_card import StrategyCardAbilityResult

                return StrategyCardAbilityResult(success=True, player_id=player_id)

            def execute_secondary_ability(
                self, player_id: str, game_state=None, **kwargs
            ):
                from ti4.core.base_strategy_card import StrategyCardAbilityResult

                return StrategyCardAbilityResult(success=True, player_id=player_id)

        card = TestStrategyCard()

        # Should have the same interface as TechnologyStrategyCard
        assert hasattr(card, "get_initiative_value")
        assert callable(card.get_initiative_value)

        # Should return correct initiative value
        assert card.get_initiative_value() == 1
        assert card.get_card_type() == StrategyCardType.LEADERSHIP


class TestStrategyCardRegistry:
    """Test the strategy card registry system."""

    def test_strategy_card_registry_exists(self) -> None:
        """Test that strategy card registry system exists.

        Requirements: 5.7 - Strategy card registry system for all 8 cards
        """
        # RED: This will fail until we create the registry
        from ti4.core.strategy_card_registry import StrategyCardRegistry

        registry = StrategyCardRegistry()
        assert registry is not None

    def test_registry_contains_all_eight_cards(self) -> None:
        """Test that registry contains all 8 strategy cards.

        Requirements: 5.7 - Registry system for all 8 cards
        """
        from ti4.core.strategy_card_registry import StrategyCardRegistry

        registry = StrategyCardRegistry()

        # Should have all 8 strategy cards
        all_cards = registry.get_all_cards()
        assert len(all_cards) == 8

        # Should contain all strategy card types
        card_types = {card.get_card_type() for card in all_cards}
        expected_types = set(StrategyCardType)
        assert card_types == expected_types

    def test_registry_can_get_card_by_type(self) -> None:
        """Test that registry can retrieve cards by type.

        Requirements: 5.7 - Registry system for card access
        """
        from ti4.core.strategy_card_registry import StrategyCardRegistry

        registry = StrategyCardRegistry()

        # Should be able to get specific cards
        leadership_card = registry.get_card(StrategyCardType.LEADERSHIP)
        assert leadership_card is not None
        assert leadership_card.get_card_type() == StrategyCardType.LEADERSHIP
        assert leadership_card.get_initiative_value() == 1

        technology_card = registry.get_card(StrategyCardType.TECHNOLOGY)
        assert technology_card is not None
        assert technology_card.get_card_type() == StrategyCardType.TECHNOLOGY
        assert technology_card.get_initiative_value() == 7


class TestIndividualStrategyCards:
    """Test individual strategy card implementations."""

    def test_leadership_strategy_card_exists(self) -> None:
        """Test that LeadershipStrategyCard exists and follows pattern.

        Requirements: 5.1 - Individual strategy card implementations
        """
        # RED: This will fail until we create LeadershipStrategyCard
        from ti4.core.leadership_strategy_card import LeadershipStrategyCard

        card = LeadershipStrategyCard()
        assert card is not None
        assert card.get_card_type() == StrategyCardType.LEADERSHIP
        assert card.get_initiative_value() == 1

    def test_diplomacy_strategy_card_exists(self) -> None:
        """Test that DiplomacyStrategyCard exists and follows pattern.

        Requirements: 5.1 - Individual strategy card implementations
        """
        # RED: This will fail until we create DiplomacyStrategyCard
        from ti4.core.diplomacy_strategy_card import DiplomacyStrategyCard

        card = DiplomacyStrategyCard()
        assert card is not None
        assert card.get_card_type() == StrategyCardType.DIPLOMACY
        assert card.get_initiative_value() == 2

    def test_all_strategy_cards_have_correct_initiative_values(self) -> None:
        """Test that all strategy cards have correct initiative values.

        Requirements: 5.1 - Correct initiative values for all cards
        """
        from ti4.core.strategy_card_registry import StrategyCardRegistry

        registry = StrategyCardRegistry()

        # Expected initiative values
        expected_initiatives = {
            StrategyCardType.LEADERSHIP: 1,
            StrategyCardType.DIPLOMACY: 2,
            StrategyCardType.POLITICS: 3,
            StrategyCardType.CONSTRUCTION: 4,
            StrategyCardType.TRADE: 5,
            StrategyCardType.WARFARE: 6,
            StrategyCardType.TECHNOLOGY: 7,
            StrategyCardType.IMPERIAL: 8,
        }

        for card_type, expected_initiative in expected_initiatives.items():
            card = registry.get_card(card_type)
            assert card.get_initiative_value() == expected_initiative

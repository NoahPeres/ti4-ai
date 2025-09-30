"""
Tests for AI Development Algorithm technology implementation.

This module tests the AI Development Algorithm technology card, which demonstrates
that ExhaustibleTechnologyCard supports more than just ACTION abilities.
"""

from ti4.core.abilities import TimingWindow
from ti4.core.constants import Technology
from ti4.core.technology import TechnologyColor
from ti4.core.technology_cards.concrete.ai_development_algorithm import (
    AIDevelopmentAlgorithm,
)


class TestAIDevelopmentAlgorithm:
    """Test AI Development Algorithm technology implementation."""

    def test_ai_development_algorithm_basic_properties(self):
        """Test basic properties of AI Development Algorithm."""
        card = AIDevelopmentAlgorithm()

        assert card.technology_enum == Technology.AI_DEVELOPMENT_ALGORITHM
        assert card.name == "AI Development Algorithm"
        assert card.color == TechnologyColor.YELLOW
        assert card.prerequisites == []  # Level 0 technology
        assert card.faction_restriction is None  # Available to all factions

    def test_ai_development_algorithm_is_exhaustible(self):
        """Test that AI Development Algorithm can be exhausted and readied."""
        card = AIDevelopmentAlgorithm()

        # Initially not exhausted
        assert not card.is_exhausted()

        # Can be exhausted
        card.exhaust()
        assert card.is_exhausted()

        # Can be readied
        card.ready()
        assert not card.is_exhausted()

    def test_ai_development_algorithm_has_exhaustible_abilities(self):
        """Test that AI Development Algorithm has exhaustible abilities."""
        card = AIDevelopmentAlgorithm()

        exhaustible_abilities = card.get_exhaustible_abilities()
        assert len(exhaustible_abilities) == 2

        # Check ability names
        ability_names = [ability.name for ability in exhaustible_abilities]
        assert "Research Enhancement" in ability_names
        assert "Production Cost Reduction" in ability_names

    def test_ai_development_algorithm_research_enhancement_ability(self):
        """Test the research enhancement ability."""
        card = AIDevelopmentAlgorithm()

        exhaustible_abilities = card.get_exhaustible_abilities()
        research_ability = next(
            ability
            for ability in exhaustible_abilities
            if ability.name == "Research Enhancement"
        )

        assert research_ability.timing == TimingWindow.WHEN
        assert research_ability.trigger == "research_unit_upgrade_technology"
        assert research_ability.effect.type == "ignore_prerequisite"
        assert research_ability.effect.value == 1
        assert not research_ability.mandatory  # Optional ability

    def test_ai_development_algorithm_production_cost_reduction_ability(self):
        """Test the production cost reduction ability."""
        card = AIDevelopmentAlgorithm()

        exhaustible_abilities = card.get_exhaustible_abilities()
        production_ability = next(
            ability
            for ability in exhaustible_abilities
            if ability.name == "Production Cost Reduction"
        )

        assert production_ability.timing == TimingWindow.WHEN
        assert production_ability.trigger == "units_use_production"
        assert production_ability.effect.type == "reduce_production_cost"
        assert production_ability.effect.value == "unit_upgrade_count"
        assert not production_ability.mandatory  # Optional ability

    def test_ai_development_algorithm_has_no_action_ability(self):
        """Test that AI Development Algorithm has no ACTION ability."""
        card = AIDevelopmentAlgorithm()

        # Should have no ACTION ability
        action_ability = card.get_action_ability()
        assert action_ability is None

    def test_ai_development_algorithm_abilities_integration(self):
        """Test that abilities are properly integrated."""
        card = AIDevelopmentAlgorithm()

        # get_abilities() should return the same as get_exhaustible_abilities()
        all_abilities = card.get_abilities()
        exhaustible_abilities = card.get_exhaustible_abilities()

        assert len(all_abilities) == len(exhaustible_abilities)
        assert all(ability in exhaustible_abilities for ability in all_abilities)

    def test_exhaustible_technology_card_supports_non_action_abilities(self):
        """Test that ExhaustibleTechnologyCard supports non-ACTION abilities."""
        card = AIDevelopmentAlgorithm()

        # This card demonstrates that exhaustible cards can have abilities
        # that are not ACTION abilities
        exhaustible_abilities = card.get_exhaustible_abilities()

        # Both abilities should be WHEN abilities, not ACTION abilities
        for ability in exhaustible_abilities:
            assert ability.timing == TimingWindow.WHEN
            assert ability.timing != TimingWindow.ACTION

        # Should have no ACTION ability
        assert card.get_action_ability() is None

        # But should still be exhaustible
        assert not card.is_exhausted()
        card.exhaust()
        assert card.is_exhausted()


class TestExhaustibleTechnologyCardFramework:
    """Test the broader ExhaustibleTechnologyCard framework."""

    def test_exhaustible_card_supports_multiple_ability_types(self):
        """Test that exhaustible cards can support various ability types."""
        card = AIDevelopmentAlgorithm()

        # The framework should support:
        # 1. Cards with ACTION abilities (traditional exhaustible cards)
        # 2. Cards with triggered abilities that exhaust (like AI Development Algorithm)
        # 3. Cards with mixed ability types

        # AI Development Algorithm demonstrates type 2
        exhaustible_abilities = card.get_exhaustible_abilities()
        assert len(exhaustible_abilities) > 0

        # None of these should be ACTION abilities
        for ability in exhaustible_abilities:
            assert ability.timing != TimingWindow.ACTION

        # But the card should still be exhaustible
        assert hasattr(card, "exhaust")
        assert hasattr(card, "ready")
        assert hasattr(card, "is_exhausted")

    def test_get_action_ability_returns_none_for_non_action_cards(self):
        """Test that get_action_ability() correctly returns None for non-ACTION cards."""
        card = AIDevelopmentAlgorithm()

        # This card has exhaustible abilities but no ACTION abilities
        assert card.get_exhaustible_abilities()  # Has exhaustible abilities
        assert card.get_action_ability() is None  # But no ACTION ability

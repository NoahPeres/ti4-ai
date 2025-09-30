"""
Tests for technology specification system using enums.

This module tests the enum-based technology specification system that provides
a centralized registry for all technology data using only enum types.
"""

import pytest

from ti4.core.constants import (
    AbilityCondition,
    AbilityEffectType,
    AbilityTrigger,
    Expansion,
    Faction,
    Technology,
)
from ti4.core.technology import TechnologyColor


class TestTechnologySpecification:
    """Test TechnologySpecification dataclass using only enum types."""

    def test_technology_specification_creation(self):
        """Test creating a TechnologySpecification with enum types."""
        # RED: This will fail because TechnologySpecification doesn't exist yet
        from ti4.core.technology_cards.specifications import TechnologySpecification

        spec = TechnologySpecification(
            technology=Technology.GRAVITY_DRIVE,
            name="Gravity Drive",
            color=TechnologyColor.BLUE,
            prerequisites=[TechnologyColor.BLUE],
            faction_restriction=None,
            expansion=Expansion.BASE,
            abilities=[],
        )

        assert spec.technology == Technology.GRAVITY_DRIVE
        assert spec.name == "Gravity Drive"
        assert spec.color == TechnologyColor.BLUE
        assert spec.prerequisites == [TechnologyColor.BLUE]
        assert spec.faction_restriction is None
        assert spec.expansion == Expansion.BASE
        assert spec.abilities == []

    def test_technology_specification_with_faction_restriction(self):
        """Test TechnologySpecification with faction restriction."""
        from ti4.core.technology_cards.specifications import TechnologySpecification

        spec = TechnologySpecification(
            technology=Technology.SPEC_OPS_II,
            name="Spec Ops II",
            color=None,  # Unit upgrades have no color
            prerequisites=[TechnologyColor.GREEN, TechnologyColor.GREEN],
            faction_restriction=Faction.SOL,
            expansion=Expansion.BASE,
            abilities=[],
        )

        assert spec.technology == Technology.SPEC_OPS_II
        assert spec.faction_restriction == Faction.SOL
        assert spec.color is None  # Unit upgrades have no color

    def test_technology_specification_with_abilities(self):
        """Test TechnologySpecification with ability specifications."""
        from ti4.core.technology_cards.specifications import (
            AbilitySpecification,
            TechnologySpecification,
        )

        ability_spec = AbilitySpecification(
            trigger=AbilityTrigger.ACTION,
            effect=AbilityEffectType.GAIN_TRADE_GOODS,
            conditions=[AbilityCondition.HAS_SHIPS_IN_SYSTEM],
            mandatory=False,
            passive=False,
        )

        spec = TechnologySpecification(
            technology=Technology.GRAVITY_DRIVE,
            name="Gravity Drive",
            color=TechnologyColor.BLUE,
            prerequisites=[TechnologyColor.BLUE],
            faction_restriction=None,
            expansion=Expansion.BASE,
            abilities=[ability_spec],
        )

        assert len(spec.abilities) == 1
        assert spec.abilities[0].trigger == AbilityTrigger.ACTION
        assert spec.abilities[0].effect == AbilityEffectType.GAIN_TRADE_GOODS


class TestAbilitySpecification:
    """Test AbilitySpecification dataclass using only enum types."""

    def test_ability_specification_creation(self):
        """Test creating an AbilitySpecification with enum types."""
        # RED: This will fail because AbilitySpecification doesn't exist yet
        from ti4.core.technology_cards.specifications import AbilitySpecification

        spec = AbilitySpecification(
            trigger=AbilityTrigger.AFTER_TACTICAL_ACTION,
            effect=AbilityEffectType.EXPLORE_FRONTIER_TOKEN,
            conditions=[
                AbilityCondition.HAS_SHIPS_IN_SYSTEM,
                AbilityCondition.SYSTEM_CONTAINS_FRONTIER,
            ],
            mandatory=True,
            passive=False,
        )

        assert spec.trigger == AbilityTrigger.AFTER_TACTICAL_ACTION
        assert spec.effect == AbilityEffectType.EXPLORE_FRONTIER_TOKEN
        assert len(spec.conditions) == 2
        assert AbilityCondition.HAS_SHIPS_IN_SYSTEM in spec.conditions
        assert AbilityCondition.SYSTEM_CONTAINS_FRONTIER in spec.conditions
        assert spec.mandatory is True
        assert spec.passive is False

    def test_ability_specification_passive_ability(self):
        """Test AbilitySpecification for passive abilities."""
        from ti4.core.technology_cards.specifications import AbilitySpecification

        spec = AbilitySpecification(
            trigger=AbilityTrigger.WHEN_RETREAT_DECLARED,
            effect=AbilityEffectType.ALLOW_RETREAT_TO_EMPTY_ADJACENT,
            conditions=[],
            mandatory=False,
            passive=True,
        )

        assert spec.trigger == AbilityTrigger.WHEN_RETREAT_DECLARED
        assert spec.effect == AbilityEffectType.ALLOW_RETREAT_TO_EMPTY_ADJACENT
        assert spec.conditions == []
        assert spec.passive is True

    def test_ability_specification_no_conditions(self):
        """Test AbilitySpecification with no conditions."""
        from ti4.core.technology_cards.specifications import AbilitySpecification

        spec = AbilitySpecification(
            trigger=AbilityTrigger.ACTION,
            effect=AbilityEffectType.GAIN_COMMAND_TOKENS,
            conditions=[],
            mandatory=False,
            passive=False,
        )

        assert spec.conditions == []


class TestTechnologySpecificationRegistry:
    """Test TechnologySpecificationRegistry with enum-based data."""

    def test_registry_creation(self):
        """Test creating a TechnologySpecificationRegistry."""
        # RED: This will fail because TechnologySpecificationRegistry doesn't exist yet
        from ti4.core.technology_cards.specifications import (
            TechnologySpecificationRegistry,
        )

        registry = TechnologySpecificationRegistry()
        assert registry is not None

    def test_registry_get_specification(self):
        """Test getting a technology specification from the registry."""
        from ti4.core.technology_cards.specifications import (
            TechnologySpecificationRegistry,
        )

        registry = TechnologySpecificationRegistry()

        # Should have Gravity Drive specification
        spec = registry.get_specification(Technology.GRAVITY_DRIVE)
        assert spec is not None
        assert spec.technology == Technology.GRAVITY_DRIVE
        assert spec.name == "Gravity Drive"
        assert spec.color == TechnologyColor.BLUE

    def test_registry_get_nonexistent_specification(self):
        """Test getting a specification that doesn't exist."""
        from ti4.core.technology_cards.specifications import (
            TechnologySpecificationRegistry,
        )

        registry = TechnologySpecificationRegistry()

        # Should return None for unregistered technology
        spec = registry.get_specification(Technology.PLASMA_SCORING)
        assert spec is None

    def test_registry_get_all_specifications(self):
        """Test getting all specifications from the registry."""
        from ti4.core.technology_cards.specifications import (
            TechnologySpecificationRegistry,
        )

        registry = TechnologySpecificationRegistry()

        all_specs = registry.get_all_specifications()
        assert isinstance(all_specs, list)
        assert len(all_specs) > 0

        # Should contain Gravity Drive
        gravity_drive_specs = [
            s for s in all_specs if s.technology == Technology.GRAVITY_DRIVE
        ]
        assert len(gravity_drive_specs) == 1

    def test_registry_has_specification(self):
        """Test checking if registry has a specification."""
        from ti4.core.technology_cards.specifications import (
            TechnologySpecificationRegistry,
        )

        registry = TechnologySpecificationRegistry()

        assert registry.has_specification(Technology.GRAVITY_DRIVE) is True
        assert registry.has_specification(Technology.PLASMA_SCORING) is False

    def test_registry_get_specifications_by_color(self):
        """Test getting specifications filtered by color."""
        from ti4.core.technology_cards.specifications import (
            TechnologySpecificationRegistry,
        )

        registry = TechnologySpecificationRegistry()

        blue_specs = registry.get_specifications_by_color(TechnologyColor.BLUE)
        assert isinstance(blue_specs, list)

        # All returned specs should be blue
        for spec in blue_specs:
            assert spec.color == TechnologyColor.BLUE

    def test_registry_get_specifications_by_expansion(self):
        """Test getting specifications filtered by expansion."""
        from ti4.core.technology_cards.specifications import (
            TechnologySpecificationRegistry,
        )

        registry = TechnologySpecificationRegistry()

        base_specs = registry.get_specifications_by_expansion(Expansion.BASE)
        assert isinstance(base_specs, list)

        # All returned specs should be from base expansion
        for spec in base_specs:
            assert spec.expansion == Expansion.BASE


class TestSpecificationValidation:
    """Test validation of technology specifications."""

    def test_validate_specification_valid(self):
        """Test validation of a valid specification."""
        from ti4.core.technology_cards.specifications import (
            TechnologySpecification,
            validate_specification,
        )

        spec = TechnologySpecification(
            technology=Technology.GRAVITY_DRIVE,
            name="Gravity Drive",
            color=TechnologyColor.BLUE,
            prerequisites=[TechnologyColor.BLUE],
            faction_restriction=None,
            expansion=Expansion.BASE,
            abilities=[],
        )

        errors = validate_specification(spec)
        assert errors == []

    def test_validate_specification_missing_name(self):
        """Test validation of specification with missing name."""
        from ti4.core.technology_cards.specifications import (
            TechnologySpecification,
            validate_specification,
        )

        spec = TechnologySpecification(
            technology=Technology.GRAVITY_DRIVE,
            name="",  # Empty name should be invalid
            color=TechnologyColor.BLUE,
            prerequisites=[TechnologyColor.BLUE],
            faction_restriction=None,
            expansion=Expansion.BASE,
            abilities=[],
        )

        errors = validate_specification(spec)
        assert len(errors) > 0
        assert any("name" in error.lower() for error in errors)

    def test_validate_specification_unit_upgrade_with_color(self):
        """Test validation of unit upgrade with color (should be invalid)."""
        from ti4.core.technology_cards.specifications import (
            TechnologySpecification,
            validate_specification,
        )

        spec = TechnologySpecification(
            technology=Technology.CRUISER_II,
            name="Cruiser II",
            color=TechnologyColor.BLUE,  # Unit upgrades should not have color
            prerequisites=[
                TechnologyColor.YELLOW,
                TechnologyColor.RED,
                TechnologyColor.GREEN,
            ],
            faction_restriction=None,
            expansion=Expansion.BASE,
            abilities=[],
        )

        errors = validate_specification(spec)
        assert len(errors) > 0
        assert any(
            "unit upgrade" in error.lower() and "color" in error.lower()
            for error in errors
        )


class TestSpecificationValidationEnhanced:
    """Test enhanced validation features added during refactoring."""

    def test_validate_specification_invalid_type(self):
        """Test validation with invalid input type."""
        from ti4.core.technology_cards.specifications import validate_specification

        with pytest.raises(TypeError, match="Expected TechnologySpecification"):
            validate_specification("not a specification")


class TestRegistryInputValidation:
    """Test input validation for registry methods."""

    def test_get_specification_invalid_type(self):
        """Test get_specification with invalid input type."""
        from ti4.core.technology_cards.specifications import (
            TechnologySpecificationRegistry,
        )

        registry = TechnologySpecificationRegistry()

        with pytest.raises(TypeError, match="Expected Technology enum"):
            registry.get_specification("not a technology")

    def test_has_specification_invalid_type(self):
        """Test has_specification with invalid input type."""
        from ti4.core.technology_cards.specifications import (
            TechnologySpecificationRegistry,
        )

        registry = TechnologySpecificationRegistry()

        with pytest.raises(TypeError, match="Expected Technology enum"):
            registry.has_specification("not a technology")

    def test_get_specifications_by_color_invalid_type(self):
        """Test get_specifications_by_color with invalid input type."""
        from ti4.core.technology_cards.specifications import (
            TechnologySpecificationRegistry,
        )

        registry = TechnologySpecificationRegistry()

        with pytest.raises(TypeError, match="Expected TechnologyColor enum"):
            registry.get_specifications_by_color("not a color")

    def test_get_specifications_by_expansion_invalid_type(self):
        """Test get_specifications_by_expansion with invalid input type."""
        from ti4.core.technology_cards.specifications import (
            TechnologySpecificationRegistry,
        )

        registry = TechnologySpecificationRegistry()

        with pytest.raises(TypeError, match="Expected Expansion enum"):
            registry.get_specifications_by_expansion("not an expansion")


class TestUnitUpgradeConstants:
    """Test the unit upgrade constants used in validation."""

    def test_unit_upgrade_constant_usage(self):
        """Test that the UNIT_UPGRADE_TECHNOLOGIES constant is used correctly."""
        from ti4.core.technology_cards.specifications import (
            UNIT_UPGRADE_TECHNOLOGIES,
            TechnologySpecification,
            validate_specification,
        )

        # Test that a known unit upgrade is in the constant
        assert Technology.CRUISER_II in UNIT_UPGRADE_TECHNOLOGIES
        assert Technology.FIGHTER_II in UNIT_UPGRADE_TECHNOLOGIES

        # Test validation uses the constant correctly
        spec = TechnologySpecification(
            technology=Technology.CRUISER_II,
            name="Cruiser II",
            color=TechnologyColor.BLUE,  # Should be invalid
            prerequisites=[],
            faction_restriction=None,
            expansion=Expansion.BASE,
            abilities=[],
        )

        errors = validate_specification(spec)
        assert len(errors) > 0
        assert any("unit upgrade" in error.lower() for error in errors)

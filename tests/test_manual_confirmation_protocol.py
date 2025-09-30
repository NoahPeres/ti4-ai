"""
Tests for manual confirmation protocol enforcement.

This module tests the manual confirmation protocol that ensures all technology
specifications are explicitly confirmed before implementation.
"""

import pytest

from ti4.core.constants import Technology
from ti4.core.technology_cards.confirmation import require_confirmation
from ti4.core.technology_cards.exceptions import TechnologySpecificationError


class TestTechnologySpecificationError:
    """Test the TechnologySpecificationError exception class."""

    def test_exception_creation(self):
        """Test that TechnologySpecificationError can be created with a message."""
        error = TechnologySpecificationError("Test error message")
        assert str(error) == "Test error message"

    def test_exception_inheritance(self):
        """Test that TechnologySpecificationError inherits from Exception."""
        error = TechnologySpecificationError("Test error")
        assert isinstance(error, Exception)


class TestRequireConfirmation:
    """Test the require_confirmation validation function."""

    def test_require_confirmation_with_confirmed_technology(self):
        """Test that require_confirmation passes for confirmed technologies."""
        # Dark Energy Tap is confirmed in the registry
        # This should not raise an exception
        require_confirmation(Technology.DARK_ENERGY_TAP, "color")

    def test_require_confirmation_with_unconfirmed_technology(self):
        """Test that require_confirmation raises error for unconfirmed technologies."""
        # Fighter II is not confirmed in the registry
        with pytest.raises(TechnologySpecificationError) as exc_info:
            require_confirmation(Technology.FIGHTER_II, "color")

        assert "FIGHTER_II color not confirmed" in str(exc_info.value)
        assert "Please ask user for specification" in str(exc_info.value)

    def test_require_confirmation_with_different_attributes(self):
        """Test require_confirmation with different attribute names."""
        with pytest.raises(TechnologySpecificationError) as exc_info:
            require_confirmation(Technology.CRUISER_II, "prerequisites")

        assert "CRUISER_II prerequisites not confirmed" in str(exc_info.value)

    def test_require_confirmation_with_invalid_technology_type(self):
        """Test require_confirmation raises TypeError for non-Technology input."""
        with pytest.raises(TypeError) as exc_info:
            require_confirmation("not_a_technology", "color")

        assert "Expected Technology enum" in str(exc_info.value)


class TestConfirmationProtocolIntegration:
    """Test integration of confirmation protocol with technology specifications."""

    def test_specification_access_requires_confirmation(self):
        """Test that accessing unconfirmed specifications raises error."""
        from ti4.core.technology_cards.specifications import (
            TechnologySpecificationRegistry,
        )

        registry = TechnologySpecificationRegistry()

        # This should work for confirmed technologies
        spec = registry.get_specification(Technology.DARK_ENERGY_TAP)
        assert spec is not None

        # This should raise error for unconfirmed technologies
        with pytest.raises(TechnologySpecificationError):
            registry.get_specification_with_confirmation(Technology.FIGHTER_II)

    def test_technology_card_creation_requires_confirmation(self):
        """Test that creating technology cards requires confirmation."""
        from ti4.core.technology_cards.concrete.dark_energy_tap import DarkEnergyTap
        from ti4.core.technology_cards.registry import TechnologyCardRegistry

        registry = TechnologyCardRegistry()

        # Register a confirmed technology card
        dark_energy_tap = DarkEnergyTap()
        registry.register_card(dark_energy_tap)

        # This should work for confirmed technologies
        retrieved_card = registry.get_card(Technology.DARK_ENERGY_TAP)
        assert retrieved_card is not None

        # This should raise error for unconfirmed technologies when using strict mode
        with pytest.raises(TechnologySpecificationError):
            registry.get_card_with_confirmation(Technology.FIGHTER_II)

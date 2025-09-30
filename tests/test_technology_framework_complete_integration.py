"""
Complete technology framework integration tests.

This module tests the complete integration of the technology card framework
with the existing TechnologyManager and game systems, ensuring that:
1. Dark Energy Tap and Gravity Drive are properly registered
2. TechnologyManager uses the new framework
3. All existing functionality continues to work
4. No regressions are introduced
"""

import pytest

from ti4.core.constants import Technology
from ti4.core.game_technology_manager import GameTechnologyManager
from ti4.core.technology import TechnologyManager
from ti4.core.technology_cards.factory import TechnologyCardFactory


class TestCompleteFrameworkIntegration:
    """Test complete integration of technology card framework with existing systems."""

    def test_technology_manager_uses_new_framework_for_supported_technologies(self):
        """Test that TechnologyManager integrates with new framework for supported technologies."""
        # This test should fail initially - TechnologyManager doesn't use new framework yet
        manager = TechnologyManager()
        factory = TechnologyCardFactory()

        # Dark Energy Tap should be available through both systems
        assert Technology.DARK_ENERGY_TAP in manager.get_technology_deck("player1")
        assert factory.is_supported(Technology.DARK_ENERGY_TAP)

        # The manager should be able to get technology card details from the framework
        # This will fail initially because TechnologyManager doesn't integrate with framework
        card = factory.create_card(Technology.DARK_ENERGY_TAP)
        assert card.name == "Dark Energy Tap"

        # Manager should be able to use framework data for technology properties
        # This should work through the integration
        assert manager.can_research_technology("player1", Technology.DARK_ENERGY_TAP)

    def test_game_technology_manager_integrates_with_framework(self):
        """Test that GameTechnologyManager integrates with the new framework."""
        from ti4.core.game_state import GameState
        from ti4.core.player import Player

        # Create a proper game state with players
        player = Player(id="player1", faction=None)
        game_state = GameState(players=[player])
        game_state.player_technologies["player1"] = []

        manager = GameTechnologyManager(game_state)
        factory = TechnologyCardFactory()

        # Should be able to research Dark Energy Tap
        success = manager.research_technology("player1", Technology.DARK_ENERGY_TAP)
        assert success

        # Technology should be in player's technologies
        player_techs = manager.get_player_technologies("player1")
        assert Technology.DARK_ENERGY_TAP in player_techs

        # Should be able to get the technology card
        card = factory.create_card(Technology.DARK_ENERGY_TAP)
        assert card.technology_enum == Technology.DARK_ENERGY_TAP

    def test_framework_preserves_existing_technology_functionality(self):
        """Test that new framework doesn't break existing technology functionality."""
        manager = TechnologyManager()

        # Give player a blue technology to meet Gravity Drive prerequisites
        manager.gain_technology(
            "player1", Technology.ANTIMASS_DEFLECTORS
        )  # Blue tech, no prereqs

        # Existing confirmed technologies should still work
        assert manager.can_research_technology("player1", Technology.GRAVITY_DRIVE)
        assert manager.research_technology("player1", Technology.GRAVITY_DRIVE)

        # Player should have the technology
        player_techs = manager.get_player_technologies("player1")
        assert Technology.GRAVITY_DRIVE in player_techs

        # Technology properties should still work
        assert manager.get_technology_color(Technology.GRAVITY_DRIVE).value == "blue"
        assert not manager.is_unit_upgrade(Technology.GRAVITY_DRIVE)

    def test_both_dark_energy_tap_and_gravity_drive_are_fully_integrated(self):
        """Test that both Dark Energy Tap and Gravity Drive work through the complete system."""
        manager = TechnologyManager()
        factory = TechnologyCardFactory()

        # Both technologies should be supported by factory
        assert factory.is_supported(Technology.DARK_ENERGY_TAP)
        assert factory.is_supported(Technology.GRAVITY_DRIVE)

        # Both should be creatable
        dark_energy_tap = factory.create_card(Technology.DARK_ENERGY_TAP)
        gravity_drive = factory.create_card(Technology.GRAVITY_DRIVE)

        assert dark_energy_tap.name == "Dark Energy Tap"
        assert gravity_drive.name == "Gravity Drive"

        # Both should be researchable (give player blue tech for Gravity Drive prereqs)
        manager.gain_technology(
            "player1", Technology.ANTIMASS_DEFLECTORS
        )  # Blue tech, no prereqs

        assert manager.can_research_technology("player1", Technology.DARK_ENERGY_TAP)
        assert manager.can_research_technology("player1", Technology.GRAVITY_DRIVE)

        # Research both
        assert manager.research_technology("player1", Technology.DARK_ENERGY_TAP)
        assert manager.research_technology("player1", Technology.GRAVITY_DRIVE)

        # Both should be in player's technologies
        player_techs = manager.get_player_technologies("player1")
        assert Technology.DARK_ENERGY_TAP in player_techs
        assert Technology.GRAVITY_DRIVE in player_techs

    def test_framework_integration_with_abilities_system(self):
        """Test that framework integrates properly with abilities system."""
        factory = TechnologyCardFactory()

        # Get technology cards
        dark_energy_tap = factory.create_card(Technology.DARK_ENERGY_TAP)
        gravity_drive = factory.create_card(Technology.GRAVITY_DRIVE)

        # Both should have abilities
        det_abilities = dark_energy_tap.get_abilities()
        gd_abilities = gravity_drive.get_abilities()

        assert len(det_abilities) > 0
        assert len(gd_abilities) > 0

        # Abilities should have proper source attribution
        for ability in det_abilities:
            assert hasattr(ability, "source")
            assert ability.source == "Dark Energy Tap"

        for ability in gd_abilities:
            assert hasattr(ability, "source")
            assert ability.source == "Gravity Drive"

    def test_no_regressions_in_existing_tests(self):
        """Test that existing functionality has no regressions."""
        manager = TechnologyManager()

        # Test existing confirmed technologies still work
        confirmed_techs = [
            Technology.CRUISER_II,
            Technology.FIGHTER_II,
            Technology.ANTIMASS_DEFLECTORS,
        ]

        for tech in confirmed_techs:
            # Should be able to check if it's in deck
            deck = manager.get_technology_deck("player1")
            assert tech in deck

            # Should be able to research if prerequisites are met
            # (We'll just check the method doesn't crash)
            try:
                can_research = manager.can_research_technology("player1", tech)
                assert isinstance(can_research, bool)
            except ValueError:
                # Expected for technologies with unmet prerequisites
                pass

    def test_framework_error_handling_is_robust(self):
        """Test that framework error handling works correctly."""
        factory = TechnologyCardFactory()
        manager = TechnologyManager()

        # Unsupported technology should raise clear error
        with pytest.raises(ValueError, match="No implementation found"):
            factory.create_card(Technology.CRUISER_II)

        # Invalid technology enum should raise TypeError
        with pytest.raises(TypeError):
            factory.create_card("not_a_technology")  # type: ignore

        # Manager should handle unconfirmed technologies gracefully
        unconfirmed_techs = manager.get_unconfirmed_technologies()
        assert isinstance(unconfirmed_techs, set)
        assert len(unconfirmed_techs) > 0

    def test_complete_framework_integration_system(self):
        """Test the complete framework integration system."""
        from ti4.core.technology_cards.integration import TechnologyFrameworkIntegration

        # Create integration system
        integration = TechnologyFrameworkIntegration()

        # Validate integration
        validation_results = integration.validate_integration()

        # All validation checks should pass
        assert validation_results["factory_operational"]
        assert validation_results["registry_populated"]
        assert validation_results["dark_energy_tap_available"]
        assert validation_results["gravity_drive_available"]
        assert validation_results["dark_energy_tap_has_abilities"]
        assert validation_results["gravity_drive_has_abilities"]

        # Should be able to get technology cards
        det_card = integration.get_technology_card(Technology.DARK_ENERGY_TAP)
        gd_card = integration.get_technology_card(Technology.GRAVITY_DRIVE)

        assert det_card is not None
        assert gd_card is not None
        assert det_card.name == "Dark Energy Tap"  # type: ignore
        assert gd_card.name == "Gravity Drive"  # type: ignore

        # Should support both technologies
        assert integration.is_technology_supported(Technology.DARK_ENERGY_TAP)
        assert integration.is_technology_supported(Technology.GRAVITY_DRIVE)

        # Should not support unimplemented technologies
        assert not integration.is_technology_supported(Technology.CRUISER_II)

        # Should list supported technologies
        supported = integration.get_supported_technologies()
        assert Technology.DARK_ENERGY_TAP in supported
        assert Technology.GRAVITY_DRIVE in supported

    def test_global_integration_access(self):
        """Test global integration access functions."""
        from ti4.core.technology_cards import get_technology_framework_integration

        # Should be able to get global integration
        integration = get_technology_framework_integration()
        assert integration is not None

        # Should be the same instance on subsequent calls
        integration2 = get_technology_framework_integration()
        assert integration is integration2

        # Should have both technologies available
        assert integration.is_technology_supported(Technology.DARK_ENERGY_TAP)
        assert integration.is_technology_supported(Technology.GRAVITY_DRIVE)

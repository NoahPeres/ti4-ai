"""
Tests for technology card integration with unit stats system.

This module tests the integration between technology cards and the unit stats system,
ensuring that unit upgrade technologies properly modify unit statistics.
"""

import pytest

from ti4.core.constants import Technology, UnitType
from ti4.core.technology_cards.base.unit_upgrade_tech import UnitUpgradeTechnologyCard
from ti4.core.unit_stats import UnitStatsProvider


class TestUnitStatsIntegration:
    """Test technology card integration with unit stats system."""

    def test_unit_upgrade_technology_registers_with_unit_stats_provider(self) -> None:
        """Test that unit upgrade technologies register modifications with UnitStatsProvider."""
        # RED: This test should fail because we haven't implemented the enum-based system yet

        # Create a test unit upgrade technology
        class TestFighterII(UnitUpgradeTechnologyCard):
            @property
            def prerequisites(self) -> list:
                return []

            @property
            def faction_restriction(self):
                return None

            def get_abilities(self) -> list:
                return []

            def get_unit_stat_modifications(self) -> dict:
                # This should use enum-based modifications
                from ti4.core.constants import UnitStatModification

                return {
                    UnitStatModification.MOVEMENT: 1,  # Fighter II gains movement
                    UnitStatModification.COMBAT_VALUE: 8,  # Fighter II improves combat
                }

        # Create technology and unit stats provider
        fighter_ii = TestFighterII(
            Technology.FIGHTER_II, "Fighter II", UnitType.FIGHTER
        )
        unit_stats_provider = UnitStatsProvider()

        # Register the technology
        fighter_ii.register_with_systems(None, unit_stats_provider)

        # Test that the modifications are applied
        base_fighter_stats = unit_stats_provider.get_unit_stats(UnitType.FIGHTER)
        upgraded_fighter_stats = unit_stats_provider.get_unit_stats(
            UnitType.FIGHTER, technologies={Technology.FIGHTER_II}
        )

        # Fighter II should have improved stats
        assert upgraded_fighter_stats.movement == base_fighter_stats.movement + 1
        assert upgraded_fighter_stats.combat_value == 8

    def test_enum_based_unit_stat_modifications(self) -> None:
        """Test that unit stat modifications use enum-based system."""
        # RED: This test should fail because UnitStatModification enum doesn't exist yet
        from ti4.core.constants import UnitStatModification

        # Create a test unit upgrade technology using enums
        class TestCruiserII(UnitUpgradeTechnologyCard):
            @property
            def prerequisites(self) -> list:
                return []

            @property
            def faction_restriction(self):
                return None

            def get_abilities(self) -> list:
                return []

            def get_unit_stat_modifications(self) -> dict[UnitStatModification, int]:
                # This should use enum-based modifications
                return {
                    UnitStatModification.MOVEMENT: 1,  # +1 movement
                    UnitStatModification.CAPACITY: 1,  # +1 capacity
                    UnitStatModification.COMBAT_VALUE: 6,  # Better combat (6 instead of 7)
                }

        # Create technology and unit stats provider
        cruiser_ii = TestCruiserII(
            Technology.CRUISER_II, "Cruiser II", UnitType.CRUISER
        )
        unit_stats_provider = UnitStatsProvider()

        # Register the technology
        cruiser_ii.register_with_systems(None, unit_stats_provider)

        # Test that the modifications are applied
        base_cruiser_stats = unit_stats_provider.get_unit_stats(UnitType.CRUISER)
        upgraded_cruiser_stats = unit_stats_provider.get_unit_stats(
            UnitType.CRUISER, technologies={Technology.CRUISER_II}
        )

        # Cruiser II should have improved stats
        assert upgraded_cruiser_stats.movement == base_cruiser_stats.movement + 1
        assert upgraded_cruiser_stats.capacity == base_cruiser_stats.capacity + 1
        assert upgraded_cruiser_stats.combat_value == 6  # Better combat value

    def test_automatic_technology_registration(self) -> None:
        """Test that technology modifications are registered automatically."""
        from ti4.core.constants import UnitStatModification

        # Create a test unit upgrade technology
        class TestDreadnoughtII(UnitUpgradeTechnologyCard):
            @property
            def prerequisites(self) -> list:
                return []

            @property
            def faction_restriction(self):
                return None

            def get_abilities(self) -> list:
                return []

            def get_unit_stat_modifications(self) -> dict[UnitStatModification, int]:
                return {
                    UnitStatModification.SUSTAIN_DAMAGE: True,  # Already has sustain damage
                    UnitStatModification.BOMBARDMENT: True,  # Already has bombardment
                    UnitStatModification.BOMBARDMENT_DICE: 2,  # +1 bombardment dice
                }

        # Create technology and unit stats provider
        dreadnought_ii = TestDreadnoughtII(
            Technology.DREADNOUGHT_II, "Dreadnought II", UnitType.DREADNOUGHT
        )
        unit_stats_provider = UnitStatsProvider()

        # Register the technology - this should automatically register unit stat modifications
        dreadnought_ii.register_with_systems(None, unit_stats_provider)

        # Test that the modifications are applied
        base_dreadnought_stats = unit_stats_provider.get_unit_stats(
            UnitType.DREADNOUGHT
        )
        upgraded_dreadnought_stats = unit_stats_provider.get_unit_stats(
            UnitType.DREADNOUGHT, technologies={Technology.DREADNOUGHT_II}
        )

        # Dreadnought II should have improved bombardment
        assert (
            upgraded_dreadnought_stats.sustain_damage
        )  # Should still have sustain damage
        assert upgraded_dreadnought_stats.bombardment  # Should still have bombardment
        assert (
            upgraded_dreadnought_stats.bombardment_dice
            == base_dreadnought_stats.bombardment_dice + 2
        )

    def test_unit_stat_modification_mapper_error_handling(self) -> None:
        """Test that UnitStatModificationMapper handles errors correctly."""
        from ti4.core.constants import UnitStatModification
        from ti4.core.technology_cards.unit_stats_integration import (
            UnitStatModificationMapper,
        )

        # Test empty modifications
        empty_stats = UnitStatModificationMapper.map_modifications_to_unit_stats({})
        assert empty_stats.cost == 0
        assert empty_stats.movement == 0

        # Test invalid modification type
        with pytest.raises(ValueError, match="Invalid modification type"):
            UnitStatModificationMapper.map_modifications_to_unit_stats({"invalid": 1})

        # Test boolean conversion
        bool_stats = UnitStatModificationMapper.map_modifications_to_unit_stats(
            {
                UnitStatModification.SUSTAIN_DAMAGE: 1,  # Should be converted to True
                UnitStatModification.BOMBARDMENT: 0,  # Should be converted to False
            }
        )
        assert bool_stats.sustain_damage
        assert not bool_stats.bombardment

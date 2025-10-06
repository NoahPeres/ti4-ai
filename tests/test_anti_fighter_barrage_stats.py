"""
Tests for Anti-Fighter Barrage unit statistics enhancements.

This module tests the enhanced unit statistics system for Anti-Fighter Barrage,
including AFB-specific values and dice counts.
"""

from ti4.core.constants import UnitType
from ti4.core.unit_stats import UnitStats, UnitStatsProvider


class TestAntiFighterBarrageStats:
    """Test Anti-Fighter Barrage statistics enhancements."""

    def test_unit_stats_has_afb_value_and_dice_fields(self) -> None:
        """Test that UnitStats has anti_fighter_barrage_value and anti_fighter_barrage_dice fields."""
        # RED: This test should fail because the new fields don't exist yet
        stats = UnitStats(anti_fighter_barrage_value=9, anti_fighter_barrage_dice=2)

        assert stats.anti_fighter_barrage_value == 9
        assert stats.anti_fighter_barrage_dice == 2

    def test_destroyer_has_afb_stats(self) -> None:
        """Test that Destroyer has proper AFB statistics."""
        # RED: This test should fail because Destroyer doesn't have AFB stats yet
        provider = UnitStatsProvider()
        destroyer_stats = provider.get_unit_stats(UnitType.DESTROYER)

        # Destroyer should have AFB ability with value 9 and 1 dice
        assert destroyer_stats.anti_fighter_barrage is True
        assert destroyer_stats.anti_fighter_barrage_value == 9
        assert destroyer_stats.anti_fighter_barrage_dice == 1

    def test_destroyer_ii_has_enhanced_afb_stats(self) -> None:
        """Test that Destroyer II has enhanced AFB statistics."""
        # CONFIRMED SPECIFICATIONS - User confirmed from ability compendium:
        # AFB 6x3, Move 2, Combat 8
        provider = UnitStatsProvider()
        destroyer_ii_stats = provider.get_unit_stats(UnitType.DESTROYER_II)

        # Destroyer II should have AFB ability with value 6 and 3 dice
        assert destroyer_ii_stats.anti_fighter_barrage is True
        assert destroyer_ii_stats.anti_fighter_barrage_value == 6
        assert destroyer_ii_stats.anti_fighter_barrage_dice == 3

        # Verify other confirmed stats
        assert destroyer_ii_stats.combat_value == 8
        assert destroyer_ii_stats.movement == 2

    def test_non_afb_units_have_none_afb_values(self) -> None:
        """Test that units without AFB have None AFB values."""
        provider = UnitStatsProvider()

        # Test various units that don't have AFB
        for unit_type in [UnitType.FIGHTER, UnitType.CRUISER, UnitType.CARRIER]:
            stats = provider.get_unit_stats(unit_type)
            assert stats.anti_fighter_barrage is False
            assert stats.anti_fighter_barrage_value is None
            assert stats.anti_fighter_barrage_dice == 0

    def test_unit_stats_with_modifications_preserves_afb_fields(self) -> None:
        """Test that with_modifications preserves AFB fields."""
        # RED: This test should fail because with_modifications doesn't handle new fields
        original_stats = UnitStats(
            anti_fighter_barrage=True,
            anti_fighter_barrage_value=9,
            anti_fighter_barrage_dice=1,
        )

        modified_stats = original_stats.with_modifications(movement=2)

        assert modified_stats.anti_fighter_barrage is True
        assert modified_stats.anti_fighter_barrage_value == 9
        assert modified_stats.anti_fighter_barrage_dice == 1
        assert modified_stats.movement == 2

    def test_afb_modifications_through_with_modifications(self) -> None:
        """Test that AFB fields can be modified through with_modifications."""
        # RED: This test should fail because with_modifications doesn't handle new fields
        original_stats = UnitStats(
            anti_fighter_barrage=True,
            anti_fighter_barrage_value=9,
            anti_fighter_barrage_dice=1,
        )

        modified_stats = original_stats.with_modifications(
            anti_fighter_barrage_value=8, anti_fighter_barrage_dice=2
        )

        assert modified_stats.anti_fighter_barrage is True
        assert modified_stats.anti_fighter_barrage_value == 8
        assert modified_stats.anti_fighter_barrage_dice == 2

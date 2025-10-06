"""
Tests for Anti-Fighter Barrage Resolution System.

This module tests the AFB dice rolling, hit calculation, and integration
with combat roll modifiers and effects system.
"""

from unittest.mock import patch

from ti4.core.combat import CombatResolver
from ti4.core.constants import UnitType
from ti4.core.unit import Unit


class TestAntiFighterBarrageResolution:
    """Test Anti-Fighter Barrage resolution system."""

    def test_afb_dice_rolling_uses_unit_specific_values(self) -> None:
        """Test that AFB dice rolling uses unit-specific AFB values and dice counts."""
        # RED: This enhanced method doesn't exist yet
        resolver = CombatResolver()
        destroyer = Unit(UnitType.DESTROYER, "player1")
        destroyer_ii = Unit(UnitType.DESTROYER_II, "player1")
        target_fighters = [Unit(UnitType.FIGHTER, "player2")]

        # Mock dice rolls for predictable results
        with patch("random.randint") as mock_randint:
            # Destroyer: AFB value 9, 1 dice - roll 9 (hit)
            mock_randint.return_value = 9
            hits = resolver.perform_anti_fighter_barrage_enhanced(
                destroyer, target_fighters
            )
            assert hits == 1
            mock_randint.assert_called_with(1, 10)  # Standard 10-sided dice

            # Destroyer II: AFB value 6, 3 dice - roll 6, 7, 5 (2 hits)
            mock_randint.side_effect = [6, 7, 5]
            hits = resolver.perform_anti_fighter_barrage_enhanced(
                destroyer_ii, target_fighters
            )
            assert hits == 2
            assert (
                mock_randint.call_count == 4
            )  # 1 from destroyer + 3 from destroyer_ii

    def test_afb_hit_calculation_treats_rolls_as_combat_rolls(self) -> None:
        """Test that AFB hit calculation treats AFB rolls as combat rolls."""
        # RED: This enhanced method doesn't exist yet
        resolver = CombatResolver()
        destroyer = Unit(UnitType.DESTROYER, "player1")
        target_fighters = [Unit(UnitType.FIGHTER, "player2")]

        # Test various dice results against AFB value 9
        with patch("random.randint") as mock_randint:
            # Roll 8 - miss
            mock_randint.return_value = 8
            hits = resolver.perform_anti_fighter_barrage_enhanced(
                destroyer, target_fighters
            )
            assert hits == 0

            # Roll 9 - hit
            mock_randint.return_value = 9
            hits = resolver.perform_anti_fighter_barrage_enhanced(
                destroyer, target_fighters
            )
            assert hits == 1

            # Roll 10 - hit
            mock_randint.return_value = 10
            hits = resolver.perform_anti_fighter_barrage_enhanced(
                destroyer, target_fighters
            )
            assert hits == 1

    def test_afb_with_combat_roll_modifiers(self) -> None:
        """Test that AFB integrates with combat roll modifiers and effects."""
        # RED: This enhanced method with modifiers doesn't exist yet
        resolver = CombatResolver()
        destroyer = Unit(UnitType.DESTROYER, "player1")
        target_fighters = [Unit(UnitType.FIGHTER, "player2")]

        # Test with +1 modifier (makes it easier to hit)
        with patch("random.randint") as mock_randint:
            # Roll 8 with +1 modifier should hit (effective combat value becomes 8)
            mock_randint.return_value = 8
            hits = resolver.perform_anti_fighter_barrage_with_modifiers(
                destroyer, target_fighters, modifier=1
            )
            assert hits == 1

            # Roll 7 with +1 modifier should miss (effective combat value is 8)
            mock_randint.return_value = 7
            hits = resolver.perform_anti_fighter_barrage_with_modifiers(
                destroyer, target_fighters, modifier=1
            )
            assert hits == 0

    def test_afb_with_negative_modifiers(self) -> None:
        """Test AFB with negative modifiers (makes it harder to hit)."""
        # RED: This enhanced method with modifiers doesn't exist yet
        resolver = CombatResolver()
        destroyer = Unit(UnitType.DESTROYER, "player1")
        target_fighters = [Unit(UnitType.FIGHTER, "player2")]

        # Test with -1 modifier (makes it harder to hit)
        with patch("random.randint") as mock_randint:
            # Roll 9 with -1 modifier should miss (effective combat value becomes 10)
            mock_randint.return_value = 9
            hits = resolver.perform_anti_fighter_barrage_with_modifiers(
                destroyer, target_fighters, modifier=-1
            )
            assert hits == 0

            # Roll 10 with -1 modifier should hit (effective combat value is 10)
            mock_randint.return_value = 10
            hits = resolver.perform_anti_fighter_barrage_with_modifiers(
                destroyer, target_fighters, modifier=-1
            )
            assert hits == 1

    def test_afb_no_targets_returns_zero_hits(self) -> None:
        """Test that AFB returns zero hits when no valid targets are present."""
        # RED: This enhanced method doesn't exist yet
        resolver = CombatResolver()
        destroyer = Unit(UnitType.DESTROYER, "player1")

        # No targets
        hits = resolver.perform_anti_fighter_barrage_enhanced(destroyer, [])
        assert hits == 0

        # Non-fighter targets
        non_fighter_targets = [
            Unit(UnitType.CRUISER, "player2"),
            Unit(UnitType.DESTROYER, "player2"),
        ]
        hits = resolver.perform_anti_fighter_barrage_enhanced(
            destroyer, non_fighter_targets
        )
        assert hits == 0

    def test_afb_multiple_dice_resolution(self) -> None:
        """Test AFB resolution with multiple dice (Destroyer II)."""
        # RED: This enhanced method doesn't exist yet
        resolver = CombatResolver()
        destroyer_ii = Unit(UnitType.DESTROYER_II, "player1")
        target_fighters = [Unit(UnitType.FIGHTER, "player2")]

        # Test all dice hit
        with patch("random.randint") as mock_randint:
            mock_randint.side_effect = [6, 7, 8]  # All hit (AFB value 6)
            hits = resolver.perform_anti_fighter_barrage_enhanced(
                destroyer_ii, target_fighters
            )
            assert hits == 3

        # Test mixed results
        with patch("random.randint") as mock_randint:
            mock_randint.side_effect = [5, 6, 7]  # 1 miss, 2 hits
            hits = resolver.perform_anti_fighter_barrage_enhanced(
                destroyer_ii, target_fighters
            )
            assert hits == 2

        # Test all dice miss
        with patch("random.randint") as mock_randint:
            mock_randint.side_effect = [4, 5, 3]  # All miss (AFB value 6)
            hits = resolver.perform_anti_fighter_barrage_enhanced(
                destroyer_ii, target_fighters
            )
            assert hits == 0

    def test_non_afb_unit_returns_zero_hits(self) -> None:
        """Test that units without AFB ability return zero hits."""
        # RED: This enhanced method doesn't exist yet
        resolver = CombatResolver()
        fighter = Unit(UnitType.FIGHTER, "player1")
        cruiser = Unit(UnitType.CRUISER, "player1")
        target_fighters = [Unit(UnitType.FIGHTER, "player2")]

        # Non-AFB units should return 0 hits
        assert (
            resolver.perform_anti_fighter_barrage_enhanced(fighter, target_fighters)
            == 0
        )
        assert (
            resolver.perform_anti_fighter_barrage_enhanced(cruiser, target_fighters)
            == 0
        )

    def test_afb_with_zero_dice_returns_zero_hits(self) -> None:
        """Test that AFB with zero dice returns zero hits."""
        # This tests edge case where AFB ability exists but dice count is 0
        resolver = CombatResolver()

        # Create a mock unit with AFB but 0 dice (edge case)
        from ti4.core.unit_stats import UnitStats

        mock_stats = UnitStats(
            anti_fighter_barrage=True,
            anti_fighter_barrage_value=9,
            anti_fighter_barrage_dice=0,
        )

        # We'll test this through the existing perform_anti_fighter_barrage method
        # which should handle this case
        destroyer = Unit(UnitType.DESTROYER, "player1")
        target_fighters = [Unit(UnitType.FIGHTER, "player2")]

        # Patch the unit's stats to have 0 dice
        with patch.object(destroyer, "get_stats", return_value=mock_stats):
            hits = resolver.perform_anti_fighter_barrage(destroyer, target_fighters)
            assert hits == 0


class TestAntiFighterBarrageIntegration:
    """Test AFB integration with combat system."""

    def test_afb_uses_standard_combat_dice_mechanics(self) -> None:
        """Test that AFB uses the same dice mechanics as regular combat."""
        # This ensures AFB rolls are treated as combat rolls
        resolver = CombatResolver()

        # Test that AFB uses the same hit calculation as regular combat
        dice_results = [6, 7, 8, 9, 10]
        afb_value = 8

        # Should use the same calculation method as regular combat
        expected_hits = resolver.calculate_hits(dice_results, afb_value)
        assert expected_hits == 3  # Rolls 8, 9, 10 hit

    def test_afb_modifier_integration(self) -> None:
        """Test that AFB modifiers work the same as combat modifiers."""
        resolver = CombatResolver()

        # Test modifier calculation consistency
        dice_results = [7, 8, 9]
        base_value = 9
        modifier = 1

        # AFB with modifiers should use same calculation as combat with modifiers
        expected_hits = resolver.calculate_hits_with_modifiers(
            dice_results, base_value, modifier
        )
        assert expected_hits == 2  # With +1 modifier, effective value is 8, so 8,9 hit

    def test_afb_respects_dice_bounds(self) -> None:
        """Test that AFB respects standard dice bounds (1-10)."""
        resolver = CombatResolver()

        # Test extreme modifiers don't break dice bounds
        dice_results = [1, 10]

        # Very large positive modifier
        hits = resolver.calculate_hits_with_modifiers(dice_results, 10, 20)
        assert hits == 2  # Should hit on 1 (minimum bound)

        # Very large negative modifier
        hits = resolver.calculate_hits_with_modifiers(dice_results, 1, -20)
        assert hits == 1  # Should only hit on 10 (maximum bound)

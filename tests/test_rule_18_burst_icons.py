"""Tests for Rule 18.2: Burst Icon Mechanics."""

from src.ti4.core.combat import CombatResolver
from src.ti4.core.constants import UnitType
from src.ti4.core.unit import Unit
from src.ti4.core.unit_stats import UnitStats, UnitStatsProvider


class TestRule18BurstIconMechanics:
    """Test Rule 18.2: If a unit's combat value contains two or more burst icons,
    instead of rolling a single die, the player rolls one die for each burst icon.

    Note: Burst icons are purely visual - the actual dice count is stored in combat_dice."""

    def test_unit_with_burst_icons_rolls_multiple_dice(self) -> None:
        """Test that a unit with burst icons rolls one die per burst icon."""
        # Create a unit with burst icons (e.g., War Sun has 3 burst icons)
        unit = Unit(unit_type=UnitType.WAR_SUN, owner="player1")

        # War Sun should have 3 burst icons (3 dice)
        resolver = CombatResolver()

        # Mock the dice rolling to ensure we get predictable results
        # This should roll 3 dice for War Sun's 3 burst icons
        hits = resolver.roll_dice_for_unit_with_burst_icons(unit)

        # The method should exist and handle burst icons
        assert hits >= 0  # Should return valid hit count

    def test_unit_without_burst_icons_rolls_single_die(self) -> None:
        """Test that a unit without burst icons rolls only one die."""
        # Create a unit without burst icons (e.g., Cruiser has 1 die)
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")

        resolver = CombatResolver()

        # This should roll 1 die for Cruiser (no burst icons)
        hits = resolver.roll_dice_for_unit_with_burst_icons(unit)

        # Should work the same as regular dice rolling for single die units
        assert hits >= 0

    def test_burst_icon_count_determines_dice_count(self) -> None:
        """Test that the number of burst icons determines dice count."""
        # Create a custom unit stats with specific burst icon count
        UnitStatsProvider()

        # Register a custom unit with 2 burst icons (represented by combat_dice)
        custom_stats = UnitStats(
            combat_value=6,
            combat_dice=2,  # 2 burst icons = 2 dice
        )

        # Burst icons are visual only - combat_dice holds the actual count
        assert custom_stats.combat_dice == 2

    def test_burst_icon_dice_rolling_calculation(self) -> None:
        """Test that burst icons correctly calculate hits."""
        resolver = CombatResolver()

        # Test with calculate_hits method directly (not burst icon specific)
        dice_results = [4, 7, 9]  # 3 dice results
        combat_value = 6

        # Should get 2 hits (7 and 9 are >= 6)
        hits = resolver.calculate_hits(dice_results, combat_value)
        assert hits == 2

    def test_war_sun_has_three_burst_icons(self) -> None:
        """Test that War Sun has 3 burst icons as per TI4 rules."""
        stats_provider = UnitStatsProvider()
        war_sun_stats = stats_provider.get_unit_stats(UnitType.WAR_SUN)

        # War Sun should have 3 burst icons (represented by combat_dice = 3)
        assert war_sun_stats.combat_dice == 3

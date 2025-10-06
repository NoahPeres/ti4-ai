"""
Tests for Anti-Fighter Barrage detection and validation.

This module tests the enhanced Unit class AFB capability detection,
validation methods, and target filtering functionality.
"""

import pytest

from ti4.core.constants import UnitType
from ti4.core.unit import Unit


class TestAntiFighterBarrageDetection:
    """Test Anti-Fighter Barrage detection and validation."""

    def test_unit_can_detect_afb_capability(self) -> None:
        """Test that Unit class can properly detect AFB capability using new stats."""

        destroyer = Unit(UnitType.DESTROYER, "player1")
        fighter = Unit(UnitType.FIGHTER, "player1")

        assert destroyer.has_anti_fighter_barrage() is True
        assert fighter.has_anti_fighter_barrage() is False

    def test_unit_get_afb_value_method(self) -> None:
        """Test that Unit class can retrieve AFB value."""
        destroyer = Unit(UnitType.DESTROYER, "player1")
        destroyer_ii = Unit(UnitType.DESTROYER_II, "player1")

        assert destroyer.get_anti_fighter_barrage_value() == 9
        assert destroyer_ii.get_anti_fighter_barrage_value() == 6

    def test_unit_get_afb_dice_count_method(self) -> None:
        """Test that Unit class can retrieve AFB dice count."""
        destroyer = Unit(UnitType.DESTROYER, "player1")
        destroyer_ii = Unit(UnitType.DESTROYER_II, "player1")

        assert destroyer.get_anti_fighter_barrage_dice_count() == 2
        assert destroyer_ii.get_anti_fighter_barrage_dice_count() == 3

    def test_non_afb_unit_raises_error_for_afb_values(self) -> None:
        """Test that non-AFB units raise errors when accessing AFB values."""
        fighter = Unit(UnitType.FIGHTER, "player1")

        with pytest.raises(
            AttributeError, match="does not have anti-fighter barrage ability"
        ):
            fighter.get_anti_fighter_barrage_value()

        with pytest.raises(
            AttributeError, match="does not have anti-fighter barrage ability"
        ):
            fighter.get_anti_fighter_barrage_dice_count()


class TestAntiFighterBarrageValidation:
    """Test Anti-Fighter Barrage validation methods."""

    def test_validate_afb_context_space_combat_only(self) -> None:
        """Test that AFB validation ensures it's only used in space combat."""
        destroyer = Unit(UnitType.DESTROYER, "player1")

        # Should pass for space combat context
        assert destroyer.validate_anti_fighter_barrage_context("space_combat") is True

        # Should fail for other contexts
        assert destroyer.validate_anti_fighter_barrage_context("ground_combat") is False
        assert destroyer.validate_anti_fighter_barrage_context("bombardment") is False

    def test_validate_afb_context_non_afb_unit(self) -> None:
        """Test that non-AFB units fail AFB context validation."""
        fighter = Unit(UnitType.FIGHTER, "player1")

        assert fighter.validate_anti_fighter_barrage_context("space_combat") is False

    def test_can_perform_anti_fighter_barrage_method(self) -> None:
        """Test comprehensive AFB capability check."""
        destroyer = Unit(UnitType.DESTROYER, "player1")
        fighter = Unit(UnitType.FIGHTER, "player1")

        # Destroyer can perform AFB in space combat
        assert destroyer.can_perform_anti_fighter_barrage("space_combat") is True

        # Destroyer cannot perform AFB in other contexts
        assert destroyer.can_perform_anti_fighter_barrage("ground_combat") is False

        # Fighter cannot perform AFB at all
        assert fighter.can_perform_anti_fighter_barrage("space_combat") is False


class TestAntiFighterBarrageTargetFiltering:
    """Test Anti-Fighter Barrage target filtering functionality."""

    def test_is_valid_afb_target_fighters_only(self) -> None:
        """Test that AFB can only target fighters."""
        fighter = Unit(UnitType.FIGHTER, "player2")
        destroyer = Unit(UnitType.DESTROYER, "player2")
        cruiser = Unit(UnitType.CRUISER, "player2")

        assert fighter.is_valid_afb_target() is True
        assert destroyer.is_valid_afb_target() is False
        assert cruiser.is_valid_afb_target() is False

    def test_filter_afb_targets_from_unit_list(self) -> None:
        """Test filtering AFB targets from a list of units."""
        units = [
            Unit(UnitType.FIGHTER, "player2"),
            Unit(UnitType.DESTROYER, "player2"),
            Unit(UnitType.FIGHTER, "player2"),
            Unit(UnitType.CRUISER, "player2"),
        ]

        afb_targets = Unit.filter_afb_targets(units)

        assert len(afb_targets) == 2
        assert all(unit.unit_type == UnitType.FIGHTER for unit in afb_targets)

    def test_filter_enemy_afb_targets(self) -> None:
        """Test filtering AFB targets to only include enemy units."""
        units = [
            Unit(UnitType.FIGHTER, "player1"),  # Same player
            Unit(UnitType.FIGHTER, "player2"),  # Enemy
            Unit(UnitType.DESTROYER, "player2"),  # Enemy but not fighter
            Unit(UnitType.FIGHTER, "player2"),  # Enemy fighter
        ]

        enemy_afb_targets = Unit.filter_enemy_afb_targets(units, "player1")

        assert len(enemy_afb_targets) == 2
        assert all(unit.unit_type == UnitType.FIGHTER for unit in enemy_afb_targets)
        assert all(unit.owner == "player2" for unit in enemy_afb_targets)

    def test_filter_afb_targets_empty_list(self) -> None:
        """Test AFB target filtering with empty unit list."""
        afb_targets = Unit.filter_afb_targets([])
        assert afb_targets == []

    def test_filter_afb_targets_no_fighters(self) -> None:
        """Test AFB target filtering when no fighters are present."""
        units = [
            Unit(UnitType.DESTROYER, "player2"),
            Unit(UnitType.CRUISER, "player2"),
            Unit(UnitType.CARRIER, "player2"),
        ]

        afb_targets = Unit.filter_afb_targets(units)
        assert afb_targets == []

"""
Tests for Anti-Fighter Barrage comprehensive error handling and edge cases.

This module tests the comprehensive error handling, validation, and edge case
scenarios for the Anti-Fighter Barrage system as specified in task 6.
"""

from unittest.mock import patch

import pytest

from ti4.core.combat import CombatResolver
from ti4.core.constants import UnitType
from ti4.core.exceptions import InvalidCombatStateError, InvalidGameStateError
from ti4.core.system import System
from ti4.core.unit import Unit


class TestAntiFighterBarrageContextValidation:
    """Test AFB usage context validation (space combat only)."""

    def test_afb_context_validation_space_combat_only(self) -> None:
        """Test that AFB validation ensures it's only used in space combat context."""
        resolver = CombatResolver()

        # Should pass for space combat context
        assert resolver.validate_afb_context("space_combat") is True

        # Should fail for other contexts
        assert resolver.validate_afb_context("ground_combat") is False
        assert resolver.validate_afb_context("bombardment") is False
        assert resolver.validate_afb_context("invasion") is False
        assert resolver.validate_afb_context("production") is False
        assert resolver.validate_afb_context("") is False
        assert resolver.validate_afb_context(None) is False

    def test_afb_context_validation_with_invalid_context_raises_error(self) -> None:
        """Test that AFB with invalid context raises appropriate error."""
        resolver = CombatResolver()
        destroyer = Unit(UnitType.DESTROYER, "player1")
        target_fighters = [Unit(UnitType.FIGHTER, "player2")]

        # Should raise error when trying to use AFB in wrong context
        with pytest.raises(
            InvalidCombatStateError,
            match="Anti-Fighter Barrage can only be used in space combat",
        ):
            resolver.perform_anti_fighter_barrage_with_context_validation(
                destroyer, target_fighters, "ground_combat"
            )

    def test_afb_context_validation_case_insensitive(self) -> None:
        """Test that AFB context validation is case insensitive."""
        resolver = CombatResolver()

        # Should accept various case formats
        assert resolver.validate_afb_context("SPACE_COMBAT") is True
        assert resolver.validate_afb_context("Space_Combat") is True
        assert resolver.validate_afb_context("space_combat") is True


class TestAntiFighterBarrageNoFightersScenario:
    """Test AFB graceful handling when no fighters are present."""

    def test_afb_with_no_fighters_present_returns_zero_hits(self) -> None:
        """Test that AFB with no fighters present returns zero hits gracefully."""
        resolver = CombatResolver()
        destroyer = Unit(UnitType.DESTROYER, "player1")

        # No units at all
        hits = resolver.perform_anti_fighter_barrage_enhanced(destroyer, [])
        assert hits == 0

        # Non-fighter units only
        non_fighter_units = [
            Unit(UnitType.CRUISER, "player2"),
            Unit(UnitType.DESTROYER, "player2"),
            Unit(UnitType.CARRIER, "player2"),
        ]
        hits = resolver.perform_anti_fighter_barrage_enhanced(
            destroyer, non_fighter_units
        )
        assert hits == 0

    def test_afb_with_no_fighters_logs_appropriate_message(self) -> None:
        """Test that AFB with no fighters logs appropriate informational message."""
        resolver = CombatResolver()
        destroyer = Unit(UnitType.DESTROYER, "player1")

        with patch("ti4.core.combat.logger") as mock_logger:
            resolver.perform_anti_fighter_barrage_enhanced(destroyer, [])

            # Should log info message about no valid targets
            mock_logger.info.assert_called_with(
                "Anti-Fighter Barrage performed by %s but no valid fighter targets found",
                destroyer.unit_type.name,
            )

    def test_afb_phase_with_no_fighters_completes_successfully(self) -> None:
        """Test that AFB phase completes successfully even with no fighters."""
        resolver = CombatResolver()
        system = System("test_system")

        # Add non-fighter units to system
        destroyer = Unit(UnitType.DESTROYER, "player1")
        cruiser = Unit(UnitType.CRUISER, "player2")
        system.place_unit_in_space(destroyer)
        system.place_unit_in_space(cruiser)

        # AFB phase should complete without errors
        result = resolver.resolve_anti_fighter_barrage_phase(
            system, "player1", "player2"
        )

        assert result.attacker_hits == 0
        assert result.defender_hits == 0
        assert len(result.destroyed_fighters) == 0


class TestAntiFighterBarrageInvalidHitAssignments:
    """Test clear error messages for invalid hit assignments."""

    def test_invalid_hit_assignment_duplicate_fighters_error_message(self) -> None:
        """Test clear error message for duplicate fighter assignments."""
        resolver = CombatResolver()
        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        fighters = [fighter1]

        with pytest.raises(ValueError) as exc_info:
            resolver.validate_afb_hit_assignments(fighters, ["fighter1", "fighter1"], 2)

        assert "Duplicate fighter assignment" in str(exc_info.value)
        assert "fighter1" in str(exc_info.value)

    def test_invalid_hit_assignment_nonexistent_fighter_error_message(self) -> None:
        """Test clear error message for nonexistent fighter assignments."""
        resolver = CombatResolver()
        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        fighters = [fighter1]

        with pytest.raises(ValueError) as exc_info:
            resolver.validate_afb_hit_assignments(fighters, ["nonexistent"], 1)

        assert "Fighter with ID 'nonexistent' not found" in str(exc_info.value)
        assert "Available fighters:" in str(exc_info.value)

    def test_invalid_hit_assignment_wrong_count_error_message(self) -> None:
        """Test clear error message for wrong number of assignments."""
        resolver = CombatResolver()
        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        fighter2 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter2")
        fighters = [fighter1, fighter2]

        # Too many assignments
        with pytest.raises(ValueError) as exc_info:
            resolver.validate_afb_hit_assignments(fighters, ["fighter1", "fighter2"], 1)

        assert "Expected 1 hit assignments, but received 2" in str(exc_info.value)

        # Too few assignments
        with pytest.raises(ValueError) as exc_info:
            resolver.validate_afb_hit_assignments(fighters, ["fighter1"], 2)

        assert "Expected 2 hit assignments, but received 1" in str(exc_info.value)

    def test_invalid_hit_assignment_non_fighter_target_error_message(self) -> None:
        """Test clear error message when trying to assign hits to non-fighters."""
        resolver = CombatResolver()
        cruiser = Unit(UnitType.CRUISER, "player2", unit_id="cruiser1")
        units = [cruiser]

        with pytest.raises(ValueError) as exc_info:
            resolver.validate_afb_hit_assignments(units, ["cruiser1"], 1)

        assert "Unit 'cruiser1' (CRUISER) is not a valid AFB target" in str(
            exc_info.value
        )
        assert "Only fighters can be targeted by Anti-Fighter Barrage" in str(
            exc_info.value
        )


class TestAntiFighterBarrageGameStateConsistency:
    """Test game state consistency checks and recovery mechanisms."""

    def test_afb_with_corrupted_unit_stats_raises_error(self) -> None:
        """Test that AFB with corrupted unit stats raises appropriate error."""
        resolver = CombatResolver()
        destroyer = Unit(UnitType.DESTROYER, "player1")
        target_fighters = [Unit(UnitType.FIGHTER, "player2")]

        # Mock corrupted stats (AFB enabled but no value)
        with patch.object(destroyer, "get_stats") as mock_stats:
            mock_stats.return_value.anti_fighter_barrage = True
            mock_stats.return_value.anti_fighter_barrage_value = None
            mock_stats.return_value.anti_fighter_barrage_dice = 1

            with pytest.raises(InvalidGameStateError, match="Corrupted AFB stats"):
                resolver.perform_anti_fighter_barrage_enhanced(
                    destroyer, target_fighters
                )

    def test_afb_with_invalid_system_state_raises_error(self) -> None:
        """Test that AFB with invalid system state raises appropriate error."""
        resolver = CombatResolver()
        system = None  # Invalid system

        with pytest.raises(
            InvalidGameStateError, match="Invalid system state for AFB resolution"
        ):
            resolver.resolve_anti_fighter_barrage_phase(system, "player1", "player2")

    def test_afb_with_missing_player_units_raises_error(self) -> None:
        """Test that AFB with missing player units raises appropriate error."""
        resolver = CombatResolver()
        system = System("test_system")

        # System has no units for the specified players
        with pytest.raises(InvalidGameStateError, match="No units found for player"):
            resolver.resolve_anti_fighter_barrage_phase(
                system, "nonexistent_player", "player2"
            )

    def test_afb_game_state_recovery_after_error(self) -> None:
        """Test that game state can recover after AFB errors."""
        resolver = CombatResolver()
        system = System("test_system")

        # Add valid units
        destroyer = Unit(UnitType.DESTROYER, "player1")
        fighter = Unit(UnitType.FIGHTER, "player2")
        system.place_unit_in_space(destroyer)
        system.place_unit_in_space(fighter)

        # Simulate error during AFB resolution
        with patch.object(
            resolver,
            "perform_anti_fighter_barrage_enhanced",
            side_effect=RuntimeError("Test error"),
        ):
            with pytest.raises(RuntimeError):
                resolver.resolve_anti_fighter_barrage_phase(
                    system, "player1", "player2"
                )

        # System should still be in valid state
        assert len(system.space_units) == 2
        assert destroyer in system.space_units
        assert fighter in system.space_units

    def test_afb_consistency_check_validates_unit_ownership(self) -> None:
        """Test that AFB consistency checks validate unit ownership."""
        resolver = CombatResolver()

        # Fighter with wrong owner in assignment
        fighter1 = Unit(
            UnitType.FIGHTER, "player1", unit_id="fighter1"
        )  # Same player as attacker
        fighters = [fighter1]

        with pytest.raises(ValueError, match="Cannot assign AFB hits to own units"):
            resolver.validate_afb_hit_assignments_with_ownership(
                fighters, ["fighter1"], 1, attacking_player="player1"
            )

    def test_afb_consistency_check_validates_round_number(self) -> None:
        """Test that AFB consistency checks validate it's first round only."""
        resolver = CombatResolver()
        destroyer = Unit(UnitType.DESTROYER, "player1")
        target_fighters = [Unit(UnitType.FIGHTER, "player2")]

        # Should fail if not first round
        with pytest.raises(
            InvalidCombatStateError,
            match="Anti-Fighter Barrage only allowed in first round",
        ):
            resolver.perform_anti_fighter_barrage_with_round_validation(
                destroyer, target_fighters, round_number=2
            )


class TestAntiFighterBarrageEdgeCases:
    """Test additional edge cases for AFB system."""

    def test_afb_with_zero_dice_unit_handles_gracefully(self) -> None:
        """Test that AFB with zero dice unit handles gracefully."""
        resolver = CombatResolver()

        # Create unit with AFB but zero dice (edge case)
        from ti4.core.unit_stats import UnitStats

        zero_dice_stats = UnitStats(
            anti_fighter_barrage=True,
            anti_fighter_barrage_value=9,
            anti_fighter_barrage_dice=0,
        )

        destroyer = Unit(UnitType.DESTROYER, "player1")
        target_fighters = [Unit(UnitType.FIGHTER, "player2")]

        with patch.object(destroyer, "get_stats", return_value=zero_dice_stats):
            hits = resolver.perform_anti_fighter_barrage_enhanced(
                destroyer, target_fighters
            )
            assert hits == 0

    def test_afb_with_extremely_high_dice_count_handles_gracefully(self) -> None:
        """Test that AFB with extremely high dice count handles gracefully."""
        resolver = CombatResolver()

        # Create unit with very high dice count
        from ti4.core.unit_stats import UnitStats

        high_dice_stats = UnitStats(
            anti_fighter_barrage=True,
            anti_fighter_barrage_value=9,
            anti_fighter_barrage_dice=1000,  # Extremely high
        )

        destroyer = Unit(UnitType.DESTROYER, "player1")
        target_fighters = [Unit(UnitType.FIGHTER, "player2")]

        with patch.object(destroyer, "get_stats", return_value=high_dice_stats):
            with patch("random.randint", return_value=10):  # All hits
                hits = resolver.perform_anti_fighter_barrage_enhanced(
                    destroyer, target_fighters
                )
                assert hits == 1000  # Should handle large numbers

    def test_afb_with_invalid_dice_value_raises_error(self) -> None:
        """Test that AFB with invalid dice value raises appropriate error."""
        resolver = CombatResolver()

        # Create unit with invalid AFB value
        from ti4.core.unit_stats import UnitStats

        invalid_stats = UnitStats(
            anti_fighter_barrage=True,
            anti_fighter_barrage_value=15,  # Invalid (> 10)
            anti_fighter_barrage_dice=1,
        )

        destroyer = Unit(UnitType.DESTROYER, "player1")
        target_fighters = [Unit(UnitType.FIGHTER, "player2")]

        with patch.object(destroyer, "get_stats", return_value=invalid_stats):
            with pytest.raises(ValueError, match="Invalid AFB value"):
                resolver.perform_anti_fighter_barrage_enhanced(
                    destroyer, target_fighters
                )

    def test_afb_with_negative_dice_count_raises_error(self) -> None:
        """Test that AFB with negative dice count raises appropriate error."""
        resolver = CombatResolver()

        # Create unit with negative dice count
        from ti4.core.unit_stats import UnitStats

        negative_dice_stats = UnitStats(
            anti_fighter_barrage=True,
            anti_fighter_barrage_value=9,
            anti_fighter_barrage_dice=-1,  # Invalid
        )

        destroyer = Unit(UnitType.DESTROYER, "player1")
        target_fighters = [Unit(UnitType.FIGHTER, "player2")]

        with patch.object(destroyer, "get_stats", return_value=negative_dice_stats):
            with pytest.raises(ValueError, match="AFB dice count cannot be negative"):
                resolver.perform_anti_fighter_barrage_enhanced(
                    destroyer, target_fighters
                )


class TestAntiFighterBarrageSystemIntegration:
    """Test AFB system integration with comprehensive error handling."""

    def test_complete_afb_system_with_all_validations(self) -> None:
        """Test complete AFB system with all validations enabled."""
        resolver = CombatResolver()
        system = System("test_system")

        # Setup valid scenario
        destroyer = Unit(UnitType.DESTROYER, "player1")
        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        fighter2 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter2")

        system.place_unit_in_space(destroyer)
        system.place_unit_in_space(fighter1)
        system.place_unit_in_space(fighter2)

        # Should complete successfully with all validations
        result = resolver.resolve_anti_fighter_barrage_phase_with_full_validation(
            system, "player1", "player2", round_number=1, context="space_combat"
        )

        assert result is not None
        assert result.attacker_hits >= 0
        assert result.defender_hits >= 0

    def test_afb_system_error_recovery_maintains_consistency(self) -> None:
        """Test that AFB system error recovery maintains game state consistency."""
        resolver = CombatResolver()
        system = System("test_system")

        # Setup scenario
        destroyer = Unit(UnitType.DESTROYER, "player1")
        fighter = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")

        system.place_unit_in_space(destroyer)
        system.place_unit_in_space(fighter)

        original_unit_count = len(system.space_units)

        # Simulate error during hit assignment by making assign_afb_hits_to_fighters fail
        # and ensuring _simulate_afb_hit_assignment doesn't catch it
        def failing_assignment(*args, **kwargs):
            raise RuntimeError("Assignment error")

        # Mock AFB to always produce hits so hit assignment is called
        with patch.object(
            resolver, "perform_anti_fighter_barrage_enhanced", return_value=1
        ):
            with patch.object(
                resolver, "assign_afb_hits_to_fighters", side_effect=failing_assignment
            ):
                # Also patch _simulate_afb_hit_assignment to not catch the exception
                with patch.object(
                    resolver,
                    "_simulate_afb_hit_assignment",
                    side_effect=failing_assignment,
                ):
                    with pytest.raises(RuntimeError):
                        resolver.resolve_anti_fighter_barrage_phase(
                            system, "player1", "player2"
                        )

        # System should maintain consistency
        assert len(system.space_units) == original_unit_count
        assert destroyer in system.space_units
        assert fighter in system.space_units

    def test_afb_system_with_concurrent_modifications_raises_error(self) -> None:
        """Test that AFB system detects concurrent modifications and raises error."""
        resolver = CombatResolver()
        system = System("test_system")

        destroyer = Unit(UnitType.DESTROYER, "player1")
        fighter = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")

        system.place_unit_in_space(destroyer)
        system.place_unit_in_space(fighter)

        # Mock concurrent modification during AFB resolution
        def mock_afb_with_modification(*args, **kwargs):
            # Simulate another process removing the fighter
            system.remove_unit_from_space(fighter)
            return 1  # Return hits even though fighter was removed

        with patch.object(
            resolver,
            "perform_anti_fighter_barrage_enhanced",
            side_effect=mock_afb_with_modification,
        ):
            with pytest.raises(InvalidGameStateError, match="Game state.*during AFB"):
                resolver.resolve_anti_fighter_barrage_phase_with_consistency_check(
                    system, "player1", "player2"
                )

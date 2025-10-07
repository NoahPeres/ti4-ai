"""
Tests for Anti-Fighter Barrage Hit Assignment and Fighter Destruction.

This module tests the AFB hit assignment validation system, fighter selection
and destruction mechanics, and excess hit handling.
"""

from unittest.mock import patch

import pytest

from ti4.core.combat import CombatResolver
from ti4.core.constants import UnitType
from ti4.core.unit import Unit


class TestAntiFighterBarrageHitAssignment:
    """Test Anti-Fighter Barrage hit assignment system."""

    def test_validate_afb_hit_assignments_valid_assignments(self) -> None:
        """Test validation of valid AFB hit assignments."""
        resolver = CombatResolver()

        # Create fighter targets
        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        fighter2 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter2")
        fighter3 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter3")
        fighters = [fighter1, fighter2, fighter3]

        # Valid assignment: 2 hits to 2 different fighters
        assignments = ["fighter1", "fighter2"]
        is_valid = resolver.validate_afb_hit_assignments(fighters, assignments, 2)
        assert is_valid is True

        # Valid assignment: 1 hit to 1 fighter
        assignments = ["fighter3"]
        is_valid = resolver.validate_afb_hit_assignments(fighters, assignments, 1)
        assert is_valid is True

    def test_validate_afb_hit_assignments_invalid_assignments(self) -> None:
        """Test validation rejects invalid AFB hit assignments."""
        resolver = CombatResolver()

        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        fighter2 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter2")
        fighters = [fighter1, fighter2]

        # Invalid: Wrong number of assignments (too many)
        assignments = ["fighter1", "fighter2"]
        with pytest.raises(
            ValueError, match="Expected 1 hit assignments, but received 2"
        ):
            resolver.validate_afb_hit_assignments(fighters, assignments, 1)

        # Invalid: Wrong number of assignments (too few)
        assignments = ["fighter1"]
        with pytest.raises(
            ValueError, match="Expected 2 hit assignments, but received 1"
        ):
            resolver.validate_afb_hit_assignments(fighters, assignments, 2)

        # Invalid: Non-existent fighter ID
        assignments = ["nonexistent_fighter"]
        with pytest.raises(
            ValueError, match="Fighter with ID 'nonexistent_fighter' not found"
        ):
            resolver.validate_afb_hit_assignments(fighters, assignments, 1)

        # Invalid: Duplicate assignments
        assignments = ["fighter1", "fighter1"]
        with pytest.raises(ValueError, match="Duplicate fighter assignment"):
            resolver.validate_afb_hit_assignments(fighters, assignments, 2)

    def test_assign_afb_hits_to_fighters(self) -> None:
        """Test assigning AFB hits to specific fighters."""
        resolver = CombatResolver()

        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        fighter2 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter2")
        fighter3 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter3")
        fighters = [fighter1, fighter2, fighter3]

        # Assign 2 hits to specific fighters
        assignments = ["fighter1", "fighter3"]
        destroyed = resolver.assign_afb_hits_to_fighters(fighters, assignments)

        # Should return the destroyed fighters
        assert len(destroyed) == 2
        assert fighter1 in destroyed
        assert fighter3 in destroyed
        assert fighter2 not in destroyed

    def test_assign_afb_hits_empty_assignments(self) -> None:
        """Test assigning AFB hits with empty assignments."""
        resolver = CombatResolver()

        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        fighters = [fighter1]

        # No assignments should return no destroyed units
        destroyed = resolver.assign_afb_hits_to_fighters(fighters, [])
        assert len(destroyed) == 0

    def test_handle_excess_afb_hits(self) -> None:
        """Test that excess AFB hits beyond available fighters have no effect."""
        resolver = CombatResolver()

        # Only 2 fighters available
        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        fighter2 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter2")
        fighters = [fighter1, fighter2]

        # 3 hits but only 2 fighters - excess hits should be ignored
        max_assignments = resolver.calculate_max_afb_assignments(fighters, 3)
        assert max_assignments == 2  # Can only assign to available fighters

        # Validate that we can only assign up to the number of available fighters
        assignments = ["fighter1", "fighter2"]
        with pytest.raises(
            ValueError, match="Expected 3 hit assignments, but received 2"
        ):
            resolver.validate_afb_hit_assignments(fighters, assignments, 3)

    def test_afb_hit_assignment_with_no_fighters(self) -> None:
        """Test AFB hit assignment when no fighters are present."""
        resolver = CombatResolver()

        # No fighters available
        fighters = []

        # Any hits should have no effect
        max_assignments = resolver.calculate_max_afb_assignments(fighters, 5)
        assert max_assignments == 0

        # No assignments possible
        destroyed = resolver.assign_afb_hits_to_fighters(fighters, [])
        assert len(destroyed) == 0

    def test_afb_hit_assignment_validation_with_mixed_units(self) -> None:
        """Test that AFB hit assignment only works with fighters."""
        resolver = CombatResolver()

        # Mix of fighters and non-fighters
        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        cruiser = Unit(UnitType.CRUISER, "player2", unit_id="cruiser1")
        destroyer = Unit(UnitType.DESTROYER, "player2", unit_id="destroyer1")
        units = [fighter1, cruiser, destroyer]

        # Should only be able to assign to fighters
        assignments = ["fighter1"]
        is_valid = resolver.validate_afb_hit_assignments(units, assignments, 1)
        assert is_valid is True

        # Cannot assign to non-fighters
        assignments = ["cruiser1"]
        with pytest.raises(
            ValueError, match="Unit 'cruiser1' \\(CRUISER\\) is not a valid AFB target"
        ):
            resolver.validate_afb_hit_assignments(units, assignments, 1)


class TestAntiFighterBarrageFighterDestruction:
    """Test Anti-Fighter Barrage fighter destruction mechanics."""

    def test_destroy_fighters_from_afb_hits(self) -> None:
        """Test that fighters are properly destroyed from AFB hits."""
        resolver = CombatResolver()

        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        fighter2 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter2")
        fighters = [fighter1, fighter2]

        # Destroy both fighters
        assignments = ["fighter1", "fighter2"]
        destroyed = resolver.assign_afb_hits_to_fighters(fighters, assignments)

        assert len(destroyed) == 2
        assert fighter1 in destroyed
        assert fighter2 in destroyed

    def test_partial_fighter_destruction(self) -> None:
        """Test partial destruction of fighters from AFB hits."""
        resolver = CombatResolver()

        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        fighter2 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter2")
        fighter3 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter3")
        fighters = [fighter1, fighter2, fighter3]

        # Only destroy 2 out of 3 fighters
        assignments = ["fighter1", "fighter3"]
        destroyed = resolver.assign_afb_hits_to_fighters(fighters, assignments)

        assert len(destroyed) == 2
        assert fighter1 in destroyed
        assert fighter3 in destroyed
        assert fighter2 not in destroyed

    def test_fighter_destruction_preserves_other_units(self) -> None:
        """Test that AFB fighter destruction doesn't affect other unit types."""
        resolver = CombatResolver()

        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        cruiser = Unit(UnitType.CRUISER, "player2", unit_id="cruiser1")
        destroyer = Unit(UnitType.DESTROYER, "player2", unit_id="destroyer1")
        all_units = [fighter1, cruiser, destroyer]

        # Only assign to fighter
        assignments = ["fighter1"]
        destroyed = resolver.assign_afb_hits_to_fighters(all_units, assignments)

        # Only the fighter should be destroyed
        assert len(destroyed) == 1
        assert fighter1 in destroyed
        assert cruiser not in destroyed
        assert destroyer not in destroyed


class TestAntiFighterBarrageExcessHitHandling:
    """Test Anti-Fighter Barrage excess hit handling."""

    def test_excess_hits_beyond_available_fighters(self) -> None:
        """Test that excess hits beyond available fighters have no effect."""
        resolver = CombatResolver()

        # Only 1 fighter available
        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        fighters = [fighter1]

        # 3 hits but only 1 fighter
        max_assignments = resolver.calculate_max_afb_assignments(fighters, 3)
        assert max_assignments == 1  # Can only destroy 1 fighter

        # Can only assign to the available fighter
        assignments = ["fighter1"]
        destroyed = resolver.assign_afb_hits_to_fighters(fighters, assignments)
        assert len(destroyed) == 1
        assert fighter1 in destroyed

    def test_zero_hits_no_destruction(self) -> None:
        """Test that zero hits result in no fighter destruction."""
        resolver = CombatResolver()

        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        fighter2 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter2")
        fighters = [fighter1, fighter2]

        # 0 hits should result in no assignments
        max_assignments = resolver.calculate_max_afb_assignments(fighters, 0)
        assert max_assignments == 0

        # No assignments should destroy no fighters
        destroyed = resolver.assign_afb_hits_to_fighters(fighters, [])
        assert len(destroyed) == 0

    def test_hits_equal_to_fighter_count(self) -> None:
        """Test hits exactly equal to the number of available fighters."""
        resolver = CombatResolver()

        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        fighter2 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter2")
        fighters = [fighter1, fighter2]

        # 2 hits for 2 fighters - perfect match
        max_assignments = resolver.calculate_max_afb_assignments(fighters, 2)
        assert max_assignments == 2

        assignments = ["fighter1", "fighter2"]
        destroyed = resolver.assign_afb_hits_to_fighters(fighters, assignments)
        assert len(destroyed) == 2
        assert fighter1 in destroyed
        assert fighter2 in destroyed


class TestAntiFighterBarrageIntegrationWithHitAssignment:
    """Test AFB integration with hit assignment system."""

    def test_complete_afb_resolution_with_hit_assignment(self) -> None:
        """Test complete AFB resolution including hit assignment."""
        # This will test the integration once we implement the methods
        resolver = CombatResolver()

        # Setup: Destroyer vs 3 fighters
        destroyer = Unit(UnitType.DESTROYER, "player1")
        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        fighter2 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter2")
        fighter3 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter3")
        target_fighters = [fighter1, fighter2, fighter3]

        # Mock AFB to produce 2 hits
        with patch.object(
            resolver, "perform_anti_fighter_barrage_enhanced", return_value=2
        ):
            hits = resolver.perform_anti_fighter_barrage_enhanced(
                destroyer, target_fighters
            )
            assert hits == 2

            # Player chooses which fighters to destroy
            assignments = ["fighter1", "fighter3"]

            # Validate assignment
            is_valid = resolver.validate_afb_hit_assignments(
                target_fighters, assignments, hits
            )
            assert is_valid is True

            # Apply assignment
            destroyed = resolver.assign_afb_hits_to_fighters(
                target_fighters, assignments
            )
            assert len(destroyed) == 2
            assert fighter1 in destroyed
            assert fighter3 in destroyed
            assert fighter2 not in destroyed

    def test_afb_with_insufficient_fighters_for_hits(self) -> None:
        """Test AFB when there are more hits than fighters."""
        resolver = CombatResolver()

        # Setup: Destroyer vs 1 fighter
        destroyer = Unit(UnitType.DESTROYER, "player1")
        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        target_fighters = [fighter1]

        # Mock AFB to produce 3 hits (more than available fighters)
        with patch.object(
            resolver, "perform_anti_fighter_barrage_enhanced", return_value=3
        ):
            hits = resolver.perform_anti_fighter_barrage_enhanced(
                destroyer, target_fighters
            )
            assert hits == 3

            # Can only assign to available fighters
            max_assignments = resolver.calculate_max_afb_assignments(
                target_fighters, hits
            )
            assert max_assignments == 1

            # Player can only destroy the available fighter
            assignments = ["fighter1"]
            destroyed = resolver.assign_afb_hits_to_fighters(
                target_fighters, assignments
            )
            assert len(destroyed) == 1
            assert fighter1 in destroyed


class TestAntiFighterBarrageErrorHandling:
    """Test AFB error handling and edge cases."""

    def test_validate_afb_hit_assignments_negative_hits_raises_error(self) -> None:
        """Test that negative expected hits raises ValueError."""
        resolver = CombatResolver()
        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        fighters = [fighter1]

        with pytest.raises(ValueError, match="expected_hits must be non-negative"):
            resolver.validate_afb_hit_assignments(fighters, [], -1)

    def test_assign_afb_hits_invalid_unit_id_raises_error(self) -> None:
        """Test that invalid unit ID raises ValueError."""
        resolver = CombatResolver()
        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        fighters = [fighter1]

        with pytest.raises(ValueError, match="Unit ID 'nonexistent' not found"):
            resolver.assign_afb_hits_to_fighters(fighters, ["nonexistent"])

    def test_assign_afb_hits_non_fighter_unit_raises_error(self) -> None:
        """Test that assigning hits to non-fighter raises ValueError."""
        resolver = CombatResolver()
        cruiser = Unit(UnitType.CRUISER, "player2", unit_id="cruiser1")
        units = [cruiser]

        with pytest.raises(ValueError, match="is not a valid AFB target"):
            resolver.assign_afb_hits_to_fighters(units, ["cruiser1"])

    def test_assign_afb_hits_to_empty_units_with_assignments_raises_error(self) -> None:
        """Test that assigning hits when no units available raises ValueError."""
        resolver = CombatResolver()

        with pytest.raises(
            ValueError, match="Cannot assign hits when no units are available"
        ):
            resolver.assign_afb_hits_to_fighters([], ["fighter1"])

    def test_calculate_max_afb_assignments_negative_hits_raises_error(self) -> None:
        """Test that negative hits raises ValueError."""
        resolver = CombatResolver()
        fighter1 = Unit(UnitType.FIGHTER, "player2", unit_id="fighter1")
        fighters = [fighter1]

        with pytest.raises(ValueError, match="hits must be non-negative"):
            resolver.calculate_max_afb_assignments(fighters, -1)

"""
Tests for Anti-Fighter Barrage integration with Space Combat Flow.

This module tests the integration of AFB as the first step of space combat
during tactical actions, including timing restrictions and proper sequencing.
"""

from unittest.mock import patch

from ti4.core.combat import CombatResolver
from ti4.core.constants import UnitType
from ti4.core.system import System
from ti4.core.unit import Unit


class TestAntiFighterBarrageSpaceCombatIntegration:
    """Test AFB integration with space combat flow."""

    def test_afb_occurs_as_first_step_of_space_combat(self) -> None:
        """Test that AFB occurs as the first step of space combat during tactical actions."""
        resolver = CombatResolver()
        system = System("test_system")

        # Setup: Destroyer vs Fighters
        destroyer = Unit(UnitType.DESTROYER, "player1")
        fighter1 = Unit(UnitType.FIGHTER, "player2")
        fighter2 = Unit(UnitType.FIGHTER, "player2")

        system.place_unit_in_space(destroyer)
        system.place_unit_in_space(fighter1)
        system.place_unit_in_space(fighter2)

        # Mock AFB resolution to return 1 hit
        with patch.object(
            resolver, "perform_anti_fighter_barrage_enhanced", return_value=1
        ):
            # Execute space combat with AFB phase
            result = resolver.resolve_space_combat_with_afb(
                system, "player1", "player2"
            )

            # AFB should have been called first
            resolver.perform_anti_fighter_barrage_enhanced.assert_called()
            assert result.afb_hits_attacker == 1
            assert result.afb_hits_defender == 0

    def test_afb_timing_restrictions_first_round_only(self) -> None:
        """Test that AFB only occurs during the first round of space combat."""
        resolver = CombatResolver()
        system = System("test_system")

        destroyer = Unit(UnitType.DESTROYER, "player1")
        fighter = Unit(UnitType.FIGHTER, "player2")

        system.place_unit_in_space(destroyer)
        system.place_unit_in_space(fighter)

        # Mock combat to simulate multiple rounds
        with patch.object(
            resolver, "perform_anti_fighter_barrage_enhanced", return_value=0
        ) as mock_afb:
            # First round - AFB should occur
            resolver.resolve_space_combat_round_with_afb(
                system, "player1", "player2", round_number=1
            )
            assert mock_afb.call_count == 1

            # Second round - AFB should NOT occur
            resolver.resolve_space_combat_round_with_afb(
                system, "player1", "player2", round_number=2
            )
            assert mock_afb.call_count == 1  # Still only called once

    def test_afb_occurs_before_regular_combat_rolls(self) -> None:
        """Test that AFB occurs before regular combat rolls but after combat setup."""
        resolver = CombatResolver()
        system = System("test_system")

        destroyer = Unit(UnitType.DESTROYER, "player1")
        cruiser = Unit(UnitType.CRUISER, "player1")
        fighter = Unit(UnitType.FIGHTER, "player2")

        system.place_unit_in_space(destroyer)
        system.place_unit_in_space(cruiser)
        system.place_unit_in_space(fighter)

        call_order = []

        def track_afb_call(*args, **kwargs):
            call_order.append("afb")
            return 1

        def track_combat_call(*args, **kwargs):
            call_order.append("combat")
            return 1

        with patch.object(
            resolver,
            "perform_anti_fighter_barrage_enhanced",
            side_effect=track_afb_call,
        ):
            with patch.object(
                resolver, "roll_dice_for_unit", side_effect=track_combat_call
            ):
                resolver.resolve_space_combat_with_afb(system, "player1", "player2")

                # AFB should be called before regular combat
                assert call_order[0] == "afb"
                assert "combat" in call_order
                assert call_order.index("afb") < call_order.index("combat")

    def test_afb_integration_with_tactical_action_combat_flow(self) -> None:
        """Test AFB integration with existing tactical action combat flow."""
        resolver = CombatResolver()
        system = System("test_system")

        # Setup combat scenario
        destroyer = Unit(UnitType.DESTROYER, "player1")
        fighter1 = Unit(UnitType.FIGHTER, "player2")
        fighter2 = Unit(UnitType.FIGHTER, "player2")

        system.place_unit_in_space(destroyer)
        system.place_unit_in_space(fighter1)
        system.place_unit_in_space(fighter2)

        # Mock AFB to destroy one fighter
        with patch.object(
            resolver, "perform_anti_fighter_barrage_enhanced", return_value=1
        ):
            with patch.object(
                resolver, "assign_afb_hits_to_fighters", return_value=[fighter1]
            ):
                result = resolver.resolve_tactical_action_space_combat(
                    system, "player1"
                )

                # AFB should have been resolved
                assert result.afb_phase_completed is True
                assert len(result.destroyed_by_afb) == 1
                assert fighter1 in result.destroyed_by_afb

    def test_afb_with_no_valid_targets_still_executes(self) -> None:
        """Test that AFB executes even when no valid targets are present."""
        resolver = CombatResolver()
        system = System("test_system")

        # Setup: Destroyer vs Cruiser (no fighters)
        destroyer = Unit(UnitType.DESTROYER, "player1")
        cruiser = Unit(UnitType.CRUISER, "player2")

        system.place_unit_in_space(destroyer)
        system.place_unit_in_space(cruiser)

        with patch.object(
            resolver, "perform_anti_fighter_barrage_enhanced", return_value=0
        ) as mock_afb:
            result = resolver.resolve_space_combat_with_afb(
                system, "player1", "player2"
            )

            # AFB should still be called even with no valid targets
            mock_afb.assert_called_once()
            assert result.afb_hits_attacker == 0

    def test_afb_simultaneous_resolution_both_players(self) -> None:
        """Test that AFB is resolved simultaneously for both players."""
        resolver = CombatResolver()
        system = System("test_system")

        # Setup: Both players have destroyers and fighters
        destroyer1 = Unit(UnitType.DESTROYER, "player1")
        fighter1 = Unit(UnitType.FIGHTER, "player1")
        destroyer2 = Unit(UnitType.DESTROYER, "player2")
        fighter2 = Unit(UnitType.FIGHTER, "player2")

        system.place_unit_in_space(destroyer1)
        system.place_unit_in_space(fighter1)
        system.place_unit_in_space(destroyer2)
        system.place_unit_in_space(fighter2)

        # Mock AFB for both players
        def mock_afb_side_effect(unit, targets):
            if unit.owner == "player1":
                return 1  # Player 1 destroyer hits
            else:
                return 1  # Player 2 destroyer hits

        with patch.object(
            resolver,
            "perform_anti_fighter_barrage_enhanced",
            side_effect=mock_afb_side_effect,
        ):
            result = resolver.resolve_space_combat_with_afb(
                system, "player1", "player2"
            )

            # Both players should have AFB hits
            assert result.afb_hits_attacker == 1
            assert result.afb_hits_defender == 1


class TestAntiFighterBarrageResult:
    """Test AFB result data structure."""

    def test_afb_result_contains_required_fields(self) -> None:
        """Test that AFB result contains all required fields."""
        from ti4.core.combat import AntiFighterBarrageResult

        result = AntiFighterBarrageResult(
            attacker_hits=2,
            defender_hits=1,
            destroyed_fighters=[],
            remaining_fighters=[],
        )

        assert result.attacker_hits == 2
        assert result.defender_hits == 1
        assert isinstance(result.destroyed_fighters, list)
        assert isinstance(result.remaining_fighters, list)


class TestSpaceCombatWithAFBResult:
    """Test space combat result with AFB integration."""

    def test_space_combat_result_includes_afb_data(self) -> None:
        """Test that space combat result includes AFB phase data."""
        from ti4.core.combat import SpaceCombatResult

        result = SpaceCombatResult(
            winner="player1",
            afb_phase_completed=True,
            afb_hits_attacker=2,
            afb_hits_defender=0,
            destroyed_by_afb=[],
            regular_combat_completed=True,
        )

        assert result.afb_phase_completed is True
        assert result.afb_hits_attacker == 2
        assert result.afb_hits_defender == 0
        assert isinstance(result.destroyed_by_afb, list)


class TestAntiFighterBarrageTimingValidation:
    """Test AFB timing validation and restrictions."""

    def test_afb_only_in_space_combat_context(self) -> None:
        """Test that AFB is only usable in space combat context."""
        resolver = CombatResolver()

        # Should be valid in space combat
        assert resolver.validate_afb_context("space_combat") is True

        # Should be invalid in other contexts
        assert resolver.validate_afb_context("ground_combat") is False
        assert resolver.validate_afb_context("bombardment") is False

    def test_afb_round_restriction_validation(self) -> None:
        """Test that AFB is restricted to first round only."""
        resolver = CombatResolver()

        # Should be valid in round 1
        assert resolver.can_perform_afb_in_round(1) is True

        # Should be invalid in subsequent rounds
        assert resolver.can_perform_afb_in_round(2) is False
        assert resolver.can_perform_afb_in_round(3) is False


class TestAntiFighterBarrageIntegrationEdgeCases:
    """Test AFB integration edge cases."""

    def test_afb_with_mixed_unit_types(self) -> None:
        """Test AFB integration with mixed unit types in combat."""
        resolver = CombatResolver()
        system = System("test_system")

        # Mix of AFB and non-AFB units
        destroyer = Unit(UnitType.DESTROYER, "player1")  # Has AFB
        cruiser = Unit(UnitType.CRUISER, "player1")  # No AFB
        fighter1 = Unit(UnitType.FIGHTER, "player2")
        fighter2 = Unit(UnitType.FIGHTER, "player2")

        system.place_unit_in_space(destroyer)
        system.place_unit_in_space(cruiser)
        system.place_unit_in_space(fighter1)
        system.place_unit_in_space(fighter2)

        with patch.object(
            resolver, "perform_anti_fighter_barrage_enhanced"
        ) as mock_afb:
            mock_afb.return_value = 1

            resolver.resolve_space_combat_with_afb(system, "player1", "player2")

            # AFB should only be called for destroyer, not cruiser
            assert mock_afb.call_count == 1
            mock_afb.assert_called_with(destroyer, [fighter1, fighter2])

    def test_afb_with_no_afb_capable_units(self) -> None:
        """Test space combat when no units have AFB capability."""
        resolver = CombatResolver()
        system = System("test_system")

        # No AFB capable units
        cruiser1 = Unit(UnitType.CRUISER, "player1")
        cruiser2 = Unit(UnitType.CRUISER, "player2")

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        with patch.object(
            resolver, "perform_anti_fighter_barrage_enhanced"
        ) as mock_afb:
            result = resolver.resolve_space_combat_with_afb(
                system, "player1", "player2"
            )

            # AFB should not be called when no units have the ability
            mock_afb.assert_not_called()
            assert result.afb_hits_attacker == 0
            assert result.afb_hits_defender == 0

    def test_afb_integration_preserves_existing_combat_mechanics(self) -> None:
        """Test that AFB integration doesn't break existing combat mechanics."""
        resolver = CombatResolver()
        system = System("test_system")

        # Standard combat scenario
        cruiser1 = Unit(UnitType.CRUISER, "player1")
        cruiser2 = Unit(UnitType.CRUISER, "player2")

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        # Mock regular combat methods to ensure they still work
        with patch.object(
            resolver, "roll_dice_for_unit", return_value=1
        ) as mock_combat:
            result = resolver.resolve_space_combat_with_afb(
                system, "player1", "player2"
            )

            # Regular combat should still be called
            mock_combat.assert_called()
            assert result.regular_combat_completed is True

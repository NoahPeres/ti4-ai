"""Tests for Rule 31: DESTROYED - Unit destruction mechanics.

This module tests the implementation of Rule 31: DESTROYED according to the TI4 LRR.
Tests cover unit destruction, reinforcement return, and destruction vs removal distinction.

LRR Reference: Rule 31: DESTROYED
- 31.1: Hit assignment and unit destruction
- 31.2: Distinction between destroyed and removed units
"""

from unittest.mock import Mock

import pytest

from src.ti4.core.combat import CombatResolver
from src.ti4.core.constants import UnitType
from src.ti4.core.destruction import UnitDestructionManager
from src.ti4.core.planet import Planet
from src.ti4.core.reinforcements import ReinforcementPool
from src.ti4.core.system import System
from src.ti4.core.unit import Unit


class TestRule31UnitDestruction:
    """Test Rule 31.1: Hit assignment and unit destruction."""

    def test_unit_destroyed_returns_to_reinforcements(self) -> None:
        """Test that destroyed units are returned to reinforcements.

        LRR 31: When a player's unit is destroyed, it is removed from the
        game board and returned to their reinforcements.
        """
        # Setup
        system = System(system_id="test_system")
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")

        system.place_unit_in_space(cruiser)
        system.place_unit_in_space(fighter)

        reinforcements = ReinforcementPool("player1")
        destruction_manager = UnitDestructionManager()

        # Initial state
        assert cruiser in system.space_units
        assert fighter in system.space_units
        assert reinforcements.get_unit_count(UnitType.CRUISER) == 0
        assert reinforcements.get_unit_count(UnitType.FIGHTER) == 0

        # Destroy units
        destroyed_units = [cruiser, fighter]
        destruction_manager.destroy_units(destroyed_units, system, reinforcements)

        # Verify units removed from board
        assert cruiser not in system.space_units
        assert fighter not in system.space_units

        # Verify units returned to reinforcements
        assert reinforcements.get_unit_count(UnitType.CRUISER) == 1
        assert reinforcements.get_unit_count(UnitType.FIGHTER) == 1

    def test_hit_assignment_destroys_chosen_units(self) -> None:
        """Test Rule 31.1: Player chooses which units are destroyed by hits.

        LRR 31.1: When a player assigns hits that were produced against their units,
        that player chooses a number of their units to be destroyed equal to the
        number of hits produced against those units.
        """
        # Setup
        resolver = CombatResolver()
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        fighter1 = Unit(unit_type=UnitType.FIGHTER, owner="player1")
        fighter2 = Unit(unit_type=UnitType.FIGHTER, owner="player1")

        units = [cruiser, fighter1, fighter2]

        # Player chooses to destroy both fighters (2 hits)
        hit_assignments = [fighter1.id, fighter2.id]
        destroyed_units = resolver.assign_hits_by_player_choice(units, hit_assignments)

        # Verify correct units destroyed
        assert len(destroyed_units) == 2
        assert fighter1 in destroyed_units
        assert fighter2 in destroyed_units
        assert cruiser not in destroyed_units

    def test_sustain_damage_prevents_destruction(self) -> None:
        """Test that sustain damage prevents unit destruction."""
        # Setup
        dreadnought = Unit(unit_type=UnitType.DREADNOUGHT, owner="player1")
        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")

        system = System(system_id="test_system")
        system.place_unit_in_space(dreadnought)
        system.place_unit_in_space(fighter)

        reinforcements = ReinforcementPool("player1")
        destruction_manager = UnitDestructionManager()

        # Dreadnought sustains damage instead of being destroyed
        dreadnought.sustain_damage()

        # Only fighter should be destroyed
        destroyed_units = [fighter]  # Dreadnought sustained, not destroyed
        destruction_manager.destroy_units(destroyed_units, system, reinforcements)

        # Verify dreadnought still on board but damaged
        assert dreadnought in system.space_units
        assert dreadnought.has_sustained_damage is True

        # Verify fighter destroyed and returned to reinforcements
        assert fighter not in system.space_units
        assert reinforcements.get_unit_count(UnitType.FIGHTER) == 1


class TestRule31DestructionVsRemoval:
    """Test Rule 31.2: Distinction between destroyed and removed units."""

    def test_destroyed_units_trigger_effects(self) -> None:
        """Test that destroyed units trigger destruction effects.

        LRR 31.2: If a player's unit is removed from the board by a game effect,
        it is not treated as being destroyed; effects that trigger when a unit
        is destroyed are not triggered.
        """
        # Setup
        system = System(system_id="test_system")
        planet = Planet("test_planet", resources=2, influence=1)
        system.add_planet(planet)
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        system.place_unit_on_planet(infantry, "test_planet")

        destruction_manager = UnitDestructionManager()
        effect_triggered = Mock()

        # Register destruction effect
        destruction_manager.register_destruction_effect(
            UnitType.INFANTRY, effect_triggered
        )

        # Destroy unit (should trigger effects)
        destruction_event = destruction_manager.destroy_unit(infantry, system)

        # Verify effect was triggered
        effect_triggered.assert_called_once()
        assert destruction_event.unit == infantry
        assert destruction_event.was_destroyed is True

    def test_removed_units_do_not_trigger_effects(self) -> None:
        """Test that removed (not destroyed) units do not trigger destruction effects."""
        # Setup
        system = System(system_id="test_system")
        planet = Planet("test_planet", resources=2, influence=1)
        system.add_planet(planet)
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        system.place_unit_on_planet(infantry, "test_planet")

        destruction_manager = UnitDestructionManager()
        effect_triggered = Mock()

        # Register destruction effect
        destruction_manager.register_destruction_effect(
            UnitType.INFANTRY, effect_triggered
        )

        # Remove unit (should NOT trigger effects)
        removal_event = destruction_manager.remove_unit(infantry, system)

        # Verify effect was NOT triggered
        effect_triggered.assert_not_called()
        assert removal_event.unit == infantry
        assert removal_event.was_destroyed is False

    def test_fleet_pool_removal_vs_combat_destruction(self) -> None:
        """Test distinction between fleet pool removal and combat destruction."""
        # Setup
        system = System(system_id="test_system")
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner="player1")

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        destruction_manager = UnitDestructionManager()
        reinforcements = ReinforcementPool("player1")

        # Combat destruction (triggers effects)
        combat_destruction = destruction_manager.destroy_unit_in_combat(
            cruiser1, system, reinforcements
        )
        assert combat_destruction.was_destroyed is True
        assert combat_destruction.trigger_effects is True

        # Fleet pool removal (does not trigger effects)
        fleet_pool_removal = destruction_manager.remove_unit_for_fleet_pool(
            cruiser2, system, reinforcements
        )
        assert fleet_pool_removal.was_destroyed is False
        assert fleet_pool_removal.trigger_effects is False


class TestRule31ReinforcementIntegration:
    """Test integration with reinforcement pool system."""

    def test_reinforcement_pool_tracking(self) -> None:
        """Test that reinforcement pools correctly track returned units."""
        reinforcements = ReinforcementPool("player1")

        # Initial state - full reinforcements
        initial_cruisers = 2
        initial_fighters = 8
        reinforcements.set_unit_count(UnitType.CRUISER, initial_cruisers)
        reinforcements.set_unit_count(UnitType.FIGHTER, initial_fighters)

        # Remove units for production
        reinforcements.remove_units(UnitType.CRUISER, 1)
        reinforcements.remove_units(UnitType.FIGHTER, 3)

        assert reinforcements.get_unit_count(UnitType.CRUISER) == 1
        assert reinforcements.get_unit_count(UnitType.FIGHTER) == 5

        # Return destroyed units
        reinforcements.return_destroyed_unit(UnitType.CRUISER)
        reinforcements.return_destroyed_unit(UnitType.FIGHTER)

        assert reinforcements.get_unit_count(UnitType.CRUISER) == 2
        assert reinforcements.get_unit_count(UnitType.FIGHTER) == 6

    def test_multiple_units_destroyed_simultaneously(self) -> None:
        """Test handling multiple units destroyed in same combat round."""
        system = System(system_id="test_system")
        units = [
            Unit(unit_type=UnitType.FIGHTER, owner="player1"),
            Unit(unit_type=UnitType.FIGHTER, owner="player1"),
            Unit(unit_type=UnitType.CRUISER, owner="player1"),
        ]

        for unit in units:
            system.place_unit_in_space(unit)

        reinforcements = ReinforcementPool("player1")
        destruction_manager = UnitDestructionManager()

        # Destroy all units simultaneously
        destruction_events = destruction_manager.destroy_units(
            units, system, reinforcements
        )

        # Verify all units removed from board
        for unit in units:
            assert unit not in system.space_units

        # Verify all units returned to reinforcements
        assert reinforcements.get_unit_count(UnitType.FIGHTER) == 2
        assert reinforcements.get_unit_count(UnitType.CRUISER) == 1

        # Verify destruction events created
        assert len(destruction_events) == 3
        for event in destruction_events:
            assert event.was_destroyed is True


class TestRule31EdgeCases:
    """Test edge cases and error conditions for Rule 31."""

    def test_destroy_unit_not_on_board(self) -> None:
        """Test error handling when trying to destroy unit not on board."""
        system = System(system_id="test_system")
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")

        destruction_manager = UnitDestructionManager()

        # Unit is not on the board
        with pytest.raises(ValueError, match="Unit not found in system"):
            destruction_manager.destroy_unit(unit, system)

    def test_invalid_hit_assignment_duplicate_units(self) -> None:
        """Test validation of hit assignments with duplicate unit assignments."""
        resolver = CombatResolver()
        units = [Unit(unit_type=UnitType.FIGHTER, owner="player1")]

        # Try to assign 2 hits to 1 unit (should be invalid)
        hit_assignments = [units[0].id, units[0].id]

        # This should be invalid according to validation logic
        is_valid = resolver.validate_hit_assignment_choices(units, hit_assignments, 2)
        assert is_valid is False  # Should fail validation

    def test_invalid_hit_assignment_nonexistent_unit(self) -> None:
        """Test validation of hit assignments with invalid unit IDs."""
        resolver = CombatResolver()
        units = [Unit(unit_type=UnitType.FIGHTER, owner="player1")]

        # Try to assign hit to non-existent unit
        hit_assignments = ["invalid_unit_id"]

        # This should be invalid according to validation logic
        is_valid = resolver.validate_hit_assignment_choices(units, hit_assignments, 1)
        assert is_valid is False  # Should fail validation

    def test_reinforcement_pool_capacity_limits(self) -> None:
        """Test that reinforcement pools respect capacity limits."""
        reinforcements = ReinforcementPool("player1")

        # Set maximum capacity
        max_fighters = 8
        reinforcements.set_max_capacity(UnitType.FIGHTER, max_fighters)
        reinforcements.set_unit_count(UnitType.FIGHTER, max_fighters)

        # Try to return more units than capacity
        with pytest.raises(ValueError, match="Reinforcement pool at capacity"):
            reinforcements.return_destroyed_unit(UnitType.FIGHTER)


class TestRule31CombatIntegration:
    """Test integration with existing combat systems."""

    def test_combat_resolution_with_destruction(self) -> None:
        """Test full combat resolution including unit destruction."""
        system = System(system_id="test_system")

        # Player 1 units
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        fighter1 = Unit(unit_type=UnitType.FIGHTER, owner="player1")

        # Player 2 units
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner="player2")
        fighter2 = Unit(unit_type=UnitType.FIGHTER, owner="player2")

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(fighter1)
        system.place_unit_in_space(cruiser2)
        system.place_unit_in_space(fighter2)

        resolver = CombatResolver()
        reinforcements1 = ReinforcementPool("player1")
        reinforcements2 = ReinforcementPool("player2")

        # Simulate combat round with 1 hit each
        # Player 1 chooses to lose fighter
        destroyed_p1 = resolver.assign_hits_by_player_choice(
            [cruiser1, fighter1], [fighter1.id]
        )

        # Player 2 chooses to lose fighter
        destroyed_p2 = resolver.assign_hits_by_player_choice(
            [cruiser2, fighter2], [fighter2.id]
        )

        # Process destruction
        destruction_manager = UnitDestructionManager()
        destruction_manager.destroy_units(destroyed_p1, system, reinforcements1)
        destruction_manager.destroy_units(destroyed_p2, system, reinforcements2)

        # Verify final state
        assert cruiser1 in system.space_units
        assert cruiser2 in system.space_units
        assert fighter1 not in system.space_units
        assert fighter2 not in system.space_units

        assert reinforcements1.get_unit_count(UnitType.FIGHTER) == 1
        assert reinforcements2.get_unit_count(UnitType.FIGHTER) == 1

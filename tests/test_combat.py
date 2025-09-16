"""Tests for combat system."""

from src.ti4.core.combat import CombatDetector, CombatInitiator, CombatResolver
from src.ti4.core.fleet import Fleet
from src.ti4.core.system import System
from src.ti4.core.unit import Unit


class TestCombatDetector:
    def test_combat_detector_creation(self):
        """Test that CombatDetector can be created."""
        detector = CombatDetector()
        assert detector is not None

    def test_detect_combat_opposing_fleets(self):
        """Test that combat is detected when opposing fleets are in same system."""
        detector = CombatDetector()
        system = System(system_id="test_system")

        # Create opposing fleets
        fleet1 = Fleet(owner="player1", system_id="test_system")
        fleet2 = Fleet(owner="player2", system_id="test_system")

        # Add units to fleets
        cruiser1 = Unit(unit_type="cruiser", owner="player1")
        cruiser2 = Unit(unit_type="cruiser", owner="player2")

        fleet1.add_unit(cruiser1)
        fleet2.add_unit(cruiser2)

        # Place units in system
        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        # Should detect combat
        assert detector.should_initiate_combat(system) is True

    def test_no_combat_same_owner(self):
        """Test that no combat occurs when all units have same owner."""
        detector = CombatDetector()
        system = System(system_id="test_system")

        # Create fleets with same owner
        fleet1 = Fleet(owner="player1", system_id="test_system")
        fleet2 = Fleet(owner="player1", system_id="test_system")

        # Add units to fleets
        cruiser1 = Unit(unit_type="cruiser", owner="player1")
        cruiser2 = Unit(unit_type="cruiser", owner="player1")

        fleet1.add_unit(cruiser1)
        fleet2.add_unit(cruiser2)

        # Place units in system
        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        # Should not detect combat
        assert detector.should_initiate_combat(system) is False


class TestCombatInitiator:
    def test_combat_initiator_creation(self):
        """Test that CombatInitiator can be created."""
        initiator = CombatInitiator()
        assert initiator is not None

    def test_get_combat_participants(self):
        """Test getting combat participants from a system."""
        initiator = CombatInitiator()
        system = System(system_id="test_system")

        # Create units from different players
        cruiser1 = Unit(unit_type="cruiser", owner="player1")
        cruiser2 = Unit(unit_type="cruiser", owner="player2")
        fighter1 = Unit(unit_type="fighter", owner="player1")

        # Place units in system
        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)
        system.place_unit_in_space(fighter1)

        # Get participants
        participants = initiator.get_combat_participants(system)

        # Should return units grouped by owner
        assert len(participants) == 2  # Two players
        assert "player1" in participants
        assert "player2" in participants
        assert len(participants["player1"]) == 2  # cruiser + fighter
        assert len(participants["player2"]) == 1  # cruiser

    def test_no_participants_empty_system(self):
        """Test that empty system has no combat participants."""
        initiator = CombatInitiator()
        system = System(system_id="test_system")

        participants = initiator.get_combat_participants(system)

        assert len(participants) == 0


class TestCombatResolver:
    def test_combat_resolver_creation(self):
        """Test that CombatResolver can be created."""
        resolver = CombatResolver()
        assert resolver is not None

    def test_roll_dice_for_unit(self):
        """Test rolling dice for a single unit."""
        resolver = CombatResolver()
        unit = Unit(unit_type="cruiser", owner="player1")

        # Roll dice for unit using its natural dice count (cruiser rolls 1 die)
        hits = resolver.roll_dice_for_unit(unit)

        # Should return number of hits (0 or 1 for cruiser)
        assert isinstance(hits, int)
        assert 0 <= hits <= 1

    def test_roll_dice_for_multi_dice_unit(self):
        """Test rolling dice for a unit that rolls multiple dice."""
        resolver = CombatResolver()
        unit = Unit(unit_type="war_sun", owner="player1")

        # War sun rolls 3 dice with combat value 3 (should hit on 3+)
        hits = resolver.roll_dice_for_unit(unit)

        # Should return number of hits (0 to 3 for war sun)
        assert isinstance(hits, int)
        assert 0 <= hits <= 3

    def test_roll_dice_with_override(self):
        """Test rolling dice with dice count override."""
        resolver = CombatResolver()
        unit = Unit(unit_type="cruiser", owner="player1")

        # Override dice count to 2 (instead of cruiser's natural 1)
        hits = resolver.roll_dice_for_unit(unit, dice_count=2)

        # Should return number of hits (0 to 2)
        assert isinstance(hits, int)
        assert 0 <= hits <= 2

    def test_unit_combat_dice_values(self):
        """Test that units have correct combat dice values."""
        # Test various unit types have correct dice counts
        cruiser = Unit(unit_type="cruiser", owner="player1")
        assert cruiser.get_combat_dice() == 1

        dreadnought = Unit(unit_type="dreadnought", owner="player1")
        assert dreadnought.get_combat_dice() == 1

        war_sun = Unit(unit_type="war_sun", owner="player1")
        assert war_sun.get_combat_dice() == 3

        fighter = Unit(unit_type="fighter", owner="player1")
        assert fighter.get_combat_dice() == 1

        space_dock = Unit(unit_type="space_dock", owner="player1")
        assert space_dock.get_combat_dice() == 0  # Non-combat unit

    def test_calculate_hits_multiple_dice(self):
        """Test calculating hits from multiple dice rolls."""
        resolver = CombatResolver()

        # Test with known dice results
        dice_results = [6, 7, 8, 9, 10]  # 7+ should hit (4 hits)
        combat_value = 7

        hits = resolver.calculate_hits(dice_results, combat_value)
        assert hits == 4

    def test_calculate_hits_no_hits(self):
        """Test calculating hits when no dice meet combat value."""
        resolver = CombatResolver()

        # Test with dice that don't hit
        dice_results = [1, 2, 3, 4, 5, 6]  # None hit with combat value 7
        combat_value = 7

        hits = resolver.calculate_hits(dice_results, combat_value)
        assert hits == 0

    def test_resolve_sustain_damage_abilities(self):
        """Test resolving sustain damage abilities before hit assignment."""
        resolver = CombatResolver()

        # Create units with sustain damage
        dreadnought = Unit(unit_type="dreadnought", owner="player1")
        fighter = Unit(unit_type="fighter", owner="player1")

        units = [dreadnought, fighter]
        hits = 2

        # Player chooses to use sustain damage on dreadnought
        sustain_choices = {dreadnought.id: True}  # Player chooses to sustain

        # Resolve sustain damage abilities (cancels 1 hit)
        remaining_hits = resolver.resolve_sustain_damage_abilities(
            units, hits, sustain_choices
        )

        # Should have 1 hit remaining after sustaining 1
        assert remaining_hits == 1
        assert dreadnought.has_sustained_damage

    def test_assign_hits_with_player_choice(self):
        """Test hit assignment with player choice."""
        resolver = CombatResolver()

        # Create units to take hits
        cruiser = Unit(unit_type="cruiser", owner="player1")
        fighter = Unit(unit_type="fighter", owner="player1")

        units = [cruiser, fighter]

        # Player chooses to assign hit to fighter
        hit_assignments = [fighter.id]  # Player's choice

        # Assign hits based on player choice
        destroyed_units = resolver.assign_hits_by_player_choice(units, hit_assignments)

        # Fighter should be destroyed based on player choice
        assert len(destroyed_units) == 1
        assert fighter in destroyed_units
        assert cruiser not in destroyed_units

    def test_validate_hit_assignment_choices(self):
        """Test validation of player hit assignment choices."""
        resolver = CombatResolver()

        # Create units
        cruiser = Unit(unit_type="cruiser", owner="player1")
        fighter = Unit(unit_type="fighter", owner="player1")

        units = [cruiser, fighter]

        # Valid assignment (1 hit to 1 unit)
        valid_assignments = [fighter.id]
        assert (
            resolver.validate_hit_assignment_choices(units, valid_assignments, 1)
            is True
        )

        # Invalid assignment (too many hits assigned)
        invalid_assignments = [fighter.id, cruiser.id]
        assert (
            resolver.validate_hit_assignment_choices(units, invalid_assignments, 1)
            is False
        )

    def test_apply_combat_modifiers(self):
        """Test applying combat modifiers to dice rolls."""
        resolver = CombatResolver()

        # Test with +1 modifier
        dice_results = [
            6,
            7,
            8,
        ]  # Base combat value 7, with +1 modifier should hit on 6+
        combat_value = 7
        modifier = 1  # +1 to hit

        hits = resolver.calculate_hits_with_modifiers(
            dice_results, combat_value, modifier
        )
        assert hits == 3  # All dice should hit with +1 modifier

    def test_calculate_hits_with_negative_modifiers(self):
        """Test calculating hits with negative modifiers."""
        resolver = CombatResolver()

        # Test with -1 modifier
        dice_results = [
            7,
            8,
            9,
        ]  # Base combat value 7, with -1 modifier should hit on 8+
        combat_value = 7
        modifier = -1  # -1 to hit

        hits = resolver.calculate_hits_with_modifiers(
            dice_results, combat_value, modifier
        )
        assert hits == 2  # Only 8 and 9 should hit with -1 modifier

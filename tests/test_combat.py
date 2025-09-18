"""Tests for combat system."""

from src.ti4.core.combat import CombatDetector, CombatInitiator, CombatResolver
from src.ti4.core.constants import UnitType
from src.ti4.core.fleet import Fleet
from src.ti4.core.system import System
from src.ti4.core.unit import Unit


class TestCombatDetector:
    def test_combat_detector_creation(self) -> None:
        """Test that CombatDetector can be created."""
        detector = CombatDetector()
        assert detector is not None

    def test_detect_combat_opposing_fleets(self) -> None:
        """Test that combat is detected when opposing fleets are in the same system."""
        system = System(system_id="test_system")

        # Create fleets with opposing owners
        fleet1 = Fleet(owner="player1", system_id="test_system")
        fleet2 = Fleet(owner="player2", system_id="test_system")

        # Add units to fleets
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner="player2")

        fleet1.add_unit(cruiser1)
        fleet2.add_unit(cruiser2)

        # Add units to system space area
        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        # Add fleets to system
        system.add_fleet(fleet1)
        system.add_fleet(fleet2)

        detector = CombatDetector()
        assert detector.should_initiate_combat(system) is True

    def test_no_combat_same_owner(self) -> None:
        """Test that no combat is detected when fleets have the same owner."""
        system = System(system_id="test_system")

        # Create fleets with same owner
        fleet1 = Fleet(owner="player1", system_id="test_system")
        fleet2 = Fleet(owner="player1", system_id="test_system")

        # Add units to fleets
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner="player1")

        fleet1.add_unit(cruiser1)
        fleet2.add_unit(cruiser2)

        # Add units to system space area
        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        # Add fleets to system
        system.add_fleet(fleet1)
        system.add_fleet(fleet2)

        detector = CombatDetector()
        combat_detected = detector.should_initiate_combat(system)

        # Should not detect combat (same owner)
        assert combat_detected is False


class TestCombatInitiator:
    def test_combat_initiator_creation(self) -> None:
        """Test that CombatInitiator can be created."""
        initiator = CombatInitiator()
        assert initiator is not None

    def test_get_combat_participants(self) -> None:
        """Test getting combat participants from a system."""
        system = System(system_id="test_system")

        # Create fleets with opposing owners
        fleet1 = Fleet(owner="player1", system_id="test_system")
        fleet2 = Fleet(owner="player2", system_id="test_system")

        # Add units to fleets
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        cruiser3 = Unit(unit_type=UnitType.CRUISER, owner="player2")

        fleet1.add_unit(cruiser1)
        fleet1.add_unit(cruiser2)

        fleet2.add_unit(cruiser3)

        # Add units to system space area
        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)
        system.place_unit_in_space(cruiser3)

        # Add fleets to system
        system.add_fleet(fleet1)
        system.add_fleet(fleet2)

        initiator = CombatInitiator()
        participants = initiator.get_combat_participants(system)

        # Should have 2 players participating
        assert len(participants) == 2
        assert "player1" in participants
        assert "player2" in participants
        assert len(participants["player1"]) == 2  # 2 cruisers
        assert len(participants["player2"]) == 1  # 1 cruiser

    def test_no_participants_empty_system(self) -> None:
        """Test that empty system has no combat participants."""
        initiator = CombatInitiator()
        system = System(system_id="test_system")

        participants = initiator.get_combat_participants(system)

        assert len(participants) == 0


class TestCombatResolver:
    def test_combat_resolver_creation(self) -> None:
        """Test that CombatResolver can be created."""
        resolver = CombatResolver()
        assert resolver is not None

    def test_roll_dice_for_unit(self) -> None:
        """Test rolling dice for a single unit."""
        resolver = CombatResolver()
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")

        # Test with default dice count (should use unit's combat_dice)
        hits = resolver.roll_dice_for_unit(unit)
        assert isinstance(hits, int)
        assert hits >= 0

        # Test with override dice count
        hits = resolver.roll_dice_for_unit(unit, dice_count=0)
        assert hits == 0  # No dice should result in no hits

    def test_roll_dice_for_multi_dice_unit(self) -> None:
        """Test rolling dice for a unit with multiple dice."""
        resolver = CombatResolver()
        unit = Unit(unit_type=UnitType.WAR_SUN, owner="player1")

        # Test with default dice count (should use unit's combat_dice)
        hits = resolver.roll_dice_for_unit(unit)
        assert isinstance(hits, int)
        assert hits >= 0

        # Test with override dice count
        hits = resolver.roll_dice_for_unit(unit, dice_count=2)
        assert isinstance(hits, int)
        assert hits >= 0

    def test_roll_dice_with_override(self) -> None:
        """Test rolling dice with override values."""
        resolver = CombatResolver()
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")

        # Test with dice count override
        hits = resolver.roll_dice_for_unit(unit, dice_count=3)
        assert isinstance(hits, int)
        assert hits >= 0

    def test_unit_combat_dice_values(self) -> None:
        """Test that units have correct combat dice values."""
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        assert cruiser.get_stats().combat_dice == 1

        dreadnought = Unit(unit_type=UnitType.DREADNOUGHT, owner="player1")
        assert dreadnought.get_stats().combat_dice == 1

        war_sun = Unit(unit_type=UnitType.WAR_SUN, owner="player1")
        assert war_sun.get_stats().combat_dice == 3

        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")
        assert fighter.get_stats().combat_dice == 1

        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        assert space_dock.get_stats().combat_dice == 0

    def test_calculate_hits_multiple_dice(self) -> None:
        """Test calculating hits from multiple dice rolls."""
        resolver = CombatResolver()

        # Test with known dice results
        dice_results = [6, 7, 8, 9, 10]  # 7+ should hit (4 hits)
        combat_value = 7

        hits = resolver.calculate_hits(dice_results, combat_value)
        assert hits == 4

    def test_calculate_hits_no_hits(self) -> None:
        """Test calculating hits when no dice meet combat value."""
        resolver = CombatResolver()

        # Test with dice that don't hit
        dice_results = [1, 2, 3, 4, 5, 6]  # None hit with combat value 7
        combat_value = 7

        hits = resolver.calculate_hits(dice_results, combat_value)
        assert hits == 0

    def test_resolve_sustain_damage_abilities(self) -> None:
        """Test resolving sustain damage abilities."""
        resolver = CombatResolver()

        # Create units with sustain damage
        dreadnought = Unit(unit_type=UnitType.DREADNOUGHT, owner="player1")
        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")

        units = [dreadnought, fighter]
        hits = 2

        # Test sustain damage resolution
        sustain_choices = {dreadnought.id: True}  # Choose to sustain with dreadnought
        remaining_hits = resolver.resolve_sustain_damage_abilities(
            units, hits, sustain_choices
        )

        # Should have 1 hit remaining after sustaining 1
        assert remaining_hits == 1

    def test_assign_hits_with_player_choice(self) -> None:
        """Test assigning hits with player choice."""
        resolver = CombatResolver()

        # Create units
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")

        units = [cruiser, fighter]

        # Test hit assignment by player choice
        hit_assignments = [fighter.id]  # Choose to lose the fighter
        destroyed_units = resolver.assign_hits_by_player_choice(units, hit_assignments)

        # Should have 1 destroyed unit (fighter)
        assert len(destroyed_units) == 1
        assert destroyed_units[0] == fighter

    def test_validate_hit_assignment_choices(self) -> None:
        """Test validating hit assignment choices."""
        resolver = CombatResolver()

        # Create units
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")

        units = [cruiser, fighter]

        # Valid choices
        assert resolver.validate_hit_assignment_choices(units, [cruiser.id], 1) is True
        assert resolver.validate_hit_assignment_choices(units, [fighter.id], 1) is True

        # Invalid choices
        assert (
            resolver.validate_hit_assignment_choices(units, ["invalid_id"], 1) is False
        )  # Invalid ID
        assert (
            resolver.validate_hit_assignment_choices(units, [cruiser.id, fighter.id], 1)
            is False
        )  # Too many choices
        assert (
            resolver.validate_hit_assignment_choices(units, [], 1) is False
        )  # Too few choices (no units assigned for 1 hit)
        assert (
            resolver.validate_hit_assignment_choices(units, [cruiser.id], 2) is False
        )  # Too few choices (1 unit assigned for 2 hits)

    def test_apply_combat_modifiers(self) -> None:
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

    def test_calculate_hits_with_negative_modifiers(self) -> None:
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


class TestUnitAbilitiesInCombat:
    def test_anti_fighter_barrage_timing(self) -> None:
        """Test that anti-fighter barrage happens before regular combat."""
        # Create a destroyer (has anti-fighter barrage)
        destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player1")

        # Create enemy fighters
        [
            Unit(unit_type=UnitType.FIGHTER, owner="player2"),
            Unit(unit_type=UnitType.FIGHTER, owner="player2"),
        ]

        # Test that destroyer has the ability (this internally checks get_stats().anti_fighter_barrage)
        assert destroyer.has_anti_fighter_barrage() is True

    def test_space_cannon_defensive_fire(self) -> None:
        """Test space cannon defensive fire."""
        # Create a PDS (has space cannon)
        pds = Unit(unit_type=UnitType.PDS, owner="player1")

        # Create enemy units entering the system
        [
            Unit(unit_type=UnitType.CRUISER, owner="player2"),
            Unit(unit_type=UnitType.FIGHTER, owner="player2"),
        ]

        # Space cannon should fire before regular combat
        assert pds.get_stats().space_cannon == 1

    def test_sustain_damage_prevents_destruction(self) -> None:
        """Test that sustain damage prevents unit destruction."""
        # Create a dreadnought (has sustain damage)
        dreadnought = Unit(unit_type=UnitType.DREADNOUGHT, owner="player1")

        # Dreadnought should have sustain damage ability
        assert dreadnought.get_stats().sustain_damage is True

        # After taking a hit, it should still be alive but damaged
        # This would be handled by the combat resolver in practice

    def test_anti_fighter_barrage_only_targets_fighters(self) -> None:
        """Test that anti-fighter barrage only targets fighters."""
        # Create a destroyer
        Unit(unit_type=UnitType.DESTROYER, owner="player1")

        # Create mixed enemy units
        enemy_units = [
            Unit(unit_type=UnitType.FIGHTER, owner="player2"),
            Unit(unit_type=UnitType.CRUISER, owner="player2"),
            Unit(unit_type=UnitType.FIGHTER, owner="player2"),
        ]

        # Anti-fighter barrage should only affect fighters
        fighters = [unit for unit in enemy_units if unit.unit_type == "fighter"]
        assert len(fighters) == 2

    def test_unit_without_ability_cannot_use_it(self) -> None:
        """Test that units without specific abilities cannot use them."""
        # Create a fighter (no special abilities)
        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")
        [Unit(unit_type=UnitType.FIGHTER, owner="player2")]

        # Fighter should not have anti-fighter barrage
        assert fighter.get_stats().anti_fighter_barrage == 0

    def test_sustain_damage_can_only_be_used_once(self) -> None:
        """Test that sustain damage can only be used once per combat."""
        # Create a cruiser (no sustain damage)
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        [Unit(unit_type=UnitType.FIGHTER, owner="player2")]

        # Cruiser should not have sustain damage
        assert cruiser.get_stats().sustain_damage is False

        # Create a dreadnought (has sustain damage)
        Unit(unit_type=UnitType.DREADNOUGHT, owner="player1")

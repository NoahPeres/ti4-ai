"""Tests for Rule 15: BOMBARDMENT implementation.

This module tests the bombardment unit ability mechanics as defined in the LRR.
Bombardment allows ships to destroy ground forces on planets during invasion.

LRR Reference: Rule 15 - BOMBARDMENT (UNIT ABILITY)
"""


import pytest

from src.ti4.core.constants import UnitType
from src.ti4.core.planet import Planet
from src.ti4.core.system import System
from src.ti4.core.unit import Unit


class TestRule15BombardmentRolls:
    """Test Rule 15.1: Bombardment roll mechanics."""

    def test_bombardment_roll_basic_mechanics(self) -> None:
        """Test Rule 15.1: Basic bombardment roll with hit calculation.

        LRR: "The active player chooses which planet each of their units that has a
        'Bombardment' ability will bombard. Then, that player rolls dice for each
        of those units; this is called a bombardment roll."
        """
        # Create system with planet and ground forces
        system = System("test_system")
        planet = Planet("test_planet", resources=2, influence=1)
        system.add_planet(planet)

        # Add defending ground forces
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="defender")
        planet.place_unit(infantry)

        # Add attacking ship with bombardment
        dreadnought = Unit(unit_type=UnitType.DREADNOUGHT, owner="attacker")
        system.place_unit_in_space(dreadnought)

        # Execute bombardment
        from src.ti4.core.bombardment import BombardmentSystem
        bombardment = BombardmentSystem()
        result = bombardment.execute_bombardment(
            system=system,
            attacking_player="attacker",
            planet_targets={"test_planet": [dreadnought]}
        )

        # Verify bombardment was executed (result should be a dict with planet names)
        assert isinstance(result, dict)
        assert "test_planet" in result

    def test_bombardment_value_and_dice_count(self) -> None:
        """Test Rule 15.1b: Bombardment value format 'Bombardment X (xY)'.

        LRR: "The 'Bombardment' ability is displayed as 'Bombardment X (xY).'
        The X is the minimum value needed for a die to produce a hit, and Y is
        the number of dice rolled."
        """
        # Create units with different bombardment values
        dreadnought = Unit(unit_type=UnitType.DREADNOUGHT, owner="player1")
        war_sun = Unit(unit_type=UnitType.WAR_SUN, owner="player1")

        # Dreadnought should have Bombardment 5 (x1)
        assert dreadnought.get_bombardment_value() == 5
        assert dreadnought.get_bombardment_dice_count() == 1

        # War Sun should have Bombardment 3 (x3)
        assert war_sun.get_bombardment_value() == 3
        assert war_sun.get_bombardment_dice_count() == 3

    def test_bombardment_hit_calculation(self) -> None:
        """Test Rule 15.1: Hit calculation based on bombardment value.

        LRR: "A hit is produced for each die roll that is equal to or greater
        than the unit's 'Bombardment' value."
        """
        from src.ti4.core.bombardment import BombardmentRoll

        # Test with fixed dice rolls
        roll = BombardmentRoll(bombardment_value=5, dice_count=2)
        hits = roll.calculate_hits(dice_results=[4, 6])  # One hit (6 >= 5)
        assert hits == 1

        hits = roll.calculate_hits(dice_results=[5, 5])  # Two hits (both >= 5)
        assert hits == 2

    def test_combat_roll_separation(self) -> None:
        """Test Rule 15.1c: Bombardment rolls separate from combat rolls.

        LRR: "Game effects that reroll, modify, or otherwise affect combat rolls
        do not affect bombardment rolls."
        """
        # This should fail until bombardment roll system is implemented
        with pytest.raises(AttributeError):
            from src.ti4.core.bombardment import BombardmentRoll
            from src.ti4.core.combat import CombatModifier

            # Combat modifiers should not affect bombardment
            roll = BombardmentRoll(bombardment_value=5, dice_count=1)
            modifier = CombatModifier(reroll_misses=True)

            # Bombardment should ignore combat modifiers
            assert not roll.is_affected_by_combat_modifier(modifier)


class TestRule15PlanetTargeting:
    """Test Rule 15.1d: Multi-planet bombardment targeting."""

    def test_multi_planet_bombardment_targeting(self) -> None:
        """Test Rule 15.1d: Multiple planets can be bombarded with declaration.

        LRR: "Multiple planets in a system may be bombarded, but a player must
        declare which planet a unit is bombarding before making a bombardment roll."
        """
        # Create system with multiple planets
        system = System("multi_planet_system")
        planet1 = Planet("planet1", resources=2, influence=1)
        planet2 = Planet("planet2", resources=1, influence=2)
        system.add_planet(planet1)
        system.add_planet(planet2)

        # Add ground forces to both planets
        infantry1 = Unit(unit_type=UnitType.INFANTRY, owner="defender")
        infantry2 = Unit(unit_type=UnitType.INFANTRY, owner="defender")
        planet1.place_unit(infantry1)
        planet2.place_unit(infantry2)

        # Add multiple bombardment ships
        dreadnought1 = Unit(unit_type=UnitType.DREADNOUGHT, owner="attacker")
        dreadnought2 = Unit(unit_type=UnitType.DREADNOUGHT, owner="attacker")
        system.place_unit_in_space(dreadnought1)
        system.place_unit_in_space(dreadnought2)

        # This should fail until planet targeting is implemented
        with pytest.raises(AttributeError):
            from src.ti4.core.bombardment import BombardmentTargeting

            targeting = BombardmentTargeting()
            targets = targeting.assign_bombardment_targets(
                bombardment_units=[dreadnought1, dreadnought2],
                available_planets=["planet1", "planet2"]
            )

            # Should allow targeting different planets
            assert "planet1" in targets
            assert "planet2" in targets

    def test_bombardment_target_validation(self) -> None:
        """Test that bombardment targets must be declared before rolling."""
        # This should fail until target validation is implemented
        with pytest.raises(AttributeError):
            from src.ti4.core.bombardment import BombardmentSystem

            bombardment = BombardmentSystem()

            # Should require target declaration
            with pytest.raises(ValueError, match="must declare targets"):
                bombardment.execute_bombardment_without_targets()


class TestRule15PlanetaryShieldPrevention:
    """Test Rule 15.1f: Planetary shield bombardment prevention."""

    def test_planetary_shield_prevents_bombardment(self) -> None:
        """Test Rule 15.1f: Planets with planetary shield cannot be bombarded.

        LRR: "Planets that contain a unit with the 'Planetary Shield' ability
        cannot be bombarded."
        """
        # Create planet with planetary shield unit
        planet = Planet("shielded_planet", resources=2, influence=1)
        pds = Unit(unit_type=UnitType.PDS, owner="defender")
        planet.place_unit(pds)

        from src.ti4.core.bombardment import BombardmentSystem

        bombardment = BombardmentSystem()
        can_bombard = bombardment.can_bombard_planet(planet)
        assert can_bombard is False

    def test_bombardment_allowed_without_planetary_shield(self) -> None:
        """Test that bombardment is allowed on planets without planetary shield."""
        # Create planet without planetary shield
        planet = Planet("unshielded_planet", resources=2, influence=1)
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="defender")
        planet.place_unit(infantry)

        from src.ti4.core.bombardment import BombardmentSystem

        bombardment = BombardmentSystem()
        can_bombard = bombardment.can_bombard_planet(planet)
        assert can_bombard is True


class TestRule15GroundForceDestruction:
    """Test Rule 15.2: Ground force destruction from bombardment hits."""

    def test_ground_force_destruction_basic(self) -> None:
        """Test Rule 15.2: Defending player destroys ground forces for hits.

        LRR: "The player who controls the planet that is being bombarded chooses
        and destroys one of their ground forces on that planet for each hit result
        the bombardment roll produced."
        """
        # Create planet with multiple ground forces
        planet = Planet("target_planet", resources=2, influence=1)
        infantry1 = Unit(unit_type=UnitType.INFANTRY, owner="defender")
        infantry2 = Unit(unit_type=UnitType.INFANTRY, owner="defender")
        mech = Unit(unit_type=UnitType.MECH, owner="defender")
        planet.place_unit(infantry1)
        planet.place_unit(infantry2)
        planet.place_unit(mech)

        from src.ti4.core.bombardment import BombardmentHitAssignment

        hit_assignment = BombardmentHitAssignment()
        destroyed_units = hit_assignment.assign_bombardment_hits(
            planet=planet,
            hits=2,
            defending_player="defender"
        )

        assert len(destroyed_units) == 2
        assert all(unit.owner == "defender" for unit in destroyed_units)

    def test_excess_hits_have_no_effect(self) -> None:
        """Test Rule 15.2a: Excess hits beyond ground forces have no effect.

        LRR: "If a player has to assign more hits than that player has ground forces,
        the excess hits have no effect."
        """
        # Create planet with only one ground force
        planet = Planet("target_planet", resources=2, influence=1)
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="defender")
        planet.place_unit(infantry)

        from src.ti4.core.bombardment import BombardmentHitAssignment

        hit_assignment = BombardmentHitAssignment()
        destroyed_units = hit_assignment.assign_bombardment_hits(
            planet=planet,
            hits=3,  # More hits than ground forces
            defending_player="defender"
        )

        # Should only destroy the one available unit
        assert len(destroyed_units) == 1
        assert destroyed_units[0] == infantry

    def test_player_choice_in_unit_destruction(self) -> None:
        """Test that defending player chooses which units to destroy."""
        # Create planet with different unit types
        planet = Planet("target_planet", resources=2, influence=1)
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="defender")
        mech = Unit(unit_type=UnitType.MECH, owner="defender")
        planet.place_unit(infantry)
        planet.place_unit(mech)

        from src.ti4.core.bombardment import BombardmentHitAssignment

        hit_assignment = BombardmentHitAssignment()

        # Player should be able to choose which unit to destroy
        destroyed_units = hit_assignment.assign_bombardment_hits(
            planet=planet,
            hits=1,
            defending_player="defender",
            player_choice=[mech]  # Player chooses to destroy mech
        )

        assert len(destroyed_units) == 1
        assert destroyed_units[0] == mech


class TestRule15FactionSpecificRules:
    """Test Rule 15.1e: Faction-specific bombardment rules."""

    def test_l1z1x_harrow_ability_exception(self) -> None:
        """Test Rule 15.1e: L1Z1X Harrow ability doesn't affect own ground forces.

        LRR: "The L1Z1X's 'Harrow' ability does not affect the L1Z1X player's
        own ground forces."
        """
        # This should fail until faction-specific rules are implemented
        with pytest.raises(AttributeError):
            from src.ti4.core.faction import Faction

            from src.ti4.core.bombardment import BombardmentSystem

            bombardment = BombardmentSystem()

            # L1Z1X should not be able to bombard their own ground forces
            can_bombard_own = bombardment.can_bombard_own_ground_forces(
                faction=Faction.L1Z1X,
                ability="harrow"
            )
            assert can_bombard_own is False


class TestRule15IntegrationWithInvasion:
    """Test bombardment integration with invasion mechanics."""

    def test_bombardment_timing_in_invasion(self) -> None:
        """Test that bombardment occurs at correct step in invasion sequence."""
        # This should fail until invasion integration is implemented
        with pytest.raises(AttributeError):
            from src.ti4.core.invasion import InvasionSequence

            invasion = InvasionSequence()
            steps = invasion.get_invasion_steps()

            # Bombardment should occur before ground combat
            bombardment_index = steps.index("bombardment")
            ground_combat_index = steps.index("ground_combat")
            assert bombardment_index < ground_combat_index

    def test_bombardment_affects_ground_combat(self) -> None:
        """Test that bombardment destruction affects subsequent ground combat."""
        # This should fail until integration is implemented
        with pytest.raises(AttributeError):

            # Bombardment should reduce defending ground forces
            # before ground combat begins
            pass


class TestRule15TechnologyIntegration:
    """Test bombardment interaction with technologies."""

    def test_plasma_scoring_technology_interaction(self) -> None:
        """Test Plasma Scoring technology adds dice to bombardment rolls.

        LRR FAQ: "Plasma Scoring only grants one additional die for each
        'Bombardment' or 'Space Cannon' roll."
        """
        # This should fail until technology integration is implemented
        with pytest.raises(AttributeError):
            from src.ti4.core.bombardment import BombardmentRoll
            from src.ti4.core.technology import Technology

            # With Plasma Scoring, bombardment should get +1 die
            roll = BombardmentRoll(
                bombardment_value=5,
                dice_count=1,
                technologies=[Technology.PLASMA_SCORING]
            )

            assert roll.get_total_dice_count() == 2  # Base 1 + Plasma Scoring 1

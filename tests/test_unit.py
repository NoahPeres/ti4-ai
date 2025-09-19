"""Tests for unit structure."""

import pytest

from src.ti4.core.constants import UnitType
from src.ti4.core.unit import Unit


class TestUnit:
    def test_unit_creation(self) -> None:
        """Test that a unit can be created with type and owner."""
        unit = Unit(unit_type=UnitType.FIGHTER, owner="player1")
        assert unit.unit_type == UnitType.FIGHTER
        assert unit.owner == "player1"


class TestUnitAbilities:
    def test_sustain_damage_ability_detection(self) -> None:
        """Test that units with sustain damage ability are correctly identified."""
        # Units with sustain damage
        dreadnought = Unit(unit_type=UnitType.DREADNOUGHT, owner="player1")
        assert dreadnought.has_sustain_damage() is True

        war_sun = Unit(unit_type=UnitType.WAR_SUN, owner="player1")
        assert war_sun.has_sustain_damage() is True

        mech = Unit(unit_type=UnitType.MECH, owner="player1")
        assert mech.has_sustain_damage() is True

        # Units without sustain damage
        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")
        assert fighter.has_sustain_damage() is False

        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        assert cruiser.has_sustain_damage() is False

    def test_sustain_damage_activation(self) -> None:
        """Test that sustain damage can be activated on units that have the ability."""
        dreadnought = Unit(unit_type=UnitType.DREADNOUGHT, owner="player1")

        # Initially, unit has not sustained damage
        assert dreadnought.has_sustained_damage is False

        # Activate sustain damage ability
        dreadnought.sustain_damage()

        # Unit should now have sustained damage
        assert dreadnought.has_sustained_damage is True

    def test_sustain_damage_invalid_unit(self) -> None:
        """Test that sustain damage cannot be activated on units without the ability."""
        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")

        # Fighter cannot sustain damage
        with pytest.raises(ValueError, match="Unit UnitType.FIGHTER cannot sustain damage"):
            fighter.sustain_damage()

    def test_sustain_damage_repair(self) -> None:
        """Test that sustained damage can be repaired."""
        dreadnought = Unit(unit_type=UnitType.DREADNOUGHT, owner="player1")

        # Sustain damage first
        dreadnought.sustain_damage()
        assert dreadnought.has_sustained_damage is True

        # Repair the damage
        dreadnought.repair_damage()
        assert dreadnought.has_sustained_damage is False

    def test_anti_fighter_barrage_ability(self) -> None:
        """Test that units with anti-fighter barrage ability are correctly identified."""
        # Units with anti-fighter barrage
        destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player1")
        assert destroyer.has_anti_fighter_barrage() is True

        # Units without anti-fighter barrage
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        assert cruiser.has_anti_fighter_barrage() is False

    def test_space_cannon_ability(self) -> None:
        """Test that units with space cannon ability are correctly identified."""
        # Units with space cannon
        pds = Unit(unit_type=UnitType.PDS, owner="player1")
        assert pds.has_space_cannon() is True

        # Units without space cannon
        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")
        assert fighter.has_space_cannon() is False

    def test_bombardment_ability(self) -> None:
        """Test that units with bombardment ability are correctly identified."""
        # Units with bombardment
        dreadnought = Unit(unit_type=UnitType.DREADNOUGHT, owner="player1")
        assert dreadnought.has_bombardment() is True

        war_sun = Unit(unit_type=UnitType.WAR_SUN, owner="player1")
        assert war_sun.has_bombardment() is True

        # Units without bombardment
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        assert cruiser.has_bombardment() is False

        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")
        assert fighter.has_bombardment() is False

    def test_deploy_ability(self) -> None:
        """Test that units with deploy ability are correctly identified."""
        # Units with deploy
        mech = Unit(unit_type=UnitType.MECH, owner="player1")
        assert mech.has_deploy() is True

        # Units without deploy
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        assert infantry.has_deploy() is False

        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")
        assert fighter.has_deploy() is False

    def test_planetary_shield_ability(self) -> None:
        """Test that units with planetary shield ability are correctly identified."""
        # Units with planetary shield
        pds = Unit(unit_type=UnitType.PDS, owner="player1")
        assert pds.has_planetary_shield() is True

        # Units without planetary shield
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        assert infantry.has_planetary_shield() is False

        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        assert space_dock.has_planetary_shield() is False

    def test_production_ability(self) -> None:
        """Test that units with production ability return correct values."""
        # Units with production
        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        assert space_dock.get_production() == 2

        # Units without production
        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")
        assert fighter.get_production() == 0

        pds = Unit(unit_type=UnitType.PDS, owner="player1")
        assert pds.get_production() == 0

    def test_multiple_abilities_on_same_unit(self) -> None:
        """Test that units can have multiple abilities simultaneously."""
        # War sun has sustain damage and bombardment but not anti-fighter barrage
        war_sun = Unit(unit_type=UnitType.WAR_SUN, owner="player1")
        assert war_sun.has_sustain_damage() is True
        assert war_sun.has_bombardment() is True
        assert war_sun.has_anti_fighter_barrage() is False
        assert war_sun.has_space_cannon() is False
        assert war_sun.has_deploy() is False
        assert war_sun.has_planetary_shield() is False

        # Destroyer has anti-fighter barrage but not other abilities
        destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player1")
        assert destroyer.has_anti_fighter_barrage() is True
        assert destroyer.has_sustain_damage() is False
        assert destroyer.has_space_cannon() is False
        assert destroyer.has_bombardment() is False
        assert destroyer.has_deploy() is False
        assert destroyer.has_planetary_shield() is False

        # PDS has space cannon and planetary shield
        pds = Unit(unit_type=UnitType.PDS, owner="player1")
        assert pds.has_space_cannon() is True
        assert pds.has_planetary_shield() is True
        assert pds.has_sustain_damage() is False
        assert pds.has_bombardment() is False
        assert pds.has_deploy() is False

        # Mech has sustain damage and deploy
        mech = Unit(unit_type=UnitType.MECH, owner="player1")
        assert mech.has_sustain_damage() is True
        assert mech.has_deploy() is True
        assert mech.has_bombardment() is False
        assert mech.has_space_cannon() is False
        assert mech.has_planetary_shield() is False

        # Dreadnought has sustain damage and bombardment
        dreadnought = Unit(unit_type=UnitType.DREADNOUGHT, owner="player1")
        assert dreadnought.has_sustain_damage() is True
        assert dreadnought.has_bombardment() is True
        assert dreadnought.has_deploy() is False
        assert dreadnought.has_space_cannon() is False
        assert dreadnought.has_planetary_shield() is False


class TestUnitAbilitiesIntegration:
    """Test integration of unit abilities with other systems."""

    def test_all_unit_abilities_coverage(self) -> None:
        """Test that all TI4 unit abilities are implemented and accessible."""
        # Create units and verify all abilities are accessible
        units_and_abilities = [
            (UnitType.CARRIER, ["capacity"]),
            (UnitType.CRUISER, []),
            (UnitType.CRUISER_II, ["capacity"]),
            (UnitType.DREADNOUGHT, ["sustain_damage", "bombardment", "capacity"]),
            (UnitType.DESTROYER, ["anti_fighter_barrage"]),
            (UnitType.FIGHTER, []),
            (UnitType.INFANTRY, []),
            (UnitType.MECH, ["sustain_damage", "deploy"]),
            (UnitType.PDS, ["space_cannon", "planetary_shield"]),
            (UnitType.SPACE_DOCK, ["production"]),
            (UnitType.WAR_SUN, ["sustain_damage", "bombardment", "capacity"]),
        ]

        for unit_type, expected_abilities in units_and_abilities:
            unit = Unit(unit_type=unit_type, owner="player1")

            # Test that all ability methods exist and return boolean/int values
            assert isinstance(unit.has_sustain_damage(), bool)
            assert isinstance(unit.has_anti_fighter_barrage(), bool)
            assert isinstance(unit.has_space_cannon(), bool)
            assert isinstance(unit.has_bombardment(), bool)
            assert isinstance(unit.has_deploy(), bool)
            assert isinstance(unit.has_planetary_shield(), bool)
            assert isinstance(unit.get_production(), int)
            assert isinstance(unit.get_capacity(), int)

            # Verify specific abilities for this unit type
            if "sustain_damage" in expected_abilities:
                assert unit.has_sustain_damage() is True
            if "anti_fighter_barrage" in expected_abilities:
                assert unit.has_anti_fighter_barrage() is True
            if "space_cannon" in expected_abilities:
                assert unit.has_space_cannon() is True
            if "bombardment" in expected_abilities:
                assert unit.has_bombardment() is True
            if "deploy" in expected_abilities:
                assert unit.has_deploy() is True
            if "planetary_shield" in expected_abilities:
                assert unit.has_planetary_shield() is True
            if "production" in expected_abilities:
                assert unit.get_production() > 0
            if "capacity" in expected_abilities:
                assert unit.get_capacity() > 0

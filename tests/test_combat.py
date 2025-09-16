"""Tests for combat system."""

from src.ti4.core.combat import CombatDetector, CombatInitiator
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

"""Tests for Rule 29: DEFENDER - Non-active player is the defender in combat."""

from unittest.mock import Mock

import pytest

from ti4.core.combat import CombatRoleManager, RetreatManager
from ti4.core.constants import Faction, UnitType
from ti4.core.game_controller import GameController
from ti4.core.planet import Planet
from ti4.core.player import Player
from ti4.core.system import System
from ti4.core.unit import Unit


class TestRule29Defender:
    """Test suite for Rule 29: DEFENDER implementation."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        # Create mock game controller
        self.game_controller = Mock(spec=GameController)

        # Create test players
        self.player1 = Player(id="player1", faction=Faction.SOL)
        self.player2 = Player(id="player2", faction=Faction.XXCHA)
        self.player3 = Player(id="player3", faction=Faction.HACAN)

        # Set player1 as active player by default
        self.game_controller.get_current_player.return_value = self.player1

    def test_defender_is_non_active_player_space_combat(self) -> None:
        """Test Rule 29: Non-active player is defender in space combat."""
        # Setup space combat scenario
        system = System(system_id="test_system")

        # Add ships from both players
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player1")  # Active player
        cruiser2 = Unit(
            unit_type=UnitType.CRUISER, owner="player2"
        )  # Non-active player

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        role_manager = CombatRoleManager(self.game_controller)

        # Test defender identification
        defender_ids = role_manager.get_defender_ids(system)

        assert len(defender_ids) == 1
        assert defender_ids[0] == "player2"  # Non-active player is defender
        assert "player1" not in defender_ids  # Active player is not defender

    def test_defender_is_non_active_player_ground_combat(self) -> None:
        """Test Rule 29: Non-active player is defender in ground combat."""
        # Setup ground combat scenario
        system = System(system_id="test_system")
        planet = Planet(name="test_planet", resources=2, influence=1)
        system.add_planet(planet)

        # Add ground forces from both players
        infantry1 = Unit(unit_type=UnitType.INFANTRY, owner="player1")  # Active player
        infantry2 = Unit(
            unit_type=UnitType.INFANTRY, owner="player2"
        )  # Non-active player

        planet.place_unit(infantry1)
        planet.place_unit(infantry2)

        role_manager = CombatRoleManager(self.game_controller)

        # Test ground combat defender identification
        defender_id = role_manager.get_ground_combat_defender_id(system, "test_planet")

        assert defender_id == "player2"  # Non-active player is defender

    def test_multiple_defenders_in_space_combat(self) -> None:
        """Test Rule 29: Multiple non-active players are all defenders."""
        # Setup three-player space combat
        system = System(system_id="test_system")

        # Add ships from all three players
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player1")  # Active player
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner="player2")  # Defender 1
        cruiser3 = Unit(unit_type=UnitType.CRUISER, owner="player3")  # Defender 2

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)
        system.place_unit_in_space(cruiser3)

        role_manager = CombatRoleManager(self.game_controller)

        # Test multiple defenders
        defender_ids = role_manager.get_defender_ids(system)

        assert len(defender_ids) == 2
        assert "player2" in defender_ids
        assert "player3" in defender_ids
        assert "player1" not in defender_ids  # Active player is attacker, not defender

    def test_defender_role_changes_with_active_player(self) -> None:
        """Test Rule 29: Defender role changes when active player changes."""
        # Setup combat scenario
        system = System(system_id="test_system")

        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner="player2")

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        role_manager = CombatRoleManager(self.game_controller)

        # Initially player1 is active, player2 is defender
        defender_ids = role_manager.get_defender_ids(system)
        assert defender_ids == ["player2"]

        # Change active player to player2
        self.game_controller.active_player_id = self.player2.id
        self.game_controller.get_current_player.return_value = self.player2

        # Now player1 should be defender
        defender_ids = role_manager.get_defender_ids(system)
        assert defender_ids == ["player1"]

    def test_defender_retreat_priority(self) -> None:
        """Test Rule 78.4: Defender announces retreats first."""
        retreat_manager = RetreatManager(attacker_id="player1", defender_id="player2")

        # Defender should be able to announce retreat first
        assert retreat_manager.can_announce_retreat("player2") is True

        # Attacker should also be able to announce retreat initially
        assert retreat_manager.can_announce_retreat("player1") is True

        # After defender announces retreat, attacker cannot retreat
        retreat_manager.announce_retreat("player2")
        assert retreat_manager.can_announce_retreat("player1") is False

    def test_attacker_cannot_retreat_after_defender_announces(self) -> None:
        """Test Rule 78.4b: If defender announces retreat, attacker cannot retreat."""
        retreat_manager = RetreatManager(attacker_id="player1", defender_id="player2")

        # Defender announces retreat
        retreat_manager.announce_retreat("player2")

        # Attacker should not be able to announce retreat
        assert retreat_manager.can_announce_retreat("player1") is False

        # Attempting to announce should raise error
        with pytest.raises(ValueError, match="cannot announce retreat"):
            retreat_manager.announce_retreat("player1")

    def test_attacker_can_retreat_if_defender_does_not(self) -> None:
        """Test that attacker can retreat if defender doesn't announce retreat."""
        retreat_manager = RetreatManager(attacker_id="player1", defender_id="player2")

        # Attacker announces retreat (defender hasn't)
        assert retreat_manager.can_announce_retreat("player1") is True
        retreat_manager.announce_retreat("player1")

        # Defender should still be able to announce retreat
        assert retreat_manager.can_announce_retreat("player2") is True

    def test_no_combat_raises_error_for_defender(self) -> None:
        """Test that defender identification raises error when no combat exists."""
        # Setup system with only one player's ships
        system = System(system_id="test_system")
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        system.place_unit_in_space(cruiser)

        role_manager = CombatRoleManager(self.game_controller)

        # Should raise error when trying to get defenders with no combat
        with pytest.raises(ValueError, match="No combat in system"):
            role_manager.get_defender_ids(system)

    def test_defender_role_consistency_across_combat_rounds(self) -> None:
        """Test that defender role remains consistent throughout combat."""
        # Setup combat scenario
        system = System(system_id="test_system")

        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player1")  # Active/Attacker
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner="player2")  # Defender

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        role_manager = CombatRoleManager(self.game_controller)

        # Check defender role multiple times (simulating multiple combat rounds)
        for _ in range(3):
            defender_ids = role_manager.get_defender_ids(system)
            assert defender_ids == ["player2"]

            attacker_id = role_manager.get_attacker_id(system)
            assert attacker_id == "player1"

    def test_defender_identification_with_mixed_unit_types(self) -> None:
        """Test defender identification works with various unit types in combat."""
        # Setup system with mixed unit types
        system = System(system_id="test_system")

        # Player1 (active) has destroyer and fighter
        destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player1")
        fighter1 = Unit(unit_type=UnitType.FIGHTER, owner="player1")

        # Player2 (defender) has cruiser and fighter
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player2")
        fighter2 = Unit(unit_type=UnitType.FIGHTER, owner="player2")

        system.place_unit_in_space(destroyer)
        system.place_unit_in_space(fighter1)
        system.place_unit_in_space(cruiser)
        system.place_unit_in_space(fighter2)

        role_manager = CombatRoleManager(self.game_controller)

        # Verify defender identification
        defender_ids = role_manager.get_defender_ids(system)
        assert len(defender_ids) == 1
        assert defender_ids[0] == "player2"

    def test_ground_combat_defender_with_multiple_planets(self) -> None:
        """Test ground combat defender identification on specific planets."""
        # Setup system with multiple planets
        system = System(system_id="test_system")

        planet1 = Planet(name="planet1", resources=2, influence=1)
        planet2 = Planet(name="planet2", resources=1, influence=2)
        system.add_planet(planet1)
        system.add_planet(planet2)

        # Combat on planet1: player1 vs player2
        infantry1_p1 = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        infantry2_p1 = Unit(unit_type=UnitType.INFANTRY, owner="player2")
        planet1.place_unit(infantry1_p1)
        planet1.place_unit(infantry2_p1)

        # Combat on planet2: player1 vs player3
        infantry1_p2 = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        infantry3_p2 = Unit(unit_type=UnitType.INFANTRY, owner="player3")
        planet2.place_unit(infantry1_p2)
        planet2.place_unit(infantry3_p2)

        role_manager = CombatRoleManager(self.game_controller)

        # Test defender identification per planet
        defender_p1 = role_manager.get_ground_combat_defender_id(system, "planet1")
        defender_p2 = role_manager.get_ground_combat_defender_id(system, "planet2")

        assert defender_p1 == "player2"
        assert defender_p2 == "player3"

    def test_get_defender_id_fails_with_multiple_defenders(self) -> None:
        """Test that get_defender_id() raises error when multiple defenders exist."""
        # Setup three-player space combat
        system = System(system_id="test_system")

        # Add ships from all three players
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player1")  # Active player
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner="player2")  # Defender 1
        cruiser3 = Unit(unit_type=UnitType.CRUISER, owner="player3")  # Defender 2

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)
        system.place_unit_in_space(cruiser3)

        role_manager = CombatRoleManager(self.game_controller)

        # Test that get_defender_id() fails with multiple defenders
        with pytest.raises(ValueError, match="Multiple defenders present"):
            role_manager.get_defender_id(system)

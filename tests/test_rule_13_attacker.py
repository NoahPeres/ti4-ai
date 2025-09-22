"""Tests for Rule 13: ATTACKER - Active player is always the attacker in combat."""

from unittest.mock import Mock

import pytest

from src.ti4.core.combat import CombatRoleManager
from src.ti4.core.constants import Faction
from src.ti4.core.game_controller import GameController
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.system import System
from src.ti4.core.unit import Unit, UnitType


class TestRule13Attacker:
    """Test suite for Rule 13: ATTACKER implementation."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        # Create mock game controller
        self.game_controller = Mock(spec=GameController)

        # Create test players
        self.player1 = Player(id="player1", faction=Faction.SOL)
        self.player2 = Player(id="player2", faction=Faction.XXCHA)
        self.player3 = Player(id="player3", faction=Faction.HACAN)

        # Set player1 as active player by default
        self.game_controller.active_player_id = self.player1.id
        self.game_controller.get_current_player.return_value = self.player1

        # Mock get_player method
        def mock_get_player(player_id: str) -> Player:
            if player_id == "player1":
                return self.player1
            elif player_id == "player2":
                return self.player2
            elif player_id == "player3":
                return self.player3
            else:
                raise ValueError(f"Unknown player: {player_id}")

        self.game_controller.get_player = mock_get_player

    def test_attacker_role_in_space_combat(self) -> None:
        """Test that active player is attacker in space combat."""
        # Setup space combat scenario
        system = System(system_id="test_system")

        # Add units from both players to create combat
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner=self.player1.id)
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner=self.player2.id)

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        # Create combat role manager
        role_manager = CombatRoleManager(self.game_controller)

        # Test that active player is attacker
        attacker_id = role_manager.get_attacker_id(system)
        assert attacker_id == self.player1.id

        # Test that non-active player is defender
        defender_id = role_manager.get_defender_id(system)
        assert defender_id == self.player2.id

    def test_attacker_role_in_ground_combat(self) -> None:
        """Test that active player is attacker in ground combat."""
        # Setup planet with ground units
        planet = Planet(name="test_planet", resources=2, influence=1)
        system = System(system_id="test_system")
        system.add_planet(planet)

        # Add ground units from both players
        infantry1 = Unit(unit_type=UnitType.INFANTRY, owner=self.player1.id)
        infantry2 = Unit(unit_type=UnitType.INFANTRY, owner=self.player2.id)

        planet.place_unit(infantry1)
        planet.place_unit(infantry2)

        # Create combat role manager
        role_manager = CombatRoleManager(self.game_controller)

        # Test that active player is attacker in ground combat
        attacker_id = role_manager.get_ground_combat_attacker_id(system, "test_planet")
        assert attacker_id == self.player1.id

        # Test that non-active player is defender in ground combat
        defender_id = role_manager.get_ground_combat_defender_id(system, "test_planet")
        assert defender_id == self.player2.id

    def test_active_player_changes_attacker_role(self) -> None:
        """Test that attacker role changes when active player changes."""
        # Setup combat scenario
        system = System(system_id="test_system")

        # Add units from both players
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner=self.player1.id)
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner=self.player2.id)

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        # Create combat role manager
        role_manager = CombatRoleManager(self.game_controller)

        # Initially player1 is active (attacker)
        attacker_id = role_manager.get_attacker_id(system)
        assert attacker_id == self.player1.id

        # Change active player to player2
        self.game_controller.active_player_id = self.player2.id
        self.game_controller.get_current_player.return_value = self.player2

        # Now player2 should be attacker
        attacker_id = role_manager.get_attacker_id(system)
        assert attacker_id == self.player2.id

        # And player1 should be defender
        defender_id = role_manager.get_defender_id(system)
        assert defender_id == self.player1.id

    def test_attacker_role_with_tactical_action(self) -> None:
        """Test attacker role during tactical action execution."""
        # Setup system for tactical action
        system = System(system_id="test_system")

        # Add units that would create combat
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner=self.player1.id)
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner=self.player2.id)

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        # Create combat role manager
        role_manager = CombatRoleManager(self.game_controller)

        # During tactical action, active player should be attacker
        attacker_id = role_manager.get_attacker_id(system)
        assert attacker_id == self.player1.id

        # Verify combat is detected
        assert role_manager.has_combat(system)

    def test_attacker_role_persists_during_combat_rounds(self) -> None:
        """Test that attacker role persists throughout combat rounds."""
        # Setup combat scenario
        system = System(system_id="test_system")

        # Add multiple units for extended combat
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner=self.player1.id)
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner=self.player2.id)
        destroyer1 = Unit(unit_type=UnitType.DESTROYER, owner=self.player1.id)
        destroyer2 = Unit(unit_type=UnitType.DESTROYER, owner=self.player2.id)

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)
        system.place_unit_in_space(destroyer1)
        system.place_unit_in_space(destroyer2)

        # Create combat role manager
        role_manager = CombatRoleManager(self.game_controller)

        # Attacker should remain consistent across multiple checks
        for _ in range(3):  # Simulate multiple combat rounds
            attacker_id = role_manager.get_attacker_id(system)
            assert attacker_id == self.player1.id

            defender_id = role_manager.get_defender_id(system)
            assert defender_id == self.player2.id

    def test_no_combat_raises_error(self) -> None:
        """Test that methods raise appropriate errors when no combat exists."""
        # Setup system with no opposing forces
        system = System(system_id="test_system")

        # Add units from only one player (no combat)
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner=self.player1.id)
        system.place_unit_in_space(cruiser1)

        # Create combat role manager
        role_manager = CombatRoleManager(self.game_controller)

        # Should raise error when trying to get defender (no combat)
        with pytest.raises(ValueError, match="No combat in system"):
            role_manager.get_defender_id(system)

        # Should also raise error when trying to get attacker (no combat)
        with pytest.raises(ValueError, match="No combat in system"):
            role_manager.get_attacker_id(system)

        # Should detect no combat
        assert not role_manager.has_combat(system)

    def test_retreat_manager_initialization(self) -> None:
        """Test that retreat manager properly integrates with attacker role."""
        # Setup combat scenario
        system = System(system_id="test_system")

        # Add units from both players
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner=self.player1.id)
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner=self.player2.id)

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        # Create combat role manager
        role_manager = CombatRoleManager(self.game_controller)

        # Verify attacker and defender roles for retreat system
        attacker_id = role_manager.get_attacker_id(system)
        defender_id = role_manager.get_defender_id(system)

        assert attacker_id == self.player1.id
        assert defender_id == self.player2.id

        # Verify combat is properly detected
        assert role_manager.has_combat(system)

    def test_ground_combat_defender_selection(self) -> None:
        """Test that ground combat defender is correctly identified."""
        # Setup planet with ground units
        planet = Planet(name="test_planet", resources=2, influence=1)
        system = System(system_id="test_system")
        system.add_planet(planet)

        # Add ground units from both players
        infantry1 = Unit(unit_type=UnitType.INFANTRY, owner=self.player1.id)
        infantry2 = Unit(unit_type=UnitType.INFANTRY, owner=self.player2.id)

        planet.place_unit(infantry1)
        planet.place_unit(infantry2)

        # Create combat role manager
        role_manager = CombatRoleManager(self.game_controller)

        # Test that non-active player is defender in ground combat
        defender_id = role_manager.get_ground_combat_defender_id(system, "test_planet")
        assert defender_id == self.player2.id

    def test_space_combat_defender_selection(self) -> None:
        """Test that space combat defender is correctly identified."""
        # Setup combat scenario
        system = System(system_id="test_system")

        # Add units from both players to create combat
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner=self.player1.id)
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner=self.player2.id)

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        # Create combat role manager
        role_manager = CombatRoleManager(self.game_controller)

        # Test that non-active player is defender
        defender_id = role_manager.get_defender_id(system)
        assert defender_id == self.player2.id

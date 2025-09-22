"""Tests for Rule 13: ATTACKER.

This module tests the implementation of Rule 13 from the Living Rules Reference,
which defines that during combat, the active player is the attacker.
"""

import pytest

from ti4.core.combat import CombatRoleManager
from ti4.core.constants import UnitType
from ti4.core.game_controller import GameController
from ti4.core.planet import Planet
from ti4.core.player import Player
from ti4.core.system import System
from ti4.core.unit import Unit


class TestRule13Attacker:
    """Test cases for Rule 13: ATTACKER."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.player1 = Player(id="player1", faction="test_faction1")
        self.player2 = Player(id="player2", faction="test_faction2")
        self.player3 = Player(id="player3", faction="test_faction3")

        players = [self.player1, self.player2, self.player3]
        self.game_controller = GameController(players)
        self.game_controller.start_action_phase()

    def test_active_player_is_attacker_in_space_combat(self) -> None:
        """Test that the active player is always the attacker in space combat."""
        # Setup combat scenario
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

    def test_attacker_role_with_retreat_manager(self) -> None:
        """Test attacker role integration with retreat manager."""
        # Setup combat scenario
        system = System(system_id="test_system")

        # Add units from both players
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner=self.player1.id)
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner=self.player2.id)

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        # Create combat role manager
        role_manager = CombatRoleManager(self.game_controller)

        # Get attacker ID
        attacker_id = role_manager.get_attacker_id(system)

        # Verify attacker role
        current_player_id = self.game_controller.get_current_player().id
        assert attacker_id == current_player_id

    def test_active_player_changes_attacker_role(self) -> None:
        """Test that when active player changes, attacker role changes."""
        # Setup combat scenario
        system = System(system_id="test_system")

        # Add units from both players to create combat
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner=self.player1.id)
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner=self.player2.id)

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        # Create combat role manager
        role_manager = CombatRoleManager(self.game_controller)

        # Initial attacker should be player1 (current active player)
        initial_attacker = role_manager.get_attacker_id(system)
        assert initial_attacker == self.player1.id

        # Advance to next player
        self.game_controller.advance_to_player(self.player2.id)

        # Now player2 should be the attacker
        new_attacker = role_manager.get_attacker_id(system)
        assert new_attacker == self.player2.id

    def test_attacker_role_with_multiple_players(self) -> None:
        """Test attacker role when multiple players have units in system."""
        # Setup combat scenario with three players
        system = System(system_id="test_system")

        # Add units from all three players
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner=self.player1.id)
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner=self.player2.id)
        cruiser3 = Unit(unit_type=UnitType.CRUISER, owner=self.player3.id)

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)
        system.place_unit_in_space(cruiser3)

        # Create combat role manager
        role_manager = CombatRoleManager(self.game_controller)

        # Active player should be attacker regardless of number of players
        attacker_id = role_manager.get_attacker_id(system)
        assert attacker_id == self.player1.id

        # Change active player to player3
        self.game_controller.advance_to_player(self.player3.id)

        # Now player3 should be attacker
        attacker_id = role_manager.get_attacker_id(system)
        assert attacker_id == self.player3.id

    def test_no_combat_raises_error(self) -> None:
        """Test that getting attacker when no combat exists raises error."""
        # Setup system with no opposing units
        system = System(system_id="test_system")

        # Add unit from only one player (no combat)
        cruiser = Unit(unit_type=UnitType.CRUISER, owner=self.player1.id)
        system.place_unit_in_space(cruiser)

        # Create combat role manager
        role_manager = CombatRoleManager(self.game_controller)

        # Should raise error when no combat exists
        with pytest.raises(ValueError, match="No combat in system"):
            role_manager.get_attacker_id(system)

    def test_attacker_role_with_tactical_action(self) -> None:
        """Test attacker role when combat is triggered by tactical action."""
        # Setup system with existing units
        system = System(system_id="test_system")

        # Player2 has existing unit in system
        existing_cruiser = Unit(unit_type=UnitType.CRUISER, owner=self.player2.id)
        system.place_unit_in_space(existing_cruiser)

        # Player1 (active) moves unit into system, triggering combat
        moving_cruiser = Unit(unit_type=UnitType.CRUISER, owner=self.player1.id)
        system.place_unit_in_space(moving_cruiser)

        # Create combat role manager
        role_manager = CombatRoleManager(self.game_controller)

        # Active player (who triggered combat) should be attacker
        attacker_id = role_manager.get_attacker_id(system)
        assert attacker_id == self.player1.id

    def test_attacker_role_persists_during_combat_rounds(self) -> None:
        """Test that attacker role doesn't change during combat rounds."""
        # Setup combat scenario
        system = System(system_id="test_system")

        # Add units from both players
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner=self.player1.id)
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner=self.player2.id)

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        # Create combat role manager
        role_manager = CombatRoleManager(self.game_controller)

        # Get initial attacker
        initial_attacker = role_manager.get_attacker_id(system)
        assert initial_attacker == self.player1.id

        # Simulate multiple combat rounds - attacker should remain same
        for _ in range(3):
            attacker_id = role_manager.get_attacker_id(system)
            assert attacker_id == initial_attacker

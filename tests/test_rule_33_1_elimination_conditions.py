"""Tests for Rule 33.1 - Elimination Conditions.

Rule 33.1: A player is eliminated if they have no ground forces on the game board,
have no unit with a production value on the game board, and do not control any planets.
"""

import pytest

from src.ti4.core.constants import Faction, UnitType
from src.ti4.core.game_state import GameState
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.system import System
from src.ti4.core.unit import Unit


class TestRule33_1EliminationConditions:
    """Test cases for Rule 33.1 - Three-condition elimination check."""

    def test_player_not_eliminated_with_ground_forces(self):
        """Test that a player with ground forces is not eliminated."""
        # Arrange
        game_state = GameState()
        player = Player(id="player1", faction=Faction.ARBOREC)
        game_state = game_state.add_player(player)

        # Add a system with ground forces
        system = System(system_id="test_system")
        planet = Planet(name="Test Planet", resources=2, influence=1)
        ground_force = Unit(unit_type=UnitType.INFANTRY, owner="player1")

        # Add ground force to planet and planet to system
        planet.place_unit(ground_force)
        system.add_planet(planet)
        game_state = game_state._create_new_state(systems={"test_system": system})

        # Act
        is_eliminated = game_state.should_eliminate_player("player1")

        # Assert
        assert not is_eliminated, "Player with ground forces should not be eliminated"

    def test_player_not_eliminated_with_production_units(self):
        """Test that a player with production units is not eliminated."""
        # Arrange
        game_state = GameState()
        player = Player(id="player1", faction=Faction.ARBOREC)
        game_state = game_state.add_player(player)

        # Add a system with a space dock (production unit)
        system = System(system_id="test_system")
        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        planet = Planet(name="Test Planet", resources=2, influence=1)

        # Add space dock to planet and planet to system
        planet.place_unit(space_dock)
        system.add_planet(planet)
        game_state = game_state._create_new_state(systems={"test_system": system})

        # Act
        is_eliminated = game_state.should_eliminate_player("player1")

        # Assert
        assert not is_eliminated, (
            "Player with production units should not be eliminated"
        )

    def test_player_not_eliminated_with_controlled_planet(self):
        """Test that a player who controls a planet is not eliminated."""
        # Arrange
        game_state = GameState()
        player = Player(id="player1", faction=Faction.ARBOREC)
        game_state = game_state.add_player(player)

        # Add a system with a planet
        system = System(system_id="test_system")
        planet = Planet(name="Test Planet", resources=2, influence=1)
        system.add_planet(planet)
        game_state = game_state._create_new_state(systems={"test_system": system})

        # Player gains control of the planet (using proper GameState method)
        success, game_state = game_state.gain_planet_control("player1", planet)
        assert success, "Player should successfully gain control of the planet"

        # Act
        is_eliminated = game_state.should_eliminate_player("player1")

        # Assert
        assert not is_eliminated, (
            "Player who controls a planet should not be eliminated"
        )

    def test_player_eliminated_with_all_three_conditions(self):
        """Test that a player is eliminated when all three conditions are met."""
        # Arrange
        game_state = GameState()
        player = Player(id="player1", faction=Faction.ARBOREC)
        game_state = game_state.add_player(player)

        # Add a system with no player units or controlled planets
        system = System(system_id="test_system")
        planet = Planet(name="Test Planet", resources=2, influence=1)
        # Planet is not controlled by player1
        system.add_planet(planet)
        game_state = game_state._create_new_state(systems={"test_system": system})

        # Act
        is_eliminated = game_state.should_eliminate_player("player1")

        # Assert
        assert is_eliminated, (
            "Player with no ground forces, no production units, and no controlled planets should be eliminated"
        )

    def test_player_not_eliminated_with_only_two_conditions(self):
        """Test that a player is not eliminated when only two of three conditions are met."""
        # Arrange
        game_state = GameState()
        player = Player(id="player1", faction=Faction.ARBOREC)
        game_state = game_state.add_player(player)

        # Add a system where player has no ground forces and no production units, but controls a planet
        system = System(system_id="test_system")
        planet = Planet(name="Test Planet", resources=2, influence=1)
        system.add_planet(planet)
        game_state = game_state._create_new_state(systems={"test_system": system})

        # Player gains control of the planet (using proper GameState method)
        success, game_state = game_state.gain_planet_control("player1", planet)
        assert success, "Player should successfully gain control of the planet"

        # Act
        is_eliminated = game_state.should_eliminate_player("player1")

        # Assert
        assert not is_eliminated, (
            "Player should not be eliminated when only two of three conditions are met"
        )

    def test_elimination_check_for_nonexistent_player(self):
        """Test elimination check for a player that doesn't exist."""
        # Arrange
        game_state = GameState()

        # Act & Assert
        with pytest.raises(
            ValueError, match="Player nonexistent_player does not exist"
        ):
            game_state.should_eliminate_player("nonexistent_player")

"""Integration tests for home system control validation with objective scoring.

This module tests the integration between HomeSystemControlValidator and
the objective scoring system to ensure Rule 61.16 is properly enforced.

LRR References:
- Rule 61.16: Home system control requirement for public objectives
- Requirements 2.1, 2.2, 2.3, 2.4, 2.5
"""

from src.ti4.core.constants import Faction
from src.ti4.core.galaxy import Galaxy
from src.ti4.core.game_state import GameState
from src.ti4.core.home_system_control_validator import HomeSystemControlValidator
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.system import System


class TestHomeSystemControlIntegration:
    """Integration tests for home system control validation."""

    def test_home_system_control_with_empty_home_system(self) -> None:
        """Test validation with home system that has no planets."""
        # Arrange
        validator = HomeSystemControlValidator()
        player = Player(id="player1", faction=Faction.SOL)

        # Create empty home system
        home_system = System("home_system_1")
        # No planets added to system

        galaxy = Galaxy()
        galaxy.register_system(home_system)
        game_state = GameState(players=[player], galaxy=galaxy)

        # Act
        result = validator.validate_home_system_control("player1", game_state)

        # Assert - empty home system should be valid (no planets to control)
        assert result.is_valid is True
        assert result.error_message is None

    def test_home_system_control_with_uncontrolled_planets(self) -> None:
        """Test validation with planets that have no controller."""
        # Arrange
        validator = HomeSystemControlValidator()
        player = Player(id="player1", faction=Faction.SOL)

        # Create home system with uncontrolled planet
        home_system = System("home_system_1")
        home_planet = Planet("Jord", resources=4, influence=2)
        # Planet has no controller (controlled_by is None)
        home_system.add_planet(home_planet)

        galaxy = Galaxy()
        galaxy.register_system(home_system)
        game_state = GameState(players=[player], galaxy=galaxy)

        # Act
        result = validator.validate_home_system_control("player1", game_state)

        # Assert
        assert result.is_valid is False
        assert "Jord" in result.error_message
        assert "not controlled" in result.error_message

    def test_get_home_system_planets_with_empty_system(self) -> None:
        """Test get_home_system_planets with empty system."""
        # Arrange
        validator = HomeSystemControlValidator()
        player = Player(id="player1", faction=Faction.SOL)

        # Create empty home system
        home_system = System("home_system_1")

        galaxy = Galaxy()
        galaxy.register_system(home_system)
        game_state = GameState(players=[player], galaxy=galaxy)

        # Act
        planets = validator.get_home_system_planets("player1", game_state)

        # Assert
        assert len(planets) == 0

    def test_validate_home_system_control_with_mixed_planet_states(self) -> None:
        """Test validation with mix of controlled, uncontrolled, and enemy-controlled planets."""
        # Arrange
        validator = HomeSystemControlValidator()
        player = Player(id="player1", faction=Faction.SOL)

        # Create home system with mixed planet control states
        home_system = System("home_system_1")

        planet1 = Planet("Jord", resources=4, influence=2)
        planet1.set_control("player1")  # Controlled by player

        planet2 = Planet("New Albion", resources=1, influence=1)
        # Planet2 has no controller (controlled_by is None)

        planet3 = Planet("Sanctuary", resources=2, influence=2)
        planet3.set_control("player2")  # Controlled by different player

        home_system.add_planet(planet1)
        home_system.add_planet(planet2)
        home_system.add_planet(planet3)

        galaxy = Galaxy()
        galaxy.register_system(home_system)
        game_state = GameState(players=[player], galaxy=galaxy)

        # Act
        result = validator.validate_home_system_control("player1", game_state)

        # Assert
        assert result.is_valid is False
        assert "New Albion" in result.error_message
        assert "Sanctuary" in result.error_message
        assert "not controlled" in result.error_message

    def test_validate_home_system_control_case_sensitivity(self) -> None:
        """Test that player ID matching is case sensitive."""
        # Arrange
        validator = HomeSystemControlValidator()
        player = Player(id="player1", faction=Faction.SOL)

        # Create home system with planet controlled by different case player id
        home_system = System("home_system_1")
        home_planet = Planet("Jord", resources=4, influence=2)
        home_planet.set_control("Player1")  # Capital P - different from player id
        home_system.add_planet(home_planet)

        galaxy = Galaxy()
        galaxy.register_system(home_system)
        game_state = GameState(players=[player], galaxy=galaxy)

        # Act
        result = validator.validate_home_system_control("player1", game_state)

        # Assert - should fail because "player1" != "Player1"
        assert result.is_valid is False
        assert "Jord" in result.error_message

    def test_home_system_id_generation_logic(self) -> None:
        """Test the home system ID generation logic for different player IDs."""
        # Arrange
        validator = HomeSystemControlValidator()

        test_cases = [
            ("player1", "home_system_1"),
            ("player2", "home_system_2"),
            ("player10", "home_system_10"),
            ("player123", "home_system_123"),
        ]

        for player_id, expected_system_id in test_cases:
            player = Player(id=player_id, faction=Faction.SOL)

            # Create home system with expected ID
            home_system = System(expected_system_id)
            home_planet = Planet("TestPlanet", resources=1, influence=1)
            home_planet.set_control(player_id)
            home_system.add_planet(home_planet)

            galaxy = Galaxy()
            galaxy.register_system(home_system)
            game_state = GameState(players=[player], galaxy=galaxy)

            # Act
            result = validator.validate_home_system_control(player_id, game_state)

            # Assert
            assert result.is_valid is True, f"Failed for player_id: {player_id}"

    def test_home_system_id_generation_with_non_standard_player_id(self) -> None:
        """Test home system ID generation with non-standard player ID format."""
        # Arrange
        validator = HomeSystemControlValidator()
        player = Player(id="custom_player_id", faction=Faction.SOL)

        # The current implementation splits on 'player' and takes the last part
        # For "custom_player_id", this would be "_id"
        expected_system_id = "home_system__id"

        # Create home system with expected ID
        home_system = System(expected_system_id)
        home_planet = Planet("TestPlanet", resources=1, influence=1)
        home_planet.set_control("custom_player_id")
        home_system.add_planet(home_planet)

        galaxy = Galaxy()
        galaxy.register_system(home_system)
        game_state = GameState(players=[player], galaxy=galaxy)

        # Act
        result = validator.validate_home_system_control("custom_player_id", game_state)

        # Assert
        assert result.is_valid is True

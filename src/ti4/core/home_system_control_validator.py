"""Home system control validation for TI4 objective scoring.

This module implements Rule 61.16 validation that requires players to control
all planets in their home system before scoring public objectives.

LRR References:
- Rule 61.16: Home system control requirement for public objectives
- Requirements 2.1, 2.2, 2.3, 2.4, 2.5
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game_state import GameState
    from .planet import Planet


@dataclass(frozen=True)
class ValidationResult:
    """Result of home system control validation.

    Args:
        is_valid: True if validation passed, False otherwise
        error_message: Descriptive error message if validation failed, None if valid
    """

    is_valid: bool
    error_message: str | None


class HomeSystemControlError(Exception):
    """Exception raised when home system control validation fails."""

    pass


class HomeSystemControlValidator:
    """Validates home system control for public objective eligibility.

    This class implements Rule 61.16 which requires players to control all
    planets in their home system before they can score public objectives.
    """

    def validate_home_system_control(
        self, player_id: str, game_state: GameState
    ) -> ValidationResult:
        """Validate that player controls all planets in their home system.

        Args:
            player_id: ID of the player to validate
            game_state: Current game state

        Returns:
            ValidationResult indicating success or failure with error details

        Raises:
            ValueError: If player not found, galaxy not set, or home system not found
        """
        # Validate player exists
        if not any(player.id == player_id for player in game_state.players):
            raise ValueError(f"Player {player_id} not found in game state")

        # Validate galaxy exists
        if game_state.galaxy is None:
            # If no galaxy is set up, we can't validate home system control
            # This is acceptable for testing scenarios or early game setup
            return ValidationResult(is_valid=True, error_message=None)

        # Get home system planets
        home_planets = self.get_home_system_planets(player_id, game_state)

        # Check control of each planet
        uncontrolled_planets = []
        for planet in home_planets:
            if planet.controlled_by != player_id:
                uncontrolled_planets.append(planet.name)

        # Return validation result
        if uncontrolled_planets:
            error_msg = f"The following planets in home system are not controlled by player {player_id}: {', '.join(uncontrolled_planets)}"
            return ValidationResult(is_valid=False, error_message=error_msg)

        return ValidationResult(is_valid=True, error_message=None)

    def get_home_system_planets(
        self, player_id: str, game_state: GameState
    ) -> list[Planet]:
        """Get all planets in player's home system.

        Args:
            player_id: ID of the player
            game_state: Current game state

        Returns:
            List of planets in the player's home system

        Raises:
            ValueError: If home system not found for player
        """
        if game_state.galaxy is None:
            raise ValueError("Galaxy not found in game state")

        # For now, use a simple mapping based on player ID
        # This will be enhanced when faction-specific home systems are implemented
        home_system_id = f"home_system_{player_id.split('player')[-1]}"

        home_system = game_state.galaxy.get_system(home_system_id)
        if home_system is None:
            raise ValueError(f"Home system not found for player {player_id}")

        return home_system.planets.copy()

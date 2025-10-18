"""Game-level technology management integration.

This module provides the bridge between Rule 90 TechnologyManager and the game state system.
"""

from .constants import Technology
from .game_state import GameState
from .technology import TechnologyManager


class GameTechnologyManager:
    """Manages technology integration with game state.

    This class coordinates between the Rule 90 TechnologyManager and the game state,
    ensuring consistency and providing a unified interface for technology operations.
    """

    def __init__(self, game_state: GameState) -> None:
        """Initialize the game technology manager.

        Args:
            game_state: The game state to manage technologies for
        """
        self.game_state = game_state
        self.technology_manager = TechnologyManager()

        # Initialize technology manager with existing game state data
        self._sync_from_game_state()

    def _sync_from_game_state(self) -> None:
        """Sync technology manager with existing game state data."""
        # First try to sync from player_technologies dict
        for player_id, tech_names in self.game_state.player_technologies.items():
            for tech_name in tech_names:
                try:
                    # Convert string to Technology enum
                    technology = Technology(tech_name)
                    self.technology_manager.gain_technology(player_id, technology)
                except ValueError:
                    # Skip unknown technologies (might be faction-specific)
                    continue

        # For mock game states, also check player state technologies
        if hasattr(self.game_state, "players") and isinstance(
            self.game_state.players, dict
        ):
            for player_id, player_state in self.game_state.players.items():
                if hasattr(player_state, "technologies"):
                    for tech_name in player_state.technologies:
                        try:
                            # Convert string to Technology enum
                            technology = Technology(tech_name)
                            self.technology_manager.gain_technology(
                                player_id, technology
                            )
                        except ValueError:
                            # Skip unknown technologies (might be faction-specific)
                            continue

    def _sync_to_game_state(self) -> None:
        """Sync technology manager data back to game state."""
        # Handle both real GameState (list of Player objects) and mock GameState (dict)
        if isinstance(self.game_state.players, list):
            # Real GameState with list of Player objects
            for player in self.game_state.players:
                player_id = player.id
                player_technologies = self.technology_manager.get_player_technologies(
                    player_id
                )
                tech_names = {tech.value for tech in player_technologies}

                # Update GameState technology tracking
                self.game_state.player_technologies[player_id] = list(tech_names)
        else:
            # Mock GameState with dict of player_id -> player_state
            for player_id in self.game_state.players.keys():
                player_technologies = self.technology_manager.get_player_technologies(
                    player_id
                )
                tech_names = {tech.value for tech in player_technologies}

                # Update GameState technology tracking
                self.game_state.player_technologies[player_id] = list(tech_names)

                # Also update mock player state if it exists
                player_state = self.game_state.players.get(player_id)
                if player_state and hasattr(player_state, "technologies"):
                    player_state.technologies = tech_names

    def can_research_technology(self, player_id: str, technology: Technology) -> bool:
        """Check if a player can research a technology.

        Args:
            player_id: The player attempting to research
            technology: The technology to research

        Returns:
            True if the player can research the technology
        """
        return self.technology_manager.can_research_technology(player_id, technology)

    def research_technology(self, player_id: str, technology: Technology) -> bool:
        """Research a technology for a player.

        Args:
            player_id: The player researching the technology
            technology: The technology to research

        Returns:
            True if research was successful
        """
        success = self.technology_manager.research_technology(player_id, technology)

        if success:
            # Sync back to game state
            self._sync_to_game_state()

            # Note: Research history tracking would be handled by the game controller
            # that manages the GameState transitions, not by this manager directly

        return success

    def get_player_technologies(self, player_id: str) -> set[Technology]:
        """Get all technologies owned by a player.

        Args:
            player_id: The player to get technologies for

        Returns:
            Set of technologies owned by the player
        """
        return self.technology_manager.get_player_technologies(player_id)

    def get_technology_deck(self, player_id: str) -> set[Technology]:
        """Get all technologies available in a player's deck.

        Args:
            player_id: The player to get the deck for

        Returns:
            Set of technologies available to research
        """
        return self.technology_manager.get_technology_deck(player_id)

    def get_technology_color(self, technology: Technology) -> str | None:
        """Get the color of a technology (if it has one).

        Args:
            technology: The technology to get the color for

        Returns:
            The color name, or None if it's a unit upgrade
        """
        try:
            color = self.technology_manager.get_technology_color(technology)
            return color.value
        except ValueError:
            # Unit upgrade or unconfirmed technology
            return None

    def is_unit_upgrade(self, technology: Technology) -> bool:
        """Check if a technology is a unit upgrade.

        Args:
            technology: The technology to check

        Returns:
            True if the technology is a unit upgrade
        """
        try:
            return self.technology_manager.is_unit_upgrade(technology)
        except ValueError:
            # Unconfirmed technology
            return False

    def get_unconfirmed_technologies(self) -> set[Technology]:
        """Get all technologies that need manual specification.

        Returns:
            Set of technologies missing confirmed specifications
        """
        return self.technology_manager.get_unconfirmed_technologies()

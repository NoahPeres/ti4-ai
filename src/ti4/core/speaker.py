"""Rule 80: SPEAKER - Speaker token privileges and powers.

LRR Rule 80: SPEAKER
The speaker is the player who has the speaker token.

80.1 - Initiative Order: Speaker is first player in initiative order
80.2 - Breaking Ties: Speaker breaks ties
80.3 - Token Passing: During agenda phase, speaker passes speaker token to player of their choice after resolving agenda
80.4 - Politics Strategy Card: If player has Politics strategy card, they can choose to take speaker token instead of drawing action cards
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game_state import GameState


class SpeakerManager:
    """Manages the speaker token and related functionality for Rule 80."""

    def _validate_player_id(
        self, game_state: GameState, player_id: str, context: str = "Player"
    ) -> None:
        """Validate that a player ID is valid and exists in the game.

        Args:
            game_state: Current game state
            player_id: ID of the player to validate
            context: Context for error messages (e.g., "Player", "New speaker")

        Raises:
            ValueError: If player_id is invalid or player does not exist in the game
        """
        if not player_id or not player_id.strip():
            raise ValueError(f"{context} ID cannot be empty")

        if not any(player.id == player_id for player in game_state.players):
            raise ValueError(f"{context} {player_id} does not exist")

    def _assign_speaker_internal(
        self, game_state: GameState, player_id: str, context: str = "Player"
    ) -> GameState:
        """Internal method to assign speaker with custom validation context."""
        self._validate_player_id(game_state, player_id, context)
        return game_state._create_new_state(speaker_id=player_id)

    def assign_speaker(self, game_state: GameState, player_id: str) -> GameState:
        """Assign the speaker token to a player.

        Args:
            game_state: Current game state
            player_id: ID of the player to assign as speaker

        Returns:
            New game state with speaker assigned

        Raises:
            ValueError: If player_id is invalid or player does not exist in the game
        """
        return self._assign_speaker_internal(game_state, player_id, "Player")

    def get_current_speaker(self, game_state: GameState) -> str | None:
        """Get the current speaker player ID.

        Args:
            game_state: Current game state

        Returns:
            Player ID of current speaker, or None if no speaker assigned
        """
        return game_state.speaker_id

    def get_initiative_order(self, game_state: GameState) -> list[str]:
        """Get the initiative order with speaker first (Rule 80.1).

        Args:
            game_state: Current game state

        Returns:
            List of player IDs in initiative order, with speaker first
        """
        all_player_ids = [player.id for player in game_state.players]

        # If no speaker, return players in their natural order
        if not game_state.speaker_id:
            return all_player_ids

        # Speaker goes first, then other players in their original order
        return [game_state.speaker_id] + [
            pid for pid in all_player_ids if pid != game_state.speaker_id
        ]

    def break_tie(self, game_state: GameState, tied_players: list[str]) -> str:
        """Break ties using speaker priority (Rule 80.2).

        Args:
            game_state: Current game state
            tied_players: List of player IDs that are tied

        Returns:
            Player ID of the tie winner (speaker if tied, otherwise first in initiative order)

        Raises:
            ValueError: If tied_players is empty or contains invalid player IDs
        """
        if not tied_players:
            raise ValueError("Cannot break tie with empty player list")

        # Validate all players exist
        all_player_ids = {player.id for player in game_state.players}
        for player_id in tied_players:
            if player_id not in all_player_ids:
                raise ValueError(f"Player {player_id} does not exist")

        # If speaker is among tied players, speaker wins
        if game_state.speaker_id and game_state.speaker_id in tied_players:
            return game_state.speaker_id

        # Otherwise, use initiative order to break tie
        initiative_order = self.get_initiative_order(game_state)
        for player_id in initiative_order:
            if player_id in tied_players:
                return player_id

        # This should never happen if tied_players contains valid player IDs
        return tied_players[0]

    def pass_speaker_token(
        self, game_state: GameState, new_speaker_id: str
    ) -> GameState:
        """Pass the speaker token to a new player (Rule 80.3).

        This method implements the token passing mechanism that occurs during the agenda phase,
        where the current speaker chooses who receives the speaker token next.

        Args:
            game_state: Current game state
            new_speaker_id: ID of the player to receive the speaker token

        Returns:
            New game state with speaker token passed to the new player

        Raises:
            ValueError: If new_speaker_id is invalid or player does not exist in the game
        """
        return self._assign_speaker_internal(game_state, new_speaker_id, "New speaker")

    def handle_speaker_elimination(
        self, game_state: GameState, eliminated_player_id: str
    ) -> GameState:
        """Handle speaker elimination by passing token to left player (Rule 80.7).

        When the speaker is eliminated from the game, the speaker token passes to the
        player to the speaker's left (clockwise in player order).

        Args:
            game_state: Current game state
            eliminated_player_id: ID of the player being eliminated

        Returns:
            New game state with speaker token passed to the next player

        Raises:
            ValueError: If eliminated_player_id is not the current speaker
        """
        if game_state.speaker_id != eliminated_player_id:
            raise ValueError(
                f"Player {eliminated_player_id} is not the current speaker"
            )

        # Find the next player in clockwise order (to the left of the eliminated speaker)
        player_ids = [player.id for player in game_state.players]
        current_index = player_ids.index(eliminated_player_id)
        next_index = (current_index + 1) % len(player_ids)
        next_speaker_id = player_ids[next_index]

        return self._assign_speaker_internal(
            game_state, next_speaker_id, "Next speaker"
        )

    def politics_card_choose_speaker(
        self, game_state: GameState, new_speaker_id: str
    ) -> GameState:
        """Choose new speaker using Politics strategy card (Rule 80.6).

        The Politics strategy card allows choosing any player OTHER than the current
        speaker to gain the speaker token.

        Args:
            game_state: Current game state
            new_speaker_id: ID of the player to become the new speaker

        Returns:
            New game state with speaker token assigned to the chosen player

        Raises:
            ValueError: If new_speaker_id is the current speaker or invalid
        """
        if game_state.speaker_id == new_speaker_id:
            raise ValueError(
                f"Cannot choose current speaker {new_speaker_id} as new speaker"
            )

        return self._assign_speaker_internal(game_state, new_speaker_id, "New speaker")

    def assign_random_speaker(self, game_state: GameState) -> GameState:
        """Assign a random player as speaker during setup (Rule 80.5).

        Args:
            game_state: Current game state

        Returns:
            Updated game state with random speaker assigned

        Raises:
            ValueError: If no players exist in the game
        """
        if not game_state.players:
            raise ValueError("Cannot assign random speaker: no players in game")

        import random

        random_player = random.choice(game_state.players)
        return self.assign_speaker(game_state, random_player.id)

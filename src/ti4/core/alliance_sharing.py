"""Alliance promissory note commander ability sharing system.

This module implements Rule 51.8: Alliance promissory note allows sharing commander abilities.
Handles commander ability access control and execution for Alliance promissory notes.

LRR References:
- Rule 51.8: Alliance promissory note allows sharing commander abilities
- Rule 51.8a: Commander's owner can still use ability even when Alliance note is shared
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .leaders import LeaderAbilityResult, LeaderLockStatus
from .transactions import PromissoryNote, PromissoryNoteType

if TYPE_CHECKING:
    from .game_state import GameState
    from .player import Player


class AllianceAbilityManager:
    """Manages Alliance promissory note commander ability sharing.

    Handles:
    - Granting commander access via Alliance promissory notes
    - Validating shared commander ability usage
    - Executing shared commander abilities
    - Revoking access when Alliance notes are returned

    LRR References:
    - Rule 51.8: Alliance promissory note allows sharing commander abilities
    - Rule 51.8a: Commander's owner can still use ability even when Alliance note is shared
    """

    def __init__(self) -> None:
        """Initialize the Alliance ability manager."""
        # Track active Alliance notes: (receiving_player, issuing_player) -> PromissoryNote
        self._active_alliance_notes: dict[tuple[str, str], PromissoryNote] = {}

    def grant_commander_access(
        self, alliance_note: PromissoryNote, game_state: GameState
    ) -> None:
        """Grant commander ability access via Alliance promissory note.

        Args:
            alliance_note: The Alliance promissory note granting access
            game_state: Current game state

        Raises:
            ValueError: If the note is not an Alliance promissory note or has invalid data

        LRR References:
        - Rule 51.8: Alliance promissory note allows sharing commander abilities
        """
        self._validate_alliance_note(alliance_note)

        # Store the active Alliance note
        # We've already validated that receiving_player is not None
        assert alliance_note.receiving_player is not None
        key = (alliance_note.receiving_player, alliance_note.issuing_player)
        self._active_alliance_notes[key] = alliance_note

    def revoke_commander_access(
        self, alliance_note: PromissoryNote, game_state: GameState
    ) -> None:
        """Revoke commander ability access when Alliance note is returned.

        Args:
            alliance_note: The Alliance promissory note being returned
            game_state: Current game state

        Raises:
            ValueError: If the note is not an Alliance promissory note

        LRR References:
        - Rule 51.8: Alliance note must be active for sharing
        """
        self._validate_alliance_note(alliance_note)

        # Remove the Alliance note
        # We've already validated that receiving_player is not None
        assert alliance_note.receiving_player is not None
        key = (alliance_note.receiving_player, alliance_note.issuing_player)
        self._active_alliance_notes.pop(key, None)

    def can_use_shared_commander(
        self, using_player: str, commander_owner: str, game_state: GameState
    ) -> bool:
        """Check if a player can use another player's commander ability.

        Args:
            using_player: The player attempting to use the commander ability
            commander_owner: The player who owns the commander
            game_state: Current game state

        Returns:
            True if the player can use the shared commander ability

        Raises:
            ValueError: If player IDs are invalid

        LRR References:
        - Rule 51.8: Alliance promissory note allows sharing commander abilities
        - Rule 51.8a: Commander's owner can still use ability
        """
        self._validate_player_ids(using_player, commander_owner)

        # Owner can always use their own commander
        if using_player == commander_owner:
            return True

        # Check if there's an active Alliance note
        key = (using_player, commander_owner)
        if key not in self._active_alliance_notes:
            return False

        # Get the commander from the owner
        owner_player = self._get_player_by_id(game_state, commander_owner)
        if not owner_player:
            return False

        commander = owner_player.leader_sheet.commander
        if not commander:
            return False

        # Commander must be unlocked to be shared
        return commander.lock_status == LeaderLockStatus.UNLOCKED

    def execute_shared_commander_ability(
        self,
        using_player: str,
        commander_owner: str,
        game_state: GameState,
        **kwargs: Any,
    ) -> LeaderAbilityResult:
        """Execute a shared commander ability.

        Args:
            using_player: The player executing the commander ability
            commander_owner: The player who owns the commander
            game_state: Current game state
            **kwargs: Additional arguments for ability execution

        Returns:
            Result of the commander ability execution

        Raises:
            ValueError: If player IDs are invalid

        LRR References:
        - Rule 51.8: Alliance promissory note allows sharing commander abilities
        - Rule 51.8a: Commander's owner can still use ability
        """
        self._validate_player_ids(using_player, commander_owner)

        # Check if the player can use the shared commander
        if not self.can_use_shared_commander(using_player, commander_owner, game_state):
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message="No access to shared commander ability",
            )

        # Get the commander from the owner
        owner_player = self._get_player_by_id(game_state, commander_owner)
        if not owner_player:
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message=f"Commander owner {commander_owner} not found",
            )

        commander = owner_player.leader_sheet.commander
        if not commander:
            return LeaderAbilityResult(
                success=False, effects=[], error_message="Commander not found"
            )

        # Execute the commander ability
        return commander.execute_ability(game_state, **kwargs)

    def _validate_alliance_note(self, alliance_note: PromissoryNote) -> None:
        """Validate that a promissory note is a valid Alliance note.

        Args:
            alliance_note: The promissory note to validate

        Raises:
            ValueError: If the note is invalid
        """
        if alliance_note.note_type != PromissoryNoteType.ALLIANCE:
            raise ValueError(
                "Only Alliance promissory notes can grant commander access"
            )

        if not alliance_note.receiving_player:
            raise ValueError("Alliance note must have a receiving player")

        if not alliance_note.issuing_player:
            raise ValueError("Alliance note must have an issuing player")

        if alliance_note.receiving_player == alliance_note.issuing_player:
            raise ValueError("Alliance note cannot be between the same player")

    def _validate_player_ids(
        self, using_player: str | None, commander_owner: str | None
    ) -> None:
        """Validate player ID parameters.

        Args:
            using_player: The player attempting to use the ability
            commander_owner: The player who owns the commander

        Raises:
            ValueError: If player IDs are invalid
        """
        if not using_player or (
            isinstance(using_player, str) and not using_player.strip()
        ):
            raise ValueError("using_player cannot be empty or None")

        if not commander_owner or (
            isinstance(commander_owner, str) and not commander_owner.strip()
        ):
            raise ValueError("commander_owner cannot be empty or None")

    def handle_player_elimination(self, eliminated_player_id: str) -> None:
        """Handle player elimination by revoking all Alliance notes involving the player.

        Args:
            eliminated_player_id: The ID of the player being eliminated

        LRR Reference: Rule 69.7 - When player eliminated, all matching promissory notes returned
        """
        # Find all Alliance notes involving the eliminated player and remove them
        notes_to_remove = []

        for key, _note in self._active_alliance_notes.items():
            receiving_player, issuing_player = key
            if (
                receiving_player == eliminated_player_id
                or issuing_player == eliminated_player_id
            ):
                notes_to_remove.append(key)

        # Remove all Alliance notes involving the eliminated player
        for key in notes_to_remove:
            self._active_alliance_notes.pop(key, None)

    def _get_player_by_id(self, game_state: GameState, player_id: str) -> Player | None:
        """Get a player by their ID from the game state.

        Args:
            game_state: The game state to search
            player_id: The ID of the player to find

        Returns:
            The player with the specified ID, or None if not found
        """
        for player in game_state.players:
            if player.id == player_id:
                return player
        return None

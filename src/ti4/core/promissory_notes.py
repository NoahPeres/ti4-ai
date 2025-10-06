"""Promissory note system for TI4 Rule 69: PROMISSORY NOTES.

This module implements Rule 69: PROMISSORY NOTES mechanics according to the TI4 LRR.
Handles promissory note management, ownership, resolution, and lifecycle.
"""

from typing import TYPE_CHECKING

from .transactions import PromissoryNote, PromissoryNoteType

if TYPE_CHECKING:
    from .alliance_sharing import AllianceAbilityManager
    from .game_state import GameState


class PromissoryNoteManager:
    """Manages promissory note mechanics according to Rule 69.

    Handles:
    - Card resolution and timing (Rule 69.1)
    - Own card restriction validation (Rule 69.2)
    - Card return timing (Rule 69.3)
    - Reuse after return (Rule 69.4)
    - Hidden information management (Rule 69.6)
    - Elimination effects (Rule 69.7)
    """

    def __init__(self) -> None:
        """Initialize the promissory note manager."""
        # Rule 69.6: Players should keep promissory note hands hidden
        self._player_hands: dict[str, list[PromissoryNote]] = {}

        # Rule 69.4: Track returned notes that can be reused
        self._available_notes: set[PromissoryNote] = set()

        # Alliance ability manager for handling commander sharing
        from .alliance_sharing import AllianceAbilityManager

        self._alliance_manager = AllianceAbilityManager()

    def can_player_play_note(self, note: PromissoryNote, player_id: str) -> bool:
        """Check if a player can play a promissory note according to Rule 69.2.

        Args:
            note: The promissory note to check
            player_id: The player attempting to play the note

        Returns:
            True if the player can play the note, False if restricted

        LRR Reference: Rule 69.2 - Players cannot play their own color's or faction's promissory notes
        """
        # Rule 69.2: Players cannot play their own color's or faction's promissory notes
        return note.issuing_player != player_id

    def add_note_to_hand(self, note: PromissoryNote, player_id: str) -> None:
        """Add a promissory note to a player's hidden hand.

        Args:
            note: The promissory note to add
            player_id: The player receiving the note

        LRR Reference: Rule 69.6 - Players should keep promissory note hands hidden
        """
        if player_id not in self._player_hands:
            self._player_hands[player_id] = []
        self._player_hands[player_id].append(note)

        # Rule 69.4: Remove from available notes when given to a player
        self._available_notes.discard(note)

    def get_player_hand(self, player_id: str) -> list[PromissoryNote]:
        """Get a player's promissory note hand.

        Args:
            player_id: The player whose hand to retrieve

        Returns:
            List of promissory notes in the player's hand

        LRR Reference: Rule 69.6 - Players should keep promissory note hands hidden
        """
        return self._player_hands.get(player_id, [])

    def return_note_after_use(
        self,
        note: PromissoryNote,
        player_id: str,
        game_state: "GameState | None" = None,
    ) -> None:
        """Return a promissory note after its ability is resolved.

        Args:
            note: The promissory note to return
            player_id: The player returning the note
            game_state: Current game state (required for Alliance note revocation)

        LRR Reference: Rule 69.3 - Promissory notes returned after abilities completely resolved
        """
        # Handle Alliance note revocation before general return processing
        if note.note_type == PromissoryNoteType.ALLIANCE:
            if game_state is None:
                raise ValueError(
                    "game_state is required to revoke Alliance note commander access"
                )
            self._alliance_manager.revoke_commander_access(note, game_state)

        # Remove note from player's hand
        if player_id in self._player_hands and note in self._player_hands[player_id]:
            self._player_hands[player_id].remove(note)

        # Rule 69.4: Make note available for future transactions
        self._available_notes.add(note)

    def is_note_available_for_transaction(self, note: PromissoryNote) -> bool:
        """Check if a promissory note is available for transaction.

        Args:
            note: The promissory note to check

        Returns:
            True if the note is available for transaction

        LRR Reference: Rule 69.4 - Returned promissory notes can be given to other players again
        """
        return note in self._available_notes

    def handle_player_elimination(self, eliminated_player: str) -> None:
        """Handle player elimination by returning all their promissory notes.

        Args:
            eliminated_player: The player being eliminated

        LRR Reference: Rule 69.7 - When player eliminated, all matching color/faction
        promissory notes returned to game box
        """
        # Handle notes in the eliminated player's hand
        if eliminated_player in self._player_hands:
            eliminated_player_hand = self._player_hands[eliminated_player].copy()

            # Iterate through each note in the eliminated player's hand
            for note in eliminated_player_hand:
                # If the note belongs to another player, return it to their available pool
                if note.issuing_player != eliminated_player:
                    # Add to available notes for the issuing player
                    self._available_notes.add(note)
                    # Remove from eliminated player's hand
                    if note in self._player_hands[eliminated_player]:
                        self._player_hands[eliminated_player].remove(note)

            # Remove the eliminated player's hand entry
            del self._player_hands[eliminated_player]

        # Remove all notes issued by the eliminated player from other players' hands
        for _player_id, hand in self._player_hands.items():
            # Create a copy of the hand to iterate over while modifying
            hand_copy = hand.copy()
            for note in hand_copy:
                if note.issuing_player == eliminated_player:
                    hand.remove(note)

        # Remove all notes issued by the eliminated player from available notes
        notes_to_remove = {
            note
            for note in self._available_notes
            if note.issuing_player == eliminated_player
        }
        self._available_notes -= notes_to_remove

        # Handle Alliance note revocation for eliminated player
        # Revoke Alliance access for all notes involving the eliminated player
        self._alliance_manager.handle_player_elimination(eliminated_player)

    def activate_alliance_note(
        self, alliance_note: PromissoryNote, game_state: "GameState"
    ) -> None:
        """Activate an Alliance promissory note to grant commander ability access.

        Args:
            alliance_note: The Alliance promissory note to activate
            game_state: Current game state

        Raises:
            ValueError: If the note is not an Alliance note or commander is locked

        LRR Reference: Rule 51.8 - Alliance promissory note allows sharing commander abilities
        """
        # Validate that this is an Alliance note
        if alliance_note.note_type != PromissoryNoteType.ALLIANCE:
            raise ValueError(
                "Only Alliance promissory notes can be activated for commander sharing"
            )

        if not alliance_note.receiving_player:
            raise ValueError("Alliance note must have a receiving player")

        if not alliance_note.issuing_player:
            raise ValueError("Alliance note must have an issuing player")

        # Check that the commander is unlocked before granting access
        issuing_player = None
        for player in game_state.players:
            if player.id == alliance_note.issuing_player:
                issuing_player = player
                break

        if not issuing_player:
            raise ValueError(
                f"Issuing player {alliance_note.issuing_player} not found in game state"
            )

        commander = issuing_player.leader_sheet.commander
        if not commander:
            raise ValueError(
                f"Commander not found for player {alliance_note.issuing_player}"
            )

        from .leaders import LeaderLockStatus

        if commander.lock_status != LeaderLockStatus.UNLOCKED:
            raise ValueError(
                "Commander must be unlocked to share via Alliance promissory note"
            )

        # Grant commander access through Alliance manager
        self._alliance_manager.grant_commander_access(alliance_note, game_state)

    def get_alliance_manager(self) -> "AllianceAbilityManager":
        """Get the Alliance ability manager for direct access.

        Returns:
            The Alliance ability manager instance
        """
        return self._alliance_manager

    def __eq__(self, other: object) -> bool:
        """Check equality with another PromissoryNoteManager."""
        if not isinstance(other, PromissoryNoteManager):
            return False
        return (
            self._player_hands == other._player_hands
            and self._available_notes == other._available_notes
        )

    def __hash__(self) -> int:
        """PromissoryNoteManager is not hashable due to mutable state."""
        raise TypeError("PromissoryNoteManager is mutable and cannot be hashed")

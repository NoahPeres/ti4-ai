"""Tests for Alliance promissory note commander ability sharing.

This module tests the Alliance promissory note mechanism for sharing commander
abilities according to TI4 LRR Rule 51.8.

Rule 51.8 Sub-rules tested:
- 51.8: Alliance promissory note allows sharing commander abilities
- 51.8a: Commander's owner can still use ability even when Alliance note is shared

Requirements tested:
- 6.1: Alliance promissory note grants access to commander ability
- 6.2: Shared commander ability functions identically to original
- 6.3: Alliance note return revokes shared access
- 6.4: Multiple Alliance notes provide independent access
- 6.5: Locked commanders cannot be shared via Alliance notes
"""

import pytest

from ti4.core.constants import Faction
from ti4.core.game_state import GameState
from ti4.core.leaders import LeaderLockStatus
from ti4.core.player import Player
from ti4.core.transactions import PromissoryNote, PromissoryNoteType


class TestAlliancePromissoryNoteSharing:
    """Test Alliance promissory note commander ability sharing mechanism."""

    def test_alliance_note_grants_access_to_unlocked_commander_ability(self) -> None:
        """Test that Alliance promissory note grants access to unlocked commander ability.

        LRR Reference: Rule 51.8 - Alliance promissory note allows sharing commander abilities
        Requirements: 6.1, 6.2
        """
        # RED phase - this test will fail until we implement the sharing mechanism

        # Create players
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)

        # Initialize leaders for both players
        from ti4.core.leaders import initialize_player_leaders

        initialize_player_leaders(player1)
        initialize_player_leaders(player2)

        # Unlock player1's commander
        commander = player1.leader_sheet.commander
        assert commander is not None
        commander.unlock()

        # Create Alliance promissory note from player1 to player2
        alliance_note = PromissoryNote(
            note_type=PromissoryNoteType.ALLIANCE,
            issuing_player="player1",
            receiving_player="player2",
        )

        # Create game state and add players
        game_state = GameState()
        game_state = game_state.add_player(player1)
        game_state = game_state.add_player(player2)

        # This should fail initially - we need to implement the sharing mechanism
        from ti4.core.alliance_sharing import AllianceAbilityManager

        alliance_manager = AllianceAbilityManager()

        # Grant access via Alliance note
        alliance_manager.grant_commander_access(alliance_note, game_state)

        # Player2 should now be able to use player1's commander ability
        can_use = alliance_manager.can_use_shared_commander(
            "player2", "player1", game_state
        )
        assert can_use is True

    def test_alliance_note_does_not_grant_access_to_locked_commander(self) -> None:
        """Test that Alliance promissory note does not grant access to locked commanders.

        LRR Reference: Rule 51.8 - Alliance only works if commander is unlocked
        Requirements: 6.5
        """
        # Create players
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)

        # Initialize leaders for both players
        from ti4.core.leaders import initialize_player_leaders

        initialize_player_leaders(player1)
        initialize_player_leaders(player2)

        # Keep player1's commander locked
        commander = player1.leader_sheet.commander
        assert commander is not None
        assert commander.lock_status == LeaderLockStatus.LOCKED

        # Create Alliance promissory note from player1 to player2
        alliance_note = PromissoryNote(
            note_type=PromissoryNoteType.ALLIANCE,
            issuing_player="player1",
            receiving_player="player2",
        )

        # Create game state
        game_state = GameState()

        from ti4.core.alliance_sharing import AllianceAbilityManager

        alliance_manager = AllianceAbilityManager()

        # Grant access via Alliance note
        alliance_manager.grant_commander_access(alliance_note, game_state)

        # Player2 should NOT be able to use player1's locked commander ability
        can_use = alliance_manager.can_use_shared_commander(
            "player2", "player1", game_state
        )
        assert can_use is False

    def test_original_owner_can_still_use_commander_when_alliance_shared(self) -> None:
        """Test that commander's owner can still use ability when Alliance note is active.

        LRR Reference: Rule 51.8a - Commander's owner can still use ability
        Requirements: 6.1, 6.2
        """
        # Create players
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)

        # Initialize leaders for both players
        from ti4.core.leaders import initialize_player_leaders

        initialize_player_leaders(player1)
        initialize_player_leaders(player2)

        # Unlock player1's commander
        commander = player1.leader_sheet.commander
        assert commander is not None
        commander.unlock()

        # Create Alliance promissory note from player1 to player2
        alliance_note = PromissoryNote(
            note_type=PromissoryNoteType.ALLIANCE,
            issuing_player="player1",
            receiving_player="player2",
        )

        # Create game state and add players
        game_state = GameState()
        game_state = game_state.add_player(player1)
        game_state = game_state.add_player(player2)

        from ti4.core.alliance_sharing import AllianceAbilityManager

        alliance_manager = AllianceAbilityManager()

        # Grant access via Alliance note
        alliance_manager.grant_commander_access(alliance_note, game_state)

        # Both players should be able to use the commander ability
        owner_can_use = alliance_manager.can_use_shared_commander(
            "player1", "player1", game_state
        )
        recipient_can_use = alliance_manager.can_use_shared_commander(
            "player2", "player1", game_state
        )

        assert owner_can_use is True
        assert recipient_can_use is True

    def test_alliance_note_return_revokes_shared_access(self) -> None:
        """Test that returning Alliance promissory note revokes shared access.

        LRR Reference: Rule 51.8 - Alliance note must be active for sharing
        Requirements: 6.3
        """
        # Create players
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)

        # Initialize leaders for both players
        from ti4.core.leaders import initialize_player_leaders

        initialize_player_leaders(player1)
        initialize_player_leaders(player2)

        # Unlock player1's commander
        commander = player1.leader_sheet.commander
        assert commander is not None
        commander.unlock()

        # Create Alliance promissory note from player1 to player2
        alliance_note = PromissoryNote(
            note_type=PromissoryNoteType.ALLIANCE,
            issuing_player="player1",
            receiving_player="player2",
        )

        # Create game state and add players
        game_state = GameState()
        game_state = game_state.add_player(player1)
        game_state = game_state.add_player(player2)

        from ti4.core.alliance_sharing import AllianceAbilityManager

        alliance_manager = AllianceAbilityManager()

        # Grant access via Alliance note
        alliance_manager.grant_commander_access(alliance_note, game_state)

        # Verify access is granted
        can_use_before = alliance_manager.can_use_shared_commander(
            "player2", "player1", game_state
        )
        assert can_use_before is True

        # Return the Alliance note
        alliance_manager.revoke_commander_access(alliance_note, game_state)

        # Access should be revoked
        can_use_after = alliance_manager.can_use_shared_commander(
            "player2", "player1", game_state
        )
        assert can_use_after is False

    def test_multiple_alliance_notes_provide_independent_access(self) -> None:
        """Test that multiple Alliance notes provide independent access.

        Requirements: 6.4
        """
        # Create three players
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)
        player3 = Player(id="player3", faction=Faction.SAAR)

        # Initialize leaders for all players
        from ti4.core.leaders import initialize_player_leaders

        initialize_player_leaders(player1)
        initialize_player_leaders(player2)
        initialize_player_leaders(player3)

        # Unlock commanders for player1 and player2
        player1.leader_sheet.commander.unlock()
        player2.leader_sheet.commander.unlock()

        # Create Alliance promissory notes
        alliance_note_1to3 = PromissoryNote(
            note_type=PromissoryNoteType.ALLIANCE,
            issuing_player="player1",
            receiving_player="player3",
        )
        alliance_note_2to3 = PromissoryNote(
            note_type=PromissoryNoteType.ALLIANCE,
            issuing_player="player2",
            receiving_player="player3",
        )

        # Create game state and add players
        game_state = GameState()
        game_state = game_state.add_player(player1)
        game_state = game_state.add_player(player2)
        game_state = game_state.add_player(player3)

        from ti4.core.alliance_sharing import AllianceAbilityManager

        alliance_manager = AllianceAbilityManager()

        # Grant access via both Alliance notes
        alliance_manager.grant_commander_access(alliance_note_1to3, game_state)
        alliance_manager.grant_commander_access(alliance_note_2to3, game_state)

        # Player3 should have access to both commanders
        can_use_player1_commander = alliance_manager.can_use_shared_commander(
            "player3", "player1", game_state
        )
        can_use_player2_commander = alliance_manager.can_use_shared_commander(
            "player3", "player2", game_state
        )

        assert can_use_player1_commander is True
        assert can_use_player2_commander is True

        # Return one Alliance note
        alliance_manager.revoke_commander_access(alliance_note_1to3, game_state)

        # Player3 should still have access to player2's commander
        can_use_player1_after = alliance_manager.can_use_shared_commander(
            "player3", "player1", game_state
        )
        can_use_player2_after = alliance_manager.can_use_shared_commander(
            "player3", "player2", game_state
        )

        assert can_use_player1_after is False
        assert can_use_player2_after is True

    def test_shared_commander_ability_execution_functions_identically(self) -> None:
        """Test that shared commander ability execution functions identically to original.

        Requirements: 6.2
        """
        # Create players
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)

        # Initialize leaders for both players
        from ti4.core.leaders import initialize_player_leaders

        initialize_player_leaders(player1)
        initialize_player_leaders(player2)

        # Unlock player1's commander
        commander = player1.leader_sheet.commander
        assert commander is not None
        commander.unlock()

        # Create Alliance promissory note from player1 to player2
        alliance_note = PromissoryNote(
            note_type=PromissoryNoteType.ALLIANCE,
            issuing_player="player1",
            receiving_player="player2",
        )

        # Create game state and add players
        game_state = GameState()
        game_state = game_state.add_player(player1)
        game_state = game_state.add_player(player2)

        from ti4.core.alliance_sharing import AllianceAbilityManager

        alliance_manager = AllianceAbilityManager()

        # Grant access via Alliance note
        alliance_manager.grant_commander_access(alliance_note, game_state)

        # Execute ability as original owner
        original_result = alliance_manager.execute_shared_commander_ability(
            "player1", "player1", game_state
        )

        # Execute ability as shared user
        shared_result = alliance_manager.execute_shared_commander_ability(
            "player2", "player1", game_state
        )

        # Results should be identical (both successful with same effects)
        assert original_result.success is True
        assert shared_result.success is True
        assert original_result.effects == shared_result.effects


class TestAlliancePromissoryNoteValidation:
    """Test validation for Alliance promissory note sharing."""

    def test_cannot_grant_access_with_invalid_alliance_note(self) -> None:
        """Test that invalid Alliance notes cannot grant commander access."""
        # Create game state
        game_state = GameState()

        from ti4.core.alliance_sharing import AllianceAbilityManager

        alliance_manager = AllianceAbilityManager()

        # Try to grant access with non-Alliance note
        non_alliance_note = PromissoryNote(
            note_type=PromissoryNoteType.CEASEFIRE,
            issuing_player="player1",
            receiving_player="player2",
        )

        with pytest.raises(ValueError, match="Only Alliance promissory notes"):
            alliance_manager.grant_commander_access(non_alliance_note, game_state)

    def test_cannot_use_shared_commander_without_active_alliance_note(self) -> None:
        """Test that commander cannot be used without active Alliance note."""
        # Create game state
        game_state = GameState()

        from ti4.core.alliance_sharing import AllianceAbilityManager

        alliance_manager = AllianceAbilityManager()

        # Try to use shared commander without any Alliance note
        can_use = alliance_manager.can_use_shared_commander(
            "player2", "player1", game_state
        )
        assert can_use is False

    def test_cannot_execute_shared_ability_without_access(self) -> None:
        """Test that shared ability cannot be executed without proper access."""
        # Create game state
        game_state = GameState()

        from ti4.core.alliance_sharing import AllianceAbilityManager

        alliance_manager = AllianceAbilityManager()

        # Try to execute shared ability without access
        result = alliance_manager.execute_shared_commander_ability(
            "player2", "player1", game_state
        )

        assert result.success is False
        assert "No access to shared commander" in result.error_message

    def test_validation_rejects_invalid_player_ids(self) -> None:
        """Test that validation rejects invalid player IDs."""
        from ti4.core.alliance_sharing import AllianceAbilityManager

        alliance_manager = AllianceAbilityManager()
        game_state = GameState()

        # Test empty using_player
        with pytest.raises(ValueError, match="using_player cannot be empty"):
            alliance_manager.can_use_shared_commander("", "player1", game_state)

        # Test empty commander_owner
        with pytest.raises(ValueError, match="commander_owner cannot be empty"):
            alliance_manager.can_use_shared_commander("player1", "", game_state)

        # Test None using_player
        with pytest.raises(ValueError, match="using_player cannot be empty"):
            alliance_manager.can_use_shared_commander(None, "player1", game_state)

    def test_validation_rejects_invalid_alliance_notes(self) -> None:
        """Test that validation rejects invalid Alliance notes."""
        from ti4.core.alliance_sharing import AllianceAbilityManager

        alliance_manager = AllianceAbilityManager()
        game_state = GameState()

        # Test Alliance note without receiving player
        invalid_note = PromissoryNote(
            note_type=PromissoryNoteType.ALLIANCE,
            issuing_player="player1",
            receiving_player=None,
        )

        with pytest.raises(
            ValueError, match="Alliance note must have a receiving player"
        ):
            alliance_manager.grant_commander_access(invalid_note, game_state)

        # Test Alliance note with same issuing and receiving player
        self_note = PromissoryNote(
            note_type=PromissoryNoteType.ALLIANCE,
            issuing_player="player1",
            receiving_player="player1",
        )

        with pytest.raises(
            ValueError, match="Alliance note cannot be between the same player"
        ):
            alliance_manager.grant_commander_access(self_note, game_state)

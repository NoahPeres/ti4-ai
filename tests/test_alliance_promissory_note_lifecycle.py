"""Integration tests for Alliance promissory note lifecycle management.

This module tests the complete lifecycle of Alliance promissory notes from
transaction to activation to return, ensuring proper integration between
the promissory note system and leader ability sharing.

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
from ti4.core.leaders import initialize_player_leaders
from ti4.core.player import Player
from ti4.core.promissory_notes import PromissoryNoteManager
from ti4.core.transactions import PromissoryNote, PromissoryNoteType


class TestAlliancePromissoryNoteLifecycle:
    """Test complete Alliance promissory note lifecycle integration."""

    def test_alliance_note_activation_grants_commander_access(self) -> None:
        """Test that activating Alliance note through promissory note system grants commander access.

        This tests the integration between PromissoryNoteManager and AllianceAbilityManager.
        Requirements: 6.1
        """
        # RED phase - this test will fail until we implement the integration

        # Create players
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)

        # Initialize leaders
        initialize_player_leaders(player1)
        initialize_player_leaders(player2)

        # Unlock player1's commander
        player1.leader_sheet.commander.unlock()

        # Create Alliance promissory note
        alliance_note = PromissoryNote(
            note_type=PromissoryNoteType.ALLIANCE,
            issuing_player="player1",
            receiving_player="player2",
        )

        # Create game state and managers
        game_state = GameState()
        game_state = game_state.add_player(player1)
        game_state = game_state.add_player(player2)

        promissory_manager = PromissoryNoteManager()

        # Give Alliance note to player2 through promissory note system
        promissory_manager.add_note_to_hand(alliance_note, "player2")

        # Player2 should not have access yet (note not activated)
        alliance_manager = promissory_manager.get_alliance_manager()

        can_use_before = alliance_manager.can_use_shared_commander(
            "player2", "player1", game_state
        )
        assert can_use_before is False

        # Activate the Alliance note (this should grant access)
        promissory_manager.activate_alliance_note(alliance_note, game_state)

        # Player2 should now have access to player1's commander
        can_use_after = alliance_manager.can_use_shared_commander(
            "player2", "player1", game_state
        )
        assert can_use_after is True

    def test_alliance_note_return_revokes_commander_access(self) -> None:
        """Test that returning Alliance note through promissory note system revokes commander access.

        Requirements: 6.3
        """
        # Create players and setup
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)

        initialize_player_leaders(player1)
        initialize_player_leaders(player2)
        player1.leader_sheet.commander.unlock()

        alliance_note = PromissoryNote(
            note_type=PromissoryNoteType.ALLIANCE,
            issuing_player="player1",
            receiving_player="player2",
        )

        game_state = GameState()
        game_state = game_state.add_player(player1)
        game_state = game_state.add_player(player2)

        promissory_manager = PromissoryNoteManager()
        alliance_manager = promissory_manager.get_alliance_manager()

        # Give and activate Alliance note
        promissory_manager.add_note_to_hand(alliance_note, "player2")
        promissory_manager.activate_alliance_note(alliance_note, game_state)

        # Verify access is granted
        can_use_before = alliance_manager.can_use_shared_commander(
            "player2", "player1", game_state
        )
        assert can_use_before is True

        # Return the Alliance note
        promissory_manager.return_note_after_use(alliance_note, "player2", game_state)

        # Access should be revoked
        can_use_after = alliance_manager.can_use_shared_commander(
            "player2", "player1", game_state
        )
        assert can_use_after is False

    def test_multiple_alliance_notes_lifecycle_independence(self) -> None:
        """Test that multiple Alliance notes have independent lifecycles.

        Requirements: 6.4
        """
        # Create three players
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)
        player3 = Player(id="player3", faction=Faction.SAAR)

        # Initialize and unlock commanders
        initialize_player_leaders(player1)
        initialize_player_leaders(player2)
        initialize_player_leaders(player3)
        player1.leader_sheet.commander.unlock()
        player2.leader_sheet.commander.unlock()

        # Create Alliance notes
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

        game_state = GameState()
        game_state = game_state.add_player(player1)
        game_state = game_state.add_player(player2)
        game_state = game_state.add_player(player3)

        promissory_manager = PromissoryNoteManager()
        alliance_manager = promissory_manager.get_alliance_manager()

        # Give and activate both Alliance notes
        promissory_manager.add_note_to_hand(alliance_note_1to3, "player3")
        promissory_manager.add_note_to_hand(alliance_note_2to3, "player3")

        promissory_manager.activate_alliance_note(alliance_note_1to3, game_state)
        promissory_manager.activate_alliance_note(alliance_note_2to3, game_state)

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
        promissory_manager.return_note_after_use(
            alliance_note_1to3, "player3", game_state
        )

        # Player3 should still have access to player2's commander but not player1's
        can_use_player1_after = alliance_manager.can_use_shared_commander(
            "player3", "player1", game_state
        )
        can_use_player2_after = alliance_manager.can_use_shared_commander(
            "player3", "player2", game_state
        )

        assert can_use_player1_after is False
        assert can_use_player2_after is True

    def test_alliance_note_reuse_after_return(self) -> None:
        """Test that Alliance notes can be reused after being returned.

        Requirements: 6.1, 6.3
        """
        # Create players
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)
        player3 = Player(id="player3", faction=Faction.SAAR)

        # Initialize leaders
        initialize_player_leaders(player1)
        initialize_player_leaders(player2)
        initialize_player_leaders(player3)
        player1.leader_sheet.commander.unlock()

        alliance_note = PromissoryNote(
            note_type=PromissoryNoteType.ALLIANCE,
            issuing_player="player1",
            receiving_player="player2",
        )

        game_state = GameState()
        game_state = game_state.add_player(player1)
        game_state = game_state.add_player(player2)
        game_state = game_state.add_player(player3)

        promissory_manager = PromissoryNoteManager()
        alliance_manager = promissory_manager.get_alliance_manager()

        # First use: player2 gets and uses Alliance note
        promissory_manager.add_note_to_hand(alliance_note, "player2")
        promissory_manager.activate_alliance_note(alliance_note, game_state)

        # Verify player2 has access
        can_use_player2 = alliance_manager.can_use_shared_commander(
            "player2", "player1", game_state
        )
        assert can_use_player2 is True

        # Return the note
        promissory_manager.return_note_after_use(alliance_note, "player2", game_state)

        # Verify access is revoked
        can_use_player2_after = alliance_manager.can_use_shared_commander(
            "player2", "player1", game_state
        )
        assert can_use_player2_after is False

        # Second use: player3 gets the same Alliance note
        # Update the receiving player for reuse
        reused_alliance_note = PromissoryNote(
            note_type=PromissoryNoteType.ALLIANCE,
            issuing_player="player1",
            receiving_player="player3",
        )

        promissory_manager.add_note_to_hand(reused_alliance_note, "player3")
        promissory_manager.activate_alliance_note(reused_alliance_note, game_state)

        # Verify player3 has access but player2 still doesn't
        can_use_player3 = alliance_manager.can_use_shared_commander(
            "player3", "player1", game_state
        )
        can_use_player2_final = alliance_manager.can_use_shared_commander(
            "player2", "player1", game_state
        )

        assert can_use_player3 is True
        assert can_use_player2_final is False

    def test_player_elimination_revokes_all_alliance_access(self) -> None:
        """Test that player elimination properly revokes all Alliance-based commander access.

        Requirements: 6.3
        """
        # Create players
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)
        player3 = Player(id="player3", faction=Faction.SAAR)

        # Initialize leaders
        initialize_player_leaders(player1)
        initialize_player_leaders(player2)
        initialize_player_leaders(player3)
        player1.leader_sheet.commander.unlock()

        # Create Alliance notes
        alliance_note_1to2 = PromissoryNote(
            note_type=PromissoryNoteType.ALLIANCE,
            issuing_player="player1",
            receiving_player="player2",
        )
        alliance_note_1to3 = PromissoryNote(
            note_type=PromissoryNoteType.ALLIANCE,
            issuing_player="player1",
            receiving_player="player3",
        )

        game_state = GameState()
        game_state = game_state.add_player(player1)
        game_state = game_state.add_player(player2)
        game_state = game_state.add_player(player3)

        promissory_manager = PromissoryNoteManager()
        alliance_manager = promissory_manager.get_alliance_manager()

        # Activate both Alliance notes
        promissory_manager.add_note_to_hand(alliance_note_1to2, "player2")
        promissory_manager.add_note_to_hand(alliance_note_1to3, "player3")
        promissory_manager.activate_alliance_note(alliance_note_1to2, game_state)
        promissory_manager.activate_alliance_note(alliance_note_1to3, game_state)

        # Verify both players have access
        can_use_player2 = alliance_manager.can_use_shared_commander(
            "player2", "player1", game_state
        )
        can_use_player3 = alliance_manager.can_use_shared_commander(
            "player3", "player1", game_state
        )

        assert can_use_player2 is True
        assert can_use_player3 is True

        # Eliminate player1 (the commander owner)
        promissory_manager.handle_player_elimination("player1")

        # Both players should lose access to player1's commander
        can_use_player2_after = alliance_manager.can_use_shared_commander(
            "player2", "player1", game_state
        )
        can_use_player3_after = alliance_manager.can_use_shared_commander(
            "player3", "player1", game_state
        )

        assert can_use_player2_after is False
        assert can_use_player3_after is False


class TestAlliancePromissoryNoteIntegrationValidation:
    """Test validation for Alliance promissory note integration."""

    def test_cannot_activate_alliance_note_for_locked_commander(self) -> None:
        """Test that Alliance notes cannot be activated if commander is locked.

        Requirements: 6.5
        """
        # Create players
        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)

        # Initialize leaders but keep commander locked
        initialize_player_leaders(player1)
        initialize_player_leaders(player2)

        # Verify commander is locked
        assert player1.leader_sheet.commander.lock_status.name == "LOCKED"

        alliance_note = PromissoryNote(
            note_type=PromissoryNoteType.ALLIANCE,
            issuing_player="player1",
            receiving_player="player2",
        )

        game_state = GameState()
        game_state = game_state.add_player(player1)
        game_state = game_state.add_player(player2)

        promissory_manager = PromissoryNoteManager()

        # Give Alliance note to player2
        promissory_manager.add_note_to_hand(alliance_note, "player2")

        # Attempting to activate should fail or have no effect
        with pytest.raises(ValueError, match="Commander must be unlocked"):
            promissory_manager.activate_alliance_note(alliance_note, game_state)

    def test_cannot_activate_invalid_alliance_note(self) -> None:
        """Test that invalid Alliance notes cannot be activated."""
        game_state = GameState()
        promissory_manager = PromissoryNoteManager()

        # Try to activate non-Alliance note
        non_alliance_note = PromissoryNote(
            note_type=PromissoryNoteType.CEASEFIRE,
            issuing_player="player1",
            receiving_player="player2",
        )

        with pytest.raises(ValueError, match="Only Alliance promissory notes"):
            promissory_manager.activate_alliance_note(non_alliance_note, game_state)

    def test_cannot_activate_alliance_note_without_receiving_player(self) -> None:
        """Test that Alliance notes without receiving player cannot be activated."""
        game_state = GameState()
        promissory_manager = PromissoryNoteManager()

        # Alliance note without receiving player
        invalid_note = PromissoryNote(
            note_type=PromissoryNoteType.ALLIANCE,
            issuing_player="player1",
            receiving_player=None,
        )

        with pytest.raises(
            ValueError, match="Alliance note must have a receiving player"
        ):
            promissory_manager.activate_alliance_note(invalid_note, game_state)

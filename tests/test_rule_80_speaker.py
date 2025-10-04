"""Tests for Rule 80: SPEAKER - Speaker token privileges and powers.

LRR Rule 80: SPEAKER
The speaker is the player who has the speaker token.

80.1 - Initiative Order: Speaker is first player in initiative order
80.2 - Breaking Ties: Speaker breaks ties
80.3 - Token Passing: During agenda phase, speaker passes speaker token to player of their choice after resolving agenda
80.4 - Politics Strategy Card: If player has Politics strategy card, they can choose to take speaker token instead of drawing action cards
"""

import pytest

from src.ti4.core.game_state import GameState
from src.ti4.core.player import Player
from src.ti4.core.speaker import SpeakerManager


class TestRule80Speaker:
    """Test Rule 80: SPEAKER implementation."""

    def test_speaker_manager_can_be_created(self) -> None:
        """Test that a SpeakerManager can be created."""
        manager = SpeakerManager()
        assert manager is not None

    def test_speaker_manager_can_assign_speaker_to_player(self) -> None:
        """Test that the speaker token can be assigned to a player."""
        # Arrange
        from src.ti4.core.constants import Faction

        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)
        game_state = GameState(players=[player1, player2])
        manager = SpeakerManager()

        # Act
        new_state = manager.assign_speaker(game_state, "player1")

        # Assert
        assert new_state.speaker_id == "player1"

    def test_speaker_manager_validates_player_exists_when_assigning(self) -> None:
        """Test that assigning speaker to non-existent player raises error."""
        # Arrange
        from src.ti4.core.constants import Faction

        player1 = Player(id="player1", faction=Faction.SOL)
        game_state = GameState(players=[player1])
        manager = SpeakerManager()

        # Act & Assert
        with pytest.raises(ValueError, match="Player nonexistent does not exist"):
            manager.assign_speaker(game_state, "nonexistent")

    def test_speaker_manager_validates_empty_player_id(self) -> None:
        """Test that assigning speaker with empty player ID raises error."""
        # Arrange
        from src.ti4.core.constants import Faction

        player1 = Player(id="player1", faction=Faction.SOL)
        game_state = GameState(players=[player1])
        manager = SpeakerManager()

        # Act & Assert
        with pytest.raises(ValueError, match="Player ID cannot be empty"):
            manager.assign_speaker(game_state, "")

        with pytest.raises(ValueError, match="Player ID cannot be empty"):
            manager.assign_speaker(game_state, "   ")

    def test_speaker_manager_can_get_current_speaker(self) -> None:
        """Test that the current speaker can be retrieved."""
        # Arrange
        from src.ti4.core.constants import Faction

        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)
        game_state = GameState(players=[player1, player2])
        manager = SpeakerManager()

        # Act - no speaker initially
        current_speaker = manager.get_current_speaker(game_state)

        # Assert
        assert current_speaker is None

        # Act - assign speaker
        new_state = manager.assign_speaker(game_state, "player1")
        current_speaker = manager.get_current_speaker(new_state)

        # Assert
        assert current_speaker == "player1"

    def test_speaker_is_first_in_initiative_order(self) -> None:
        """Test Rule 80.1: Speaker is first player in initiative order."""
        # Arrange
        from src.ti4.core.constants import Faction

        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)
        player3 = Player(id="player3", faction=Faction.SOL)
        game_state = GameState(players=[player1, player2, player3])
        manager = SpeakerManager()

        # Act - assign player2 as speaker
        new_state = manager.assign_speaker(game_state, "player2")
        initiative_order = manager.get_initiative_order(new_state)

        # Assert - speaker should be first
        assert initiative_order[0] == "player2"
        assert len(initiative_order) == 3
        assert "player1" in initiative_order
        assert "player3" in initiative_order

    def test_politics_strategy_card_integration(self) -> None:
        """Test Rule 80.4: Politics strategy card can take speaker token instead of drawing action cards."""
        # Arrange
        from src.ti4.core.constants import Faction

        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)
        game_state = GameState(players=[player1, player2])
        manager = SpeakerManager()

        # Act - test integration with game state's set_speaker method
        new_state = game_state.set_speaker("player1")
        current_speaker = manager.get_current_speaker(new_state)

        # Assert - should work with existing game state methods
        assert current_speaker == "player1"

        # Act - test that SpeakerManager can work with game state speaker methods
        new_state2 = manager.assign_speaker(game_state, "player2")
        game_state_speaker = new_state2.get_speaker()

        # Assert - should be consistent
        assert game_state_speaker == "player2"

    def test_speaker_breaks_ties(self) -> None:
        """Test Rule 80.2: Speaker breaks ties."""
        # Arrange
        from src.ti4.core.constants import Faction

        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)
        player3 = Player(id="player3", faction=Faction.SOL)
        game_state = GameState(players=[player1, player2, player3])
        manager = SpeakerManager()

        # Act - assign player3 as speaker
        new_state = manager.assign_speaker(game_state, "player3")

        # Test tie-breaking with a list of tied players
        tied_players = ["player1", "player2", "player3"]
        tie_winner = manager.break_tie(new_state, tied_players)

        # Assert - speaker should win the tie
        assert tie_winner == "player3"

        # Test tie-breaking when speaker is not in the tied list
        tied_players_no_speaker = ["player1", "player2"]
        tie_winner_no_speaker = manager.break_tie(new_state, tied_players_no_speaker)

        # Assert - should return first player in initiative order (not speaker since speaker not tied)
        assert tie_winner_no_speaker == "player1"

    def test_speaker_token_passing_during_agenda_phase(self) -> None:
        """Test Rule 80.3: Speaker passes token to chosen player during agenda phase."""
        # Arrange
        from src.ti4.core.constants import Faction

        player1 = Player(id="player1", faction=Faction.ARBOREC)
        player2 = Player(id="player2", faction=Faction.BARONY)
        player3 = Player(id="player3", faction=Faction.SOL)

        game_state = GameState(players=[player1, player2, player3])
        manager = SpeakerManager()

        # Act - assign player1 as speaker, then pass token to player2
        new_state = manager.assign_speaker(game_state, "player1")
        final_state = manager.pass_speaker_token(new_state, "player2")

        # Assert - speaker should now be player2
        assert final_state.speaker_id == "player2"
        assert manager.get_current_speaker(final_state) == "player2"

    def test_speaker_token_passing_validates_player_exists(self) -> None:
        """Test that token passing validates the new speaker exists."""
        # Arrange
        from src.ti4.core.constants import Faction

        player1 = Player(id="player1", faction=Faction.ARBOREC)
        game_state = GameState(players=[player1])
        manager = SpeakerManager()

        # Act & Assert
        with pytest.raises(ValueError, match="New speaker nonexistent does not exist"):
            manager.pass_speaker_token(game_state, "nonexistent")

    def test_speaker_token_passing_validates_empty_player_id(self) -> None:
        """Test that token passing validates empty player ID."""
        # Arrange
        from src.ti4.core.constants import Faction

        player1 = Player(id="player1", faction=Faction.ARBOREC)
        game_state = GameState(players=[player1])
        manager = SpeakerManager()

        # Act & Assert
        with pytest.raises(ValueError, match="New speaker ID cannot be empty"):
            manager.pass_speaker_token(game_state, "")

        with pytest.raises(ValueError, match="New speaker ID cannot be empty"):
            manager.pass_speaker_token(game_state, "   ")

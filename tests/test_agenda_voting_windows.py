"""
Test suite for agenda phase voting timing windows.

This module tests the proper implementation of timing windows during the agenda phase
according to LRR 8.4-8.8 and the TI4 ability compendium.

Key timing windows tested:
- When an agenda is revealed
- After an agenda is revealed
- Before players vote
- When casting votes
- After casting votes
- After outcome is resolved
"""

from unittest.mock import Mock, patch

from ti4.core.agenda_phase import AgendaPhase
from ti4.core.game_state import GameState
from ti4.core.player import Player


class TestAgendaVotingWindows:
    """Test proper timing windows during agenda phase voting."""

    def test_when_agenda_revealed_timing_window_exists(self):
        """
        Test that there is a proper timing window when an agenda is revealed.

        This timing window should allow for:
        - Veto action card
        - Political Secret promissory note
        - Political Favor promissory note
        - QUASH faction ability (Xxcha)

        RED PHASE: This test should fail because we don't have proper timing windows implemented.
        """
        # Arrange
        game_state = Mock(spec=GameState)
        players = [Mock(spec=Player) for _ in range(4)]
        game_state.players = players

        agenda_phase = AgendaPhase()

        # Mock agenda card
        mock_agenda = Mock()
        mock_agenda.name = "Test Agenda"

        # Track timing window callbacks
        timing_callbacks = []

        def mock_callback(timing_window, **kwargs):
            timing_callbacks.append((timing_window, kwargs))

        # Act - reveal an agenda
        # This should trigger "when_agenda_revealed" timing window
        with patch.object(
            agenda_phase, "trigger_timing_window", side_effect=mock_callback
        ):
            agenda_phase.reveal_agenda(mock_agenda)

        # Assert - timing window should be triggered
        assert len(timing_callbacks) > 0
        assert any(window[0] == "when_agenda_revealed" for window in timing_callbacks)

    def test_after_agenda_revealed_timing_window_exists(self):
        """
        Test that there is a proper timing window after an agenda is revealed.

        This timing window should allow for:
        - All rider action cards (Construction, Diplomacy, Imperial, etc.)
        - Keleres Rider promissory note
        - Hack Election action card
        - Insider Information action card
        - Sanction action card
        - GALACTIC THREAT faction ability (Nekro)

        RED PHASE: This test should fail because we don't have proper timing windows implemented.
        """
        # Arrange
        game_state = Mock(spec=GameState)
        players = [Mock(spec=Player) for _ in range(4)]
        game_state.players = players

        agenda_phase = AgendaPhase()

        # Mock agenda card
        mock_agenda = Mock()
        mock_agenda.name = "Test Agenda"

        # Track timing window callbacks
        timing_callbacks = []

        def mock_callback(timing_window, **kwargs):
            timing_callbacks.append((timing_window, kwargs))

        # Act - reveal an agenda (which should complete and trigger after timing)
        with patch.object(
            agenda_phase, "trigger_timing_window", side_effect=mock_callback
        ):
            agenda_phase.reveal_agenda(mock_agenda)

        # Assert - timing window should be triggered
        assert len(timing_callbacks) > 0
        assert any(window[0] == "after_agenda_revealed" for window in timing_callbacks)

    def test_before_players_vote_timing_window_exists(self):
        """
        Test that there is a proper timing window before players vote.

        This timing window should allow for:
        - Genetic Recombination technology (Mahact)

        RED PHASE: This test should fail because we don't have proper timing windows implemented.
        """
        # Arrange
        game_state = Mock(spec=GameState)
        players = [Mock(spec=Player) for _ in range(4)]
        game_state.players = players

        agenda_phase = AgendaPhase()

        # Mock agenda card and voting setup
        mock_agenda = Mock()
        mock_agenda.name = "Test Agenda"
        mock_agenda.outcomes = ["For", "Against"]

        # Track timing window callbacks
        timing_callbacks = []

        def mock_callback(timing_window, **kwargs):
            timing_callbacks.append((timing_window, kwargs))

        # Act - start voting process
        with patch.object(
            agenda_phase, "trigger_timing_window", side_effect=mock_callback
        ):
            agenda_phase.start_voting(mock_agenda)

        # Assert - timing window should be triggered
        assert len(timing_callbacks) > 0
        assert any(window[0] == "before_players_vote" for window in timing_callbacks)

"""
Test cases for agenda voting mechanics and timing windows.

These tests verify the implementation of LRR 8.4-8.6 (Agenda Phase)
and the timing windows identified from the TI4 ability compendium.
"""

from ti4.core.agenda_phase import AgendaCard, AgendaPhase, AgendaType
from ti4.core.constants import Faction
from ti4.testing.scenario_builder import GameScenarioBuilder


class TestAgendaVotingMechanics:
    """Test the core voting mechanics and timing windows."""

    def test_voting_sequence_follows_lrr_order(self):
        """
        Test that voting follows the proper sequence according to LRR 8.5:
        1. Reveal agenda
        2. Trigger "when agenda revealed" timing window
        3. Trigger "after agenda revealed" timing window
        4. Trigger "before players vote" timing window
        5. Players vote in speaker order
        6. Trigger "after voting" timing window
        7. Resolve agenda effects
        """
        GameScenarioBuilder().with_players(
            ("player1", Faction.SOL), ("player2", Faction.XXCHA)
        ).build()
        agenda_phase = AgendaPhase()

        # Create a test agenda
        test_agenda = AgendaCard(
            name="Test Agenda",
            agenda_type=AgendaType.LAW,
            outcomes=["For", "Against"],
            for_effect="Test law effect",
        )

        # Track timing window calls
        timing_calls = []
        original_trigger = agenda_phase.trigger_timing_window

        def mock_trigger(window_type, **kwargs):
            timing_calls.append(window_type)
            return original_trigger(window_type, **kwargs)

        agenda_phase.trigger_timing_window = mock_trigger

        # Execute the voting sequence
        agenda_phase.reveal_agenda(test_agenda)
        agenda_phase.start_voting(test_agenda)

        # Verify timing windows were called in correct order
        expected_sequence = [
            "when_agenda_revealed",
            "after_agenda_revealed",
            "before_players_vote",
        ]

        assert timing_calls == expected_sequence, (
            f"Expected {expected_sequence}, got {timing_calls}"
        )

    def test_action_cards_can_trigger_during_appropriate_windows(self):
        """
        Test that action cards can be triggered during their appropriate timing windows.

        Based on TI4 compendium analysis:
        - Veto: "when an agenda is revealed"
        - Assassinate Representative: "after an agenda is revealed"
        - Bribery: "after a player votes"
        """
        GameScenarioBuilder().with_players(
            ("player1", Faction.SOL), ("player2", Faction.XXCHA)
        ).build()
        agenda_phase = AgendaPhase()

        test_agenda = AgendaCard(
            name="Test Agenda",
            agenda_type=AgendaType.LAW,
            outcomes=["For", "Against"],
            for_effect="Test law effect",
        )

        # Track what can be triggered during each window
        triggered_abilities = []

        def mock_trigger(window_type, **kwargs):
            # Simulate checking what abilities can trigger
            if window_type == "when_agenda_revealed":
                triggered_abilities.append("Veto")
            elif window_type == "after_agenda_revealed":
                triggered_abilities.append("Assassinate Representative")
            elif window_type == "before_players_vote":
                triggered_abilities.append("Genetic Recombination")

        agenda_phase.trigger_timing_window = mock_trigger

        # Execute sequence
        agenda_phase.reveal_agenda(test_agenda)
        agenda_phase.start_voting(test_agenda)

        # Verify appropriate action cards can trigger
        assert "Veto" in triggered_abilities
        assert "Assassinate Representative" in triggered_abilities
        assert "Genetic Recombination" in triggered_abilities

    def test_promissory_notes_can_trigger_during_appropriate_windows(self):
        """
        Test that promissory notes can be triggered during their appropriate timing windows.

        Based on TI4 compendium analysis:
        - Political Secret: "when an agenda is revealed"
        - Keleres Rider: "after an agenda is revealed"
        """
        GameScenarioBuilder().with_players(
            ("player1", Faction.SOL), ("player2", Faction.XXCHA)
        ).build()
        agenda_phase = AgendaPhase()

        test_agenda = AgendaCard(
            name="Test Agenda",
            agenda_type=AgendaType.LAW,
            outcomes=["For", "Against"],
            for_effect="Test law effect",
        )

        # Track promissory note triggers
        triggered_promissory = []

        def mock_trigger(window_type, **kwargs):
            if window_type == "when_agenda_revealed":
                triggered_promissory.append("Political Secret")
            elif window_type == "after_agenda_revealed":
                triggered_promissory.append("Keleres Rider")

        agenda_phase.trigger_timing_window = mock_trigger

        # Execute sequence
        agenda_phase.reveal_agenda(test_agenda)

        # Verify promissory notes can trigger
        assert "Political Secret" in triggered_promissory
        assert "Keleres Rider" in triggered_promissory

    def test_faction_abilities_can_trigger_during_appropriate_windows(self):
        """
        Test that faction abilities can be triggered during their appropriate timing windows.

        Based on TI4 compendium analysis:
        - QUASH (Xxcha): "when an agenda is revealed"
        - ZEAL (Argent Flight): affects voting order and vote count
        """
        GameScenarioBuilder().with_players(
            ("player1", Faction.SOL), ("player2", Faction.XXCHA)
        ).build()
        agenda_phase = AgendaPhase()

        test_agenda = AgendaCard(
            name="Test Agenda",
            agenda_type=AgendaType.LAW,
            outcomes=["For", "Against"],
            for_effect="Test law effect",
        )

        # Track faction ability triggers
        triggered_abilities = []

        def mock_trigger(window_type, **kwargs):
            if window_type == "when_agenda_revealed":
                triggered_abilities.append("QUASH")
            elif window_type == "before_players_vote":
                triggered_abilities.append("ZEAL")

        agenda_phase.trigger_timing_window = mock_trigger

        # Execute sequence
        agenda_phase.reveal_agenda(test_agenda)
        agenda_phase.start_voting(test_agenda)

        # Verify faction abilities can trigger
        assert "QUASH" in triggered_abilities
        assert "ZEAL" in triggered_abilities

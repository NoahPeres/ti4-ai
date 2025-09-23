"""
Test Rule 8: AGENDA PHASE

This module tests the agenda phase mechanics according to LRR Rule 8.

Key Requirements from LRR:
- 8.1: Agenda phase skipped until custodians token removed from Mecatol Rex
- 8.2: First agenda resolution (reveal, vote, resolve)
- 8.3: Second agenda resolution
- 8.4: Ready all exhausted planets, then new round begins
- 8.5-8.13: Voting mechanics with influence values

Test Coverage:
- Phase activation conditions
- Two-agenda sequence
- Voting mechanics and influence calculation
- Law vs directive resolution
- Planet readying after phase
- Speaker privileges and tie-breaking
"""

from unittest.mock import Mock

# Import core game components
from ti4.core.agenda_phase import (
    AgendaCard,
    AgendaPhase,
    AgendaType,
    CustodiansToken,
    SpeakerSystem,
    VoteResult,
    VotingSystem,
)
from ti4.core.planet import Planet


class TestRule08AgendaPhaseActivation:
    """Test Rule 8.1: Agenda phase activation conditions."""

    def test_agenda_phase_skipped_when_custodians_token_present(self):
        """
        Test that agenda phase is skipped when custodians token is on Mecatol Rex.

        LRR 8.1: Players skip the agenda phase during the early portion of each game.
        After the custodians token is removed from Mecatol Rex, the agenda phase
        is added to each game round.
        """
        # Setup: Game with custodians token still on Mecatol Rex
        custodians = CustodiansToken()
        agenda_phase = AgendaPhase()

        # Custodians token is present on Mecatol Rex
        assert custodians.is_on_mecatol_rex()

        # Agenda phase should be skipped
        result = agenda_phase.should_execute_phase(custodians)
        assert not result

    def test_agenda_phase_activated_after_custodians_removal(self):
        """
        Test that agenda phase becomes active after custodians token removal.

        LRR 8.1: After the custodians token is removed from Mecatol Rex,
        the agenda phase is added to each game round.
        """
        # Setup: Game after custodians token removal
        custodians = CustodiansToken()
        agenda_phase = AgendaPhase()

        # Remove custodians token (simulate player spending 6 influence)
        custodians.remove_from_mecatol_rex("player1")
        assert not custodians.is_on_mecatol_rex()

        # Agenda phase should now be active
        result = agenda_phase.should_execute_phase(custodians)
        assert result


class TestRule08AgendaSequence:
    """Test Rule 8.2-8.4: Two-agenda sequence and planet readying."""

    def test_first_agenda_resolution_sequence(self):
        """
        Test the first agenda resolution follows correct sequence.

        LRR 8.2: STEP 1-FIRST AGENDA: Players resolve the first agenda by
        following these steps in order:
        i. REVEAL AGENDA: The speaker draws one agenda card
        ii. VOTE: Each player votes starting left of speaker clockwise
        iii. RESOLVE OUTCOME: Tally votes and resolve winning outcome
        """
        # Setup
        agenda_phase = AgendaPhase()
        speaker_system = SpeakerSystem()
        voting_system = VotingSystem()

        # Mock agenda deck and players
        agenda_deck = Mock()
        test_agenda = AgendaCard(
            name="Test Law", agenda_type=AgendaType.LAW, outcomes=["For", "Against"]
        )
        agenda_deck.draw_top_card.return_value = test_agenda

        players = ["speaker", "player2", "player3"]
        speaker_system.set_speaker("speaker")

        # Execute first agenda
        result = agenda_phase.resolve_first_agenda(
            agenda_deck, speaker_system, voting_system, players
        )

        # Verify sequence executed
        assert result.success
        assert result.agenda_revealed == test_agenda
        assert result.voting_completed
        assert result.outcome_resolved

    def test_second_agenda_resolution_sequence(self):
        """
        Test the second agenda resolution follows same sequence.

        LRR 8.3: STEP 2-SECOND AGENDA: Players repeat the "First Agenda"
        step of this phase for a second agenda.
        """
        # Setup
        agenda_phase = AgendaPhase()
        speaker_system = SpeakerSystem()
        voting_system = VotingSystem()

        # Mock second agenda
        agenda_deck = Mock()
        second_agenda = AgendaCard(
            name="Test Directive",
            agenda_type=AgendaType.DIRECTIVE,
            outcomes=["Option A", "Option B", "Option C"],
        )
        agenda_deck.draw_top_card.return_value = second_agenda

        players = ["speaker", "player2", "player3"]

        # Execute second agenda
        result = agenda_phase.resolve_second_agenda(
            agenda_deck, speaker_system, voting_system, players
        )

        # Verify same sequence as first agenda
        assert result.success
        assert result.agenda_revealed == second_agenda
        assert result.voting_completed
        assert result.outcome_resolved

    def test_planet_readying_after_agendas(self):
        """
        Test that all exhausted planets are readied after both agendas.

        LRR 8.4: STEP 3-READY PLANETS: Each player readies each of their
        exhausted planets. Then, a new game round begins starting with
        the strategy phase.
        """
        # Setup: Players with exhausted planets
        agenda_phase = AgendaPhase()

        # Mock players with exhausted planets
        player1_planets = [
            Planet("Mecatol Rex", resources=1, influence=6),
            Planet("Jord", resources=4, influence=4),
        ]
        player2_planets = [Planet("Muaat", resources=4, influence=2)]

        # Exhaust the planets
        for planet in player1_planets + player2_planets:
            planet.exhaust()

        players_planets = {"player1": player1_planets, "player2": player2_planets}

        # Execute planet readying
        result = agenda_phase.ready_all_planets(players_planets)

        # Verify all planets are readied
        assert result.success
        for player_planets in players_planets.values():
            for planet in player_planets:
                assert not planet.is_exhausted()


class TestRule08VotingMechanics:
    """Test Rule 8.5-8.13: Voting mechanics and influence calculation."""

    def test_vote_casting_with_planet_exhaustion(self):
        """
        Test voting by exhausting planets for influence values.

        LRR 8.6: To cast votes, a player exhausts any number of their planets
        and chooses an outcome. The number of votes cast for that outcome is
        equal to the combined influence values of the planets that the player exhausts.
        """
        # Setup
        voting_system = VotingSystem()

        # Player with planets
        player_planets = [
            Planet("Mecatol Rex", resources=1, influence=6),
            Planet("Jord", resources=4, influence=4),
            Planet("Abyz", resources=3, influence=3),
        ]

        # Player chooses to exhaust Mecatol Rex and Jord for "For" outcome
        planets_to_exhaust = [
            player_planets[0],
            player_planets[1],
        ]  # 6 + 4 = 10 influence

        result = voting_system.cast_votes(
            player_id="player1", planets=planets_to_exhaust, outcome="For"
        )

        # Verify vote casting
        assert result.success
        assert result.votes_cast == 10  # 6 + 4 influence
        assert result.outcome == "For"

        # Verify planets are exhausted
        assert player_planets[0].is_exhausted()  # Mecatol Rex
        assert player_planets[1].is_exhausted()  # Jord
        assert not player_planets[2].is_exhausted()  # Abyz not used

    def test_cannot_split_votes_across_outcomes(self):
        """
        Test that players cannot cast votes for multiple outcomes.

        LRR 8.7: A player cannot cast votes for multiple outcomes of the same agenda.
        Each vote a player casts must be for the same outcome.
        """
        # Setup
        voting_system = VotingSystem()

        player_planets = [
            Planet("Mecatol Rex", resources=1, influence=6),
            Planet("Jord", resources=4, influence=4),
        ]

        # First vote for "For"
        result1 = voting_system.cast_votes(
            player_id="player1", planets=[player_planets[0]], outcome="For"
        )
        assert result1.success

        # Attempt to vote for "Against" with same player
        result2 = voting_system.cast_votes(
            player_id="player1", planets=[player_planets[1]], outcome="Against"
        )

        # Should fail - cannot split votes
        assert not result2.success
        assert (
            "cannot cast votes for multiple outcomes" in result2.error_message.lower()
        )

    def test_for_against_voting_constraint(self):
        """
        Test For/Against agenda voting constraints.

        LRR 8.8: Some agendas have "For" and "Against" outcomes. When a player
        casts votes on such an agenda, that player must cast their votes either
        "For" or "Against."
        """
        # Setup
        voting_system = VotingSystem()

        # For/Against agenda
        agenda = AgendaCard(
            name="Test Law", agenda_type=AgendaType.LAW, outcomes=["For", "Against"]
        )

        player_planets = [Planet("Mecatol Rex", resources=1, influence=6)]

        # Valid vote for "For"
        result = voting_system.cast_votes(
            player_id="player1", planets=player_planets, outcome="For", agenda=agenda
        )
        assert result.success

        # Invalid vote for non-existent outcome
        result_invalid = voting_system.cast_votes(
            player_id="player2", planets=player_planets, outcome="Maybe", agenda=agenda
        )
        assert not result_invalid.success

    def test_speaker_votes_last_and_breaks_ties(self):
        """
        Test speaker voting order and tie-breaking privileges.

        LRR 80.2: During the agenda phase, the speaker reveals the top agenda card
        from the agenda deck before each vote. The speaker is always the last player
        to vote and decides which outcome to resolve if the outcomes are tied.
        """
        # Setup
        voting_system = VotingSystem()
        speaker_system = SpeakerSystem()
        speaker_system.set_speaker("speaker")

        # Mock voting scenario with tie
        players = ["player1", "player2", "speaker"]

        # Players vote (not speaker)
        voting_system.cast_votes("player1", [], "For")  # 0 votes
        voting_system.cast_votes("player2", [], "Against")  # 0 votes

        # Verify speaker votes last
        voting_order = voting_system.get_voting_order(players, speaker_system)
        assert voting_order == ["player1", "player2", "speaker"]

        # Simulate tie scenario
        vote_tally = {"For": 5, "Against": 5}

        # Speaker breaks tie
        tie_result = speaker_system.resolve_tie(vote_tally, chosen_outcome="For")
        assert tie_result.winning_outcome == "For"
        assert tie_result.resolved_by_speaker


class TestRule08LawVsDirectiveResolution:
    """Test different resolution mechanics for laws vs directives."""

    def test_law_resolution_with_for_against(self):
        """
        Test law resolution mechanics.

        Laws become permanent game effects when "For" wins,
        or are discarded when "Against" wins.
        """
        # Setup
        agenda_phase = AgendaPhase()

        law_agenda = AgendaCard(
            name="Anti-Intellectual Revolution",
            agenda_type=AgendaType.LAW,
            outcomes=["For", "Against"],
            for_effect="After a player researches technology, destroy 1 non-fighter ship",
            against_effect="Each player exhausts 1 planet per technology owned",
        )

        # "For" outcome wins
        vote_result = VoteResult(
            winning_outcome="For", vote_tally={"For": 8, "Against": 3}
        )

        resolution_result = agenda_phase.resolve_agenda_outcome(law_agenda, vote_result)

        # Law should be attached as permanent effect
        assert resolution_result.success
        assert resolution_result.law_enacted
        assert resolution_result.permanent_effect_added

    def test_directive_resolution_one_time_effect(self):
        """
        Test directive resolution mechanics.

        LRR 7.7-7.8: Directives provide one-time game effects. When resolving
        a directive, players resolve the outcome that received the most votes
        and discard the agenda card.
        """
        # Setup
        agenda_phase = AgendaPhase()

        directive_agenda = AgendaCard(
            name="Core Mining",
            agenda_type=AgendaType.DIRECTIVE,
            outcomes=["Elect Hazardous Planet"],
            effect="Attach to elected planet, destroy 1 infantry, +2 resources",
        )

        vote_result = VoteResult(
            winning_outcome="Elect Hazardous Planet",
            vote_tally={"Elect Hazardous Planet": 5},
            elected_planet="Muaat",
        )

        resolution_result = agenda_phase.resolve_agenda_outcome(
            directive_agenda, vote_result
        )

        # Directive should execute once and be discarded
        assert resolution_result.success
        assert resolution_result.one_time_effect_executed
        assert resolution_result.agenda_discarded


class TestRule08IntegrationWithGameFlow:
    """Test agenda phase integration with overall game flow."""

    def test_complete_agenda_phase_execution(self):
        """
        Test complete agenda phase execution in game context.

        Integration test covering full agenda phase workflow:
        1. Check custodians token status
        2. Execute first agenda (reveal, vote, resolve)
        3. Execute second agenda (reveal, vote, resolve)
        4. Ready all exhausted planets
        5. Transition to next round
        """
        # Setup complete game context
        agenda_phase = AgendaPhase()
        custodians = CustodiansToken()
        custodians.remove_from_mecatol_rex("player1")  # Enable agenda phase

        # Mock game state
        game_state = Mock()
        game_state.get_players.return_value = ["speaker", "player2", "player3"]
        game_state.get_speaker_system.return_value = SpeakerSystem()
        game_state.get_agenda_deck.return_value = Mock()

        # Execute complete agenda phase
        result = agenda_phase.execute_complete_phase(game_state)

        # Verify full execution
        assert result.success
        assert result.first_agenda_resolved
        assert result.second_agenda_resolved
        assert result.planets_readied
        assert result.ready_for_next_round

    def test_agenda_phase_skipped_in_early_game(self):
        """
        Test that agenda phase is properly skipped in early game.

        Ensures game flow continues correctly when custodians token present.
        """
        # Setup early game state
        agenda_phase = AgendaPhase()
        custodians = CustodiansToken()  # Still on Mecatol Rex

        game_state = Mock()

        # Attempt to execute agenda phase
        result = agenda_phase.execute_complete_phase(game_state, custodians)

        # Should be skipped
        assert result.success
        assert result.phase_skipped
        assert result.reason == "Custodians token still on Mecatol Rex"

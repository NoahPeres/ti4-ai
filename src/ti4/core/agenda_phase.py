"""
Agenda Phase Implementation for TI4 AI

This module implements Rule 8: AGENDA PHASE mechanics according to the LRR.

Key Components:
- AgendaPhase: Main phase controller
- VotingSystem: Handles voting mechanics and influence calculation
- AgendaCard: Represents agenda cards (laws and directives)
- CustodiansToken: Tracks custodians token state
- SpeakerSystem: Manages speaker privileges and tie-breaking
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class AgendaType(Enum):
    """Types of agenda cards."""

    LAW = "law"
    DIRECTIVE = "directive"


@dataclass
class AgendaCard:
    """Represents an agenda card."""

    name: str
    agenda_type: AgendaType
    outcomes: list[str]
    for_effect: str | None = None
    against_effect: str | None = None
    effect: str | None = None


@dataclass
class VoteResult:
    """Result of voting on an agenda."""

    winning_outcome: str
    vote_tally: dict[str, int]
    elected_planet: str | None = None
    resolved_by_speaker: bool = False
    success: bool = True


@dataclass
class AgendaPhaseResult:
    """Result of agenda phase execution."""

    success: bool
    first_agenda_resolved: bool = False
    second_agenda_resolved: bool = False
    planets_readied: bool = False
    ready_for_next_round: bool = False
    phase_skipped: bool = False
    reason: str | None = None
    agenda_revealed: AgendaCard | None = None
    voting_completed: bool = False
    outcome_resolved: bool = False
    law_enacted: bool = False
    permanent_effect_added: bool = False
    one_time_effect_executed: bool = False
    agenda_discarded: bool = False
    error_message: str | None = None


@dataclass
class VotingOutcome:
    """Result of a voting action."""

    success: bool
    votes_cast: int = 0
    outcome: str | None = None
    error_message: str | None = None


class CustodiansToken:
    """Manages the custodians token state."""

    def __init__(self) -> None:
        self.on_mecatol_rex = True

    def is_on_mecatol_rex(self) -> bool:
        """Check if custodians token is on Mecatol Rex."""
        return self.on_mecatol_rex

    def remove_from_mecatol_rex(self, player_id: str | None = None) -> bool:
        """Remove custodians token from Mecatol Rex."""
        if self.on_mecatol_rex:
            self.on_mecatol_rex = False
            return True
        return False


class SpeakerSystem:
    """Manages speaker privileges and tie-breaking."""

    def __init__(self) -> None:
        self.speaker_id: str | None = None

    def set_speaker(self, player_id: str) -> None:
        """Set the current speaker."""
        self.speaker_id = player_id

    def get_speaker(self) -> str | None:
        """Get the current speaker."""
        return self.speaker_id

    def resolve_tie(
        self, vote_tally: dict[str, int], chosen_outcome: str
    ) -> VoteResult:
        """Resolve a tie by speaker choice."""
        return VoteResult(
            winning_outcome=chosen_outcome,
            vote_tally=vote_tally,
            resolved_by_speaker=True,
        )


class VotingSystem:
    """Handles voting mechanics and influence calculation."""

    def __init__(self) -> None:
        self.player_votes: dict[str, str] = {}  # Track player vote outcomes
        self._vote_tally: dict[str, int] = {}

    def cast_votes(
        self,
        player_id: str,
        planets: list[Any],
        outcome: str,
        agenda: AgendaCard | None = None,
    ) -> VotingOutcome:
        """
        Cast votes using planet influence.

        LRR 8.6: Players cast votes by exhausting planets equal to the influence
        value they wish to spend.
        """
        # Validate agenda outcomes if provided
        if agenda and outcome not in agenda.outcomes:
            return VotingOutcome(
                success=False, error_message=f"Invalid outcome '{outcome}' for agenda"
            )

        # Enforce one vote action per player per agenda (no stacking/splitting)
        if player_id in self.player_votes:
            previous_outcome = self.player_votes[player_id]
            if previous_outcome != outcome:
                return VotingOutcome(
                    success=False,
                    error_message=(
                        f"Player {player_id} cannot cast votes for multiple outcomes "
                        f"(previously voted '{previous_outcome}', now attempting '{outcome}')"
                    ),
                )
            return VotingOutcome(
                success=False,
                error_message=f"Player {player_id} has already voted for this agenda",
            )

        # Validate planets and precompute influence; do not mutate until all checks pass
        seen: set[int] = set()
        total_influence = 0
        to_exhaust: list[Any] = []
        for planet in planets:
            pid = id(planet)
            if pid in seen:
                return VotingOutcome(
                    success=False,
                    error_message="Cannot use duplicate planet in vote list",
                )
            seen.add(pid)

            if not hasattr(planet, "influence") or not hasattr(planet, "exhaust"):
                return VotingOutcome(
                    success=False, error_message="Invalid planet object for voting"
                )

            # Validate ownership
            if hasattr(planet, "controlled_by") and planet.controlled_by != player_id:
                return VotingOutcome(
                    success=False,
                    error_message=f"Player {player_id} does not have ownership of planet {getattr(planet, 'name', '<unknown>')}",
                )

            # Validate spendability
            if (
                hasattr(planet, "can_spend_influence")
                and not planet.can_spend_influence()
            ):
                return VotingOutcome(
                    success=False,
                    error_message=f"Planet {getattr(planet, 'name', '<unknown>')} is already exhausted and cannot be used",
                )

            total_influence += int(getattr(planet, "influence", 0))
            to_exhaust.append(planet)

        # All validations passed; now mutate with rollback on error
        exhausted: list[Any] = []
        try:
            for planet in to_exhaust:
                planet.exhaust()
                exhausted.append(planet)
        except Exception as exc:
            for p in exhausted:
                if hasattr(p, "ready"):
                    p.ready()
            return VotingOutcome(success=False, error_message=str(exc))

        self.player_votes[player_id] = outcome
        self._vote_tally[outcome] = self._vote_tally.get(outcome, 0) + total_influence

        return VotingOutcome(success=True, votes_cast=total_influence, outcome=outcome)

    def get_vote_tally(self) -> dict[str, int]:
        """Get current vote tally for all outcomes."""
        return self._vote_tally.copy()

    def reset_votes(self) -> None:
        """Reset all votes and tally for a new agenda."""
        self.player_votes.clear()
        self._vote_tally.clear()

    def get_voting_order(
        self, players: list[str], speaker_system: SpeakerSystem
    ) -> list[str]:
        """
        Get voting order with speaker voting last.

        LRR 80.2: The speaker is always the last player to vote.
        """
        speaker = speaker_system.get_speaker()
        if speaker and speaker in players:
            other_players = [p for p in players if p != speaker]
            return other_players + [speaker]
        return players


class AgendaPhase:
    """Main agenda phase controller."""

    def __init__(self, game_state: Any | None = None) -> None:
        pass

    def should_execute_phase(self, custodians: CustodiansToken) -> bool:
        """Check if agenda phase should execute."""
        return not custodians.is_on_mecatol_rex()

    def resolve_first_agenda(
        self,
        agenda_deck: Any,
        speaker_system: SpeakerSystem,
        voting_system: VotingSystem,
        players: list[str],
    ) -> AgendaPhaseResult:
        """
        Resolve the first agenda of the phase.

        LRR 8.2: The speaker reveals the top agenda card from the agenda deck.
        """
        # Reset voting system for new agenda
        voting_system.reset_votes()

        # Draw agenda card from deck
        agenda = agenda_deck.draw_top_card()

        # Get voting order (speaker votes last)
        _ = voting_system.get_voting_order(players, speaker_system)

        # Simulate voting process (in real implementation, this would be interactive)
        # For now, we'll just mark as completed with basic vote tally
        vote_tally = voting_system.get_vote_tally()

        # Determine winning outcome from vote tally
        if not vote_tally:
            # No votes cast — treat as a tie of zero and let the speaker decide
            zero_tally = dict.fromkeys(agenda.outcomes or ["For", "Against"], 0)
            chosen = agenda.outcomes[0] if agenda.outcomes else "For"
            vote_result = speaker_system.resolve_tie(zero_tally, chosen)
        else:
            # Find outcome with most votes
            max_votes = max(vote_tally.values())
            tied_outcomes = [
                outcome for outcome, votes in vote_tally.items() if votes == max_votes
            ]

            if len(tied_outcomes) == 1:
                # Clear winner
                winning_outcome = tied_outcomes[0]
                vote_result = VoteResult(
                    winning_outcome=winning_outcome, vote_tally=vote_tally, success=True
                )
            else:
                # Tie - speaker decides (chooses first tied outcome for simulation)
                winning_outcome = tied_outcomes[0]
                vote_result = speaker_system.resolve_tie(vote_tally, winning_outcome)

        # Resolve the agenda outcome
        outcome_result = self.resolve_agenda_outcome(agenda, vote_result)

        return AgendaPhaseResult(
            success=True,
            first_agenda_resolved=True,
            agenda_revealed=agenda,
            voting_completed=True,
            outcome_resolved=outcome_result.outcome_resolved,
            law_enacted=outcome_result.law_enacted,
            permanent_effect_added=outcome_result.permanent_effect_added,
            one_time_effect_executed=outcome_result.one_time_effect_executed,
            agenda_discarded=outcome_result.agenda_discarded,
        )

    def resolve_second_agenda(
        self,
        agenda_deck: Any,
        speaker_system: SpeakerSystem,
        voting_system: VotingSystem,
        players: list[str],
    ) -> AgendaPhaseResult:
        """
        Resolve the second agenda of the phase.

        LRR 8.3: After resolving the first agenda, the speaker reveals
        the top agenda card from the agenda deck.
        """
        # Reset voting system for new agenda
        voting_system.reset_votes()

        # Draw second agenda card from deck
        agenda = agenda_deck.draw_top_card()

        # Get voting order (speaker votes last)
        _ = voting_system.get_voting_order(players, speaker_system)

        # Simulate voting process (in real implementation, this would be interactive)
        # For now, we'll just mark as completed with basic vote tally
        vote_tally = voting_system.get_vote_tally()

        # Determine winning outcome from vote tally
        if not vote_tally:
            # No votes cast — treat as a tie of zero and let the speaker decide
            zero_tally = dict.fromkeys(agenda.outcomes or ["For", "Against"], 0)
            chosen = agenda.outcomes[0] if agenda.outcomes else "For"
            vote_result = speaker_system.resolve_tie(zero_tally, chosen)
        else:
            # Find outcome with most votes
            max_votes = max(vote_tally.values())
            tied_outcomes = [
                outcome for outcome, votes in vote_tally.items() if votes == max_votes
            ]

            if len(tied_outcomes) == 1:
                # Clear winner
                winning_outcome = tied_outcomes[0]
                vote_result = VoteResult(
                    winning_outcome=winning_outcome, vote_tally=vote_tally, success=True
                )
            else:
                # Tie - speaker decides (chooses first tied outcome for simulation)
                winning_outcome = tied_outcomes[0]
                vote_result = speaker_system.resolve_tie(vote_tally, winning_outcome)

        # Resolve the agenda outcome
        outcome_result = self.resolve_agenda_outcome(agenda, vote_result)

        return AgendaPhaseResult(
            success=True,
            second_agenda_resolved=True,
            agenda_revealed=agenda,
            voting_completed=True,
            outcome_resolved=outcome_result.outcome_resolved,
            law_enacted=outcome_result.law_enacted,
            permanent_effect_added=outcome_result.permanent_effect_added,
            one_time_effect_executed=outcome_result.one_time_effect_executed,
            agenda_discarded=outcome_result.agenda_discarded,
        )

    def ready_all_planets(
        self, players_planets: dict[str, list[Any]]
    ) -> AgendaPhaseResult:
        """
        Ready all planets after agenda phase.

        LRR 8.4: After resolving the second agenda, ready all exhausted planets.
        """
        for player_planets in players_planets.values():
            for planet in player_planets:
                if hasattr(planet, "ready"):
                    planet.ready()

        return AgendaPhaseResult(success=True, planets_readied=True)

    def resolve_agenda_outcome(
        self, agenda: AgendaCard, vote_result: VoteResult
    ) -> AgendaPhaseResult:
        """
        Resolve the outcome of an agenda based on voting results.

        LRR 7.7-7.8: Laws become permanent effects when "For" wins,
        directives provide one-time effects.
        """
        if agenda.agenda_type == AgendaType.LAW:
            if vote_result.winning_outcome == "For":
                # Law is enacted as permanent effect
                return AgendaPhaseResult(
                    success=True,
                    law_enacted=True,
                    permanent_effect_added=True,
                    outcome_resolved=True,
                )
            else:
                # Law is discarded (Against or other outcome)
                return AgendaPhaseResult(
                    success=True, agenda_discarded=True, outcome_resolved=True
                )

        elif agenda.agenda_type == AgendaType.DIRECTIVE:
            # Handle different directive outcomes
            if vote_result.winning_outcome == "Elect" or str(
                vote_result.winning_outcome
            ).startswith("Elect"):
                # Elect outcome - choose a player/planet/system
                elected_target = vote_result.elected_planet or "default_target"
                return AgendaPhaseResult(
                    success=True,
                    one_time_effect_executed=True,
                    agenda_discarded=True,
                    outcome_resolved=True,
                    reason=f"Elected: {elected_target}",
                )
            elif vote_result.winning_outcome in ["For", "Against"]:
                # Standard For/Against directive
                effect_applied = vote_result.winning_outcome == "For"
                return AgendaPhaseResult(
                    success=True,
                    one_time_effect_executed=effect_applied,
                    agenda_discarded=True,
                    outcome_resolved=True,
                    reason=f"Directive {vote_result.winning_outcome} - Effect {'applied' if effect_applied else 'not applied'}",
                )
            else:
                # Other directive outcomes (custom outcomes)
                return AgendaPhaseResult(
                    success=True,
                    one_time_effect_executed=True,
                    agenda_discarded=True,
                    outcome_resolved=True,
                    reason=f"Directive outcome: {vote_result.winning_outcome}",
                )

        return AgendaPhaseResult(success=False, error_message="Unknown agenda type")

    def execute_complete_phase(
        self, game_state: Any, custodians: CustodiansToken | None = None
    ) -> AgendaPhaseResult:
        """
        Execute the complete agenda phase sequence.

        LRR 8.1: The agenda phase is executed only if the custodians token
        is not on Mecatol Rex.
        """
        if custodians is None:
            custodians = getattr(game_state, "get_custodians_token", lambda: None)()
        if custodians and custodians.is_on_mecatol_rex():
            return AgendaPhaseResult(
                success=True,
                phase_skipped=True,
                reason="Custodians token still on Mecatol Rex",
            )

        # Initialize systems for agenda phase (prefer game_state wiring, fallback to simple defaults)
        speaker_system = getattr(
            game_state, "get_speaker_system", lambda: SpeakerSystem()
        )()
        voting_system = getattr(
            game_state, "get_voting_system", lambda: VotingSystem()
        )()
        players = getattr(
            game_state, "get_players", lambda: ["player1", "player2", "player3"]
        )()

        class _DefaultAgendaDeck:
            def draw_top_card(self) -> AgendaCard:
                return AgendaCard(
                    name="Mock Agenda",
                    agenda_type=AgendaType.LAW,
                    outcomes=["For", "Against"],
                )

        agenda_deck = getattr(
            game_state, "get_agenda_deck", lambda: _DefaultAgendaDeck()
        )()

        try:
            # Execute first agenda
            first_result = self.resolve_first_agenda(
                agenda_deck, speaker_system, voting_system, players
            )

            if not first_result.success:
                return first_result

            # Execute second agenda
            second_result = self.resolve_second_agenda(
                agenda_deck, speaker_system, voting_system, players
            )

            if not second_result.success:
                return second_result

            # Ready all planets
            players_planets: dict[str, list[Any]] = getattr(
                game_state, "get_players_planets", lambda: {}
            )()
            ready_result = self.ready_all_planets(players_planets)

            if not ready_result.success:
                return ready_result

            # Combine results
            return AgendaPhaseResult(
                success=True,
                first_agenda_resolved=first_result.first_agenda_resolved,
                second_agenda_resolved=second_result.second_agenda_resolved,
                planets_readied=ready_result.planets_readied,
                ready_for_next_round=True,
                voting_completed=bool(
                    first_result.voting_completed and second_result.voting_completed
                ),
                outcome_resolved=bool(
                    first_result.outcome_resolved and second_result.outcome_resolved
                ),
            )

        except Exception as e:
            return AgendaPhaseResult(
                success=False, error_message=f"Agenda phase execution failed: {str(e)}"
            )

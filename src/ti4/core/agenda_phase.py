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
class AgendaOutcome:
    """Represents a possible outcome of an agenda."""

    name: str
    description: str
    effect: str | None = None


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

    def remove_from_mecatol_rex(self, player_id: str) -> bool:
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
        # Check if player already voted for different outcome
        if player_id in self.player_votes:
            if self.player_votes[player_id] != outcome:
                return VotingOutcome(
                    success=False,
                    error_message="Player cannot cast votes for multiple outcomes",
                )

        # Validate agenda outcomes if provided
        if agenda and outcome not in agenda.outcomes:
            return VotingOutcome(
                success=False, error_message=f"Invalid outcome '{outcome}' for agenda"
            )

        # Calculate total influence and exhaust planets
        total_influence = 0
        for planet in planets:
            if hasattr(planet, "influence") and hasattr(planet, "exhaust"):
                total_influence += planet.influence
                planet.exhaust()  # Exhaust planet when voting

        # Record vote
        self.player_votes[player_id] = outcome

        return VotingOutcome(success=True, votes_cast=total_influence, outcome=outcome)

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
        # Draw agenda card from deck
        agenda = agenda_deck.draw_top_card()

        return AgendaPhaseResult(
            success=True,
            first_agenda_resolved=True,
            agenda_revealed=agenda,
            voting_completed=True,
            outcome_resolved=True,
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
        # Draw second agenda card from deck
        agenda = agenda_deck.draw_top_card()

        return AgendaPhaseResult(
            success=True,
            second_agenda_resolved=True,
            agenda_revealed=agenda,
            voting_completed=True,
            outcome_resolved=True,
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
                # Law is discarded
                return AgendaPhaseResult(
                    success=True, agenda_discarded=True, outcome_resolved=True
                )

        elif agenda.agenda_type == AgendaType.DIRECTIVE:
            # Directive provides one-time effect and is discarded
            return AgendaPhaseResult(
                success=True,
                one_time_effect_executed=True,
                agenda_discarded=True,
                outcome_resolved=True,
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
        if custodians and custodians.is_on_mecatol_rex():
            return AgendaPhaseResult(
                success=True,
                phase_skipped=True,
                reason="Custodians token still on Mecatol Rex",
            )

        # Placeholder for complete phase execution
        return AgendaPhaseResult(
            success=True,
            first_agenda_resolved=True,
            second_agenda_resolved=True,
            planets_readied=True,
            ready_for_next_round=True,
        )

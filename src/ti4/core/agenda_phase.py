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
from typing import Any, Callable

# Voting orchestration imports removed - will be re-implemented via TDD


class VotingValidationError(Exception):
    """Raised when voting validation fails with detailed error information."""

    def __init__(
        self, message: str, agenda_name: str = "", attempted_outcome: str = ""
    ):
        super().__init__(message)
        self.agenda_name = agenda_name
        self.attempted_outcome = attempted_outcome


@dataclass
class VotingValidationResult:
    """Result of agenda-specific voting validation."""

    is_valid: bool
    error_message: str = ""


@dataclass
class ElectionProcessingResult:
    """Result of election outcome processing."""

    success: bool
    elected_target: str = ""
    error_message: str = ""


@dataclass
class VotingBypassResult:
    """Result of voting bypass execution."""

    success: bool
    bypassed_by_committee_formation: bool = False
    elected_target: str = ""
    error_message: str = ""


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

    outcome: str
    elected_target: str | None = None
    votes_for: dict[str, int] | None = None
    votes_against: dict[str, int] | None = None
    winning_outcome: str | None = None
    vote_tally: dict[str, int] | None = None
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
            outcome=chosen_outcome,
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
        agenda: AgendaCard | Any | None = None,
    ) -> VotingOutcome:
        """
        Cast votes using planet influence.

        LRR 8.6: Players cast votes by exhausting planets equal to the influence
        value they wish to spend.
        """
        # Validate agenda outcomes if provided
        if agenda:
            # Get outcomes from either legacy or concrete card
            if hasattr(agenda, "get_voting_outcomes"):
                # Concrete agenda card
                valid_outcomes = agenda.get_voting_outcomes()
            elif hasattr(agenda, "outcomes"):
                # Legacy AgendaCard
                valid_outcomes = agenda.outcomes
            else:
                # Fallback
                valid_outcomes = ["For", "Against"]

            if outcome not in valid_outcomes:
                return VotingOutcome(
                    success=False,
                    error_message=f"Invalid outcome '{outcome}' for agenda",
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
        seen: set[str] = set()
        total_influence = 0
        to_exhaust: list[Any] = []
        for planet in planets:
            # Use stable planet name instead of object identity for deduplication
            planet_name = getattr(planet, "name", str(planet))
            if planet_name in seen:
                return VotingOutcome(
                    success=False,
                    error_message="Cannot use duplicate planet in vote list",
                )
            seen.add(str(planet_name))

            if not hasattr(planet, "influence") or not hasattr(planet, "exhaust"):
                return VotingOutcome(
                    success=False, error_message="Invalid planet object for voting"
                )

            # Validate ownership
            if planet.controlled_by != player_id:
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
        Returns a fresh copy to prevent caller-side mutations.
        """
        speaker = speaker_system.get_speaker()
        if speaker and speaker in players:
            other_players = [p for p in players if p != speaker]
            return other_players + [speaker]
        return players.copy()

    def validate_outcome_against_card(
        self, outcome: str, agenda_card: AgendaCard | Any
    ) -> bool:
        """Validate voting outcome against agenda card specifications."""
        if not agenda_card or not outcome:
            return False

        valid_outcomes = self._get_voting_outcomes_from_card(agenda_card)
        return outcome in valid_outcomes

    def get_valid_election_targets(
        self, agenda_card: AgendaCard | Any, game_state: Any
    ) -> list[str]:
        """Get valid election targets for an agenda card."""
        if not agenda_card or not game_state:
            return []

        # Basic implementation - return empty list for now
        # Future enhancement: implement based on agenda card type
        return []

    def validate_election_target(
        self, agenda_card: AgendaCard | Any, target: str, game_state: Any
    ) -> bool:
        """Validate an election target for an agenda card."""
        if not agenda_card or not target or not game_state:
            return False

        # Basic implementation - always return True for now
        # Future enhancement: implement based on agenda card requirements
        return True

    def validate_agenda_specific_requirements(
        self, agenda_card: AgendaCard | Any, target: str, game_state: Any
    ) -> VotingValidationResult:
        """Validate agenda-specific requirements for voting."""
        if not agenda_card:
            return VotingValidationResult(
                is_valid=False, error_message="Agenda card cannot be None"
            )

        if not target:
            return VotingValidationResult(
                is_valid=False, error_message="Target cannot be empty"
            )

        # Basic implementation - always return valid for now
        # Future enhancement: implement agenda-specific validation logic
        return VotingValidationResult(is_valid=True)

    def _get_agenda_name(self, agenda_card: AgendaCard | Any) -> str:
        """Helper method to get agenda name from either legacy or concrete card."""
        if hasattr(agenda_card, "get_name"):
            name = agenda_card.get_name()
            return name if isinstance(name, str) else "Unknown Agenda"
        elif hasattr(agenda_card, "name"):
            name = agenda_card.name
            return name if isinstance(name, str) else "Unknown Agenda"
        return "Unknown Agenda"

    def _get_voting_outcomes_from_card(
        self, agenda_card: AgendaCard | Any
    ) -> list[str]:
        """Helper method to get voting outcomes from either legacy or concrete card."""
        if hasattr(agenda_card, "get_voting_outcomes"):
            outcomes = agenda_card.get_voting_outcomes()
            return outcomes if isinstance(outcomes, list) else ["For", "Against"]
        elif hasattr(agenda_card, "outcomes"):
            outcomes = agenda_card.outcomes
            return outcomes if isinstance(outcomes, list) else ["For", "Against"]
        return ["For", "Against"]

    def validate_outcome_with_detailed_errors(
        self, outcome: str, agenda_card: AgendaCard | Any
    ) -> bool:
        """Validate outcome with detailed error information."""
        if not outcome:
            raise VotingValidationError("Outcome cannot be empty")

        if not agenda_card:
            raise VotingValidationError("Agenda card cannot be None")

        agenda_name = self._get_agenda_name(agenda_card)

        # Check if outcome is valid
        if not self.validate_outcome_against_card(outcome, agenda_card):
            raise VotingValidationError(
                f"Invalid voting outcome '{outcome}' for agenda '{agenda_name}'",
                agenda_name=agenda_name,
                attempted_outcome=outcome,
            )
        return True

    def process_election_outcome(
        self, agenda_card: AgendaCard | Any, vote_result: VoteResult, game_state: Any
    ) -> ElectionProcessingResult:
        """Process election outcome for an agenda card."""
        if not agenda_card or not vote_result:
            return ElectionProcessingResult(
                success=False,
                error_message="Invalid parameters for election processing",
            )

        # Basic implementation
        return ElectionProcessingResult(
            success=True, elected_target=vote_result.elected_target or ""
        )

    def can_bypass_voting(self, committee_card: Any, target_agenda: Any) -> bool:
        """Check if voting can be bypassed using Committee Formation."""
        if not committee_card or not target_agenda:
            return False

        # Check if committee card has bypass ability
        if hasattr(committee_card, "can_bypass_election_agenda"):
            # Get the first voting outcome from target agenda to check if it's an election
            outcomes = self._get_voting_outcomes_from_card(target_agenda)
            if outcomes:
                from .game_state import GameState

                game_state = GameState()  # Minimal game state for testing
                result = committee_card.can_bypass_election_agenda(
                    outcomes[0], game_state
                )
                return bool(result)
        return False

    def execute_voting_bypass(
        self,
        committee_card: Any,
        target_agenda: Any,
        chosen_player: str,
        game_state: Any,
    ) -> VotingBypassResult:
        """Execute voting bypass using Committee Formation."""
        if not committee_card or not target_agenda or not chosen_player:
            return VotingBypassResult(
                success=False, error_message="Invalid parameters for voting bypass"
            )

        # Basic implementation
        return VotingBypassResult(
            success=True,
            bypassed_by_committee_formation=True,
            elected_target=chosen_player,
        )


class AgendaPhase:
    """Main controller for the agenda phase."""

    def __init__(self) -> None:
        """Initialize the agenda phase."""
        self.voting_system = VotingSystem()
        self.speaker_system = SpeakerSystem()
        self._agenda_card_registry: Any | None = None

    def trigger_timing_window(self, timing_window: str, **kwargs: Any) -> None:
        """
        Trigger a timing window for action cards, promissory notes, and faction abilities.

        This is a placeholder implementation that will be properly developed via TDD.
        """
        # Minimal implementation - does nothing for now
        pass

    def reveal_agenda(self, agenda: AgendaCard | Any) -> None:
        """
        Reveal an agenda card and trigger appropriate timing windows.

        According to LRR 8.4 and TI4 compendium, this should trigger:
        1. "when_agenda_revealed" timing window
        2. "after_agenda_revealed" timing window

        Supports both legacy AgendaCard and concrete agenda card instances.
        """
        # Trigger "when an agenda is revealed" timing window
        self.trigger_timing_window("when_agenda_revealed", agenda=agenda)

        # Trigger "after an agenda is revealed" timing window
        self.trigger_timing_window("after_agenda_revealed", agenda=agenda)

    def can_bypass_voting_with_committee_formation(self, card: Any) -> bool:
        """Check if voting can be bypassed with Committee Formation."""
        # Simple implementation - check if card has bypass ability
        return hasattr(card, "can_bypass_election_agenda")

    def use_committee_formation_bypass(self, card: Any, chosen_player: str) -> Any:
        """Use Committee Formation to bypass voting."""
        # Delegate to the card's bypass ability
        if hasattr(card, "use_bypass_ability"):
            from .game_state import GameState

            game_state = GameState()  # Minimal game state for testing
            return card.use_bypass_ability(chosen_player, game_state)

        # Fallback implementation
        from .agenda_cards.effect_resolver import AgendaResolutionResult

        return AgendaResolutionResult(
            success=True,
            directive_executed=True,
            elected_target=chosen_player,
            description=f"Committee Formation: {chosen_player} elected without voting",
        )

    def start_voting(self, agenda: AgendaCard | Any) -> None:
        """
        Start the voting process for an agenda.

        Supports both legacy AgendaCard and concrete agenda card instances.
        """
        # Trigger timing window before players vote
        self.trigger_timing_window("before_players_vote", agenda=agenda)
        # Minimal implementation - does nothing else for now
        pass

    def should_execute_phase(self, custodians: CustodiansToken) -> bool:
        """Check if agenda phase should execute."""
        return not custodians.is_on_mecatol_rex()

    def _determine_vote_result(
        self,
        agenda: AgendaCard | Any,
        voting_system: VotingSystem,
        speaker_system: SpeakerSystem,
    ) -> VoteResult:
        """
        Helper method to determine the winning outcome from vote tallies.

        Handles both empty tallies (speaker decides) and ties (speaker breaks).
        Supports both legacy AgendaCard and concrete agenda card instances.
        """
        vote_tally = voting_system.get_vote_tally()

        # Get outcomes from either legacy AgendaCard or concrete card
        outcomes = self._get_voting_outcomes(agenda)

        if not vote_tally:
            # No votes cast — treat as a tie of zero and let the speaker decide
            zero_tally = dict.fromkeys(outcomes or ["For", "Against"], 0)
            chosen = outcomes[0] if outcomes else "For"
            return speaker_system.resolve_tie(zero_tally, chosen)
        else:
            # Find outcome with most votes
            max_votes = max(vote_tally.values())
            tied_outcomes = [
                outcome for outcome, votes in vote_tally.items() if votes == max_votes
            ]

            if len(tied_outcomes) == 1:
                # Clear winner
                winning_outcome = tied_outcomes[0]
                return VoteResult(
                    outcome=winning_outcome,
                    winning_outcome=winning_outcome,
                    vote_tally=vote_tally,
                    success=True,
                )
            else:
                # Tie - speaker decides (chooses first tied outcome for simulation)
                winning_outcome = tied_outcomes[0]
                return speaker_system.resolve_tie(vote_tally, winning_outcome)

    def resolve_first_agenda(
        self,
        agenda_deck: Any,
        speaker_system: SpeakerSystem,
        voting_system: VotingSystem,
        players: list[str],
        voting_callback: Callable[[VoteResult], VoteResult] | None = None,
    ) -> AgendaPhaseResult:
        """
        Resolve the first agenda of the phase using the voting orchestration system.

        LRR 8.2: The speaker reveals the top agenda card from the agenda deck.

        Flow: reveal → reset_votes → external voting window → tally/resolve
        """
        # Validate inputs
        if agenda_deck is None:
            raise ValueError("Agenda deck cannot be None")
        if speaker_system is None:
            raise ValueError("Speaker system cannot be None")
        if voting_system is None:
            raise ValueError("Voting system cannot be None")
        if not players:
            raise ValueError("Players list cannot be empty")

        # Draw agenda card from deck
        agenda = agenda_deck.draw_top_card()

        # Reset voting system for new agenda (immediately after reveal, before any external voting)
        voting_system.reset_votes()

        # Reveal the agenda (triggers timing windows)
        self.reveal_agenda(agenda)

        # Get voting order (speaker votes last)
        voting_system.get_voting_order(players, speaker_system)

        # Start voting process (triggers before_players_vote timing window)
        self.start_voting(agenda)

        # TODO: Implement voting orchestration system via TDD
        # For now, use simplified voting approach
        # orchestration_result = self.voting_orchestrator.start_voting_session(
        #     agenda=agenda,
        #     players=players,
        #     voting_order=voting_order,
        #     timeout_seconds=300.0  # 5 minutes default
        # )

        # if not orchestration_result.success:
        #     return AgendaPhaseResult(
        #         success=False,
        #         error_message=f"Failed to start voting session: {orchestration_result.error_message}"
        #     )

        # If a voting callback is provided, use it to handle the voting window
        # Otherwise, fall back to the old simulation behavior
        if voting_callback:
            # TODO: Implement voting orchestration system via TDD
            # For now, use simplified voting approach without orchestration
            vote_result = self._determine_vote_result(
                agenda, voting_system, speaker_system
            )
            try:
                # Call the voting callback with the result
                vote_result = voting_callback(vote_result)
            except Exception as e:
                return AgendaPhaseResult(
                    success=False, error_message=f"Voting callback failed: {e}"
                )
        else:
            # Fallback: simulate voting process for backward compatibility
            vote_result = self._determine_vote_result(
                agenda, voting_system, speaker_system
            )

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
        voting_callback: Callable[[VoteResult], VoteResult] | None = None,
    ) -> AgendaPhaseResult:
        """
        Resolve the second agenda of the agenda phase.

        Args:
            agenda_deck: The agenda deck to draw from
            speaker_system: The speaker system for tie resolution
            voting_system: The voting system for vote management
            players: List of player IDs in the game
            voting_callback: Optional callback for handling voting window

        Returns:
            AgendaPhaseResult indicating success/failure and details
        """
        # Draw second agenda
        try:
            agenda = agenda_deck.draw_top_card()
        except Exception as e:
            return AgendaPhaseResult(
                success=False, error_message=f"Failed to draw second agenda: {e}"
            )

        # Reveal agenda and trigger timing windows
        self.reveal_agenda(agenda)

        # Reset voting system for new agenda (immediately after reveal, before any external voting)
        voting_system.reset_votes()

        # Get voting order (speaker votes last)
        voting_system.get_voting_order(players, speaker_system)

        # Start voting process (triggers before_players_vote timing window)
        self.start_voting(agenda)

        # TODO: Implement voting orchestration system via TDD
        # For now, use simplified voting approach
        # orchestration_result = self.voting_orchestrator.start_voting_session(
        #     agenda=agenda,
        #     players=players,
        #     voting_order=voting_order,
        #     timeout_seconds=300.0  # 5 minutes default
        # )

        # if not orchestration_result.success:
        #     return AgendaPhaseResult(
        #         success=False,
        #         error_message=f"Failed to start voting session: {orchestration_result.error_message}"
        #     )

        # If a voting callback is provided, use it to handle the voting window
        # Otherwise, fall back to the old simulation behavior
        if voting_callback:
            # TODO: Implement voting orchestration system via TDD
            # For now, use simplified voting approach without orchestration
            vote_result = self._determine_vote_result(
                agenda, voting_system, speaker_system
            )
            try:
                # Call the voting callback with the result
                vote_result = voting_callback(vote_result)
            except Exception as e:
                return AgendaPhaseResult(
                    success=False, error_message=f"Voting callback failed: {e}"
                )
        else:
            # Fallback: simulate voting process for backward compatibility
            vote_result = self._determine_vote_result(
                agenda, voting_system, speaker_system
            )

        # Resolve the agenda outcome
        outcome_result = self.resolve_agenda_outcome(agenda, vote_result)

        return AgendaPhaseResult(
            success=outcome_result.success,
            second_agenda_resolved=True,
            agenda_revealed=agenda,
            voting_completed=True,
            outcome_resolved=outcome_result.success,
            law_enacted=outcome_result.law_enacted,
            permanent_effect_added=outcome_result.permanent_effect_added,
            one_time_effect_executed=outcome_result.one_time_effect_executed,
            agenda_discarded=outcome_result.agenda_discarded,
            error_message=outcome_result.error_message,
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
                planet.ready()

        return AgendaPhaseResult(success=True, planets_readied=True)

    def resolve_agenda_outcome(
        self, agenda: AgendaCard | Any, vote_result: VoteResult
    ) -> AgendaPhaseResult:
        """
        Resolve the outcome of an agenda based on voting results.

        LRR 7.7-7.8: Laws become permanent effects when "For" wins,
        directives provide one-time effects.
        Supports both legacy AgendaCard and concrete agenda card instances.
        """
        # Get agenda type and name from either legacy or concrete card
        agenda_type = self._get_agenda_type(agenda)
        agenda_name = self._get_agenda_name(agenda)

        if agenda_type == AgendaType.LAW:
            if vote_result.winning_outcome == "For":
                # Law is enacted as permanent effect
                effect_description = (
                    getattr(agenda, "for_effect", None) or "Law enacted"
                )
                return AgendaPhaseResult(
                    success=True,
                    law_enacted=True,
                    permanent_effect_added=True,
                    outcome_resolved=True,
                    reason=f"Law '{agenda_name}' enacted: {effect_description}",
                )
            elif vote_result.winning_outcome == "Elect" or str(
                vote_result.winning_outcome
            ).startswith("Elect"):
                # Elect outcome on Law - becomes permanent effect (LRR 8.20-8.21)
                elected_target = vote_result.elected_planet or "default_target"
                effect_description = (
                    getattr(agenda, "for_effect", None) or "Law enacted with election"
                )
                return AgendaPhaseResult(
                    success=True,
                    law_enacted=True,
                    permanent_effect_added=True,
                    outcome_resolved=True,
                    reason=f"Law '{agenda_name}' enacted with elected target '{elected_target}': {effect_description}",
                )
            else:
                # Law is discarded (Against or other outcome)
                effect_description = (
                    getattr(agenda, "against_effect", None) or "Law discarded"
                )
                return AgendaPhaseResult(
                    success=True,
                    agenda_discarded=True,
                    outcome_resolved=True,
                    reason=f"Law '{agenda_name}' rejected: {effect_description}",
                )

        elif agenda_type == AgendaType.DIRECTIVE:
            # Handle different directive outcomes
            if vote_result.winning_outcome == "Elect" or str(
                vote_result.winning_outcome
            ).startswith("Elect"):
                # Elect outcome - choose a player/planet/system
                elected_target = vote_result.elected_planet or "default_target"
                effect_description = (
                    getattr(agenda, "for_effect", None) or "Election effect applied"
                )
                return AgendaPhaseResult(
                    success=True,
                    one_time_effect_executed=True,
                    agenda_discarded=True,
                    outcome_resolved=True,
                    reason=f"Directive '{agenda_name}' - Elected '{elected_target}': {effect_description}",
                )
            elif vote_result.winning_outcome in ["For", "Against"]:
                # Standard For/Against directive
                effect_applied = vote_result.winning_outcome == "For"
                if effect_applied:
                    effect_description = (
                        getattr(agenda, "for_effect", None) or "For effect applied"
                    )
                    reason = f"Directive '{agenda_name}' passed: {effect_description}"
                else:
                    effect_description = (
                        getattr(agenda, "against_effect", None)
                        or "Against effect applied"
                    )
                    reason = f"Directive '{agenda_name}' failed: {effect_description}"

                return AgendaPhaseResult(
                    success=True,
                    one_time_effect_executed=effect_applied,
                    agenda_discarded=True,
                    outcome_resolved=True,
                    reason=reason,
                )
            else:
                # Other directive outcomes (custom outcomes)
                effect_description = (
                    getattr(agenda, "effect", None)
                    or f"Custom outcome: {vote_result.winning_outcome}"
                )
                return AgendaPhaseResult(
                    success=True,
                    one_time_effect_executed=True,
                    agenda_discarded=True,
                    outcome_resolved=True,
                    reason=f"Directive '{agenda_name}' - {effect_description}",
                )

        return AgendaPhaseResult(success=False, error_message="Unknown agenda type")

    def set_agenda_card_registry(self, registry: Any) -> None:
        """Set the agenda card registry for concrete card support."""
        self._agenda_card_registry = registry

    def get_agenda_card_registry(self) -> Any | None:
        """Get the current agenda card registry."""
        return self._agenda_card_registry

    def can_resolve_concrete_cards(self) -> bool:
        """Check if agenda phase can resolve concrete cards."""
        return self._agenda_card_registry is not None

    def _get_voting_outcomes(self, agenda: AgendaCard | Any) -> list[str]:
        """Get voting outcomes from either legacy or concrete agenda card."""
        if hasattr(agenda, "get_voting_outcomes"):
            # Concrete agenda card
            outcomes = agenda.get_voting_outcomes()
            return outcomes if isinstance(outcomes, list) else ["For", "Against"]
        elif hasattr(agenda, "outcomes"):
            # Legacy AgendaCard
            outcomes = agenda.outcomes
            return outcomes if isinstance(outcomes, list) else ["For", "Against"]
        else:
            # Fallback
            return ["For", "Against"]

    def _get_agenda_name(self, agenda: AgendaCard | Any) -> str:
        """Get agenda name from either legacy or concrete agenda card."""
        if hasattr(agenda, "get_name"):
            # Concrete agenda card
            name = agenda.get_name()
            return name if isinstance(name, str) else "Unknown Agenda"
        elif hasattr(agenda, "name"):
            # Legacy AgendaCard
            name = agenda.name
            return name if isinstance(name, str) else "Unknown Agenda"
        else:
            return "Unknown Agenda"

    def _get_agenda_type(self, agenda: AgendaCard | Any) -> AgendaType:
        """Get agenda type from either legacy or concrete agenda card."""
        if hasattr(agenda, "get_agenda_type"):
            # Concrete agenda card
            agenda_type = agenda.get_agenda_type()
            return (
                agenda_type if isinstance(agenda_type, AgendaType) else AgendaType.LAW
            )
        elif hasattr(agenda, "agenda_type"):
            # Legacy AgendaCard
            agenda_type = agenda.agenda_type
            return (
                agenda_type if isinstance(agenda_type, AgendaType) else AgendaType.LAW
            )
        else:
            # Default to LAW for safety
            return AgendaType.LAW

    def execute_complete_phase(
        self,
        game_state: Any,
        custodians: CustodiansToken | None = None,
        voting_callback: Callable[[VoteResult], VoteResult] | None = None,
    ) -> AgendaPhaseResult:
        """
        Execute the complete agenda phase sequence with voting orchestration support.

        LRR 8.1: The agenda phase is executed only if the custodians token
        is not on Mecatol Rex.

        Args:
            game_state: The current game state
            custodians: The custodians token (optional)
            voting_callback: Optional callback to handle voting windows interactively
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
            # Execute first agenda with voting orchestration
            first_result = self.resolve_first_agenda(
                agenda_deck, speaker_system, voting_system, players, voting_callback
            )

            if not first_result.success:
                return first_result

            # Execute second agenda with voting orchestration
            second_result = self.resolve_second_agenda(
                agenda_deck, speaker_system, voting_system, players, voting_callback
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
            # Ensure voting orchestration is cleaned up on error
            # TODO: Implement proper voting orchestration cleanup
            # self.voting_orchestrator.cancel_voting(f"Phase execution error: {e}")
            return AgendaPhaseResult(
                success=False, error_message=f"Agenda phase execution failed: {str(e)}"
            )

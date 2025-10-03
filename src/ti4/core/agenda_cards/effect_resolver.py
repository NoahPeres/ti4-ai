"""
Agenda effect resolution system for TI4 agenda cards.

This module provides the AgendaEffectResolver class for resolving agenda card
effects based on voting outcomes, handling both law enactment and directive execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..agenda_phase import VoteResult
    from ..game_state import GameState
    from .base import BaseAgendaCard


@dataclass
class AgendaResolutionResult:
    """Result of resolving an agenda card outcome."""

    success: bool
    law_enacted: bool = False
    directive_executed: bool = False
    description: str = ""
    elected_target: str | None = None


class AgendaResolutionError(Exception):
    """Raised when agenda resolution fails."""


class OutcomeValidationError(AgendaResolutionError):
    """Raised when voting outcome validation fails."""


class ElectionValidationError(AgendaResolutionError):
    """Raised when election validation fails."""


class AgendaEffectResolver:
    """Resolves agenda card effects based on voting outcomes."""

    def __init__(self) -> None:
        """Initialize the agenda effect resolver."""
        pass

    def resolve_agenda_outcome(
        self,
        agenda: BaseAgendaCard,
        vote_result: VoteResult,
        game_state: GameState,
    ) -> AgendaResolutionResult:
        """Resolve agenda based on voting outcome."""
        # Basic validation
        if agenda is None:
            raise AgendaResolutionError("Agenda card cannot be None")
        if vote_result is None:
            raise AgendaResolutionError("Vote result cannot be None")
        if game_state is None:
            raise AgendaResolutionError("Game state cannot be None")

        # Validate outcome against card
        winning_outcome = vote_result.winning_outcome
        if winning_outcome is None:
            raise AgendaResolutionError("Vote result winning_outcome cannot be None")

        if not self.validate_outcome(winning_outcome, agenda):
            raise OutcomeValidationError(
                f"Invalid outcome '{winning_outcome}' for agenda"
            )

        # Check if election outcome requires elected target
        if self._is_election_outcome(winning_outcome):
            elected_target = vote_result.elected_target or getattr(
                vote_result, "elected_planet", None
            )
            if not elected_target:
                raise ElectionValidationError(
                    "Election outcome requires elected_target but none provided"
                )
            if not vote_result.elected_target:
                vote_result.elected_target = elected_target

        # Determine if this is a law or directive
        from ..constants import AgendaType

        if agenda.get_agenda_type() == AgendaType.LAW:
            return self._resolve_law_outcome(agenda, vote_result, game_state)
        else:
            return self._resolve_directive_outcome(agenda, vote_result, game_state)

    def _resolve_law_outcome(
        self,
        agenda: BaseAgendaCard,
        vote_result: VoteResult,
        game_state: GameState,
    ) -> AgendaResolutionResult:
        """Resolve law card outcome."""
        description = f"{agenda.get_name()} enacted"
        if vote_result.elected_target:
            description += f" with {vote_result.elected_target} elected"

        # Enact the law in the game state
        if game_state.law_manager is not None:
            from ..agenda_cards.law_manager import ActiveLaw

            # Delegate to the card's resolver for richer payload or ActiveLaw
            winning_outcome = vote_result.winning_outcome or "For"  # Default fallback
            resolution_payload = agenda.resolve_outcome(
                winning_outcome, vote_result, game_state
            )
            # Use the real current round, fall back to 1 if missing
            enacted_round = getattr(game_state, "current_round", 1)

            if isinstance(resolution_payload, ActiveLaw):
                active_law = resolution_payload
            else:
                # Extract or default the effect description
                effect_description = getattr(
                    resolution_payload, "description", f"{agenda.get_name()} law effect"
                )
                # If the resolver provided its own description, use it
                if getattr(resolution_payload, "description", None):
                    description = resolution_payload.description

                active_law = ActiveLaw(
                    agenda_card=agenda,
                    enacted_round=enacted_round,
                    effect_description=effect_description,
                    elected_target=vote_result.elected_target,
                )

            game_state.law_manager.enact_law(active_law)

        return AgendaResolutionResult(
            success=True,
            law_enacted=True,
            directive_executed=False,
            description=description,
            elected_target=vote_result.elected_target,
        )

    def _resolve_directive_outcome(
        self,
        agenda: BaseAgendaCard,
        vote_result: VoteResult,
        game_state: GameState,
    ) -> AgendaResolutionResult:
        """Resolve directive card outcome."""
        # Execute the directive's effects and capture any payload (including a custom description).
        winning_outcome = vote_result.winning_outcome or "For"  # Default fallback
        resolution_payload = agenda.resolve_outcome(
            winning_outcome, vote_result, game_state
        )

        # Fallback description if the payload didn't override it.
        description = f"{agenda.get_name()} executed"
        if vote_result.elected_target:
            description += f" with {vote_result.elected_target} elected"
        if (
            hasattr(resolution_payload, "description")
            and resolution_payload.description
        ):
            description = resolution_payload.description

        return AgendaResolutionResult(
            success=True,
            law_enacted=False,
            directive_executed=True,
            description=description,
            elected_target=vote_result.elected_target,
        )

    def validate_outcome(self, outcome: str, agenda: BaseAgendaCard) -> bool:
        """Validate voting outcome against card specifications."""
        if not outcome or outcome is None:
            return False

        # Get valid outcomes from agenda card
        valid_outcomes = agenda.get_voting_outcomes()
        return outcome in valid_outcomes

    def validate_planet_election(
        self, planet_name: str, outcome: str, game_state: GameState
    ) -> bool:
        """Validate planet election for different planet types."""
        if not planet_name or planet_name is None:
            return False

        # Find the planet in the game state
        planet = None
        for player_planets in game_state.player_planets.values():
            for p in player_planets:
                if p.name == planet_name:
                    planet = p
                    break
            if planet:
                break

        if not planet:
            return False  # Planet not found

        # Validate planet type based on outcome
        if outcome == "Elect Cultural Planet":
            return "cultural" in planet.traits
        elif outcome == "Elect Industrial Planet":
            return "industrial" in planet.traits
        elif outcome == "Elect Hazardous Planet":
            return "hazardous" in planet.traits

        # For other outcomes, accept any planet
        return True

    def validate_player_election(
        self, player_id: str, outcome: str, game_state: GameState
    ) -> bool:
        """Validate player election."""
        if not player_id or player_id is None:
            return False

        # Check if player exists in game state
        player_ids = [player.id for player in game_state.players]
        return player_id in player_ids

    def _is_election_outcome(self, outcome: str) -> bool:
        """Check if outcome is an election type."""
        election_keywords = ["Elect"]
        return any(keyword in outcome for keyword in election_keywords)

    def is_election_outcome(self, outcome: str) -> bool:
        """Check if outcome is an election type (public method)."""
        return self._is_election_outcome(outcome)

    def validate_election_target(
        self, target: str | None, outcome: str, game_state: GameState
    ) -> bool:
        """Validate election target for the given outcome."""
        # Validate inputs
        if target is None or target == "":
            raise ElectionValidationError("Election target cannot be None or empty")

        if game_state is None:
            raise ElectionValidationError("Game state cannot be None")

        if not self.is_election_outcome(outcome):
            raise ElectionValidationError("Invalid election outcome")

        # Delegate to specific validation methods
        if "Player" in outcome:
            return self.validate_player_election(target, outcome, game_state)
        elif "Planet" in outcome:
            return self.validate_planet_election(target, outcome, game_state)
        else:
            # For other election types (e.g., objectives), basic validation
            return True

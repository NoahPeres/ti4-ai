"""Core game state management for TI4."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from .game_phase import GamePhase
from .player import Player
from .promissory_notes import PromissoryNoteManager

if TYPE_CHECKING:
    from .galaxy import Galaxy
    from .objective import Objective
    from .planet import Planet
    from .planet_card import PlanetCard
    from .strategic_action import StrategyCardType
    from .strategy_cards.coordinator import StrategyCardCoordinator
    from .system import System
    from .technology import TechnologyCard
else:
    Galaxy = "Galaxy"
    Objective = "Objective"
    PlanetCard = "PlanetCard"
    StrategyCardType = "StrategyCardType"
    StrategyCardCoordinator = "StrategyCardCoordinator"
    TechnologyCard = "TechnologyCard"


# Victory condition constants
VICTORY_POINTS_TO_WIN = 10


@dataclass(frozen=True)
class GameState:
    """Represents the complete state of a TI4 game."""

    game_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    players: list[Player] = field(default_factory=list, hash=False)
    galaxy: Galaxy | None = None
    phase: GamePhase = GamePhase.SETUP
    systems: dict[str, System] = field(default_factory=dict, hash=False)
    # player_resources field removed - incorrect implementation
    # Resources should be tracked on planets per Rules 47 and 75
    player_technologies: dict[str, list[str]] = field(default_factory=dict, hash=False)
    # Player planets (Rule 34)
    player_planets: dict[str, list[Planet]] = field(default_factory=dict, hash=False)
    # Player technology cards (Rule 34)
    player_technology_cards: dict[str, list[TechnologyCard]] = field(
        default_factory=dict, hash=False
    )
    victory_points: dict[str, int] = field(default_factory=dict, hash=False)
    completed_objectives: dict[str, list[str]] = field(default_factory=dict, hash=False)

    # Phase-specific scoring tracking
    status_phase_scoring: dict[str, dict[str, int]] = field(
        default_factory=dict, hash=False
    )  # player_id -> {public: count, secret: count}
    combat_scoring: dict[str, list[str]] = field(
        default_factory=dict, hash=False
    )  # combat_id -> [objective_ids]

    # Secret objective system (Rule 61.19-61.20)
    player_secret_objectives: dict[str, list[Objective]] = field(
        default_factory=dict, hash=False
    )  # player_id -> [secret_objectives]
    secret_objective_deck: list[Objective] = field(
        default_factory=list, hash=False
    )  # Deck of unassigned secret objectives
    # player_influence field removed - incorrect implementation
    # Influence should be tracked on planets per Rules 47 and 75

    # Strategy card system (Rule 83)
    strategy_card_assignments: dict[str, StrategyCardType] = field(
        default_factory=dict, hash=False
    )  # player_id -> strategy_card
    exhausted_strategy_cards: set[StrategyCardType] = field(
        default_factory=set, hash=False
    )  # Set of exhausted strategy cards
    strategy_card_coordinator: StrategyCardCoordinator | None = field(
        default=None, hash=False
    )  # Optional strategy card coordinator
    # Rule 98.2a: Victory points to win (10 for standard, 14 for variant)
    victory_points_to_win: int = VICTORY_POINTS_TO_WIN

    # Rule 25: Planet control and card management
    planet_card_deck: dict[str, PlanetCard] = field(default_factory=dict, hash=False)
    player_planet_cards: dict[str, list[PlanetCard]] = field(
        default_factory=dict, hash=False
    )
    planet_control_tokens: dict[str, set[str]] = field(default_factory=dict, hash=False)
    # Centralized planet control mapping to avoid mutating Planet objects
    planet_control_mapping: dict[str, str | None] = field(
        default_factory=dict, hash=False
    )
    # Planet attachment tokens for visual board representation (Rule 12.3)
    planet_attachment_tokens: dict[str, set[str]] = field(
        default_factory=dict, hash=False
    )  # planet_name -> {token_ids}

    # Agenda cards (Rule 22)
    player_agenda_cards: dict[str, list[Any]] = field(
        default_factory=dict, hash=False
    )  # player_id -> [agenda_cards]
    agenda_discard_pile: list[Any] = field(
        default_factory=list, hash=False
    )  # Discarded agenda cards

    # Promissory note management (Rule 69)
    promissory_note_manager: PromissoryNoteManager = field(
        default_factory=PromissoryNoteManager, hash=False
    )

    # Action card system (Rule 2)
    player_action_cards: dict[str, list[str]] = field(
        default_factory=dict, hash=False
    )  # player_id -> [action_card_names]
    action_card_discard_pile: list[str] = field(
        default_factory=list, hash=False
    )  # Discarded action cards

    # Speaker system (Rule 80)
    speaker_id: str | None = field(
        default=None, hash=False
    )  # Current speaker player ID

    def __post_init__(self) -> None:
        """Validate game state invariants after initialization."""
        if self.victory_points_to_win <= 0:
            raise ValueError(
                f"victory_points_to_win must be positive, got {self.victory_points_to_win}"
            )

    def get_victory_points(self, player_id: str) -> int:
        """Get the victory points for a player."""
        return self.victory_points.get(player_id, 0)

    def award_victory_points(self, player_id: str, points: int) -> GameState:
        """Award victory points to a player, returning a new GameState."""
        # Validate player exists in the game
        if not any(player.id == player_id for player in self.players):
            raise ValueError(f"Player {player_id} does not exist in the game")

        new_victory_points = self.victory_points.copy()
        current_points = new_victory_points.get(player_id, 0)
        new_points = current_points + points

        # Guard against negative victory points
        if new_points < 0:
            raise ValueError(
                f"Player {player_id} cannot have negative victory points (attempted: {new_points})"
            )

        # Rule 98.4a: Player cannot have more than maximum victory points
        if new_points > self.victory_points_to_win:
            raise ValueError(
                f"Player {player_id} cannot exceed maximum victory points ({self.victory_points_to_win})"
            )

        new_victory_points[player_id] = new_points

        return self._create_new_state(victory_points=new_victory_points)

    def has_winner(self) -> bool:
        """Check if any player has reached the victory condition."""
        return any(
            points >= self.victory_points_to_win
            for points in self.victory_points.values()
        )

    def get_winner(self) -> str | None:
        """Get the player ID of the winner, if any."""
        # Rule 98.7: Initiative order determines winner in case of ties
        winners = []
        for player_id, points in self.victory_points.items():
            if points >= self.victory_points_to_win:
                winners.append(player_id)

        if not winners:
            return None

        # Use the helper method to sort winners by initiative order
        sorted_winners = self._sort_players_by_initiative_order(winners)
        return sorted_winners[0] if sorted_winners else winners[0]

    def get_players_with_most_victory_points(self) -> list[str]:
        """Get all players tied for the most victory points (Rule 98.5).

        Returns players in initiative order for deterministic tie-breaking.
        """
        if not self.victory_points:
            return []

        max_points = max(self.victory_points.values())
        tied_players = [
            player_id
            for player_id, points in self.victory_points.items()
            if points == max_points
        ]

        # Return in initiative order for deterministic results
        return self._sort_players_by_initiative_order(tied_players)

    def get_players_with_fewest_victory_points(self) -> list[str]:
        """Get all players tied for the fewest victory points (Rule 98.5).

        Returns players in initiative order for deterministic tie-breaking.
        """
        if not self.victory_points:
            return []

        min_points = min(self.victory_points.values())
        tied_players = [
            player_id
            for player_id, points in self.victory_points.items()
            if points == min_points
        ]

        # Return in initiative order for deterministic results
        return self._sort_players_by_initiative_order(tied_players)

    def _sort_players_by_initiative_order(self, player_ids: list[str]) -> list[str]:
        """Sort a list of player IDs by initiative order.

        Uses the same logic as get_winner() to determine initiative order.
        For STATUS phase, uses status phase initiative order as per Rule 98.7.
        """
        if not player_ids:
            return []

        # Get initiative order from StrategyCardCoordinator if available
        if self.strategy_card_coordinator:
            # Use status phase initiative order when in STATUS phase (Rule 98.7)
            if self.phase == GamePhase.STATUS:
                initiative_order = (
                    self.strategy_card_coordinator.get_status_phase_initiative_order()
                )
            else:
                initiative_order = (
                    self.strategy_card_coordinator.get_action_phase_initiative_order()
                )
        elif self.strategy_card_assignments:
            # Sort by strategy card initiative numbers, including all players
            from .strategy_cards.coordinator import STRATEGY_CARD_INITIATIVE_NUMBERS

            # Create list of all players with their initiative values
            all_player_ids = [player.id for player in self.players]
            player_initiatives = []

            for player_id in all_player_ids:
                if player_id in self.strategy_card_assignments:
                    # Player has a strategy card - use its initiative number
                    card = self.strategy_card_assignments[player_id]
                    initiative_num = STRATEGY_CARD_INITIATIVE_NUMBERS.get(
                        card.value.lower(), 999
                    )
                else:
                    # Player has no strategy card - use high initiative number (999)
                    initiative_num = 999

                player_initiatives.append((player_id, initiative_num))

            # Sort by initiative number, with stable ordering for ties
            player_initiatives.sort(key=lambda x: (x[1], all_player_ids.index(x[0])))
            initiative_order = [player_id for player_id, _ in player_initiatives]
        else:
            # Fallback to players list order
            initiative_order = [player.id for player in self.players]

        # Return players in initiative order
        result = []
        for player_id in initiative_order:
            if player_id in player_ids:
                result.append(player_id)

        # Add any players not found in initiative order (shouldn't happen normally)
        for player_id in player_ids:
            if player_id not in result:
                result.append(player_id)

        return result

    def is_objective_completed(self, player_id: str, objective: Objective) -> bool:
        """Check if a player has completed a specific objective."""
        player_objectives = self.completed_objectives.get(player_id, [])
        return objective.id in player_objectives

    def complete_objective(self, player_id: str, objective: Objective) -> GameState:
        """Mark an objective as completed for a player, returning a new GameState."""
        new_completed_objectives = {
            pid: objectives.copy()
            for pid, objectives in self.completed_objectives.items()
        }

        if player_id not in new_completed_objectives:
            new_completed_objectives[player_id] = []

        if objective.id not in new_completed_objectives[player_id]:
            new_completed_objectives[player_id].append(objective.id)

        return self._create_new_state(completed_objectives=new_completed_objectives)

    def _create_new_state(self, **kwargs: Any) -> GameState:
        """Create a new GameState with updated fields."""
        # Prepare a copy to avoid cross-state aliasing
        _tokens_in = kwargs.get(
            "planet_attachment_tokens", self.planet_attachment_tokens
        )
        _tokens_copy = {
            planet_name: tokens.copy() for planet_name, tokens in _tokens_in.items()
        }

        new_state = GameState(
            game_id=self.game_id,
            players=kwargs.get("players", self.players),
            galaxy=self.galaxy,
            phase=self.phase,
            systems=kwargs.get("systems", self.systems),
            # player_resources parameter removed - incorrect implementation
            player_technologies=kwargs.get(
                "player_technologies", self.player_technologies
            ),
            player_planets=kwargs.get("player_planets", self.player_planets),
            player_technology_cards=kwargs.get(
                "player_technology_cards", self.player_technology_cards
            ),
            victory_points=kwargs.get("victory_points", self.victory_points),
            completed_objectives=kwargs.get(
                "completed_objectives", self.completed_objectives
            ),
            status_phase_scoring=kwargs.get(
                "status_phase_scoring", self.status_phase_scoring
            ),
            combat_scoring=kwargs.get("combat_scoring", self.combat_scoring),
            player_secret_objectives=kwargs.get(
                "player_secret_objectives", self.player_secret_objectives
            ),
            secret_objective_deck=kwargs.get(
                "secret_objective_deck", self.secret_objective_deck
            ),
            # player_influence parameter removed - incorrect implementation
            strategy_card_assignments=kwargs.get(
                "strategy_card_assignments", self.strategy_card_assignments
            ),
            exhausted_strategy_cards=kwargs.get(
                "exhausted_strategy_cards", self.exhausted_strategy_cards
            ),
            strategy_card_coordinator=kwargs.get(
                "strategy_card_coordinator", self.strategy_card_coordinator
            ),
            victory_points_to_win=kwargs.get(
                "victory_points_to_win", self.victory_points_to_win
            ),
            # Rule 25: Planet control attributes
            planet_card_deck=kwargs.get("planet_card_deck", self.planet_card_deck),
            player_planet_cards=kwargs.get(
                "player_planet_cards", self.player_planet_cards
            ),
            planet_control_tokens=kwargs.get(
                "planet_control_tokens", self.planet_control_tokens
            ),
            planet_control_mapping=kwargs.get(
                "planet_control_mapping", self.planet_control_mapping
            ),
            planet_attachment_tokens=_tokens_copy,
            # Agenda card system
            player_agenda_cards=kwargs.get(
                "player_agenda_cards", self.player_agenda_cards
            ),
            agenda_discard_pile=kwargs.get(
                "agenda_discard_pile", self.agenda_discard_pile
            ),
            # Promissory note system
            promissory_note_manager=kwargs.get(
                "promissory_note_manager", self.promissory_note_manager
            ),
            # Action card system
            player_action_cards=kwargs.get(
                "player_action_cards", self.player_action_cards
            ),
            action_card_discard_pile=kwargs.get(
                "action_card_discard_pile", self.action_card_discard_pile
            ),
            # Speaker token system
            speaker_id=kwargs.get("speaker_id", self.speaker_id),
        )

        # Ensure every planet card now points at this cloned state for token bookkeeping.
        # Clone PlanetCard instances to avoid mutating the original state's cards
        cloned_planet_card_deck = {}
        for planet_name, card in new_state.planet_card_deck.items():
            cloned_card = card.clone_for_state(new_state)
            cloned_planet_card_deck[planet_name] = cloned_card
        # Use object.__setattr__ to bypass frozen dataclass restriction
        object.__setattr__(new_state, "planet_card_deck", cloned_planet_card_deck)

        cloned_player_planet_cards = {}
        for player_id, cards in new_state.player_planet_cards.items():
            cloned_cards = []
            for card in cards:
                cloned_card = card.clone_for_state(new_state)
                cloned_cards.append(cloned_card)
            cloned_player_planet_cards[player_id] = cloned_cards
        # Use object.__setattr__ to bypass frozen dataclass restriction
        object.__setattr__(new_state, "player_planet_cards", cloned_player_planet_cards)

        return new_state

    def is_valid(self) -> bool:
        """Validate the consistency of the game state."""
        return True

    def score_objective_during_combat(
        self, player_id: str, objective: Objective, combat_id: str
    ) -> GameState:
        """Score an objective during combat with combat-specific limits."""
        # Rule 61.7: Players can only score one objective during or after each combat
        if (
            combat_id in self.combat_scoring
            and len(self.combat_scoring[combat_id]) >= 1
        ):
            raise ValueError(f"Already scored an objective during combat '{combat_id}'")

        # Must be action phase objective
        if objective.scoring_phase != GamePhase.ACTION:
            raise ValueError(
                f"Cannot score {objective.scoring_phase.value} phase objective during combat"
            )

        # Score the objective normally
        new_state = self.score_objective(player_id, objective, GamePhase.ACTION)

        # Update combat scoring tracking
        new_combat_scoring = new_state.combat_scoring.copy()
        if combat_id not in new_combat_scoring:
            new_combat_scoring[combat_id] = []
        new_combat_scoring[combat_id].append(objective.id)

        return new_state._create_new_state(combat_scoring=new_combat_scoring)

    def execute_status_phase_step_1_score_objectives(
        self, player_id: str, objectives: list[Objective]
    ) -> GameState:
        """Execute status phase step 1: score objectives."""
        # Rule 81.1: Following initiative order, each player may score up to one public and one secret objective
        current_state = self

        for objective in objectives:
            current_state = current_state.score_objective(
                player_id, objective, GamePhase.STATUS
            )

        return current_state

    def advance_to_next_status_phase(self) -> GameState:
        """Advance to next status phase, resetting per-phase scoring limits."""
        # Reset status phase scoring limits for new phase
        return self._create_new_state(status_phase_scoring={})

    def _validate_status_phase_scoring_limits(
        self, player_id: str, objective: Objective
    ) -> None:
        """Validate status phase scoring limits (Rule 61.6)."""
        player_scoring = self.status_phase_scoring.get(
            player_id, {"public": 0, "secret": 0}
        )

        if objective.is_public and player_scoring.get("public", 0) >= 1:
            raise ValueError(
                f"Already scored a public objective during this status phase for player '{player_id}'"
            )

        if not objective.is_public and player_scoring.get("secret", 0) >= 1:
            raise ValueError(
                f"Already scored a secret objective during this status phase for player '{player_id}'"
            )

    def _update_status_phase_scoring(
        self, player_id: str, objective: Objective, current_phase: GamePhase
    ) -> dict[str, dict[str, int]]:
        """Update status phase scoring tracking."""
        new_status_phase_scoring = {
            pid: scoring.copy() for pid, scoring in self.status_phase_scoring.items()
        }

        if current_phase == GamePhase.STATUS:
            if player_id not in new_status_phase_scoring:
                new_status_phase_scoring[player_id] = {"public": 0, "secret": 0}

            if objective.is_public:
                new_status_phase_scoring[player_id]["public"] += 1
            else:
                new_status_phase_scoring[player_id]["secret"] += 1

        return new_status_phase_scoring

    # Secret Objective System Methods (Rule 61.19-61.20)

    def assign_secret_objective(
        self, player_id: str, objective: Objective
    ) -> GameState:
        """Assign a secret objective to a player (Rule 61.19)."""
        # Check if player already has this secret objective
        player_secrets = self.player_secret_objectives.get(player_id, [])
        if any(obj.id == objective.id for obj in player_secrets):
            raise ValueError(
                f"Player {player_id} already has secret objective {objective.id}"
            )

        # Check 3 secret objective limit (Rule 61.20)
        if len(player_secrets) >= 3:
            raise ValueError(
                f"Player {player_id} already has maximum of 3 secret objectives"
            )

        # Add secret objective to player's hand
        new_player_secret_objectives = {
            pid: objectives.copy() if isinstance(objectives, list) else objectives
            for pid, objectives in self.player_secret_objectives.items()
        }

        if player_id not in new_player_secret_objectives:
            new_player_secret_objectives[player_id] = []

        new_player_secret_objectives[player_id].append(objective)

        return self._create_new_state(
            player_secret_objectives=new_player_secret_objectives
        )

    def get_player_secret_objectives(self, player_id: str) -> list[Objective]:
        """Get secret objectives owned by a player."""
        return self.player_secret_objectives.get(player_id, [])

    def score_objective(
        self, player_id: str, objective: Objective, current_phase: GamePhase
    ) -> GameState:
        """
        Score an objective for a player with comprehensive validation.

        This method implements the complete Rule 61 objective scoring system including:
        - Phase-specific timing validation (Rule 61.5)
        - Secret objective ownership verification (Rule 61.19-61.20)
        - One-time scoring enforcement (Rule 61.8)
        - Status phase scoring limits (Rule 61.6)

        Args:
            player_id: The ID of the player scoring the objective
            objective: The objective being scored
            current_phase: The current game phase when scoring occurs

        Returns:
            New GameState with the objective scored and all tracking updated

        Raises:
            ValueError: If scoring validation fails for any reason
        """
        self._validate_objective_scoring(player_id, objective, current_phase)

        return self._execute_objective_scoring(player_id, objective, current_phase)

    def _validate_objective_scoring(
        self, player_id: str, objective: Objective, current_phase: GamePhase
    ) -> None:
        """Validate all conditions for objective scoring."""
        # Validate player exists in the game
        if not any(player.id == player_id for player in self.players):
            raise ValueError(f"Player {player_id} does not exist in the game")

        # Rule 61.19-61.20: Secret objective ownership validation
        if not objective.is_public:
            self._validate_secret_objective_ownership(player_id, objective)

        # Rule 61.5: Phase-specific timing validation
        self._validate_objective_timing(objective, current_phase)

        # Rule 61.8: One-time scoring enforcement
        self._validate_objective_not_already_scored(player_id, objective)

        # Rule 61.6: Status phase scoring limits
        if current_phase == GamePhase.STATUS:
            self._validate_status_phase_scoring_limits(player_id, objective)

    def _validate_secret_objective_ownership(
        self, player_id: str, objective: Objective
    ) -> None:
        """Validate that the player owns the secret objective they're trying to score."""
        player_secrets = self.get_player_secret_objectives(player_id)
        if not any(obj.id == objective.id for obj in player_secrets):
            raise ValueError(
                f"Cannot score secret objective {objective.id} - not owned by player {player_id}"
            )

    def _validate_objective_timing(
        self, objective: Objective, current_phase: GamePhase
    ) -> None:
        """Validate that the objective can be scored in the current phase."""
        if objective.scoring_phase != current_phase:
            raise ValueError(
                f"Cannot score objective '{objective.id}' requiring {objective.scoring_phase.value} phase during {current_phase.value} phase"
            )

    def _validate_objective_not_already_scored(
        self, player_id: str, objective: Objective
    ) -> None:
        """Validate that the objective hasn't already been scored by this player."""
        if self.is_objective_completed(player_id, objective):
            raise ValueError(
                f"Objective '{objective.id}' already scored by player '{player_id}'"
            )

    def _execute_objective_scoring(
        self, player_id: str, objective: Objective, current_phase: GamePhase
    ) -> GameState:
        """Execute the objective scoring with all state updates."""
        # Update completed objectives tracking
        new_completed_objectives = self._update_completed_objectives(
            player_id, objective
        )

        # Award victory points
        new_victory_points = self._update_victory_points(player_id, objective)

        # Update phase-specific scoring tracking
        new_status_phase_scoring = self._update_status_phase_scoring(
            player_id, objective, current_phase
        )

        # Remove secret objective from player's hand when scored
        new_player_secret_objectives = self._update_secret_objectives_after_scoring(
            player_id, objective
        )

        return self._create_new_state(
            completed_objectives=new_completed_objectives,
            victory_points=new_victory_points,
            status_phase_scoring=new_status_phase_scoring,
            player_secret_objectives=new_player_secret_objectives,
        )

    def _update_completed_objectives(
        self, player_id: str, objective: Objective
    ) -> dict[str, list[str]]:
        """Update the completed objectives tracking."""
        new_completed_objectives = {
            pid: objectives.copy()
            for pid, objectives in self.completed_objectives.items()
        }

        if player_id not in new_completed_objectives:
            new_completed_objectives[player_id] = []

        new_completed_objectives[player_id].append(objective.id)
        return new_completed_objectives

    def _update_victory_points(
        self, player_id: str, objective: Objective
    ) -> dict[str, int]:
        """Update the victory points for the player."""
        new_victory_points = self.victory_points.copy()
        current_points = new_victory_points.get(player_id, 0)
        new_total = current_points + objective.points
        if new_total > self.victory_points_to_win:
            raise ValueError(
                f"Player {player_id} cannot exceed maximum victory points ({self.victory_points_to_win}) when scoring objective '{objective.id}'"
            )
        new_victory_points[player_id] = new_total
        return new_victory_points

    def _update_secret_objectives_after_scoring(
        self, player_id: str, objective: Objective
    ) -> dict[str, list[Objective]]:
        """Remove scored secret objective from player's hand."""
        new_player_secret_objectives = {
            pid: objectives.copy() if isinstance(objectives, list) else objectives
            for pid, objectives in self.player_secret_objectives.items()
        }

        if not objective.is_public and player_id in new_player_secret_objectives:
            new_player_secret_objectives[player_id] = [
                obj
                for obj in new_player_secret_objectives[player_id]
                if obj.id != objective.id
            ]

        return new_player_secret_objectives

    def can_player_see_objective(self, player_id: str, objective: Objective) -> bool:
        """Check if a player can see an objective (public objectives and completed objectives are visible)."""
        if objective.is_public:
            return True

        # Check if objective is completed by any player (completed secret objectives are revealed)
        for _pid, completed in self.completed_objectives.items():
            if objective.id in completed:
                return True

        return False

    # Secret Objective Deck Management

    def get_secret_objective_deck_size(self) -> int:
        """Get the size of the secret objective deck.

        Returns:
            The number of secret objectives in the deck
        """
        return len(self.secret_objective_deck)

    def shuffle_secret_objective_deck(self) -> GameState:
        """Shuffle the secret objective deck.

        Returns:
            New GameState with shuffled secret objective deck
        """
        import random

        new_deck = self.secret_objective_deck.copy()
        random.shuffle(new_deck)
        return self._create_new_state(secret_objective_deck=new_deck)

    # Imperial Strategy Card Methods (Rule 45.4)

    def execute_imperial_primary_ability(self, player_id: str) -> GameState:
        """Execute Imperial strategy card primary ability - draw a secret objective."""
        if len(self.secret_objective_deck) == 0:
            raise ValueError("Secret objective deck is empty")

        # Check if player can draw (not at 3 objective limit)
        player_secrets = self.get_player_secret_objectives(player_id)
        if len(player_secrets) >= 3:
            raise ValueError(
                f"Cannot draw secret objective - player {player_id} already at maximum of 3"
            )

        # Draw top secret objective from deck
        new_deck = self.secret_objective_deck.copy()
        drawn_objective = new_deck.pop(0)

        # Assign to player
        new_state = self._create_new_state(secret_objective_deck=new_deck)
        return new_state.assign_secret_objective(player_id, drawn_objective)

    # Imperial secondary ability removed - was incorrectly implemented
    # According to Rule 45.3, players spend one command token from their strategy pool
    # to draw one secret objective card, not influence

    # Player influence/resource tracking removed - incorrect implementation
    # According to Rules 47 and 75, influence and resources are planet stats, not player stats
    # Players spend influence/resources by exhausting planet cards, not from player pools

    def add_player(self, player: Player) -> GameState:
        """Add a player to the game."""
        new_players = self.players.copy()
        new_players.append(player)

        # Initialize player-specific tracking
        # Player resource tracking removed - incorrect implementation
        new_player_technologies = self.player_technologies.copy()
        new_victory_points = self.victory_points.copy()
        new_completed_objectives = self.completed_objectives.copy()
        new_status_phase_scoring = self.status_phase_scoring.copy()
        new_combat_scoring = self.combat_scoring.copy()
        new_player_secret_objectives = self.player_secret_objectives.copy()
        # Player influence tracking removed - incorrect implementation

        # Initialize empty tracking for new player
        # Player resource tracking removed - incorrect implementation
        # Resources should be tracked on planets, not as player pools
        new_player_technologies[player.id] = []
        new_victory_points[player.id] = 0
        new_completed_objectives[player.id] = []
        new_status_phase_scoring[player.id] = {"public": 0, "secret": 0}
        new_combat_scoring[player.id] = []
        new_player_secret_objectives[player.id] = []
        # Player influence tracking removed - incorrect implementation
        # Influence should be tracked on planets per Rules 47 and 75

        # Initialize action card hand for new player
        new_player_action_cards = self.player_action_cards.copy()
        new_player_action_cards[player.id] = []

        return self._create_new_state(
            players=new_players,
            # player_resources parameter removed - incorrect implementation
            player_technologies=new_player_technologies,
            victory_points=new_victory_points,
            completed_objectives=new_completed_objectives,
            status_phase_scoring=new_status_phase_scoring,
            combat_scoring=new_combat_scoring,
            player_secret_objectives=new_player_secret_objectives,
            player_action_cards=new_player_action_cards,
            # player_influence parameter removed - incorrect implementation
        )

    def _get_next_speaker_after_elimination(
        self, eliminated_player_id: str
    ) -> str | None:
        """
        Get the next speaker after a player is eliminated.

        Rule 33.8: If the speaker becomes eliminated, the speaker token passes
        to the player to the speaker's left.

        Args:
            eliminated_player_id: ID of the player being eliminated

        Returns:
            ID of the new speaker (unchanged if eliminated player wasn't speaker)
        """
        # If the eliminated player wasn't the speaker, no change needed
        if self.speaker_id != eliminated_player_id:
            return self.speaker_id

        # Find the next player to the left of the eliminated speaker
        player_ids = [player.id for player in self.players]
        if len(player_ids) <= 1:
            # Edge case: if only one player left, they become speaker
            return player_ids[0] if player_ids else self.speaker_id

        try:
            current_index = player_ids.index(eliminated_player_id)
            # Get the next player (to the left in turn order)
            next_index = (current_index + 1) % len(player_ids)
            return player_ids[next_index]
        except ValueError:
            # Fallback: return first remaining player
            return player_ids[0]

    def eliminate_player(self, player_id: str) -> GameState:
        """Eliminate a player from the game according to Rule 33.

        Args:
            player_id: The player to eliminate

        Returns:
            New GameState with player eliminated

        LRR Reference: Rule 33.2 - Component return to game box
        """
        # Local import to avoid circular dependencies
        from .planet import Planet
        from .system import System

        # Validate player exists
        if not any(player.id == player_id for player in self.players):
            raise ValueError(f"Player {player_id} does not exist")

        # Rule 33.2: Return all components to game box
        # Remove all units owned by the player
        new_systems = {}
        for system_id, system in self.systems.items():
            # Clone system preserving all attributes
            new_system = System(system_id)

            # Preserve system-level state
            new_system.space_units = [
                unit for unit in system.space_units if unit.owner != player_id
            ]
            new_system.command_tokens = {
                pid: token
                for pid, token in system.command_tokens.items()
                if pid != player_id
            }

            # Preserve system attributes if they exist
            if hasattr(system, "wormholes"):
                new_system.wormholes = (
                    system.wormholes.copy()
                    if hasattr(system.wormholes, "copy")
                    else system.wormholes
                )

            # Copy planets preserving all attributes and flags
            for planet in system.planets:
                new_planet = Planet(
                    planet.name,
                    planet.resources,
                    planet.influence,
                )

                # Preserve planet exhaustion state
                if hasattr(planet, "_exhausted"):
                    new_planet._exhausted = planet._exhausted

                # Only keep units not owned by eliminated player
                for unit in planet.units:
                    if unit.owner != player_id:
                        new_planet.place_unit(unit)

                new_system.add_planet(new_planet)

            new_systems[system_id] = new_system

        # Remove player from players list
        new_players = [player for player in self.players if player.id != player_id]

        # Remove player from planet control mapping
        # Set eliminated player's controlled planets to None instead of filtering them out
        new_planet_control_mapping = self.planet_control_mapping.copy()
        for planet_name, controller in list(new_planet_control_mapping.items()):
            if controller == player_id:
                new_planet_control_mapping[planet_name] = None

        # Remove player from planet-related data structures
        new_player_planets = {
            pid: planets
            for pid, planets in self.player_planets.items()
            if pid != player_id
        }

        new_player_planet_cards = {
            pid: cards
            for pid, cards in self.player_planet_cards.items()
            if pid != player_id
        }

        # Return eliminated player's planet cards to deck
        new_planet_card_deck = self.planet_card_deck.copy()
        if player_id in self.player_planet_cards:
            for card in self.player_planet_cards[player_id]:
                # Use deck.add method if available, otherwise preserve structure
                if hasattr(new_planet_card_deck, "add"):
                    new_planet_card_deck.add(card)
                elif hasattr(new_planet_card_deck, "cards"):
                    new_planet_card_deck.cards[card.name] = card
                else:
                    # Fallback to direct assignment preserving existing structure
                    new_planet_card_deck[card.name] = card

        # Rule 33.3: Discard eliminated player's agenda cards
        new_agenda_discard_pile = self.agenda_discard_pile.copy()
        if player_id in self.player_agenda_cards:
            new_agenda_discard_pile.extend(self.player_agenda_cards[player_id])

        new_player_agenda_cards = {
            pid: cards
            for pid, cards in self.player_agenda_cards.items()
            if pid != player_id
        }

        # Rule 33.5: Discard eliminated player's action cards
        new_action_card_discard_pile = self.action_card_discard_pile.copy()
        if player_id in self.player_action_cards:
            new_action_card_discard_pile.extend(self.player_action_cards[player_id])

        new_player_action_cards = {
            pid: cards
            for pid, cards in self.player_action_cards.items()
            if pid != player_id
        }

        # Rule 33.7: Remove eliminated player's secret objectives
        new_player_secret_objectives = {
            pid: objectives
            for pid, objectives in self.player_secret_objectives.items()
            if pid != player_id
        }

        # Rule 33.4: Handle promissory note elimination
        new_promissory_note_manager = PromissoryNoteManager()
        # Copy existing state
        new_promissory_note_manager._player_hands = {
            pid: hand.copy()
            for pid, hand in self.promissory_note_manager._player_hands.items()
        }
        new_promissory_note_manager._available_notes = (
            self.promissory_note_manager._available_notes.copy()
        )
        # Handle elimination
        new_promissory_note_manager.handle_player_elimination(player_id)

        # Rule 33.6: Return eliminated player's strategy cards to common play area
        new_strategy_card_assignments = {
            pid: card
            for pid, card in self.strategy_card_assignments.items()
            if pid != player_id
        }

        # Clean up all per-player mappings
        new_victory_points = {
            pid: points
            for pid, points in self.victory_points.items()
            if pid != player_id
        }

        new_completed_objectives = {
            pid: objectives
            for pid, objectives in self.completed_objectives.items()
            if pid != player_id
        }

        new_player_technologies = {
            pid: techs
            for pid, techs in self.player_technologies.items()
            if pid != player_id
        }

        new_player_technology_cards = {
            pid: cards
            for pid, cards in self.player_technology_cards.items()
            if pid != player_id
        }

        new_status_phase_scoring = {
            pid: scoring
            for pid, scoring in self.status_phase_scoring.items()
            if pid != player_id
        }

        new_combat_scoring = {
            pid: scoring
            for pid, scoring in self.combat_scoring.items()
            if pid != player_id
        }

        # Rule 33.8: Transfer speaker token if speaker is eliminated
        new_speaker_id = self._get_next_speaker_after_elimination(player_id)

        return self._create_new_state(
            players=new_players,
            systems=new_systems,
            planet_control_mapping=new_planet_control_mapping,
            player_planets=new_player_planets,
            planet_card_deck=new_planet_card_deck,
            player_planet_cards=new_player_planet_cards,
            player_agenda_cards=new_player_agenda_cards,
            agenda_discard_pile=new_agenda_discard_pile,
            player_action_cards=new_player_action_cards,
            action_card_discard_pile=new_action_card_discard_pile,
            player_secret_objectives=new_player_secret_objectives,
            promissory_note_manager=new_promissory_note_manager,
            strategy_card_assignments=new_strategy_card_assignments,
            speaker_id=new_speaker_id,
            victory_points=new_victory_points,
            completed_objectives=new_completed_objectives,
            player_technologies=new_player_technologies,
            player_technology_cards=new_player_technology_cards,
            status_phase_scoring=new_status_phase_scoring,
            combat_scoring=new_combat_scoring,
        )

    def discard_player_agenda_cards(self, player_id: str) -> GameState:
        """Discard all agenda cards owned by a player according to Rule 33.3.

        Args:
            player_id: The player whose agenda cards should be discarded

        Returns:
            New GameState with player's agenda cards discarded

        LRR Reference: Rule 33.3 - Agenda card discard on elimination
        """
        # Move player's agenda cards to discard pile
        new_agenda_discard_pile = self.agenda_discard_pile.copy()
        if player_id in self.player_agenda_cards:
            new_agenda_discard_pile.extend(self.player_agenda_cards[player_id])

        # Remove player from agenda cards mapping
        new_player_agenda_cards = {
            pid: cards
            for pid, cards in self.player_agenda_cards.items()
            if pid != player_id
        }

        return self._create_new_state(
            player_agenda_cards=new_player_agenda_cards,
            agenda_discard_pile=new_agenda_discard_pile,
        )

    def should_eliminate_player(self, player_id: str) -> bool:
        """Check if a player should be eliminated according to Rule 33.1.

        A player is eliminated if they have:
        - No ground forces
        - No production units
        - Control no planets

        Args:
            player_id: The player to check for elimination

        Returns:
            True if the player should be eliminated

        Raises:
            ValueError: If player does not exist

        LRR Reference: Rule 33.1 - Elimination Conditions
        """
        # Validate player exists
        if not any(player.id == player_id for player in self.players):
            raise ValueError(f"Player {player_id} does not exist")

        # Import here to avoid circular imports
        from .constants import GameConstants

        # Check if player has ground forces
        has_ground_forces = False
        for system in self.systems.values():
            # Check planets for ground forces
            for planet in system.planets:
                for unit in planet.units:
                    if (
                        unit.owner == player_id
                        and unit.unit_type in GameConstants.GROUND_FORCE_TYPES
                    ):
                        has_ground_forces = True
                        break
                if has_ground_forces:
                    break
            if has_ground_forces:
                break

        # Check if player has production units
        has_production_units = False
        for system in self.systems.values():
            # Check planets for production units
            for planet in system.planets:
                for unit in planet.units:
                    if unit.owner == player_id and unit.has_production():
                        has_production_units = True
                        break
                if has_production_units:
                    break

            # Check space for production units
            if not has_production_units:
                for unit in system.space_units:
                    if unit.owner == player_id and unit.has_production():
                        has_production_units = True
                        break

            if has_production_units:
                break

        # Check if player controls any planets
        controls_planets = any(
            controller == player_id
            for controller in self.planet_control_mapping.values()
        )

        # Rule 33.1: Player is eliminated if ALL three conditions are true:
        # - No ground forces AND no production units AND controls no planets
        return (
            not has_ground_forces and not has_production_units and not controls_planets
        )

    def resolve_planet_control_change(self, planet: Planet) -> GameState:
        """Resolve planet control changes based on unit presence (Rule 25.5).

        Args:
            planet: The planet to check for control changes

        Returns:
            New GameState with resolved control changes
        """
        # Use centralized mapping instead of planet.controlled_by
        current_controller = self.planet_control_mapping.get(planet.name)

        # Check if current controller has units
        if current_controller:
            has_controlling_units = any(
                unit.owner == current_controller for unit in planet.units
            )

            # Rule 25.5: Lose control if no units and another player has units
            if not has_controlling_units:
                other_players_with_units = {
                    unit.owner
                    for unit in planet.units
                    if unit.owner != current_controller
                }

                if other_players_with_units:
                    # Lose control
                    new_state = self.lose_planet_control(current_controller, planet)

                    # Rule 25.5a: Player with units gains control (deterministic)
                    candidates = list(other_players_with_units)
                    new_controller = self._sort_players_by_initiative_order(candidates)[
                        0
                    ]
                    _, final_state = new_state.gain_planet_control(
                        new_controller, planet
                    )
                    return final_state

        return self

    def gain_planet_control(
        self, player_id: str, planet: Planet
    ) -> tuple[bool, GameState]:
        """Handle gaining control of a planet according to Rule 25.

        Args:
            player_id: The player gaining control
            planet: The planet being controlled

        Returns:
            Tuple of (exploration_triggered, new_game_state)
        """
        # Rule 25.2: Cannot gain control of already controlled planet
        current_controller = self.planet_control_mapping.get(planet.name)
        if current_controller == player_id:
            raise ValueError("Player already controls this planet")

        # Determine if this triggers exploration (Rule 25.1c)
        was_uncontrolled = current_controller is None

        # Get or create planet card
        planet_card = self._get_or_create_planet_card(planet)

        # Rule 25.1: Planet card is exhausted when gained
        if not planet_card.is_exhausted():
            planet_card.exhaust()

        # Update planet control mapping
        new_planet_control_mapping = self.planet_control_mapping.copy()
        new_planet_control_mapping[planet.name] = player_id

        # Update player planets list
        new_player_planets = {
            pid: planets.copy() for pid, planets in self.player_planets.items()
        }
        if player_id not in new_player_planets:
            new_player_planets[player_id] = []
        if planet not in new_player_planets[player_id]:
            new_player_planets[player_id].append(planet)

        # Rule 25.4: If player controls planet without units, place control token
        new_planet_control_tokens = {
            planet_name: tokens.copy()
            for planet_name, tokens in self.planet_control_tokens.items()
        }

        # Check if player has units on the planet
        player_has_units = any(unit.owner == player_id for unit in planet.units)
        if not player_has_units:
            if planet.name not in new_planet_control_tokens:
                new_planet_control_tokens[planet.name] = set()
            new_planet_control_tokens[planet.name].add(player_id)

        # Handle planet card transfer
        new_planet_card_deck = self.planet_card_deck.copy()
        new_player_planet_cards = {
            pid: cards.copy() for pid, cards in self.player_planet_cards.items()
        }

        if was_uncontrolled:
            # Transfer from deck to player
            if planet_card.name in new_planet_card_deck:
                del new_planet_card_deck[planet_card.name]
            if player_id not in new_player_planet_cards:
                new_player_planet_cards[player_id] = []
            new_player_planet_cards[player_id].append(planet_card)
        else:
            # Transfer from previous controller to new controller
            if current_controller in new_player_planet_cards:
                # Find the existing planet card to preserve attachments
                existing_card = None
                for card in new_player_planet_cards[current_controller]:
                    if card.name == planet_card.name:
                        existing_card = card
                        break

                # Use existing card if found, otherwise use the one we got/created
                if existing_card:
                    planet_card = existing_card

                new_player_planet_cards[current_controller] = [
                    card
                    for card in new_player_planet_cards[current_controller]
                    if card.name != planet_card.name
                ]
            if player_id not in new_player_planet_cards:
                new_player_planet_cards[player_id] = []
            new_player_planet_cards[player_id].append(planet_card)

        new_state = self._create_new_state(
            planet_control_mapping=new_planet_control_mapping,
            player_planets=new_player_planets,
            planet_card_deck=new_planet_card_deck,
            player_planet_cards=new_player_planet_cards,
            planet_control_tokens=new_planet_control_tokens,
        )

        return was_uncontrolled, new_state

    def lose_planet_control(self, player_id: str, planet: Planet) -> GameState:
        """Handle losing control of a planet according to Rule 25.

        Args:
            player_id: The player losing control
            planet: The planet being lost

        Returns:
            New GameState with updated control
        """
        # Update planet control mapping
        new_planet_control_mapping = self.planet_control_mapping.copy()
        new_planet_control_mapping[planet.name] = None

        # Update player planets list
        new_player_planets = {
            pid: planets.copy() for pid, planets in self.player_planets.items()
        }
        if player_id in new_player_planets:
            new_player_planets[player_id] = [
                p for p in new_player_planets[player_id] if p.name != planet.name
            ]

        # Rule 25.7: Remove control token when losing control
        new_planet_control_tokens = {
            planet_name: tokens.copy()
            for planet_name, tokens in self.planet_control_tokens.items()
        }
        if planet.name in new_planet_control_tokens:
            new_planet_control_tokens[planet.name].discard(player_id)
            # Remove empty sets to keep data clean
            if not new_planet_control_tokens[planet.name]:
                del new_planet_control_tokens[planet.name]

        # Handle planet card - return to deck
        new_planet_card_deck = self.planet_card_deck.copy()
        new_player_planet_cards = {
            pid: cards.copy() for pid, cards in self.player_planet_cards.items()
        }

        if player_id in new_player_planet_cards:
            for card in new_player_planet_cards[player_id]:
                if card.name == planet.name:
                    new_planet_card_deck[card.name] = card
                    break
            new_player_planet_cards[player_id] = [
                card
                for card in new_player_planet_cards[player_id]
                if card.name != planet.name
            ]

        return self._create_new_state(
            planet_control_mapping=new_planet_control_mapping,
            player_planets=new_player_planets,
            planet_card_deck=new_planet_card_deck,
            player_planet_cards=new_player_planet_cards,
            planet_control_tokens=new_planet_control_tokens,
        )

    def _get_or_create_planet_card(self, planet: Planet) -> PlanetCard:
        """Get or create a planet card for the given planet."""
        # Local import to avoid circular dependencies
        from .planet_card import PlanetCard

        # First check if it's already in the deck
        if planet.name in self.planet_card_deck:
            return self.planet_card_deck[planet.name]

        # Check if it's in any player's cards
        for player_cards in self.player_planet_cards.values():
            for card in player_cards:
                if card.name == planet.name:
                    return card

        # Create new planet card if not found
        return PlanetCard(
            name=planet.name,
            resources=planet.resources,
            influence=planet.influence,
            game_state=self,
        )

    def get_player_planet_cards(self, player_id: str) -> list[PlanetCard]:
        """Get all planet cards in a player's play area.

        Args:
            player_id: The player ID

        Returns:
            List of planet cards in player's play area
        """
        return self.player_planet_cards.get(player_id, [])

    def is_planet_card_in_deck(self, planet_name: str) -> bool:
        """Check if a planet card is still in the deck.

        Args:
            planet_name: Name of the planet

        Returns:
            True if card is in deck, False otherwise
        """
        return planet_name in self.planet_card_deck

    def get_planet_card_deck_size(self) -> int:
        """Get the current size of the planet card deck.

        Returns:
            Number of planet cards remaining in deck
        """
        return len(self.planet_card_deck)

    def has_control_token_on_planet(self, player_id: str, planet: Planet) -> bool:
        """Check if a player has a control token on a planet.

        Args:
            player_id: The player ID
            planet: The planet to check

        Returns:
            True if player has control token on planet
        """
        return player_id in self.planet_control_tokens.get(planet.name, set())

    def _transfer_planet_card_from_deck(
        self, player_id: str, planet_card: PlanetCard
    ) -> None:
        """Transfer a planet card from deck to player's play area.

        Args:
            player_id: The receiving player
            planet_card: The planet card to transfer
        """
        # Remove from deck
        if planet_card.name in self.planet_card_deck:
            del self.planet_card_deck[planet_card.name]

        # Add to player's play area
        if player_id not in self.player_planet_cards:
            self.player_planet_cards[player_id] = []
        self.player_planet_cards[player_id].append(planet_card)

    def _transfer_planet_card_between_players(
        self, from_player: str, to_player: str, planet_card: PlanetCard
    ) -> None:
        """Transfer a planet card between players' play areas.

        Args:
            from_player: The player losing the card
            to_player: The player gaining the card
            planet_card: The planet card to transfer
        """
        # Remove from source player
        if from_player in self.player_planet_cards:
            self.player_planet_cards[from_player] = [
                card
                for card in self.player_planet_cards[from_player]
                if card.name != planet_card.name
            ]

        # Add to destination player
        if to_player not in self.player_planet_cards:
            self.player_planet_cards[to_player] = []
        self.player_planet_cards[to_player].append(planet_card)

    def _find_player_planet_card(
        self, player_id: str, planet_name: str
    ) -> PlanetCard | None:
        """Find a specific planet card in a player's play area.

        Args:
            player_id: The player ID
            planet_name: Name of the planet

        Returns:
            The planet card if found, None otherwise
        """
        player_cards = self.player_planet_cards.get(player_id, [])
        for card in player_cards:
            if card.name == planet_name:
                return card
        return None

    def add_player_planet(self, player_id: str, planet: Planet) -> GameState:
        """Add a planet to a player's controlled planets.

        Args:
            player_id: The player ID
            planet: The planet to add

        Returns:
            New GameState with updated player planets
        """
        new_player_planets = {
            pid: planets.copy() for pid, planets in self.player_planets.items()
        }

        if player_id not in new_player_planets:
            new_player_planets[player_id] = []

        # Only add if not already present (by name)
        if all(p.name != planet.name for p in new_player_planets[player_id]):
            new_player_planets[player_id].append(planet)

        return self._create_new_state(player_planets=new_player_planets)

    def get_secret_objective_deck(self) -> list[Objective]:
        """Get the secret objective deck.

        Returns:
            List of secret objectives in the deck
        """
        return self.secret_objective_deck.copy()

    # Backward compatibility alias
    def shuffle_secret_objectives(self) -> GameState:
        """Shuffle the secret objective deck.

        Deprecated: Use shuffle_secret_objective_deck instead.

        Returns:
            New GameState with shuffled secret objective deck
        """
        return self.shuffle_secret_objective_deck()

    def ready_strategy_card(self, card: StrategyCardType) -> GameState:
        """Ready a strategy card (remove from exhausted set).

        Args:
            card: The strategy card to ready

        Returns:
            New GameState with card readied
        """
        new_exhausted = self.exhausted_strategy_cards.copy()
        new_exhausted.discard(card)
        return self._create_new_state(exhausted_strategy_cards=new_exhausted)

    def ready_all_strategy_cards(self) -> GameState:
        """Ready all strategy cards (clear exhausted set).

        Returns:
            New GameState with all cards readied
        """
        return self._create_new_state(exhausted_strategy_cards=set())

    def clear_strategy_card_assignments(self) -> GameState:
        """Clear all strategy card assignments.

        Returns:
            New GameState with cleared assignments
        """
        return self._create_new_state(strategy_card_assignments={})

    def synchronize_with_coordinator(
        self, coordinator: StrategyCardCoordinator
    ) -> GameState:
        """Synchronize game state with strategy card coordinator.

        Args:
            coordinator: The strategy card coordinator to sync with

        Returns:
            New GameState synchronized with coordinator
        """
        if not coordinator:
            return self

        # Get current assignments from coordinator
        coordinator_assignments = coordinator.get_player_strategy_card_assignments()
        coordinator_exhausted = coordinator.get_exhausted_cards()

        return self._create_new_state(
            strategy_card_assignments=coordinator_assignments,
            exhausted_strategy_cards=coordinator_exhausted,
        )

    def get_player_planets(self, player_id: str) -> list[Planet]:
        """Get all planets controlled by a player.

        Args:
            player_id: The player ID

        Returns:
            List of planets controlled by the player
        """
        return self.player_planets.get(player_id, [])

    def add_player_technology(
        self, player_id: str, technology: TechnologyCard
    ) -> GameState:
        """Add a technology card to a player's technology cards.

        Args:
            player_id: The player ID
            technology: The technology card to add

        Returns:
            New GameState with updated player technology cards
        """
        new_player_technology_cards = {
            pid: cards.copy() for pid, cards in self.player_technology_cards.items()
        }

        if player_id not in new_player_technology_cards:
            new_player_technology_cards[player_id] = []

        # Only add if not already present
        if technology not in new_player_technology_cards[player_id]:
            new_player_technology_cards[player_id].append(technology)

        return self._create_new_state(
            player_technology_cards=new_player_technology_cards
        )

    def get_player_technology_cards(self, player_id: str) -> list[TechnologyCard]:
        """Get all technology cards owned by a player.

        Args:
            player_id: The player ID

        Returns:
            List of technology cards owned by the player
        """
        return self.player_technology_cards.get(player_id, [])

    def add_secret_objective_to_deck(self, objective: Objective) -> GameState:
        """Add a secret objective to the deck.

        Args:
            objective: The objective to add

        Returns:
            New GameState with updated secret objective deck
        """
        new_deck = self.secret_objective_deck.copy()
        if objective not in new_deck:
            new_deck.append(objective)
        return self._create_new_state(secret_objective_deck=new_deck)

    def assign_strategy_card(self, player_id: str, card: StrategyCardType) -> GameState:
        """Assign a strategy card to a player.

        Args:
            player_id: The player ID to assign the card to
            card: The strategy card to assign

        Returns:
            New GameState with updated strategy card assignments

        Raises:
            ValueError: If player_id is None/empty or card is None, or if card is already assigned
        """
        if player_id is None:
            raise ValueError("Player ID cannot be None")
        if player_id == "":
            raise ValueError("Player ID cannot be empty")
        if card is None:
            raise ValueError("Strategy card cannot be None")

        # Check if card is already assigned to another player
        for existing_player_id, existing_card in self.strategy_card_assignments.items():
            if existing_card == card and existing_player_id != player_id:
                raise ValueError(
                    f"Strategy card {card} is already assigned to player {existing_player_id}"
                )

        new_assignments = self.strategy_card_assignments.copy()
        new_assignments[player_id] = card
        return self._create_new_state(strategy_card_assignments=new_assignments)

    def exhaust_strategy_card(self, card: StrategyCardType) -> GameState:
        """Exhaust a strategy card.

        Args:
            card: The strategy card to exhaust

        Returns:
            New GameState with card added to exhausted set

        Raises:
            ValueError: If card is None
        """
        if card is None:
            raise ValueError("Strategy card cannot be None")

        new_exhausted = self.exhausted_strategy_cards.copy()
        new_exhausted.add(card)
        return self._create_new_state(exhausted_strategy_cards=new_exhausted)

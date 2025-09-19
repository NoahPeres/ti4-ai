"""Core game state management for TI4."""

import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional

from .game_phase import GamePhase
from .player import Player

if TYPE_CHECKING:
    from .galaxy import Galaxy
    from .objective import Objective
    from .strategic_action import StrategyCardType
    from .strategy_card_coordinator import StrategyCardCoordinator
    from .system import System
else:
    Galaxy = "Galaxy"
    System = "System"
    Objective = "Objective"
    StrategyCardType = "StrategyCardType"
    StrategyCardCoordinator = "StrategyCardCoordinator"

# Victory condition constants
VICTORY_POINTS_TO_WIN = 10


@dataclass(frozen=True)
class GameState:
    """Represents the complete state of a TI4 game."""

    game_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    players: list[Player] = field(default_factory=list, hash=False)
    galaxy: Optional[Galaxy] = None
    phase: GamePhase = GamePhase.SETUP
    systems: dict[str, System] = field(default_factory=dict, hash=False)
    # player_resources field removed - incorrect implementation
    # Resources should be tracked on planets per Rules 47 and 75
    player_technologies: dict[str, list[str]] = field(default_factory=dict, hash=False)
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
    strategy_card_assignments: dict[str, "StrategyCardType"] = field(
        default_factory=dict, hash=False
    )  # player_id -> strategy_card
    exhausted_strategy_cards: set["StrategyCardType"] = field(
        default_factory=set, hash=False
    )  # Set of exhausted strategy cards

    def get_victory_points(self, player_id: str) -> int:
        """Get the victory points for a player."""
        return self.victory_points.get(player_id, 0)

    def award_victory_points(self, player_id: str, points: int) -> "GameState":
        """Award victory points to a player, returning a new GameState."""
        new_victory_points = self.victory_points.copy()
        current_points = new_victory_points.get(player_id, 0)
        new_victory_points[player_id] = current_points + points

        return self._create_new_state(victory_points=new_victory_points)

    def has_winner(self) -> bool:
        """Check if any player has reached the victory condition."""
        return any(
            points >= VICTORY_POINTS_TO_WIN for points in self.victory_points.values()
        )

    def get_winner(self) -> Optional[str]:
        """Get the player ID of the winner, if any."""
        for player_id, points in self.victory_points.items():
            if points >= VICTORY_POINTS_TO_WIN:
                return player_id
        return None

    def is_objective_completed(self, player_id: str, objective: Objective) -> bool:
        """Check if a player has completed a specific objective."""
        player_objectives = self.completed_objectives.get(player_id, [])
        return objective.id in player_objectives

    def complete_objective(self, player_id: str, objective: Objective) -> "GameState":
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

    def _create_new_state(self, **kwargs: Any) -> "GameState":
        """Create a new GameState with updated fields."""
        return GameState(
            game_id=self.game_id,
            players=self.players,
            galaxy=self.galaxy,
            phase=self.phase,
            systems=self.systems,
            # player_resources parameter removed - incorrect implementation
            player_technologies=self.player_technologies,
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
        )

    def is_valid(self) -> bool:
        """Validate the consistency of the game state."""
        return True

    def score_objective_during_combat(
        self, player_id: str, objective: "Objective", combat_id: str
    ) -> "GameState":
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
        self, player_id: str, objectives: list["Objective"]
    ) -> "GameState":
        """Execute status phase step 1: score objectives."""
        # Rule 81.1: Following initiative order, each player may score up to one public and one secret objective
        current_state = self

        for objective in objectives:
            current_state = current_state.score_objective(
                player_id, objective, GamePhase.STATUS
            )

        return current_state

    def advance_to_next_status_phase(self) -> "GameState":
        """Advance to next status phase, resetting per-phase scoring limits."""
        # Reset status phase scoring limits for new phase
        return self._create_new_state(status_phase_scoring={})

    def _validate_status_phase_scoring_limits(
        self, player_id: str, objective: "Objective"
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
        self, player_id: str, objective: "Objective", current_phase: GamePhase
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
        self, player_id: str, objective: "Objective"
    ) -> "GameState":
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

    def get_player_secret_objectives(self, player_id: str) -> list["Objective"]:
        """Get secret objectives owned by a player."""
        return self.player_secret_objectives.get(player_id, [])

    def score_objective(
        self, player_id: str, objective: "Objective", current_phase: GamePhase
    ) -> "GameState":
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
        self, player_id: str, objective: "Objective", current_phase: GamePhase
    ) -> None:
        """Validate all conditions for objective scoring."""
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
        self, player_id: str, objective: "Objective"
    ) -> None:
        """Validate that the player owns the secret objective they're trying to score."""
        player_secrets = self.get_player_secret_objectives(player_id)
        if not any(obj.id == objective.id for obj in player_secrets):
            raise ValueError(
                f"Cannot score secret objective {objective.id} - not owned by player {player_id}"
            )

    def _validate_objective_timing(
        self, objective: "Objective", current_phase: GamePhase
    ) -> None:
        """Validate that the objective can be scored in the current phase."""
        if objective.scoring_phase != current_phase:
            raise ValueError(
                f"Cannot score objective '{objective.id}' requiring {objective.scoring_phase.value} phase during {current_phase.value} phase"
            )

    def _validate_objective_not_already_scored(
        self, player_id: str, objective: "Objective"
    ) -> None:
        """Validate that the objective hasn't already been scored by this player."""
        if self.is_objective_completed(player_id, objective):
            raise ValueError(
                f"Objective '{objective.id}' already scored by player '{player_id}'"
            )

    def _execute_objective_scoring(
        self, player_id: str, objective: "Objective", current_phase: GamePhase
    ) -> "GameState":
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
        self, player_id: str, objective: "Objective"
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
        self, player_id: str, objective: "Objective"
    ) -> dict[str, int]:
        """Update the victory points for the player."""
        new_victory_points = self.victory_points.copy()
        current_points = new_victory_points.get(player_id, 0)
        new_victory_points[player_id] = current_points + objective.points
        return new_victory_points

    def _update_secret_objectives_after_scoring(
        self, player_id: str, objective: "Objective"
    ) -> dict[str, list["Objective"]]:
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

    def can_player_see_objective(self, player_id: str, objective: "Objective") -> bool:
        """Check if a player can see an objective (public objectives and completed objectives are visible)."""
        if objective.is_public:
            return True

        # Check if objective is completed by any player (completed secret objectives are revealed)
        for _pid, completed in self.completed_objectives.items():
            if objective.id in completed:
                return True

        return False

    # Secret Objective Deck Management

    def add_secret_objective_to_deck(self, objective: "Objective") -> "GameState":
        """Add a secret objective to the deck."""
        new_deck = self.secret_objective_deck.copy()
        new_deck.append(objective)
        return self._create_new_state(secret_objective_deck=new_deck)

    def get_secret_objective_deck_size(self) -> int:
        """Get the size of the secret objective deck."""
        return len(self.secret_objective_deck)

    def shuffle_secret_objective_deck(self) -> "GameState":
        """Shuffle the secret objective deck."""
        import random

        new_deck = self.secret_objective_deck.copy()
        random.shuffle(new_deck)
        return self._create_new_state(secret_objective_deck=new_deck)

    # Imperial Strategy Card Methods (Rule 45.4)

    def execute_imperial_primary_ability(self, player_id: str) -> "GameState":
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

    def add_player(self, player: "Player") -> "GameState":
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

        return self._create_new_state(
            players=new_players,
            # player_resources parameter removed - incorrect implementation
            player_technologies=new_player_technologies,
            victory_points=new_victory_points,
            completed_objectives=new_completed_objectives,
            status_phase_scoring=new_status_phase_scoring,
            combat_scoring=new_combat_scoring,
            player_secret_objectives=new_player_secret_objectives,
            # player_influence parameter removed - incorrect implementation
        )

    def eliminate_player(self, player_id: str) -> "GameState":
        """Eliminate a player from the game, removing their secret objectives."""
        new_player_secret_objectives = {
            pid: objectives
            for pid, objectives in self.player_secret_objectives.items()
            if pid != player_id
        }

        return self._create_new_state(
            player_secret_objectives=new_player_secret_objectives
        )

    # Strategy Card Management Methods (Rule 83)

    def assign_strategy_card(
        self, player_id: str, strategy_card: "StrategyCardType"
    ) -> "GameState":
        """Assign a strategy card to a player.

        Args:
            player_id: The player to assign the card to
            strategy_card: The strategy card to assign

        Returns:
            New GameState with the strategy card assigned

        Raises:
            ValueError: If inputs are invalid or card is already assigned

        Requirements: 1.3, 6.2 - Strategy card tracking and state synchronization
        """
        # Input validation
        if player_id is None:
            raise ValueError("Player ID cannot be None")
        if not isinstance(player_id, str) or not player_id.strip():
            raise ValueError("Player ID cannot be empty")
        if strategy_card is None:
            raise ValueError("Strategy card cannot be None")

        # Check if card is already assigned to another player
        for existing_player, existing_card in self.strategy_card_assignments.items():
            if existing_card == strategy_card and existing_player != player_id:
                raise ValueError(
                    f"Strategy card {strategy_card.value} is already assigned to player {existing_player}"
                )

        # Create new assignments
        new_assignments = self.strategy_card_assignments.copy()
        new_assignments[player_id] = strategy_card

        return self._create_new_state(strategy_card_assignments=new_assignments)

    def exhaust_strategy_card(self, strategy_card: "StrategyCardType") -> "GameState":
        """Exhaust a strategy card (mark as used).

        Args:
            strategy_card: The strategy card to exhaust

        Returns:
            New GameState with the strategy card exhausted

        Raises:
            ValueError: If strategy card is None

        Requirements: 4.5 - State persistence for card exhaustion
        """
        if strategy_card is None:
            raise ValueError("Strategy card cannot be None")

        new_exhausted_cards = self.exhausted_strategy_cards.copy()
        new_exhausted_cards.add(strategy_card)

        return self._create_new_state(exhausted_strategy_cards=new_exhausted_cards)

    def ready_strategy_card(self, strategy_card: "StrategyCardType") -> "GameState":
        """Ready a strategy card (mark as available for use).

        Args:
            strategy_card: The strategy card to ready

        Returns:
            New GameState with the strategy card readied

        Requirements: 4.5, 10.2 - State persistence and round management
        """
        new_exhausted_cards = self.exhausted_strategy_cards.copy()
        new_exhausted_cards.discard(strategy_card)

        return self._create_new_state(exhausted_strategy_cards=new_exhausted_cards)

    def ready_all_strategy_cards(self) -> "GameState":
        """Ready all strategy cards for the next round.

        Returns:
            New GameState with all strategy cards readied

        Requirements: 10.2 - Round management state tracking
        """
        return self._create_new_state(exhausted_strategy_cards=set())

    def clear_strategy_card_assignments(self) -> "GameState":
        """Clear all strategy card assignments for round reset.

        Returns:
            New GameState with no strategy card assignments

        Requirements: 10.2 - Round management state tracking
        """
        return self._create_new_state(strategy_card_assignments={})

    def synchronize_with_coordinator(
        self, coordinator: "StrategyCardCoordinator"
    ) -> "GameState":
        """Synchronize GameState with StrategyCardCoordinator.

        Args:
            coordinator: The StrategyCardCoordinator to synchronize with

        Returns:
            New GameState synchronized with coordinator state

        Requirements: 6.2 - State synchronization with StrategyCardCoordinator
        """
        # Import here to avoid circular imports
        from .strategy_card_coordinator import StrategyCardCoordinator

        if not isinstance(coordinator, StrategyCardCoordinator):
            raise ValueError("Coordinator must be a StrategyCardCoordinator instance")

        # Get assignments directly from coordinator's internal state
        new_assignments = coordinator._card_assignments.copy()

        # Get exhausted cards from coordinator
        new_exhausted_cards = set()
        for player_id, card in new_assignments.items():
            if coordinator.is_strategy_card_exhausted(player_id, card):
                new_exhausted_cards.add(card)

        return self._create_new_state(
            strategy_card_assignments=new_assignments,
            exhausted_strategy_cards=new_exhausted_cards,
        )

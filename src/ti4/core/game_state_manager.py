"""Centralized game state management for TI4."""

from dataclasses import dataclass, field
from typing import Optional

from .fleet import Fleet
from .galaxy import Galaxy
from .game_phase import GamePhase
from .player import Player
from .strategy_card import StrategyCard
from .system import System
from .unit_stats import UnitStatsProvider


@dataclass
class PlayerState:
    """Represents the complete state of a player."""

    player: Player
    tactic_tokens: int = 3  # For tactical actions (TI4 rules 20.1)
    fleet_tokens: int = 3  # For fleet supply - max number of fleets
    strategy_tokens: int = 2  # For secondary abilities
    strategy_cards: list[StrategyCard] = field(default_factory=list)
    technologies: set[str] = field(default_factory=set)
    fleets: list[Fleet] = field(default_factory=list)
    resources: int = 0
    influence: int = 0


@dataclass
class GameState:
    """Represents the complete state of a TI4 game."""

    players: dict[str, PlayerState] = field(default_factory=dict)
    galaxy: Optional[Galaxy] = None
    systems: dict[str, System] = field(default_factory=dict)
    current_phase: GamePhase = GamePhase.SETUP
    current_player_index: int = 0
    round_number: int = 1
    unit_stats_provider: UnitStatsProvider = field(default_factory=UnitStatsProvider)

    def get_current_player(self) -> Optional[PlayerState]:
        """Get the currently active player state."""
        if not self.players:
            return None
        player_ids = list(self.players.keys())
        if 0 <= self.current_player_index < len(player_ids):
            return self.players[player_ids[self.current_player_index]]
        return None

    def get_player_state(self, player_id: str) -> Optional[PlayerState]:
        """Get the state for a specific player."""
        return self.players.get(player_id)

    def add_player(self, player: Player) -> None:
        """Add a player to the game."""
        self.players[player.id] = PlayerState(player=player)

    def get_turn_order(self) -> list[str]:
        """Get the current turn order (player IDs)."""
        return list(self.players.keys())


class GameStateManager:
    """Manages game state transitions and validation."""

    def __init__(self, game_state: Optional[GameState] = None):
        """Initialize with optional existing game state."""
        self.game_state = game_state or GameState()

    def validate_state(self) -> list[str]:
        """Validate the current game state and return any errors."""
        errors = []

        # Validate player states
        for player_id, player_state in self.game_state.players.items():
            player_errors = self._validate_player_state(player_state)
            errors.extend([f"Player {player_id}: {error}" for error in player_errors])

        # Validate phase-specific rules
        phase_errors = self._validate_phase_rules()
        errors.extend(phase_errors)

        return errors

    def _validate_player_state(self, player_state: PlayerState) -> list[str]:
        """Validate a single player's state."""
        errors = []

        # Validate fleet supply (fleet pool tokens)
        fleets_requiring_supply = sum(
            1 for fleet in player_state.fleets if fleet.requires_fleet_supply()
        )
        if fleets_requiring_supply > player_state.fleet_tokens:
            errors.append(
                f"Fleet supply exceeded: {fleets_requiring_supply} > {player_state.fleet_tokens}"
            )

        # Validate fleet capacity
        for i, fleet in enumerate(player_state.fleets):
            if fleet.get_carried_units_count() > fleet.get_total_capacity():
                errors.append(f"Fleet {i} capacity exceeded")

        return errors

    def _validate_phase_rules(self) -> list[str]:
        """Validate phase-specific rules."""
        errors = []

        if self.game_state.current_phase == GamePhase.STRATEGY:
            # All players should have strategy cards
            for player_id, player_state in self.game_state.players.items():
                if not player_state.strategy_cards:
                    errors.append(
                        f"Player {player_id} missing strategy card in strategy phase"
                    )

        return errors

    def transition_to_phase(self, new_phase: GamePhase) -> bool:
        """Attempt to transition to a new phase."""
        # Validate current state before transition
        errors = self.validate_state()
        if errors:
            return False

        # Perform phase-specific cleanup/setup
        self._cleanup_phase(self.game_state.current_phase)
        self.game_state.current_phase = new_phase
        self._setup_phase(new_phase)

        return True

    def _cleanup_phase(self, phase: GamePhase) -> None:
        """Cleanup when leaving a phase."""
        if phase == GamePhase.STRATEGY:
            # Reset turn order based on strategy cards
            self._update_turn_order_by_initiative()

    def _setup_phase(self, phase: GamePhase) -> None:
        """Setup when entering a phase."""
        if phase == GamePhase.ACTION:
            # Reset action phase state
            self.game_state.current_player_index = 0

    def _update_turn_order_by_initiative(self) -> None:
        """Update turn order based on strategy card initiative."""
        player_initiatives = []
        for player_id, player_state in self.game_state.players.items():
            if player_state.strategy_cards:
                min_initiative = min(
                    card.initiative for card in player_state.strategy_cards
                )
                player_initiatives.append((player_id, min_initiative))

        # Sort by initiative and update player order
        player_initiatives.sort(key=lambda x: x[1])

        # This would require restructuring the players dict to maintain order
        # For now, we'll keep it simple

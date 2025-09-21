"""Game controller for managing TI4 game flow."""

# Import for type hints
from typing import TYPE_CHECKING, Any, Optional, Union

from src.ti4.commands.base import GameCommand
from src.ti4.commands.manager import CommandManager
from src.ti4.core.events import create_phase_changed_event
from src.ti4.core.exceptions import InvalidPlayerError
from src.ti4.core.game_phase import GamePhase
from src.ti4.core.game_state_machine import GameStateMachine
from src.ti4.core.player import Player
from src.ti4.core.strategy_card import STANDARD_STRATEGY_CARDS, StrategyCard
from src.ti4.core.validation import ValidationError

if TYPE_CHECKING:
    from src.ti4.core.strategy_cards.strategic_action import StrategyCardType


class GameController:
    """Manages game flow and turn order for TI4."""

    def __init__(self, players: list[Player]) -> None:
        """Initialize the game controller with players."""
        if not players:
            raise InvalidPlayerError("At least one player is required")
        if len(players) < 3:
            raise InvalidPlayerError("At least 3 players are required for TI4")
        self._players = players
        self._current_player_index = 0
        self._state_machine = GameStateMachine()
        self._available_strategy_cards = list(STANDARD_STRATEGY_CARDS)
        self._selected_strategy_cards: dict[str, list[StrategyCard]] = {}
        self._consecutive_passes = 0
        self._command_manager = CommandManager()
        self._event_bus: Optional[Any] = None
        self._game_id = "default_game"  # TODO: Make this configurable
        self._round_number = 1
        self._current_game_state: Optional[Any] = None  # Will be set when game starts
        self._passed_players: set[str] = set()  # Track players who have passed
        self._strategic_actions_taken: dict[
            str, set[int]
        ] = {}  # Track strategic actions taken by player
        self._actions_taken_this_turn: set[str] = set()
        # Dynamic strategy card type to ID mapping derived from STANDARD_STRATEGY_CARDS
        self._strategy_card_type_to_id = {
            c.name.lower(): c.id for c in STANDARD_STRATEGY_CARDS
        }

    def get_turn_order(self) -> list[Player]:
        """Get the current turn order."""
        return self._players

    def get_current_player(self) -> Player:
        """Get the currently active player."""
        return self._players[self._current_player_index]

    def advance_turn(self) -> None:
        """Advance to the next player's turn."""
        # Clear actions taken this turn when advancing
        self._actions_taken_this_turn.clear()

        # If all players have passed, don't advance
        if self.is_action_phase_complete():
            return

        # Find next player who hasn't passed using for-loop with else clause
        for _ in range(len(self._players)):
            self._current_player_index = (self._current_player_index + 1) % len(
                self._players
            )
            current_player = self._players[self._current_player_index]

            # If this player hasn't passed, they get the turn
            if not self.has_passed(current_player.id):
                break
        else:
            # All players have passed, phase is complete
            return

    def advance_to_player(self, player_id: str) -> None:
        """Advance to a specific player."""
        # Guard against misuse outside ACTION phase
        if self.get_current_phase() != GamePhase.ACTION:
            raise ValidationError(
                f"advance_to_player can only be used in ACTION phase, current phase is {self.get_current_phase()}"
            )

        for i, player in enumerate(self._players):
            if player.id == player_id:
                if self.has_passed(player_id):
                    raise ValidationError(
                        "Cannot activate a player who has already passed"
                    )
                self._current_player_index = i
                return
        raise InvalidPlayerError(f"Player '{player_id}' not found")

    def has_passed(self, player_id: str) -> bool:
        """Check if a player has passed in the current action phase."""
        return player_id in self._passed_players

    def assign_strategy_card(
        self,
        player_id: str,
        card_id: Union[int, "StrategyCardType"],
        *,
        allow_during_action: bool = False,
    ) -> None:
        """Assign a strategy card to a player."""
        self._validate_player_exists(player_id)

        # Phase guard: Only allow strategy card assignment during STRATEGY or SETUP phases
        # Exception: Allow during ACTION phase when explicitly flagged (for testing purposes)
        current_phase = self.get_current_phase()
        allowed_phases = [GamePhase.STRATEGY, GamePhase.SETUP]
        if allow_during_action:
            allowed_phases.append(GamePhase.ACTION)

        if current_phase not in allowed_phases:
            phase_names = ", ".join(phase.value for phase in allowed_phases)
            raise ValidationError(
                f"Cannot assign strategy cards during {current_phase.value} phase. "
                f"Strategy cards can only be assigned during {phase_names} phases."
            )

        if isinstance(card_id, int):
            self.select_strategy_card(player_id, card_id)
            return

        # StrategyCardType
        mapped = self._strategy_card_type_to_id.get(card_id.value)
        if mapped is None:
            raise ValidationError(f"Unknown strategy card type: {card_id.value}")
        self.select_strategy_card(player_id, mapped)

    def must_pass(self, player_id: str) -> bool:
        """Check if a player must pass (cannot perform any action).

        A player must pass when they have no available actions to take.
        This is used as a future-proof mechanism for scenarios where
        players might be forced to pass due to game state constraints.

        Args:
            player_id: The ID of the player to check

        Returns:
            True if the player must pass, False if they have available actions
        """
        self._validate_player_exists(player_id)
        return not self._can_perform_any_action(player_id)

    def _can_perform_any_action(self, player_id: str) -> bool:
        """Check if a player can perform any action.

        This method determines whether a player has any available actions
        they can take during their turn. Currently focuses on action phase
        logic but can be extended for other phases.

        Args:
            player_id: The ID of the player to check

        Returns:
            True if the player can perform any action, False otherwise
        """
        # Player has passed, cannot perform actions
        if self.has_passed(player_id):
            return False

        # In action phase, check if player has any available actions
        if self.get_current_phase() == GamePhase.ACTION:
            # Player can always take tactical actions unless they've passed
            return True

        # In other phases, assume no actions available
        return False

    def resolve_start_of_turn_abilities(self, player_id: str) -> None:
        """Resolve start of turn abilities for a player.

        This method is called when a player passes their turn to resolve
        any start-of-turn abilities they may have. Currently a placeholder
        but includes logging for test verification.

        Args:
            player_id: The ID of the player whose abilities to resolve
        """
        # Log the invocation for test verification
        # This helps prove the method was called during testing
        import logging

        logger = logging.getLogger(__name__)
        logger.debug(f"Resolving start-of-turn abilities for player {player_id}")

        # Placeholder for start of turn ability resolution
        # Future implementation will handle faction abilities, technology abilities, etc.
        pass

    def resolve_transactions(self, player_id: str) -> None:
        """Resolve transactions for a player.

        This method is called when a player passes their turn to resolve
        any transactions they may want to make. Currently a placeholder
        but includes logging for test verification.

        Args:
            player_id: The ID of the player whose transactions to resolve
        """
        # Log the invocation for test verification
        # This helps prove the method was called during testing
        import logging

        logger = logging.getLogger(__name__)
        logger.debug(f"Resolving transactions for player {player_id}")

        # Placeholder for transaction resolution
        # Future implementation will handle trade goods, commodities, etc.
        pass

    def can_resolve_secondary_ability(
        self, player_id: str, card_type: "StrategyCardType"
    ) -> bool:
        """Check if a player can resolve a secondary ability."""
        # Passed players can still resolve secondary abilities
        return True

    def can_pass(self, player_id: str) -> bool:
        """Check if a player can pass according to Rule 3 requirements."""
        self._validate_player_exists(player_id)

        # Future-proof: Always allow passing if player must pass (cannot perform any action)
        if self.must_pass(player_id):
            return True

        # Get player's strategy cards
        player_cards = self._selected_strategy_cards.get(player_id, [])
        if not player_cards:
            return True  # No cards, can pass

        # Check if player has performed strategic action for all required cards
        strategic_actions = self._strategic_actions_taken.get(player_id, set())

        # Must have taken strategic action for all cards (both single and multi-card games)
        return all(card.id in strategic_actions for card in player_cards)

    def _validate_player_exists(self, player_id: str) -> None:
        """Validate that a player exists in the game."""
        if not any(player.id == player_id for player in self._players):
            raise InvalidPlayerError(f"Player '{player_id}' not found in game")

    def is_player_activated(self, player_id: str) -> bool:
        """Check if a specific player is currently activated."""
        self._validate_player_exists(player_id)
        current_player = self.get_current_player()
        return current_player.id == player_id

    def pass_turn(self, player_id: str) -> None:
        """Allow a player to pass their turn."""
        if not self.is_player_activated(player_id):
            from .validation import ValidationError

            current_player = self.get_current_player()
            raise ValidationError(
                f"Player '{player_id}' is not currently active. Expected: '{current_player.id}', Actual: '{player_id}'",
                "player_id",
                player_id,
            )

        self.advance_turn()

    def start_strategy_phase(self) -> None:
        """Start the strategy phase."""
        self._state_machine.transition_to(GamePhase.STRATEGY)
        # Reset strategy card selections
        self._available_strategy_cards = list(STANDARD_STRATEGY_CARDS)
        self._selected_strategy_cards = {}

    def get_available_strategy_cards(self) -> list[StrategyCard]:
        """Get the list of available strategy cards."""
        return list(self._available_strategy_cards)

    def select_strategy_card(self, player_id: str, card_id: int) -> None:
        """Allow a player to select a strategy card."""
        self._validate_player_exists(player_id)

        # Find the card
        card = next(
            (c for c in self._available_strategy_cards if c.id == card_id), None
        )
        if card is None:
            raise ValidationError(f"Strategy card with id {card_id} is not available")

        # Initialize player's card list if needed
        if player_id not in self._selected_strategy_cards:
            self._selected_strategy_cards[player_id] = []

        # Add card to player's list and remove from available
        self._selected_strategy_cards[player_id].append(card)
        self._available_strategy_cards.remove(card)

    def get_player_strategy_cards(self, player_id: str) -> list[StrategyCard]:
        """Get the strategy cards selected by a player."""
        return self._selected_strategy_cards.get(player_id, [])

    def get_strategy_phase_turn_order(self) -> list[Player]:
        """Get turn order based on strategy card initiative values."""
        # Create list of (player, initiative) pairs
        player_initiatives = []
        for player in self._players:
            cards = self._selected_strategy_cards.get(player.id, [])
            if cards:
                # Use the lowest initiative among player's cards
                lowest_initiative = min(card.initiative for card in cards)
                player_initiatives.append((player, lowest_initiative))

        # Sort by initiative (lowest first)
        player_initiatives.sort(key=lambda x: x[1])

        # Return just the players in order
        return [player for player, _ in player_initiatives]

    def _get_cards_per_player(self) -> int:
        """Calculate how many strategy cards each player should have."""
        total_strategy_cards = len(STANDARD_STRATEGY_CARDS)  # 8 cards
        return total_strategy_cards // len(self._players)

    def is_strategy_phase_complete(self) -> bool:
        """Check if all players have selected their required number of strategy cards."""
        cards_per_player = self._get_cards_per_player()

        # Check if all players have exactly the required number of cards
        return all(
            player.id in self._selected_strategy_cards
            and len(self._selected_strategy_cards[player.id]) == cards_per_player
            for player in self._players
        )

    def start_action_phase(self) -> None:
        """Start the action phase."""
        # Ensure we're in the correct phase to transition to ACTION
        if self._state_machine.current_phase == GamePhase.SETUP:
            self._state_machine.transition_to(GamePhase.STRATEGY)
        self._state_machine.transition_to(GamePhase.ACTION)
        # Reset pass state for new action phase
        self._passed_players.clear()
        self._consecutive_passes = 0
        self._actions_taken_this_turn.clear()
        self._strategic_actions_taken.clear()

        # For now, skip event creation since we don't have game_id or round_number
        # TODO: Add proper event handling when game state is fully implemented

    def get_current_phase(self) -> GamePhase:
        """Get the current game phase."""
        return self._state_machine.current_phase

    def _validate_action_preconditions(
        self, player_id: str, *, for_pass: bool = False
    ) -> None:
        """Validate that a player can take an action."""
        self._validate_player_exists(player_id)

        # Check if we're in the ACTION phase
        current_phase = self.get_current_phase()
        if current_phase != GamePhase.ACTION:
            action_type = "pass" if for_pass else "take action"
            raise ValidationError(
                f"Cannot {action_type} during {current_phase.value} phase. "
                f"Actions can only be taken during the ACTION phase. "
                f"Current player: {player_id}"
            )

        # Check if player has already passed
        if self.has_passed(player_id):
            action_type = "pass again" if for_pass else "take action"
            raise ValidationError(
                f"Player {player_id} has already passed and cannot {action_type}. "
                f"Passed players: {list(self._passed_players)}"
            )

        # Check if it's the player's turn
        current_player = self.get_current_player()
        if current_player.id != player_id:
            action_type = "pass" if for_pass else "take action"
            raise ValidationError(
                f"Cannot {action_type}: it is {current_player.id}'s turn, not {player_id}'s turn. "
                f"Turn order: {[p.id for p in self._players]}"
            )

        # Check if player must pass (but allow passing when for_pass=True)
        if self.must_pass(player_id) and not for_pass:
            raise ValidationError("Player must pass")

        # Check if player has already taken an action this turn
        if player_id in self._actions_taken_this_turn:
            raise ValidationError("Already took action this turn")

    def _reset_consecutive_passes(self) -> None:
        """Reset the consecutive passes counter."""
        self._consecutive_passes = 0

    def take_tactical_action(self, player_id: str, action_type: str) -> None:
        """Allow a player to take a tactical action."""
        self._validate_action_preconditions(player_id)
        self._reset_consecutive_passes()

        # Track that this player took an action this turn
        self._actions_taken_this_turn.add(player_id)

        # Advance to next player after taking action
        self.advance_turn()

    def take_strategic_action(
        self, player_id: str, action_type: Union[int, str, "StrategyCardType"]
    ) -> None:
        """Allow a player to take a strategic action.

        Args:
            player_id: The ID of the player taking the action
            action_type: The strategy card to use. Can be:
                - int: Numeric strategy card ID (1-8)
                - str: String representation of strategy card ID (e.g., "1", "2")
                - StrategyCardType: Enum value for the strategy card type

        Raises:
            ValidationError: If the player doesn't own the card or input is invalid
        """
        self._validate_action_preconditions(player_id)

        # Validate that the player owns the strategy card they're trying to use
        player_cards = self.get_player_strategy_cards(player_id)
        owned_ids = {c.id for c in player_cards}

        # Handle string input: accept either numeric ID or canonical card name
        if isinstance(action_type, str):
            s = action_type.strip().lower()
            if s.isdigit():
                card_id = int(s)
            else:
                mapped = self._strategy_card_type_to_id.get(s)
                if mapped is None:
                    # Provide helpful error message with available card names
                    available_names = sorted(self._strategy_card_type_to_id.keys())
                    raise ValidationError(
                        f"String input '{action_type}' must be either a valid strategy card ID (1-8) "
                        f"or a valid card name. Available card names: {', '.join(available_names)}. "
                        f"Received unrecognized string: '{s}'"
                    )
                card_id = mapped

            # Validate card ID is in valid range
            if not (1 <= card_id <= 8):
                raise ValidationError(
                    f"Strategy card ID must be between 1 and 8, got {card_id}"
                )

            # Check if player owns this card
            if card_id not in owned_ids:
                raise ValidationError(
                    f"Player {player_id} does not own strategy card {card_id}. "
                    f"Player owns cards: {sorted(owned_ids)}, Requested: {card_id}"
                )
        elif isinstance(action_type, int):
            # Handle direct int input
            card_id = action_type
            # Check if player owns this card
            if card_id not in owned_ids:
                raise ValidationError(
                    f"Player {player_id} does not own strategy card {card_id}. "
                    f"Player owns cards: {sorted(owned_ids)}, Requested: {card_id}"
                )
        else:
            # Handle StrategyCardType enum with proper ID mapping
            card_id_maybe = self._strategy_card_type_to_id.get(action_type.value)
            if card_id_maybe is None:
                raise ValidationError(
                    f"Unknown strategy card type: {action_type.value}"
                )
            card_id = card_id_maybe  # Now mypy knows card_id is int

            # Check if player owns this card
            if card_id not in owned_ids:
                raise ValidationError(
                    f"Player {player_id} does not own strategy card {action_type.value} (ID: {card_id}). "
                    f"Player owns cards: {sorted(owned_ids)}, Requested: {card_id}"
                )

        # Enforce once-per-phase use of each strategy card (Rule 3)
        prev = self._strategic_actions_taken.get(player_id, set())
        if card_id in prev:
            raise ValidationError(
                f"Strategy card {card_id} already used this phase by player {player_id}. "
                f"Cards used this phase: {sorted(prev)}, Attempted: {card_id}"
            )

        self._reset_consecutive_passes()

        # Track that this player took an action this turn
        self._actions_taken_this_turn.add(player_id)

        # Track that this player took a strategic action
        self._strategic_actions_taken.setdefault(player_id, set()).add(card_id)

        # Advance to next player after taking action
        self.advance_turn()

    def pass_action_phase_turn(self, player_id: str) -> None:
        """Allow a player to pass their turn in the action phase."""
        self._validate_action_preconditions(player_id, for_pass=True)

        # Check Rule 3 pass requirements
        if not self.can_pass(player_id):
            raise ValidationError("Must perform strategic action before passing")

        # Resolve start of turn abilities and transactions
        self.resolve_start_of_turn_abilities(player_id)
        self.resolve_transactions(player_id)

        # Mark player as passed
        self._passed_players.add(player_id)

        # Increment consecutive passes and advance turn
        self._consecutive_passes += 1
        self.advance_turn()

        # Check if phase is complete and advance if so
        if self.is_action_phase_complete():
            self.advance_to_next_phase()

    def is_action_phase_complete(self) -> bool:
        """Check if action phase is complete (all players passed)."""
        return len(self._passed_players) >= len(self._players)

    def advance_to_next_phase(self) -> None:
        """Advance to the next phase when action phase is complete."""
        if self.is_action_phase_complete():
            self.advance_to_phase(GamePhase.STATUS)

    def undo_last_action(self) -> bool:
        """Undo the last action taken. Returns True if successful."""
        try:
            if self._current_game_state is None:
                # No game state available for undo
                return False

            previous_state = self._command_manager.undo_last_command(
                self._current_game_state
            )
            self._current_game_state = previous_state
            return True
        except ValidationError:
            # No commands to undo
            return False

    def redo_last_action(self) -> bool:
        """Redo the last undone action. Returns True if successful."""
        # For now, we don't have redo functionality implemented
        # This would require a separate redo stack in CommandManager
        return False

    def set_current_game_state(self, game_state: Any) -> None:
        """Set the current game state."""
        self._current_game_state = game_state

    def get_current_game_state(self) -> Optional[Any]:
        """Get the current game state."""
        return self._current_game_state

    def execute_command(self, command: Any, game_state: Any) -> Any:
        """Execute a command and update the current game state."""
        new_state = self._command_manager.execute_command(command, game_state)
        self._current_game_state = new_state
        return new_state

    def get_action_history(self) -> list[GameCommand]:
        """Get the history of actions taken."""
        return self._command_manager.get_command_history()

    def set_event_bus(self, event_bus: Any) -> None:
        """Set the event bus for publishing game events."""
        self._event_bus = event_bus

    def advance_to_phase(self, new_phase: GamePhase) -> None:
        """Advance to a new game phase with validation and publish event."""
        old_phase = self._state_machine.current_phase

        # Use state machine for validated transition
        self._state_machine.transition_to(new_phase)

        # Publish phase changed event if event bus is available
        if self._event_bus is not None:
            event = create_phase_changed_event(
                game_id=self._game_id,
                from_phase=old_phase.value,
                to_phase=new_phase.value,
                round_number=self._round_number,
            )
            self._event_bus.publish(event)

"""Action Card system implementation for TI4.

This module implements the Action Card system as defined in LRR Rules 2 and 1.22.
Action cards provide players with various abilities that can be resolved during
specific timing windows.

LRR References:
- Rule 2: Action Cards
- Rule 1.22: Component-Specific Rules for Action Cards
- Rule 22: Component Action
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any


class ActionCardTiming(Enum):
    """Timing windows when action cards can be played.

    LRR 2.6: The first paragraph describes timing of when card's ability can be resolved.
    """

    COMPONENT_ACTION = (
        "component_action"  # Requires component action during action phase
    )
    COMBAT = "combat"  # During combat
    SPACE_COMBAT = "space_combat"  # During space combat
    GROUND_COMBAT = "ground_combat"  # During ground combat
    AGENDA_PHASE = "agenda_phase"  # During agenda phase
    STATUS_PHASE = "status_phase"  # During status phase


@dataclass
class ActionCardContext:
    """Context for action card resolution."""

    player_id: str
    game_state: Any | None = None
    target_player: str | None = None
    target_system: str | None = None
    target_units: list[str] | None = None
    additional_data: dict[str, Any] | None = None


@dataclass
class ActionCardResult:
    """Result of action card resolution."""

    success: bool
    card_discarded: bool = True
    card_returned_to_hand: bool = False
    effects_applied: list[str] | None = None
    error_message: str | None = None
    additional_data: dict[str, Any] | None = None


class ActionCard(ABC):
    """Base class for all Action Cards.

    LRR 2: Action cards provide players with various abilities that they can
    resolve as described on the cards.

    LRR 1.22: The opening paragraph of each ability found on an action card
    describes when a player can resolve that card's ability.
    """

    def __init__(
        self,
        name: str,
        timing: ActionCardTiming,
        description: str,
        flavor_text: str | None = None,
    ):
        self.name = name
        self.timing = timing
        self.description = description
        self.flavor_text = flavor_text

    @abstractmethod
    def can_play(self, context: ActionCardContext) -> tuple[bool, str | None]:
        """Check if this action card can be played in the given context.

        LRR 22.3: A component action cannot be performed if its ability
        cannot be completely resolved.

        Args:
            context: The context in which the card would be played

        Returns:
            Tuple of (can_play, error_message)
        """
        pass

    @abstractmethod
    def resolve(self, context: ActionCardContext) -> ActionCardResult:
        """Resolve the action card's ability.

        Args:
            context: The context for resolution

        Returns:
            Result of the card resolution
        """
        pass

    def get_timing_description(self) -> str:
        """Get the timing description for this card."""
        return f"{self.timing.value}: {self.description}"

    def requires_component_action(self) -> bool:
        """Check if this card requires a component action to play.

        LRR 2.6a: If an action card contains the word "Action," a player must
        use a component action during the action phase to resolve the ability.
        """
        return self.timing == ActionCardTiming.COMPONENT_ACTION


class ActionCardManager:
    """Manager for action card resolution and validation.

    Handles the rules around action card play, including timing validation,
    duplicate card restrictions, and integration with the component action system.
    """

    def __init__(self) -> None:
        self._played_cards_this_window: dict[str, list[str]] = {}
        self._current_timing_window: str | None = None

    def set_timing_window(self, window: str) -> None:
        """Set the current timing window for action card resolution."""
        if window != self._current_timing_window:
            self._current_timing_window = window
            self._played_cards_this_window[window] = []

    def can_play_card(
        self,
        card: ActionCard,
        context: ActionCardContext,
        timing_window: str | None = None,
    ) -> tuple[bool, str | None]:
        """Check if an action card can be played.

        LRR 2.6b: Multiple action cards with the same name cannot be played
        during a single timing window to affect the same units or game effect.

        Args:
            card: The action card to check
            context: The context for playing the card
            timing_window: Optional specific timing window

        Returns:
            Tuple of (can_play, error_message)
        """
        # Check basic card requirements
        can_play, card_error = card.can_play(context)
        if not can_play:
            return (
                False,
                card_error or f"Card {card.name} cannot be played in current context",
            )

        # Check timing window restrictions
        window = timing_window or self._current_timing_window
        if window and window in self._played_cards_this_window:
            if card.name in self._played_cards_this_window[window]:
                return False, f"Card {card.name} already played this timing window"

        return True, None

    def play_card(
        self,
        card: ActionCard,
        context: ActionCardContext,
        timing_window: str | None = None,
    ) -> ActionCardResult:
        """Play an action card.

        Args:
            card: The action card to play
            context: The context for playing the card
            timing_window: Optional specific timing window

        Returns:
            Result of playing the card
        """
        # Validate card can be played
        can_play, error = self.can_play_card(card, context, timing_window)
        if not can_play:
            return ActionCardResult(
                success=False, card_discarded=False, error_message=error
            )

        # Track card play for duplicate prevention
        window = timing_window or self._current_timing_window
        if window:
            if window not in self._played_cards_this_window:
                self._played_cards_this_window[window] = []
            self._played_cards_this_window[window].append(card.name)

        # Resolve the card
        try:
            result = card.resolve(context)
            return result
        except Exception as e:
            return ActionCardResult(
                success=False,
                card_discarded=False,
                error_message=f"Error resolving card {card.name}: {str(e)}",
            )

    def cancel_card(self, card_name: str, timing_window: str | None = None) -> None:
        """Cancel a played action card.

        LRR 2.8: If an action card is canceled, that card has no effect and is discarded.
        LRR 2.6b: Canceled cards are not treated as being played.
        """
        window = timing_window or self._current_timing_window
        if window and window in self._played_cards_this_window:
            if card_name in self._played_cards_this_window[window]:
                self._played_cards_this_window[window].remove(card_name)

    def clear_timing_window(self, window: str | None = None) -> None:
        """Clear played cards for a timing window."""
        window_to_clear = window or self._current_timing_window
        if window_to_clear and window_to_clear in self._played_cards_this_window:
            self._played_cards_this_window[window_to_clear].clear()

    def draw_action_cards(
        self, player_id: str, count: int, game_state: Any
    ) -> list[str]:
        """Draw action cards for a player.

        Args:
            player_id: The player drawing cards
            count: Number of cards to draw
            game_state: Game state to update (mutable reference expected)

        Returns:
            List of card names drawn

        Note:
            This method expects the caller to handle GameState updates.
            If game_state has a draw_action_cards method that returns a new state,
            the caller must capture and use that new state.
        """
        # For now, return placeholder card names
        # The actual state management should be handled by the caller
        # who has access to the GameState's draw_action_cards method
        return [f"action_card_{i + 1}" for i in range(count)]


# Example Action Card implementations


class DirectHitActionCard(ActionCard):
    """Direct Hit action card implementation.

    Example of a combat timing action card that destroys a ship.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Direct Hit",
            timing=ActionCardTiming.SPACE_COMBAT,
            description="After another player's ship is destroyed: Destroy another one of that player's ships in the same system.",
            flavor_text="The Letnev commander's eyes gleamed as the enemy flagship erupted in flames.",
        )

    def can_play(self, context: ActionCardContext) -> tuple[bool, str | None]:
        """Check if Direct Hit can be played."""
        # Requires target player and system with ships
        if not context.target_units or len(context.target_units) == 0:
            return False, "No valid targets available"

        return True, None

    def resolve(self, context: ActionCardContext) -> ActionCardResult:
        """Resolve Direct Hit effect."""
        if not context.target_units:
            return ActionCardResult(
                success=False, error_message="No target units specified"
            )

        # In a real implementation, this would destroy a ship
        destroyed_ship = context.target_units[0]

        return ActionCardResult(
            success=True,
            effects_applied=[f"Destroyed {destroyed_ship}"],
            additional_data={
                "destroyed_unit": destroyed_ship,
                "target_player": context.target_player,
                "system": context.target_system,
            },
        )


class LeadershipRiderActionCard(ActionCard):
    """Leadership Rider action card implementation.

    Example of a component action timing action card.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Leadership Rider",
            timing=ActionCardTiming.COMPONENT_ACTION,
            description="Action: Predict aloud the outcome of this agenda. If your prediction is correct, gain 3 command tokens.",
            flavor_text="Sometimes the best leaders are those who can see what others cannot.",
        )

    def can_play(self, context: ActionCardContext) -> tuple[bool, str | None]:
        """Check if Leadership Rider can be played."""
        # Can be played as component action
        return True, None

    def resolve(self, context: ActionCardContext) -> ActionCardResult:
        """Resolve Leadership Rider effect."""
        # In a real implementation, this would track the prediction
        return ActionCardResult(
            success=True,
            effects_applied=["Gained 3 command tokens"],
            additional_data={"command_tokens_gained": 3},
        )


class UpgradeActionCard(ActionCard):
    """Upgrade action card implementation.

    Example of an action timing card that requires component action.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Upgrade",
            timing=ActionCardTiming.COMPONENT_ACTION,
            description="Action: Replace 1 of your cruisers in your home system or in a system that contains 1 or more of your space docks with 1 dreadnought.",
            flavor_text="The shipyards worked around the clock to retrofit the aging cruiser.",
        )

    def can_play(self, context: ActionCardContext) -> tuple[bool, str | None]:
        """Check if Upgrade can be played."""
        # Requires target system with cruiser and either home system or space dock
        if not context.target_units or not any(
            "cruiser" in unit.lower() for unit in context.target_units
        ):
            return False, "No units to upgrade"

        return True, None

    def resolve(self, context: ActionCardContext) -> ActionCardResult:
        """Resolve Upgrade effect."""
        if not context.target_units:
            return ActionCardResult(
                success=False, error_message="No cruiser to upgrade"
            )

        # Find cruiser to upgrade
        cruiser_to_upgrade = None
        for unit in context.target_units:
            if "cruiser" in unit.lower():
                cruiser_to_upgrade = unit
                break

        if not cruiser_to_upgrade:
            return ActionCardResult(
                success=False, error_message="No cruiser found to upgrade"
            )

        return ActionCardResult(
            success=True,
            effects_applied=[f"Upgraded {cruiser_to_upgrade} to dreadnought"],
            additional_data={
                "upgraded_unit": cruiser_to_upgrade,
                "new_unit": "dreadnought",
                "system": context.target_system,
            },
        )

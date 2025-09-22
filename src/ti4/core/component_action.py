"""Component Action system implementation for TI4.

This module implements the Component Action system as defined in LRR Rule 22.
Component actions are actions that players can perform during their turn in the
action phase, found on various game components including action cards.

LRR References:
- Rule 22: Component Action
- Rule 3.1: Action types during action phase
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from .action_cards import (
    ActionCard,
    ActionCardContext,
    ActionCardManager,
)


class ComponentActionType(Enum):
    """Types of component actions available."""

    ACTION_CARD = "action_card"
    TECHNOLOGY = "technology"
    LEADER = "leader"
    EXPLORATION = "exploration"
    RELIC = "relic"
    PROMISSORY_NOTE = "promissory_note"
    FACTION_ABILITY = "faction_ability"


@dataclass
class ComponentActionContext:
    """Context for component action execution."""

    player_id: str
    action_type: ComponentActionType
    component_id: str
    game_state: Optional[Any] = None
    targets: Optional[dict[str, Any]] = None
    additional_data: Optional[dict[str, Any]] = None


@dataclass
class ComponentActionResult:
    """Result of component action execution."""

    success: bool
    action_consumed: bool = True  # Whether this used the player's action
    effects_applied: Optional[list[str]] = None
    error_message: Optional[str] = None
    additional_data: Optional[dict[str, Any]] = None


class ComponentActionProvider(ABC):
    """Base class for components that provide component actions."""

    @abstractmethod
    def can_perform_component_action(self, context: ComponentActionContext) -> bool:
        """Check if the component action can be performed."""
        pass

    @abstractmethod
    def perform_component_action(
        self, context: ComponentActionContext
    ) -> ComponentActionResult:
        """Perform the component action."""
        pass

    @abstractmethod
    def get_component_action_description(self) -> str:
        """Get description of the component action."""
        pass


class ComponentActionManager:
    """Manager for component actions during the action phase.

    LRR 22: Component actions can be found on various game components and are
    performed during a player's turn in the action phase.
    """

    def __init__(self) -> None:
        self._action_card_manager = ActionCardManager()
        self._registered_providers: dict[str, ComponentActionProvider] = {}
        self._current_player: Optional[str] = None
        self._action_phase_active = False

    def set_action_phase_active(self, active: bool) -> None:
        """Set whether the action phase is currently active."""
        self._action_phase_active = active

    def set_current_player(self, player_id: str) -> None:
        """Set the current active player."""
        self._current_player = player_id

    def register_component_provider(
        self, component_id: str, provider: ComponentActionProvider
    ) -> None:
        """Register a component action provider."""
        self._registered_providers[component_id] = provider

    def can_perform_component_action(
        self,
        player_id: str,
        action_type: ComponentActionType,
        component_id: str,
        **kwargs: Any,
    ) -> tuple[bool, Optional[str]]:
        """Check if a component action can be performed.

        LRR 22.3: A component action cannot be performed if its ability
        cannot be completely resolved.

        Args:
            player_id: The player attempting the action
            action_type: Type of component action
            component_id: ID of the component
            **kwargs: Additional context data

        Returns:
            Tuple of (can_perform, error_message)
        """
        # Check if action phase is active
        if not self._action_phase_active:
            return False, "Component actions can only be performed during action phase"

        # Check if it's the player's turn
        if self._current_player != player_id:
            return False, f"It is not {player_id}'s turn"

        # Create context
        context = ComponentActionContext(
            player_id=player_id,
            action_type=action_type,
            component_id=component_id,
            targets=kwargs.get("targets"),
            additional_data=kwargs.get("additional_data"),
        )

        # Handle action cards specially
        if action_type == ComponentActionType.ACTION_CARD:
            return self._can_perform_action_card_component_action(context, **kwargs)

        # Handle other component types
        if component_id in self._registered_providers:
            provider = self._registered_providers[component_id]
            if provider.can_perform_component_action(context):
                return True, None
            else:
                return False, f"Component {component_id} cannot perform action"

        return False, f"Unknown component: {component_id}"

    def perform_component_action(
        self,
        player_id: str,
        action_type: ComponentActionType,
        component_id: str,
        **kwargs: Any,
    ) -> ComponentActionResult:
        """Perform a component action.

        LRR 22.2: To perform a component action, a player reads the action's
        text and follows the instructions as described.

        Args:
            player_id: The player performing the action
            action_type: Type of component action
            component_id: ID of the component
            **kwargs: Additional context data

        Returns:
            Result of the component action
        """
        # Validate action can be performed
        can_perform, error = self.can_perform_component_action(
            player_id, action_type, component_id, **kwargs
        )

        if not can_perform:
            return ComponentActionResult(
                success=False, action_consumed=False, error_message=error
            )

        # Create context
        context = ComponentActionContext(
            player_id=player_id,
            action_type=action_type,
            component_id=component_id,
            game_state=kwargs.get("game_state"),
            targets=kwargs.get("targets"),
            additional_data=kwargs.get("additional_data"),
        )

        # Handle action cards specially
        if action_type == ComponentActionType.ACTION_CARD:
            return self._perform_action_card_component_action(context, **kwargs)

        # Handle other component types
        if component_id in self._registered_providers:
            provider = self._registered_providers[component_id]
            return provider.perform_component_action(context)

        return ComponentActionResult(
            success=False,
            action_consumed=False,
            error_message=f"Unknown component: {component_id}",
        )

    def _can_perform_action_card_component_action(
        self, context: ComponentActionContext, **kwargs: Any
    ) -> tuple[bool, Optional[str]]:
        """Check if an action card component action can be performed."""
        action_card = kwargs.get("action_card")
        if not isinstance(action_card, ActionCard):
            return False, "Invalid action card provided"

        # Check if card requires component action
        if not action_card.requires_component_action():
            return False, f"Card {action_card.name} does not require component action"

        # Create action card context
        card_context = ActionCardContext(
            player_id=context.player_id,
            game_state=context.game_state,
            target_player=kwargs.get("target_player"),
            target_system=kwargs.get("target_system"),
            target_units=kwargs.get("target_units"),
            additional_data=context.additional_data,
        )

        # Check if card can be played
        return self._action_card_manager.can_play_card(action_card, card_context)

    def _perform_action_card_component_action(
        self, context: ComponentActionContext, **kwargs: Any
    ) -> ComponentActionResult:
        """Perform an action card component action."""
        action_card = kwargs.get("action_card")
        if not isinstance(action_card, ActionCard):
            return ComponentActionResult(
                success=False,
                action_consumed=False,
                error_message="Invalid action card provided",
            )

        # Create action card context
        card_context = ActionCardContext(
            player_id=context.player_id,
            game_state=context.game_state,
            target_player=kwargs.get("target_player"),
            target_system=kwargs.get("target_system"),
            target_units=kwargs.get("target_units"),
            additional_data=context.additional_data,
        )

        # Play the card
        card_result = self._action_card_manager.play_card(action_card, card_context)

        # Convert to component action result
        return ComponentActionResult(
            success=card_result.success,
            action_consumed=card_result.success,  # Only consume action if successful
            effects_applied=card_result.effects_applied,
            error_message=card_result.error_message,
            additional_data=card_result.additional_data,
        )

    def cancel_component_action(
        self, player_id: str, action_type: ComponentActionType, component_id: str
    ) -> None:
        """Cancel a component action.

        LRR 22.4: If a component action is canceled, it does not use that
        player's action.
        """
        if action_type == ComponentActionType.ACTION_CARD:
            self._action_card_manager.cancel_card(component_id)

    def get_available_component_actions(self, player_id: str) -> list[dict[str, Any]]:
        """Get list of available component actions for a player."""
        if not self._action_phase_active or self._current_player != player_id:
            return []

        available_actions = []

        # Add registered component providers
        for component_id, provider in self._registered_providers.items():
            context = ComponentActionContext(
                player_id=player_id,
                action_type=ComponentActionType.TECHNOLOGY,  # Default type
                component_id=component_id,
            )

            if provider.can_perform_component_action(context):
                available_actions.append(
                    {
                        "component_id": component_id,
                        "description": provider.get_component_action_description(),
                        "type": "component",
                    }
                )

        return available_actions


# Example component action provider for technology cards


class TechnologyComponentActionProvider(ComponentActionProvider):
    """Example provider for technology component actions."""

    def __init__(
        self,
        tech_name: str,
        description: str,
        requirements: Optional[dict[str, Any]] = None,
    ):
        self.tech_name = tech_name
        self.description = description
        self.requirements = requirements or {}

    def can_perform_component_action(self, context: ComponentActionContext) -> bool:
        """Check if technology component action can be performed."""
        # In a real implementation, this would check technology requirements
        return True

    def perform_component_action(
        self, context: ComponentActionContext
    ) -> ComponentActionResult:
        """Perform technology component action."""
        return ComponentActionResult(
            success=True,
            effects_applied=[f"Used {self.tech_name} technology"],
            additional_data={"technology_used": self.tech_name},
        )

    def get_component_action_description(self) -> str:
        """Get description of the technology action."""
        return f"{self.tech_name}: {self.description}"

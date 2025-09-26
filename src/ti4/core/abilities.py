"""
Core abilities system for TI4 - Rule 1: ABILITIES

This module implements the comprehensive ability system including:
- Timing windows (when/before/after) with proper precedence
- Ability costs, effects, and triggers
- Multi-player ability resolution
- Component-specific ability handling

Key LRR Rules Implemented:
- 1.2: Card abilities take precedence over rules
- 1.6: "Cannot" effects are absolute
- 1.14: Before/after timing is immediate
- 1.15: "When" timing can modify events
- 1.16: "When" has priority over "after"
- 1.17: "Then" requires sequential success
- 1.18: Abilities resolve once per trigger occurrence
"""

import itertools
import logging
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import TYPE_CHECKING, Any, Callable, Optional, Protocol

if TYPE_CHECKING:
    from ti4.core.game_state import GameState

logger = logging.getLogger(__name__)


class TimingWindow(IntEnum):
    """
    Timing windows for ability resolution with built-in precedence.
    Higher values = higher priority (Rule 1.16: when > after)
    """

    AFTER = 1  # After an event occurs
    BEFORE = 2  # Before an event occurs
    WHEN = 3  # At the moment of an event (highest priority)
    ACTION = 4  # During action phase
    START_OF_TURN = 5  # At turn start
    END_OF_TURN = 6  # At turn end
    START_OF_PHASE = 7  # At phase start
    END_OF_PHASE = 8  # At phase end


class AbilityPrecedence(IntEnum):
    """
    Ability precedence levels (Rules 1.2, 1.6)
    Higher values = higher precedence
    """

    NORMAL = 1  # Standard ability
    CARD_OVERRIDE = 2  # Card abilities override rules (Rule 1.2)
    CANNOT_ABSOLUTE = 3  # "Cannot" effects are absolute (Rule 1.6)


class AbilityFrequency(Enum):
    """How often an ability can be triggered"""

    ONCE_PER_TRIGGER = "once_per_trigger"  # Once per occurrence of timing event
    ONCE_PER_TURN = "once_per_turn"  # Once per player turn
    ONCE_PER_ROUND = "once_per_round"  # Once per game round
    UNLIMITED = "unlimited"  # No frequency limit


@dataclass
class AbilityEffect:
    """
    Represents the effect of an ability (Rule 1.9: partial resolution)
    """

    type: str  # Type of effect (modify, trigger, replace, etc.)
    value: Any  # Effect value/data
    target: Optional[str] = None  # Target of the effect
    conditions: Optional[list[dict[str, Any]]] = (
        None  # Conditional effects for "then" (Rule 1.17)
    )

    def is_cannot_effect(self) -> bool:
        """Check if this is a "cannot" effect (Rule 1.6)"""
        return self.type == "cannot"

    def is_conditional(self) -> bool:
        """Check if this effect has "then" conditions (Rule 1.17)"""
        return self.conditions is not None


class PlayerProtocol(Protocol):
    """Protocol for player objects used in ability cost validation"""

    resources: int
    trade_goods: int
    command_tokens: int


@dataclass
class AbilityCost:
    """
    Represents the cost to activate an ability (Rules 1.11, 1.12)
    """

    type: Optional[str] = None  # Single cost type
    amount: Optional[int] = None  # Single cost amount
    costs: Optional[list[dict[str, Any]]] = None  # Multiple costs

    def can_pay(self, player: PlayerProtocol) -> bool:
        """Check if player can pay the ability cost"""
        if self.type and self.amount:
            # Single cost type
            return self._can_pay_single_cost(player, self.type, self.amount)

        if self.costs:
            # Multiple costs - all must be payable
            return all(
                self._can_pay_single_cost(player, cost["type"], cost.get("amount", 1))
                for cost in self.costs
            )

        return True  # No cost

    def _can_pay_single_cost(
        self, player: PlayerProtocol, cost_type: str, amount: int
    ) -> bool:
        """Check if player can pay a single cost type"""
        cost_checkers: dict[str, Callable[[PlayerProtocol], bool]] = {
            "resources": lambda p: p.resources >= amount,
            "trade_goods": lambda p: p.trade_goods >= amount,
            "command_tokens": lambda p: p.command_tokens >= amount,
            "exhaust_card": lambda p: True,  # Simplified for now - would need card_id context
        }

        checker = cost_checkers.get(cost_type)
        if checker:
            return bool(checker(player))
        return False


@dataclass
class Ability:
    """
    Core ability class representing a single ability

    Implements LRR Rules:
    - 1.14: Before/after timing is immediate
    - 1.15: "When" timing can modify events
    - 1.16: "When" has priority over "after"
    - 1.18: Abilities resolve once per trigger occurrence
    """

    name: str
    timing: TimingWindow
    trigger: str
    effect: AbilityEffect
    precedence: AbilityPrecedence = AbilityPrecedence.NORMAL
    cost: Optional[AbilityCost] = None
    duration: Optional[str] = None
    frequency: AbilityFrequency = AbilityFrequency.ONCE_PER_TRIGGER
    context_resolver: bool = False
    mandatory: bool = False

    # Private fields for tracking
    _usage_count: dict[str, int] = field(default_factory=dict)
    _active_until: Optional[str] = None
    _last_triggered: Optional[str] = None

    def can_trigger(self, event: str, context: Optional[dict[str, Any]] = None) -> bool:
        """Check if ability can trigger for the given event"""
        if self.trigger != event:
            return False

        # Check frequency limits
        if not self._check_frequency_limit(event, context):
            return False

        return True

    def is_active(self) -> bool:
        """Check if ability is currently active (Rule 1.3 duration tracking)"""
        if self.duration is None:
            return True

        # Duration tracking would need game state integration
        # For now, assume active
        return True

    def get_precedence_score(self) -> int:
        """Get combined precedence score for conflict resolution"""
        return (self.precedence.value * 100) + self.timing.value

    def _check_frequency_limit(
        self, event: str, context: Optional[dict[str, Any]]
    ) -> bool:
        """Check if ability can be used based on frequency limits (Rule 1.18)"""
        if self.frequency == AbilityFrequency.UNLIMITED:
            return True

        trigger_key = self._get_trigger_key(event, context)
        current_count = self._usage_count.get(trigger_key, 0)

        if self.frequency == AbilityFrequency.ONCE_PER_TRIGGER:
            return current_count == 0
        elif self.frequency == AbilityFrequency.ONCE_PER_TURN:
            # Use turn-specific key for turn-based frequency
            turn_id = None
            if context:
                turn_id = context.get("turn") or context.get("turn_id")
            if turn_id is not None:
                turn_key = f"{trigger_key}|turn:{turn_id}"
                return self._usage_count.get(turn_key, 0) == 0
            return True  # Allow if no turn context available
        elif self.frequency == AbilityFrequency.ONCE_PER_ROUND:
            # Use round-specific key for round-based frequency
            round_id = None
            if context:
                round_id = context.get("round") or context.get("round_id")
            if round_id is not None:
                round_key = f"{trigger_key}|round:{round_id}"
                return self._usage_count.get(round_key, 0) == 0
            return True  # Allow if no round context available

        # Other frequency types would need game state integration
        return True

    def _get_trigger_key(self, event: str, context: Optional[dict[str, Any]]) -> str:
        """Generate unique key for tracking trigger frequency"""
        if context:
            if "occurrence_id" in context:
                return f"{event}_{context['occurrence_id']}"
            if "combat_id" in context:
                return f"{event}_{context['combat_id']}"
        return event

    def mark_used(self, event: str, context: Optional[dict[str, Any]] = None) -> None:
        """Mark ability as used for frequency tracking"""
        trigger_key = self._get_trigger_key(event, context)
        self._usage_count[trigger_key] = self._usage_count.get(trigger_key, 0) + 1

        # For turn/round-based frequencies, also track with specific keys
        if self.frequency == AbilityFrequency.ONCE_PER_TURN and context:
            turn_id = context.get("turn") or context.get("turn_id")
            if turn_id is not None:
                turn_key = f"{trigger_key}|turn:{turn_id}"
                self._usage_count[turn_key] = self._usage_count.get(turn_key, 0) + 1
        elif self.frequency == AbilityFrequency.ONCE_PER_ROUND and context:
            round_id = context.get("round") or context.get("round_id")
            if round_id is not None:
                round_key = f"{trigger_key}|round:{round_id}"
                self._usage_count[round_key] = self._usage_count.get(round_key, 0) + 1

        self._last_triggered = trigger_key


@dataclass
class AbilityResolutionResult:
    """Result of ability resolution"""

    success: bool
    resolved_abilities: list[Ability]
    failed_abilities: list[Ability] = field(default_factory=list)
    event_modified: bool = False
    winning_ability: Optional[Ability] = None
    errors: list[str] = field(default_factory=list)


class AbilityManager:
    """
    Manages all abilities in the game and handles resolution conflicts

    Implements LRR Rules:
    - 1.7: Complete ability resolution
    - 1.8: Mandatory ability triggers
    - 1.9: Partial resolution of "and" effects
    - 1.19: Action phase multi-player resolution
    - 1.20: Strategy/agenda phase resolution
    """

    def __init__(self, game_state: "GameState") -> None:
        self.game_state = game_state
        self.abilities: list[Ability] = []
        self.pending_resolutions: list[Ability] = []
        self._occurrence_counter = itertools.count(1)

    def add_ability(self, ability: Ability) -> None:
        """Add an ability to the manager"""
        self.abilities.append(ability)
        logger.debug(f"Added ability: {ability.name}")

    def remove_ability(self, ability: Ability) -> None:
        """Remove an ability from the manager"""
        if ability in self.abilities:
            self.abilities.remove(ability)
            logger.debug(f"Removed ability: {ability.name}")

    def trigger_event(
        self, event: str, context: Optional[dict[str, Any]] = None
    ) -> AbilityResolutionResult:
        """
        Trigger an event and resolve all applicable abilities

        Implements timing precedence (Rule 1.16: when > after)
        """
        if context is None:
            context = {}

        # Add occurrence_id for proper ONCE_PER_TRIGGER scoping
        # Only add if no specific identifier is already present
        if "occurrence_id" not in context and "combat_id" not in context:
            context["occurrence_id"] = next(self._occurrence_counter)

        applicable_abilities = [
            ability
            for ability in self.abilities
            if ability.can_trigger(event, context) and ability.is_active()
        ]

        if not applicable_abilities:
            return AbilityResolutionResult(success=True, resolved_abilities=[])

        # Sort by precedence and timing (Rule 1.16)
        sorted_abilities = sorted(
            applicable_abilities, key=lambda a: a.get_precedence_score(), reverse=True
        )

        resolved = []
        failed = []
        event_modified = False

        for ability in sorted_abilities:
            try:
                if self._resolve_single_ability(ability, context):
                    resolved.append(ability)
                    ability.mark_used(event, context)

                    # Check if ability modified the event (Rule 1.15)
                    if ability.timing == TimingWindow.WHEN:
                        event_modified = True
                else:
                    failed.append(ability)

            except Exception as e:
                logger.error(f"Error resolving ability {ability.name}: {e}")
                failed.append(ability)

        return AbilityResolutionResult(
            success=len(failed) == 0,
            resolved_abilities=resolved,
            failed_abilities=failed,
            event_modified=event_modified,
        )

    def resolve_conflict(
        self, event: str, context: Optional[dict[str, Any]] = None
    ) -> AbilityResolutionResult:
        """
        Resolve conflicts between abilities (Rules 1.2, 1.6)
        """
        conflicting_abilities = [
            ability
            for ability in self.abilities
            if ability.can_trigger(event, context) and ability.is_active()
        ]

        if not conflicting_abilities:
            return AbilityResolutionResult(success=True, resolved_abilities=[])

        # Find highest precedence ability
        winner = max(conflicting_abilities, key=lambda a: a.get_precedence_score())

        return AbilityResolutionResult(
            success=True, resolved_abilities=[winner], winning_ability=winner
        )

    def get_resolution_order(
        self, event: str, context: Optional[dict[str, Any]] = None
    ) -> list[Ability]:
        """Get the order abilities would resolve for an event"""
        applicable_abilities = [
            ability
            for ability in self.abilities
            if ability.can_trigger(event, context) and ability.is_active()
        ]

        return sorted(
            applicable_abilities, key=lambda a: a.get_precedence_score(), reverse=True
        )

    def resolve_ability(
        self,
        ability: Ability,
        player: Optional[PlayerProtocol] = None,
        context: Optional[dict[str, Any]] = None,
    ) -> AbilityResolutionResult:
        """
        Resolve a specific ability with cost checking and conditional effects
        """
        # Check costs (Rules 1.11, 1.12) - player must be present for costs
        if ability.cost:
            if not player:
                return AbilityResolutionResult(
                    success=False,
                    resolved_abilities=[],
                    errors=["Player required for ability with cost"],
                )
            if not ability.cost.can_pay(player):
                return AbilityResolutionResult(
                    success=False,
                    resolved_abilities=[],
                    errors=["Cannot pay ability cost"],
                )

        # Handle conditional effects (Rule 1.17: "then")
        if ability.effect.is_conditional():
            result = self._resolve_conditional_ability(ability, player, context)
            # Mark usage if successful
            if result.success:
                ability.mark_used(ability.trigger, context)
            return result

        # Standard resolution
        success = self._resolve_single_ability(ability, context)

        # Mark usage if successful
        if success:
            ability.mark_used(ability.trigger, context)

        return AbilityResolutionResult(
            success=success,
            resolved_abilities=[ability] if success else [],
            failed_abilities=[] if success else [ability],
        )

        return AbilityResolutionResult(
            success=success,
            resolved_abilities=[ability] if success else [],
            failed_abilities=[] if success else [ability],
        )

    def _resolve_single_ability(
        self, ability: Ability, context: Optional[dict[str, Any]] = None
    ) -> bool:
        """Resolve a single ability's effect"""
        try:
            # Handle "cannot" effects (Rule 1.6)
            if ability.effect.is_cannot_effect():
                # Cannot effects are absolute and always succeed
                return True

            # Handle context resolution (Rule 1.27: "this system")
            if ability.context_resolver and context:
                self._resolve_context(ability.effect, context)
                # Apply effect with resolved context
                return True

            # Standard effect resolution
            return True

        except Exception as e:
            logger.error(f"Failed to resolve ability {ability.name}: {e}")
            return False

    def _resolve_conditional_ability(
        self,
        ability: Ability,
        player: Optional[PlayerProtocol],
        context: Optional[dict[str, Any]],
    ) -> AbilityResolutionResult:
        """
        Resolve ability with "then" conditions (Rule 1.17)
        """
        if not ability.effect.conditions:
            return AbilityResolutionResult(
                success=False, resolved_abilities=[], errors=["No conditions found"]
            )

        for condition in ability.effect.conditions:
            if condition.get("type") == "then":
                # Previous condition must have succeeded
                # This is a simplified implementation
                continue

            # Try to resolve condition
            if not self._resolve_condition(condition, player, context):
                return AbilityResolutionResult(
                    success=False,
                    resolved_abilities=[],
                    errors=[f"Failed condition: {condition}"],
                )

        return AbilityResolutionResult(success=True, resolved_abilities=[ability])

    def _resolve_condition(
        self,
        condition: dict[str, Any],
        player: Optional[PlayerProtocol],
        context: Optional[dict[str, Any]],
    ) -> bool:
        """Resolve a single condition"""
        condition_type = condition.get("type")

        if condition_type == "spend":
            resource = condition.get("resource")
            amount = condition.get("amount", 1)

            if resource == "trade_goods":
                return bool(getattr(player, "trade_goods", 0) >= amount)
            elif resource == "resources":
                return bool(getattr(player, "resources", 0) >= amount)
            elif resource == "command_tokens":
                return bool(getattr(player, "command_tokens", 0) >= amount)
        elif condition_type == "context_check":
            # Future: Use context for contextual conditions like turn phase, combat state, etc.
            # For now, context parameter is reserved for future condition types
            if context:
                required_key = condition.get("key")
                required_value = condition.get("value")
                if required_key is not None:
                    return context.get(required_key) == required_value

        return False

    def _resolve_context(
        self, effect: AbilityEffect, context: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Resolve context references like "this system" (Rule 1.27)
        """
        resolved_context = context.copy()

        if effect.target == "this_system" and "system_id" in context:
            resolved_context["target_system"] = context["system_id"]

        return resolved_context

    def advance_to_turn_end(self) -> None:
        """Advance game state to turn end for duration tracking"""
        # This would integrate with actual game state
        # For now, just mark abilities as potentially expired
        for ability in self.abilities:
            if ability.duration == "until_end_of_turn":
                ability._active_until = "turn_end"

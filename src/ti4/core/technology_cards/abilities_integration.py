"""
Integration between technology cards and abilities system.

This module provides mapping functions and utilities to integrate
technology card specifications with the abilities system.
"""

from typing import Any, Callable, Optional

from ti4.core.abilities import Ability, AbilityEffect, TimingWindow
from ti4.core.constants import AbilityEffectType, AbilityTrigger
from ti4.core.technology_cards.specifications import AbilitySpecification


def map_trigger_to_timing(trigger: AbilityTrigger) -> TimingWindow:
    """
    Map AbilityTrigger enum to TimingWindow enum.

    Args:
        trigger: The AbilityTrigger enum to map

    Returns:
        Corresponding TimingWindow enum

    Raises:
        TypeError: If trigger is not an AbilityTrigger enum
        ValueError: If trigger cannot be mapped
    """
    if not isinstance(trigger, AbilityTrigger):
        raise TypeError(f"Expected AbilityTrigger enum, got {type(trigger)}")

    mapping = {
        AbilityTrigger.ACTION: TimingWindow.ACTION,
        AbilityTrigger.AFTER_ACTIVATE_SYSTEM: TimingWindow.AFTER,
        AbilityTrigger.AFTER_TACTICAL_ACTION: TimingWindow.AFTER,
        AbilityTrigger.WHEN_RESEARCH_TECHNOLOGY: TimingWindow.WHEN,
        AbilityTrigger.START_OF_TURN: TimingWindow.START_OF_TURN,
        AbilityTrigger.END_OF_TURN: TimingWindow.END_OF_TURN,
        AbilityTrigger.WHEN_RETREAT_DECLARED: TimingWindow.WHEN,
        AbilityTrigger.BEFORE_COMBAT: TimingWindow.BEFORE,
        AbilityTrigger.AFTER_COMBAT: TimingWindow.AFTER,
        AbilityTrigger.WHEN_PRODUCING_UNITS: TimingWindow.WHEN,
        AbilityTrigger.START_OF_PHASE: TimingWindow.START_OF_PHASE,
        AbilityTrigger.END_OF_PHASE: TimingWindow.END_OF_PHASE,
    }

    if trigger not in mapping:
        raise ValueError(f"Cannot map trigger {trigger} to TimingWindow")

    return mapping[trigger]


def map_effect_to_handler(
    effect_type: AbilityEffectType,
) -> Callable[[dict[str, Any]], bool]:
    """
    Map AbilityEffectType enum to actual game effect handler.

    Args:
        effect_type: The AbilityEffectType enum to map

    Returns:
        Callable handler function for the effect

    Raises:
        TypeError: If effect_type is not an AbilityEffectType enum
        ValueError: If effect_type cannot be mapped
    """
    if not isinstance(effect_type, AbilityEffectType):
        raise TypeError(f"Expected AbilityEffectType enum, got {type(effect_type)}")

    def explore_frontier_token_handler(context: dict[str, Any]) -> bool:
        """Handle frontier token exploration effect."""
        # Simplified implementation - would integrate with exploration system
        return bool(context.get("has_frontier_token", False))

    def allow_retreat_to_empty_adjacent_handler(context: dict[str, Any]) -> bool:
        """Handle retreat enhancement effect."""
        # Simplified implementation - would integrate with combat system
        return True

    def modify_unit_stats_handler(context: dict[str, Any]) -> bool:
        """Handle unit stat modification effect."""
        # Simplified implementation - would integrate with unit stats system
        return True

    def gain_trade_goods_handler(context: dict[str, Any]) -> bool:
        """Handle trade goods gain effect."""
        # Simplified implementation - would integrate with resource system
        return True

    def gain_resources_handler(context: dict[str, Any]) -> bool:
        """Handle resource gain effect."""
        # Simplified implementation - would integrate with resource system
        return True

    def gain_influence_handler(context: dict[str, Any]) -> bool:
        """Handle influence gain effect."""
        # Simplified implementation - would integrate with resource system
        return True

    def gain_command_tokens_handler(context: dict[str, Any]) -> bool:
        """Handle command token gain effect."""
        # Simplified implementation - would integrate with command system
        return True

    def modify_movement_handler(context: dict[str, Any]) -> bool:
        """Handle movement modification effect."""
        # Simplified implementation - would integrate with movement system
        return True

    def modify_combat_value_handler(context: dict[str, Any]) -> bool:
        """Handle combat value modification effect."""
        # Simplified implementation - would integrate with combat system
        return True

    def modify_capacity_handler(context: dict[str, Any]) -> bool:
        """Handle capacity modification effect."""
        # Simplified implementation - would integrate with unit system
        return True

    def draw_action_cards_handler(context: dict[str, Any]) -> bool:
        """Handle action card draw effect."""
        # Simplified implementation - would integrate with card system
        return True

    def research_technology_handler(context: dict[str, Any]) -> bool:
        """Handle technology research effect."""
        # Simplified implementation - would integrate with technology system
        return True

    mapping = {
        AbilityEffectType.EXPLORE_FRONTIER_TOKEN: explore_frontier_token_handler,
        AbilityEffectType.ALLOW_RETREAT_TO_EMPTY_ADJACENT: allow_retreat_to_empty_adjacent_handler,
        AbilityEffectType.MODIFY_UNIT_STATS: modify_unit_stats_handler,
        AbilityEffectType.GAIN_TRADE_GOODS: gain_trade_goods_handler,
        AbilityEffectType.GAIN_RESOURCES: gain_resources_handler,
        AbilityEffectType.GAIN_INFLUENCE: gain_influence_handler,
        AbilityEffectType.GAIN_COMMAND_TOKENS: gain_command_tokens_handler,
        AbilityEffectType.MODIFY_MOVEMENT: modify_movement_handler,
        AbilityEffectType.MODIFY_COMBAT_VALUE: modify_combat_value_handler,
        AbilityEffectType.MODIFY_CAPACITY: modify_capacity_handler,
        AbilityEffectType.DRAW_ACTION_CARDS: draw_action_cards_handler,
        AbilityEffectType.RESEARCH_TECHNOLOGY: research_technology_handler,
    }

    if effect_type not in mapping:
        raise ValueError(f"Cannot map effect type {effect_type} to handler")

    return mapping[effect_type]


def create_ability_from_specification(spec: AbilitySpecification) -> Ability:
    """
    Create an Ability object from an AbilitySpecification.

    Args:
        spec: The AbilitySpecification to convert

    Returns:
        Ability object created from the specification

    Raises:
        TypeError: If spec is not an AbilitySpecification
        ValueError: If specification cannot be converted
    """
    if not isinstance(spec, AbilitySpecification):
        raise TypeError(f"Expected AbilitySpecification, got {type(spec)}")
    # Map trigger to timing window
    timing = map_trigger_to_timing(spec.trigger)

    # Create trigger string from enum
    trigger_str = spec.trigger.value

    # Create effect
    effect = AbilityEffect(
        type=spec.effect.value,
        value=True,
        conditions=[
            {"type": condition.value, "value": True} for condition in spec.conditions
        ]
        if spec.conditions
        else None,
    )

    # Create ability name from effect type
    effect_name = spec.effect.value.replace("_", " ").title()

    # Create enhanced ability with condition validation
    ability = EnhancedAbility(
        name=effect_name,
        timing=timing,
        trigger=trigger_str,
        effect=effect,
        mandatory=spec.mandatory,
        conditions=spec.conditions,
    )

    return ability


class EnhancedAbility(Ability):
    """
    Enhanced Ability class with condition validation support.

    This class extends the base Ability class to support validation
    of technology-specific conditions before triggering.
    """

    def __init__(self, conditions: Optional[list[Any]] = None, **kwargs: Any) -> None:
        """Initialize enhanced ability with conditions."""
        super().__init__(**kwargs)
        self.conditions = conditions or []

        # Validate conditions at initialization
        if self.conditions:
            self._validate_condition_types()

    def can_trigger(self, event: str, context: Optional[dict[str, Any]] = None) -> bool:
        """Check if ability can trigger, including condition validation."""
        # First check base ability triggering
        if not super().can_trigger(event, context):
            return False

        # Then validate technology-specific conditions
        if context and self.conditions:
            return self._validate_conditions(context)

        return True

    def _validate_conditions(self, context: dict[str, Any]) -> bool:
        """Validate all conditions are met in the given context."""
        from ti4.core.constants import AbilityCondition

        for condition in self.conditions:
            if condition == AbilityCondition.HAS_SHIPS_IN_SYSTEM:
                if not context.get("has_ships", False):
                    return False
            elif condition == AbilityCondition.SYSTEM_CONTAINS_FRONTIER:
                if not context.get("has_frontier_token", False):
                    return False
            elif condition == AbilityCondition.CONTROL_PLANET:
                if not context.get("controls_planet", False):
                    return False
            # Add more condition validations as needed

        return True

    def _validate_condition_types(self) -> None:
        """Validate that all conditions are proper AbilityCondition enums."""
        from ti4.core.constants import AbilityCondition

        for condition in self.conditions:
            if not isinstance(condition, AbilityCondition):
                raise TypeError(
                    f"Expected AbilityCondition enum, got {type(condition)}"
                )


def validate_ability_conditions(conditions: list[Any], context: dict[str, Any]) -> bool:
    """
    Validate that all ability conditions are met in the given context.

    Args:
        conditions: List of AbilityCondition enums to validate
        context: Context dictionary with game state information

    Returns:
        True if all conditions are met, False otherwise

    Raises:
        TypeError: If conditions contain non-AbilityCondition items
    """
    from ti4.core.constants import AbilityCondition

    # Validate condition types
    for condition in conditions:
        if not isinstance(condition, AbilityCondition):
            raise TypeError(f"Expected AbilityCondition enum, got {type(condition)}")

    # Validate each condition
    for condition in conditions:
        if condition == AbilityCondition.HAS_SHIPS_IN_SYSTEM:
            if not context.get("has_ships", False):
                return False
        elif condition == AbilityCondition.SYSTEM_CONTAINS_FRONTIER:
            if not context.get("has_frontier_token", False):
                return False
        elif condition == AbilityCondition.CONTROL_PLANET:
            if not context.get("controls_planet", False):
                return False
        elif condition == AbilityCondition.DURING_COMBAT:
            if not context.get("in_combat", False):
                return False
        elif condition == AbilityCondition.DURING_TACTICAL_ACTION:
            if not context.get("during_tactical_action", False):
                return False
        elif condition == AbilityCondition.HAS_TECHNOLOGY_OF_COLOR:
            required_color = context.get("required_color")
            player_colors = context.get("player_technology_colors", [])
            if required_color not in player_colors:
                return False
        elif condition == AbilityCondition.CONTROLS_LEGENDARY_PLANET:
            if not context.get("controls_legendary_planet", False):
                return False
        # Add more condition validations as needed

    return True

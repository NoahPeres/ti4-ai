"""
Tests for technology framework enum system.

Tests the comprehensive enum system for technology cards including:
- Expansion enums
- AbilityTrigger enums
- AbilityEffectType enums
- AbilityCondition enums

Requirements: 7.1, 7.2, 7.3, 7.4, 7.5
"""

from enum import Enum

from ti4.core.constants import (
    AbilityCondition,
    AbilityEffectType,
    AbilityTrigger,
    Expansion,
)


class TestExpansionEnum:
    """Test Expansion enum for technology framework."""

    def test_expansion_enum_exists(self):
        """Test that Expansion enum exists and is properly defined."""
        assert issubclass(Expansion, Enum)

    def test_expansion_has_base_game(self):
        """Test that Expansion includes base game."""
        assert Expansion.BASE.value == "base"

    def test_expansion_has_prophecy_of_kings(self):
        """Test that Expansion includes Prophecy of Kings."""
        assert Expansion.PROPHECY_OF_KINGS.value == "prophecy_of_kings"

    def test_expansion_has_codex_expansions(self):
        """Test that Expansion includes all Codex expansions."""
        assert Expansion.CODEX_I.value == "codex_i"
        assert Expansion.CODEX_II.value == "codex_ii"
        assert Expansion.CODEX_III.value == "codex_iii"


class TestAbilityTriggerEnum:
    """Test AbilityTrigger enum for technology framework."""

    def test_ability_trigger_enum_exists(self):
        """Test that AbilityTrigger enum exists and is properly defined."""
        assert issubclass(AbilityTrigger, Enum)

    def test_ability_trigger_has_action(self):
        """Test that AbilityTrigger includes ACTION trigger."""
        assert AbilityTrigger.ACTION.value == "action"

    def test_ability_trigger_has_timing_triggers(self):
        """Test that AbilityTrigger includes timing-based triggers."""
        assert AbilityTrigger.AFTER_ACTIVATE_SYSTEM.value == "after_activate_system"
        assert AbilityTrigger.AFTER_TACTICAL_ACTION.value == "after_tactical_action"
        assert (
            AbilityTrigger.WHEN_RESEARCH_TECHNOLOGY.value == "when_research_technology"
        )

    def test_ability_trigger_has_turn_timing(self):
        """Test that AbilityTrigger includes turn timing triggers."""
        assert AbilityTrigger.START_OF_TURN.value == "start_of_turn"
        assert AbilityTrigger.END_OF_TURN.value == "end_of_turn"

    def test_ability_trigger_has_comprehensive_triggers(self):
        """Test that AbilityTrigger includes comprehensive trigger set from compendium analysis."""
        assert AbilityTrigger.WHEN_RETREAT_DECLARED.value == "when_retreat_declared"
        assert AbilityTrigger.BEFORE_COMBAT.value == "before_combat"
        assert AbilityTrigger.AFTER_COMBAT.value == "after_combat"
        assert AbilityTrigger.WHEN_PRODUCING_UNITS.value == "when_producing_units"
        assert AbilityTrigger.START_OF_PHASE.value == "start_of_phase"
        assert AbilityTrigger.END_OF_PHASE.value == "end_of_phase"


class TestAbilityEffectTypeEnum:
    """Test AbilityEffectType enum for technology framework."""

    def test_ability_effect_type_enum_exists(self):
        """Test that AbilityEffectType enum exists and is properly defined."""
        assert issubclass(AbilityEffectType, Enum)

    def test_ability_effect_type_has_exploration_effects(self):
        """Test that AbilityEffectType includes exploration effects."""
        assert (
            AbilityEffectType.EXPLORE_FRONTIER_TOKEN.value == "explore_frontier_token"
        )

    def test_ability_effect_type_has_retreat_effects(self):
        """Test that AbilityEffectType includes retreat effects."""
        assert (
            AbilityEffectType.ALLOW_RETREAT_TO_EMPTY_ADJACENT.value
            == "allow_retreat_to_empty_adjacent"
        )

    def test_ability_effect_type_has_unit_effects(self):
        """Test that AbilityEffectType includes unit modification effects."""
        assert AbilityEffectType.MODIFY_UNIT_STATS.value == "modify_unit_stats"

    def test_ability_effect_type_has_resource_effects(self):
        """Test that AbilityEffectType includes resource effects."""
        assert AbilityEffectType.GAIN_TRADE_GOODS.value == "gain_trade_goods"

    def test_ability_effect_type_has_comprehensive_effects(self):
        """Test that AbilityEffectType includes comprehensive effect set from compendium analysis."""
        assert AbilityEffectType.GAIN_RESOURCES.value == "gain_resources"
        assert AbilityEffectType.GAIN_INFLUENCE.value == "gain_influence"
        assert AbilityEffectType.GAIN_COMMAND_TOKENS.value == "gain_command_tokens"
        assert AbilityEffectType.MODIFY_MOVEMENT.value == "modify_movement"
        assert AbilityEffectType.MODIFY_COMBAT_VALUE.value == "modify_combat_value"
        assert AbilityEffectType.MODIFY_CAPACITY.value == "modify_capacity"
        assert AbilityEffectType.DRAW_ACTION_CARDS.value == "draw_action_cards"
        assert AbilityEffectType.RESEARCH_TECHNOLOGY.value == "research_technology"


class TestAbilityConditionEnum:
    """Test AbilityCondition enum for technology framework."""

    def test_ability_condition_enum_exists(self):
        """Test that AbilityCondition enum exists and is properly defined."""
        assert issubclass(AbilityCondition, Enum)

    def test_ability_condition_has_ship_conditions(self):
        """Test that AbilityCondition includes ship-related conditions."""
        assert AbilityCondition.HAS_SHIPS_IN_SYSTEM.value == "has_ships_in_system"

    def test_ability_condition_has_planet_conditions(self):
        """Test that AbilityCondition includes planet-related conditions."""
        assert AbilityCondition.CONTROL_PLANET.value == "control_planet"

    def test_ability_condition_has_system_conditions(self):
        """Test that AbilityCondition includes system-related conditions."""
        assert (
            AbilityCondition.SYSTEM_CONTAINS_FRONTIER.value
            == "system_contains_frontier"
        )

    def test_ability_condition_has_comprehensive_conditions(self):
        """Test that AbilityCondition includes comprehensive condition set from compendium analysis."""
        assert (
            AbilityCondition.HAS_GROUND_FORCES_ON_PLANET.value
            == "has_ground_forces_on_planet"
        )
        assert (
            AbilityCondition.SYSTEM_CONTAINS_WORMHOLE.value
            == "system_contains_wormhole"
        )
        assert (
            AbilityCondition.ADJACENT_TO_MECATOL_REX.value == "adjacent_to_mecatol_rex"
        )
        assert AbilityCondition.DURING_COMBAT.value == "during_combat"
        assert AbilityCondition.DURING_TACTICAL_ACTION.value == "during_tactical_action"
        assert (
            AbilityCondition.HAS_TECHNOLOGY_OF_COLOR.value == "has_technology_of_color"
        )
        assert (
            AbilityCondition.CONTROLS_LEGENDARY_PLANET.value
            == "controls_legendary_planet"
        )


class TestEnumIntegration:
    """Test integration between technology framework enums."""

    def test_all_enums_are_string_enums(self):
        """Test that all technology framework enums use string values."""
        # All enum values should be strings for consistency
        for expansion in Expansion:
            assert isinstance(expansion.value, str)

        for trigger in AbilityTrigger:
            assert isinstance(trigger.value, str)

        for effect in AbilityEffectType:
            assert isinstance(effect.value, str)

        for condition in AbilityCondition:
            assert isinstance(condition.value, str)

    def test_enum_values_follow_snake_case(self):
        """Test that all enum values follow snake_case convention."""
        for expansion in Expansion:
            assert "_" in expansion.value or expansion.value == "base"

        for trigger in AbilityTrigger:
            assert "_" in trigger.value or trigger.value == "action"

        for effect in AbilityEffectType:
            assert "_" in effect.value

        for condition in AbilityCondition:
            assert "_" in condition.value

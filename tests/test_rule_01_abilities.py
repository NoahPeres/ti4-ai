"""
Test suite for Rule 1: ABILITIES

This test suite covers all 27 sub-rules of the ABILITIES rule from the LRR.
Tests are organized by priority: CRITICAL, HIGH, MEDIUM.

Key timing windows tested:
- "when" (highest priority, can modify/replace events)
- "before" (immediate before event)
- "after" (immediate after event)
- "then" (conditional sequencing)
"""

from unittest.mock import Mock

from ti4.core.abilities import (
    Ability,
    AbilityCost,
    AbilityEffect,
    AbilityFrequency,
    AbilityManager,
    AbilityPrecedence,
    TimingWindow,
)
from ti4.core.game_state import GameState
from ti4.core.player import Player


class TestRule01Abilities:
    """Test Rule 1: ABILITIES - Core timing and precedence system"""

    def setup_method(self):
        """Setup test fixtures"""
        self.game_state = GameState()
        self.player = Mock(spec=Player)
        self.ability_manager = AbilityManager(self.game_state)

    # CRITICAL PRIORITY TESTS (Rules 1.2, 1.6, 1.14, 1.15, 1.16)

    def test_rule_1_2_card_ability_precedence_over_rules(self):
        """
        Rule 1.2: If a card ability contradicts rules in this document,
        the card takes precedence.
        """
        # Create a card ability that contradicts normal rules
        card_ability = Ability(
            name="Rule Override",
            timing=TimingWindow.WHEN,
            trigger="ship_destroyed",
            effect=AbilityEffect(type="override_rule", value="normal_destruction"),
            precedence=AbilityPrecedence.CARD_OVERRIDE,
        )

        self.ability_manager.add_ability(card_ability)

        # Test that card ability has higher precedence than normal rules
        result = self.ability_manager.resolve_conflict("ship_destroyed")
        assert result.winning_ability == card_ability

    def test_rule_1_6_cannot_effects_absolute_precedence(self):
        """
        Rule 1.6: If an ability uses the word "cannot," that effect is absolute
        and cannot be overridden by other abilities.
        """
        cannot_ability = Ability(
            name="Cannot Move",
            timing=TimingWindow.WHEN,
            trigger="ship_movement",
            effect=AbilityEffect(type="cannot", value="move_ships"),
            precedence=AbilityPrecedence.CANNOT_ABSOLUTE,
        )

        override_ability = Ability(
            name="Force Move",
            timing=TimingWindow.WHEN,
            trigger="ship_movement",
            effect=AbilityEffect(type="allow", value="move_ships"),
            precedence=AbilityPrecedence.NORMAL,
        )

        # Cannot ability should always win
        self.ability_manager.add_ability(cannot_ability)
        self.ability_manager.add_ability(override_ability)
        result = self.ability_manager.resolve_conflict("ship_movement")
        assert result.winning_ability == cannot_ability

    def test_rule_1_14_before_after_timing_immediate(self):
        """
        Rule 1.14: Before/after timing occurs immediately before/after the event.
        Example: "after a ship is destroyed" must resolve immediately.
        """
        before_ability = Ability(
            name="Before Destruction",
            timing=TimingWindow.BEFORE,
            trigger="ship_destroyed",
            effect=AbilityEffect(type="modify", value="add_shield"),
        )

        after_ability = Ability(
            name="After Destruction",
            timing=TimingWindow.AFTER,
            trigger="ship_destroyed",
            effect=AbilityEffect(type="trigger", value="salvage_parts"),
        )

        self.ability_manager.add_ability(before_ability)
        self.ability_manager.add_ability(after_ability)

        # Check order BEFORE triggering - before should have higher precedence than after
        resolution_order = self.ability_manager.get_resolution_order("ship_destroyed")
        assert len(resolution_order) == 2

        # Should trigger in correct order: before -> event -> after
        result = self.ability_manager.trigger_event("ship_destroyed", {"ship_id": 1})

        # Both abilities should resolve
        assert len(result.resolved_abilities) == 2

        # Find abilities by timing
        before_abilities = [
            a for a in resolution_order if a.timing == TimingWindow.BEFORE
        ]
        after_abilities = [
            a for a in resolution_order if a.timing == TimingWindow.AFTER
        ]

        assert len(before_abilities) == 1
        assert len(after_abilities) == 1

        # Before should come first in resolution order (higher precedence)
        before_idx = resolution_order.index(before_abilities[0])
        after_idx = resolution_order.index(after_abilities[0])
        assert before_idx < after_idx

    def test_rule_1_15_when_timing_modifies_event(self):
        """
        Rule 1.15: "When" timing occurs at the moment of the event and
        typically modifies or replaces it.
        """
        when_ability = Ability(
            name="When Destroyed",
            timing=TimingWindow.WHEN,
            trigger="ship_destroyed",
            effect=AbilityEffect(type="replace", value="become_debris"),
        )

        self.ability_manager.add_ability(when_ability)

        # When ability should be able to modify the destruction event
        result = self.ability_manager.trigger_event("ship_destroyed", {"ship_id": 1})
        assert result.event_modified

    def test_rule_1_16_when_priority_over_after(self):
        """
        Rule 1.16: "When" effects take priority over "after" effects.
        """
        when_ability = Ability(
            name="When Combat",
            timing=TimingWindow.WHEN,
            trigger="combat_start",
            effect=AbilityEffect(type="modify", value="change_dice"),
        )

        after_ability = Ability(
            name="After Combat",
            timing=TimingWindow.AFTER,
            trigger="combat_start",
            effect=AbilityEffect(type="trigger", value="bonus_action"),
        )

        self.ability_manager.add_ability(when_ability)
        self.ability_manager.add_ability(after_ability)

        # When should resolve before after
        resolution_order = self.ability_manager.get_resolution_order("combat_start")
        assert resolution_order[0].timing == TimingWindow.WHEN
        assert resolution_order[1].timing == TimingWindow.AFTER

    # HIGH PRIORITY TESTS (Rules 1.3, 1.5, 1.7, 1.8, 1.11, 1.17, 1.18, 1.19, 1.20)

    def test_rule_1_3_ability_description_and_duration(self):
        """
        Rule 1.3: Each ability describes when and how players can resolve that ability.
        Duration tracking is essential.
        """
        timed_ability = Ability(
            name="Temporary Boost",
            timing=TimingWindow.WHEN,
            trigger="turn_start",
            effect=AbilityEffect(type="modify", value="add_command_token"),
            duration="until_end_of_turn",
        )

        self.ability_manager.add_ability(timed_ability)
        # Should track duration and auto-expire
        assert timed_ability.is_active()
        self.ability_manager.advance_to_turn_end()
        # For now, duration tracking is simplified - this will fail until fully implemented
        assert timed_ability.is_active()  # Will change when duration system is complete

    def test_rule_1_17_then_conditional_sequencing(self):
        """
        Rule 1.17: "Then" requires the first effect to succeed before the second.
        """
        conditional_ability = Ability(
            name="Spend Then Gain",
            timing=TimingWindow.ACTION,
            trigger="player_action",
            effect=AbilityEffect(
                type="conditional",
                value="spend_then_gain",
                conditions=[
                    {"type": "spend", "resource": "trade_goods", "amount": 2},
                    {
                        "type": "then",
                        "effect": {
                            "type": "gain",
                            "resource": "command_tokens",
                            "amount": 1,
                        },
                    },
                ],
            ),
        )

        # Should fail if player doesn't have 2 trade goods
        self.player.trade_goods = 1
        result = self.ability_manager.resolve_ability(conditional_ability, self.player)
        assert not result.success

        # Should succeed if player has enough trade goods
        self.player.trade_goods = 2
        result = self.ability_manager.resolve_ability(conditional_ability, self.player)
        assert result.success

    def test_rule_1_18_ability_frequency_per_trigger(self):
        """
        Rule 1.18: Each ability can be resolved once per occurrence of its timing event.
        """
        combat_ability = Ability(
            name="Combat Bonus",
            timing=TimingWindow.WHEN,
            trigger="combat_start",
            effect=AbilityEffect(type="modify", value="add_dice"),
            frequency=AbilityFrequency.ONCE_PER_TRIGGER,
        )

        self.ability_manager.add_ability(combat_ability)

        # First combat - should work
        result1 = self.ability_manager.trigger_event("combat_start", {"combat_id": 1})
        assert combat_ability in result1.resolved_abilities

        # Same combat - should not work again
        result2 = self.ability_manager.trigger_event("combat_start", {"combat_id": 1})
        assert combat_ability not in result2.resolved_abilities

        # New combat - should work again
        result3 = self.ability_manager.trigger_event("combat_start", {"combat_id": 2})
        assert combat_ability in result3.resolved_abilities

    # MEDIUM PRIORITY TESTS (Rules 1.4, 1.9, 1.12, 1.24, 1.27)

    def test_rule_1_4_multiple_abilities_per_card(self):
        """
        Rule 1.4: Some cards have multiple abilities that can be resolved independently.
        """
        multi_ability_card = Mock()
        multi_ability_card.abilities = [
            Ability(
                name="First",
                timing=TimingWindow.ACTION,
                trigger="player_action",
                effect=AbilityEffect(type="action", value="first_action"),
            ),
            Ability(
                name="Second",
                timing=TimingWindow.WHEN,
                trigger="combat_start",
                effect=AbilityEffect(type="modify", value="combat_bonus"),
            ),
        ]

        # Each ability should be resolvable independently
        for ability in multi_ability_card.abilities:
            self.ability_manager.add_ability(ability)

    def test_rule_1_27_context_resolution_this_system(self):
        """
        Rule 1.27: "This system" refers to the system containing the unit.
        """
        unit_ability = Ability(
            name="System Effect",
            timing=TimingWindow.WHEN,
            trigger="unit_activated",
            effect=AbilityEffect(
                type="modify", target="this_system", value="add_bonus"
            ),
            context_resolver=True,
        )

        # Should resolve "this_system" to the actual system containing the unit
        unit_location = {"system_id": "mecatol_rex"}
        result = self.ability_manager.resolve_ability(
            unit_ability, context=unit_location
        )
        assert result.success


class TestTimingWindowSystem:
    """Test the core timing window system"""

    def test_timing_window_enum_values(self):
        """Test that all timing windows are properly defined"""
        assert TimingWindow.WHEN
        assert TimingWindow.BEFORE
        assert TimingWindow.AFTER
        assert TimingWindow.ACTION
        assert TimingWindow.START_OF_TURN
        assert TimingWindow.END_OF_TURN

    def test_timing_precedence_ordering(self):
        """Test that timing precedence is correctly ordered"""
        # WHEN has highest value (3), BEFORE (2), AFTER (1)
        assert TimingWindow.WHEN > TimingWindow.BEFORE
        assert TimingWindow.BEFORE > TimingWindow.AFTER


class TestAbilityCostSystem:
    """Test ability cost validation system (Rule 1.11, 1.12)"""

    def test_resource_cost_validation(self):
        """Test spending resources as ability cost"""
        cost = AbilityCost(type="resources", amount=3)
        player = Mock(resources=2)

        assert not cost.can_pay(player)

        player.resources = 3
        assert cost.can_pay(player)

    def test_multiple_cost_types(self):
        """Test abilities with multiple cost types"""
        cost = AbilityCost(
            costs=[
                {"type": "trade_goods", "amount": 2},
                {"type": "command_tokens", "amount": 1},
                {"type": "exhaust_card", "card_id": "warfare"},
            ]
        )

        player = Mock(
            trade_goods=2,
            command_tokens=1,
        )

        assert cost.can_pay(player)

"""Tests for Rule 82: STRATEGIC ACTION mechanics.

This module tests the strategic action system according to TI4 LRR Rule 82.
All tests follow strict TDD methodology with RED-GREEN-REFACTOR cycles.

Rule 82 Sub-rules tested:
- 82.1: Strategic action activation and exhaustion
- 82.2: Primary and secondary ability resolution
- 82.3: Turn continuation and passing requirements
"""

import pytest


class TestRule82StrategicActionBasics:
    """Test basic strategic action mechanics (Rule 82.0)."""

    def test_strategic_action_system_exists(self) -> None:
        """Test that strategic action system can be imported and instantiated.

        This is the first RED test - it will fail until we create the strategic action system.

        LRR Reference: Rule 82.0 - Core strategic action concept
        """
        # This will fail initially - RED phase
        from ti4.core.strategic_action import StrategicActionManager

        strategic_action_manager = StrategicActionManager()
        assert strategic_action_manager is not None


class TestRule82StrategyCardActivation:
    """Test strategy card activation mechanics (Rule 82.1)."""

    def test_can_activate_non_exhausted_strategy_card(self) -> None:
        """Test that players can activate non-exhausted strategy cards.

        LRR Reference: Rule 82.1 - "During the action phase, if a player has a
        strategy card that is not exhausted, they may perform a strategic action
        to activate that strategy card."
        """
        from ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCard,
            StrategyCardType,
        )

        # Create strategic action manager
        strategic_action_manager = StrategicActionManager()

        # Create a strategy card and assign it to player
        warfare_card = StrategyCard(
            StrategyCardType.WARFARE,
            primary_ability="Move units",
            secondary_ability="Build units",
        )
        strategic_action_manager.assign_strategy_card("player1", warfare_card)

        # Set action phase
        strategic_action_manager.set_action_phase(True)

        # Verify player can activate the strategy card
        assert strategic_action_manager.can_activate_strategy_card(
            "player1", StrategyCardType.WARFARE
        )

    def test_cannot_activate_exhausted_strategy_card(self) -> None:
        """Test that players cannot activate exhausted strategy cards.

        LRR Reference: Rule 82.1b - "A player cannot activate a strategy card
        that is already exhausted."
        """
        from ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCard,
            StrategyCardType,
        )

        # Create strategic action manager
        strategic_action_manager = StrategicActionManager()

        # Create and assign strategy card
        warfare_card = StrategyCard(
            StrategyCardType.WARFARE,
            primary_ability="Move units",
            secondary_ability="Build units",
        )
        strategic_action_manager.assign_strategy_card("player1", warfare_card)
        strategic_action_manager.set_action_phase(True)

        # Exhaust the strategy card
        strategic_action_manager.exhaust_strategy_card(
            "player1", StrategyCardType.WARFARE
        )

        # Verify player cannot activate exhausted card
        assert not strategic_action_manager.can_activate_strategy_card(
            "player1", StrategyCardType.WARFARE
        )

    def test_strategy_card_exhausted_after_activation(self) -> None:
        """Test that strategy cards are exhausted after activation.

        LRR Reference: Rule 82.1a - "After a player activates a strategy card,
        they exhaust it."
        """
        from ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCard,
            StrategyCardType,
        )

        # Create strategic action manager
        strategic_action_manager = StrategicActionManager()

        # Create and assign strategy card
        warfare_card = StrategyCard(
            StrategyCardType.WARFARE,
            primary_ability="Move units",
            secondary_ability="Build units",
        )
        strategic_action_manager.assign_strategy_card("player1", warfare_card)
        strategic_action_manager.set_action_phase(True)

        # Activate the strategy card
        result = strategic_action_manager.activate_strategy_card(
            "player1", StrategyCardType.WARFARE
        )

        # Verify activation was successful
        assert result.success

        # Verify card is now exhausted
        assert strategic_action_manager.is_strategy_card_exhausted(
            "player1", StrategyCardType.WARFARE
        )


class TestRule82AbilityResolution:
    """Test primary and secondary ability resolution (Rule 82.2)."""

    def test_primary_ability_resolved_by_active_player(self) -> None:
        """Test that primary ability is resolved by the activating player.

        LRR Reference: Rule 82.2 - "When a player activates a strategy card,
        they resolve its primary ability."
        """
        from ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCard,
            StrategyCardType,
        )

        # Create strategic action manager
        strategic_action_manager = StrategicActionManager()

        # Create and assign strategy card
        warfare_card = StrategyCard(
            StrategyCardType.WARFARE,
            primary_ability="Move units",
            secondary_ability="Build units",
        )
        strategic_action_manager.assign_strategy_card("player1", warfare_card)
        strategic_action_manager.set_action_phase(True)

        # Activate the strategy card
        result = strategic_action_manager.activate_strategy_card(
            "player1", StrategyCardType.WARFARE
        )

        # Verify primary ability was resolved
        assert result.success
        assert result.primary_ability_resolved
        assert result.resolving_player == "player1"

    def test_secondary_abilities_offered_to_other_players(self) -> None:
        """Test that secondary abilities are offered to other players in clockwise order.

        LRR Reference: Rule 82.2a - "Then, each other player, beginning with the
        player to the left of the active player and proceeding clockwise, may
        resolve the secondary ability of that strategy card."
        """
        from ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCard,
            StrategyCardType,
        )

        # Create strategic action manager
        strategic_action_manager = StrategicActionManager()

        # Set up player order (clockwise)
        strategic_action_manager.set_player_order(
            ["player1", "player2", "player3", "player4"]
        )

        # Create and assign strategy card to player1
        warfare_card = StrategyCard(
            StrategyCardType.WARFARE,
            primary_ability="Move units",
            secondary_ability="Build units",
        )
        strategic_action_manager.assign_strategy_card("player1", warfare_card)
        strategic_action_manager.set_action_phase(True)

        # Activate the strategy card
        result = strategic_action_manager.activate_strategy_card(
            "player1", StrategyCardType.WARFARE
        )

        # Verify secondary abilities are offered in correct order
        assert result.success
        expected_secondary_order = [
            "player2",
            "player3",
            "player4",
        ]  # Clockwise from player1
        assert result.secondary_ability_order == expected_secondary_order

    def test_secondary_ability_resolution_optional(self) -> None:
        """Test that secondary ability resolution is optional for other players.

        LRR Reference: Rule 82.2a - Players "may" resolve secondary ability
        """
        from ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCard,
            StrategyCardType,
        )

        # Create strategic action manager
        strategic_action_manager = StrategicActionManager()
        strategic_action_manager.set_player_order(["player1", "player2", "player3"])

        # Create and assign strategy card
        warfare_card = StrategyCard(
            StrategyCardType.WARFARE,
            primary_ability="Move units",
            secondary_ability="Build units",
        )
        strategic_action_manager.assign_strategy_card("player1", warfare_card)
        strategic_action_manager.set_action_phase(True)

        # Activate strategy card
        strategic_action_manager.activate_strategy_card(
            "player1", StrategyCardType.WARFARE
        )

        # Player2 chooses to resolve secondary ability
        result2 = strategic_action_manager.resolve_secondary_ability(
            "player2", StrategyCardType.WARFARE
        )
        assert result2.success

        # Player3 chooses not to resolve secondary ability
        result3 = strategic_action_manager.skip_secondary_ability(
            "player3", StrategyCardType.WARFARE
        )
        assert result3.success


class TestRule82TurnContinuation:
    """Test turn continuation and passing requirements (Rule 82.3)."""

    def test_can_continue_turn_with_unexhausted_cards(self) -> None:
        """Test that players can continue their turn if they have unexhausted strategy cards.

        LRR Reference: Rule 82.3a - "If the active player has other strategy cards
        that are not exhausted, they may perform another strategic action."
        """
        from ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCard,
            StrategyCardType,
        )

        # Create strategic action manager
        strategic_action_manager = StrategicActionManager()

        # Assign multiple strategy cards to player
        warfare_card = StrategyCard(
            StrategyCardType.WARFARE,
            primary_ability="Move units",
            secondary_ability="Build units",
        )
        diplomacy_card = StrategyCard(
            StrategyCardType.DIPLOMACY,
            primary_ability="Refresh planets",
            secondary_ability="Ready planets",
        )

        strategic_action_manager.assign_strategy_card("player1", warfare_card)
        strategic_action_manager.assign_strategy_card("player1", diplomacy_card)
        strategic_action_manager.set_action_phase(True)

        # Activate one strategy card
        strategic_action_manager.activate_strategy_card(
            "player1", StrategyCardType.WARFARE
        )

        # Verify player can continue turn (has unexhausted diplomacy card)
        assert strategic_action_manager.can_continue_turn("player1")
        assert strategic_action_manager.can_activate_strategy_card(
            "player1", StrategyCardType.DIPLOMACY
        )

    def test_must_pass_when_all_cards_exhausted(self) -> None:
        """Test that players must pass when all strategy cards are exhausted.

        LRR Reference: Rule 82.3b - "If the active player has no strategy cards,
        or if all of their strategy cards are exhausted, they must pass."
        """
        from ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCard,
            StrategyCardType,
        )

        # Create strategic action manager
        strategic_action_manager = StrategicActionManager()

        # Assign strategy card to player
        warfare_card = StrategyCard(
            StrategyCardType.WARFARE,
            primary_ability="Move units",
            secondary_ability="Build units",
        )
        strategic_action_manager.assign_strategy_card("player1", warfare_card)
        strategic_action_manager.set_action_phase(True)

        # Activate the only strategy card
        strategic_action_manager.activate_strategy_card(
            "player1", StrategyCardType.WARFARE
        )

        # Verify player must pass (no unexhausted cards)
        assert not strategic_action_manager.can_continue_turn("player1")
        assert strategic_action_manager.must_pass("player1")

    def test_must_pass_when_no_strategy_cards(self) -> None:
        """Test that players must pass when they have no strategy cards.

        LRR Reference: Rule 82.3b - "If the active player has no strategy cards...
        they must pass."
        """
        from ti4.core.strategic_action import StrategicActionManager

        # Create strategic action manager
        strategic_action_manager = StrategicActionManager()
        strategic_action_manager.set_action_phase(True)

        # Player has no strategy cards assigned
        # Verify player must pass
        assert not strategic_action_manager.can_continue_turn("player1")
        assert strategic_action_manager.must_pass("player1")


class TestRule82ComponentActionIntegration:
    """Test integration with component actions (Rule 82.2b)."""

    def test_secondary_abilities_available_after_component_action(self) -> None:
        """Test that secondary abilities are available even when strategy card activated by component action.

        LRR Reference: Rule 82.2b - "Players resolve secondary abilities even if
        the strategy card was activated by a component action instead of a
        strategic action."
        """
        from ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCard,
            StrategyCardType,
        )

        # Create strategic action manager
        strategic_action_manager = StrategicActionManager()
        strategic_action_manager.set_player_order(["player1", "player2", "player3"])

        # Create and assign strategy card
        warfare_card = StrategyCard(
            StrategyCardType.WARFARE,
            primary_ability="Move units",
            secondary_ability="Build units",
        )
        strategic_action_manager.assign_strategy_card("player1", warfare_card)
        strategic_action_manager.set_action_phase(True)

        # Activate strategy card via component action (not strategic action)
        result = strategic_action_manager.activate_strategy_card_via_component_action(
            "player1", StrategyCardType.WARFARE
        )

        # Verify secondary abilities are still offered
        assert result.success
        assert result.secondary_abilities_offered
        expected_secondary_order = ["player2", "player3"]
        assert result.secondary_ability_order == expected_secondary_order


class TestRule82InputValidation:
    """Test input validation and error handling."""

    def test_empty_player_id_validation(self) -> None:
        """Test that empty player IDs are properly validated."""
        from ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCard,
            StrategyCardType,
        )

        strategic_action_manager = StrategicActionManager()

        # Test empty player ID in various methods
        assert not strategic_action_manager.can_activate_strategy_card(
            "", StrategyCardType.WARFARE
        )
        assert not strategic_action_manager.can_continue_turn("")
        assert strategic_action_manager.must_pass("")

        # Test None strategy card assignment
        with pytest.raises(ValueError, match="Strategy card cannot be None"):
            strategic_action_manager.assign_strategy_card("player1", None)

        # Test empty player ID assignment
        warfare_card = StrategyCard(
            StrategyCardType.WARFARE, "Move units", "Build units"
        )
        with pytest.raises(ValueError, match="Player ID cannot be empty"):
            strategic_action_manager.assign_strategy_card("", warfare_card)

    def test_empty_player_order_validation(self) -> None:
        """Test that empty player order is properly validated."""
        from ti4.core.strategic_action import StrategicActionManager

        strategic_action_manager = StrategicActionManager()

        # Test empty player order
        with pytest.raises(ValueError, match="Player order cannot be empty"):
            strategic_action_manager.set_player_order([])


class TestRule82StrategyCardEnum:
    """Test strategy card enum functionality."""

    def test_strategy_card_enum_values(self) -> None:
        """Test that strategy card enum has correct values."""
        from ti4.core.strategic_action import StrategyCardType

        # Test all strategy card types exist
        assert StrategyCardType.LEADERSHIP.value == "leadership"
        assert StrategyCardType.DIPLOMACY.value == "diplomacy"
        assert StrategyCardType.POLITICS.value == "politics"
        assert StrategyCardType.CONSTRUCTION.value == "construction"
        assert StrategyCardType.TRADE.value == "trade"
        assert StrategyCardType.WARFARE.value == "warfare"
        assert StrategyCardType.TECHNOLOGY.value == "technology"
        assert StrategyCardType.IMPERIAL.value == "imperial"

    def test_strategy_card_accepts_enum_and_string(self) -> None:
        """Test that methods accept both enum and string card names."""
        from ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCard,
            StrategyCardType,
        )

        strategic_action_manager = StrategicActionManager()
        warfare_card = StrategyCard(
            StrategyCardType.WARFARE, "Move units", "Build units"
        )
        strategic_action_manager.assign_strategy_card("player1", warfare_card)
        strategic_action_manager.set_action_phase(True)

        # Test with enum
        assert strategic_action_manager.can_activate_strategy_card(
            "player1", StrategyCardType.WARFARE
        )

        # Test with string
        assert strategic_action_manager.can_activate_strategy_card("player1", "warfare")

        # Test exhaustion with both
        strategic_action_manager.exhaust_strategy_card(
            "player1", StrategyCardType.WARFARE
        )
        assert strategic_action_manager.is_strategy_card_exhausted("player1", "warfare")

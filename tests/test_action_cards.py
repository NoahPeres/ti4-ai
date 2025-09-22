"""Tests for Action Card system implementation.

This module tests the action card system as defined in LRR Rule 1.22 and Rule 2.6.
Tests cover action card timing, resolution, component actions, and integration.

LRR References:
- Rule 1.22: Action Card Abilities
- Rule 2.6: Action Cards
- Rule 22: Component Action
"""

import pytest

from src.ti4.core.action_cards import (
    ActionCardContext,
    ActionCardManager,
    ActionCardResult,
    ActionCardTiming,
    DirectHitActionCard,
    LeadershipRiderActionCard,
    UpgradeActionCard,
)
from src.ti4.core.component_action import (
    ComponentActionContext,
    ComponentActionManager,
    ComponentActionType,
    TechnologyComponentActionProvider,
)


class TestActionCardTiming:
    """Test ActionCardTiming enum."""

    def test_timing_values(self):
        """Test that timing enum has expected values."""
        assert ActionCardTiming.COMPONENT_ACTION.value == "component_action"
        assert ActionCardTiming.COMBAT.value == "combat"
        assert ActionCardTiming.SPACE_COMBAT.value == "space_combat"
        assert ActionCardTiming.GROUND_COMBAT.value == "ground_combat"
        assert ActionCardTiming.AGENDA_PHASE.value == "agenda_phase"
        assert ActionCardTiming.STATUS_PHASE.value == "status_phase"


class TestActionCardContext:
    """Test ActionCardContext data class."""

    def test_context_creation(self):
        """Test creating action card context."""
        context = ActionCardContext(
            player_id="player1",
            game_state={"turn": 1},
            target_player="player2",
            target_system="system1",
        )

        assert context.player_id == "player1"
        assert context.game_state == {"turn": 1}
        assert context.target_player == "player2"
        assert context.target_system == "system1"
        assert context.target_units is None
        assert context.additional_data is None


class TestActionCardResult:
    """Test ActionCardResult data class."""

    def test_result_creation(self):
        """Test creating action card result."""
        result = ActionCardResult(
            success=True, effects_applied=["effect1", "effect2"], error_message=None
        )

        assert result.success is True
        assert result.effects_applied == ["effect1", "effect2"]
        assert result.error_message is None
        assert result.additional_data is None


class TestDirectHitActionCard:
    """Test DirectHit action card implementation."""

    def test_direct_hit_properties(self):
        """Test DirectHit card properties."""
        card = DirectHitActionCard()

        assert card.name == "Direct Hit"
        assert card.timing == ActionCardTiming.SPACE_COMBAT
        assert card.requires_component_action() is False
        assert "destroy" in card.description.lower()

    def test_direct_hit_can_play_valid(self):
        """Test DirectHit can be played with valid target."""
        card = DirectHitActionCard()
        context = ActionCardContext(
            player_id="player1", target_units=["destroyer", "cruiser"]
        )

        can_play, error = card.can_play(context)
        assert can_play is True
        assert error is None

    def test_direct_hit_can_play_no_targets(self):
        """Test DirectHit cannot be played without targets."""
        card = DirectHitActionCard()
        context = ActionCardContext(player_id="player1")

        can_play, error = card.can_play(context)
        assert can_play is False
        assert "no valid targets" in error.lower()

    def test_direct_hit_resolve(self):
        """Test DirectHit resolution."""
        card = DirectHitActionCard()
        context = ActionCardContext(player_id="player1", target_units=["destroyer"])

        result = card.resolve(context)
        assert result.success is True
        assert "destroyed destroyer" in result.effects_applied[0].lower()


class TestLeadershipRiderActionCard:
    """Test Leadership Rider action card implementation."""

    def test_leadership_rider_properties(self):
        """Test Leadership Rider card properties."""
        card = LeadershipRiderActionCard()

        assert card.name == "Leadership Rider"
        assert card.timing == ActionCardTiming.COMPONENT_ACTION
        assert card.requires_component_action() is True
        assert "command tokens" in card.description.lower()

    def test_leadership_rider_can_play(self):
        """Test Leadership Rider can be played."""
        card = LeadershipRiderActionCard()
        context = ActionCardContext(player_id="player1")

        can_play, error = card.can_play(context)
        assert can_play is True
        assert error is None

    def test_leadership_rider_resolve(self):
        """Test Leadership Rider resolution."""
        card = LeadershipRiderActionCard()
        context = ActionCardContext(player_id="player1")

        result = card.resolve(context)
        assert result.success is True
        assert "gained 3 command tokens" in result.effects_applied[0].lower()


class TestUpgradeActionCard:
    """Test Upgrade action card implementation."""

    def test_upgrade_properties(self):
        """Test Upgrade card properties."""
        card = UpgradeActionCard()

        assert card.name == "Upgrade"
        assert card.timing == ActionCardTiming.COMPONENT_ACTION
        assert card.requires_component_action() is True
        assert "replace" in card.description.lower()

    def test_upgrade_can_play_valid(self):
        """Test Upgrade can be played with valid units."""
        card = UpgradeActionCard()
        context = ActionCardContext(
            player_id="player1", target_units=["cruiser", "fighter"]
        )

        can_play, error = card.can_play(context)
        assert can_play is True
        assert error is None

    def test_upgrade_can_play_no_units(self):
        """Test Upgrade cannot be played without units."""
        card = UpgradeActionCard()
        context = ActionCardContext(player_id="player1")

        can_play, error = card.can_play(context)
        assert can_play is False
        assert "no units to upgrade" in error.lower()

    def test_upgrade_resolve(self):
        """Test Upgrade card resolution."""
        card = UpgradeActionCard()
        context = ActionCardContext(player_id="player1", target_units=["cruiser"])

        result = card.resolve(context)
        assert result.success is True
        assert "cruiser" in result.effects_applied[0]
        assert "dreadnought" in result.effects_applied[0]


class TestActionCardManager:
    """Test ActionCardManager functionality."""

    def test_manager_creation(self):
        """Test creating action card manager."""
        manager = ActionCardManager()
        assert manager is not None

    def test_can_play_card_valid(self):
        """Test manager can validate playable cards."""
        manager = ActionCardManager()
        card = DirectHitActionCard()
        context = ActionCardContext(player_id="player1", target_units=["destroyer"])

        can_play, error = manager.can_play_card(card, context)
        assert can_play is True
        assert error is None

    def test_can_play_card_invalid(self):
        """Test manager rejects invalid cards."""
        manager = ActionCardManager()
        card = DirectHitActionCard()
        context = ActionCardContext(player_id="player1")  # No targets

        can_play, error = manager.can_play_card(card, context)
        assert can_play is False
        assert error is not None

    def test_play_card_success(self):
        """Test successful card play."""
        manager = ActionCardManager()
        card = LeadershipRiderActionCard()
        context = ActionCardContext(player_id="player1")

        result = manager.play_card(card, context)
        assert result.success is True
        assert result.effects_applied is not None
        assert len(result.effects_applied) > 0

    def test_play_card_failure(self):
        """Test failed card play."""
        manager = ActionCardManager()
        card = DirectHitActionCard()
        context = ActionCardContext(player_id="player1")  # No targets

        result = manager.play_card(card, context)
        assert result.success is False
        assert result.error_message is not None

    def test_cancel_card(self):
        """Test card cancellation."""
        manager = ActionCardManager()

        # Should not raise exception
        manager.cancel_card("some_card_id")


class TestComponentActionManager:
    """Test ComponentActionManager functionality."""

    def test_manager_creation(self):
        """Test creating component action manager."""
        manager = ComponentActionManager()
        assert manager is not None

    def test_set_action_phase_active(self):
        """Test setting action phase state."""
        manager = ComponentActionManager()
        manager.set_action_phase_active(True)
        # No direct way to test, but should not raise exception

    def test_set_current_player(self):
        """Test setting current player."""
        manager = ComponentActionManager()
        manager.set_current_player("player1")
        # No direct way to test, but should not raise exception

    def test_register_component_provider(self):
        """Test registering component provider."""
        manager = ComponentActionManager()
        provider = TechnologyComponentActionProvider("Test Tech", "Test description")

        manager.register_component_provider("test_tech", provider)
        # Should not raise exception

    def test_can_perform_component_action_not_action_phase(self):
        """Test component action validation when not in action phase."""
        manager = ComponentActionManager()
        manager.set_action_phase_active(False)

        can_perform, error = manager.can_perform_component_action(
            "player1", ComponentActionType.ACTION_CARD, "test_card"
        )

        assert can_perform is False
        assert "action phase" in error.lower()

    def test_can_perform_component_action_wrong_player(self):
        """Test component action validation for wrong player."""
        manager = ComponentActionManager()
        manager.set_action_phase_active(True)
        manager.set_current_player("player1")

        can_perform, error = manager.can_perform_component_action(
            "player2", ComponentActionType.ACTION_CARD, "test_card"
        )

        assert can_perform is False
        assert "not player2's turn" in error.lower()

    def test_can_perform_action_card_component_action(self):
        """Test action card component action validation."""
        manager = ComponentActionManager()
        manager.set_action_phase_active(True)
        manager.set_current_player("player1")

        card = LeadershipRiderActionCard()

        can_perform, error = manager.can_perform_component_action(
            "player1",
            ComponentActionType.ACTION_CARD,
            "leadership_rider",
            action_card=card,
        )

        assert can_perform is True
        assert error is None

    def test_perform_action_card_component_action(self):
        """Test performing action card component action."""
        manager = ComponentActionManager()
        manager.set_action_phase_active(True)
        manager.set_current_player("player1")

        card = LeadershipRiderActionCard()

        result = manager.perform_component_action(
            "player1",
            ComponentActionType.ACTION_CARD,
            "leadership_rider",
            action_card=card,
        )

        assert result.success is True
        assert result.action_consumed is True
        assert result.effects_applied is not None

    def test_perform_component_action_invalid(self):
        """Test performing invalid component action."""
        manager = ComponentActionManager()
        manager.set_action_phase_active(False)  # Not in action phase

        result = manager.perform_component_action(
            "player1", ComponentActionType.ACTION_CARD, "test_card"
        )

        assert result.success is False
        assert result.action_consumed is False
        assert result.error_message is not None

    def test_cancel_component_action(self):
        """Test canceling component action."""
        manager = ComponentActionManager()

        # Should not raise exception
        manager.cancel_component_action(
            "player1", ComponentActionType.ACTION_CARD, "test_card"
        )

    def test_get_available_component_actions_not_active(self):
        """Test getting available actions when not in action phase."""
        manager = ComponentActionManager()
        manager.set_action_phase_active(False)

        actions = manager.get_available_component_actions("player1")
        assert actions == []

    def test_get_available_component_actions_wrong_player(self):
        """Test getting available actions for wrong player."""
        manager = ComponentActionManager()
        manager.set_action_phase_active(True)
        manager.set_current_player("player1")

        actions = manager.get_available_component_actions("player2")
        assert actions == []

    def test_get_available_component_actions_with_provider(self):
        """Test getting available actions with registered provider."""
        manager = ComponentActionManager()
        manager.set_action_phase_active(True)
        manager.set_current_player("player1")

        provider = TechnologyComponentActionProvider("Test Tech", "Test description")
        manager.register_component_provider("test_tech", provider)

        actions = manager.get_available_component_actions("player1")
        assert len(actions) == 1
        assert actions[0]["component_id"] == "test_tech"
        assert actions[0]["type"] == "component"


class TestTechnologyComponentActionProvider:
    """Test TechnologyComponentActionProvider example."""

    def test_provider_creation(self):
        """Test creating technology provider."""
        provider = TechnologyComponentActionProvider("Test Tech", "Test description")

        assert provider.tech_name == "Test Tech"
        assert provider.description == "Test description"
        assert provider.requirements == {}

    def test_can_perform_component_action(self):
        """Test technology provider validation."""
        provider = TechnologyComponentActionProvider("Test Tech", "Test description")
        context = ComponentActionContext(
            player_id="player1",
            action_type=ComponentActionType.TECHNOLOGY,
            component_id="test_tech",
        )

        can_perform = provider.can_perform_component_action(context)
        assert can_perform is True

    def test_perform_component_action(self):
        """Test technology provider action."""
        provider = TechnologyComponentActionProvider("Test Tech", "Test description")
        context = ComponentActionContext(
            player_id="player1",
            action_type=ComponentActionType.TECHNOLOGY,
            component_id="test_tech",
        )

        result = provider.perform_component_action(context)
        assert result.success is True
        assert "Used Test Tech technology" in result.effects_applied[0]
        assert result.additional_data["technology_used"] == "Test Tech"

    def test_get_component_action_description(self):
        """Test technology provider description."""
        provider = TechnologyComponentActionProvider("Test Tech", "Test description")

        description = provider.get_component_action_description()
        assert "Test Tech: Test description" == description


class TestActionCardIntegration:
    """Test integration between action cards and component actions."""

    def test_action_card_component_action_integration(self):
        """Test full integration of action card with component action system."""
        # Setup managers
        component_manager = ComponentActionManager()
        component_manager.set_action_phase_active(True)
        component_manager.set_current_player("player1")

        # Create action card
        card = LeadershipRiderActionCard()

        # Test validation
        can_perform, error = component_manager.can_perform_component_action(
            "player1",
            ComponentActionType.ACTION_CARD,
            "leadership_rider",
            action_card=card,
        )

        assert can_perform is True
        assert error is None

        # Test execution
        result = component_manager.perform_component_action(
            "player1",
            ComponentActionType.ACTION_CARD,
            "leadership_rider",
            action_card=card,
        )

        assert result.success is True
        assert result.action_consumed is True
        assert len(result.effects_applied) > 0

    def test_non_component_action_card_integration(self):
        """Test action card that doesn't require component action."""
        component_manager = ComponentActionManager()
        component_manager.set_action_phase_active(True)
        component_manager.set_current_player("player1")

        # Direct Hit doesn't require component action
        card = DirectHitActionCard()

        # Should fail validation for component action
        can_perform, error = component_manager.can_perform_component_action(
            "player1", ComponentActionType.ACTION_CARD, "direct_hit", action_card=card
        )

        assert can_perform is False
        assert "does not require component action" in error.lower()


if __name__ == "__main__":
    pytest.main([__file__])

"""Tests for leader-specific exception classes.

This module tests the comprehensive exception hierarchy for leader-related errors,
including state errors, unlock errors, and ability errors with context information.

LRR References:
- Rule 51: LEADERS
- Requirements 8.4, 9.5
"""

import pytest

from src.ti4.core.constants import Faction
from src.ti4.core.leaders import (
    Agent,
    Commander,
    Hero,
    LeaderAbilityError,
    LeaderError,
    LeaderNotFoundError,
    LeaderStateError,
    LeaderUnlockError,
)


class TestLeaderErrorHierarchy:
    """Test the leader exception hierarchy and inheritance."""

    def test_leader_error_is_base_exception(self) -> None:
        """Test that LeaderError is the base exception for all leader errors."""
        error = LeaderError("Test error")
        assert isinstance(error, Exception)
        assert str(error) == "Test error"

    def test_all_leader_exceptions_inherit_from_leader_error(self) -> None:
        """Test that all specific leader exceptions inherit from LeaderError."""
        assert issubclass(LeaderNotFoundError, LeaderError)
        assert issubclass(LeaderStateError, LeaderError)
        assert issubclass(LeaderUnlockError, LeaderError)
        assert issubclass(LeaderAbilityError, LeaderError)

    def test_leader_error_with_context_information(self) -> None:
        """Test that LeaderError can include context information."""
        context = {"player_id": "player1", "leader_type": "agent"}
        error = LeaderError("Test error", context=context)

        assert str(error) == "Test error"
        assert error.context == context
        assert error.get_context_value("player_id") == "player1"
        assert error.get_context_value("leader_type") == "agent"
        assert error.get_context_value("nonexistent") is None


class TestLeaderNotFoundError:
    """Test LeaderNotFoundError with detailed context."""

    def test_leader_not_found_error_basic(self) -> None:
        """Test basic LeaderNotFoundError functionality."""
        error = LeaderNotFoundError("Leader not found")
        assert isinstance(error, LeaderError)
        assert str(error) == "Leader not found"

    def test_leader_not_found_error_with_player_context(self) -> None:
        """Test LeaderNotFoundError with player context information."""
        error = LeaderNotFoundError.for_player("player1")

        assert "Player player1 not found" in str(error)
        assert error.get_context_value("player_id") == "player1"
        assert error.get_context_value("error_type") == "player_not_found"

    def test_leader_not_found_error_with_leader_name_context(self) -> None:
        """Test LeaderNotFoundError with leader name context."""
        error = LeaderNotFoundError.for_leader_name("Test Agent", "player1")

        assert "Leader 'Test Agent' not found for player player1" in str(error)
        assert error.get_context_value("leader_name") == "Test Agent"
        assert error.get_context_value("player_id") == "player1"
        assert error.get_context_value("error_type") == "leader_not_found"

    def test_leader_not_found_error_with_leader_type_context(self) -> None:
        """Test LeaderNotFoundError with leader type context."""
        from src.ti4.core.leaders import LeaderType

        error = LeaderNotFoundError.for_leader_type(LeaderType.AGENT, "player1")

        assert "Agent leader not found for player player1" in str(error)
        assert error.get_context_value("leader_type") == LeaderType.AGENT
        assert error.get_context_value("player_id") == "player1"
        assert error.get_context_value("error_type") == "leader_type_not_found"


class TestLeaderStateError:
    """Test LeaderStateError with state transition context."""

    def test_leader_state_error_basic(self) -> None:
        """Test basic LeaderStateError functionality."""
        error = LeaderStateError("Invalid state")
        assert isinstance(error, LeaderError)
        assert str(error) == "Invalid state"

    def test_leader_state_error_for_invalid_transition(self) -> None:
        """Test LeaderStateError for invalid state transitions."""
        agent = Agent(Faction.ARBOREC, "player1")

        error = LeaderStateError.for_invalid_transition(
            agent, "exhaust", "already_exhausted"
        )

        assert "Cannot exhaust" in str(error)
        assert "already in already_exhausted state" in str(error)
        assert error.get_context_value("leader_name") == agent.get_name()
        assert error.get_context_value("current_state") == "already_exhausted"
        assert error.get_context_value("attempted_action") == "exhaust"

    def test_leader_state_error_for_ability_use_when_invalid_state(self) -> None:
        """Test LeaderStateError when trying to use ability in invalid state."""
        hero = Hero(Faction.ARBOREC, "player1")
        hero.purge()  # Purge the hero

        error = LeaderStateError.for_ability_use_invalid_state(hero)

        assert "cannot use ability" in str(error).lower()
        assert "purged" in str(error).lower()
        assert error.get_context_value("leader_name") == hero.get_name()
        assert error.get_context_value("leader_type") == hero.get_leader_type()
        assert error.get_context_value("current_lock_status") == hero.lock_status

    def test_leader_state_error_for_unlock_when_already_unlocked(self) -> None:
        """Test LeaderStateError when trying to unlock already unlocked leader."""
        commander = Commander(Faction.ARBOREC, "player1")
        commander.unlock()  # Unlock the commander

        error = LeaderStateError.for_already_unlocked(commander)

        assert "already unlocked" in str(error).lower()
        assert error.get_context_value("leader_name") == commander.get_name()
        assert error.get_context_value("current_lock_status") == commander.lock_status


class TestLeaderUnlockError:
    """Test LeaderUnlockError with unlock condition context."""

    def test_leader_unlock_error_basic(self) -> None:
        """Test basic LeaderUnlockError functionality."""
        error = LeaderUnlockError("Cannot unlock")
        assert isinstance(error, LeaderError)
        assert str(error) == "Cannot unlock"

    def test_leader_unlock_error_for_unmet_conditions(self) -> None:
        """Test LeaderUnlockError when unlock conditions are not met."""
        commander = Commander(Faction.ARBOREC, "player1")
        conditions = ["Control 3 planets", "Have 2 technology cards"]

        error = LeaderUnlockError.for_unmet_conditions(commander, conditions)

        assert "unlock conditions not met" in str(error).lower()
        assert "Control 3 planets" in str(error)
        assert "Have 2 technology cards" in str(error)
        assert error.get_context_value("leader_name") == commander.get_name()
        assert error.get_context_value("unmet_conditions") == conditions

    def test_leader_unlock_error_for_purged_hero(self) -> None:
        """Test LeaderUnlockError when trying to unlock a purged hero."""
        hero = Hero(Faction.ARBOREC, "player1")
        hero.purge()

        error = LeaderUnlockError.for_purged_hero(hero)

        assert "cannot unlock purged hero" in str(error).lower()
        assert error.get_context_value("leader_name") == hero.get_name()
        assert error.get_context_value("current_lock_status") == hero.lock_status

    def test_leader_unlock_error_for_invalid_game_state(self) -> None:
        """Test LeaderUnlockError when game state prevents unlocking."""
        commander = Commander(Faction.ARBOREC, "player1")

        error = LeaderUnlockError.for_invalid_game_state(
            commander, "Game not in action phase"
        )

        assert "cannot unlock" in str(error).lower()
        assert "due to game state" in str(error).lower()
        assert "Game not in action phase" in str(error)
        assert error.get_context_value("leader_name") == commander.get_name()
        assert error.get_context_value("game_state_issue") == "Game not in action phase"


class TestLeaderAbilityError:
    """Test LeaderAbilityError with ability execution context."""

    def test_leader_ability_error_basic(self) -> None:
        """Test basic LeaderAbilityError functionality."""
        error = LeaderAbilityError("Ability failed")
        assert isinstance(error, LeaderError)
        assert str(error) == "Ability failed"

    def test_leader_ability_error_for_invalid_target(self) -> None:
        """Test LeaderAbilityError when ability target is invalid."""
        agent = Agent(Faction.ARBOREC, "player1")

        error = LeaderAbilityError.for_invalid_target(
            agent, "invalid_system", "System does not exist"
        )

        assert "invalid target" in str(error).lower()
        assert "invalid_system" in str(error)
        assert "System does not exist" in str(error)
        assert error.get_context_value("leader_name") == agent.get_name()
        assert error.get_context_value("invalid_target") == "invalid_system"
        assert error.get_context_value("target_error") == "System does not exist"

    def test_leader_ability_error_for_insufficient_resources(self) -> None:
        """Test LeaderAbilityError when resources are insufficient."""
        commander = Commander(Faction.ARBOREC, "player1")

        error = LeaderAbilityError.for_insufficient_resources(
            commander, {"trade_goods": 2}, {"trade_goods": 5}
        )

        assert "insufficient resources" in str(error).lower()
        assert "trade_goods" in str(error)
        assert error.get_context_value("leader_name") == commander.get_name()
        assert error.get_context_value("available_resources") == {"trade_goods": 2}
        assert error.get_context_value("required_resources") == {"trade_goods": 5}

    def test_leader_ability_error_for_timing_violation(self) -> None:
        """Test LeaderAbilityError when ability is used at wrong time."""
        hero = Hero(Faction.ARBOREC, "player1")

        error = LeaderAbilityError.for_timing_violation(
            hero, "status_phase", "action_phase"
        )

        assert "timing violation" in str(error).lower()
        assert "status_phase" in str(error)
        assert "action_phase" in str(error)
        assert error.get_context_value("leader_name") == hero.get_name()
        assert error.get_context_value("current_phase") == "status_phase"
        assert error.get_context_value("required_phase") == "action_phase"

    def test_leader_ability_error_for_execution_failure(self) -> None:
        """Test LeaderAbilityError when ability execution fails internally."""
        agent = Agent(Faction.ARBOREC, "player1")

        error = LeaderAbilityError.for_execution_failure(
            agent, "Division by zero in calculation"
        )

        assert "ability execution failed" in str(error).lower()
        assert "Division by zero in calculation" in str(error)
        assert error.get_context_value("leader_name") == agent.get_name()
        assert (
            error.get_context_value("execution_error")
            == "Division by zero in calculation"
        )


class TestLeaderErrorContextMethods:
    """Test context methods and error message formatting."""

    def test_error_context_serialization(self) -> None:
        """Test that error context can be serialized for logging."""
        context = {
            "player_id": "player1",
            "leader_type": "agent",
            "timestamp": "2024-01-01T00:00:00Z",
        }
        error = LeaderError("Test error", context=context)

        serialized = error.serialize_context()
        assert isinstance(serialized, dict)
        assert serialized["player_id"] == "player1"
        assert serialized["leader_type"] == "agent"
        assert serialized["timestamp"] == "2024-01-01T00:00:00Z"

    def test_error_context_filtering(self) -> None:
        """Test that error context can be filtered for sensitive information."""
        context = {
            "player_id": "player1",
            "secret_key": "sensitive_data",
            "leader_name": "Test Agent",
        }
        error = LeaderError("Test error", context=context)

        filtered = error.get_filtered_context(exclude_keys=["secret_key"])
        assert "player_id" in filtered
        assert "leader_name" in filtered
        assert "secret_key" not in filtered

    def test_error_message_with_context_formatting(self) -> None:
        """Test that error messages can include formatted context."""
        agent = Agent(Faction.ARBOREC, "player1")
        agent.exhaust()  # Exhaust the agent first to get the expected error
        error = LeaderStateError.for_ability_use_invalid_state(agent)

        formatted_message = error.get_formatted_message()
        assert agent.get_name() in formatted_message
        assert "exhausted" in formatted_message.lower()
        assert "Leader: Agent" in formatted_message


class TestLeaderErrorIntegration:
    """Test leader error integration with actual leader operations."""

    def test_agent_exhaust_when_already_exhausted_raises_state_error(self) -> None:
        """Test that exhausting an already exhausted agent raises LeaderStateError."""
        agent = Agent(Faction.ARBOREC, "player1")
        agent.exhaust()  # First exhaust should work

        # Second exhaust should raise LeaderStateError
        with pytest.raises(LeaderStateError) as exc_info:
            agent.exhaust()

        error = exc_info.value
        assert "already in already_exhausted state" in str(error).lower()
        assert error.get_context_value("leader_name") == agent.get_name()

    def test_hero_unlock_when_purged_raises_unlock_error(self) -> None:
        """Test that unlocking a purged hero raises LeaderUnlockError."""
        hero = Hero(Faction.ARBOREC, "player1")
        hero.purge()  # Purge the hero first

        # Trying to unlock should raise LeaderUnlockError
        with pytest.raises(LeaderUnlockError) as exc_info:
            hero.unlock()

        error = exc_info.value
        assert "purged" in str(error).lower()
        assert error.get_context_value("leader_name") == hero.get_name()

    def test_commander_ability_when_locked_raises_state_error(self) -> None:
        """Test that using commander ability when locked raises LeaderStateError."""
        commander = Commander(Faction.ARBOREC, "player1")

        # Commander starts locked, so ability use should fail
        # This will be implemented when we enhance the execute_ability method
        # For now, we test the can_use_ability method
        assert not commander.can_use_ability()

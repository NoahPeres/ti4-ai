"""Tests for Commander class implementation.

This module tests the Commander class with unlock mechanics:
- Commander class extending BaseLeader
- unlock() method and unlock condition checking
- can_use_ability() validation for unlocked state
- Commander unlock mechanics

LRR References:
- Rule 51: LEADERS
- Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6
"""

import pytest

from src.ti4.core.constants import Faction
from src.ti4.core.leaders import LeaderLockStatus, LeaderType


def test_commander_class_exists():
    """Test that Commander class exists and can be instantiated.

    Requirements: 3.1 - Commander class extending BaseLeader
    """
    from src.ti4.core.leaders import Commander

    commander = Commander(faction=Faction.SOL, player_id="test_player")
    assert commander is not None


def test_commander_has_correct_leader_type():
    """Test that Commander returns correct leader type.

    Requirements: 3.1 - Commander class extending BaseLeader
    """
    from src.ti4.core.leaders import Commander

    commander = Commander(faction=Faction.SOL, player_id="test_player")
    assert commander.get_leader_type() == LeaderType.COMMANDER


def test_commander_starts_locked():
    """Test that Commander starts in locked state.

    Requirements: 3.1 - Commanders start locked
    """
    from src.ti4.core.leaders import Commander

    commander = Commander(faction=Faction.SOL, player_id="test_player")
    assert commander.lock_status == LeaderLockStatus.LOCKED


def test_commander_has_no_ready_status():
    """Test that Commander has no ready/exhaust status.

    Requirements: 3.5 - Commanders don't have ready/exhaust mechanics
    """
    from src.ti4.core.leaders import Commander

    commander = Commander(faction=Faction.SOL, player_id="test_player")
    assert commander.ready_status is None


def test_commander_cannot_use_ability_when_locked():
    """Test that Commander cannot use ability when locked.

    Requirements: 3.6 - Commander abilities rejected when locked
    """
    from src.ti4.core.leaders import Commander

    commander = Commander(faction=Faction.SOL, player_id="test_player")
    assert commander.can_use_ability() is False


def test_commander_unlock_method():
    """Test that Commander unlock() method changes state to unlocked.

    Requirements: 3.2 - Commander becomes unlocked when conditions are met
    """
    from src.ti4.core.leaders import Commander

    commander = Commander(faction=Faction.SOL, player_id="test_player")
    commander.unlock()
    assert commander.lock_status == LeaderLockStatus.UNLOCKED


def test_commander_can_use_ability_when_unlocked():
    """Test that Commander can use ability when unlocked.

    Requirements: 3.3 - Commander abilities available when unlocked
    """
    from src.ti4.core.leaders import Commander

    commander = Commander(faction=Faction.SOL, player_id="test_player")
    commander.unlock()
    assert commander.can_use_ability() is True


def test_commander_remains_unlocked():
    """Test that Commander remains unlocked after unlock.

    Requirements: 3.4 - Commander remains unlocked for rest of game
    """
    from src.ti4.core.leaders import Commander

    commander = Commander(faction=Faction.SOL, player_id="test_player")
    commander.unlock()

    # Verify it stays unlocked
    assert commander.lock_status == LeaderLockStatus.UNLOCKED
    assert commander.can_use_ability() is True


def test_commander_unlock_when_already_unlocked():
    """Test that unlocking an already unlocked commander is safe.

    Requirements: 3.2 - Robust state management
    """
    from src.ti4.core.leaders import Commander

    commander = Commander(faction=Faction.SOL, player_id="test_player")
    commander.unlock()

    # Should not raise error when unlocking already unlocked commander
    commander.unlock()
    assert commander.lock_status == LeaderLockStatus.UNLOCKED


def test_commander_unlock_conditions_placeholder():
    """Test that Commander has unlock conditions (placeholder implementation).

    Requirements: 3.2 - Commander has unlock conditions
    """
    from src.ti4.core.leaders import Commander

    commander = Commander(faction=Faction.SOL, player_id="test_player")
    conditions = commander.get_unlock_conditions()

    # Should return a list (even if placeholder)
    assert isinstance(conditions, list)


def test_commander_check_unlock_conditions_placeholder():
    """Test that Commander can check unlock conditions (placeholder implementation).

    Requirements: 3.2 - Commander can check unlock conditions
    """
    from src.ti4.core.leaders import Commander

    commander = Commander(faction=Faction.SOL, player_id="test_player")

    # Mock game state for testing
    class MockGameState:
        pass

    game_state = MockGameState()
    result = commander.check_unlock_conditions(game_state)

    # Should return a boolean (even if placeholder)
    assert isinstance(result, bool)


def test_commander_execute_ability_placeholder():
    """Test that Commander can execute abilities (placeholder implementation).

    Requirements: 3.3 - Commander abilities available when unlocked
    """
    from src.ti4.core.leaders import Commander

    commander = Commander(faction=Faction.SOL, player_id="test_player")
    commander.unlock()

    # Mock game state for testing
    class MockGameState:
        pass

    game_state = MockGameState()
    result = commander.execute_ability(game_state)

    # Should return LeaderAbilityResult
    assert result.success is True
    assert isinstance(result.effects, list)


def test_commander_no_exhaustion_after_ability():
    """Test that Commander does not become exhausted after using ability.

    Requirements: 3.5 - Commander abilities don't cause exhaustion
    """
    from src.ti4.core.leaders import Commander

    commander = Commander(faction=Faction.SOL, player_id="test_player")
    commander.unlock()

    # Mock game state for testing
    class MockGameState:
        pass

    game_state = MockGameState()

    # Use ability multiple times
    commander.execute_ability(game_state)
    commander.execute_ability(game_state)

    # Should still be able to use ability (no exhaustion)
    assert commander.can_use_ability() is True
    assert commander.ready_status is None  # No ready/exhaust status


def test_commander_input_validation():
    """Test that Commander constructor validates inputs properly.

    Requirements: 3.1 - Robust error handling
    """
    from src.ti4.core.leaders import Commander

    # Test empty player_id validation
    with pytest.raises(ValueError, match="player_id cannot be empty or None"):
        Commander(faction=Faction.SOL, player_id="")

    # Test invalid faction type
    with pytest.raises(TypeError, match="faction must be a Faction enum value"):
        Commander(faction="invalid_faction", player_id="test_player")

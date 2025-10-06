"""Tests for Hero class implementation.

This module tests the Hero class with unlock and purge mechanics:
- Hero class extending BaseLeader
- unlock() and purge() methods for hero lifecycle
- can_use_ability() validation for unlocked but not purged state
- Hero unlock and purge mechanics

LRR References:
- Rule 51: LEADERS
- Requirements 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7
"""

import pytest

from src.ti4.core.constants import Faction
from src.ti4.core.leaders import LeaderLockStatus, LeaderType, LeaderUnlockError


def test_hero_class_exists():
    """Test that Hero class exists and can be instantiated.

    Requirements: 4.1 - Hero class extending BaseLeader
    """
    from src.ti4.core.leaders import Hero

    hero = Hero(faction=Faction.SOL, player_id="test_player")
    assert hero is not None


def test_hero_has_correct_leader_type():
    """Test that Hero returns correct leader type.

    Requirements: 4.1 - Hero class extending BaseLeader
    """
    from src.ti4.core.leaders import Hero

    hero = Hero(faction=Faction.SOL, player_id="test_player")
    assert hero.get_leader_type() == LeaderType.HERO


def test_hero_starts_locked():
    """Test that Hero starts in locked state.

    Requirements: 4.1 - Heroes start locked
    """
    from src.ti4.core.leaders import Hero

    hero = Hero(faction=Faction.SOL, player_id="test_player")
    assert hero.lock_status == LeaderLockStatus.LOCKED


def test_hero_has_no_ready_status():
    """Test that Hero has no ready/exhaust status.

    Requirements: 4.5 - Heroes don't have ready/exhaust mechanics
    """
    from src.ti4.core.leaders import Hero

    hero = Hero(faction=Faction.SOL, player_id="test_player")
    assert hero.ready_status is None


def test_hero_cannot_use_ability_when_locked():
    """Test that Hero cannot use ability when locked.

    Requirements: 4.6 - Hero abilities rejected when locked
    """
    from src.ti4.core.leaders import Hero

    hero = Hero(faction=Faction.SOL, player_id="test_player")
    assert hero.can_use_ability() is False


def test_hero_unlock_method():
    """Test that Hero unlock() method changes state to unlocked.

    Requirements: 4.2 - Hero becomes unlocked when conditions are met
    """
    from src.ti4.core.leaders import Hero

    hero = Hero(faction=Faction.SOL, player_id="test_player")
    hero.unlock()
    assert hero.lock_status == LeaderLockStatus.UNLOCKED


def test_hero_can_use_ability_when_unlocked():
    """Test that Hero can use ability when unlocked but not purged.

    Requirements: 4.2 - Hero abilities available when unlocked
    """
    from src.ti4.core.leaders import Hero

    hero = Hero(faction=Faction.SOL, player_id="test_player")
    hero.unlock()
    assert hero.can_use_ability() is True


def test_hero_purge_method():
    """Test that Hero purge() method changes state to purged.

    Requirements: 4.3 - Hero is purged after ability use
    """
    from src.ti4.core.leaders import Hero

    hero = Hero(faction=Faction.SOL, player_id="test_player")
    hero.unlock()
    hero.purge()
    assert hero.lock_status == LeaderLockStatus.PURGED


def test_hero_cannot_use_ability_when_purged():
    """Test that Hero cannot use ability when purged.

    Requirements: 4.4, 4.7 - Hero abilities permanently unavailable after purging
    """
    from src.ti4.core.leaders import Hero

    hero = Hero(faction=Faction.SOL, player_id="test_player")
    hero.unlock()
    hero.purge()
    assert hero.can_use_ability() is False


def test_hero_unlock_purge_lifecycle():
    """Test complete hero lifecycle: locked -> unlocked -> purged.

    Requirements: 4.1, 4.2, 4.3, 4.4 - Complete hero lifecycle
    """
    from src.ti4.core.leaders import Hero

    hero = Hero(faction=Faction.SOL, player_id="test_player")

    # Start locked
    assert hero.lock_status == LeaderLockStatus.LOCKED
    assert hero.can_use_ability() is False

    # Unlock
    hero.unlock()
    assert hero.lock_status == LeaderLockStatus.UNLOCKED
    assert hero.can_use_ability() is True

    # Purge
    hero.purge()
    assert hero.lock_status == LeaderLockStatus.PURGED
    assert hero.can_use_ability() is False


def test_hero_unlock_when_already_unlocked():
    """Test that unlocking an already unlocked hero is safe.

    Requirements: 4.2 - Robust state management
    """
    from src.ti4.core.leaders import Hero

    hero = Hero(faction=Faction.SOL, player_id="test_player")
    hero.unlock()

    # Should not raise error when unlocking already unlocked hero
    hero.unlock()
    assert hero.lock_status == LeaderLockStatus.UNLOCKED


def test_hero_purge_when_locked():
    """Test that purging a locked hero changes state to purged.

    Requirements: 4.3 - Purge method should work regardless of current state
    """
    from src.ti4.core.leaders import Hero

    hero = Hero(faction=Faction.SOL, player_id="test_player")
    hero.purge()
    assert hero.lock_status == LeaderLockStatus.PURGED


def test_hero_purge_when_already_purged():
    """Test that purging an already purged hero is safe.

    Requirements: 4.3 - Robust state management
    """
    from src.ti4.core.leaders import Hero

    hero = Hero(faction=Faction.SOL, player_id="test_player")
    hero.purge()

    # Should not raise error when purging already purged hero
    hero.purge()
    assert hero.lock_status == LeaderLockStatus.PURGED


def test_hero_unlock_conditions_placeholder():
    """Test that Hero has unlock conditions (placeholder implementation).

    Requirements: 4.2 - Hero has unlock conditions
    """
    from src.ti4.core.leaders import Hero

    hero = Hero(faction=Faction.SOL, player_id="test_player")
    conditions = hero.get_unlock_conditions()

    # Should return a list (even if placeholder)
    assert isinstance(conditions, list)


def test_hero_check_unlock_conditions_placeholder():
    """Test that Hero can check unlock conditions (placeholder implementation).

    Requirements: 4.2 - Hero can check unlock conditions
    """
    from src.ti4.core.leaders import Hero

    hero = Hero(faction=Faction.SOL, player_id="test_player")

    # Mock game state for testing
    class MockGameState:
        pass

    game_state = MockGameState()
    result = hero.check_unlock_conditions(game_state)

    # Should return a boolean (even if placeholder)
    assert isinstance(result, bool)


def test_hero_execute_ability_placeholder():
    """Test that Hero can execute abilities (placeholder implementation).

    Requirements: 4.2 - Hero abilities available when unlocked
    """
    from src.ti4.core.leaders import Hero

    hero = Hero(faction=Faction.SOL, player_id="test_player")
    hero.unlock()

    # Mock game state for testing
    class MockGameState:
        pass

    game_state = MockGameState()
    result = hero.execute_ability(game_state)

    # Should return LeaderAbilityResult
    assert result.success is True
    assert isinstance(result.effects, list)


def test_hero_no_exhaustion_mechanics():
    """Test that Hero does not have exhaustion mechanics.

    Requirements: 4.5 - Heroes don't have ready/exhaust mechanics
    """
    from src.ti4.core.leaders import Hero

    hero = Hero(faction=Faction.SOL, player_id="test_player")

    # Hero should not have exhaust/ready methods
    assert not hasattr(hero, "exhaust")
    assert not hasattr(hero, "ready")
    assert hero.ready_status is None


def test_hero_unlock_when_purged_raises_error():
    """Test that unlocking a purged hero raises an error.

    Requirements: 4.3, 4.4 - Heroes cannot be unlocked after purging
    """
    from src.ti4.core.leaders import Hero

    hero = Hero(faction=Faction.SOL, player_id="test_player")
    hero.purge()

    with pytest.raises(
        LeaderUnlockError,
        match="Cannot unlock purged hero Hero - heroes that have been purged cannot be unlocked again",
    ):
        hero.unlock()


def test_hero_input_validation():
    """Test that Hero constructor validates inputs properly.

    Requirements: 4.1 - Robust error handling
    """
    from src.ti4.core.leaders import Hero

    # Test empty player_id validation
    with pytest.raises(ValueError, match="player_id cannot be empty or None"):
        Hero(faction=Faction.SOL, player_id="")

    # Test invalid faction type
    with pytest.raises(TypeError, match="faction must be a Faction enum value"):
        Hero(faction="invalid_faction", player_id="test_player")

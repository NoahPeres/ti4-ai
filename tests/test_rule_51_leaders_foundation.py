"""Tests for Rule 51: LEADERS - Core Foundation.

This module tests the foundational components of the leader system:
- Leader enums and data structures
- BaseLeader abstract class
- LeaderAbilityResult for standardized outcomes

LRR References:
- Rule 51: LEADERS
- Requirements 1.1, 1.2, 1.3, 8.1, 8.2, 8.3
"""

import pytest

from src.ti4.core.constants import Faction


def test_leader_type_enum_exists():
    """Test that LeaderType enum exists with correct values.

    Requirements: 1.1, 1.2
    """
    from src.ti4.core.leaders import LeaderType

    # Test enum values match TI4 leader types
    assert LeaderType.AGENT.value == "agent"
    assert LeaderType.COMMANDER.value == "commander"
    assert LeaderType.HERO.value == "hero"

    # Test all three types are present
    assert len(LeaderType) == 3


def test_leader_lock_status_enum_exists():
    """Test that LeaderLockStatus enum exists with correct values.

    Requirements: 8.1, 8.2
    """
    from src.ti4.core.leaders import LeaderLockStatus

    # Test enum values for leader state management
    assert LeaderLockStatus.LOCKED.value == "locked"
    assert LeaderLockStatus.UNLOCKED.value == "unlocked"
    assert LeaderLockStatus.PURGED.value == "purged"

    # Test all states are present
    assert len(LeaderLockStatus) == 3


def test_leader_ready_status_enum_exists():
    """Test that LeaderReadyStatus enum exists with correct values.

    Requirements: 8.1, 8.2
    """
    from src.ti4.core.leaders import LeaderReadyStatus

    # Test enum values for agent ready/exhaust mechanics
    assert LeaderReadyStatus.READIED.value == "readied"
    assert LeaderReadyStatus.EXHAUSTED.value == "exhausted"

    # Test both states are present
    assert len(LeaderReadyStatus) == 2


def test_leader_ability_result_structure():
    """Test that LeaderAbilityResult dataclass has correct structure.

    Requirements: 8.3
    """
    from src.ti4.core.leaders import LeaderAbilityResult

    # Test successful result creation
    result = LeaderAbilityResult(
        success=True,
        effects=["Test effect"],
        error_message=None,
        game_state_changes={"test": "change"},
    )

    assert result.success is True
    assert result.effects == ["Test effect"]
    assert result.error_message is None
    assert result.game_state_changes == {"test": "change"}


def test_leader_ability_result_failure():
    """Test LeaderAbilityResult for failure cases.

    Requirements: 8.3
    """
    from src.ti4.core.leaders import LeaderAbilityResult

    # Test failure result creation
    result = LeaderAbilityResult(
        success=False, effects=[], error_message="Test error", game_state_changes=None
    )

    assert result.success is False
    assert result.effects == []
    assert result.error_message == "Test error"
    assert result.game_state_changes is None


def test_base_leader_abstract_class_exists():
    """Test that BaseLeader abstract class exists and cannot be instantiated.

    Requirements: 1.3, 8.1
    """
    from src.ti4.core.leaders import BaseLeader

    # Test that BaseLeader is abstract and cannot be instantiated
    with pytest.raises(TypeError):
        BaseLeader(faction=Faction.SOL, player_id="test_player")


def test_base_leader_has_required_abstract_methods():
    """Test that BaseLeader has all required abstract methods.

    Requirements: 1.3, 8.1, 8.2
    """
    from src.ti4.core.leaders import BaseLeader

    # Get abstract methods
    abstract_methods = getattr(BaseLeader, "__abstractmethods__", set())

    # Test required abstract methods are present
    expected_methods = {
        "get_leader_type",
        "get_name",
        "get_unlock_conditions",
        "check_unlock_conditions",
        "execute_ability",
        "_get_initial_lock_status",
        "_get_initial_ready_status",
    }

    assert expected_methods.issubset(abstract_methods)


def test_base_leader_input_validation():
    """Test that BaseLeader constructor validates inputs properly.

    Requirements: 8.1 - Robust error handling
    """
    from src.ti4.core.leaders import (
        BaseLeader,
        LeaderAbilityResult,
        LeaderLockStatus,
        LeaderReadyStatus,
        LeaderType,
    )

    # Create a concrete test class to test validation
    class TestLeader(BaseLeader):
        def get_leader_type(self) -> LeaderType:
            return LeaderType.AGENT

        def get_name(self) -> str:
            return "Test Leader"

        def get_unlock_conditions(self) -> list[str]:
            return []

        def check_unlock_conditions(self, game_state) -> bool:
            return True

        def execute_ability(self, game_state, **kwargs) -> LeaderAbilityResult:
            return LeaderAbilityResult(success=True, effects=[])

        def _get_initial_lock_status(self) -> LeaderLockStatus:
            return LeaderLockStatus.UNLOCKED

        def _get_initial_ready_status(self) -> LeaderReadyStatus | None:
            return LeaderReadyStatus.READIED

        def can_use_ability(self) -> bool:
            return True

        def unlock(self) -> None:
            pass

    # Test empty player_id validation
    with pytest.raises(ValueError, match="player_id cannot be empty or None"):
        TestLeader(faction=Faction.SOL, player_id="")

    with pytest.raises(ValueError, match="player_id cannot be empty or None"):
        TestLeader(faction=Faction.SOL, player_id="   ")


def test_base_leader_faction_validation():
    """Test that BaseLeader constructor validates faction type.

    Requirements: 8.1 - Robust error handling
    """
    from src.ti4.core.leaders import (
        BaseLeader,
        LeaderAbilityResult,
        LeaderLockStatus,
        LeaderReadyStatus,
        LeaderType,
    )

    # Create a concrete test class to test validation
    class TestLeader(BaseLeader):
        def get_leader_type(self) -> LeaderType:
            return LeaderType.AGENT

        def get_name(self) -> str:
            return "Test Leader"

        def get_unlock_conditions(self) -> list[str]:
            return []

        def check_unlock_conditions(self, game_state) -> bool:
            return True

        def execute_ability(self, game_state, **kwargs) -> LeaderAbilityResult:
            return LeaderAbilityResult(success=True, effects=[])

        def _get_initial_lock_status(self) -> LeaderLockStatus:
            return LeaderLockStatus.UNLOCKED

        def _get_initial_ready_status(self) -> LeaderReadyStatus | None:
            return LeaderReadyStatus.READIED

        def can_use_ability(self) -> bool:
            return True

        def unlock(self) -> None:
            pass

    # Test invalid faction type
    with pytest.raises(TypeError, match="faction must be a Faction enum value"):
        TestLeader(faction="invalid_faction", player_id="test_player")

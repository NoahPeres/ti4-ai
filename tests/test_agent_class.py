"""Tests for Agent class implementation.

This module tests the Agent class with ready/exhaust mechanics:
- Agent class extending BaseLeader
- exhaust() and ready() methods for state management
- can_use_ability() validation for readied state
- Agent state transitions

LRR References:
- Rule 51: LEADERS
- Requirements 2.1, 2.2, 2.3, 2.4, 2.5
"""

from src.ti4.core.constants import Faction
from src.ti4.core.leaders import (
    LeaderLockStatus,
    LeaderReadyStatus,
    LeaderStateError,
    LeaderType,
)


def test_agent_class_exists():
    """Test that Agent class exists and can be instantiated.

    Requirements: 2.1 - Agent class extending BaseLeader
    """
    from src.ti4.core.leaders import Agent

    agent = Agent(faction=Faction.SOL, player_id="test_player")
    assert agent is not None


def test_agent_has_correct_leader_type():
    """Test that Agent returns correct leader type.

    Requirements: 2.1 - Agent class extending BaseLeader
    """
    from src.ti4.core.leaders import Agent

    agent = Agent(faction=Faction.SOL, player_id="test_player")
    assert agent.get_leader_type() == LeaderType.AGENT


def test_agent_starts_unlocked():
    """Test that Agent starts in unlocked state.

    Requirements: 2.1 - Agents start unlocked without requiring unlock
    """
    from src.ti4.core.leaders import Agent

    agent = Agent(faction=Faction.SOL, player_id="test_player")
    assert agent.lock_status == LeaderLockStatus.UNLOCKED


def test_agent_starts_readied():
    """Test that Agent starts in readied state.

    Requirements: 2.2 - Agents start readied
    """
    from src.ti4.core.leaders import Agent

    agent = Agent(faction=Faction.SOL, player_id="test_player")
    assert agent.ready_status == LeaderReadyStatus.READIED


def test_agent_can_use_ability_when_readied():
    """Test that Agent can use ability when readied.

    Requirements: 2.4 - Agent abilities available when readied
    """
    from src.ti4.core.leaders import Agent

    agent = Agent(faction=Faction.SOL, player_id="test_player")
    assert agent.can_use_ability() is True


def test_agent_exhaust_method():
    """Test that Agent exhaust() method changes state to exhausted.

    Requirements: 2.2 - Agent becomes exhausted when ability is used
    """
    from src.ti4.core.leaders import Agent

    agent = Agent(faction=Faction.SOL, player_id="test_player")
    agent.exhaust()
    assert agent.ready_status == LeaderReadyStatus.EXHAUSTED


def test_agent_cannot_use_ability_when_exhausted():
    """Test that Agent cannot use ability when exhausted.

    Requirements: 2.5 - Agent abilities unavailable when exhausted
    """
    from src.ti4.core.leaders import Agent

    agent = Agent(faction=Faction.SOL, player_id="test_player")
    agent.exhaust()
    assert agent.can_use_ability() is False


def test_agent_ready_method():
    """Test that Agent ready() method changes state to readied.

    Requirements: 2.3 - Agents become readied during status phase
    """
    from src.ti4.core.leaders import Agent

    agent = Agent(faction=Faction.SOL, player_id="test_player")
    agent.exhaust()
    agent.ready()
    assert agent.ready_status == LeaderReadyStatus.READIED


def test_agent_ready_exhaust_cycle():
    """Test complete ready/exhaust cycle.

    Requirements: 2.2, 2.3 - Complete state transition cycle
    """
    from src.ti4.core.leaders import Agent

    agent = Agent(faction=Faction.SOL, player_id="test_player")

    # Start readied
    assert agent.ready_status == LeaderReadyStatus.READIED
    assert agent.can_use_ability() is True

    # Exhaust
    agent.exhaust()
    assert agent.ready_status == LeaderReadyStatus.EXHAUSTED
    assert agent.can_use_ability() is False

    # Ready again
    agent.ready()
    assert agent.ready_status == LeaderReadyStatus.READIED
    assert agent.can_use_ability() is True


def test_agent_exhaust_when_already_exhausted():
    """Test that exhausting an already exhausted agent raises error.

    Requirements: 2.2 - Robust state management with validation
    """
    import pytest

    from src.ti4.core.leaders import Agent

    agent = Agent(faction=Faction.SOL, player_id="test_player")
    agent.exhaust()

    with pytest.raises(
        LeaderStateError,
        match="Cannot exhaust Agent - already in already_exhausted state",
    ):
        agent.exhaust()


def test_agent_ready_when_already_readied():
    """Test that readying an already readied agent raises error.

    Requirements: 2.3 - Robust state management with validation
    """
    import pytest

    from src.ti4.core.leaders import Agent

    agent = Agent(faction=Faction.SOL, player_id="test_player")

    with pytest.raises(ValueError, match="Cannot ready agent in readied state"):
        agent.ready()

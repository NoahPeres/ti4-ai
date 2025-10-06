"""Tests for placeholder leader implementations.

This module tests the placeholder leader implementations that validate
the leader system architecture with different ability patterns.

LRR References:
- Rule 51: LEADERS
- Requirements 7.1, 7.2, 7.3, 7.4, 7.5

Note: These test placeholder implementations for architecture validation only.
"""

import pytest

from src.ti4.core.constants import Faction
from src.ti4.core.leaders import (
    LeaderLockStatus,
    LeaderReadyStatus,
    LeaderType,
    LeaderUnlockError,
)
from src.ti4.core.placeholder_leaders import (
    ConditionalTargetAgent,
    PowerfulHero,
    SimpleResourceAgent,
    UnlockableCommander,
    create_complex_placeholder_leaders,
    create_placeholder_leaders,
)


class MockGameState:
    """Mock game state for testing placeholder leaders."""

    def __init__(self, **kwargs):
        """Initialize mock game state with configurable attributes."""
        self.current_round = kwargs.get("current_round", 1)
        self._players_dict = kwargs.get("players", {})
        # Add phase for validation framework (matches GameState.phase)
        self.phase = kwargs.get("current_phase", "action_phase")

    def add_player(self, player_id: str, **player_attrs):
        """Add a mock player to the game state."""
        self._players_dict[player_id] = MockPlayer(player_id, **player_attrs)

    def get_player(self, player_id: str):
        """Get a player from the game state."""
        return self._players_dict.get(player_id)

    @property
    def players(self):
        """Return players as an iterable for validation code."""
        return self._players_dict.values()


class MockPlayer:
    """Mock player for testing."""

    def __init__(self, player_id: str, **kwargs):
        """Initialize mock player with configurable attributes."""
        self.id = player_id
        self.player_id = player_id  # Some code might expect player_id instead of id
        self.controlled_planets = kwargs.get("controlled_planets", 0)
        self.trade_goods = kwargs.get("trade_goods", 0)
        self.controls_mecatol_rex = kwargs.get("controls_mecatol_rex", False)
        self.completed_objectives = kwargs.get("completed_objectives", 0)
        self.victory_points = kwargs.get("victory_points", 0)


class TestSimpleResourceAgent:
    """Test the SimpleResourceAgent placeholder implementation."""

    def test_simple_agent_initialization(self):
        """Test that SimpleResourceAgent initializes correctly."""
        agent = SimpleResourceAgent(faction=Faction.SOL, player_id="test_player")

        assert agent.get_leader_type() == LeaderType.AGENT
        assert agent.get_name() == "Simple Resource Agent"
        assert agent.faction == Faction.SOL
        assert agent.player_id == "test_player"
        assert agent.lock_status == LeaderLockStatus.UNLOCKED
        assert agent.ready_status == LeaderReadyStatus.READIED

    def test_simple_agent_unlock_conditions(self):
        """Test that agents have no unlock conditions."""
        agent = SimpleResourceAgent(faction=Faction.SOL, player_id="test_player")
        game_state = MockGameState()

        assert agent.get_unlock_conditions() == []
        assert agent.check_unlock_conditions(game_state) is True

    def test_simple_agent_ability_success(self):
        """Test successful execution of simple agent ability."""
        agent = SimpleResourceAgent(faction=Faction.SOL, player_id="test_player")
        game_state = MockGameState()

        # Agent should be able to use ability when readied
        assert agent.can_use_ability() is True

        result = agent.execute_ability(game_state)

        assert result.success is True
        assert "Generated 1 trade good" in result.effects
        assert result.error_message is None
        assert result.game_state_changes is not None
        assert result.game_state_changes["trade_goods_gained"] == 1
        assert result.game_state_changes["ability_used"] == "Simple Resource Agent"

    def test_simple_agent_ability_when_exhausted(self):
        """Test that exhausted agent cannot use ability."""
        agent = SimpleResourceAgent(faction=Faction.SOL, player_id="test_player")
        game_state = MockGameState()

        # Exhaust the agent
        agent.exhaust()
        assert agent.can_use_ability() is False

        result = agent.execute_ability(game_state)

        assert result.success is False
        assert result.effects == []
        assert "cannot use ability in current state" in result.error_message

    def test_simple_agent_ready_exhaust_cycle(self):
        """Test agent ready/exhaust state transitions."""
        agent = SimpleResourceAgent(faction=Faction.SOL, player_id="test_player")

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


class TestConditionalTargetAgent:
    """Test the ConditionalTargetAgent placeholder implementation."""

    def test_conditional_agent_initialization(self):
        """Test that ConditionalTargetAgent initializes correctly."""
        agent = ConditionalTargetAgent(faction=Faction.HACAN, player_id="test_player")

        assert agent.get_leader_type() == LeaderType.AGENT
        assert agent.get_name() == "Conditional Target Agent"
        assert agent.faction == Faction.HACAN
        assert agent.player_id == "test_player"

    def test_conditional_agent_missing_target(self):
        """Test that ability fails when target parameter is missing."""
        agent = ConditionalTargetAgent(faction=Faction.HACAN, player_id="test_player")
        game_state = MockGameState(current_round=2)

        result = agent.execute_ability(game_state)

        assert result.success is False
        assert "Target parameter is required" in result.error_message

    def test_conditional_agent_invalid_target_type(self):
        """Test that ability fails with invalid target type."""
        agent = ConditionalTargetAgent(faction=Faction.HACAN, player_id="test_player")
        game_state = MockGameState(current_round=2)

        # Test with non-string target
        result = agent.execute_ability(game_state, target=123)
        assert result.success is False
        assert "Target must be a non-empty string" in result.error_message

        # Test with empty string target
        result = agent.execute_ability(game_state, target="")
        assert result.success is False
        assert "Target must be a non-empty string" in result.error_message

    def test_conditional_agent_early_round_restriction(self):
        """Test that ability fails in early rounds."""
        agent = ConditionalTargetAgent(faction=Faction.HACAN, player_id="test_player")
        game_state = MockGameState(current_round=1)

        result = agent.execute_ability(game_state, target="planet_a")

        assert result.success is False
        assert "can only be used from round 2 onwards" in result.error_message

    def test_conditional_agent_invalid_target(self):
        """Test that ability fails with invalid target."""
        agent = ConditionalTargetAgent(faction=Faction.HACAN, player_id="test_player")
        game_state = MockGameState(current_round=2)

        result = agent.execute_ability(game_state, target="invalid_target")

        assert result.success is False
        assert "Invalid target 'invalid_target'" in result.error_message
        assert "Valid targets:" in result.error_message

    def test_conditional_agent_successful_execution(self):
        """Test successful execution with valid conditions."""
        agent = ConditionalTargetAgent(faction=Faction.HACAN, player_id="test_player")
        game_state = MockGameState(current_round=3)

        result = agent.execute_ability(game_state, target="planet_a")

        assert result.success is True
        assert "Applied conditional effect to planet_a" in result.effects
        assert result.game_state_changes["target_affected"] == "planet_a"
        assert result.game_state_changes["effect_type"] == "conditional_boost"

    def test_conditional_agent_all_valid_targets(self):
        """Test that all valid targets work correctly."""
        agent = ConditionalTargetAgent(faction=Faction.HACAN, player_id="test_player")
        game_state = MockGameState(current_round=2)

        valid_targets = ["planet_a", "planet_b", "planet_c"]

        for target in valid_targets:
            result = agent.execute_ability(game_state, target=target)
            assert result.success is True
            assert f"Applied conditional effect to {target}" in result.effects


class TestUnlockableCommander:
    """Test the UnlockableCommander placeholder implementation."""

    def test_commander_initialization(self):
        """Test that UnlockableCommander initializes correctly."""
        commander = UnlockableCommander(faction=Faction.XXCHA, player_id="test_player")

        assert commander.get_leader_type() == LeaderType.COMMANDER
        assert commander.get_name() == "Unlockable Commander"
        assert commander.faction == Faction.XXCHA
        assert commander.player_id == "test_player"
        assert commander.lock_status == LeaderLockStatus.LOCKED
        assert commander.ready_status is None  # Commanders don't have ready status

    def test_commander_unlock_conditions(self):
        """Test commander unlock conditions."""
        commander = UnlockableCommander(faction=Faction.XXCHA, player_id="test_player")

        conditions = commander.get_unlock_conditions()
        assert "Control 3 or more planets" in conditions
        assert "Have at least 5 trade goods" in conditions

    def test_commander_unlock_conditions_not_met(self):
        """Test that unlock conditions fail when not met."""
        commander = UnlockableCommander(faction=Faction.XXCHA, player_id="test_player")
        game_state = MockGameState()

        # Add player with insufficient resources
        game_state.add_player("test_player", controlled_planets=2, trade_goods=3)

        assert commander.check_unlock_conditions(game_state) is False

    def test_commander_unlock_conditions_partially_met(self):
        """Test unlock conditions when only some are met."""
        commander = UnlockableCommander(faction=Faction.XXCHA, player_id="test_player")
        game_state = MockGameState()

        # Test with enough planets but not enough trade goods
        game_state.add_player("test_player", controlled_planets=4, trade_goods=2)
        assert commander.check_unlock_conditions(game_state) is False

        # Test with enough trade goods but not enough planets
        game_state.add_player("test_player", controlled_planets=1, trade_goods=8)
        assert commander.check_unlock_conditions(game_state) is False

    def test_commander_unlock_conditions_fully_met(self):
        """Test unlock conditions when all are met."""
        commander = UnlockableCommander(faction=Faction.XXCHA, player_id="test_player")
        game_state = MockGameState()

        # Add player with sufficient resources
        game_state.add_player("test_player", controlled_planets=5, trade_goods=7)

        assert commander.check_unlock_conditions(game_state) is True

    def test_commander_unlock_conditions_missing_player(self):
        """Test unlock conditions when player is not in game state."""
        commander = UnlockableCommander(
            faction=Faction.XXCHA, player_id="missing_player"
        )
        game_state = MockGameState()

        assert commander.check_unlock_conditions(game_state) is False

    def test_commander_ability_when_locked(self):
        """Test that locked commander cannot use ability."""
        commander = UnlockableCommander(faction=Faction.XXCHA, player_id="test_player")
        game_state = MockGameState()

        assert commander.can_use_ability() is False

        result = commander.execute_ability(game_state)

        assert result.success is False
        assert "is not unlocked" in result.error_message

    def test_commander_ability_when_unlocked(self):
        """Test successful commander ability execution when unlocked."""
        commander = UnlockableCommander(faction=Faction.XXCHA, player_id="test_player")
        game_state = MockGameState()

        # Unlock the commander
        commander.unlock()
        assert commander.can_use_ability() is True

        result = commander.execute_ability(game_state)

        assert result.success is True
        assert "All controlled planets produce +1 resource" in result.effects
        assert result.game_state_changes["ongoing_effect"] == "planet_resource_bonus"
        assert result.game_state_changes["bonus_amount"] == 1

    def test_commander_unlock_mechanics(self):
        """Test commander unlock state transitions."""
        commander = UnlockableCommander(faction=Faction.XXCHA, player_id="test_player")

        # Start locked
        assert commander.lock_status == LeaderLockStatus.LOCKED
        assert commander.can_use_ability() is False

        # Unlock
        commander.unlock()
        assert commander.lock_status == LeaderLockStatus.UNLOCKED
        assert commander.can_use_ability() is True

        # Unlocking again should not change state
        commander.unlock()
        assert commander.lock_status == LeaderLockStatus.UNLOCKED


class TestPowerfulHero:
    """Test the PowerfulHero placeholder implementation."""

    def test_hero_initialization(self):
        """Test that PowerfulHero initializes correctly."""
        hero = PowerfulHero(faction=Faction.JORD, player_id="test_player")

        assert hero.get_leader_type() == LeaderType.HERO
        assert hero.get_name() == "Powerful Hero"
        assert hero.faction == Faction.JORD
        assert hero.player_id == "test_player"
        assert hero.lock_status == LeaderLockStatus.LOCKED
        assert hero.ready_status is None  # Heroes don't have ready status

    def test_hero_unlock_conditions(self):
        """Test hero unlock conditions."""
        hero = PowerfulHero(faction=Faction.JORD, player_id="test_player")

        conditions = hero.get_unlock_conditions()
        assert "Control Mecatol Rex" in conditions
        assert "Have completed 2 or more objectives" in conditions
        assert "Have at least 10 victory points" in conditions

    def test_hero_unlock_conditions_not_met(self):
        """Test that unlock conditions fail when not met."""
        hero = PowerfulHero(faction=Faction.JORD, player_id="test_player")
        game_state = MockGameState()

        # Add player with insufficient progress
        game_state.add_player(
            "test_player",
            controls_mecatol_rex=False,
            completed_objectives=1,
            victory_points=5,
        )

        assert hero.check_unlock_conditions(game_state) is False

    def test_hero_unlock_conditions_partially_met(self):
        """Test unlock conditions when only some are met."""
        hero = PowerfulHero(faction=Faction.JORD, player_id="test_player")
        game_state = MockGameState()

        # Test with Mecatol Rex but not enough objectives/points
        game_state.add_player(
            "test_player",
            controls_mecatol_rex=True,
            completed_objectives=1,
            victory_points=5,
        )
        assert hero.check_unlock_conditions(game_state) is False

        # Test with objectives but not Mecatol Rex or points
        game_state.add_player(
            "test_player",
            controls_mecatol_rex=False,
            completed_objectives=3,
            victory_points=5,
        )
        assert hero.check_unlock_conditions(game_state) is False

    def test_hero_unlock_conditions_fully_met(self):
        """Test unlock conditions when all are met."""
        hero = PowerfulHero(faction=Faction.JORD, player_id="test_player")
        game_state = MockGameState()

        # Add player with all requirements met
        game_state.add_player(
            "test_player",
            controls_mecatol_rex=True,
            completed_objectives=3,
            victory_points=12,
        )

        assert hero.check_unlock_conditions(game_state) is True

    def test_hero_ability_when_locked(self):
        """Test that locked hero cannot use ability."""
        hero = PowerfulHero(faction=Faction.JORD, player_id="test_player")
        game_state = MockGameState()

        assert hero.can_use_ability() is False

        result = hero.execute_ability(game_state)

        assert result.success is False
        assert "cannot use ability in current state" in result.error_message

    def test_hero_ability_when_purged(self):
        """Test that purged hero cannot use ability."""
        hero = PowerfulHero(faction=Faction.JORD, player_id="test_player")
        game_state = MockGameState()

        # Unlock then purge
        hero.unlock()
        hero.purge()

        assert hero.can_use_ability() is False

        result = hero.execute_ability(game_state)

        assert result.success is False
        assert "cannot use ability in current state" in result.error_message

    def test_hero_ability_successful_execution(self):
        """Test successful hero ability execution."""
        hero = PowerfulHero(faction=Faction.JORD, player_id="test_player")
        game_state = MockGameState()

        # Unlock the hero
        hero.unlock()
        assert hero.can_use_ability() is True

        result = hero.execute_ability(game_state)

        assert result.success is True

        # Check all expected effects
        expected_effects = [
            "Gained 3 command tokens",
            "Drew 2 action cards",
            "Gained 5 trade goods",
            "All ships gain +1 combat for this round",
        ]

        for effect in expected_effects:
            assert effect in result.effects

        # Check game state changes
        changes = result.game_state_changes
        assert changes["command_tokens_gained"] == 3
        assert changes["action_cards_drawn"] == 2
        assert changes["trade_goods_gained"] == 5
        assert changes["combat_bonus_active"] is True
        assert changes["combat_bonus_amount"] == 1
        assert changes["hero_purged"] is True

    def test_hero_unlock_and_purge_mechanics(self):
        """Test hero unlock and purge state transitions."""
        hero = PowerfulHero(faction=Faction.JORD, player_id="test_player")

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

    def test_hero_cannot_unlock_when_purged(self):
        """Test that purged heroes cannot be unlocked."""
        hero = PowerfulHero(faction=Faction.JORD, player_id="test_player")

        # Purge directly from locked state
        hero.purge()
        assert hero.lock_status == LeaderLockStatus.PURGED

        # Attempting to unlock should raise error
        with pytest.raises(LeaderUnlockError, match="Cannot unlock purged hero"):
            hero.unlock()


class TestPlaceholderLeaderFactories:
    """Test the factory functions for creating placeholder leaders."""

    def test_create_placeholder_leaders(self):
        """Test basic placeholder leader creation."""
        leaders = create_placeholder_leaders(Faction.SOL, "test_player")

        assert len(leaders) == 3

        # Check types and order
        assert isinstance(leaders[0], SimpleResourceAgent)
        assert isinstance(leaders[1], UnlockableCommander)
        assert isinstance(leaders[2], PowerfulHero)

        # Check all have correct faction and player
        for leader in leaders:
            assert leader.faction == Faction.SOL
            assert leader.player_id == "test_player"

    def test_create_complex_placeholder_leaders(self):
        """Test complex placeholder leader creation."""
        leaders = create_complex_placeholder_leaders(Faction.HACAN, "test_player")

        assert len(leaders) == 3

        # Check types and order
        assert isinstance(leaders[0], ConditionalTargetAgent)
        assert isinstance(leaders[1], UnlockableCommander)
        assert isinstance(leaders[2], PowerfulHero)

        # Check all have correct faction and player
        for leader in leaders:
            assert leader.faction == Faction.HACAN
            assert leader.player_id == "test_player"

    def test_factory_functions_with_different_factions(self):
        """Test factory functions work with different factions."""
        factions_to_test = [Faction.SOL, Faction.HACAN, Faction.XXCHA, Faction.JORD]

        for faction in factions_to_test:
            # Test basic factory
            basic_leaders = create_placeholder_leaders(
                faction, f"player_{faction.value}"
            )
            assert len(basic_leaders) == 3
            assert all(leader.faction == faction for leader in basic_leaders)

            # Test complex factory
            complex_leaders = create_complex_placeholder_leaders(
                faction, f"player_{faction.value}"
            )
            assert len(complex_leaders) == 3
            assert all(leader.faction == faction for leader in complex_leaders)


class TestPlaceholderLeaderIntegration:
    """Integration tests for placeholder leaders with the leader system."""

    def test_placeholder_leaders_with_leader_sheet(self):
        """Test that placeholder leaders work with LeaderSheet."""
        from src.ti4.core.leaders import LeaderSheet

        leaders = create_placeholder_leaders(Faction.SOL, "test_player")
        sheet = LeaderSheet(player_id="test_player")

        # Assign leaders to sheet
        sheet.set_agent(leaders[0])
        sheet.set_commander(leaders[1])
        sheet.set_hero(leaders[2])

        assert sheet.is_complete()
        assert len(sheet.get_all_leaders()) == 3

        # Test retrieval by type
        assert sheet.get_leader_by_type(LeaderType.AGENT) == leaders[0]
        assert sheet.get_leader_by_type(LeaderType.COMMANDER) == leaders[1]
        assert sheet.get_leader_by_type(LeaderType.HERO) == leaders[2]

        # Test retrieval by name
        assert sheet.get_leader_by_name("Simple Resource Agent") == leaders[0]
        assert sheet.get_leader_by_name("Unlockable Commander") == leaders[1]
        assert sheet.get_leader_by_name("Powerful Hero") == leaders[2]

    def test_placeholder_leaders_with_leader_registry(self):
        """Test that placeholder leaders work with LeaderRegistry patterns."""
        from src.ti4.core.leaders import LeaderRegistry

        registry = LeaderRegistry()

        # Test that registry can create leaders (uses base classes)
        registry_leaders = registry.create_faction_leaders(Faction.SOL, "test_player")
        assert len(registry_leaders) == 3

        # Test that placeholder leaders follow same pattern
        placeholder_leaders = create_placeholder_leaders(Faction.SOL, "test_player")
        assert len(placeholder_leaders) == 3

        # Both should have same leader types in same order
        for i in range(3):
            assert (
                registry_leaders[i].get_leader_type()
                == placeholder_leaders[i].get_leader_type()
            )

    def test_placeholder_leader_ability_validation(self):
        """Test placeholder leaders with ability validation framework."""
        from src.ti4.core.game_phase import GamePhase
        from src.ti4.core.leaders import LeaderAbilityValidator

        agent = SimpleResourceAgent(faction=Faction.SOL, player_id="test_player")
        game_state = MockGameState(current_phase=GamePhase.ACTION)

        # Add the player to the game state for validation
        game_state.add_player("test_player")

        # Test validation passes for readied agent
        error = LeaderAbilityValidator.validate_ability_execution(agent, game_state)
        assert error is None

        # Test validation fails for exhausted agent
        agent.exhaust()
        error = LeaderAbilityValidator.validate_ability_execution(agent, game_state)
        assert error is not None
        assert "exhausted" in error.lower()

    def test_end_to_end_placeholder_leader_workflow(self):
        """Test complete workflow with placeholder leaders."""
        # Create leaders
        leaders = create_placeholder_leaders(Faction.SOL, "test_player")
        agent, commander, hero = leaders

        # Create game state with player
        game_state = MockGameState(current_round=3)
        game_state.add_player(
            "test_player",
            controlled_planets=5,
            trade_goods=7,
            controls_mecatol_rex=True,
            completed_objectives=3,
            victory_points=12,
        )

        # Test agent workflow
        assert agent.can_use_ability()
        agent_result = agent.execute_ability(game_state)
        assert agent_result.success
        agent.exhaust()  # Simulate post-ability exhaustion
        assert not agent.can_use_ability()

        # Test commander workflow
        assert not commander.can_use_ability()  # Starts locked
        assert commander.check_unlock_conditions(game_state)  # Conditions met
        commander.unlock()
        assert commander.can_use_ability()
        commander_result = commander.execute_ability(game_state)
        assert commander_result.success

        # Test hero workflow
        assert not hero.can_use_ability()  # Starts locked
        assert hero.check_unlock_conditions(game_state)  # Conditions met
        hero.unlock()
        assert hero.can_use_ability()
        hero_result = hero.execute_ability(game_state)
        assert hero_result.success
        hero.purge()  # Simulate post-ability purge
        assert not hero.can_use_ability()

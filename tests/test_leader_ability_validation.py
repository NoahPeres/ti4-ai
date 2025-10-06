"""Tests for leader ability validation framework.

This module tests the LeaderAbilityValidator class and related validation
functionality for Rule 51: LEADERS.

LRR References:
- Rule 51: LEADERS
- Requirements 9.1, 9.2, 9.3, 9.4, 9.5
"""

from unittest.mock import Mock

from src.ti4.core.constants import Faction
from src.ti4.core.game_phase import GamePhase
from src.ti4.core.game_state import GameState
from src.ti4.core.leaders import (
    Agent,
    Commander,
    Hero,
    LeaderAbilityValidator,
    LeaderLockStatus,
    LeaderManager,
    LeaderReadyStatus,
)
from src.ti4.core.player import Player


class TestLeaderAbilityValidator:
    """Test cases for LeaderAbilityValidator class.

    Tests comprehensive validation for leader ability execution including
    state validation, timing validation, resource validation, and target validation.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 9.1, 9.2, 9.3, 9.4, 9.5
    """

    def test_validate_ability_execution_success(self) -> None:
        """Test successful validation when all conditions are met."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        player = Mock(spec=Player)
        player.id = "player1"
        game_state = Mock(spec=GameState)
        game_state.phase = GamePhase.ACTION
        game_state.players = [player]

        # Act
        result = LeaderAbilityValidator.validate_ability_execution(agent, game_state)

        # Assert
        assert result is None

    def test_validate_ability_execution_leader_state_failure(self) -> None:
        """Test validation failure when leader is in invalid state."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        agent.exhaust()  # Make agent exhausted
        game_state = Mock(spec=GameState)

        # Act
        result = LeaderAbilityValidator.validate_ability_execution(agent, game_state)

        # Assert
        assert result is not None
        assert "exhausted" in result
        assert "cannot use abilities" in result

    def test_validate_leader_state_agent_unlocked_and_readied(self) -> None:
        """Test agent state validation when unlocked and readied."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")

        # Act
        result = LeaderAbilityValidator._validate_leader_state(agent)

        # Assert
        assert result is None

    def test_validate_leader_state_agent_exhausted(self) -> None:
        """Test agent state validation when exhausted."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        agent.exhaust()

        # Act
        result = LeaderAbilityValidator._validate_leader_state(agent)

        # Assert
        assert result is not None
        assert "Agent" in result
        assert "exhausted" in result
        assert "cannot use abilities until readied" in result

    def test_validate_leader_state_commander_locked(self) -> None:
        """Test commander state validation when locked."""
        # Arrange
        commander = Commander(faction=Faction.ARBOREC, player_id="player1")

        # Act
        result = LeaderAbilityValidator._validate_leader_state(commander)

        # Assert
        assert result is not None
        assert "Commander" in result
        assert "locked" in result
        assert "cannot use abilities until unlocked" in result

    def test_validate_leader_state_commander_unlocked(self) -> None:
        """Test commander state validation when unlocked."""
        # Arrange
        commander = Commander(faction=Faction.ARBOREC, player_id="player1")
        commander.unlock()

        # Act
        result = LeaderAbilityValidator._validate_leader_state(commander)

        # Assert
        assert result is None

    def test_validate_leader_state_hero_locked(self) -> None:
        """Test hero state validation when locked."""
        # Arrange
        hero = Hero(faction=Faction.ARBOREC, player_id="player1")

        # Act
        result = LeaderAbilityValidator._validate_leader_state(hero)

        # Assert
        assert result is not None
        assert "Hero" in result
        assert "locked" in result
        assert "cannot use abilities until unlocked" in result

    def test_validate_leader_state_hero_unlocked(self) -> None:
        """Test hero state validation when unlocked."""
        # Arrange
        hero = Hero(faction=Faction.ARBOREC, player_id="player1")
        hero.unlock()

        # Act
        result = LeaderAbilityValidator._validate_leader_state(hero)

        # Assert
        assert result is None

    def test_validate_leader_state_hero_purged(self) -> None:
        """Test hero state validation when purged."""
        # Arrange
        hero = Hero(faction=Faction.ARBOREC, player_id="player1")
        hero.unlock()
        hero.purge()

        # Act
        result = LeaderAbilityValidator._validate_leader_state(hero)

        # Assert
        assert result is not None
        assert "Hero" in result
        assert "purged" in result
        assert "can no longer use abilities" in result


class TestLeaderAbilityValidatorTiming:
    """Test cases for timing validation in LeaderAbilityValidator.

    Tests game phase validation and sequence timing validation.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 9.1, 9.5
    """

    def test_validate_timing_no_current_phase(self) -> None:
        """Test timing validation when current phase is not available."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        game_state = Mock(spec=GameState)
        game_state.phase = None

        # Act
        result = LeaderAbilityValidator._validate_timing(agent, game_state)

        # Assert
        assert result is not None
        assert "Cannot determine current game phase" in result

    def test_validate_timing_valid_phase(self) -> None:
        """Test timing validation with valid game phase."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        game_state = Mock(spec=GameState)
        game_state.phase = GamePhase.ACTION

        # Act
        result = LeaderAbilityValidator._validate_timing(
            agent, game_state, timing_window="action_phase"
        )

        # Assert
        assert result is None

    def test_validate_phase_timing_action_phase_valid(self) -> None:
        """Test phase timing validation for action phase abilities."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")

        # Act
        result = LeaderAbilityValidator._validate_phase_timing(
            GamePhase.ACTION, "action_phase", agent
        )

        # Assert
        assert result is None

    def test_validate_phase_timing_action_phase_invalid(self) -> None:
        """Test phase timing validation failure for action phase abilities."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")

        # Act
        result = LeaderAbilityValidator._validate_phase_timing(
            GamePhase.STATUS, "action_phase", agent
        )

        # Assert
        assert result is not None
        assert "Agent" in result
        assert "can only be used during action phase" in result
        assert "current phase is status" in result

    def test_validate_phase_timing_any_phase_valid(self) -> None:
        """Test phase timing validation for abilities usable in any phase."""
        # Arrange
        commander = Commander(faction=Faction.ARBOREC, player_id="player1")

        # Act - Test multiple phases
        phases_to_test = [
            GamePhase.SETUP,
            GamePhase.STRATEGY,
            GamePhase.ACTION,
            GamePhase.STATUS,
            GamePhase.AGENDA,
        ]

        for phase in phases_to_test:
            result = LeaderAbilityValidator._validate_phase_timing(
                phase, "any_phase", commander
            )
            assert result is None

    def test_validate_phase_timing_status_phase_valid(self) -> None:
        """Test phase timing validation for status phase abilities."""
        # Arrange
        hero = Hero(faction=Faction.ARBOREC, player_id="player1")

        # Act
        result = LeaderAbilityValidator._validate_phase_timing(
            GamePhase.STATUS, "status_phase", hero
        )

        # Assert
        assert result is None

    def test_validate_phase_timing_unknown_timing_window(self) -> None:
        """Test phase timing validation with unknown timing window."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")

        # Act
        result = LeaderAbilityValidator._validate_phase_timing(
            GamePhase.ACTION, "unknown_timing", agent
        )

        # Assert
        assert result is None  # Unknown timing windows are allowed (no restriction)

    def test_validate_sequence_timing_placeholder(self) -> None:
        """Test sequence timing validation (placeholder implementation)."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        game_state = Mock(spec=GameState)

        # Act
        result = LeaderAbilityValidator._validate_sequence_timing(
            agent, game_state, before_action="some_action"
        )

        # Assert
        assert result is None  # Placeholder implementation returns None


class TestLeaderAbilityValidatorResources:
    """Test cases for resource validation in LeaderAbilityValidator.

    Tests validation of trade goods, influence, resources, and command token costs.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 9.3
    """

    def test_validate_resources_player_not_found(self) -> None:
        """Test resource validation when player is not found."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        game_state = Mock(spec=GameState)
        game_state.players = []

        # Act
        result = LeaderAbilityValidator._validate_resources(agent, game_state)

        # Assert
        assert result is not None
        assert "Player player1 not found" in result

    def test_validate_resources_no_costs(self) -> None:
        """Test resource validation when no costs are specified."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        player = Mock(spec=Player)
        player.id = "player1"
        game_state = Mock(spec=GameState)
        game_state.players = [player]

        # Act
        result = LeaderAbilityValidator._validate_resources(agent, game_state)

        # Assert
        assert result is None

    def test_validate_resources_sufficient_trade_goods(self) -> None:
        """Test resource validation with sufficient trade goods."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        player = Mock(spec=Player)
        player.id = "player1"
        player.trade_goods = 5
        game_state = Mock(spec=GameState)
        game_state.players = [player]

        # Act
        result = LeaderAbilityValidator._validate_resources(
            agent, game_state, trade_goods_cost=3
        )

        # Assert
        assert result is None

    def test_validate_resources_insufficient_trade_goods(self) -> None:
        """Test resource validation with insufficient trade goods."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        player = Mock(spec=Player)
        player.id = "player1"
        player.trade_goods = 2
        game_state = Mock(spec=GameState)
        game_state.players = [player]

        # Act
        result = LeaderAbilityValidator._validate_resources(
            agent, game_state, trade_goods_cost=5
        )

        # Assert
        assert result is not None
        assert "Agent" in result
        assert "requires 5 trade goods" in result
        assert "only has 2" in result

    def test_validate_resources_sufficient_influence(self) -> None:
        """Test resource validation with sufficient influence."""
        # Arrange
        commander = Commander(faction=Faction.ARBOREC, player_id="player1")
        player = Mock(spec=Player)
        player.id = "player1"
        player.available_influence = 8
        game_state = Mock(spec=GameState)
        game_state.players = [player]

        # Act
        result = LeaderAbilityValidator._validate_resources(
            commander, game_state, influence_cost=6
        )

        # Assert
        assert result is None

    def test_validate_resources_insufficient_influence(self) -> None:
        """Test resource validation with insufficient influence."""
        # Arrange
        commander = Commander(faction=Faction.ARBOREC, player_id="player1")
        player = Mock(spec=Player)
        player.id = "player1"
        player.available_influence = 3
        game_state = Mock(spec=GameState)
        game_state.players = [player]

        # Act
        result = LeaderAbilityValidator._validate_resources(
            commander, game_state, influence_cost=5
        )

        # Assert
        assert result is not None
        assert "Commander" in result
        assert "requires 5 influence" in result
        assert "only has 3" in result

    def test_validate_resources_sufficient_resources(self) -> None:
        """Test resource validation with sufficient resources."""
        # Arrange
        hero = Hero(faction=Faction.ARBOREC, player_id="player1")
        player = Mock(spec=Player)
        player.id = "player1"
        player.available_resources = 10
        game_state = Mock(spec=GameState)
        game_state.players = [player]

        # Act
        result = LeaderAbilityValidator._validate_resources(
            hero, game_state, resource_cost=7
        )

        # Assert
        assert result is None

    def test_validate_resources_insufficient_resources(self) -> None:
        """Test resource validation with insufficient resources."""
        # Arrange
        hero = Hero(faction=Faction.ARBOREC, player_id="player1")
        player = Mock(spec=Player)
        player.id = "player1"
        player.available_resources = 4
        game_state = Mock(spec=GameState)
        game_state.players = [player]

        # Act
        result = LeaderAbilityValidator._validate_resources(
            hero, game_state, resource_cost=6
        )

        # Assert
        assert result is not None
        assert "Hero" in result
        assert "requires 6 resources" in result
        assert "only has 4" in result

    def test_validate_resources_sufficient_command_tokens(self) -> None:
        """Test resource validation with sufficient command tokens."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        player = Mock(spec=Player)
        player.id = "player1"
        player.available_command_tokens = 4
        game_state = Mock(spec=GameState)
        game_state.players = [player]

        # Act
        result = LeaderAbilityValidator._validate_resources(
            agent, game_state, command_token_cost=2
        )

        # Assert
        assert result is None

    def test_validate_resources_insufficient_command_tokens(self) -> None:
        """Test resource validation with insufficient command tokens."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        player = Mock(spec=Player)
        player.id = "player1"
        player.available_command_tokens = 1
        game_state = Mock(spec=GameState)
        game_state.players = [player]

        # Act
        result = LeaderAbilityValidator._validate_resources(
            agent, game_state, command_token_cost=3
        )

        # Assert
        assert result is not None
        assert "Agent" in result
        assert "requires 3 command tokens" in result
        assert "only has 1" in result

    def test_validate_resources_multiple_costs(self) -> None:
        """Test resource validation with multiple resource costs."""
        # Arrange
        commander = Commander(faction=Faction.ARBOREC, player_id="player1")
        player = Mock(spec=Player)
        player.id = "player1"
        player.trade_goods = 3
        player.available_influence = 5
        player.available_resources = 4
        player.available_command_tokens = 2
        game_state = Mock(spec=GameState)
        game_state.players = [player]

        # Act
        result = LeaderAbilityValidator._validate_resources(
            commander,
            game_state,
            trade_goods_cost=2,
            influence_cost=4,
            resource_cost=3,
            command_token_cost=1,
        )

        # Assert
        assert result is None

    def test_validate_resources_multiple_costs_one_insufficient(self) -> None:
        """Test resource validation with multiple costs where one is insufficient."""
        # Arrange
        commander = Commander(faction=Faction.ARBOREC, player_id="player1")
        player = Mock(spec=Player)
        player.id = "player1"
        player.trade_goods = 3
        player.available_influence = 2  # Insufficient
        player.available_resources = 4
        player.available_command_tokens = 2
        game_state = Mock(spec=GameState)
        game_state.players = [player]

        # Act
        result = LeaderAbilityValidator._validate_resources(
            commander,
            game_state,
            trade_goods_cost=2,
            influence_cost=4,  # Requires 4, but player only has 2
            resource_cost=3,
            command_token_cost=1,
        )

        # Assert
        assert result is not None
        assert "requires 4 influence" in result
        assert "only has 2" in result


class TestLeaderAbilityValidatorTargets:
    """Test cases for target validation in LeaderAbilityValidator.

    Tests validation of player, system, planet, and unit targets.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 9.4
    """

    def test_validate_targets_no_targets(self) -> None:
        """Test target validation when no targets are specified."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        game_state = Mock(spec=GameState)

        # Act
        result = LeaderAbilityValidator._validate_targets(agent, game_state)

        # Assert
        assert result is None

    def test_validate_player_target_exists(self) -> None:
        """Test player target validation when target exists."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        player1 = Mock(spec=Player)
        player1.id = "player1"
        player2 = Mock(spec=Player)
        player2.id = "player2"
        game_state = Mock(spec=GameState)
        game_state.players = [player1, player2]

        # Act
        result = LeaderAbilityValidator._validate_targets(
            agent, game_state, target_player="player2"
        )

        # Assert
        assert result is None

    def test_validate_player_target_not_exists(self) -> None:
        """Test player target validation when target doesn't exist."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        player1 = Mock(spec=Player)
        player1.id = "player1"
        game_state = Mock(spec=GameState)
        game_state.players = [player1]

        # Act
        result = LeaderAbilityValidator._validate_targets(
            agent, game_state, target_player="nonexistent"
        )

        # Assert
        assert result is not None
        assert "Target player nonexistent does not exist" in result

    def test_validate_player_target_self(self) -> None:
        """Test player target validation when targeting self."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        player1 = Mock(spec=Player)
        player1.id = "player1"
        game_state = Mock(spec=GameState)
        game_state.players = [player1]

        # Act
        result = LeaderAbilityValidator._validate_targets(
            agent, game_state, target_player="player1"
        )

        # Assert
        assert result is None  # Self-targeting is allowed by default

    def test_validate_system_target_valid(self) -> None:
        """Test system target validation with valid system."""
        # Arrange
        commander = Commander(faction=Faction.ARBOREC, player_id="player1")
        game_state = Mock(spec=GameState)

        # Act
        result = LeaderAbilityValidator._validate_targets(
            commander, game_state, target_system="system_01"
        )

        # Assert
        assert result is None

    def test_validate_system_target_empty(self) -> None:
        """Test system target validation with empty system."""
        # Arrange
        commander = Commander(faction=Faction.ARBOREC, player_id="player1")
        game_state = Mock(spec=GameState)

        # Act
        result = LeaderAbilityValidator._validate_targets(
            commander, game_state, target_system=""
        )

        # Assert
        assert result is not None
        assert "System target cannot be empty" in result

    def test_validate_planet_target_valid(self) -> None:
        """Test planet target validation with valid planet."""
        # Arrange
        hero = Hero(faction=Faction.ARBOREC, player_id="player1")
        game_state = Mock(spec=GameState)

        # Act
        result = LeaderAbilityValidator._validate_targets(
            hero, game_state, target_planet="Mecatol Rex"
        )

        # Assert
        assert result is None

    def test_validate_planet_target_empty(self) -> None:
        """Test planet target validation with empty planet."""
        # Arrange
        hero = Hero(faction=Faction.ARBOREC, player_id="player1")
        game_state = Mock(spec=GameState)

        # Act
        result = LeaderAbilityValidator._validate_targets(
            hero, game_state, target_planet=""
        )

        # Assert
        assert result is not None
        assert "Planet target cannot be empty" in result

    def test_validate_unit_targets_valid(self) -> None:
        """Test unit target validation with valid units."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        game_state = Mock(spec=GameState)

        # Act
        result = LeaderAbilityValidator._validate_targets(
            agent, game_state, target_units=["unit1", "unit2", "unit3"]
        )

        # Assert
        assert result is None

    def test_validate_unit_targets_empty_list(self) -> None:
        """Test unit target validation with empty list."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        game_state = Mock(spec=GameState)

        # Act
        result = LeaderAbilityValidator._validate_targets(
            agent, game_state, target_units=[]
        )

        # Assert
        assert result is not None
        assert "Unit targets list cannot be empty when specified" in result

    def test_validate_unit_targets_empty_unit(self) -> None:
        """Test unit target validation with empty unit in list."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        game_state = Mock(spec=GameState)

        # Act
        result = LeaderAbilityValidator._validate_targets(
            agent, game_state, target_units=["unit1", "", "unit3"]
        )

        # Assert
        assert result is not None
        assert "Unit target cannot be empty" in result

    def test_validate_targets_multiple_targets(self) -> None:
        """Test target validation with multiple target types."""
        # Arrange
        commander = Commander(faction=Faction.ARBOREC, player_id="player1")
        player1 = Mock(spec=Player)
        player1.id = "player1"
        player2 = Mock(spec=Player)
        player2.id = "player2"
        game_state = Mock(spec=GameState)
        game_state.players = [player1, player2]

        # Act
        result = LeaderAbilityValidator._validate_targets(
            commander,
            game_state,
            target_player="player2",
            target_system="system_01",
            target_planet="Mecatol Rex",
            target_units=["unit1", "unit2"],
        )

        # Assert
        assert result is None


class TestLeaderManagerValidation:
    """Test cases for LeaderManager validation integration.

    Tests that LeaderManager properly uses the validation framework.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 9.1, 9.2, 9.3, 9.4, 9.5
    """

    def test_validate_leader_ability_success(self) -> None:
        """Test LeaderManager.validate_leader_ability with successful validation."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        player = Mock(spec=Player)
        player.id = "player1"
        player.leader_sheet = Mock()
        player.leader_sheet.get_leader_by_name.return_value = agent

        game_state = Mock(spec=GameState)
        game_state.phase = GamePhase.ACTION
        game_state.players = [player]

        manager = LeaderManager(game_state)

        # Act
        result = manager.validate_leader_ability("player1", "Agent")

        # Assert
        assert result is None

    def test_validate_leader_ability_leader_not_found(self) -> None:
        """Test LeaderManager.validate_leader_ability when leader not found."""
        # Arrange
        player = Mock(spec=Player)
        player.id = "player1"
        player.leader_sheet = Mock()
        player.leader_sheet.get_leader_by_name.return_value = None

        game_state = Mock(spec=GameState)
        game_state.players = [player]

        manager = LeaderManager(game_state)

        # Act
        result = manager.validate_leader_ability("player1", "NonExistent")

        # Assert
        assert result is not None
        assert "Leader NonExistent not found" in result

    def test_validate_leader_ability_validation_failure(self) -> None:
        """Test LeaderManager.validate_leader_ability with validation failure."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        agent.exhaust()  # Make agent exhausted

        player = Mock(spec=Player)
        player.id = "player1"
        player.leader_sheet = Mock()
        player.leader_sheet.get_leader_by_name.return_value = agent

        game_state = Mock(spec=GameState)
        game_state.phase = GamePhase.ACTION
        game_state.players = [player]

        manager = LeaderManager(game_state)

        # Act
        result = manager.validate_leader_ability("player1", "Agent")

        # Assert
        assert result is not None
        assert "exhausted" in result

    def test_execute_leader_ability_with_validation_success(self) -> None:
        """Test LeaderManager.execute_leader_ability with successful validation."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")

        player = Mock(spec=Player)
        player.id = "player1"
        player.leader_sheet = Mock()
        player.leader_sheet.get_leader_by_name.return_value = agent

        game_state = Mock(spec=GameState)
        game_state.phase = GamePhase.ACTION
        game_state.players = [player]

        manager = LeaderManager(game_state)

        # Act
        result = manager.execute_leader_ability("player1", "Agent")

        # Assert
        assert result.success is True
        assert agent.ready_status == LeaderReadyStatus.EXHAUSTED

    def test_execute_leader_ability_with_validation_failure(self) -> None:
        """Test LeaderManager.execute_leader_ability with validation failure."""
        # Arrange
        commander = Commander(faction=Faction.ARBOREC, player_id="player1")
        # Commander starts locked, so validation should fail

        player = Mock(spec=Player)
        player.id = "player1"
        player.leader_sheet = Mock()
        player.leader_sheet.get_leader_by_name.return_value = commander

        game_state = Mock(spec=GameState)
        game_state.phase = GamePhase.ACTION
        game_state.players = [player]

        manager = LeaderManager(game_state)

        # Act
        result = manager.execute_leader_ability("player1", "Commander")

        # Assert
        assert result.success is False
        assert "locked" in result.error_message
        assert commander.lock_status == LeaderLockStatus.LOCKED  # Unchanged

    def test_execute_leader_ability_hero_purged_after_use(self) -> None:
        """Test that heroes are purged after successful ability execution."""
        # Arrange
        hero = Hero(faction=Faction.ARBOREC, player_id="player1")
        hero.unlock()  # Unlock hero so it can use abilities

        player = Mock(spec=Player)
        player.id = "player1"
        player.leader_sheet = Mock()
        player.leader_sheet.get_leader_by_name.return_value = hero

        game_state = Mock(spec=GameState)
        game_state.phase = GamePhase.ACTION
        game_state.players = [player]

        manager = LeaderManager(game_state)

        # Act
        result = manager.execute_leader_ability("player1", "Hero")

        # Assert
        assert result.success is True
        assert hero.lock_status == LeaderLockStatus.PURGED


class TestLeaderAbilityValidatorUnlockConditions:
    """Test cases for unlock condition validation in LeaderAbilityValidator.

    Tests validation of unlock attempts for commanders and heroes.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 9.1, 9.2, 9.5
    """

    def test_validate_unlock_conditions_agent_invalid(self) -> None:
        """Test unlock validation for agents (should fail - agents don't need unlock)."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        game_state = Mock(spec=GameState)

        # Act
        result = LeaderAbilityValidator.validate_unlock_conditions(agent, game_state)

        # Assert
        assert result is not None
        assert "Agents do not need to be unlocked" in result

    def test_validate_unlock_conditions_commander_already_unlocked(self) -> None:
        """Test unlock validation for already unlocked commander."""
        # Arrange
        commander = Commander(faction=Faction.ARBOREC, player_id="player1")
        commander.unlock()  # Already unlocked
        game_state = Mock(spec=GameState)

        # Act
        result = LeaderAbilityValidator.validate_unlock_conditions(
            commander, game_state
        )

        # Assert
        assert result is not None
        assert "already unlocked" in result

    def test_validate_unlock_conditions_hero_purged(self) -> None:
        """Test unlock validation for purged hero."""
        # Arrange
        hero = Hero(faction=Faction.ARBOREC, player_id="player1")
        hero.unlock()
        hero.purge()  # Purged
        game_state = Mock(spec=GameState)

        # Act
        result = LeaderAbilityValidator.validate_unlock_conditions(hero, game_state)

        # Assert
        assert result is not None
        assert "purged and cannot be unlocked" in result

    def test_validate_unlock_conditions_commander_conditions_not_met(self) -> None:
        """Test unlock validation when conditions are not met."""
        # Arrange
        commander = Commander(faction=Faction.ARBOREC, player_id="player1")
        game_state = Mock(spec=GameState)

        # Act
        result = LeaderAbilityValidator.validate_unlock_conditions(
            commander, game_state
        )

        # Assert
        assert result is not None
        assert "Unlock conditions not met" in result

    def test_validate_unlock_conditions_hero_valid(self) -> None:
        """Test unlock validation for hero with met conditions."""
        # Arrange
        hero = Hero(faction=Faction.ARBOREC, player_id="player1")
        hero.check_unlock_conditions = Mock(return_value=True)  # Mock conditions as met
        game_state = Mock(spec=GameState)

        # Act
        result = LeaderAbilityValidator.validate_unlock_conditions(hero, game_state)

        # Assert
        assert result is None


class TestLeaderAbilityValidatorStateTransitions:
    """Test cases for state transition validation in LeaderAbilityValidator.

    Tests validation of leader state changes and transitions.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 9.1, 9.2
    """

    def test_validate_state_transition_agent_exhaust_valid(self) -> None:
        """Test valid agent exhaust transition."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")

        # Act
        result = LeaderAbilityValidator.validate_state_transition(
            agent, "readied", "exhausted", "exhaust"
        )

        # Assert
        assert result is None

    def test_validate_state_transition_agent_exhaust_invalid(self) -> None:
        """Test invalid agent exhaust transition (already exhausted)."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        agent.exhaust()  # Already exhausted

        # Act
        result = LeaderAbilityValidator.validate_state_transition(
            agent, "exhausted", "exhausted", "exhaust"
        )

        # Assert
        assert result is not None
        assert "not in readied state" in result

    def test_validate_state_transition_agent_ready_valid(self) -> None:
        """Test valid agent ready transition."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        agent.exhaust()  # Make exhausted first

        # Act
        result = LeaderAbilityValidator.validate_state_transition(
            agent, "exhausted", "readied", "ready"
        )

        # Assert
        assert result is None

    def test_validate_state_transition_agent_ready_invalid(self) -> None:
        """Test invalid agent ready transition (not exhausted)."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")

        # Act
        result = LeaderAbilityValidator.validate_state_transition(
            agent, "readied", "readied", "ready"
        )

        # Assert
        assert result is not None
        assert "not in exhausted state" in result

    def test_validate_state_transition_commander_unlock_valid(self) -> None:
        """Test valid commander unlock transition."""
        # Arrange
        commander = Commander(faction=Faction.ARBOREC, player_id="player1")

        # Act
        result = LeaderAbilityValidator.validate_state_transition(
            commander, "locked", "unlocked", "unlock"
        )

        # Assert
        assert result is None

    def test_validate_state_transition_commander_unlock_invalid(self) -> None:
        """Test invalid commander unlock transition (already unlocked)."""
        # Arrange
        commander = Commander(faction=Faction.ARBOREC, player_id="player1")
        commander.unlock()  # Already unlocked

        # Act
        result = LeaderAbilityValidator.validate_state_transition(
            commander, "unlocked", "unlocked", "unlock"
        )

        # Assert
        assert result is not None
        assert "not in locked state" in result

    def test_validate_state_transition_hero_unlock_valid(self) -> None:
        """Test valid hero unlock transition."""
        # Arrange
        hero = Hero(faction=Faction.ARBOREC, player_id="player1")

        # Act
        result = LeaderAbilityValidator.validate_state_transition(
            hero, "locked", "unlocked", "unlock"
        )

        # Assert
        assert result is None

    def test_validate_state_transition_hero_unlock_purged(self) -> None:
        """Test invalid hero unlock transition (purged)."""
        # Arrange
        hero = Hero(faction=Faction.ARBOREC, player_id="player1")
        hero.unlock()
        hero.purge()  # Purged

        # Act
        result = LeaderAbilityValidator.validate_state_transition(
            hero, "purged", "unlocked", "unlock"
        )

        # Assert
        assert result is not None
        assert "hero has been purged" in result

    def test_validate_state_transition_hero_purge_valid(self) -> None:
        """Test valid hero purge transition."""
        # Arrange
        hero = Hero(faction=Faction.ARBOREC, player_id="player1")
        hero.unlock()

        # Act
        result = LeaderAbilityValidator.validate_state_transition(
            hero, "unlocked", "purged", "purge"
        )

        # Assert
        assert result is None

    def test_validate_state_transition_hero_purge_invalid(self) -> None:
        """Test invalid hero purge transition (already purged)."""
        # Arrange
        hero = Hero(faction=Faction.ARBOREC, player_id="player1")
        hero.unlock()
        hero.purge()  # Already purged

        # Act
        result = LeaderAbilityValidator.validate_state_transition(
            hero, "purged", "purged", "purge"
        )

        # Assert
        assert result is not None
        assert "already purged" in result


class TestLeaderAbilityValidatorComprehensive:
    """Test cases for comprehensive validation in LeaderAbilityValidator.

    Tests comprehensive validation that collects all errors.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 9.1, 9.2, 9.3, 9.4, 9.5
    """

    def test_validate_comprehensive_prerequisites_all_valid(self) -> None:
        """Test comprehensive validation when all prerequisites are met."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        player = Mock(spec=Player)
        player.id = "player1"
        game_state = Mock(spec=GameState)
        game_state.phase = GamePhase.ACTION
        game_state.players = [player]

        # Act
        errors = LeaderAbilityValidator.validate_comprehensive_prerequisites(
            agent, game_state
        )

        # Assert
        assert len(errors) == 0

    def test_validate_comprehensive_prerequisites_multiple_errors(self) -> None:
        """Test comprehensive validation with multiple validation failures."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        agent.exhaust()  # Make exhausted (state error)

        player = Mock(spec=Player)
        player.id = "player1"
        player.trade_goods = 1  # Insufficient for cost (resource error)

        game_state = Mock(spec=GameState)
        game_state.phase = None  # No phase (timing error)
        game_state.players = [player]

        # Act
        errors = LeaderAbilityValidator.validate_comprehensive_prerequisites(
            agent,
            game_state,
            trade_goods_cost=5,  # More than player has
            target_player="nonexistent",  # Invalid target
        )

        # Assert
        assert (
            len(errors) >= 3
        )  # Should have state, timing, resource, and target errors
        error_text = " ".join(errors)
        assert "exhausted" in error_text
        assert "game phase" in error_text
        assert "trade goods" in error_text
        assert "does not exist" in error_text

    def test_validate_comprehensive_prerequisites_single_error(self) -> None:
        """Test comprehensive validation with single validation failure."""
        # Arrange
        commander = Commander(faction=Faction.ARBOREC, player_id="player1")
        # Commander starts locked (state error)

        player = Mock(spec=Player)
        player.id = "player1"
        game_state = Mock(spec=GameState)
        game_state.phase = GamePhase.ACTION
        game_state.players = [player]

        # Act
        errors = LeaderAbilityValidator.validate_comprehensive_prerequisites(
            commander, game_state
        )

        # Assert
        assert len(errors) == 1
        assert "locked" in errors[0]


class TestLeaderAbilityValidatorEdgeCases:
    """Test cases for edge case validation in LeaderAbilityValidator.

    Tests validation of unusual scenarios and edge cases.

    LRR References:
    - Rule 51: LEADERS
    - Requirements 9.1, 9.2, 9.3, 9.4, 9.5
    """

    def test_validate_edge_cases_none_leader(self) -> None:
        """Test edge case validation with None leader."""
        # Arrange
        game_state = Mock(spec=GameState)

        # Act
        result = LeaderAbilityValidator.validate_edge_cases(None, game_state)

        # Assert
        assert result is not None
        assert "Leader cannot be None" in result

    def test_validate_edge_cases_none_game_state(self) -> None:
        """Test edge case validation with None game state."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")

        # Act
        result = LeaderAbilityValidator.validate_edge_cases(agent, None)

        # Assert
        assert result is not None
        assert "Game state cannot be None" in result

    def test_validate_edge_cases_invalid_leader_object(self) -> None:
        """Test edge case validation with invalid leader object."""

        # Arrange
        class InvalidLeader:
            pass  # No get_leader_type method

        invalid_leader = InvalidLeader()
        game_state = Mock(spec=GameState)

        # Act
        result = LeaderAbilityValidator.validate_edge_cases(invalid_leader, game_state)

        # Assert
        assert result is not None
        assert "missing get_leader_type method" in result

    def test_validate_edge_cases_invalid_leader_type(self) -> None:
        """Test edge case validation with invalid leader type."""
        # Arrange
        invalid_leader = Mock()
        invalid_leader.get_leader_type.return_value = "INVALID_TYPE"
        invalid_leader.player_id = "player1"
        game_state = Mock(spec=GameState)
        game_state.players = []

        # Act
        result = LeaderAbilityValidator.validate_edge_cases(invalid_leader, game_state)

        # Assert
        assert result is not None
        assert "Invalid leader type" in result

    def test_validate_edge_cases_missing_player_id(self) -> None:
        """Test edge case validation with missing player_id."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        agent.player_id = ""  # Empty player_id
        game_state = Mock(spec=GameState)

        # Act
        result = LeaderAbilityValidator.validate_edge_cases(agent, game_state)

        # Assert
        assert result is not None
        assert "valid player_id" in result

    def test_validate_edge_cases_player_not_in_game_state(self) -> None:
        """Test edge case validation when player not in game state."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        game_state = Mock(spec=GameState)
        game_state.players = []  # No players

        # Act
        result = LeaderAbilityValidator.validate_edge_cases(agent, game_state)

        # Assert
        assert result is not None
        assert "not found in game state" in result

    def test_validate_edge_cases_agent_invalid_lock_status(self) -> None:
        """Test edge case validation for agent with invalid lock status."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        agent.lock_status = LeaderLockStatus.LOCKED  # Invalid for agent

        player = Mock(spec=Player)
        player.id = "player1"
        game_state = Mock(spec=GameState)
        game_state.players = [player]

        # Act
        result = LeaderAbilityValidator.validate_edge_cases(agent, game_state)

        # Assert
        assert result is not None
        assert "invalid lock status" in result

    def test_validate_edge_cases_commander_with_ready_status(self) -> None:
        """Test edge case validation for commander with invalid ready status."""
        # Arrange
        commander = Commander(faction=Faction.ARBOREC, player_id="player1")
        commander.ready_status = LeaderReadyStatus.READIED  # Invalid for commander

        player = Mock(spec=Player)
        player.id = "player1"
        game_state = Mock(spec=GameState)
        game_state.players = [player]

        # Act
        result = LeaderAbilityValidator.validate_edge_cases(commander, game_state)

        # Assert
        assert result is not None
        assert "should not have ready_status" in result

    def test_validate_edge_cases_valid_agent(self) -> None:
        """Test edge case validation for valid agent."""
        # Arrange
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")

        player = Mock(spec=Player)
        player.id = "player1"
        game_state = Mock(spec=GameState)
        game_state.players = [player]

        # Act
        result = LeaderAbilityValidator.validate_edge_cases(agent, game_state)

        # Assert
        assert result is None

    def test_validate_edge_cases_valid_commander(self) -> None:
        """Test edge case validation for valid commander."""
        # Arrange
        commander = Commander(faction=Faction.ARBOREC, player_id="player1")

        player = Mock(spec=Player)
        player.id = "player1"
        game_state = Mock(spec=GameState)
        game_state.players = [player]

        # Act
        result = LeaderAbilityValidator.validate_edge_cases(commander, game_state)

        # Assert
        assert result is None

    def test_validate_edge_cases_valid_hero(self) -> None:
        """Test edge case validation for valid hero."""
        # Arrange
        hero = Hero(faction=Faction.ARBOREC, player_id="player1")

        player = Mock(spec=Player)
        player.id = "player1"
        game_state = Mock(spec=GameState)
        game_state.players = [player]

        # Act
        result = LeaderAbilityValidator.validate_edge_cases(hero, game_state)

        # Assert
        assert result is None

"""Integration tests for leader abilities with game systems.

This module tests the integration of leader abilities with various game systems
including combat, resource management, movement, and other core mechanics.

LRR References:
- Rule 51: LEADERS
- Requirements 10.1, 10.2, 10.3, 10.4, 10.5

Test Categories:
- Combat system integration
- Resource management integration
- Movement system integration
- Cross-system leader effects
- System interaction validation
"""

from unittest.mock import Mock

from src.ti4.core.constants import Faction, UnitType
from src.ti4.core.game_state import GameState
from src.ti4.core.leaders import (
    LeaderLockStatus,
    LeaderManager,
)
from src.ti4.core.placeholder_leaders import (
    ConditionalTargetAgent,
    PowerfulHero,
    SimpleResourceAgent,
    UnlockableCommander,
)
from src.ti4.core.player import Player
from src.ti4.core.system import System
from src.ti4.core.unit import Unit


class TestCombatSystemIntegration:
    """Test leader ability integration with the combat system.

    Validates that leader abilities can properly integrate with combat mechanics,
    modify combat values, and interact with combat phases.

    Requirements: 10.1
    """

    def test_agent_ability_modifies_combat_values(self):
        """Test that agent abilities can modify combat values during combat.

        RED: Create failing test for agent combat modification
        """
        # Arrange
        game_state = Mock(spec=GameState)
        player = Mock(spec=Player)
        player.id = "player1"
        player.faction = Faction.ARBOREC

        # Create a combat-modifying agent
        agent = SimpleResourceAgent(faction=Faction.ARBOREC, player_id="player1")

        # Mock combat system
        combat_manager = Mock()
        game_state.combat_manager = combat_manager

        # Act & Assert - This should fail initially
        result = agent.execute_ability(game_state, combat_modifier=True)

        # This assertion will fail until we implement combat integration
        assert result.success is True
        assert "combat" in str(result.effects).lower()

    def test_commander_provides_ongoing_combat_bonus(self):
        """Test that unlocked commanders provide ongoing combat bonuses.

        RED: Create failing test for commander combat bonus
        """
        # Arrange
        game_state = Mock(spec=GameState)
        commander = UnlockableCommander(faction=Faction.ARBOREC, player_id="player1")
        commander.unlock()  # Unlock the commander

        # Mock combat scenario
        combat_system = Mock()
        game_state.combat_system = combat_system

        # Act
        result = commander.execute_ability(game_state, combat_context=True)

        # Assert - This should fail until we implement ongoing effects
        assert result.success is True
        assert result.game_state_changes is not None
        assert (
            "combat" in str(result.effects).lower()
            or "bonus" in str(result.effects).lower()
        )

    def test_hero_ability_affects_multiple_combat_units(self):
        """Test that hero abilities can affect multiple units in combat.

        RED: Create failing test for hero multi-unit effects
        """
        # Arrange
        game_state = Mock(spec=GameState)
        hero = PowerfulHero(faction=Faction.ARBOREC, player_id="player1")
        hero.unlock()  # Unlock the hero

        # Mock units in combat
        units = [
            Mock(spec=Unit, unit_type=UnitType.FIGHTER, owner="player1"),
            Mock(spec=Unit, unit_type=UnitType.CRUISER, owner="player1"),
            Mock(spec=Unit, unit_type=UnitType.DREADNOUGHT, owner="player1"),
        ]

        system = Mock(spec=System)
        system.space_units = units
        game_state.get_system = Mock(return_value=system)

        # Act
        result = hero.execute_ability(
            game_state, target_system="system1", affect_all_units=True
        )

        # Assert - This should fail until we implement multi-unit effects
        assert result.success is True
        assert (
            "ships" in str(result.effects).lower()
            or "combat" in str(result.effects).lower()
        )
        assert (
            hero.lock_status == LeaderLockStatus.PURGED
        )  # Hero should be purged after use

    def test_leader_ability_timing_during_combat_phases(self):
        """Test that leader abilities respect combat phase timing restrictions.

        RED: Create failing test for combat timing validation
        """
        # Arrange
        game_state = Mock(spec=GameState)
        game_state.current_phase = "combat"
        game_state.combat_step = "assign_hits"

        agent = ConditionalTargetAgent(faction=Faction.ARBOREC, player_id="player1")

        # Act
        result = agent.execute_ability(
            game_state,
            target="enemy_ship",
            timing_window="before_dice_roll",
            override_round_check=True,  # Override round check for testing
        )

        # Assert - This should fail until we implement timing validation
        assert result.success is False
        assert "timing" in result.error_message.lower()


class TestResourceManagementIntegration:
    """Test leader ability integration with resource management systems.

    Validates that leader abilities can generate resources, modify production,
    and interact with trade goods and other economic mechanics.

    Requirements: 10.2
    """

    def test_agent_generates_trade_goods(self):
        """Test that agent abilities can generate trade goods.

        GREEN: Implement basic resource generation
        """
        # Arrange
        game_state = Mock(spec=GameState)
        player = Mock(spec=Player)
        player.id = "player1"
        player.trade_goods = 5

        game_state.get_player = Mock(return_value=player)

        agent = SimpleResourceAgent(faction=Faction.ARBOREC, player_id="player1")

        # Act
        result = agent.execute_ability(game_state)

        # Assert
        assert result.success is True
        assert result.game_state_changes is not None
        assert result.game_state_changes.get("trade_goods_gained") == 1

    def test_commander_modifies_resource_production(self):
        """Test that commander abilities can modify resource production.

        RED: Create failing test for production modification
        """
        # Arrange
        game_state = Mock(spec=GameState)
        player = Mock(spec=Player)
        player.id = "player1"
        player.controlled_planets = 4  # Meets unlock condition
        player.trade_goods = 6  # Meets unlock condition

        game_state.get_player = Mock(return_value=player)

        commander = UnlockableCommander(faction=Faction.ARBOREC, player_id="player1")

        # Check unlock conditions and unlock if met
        if commander.check_unlock_conditions(game_state):
            commander.unlock()

        # Mock production system
        production_manager = Mock()
        game_state.production_manager = production_manager

        # Act
        result = commander.execute_ability(game_state, production_context=True)

        # Assert - This should fail until we implement production integration
        assert result.success is True
        assert (
            "resource" in str(result.effects).lower()
            or "production" in str(result.effects).lower()
        )

    def test_hero_provides_massive_resource_gain(self):
        """Test that hero abilities can provide significant resource benefits.

        GREEN: Implement hero resource effects using existing placeholder
        """
        # Arrange
        game_state = Mock(spec=GameState)
        player = Mock(spec=Player)
        player.id = "player1"
        player.controls_mecatol_rex = True
        player.completed_objectives = 3
        player.victory_points = 12

        game_state.get_player = Mock(return_value=player)

        hero = PowerfulHero(faction=Faction.ARBOREC, player_id="player1")

        # Check unlock conditions and unlock if met
        if hero.check_unlock_conditions(game_state):
            hero.unlock()

        # Act
        result = hero.execute_ability(game_state)

        # Assert
        assert result.success is True
        assert result.game_state_changes is not None
        # Hero should provide multiple resource benefits
        assert result.game_state_changes.get("trade_goods_gained") == 5
        assert result.game_state_changes.get("command_tokens_gained") == 3
        assert hero.lock_status == LeaderLockStatus.PURGED

    def test_leader_ability_validates_resource_costs(self):
        """Test that leader abilities validate resource costs before execution.

        RED: Create failing test for resource cost validation
        """
        # Arrange
        game_state = Mock(spec=GameState)
        player = Mock(spec=Player)
        player.id = "player1"
        player.trade_goods = 2  # Insufficient resources

        game_state.get_player = Mock(return_value=player)

        agent = ConditionalTargetAgent(faction=Faction.ARBOREC, player_id="player1")

        # Act
        result = agent.execute_ability(
            game_state,
            target="planet_a",
            resource_cost=5,  # Requires more than player has
            override_round_check=True,  # Override round check for testing
        )

        # Assert - This should fail until we implement cost validation
        assert result.success is False
        assert (
            "resource" in result.error_message.lower()
            or "cost" in result.error_message.lower()
        )


class TestMovementSystemIntegration:
    """Test leader ability integration with movement systems.

    Validates that leader abilities can modify movement values, enable special
    movement, and interact with transport and fleet mechanics.

    Requirements: 10.3
    """

    def test_agent_provides_movement_bonus(self):
        """Test that agent abilities can provide movement bonuses.

        RED: Create failing test for movement modification
        """
        # Arrange
        game_state = Mock(spec=GameState)
        player = Mock(spec=Player)
        player.id = "player1"

        game_state.get_player = Mock(return_value=player)

        agent = SimpleResourceAgent(faction=Faction.ARBOREC, player_id="player1")

        # Mock movement system
        movement_manager = Mock()
        game_state.movement_manager = movement_manager

        # Act
        result = agent.execute_ability(game_state, movement_bonus=True)

        # Assert - This should fail until we implement movement integration
        assert result.success is True
        assert (
            "movement" in str(result.effects).lower()
            or "move" in str(result.effects).lower()
        )

    def test_commander_enables_special_movement(self):
        """Test that commander abilities can enable special movement rules.

        RED: Create failing test for special movement
        """
        # Arrange
        game_state = Mock(spec=GameState)
        player = Mock(spec=Player)
        player.id = "player1"
        player.controlled_planets = 4
        player.trade_goods = 6

        game_state.get_player = Mock(return_value=player)

        commander = UnlockableCommander(faction=Faction.ARBOREC, player_id="player1")

        if commander.check_unlock_conditions(game_state):
            commander.unlock()

        # Mock fleet with units
        units = [Mock(spec=Unit, unit_type=UnitType.CRUISER, owner="player1")]

        # Act
        result = commander.execute_ability(
            game_state, special_movement=True, target_units=units
        )

        # Assert - This should fail until we implement special movement
        assert result.success is True
        assert (
            commander.lock_status == LeaderLockStatus.UNLOCKED
        )  # Commander stays unlocked

    def test_hero_enables_massive_fleet_movement(self):
        """Test that hero abilities can enable large-scale fleet movement.

        RED: Create failing test for fleet movement
        """
        # Arrange
        game_state = Mock(spec=GameState)
        player = Mock(spec=Player)
        player.id = "player1"
        player.controls_mecatol_rex = True
        player.completed_objectives = 2
        player.victory_points = 10

        game_state.get_player = Mock(return_value=player)

        hero = PowerfulHero(faction=Faction.ARBOREC, player_id="player1")

        if hero.check_unlock_conditions(game_state):
            hero.unlock()

        # Mock large fleet
        fleet_units = [
            Mock(spec=Unit, unit_type=UnitType.DREADNOUGHT, owner="player1"),
            Mock(spec=Unit, unit_type=UnitType.CRUISER, owner="player1"),
            Mock(spec=Unit, unit_type=UnitType.FIGHTER, owner="player1"),
            Mock(spec=Unit, unit_type=UnitType.FIGHTER, owner="player1"),
        ]

        # Act
        result = hero.execute_ability(
            game_state, fleet_movement=True, target_fleet=fleet_units
        )

        # Assert - This should fail until we implement fleet movement
        assert result.success is True
        assert len(fleet_units) > 0  # Ensure we're testing with actual units
        assert hero.lock_status == LeaderLockStatus.PURGED

    def test_leader_ability_respects_movement_restrictions(self):
        """Test that leader abilities respect movement restrictions and anomalies.

        RED: Create failing test for movement restrictions
        """
        # Arrange
        game_state = Mock(spec=GameState)

        # Mock system with anomaly that restricts movement
        system = Mock(spec=System)
        system.has_anomaly = Mock(return_value=True)
        system.anomaly_type = "nebula"

        game_state.get_system = Mock(return_value=system)

        agent = ConditionalTargetAgent(faction=Faction.ARBOREC, player_id="player1")

        # Act
        result = agent.execute_ability(
            game_state,
            target="restricted_system",
            movement_through_anomaly=True,
            override_round_check=True,  # Override round check for testing
        )

        # Assert - This should fail until we implement restriction validation
        assert result.success is False
        assert (
            "restricted" in result.error_message.lower()
            or "anomaly" in result.error_message.lower()
        )


class TestCrossSystemLeaderEffects:
    """Test leader abilities that affect multiple game systems simultaneously.

    Validates complex leader abilities that interact with multiple systems
    and coordinate effects across different game mechanics.

    Requirements: 10.4, 10.5
    """

    def test_hero_affects_combat_and_resources_simultaneously(self):
        """Test hero ability that affects both combat and resource systems.

        GREEN: Use existing PowerfulHero implementation that affects multiple systems
        """
        # Arrange
        game_state = Mock(spec=GameState)
        player = Mock(spec=Player)
        player.id = "player1"
        player.controls_mecatol_rex = True
        player.completed_objectives = 2
        player.victory_points = 10

        game_state.get_player = Mock(return_value=player)

        hero = PowerfulHero(faction=Faction.ARBOREC, player_id="player1")

        if hero.check_unlock_conditions(game_state):
            hero.unlock()

        # Act
        result = hero.execute_ability(game_state)

        # Assert - PowerfulHero affects multiple systems
        assert result.success is True
        assert result.game_state_changes is not None

        # Check multiple system effects
        changes = result.game_state_changes
        assert changes.get("trade_goods_gained") == 5  # Resource system
        assert changes.get("command_tokens_gained") == 3  # Command system
        assert changes.get("combat_bonus_active") is True  # Combat system
        assert changes.get("action_cards_drawn") == 2  # Card system

        assert hero.lock_status == LeaderLockStatus.PURGED

    def test_commander_provides_ongoing_multi_system_benefits(self):
        """Test commander ability that provides ongoing benefits to multiple systems.

        RED: Create failing test for multi-system ongoing effects
        """
        # Arrange
        game_state = Mock(spec=GameState)
        player = Mock(spec=Player)
        player.id = "player1"
        player.controlled_planets = 4
        player.trade_goods = 6

        game_state.get_player = Mock(return_value=player)

        commander = UnlockableCommander(faction=Faction.ARBOREC, player_id="player1")

        if commander.check_unlock_conditions(game_state):
            commander.unlock()

        # Mock multiple systems
        production_manager = Mock()
        combat_manager = Mock()
        movement_manager = Mock()

        game_state.production_manager = production_manager
        game_state.combat_manager = combat_manager
        game_state.movement_manager = movement_manager

        # Act
        result = commander.execute_ability(game_state, multi_system_effect=True)

        # Assert - This should fail until we implement multi-system effects
        assert result.success is True
        assert result.game_state_changes is not None

        # Should affect multiple systems
        changes = result.game_state_changes
        assert "ongoing_effect" in changes
        assert commander.lock_status == LeaderLockStatus.UNLOCKED  # Stays unlocked

    def test_agent_ability_chains_with_other_systems(self):
        """Test agent ability that triggers effects in other game systems.

        RED: Create failing test for system chaining
        """
        # Arrange
        game_state = Mock(spec=GameState)

        agent = ConditionalTargetAgent(faction=Faction.ARBOREC, player_id="player1")

        # Mock systems that should be triggered
        technology_manager = Mock()
        objective_manager = Mock()

        game_state.technology_manager = technology_manager
        game_state.objective_manager = objective_manager

        # Act
        result = agent.execute_ability(
            game_state,
            target="planet_a",
            chain_effects=True,
            override_round_check=True,  # Override round check for testing
        )

        # Assert - This should fail until we implement chaining
        assert result.success is True
        assert result.game_state_changes is not None

        # Should trigger effects in other systems
        changes = result.game_state_changes
        assert "chain_triggered" in str(changes) or "secondary_effect" in str(changes)

    def test_leader_manager_coordinates_cross_system_effects(self):
        """Test that LeaderManager properly coordinates effects across systems.

        RED: Create failing test for manager coordination
        """
        # Arrange
        game_state = Mock(spec=GameState)
        game_state.current_phase = "action"  # Provide a valid phase

        # Mock player with leaders
        player = Mock(spec=Player)
        player.id = "player1"

        # Create leaders with cross-system effects
        agent = SimpleResourceAgent(faction=Faction.ARBOREC, player_id="player1")
        commander = UnlockableCommander(faction=Faction.ARBOREC, player_id="player1")
        commander.unlock()

        # Create proper leader sheet mock
        from src.ti4.core.leaders import LeaderSheet

        leader_sheet = LeaderSheet(player_id="player1")
        leader_sheet.set_agent(agent)
        leader_sheet.set_commander(commander)

        player.leader_sheet = leader_sheet
        player.leaders = [agent, commander]

        # Mock the players list for LeaderManager
        game_state.players = [player]
        game_state.get_player = Mock(return_value=player)

        leader_manager = LeaderManager(game_state)

        # Act
        result = leader_manager.execute_leader_ability(
            "player1", "Simple Resource Agent", coordinate_effects=True
        )

        # Assert - This should fail until we implement coordination
        assert result.success is True
        assert result.game_state_changes is not None

    def test_multiple_leader_abilities_interact_correctly(self):
        """Test that multiple leader abilities can interact without conflicts.

        RED: Create failing test for ability interaction
        """
        # Arrange
        game_state = Mock(spec=GameState)

        # Create multiple leaders for the same player
        agent = SimpleResourceAgent(faction=Faction.ARBOREC, player_id="player1")
        commander = UnlockableCommander(faction=Faction.ARBOREC, player_id="player1")
        commander.unlock()

        # Act - Use both abilities in sequence
        agent_result = agent.execute_ability(game_state)
        commander_result = commander.execute_ability(game_state, stack_with_agent=True)

        # Assert - This should fail until we implement stacking
        assert agent_result.success is True
        assert commander_result.success is True

        # Effects should stack or interact properly
        assert agent_result.game_state_changes is not None
        assert commander_result.game_state_changes is not None


class TestSystemInteractionValidation:
    """Test validation of leader ability interactions with game systems.

    Validates that leader abilities properly validate their interactions
    with other systems and handle edge cases correctly.

    Requirements: 10.5
    """

    def test_leader_ability_validates_system_availability(self):
        """Test that leader abilities validate required systems are available.

        RED: Create failing test for system availability validation
        """
        # Arrange
        game_state = Mock(spec=GameState)

        # Mock missing system
        game_state.combat_manager = None  # Combat system not available

        agent = ConditionalTargetAgent(faction=Faction.ARBOREC, player_id="player1")

        # Act
        result = agent.execute_ability(
            game_state,
            target="planet_a",
            requires_combat=True,
            override_round_check=True,  # Override round check for testing
        )

        # Assert - This should fail until we implement system validation
        assert result.success is False
        assert (
            "system" in result.error_message.lower()
            or "unavailable" in result.error_message.lower()
        )

    def test_leader_ability_handles_system_errors_gracefully(self):
        """Test that leader abilities handle system errors gracefully.

        RED: Create failing test for error handling
        """
        # Arrange
        game_state = Mock(spec=GameState)

        # Mock system that raises errors
        faulty_system = Mock()
        faulty_system.process_effect = Mock(side_effect=Exception("System error"))
        game_state.resource_manager = faulty_system

        agent = SimpleResourceAgent(faction=Faction.ARBOREC, player_id="player1")

        # Act
        result = agent.execute_ability(game_state, use_resource_system=True)

        # Assert - This should fail until we implement error handling
        assert result.success is False
        assert "error" in result.error_message.lower()

    def test_leader_ability_validates_game_state_consistency(self):
        """Test that leader abilities validate game state consistency.

        RED: Create failing test for consistency validation
        """
        # Arrange
        game_state = Mock(spec=GameState)

        # Mock inconsistent game state
        game_state.current_round = 3
        game_state.current_phase = "status"  # Inconsistent with ability timing

        agent = ConditionalTargetAgent(faction=Faction.ARBOREC, player_id="player1")

        # Act
        result = agent.execute_ability(
            game_state,
            target="planet_a",
            requires_action_phase=True,
            override_round_check=True,  # Override round check for testing
        )

        # Assert - This should fail until we implement consistency validation
        assert result.success is False
        assert (
            "phase" in result.error_message.lower()
            or "timing" in result.error_message.lower()
        )

    def test_leader_ability_prevents_invalid_system_modifications(self):
        """Test that leader abilities prevent invalid modifications to game systems.

        RED: Create failing test for modification validation
        """
        # Arrange
        game_state = Mock(spec=GameState)

        hero = PowerfulHero(faction=Faction.ARBOREC, player_id="player1")
        hero.unlock()

        # Act - Try to make invalid modification
        result = hero.execute_ability(
            game_state, invalid_modification=True, modify_locked_system=True
        )

        # Assert - This should fail until we implement modification validation
        assert result.success is False
        assert (
            "invalid" in result.error_message.lower()
            or "locked" in result.error_message.lower()
        )

"""Game state persistence and loading tests for Rule 51: LEADERS.

This module tests that leader states are properly saved and restored,
leader state consistency across game save/load cycles, leader ability
effects persist correctly, and game state integrity with leaders.

LRR References:
- Rule 51: LEADERS
- Requirements 8.2, 8.3

Test Categories:
- Leader state serialization and deserialization
- Leader state consistency across save/load cycles
- Leader ability effects persistence
- Game state integrity with leaders
- Cross-system leader state preservation
"""

import copy

from src.ti4.core.constants import Faction
from src.ti4.core.game_state import GameState
from src.ti4.core.leaders import (
    LeaderLockStatus,
    LeaderManager,
    LeaderReadyStatus,
    LeaderSheet,
)
from src.ti4.core.player import Player


class MockPlayer:
    """Mock player for testing with mutable attributes."""

    def __init__(self, player_id: str, faction: Faction, **kwargs):
        """Initialize mock player with configurable attributes."""
        self.id = player_id
        self.player_id = player_id  # Some code might expect player_id instead of id
        self.faction = faction
        self.controlled_planets = kwargs.get("controlled_planets", 0)
        self.trade_goods = kwargs.get("trade_goods", 0)
        self.controls_mecatol_rex = kwargs.get("controls_mecatol_rex", False)
        self.completed_objectives = kwargs.get("completed_objectives", 0)
        self.victory_points = kwargs.get("victory_points", 0)

        # Initialize leader sheet
        self.leader_sheet = LeaderSheet(player_id=player_id)


def initialize_placeholder_leaders(player: MockPlayer) -> None:
    """Initialize placeholder leaders for testing with meaningful unlock conditions."""
    from src.ti4.core.placeholder_leaders import (
        PowerfulHero,
        SimpleResourceAgent,
        UnlockableCommander,
    )

    # Create placeholder leaders with actual unlock conditions and abilities
    agent = SimpleResourceAgent(faction=player.faction, player_id=player.id)
    commander = UnlockableCommander(faction=player.faction, player_id=player.id)
    hero = PowerfulHero(faction=player.faction, player_id=player.id)

    # Assign them to the leader sheet
    player.leader_sheet.set_agent(agent)
    player.leader_sheet.set_commander(commander)
    player.leader_sheet.set_hero(hero)


class MockGameState:
    """Mock game state for testing with mutable attributes."""

    def __init__(self, **kwargs):
        """Initialize mock game state with configurable attributes."""
        self.phase = kwargs.get(
            "current_phase", "action"
        )  # Use phase, but accept current_phase for backward compatibility
        self.current_round = kwargs.get("current_round", 1)
        self.players = kwargs.get("players", [])

    def get_player(self, player_id: str):
        """Get player by ID."""
        for player in self.players:
            if player.id == player_id:
                return player
        return None


class TestLeaderStateSerialization:
    """Test leader state serialization and deserialization.

    Validates that all leader states can be properly serialized to
    persistent storage and deserialized back to working objects.

    Requirements: 8.2, 8.3
    """

    def test_leader_sheet_serialization_basic(self):
        """Test basic leader sheet serialization.

        RED: This will fail until we implement leader sheet serialization
        """
        # Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        initialize_placeholder_leaders(player)

        leader_sheet = player.leader_sheet

        # Serialize leader sheet
        serialized = leader_sheet.serialize_for_persistence()

        # Should contain all necessary data
        assert isinstance(serialized, dict)
        assert "player_id" in serialized
        assert "agent" in serialized
        assert "commander" in serialized
        assert "hero" in serialized

        # Verify player ID
        assert serialized["player_id"] == "player1"

        # Verify each leader is serialized
        assert serialized["agent"] is not None
        assert serialized["commander"] is not None
        assert serialized["hero"] is not None

    def test_leader_sheet_deserialization_basic(self):
        """Test basic leader sheet deserialization.

        RED: This will fail until we implement leader sheet deserialization
        """
        # Create serialized data
        serialized_data = {
            "player_id": "player1",
            "agent": {
                "faction": "arborec",
                "player_id": "player1",
                "lock_status": "unlocked",
                "ready_status": "readied",
                "leader_type": "agent",
                "name": "Simple Resource Agent",
            },
            "commander": {
                "faction": "arborec",
                "player_id": "player1",
                "lock_status": "locked",
                "ready_status": None,
                "leader_type": "commander",
                "name": "Unlockable Commander",
            },
            "hero": {
                "faction": "arborec",
                "player_id": "player1",
                "lock_status": "locked",
                "ready_status": None,
                "leader_type": "hero",
                "name": "Powerful Hero",
            },
        }

        # Deserialize leader sheet
        leader_sheet = LeaderSheet.from_serialized_data(serialized_data)

        # Verify basic properties
        assert leader_sheet.player_id == "player1"
        assert leader_sheet.is_complete()

        # Verify agent
        agent = leader_sheet.agent
        assert agent is not None
        assert agent.get_name() == "Simple Resource Agent"
        assert agent.lock_status == LeaderLockStatus.UNLOCKED
        assert agent.ready_status == LeaderReadyStatus.READIED

        # Verify commander
        commander = leader_sheet.commander
        assert commander is not None
        assert commander.get_name() == "Unlockable Commander"
        assert commander.lock_status == LeaderLockStatus.LOCKED
        assert commander.ready_status is None

        # Verify hero
        hero = leader_sheet.hero
        assert hero is not None
        assert hero.get_name() == "Powerful Hero"
        assert hero.lock_status == LeaderLockStatus.LOCKED
        assert hero.ready_status is None

    def test_leader_state_serialization_all_states(self):
        """Test serialization of leaders in all possible states.

        RED: This will fail until we implement comprehensive state serialization
        """
        # Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        initialize_placeholder_leaders(player)

        agent = player.leader_sheet.agent
        commander = player.leader_sheet.commander
        hero = player.leader_sheet.hero

        # Set up different states
        agent.exhaust()  # Exhausted agent
        commander.unlock()  # Unlocked commander
        hero.unlock()
        hero.purge()  # Purged hero

        # Serialize
        serialized = player.leader_sheet.serialize_for_persistence()

        # Verify states are preserved
        assert serialized["agent"]["ready_status"] == "exhausted"
        assert serialized["commander"]["lock_status"] == "unlocked"
        assert serialized["hero"]["lock_status"] == "purged"

    def test_leader_ability_effects_serialization(self):
        """Test serialization of leader ability effects and game state changes.

        RED: This will fail until we implement ability effects persistence
        """
        # Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player])
        initialize_placeholder_leaders(player)

        leader_manager = LeaderManager(game_state)

        # Execute agent ability
        agent = player.leader_sheet.agent
        result = leader_manager.execute_leader_ability("player1", agent.get_name())

        assert result.success is True

        # Serialize the game state changes
        serialized_effects = {
            "ability_result": {
                "success": result.success,
                "effects": result.effects,
                "game_state_changes": result.game_state_changes,
            },
            "leader_state": agent.serialize_state(),
        }

        # Verify serialization includes all necessary data
        assert serialized_effects["ability_result"]["success"] is True
        assert len(serialized_effects["ability_result"]["effects"]) > 0
        assert serialized_effects["leader_state"]["ready_status"] == "exhausted"


class TestLeaderStateConsistency:
    """Test leader state consistency across save/load cycles.

    Validates that leader states remain consistent and functional
    after being saved and loaded from persistent storage.

    Requirements: 8.2, 8.3
    """

    def test_agent_ready_exhaust_cycle_persistence(self):
        """Test agent ready/exhaust cycle persists across save/load.

        RED: This will fail until we implement full persistence cycle
        """
        # Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player])
        initialize_placeholder_leaders(player)

        leader_manager = LeaderManager(game_state)
        agent = player.leader_sheet.agent

        # Initial state: readied
        assert agent.ready_status == LeaderReadyStatus.READIED

        # Use ability (should exhaust)
        result = leader_manager.execute_leader_ability("player1", agent.get_name())
        assert result.success is True
        assert agent.ready_status == LeaderReadyStatus.EXHAUSTED

        # Serialize and deserialize
        serialized = player.leader_sheet.serialize_for_persistence()
        restored_sheet = LeaderSheet.from_serialized_data(serialized)

        # Verify exhausted state persisted
        restored_agent = restored_sheet.agent
        assert restored_agent.ready_status == LeaderReadyStatus.EXHAUSTED
        assert not restored_agent.can_use_ability()

        # Ready the agent and test again
        restored_agent.ready()
        assert restored_agent.ready_status == LeaderReadyStatus.READIED
        assert restored_agent.can_use_ability()

        # Serialize and deserialize again
        serialized2 = restored_sheet.serialize_for_persistence()
        restored_sheet2 = LeaderSheet.from_serialized_data(serialized2)

        # Verify readied state persisted
        restored_agent2 = restored_sheet2.agent
        assert restored_agent2.ready_status == LeaderReadyStatus.READIED
        assert restored_agent2.can_use_ability()

    def test_commander_unlock_status_persistence(self):
        """Test commander unlock status persists across save/load.

        RED: This will fail until we implement unlock status persistence
        """
        # Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player])
        initialize_placeholder_leaders(player)

        leader_manager = LeaderManager(game_state)
        commander = player.leader_sheet.commander

        # Initial state: locked
        assert commander.lock_status == LeaderLockStatus.LOCKED
        assert not commander.can_use_ability()

        # Meet unlock conditions and unlock
        player.controlled_planets = 4
        player.trade_goods = 6
        leader_manager.check_unlock_conditions("player1")

        assert commander.lock_status == LeaderLockStatus.UNLOCKED
        assert commander.can_use_ability()

        # Serialize and deserialize
        serialized = player.leader_sheet.serialize_for_persistence()
        restored_sheet = LeaderSheet.from_serialized_data(serialized)

        # Verify unlocked state persisted
        restored_commander = restored_sheet.commander
        assert restored_commander.lock_status == LeaderLockStatus.UNLOCKED
        assert restored_commander.can_use_ability()

        # Use ability multiple times to verify ongoing functionality
        mock_game_state = MockGameState(players=[player])
        restored_manager = LeaderManager(mock_game_state)

        for _i in range(3):
            # Update the player's leader sheet to use the restored one
            player.leader_sheet = restored_sheet
            result = restored_manager.execute_leader_ability(
                "player1", restored_commander.get_name()
            )
            assert result.success is True
            assert restored_commander.lock_status == LeaderLockStatus.UNLOCKED

    def test_hero_purge_status_persistence(self):
        """Test hero purge status persists across save/load.

        RED: This will fail until we implement purge status persistence
        """
        # Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player])
        initialize_placeholder_leaders(player)

        leader_manager = LeaderManager(game_state)
        hero = player.leader_sheet.hero

        # Initial state: locked
        assert hero.lock_status == LeaderLockStatus.LOCKED

        # Unlock hero
        player.controls_mecatol_rex = True
        player.completed_objectives = 3
        player.victory_points = 12
        leader_manager.check_unlock_conditions("player1")

        assert hero.lock_status == LeaderLockStatus.UNLOCKED
        assert hero.can_use_ability()

        # Use hero ability (should purge)
        result = leader_manager.execute_leader_ability("player1", hero.get_name())
        assert result.success is True
        assert hero.lock_status == LeaderLockStatus.PURGED
        assert not hero.can_use_ability()

        # Serialize and deserialize
        serialized = player.leader_sheet.serialize_for_persistence()
        restored_sheet = LeaderSheet.from_serialized_data(serialized)

        # Verify purged state persisted
        restored_hero = restored_sheet.hero
        assert restored_hero.lock_status == LeaderLockStatus.PURGED
        assert not restored_hero.can_use_ability()

        # Verify hero cannot be used after restoration
        player.leader_sheet = restored_sheet
        mock_game_state = MockGameState(players=[player])
        restored_manager = LeaderManager(mock_game_state)

        result = restored_manager.execute_leader_ability(
            "player1", restored_hero.get_name()
        )
        assert result.success is False
        assert "purged" in result.error_message.lower()

    def test_multiple_save_load_cycles_consistency(self):
        """Test consistency across multiple save/load cycles.

        RED: This will fail until we implement robust persistence
        """
        # Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player])
        initialize_placeholder_leaders(player)

        leader_manager = LeaderManager(game_state)

        # Perform multiple operations and save/load cycles
        operations = [
            (
                "use_agent",
                lambda: leader_manager.execute_leader_ability(
                    "player1", player.leader_sheet.agent.get_name()
                ),
            ),
            ("ready_agent", lambda: player.leader_sheet.agent.ready()),
            (
                "unlock_commander",
                lambda: self._unlock_commander(player, leader_manager),
            ),
            (
                "use_commander",
                lambda: leader_manager.execute_leader_ability(
                    "player1", player.leader_sheet.commander.get_name()
                ),
            ),
        ]

        current_sheet = player.leader_sheet

        for i, (operation_name, operation) in enumerate(operations):
            # Perform operation
            if operation_name == "unlock_commander":
                player.controlled_planets = 4
                player.trade_goods = 6
                leader_manager.check_unlock_conditions("player1")
            else:
                operation()

            # Save and load
            serialized = current_sheet.serialize_for_persistence()
            current_sheet = LeaderSheet.from_serialized_data(serialized)
            player.leader_sheet = current_sheet

            # Verify state consistency after each cycle
            if i >= 0:  # After using agent
                if current_sheet.agent.ready_status == LeaderReadyStatus.EXHAUSTED:
                    assert not current_sheet.agent.can_use_ability()
            if i >= 2:  # After unlocking commander
                assert current_sheet.commander.lock_status == LeaderLockStatus.UNLOCKED
                assert current_sheet.commander.can_use_ability()

    def _unlock_commander(
        self, player: MockPlayer, leader_manager: LeaderManager
    ) -> None:
        """Helper method to unlock commander."""
        player.controlled_planets = 4
        player.trade_goods = 6
        leader_manager.check_unlock_conditions("player1")


class TestLeaderAbilityEffectsPersistence:
    """Test that leader ability effects persist correctly.

    Validates that the effects of leader abilities are properly
    preserved across save/load cycles and remain functional.

    Requirements: 8.2, 8.3
    """

    def test_agent_ability_effects_persistence(self):
        """Test that agent ability effects persist across save/load.

        RED: This will fail until we implement ability effects persistence
        """
        # Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player])
        initialize_placeholder_leaders(player)

        leader_manager = LeaderManager(game_state)
        agent = player.leader_sheet.agent

        # Execute agent ability and capture effects
        result = leader_manager.execute_leader_ability("player1", agent.get_name())
        assert result.success is True

        original_effects = result.effects.copy()
        original_changes = (
            copy.deepcopy(result.game_state_changes)
            if result.game_state_changes
            else {}
        )

        # Serialize ability result
        serialized_result = {
            "success": result.success,
            "effects": result.effects,
            "game_state_changes": result.game_state_changes,
        }

        # Deserialize and verify effects are preserved
        restored_effects = serialized_result["effects"]
        restored_changes = serialized_result["game_state_changes"]

        assert restored_effects == original_effects
        assert restored_changes == original_changes

        # Verify the effects are still meaningful
        assert len(restored_effects) > 0
        assert (
            "resource" in restored_effects[0].lower()
            or "trade" in restored_effects[0].lower()
        )

    def test_commander_ongoing_effects_persistence(self):
        """Test that commander ongoing effects persist across save/load.

        RED: This will fail until we implement ongoing effects persistence
        """
        # Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player])
        initialize_placeholder_leaders(player)

        leader_manager = LeaderManager(game_state)
        commander = player.leader_sheet.commander

        # Unlock commander
        player.controlled_planets = 4
        player.trade_goods = 6
        leader_manager.check_unlock_conditions("player1")

        # Execute commander ability multiple times
        results = []
        for _i in range(3):
            result = leader_manager.execute_leader_ability(
                "player1", commander.get_name()
            )
            assert result.success is True
            results.append(result)

        # Serialize all results
        serialized_results = []
        for result in results:
            serialized_results.append(
                {
                    "success": result.success,
                    "effects": result.effects,
                    "game_state_changes": result.game_state_changes,
                }
            )

        # Verify all results are preserved
        assert len(serialized_results) == 3
        for i, serialized in enumerate(serialized_results):
            assert serialized["success"] is True
            assert serialized["effects"] == results[i].effects
            assert serialized["game_state_changes"] == results[i].game_state_changes

    def test_hero_powerful_effects_persistence(self):
        """Test that hero powerful effects persist across save/load.

        RED: This will fail until we implement powerful effects persistence
        """
        # Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player])
        initialize_placeholder_leaders(player)

        leader_manager = LeaderManager(game_state)
        hero = player.leader_sheet.hero

        # Unlock hero
        player.controls_mecatol_rex = True
        player.completed_objectives = 3
        player.victory_points = 12
        leader_manager.check_unlock_conditions("player1")

        # Execute hero ability
        result = leader_manager.execute_leader_ability("player1", hero.get_name())
        assert result.success is True

        # Verify powerful effects
        assert result.game_state_changes is not None
        changes = result.game_state_changes
        assert changes.get("command_tokens_gained") == 3
        assert changes.get("action_cards_drawn") == 2
        assert changes.get("trade_goods_gained") == 5

        # Serialize the powerful effects
        serialized_effects = {
            "hero_ability_used": True,
            "hero_purged": True,
            "effects": result.effects,
            "game_state_changes": result.game_state_changes,
        }

        # Verify serialization preserves all powerful effects
        assert serialized_effects["hero_ability_used"] is True
        assert serialized_effects["hero_purged"] is True
        assert serialized_effects["game_state_changes"]["command_tokens_gained"] == 3
        assert serialized_effects["game_state_changes"]["action_cards_drawn"] == 2
        assert serialized_effects["game_state_changes"]["trade_goods_gained"] == 5


class TestGameStateIntegrityWithLeaders:
    """Test game state integrity with leaders across save/load cycles.

    Validates that the overall game state remains consistent and
    functional when leaders are included in persistence operations.

    Requirements: 8.2, 8.3
    """

    def test_game_state_with_leaders_serialization(self):
        """Test game state serialization includes leader data.

        RED: This will fail until we extend GameState serialization for leaders
        """
        # Create game state with players and leaders
        game_state = GameState()
        player1 = Player("player1", Faction.ARBOREC)
        player2 = Player("player2", Faction.SOL)

        # Add players to game state
        game_state = game_state._create_new_state(players=[player1, player2])

        # Initialize leaders (this would normally be done during game setup)
        from src.ti4.core.leaders import initialize_player_leaders

        initialize_player_leaders(player1)
        initialize_player_leaders(player2)

        # Serialize game state
        serialized = game_state.serialize_for_persistence()

        # Verify leader data is included
        assert "players" in serialized
        assert len(serialized["players"]) == 2

        # Verify each player has leader data
        for player_data in serialized["players"]:
            assert "leader_sheet" in player_data
            leader_sheet_data = player_data["leader_sheet"]
            assert "agent" in leader_sheet_data
            assert "commander" in leader_sheet_data
            assert "hero" in leader_sheet_data

    def test_game_state_with_leaders_deserialization(self):
        """Test game state deserialization restores leader data.

        RED: This will fail until we extend GameState deserialization for leaders
        """
        # Create serialized game state data with leaders
        serialized_data = {
            "game_id": "test-game-123",
            "players": [
                {
                    "id": "player1",
                    "faction": "arborec",
                    "leader_sheet": {
                        "player_id": "player1",
                        "agent": {
                            "faction": "arborec",
                            "player_id": "player1",
                            "lock_status": "unlocked",
                            "ready_status": "readied",
                            "leader_type": "agent",
                            "name": "Agent",
                        },
                        "commander": {
                            "faction": "arborec",
                            "player_id": "player1",
                            "lock_status": "locked",
                            "ready_status": None,
                            "leader_type": "commander",
                            "name": "Commander",
                        },
                        "hero": {
                            "faction": "arborec",
                            "player_id": "player1",
                            "lock_status": "locked",
                            "ready_status": None,
                            "leader_type": "hero",
                            "name": "Hero",
                        },
                    },
                }
            ],
        }

        # Deserialize game state
        restored_state = GameState.from_serialized_state(serialized_data)

        # Verify game state structure
        assert restored_state.game_id == "test-game-123"
        assert len(restored_state.players) == 1

        # Verify player and leader data
        player = restored_state.players[0]
        assert player.id == "player1"
        assert player.leader_sheet.is_complete()

        # Verify leader states
        agent = player.leader_sheet.agent
        commander = player.leader_sheet.commander
        hero = player.leader_sheet.hero

        assert agent.lock_status == LeaderLockStatus.UNLOCKED
        assert agent.ready_status == LeaderReadyStatus.READIED
        assert commander.lock_status == LeaderLockStatus.LOCKED
        assert hero.lock_status == LeaderLockStatus.LOCKED

    def test_game_state_integrity_after_leader_operations(self):
        """Test game state integrity after various leader operations.

        RED: This will fail until we implement comprehensive integrity checks
        """
        # Setup
        game_state = GameState()
        player = Player("player1", Faction.ARBOREC)
        game_state = game_state._create_new_state(players=[player])

        # Initialize leaders
        from src.ti4.core.leaders import initialize_player_leaders

        initialize_player_leaders(player)

        leader_manager = LeaderManager(game_state)

        # Perform various leader operations
        operations = [
            # Use agent ability
            lambda: leader_manager.execute_leader_ability("player1", "Agent"),
            # Ready agent
            lambda: leader_manager.ready_agents("player1"),
            # Check unlock conditions
            lambda: leader_manager.check_unlock_conditions("player1"),
        ]

        for operation in operations:
            # Perform operation
            operation()

            # Serialize and deserialize game state
            serialized = game_state.serialize_for_persistence()
            restored_state = GameState.from_serialized_state(serialized)

            # Verify game state integrity
            assert restored_state.is_valid()
            assert len(restored_state.players) == 1

            restored_player = restored_state.players[0]
            assert restored_player.id == "player1"
            assert restored_player.leader_sheet.is_complete()

    def test_cross_system_leader_state_preservation(self):
        """Test that leader states are preserved across different game systems.

        RED: This will fail until we implement cross-system preservation
        """
        # Setup game state with multiple systems
        game_state = GameState()
        player = Player("player1", Faction.ARBOREC)
        game_state = game_state._create_new_state(players=[player])

        # Initialize leaders
        from src.ti4.core.leaders import initialize_player_leaders

        initialize_player_leaders(player)

        # Simulate interactions with different game systems
        systems_data = {
            "combat_system": {"active_combats": []},
            "movement_system": {"active_movements": []},
            "resource_system": {"resource_pools": {}},
            "objective_system": {"completed_objectives": []},
        }

        # Add systems data to game state (simulate)
        extended_game_state = {**game_state.serialize_for_persistence(), **systems_data}

        # Verify leader data is preserved alongside other systems
        assert "players" in extended_game_state
        player_data = extended_game_state["players"][0]
        assert "leader_sheet" in player_data

        # Verify all systems coexist
        assert "combat_system" in extended_game_state
        assert "movement_system" in extended_game_state
        assert "resource_system" in extended_game_state
        assert "objective_system" in extended_game_state

        # Verify leader data integrity is maintained
        leader_sheet_data = player_data["leader_sheet"]
        assert "agent" in leader_sheet_data
        assert "commander" in leader_sheet_data
        assert "hero" in leader_sheet_data

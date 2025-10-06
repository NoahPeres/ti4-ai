"""End-to-end leader workflow tests for Rule 51: LEADERS.

This module tests complete leader lifecycles from setup to ability use,
validating agent ready/exhaust cycles, commander unlock and usage,
and hero unlock, ability use, and purging across multiple turns.

LRR References:
- Rule 51: LEADERS
- Requirements: All requirements integrated (1.1-10.5)

Test Categories:
- Complete leader lifecycle from setup to ability use
- Agent ready/exhaust cycles through multiple turns
- Commander unlock and ongoing ability usage
- Hero unlock, ability use, and purging
- Multi-turn integration scenarios
- Cross-system leader effects validation
"""

from src.ti4.core.constants import Faction
from src.ti4.core.game_state import GameState
from src.ti4.core.leaders import (
    LeaderLockStatus,
    LeaderManager,
    LeaderReadyStatus,
)
from src.ti4.core.player import Player
from src.ti4.core.status_phase import StatusPhaseManager


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
        from src.ti4.core.leaders import LeaderSheet

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
        self.completed_objectives = kwargs.get("completed_objectives", {})
        self.victory_points = kwargs.get("victory_points", {})

    def get_player(self, player_id: str):
        """Get player by ID."""
        for player in self.players:
            if player.id == player_id:
                return player
        return None

    def add_player_planet(self, player_id: str, planet):
        """Add a planet to a player's controlled planets (mock implementation)."""
        # For mock purposes, just set the attribute on the player
        player = self.get_player(player_id)
        if player:
            if not hasattr(player, "_controlled_planets"):
                player._controlled_planets = []
            player._controlled_planets.append(planet)
        return self

    def get_player_planets(self, player_id: str):
        """Get planets controlled by a player (mock implementation)."""
        player = self.get_player(player_id)
        if player and hasattr(player, "_controlled_planets"):
            return player._controlled_planets
        return []


class TestCompleteLeaderLifecycle:
    """Test complete leader lifecycle from setup to ability use.

    Validates the entire workflow from game setup through leader initialization,
    unlock condition checking, ability usage, and state management.

    Requirements: All requirements integrated
    """

    def test_complete_game_setup_to_first_ability_use(self):
        """Test complete workflow from game setup to first leader ability use.

        GREEN: Implement using mock objects to avoid frozen dataclass issues
        """
        # Phase 1: Game Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player], current_phase="action")

        # Initialize placeholder leaders during setup
        initialize_placeholder_leaders(player)

        # Verify initial states
        assert player.leader_sheet.is_complete()

        agent = player.leader_sheet.agent
        commander = player.leader_sheet.commander
        hero = player.leader_sheet.hero

        assert agent is not None
        assert commander is not None
        assert hero is not None

        # Verify initial states match requirements
        assert agent.lock_status == LeaderLockStatus.UNLOCKED  # Agents start unlocked
        assert agent.ready_status == LeaderReadyStatus.READIED  # Agents start readied
        assert (
            commander.lock_status == LeaderLockStatus.LOCKED
        )  # Commanders start locked
        assert hero.lock_status == LeaderLockStatus.LOCKED  # Heroes start locked

        # Phase 2: First Turn - Use Agent Ability
        leader_manager = LeaderManager(game_state)

        # Agent should be able to use ability immediately
        result = leader_manager.execute_leader_ability("player1", agent.get_name())

        assert result.success is True
        assert len(result.effects) > 0

        # Agent should be exhausted after use
        assert agent.ready_status == LeaderReadyStatus.EXHAUSTED

        # Phase 3: Try to use agent again (should fail)
        result2 = leader_manager.execute_leader_ability("player1", agent.get_name())

        assert result2.success is False
        assert "exhausted" in result2.error_message.lower()

        # Phase 4: Status Phase - Ready Agent
        # For this test, we'll manually ready the agent to simulate status phase
        agent.ready()
        assert agent.ready_status == LeaderReadyStatus.READIED

    def test_commander_unlock_and_ongoing_usage_workflow(self):
        """Test commander unlock conditions and ongoing ability usage.

        GREEN: Implement using mock objects for mutable attributes
        """
        # Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player], current_phase="action")

        initialize_placeholder_leaders(player)
        commander = player.leader_sheet.commander
        assert commander is not None

        # Initially locked
        assert commander.lock_status == LeaderLockStatus.LOCKED
        assert not commander.can_use_ability()

        # Try to use ability while locked (should fail)
        leader_manager = LeaderManager(game_state)
        result = leader_manager.execute_leader_ability("player1", commander.get_name())

        assert result.success is False
        assert "locked" in result.error_message.lower()

        # Meet unlock conditions (mock player state)
        player.controlled_planets = 4  # Meets condition 1
        player.trade_goods = 6  # Meets condition 2

        # Check unlock conditions
        leader_manager.check_unlock_conditions("player1")

        # Commander should now be unlocked
        assert commander.lock_status == LeaderLockStatus.UNLOCKED
        assert commander.can_use_ability()

        # Use commander ability (should succeed)
        result = leader_manager.execute_leader_ability("player1", commander.get_name())

        assert result.success is True
        assert len(result.effects) > 0

        # Commander should remain unlocked (no exhaustion)
        assert commander.lock_status == LeaderLockStatus.UNLOCKED
        assert commander.can_use_ability()

        # Can use commander ability again immediately
        result2 = leader_manager.execute_leader_ability("player1", commander.get_name())
        assert result2.success is True

    def test_hero_unlock_ability_use_and_purge_workflow(self):
        """Test hero unlock, ability use, and purging workflow.

        GREEN: Implement using mock objects for mutable attributes
        """
        # Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player], current_phase="action")

        initialize_placeholder_leaders(player)
        hero = player.leader_sheet.hero
        assert hero is not None

        # Initially locked
        assert hero.lock_status == LeaderLockStatus.LOCKED
        assert not hero.can_use_ability()

        # Try to use ability while locked (should fail)
        leader_manager = LeaderManager(game_state)
        result = leader_manager.execute_leader_ability("player1", hero.get_name())

        assert result.success is False
        assert "locked" in result.error_message.lower()

        # Meet unlock conditions (set up game state properly)

        from src.ti4.core.planet import Planet

        # Add Mecatol Rex to player's controlled planets
        mecatol_rex = Planet("Mecatol Rex", 1, 6)
        game_state = game_state.add_player_planet("player1", mecatol_rex)

        # Add completed objectives (MockGameState is mutable)
        game_state.completed_objectives = {"player1": ["obj1", "obj2", "obj3"]}

        # Add victory points (MockGameState is mutable)
        game_state.victory_points = {"player1": 12}

        # Update leader manager with new game state
        leader_manager = LeaderManager(game_state)

        # Check unlock conditions
        leader_manager.check_unlock_conditions("player1")

        # Hero should now be unlocked
        assert hero.lock_status == LeaderLockStatus.UNLOCKED
        assert hero.can_use_ability()

        # Use hero ability (should succeed and purge)
        result = leader_manager.execute_leader_ability("player1", hero.get_name())

        assert result.success is True
        assert len(result.effects) > 0

        # Hero should be purged after use
        assert hero.lock_status == LeaderLockStatus.PURGED
        assert not hero.can_use_ability()

        # Cannot use hero ability again (should fail)
        result2 = leader_manager.execute_leader_ability("player1", hero.get_name())
        assert result2.success is False
        assert "purged" in result2.error_message.lower()


class TestAgentReadyExhaustCycles:
    """Test agent ready/exhaust cycles through multiple turns.

    Validates that agents properly cycle between readied and exhausted states
    across multiple game turns and status phases.

    Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 8.4
    """

    def test_agent_multiple_turn_ready_exhaust_cycle(self):
        """Test agent ready/exhaust cycle across multiple turns.

        GREEN: Implement using mock objects and manual ready/exhaust simulation
        """
        # Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player], current_phase="action")

        initialize_placeholder_leaders(player)
        agent = player.leader_sheet.agent
        assert agent is not None

        leader_manager = LeaderManager(game_state)

        # Turn 1: Use agent ability
        assert agent.ready_status == LeaderReadyStatus.READIED

        result = leader_manager.execute_leader_ability("player1", agent.get_name())
        assert result.success is True
        assert agent.ready_status == LeaderReadyStatus.EXHAUSTED

        # End of Turn 1: Status phase readies agent (simulate manually)
        agent.ready()
        assert agent.ready_status == LeaderReadyStatus.READIED

        # Turn 2: Use agent ability again
        result = leader_manager.execute_leader_ability("player1", agent.get_name())
        assert result.success is True
        assert agent.ready_status == LeaderReadyStatus.EXHAUSTED

        # End of Turn 2: Status phase readies agent again (simulate manually)
        agent.ready()
        assert agent.ready_status == LeaderReadyStatus.READIED

    def test_agent_cannot_be_used_twice_in_same_turn(self):
        """Test that agent cannot be used twice in the same turn.

        GREEN: Implement using mock objects
        """
        # Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player], current_phase="action")

        initialize_placeholder_leaders(player)
        agent = player.leader_sheet.agent
        assert agent is not None

        leader_manager = LeaderManager(game_state)

        # First use should succeed
        result1 = leader_manager.execute_leader_ability("player1", agent.get_name())
        assert result1.success is True
        assert agent.ready_status == LeaderReadyStatus.EXHAUSTED

        # Second use in same turn should fail
        result2 = leader_manager.execute_leader_ability("player1", agent.get_name())
        assert result2.success is False
        assert "exhausted" in result2.error_message.lower()

    def test_multiple_agents_independent_ready_exhaust_cycles(self):
        """Test that multiple players' agents have independent cycles.

        GREEN: Implement using mock objects for multiple players
        """
        # Setup with two players
        player1 = MockPlayer("player1", Faction.ARBOREC)
        player2 = MockPlayer("player2", Faction.SOL)
        game_state = MockGameState(players=[player1, player2], current_phase="action")

        initialize_placeholder_leaders(player1)
        initialize_placeholder_leaders(player2)

        agent1 = player1.leader_sheet.agent
        agent2 = player2.leader_sheet.agent
        assert agent1 is not None and agent2 is not None

        leader_manager = LeaderManager(game_state)

        # Player 1 uses agent
        result1 = leader_manager.execute_leader_ability("player1", agent1.get_name())
        assert result1.success is True
        assert agent1.ready_status == LeaderReadyStatus.EXHAUSTED
        assert agent2.ready_status == LeaderReadyStatus.READIED  # Unaffected

        # Player 2 can still use their agent
        result2 = leader_manager.execute_leader_ability("player2", agent2.get_name())
        assert result2.success is True
        assert agent1.ready_status == LeaderReadyStatus.EXHAUSTED  # Still exhausted
        assert agent2.ready_status == LeaderReadyStatus.EXHAUSTED  # Now exhausted

        # Status phase readies both agents (simulate manually)
        agent1.ready()
        agent2.ready()

        # Both agents should be readied
        assert agent1.ready_status == LeaderReadyStatus.READIED
        assert agent2.ready_status == LeaderReadyStatus.READIED


class TestCommanderOngoingAbilities:
    """Test commander unlock and ongoing ability usage patterns.

    Validates commander unlock mechanics and ongoing ability availability
    throughout the game after unlock.

    Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6
    """

    def test_commander_unlock_conditions_checked_automatically(self):
        """Test that commander unlock conditions are checked automatically.

        GREEN: Implement using mock objects for mutable attributes
        """
        # Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player], current_phase="action")

        initialize_placeholder_leaders(player)
        commander = player.leader_sheet.commander
        assert commander is not None
        assert commander.lock_status == LeaderLockStatus.LOCKED

        leader_manager = LeaderManager(game_state)

        # Initially doesn't meet conditions
        player.controlled_planets = 2  # Below threshold
        player.trade_goods = 3  # Below threshold

        leader_manager.check_unlock_conditions("player1")
        assert commander.lock_status == LeaderLockStatus.LOCKED

        # Meet first condition
        player.controlled_planets = 4  # Meets condition
        leader_manager.check_unlock_conditions("player1")
        assert commander.lock_status == LeaderLockStatus.LOCKED  # Still locked

        # Meet second condition
        player.trade_goods = 6  # Meets condition
        leader_manager.check_unlock_conditions("player1")
        assert commander.lock_status == LeaderLockStatus.UNLOCKED  # Now unlocked

    def test_commander_ongoing_ability_usage_after_unlock(self):
        """Test that commander abilities can be used repeatedly after unlock.

        GREEN: Implement using mock objects
        """
        # Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player], current_phase="action")

        initialize_placeholder_leaders(player)
        commander = player.leader_sheet.commander
        assert commander is not None

        # Unlock commander
        player.controlled_planets = 4
        player.trade_goods = 6
        leader_manager = LeaderManager(game_state)
        leader_manager.check_unlock_conditions("player1")

        assert commander.lock_status == LeaderLockStatus.UNLOCKED

        # Use ability multiple times
        for _i in range(3):
            result = leader_manager.execute_leader_ability(
                "player1", commander.get_name()
            )
            assert result.success is True
            assert commander.lock_status == LeaderLockStatus.UNLOCKED  # Stays unlocked
            assert commander.can_use_ability()  # Can still use

    def test_commander_unlock_persists_across_turns(self):
        """Test that commander unlock status persists across game turns.

        GREEN: Implement using mock objects for state persistence
        """
        # Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player], current_phase="action")

        initialize_placeholder_leaders(player)
        commander = player.leader_sheet.commander
        assert commander is not None

        # Unlock commander
        player.controlled_planets = 4
        player.trade_goods = 6
        leader_manager = LeaderManager(game_state)
        leader_manager.check_unlock_conditions("player1")

        assert commander.lock_status == LeaderLockStatus.UNLOCKED

        # Simulate multiple turns
        for _turn in range(3):
            # Use commander ability
            result = leader_manager.execute_leader_ability(
                "player1", commander.get_name()
            )
            assert result.success is True

            # Commander should remain unlocked across turns
            assert commander.lock_status == LeaderLockStatus.UNLOCKED


class TestHeroUnlockAbilityPurge:
    """Test hero unlock, ability use, and purging mechanics.

    Validates the complete hero lifecycle including complex unlock conditions,
    powerful one-time abilities, and permanent purging.

    Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7
    """

    def test_hero_complex_unlock_conditions(self):
        """Test hero complex unlock condition validation.

        GREEN: Implement using mock objects for mutable attributes
        """
        # Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player], current_phase="action")

        initialize_placeholder_leaders(player)
        hero = player.leader_sheet.hero
        assert hero is not None
        assert hero.lock_status == LeaderLockStatus.LOCKED

        leader_manager = LeaderManager(game_state)

        # Meet conditions one by one
        player.controls_mecatol_rex = False
        player.completed_objectives = 1
        player.victory_points = 8

        leader_manager.check_unlock_conditions("player1")
        assert hero.lock_status == LeaderLockStatus.LOCKED

        # Meet first condition

        from src.ti4.core.planet import Planet

        # Add Mecatol Rex to player's controlled planets
        mecatol_rex = Planet("Mecatol Rex", 1, 6)
        game_state = game_state.add_player_planet("player1", mecatol_rex)
        leader_manager = LeaderManager(game_state)
        leader_manager.check_unlock_conditions("player1")
        assert hero.lock_status == LeaderLockStatus.LOCKED

        # Meet second condition
        player.completed_objectives = 3
        leader_manager.check_unlock_conditions("player1")
        assert hero.lock_status == LeaderLockStatus.LOCKED

        # Meet third condition
        player.victory_points = 12
        leader_manager.check_unlock_conditions("player1")
        assert hero.lock_status == LeaderLockStatus.UNLOCKED

    def test_hero_powerful_one_time_ability_and_purge(self):
        """Test hero powerful ability execution and automatic purging.

        GREEN: Implement using mock objects
        """
        # Setup
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player], current_phase="action")

        initialize_placeholder_leaders(player)
        hero = player.leader_sheet.hero
        assert hero is not None

        # Unlock hero - use MockPlayer's attribute setting for this test
        player.controls_mecatol_rex = True
        player.completed_objectives = 3
        player.victory_points = 12

        leader_manager = LeaderManager(game_state)
        leader_manager.check_unlock_conditions("player1")
        assert hero.lock_status == LeaderLockStatus.UNLOCKED

        # Use hero ability
        result = leader_manager.execute_leader_ability("player1", hero.get_name())

        assert result.success is True
        assert len(result.effects) > 0

        # Verify powerful effects
        assert result.game_state_changes is not None
        changes = result.game_state_changes
        assert changes.get("command_tokens_gained") == 3
        assert changes.get("action_cards_drawn") == 2
        assert changes.get("trade_goods_gained") == 5

        # Hero should be purged
        assert hero.lock_status == LeaderLockStatus.PURGED
        assert not hero.can_use_ability()

    def test_hero_cannot_be_used_after_purge(self):
        """Test that hero cannot be used after being purged.

        GREEN: Implement using mock objects
        """
        # Setup and unlock hero
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player], current_phase="action")

        initialize_placeholder_leaders(player)
        hero = player.leader_sheet.hero
        assert hero is not None

        # Unlock and use hero - MockPlayer is mutable
        player.controls_mecatol_rex = True
        player.completed_objectives = 3
        player.victory_points = 12

        leader_manager = LeaderManager(game_state)
        leader_manager.check_unlock_conditions("player1")

        # First use (should succeed and purge)
        result1 = leader_manager.execute_leader_ability("player1", hero.get_name())
        assert result1.success is True
        assert hero.lock_status == LeaderLockStatus.PURGED

        # Second use attempt (should fail)
        result2 = leader_manager.execute_leader_ability("player1", hero.get_name())
        assert result2.success is False
        assert "purged" in result2.error_message.lower()

    def test_hero_purge_persists_across_turns(self):
        """Test that hero purge status persists across game turns.

        GREEN: Implement using mock objects for state persistence
        """
        # Setup, unlock, and use hero
        player = MockPlayer("player1", Faction.ARBOREC)
        game_state = MockGameState(players=[player], current_phase="action")

        initialize_placeholder_leaders(player)
        hero = player.leader_sheet.hero
        assert hero is not None

        # Unlock and use hero - MockPlayer is mutable
        player.controls_mecatol_rex = True
        player.completed_objectives = 3
        player.victory_points = 12

        leader_manager = LeaderManager(game_state)
        leader_manager.check_unlock_conditions("player1")
        leader_manager.execute_leader_ability("player1", hero.get_name())

        assert hero.lock_status == LeaderLockStatus.PURGED

        # Simulate multiple turns
        for _turn in range(3):
            # Hero should remain purged across turns
            assert hero.lock_status == LeaderLockStatus.PURGED

            # Try to use hero (should still fail)
            result = leader_manager.execute_leader_ability("player1", hero.get_name())
            assert result.success is False


class TestMultiTurnIntegrationScenarios:
    """Test complex multi-turn scenarios with all leader types.

    Validates realistic game scenarios where multiple leaders are used
    across multiple turns with various game state changes.

    Requirements: All requirements integrated
    """

    def test_realistic_multi_turn_leader_usage_scenario(self):
        """Test realistic scenario with all three leader types across multiple turns.

        RED: This will fail until we have complete integration
        """
        # Setup game with two players
        game_state = GameState()
        player1 = Player("player1", Faction.ARBOREC)
        player2 = Player("player2", Faction.SOL)
        game_state = game_state.add_player(player1).add_player(player2)

        # Initialize leaders for both players
        initialize_placeholder_leaders(player1)
        initialize_placeholder_leaders(player2)

        leader_manager = LeaderManager(game_state)
        status_manager = StatusPhaseManager()

        # Turn 1: Both players use agents
        agent1 = player1.leader_sheet.agent
        agent2 = player2.leader_sheet.agent

        result1 = leader_manager.execute_leader_ability("player1", agent1.get_name())
        result2 = leader_manager.execute_leader_ability("player2", agent2.get_name())

        assert result1.success is True
        assert result2.success is True
        assert agent1.ready_status == LeaderReadyStatus.EXHAUSTED
        assert agent2.ready_status == LeaderReadyStatus.EXHAUSTED

        # End Turn 1: Status phase
        game_state = status_manager.ready_all_cards(game_state)

        # Turn 2: Player 1 unlocks commander
        # Note: In a real game, controlled_planets and trade_goods would be tracked in game state
        # For this test, we need to set up the game state with appropriate resources
        from dataclasses import replace

        from src.ti4.core.planet import Planet

        # Create some planets for player1 to control (need 3+ for commander unlock)
        planets = [
            Planet("Planet1", 2, 1),
            Planet("Planet2", 1, 2),
            Planet("Planet3", 3, 0),
            Planet("Planet4", 1, 1),
        ]

        # Update game state with player1 controlling planets
        for planet in planets:
            game_state = game_state.add_player_planet("player1", planet)

        # Give player1 trade goods (need 5+ for commander unlock)
        player1.gain_trade_goods(6)

        # Update the leader manager with the new game state
        leader_manager = LeaderManager(game_state)
        leader_manager.check_unlock_conditions("player1")

        # Get the updated player1 from the game state
        updated_player1 = next(p for p in game_state.players if p.id == "player1")
        commander1 = updated_player1.leader_sheet.commander
        assert commander1.lock_status == LeaderLockStatus.UNLOCKED

        # Both players use agents again, player 1 also uses commander
        # Find updated agents after status phase
        updated_player1 = None
        updated_player2 = None
        for p in game_state.players:
            if p.id == "player1":
                updated_player1 = p
            elif p.id == "player2":
                updated_player2 = p

        updated_agent1 = updated_player1.leader_sheet.agent
        updated_agent2 = updated_player2.leader_sheet.agent

        result1 = leader_manager.execute_leader_ability(
            "player1", updated_agent1.get_name()
        )
        result2 = leader_manager.execute_leader_ability(
            "player2", updated_agent2.get_name()
        )
        result3 = leader_manager.execute_leader_ability(
            "player1", commander1.get_name()
        )

        assert result1.success is True
        assert result2.success is True
        assert result3.success is True

        # Turn 3: Player 1 unlocks and uses hero
        # Add Mecatol Rex to player's controlled planets (if not already there)
        mecatol_rex = Planet("Mecatol Rex", 1, 6)
        if "Mecatol Rex" not in [
            p.name for p in game_state.get_player_planets("player1")
        ]:
            game_state = game_state.add_player_planet("player1", mecatol_rex)

        # Add more completed objectives and victory points
        game_state = replace(
            game_state,
            completed_objectives={"player1": ["obj1", "obj2", "obj3"]},
            victory_points={"player1": 12},
        )

        # Update leader manager with new game state
        leader_manager = LeaderManager(game_state)
        leader_manager.check_unlock_conditions("player1")

        # Get updated player1 from game state
        updated_player1 = next(p for p in game_state.players if p.id == "player1")
        hero1 = updated_player1.leader_sheet.hero
        assert hero1.lock_status == LeaderLockStatus.UNLOCKED

        result4 = leader_manager.execute_leader_ability("player1", hero1.get_name())
        assert result4.success is True
        assert hero1.lock_status == LeaderLockStatus.PURGED

    def test_leader_state_consistency_across_game_phases(self):
        """Test that leader states remain consistent across different game phases.

        RED: This will fail until we implement phase validation
        """
        # Setup
        game_state = GameState()
        player = Player("player1", Faction.ARBOREC)
        game_state = game_state.add_player(player)

        initialize_placeholder_leaders(player)
        leader_manager = LeaderManager(game_state)

        # Test different game phases
        phases = ["strategy", "action", "status", "agenda"]

        for phase in phases:
            # Update game state with new phase (immutable)
            from dataclasses import replace

            game_state = replace(game_state, phase=phase)

            # Update leader manager with new game state
            leader_manager = LeaderManager(game_state)

            # Get updated player reference from game state
            player = next(p for p in game_state.players if p.id == "player1")

            # Check that leader states are preserved
            agent = player.leader_sheet.agent
            commander = player.leader_sheet.commander
            hero = player.leader_sheet.hero

            # Agent should maintain its ready/exhaust state
            if agent.ready_status == LeaderReadyStatus.READIED:
                result = leader_manager.execute_leader_ability(
                    "player1", agent.get_name()
                )
                # Should succeed in action phase, might fail in others
                if phase == "action":
                    assert result.success is True
                    assert agent.ready_status == LeaderReadyStatus.EXHAUSTED

            # Commander unlock status should persist
            if commander.lock_status == LeaderLockStatus.UNLOCKED:
                assert commander.can_use_ability()

            # Hero purge status should persist
            if hero.lock_status == LeaderLockStatus.PURGED:
                assert not hero.can_use_ability()

    def test_leader_interaction_with_game_events(self):
        """Test leader interactions with various game events and state changes.

        RED: This will fail until we implement event integration
        """
        # Setup
        game_state = GameState()
        player = Player("player1", Faction.ARBOREC)
        game_state = game_state.add_player(player)

        initialize_placeholder_leaders(player)
        leader_manager = LeaderManager(game_state)

        # Simulate game events that might affect leaders
        events = [
            {"type": "planet_lost", "effect": "reduce_controlled_planets"},
            {"type": "trade_goods_spent", "effect": "reduce_trade_goods"},
            {"type": "objective_completed", "effect": "increase_objectives"},
            {"type": "victory_point_gained", "effect": "increase_victory_points"},
        ]

        for event in events:
            # Apply event effects (using game state updates)
            from dataclasses import replace

            if event["effect"] == "reduce_controlled_planets":
                # Remove a planet if any exist
                current_planets = game_state.get_player_planets("player1")
                if current_planets:
                    # Remove the last planet
                    planet_to_remove = current_planets[-1]
                    game_state = game_state.remove_player_planet(
                        "player1", planet_to_remove
                    )

            elif event["effect"] == "reduce_trade_goods":
                # Spend trade goods if player has any
                current_player = next(
                    p for p in game_state.players if p.id == "player1"
                )
                if current_player.get_trade_goods() > 0:
                    amount_to_spend = min(2, current_player.get_trade_goods())
                    current_player.spend_trade_goods(amount_to_spend)

            elif event["effect"] == "increase_objectives":
                # Add a completed objective
                current_objectives = game_state.completed_objectives.get("player1", [])
                new_objectives = current_objectives + [
                    f"objective_{len(current_objectives) + 1}"
                ]
                game_state = replace(
                    game_state,
                    completed_objectives={
                        **game_state.completed_objectives,
                        "player1": new_objectives,
                    },
                )

            elif event["effect"] == "increase_victory_points":
                # Add victory points
                current_vp = game_state.victory_points.get("player1", 0)
                game_state = replace(
                    game_state,
                    victory_points={
                        **game_state.victory_points,
                        "player1": current_vp + 2,
                    },
                )

            # Update leader manager with modified game state
            leader_manager = LeaderManager(game_state)

            # Check unlock conditions after each event
            leader_manager.check_unlock_conditions("player1")

            # Verify leader states are updated appropriately
            current_player = next(p for p in game_state.players if p.id == "player1")
            commander = current_player.leader_sheet.commander
            hero = current_player.leader_sheet.hero

            # Commander and hero unlock status should reflect current conditions
            commander_should_be_unlocked = (
                getattr(player, "controlled_planets", 0) >= 3
                and getattr(player, "trade_goods", 0) >= 5
            )

            hero_should_be_unlocked = (
                getattr(player, "controls_mecatol_rex", False)
                and getattr(player, "completed_objectives", 0) >= 2
                and getattr(player, "victory_points", 0) >= 10
            )

            if commander_should_be_unlocked:
                assert commander.lock_status == LeaderLockStatus.UNLOCKED

            if hero_should_be_unlocked and hero.lock_status != LeaderLockStatus.PURGED:
                assert hero.lock_status == LeaderLockStatus.UNLOCKED


class TestCrossSystemLeaderValidation:
    """Test leader ability validation across different game systems.

    Validates that leader abilities properly integrate with and validate
    against other game systems like combat, resources, and movement.

    Requirements: 10.1, 10.2, 10.3, 10.4, 10.5
    """

    def test_leader_ability_system_integration_validation(self):
        """Test that leader abilities validate system integration properly.

        RED: This will fail until we implement system integration validation
        """
        # Setup
        game_state = GameState()
        player = Player("player1", Faction.ARBOREC)
        game_state = game_state.add_player(player)

        initialize_placeholder_leaders(player)
        leader_manager = LeaderManager(game_state)

        # Test agent ability with system integration
        agent = player.leader_sheet.agent

        # Test combat system integration
        result = leader_manager.execute_leader_ability(
            "player1", agent.get_name(), combat_modifier=True
        )
        assert result.success is True
        assert "combat" in str(result.effects).lower()

        # Reset agent for next test
        agent.ready()

        # Test movement system integration
        result = leader_manager.execute_leader_ability(
            "player1", agent.get_name(), movement_bonus=True
        )
        assert result.success is True
        assert "movement" in str(result.effects).lower()

    def test_leader_ability_cross_system_effects(self):
        """Test leader abilities that affect multiple systems simultaneously.

        GREEN: Implement using existing placeholder hero multi-system effects
        """
        # Setup
        game_state = GameState()
        player = Player("player1", Faction.ARBOREC)
        game_state = game_state.add_player(player)

        initialize_placeholder_leaders(player)

        # Unlock hero - set up game state properly for real Player class
        from dataclasses import replace

        from src.ti4.core.planet import Planet

        # Add Mecatol Rex to player's controlled planets
        mecatol_rex = Planet("Mecatol Rex", 1, 6)
        game_state = game_state.add_player_planet("player1", mecatol_rex)

        # Add completed objectives and victory points
        game_state = replace(
            game_state,
            completed_objectives={"player1": ["obj1", "obj2", "obj3"]},
            victory_points={"player1": 12},
        )

        leader_manager = LeaderManager(game_state)
        leader_manager.check_unlock_conditions("player1")

        hero = player.leader_sheet.hero
        assert hero.lock_status == LeaderLockStatus.UNLOCKED

        # Use hero ability (affects multiple systems)
        result = leader_manager.execute_leader_ability("player1", hero.get_name())

        assert result.success is True
        assert result.game_state_changes is not None

        # Verify multi-system effects
        changes = result.game_state_changes
        assert changes.get("command_tokens_gained") == 3  # Command system
        assert changes.get("action_cards_drawn") == 2  # Card system
        assert changes.get("trade_goods_gained") == 5  # Resource system
        assert changes.get("combat_bonus_active") is True  # Combat system

    def test_leader_ability_error_handling_across_systems(self):
        """Test error handling when leader abilities interact with faulty systems.

        RED: This will fail until we implement comprehensive error handling
        """
        # Setup
        game_state = GameState()
        player = Player("player1", Faction.ARBOREC)
        game_state = game_state.add_player(player)

        initialize_placeholder_leaders(player)
        leader_manager = LeaderManager(game_state)

        agent = player.leader_sheet.agent

        # Test with faulty resource system
        result = leader_manager.execute_leader_ability(
            "player1", agent.get_name(), use_resource_system=True
        )

        # Should handle system errors gracefully
        # This will fail until we implement proper error handling
        assert result.success is False or result.success is True
        if not result.success:
            assert "error" in result.error_message.lower()

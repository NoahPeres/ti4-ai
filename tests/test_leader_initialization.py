"""Integration tests for leader sheet setup and initialization.

Tests the leader initialization during game setup including:
- Leader creation for each faction
- Proper assignment to player leader sheets
- Validation of leader configurations
- Integration with game setup process

LRR References:
- Rule 51: LEADERS
- Requirements 5.1, 5.2, 5.3, 5.4, 5.5
"""

import pytest

from ti4.core.constants import Faction
from ti4.core.leaders import Agent, Commander, Hero, LeaderType
from ti4.core.player import Player
from ti4.testing.scenario_builder import GameScenarioBuilder


class TestLeaderInitialization:
    """Test cases for leader initialization during game setup."""

    def test_player_gets_three_leaders_during_setup(self) -> None:
        """Test that each player gets exactly three leaders during game setup."""
        # RED: Test that players get leaders during setup
        game_state = (
            GameScenarioBuilder()
            .with_players(("player1", Faction.ARBOREC), ("player2", Faction.SOL))
            .build()
        )

        player1 = next(p for p in game_state.players if p.id == "player1")
        player2 = next(p for p in game_state.players if p.id == "player2")

        # Each player should have exactly three leaders
        assert len(player1.get_leaders()) == 3
        assert len(player2.get_leaders()) == 3

        # Each player should have one of each type
        player1_leaders = player1.get_leaders()
        player1_types = [leader.get_leader_type() for leader in player1_leaders]
        assert LeaderType.AGENT in player1_types
        assert LeaderType.COMMANDER in player1_types
        assert LeaderType.HERO in player1_types

        player2_leaders = player2.get_leaders()
        player2_types = [leader.get_leader_type() for leader in player2_leaders]
        assert LeaderType.AGENT in player2_types
        assert LeaderType.COMMANDER in player2_types
        assert LeaderType.HERO in player2_types

    def test_leaders_belong_to_correct_player(self) -> None:
        """Test that leaders are assigned to the correct player."""
        # RED: Test player ownership validation
        game_state = (
            GameScenarioBuilder()
            .with_players(("player1", Faction.ARBOREC), ("player2", Faction.SOL))
            .build()
        )

        player1 = next(p for p in game_state.players if p.id == "player1")
        player2 = next(p for p in game_state.players if p.id == "player2")

        # All leaders should belong to their respective players
        for leader in player1.get_leaders():
            assert leader.player_id == "player1"

        for leader in player2.get_leaders():
            assert leader.player_id == "player2"

    def test_leaders_have_correct_faction(self) -> None:
        """Test that leaders have the correct faction."""
        # RED: Test faction assignment
        game_state = (
            GameScenarioBuilder()
            .with_players(("player1", Faction.ARBOREC), ("player2", Faction.SOL))
            .build()
        )

        player1 = next(p for p in game_state.players if p.id == "player1")
        player2 = next(p for p in game_state.players if p.id == "player2")

        # All leaders should have their player's faction
        for leader in player1.get_leaders():
            assert leader.faction == Faction.ARBOREC

        for leader in player2.get_leaders():
            assert leader.faction == Faction.SOL

    def test_leader_sheet_is_complete_after_setup(self) -> None:
        """Test that leader sheet is complete after setup."""
        # RED: Test leader sheet completeness
        game_state = (
            GameScenarioBuilder().with_players(("player1", Faction.ARBOREC)).build()
        )

        player1 = next(p for p in game_state.players if p.id == "player1")

        # Leader sheet should be complete
        assert player1.leader_sheet.is_complete()

    def test_agent_starts_unlocked_and_readied(self) -> None:
        """Test that agents start in unlocked and readied state."""
        # RED: Test agent initial state
        game_state = (
            GameScenarioBuilder().with_players(("player1", Faction.ARBOREC)).build()
        )

        player1 = next(p for p in game_state.players if p.id == "player1")
        agent = player1.leader_sheet.get_leader_by_type(LeaderType.AGENT)

        assert agent is not None
        assert isinstance(agent, Agent)
        assert agent.can_use_ability()

    def test_commander_starts_locked(self) -> None:
        """Test that commanders start in locked state."""
        # RED: Test commander initial state
        game_state = (
            GameScenarioBuilder().with_players(("player1", Faction.ARBOREC)).build()
        )

        player1 = next(p for p in game_state.players if p.id == "player1")
        commander = player1.leader_sheet.get_leader_by_type(LeaderType.COMMANDER)

        assert commander is not None
        assert isinstance(commander, Commander)
        assert not commander.can_use_ability()

    def test_hero_starts_locked(self) -> None:
        """Test that heroes start in locked state."""
        # RED: Test hero initial state
        game_state = (
            GameScenarioBuilder().with_players(("player1", Faction.ARBOREC)).build()
        )

        player1 = next(p for p in game_state.players if p.id == "player1")
        hero = player1.leader_sheet.get_leader_by_type(LeaderType.HERO)

        assert hero is not None
        assert isinstance(hero, Hero)
        assert not hero.can_use_ability()

    def test_multiple_players_get_different_leaders(self) -> None:
        """Test that different players get different leader instances."""
        # RED: Test leader instance uniqueness
        game_state = (
            GameScenarioBuilder()
            .with_players(("player1", Faction.ARBOREC), ("player2", Faction.SOL))
            .build()
        )

        player1 = next(p for p in game_state.players if p.id == "player1")
        player2 = next(p for p in game_state.players if p.id == "player2")

        player1_leaders = player1.get_leaders()
        player2_leaders = player2.get_leaders()

        # Leaders should be different instances
        for leader1 in player1_leaders:
            for leader2 in player2_leaders:
                assert leader1 is not leader2

    def test_direct_player_creation_initializes_leaders(self) -> None:
        """Test that creating a Player directly also initializes leaders."""
        # RED: Test direct Player creation
        player = Player(id="test_player", faction=Faction.BARONY)

        # Player should have empty leader sheet initially
        assert len(player.get_leaders()) == 0
        assert not player.leader_sheet.is_complete()

        # But after initialization, should have all three leaders
        # This will be implemented in the initialization method
        from ti4.core.leaders import initialize_player_leaders

        initialize_player_leaders(player)

        assert len(player.get_leaders()) == 3
        assert player.leader_sheet.is_complete()

        # Check that all leader types are present
        leader_types = [leader.get_leader_type() for leader in player.get_leaders()]
        assert LeaderType.AGENT in leader_types
        assert LeaderType.COMMANDER in leader_types
        assert LeaderType.HERO in leader_types


class TestLeaderInitializationValidation:
    """Test cases for leader initialization validation."""

    def test_cannot_initialize_leaders_twice(self) -> None:
        """Test that leaders cannot be initialized twice for the same player."""
        # RED: Test double initialization prevention
        player = Player(id="test_player", faction=Faction.BARONY)

        from ti4.core.leaders import initialize_player_leaders

        # First initialization should succeed
        initialize_player_leaders(player)
        assert player.leader_sheet.is_complete()

        # Second initialization should fail
        with pytest.raises(ValueError, match="Leaders already initialized"):
            initialize_player_leaders(player)

    def test_cannot_initialize_leaders_with_invalid_faction(self) -> None:
        """Test that leader initialization validates faction."""
        # RED: Test faction validation
        # This test will be implemented when we add faction-specific leaders
        pass

    def test_leader_initialization_preserves_player_state(self) -> None:
        """Test that leader initialization doesn't affect other player state."""
        # RED: Test state preservation
        player = Player(id="test_player", faction=Faction.BARONY)

        # Modify some player state
        player.gain_command_token("tactic")
        original_reinforcements = player.reinforcements

        from ti4.core.leaders import initialize_player_leaders

        initialize_player_leaders(player)

        # Player state should be preserved
        assert player.reinforcements == original_reinforcements
        assert player.command_sheet.tactic_pool == 4  # 3 starting + 1 gained


class TestGameSetupIntegration:
    """Test cases for leader initialization integration with game setup."""

    def test_scenario_builder_initializes_leaders_automatically(self) -> None:
        """Test that GameScenarioBuilder automatically initializes leaders."""
        # RED: Test automatic initialization in scenario builder
        game_state = (
            GameScenarioBuilder()
            .with_players(
                ("player1", Faction.ARBOREC),
                ("player2", Faction.SOL),
                ("player3", Faction.HACAN),
            )
            .build()
        )

        # All players should have complete leader sheets
        for player in game_state.players:
            assert player.leader_sheet.is_complete()
            assert len(player.get_leaders()) == 3

    def test_empty_game_state_has_no_leaders(self) -> None:
        """Test that empty game state has no leaders."""
        # RED: Test empty state
        from ti4.core.game_state import GameState

        game_state = GameState()
        assert len(game_state.players) == 0

    def test_adding_player_to_existing_game_initializes_leaders(self) -> None:
        """Test that adding a player to existing game initializes their leaders."""
        # RED: Test dynamic player addition
        from ti4.core.game_state import GameState

        game_state = GameState()
        player = Player(id="new_player", faction=Faction.WINNU)

        # Initially no leaders
        assert len(player.get_leaders()) == 0

        # After adding to game, should have leaders
        # This will be implemented in a game setup method
        from ti4.core.leaders import setup_player_leaders_for_game

        setup_player_leaders_for_game(player, game_state)

        assert len(player.get_leaders()) == 3
        assert player.leader_sheet.is_complete()

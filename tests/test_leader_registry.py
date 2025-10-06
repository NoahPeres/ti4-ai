"""Tests for LeaderRegistry class.

This module tests the LeaderRegistry class which provides faction-specific
leader definitions, factory methods, and validation functionality.

LRR References:
- Rule 51: LEADERS
- Requirements 7.1, 7.2, 7.3, 7.4, 7.5
"""

import pytest

from src.ti4.core.constants import Faction
from src.ti4.core.leaders import Agent, Commander, Hero, LeaderType


class TestLeaderRegistry:
    """Test cases for LeaderRegistry functionality."""

    def test_leader_registry_can_be_imported(self) -> None:
        """Test that LeaderRegistry can be imported (RED phase)."""
        from src.ti4.core.leaders import LeaderRegistry  # noqa: F401

    def test_leader_registry_initialization(self) -> None:
        """Test LeaderRegistry initialization."""
        from src.ti4.core.leaders import LeaderRegistry

        registry = LeaderRegistry()
        assert registry is not None

    def test_create_faction_leaders_returns_three_leaders(self) -> None:
        """Test that create_faction_leaders returns exactly three leaders."""
        from src.ti4.core.leaders import LeaderRegistry

        registry = LeaderRegistry()
        leaders = registry.create_faction_leaders(Faction.SOL, "player1")

        assert len(leaders) == 3
        assert isinstance(leaders[0], Agent)
        assert isinstance(leaders[1], Commander)
        assert isinstance(leaders[2], Hero)

    def test_create_faction_leaders_with_invalid_faction_fails(self) -> None:
        """Test that create_faction_leaders fails with invalid faction."""
        from src.ti4.core.leaders import LeaderRegistry

        registry = LeaderRegistry()

        with pytest.raises(TypeError):
            registry.create_faction_leaders("invalid_faction", "player1")  # type: ignore

    def test_create_faction_leaders_with_empty_player_id_fails(self) -> None:
        """Test that create_faction_leaders fails with empty player_id."""
        from src.ti4.core.leaders import LeaderRegistry

        registry = LeaderRegistry()

        with pytest.raises(ValueError, match="player_id cannot be empty"):
            registry.create_faction_leaders(Faction.SOL, "")

    def test_get_leader_definition_returns_leader_info(self) -> None:
        """Test that get_leader_definition returns leader information."""
        from src.ti4.core.leaders import LeaderRegistry

        registry = LeaderRegistry()
        definition = registry.get_leader_definition(Faction.SOL, LeaderType.AGENT)

        assert definition is not None
        assert "name" in definition
        assert "unlock_conditions" in definition

    def test_get_leader_definition_with_invalid_faction_fails(self) -> None:
        """Test that get_leader_definition fails with invalid faction."""
        from src.ti4.core.leaders import LeaderRegistry

        registry = LeaderRegistry()

        with pytest.raises(TypeError):
            registry.get_leader_definition("invalid_faction", LeaderType.AGENT)  # type: ignore

    def test_get_leader_definition_with_invalid_leader_type_fails(self) -> None:
        """Test that get_leader_definition fails with invalid leader type."""
        from src.ti4.core.leaders import LeaderRegistry

        registry = LeaderRegistry()

        with pytest.raises(TypeError):
            registry.get_leader_definition(Faction.SOL, "invalid_type")  # type: ignore

    def test_validate_faction_support_returns_true_for_supported_faction(self) -> None:
        """Test that validate_faction_support returns True for supported factions."""
        from src.ti4.core.leaders import LeaderRegistry

        registry = LeaderRegistry()
        is_supported = registry.validate_faction_support(Faction.SOL)

        assert is_supported is True

    def test_validate_faction_support_with_invalid_faction_fails(self) -> None:
        """Test that validate_faction_support fails with invalid faction."""
        from src.ti4.core.leaders import LeaderRegistry

        registry = LeaderRegistry()

        with pytest.raises(TypeError):
            registry.validate_faction_support("invalid_faction")  # type: ignore

    def test_get_supported_factions_returns_faction_list(self) -> None:
        """Test that get_supported_factions returns list of supported factions."""
        from src.ti4.core.leaders import LeaderRegistry

        registry = LeaderRegistry()
        factions = registry.get_supported_factions()

        assert isinstance(factions, list)
        assert len(factions) > 0
        assert all(isinstance(faction, Faction) for faction in factions)

    def test_create_faction_leaders_returns_correct_types_in_order(self) -> None:
        """Test that create_faction_leaders returns leaders in correct order (agent, commander, hero)."""
        from src.ti4.core.leaders import LeaderRegistry

        registry = LeaderRegistry()
        leaders = registry.create_faction_leaders(Faction.HACAN, "player1")

        assert len(leaders) == 3
        assert leaders[0].get_leader_type() == LeaderType.AGENT
        assert leaders[1].get_leader_type() == LeaderType.COMMANDER
        assert leaders[2].get_leader_type() == LeaderType.HERO

    def test_create_faction_leaders_assigns_correct_faction_and_player(self) -> None:
        """Test that created leaders have correct faction and player assignments."""
        from src.ti4.core.leaders import LeaderRegistry

        registry = LeaderRegistry()
        leaders = registry.create_faction_leaders(Faction.XXCHA, "test_player")

        for leader in leaders:
            assert leader.faction == Faction.XXCHA
            assert leader.player_id == "test_player"

    def test_create_faction_leaders_with_whitespace_player_id_fails(self) -> None:
        """Test that create_faction_leaders fails with whitespace-only player_id."""
        from src.ti4.core.leaders import LeaderRegistry

        registry = LeaderRegistry()

        with pytest.raises(ValueError, match="player_id cannot be empty"):
            registry.create_faction_leaders(Faction.SOL, "   ")

    def test_get_leader_definition_returns_different_info_for_different_types(
        self,
    ) -> None:
        """Test that get_leader_definition returns different information for different leader types."""
        from src.ti4.core.leaders import LeaderRegistry

        registry = LeaderRegistry()

        agent_def = registry.get_leader_definition(Faction.SOL, LeaderType.AGENT)
        commander_def = registry.get_leader_definition(
            Faction.SOL, LeaderType.COMMANDER
        )
        hero_def = registry.get_leader_definition(Faction.SOL, LeaderType.HERO)

        # Agent should have no unlock conditions
        assert agent_def["unlock_conditions"] == []

        # Commander and Hero should have unlock conditions
        assert len(commander_def["unlock_conditions"]) > 0
        assert len(hero_def["unlock_conditions"]) > 0

    def test_get_leader_definition_returns_faction_specific_names(self) -> None:
        """Test that get_leader_definition returns faction-specific names."""
        from src.ti4.core.leaders import LeaderRegistry

        registry = LeaderRegistry()

        sol_agent = registry.get_leader_definition(Faction.SOL, LeaderType.AGENT)
        hacan_agent = registry.get_leader_definition(Faction.HACAN, LeaderType.AGENT)

        assert "Sol" in sol_agent["name"]
        assert "Hacan" in hacan_agent["name"]
        assert sol_agent["name"] != hacan_agent["name"]

    def test_validate_faction_support_returns_true_for_all_enum_factions(self) -> None:
        """Test that validate_faction_support returns True for all Faction enum values."""
        from src.ti4.core.leaders import LeaderRegistry

        registry = LeaderRegistry()

        # Test all factions from the enum
        for faction in Faction:
            assert registry.validate_faction_support(faction) is True

    def test_get_supported_factions_includes_all_enum_factions(self) -> None:
        """Test that get_supported_factions includes all Faction enum values."""
        from src.ti4.core.leaders import LeaderRegistry

        registry = LeaderRegistry()
        supported_factions = registry.get_supported_factions()

        # Should include all factions from the enum
        for faction in Faction:
            assert faction in supported_factions


class TestLeaderRegistryIntegration:
    """Integration tests for LeaderRegistry with other leader system components."""

    def test_registry_integration_with_leader_manager(self) -> None:
        """Test that LeaderRegistry integrates properly with LeaderManager."""
        from src.ti4.core.game_state import GameState
        from src.ti4.core.leaders import LeaderManager, LeaderRegistry
        from src.ti4.core.player import Player

        # Create a registry and use it to create leaders
        registry = LeaderRegistry()
        leaders = registry.create_faction_leaders(Faction.SOL, "player1")

        # Create a player and assign the leaders
        player = Player(id="player1", faction=Faction.SOL)
        player.leader_sheet.set_agent(leaders[0])
        player.leader_sheet.set_commander(leaders[1])
        player.leader_sheet.set_hero(leaders[2])

        # Create game state and manager
        game_state = GameState(players=[player])
        manager = LeaderManager(game_state)

        # Test that manager can work with registry-created leaders
        manager.check_unlock_conditions("player1")
        manager.ready_agents("player1")

        # Test ability execution
        result = manager.execute_leader_ability("player1", "Agent")
        assert result.success is True

    def test_registry_created_leaders_have_proper_initial_states(self) -> None:
        """Test that registry-created leaders have proper initial states."""
        from src.ti4.core.leaders import (
            LeaderLockStatus,
            LeaderReadyStatus,
            LeaderRegistry,
        )

        registry = LeaderRegistry()
        leaders = registry.create_faction_leaders(Faction.HACAN, "test_player")

        agent, commander, hero = leaders

        # Agent should start unlocked and readied
        assert agent.lock_status == LeaderLockStatus.UNLOCKED
        assert agent.ready_status == LeaderReadyStatus.READIED

        # Commander should start locked with no ready status
        assert commander.lock_status == LeaderLockStatus.LOCKED
        assert commander.ready_status is None

        # Hero should start locked with no ready status
        assert hero.lock_status == LeaderLockStatus.LOCKED
        assert hero.ready_status is None

    def test_registry_created_leaders_can_use_abilities_when_appropriate(self) -> None:
        """Test that registry-created leaders can use abilities when in appropriate states."""
        from src.ti4.core.leaders import LeaderRegistry

        registry = LeaderRegistry()
        leaders = registry.create_faction_leaders(Faction.XXCHA, "test_player")

        agent, commander, hero = leaders

        # Agent should be able to use ability initially
        assert agent.can_use_ability() is True

        # Commander and Hero should not be able to use abilities initially (locked)
        assert commander.can_use_ability() is False
        assert hero.can_use_ability() is False

        # After unlocking, they should be able to use abilities
        commander.unlock()
        hero.unlock()
        assert commander.can_use_ability() is True
        assert hero.can_use_ability() is True

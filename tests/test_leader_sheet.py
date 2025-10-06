"""Unit tests for LeaderSheet data structure implementation.

Tests the LeaderSheet class functionality including:
- Leader storage and retrieval by type
- Leader retrieval by name
- Validation and error handling
- Integration with Player class

LRR References:
- Rule 51: LEADERS
- Requirements 5.1, 5.2, 5.3, 5.4, 5.5
"""

import pytest

from src.ti4.core.constants import Faction
from src.ti4.core.leaders import (
    Agent,
    Commander,
    Hero,
    LeaderSheet,
    LeaderType,
)
from src.ti4.core.player import Player


class TestLeaderSheet:
    """Test cases for LeaderSheet data structure."""

    def test_leader_sheet_initialization(self) -> None:
        """Test LeaderSheet can be initialized with player_id."""
        # RED: Test basic initialization
        player_id = "player1"
        sheet = LeaderSheet(player_id=player_id)

        assert sheet.player_id == player_id
        assert sheet.agent is None
        assert sheet.commander is None
        assert sheet.hero is None

    def test_leader_sheet_initialization_validates_player_id(self) -> None:
        """Test LeaderSheet validates player_id during initialization."""
        # RED: Test validation of empty player_id
        with pytest.raises(ValueError, match="player_id cannot be empty or None"):
            LeaderSheet(player_id="")

        with pytest.raises(ValueError, match="player_id cannot be empty or None"):
            LeaderSheet(player_id="   ")

        with pytest.raises(ValueError, match="player_id cannot be empty or None"):
            LeaderSheet(player_id=None)  # type: ignore

    def test_get_all_leaders_empty_sheet(self) -> None:
        """Test get_all_leaders returns empty list for empty sheet."""
        # RED: Test empty sheet behavior
        sheet = LeaderSheet(player_id="player1")
        leaders = sheet.get_all_leaders()

        assert leaders == []
        assert isinstance(leaders, list)

    def test_get_all_leaders_with_leaders(self) -> None:
        """Test get_all_leaders returns all assigned leaders."""
        # RED: Test with all three leader types
        player_id = "player1"
        faction = Faction.ARBOREC

        agent = Agent(faction=faction, player_id=player_id)
        commander = Commander(faction=faction, player_id=player_id)
        hero = Hero(faction=faction, player_id=player_id)

        sheet = LeaderSheet(player_id=player_id)
        sheet.set_agent(agent)
        sheet.set_commander(commander)
        sheet.set_hero(hero)

        leaders = sheet.get_all_leaders()

        assert len(leaders) == 3
        assert agent in leaders
        assert commander in leaders
        assert hero in leaders
        # Test consistent ordering: agent, commander, hero
        assert leaders[0] == agent
        assert leaders[1] == commander
        assert leaders[2] == hero

    def test_get_all_leaders_partial_assignment(self) -> None:
        """Test get_all_leaders with only some leaders assigned."""
        # RED: Test partial assignment scenarios
        player_id = "player1"
        faction = Faction.ARBOREC

        sheet = LeaderSheet(player_id=player_id)

        # Only agent assigned
        agent = Agent(faction=faction, player_id=player_id)
        sheet.set_agent(agent)

        leaders = sheet.get_all_leaders()
        assert len(leaders) == 1
        assert leaders[0] == agent

        # Add commander
        commander = Commander(faction=faction, player_id=player_id)
        sheet.set_commander(commander)

        leaders = sheet.get_all_leaders()
        assert len(leaders) == 2
        assert leaders[0] == agent
        assert leaders[1] == commander

    def test_get_leader_by_type(self) -> None:
        """Test get_leader_by_type returns correct leader for each type."""
        # RED: Test retrieval by type
        player_id = "player1"
        faction = Faction.ARBOREC

        agent = Agent(faction=faction, player_id=player_id)
        commander = Commander(faction=faction, player_id=player_id)
        hero = Hero(faction=faction, player_id=player_id)

        sheet = LeaderSheet(player_id=player_id)
        sheet.set_agent(agent)
        sheet.set_commander(commander)
        sheet.set_hero(hero)

        assert sheet.get_leader_by_type(LeaderType.AGENT) == agent
        assert sheet.get_leader_by_type(LeaderType.COMMANDER) == commander
        assert sheet.get_leader_by_type(LeaderType.HERO) == hero

    def test_get_leader_by_type_not_assigned(self) -> None:
        """Test get_leader_by_type returns None for unassigned leaders."""
        # RED: Test None return for missing leaders
        sheet = LeaderSheet(player_id="player1")

        assert sheet.get_leader_by_type(LeaderType.AGENT) is None
        assert sheet.get_leader_by_type(LeaderType.COMMANDER) is None
        assert sheet.get_leader_by_type(LeaderType.HERO) is None

    def test_get_leader_by_type_validates_input(self) -> None:
        """Test get_leader_by_type validates leader_type parameter."""
        # RED: Test input validation
        sheet = LeaderSheet(player_id="player1")

        with pytest.raises(
            ValueError, match="leader_type must be a LeaderType enum value"
        ):
            sheet.get_leader_by_type("agent")  # type: ignore

        with pytest.raises(
            ValueError, match="leader_type must be a LeaderType enum value"
        ):
            sheet.get_leader_by_type(None)  # type: ignore

    def test_get_leader_by_name(self) -> None:
        """Test get_leader_by_name returns correct leader."""
        # RED: Test retrieval by name
        player_id = "player1"
        faction = Faction.ARBOREC

        agent = Agent(faction=faction, player_id=player_id)
        commander = Commander(faction=faction, player_id=player_id)

        sheet = LeaderSheet(player_id=player_id)
        sheet.set_agent(agent)
        sheet.set_commander(commander)

        assert sheet.get_leader_by_name("Agent") == agent
        assert sheet.get_leader_by_name("Commander") == commander

    def test_get_leader_by_name_not_found(self) -> None:
        """Test get_leader_by_name returns None for non-existent leader."""
        # RED: Test None return for missing leader
        sheet = LeaderSheet(player_id="player1")

        assert sheet.get_leader_by_name("NonExistent") is None

    def test_get_leader_by_name_validates_input(self) -> None:
        """Test get_leader_by_name validates name parameter."""
        # RED: Test input validation
        sheet = LeaderSheet(player_id="player1")

        with pytest.raises(ValueError, match="name cannot be empty or None"):
            sheet.get_leader_by_name("")

        with pytest.raises(ValueError, match="name cannot be empty or None"):
            sheet.get_leader_by_name("   ")

        with pytest.raises(ValueError, match="name cannot be empty or None"):
            sheet.get_leader_by_name(None)  # type: ignore

    def test_get_leader_by_name_strips_whitespace(self) -> None:
        """Test get_leader_by_name handles whitespace in names."""
        # RED: Test whitespace handling
        player_id = "player1"
        faction = Faction.ARBOREC

        agent = Agent(faction=faction, player_id=player_id)
        sheet = LeaderSheet(player_id=player_id)
        sheet.set_agent(agent)

        assert sheet.get_leader_by_name("  Agent  ") == agent

    def test_set_agent(self) -> None:
        """Test set_agent assigns agent correctly."""
        # RED: Test agent assignment
        player_id = "player1"
        faction = Faction.ARBOREC

        agent = Agent(faction=faction, player_id=player_id)
        sheet = LeaderSheet(player_id=player_id)

        sheet.set_agent(agent)
        assert sheet.agent == agent

    def test_set_agent_validates_input(self) -> None:
        """Test set_agent validates agent parameter."""
        # RED: Test input validation
        sheet = LeaderSheet(player_id="player1")

        with pytest.raises(ValueError, match="agent cannot be None"):
            sheet.set_agent(None)  # type: ignore

        # Test wrong type
        commander = Commander(faction=Faction.ARBOREC, player_id="player1")
        with pytest.raises(ValueError, match="agent must be a Agent instance"):
            sheet.set_agent(commander)  # type: ignore

    def test_set_agent_validates_player_ownership(self) -> None:
        """Test set_agent validates agent belongs to correct player."""
        # RED: Test player ownership validation
        sheet = LeaderSheet(player_id="player1")
        agent = Agent(faction=Faction.ARBOREC, player_id="player2")

        with pytest.raises(
            ValueError,
            match="Agent belongs to player player2, but sheet belongs to player player1",
        ):
            sheet.set_agent(agent)

    def test_set_commander(self) -> None:
        """Test set_commander assigns commander correctly."""
        # RED: Test commander assignment
        player_id = "player1"
        faction = Faction.ARBOREC

        commander = Commander(faction=faction, player_id=player_id)
        sheet = LeaderSheet(player_id=player_id)

        sheet.set_commander(commander)
        assert sheet.commander == commander

    def test_set_commander_validates_input(self) -> None:
        """Test set_commander validates commander parameter."""
        # RED: Test input validation
        sheet = LeaderSheet(player_id="player1")

        with pytest.raises(ValueError, match="commander cannot be None"):
            sheet.set_commander(None)  # type: ignore

        # Test wrong type
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        with pytest.raises(ValueError, match="commander must be a Commander instance"):
            sheet.set_commander(agent)  # type: ignore

    def test_set_commander_validates_player_ownership(self) -> None:
        """Test set_commander validates commander belongs to correct player."""
        # RED: Test player ownership validation
        sheet = LeaderSheet(player_id="player1")
        commander = Commander(faction=Faction.ARBOREC, player_id="player2")

        with pytest.raises(
            ValueError,
            match="Commander belongs to player player2, but sheet belongs to player player1",
        ):
            sheet.set_commander(commander)

    def test_set_hero(self) -> None:
        """Test set_hero assigns hero correctly."""
        # RED: Test hero assignment
        player_id = "player1"
        faction = Faction.ARBOREC

        hero = Hero(faction=faction, player_id=player_id)
        sheet = LeaderSheet(player_id=player_id)

        sheet.set_hero(hero)
        assert sheet.hero == hero

    def test_set_hero_validates_input(self) -> None:
        """Test set_hero validates hero parameter."""
        # RED: Test input validation
        sheet = LeaderSheet(player_id="player1")

        with pytest.raises(ValueError, match="hero cannot be None"):
            sheet.set_hero(None)  # type: ignore

        # Test wrong type
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        with pytest.raises(ValueError, match="hero must be a Hero instance"):
            sheet.set_hero(agent)  # type: ignore

    def test_set_hero_validates_player_ownership(self) -> None:
        """Test set_hero validates hero belongs to correct player."""
        # RED: Test player ownership validation
        sheet = LeaderSheet(player_id="player1")
        hero = Hero(faction=Faction.ARBOREC, player_id="player2")

        with pytest.raises(
            ValueError,
            match="Hero belongs to player player2, but sheet belongs to player player1",
        ):
            sheet.set_hero(hero)

    def test_is_complete(self) -> None:
        """Test is_complete returns correct status."""
        # RED: Test completeness checking
        player_id = "player1"
        faction = Faction.ARBOREC

        sheet = LeaderSheet(player_id=player_id)

        # Empty sheet is not complete
        assert not sheet.is_complete()

        # Partial assignment is not complete
        sheet.set_agent(Agent(faction=faction, player_id=player_id))
        assert not sheet.is_complete()

        sheet.set_commander(Commander(faction=faction, player_id=player_id))
        assert not sheet.is_complete()

        # All three assigned is complete
        sheet.set_hero(Hero(faction=faction, player_id=player_id))
        assert sheet.is_complete()


class TestPlayerLeaderSheetIntegration:
    """Test cases for Player class integration with LeaderSheet."""

    def test_player_has_leader_sheet(self) -> None:
        """Test Player class has leader_sheet attribute."""
        # RED: Test Player has leader sheet
        player = Player(id="player1", faction=Faction.ARBOREC)

        assert hasattr(player, "leader_sheet")
        assert isinstance(player.leader_sheet, LeaderSheet)
        assert player.leader_sheet.player_id == "player1"

    def test_player_get_leaders(self) -> None:
        """Test Player.get_leaders returns leaders from leader sheet."""
        # RED: Test Player.get_leaders method
        player = Player(id="player1", faction=Faction.ARBOREC)

        # Initially empty
        leaders = player.get_leaders()
        assert leaders == []

        # Add a leader
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        player.leader_sheet.set_agent(agent)

        leaders = player.get_leaders()
        assert len(leaders) == 1
        assert leaders[0] == agent

    def test_player_get_leader_by_name(self) -> None:
        """Test Player.get_leader_by_name delegates to leader sheet."""
        # RED: Test Player.get_leader_by_name method
        player = Player(id="player1", faction=Faction.ARBOREC)

        # No leaders initially
        assert player.get_leader_by_name("Agent") is None

        # Add a leader
        agent = Agent(faction=Faction.ARBOREC, player_id="player1")
        player.leader_sheet.set_agent(agent)

        assert player.get_leader_by_name("Agent") == agent
        assert player.get_leader_by_name("NonExistent") is None

    def test_player_leader_sheet_initialization(self) -> None:
        """Test Player initializes leader sheet with correct player_id."""
        # RED: Test automatic initialization
        player = Player(id="test_player", faction=Faction.BARONY)

        assert player.leader_sheet.player_id == "test_player"
        assert not player.leader_sheet.is_complete()

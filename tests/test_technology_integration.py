"""Tests for technology integration with game state.

This module tests the integration between Rule 90 TechnologyManager and the game state system.
"""

import pytest

from src.ti4.actions.research_technology import ResearchTechnologyAction
from src.ti4.core.constants import Faction, Technology
from src.ti4.core.game_technology_manager import GameTechnologyManager


class MockPlayerState:
    """Mock player state for testing."""

    def __init__(self, player_id: str, faction: Faction) -> None:
        self.player_id = player_id
        self.faction = faction
        self.technologies: set[str] = set()


class MockGameState:
    """Mock game state for testing technology integration."""

    def __init__(self) -> None:
        self.players: dict[str, MockPlayerState] = {}
        self.player_technologies: dict[str, list[str]] = {}
        self.round_number = 1
        self.technology_research_history: list[dict[str, str]] = []

    def add_player(self, player_id: str, faction: Faction) -> None:
        """Add a player to the game state."""
        self.players[player_id] = MockPlayerState(player_id, faction)
        self.player_technologies[player_id] = []

    def get_player_state(self, player_id: str) -> MockPlayerState | None:
        """Get the state of a specific player."""
        return self.players.get(player_id)

    def get_technology_research_history(self) -> list[dict[str, str]]:
        """Get the history of technology research actions."""
        return self.technology_research_history

    def add_technology_research_event(
        self, player_id: str, technology: str, round_number: int
    ) -> None:
        """Add a technology research event to the history."""
        event = {
            "player_id": player_id,
            "technology": technology,
            "round_number": str(round_number),
        }
        self.technology_research_history.append(event)

    def validate_consistency(self) -> list[str]:
        """Validate internal consistency of game state."""
        return []  # No errors for mock


class TestTechnologyGameStateIntegration:
    """Test technology integration with game state."""

    def test_game_technology_manager_creation(self) -> None:
        """Test that GameTechnologyManager can be created with game state."""
        game_state = MockGameState()
        game_state.add_player("player1", Faction.SOL)

        game_tech_manager = GameTechnologyManager(game_state)
        assert game_tech_manager is not None
        assert game_tech_manager.game_state == game_state

    def test_sync_existing_technologies_from_game_state(self) -> None:
        """Test that existing technologies in game state are synced to technology manager."""
        game_state = MockGameState()
        game_state.add_player("player1", Faction.SOL)

        # Add some technologies to game state
        player_state = game_state.get_player_state("player1")
        assert player_state is not None
        player_state.technologies = {"antimass_deflectors", "gravity_drive"}

        # Create game technology manager
        game_tech_manager = GameTechnologyManager(game_state)

        # Check that technologies were synced
        player_technologies = game_tech_manager.get_player_technologies("player1")
        assert Technology.ANTIMASS_DEFLECTORS in player_technologies
        assert Technology.GRAVITY_DRIVE in player_technologies

    def test_research_technology_updates_game_state(self) -> None:
        """Test that researching technology updates both systems."""
        game_state = MockGameState()
        game_state.add_player("player1", Faction.SOL)

        game_tech_manager = GameTechnologyManager(game_state)

        # Research a technology with no prerequisites
        success = game_tech_manager.research_technology(
            "player1", Technology.ANTIMASS_DEFLECTORS
        )
        assert success is True

        # Check that both systems are updated
        player_state = game_state.get_player_state("player1")
        assert player_state is not None
        assert "antimass_deflectors" in player_state.technologies
        assert "antimass_deflectors" in game_state.player_technologies["player1"]

        # Note: Research history tracking would be handled by the game controller
        # that manages GameState transitions, not by the GameTechnologyManager directly

    def test_research_technology_action_integration(self) -> None:
        """Test that ResearchTechnologyAction works with integrated system."""
        game_state = MockGameState()
        game_state.add_player("player1", Faction.SOL)

        # Create research action
        action = ResearchTechnologyAction(technology=Technology.ANTIMASS_DEFLECTORS)

        # Check that action is legal
        assert action.is_legal(game_state, "player1") is True

        # Execute action
        new_state = action.execute(game_state, "player1")

        # Check that technology was added
        player_state = new_state.get_player_state("player1")
        assert player_state is not None
        assert "antimass_deflectors" in player_state.technologies

    def test_prerequisite_validation_integration(self) -> None:
        """Test that prerequisite validation works through game state integration."""
        game_state = MockGameState()
        game_state.add_player("player1", Faction.SOL)

        # Try to research technology with prerequisites
        action = ResearchTechnologyAction(technology=Technology.CRUISER_II)

        # Should not be legal without prerequisites
        assert action.is_legal(game_state, "player1") is False

        # Should raise error when trying to execute
        with pytest.raises(ValueError, match="prerequisites not met"):
            action.execute(game_state, "player1")

    def test_technology_deck_integration(self) -> None:
        """Test that technology deck works with game state integration."""
        game_state = MockGameState()
        game_state.add_player("player1", Faction.SOL)

        game_tech_manager = GameTechnologyManager(game_state)

        # Get initial deck
        deck = game_tech_manager.get_technology_deck("player1")
        assert Technology.ANTIMASS_DEFLECTORS in deck
        assert Technology.CRUISER_II in deck

        # Research a technology
        game_tech_manager.research_technology("player1", Technology.ANTIMASS_DEFLECTORS)

        # Check that deck is updated
        new_deck = game_tech_manager.get_technology_deck("player1")
        assert Technology.ANTIMASS_DEFLECTORS not in new_deck
        assert Technology.CRUISER_II in new_deck

    def test_unit_upgrade_identification_integration(self) -> None:
        """Test that unit upgrade identification works through integration."""
        game_state = MockGameState()
        game_state.add_player("player1", Faction.SOL)

        game_tech_manager = GameTechnologyManager(game_state)

        # Test unit upgrade identification
        assert game_tech_manager.is_unit_upgrade(Technology.CRUISER_II) is True
        assert game_tech_manager.is_unit_upgrade(Technology.FIGHTER_II) is True
        assert (
            game_tech_manager.is_unit_upgrade(Technology.ANTIMASS_DEFLECTORS) is False
        )
        assert game_tech_manager.is_unit_upgrade(Technology.GRAVITY_DRIVE) is False

    def test_technology_color_integration(self) -> None:
        """Test that technology color system works through integration."""
        game_state = MockGameState()
        game_state.add_player("player1", Faction.SOL)

        game_tech_manager = GameTechnologyManager(game_state)

        # Test color identification
        assert (
            game_tech_manager.get_technology_color(Technology.ANTIMASS_DEFLECTORS)
            == "blue"
        )
        assert (
            game_tech_manager.get_technology_color(Technology.GRAVITY_DRIVE) == "blue"
        )

        # Unit upgrades should return None (no color)
        assert game_tech_manager.get_technology_color(Technology.CRUISER_II) is None
        assert game_tech_manager.get_technology_color(Technology.FIGHTER_II) is None

    def test_multiple_players_technology_isolation(self) -> None:
        """Test that technology ownership is properly isolated between players."""
        game_state = MockGameState()
        game_state.add_player("player1", Faction.SOL)
        game_state.add_player("player2", Faction.HACAN)

        game_tech_manager = GameTechnologyManager(game_state)

        # Player 1 researches a technology
        game_tech_manager.research_technology("player1", Technology.ANTIMASS_DEFLECTORS)

        # Check that only player 1 has the technology
        player1_techs = game_tech_manager.get_player_technologies("player1")
        player2_techs = game_tech_manager.get_player_technologies("player2")

        assert Technology.ANTIMASS_DEFLECTORS in player1_techs
        assert Technology.ANTIMASS_DEFLECTORS not in player2_techs

        # Check that decks are updated correctly
        player1_deck = game_tech_manager.get_technology_deck("player1")
        player2_deck = game_tech_manager.get_technology_deck("player2")

        assert Technology.ANTIMASS_DEFLECTORS not in player1_deck
        assert Technology.ANTIMASS_DEFLECTORS in player2_deck

    def test_unconfirmed_technologies_integration(self) -> None:
        """Test that unconfirmed technologies are handled properly in integration."""
        game_state = MockGameState()
        game_state.add_player("player1", Faction.SOL)

        game_tech_manager = GameTechnologyManager(game_state)

        # Get unconfirmed technologies
        unconfirmed = game_tech_manager.get_unconfirmed_technologies()
        assert len(unconfirmed) > 0

        # Should not be able to research unconfirmed technologies
        # (They should raise ValueError when trying to check prerequisites)
        for tech in unconfirmed:
            with pytest.raises(ValueError, match="prerequisites not confirmed"):
                game_tech_manager.can_research_technology("player1", tech)

    def test_game_state_consistency_validation(self) -> None:
        """Test that game state consistency is maintained after technology operations."""
        game_state = MockGameState()
        game_state.add_player("player1", Faction.SOL)

        game_tech_manager = GameTechnologyManager(game_state)

        # Research some technologies
        game_tech_manager.research_technology("player1", Technology.ANTIMASS_DEFLECTORS)
        game_tech_manager.research_technology("player1", Technology.GRAVITY_DRIVE)

        # Validate consistency
        errors = game_state.validate_consistency()
        assert len(errors) == 0  # Should have no consistency errors

        # Check that sync worked properly
        player_state = game_state.get_player_state("player1")
        assert player_state is not None
        assert len(player_state.technologies) == 2
        assert len(game_state.player_technologies["player1"]) == 2

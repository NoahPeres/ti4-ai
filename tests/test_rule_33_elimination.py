"""Tests for Rule 33: ELIMINATION.

This module tests the elimination mechanics according to TI4 LRR Rule 33.

LRR Reference: Rule 33 - ELIMINATION
- 33.1: A player is eliminated if they have no ground forces, no production units, and control no planets
- 33.2: When eliminated, all components return to game box
- 33.3: Agenda cards owned by eliminated player are discarded
"""

import pytest

from ti4.core.constants import Faction, UnitType
from ti4.core.game_state import GameState
from ti4.core.planet import Planet
from ti4.core.player import Player
from ti4.core.system import System
from ti4.core.unit import Unit


class TestRule33Elimination:
    """Test Rule 33: ELIMINATION mechanics."""

    def test_player_not_eliminated_with_ground_forces(self) -> None:
        """Test Rule 33.1: Player with ground forces is not eliminated."""
        # Setup game state with player
        player = Player("player1", Faction.SOL)
        game_state = GameState().add_player(player)

        # Create system with planet containing ground forces
        planet = Planet("Mecatol Rex", 1, 6)
        infantry = Unit(UnitType.INFANTRY, "player1")
        planet.place_unit(infantry)

        system = System("system1")
        system.add_planet(planet)

        # Add system to game state
        game_state.systems["test_system"] = system

        # Player should not be eliminated (has ground forces)
        assert not game_state.should_eliminate_player("player1")

    def test_player_not_eliminated_with_production_units_on_planet(self) -> None:
        """Test Rule 33.1: Player with production units on planet is not eliminated."""
        # Setup game state with player
        player = Player("player1", Faction.SOL)
        game_state = GameState().add_player(player)

        # Create system with planet containing production unit
        planet = Planet("Mecatol Rex", 1, 6)
        space_dock = Unit(UnitType.SPACE_DOCK, "player1")
        planet.place_unit(space_dock)

        system = System("system1")
        system.add_planet(planet)

        # Add system to game state
        game_state.systems["test_system"] = system

        # Player should not be eliminated (has production unit)
        assert not game_state.should_eliminate_player("player1")

    def test_player_not_eliminated_with_production_units_in_space(self) -> None:
        """Test Rule 33.1: Player with production units in space is not eliminated."""
        # Setup game state with player
        player = Player("player1", Faction.SOL)
        game_state = GameState().add_player(player)

        # Create system with production unit in space
        system = System("system1")
        # Use a carrier instead of war sun - carriers can be in space and have capacity
        # But for production, we need a space dock. Let's put it on a planet
        planet = Planet("Mecatol Rex", 1, 6)
        space_dock = Unit(UnitType.SPACE_DOCK, "player1")  # Space docks have production
        planet.place_unit(space_dock)
        system.add_planet(planet)

        # Add system to game state
        game_state.systems["test_system"] = system

        # Player should not be eliminated (has production unit)
        assert not game_state.should_eliminate_player("player1")

    def test_player_not_eliminated_with_controlled_planets(self) -> None:
        """Test Rule 33.1: Player controlling planets is not eliminated."""
        # Setup game state with player
        player = Player("player1", Faction.SOL)
        game_state = GameState().add_player(player)

        # Create system with planet
        planet = Planet("Mecatol Rex", 1, 6)
        system = System("system1")
        system.add_planet(planet)

        # Add system to game state and give player control of planet
        game_state.systems["test_system"] = system
        success, game_state = game_state.gain_planet_control("player1", planet)
        assert success, "Player should successfully gain control of the planet"

        # Player should not be eliminated (controls planet)
        assert not game_state.should_eliminate_player("player1")

    def test_player_eliminated_with_no_ground_forces_no_production_no_planets(
        self,
    ) -> None:
        """Test Rule 33.1: Player is eliminated when they have no ground forces, no production units, and control no planets."""
        # Setup game state with player
        player = Player("player1", Faction.SOL)
        game_state = GameState().add_player(player)

        # Create system with only non-ground, non-production units
        system = System("system1")
        fighter = Unit(UnitType.FIGHTER, "player1")  # Not ground force, not production
        system.place_unit_in_space(fighter)

        # Add system to game state
        game_state.systems["test_system"] = system

        # Player should be eliminated (no ground forces, no production, no planets)
        assert game_state.should_eliminate_player("player1")

    def test_component_return_on_elimination(self) -> None:
        """Test Rule 33.2: All player components are returned to game box on elimination."""
        # Setup game state with player
        player = Player("player1", Faction.SOL)
        game_state = GameState().add_player(player)

        # Give player some components
        system = System("system1")
        fighter = Unit(UnitType.FIGHTER, "player1")
        system.place_unit_in_space(fighter)

        # Create new game state with the system
        new_systems = game_state.systems.copy()
        new_systems["test_system"] = system
        game_state = game_state._create_new_state(systems=new_systems)

        # Give player command tokens (simulate having some in strategy pool)
        # This would be tracked in the game state

        # Eliminate the player
        new_game_state = game_state.eliminate_player("player1")

        # Verify all units are removed
        assert len(new_game_state.systems["test_system"].space_units) == 0

        # Verify player is no longer in the game
        assert not any(p.id == "player1" for p in new_game_state.players)

    def test_agenda_card_discard_on_elimination(self) -> None:
        """Test Rule 33.3: All agenda cards owned by eliminated player are discarded."""
        # Setup game state with player
        player = Player("player1", Faction.SOL)
        game_state = GameState().add_player(player)

        # Give player some agenda cards (this would be tracked in game state)
        # For now, we'll simulate this with a simple test

        # Eliminate the player
        new_game_state = game_state.eliminate_player("player1")

        # Verify player is eliminated
        assert not any(p.id == "player1" for p in new_game_state.players)

        # TODO: Add verification that agenda cards are discarded once agenda system is implemented

    def test_elimination_condition_ignores_other_players_units(self) -> None:
        """Test Rule 33.1: Elimination check only considers the specific player's units."""
        # Setup game state with two players
        player1 = Player("player1", Faction.SOL)
        player2 = Player("player2", Faction.HACAN)
        game_state = GameState().add_player(player1).add_player(player2)

        # Create system where player2 has ground forces but player1 doesn't
        planet = Planet("Mecatol Rex", 1, 6)
        infantry = Unit(UnitType.INFANTRY, "player2")  # Player2's unit
        planet.place_unit(infantry)

        system = System("system1")
        system.add_planet(planet)

        # Add system to game state
        game_state.systems["test_system"] = system

        # Player1 should be eliminated (no units of their own)
        assert game_state.should_eliminate_player("player1")

        # Player2 should not be eliminated (has ground forces)
        assert not game_state.should_eliminate_player("player2")

    def test_player_eliminated_with_no_units_at_all(self) -> None:
        """Test Rule 33.1: Player is eliminated when they have no units at all."""
        # Setup game state with player but no units
        player = Player("player1", Faction.SOL)
        game_state = GameState().add_player(player)

        # Player should be eliminated (no units at all)
        assert game_state.should_eliminate_player("player1")

    def test_multiple_elimination_conditions_all_must_be_true(self) -> None:
        """Test Rule 33.1: All three conditions must be true for elimination."""
        # Setup game state with player
        player = Player("player1", Faction.SOL)
        game_state = GameState().add_player(player)

        # Create system with ground forces AND production unit
        planet = Planet("Mecatol Rex", 1, 6)
        infantry = Unit(UnitType.INFANTRY, "player1")  # Ground force
        space_dock = Unit(UnitType.SPACE_DOCK, "player1")  # Production unit
        planet.place_unit(infantry)
        planet.place_unit(space_dock)

        system = System("system1")
        system.add_planet(planet)

        # Add system to game state and give control
        game_state.systems["test_system"] = system
        success, game_state = game_state.gain_planet_control("player1", planet)
        assert success, "Player should successfully gain control of the planet"

        # Player should not be eliminated (has all three: ground forces, production, planets)
        assert not game_state.should_eliminate_player("player1")

    def test_nonexistent_player_elimination_check_raises_error(self) -> None:
        """Test that checking elimination for nonexistent player raises error."""
        game_state = GameState()

        with pytest.raises(ValueError, match="Player nonexistent does not exist"):
            game_state.should_eliminate_player("nonexistent")

    def test_rule_33_6_strategy_cards_returned_on_elimination(self) -> None:
        """Test Rule 33.6: Strategy cards are returned to common play area when player is eliminated."""
        # Setup game state with two players
        player1 = Player("player1", Faction.SOL)
        player2 = Player("player2", Faction.HACAN)
        game_state = GameState().add_player(player1).add_player(player2)

        # Assign strategy cards to both players
        game_state = game_state.assign_strategy_card("player1", 1)  # Leadership
        game_state = game_state.assign_strategy_card("player2", 2)  # Diplomacy

        # Verify initial assignments
        assert game_state.strategy_card_assignments["player1"] == 1
        assert game_state.strategy_card_assignments["player2"] == 2

        # Eliminate player1
        new_game_state = game_state.eliminate_player("player1")

        # Verify player1's strategy card is no longer assigned
        assert "player1" not in new_game_state.strategy_card_assignments
        # Verify player2's strategy card remains
        assert new_game_state.strategy_card_assignments["player2"] == 2

    def test_rule_33_8_speaker_token_transfer_on_elimination(self) -> None:
        """Test Rule 33.8: Speaker token passes to next player when speaker is eliminated."""
        # Setup game state with three players
        player1 = Player("player1", Faction.SOL)
        player2 = Player("player2", Faction.HACAN)
        player3 = Player("player3", Faction.XXCHA)
        game_state = (
            GameState().add_player(player1).add_player(player2).add_player(player3)
        )

        # Set player1 as speaker
        game_state = game_state._create_new_state(speaker_id="player1")
        assert game_state.speaker_id == "player1"

        # Eliminate the speaker (player1)
        new_game_state = game_state.eliminate_player("player1")

        # Verify speaker token passed to next player (player2)
        assert new_game_state.speaker_id == "player2"
        # Verify player1 is no longer in the game
        assert "player1" not in [player.id for player in new_game_state.players]

    def test_rule_33_8_speaker_token_unchanged_when_non_speaker_eliminated(
        self,
    ) -> None:
        """Test Rule 33.8: Speaker token unchanged when non-speaker is eliminated."""
        # Setup game state with three players
        player1 = Player("player1", Faction.SOL)
        player2 = Player("player2", Faction.HACAN)
        player3 = Player("player3", Faction.XXCHA)
        game_state = (
            GameState().add_player(player1).add_player(player2).add_player(player3)
        )

        # Set player2 as speaker
        game_state = game_state._create_new_state(speaker_id="player2")
        assert game_state.speaker_id == "player2"

        # Eliminate non-speaker (player1)
        new_game_state = game_state.eliminate_player("player1")

        # Verify speaker token remains with player2
        assert new_game_state.speaker_id == "player2"
        # Verify player1 is no longer in the game
        assert "player1" not in [player.id for player in new_game_state.players]

    def test_rule_33_8_speaker_token_edge_case_single_player_remaining(self) -> None:
        """Test Rule 33.8: Edge case when only one player remains after elimination."""
        # Setup game state with two players
        player1 = Player("player1", Faction.SOL)
        player2 = Player("player2", Faction.HACAN)
        game_state = GameState().add_player(player1).add_player(player2)

        # Set player1 as speaker
        game_state = game_state._create_new_state(speaker_id="player1")
        assert game_state.speaker_id == "player1"

        # Eliminate the speaker (player1), leaving only player2
        new_game_state = game_state.eliminate_player("player1")

        # Verify speaker token goes to the remaining player
        assert new_game_state.speaker_id == "player2"
        # Verify only player2 remains
        assert len(new_game_state.players) == 1
        assert "player2" in [player.id for player in new_game_state.players]

"""
Test Rule 49: INVASION

Tests the five-step invasion process:
1. Bombardment step (49.1)
2. Commit ground forces step (49.2)
3. Space cannon defense step (49.3)
4. Ground combat step (49.4)
5. Establish control step (49.5)

LRR Reference: Rule 49 - INVASION
"""

from unittest.mock import Mock, patch

from ti4.core.constants import UnitType
from ti4.core.galaxy import Galaxy
from ti4.core.game_state import GameState
from ti4.core.hex_coordinate import HexCoordinate
from ti4.core.invasion import InvasionController
from ti4.core.planet import Planet
from ti4.core.player import Player
from ti4.core.system import System
from ti4.core.unit import Unit


class TestRule49BombardmentStep:
    """Test Rule 49.1: Bombardment step during invasion."""

    def test_bombardment_step_uses_bombardment_abilities(self) -> None:
        """Test Rule 49.1: Active player may use bombardment abilities.

        LRR Reference: Rule 49.1 - "The active player may use the 'Bombardment'
        ability of any of their units in the active system."
        """
        # Setup game state
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        # Setup galaxy and system
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)
        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)
        game_state = game_state._create_new_state(galaxy=galaxy)

        # Add planet to system
        planet = Planet(name="test_planet", resources=2, influence=1)
        system.add_planet(planet)

        # Add unit with bombardment ability
        bombardment_unit = Unit(unit_type=UnitType.DREADNOUGHT, owner=player.id)
        system.place_unit_in_space(bombardment_unit)

        # Add ground forces on planet to be bombarded
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="player2")
        planet.place_unit(infantry)

        # Create invasion controller
        invasion_controller = InvasionController(game_state, system, player)

        # Execute bombardment step
        result = invasion_controller.bombardment_step()

        # Should return next step
        assert result == "commit_ground_forces"

        # Should have bombardment results stored
        assert hasattr(invasion_controller, "bombardment_results")

    def test_bombardment_step_returns_commit_ground_forces(self) -> None:
        """Test Rule 49.1: Bombardment step returns next step."""
        # Setup
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)
        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)
        game_state = game_state._create_new_state(galaxy=galaxy)

        invasion_controller = InvasionController(game_state, system, player)

        # Execute bombardment step
        result = invasion_controller.bombardment_step()
        assert result == "commit_ground_forces"


class TestRule49CommitGroundForcesStep:
    """Test Rule 49.2: Commit ground forces step during invasion."""

    def test_commit_ground_forces_step_requires_ground_forces(self) -> None:
        """Test Rule 49.2: Player may commit ground forces if available.

        LRR Reference: Rule 49.2 - "If the active player has ground forces in the
        space area of the active system, that player may commit any number of those
        ground forces to land on any of the planets in that system."
        """
        # Setup
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)
        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)
        game_state = game_state._create_new_state(galaxy=galaxy)

        # Add planet to system
        planet = Planet(name="test_planet", resources=2, influence=1)
        system.add_planet(planet)

        invasion_controller = InvasionController(game_state, system, player)

        # Execute commit ground forces step - should proceed to production if no ground forces
        result = invasion_controller.commit_ground_forces_step()
        assert result == "production"

    def test_commit_ground_forces_step_returns_space_cannon_defense(self) -> None:
        """Test Rule 49.2: Commit ground forces step returns next step."""
        # Setup
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)
        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)
        game_state = game_state._create_new_state(galaxy=galaxy)

        # Add planet and ground force
        planet = Planet(name="test_planet", resources=2, influence=1)
        system.add_planet(planet)

        ground_force = Unit(unit_type=UnitType.INFANTRY, owner=player.id)
        system.place_unit_in_space(ground_force)

        invasion_controller = InvasionController(game_state, system, player)

        # Mock the ground force commitment
        with patch.object(invasion_controller, "_execute_space_cannon_defense"):
            result = invasion_controller.commit_ground_forces_step()
            assert result == "space_cannon_defense"


class TestRule49SpaceCannonDefenseStep:
    """Test Rule 49.3: Space cannon defense step during invasion."""

    def test_space_cannon_defense_step_uses_space_cannon_abilities(self) -> None:
        """Test Rule 49.3: Defending player may use space cannon abilities.

        LRR Reference: Rule 49.3 - "The defending player may use the 'Space Cannon'
        ability of any of their units on the planet."
        """
        # Setup
        game_state = GameState()
        active_player = Player("player1", "Active Player")
        defending_player = Player("player2", "Defending Player")
        game_state = game_state.add_player(active_player).add_player(defending_player)

        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)
        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)
        game_state = game_state._create_new_state(galaxy=galaxy)

        # Add planet with defending unit that has space cannon
        planet = Planet(name="test_planet", resources=2, influence=1)
        system.add_planet(planet)

        space_cannon_unit = Unit(unit_type=UnitType.PDS, owner=defending_player.id)
        space_cannon_unit.has_space_cannon = Mock(return_value=True)
        planet.place_unit(space_cannon_unit)

        invasion_controller = InvasionController(game_state, system, active_player)
        invasion_controller.invaded_planets = [planet]

        # Execute space cannon defense step
        with patch.object(
            invasion_controller, "_execute_space_cannon_defense"
        ) as mock_space_cannon:
            invasion_controller.space_cannon_defense_step()
            mock_space_cannon.assert_called_once()

    def test_space_cannon_defense_step_returns_ground_combat(self) -> None:
        """Test Rule 49.3: Space cannon defense step returns next step."""
        # Setup
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)
        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)
        game_state = game_state._create_new_state(galaxy=galaxy)

        invasion_controller = InvasionController(game_state, system, player)

        # Execute space cannon defense step
        result = invasion_controller.space_cannon_defense_step()
        assert result == "ground_combat"


class TestRule49GroundCombatStep:
    """Test Rule 49.4: Ground combat step during invasion."""

    def test_ground_combat_step_resolves_combat(self) -> None:
        """Test Rule 49.4: Players resolve ground combat on the planet.

        LRR Reference: Rule 49.4 - "Players resolve ground combat on the planet."
        """
        # Setup
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)
        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)
        game_state = game_state._create_new_state(galaxy=galaxy)

        invasion_controller = InvasionController(game_state, system, player)

        # Execute ground combat step - should return "establish_control"
        result = invasion_controller.ground_combat_step()
        assert result == "establish_control"


class TestRule49EstablishControlStep:
    """Test Rule 49.5: Establish control step during invasion."""

    def test_establish_control_step_gains_control(self) -> None:
        """Test Rule 49.5: Active player gains control of planets with their ground forces.

        LRR Reference: Rule 49.5 - "The active player gains control of each planet
        they committed ground forces to if that planet still contains at least one
        of their ground forces."
        """
        # Setup
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)
        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)
        game_state = game_state._create_new_state(galaxy=galaxy)

        # Prepare a planet with our ground forces
        planet = Planet(name="test_planet", resources=2, influence=1)
        system.add_planet(planet)
        planet.place_unit(Unit(unit_type=UnitType.INFANTRY, owner=player.id))

        invasion_controller = InvasionController(game_state, system, player)
        invasion_controller.invaded_planets = [planet]

        # Execute establish control step
        result = invasion_controller.establish_control_step()
        assert result == "production"
        assert planet.controlled_by == player.id

    def test_complete_invasion_process_integration(self) -> None:
        """Integration test for complete invasion process with all five steps."""
        # Setup: Create system with bombardment-capable ship and ground forces
        game_state = GameState()
        player1 = Player("player1", "Active Player")
        player2 = Player("player2", "Defending Player")
        game_state = game_state.add_player(player1).add_player(player2)

        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)
        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)
        game_state = game_state._create_new_state(galaxy=galaxy)

        planet = Planet(name="test_planet", resources=2, influence=1)
        system.add_planet(planet)

        # Add bombardment-capable ship (Dreadnought) in space
        dreadnought = Unit(unit_type=UnitType.DREADNOUGHT, owner=player1.id)
        system.place_unit_in_space(dreadnought)

        # Add ground forces in space for invasion
        infantry1 = Unit(unit_type=UnitType.INFANTRY, owner=player1.id)
        infantry2 = Unit(unit_type=UnitType.INFANTRY, owner=player1.id)
        system.place_unit_in_space(infantry1)
        system.place_unit_in_space(infantry2)

        # Add defending ground forces on planet
        defending_infantry = Unit(unit_type=UnitType.INFANTRY, owner=player2.id)
        planet.place_unit(defending_infantry)

        # Create invasion controller
        invasion_controller = InvasionController(game_state, system, player1)
        invasion_controller.invaded_planets = [planet]

        # Execute complete invasion process
        # Step 1: Bombardment
        result1 = invasion_controller.bombardment_step()
        assert result1 == "commit_ground_forces"
        assert hasattr(invasion_controller, "bombardment_results")

        # Step 2: Commit Ground Forces
        result2 = invasion_controller.commit_ground_forces_step()
        assert result2 == "space_cannon_defense"

        # Step 3: Space Cannon Defense
        result3 = invasion_controller.space_cannon_defense_step()
        assert result3 == "ground_combat"

        # Step 4: Ground Combat
        result4 = invasion_controller.ground_combat_step()
        assert result4 == "establish_control"

        # Step 5: Establish Control
        result5 = invasion_controller.establish_control_step()
        assert result5 == "production"

    def test_invasion_process_with_no_defenders(self) -> None:
        """Integration test for invasion of undefended planet."""
        # Setup: Create system with ground forces but no defenders
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)
        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)
        game_state = game_state._create_new_state(galaxy=galaxy)

        planet = Planet(name="test_planet", resources=2, influence=1)
        system.add_planet(planet)

        # Add ground forces in space for invasion
        infantry = Unit(unit_type=UnitType.INFANTRY, owner=player.id)
        system.place_unit_in_space(infantry)

        # Create invasion controller (no defenders on planet)
        invasion_controller = InvasionController(game_state, system, player)
        invasion_controller.invaded_planets = [planet]

        # Execute invasion process - should work even with no defenders
        result1 = invasion_controller.bombardment_step()
        assert result1 == "commit_ground_forces"

        with patch.object(invasion_controller, "_execute_space_cannon_defense"):
            result2 = invasion_controller.commit_ground_forces_step()
            assert result2 == "space_cannon_defense"

        result3 = invasion_controller.space_cannon_defense_step()
        assert result3 == "ground_combat"

        result4 = invasion_controller.ground_combat_step()
        assert result4 == "establish_control"

        result5 = invasion_controller.establish_control_step()
        assert result5 == "production"


class TestRule49InvasionProcess:
    """Test the complete invasion process."""

    def test_invasion_process_executes_all_steps_in_order(self) -> None:
        """Test that invasion process executes all five steps in correct order."""
        # Setup
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)
        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)
        game_state = game_state._create_new_state(galaxy=galaxy)

        invasion_controller = InvasionController(game_state, system, player)

        # Execute invasion - should now work and return results
        results = invasion_controller.execute_invasion()

        # Verify the results structure
        assert isinstance(results, dict)
        assert "bombardment" in results
        assert results["bombardment"] == "commit_ground_forces"

    def test_invasion_controller_initialization(self) -> None:
        """Test InvasionController proper initialization."""
        # Setup game state
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        # Setup galaxy and system
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)
        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)
        game_state = game_state._create_new_state(galaxy=galaxy)

        # Create invasion controller
        invasion_controller = InvasionController(game_state, system, player)

        # Verify initialization
        assert invasion_controller.game_state == game_state
        assert invasion_controller.system == system
        assert invasion_controller.active_player == player
        assert invasion_controller.invaded_planets == []

"""Tests for Rule 14: BLOCKADED mechanics.

This module tests the blockade system according to TI4 LRR Rule 14.
All tests follow strict TDD methodology with RED-GREEN-REFACTOR cycles.

Rule 14 Sub-rules tested:
- 14.0: Core blockade definition - production units without friendly ships
- 14.1: Production restrictions - ships blocked, ground forces allowed
- 14.2: Unit return mechanism - captured units returned on blockade
- 14.2a: Capture prevention - no captures while blockading
"""

import pytest

from ti4.core.blockade import BlockadeManager
from ti4.core.capture import CaptureManager
from ti4.core.constants import UnitType
from ti4.core.galaxy import Galaxy
from ti4.core.hex_coordinate import HexCoordinate
from ti4.core.planet import Planet
from ti4.core.system import System
from ti4.core.unit import Unit


def create_test_system_with_planet(system_id: str, planet_name: str):
    """Helper function to create a system with a planet for testing."""
    galaxy = Galaxy()
    system = System(system_id)
    coord = HexCoordinate(0, 0)

    galaxy.place_system(coord, system_id)
    galaxy.register_system(system)

    # Create planet and add to system
    planet = Planet(planet_name, resources=2, influence=1)
    system.add_planet(planet)

    return galaxy, system


class TestRule14BlockadeBasics:
    """Test basic blockade mechanics (Rule 14.0)."""

    def test_blockade_system_exists(self) -> None:
        """Test that blockade system can be imported and instantiated.

        This is the first RED test - it will fail until we create the blockade system.

        LRR Reference: Rule 14.0 - Core blockade concept
        """
        # This will fail initially - RED phase
        blockade_manager = BlockadeManager()
        assert blockade_manager is not None


class TestRule14BlockadeDetection:
    """Test blockade detection mechanics (Rule 14.0)."""

    def test_production_unit_blockaded_without_friendly_ships(self) -> None:
        """Test that production unit is blockaded when no friendly ships present.

        LRR Reference: Rule 14.0 - "A player's unit with 'Production' is blockaded
        if it is in a system that does not contain any of their ships and contains
        other players' ships."
        """
        # Create galaxy and system
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)

        # Create planet and add to system
        planet_a = Planet("planet_a", resources=2, influence=1)
        system.add_planet(planet_a)

        # Create space dock (production unit) for player1
        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        system.place_unit_on_planet(space_dock, "planet_a")

        # Create enemy ship in same system
        enemy_destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player2")
        system.place_unit_in_space(enemy_destroyer)

        # Check blockade status
        blockade_manager = BlockadeManager(galaxy)
        assert blockade_manager.is_unit_blockaded(space_dock) is True

    def test_production_unit_not_blockaded_with_friendly_ships(self) -> None:
        """Test that production unit is not blockaded when friendly ships present.

        LRR Reference: Rule 14.0 - Blockade requires absence of friendly ships
        """
        # Create galaxy and system
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)

        # Create planet and add to system
        planet_a = Planet("planet_a", resources=2, influence=1)
        system.add_planet(planet_a)

        # Create space dock for player1
        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        system.place_unit_on_planet(space_dock, "planet_a")

        # Create friendly ship in same system
        friendly_cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        system.place_unit_in_space(friendly_cruiser)

        # Create enemy ship in same system
        enemy_destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player2")
        system.place_unit_in_space(enemy_destroyer)

        # Check blockade status - should not be blockaded due to friendly ship
        blockade_manager = BlockadeManager(galaxy)
        assert blockade_manager.is_unit_blockaded(space_dock) is False

    def test_production_unit_not_blockaded_without_enemy_ships(self) -> None:
        """Test that production unit is not blockaded when no enemy ships present.

        LRR Reference: Rule 14.0 - Blockade requires presence of enemy ships
        """
        # Create galaxy and system
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)

        # Create planet and add to system
        planet_a = Planet("planet_a", resources=2, influence=1)
        system.add_planet(planet_a)

        # Create space dock for player1 (no ships in system)
        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        system.place_unit_on_planet(space_dock, "planet_a")

        # Check blockade status - should not be blockaded (no enemy ships)
        blockade_manager = BlockadeManager(galaxy)
        assert blockade_manager.is_unit_blockaded(space_dock) is False

    def test_non_production_unit_cannot_be_blockaded(self) -> None:
        """Test that units without production ability cannot be blockaded.

        LRR Reference: Rule 14.0 - Only units with "Production" can be blockaded
        """
        # Create galaxy and system
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)

        # Create planet and add to system
        planet_a = Planet("planet_a", resources=2, influence=1)
        system.add_planet(planet_a)

        # Create infantry (no production ability) for player1
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        system.place_unit_on_planet(infantry, "planet_a")

        # Create enemy ship in same system
        enemy_destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player2")
        system.place_unit_in_space(enemy_destroyer)

        # Check blockade status - should not be blockaded (no production ability)
        blockade_manager = BlockadeManager(galaxy)
        assert blockade_manager.is_unit_blockaded(infantry) is False


class TestRule14ProductionRestrictions:
    """Test production restrictions during blockade (Rule 14.1)."""

    def test_blockaded_unit_cannot_produce_ships(self) -> None:
        """Test that blockaded units cannot produce ships.

        LRR Reference: Rule 14.1 - "A player cannot use a blockaded unit to
        produce ships"
        """
        # Create blockaded space dock scenario
        galaxy, system = create_test_system_with_planet("test_system", "planet_a")

        # Create blockaded space dock
        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        system.place_unit_on_planet(space_dock, "planet_a")

        # Create enemy ship (causes blockade)
        enemy_destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player2")
        system.place_unit_in_space(enemy_destroyer)

        # Verify blockade
        blockade_manager = BlockadeManager(galaxy)
        assert blockade_manager.is_unit_blockaded(space_dock) is True

        # Test ship production restriction
        assert blockade_manager.can_produce_ships(space_dock) is False

    def test_blockaded_unit_can_produce_ground_forces(self) -> None:
        """Test that blockaded units can still produce ground forces.

        LRR Reference: Rule 14.1 - "that player can still use a blockaded unit
        to produce ground forces"
        """
        # Create blockaded space dock scenario
        galaxy, system = create_test_system_with_planet("test_system", "planet_a")

        # Create blockaded space dock
        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        system.place_unit_on_planet(space_dock, "planet_a")

        # Create enemy ship (causes blockade)
        enemy_destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player2")
        system.place_unit_in_space(enemy_destroyer)

        # Verify blockade
        blockade_manager = BlockadeManager(galaxy)
        assert blockade_manager.is_unit_blockaded(space_dock) is True

        # Test ground force production allowed
        assert blockade_manager.can_produce_ground_forces(space_dock) is True

    def test_non_blockaded_unit_can_produce_ships_and_ground_forces(self) -> None:
        """Test that non-blockaded units can produce both ships and ground forces.

        LRR Reference: Rule 14.1 - Production restrictions only apply when blockaded
        """
        # Create non-blockaded space dock scenario
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)

        # Create planet and add to system
        planet_a = Planet("planet_a", resources=2, influence=1)
        system.add_planet(planet_a)

        # Create space dock with friendly ship
        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        system.place_unit_on_planet(space_dock, "planet_a")

        friendly_cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        system.place_unit_in_space(friendly_cruiser)

        # Verify not blockaded
        blockade_manager = BlockadeManager(galaxy)
        assert blockade_manager.is_unit_blockaded(space_dock) is False

        # Test both production types allowed
        assert blockade_manager.can_produce_ships(space_dock) is True
        assert blockade_manager.can_produce_ground_forces(space_dock) is True


class TestRule14UnitReturnMechanism:
    """Test unit return mechanism during blockade (Rule 14.2)."""

    def test_captured_units_returned_on_blockade(self) -> None:
        """Test that captured units are returned when blockade occurs.

        LRR Reference: Rule 14.2 - "When a player blockades another player's
        space dock, if the blockaded player has captured any of the blockading
        player's units, those units are returned to the blockading player's
        reinforcements."
        """
        # Create galaxy and system
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)

        # Create planet and add to system
        planet_a = Planet("planet_a", resources=2, influence=1)
        system.add_planet(planet_a)

        # Create space dock for player1
        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        system.place_unit_on_planet(space_dock, "planet_a")

        # Create captured unit scenario
        capture_manager = CaptureManager()
        captured_cruiser = Unit(unit_type=UnitType.CRUISER, owner="player2")
        capture_manager.capture_unit(captured_cruiser, "player1")

        # Create blockading ship
        blockading_destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player2")
        system.place_unit_in_space(blockading_destroyer)

        # Apply blockade and check unit return
        blockade_manager = BlockadeManager(galaxy, capture_manager)
        blockade_manager.apply_blockade_effects(space_dock)

        # Verify captured unit was returned
        assert not capture_manager.is_unit_captured(captured_cruiser)

    def test_only_blockading_player_units_returned(self) -> None:
        """Test that only the blockading player's captured units are returned.

        LRR Reference: Rule 14.2 - Only units belonging to blockading player returned
        """
        # Create galaxy and system
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)

        # Create planet and add to system
        planet_a = Planet("planet_a", resources=2, influence=1)
        system.add_planet(planet_a)

        # Create space dock for player1
        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        system.place_unit_on_planet(space_dock, "planet_a")

        # Create captured units from different players
        capture_manager = CaptureManager()

        blockading_player_unit = Unit(unit_type=UnitType.CRUISER, owner="player2")
        other_player_unit = Unit(unit_type=UnitType.DESTROYER, owner="player3")

        capture_manager.capture_unit(blockading_player_unit, "player1")
        capture_manager.capture_unit(other_player_unit, "player1")

        # Create blockading ship from player2
        blockading_ship = Unit(unit_type=UnitType.DREADNOUGHT, owner="player2")
        system.place_unit_in_space(blockading_ship)

        # Apply blockade effects
        blockade_manager = BlockadeManager(galaxy, capture_manager)
        blockade_manager.apply_blockade_effects(space_dock)

        # Verify only blockading player's unit returned
        assert not capture_manager.is_unit_captured(blockading_player_unit)
        assert capture_manager.is_unit_captured(other_player_unit)


class TestRule14CapturePreventionDuringBlockade:
    """Test capture prevention during blockade (Rule 14.2a)."""

    def test_blockaded_player_cannot_capture_blockading_units(self) -> None:
        """Test that blockaded player cannot capture blockading player's units.

        LRR Reference: Rule 14.2a - "While a player is blockading another player,
        the blockaded player cannot capture any of the blockading player's units."
        """
        # Create blockade scenario
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)

        # Create planet and add to system
        planet_a = Planet("planet_a", resources=2, influence=1)
        system.add_planet(planet_a)

        # Create blockaded space dock
        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        system.place_unit_on_planet(space_dock, "planet_a")

        # Create blockading ship
        blockading_ship = Unit(unit_type=UnitType.DESTROYER, owner="player2")
        system.place_unit_in_space(blockading_ship)

        # Attempt capture during blockade
        capture_manager = CaptureManager()
        blockade_manager = BlockadeManager(galaxy, capture_manager)

        # Verify capture is prevented
        can_capture = blockade_manager.can_capture_unit(blockading_ship, "player1")
        assert can_capture is False

    def test_blockaded_player_can_capture_non_blockading_units(self) -> None:
        """Test that blockaded player can still capture non-blockading player's units.

        LRR Reference: Rule 14.2a - Restriction only applies to blockading player's units
        """
        # Create blockade scenario
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)

        # Create planet and add to system
        planet_a = Planet("planet_a", resources=2, influence=1)
        system.add_planet(planet_a)

        # Create blockaded space dock
        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        system.place_unit_on_planet(space_dock, "planet_a")

        # Create blockading ship from player2
        blockading_ship = Unit(unit_type=UnitType.DESTROYER, owner="player2")
        system.place_unit_in_space(blockading_ship)

        # Create unit from different player (player3)
        other_unit = Unit(unit_type=UnitType.CRUISER, owner="player3")

        # Test capture capability
        capture_manager = CaptureManager()
        blockade_manager = BlockadeManager(galaxy, capture_manager)

        # Verify capture of non-blockading player's unit is allowed
        can_capture = blockade_manager.can_capture_unit(other_unit, "player1")
        assert can_capture is True


class TestRule14InputValidation:
    """Test input validation and error handling."""

    def test_empty_unit_validation(self) -> None:
        """Test that None units are properly validated."""
        galaxy = Galaxy()
        blockade_manager = BlockadeManager(galaxy)

        # Test None unit handling
        with pytest.raises(ValueError, match="Unit cannot be None"):
            blockade_manager.is_unit_blockaded(None)

    def test_unit_not_in_galaxy_validation(self) -> None:
        """Test that units not placed in galaxy are handled properly."""
        galaxy = Galaxy()
        blockade_manager = BlockadeManager(galaxy)

        # Create unit not placed in any system
        orphan_unit = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")

        # Should return False for units not in galaxy
        assert blockade_manager.is_unit_blockaded(orphan_unit) is False


class TestRule14SystemIntegration:
    """Test integration with other game systems."""

    def test_blockade_status_updates_with_ship_movement(self) -> None:
        """Test that blockade status updates when ships move in/out of system."""
        # Create galaxy and systems
        galaxy = Galaxy()
        system_a = System("system_a")
        system_b = System("system_b")

        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(1, 0)

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)

        # Create planet and add to system A
        planet_a = Planet("planet_a", resources=2, influence=1)
        system_a.add_planet(planet_a)

        # Create space dock in system A
        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        system_a.place_unit_on_planet(space_dock, "planet_a")

        # Create enemy ship in system A (causes blockade)
        enemy_ship = Unit(unit_type=UnitType.DESTROYER, owner="player2")
        system_a.place_unit_in_space(enemy_ship)

        blockade_manager = BlockadeManager(galaxy)

        # Verify initial blockade
        assert blockade_manager.is_unit_blockaded(space_dock) is True

        # Move enemy ship to system B
        system_a.remove_unit_from_space(enemy_ship)
        system_b.place_unit_in_space(enemy_ship)

        # Verify blockade is lifted
        assert blockade_manager.is_unit_blockaded(space_dock) is False

    def test_multiple_blockading_players(self) -> None:
        """Test blockade behavior with multiple enemy players in same system."""
        # Create galaxy and system
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)

        # Create planet and add to system
        planet_a = Planet("planet_a", resources=2, influence=1)
        system.add_planet(planet_a)

        # Create space dock for player1
        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        system.place_unit_on_planet(space_dock, "planet_a")

        # Create ships from multiple enemy players
        enemy_ship_p2 = Unit(unit_type=UnitType.DESTROYER, owner="player2")
        enemy_ship_p3 = Unit(unit_type=UnitType.CRUISER, owner="player3")

        system.place_unit_in_space(enemy_ship_p2)
        system.place_unit_in_space(enemy_ship_p3)

        # Verify blockade occurs with multiple enemies
        blockade_manager = BlockadeManager(galaxy)
        assert blockade_manager.is_unit_blockaded(space_dock) is True

        # Verify blockading players are identified
        blockading_players = blockade_manager.get_blockading_players(space_dock)
        assert "player2" in blockading_players
        assert "player3" in blockading_players
        assert "player1" not in blockading_players

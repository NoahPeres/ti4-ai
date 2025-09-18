"""Tests for Rule 6: ADJACENCY implementation.

This module tests the adjacency rules according to LRR Rule 6:
- 6.2: Unit/Planet adjacency to systems
- 6.3: Planet adjacency to containing system
- 6.4: Hyperlane adjacency (future implementation)

Following TDD discipline: RED-GREEN-REFACTOR
"""

from src.ti4.core.constants import UnitType
from src.ti4.core.galaxy import Galaxy
from src.ti4.core.hex_coordinate import HexCoordinate
from src.ti4.core.planet import Planet
from src.ti4.core.system import System
from src.ti4.core.unit import Unit


class TestRule6UnitPlanetAdjacency:
    """Test Rule 6.2: Unit/Planet adjacency to systems.

    LRR 6.2: "A unit or planet is adjacent to all system tiles that are
    adjacent to the system tile that contains that unit or planet."

    Sub-rule 6.2a: "A system is not adjacent to itself."
    """

    def test_unit_in_space_adjacent_to_neighboring_systems(self) -> None:
        """Test that a unit in space is adjacent to systems adjacent to its containing system."""
        # Setup: Create galaxy with 3 systems in a line
        galaxy = Galaxy()

        # System A at (0,0), System B at (1,0), System C at (2,0)
        # A and B are adjacent, B and C are adjacent, A and C are not adjacent
        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(1, 0)
        coord_c = HexCoordinate(2, 0)

        system_a = System("system_a")
        system_b = System("system_b")
        system_c = System("system_c")

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.place_system(coord_c, "system_c")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)
        galaxy.register_system(system_c)

        # Place unit in system A
        unit = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        system_a.place_unit_in_space(unit)

        # Test: Unit should be adjacent to system B (adjacent to system A)
        assert galaxy.is_unit_adjacent_to_system(unit, "system_b") is True

        # Test: Unit should NOT be adjacent to system C (not adjacent to system A)
        assert galaxy.is_unit_adjacent_to_system(unit, "system_c") is False

        # Test: Unit should NOT be adjacent to its own system (Rule 6.2a)
        assert galaxy.is_unit_adjacent_to_system(unit, "system_a") is False

    def test_unit_on_planet_adjacent_to_neighboring_systems(self) -> None:
        """Test that a unit on a planet is adjacent to systems adjacent to the planet's system."""
        # Setup: Create galaxy with adjacent systems
        galaxy = Galaxy()

        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(1, 0)

        system_a = System("system_a")
        system_b = System("system_b")

        # Add planet to system A
        planet = Planet(name="Mecatol Rex", resources=1, influence=6)
        system_a.add_planet(planet)

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)

        # Place unit on planet in system A
        unit = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        system_a.place_unit_on_planet(unit, "Mecatol Rex")

        # Test: Unit on planet should be adjacent to system B
        assert galaxy.is_unit_adjacent_to_system(unit, "system_b") is True

        # Test: Unit should NOT be adjacent to its own system
        assert galaxy.is_unit_adjacent_to_system(unit, "system_a") is False

    def test_planet_adjacent_to_neighboring_systems(self) -> None:
        """Test that a planet is adjacent to systems adjacent to its containing system."""
        # Setup: Create galaxy with adjacent systems
        galaxy = Galaxy()

        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(1, 0)
        coord_c = HexCoordinate(0, 1)

        system_a = System("system_a")
        system_b = System("system_b")
        system_c = System("system_c")

        # Add planet to system A
        planet = Planet(name="Jord", resources=4, influence=2)
        system_a.add_planet(planet)

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.place_system(coord_c, "system_c")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)
        galaxy.register_system(system_c)

        # Test: Planet should be adjacent to both adjacent systems
        assert galaxy.is_planet_adjacent_to_system(planet, "system_b") is True
        assert galaxy.is_planet_adjacent_to_system(planet, "system_c") is True

        # Test: Planet SHOULD be adjacent to its own system (Rule 6.3)
        assert galaxy.is_planet_adjacent_to_system(planet, "system_a") is True

    def test_wormhole_adjacency_applies_to_units_and_planets(self) -> None:
        """Test that wormhole adjacency extends to units and planets in wormhole systems."""
        # Setup: Create galaxy with wormhole systems
        galaxy = Galaxy()

        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(3, 0)  # Distance 3, not physically adjacent

        system_a = System("system_a")
        system_b = System("system_b")

        # Add same wormhole type to both systems
        system_a.wormholes = ["alpha"]
        system_b.wormholes = ["alpha"]

        # Add planet to system A
        planet = Planet(name="Wormhole Planet", resources=2, influence=1)
        system_a.add_planet(planet)

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)

        # Place units in system A
        space_unit = Unit(unit_type=UnitType.DESTROYER, owner="player1")
        ground_unit = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        system_a.place_unit_in_space(space_unit)
        system_a.place_unit_on_planet(ground_unit, "Wormhole Planet")

        # Test: Units should be adjacent to wormhole-connected system
        assert galaxy.is_unit_adjacent_to_system(space_unit, "system_b") is True
        assert galaxy.is_unit_adjacent_to_system(ground_unit, "system_b") is True

        # Test: Planet should be adjacent to wormhole-connected system
        assert galaxy.is_planet_adjacent_to_system(planet, "system_b") is True


class TestRule6PlanetSystemAdjacency:
    """Test Rule 6.3: Planet adjacency to containing system.

    LRR 6.3: "A planet is treated as being adjacent to the system that contains that planet."
    """

    def test_planet_adjacent_to_containing_system(self) -> None:
        """Test that a planet is adjacent to its own system."""
        # Setup: Create system with planet
        galaxy = Galaxy()

        coord_a = HexCoordinate(0, 0)
        system_a = System("system_a")

        planet = Planet(name="Homeworld", resources=3, influence=4)
        system_a.add_planet(planet)

        galaxy.place_system(coord_a, "system_a")
        galaxy.register_system(system_a)

        # Test: Planet should be adjacent to its containing system
        assert galaxy.is_planet_adjacent_to_system(planet, "system_a") is True

    def test_multiple_planets_in_system_all_adjacent_to_system(self) -> None:
        """Test that all planets in a system are adjacent to that system."""
        # Setup: Create system with multiple planets
        galaxy = Galaxy()

        coord_a = HexCoordinate(0, 0)
        system_a = System("system_a")

        planet1 = Planet(name="Planet Alpha", resources=2, influence=1)
        planet2 = Planet(name="Planet Beta", resources=1, influence=2)
        system_a.add_planet(planet1)
        system_a.add_planet(planet2)

        galaxy.place_system(coord_a, "system_a")
        galaxy.register_system(system_a)

        # Test: Both planets should be adjacent to their containing system
        assert galaxy.is_planet_adjacent_to_system(planet1, "system_a") is True
        assert galaxy.is_planet_adjacent_to_system(planet2, "system_a") is True


class TestRule6EdgeCases:
    """Test edge cases and error conditions for Rule 6 adjacency."""

    def test_unit_not_in_galaxy_returns_false(self) -> None:
        """Test that adjacency check returns False for units not in the galaxy."""
        galaxy = Galaxy()

        # Create unit not placed in any system
        unit = Unit(unit_type=UnitType.FIGHTER, owner="player1")

        # Create a system
        coord_a = HexCoordinate(0, 0)
        system_a = System("system_a")
        galaxy.place_system(coord_a, "system_a")
        galaxy.register_system(system_a)

        # Test: Should return False for unit not in galaxy
        assert galaxy.is_unit_adjacent_to_system(unit, "system_a") is False

    def test_planet_not_in_galaxy_returns_false(self) -> None:
        """Test that adjacency check returns False for planets not in the galaxy."""
        galaxy = Galaxy()

        # Create planet not added to any system
        planet = Planet(name="Orphan Planet", resources=1, influence=1)

        # Create a system
        coord_a = HexCoordinate(0, 0)
        system_a = System("system_a")
        galaxy.place_system(coord_a, "system_a")
        galaxy.register_system(system_a)

        # Test: Should return False for planet not in galaxy
        assert galaxy.is_planet_adjacent_to_system(planet, "system_a") is False

    def test_nonexistent_target_system_returns_false(self) -> None:
        """Test that adjacency check returns False for nonexistent target systems."""
        galaxy = Galaxy()

        coord_a = HexCoordinate(0, 0)
        system_a = System("system_a")

        planet = Planet(name="Test Planet", resources=1, influence=1)
        system_a.add_planet(planet)

        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        system_a.place_unit_in_space(unit)

        galaxy.place_system(coord_a, "system_a")
        galaxy.register_system(system_a)

        # Test: Should return False for nonexistent target system
        assert galaxy.is_unit_adjacent_to_system(unit, "nonexistent_system") is False
        assert (
            galaxy.is_planet_adjacent_to_system(planet, "nonexistent_system") is False
        )


class TestRule6HyperlaneAdjacency:
    """Test Rule 6.4: Hyperlane adjacency.

    LRR 6.4: "Systems that are connected by lines drawn across one or more
    hyperlane tiles are adjacent for all purposes."

    Note: This is a basic implementation for testing purposes.
    Full hyperlane system would require more complex tile placement logic.
    """

    def test_systems_connected_by_hyperlane_are_adjacent(self) -> None:
        """Test that systems connected by hyperlanes are adjacent."""
        # Setup: Create galaxy with systems connected by hyperlane
        galaxy = Galaxy()

        # Place systems far apart (not physically adjacent)
        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(3, 0)  # Distance > 1, not physically adjacent

        system_a = System("system_a")
        system_b = System("system_b")

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)

        # Verify systems are NOT physically adjacent
        assert galaxy.are_systems_adjacent("system_a", "system_b") is False

        # Add hyperlane connection
        galaxy.add_hyperlane_connection("system_a", "system_b")

        # Test: Systems should now be adjacent via hyperlane
        assert galaxy.are_systems_adjacent("system_a", "system_b") is True
        assert galaxy.are_systems_adjacent("system_b", "system_a") is True

    def test_hyperlane_adjacency_extends_to_units_and_planets(self) -> None:
        """Test that hyperlane adjacency applies to units and planets."""
        # Setup: Create galaxy with hyperlane-connected systems
        galaxy = Galaxy()

        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(4, 0)  # Far apart

        system_a = System("system_a")
        system_b = System("system_b")

        # Add planet to system A
        planet = Planet(name="Hyperlane World", resources=2, influence=1)
        system_a.add_planet(planet)

        # Add unit to system A
        unit = Unit(unit_type=UnitType.DESTROYER, owner="player1")
        system_a.place_unit_in_space(unit)

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)

        # Add hyperlane connection
        galaxy.add_hyperlane_connection("system_a", "system_b")

        # Test: Unit and planet should be adjacent to hyperlane-connected system
        assert galaxy.is_unit_adjacent_to_system(unit, "system_b") is True
        assert galaxy.is_planet_adjacent_to_system(planet, "system_b") is True

    def test_multiple_hyperlane_connections(self) -> None:
        """Test that a system can have multiple hyperlane connections."""
        # Setup: Create galaxy with multiple hyperlane connections
        galaxy = Galaxy()

        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(5, 0)
        coord_c = HexCoordinate(0, 5)

        system_a = System("system_a")
        system_b = System("system_b")
        system_c = System("system_c")

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.place_system(coord_c, "system_c")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)
        galaxy.register_system(system_c)

        # Add multiple hyperlane connections from system A
        galaxy.add_hyperlane_connection("system_a", "system_b")
        galaxy.add_hyperlane_connection("system_a", "system_c")

        # Test: System A should be adjacent to both B and C via hyperlanes
        assert galaxy.are_systems_adjacent("system_a", "system_b") is True
        assert galaxy.are_systems_adjacent("system_a", "system_c") is True

        # Test: B and C should NOT be adjacent to each other (no direct connection)
        assert galaxy.are_systems_adjacent("system_b", "system_c") is False

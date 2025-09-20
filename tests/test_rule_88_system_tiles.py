"""
Test cases for Rule 88: SYSTEM TILES

Rule 88: A system tile represents an area of the galaxy. Players place system tiles during setup to create the game board.

Sub-rules:
88.1 The back of each system tile is colored green, blue, or red.
88.2 System tiles with a green-colored back are home systems and faction-specific tiles. Each home system is unique to one of the game's factions.
88.3 System tiles with a blue-colored back each contain one or more planets.
88.4 System tiles with a red-colored back are anomalies or are systems that do not contain planets.
88.5 Planets are located in systems. Ground forces and structures are usually placed on planets.
88.6 Any area on a system tile that is not a planet is space. Ships are usually placed in the space area.
88.7 Double-sided tiles that have lines crossing from one edge to another are hyperlane tiles. Hyperlane tiles are not systems.
"""

import pytest

from ti4.core.planet import Planet
from ti4.core.system_tile import SystemTile, TileColor, TileType


class TestRule88SystemTiles:
    """Test Rule 88: SYSTEM TILES"""

    def test_rule_88_1_tile_back_colors(self):
        """Test Rule 88.1: The back of each system tile is colored green, blue, or red."""
        # Test green-backed tile (home system)
        green_tile = SystemTile(tile_id="1", color=TileColor.GREEN, tile_type=TileType.HOME_SYSTEM)
        assert green_tile.color == TileColor.GREEN

        # Test blue-backed tile (planet system)
        blue_tile = SystemTile(tile_id="2", color=TileColor.BLUE, tile_type=TileType.PLANET_SYSTEM)
        assert blue_tile.color == TileColor.BLUE

        # Test red-backed tile (anomaly/empty system)
        red_tile = SystemTile(tile_id="3", color=TileColor.RED, tile_type=TileType.ANOMALY)
        assert red_tile.color == TileColor.RED

    def test_rule_88_2_green_back_home_systems(self):
        """Test Rule 88.2: System tiles with a green-colored back are home systems and faction-specific tiles."""
        home_tile = SystemTile(tile_id="1", color=TileColor.GREEN, tile_type=TileType.HOME_SYSTEM)

        assert home_tile.color == TileColor.GREEN
        assert home_tile.tile_type == TileType.HOME_SYSTEM
        assert home_tile.is_home_system()

        # Each home system should be unique to one faction
        faction_tile = SystemTile(tile_id="51", color=TileColor.GREEN, tile_type=TileType.HOME_SYSTEM, faction="The Arborec")
        assert faction_tile.faction == "The Arborec"

    def test_rule_88_3_blue_back_planet_systems(self):
        """Test Rule 88.3: System tiles with a blue-colored back each contain one or more planets."""
        # Single planet system
        single_planet_tile = SystemTile(tile_id="19", color=TileColor.BLUE, tile_type=TileType.PLANET_SYSTEM)
        planet1 = Planet("Wellon", resources=1, influence=2)
        single_planet_tile.add_planet(planet1)

        assert single_planet_tile.color == TileColor.BLUE
        assert single_planet_tile.tile_type == TileType.PLANET_SYSTEM
        assert len(single_planet_tile.planets) == 1
        assert single_planet_tile.has_planets()

        # Multi-planet system
        multi_planet_tile = SystemTile(tile_id="26", color=TileColor.BLUE, tile_type=TileType.PLANET_SYSTEM)
        planet2 = Planet("Centauri", resources=1, influence=3)
        planet3 = Planet("Gral", resources=1, influence=1)
        multi_planet_tile.add_planet(planet2)
        multi_planet_tile.add_planet(planet3)

        assert len(multi_planet_tile.planets) == 2
        assert multi_planet_tile.has_planets()

    def test_rule_88_4_red_back_anomaly_or_empty_systems(self):
        """Test Rule 88.4: System tiles with a red-colored back are anomalies or are systems that do not contain planets."""
        # Anomaly system
        anomaly_tile = SystemTile(tile_id="39", color=TileColor.RED, tile_type=TileType.ANOMALY)
        assert anomaly_tile.color == TileColor.RED
        assert anomaly_tile.tile_type == TileType.ANOMALY
        assert not anomaly_tile.has_planets()
        assert anomaly_tile.is_anomaly()

        # Empty system (no planets)
        empty_tile = SystemTile(tile_id="79", color=TileColor.RED, tile_type=TileType.EMPTY_SYSTEM)
        assert empty_tile.color == TileColor.RED
        assert empty_tile.tile_type == TileType.EMPTY_SYSTEM
        assert not empty_tile.has_planets()

    def test_rule_88_5_planets_located_in_systems(self):
        """Test Rule 88.5: Planets are located in systems. Ground forces and structures are usually placed on planets."""
        system_tile = SystemTile(tile_id="1", color=TileColor.BLUE, tile_type=TileType.PLANET_SYSTEM)
        planet = Planet("Mecatol Rex", resources=1, influence=6)
        system_tile.add_planet(planet)

        # Planet should be contained within the system
        assert planet in system_tile.planets
        assert system_tile.contains_planet("Mecatol Rex")

        # Planet should support ground forces and structures
        assert planet.can_hold_ground_forces()
        assert planet.can_hold_structures()

    def test_rule_88_6_space_areas_on_tiles(self):
        """Test Rule 88.6: Any area on a system tile that is not a planet is space. Ships are usually placed in the space area."""
        system_tile = SystemTile(tile_id="1", color=TileColor.BLUE, tile_type=TileType.PLANET_SYSTEM)
        planet = Planet("Test Planet", resources=2, influence=1)
        system_tile.add_planet(planet)

        # System should have space area
        assert system_tile.has_space_area()

        # Space area should support ships
        assert system_tile.can_hold_ships()

        # Even systems without planets have space areas
        empty_system = SystemTile(tile_id="79", color=TileColor.RED, tile_type=TileType.EMPTY_SYSTEM)
        assert empty_system.has_space_area()
        assert empty_system.can_hold_ships()

    def test_rule_88_7_hyperlane_tiles_not_systems(self):
        """Test Rule 88.7: Double-sided tiles that have lines crossing from one edge to another are hyperlane tiles. Hyperlane tiles are not systems."""
        hyperlane_tile = SystemTile(tile_id="83A", color=None, tile_type=TileType.HYPERLANE)

        assert hyperlane_tile.tile_type == TileType.HYPERLANE
        assert hyperlane_tile.is_hyperlane()
        assert not hyperlane_tile.is_system()

        # Hyperlane tiles should have crossing lines
        assert hyperlane_tile.has_crossing_lines()

        # Hyperlane tiles don't contain planets or space areas in the traditional sense
        assert not hyperlane_tile.has_planets()
        assert not hyperlane_tile.has_space_area()

    def test_system_tile_basic_properties(self):
        """Test basic SystemTile properties and methods"""
        tile = SystemTile(tile_id="42", color=TileColor.BLUE, tile_type=TileType.PLANET_SYSTEM)

        assert tile.tile_id == "42"
        assert tile.color == TileColor.BLUE
        assert tile.tile_type == TileType.PLANET_SYSTEM
        assert str(tile) == "SystemTile(42, BLUE, PLANET_SYSTEM)"

    def test_system_tile_adjacency_support(self):
        """Test that SystemTile supports adjacency operations (for Rule 6)"""
        tile1 = SystemTile(tile_id="1", color=TileColor.BLUE, tile_type=TileType.PLANET_SYSTEM)
        tile2 = SystemTile(tile_id="2", color=TileColor.RED, tile_type=TileType.ANOMALY)

        # Should be able to set adjacent tiles (implementation detail for Rule 6)
        tile1.add_adjacent_tile(tile2)
        assert tile2 in tile1.adjacent_tiles

        # Should support bidirectional adjacency
        tile2.add_adjacent_tile(tile1)
        assert tile1 in tile2.adjacent_tiles

    def test_tile_color_validation(self):
        """Test that only valid tile colors are accepted"""
        # Valid colors should work
        valid_tile = SystemTile(tile_id="1", color=TileColor.GREEN, tile_type=TileType.HOME_SYSTEM)
        assert valid_tile.color == TileColor.GREEN

        # Hyperlane tiles can have no color
        hyperlane = SystemTile(tile_id="83A", color=None, tile_type=TileType.HYPERLANE)
        assert hyperlane.color is None

    def test_tile_type_consistency(self):
        """Test that tile color and type are consistent with rules"""
        # Green tiles should be home systems
        with pytest.raises(ValueError, match="Green tiles must be home systems"):
            SystemTile(tile_id="1", color=TileColor.GREEN, tile_type=TileType.PLANET_SYSTEM)

        # Blue tiles should contain planets
        with pytest.raises(ValueError, match="Blue tiles must be planet systems"):
            SystemTile(tile_id="1", color=TileColor.BLUE, tile_type=TileType.ANOMALY)

        # Red tiles should be anomalies or empty systems
        with pytest.raises(ValueError, match="Red tiles must be anomalies or empty systems"):
            SystemTile(tile_id="1", color=TileColor.RED, tile_type=TileType.HOME_SYSTEM)

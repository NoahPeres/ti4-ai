"""Tests for Rule 76: SHIPS mechanics.

This module tests the ship system according to TI4 LRR Rule 76.
All tests follow strict TDD methodology with RED-GREEN-REFACTOR cycles.

Rule 76 Sub-rules tested:
- 76.0: Ship definition - carriers, cruisers, dreadnoughts, destroyers, fighters, war suns, flagships
- 76.1: Ship placement - ships are always placed in space
- 76.2: Fleet pool limits - ships limited by command tokens in fleet pool
- 76.3: Ship attributes - cost, combat, move, and capacity attributes
"""

from tests.test_constants import MockPlanet, MockPlayer, MockSystem
from ti4.core.constants import UnitType
from ti4.core.fleet import Fleet
from ti4.core.galaxy import Galaxy
from ti4.core.hex_coordinate import HexCoordinate
from ti4.core.planet import Planet
from ti4.core.ships import ShipManager
from ti4.core.system import System
from ti4.core.unit import Unit


class TestRule76ShipBasics:
    """Test basic ship mechanics (Rule 76.0)."""

    def test_ship_system_exists(self) -> None:
        """Test that ship system can be imported and instantiated.

        This is the first RED test - it will fail until we create the system.

        LRR Reference: Rule 76.0 - Core ship concept
        """
        # This will fail initially - RED phase
        manager = ShipManager()
        assert manager is not None


class TestRule76ShipDefinition:
    """Test ship type definition mechanics (Rule 76.0)."""

    def test_carrier_is_ship(self) -> None:
        """Test that carriers are identified as ships.

        LRR Reference: Rule 76.0 - "A ship is a unit type consisting of carriers..."
        """
        manager = ShipManager()

        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")
        is_ship = manager.is_ship(carrier)
        assert is_ship is True

    def test_cruiser_is_ship(self) -> None:
        """Test that cruisers are identified as ships.

        LRR Reference: Rule 76.0 - "...cruisers..."
        """
        manager = ShipManager()

        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        is_ship = manager.is_ship(cruiser)
        assert is_ship is True

    def test_dreadnought_is_ship(self) -> None:
        """Test that dreadnoughts are identified as ships.

        LRR Reference: Rule 76.0 - "...dreadnoughts..."
        """
        manager = ShipManager()

        dreadnought = Unit(unit_type=UnitType.DREADNOUGHT, owner="player1")
        is_ship = manager.is_ship(dreadnought)
        assert is_ship is True

    def test_destroyer_is_ship(self) -> None:
        """Test that destroyers are identified as ships.

        LRR Reference: Rule 76.0 - "...destroyers..."
        """
        manager = ShipManager()

        destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player1")
        is_ship = manager.is_ship(destroyer)
        assert is_ship is True

    def test_fighter_is_ship(self) -> None:
        """Test that fighters are identified as ships.

        LRR Reference: Rule 76.0 - "...fighters..."
        """
        manager = ShipManager()

        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")
        is_ship = manager.is_ship(fighter)
        assert is_ship is True

    def test_war_sun_is_ship(self) -> None:
        """Test that war suns are identified as ships.

        LRR Reference: Rule 76.0 - "...and war suns"
        """
        manager = ShipManager()

        war_sun = Unit(unit_type=UnitType.WAR_SUN, owner="player1")
        is_ship = manager.is_ship(war_sun)
        assert is_ship is True

    def test_flagship_is_ship(self) -> None:
        """Test that flagships are identified as ships.

        LRR Reference: Rule 76.0 - "Each race also has a unique flagship"
        """
        manager = ShipManager()

        flagship = Unit(unit_type=UnitType.FLAGSHIP, owner="player1")
        is_ship = manager.is_ship(flagship)
        assert is_ship is True

    def test_infantry_is_not_ship(self) -> None:
        """Test that infantry are not identified as ships.

        LRR Reference: Rule 76.0 - Infantry are ground forces, not ships
        """
        manager = ShipManager()

        infantry = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        is_ship = manager.is_ship(infantry)
        assert is_ship is False

    def test_mech_is_not_ship(self) -> None:
        """Test that mechs are not identified as ships.

        LRR Reference: Rule 76.0 - Mechs are ground forces, not ships
        """
        manager = ShipManager()

        mech = Unit(unit_type=UnitType.MECH, owner="player1")
        is_ship = manager.is_ship(mech)
        assert is_ship is False

    def test_space_dock_is_not_ship(self) -> None:
        """Test that space docks are not identified as ships.

        LRR Reference: Rule 76.0 - Space docks are structures, not ships
        """
        manager = ShipManager()

        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        is_ship = manager.is_ship(space_dock)
        assert is_ship is False


class TestRule76ShipPlacement:
    """Test ship placement mechanics (Rule 76.1)."""

    def test_ships_must_be_placed_in_space(self) -> None:
        """Test that ships must be placed in space areas.

        LRR Reference: Rule 76.1 - "Ships are always placed in space"
        """
        manager = ShipManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Add planet
        planet = Planet(MockPlanet.PLANET_A.value, resources=2, influence=1)
        system.add_planet(planet)

        # Create ship
        cruiser = Unit(unit_type=UnitType.CRUISER, owner=MockPlayer.PLAYER_1.value)

        # Should be able to validate ship placement in space
        can_place_in_space = manager.can_place_ship_in_space(cruiser, system)
        assert can_place_in_space is True

        # Should not be able to place ship on planet (this would be validated elsewhere)
        # This test just confirms the ship manager recognizes valid space placement
        can_place_on_planet = manager.can_place_ship_on_planet(cruiser, planet)
        assert can_place_on_planet is False


class TestRule76FleetPoolLimits:
    """Test fleet pool limit mechanics (Rule 76.2)."""

    def test_ships_limited_by_fleet_pool(self) -> None:
        """Test that ships are limited by fleet pool command tokens.

        LRR Reference: Rule 76.2 - "A player can have a number of ships in a system
        equal to or less than the number of command tokens in that player's fleet pool"
        """
        manager = ShipManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)

        # Add ships to system
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        cruiser3 = Unit(unit_type=UnitType.CRUISER, owner="player1")

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        # With fleet pool of 2, should be able to have 2 ships
        fleet_pool_size = 2
        can_add_ship = manager.can_add_ship_to_system(
            cruiser3, system, "player1", fleet_pool_size
        )
        assert can_add_ship is False  # Already at limit with 2 ships

    def test_fighters_dont_count_toward_fleet_pool(self) -> None:
        """Test that fighters don't count toward fleet pool limits.

        LRR Reference: Rule 76.2a - "Fighters do not count toward the fleet pool limit,
        and instead count against a player's capacity"
        """
        manager = ShipManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)

        # Add ships to system - 2 cruisers and fighters
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        fighter1 = Unit(unit_type=UnitType.FIGHTER, owner="player1")
        fighter2 = Unit(unit_type=UnitType.FIGHTER, owner="player1")

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)
        system.place_unit_in_space(fighter1)
        system.place_unit_in_space(fighter2)

        # Count non-fighter ships for fleet pool
        fleet_pool_size = 2
        non_fighter_ships = manager.count_non_fighter_ships_in_system(system, "player1")
        assert non_fighter_ships == 2  # Only cruisers count

        # Should still be at fleet pool limit (fighters don't count)
        cruiser3 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        can_add_ship = manager.can_add_ship_to_system(
            cruiser3, system, "player1", fleet_pool_size
        )
        assert can_add_ship is False  # At limit with non-fighter ships


class TestRule76ShipAttributes:
    """Test ship attribute mechanics (Rule 76.3)."""

    def test_ships_have_cost_attribute(self) -> None:
        """Test that ships have cost attributes.

        LRR Reference: Rule 76.3 - "Ships can have any number of the following attributes: cost..."
        """
        manager = ShipManager()

        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")

        # Should be able to get ship cost
        has_cost = manager.ship_has_cost_attribute(cruiser)
        assert has_cost is True

    def test_ships_have_combat_attribute(self) -> None:
        """Test that ships have combat attributes.

        LRR Reference: Rule 76.3 - "...combat..."
        """
        manager = ShipManager()

        destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player1")

        # Should be able to get ship combat value
        has_combat = manager.ship_has_combat_attribute(destroyer)
        assert has_combat is True

    def test_ships_have_move_attribute(self) -> None:
        """Test that ships have move attributes.

        LRR Reference: Rule 76.3 - "...move..."
        """
        manager = ShipManager()

        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")

        # Should be able to get ship move value
        has_move = manager.ship_has_move_attribute(cruiser)
        assert has_move is True

    def test_ships_can_have_capacity_attribute(self) -> None:
        """Test that ships can have capacity attributes.

        LRR Reference: Rule 76.3 - "...and capacity"
        """
        manager = ShipManager()

        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")

        # Carriers should have capacity
        has_capacity = manager.ship_has_capacity_attribute(carrier)
        assert has_capacity is True

        # Destroyers typically don't have capacity
        destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player1")
        has_capacity = manager.ship_has_capacity_attribute(destroyer)
        assert has_capacity is False


class TestRule76FleetIntegration:
    """Test integration between ship system and existing fleet system."""

    def test_ship_manager_integrates_with_fleet_class(self) -> None:
        """Test that ShipManager integrates with existing Fleet class.

        This test ensures we don't duplicate functionality and use existing systems.
        """
        manager = ShipManager()

        # Create fleet with ships
        fleet = Fleet("player1", "system1")
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")

        fleet.add_unit(cruiser1)
        fleet.add_unit(cruiser2)
        fleet.add_unit(fighter)

        # Test integration with fleet pool validation
        fleet_pool_size = 2
        can_add_cruiser = manager.can_add_ship_to_fleet(
            Unit(unit_type=UnitType.CRUISER, owner="player1"), fleet, fleet_pool_size
        )
        assert can_add_cruiser is False  # Already at limit

        # Test that fighters can still be added
        can_add_fighter = manager.can_add_ship_to_fleet(
            Unit(unit_type=UnitType.FIGHTER, owner="player1"), fleet, fleet_pool_size
        )
        assert can_add_fighter is True  # Fighters don't count toward fleet pool

    def test_ship_manager_uses_existing_fleet_validator(self) -> None:
        """Test that ShipManager uses existing FleetCapacityValidator.

        This ensures consistency with existing fleet pool validation logic.
        """
        manager = ShipManager()

        # Create multiple fleets
        fleet1 = Fleet("player1", "system1")
        fleet2 = Fleet("player1", "system2")

        # Add ships requiring fleet supply
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner="player1")

        fleet1.add_unit(cruiser1)
        fleet2.add_unit(cruiser2)

        # Test fleet pool validation
        fleet_pool_size = 2
        fleets = [fleet1, fleet2]

        # Should be valid (2 fleets, 2 fleet pool tokens)
        is_valid = manager.validate_fleet_pool_limits(fleets, fleet_pool_size)
        assert is_valid is True

        # Add another fleet with ships requiring supply
        fleet3 = Fleet("player1", "system3")
        cruiser3 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        fleet3.add_unit(cruiser3)
        fleets.append(fleet3)

        # Should be invalid (3 fleets, 2 fleet pool tokens)
        is_valid = manager.validate_fleet_pool_limits(fleets, fleet_pool_size)
        assert is_valid is False

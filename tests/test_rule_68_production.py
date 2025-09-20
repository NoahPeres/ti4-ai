"""Tests for Rule 68: PRODUCTION (UNIT ABILITY) mechanics.

This module tests the production ability system according to TI4 LRR Rule 68.
All tests follow strict TDD methodology with RED-GREEN-REFACTOR cycles.

Rule 68 Sub-rules tested:
- 68.0: Production ability definition - resolving production during tactical actions
- 68.1: Production value and limits - maximum units that can be produced
- 68.1a: Combined production values - multiple units combining production
- 68.1b: Fighter/infantry counting - individual units count toward limits
- 68.1c: Partial production - producing one fighter/infantry for full cost
- 68.1d: Arborec restriction - space dock infantry production restriction
- 68.2: Ship placement - ships must be placed in active system
- 68.3: Ground force placement - ground forces on planets with production units
- 68.4: Space area production - special placement rules for space-based production
"""

from src.ti4.core.constants import Faction, UnitType
from src.ti4.core.galaxy import Galaxy
from src.ti4.core.hex_coordinate import HexCoordinate
from src.ti4.core.planet import Planet
from src.ti4.core.production_ability import ProductionAbilityManager
from src.ti4.core.system import System
from src.ti4.core.unit import Unit
from tests.test_constants import MockPlanet, MockPlayer, MockSystem


class TestRule68ProductionAbilityBasics:
    """Test basic production ability mechanics (Rule 68.0)."""

    def test_production_ability_system_exists(self) -> None:
        """Test that production ability system can be imported and instantiated.

        This is the first RED test - it will fail until we create the system.

        LRR Reference: Rule 68.0 - Core production ability concept
        """
        # This will fail initially - RED phase
        manager = ProductionAbilityManager()
        assert manager is not None


class TestRule68ProductionValues:
    """Test production value and limit mechanics (Rule 68.1)."""

    def test_space_dock_production_value_depends_on_planet(self) -> None:
        """Test that space dock production value depends on planet resources.

        LRR Reference: Rule 68.1 - Space Dock I has "PRODUCTION: RESOURCES + 2"
        """
        manager = ProductionAbilityManager()

        # Create planet with 3 resources
        planet = Planet(MockPlanet.PLANET_A.value, resources=3, influence=1)
        space_dock = Unit(
            unit_type=UnitType.SPACE_DOCK, owner=MockPlayer.PLAYER_1.value
        )

        # Space Dock I production = planet resources + 2 = 3 + 2 = 5
        production_value = manager.get_production_value(space_dock, planet)
        assert production_value == 5

    def test_unit_without_production_has_zero_value(self) -> None:
        """Test that units without production ability have zero value.

        LRR Reference: Rule 68.1 - Production ability is specific to certain units
        """
        manager = ProductionAbilityManager()

        infantry = Unit(unit_type=UnitType.INFANTRY, owner=MockPlayer.PLAYER_1.value)
        production_value = manager.get_production_value(infantry)
        assert production_value == 0

    def test_space_dock_without_planet_has_zero_production(self) -> None:
        """Test that space dock without planet context has zero production.

        This handles edge cases where planet context is missing.
        """
        manager = ProductionAbilityManager()

        space_dock = Unit(
            unit_type=UnitType.SPACE_DOCK, owner=MockPlayer.PLAYER_1.value
        )
        production_value = manager.get_production_value(
            space_dock
        )  # No planet provided
        assert production_value == 0

    def test_production_limit_enforcement(self) -> None:
        """Test that production limits are actually enforced.

        LRR Reference: Rule 68.1 - "This value is the maximum number of units that this unit can produce"
        """
        manager = ProductionAbilityManager()

        # Create planet with 1 resource (production = 3)
        planet = Planet(MockPlanet.PLANET_A.value, resources=1, influence=1)
        space_dock = Unit(
            unit_type=UnitType.SPACE_DOCK, owner=MockPlayer.PLAYER_1.value
        )

        # Should be able to produce 3 units (within limit)
        can_produce_within_limit = manager.can_produce_units(
            space_dock, [UnitType.CRUISER, UnitType.CRUISER, UnitType.CRUISER], planet
        )
        assert can_produce_within_limit is True

        # Should NOT be able to produce 4 units (exceeds limit)
        can_produce_over_limit = manager.can_produce_units(
            space_dock,
            [UnitType.CRUISER, UnitType.CRUISER, UnitType.CRUISER, UnitType.CRUISER],
            planet,
        )
        assert can_produce_over_limit is False


class TestRule68CombinedProduction:
    """Test combined production value mechanics (Rule 68.1a)."""

    def test_multiple_production_units_combine_values(self) -> None:
        """Test that multiple production units combine their values.

        LRR Reference: Rule 68.1a - "player can produce a number of units up to the combined total"
        """
        manager = ProductionAbilityManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Add planet A with space dock (resources=2, so production=4)
        planet_a = Planet(MockPlanet.PLANET_A.value, resources=2, influence=1)
        system.add_planet(planet_a)
        space_dock_a = Unit(
            unit_type=UnitType.SPACE_DOCK, owner=MockPlayer.PLAYER_1.value
        )
        planet_a.place_unit(space_dock_a)

        # Add planet B with space dock (resources=3, so production=5)
        planet_b = Planet(MockPlanet.PLANET_B.value, resources=3, influence=1)
        system.add_planet(planet_b)
        space_dock_b = Unit(
            unit_type=UnitType.SPACE_DOCK, owner=MockPlayer.PLAYER_1.value
        )
        planet_b.place_unit(space_dock_b)

        # Combined production should be 9 (4 + 5)
        total_production = manager.get_combined_production_in_system(
            system, MockPlayer.PLAYER_1.value
        )
        assert total_production == 9

    def test_single_production_unit_uses_own_value(self) -> None:
        """Test that single production unit uses its own value.

        LRR Reference: Rule 68.1a - Combined total applies when multiple units present
        """
        manager = ProductionAbilityManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Add planet with space dock only
        planet = Planet(MockPlanet.PLANET_A.value, resources=2, influence=1)
        system.add_planet(planet)

        space_dock = Unit(
            unit_type=UnitType.SPACE_DOCK, owner=MockPlayer.PLAYER_1.value
        )
        planet.place_unit(space_dock)

        # Production should be 4 (planet resources 2 + 2 = 4)
        total_production = manager.get_combined_production_in_system(
            system, MockPlayer.PLAYER_1.value
        )
        assert total_production == 4

    def test_no_production_units_gives_zero(self) -> None:
        """Test that system with no production units gives zero production.

        LRR Reference: Rule 68.1a - Production requires units with production ability
        """
        manager = ProductionAbilityManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Add planet with non-production unit
        planet = Planet(MockPlanet.PLANET_A.value, resources=2, influence=1)
        system.add_planet(planet)

        infantry = Unit(unit_type=UnitType.INFANTRY, owner=MockPlayer.PLAYER_1.value)
        planet.place_unit(infantry)

        # Production should be 0
        total_production = manager.get_combined_production_in_system(
            system, MockPlayer.PLAYER_1.value
        )
        assert total_production == 0


class TestRule68FighterInfantryCounting:
    """Test fighter/infantry production counting mechanics (Rule 68.1b)."""

    def test_fighters_count_individually_toward_limit(self) -> None:
        """Test that fighters count individually toward production limit.

        LRR Reference: Rule 68.1b - "each individual unit counts toward the producing unit's production limit"
        """
        manager = ProductionAbilityManager()

        # Create planet and space dock
        planet = Planet(
            MockPlanet.PLANET_A.value, resources=0, influence=1
        )  # Production = 0 + 2 = 2
        space_dock = Unit(
            unit_type=UnitType.SPACE_DOCK, owner=MockPlayer.PLAYER_1.value
        )

        # Producing 2 fighters should use 2 production capacity
        production_used = manager.calculate_production_used(
            [UnitType.FIGHTER, UnitType.FIGHTER]
        )
        assert production_used == 2

        # Should be able to produce 2 fighters with space dock (production 2)
        can_produce = manager.can_produce_units(
            space_dock, [UnitType.FIGHTER, UnitType.FIGHTER], planet
        )
        assert can_produce is True

    def test_infantry_count_individually_toward_limit(self) -> None:
        """Test that infantry count individually toward production limit.

        LRR Reference: Rule 68.1b - "each individual unit counts toward the producing unit's production limit"
        """
        manager = ProductionAbilityManager()

        # Create planet and space dock
        planet = Planet(
            MockPlanet.PLANET_A.value, resources=0, influence=1
        )  # Production = 0 + 2 = 2
        space_dock = Unit(
            unit_type=UnitType.SPACE_DOCK, owner=MockPlayer.PLAYER_1.value
        )

        # Producing 2 infantry should use 2 production capacity
        production_used = manager.calculate_production_used(
            [UnitType.INFANTRY, UnitType.INFANTRY]
        )
        assert production_used == 2

        # Should be able to produce 2 infantry with space dock (production 2)
        can_produce = manager.can_produce_units(
            space_dock, [UnitType.INFANTRY, UnitType.INFANTRY], planet
        )
        assert can_produce is True

    def test_mixed_fighters_infantry_count_individually(self) -> None:
        """Test that mixed fighters and infantry count individually.

        LRR Reference: Rule 68.1b - Individual counting applies to both fighters and infantry
        """
        manager = ProductionAbilityManager()

        # Create planet and space dock
        planet = Planet(
            MockPlanet.PLANET_A.value, resources=0, influence=1
        )  # Production = 0 + 2 = 2
        space_dock = Unit(
            unit_type=UnitType.SPACE_DOCK, owner=MockPlayer.PLAYER_1.value
        )

        # Producing 1 fighter + 1 infantry should use 2 production capacity
        production_used = manager.calculate_production_used(
            [UnitType.FIGHTER, UnitType.INFANTRY]
        )
        assert production_used == 2

        # Should be able to produce 1 fighter + 1 infantry with space dock (production 2)
        can_produce = manager.can_produce_units(
            space_dock, [UnitType.FIGHTER, UnitType.INFANTRY], planet
        )
        assert can_produce is True


class TestRule68PartialProduction:
    """Test partial fighter/infantry production mechanics (Rule 68.1c)."""

    def test_can_produce_one_fighter_for_full_cost(self) -> None:
        """Test that player can produce one fighter for full cost.

        LRR Reference: Rule 68.1c - "A player can choose to produce one fighter... but must still pay the entire cost"
        """
        manager = ProductionAbilityManager()

        # Should be able to produce 1 fighter for cost of 2
        can_produce_partial = manager.can_produce_partial_fighters(1)
        assert can_produce_partial is True

        # Cost should still be full cost (0.5 * 2 = 1 resource)
        cost = manager.get_partial_fighter_cost(1)
        assert cost == 1  # Full cost for fighter pair

    def test_can_produce_one_infantry_for_full_cost(self) -> None:
        """Test that player can produce one infantry for full cost.

        LRR Reference: Rule 68.1c - "A player can choose to produce one... infantry... but must still pay the entire cost"
        """
        manager = ProductionAbilityManager()

        # Should be able to produce 1 infantry for cost of 2
        can_produce_partial = manager.can_produce_partial_infantry(1)
        assert can_produce_partial is True

        # Cost should still be full cost (0.5 * 2 = 1 resource)
        cost = manager.get_partial_infantry_cost(1)
        assert cost == 1  # Full cost for infantry pair

    def test_partial_production_still_counts_toward_limit(self) -> None:
        """Test that partial production still counts toward production limit.

        LRR Reference: Rule 68.1c + 68.1b - Partial units still count individually
        """
        manager = ProductionAbilityManager()

        # Create planet and space dock
        planet = Planet(
            MockPlanet.PLANET_A.value, resources=0, influence=1
        )  # Production = 0 + 2 = 2
        space_dock = Unit(
            unit_type=UnitType.SPACE_DOCK, owner=MockPlayer.PLAYER_1.value
        )

        # Producing 1 fighter (partial) should use 1 production capacity
        production_used = manager.calculate_production_used([UnitType.FIGHTER])
        assert production_used == 1

        # Should be able to produce 1 fighter + 1 more unit with space dock (production 2)
        can_produce = manager.can_produce_units(
            space_dock, [UnitType.FIGHTER, UnitType.INFANTRY], planet
        )
        assert can_produce is True


class TestRule68ArborecRestriction:
    """Test Arborec space dock restriction mechanics (Rule 68.1d)."""

    def test_arborec_space_dock_cannot_produce_infantry(self) -> None:
        """Test that Arborec space docks cannot produce infantry.

        LRR Reference: Rule 68.1d - "Production value from Arborec space docks cannot be used to produce infantry"
        """
        manager = ProductionAbilityManager()

        # Create planet and Arborec space dock
        planet = Planet(
            MockPlanet.PLANET_A.value, resources=1, influence=1
        )  # Production = 1 + 2 = 3
        arborec_space_dock = Unit(
            unit_type=UnitType.SPACE_DOCK, owner=Faction.ARBOREC.value
        )

        # Should not be able to produce infantry with Arborec space dock
        can_produce_infantry = manager.can_produce_units(
            arborec_space_dock, [UnitType.INFANTRY], planet
        )
        assert can_produce_infantry is False

        # Should still be able to produce other units
        can_produce_fighters = manager.can_produce_units(
            arborec_space_dock, [UnitType.FIGHTER], planet
        )
        assert can_produce_fighters is True

    def test_arborec_restriction_is_space_dock_specific(self) -> None:
        """Test that Arborec restriction is specific to space docks.

        LRR Reference: Rule 68.1d - Restriction is specific to space docks
        Note: This test validates the restriction logic, not actual Arborec infantry production
        """
        manager = ProductionAbilityManager()

        # Create planet and non-Arborec space dock for comparison
        planet = Planet(MockPlanet.PLANET_A.value, resources=1, influence=1)
        regular_space_dock = Unit(
            unit_type=UnitType.SPACE_DOCK, owner=MockPlayer.PLAYER_1.value
        )

        # Regular space dock should be able to produce infantry
        can_produce_infantry = manager.can_produce_units(
            regular_space_dock, [UnitType.INFANTRY], planet
        )
        assert can_produce_infantry is True

    def test_non_arborec_space_dock_can_produce_infantry(self) -> None:
        """Test that non-Arborec space docks can produce infantry.

        LRR Reference: Rule 68.1d - Restriction is faction-specific
        """
        manager = ProductionAbilityManager()

        # Create planet and non-Arborec space dock
        planet = Planet(
            MockPlanet.PLANET_A.value, resources=1, influence=1
        )  # Production = 1 + 2 = 3
        space_dock = Unit(
            unit_type=UnitType.SPACE_DOCK, owner=MockPlayer.PLAYER_1.value
        )

        # Should be able to produce infantry with non-Arborec space dock
        can_produce_infantry = manager.can_produce_units(
            space_dock, [UnitType.INFANTRY], planet
        )
        assert can_produce_infantry is True


class TestRule68ShipPlacement:
    """Test ship production placement mechanics (Rule 68.2)."""

    def test_ships_must_be_placed_in_active_system(self) -> None:
        """Test that ships produced via production must be placed in active system.

        LRR Reference: Rule 68.2 - "player must place them in the active system"
        """
        manager = ProductionAbilityManager()

        # Create galaxy and systems
        galaxy = Galaxy()
        active_system = System(MockSystem.TEST_SYSTEM.value)
        other_system = System(MockSystem.SYSTEM_2.value)

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)

        galaxy.place_system(coord1, MockSystem.TEST_SYSTEM.value)
        galaxy.place_system(coord2, MockSystem.SYSTEM_2.value)
        galaxy.register_system(active_system)
        galaxy.register_system(other_system)

        # Should be able to place ships in active system
        can_place_in_active = manager.can_place_produced_ships_in_system(
            [UnitType.CRUISER], active_system, active_system
        )
        assert can_place_in_active is True

        # Should not be able to place ships in other system
        can_place_in_other = manager.can_place_produced_ships_in_system(
            [UnitType.CRUISER], other_system, active_system
        )
        assert can_place_in_other is False

    def test_ship_placement_validation(self) -> None:
        """Test ship placement validation for production.

        LRR Reference: Rule 68.2 - Ship placement restrictions
        """
        manager = ProductionAbilityManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Ships should be valid for space placement
        ships = [UnitType.CRUISER, UnitType.DESTROYER, UnitType.CARRIER]
        are_ships = manager.are_units_ships(ships)
        assert are_ships is True

        # Ground forces should not be valid for space placement
        ground_forces = [UnitType.INFANTRY, UnitType.MECH]
        are_ships_gf = manager.are_units_ships(ground_forces)
        assert are_ships_gf is False


class TestRule68GroundForcePlacement:
    """Test ground force production placement mechanics (Rule 68.3)."""

    def test_ground_forces_must_be_placed_on_production_planets(self) -> None:
        """Test that ground forces must be placed on planets with production units.

        LRR Reference: Rule 68.3 - "must place those unit on planets that contain a unit that used its 'Production' ability"
        """
        manager = ProductionAbilityManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Add planets
        planet_with_production = Planet(
            MockPlanet.PLANET_A.value, resources=2, influence=1
        )
        planet_without_production = Planet(
            MockPlanet.PLANET_B.value, resources=1, influence=2
        )
        system.add_planet(planet_with_production)
        system.add_planet(planet_without_production)

        # Add space dock to planet A
        space_dock = Unit(
            unit_type=UnitType.SPACE_DOCK, owner=MockPlayer.PLAYER_1.value
        )
        planet_with_production.place_unit(space_dock)

        # Should be able to place ground forces on planet with production
        can_place_on_production_planet = (
            manager.can_place_produced_ground_forces_on_planet(
                [UnitType.INFANTRY], planet_with_production
            )
        )
        assert can_place_on_production_planet is True

        # Should not be able to place ground forces on planet without production
        can_place_on_other_planet = manager.can_place_produced_ground_forces_on_planet(
            [UnitType.INFANTRY], planet_without_production
        )
        assert can_place_on_other_planet is False

    def test_ground_force_placement_validation(self) -> None:
        """Test ground force placement validation for production.

        LRR Reference: Rule 68.3 - Ground force placement restrictions
        """
        manager = ProductionAbilityManager()

        # Ground forces should be valid for planet placement
        ground_forces = [UnitType.INFANTRY, UnitType.MECH]
        are_ground_forces = manager.are_units_ground_forces(ground_forces)
        assert are_ground_forces is True

        # Ships should not be valid for planet placement
        ships = [UnitType.CRUISER, UnitType.DESTROYER]
        are_ground_forces_ships = manager.are_units_ground_forces(ships)
        assert are_ground_forces_ships is False


class TestRule68SpaceAreaProduction:
    """Test space area production placement mechanics (Rule 68.4)."""

    def test_space_production_can_place_ground_forces_on_controlled_planet(
        self,
    ) -> None:
        """Test that space-based production can place ground forces on controlled planets.

        LRR Reference: Rule 68.4 - "may either be placed on a planet the player controls in that system"
        """
        manager = ProductionAbilityManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Add controlled planet
        controlled_planet = Planet(MockPlanet.PLANET_A.value, resources=2, influence=1)
        controlled_planet.controlled_by = MockPlayer.PLAYER_1.value
        system.add_planet(controlled_planet)

        # Add war sun in space (production unit)
        war_sun = Unit(unit_type=UnitType.WAR_SUN, owner=MockPlayer.PLAYER_1.value)
        system.place_unit_in_space(war_sun)

        # Should be able to place ground forces on controlled planet
        can_place_on_planet = (
            manager.can_space_production_place_ground_forces_on_planet(
                [UnitType.INFANTRY], controlled_planet, MockPlayer.PLAYER_1.value
            )
        )
        assert can_place_on_planet is True

    def test_space_production_can_place_ground_forces_in_space(self) -> None:
        """Test that space-based production can place ground forces in space.

        LRR Reference: Rule 68.4 - "or in the space area of that system"
        """
        manager = ProductionAbilityManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Add war sun in space (production unit)
        war_sun = Unit(unit_type=UnitType.WAR_SUN, owner=MockPlayer.PLAYER_1.value)
        system.place_unit_in_space(war_sun)

        # Should be able to place ground forces in space area
        can_place_in_space = manager.can_space_production_place_ground_forces_in_space(
            [UnitType.INFANTRY], system
        )
        assert can_place_in_space is True

    def test_space_production_cannot_place_on_uncontrolled_planet(self) -> None:
        """Test that space-based production cannot place ground forces on uncontrolled planets.

        LRR Reference: Rule 68.4 - "on a planet the player controls"
        """
        manager = ProductionAbilityManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Add uncontrolled planet
        uncontrolled_planet = Planet(
            MockPlanet.PLANET_A.value, resources=2, influence=1
        )
        uncontrolled_planet.controlled_by = (
            MockPlayer.PLAYER_2.value
        )  # Different player
        system.add_planet(uncontrolled_planet)

        # Add war sun in space (production unit)
        war_sun = Unit(unit_type=UnitType.WAR_SUN, owner=MockPlayer.PLAYER_1.value)
        system.place_unit_in_space(war_sun)

        # Should not be able to place ground forces on uncontrolled planet
        can_place_on_planet = (
            manager.can_space_production_place_ground_forces_on_planet(
                [UnitType.INFANTRY], uncontrolled_planet, MockPlayer.PLAYER_1.value
            )
        )
        assert can_place_on_planet is False


class TestRule68ProductionIntegration:
    """Test production ability integration with existing systems."""

    def test_production_ability_integrates_with_tactical_action(self) -> None:
        """Test that production ability integrates with tactical action system.

        This ensures production abilities work during tactical action production step.
        """

        production_manager = ProductionAbilityManager()
        # TacticalAction integration test - simplified for now

        # Create galaxy and system
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Add space dock
        planet = Planet(MockPlanet.PLANET_A.value, resources=2, influence=1)
        system.add_planet(planet)

        space_dock = Unit(
            unit_type=UnitType.SPACE_DOCK, owner=MockPlayer.PLAYER_1.value
        )
        planet.place_unit(space_dock)

        # Should be able to use production during tactical action
        can_use_production = production_manager.can_use_production_in_tactical_action(
            system, MockPlayer.PLAYER_1.value
        )
        assert can_use_production is True

    def test_production_ability_integrates_with_blockade_system(self) -> None:
        """Test that production ability integrates with blockade system.

        This ensures production is affected by blockades (Rule 14).
        """
        from src.ti4.core.blockade import BlockadeManager

        production_manager = ProductionAbilityManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Add space dock
        planet = Planet(MockPlanet.PLANET_A.value, resources=2, influence=1)
        system.add_planet(planet)

        space_dock = Unit(
            unit_type=UnitType.SPACE_DOCK, owner=MockPlayer.PLAYER_1.value
        )
        planet.place_unit(space_dock)

        # Add enemy ship to create blockade
        enemy_ship = Unit(unit_type=UnitType.DESTROYER, owner=MockPlayer.PLAYER_2.value)
        system.place_unit_in_space(enemy_ship)

        # Create blockade manager
        blockade_manager = BlockadeManager(galaxy)

        # Production should be affected by blockade
        is_production_blockaded = production_manager.is_production_blockaded(
            space_dock, blockade_manager
        )
        assert is_production_blockaded is True

    def test_realistic_production_scenario(self) -> None:
        """Test a realistic production scenario with proper planet-based production.

        This demonstrates how the system works in practice.
        """
        manager = ProductionAbilityManager()

        # Create a rich planet (4 resources) with space dock
        rich_planet = Planet("Mecatol Rex", resources=4, influence=6)
        space_dock = Unit(
            unit_type=UnitType.SPACE_DOCK, owner=MockPlayer.PLAYER_1.value
        )

        # Space dock production = 4 + 2 = 6
        production_value = manager.get_production_value(space_dock, rich_planet)
        assert production_value == 6

        # Should be able to produce 6 units
        can_produce_six = manager.can_produce_units(
            space_dock,
            [
                UnitType.CRUISER,
                UnitType.CRUISER,
                UnitType.DESTROYER,
                UnitType.FIGHTER,
                UnitType.FIGHTER,
                UnitType.INFANTRY,
            ],
            rich_planet,
        )
        assert can_produce_six is True

        # Should NOT be able to produce 7 units
        can_produce_seven = manager.can_produce_units(
            space_dock,
            [
                UnitType.CRUISER,
                UnitType.CRUISER,
                UnitType.DESTROYER,
                UnitType.FIGHTER,
                UnitType.FIGHTER,
                UnitType.INFANTRY,
                UnitType.MECH,
            ],
            rich_planet,
        )
        assert can_produce_seven is False

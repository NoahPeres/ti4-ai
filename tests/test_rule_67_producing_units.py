"""Tests for Rule 67: PRODUCING UNITS mechanics.

This module tests the unit production system according to TI4 LRR Rule 67.
All tests follow strict TDD methodology with RED-GREEN-REFACTOR cycles.

Rule 67 Sub-rules tested:
- 67.1: Unit cost - must spend resources equal to or greater than cost
- 67.2: Dual unit production - fighters/infantry produce two units for cost
- 67.3: Tactical action production - follows Production ability rules
- 67.4: Non-tactical production - specifies number and placement
- 67.5: Reinforcement limits - limited by units in reinforcements
- 67.6: Ship production restriction - cannot produce ships with enemy ships
"""

from src.ti4.core.constants import UnitType
from src.ti4.core.production import ProductionManager
from src.ti4.core.unit import Unit


class TestRule67ProductionBasics:
    """Test basic production mechanics (Rule 67.0)."""

    def test_production_system_exists(self) -> None:
        """Test that production system can be imported and instantiated.

        This is the first RED test - it will fail until we create the system.

        LRR Reference: Rule 67.0 - Core production concept
        """
        # This will fail initially - RED phase
        manager = ProductionManager()
        assert manager is not None


class TestRule67UnitCost:
    """Test unit cost mechanics (Rule 67.1)."""

    def test_can_produce_unit_with_sufficient_resources(self) -> None:
        """Test that units can be produced when player has sufficient resources.

        LRR Reference: Rule 67.1 - "Each unit has cost value on faction sheet or
        technology card; must spend resources equal to or greater than cost"
        """
        manager = ProductionManager()

        # Create a fighter (cost 1) with sufficient resources
        unit_type = UnitType.FIGHTER
        available_resources = 2

        can_produce = manager.can_afford_unit(unit_type, available_resources)
        assert can_produce is True

    def test_cannot_produce_unit_with_insufficient_resources(self) -> None:
        """Test that units cannot be produced when player lacks sufficient resources.

        LRR Reference: Rule 67.1 - Must spend resources equal to or greater than cost
        """
        manager = ProductionManager()

        # Create a cruiser (cost 2) with insufficient resources
        unit_type = UnitType.CRUISER
        available_resources = 1

        can_produce = manager.can_afford_unit(unit_type, available_resources)
        assert can_produce is False

    def test_can_produce_unit_with_exact_resources(self) -> None:
        """Test that units can be produced with exactly the required resources.

        LRR Reference: Rule 67.1 - Resources equal to cost is sufficient
        """
        manager = ProductionManager()

        # Create a space dock (cost 4) with exact resources
        unit_type = UnitType.SPACE_DOCK
        available_resources = 4

        can_produce = manager.can_afford_unit(unit_type, available_resources)
        assert can_produce is True


class TestRule67DualUnitProduction:
    """Test dual unit production mechanics (Rule 67.2)."""

    def test_fighter_dual_production(self) -> None:
        """Test that fighters produce two units for their cost.

        LRR Reference: Rule 67.2 - "Cost with two icons (fighters/infantry)
        produces two units for that cost"
        """
        manager = ProductionManager()

        # Fighter cost should produce 2 units
        unit_type = UnitType.FIGHTER
        units_produced = manager.get_units_produced_for_cost(unit_type)
        assert units_produced == 2

    def test_infantry_dual_production(self) -> None:
        """Test that infantry produce two units for their cost.

        LRR Reference: Rule 67.2 - Fighters and infantry both have dual production
        """
        manager = ProductionManager()

        # Infantry cost should produce 2 units
        unit_type = UnitType.INFANTRY
        units_produced = manager.get_units_produced_for_cost(unit_type)
        assert units_produced == 2

    def test_single_unit_production(self) -> None:
        """Test that other units produce only one unit for their cost.

        LRR Reference: Rule 67.2 - Only fighters/infantry have dual production
        """
        manager = ProductionManager()

        # Cruiser should produce only 1 unit
        unit_type = UnitType.CRUISER
        units_produced = manager.get_units_produced_for_cost(unit_type)
        assert units_produced == 1


class TestRule67ShipProductionRestriction:
    """Test ship production restriction mechanics (Rule 67.6)."""

    def test_cannot_produce_ships_with_enemy_ships_present(self) -> None:
        """Test that ships cannot be produced in systems with enemy ships.

        LRR Reference: Rule 67.6 - "Cannot produce ships in system containing
        other players' ships"
        """
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.planet import Planet
        from src.ti4.core.system import System

        manager = ProductionManager()

        # Create galaxy and system with enemy ships
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)

        # Add planet and space dock
        planet = Planet("planet_a", resources=2, influence=1)
        system.add_planet(planet)

        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        system.place_unit_on_planet(space_dock, "planet_a")

        # Add enemy ship
        enemy_ship = Unit(unit_type=UnitType.DESTROYER, owner="player2")
        system.place_unit_in_space(enemy_ship)

        # Should not be able to produce ships
        can_produce = manager.can_produce_ships_in_system(system, "player1")
        assert can_produce is False

    def test_can_produce_ships_without_enemy_ships(self) -> None:
        """Test that ships can be produced in systems without enemy ships.

        LRR Reference: Rule 67.6 - Restriction only applies when enemy ships present
        """
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.planet import Planet
        from src.ti4.core.system import System

        manager = ProductionManager()

        # Create galaxy and system without enemy ships
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)

        # Add planet and space dock
        planet = Planet("planet_a", resources=2, influence=1)
        system.add_planet(planet)

        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        system.place_unit_on_planet(space_dock, "planet_a")

        # Should be able to produce ships (no enemy ships)
        can_produce = manager.can_produce_ships_in_system(system, "player1")
        assert can_produce is True


class TestRule67ReinforcementLimits:
    """Test reinforcement limit mechanics (Rule 67.5)."""

    def test_can_produce_unit_with_available_reinforcements(self) -> None:
        """Test that units can be produced when reinforcements are available.

        LRR Reference: Rule 67.5 - "Players limited by units in reinforcements"
        """
        manager = ProductionManager()

        # Player has 2 fighters available in reinforcements
        unit_type = UnitType.FIGHTER
        available_reinforcements = 2

        can_produce = manager.can_produce_from_reinforcements(
            unit_type, available_reinforcements, 1
        )
        assert can_produce is True

    def test_cannot_produce_unit_without_reinforcements(self) -> None:
        """Test that units cannot be produced when no reinforcements available.

        LRR Reference: Rule 67.5 - Limited by units in reinforcements
        """
        manager = ProductionManager()

        # Player has 0 fighters available in reinforcements
        unit_type = UnitType.FIGHTER
        available_reinforcements = 0

        can_produce = manager.can_produce_from_reinforcements(
            unit_type, available_reinforcements, 1
        )
        assert can_produce is False

    def test_dual_unit_production_requires_sufficient_reinforcements(self) -> None:
        """Test that dual unit production requires sufficient reinforcements.

        LRR Reference: Rule 67.5 + 67.2 - Dual production limited by reinforcements
        """
        manager = ProductionManager()

        # Player wants to produce 1 fighter (which produces 2 units) but only has 1 in reinforcements
        unit_type = UnitType.FIGHTER
        available_reinforcements = 1
        units_to_produce = 1  # This would produce 2 fighters due to dual production

        can_produce = manager.can_produce_from_reinforcements(
            unit_type, available_reinforcements, units_to_produce
        )
        assert can_produce is False


class TestRule67Integration:
    """Test integration between different production rules."""

    def test_complete_production_validation(self) -> None:
        """Test complete production validation combining multiple rules.

        This test validates the integration of:
        - Rule 67.1: Unit cost validation
        - Rule 67.2: Dual unit production
        - Rule 67.5: Reinforcement limits
        - Rule 67.6: Ship production restrictions
        """
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.planet import Planet
        from src.ti4.core.system import System
        from src.ti4.core.unit import Unit

        manager = ProductionManager()

        # Create system without enemy ships
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)

        planet = Planet("planet_a", resources=2, influence=1)
        system.add_planet(planet)

        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        system.place_unit_on_planet(space_dock, "planet_a")

        # Test fighter production (dual unit, cost 1)
        unit_type = UnitType.FIGHTER
        available_resources = 2  # Enough for 2 fighter productions
        available_reinforcements = 3  # Only 3 fighters available
        units_to_produce = 2  # Want to produce 2 times (= 4 fighters total)

        # Check all validation steps
        can_afford = manager.can_afford_unit(unit_type, available_resources)
        can_produce_ships = manager.can_produce_ships_in_system(system, "player1")
        can_produce_reinforcements = manager.can_produce_from_reinforcements(
            unit_type, available_reinforcements, units_to_produce
        )

        # Should pass cost and ship restrictions but fail reinforcement limits
        assert can_afford is True
        assert can_produce_ships is True
        assert can_produce_reinforcements is False  # Need 4 fighters but only have 3


class TestRule67BlockadeIntegration:
    """Test integration between production and blockade systems."""

    def test_production_integrates_with_blockade_manager(self) -> None:
        """Test that production system properly integrates with blockade manager.

        LRR Reference: Rule 67.6 + Rule 14.1 - Production restrictions with blockade integration
        """
        from src.ti4.core.blockade import BlockadeManager
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.planet import Planet
        from src.ti4.core.system import System

        manager = ProductionManager()

        # Create galaxy and system with blockaded space dock
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)

        # Add planet and space dock
        planet = Planet("planet_a", resources=2, influence=1)
        system.add_planet(planet)

        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        system.place_unit_on_planet(space_dock, "planet_a")

        # Add enemy ship to create blockade
        enemy_ship = Unit(unit_type=UnitType.DESTROYER, owner="player2")
        system.place_unit_in_space(enemy_ship)

        # Create blockade manager and check integration
        blockade_manager = BlockadeManager(galaxy)

        # Production system should integrate with blockade manager
        can_produce_ships = manager.can_produce_ships_with_blockade_check(
            space_dock, blockade_manager
        )
        assert can_produce_ships is False  # Blockaded units cannot produce ships

    def test_production_allows_ships_when_not_blockaded(self) -> None:
        """Test that production allows ships when unit is not blockaded.

        LRR Reference: Rule 67.6 + Rule 14.1 - Production allowed when not blockaded
        """
        from src.ti4.core.blockade import BlockadeManager
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.planet import Planet
        from src.ti4.core.system import System

        manager = ProductionManager()

        # Create galaxy and system without blockade
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)

        # Add planet and space dock
        planet = Planet("planet_a", resources=2, influence=1)
        system.add_planet(planet)

        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        system.place_unit_on_planet(space_dock, "planet_a")

        # Add friendly ship (no blockade)
        friendly_ship = Unit(unit_type=UnitType.DESTROYER, owner="player1")
        system.place_unit_in_space(friendly_ship)

        # Create blockade manager and check integration
        blockade_manager = BlockadeManager(galaxy)

        # Production system should allow ships when not blockaded
        can_produce_ships = manager.can_produce_ships_with_blockade_check(
            space_dock, blockade_manager
        )
        assert can_produce_ships is True  # Non-blockaded units can produce ships


class TestRule67TacticalActionIntegration:
    """Test integration between production and tactical action systems."""

    def test_production_step_can_be_created(self) -> None:
        """Test that ProductionStep can be created for tactical actions.

        LRR Reference: Rule 67.3 - Production during tactical action
        """
        from src.ti4.actions.production_step import ProductionStep

        # Should be able to create a production step
        step = ProductionStep()
        assert step is not None

    def test_production_step_integrates_with_tactical_action(self) -> None:
        """Test that ProductionStep integrates with tactical action workflow.

        LRR Reference: Rule 67.3 - Production follows tactical action rules
        """
        from src.ti4.actions.production_step import ProductionStep
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.planet import Planet
        from src.ti4.core.system import System

        step = ProductionStep()

        # Create galaxy and system for tactical action
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)

        # Add planet and space dock
        planet = Planet("planet_a", resources=2, influence=1)
        system.add_planet(planet)

        space_dock = Unit(unit_type=UnitType.SPACE_DOCK, owner="player1")
        system.place_unit_on_planet(space_dock, "planet_a")

        # Should be able to check if production is available
        can_execute = step.can_execute_legacy(system, "player1")
        assert can_execute is True  # System has production unit

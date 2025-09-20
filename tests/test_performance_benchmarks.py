"""Performance benchmarks and profiling tests."""

import time

from src.ti4.core.constants import UnitType
from src.ti4.core.galaxy import Galaxy
from src.ti4.core.game_state import GameState
from src.ti4.core.movement import MovementValidator
from src.ti4.core.player import Player
from src.ti4.core.unit import Unit
from src.ti4.core.unit_stats import UnitStatsProvider


class TestPerformanceBenchmarks:
    """Benchmark tests for performance-critical operations."""

    def test_unit_stats_calculation_performance(self) -> None:
        """Benchmark unit stats calculation performance."""
        UnitStatsProvider()

        # Create many units for testing
        units = []
        for i in range(1000):
            unit_type = [
                UnitType.CRUISER,
                UnitType.DESTROYER,
                UnitType.CARRIER,
                UnitType.FIGHTER,
            ][i % 4]
            unit = Unit(unit_type=unit_type, owner=f"player{i % 4}")
            units.append(unit)

        # Benchmark stats calculation
        start_time = time.time()

        for unit in units:
            # Calculate stats multiple times to simulate game operations
            unit.get_combat()
            unit.get_movement()
            unit.get_capacity()
            unit.get_cost()

        end_time = time.time()
        calculation_time = end_time - start_time

        # Should complete within reasonable time (adjust threshold as needed)
        assert calculation_time < 1.0, (
            f"Stats calculation took {calculation_time:.3f}s, expected < 1.0s"
        )

        print(f"Unit stats calculation for 1000 units: {calculation_time:.3f}s")

    def test_movement_validation_performance(self) -> None:
        """Benchmark movement validation performance."""
        galaxy = Galaxy()
        validator = MovementValidator(galaxy)

        # Create a large galaxy with many systems
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.system import System

        systems = []
        for x in range(-5, 6):
            for y in range(-5, 6):
                if abs(x) + abs(y) <= 5:  # Create hexagonal galaxy
                    coord = HexCoordinate(x, y)
                    system_id = f"system_{x}_{y}"
                    system = System(system_id)

                    galaxy.place_system(coord, system_id)
                    galaxy.register_system(system)
                    systems.append(system)

        # Create units in systems
        units = []
        for i, system in enumerate(systems[:50]):  # Limit to 50 systems for performance
            unit = Unit(unit_type=UnitType.CRUISER, owner=f"player{i % 4}")
            system.place_unit_in_space(unit)
            units.append((unit, system))

        # Benchmark movement validation
        start_time = time.time()

        from src.ti4.core.movement import MovementOperation

        for unit, from_system in units:
            # Try to validate movement to adjacent systems
            for target_system in systems[:10]:  # Check first 10 systems
                if target_system != from_system:
                    movement = MovementOperation(
                        unit=unit,
                        from_system_id=from_system.system_id,
                        to_system_id=target_system.system_id,
                        player_id=f"player{units.index((unit, from_system)) % 4}",
                    )
                    validator.validate_movement(movement)

        end_time = time.time()
        validation_time = end_time - start_time

        # Should complete within reasonable time
        assert validation_time < 3.5, (
            f"Movement validation took {validation_time:.3f}s, expected < 3.5s"
        )

        print(f"Movement validation for {len(units)} units: {validation_time:.3f}s")

    def test_cached_operations_performance(self) -> None:
        """Test performance of cached vs non-cached operations."""
        # Create units with technologies for caching test
        units = []
        for _i in range(100):
            unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
            # Add some technologies to test caching
            unit.add_technology("gravity_drive")
            unit.add_technology("cruiser_ii")
            units.append(unit)

        # Benchmark repeated stats access (should benefit from caching)
        start_time = time.time()

        for _ in range(10):  # Multiple iterations to test caching
            for unit in units:
                unit.get_movement()
                unit.get_combat()
                unit.get_capacity()

        end_time = time.time()
        cached_time = end_time - start_time

        print(f"Cached operations for 100 units (10 iterations): {cached_time:.3f}s")

        # Should be reasonably fast with caching
        assert cached_time < 0.5, (
            f"Cached operations took {cached_time:.3f}s, expected < 0.5s"
        )

    def test_game_state_operations_performance(self) -> None:
        """Benchmark game state operations."""
        # Create a game state with multiple players and units
        game_state = GameState()

        # Add players
        for i in range(4):
            player = Player(f"player{i}", f"Faction {i}")
            game_state = game_state.add_player(player)

        # Create units for each player using scenario builder approach
        start_time = time.time()

        # Create systems and place units
        from src.ti4.core.system import System

        for player_id in range(4):
            system_id = f"system_{player_id}"
            system = System(system_id)

            for unit_type in [
                UnitType.CRUISER,
                UnitType.DESTROYER,
                UnitType.CARRIER,
                UnitType.FIGHTER,
                UnitType.INFANTRY,
            ]:
                for _ in range(5):  # 5 of each unit type per player
                    unit = Unit(unit_type=unit_type, owner=f"player{player_id}")
                    system.place_unit_in_space(unit)

            # Add system to game state
            new_systems = game_state.systems.copy()
            new_systems[system_id] = system
            game_state = game_state._create_new_state(systems=new_systems)

        end_time = time.time()
        creation_time = end_time - start_time

        print(f"Game state creation with 100 units: {creation_time:.3f}s")

        # Should complete within reasonable time
        assert creation_time < 1.0, (
            f"Game state operations took {creation_time:.3f}s, expected < 1.0s"
        )

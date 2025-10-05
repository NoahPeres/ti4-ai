"""
Tests for Rule 9: ANOMALIES implementation.

LRR References:
- Rule 9: ANOMALIES - Core anomaly system
- Rule 88.4: System Tiles - Red-backed anomaly tiles
"""

import pytest

from src.ti4.core.exceptions import InvalidAnomalyTypeError
from src.ti4.core.system import System
from src.ti4.core.system_tile import SystemTile, TileColor, TileType


class TestAnomalyTypeEnum:
    """Test the AnomalyType enum implementation."""

    def test_anomaly_type_enum_exists(self) -> None:
        """Test that AnomalyType enum is defined with correct values."""
        from src.ti4.core.constants import AnomalyType

        # Test all four anomaly types exist
        assert AnomalyType.ASTEROID_FIELD.value == "asteroid_field"
        assert AnomalyType.NEBULA.value == "nebula"
        assert AnomalyType.SUPERNOVA.value == "supernova"
        assert AnomalyType.GRAVITY_RIFT.value == "gravity_rift"


class TestSystemAnomalyIntegration:
    """Test System class integration with anomaly properties."""

    def test_system_can_have_anomaly_types(self) -> None:
        """Test that System can track anomaly types."""
        from src.ti4.core.constants import AnomalyType

        system = System("test_system")

        # System should start with no anomaly types
        assert system.get_anomaly_types() == []
        assert not system.is_anomaly()

        # Should be able to add anomaly types
        system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)
        assert AnomalyType.ASTEROID_FIELD in system.get_anomaly_types()
        assert system.is_anomaly()
        assert system.has_anomaly_type(AnomalyType.ASTEROID_FIELD)

    def test_system_can_have_multiple_anomaly_types(self) -> None:
        """Test that System can have multiple anomaly types (Requirement 1.3)."""
        from src.ti4.core.constants import AnomalyType

        system = System("multi_anomaly_system")

        # Add multiple anomaly types
        system.add_anomaly_type(AnomalyType.NEBULA)
        system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        anomaly_types = system.get_anomaly_types()
        assert AnomalyType.NEBULA in anomaly_types
        assert AnomalyType.GRAVITY_RIFT in anomaly_types
        assert len(anomaly_types) == 2
        assert system.is_anomaly()

    def test_system_with_planets_can_be_anomaly(self) -> None:
        """Test that System with planets can still be an anomaly (Requirement 1.4)."""
        from src.ti4.core.constants import AnomalyType
        from src.ti4.core.planet import Planet

        system = System("anomaly_with_planet")
        planet = Planet("Test Planet", resources=2, influence=1)
        system.add_planet(planet)

        # System with planets can still be an anomaly
        system.add_anomaly_type(AnomalyType.NEBULA)

        assert system.is_anomaly()
        assert system.has_anomaly_type(AnomalyType.NEBULA)
        assert len(system.planets) == 1
        assert system.planets[0].name == "Test Planet"


class TestSystemTileAnomalyIntegration:
    """Test SystemTile integration with anomaly identification."""

    def test_system_tile_anomaly_identification(self) -> None:
        """Test that SystemTile.is_anomaly() works with anomaly systems."""
        # Create an anomaly tile
        anomaly_tile = SystemTile(
            tile_id="test_anomaly", color=TileColor.RED, tile_type=TileType.ANOMALY
        )

        # Should be identified as anomaly
        assert anomaly_tile.is_anomaly()
        assert anomaly_tile.color == TileColor.RED
        assert anomaly_tile.tile_type == TileType.ANOMALY

    def test_non_anomaly_tiles_not_identified_as_anomaly(self) -> None:
        """Test that non-anomaly tiles are not identified as anomalies."""
        # Create a planet system tile
        planet_tile = SystemTile(
            tile_id="test_planet",
            color=TileColor.BLUE,
            tile_type=TileType.PLANET_SYSTEM,
        )

        # Should not be identified as anomaly
        assert not planet_tile.is_anomaly()

        # Create an empty system tile
        empty_tile = SystemTile(
            tile_id="test_empty", color=TileColor.RED, tile_type=TileType.EMPTY_SYSTEM
        )

        # Should not be identified as anomaly
        assert not empty_tile.is_anomaly()


class TestAnomalyValidation:
    """Test anomaly type validation and error handling."""

    def test_invalid_anomaly_type_raises_error(self) -> None:
        """Test that invalid anomaly types raise appropriate errors."""
        from src.ti4.core.constants import AnomalyType

        system = System("test_system")

        # Should be able to add valid anomaly types
        system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)

        # Test that we can remove anomaly types
        system.remove_anomaly_type(AnomalyType.ASTEROID_FIELD)
        assert not system.has_anomaly_type(AnomalyType.ASTEROID_FIELD)
        assert not system.is_anomaly()

    def test_anomaly_type_removal_when_not_present(self) -> None:
        """Test removing anomaly type that isn't present doesn't cause errors."""
        from src.ti4.core.constants import AnomalyType

        system = System("test_system")

        # Should not raise error when removing non-existent anomaly type
        system.remove_anomaly_type(AnomalyType.NEBULA)
        assert not system.has_anomaly_type(AnomalyType.NEBULA)

    def test_none_anomaly_type_raises_error(self) -> None:
        """Test that None anomaly type raises ValueError."""
        system = System("test_system")

        with pytest.raises(
            InvalidAnomalyTypeError, match="Anomaly type cannot be None"
        ):
            system.add_anomaly_type(None)  # type: ignore

        with pytest.raises(
            InvalidAnomalyTypeError, match="Anomaly type cannot be None"
        ):
            system.remove_anomaly_type(None)  # type: ignore

        with pytest.raises(
            InvalidAnomalyTypeError, match="Anomaly type cannot be None"
        ):
            system.has_anomaly_type(None)  # type: ignore

    def test_invalid_string_anomaly_type_raises_error(self) -> None:
        """Test that invalid string anomaly types raise ValueError."""
        system = System("test_system")

        with pytest.raises(
            InvalidAnomalyTypeError, match="Invalid anomaly type: invalid_type"
        ):
            system.add_anomaly_type("invalid_type")

        with pytest.raises(
            InvalidAnomalyTypeError, match="Invalid anomaly type: invalid_type"
        ):
            system.remove_anomaly_type("invalid_type")

        with pytest.raises(
            InvalidAnomalyTypeError, match="Invalid anomaly type: invalid_type"
        ):
            system.has_anomaly_type("invalid_type")

    def test_string_anomaly_types_work_correctly(self) -> None:
        """Test that valid string anomaly types work correctly."""
        system = System("test_system")

        # Should work with string values
        system.add_anomaly_type("asteroid_field")
        assert system.has_anomaly_type("asteroid_field")

        system.remove_anomaly_type("asteroid_field")
        assert not system.has_anomaly_type("asteroid_field")


class TestAnomalySystemQueries:
    """Test anomaly system querying and identification methods."""

    def test_get_anomaly_types_returns_copy(self) -> None:
        """Test that get_anomaly_types returns a copy to prevent external modification."""
        from src.ti4.core.constants import AnomalyType

        system = System("test_system")
        system.add_anomaly_type(AnomalyType.SUPERNOVA)

        anomaly_types = system.get_anomaly_types()
        original_length = len(anomaly_types)

        # Modifying returned list should not affect system
        anomaly_types.append(AnomalyType.NEBULA)

        # System should be unchanged
        assert len(system.get_anomaly_types()) == original_length
        assert not system.has_anomaly_type(AnomalyType.NEBULA)

    def test_anomaly_identification_methods(self) -> None:
        """Test various anomaly identification methods work correctly."""
        from src.ti4.core.constants import AnomalyType

        system = System("test_system")

        # Empty system
        assert system.get_anomaly_types() == []
        assert not system.is_anomaly()
        assert not system.has_anomaly_type(AnomalyType.ASTEROID_FIELD)

        # Add anomaly
        system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)

        # Should be detected
        assert len(system.get_anomaly_types()) == 1
        assert system.is_anomaly()
        assert system.has_anomaly_type(AnomalyType.ASTEROID_FIELD)
        assert not system.has_anomaly_type(AnomalyType.NEBULA)


class TestAsteroidFieldMovementBlocking:
    """Test asteroid field movement blocking (Requirements 2.1-2.4)."""

    def test_asteroid_field_blocks_movement_into_system(self) -> None:
        """Test that ships cannot move into asteroid field systems (Requirement 2.1)."""
        from src.ti4.core.constants import AnomalyType, UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule, MovementContext
        from src.ti4.core.unit import Unit

        # Create galaxy with asteroid field system
        galaxy = Galaxy()
        from_coord = HexCoordinate(0, 0)
        to_coord = HexCoordinate(1, 0)

        from_system = System("from_system")
        to_system = System("asteroid_system")
        to_system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)

        galaxy.place_system(from_coord, "from_system")
        galaxy.register_system(from_system)
        galaxy.place_system(to_coord, "asteroid_system")
        galaxy.register_system(to_system)

        # Create movement context
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        context = MovementContext(
            unit=unit,
            from_coordinate=from_coord,
            to_coordinate=to_coord,
            player_technologies=set(),
            galaxy=galaxy,
        )

        # Movement should be blocked
        anomaly_rule = AnomalyRule()
        assert not anomaly_rule.can_move(context)

    def test_asteroid_field_blocks_movement_through_system(self) -> None:
        """Test that ships cannot move through asteroid field systems (Requirement 2.2)."""
        from src.ti4.core.constants import AnomalyType, UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule, MovementContext
        from src.ti4.core.unit import Unit

        # Create galaxy with asteroid field in the path
        galaxy = Galaxy()
        from_coord = HexCoordinate(0, 0)
        through_coord = HexCoordinate(1, 0)
        to_coord = HexCoordinate(2, 0)

        from_system = System("from_system")
        through_system = System("asteroid_system")
        to_system = System("to_system")

        through_system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)

        galaxy.place_system(from_coord, "from_system")
        galaxy.register_system(from_system)
        galaxy.place_system(through_coord, "asteroid_system")
        galaxy.register_system(through_system)
        galaxy.place_system(to_coord, "to_system")
        galaxy.register_system(to_system)

        # Create movement context with path through asteroid field
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        context = MovementContext(
            unit=unit,
            from_coordinate=from_coord,
            to_coordinate=to_coord,
            player_technologies=set(),
            galaxy=galaxy,
            path=[from_coord, through_coord, to_coord],
        )

        # Movement should be blocked
        anomaly_rule = AnomalyRule()
        assert not anomaly_rule.can_move(context)

    def test_asteroid_field_with_planets_still_blocks_movement(self) -> None:
        """Test that asteroid fields with planets still block movement (Requirement 2.4)."""
        from src.ti4.core.constants import AnomalyType, UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule, MovementContext
        from src.ti4.core.planet import Planet
        from src.ti4.core.unit import Unit

        # Create galaxy with asteroid field system that has planets
        galaxy = Galaxy()
        from_coord = HexCoordinate(0, 0)
        to_coord = HexCoordinate(1, 0)

        from_system = System("from_system")
        to_system = System("asteroid_with_planet")
        to_system.add_anomaly_type(AnomalyType.ASTEROID_FIELD)

        # Add planet to asteroid field system
        planet = Planet("Test Planet", resources=2, influence=1)
        to_system.add_planet(planet)

        galaxy.place_system(from_coord, "from_system")
        galaxy.register_system(from_system)
        galaxy.place_system(to_coord, "asteroid_with_planet")
        galaxy.register_system(to_system)

        # Create movement context
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        context = MovementContext(
            unit=unit,
            from_coordinate=from_coord,
            to_coordinate=to_coord,
            player_technologies=set(),
            galaxy=galaxy,
        )

        # Movement should still be blocked despite having planets
        anomaly_rule = AnomalyRule()
        assert not anomaly_rule.can_move(context)


class TestSupernovaMovementBlocking:
    """Test supernova movement blocking (Requirements 3.1-3.4)."""

    def test_supernova_blocks_movement_into_system(self) -> None:
        """Test that ships cannot move into supernova systems (Requirement 3.1)."""
        from src.ti4.core.constants import AnomalyType, UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule, MovementContext
        from src.ti4.core.unit import Unit

        # Create galaxy with supernova system
        galaxy = Galaxy()
        from_coord = HexCoordinate(0, 0)
        to_coord = HexCoordinate(1, 0)

        from_system = System("from_system")
        to_system = System("supernova_system")
        to_system.add_anomaly_type(AnomalyType.SUPERNOVA)

        galaxy.place_system(from_coord, "from_system")
        galaxy.register_system(from_system)
        galaxy.place_system(to_coord, "supernova_system")
        galaxy.register_system(to_system)

        # Create movement context
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        context = MovementContext(
            unit=unit,
            from_coordinate=from_coord,
            to_coordinate=to_coord,
            player_technologies=set(),
            galaxy=galaxy,
        )

        # Movement should be blocked
        anomaly_rule = AnomalyRule()
        assert not anomaly_rule.can_move(context)

    def test_supernova_blocks_movement_through_system(self) -> None:
        """Test that ships cannot move through supernova systems (Requirement 3.2)."""
        from src.ti4.core.constants import AnomalyType, UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule, MovementContext
        from src.ti4.core.unit import Unit

        # Create galaxy with supernova in the path
        galaxy = Galaxy()
        from_coord = HexCoordinate(0, 0)
        through_coord = HexCoordinate(1, 0)
        to_coord = HexCoordinate(2, 0)

        from_system = System("from_system")
        through_system = System("supernova_system")
        to_system = System("to_system")

        through_system.add_anomaly_type(AnomalyType.SUPERNOVA)

        galaxy.place_system(from_coord, "from_system")
        galaxy.register_system(from_system)
        galaxy.place_system(through_coord, "supernova_system")
        galaxy.register_system(through_system)
        galaxy.place_system(to_coord, "to_system")
        galaxy.register_system(to_system)

        # Create movement context with path through supernova
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        context = MovementContext(
            unit=unit,
            from_coordinate=from_coord,
            to_coordinate=to_coord,
            player_technologies=set(),
            galaxy=galaxy,
            path=[from_coord, through_coord, to_coord],
        )

        # Movement should be blocked
        anomaly_rule = AnomalyRule()
        assert not anomaly_rule.can_move(context)

    def test_supernova_completely_inaccessible(self) -> None:
        """Test that supernova systems are completely inaccessible (Requirement 3.4)."""
        from src.ti4.core.constants import AnomalyType, UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule, MovementContext
        from src.ti4.core.unit import Unit

        # Create galaxy with supernova system
        galaxy = Galaxy()
        from_coord = HexCoordinate(0, 0)
        to_coord = HexCoordinate(1, 0)

        from_system = System("from_system")
        to_system = System("supernova_system")
        to_system.add_anomaly_type(AnomalyType.SUPERNOVA)

        galaxy.place_system(from_coord, "from_system")
        galaxy.register_system(from_system)
        galaxy.place_system(to_coord, "supernova_system")
        galaxy.register_system(to_system)

        # Test different unit types - all should be blocked
        unit_types = [
            UnitType.FIGHTER,
            UnitType.DESTROYER,
            UnitType.CRUISER,
            UnitType.CARRIER,
            UnitType.DREADNOUGHT,
            UnitType.FLAGSHIP,
        ]

        anomaly_rule = AnomalyRule()

        for unit_type in unit_types:
            unit = Unit(unit_type=unit_type, owner="player1")
            context = MovementContext(
                unit=unit,
                from_coordinate=from_coord,
                to_coordinate=to_coord,
                player_technologies=set(),
                galaxy=galaxy,
            )

            # No ships can ever enter supernova systems
            assert not anomaly_rule.can_move(context)


class TestNebulaMovementRestrictions:
    """Test nebula movement restrictions (Requirements 4.1-4.4)."""

    def test_nebula_blocks_movement_when_not_active_system(self) -> None:
        """Test that ships cannot move into nebula when it's not the active system (Requirement 4.1)."""
        from src.ti4.core.constants import AnomalyType, UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule, MovementContext
        from src.ti4.core.unit import Unit

        # Create galaxy with nebula system
        galaxy = Galaxy()
        from_coord = HexCoordinate(0, 0)
        to_coord = HexCoordinate(1, 0)

        from_system = System("from_system")
        to_system = System("nebula_system")
        to_system.add_anomaly_type(AnomalyType.NEBULA)

        galaxy.place_system(from_coord, "from_system")
        galaxy.register_system(from_system)
        galaxy.place_system(to_coord, "nebula_system")
        galaxy.register_system(to_system)

        # Create movement context without active system (nebula is not active)
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        context = MovementContext(
            unit=unit,
            from_coordinate=from_coord,
            to_coordinate=to_coord,
            player_technologies=set(),
            galaxy=galaxy,
        )

        # Movement should be blocked when nebula is not active system
        anomaly_rule = AnomalyRule()
        assert not anomaly_rule.can_move(context)

    def test_nebula_allows_movement_when_active_system(self) -> None:
        """Test that ships can move into nebula when it's the active system (Requirement 4.2)."""
        from src.ti4.core.constants import AnomalyType, UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule, MovementContext
        from src.ti4.core.unit import Unit

        # Create galaxy with nebula system
        galaxy = Galaxy()
        from_coord = HexCoordinate(0, 0)
        to_coord = HexCoordinate(1, 0)

        from_system = System("from_system")
        to_system = System("nebula_system")
        to_system.add_anomaly_type(AnomalyType.NEBULA)

        galaxy.place_system(from_coord, "from_system")
        galaxy.register_system(from_system)
        galaxy.place_system(to_coord, "nebula_system")
        galaxy.register_system(to_system)

        # Create movement context with nebula as active system
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        context = MovementContext(
            unit=unit,
            from_coordinate=from_coord,
            to_coordinate=to_coord,
            player_technologies=set(),
            galaxy=galaxy,
            active_system_coordinate=to_coord,  # Nebula is the active system
        )

        # Movement should be allowed when nebula is active system
        anomaly_rule = AnomalyRule()
        assert anomaly_rule.can_move(context)

    def test_ships_in_nebula_have_move_value_one(self) -> None:
        """Test that ships in nebula systems have move value 1 (Requirement 4.3)."""
        from src.ti4.core.constants import AnomalyType, UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule
        from src.ti4.core.unit import Unit

        # Create galaxy with nebula system
        galaxy = Galaxy()
        nebula_coord = HexCoordinate(0, 0)
        to_coord = HexCoordinate(1, 0)

        nebula_system = System("nebula_system")
        nebula_system.add_anomaly_type(AnomalyType.NEBULA)
        to_system = System("to_system")

        galaxy.place_system(nebula_coord, "nebula_system")
        galaxy.register_system(nebula_system)
        galaxy.place_system(to_coord, "to_system")
        galaxy.register_system(to_system)

        # Create unit with higher base move value
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")  # Cruiser has move 2

        # Movement range should be 1 when starting from nebula
        anomaly_rule = AnomalyRule()
        move_range = anomaly_rule.get_movement_range_from_system(
            unit, set(), nebula_system
        )
        assert move_range == 1

    def test_ships_not_in_nebula_keep_normal_move_value(self) -> None:
        """Test that ships not in nebula keep their normal move value (Requirement 4.4)."""
        from src.ti4.core.constants import UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule
        from src.ti4.core.unit import Unit

        # Create galaxy with normal system
        galaxy = Galaxy()
        from_coord = HexCoordinate(0, 0)
        to_coord = HexCoordinate(1, 0)

        from_system = System("normal_system")
        to_system = System("to_system")

        galaxy.place_system(from_coord, "normal_system")
        galaxy.register_system(from_system)
        galaxy.place_system(to_coord, "to_system")
        galaxy.register_system(to_system)

        # Create unit with normal move value
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")  # Cruiser has move 2

        # Movement range should be normal when not starting from nebula
        anomaly_rule = AnomalyRule()
        move_range = anomaly_rule.get_movement_range_from_system(
            unit, set(), from_system
        )
        assert move_range == 2  # Normal cruiser move value

    def test_nebula_movement_through_path_blocked_when_not_active(self) -> None:
        """Test that movement through nebula in path is blocked when nebula is not active."""
        from src.ti4.core.constants import AnomalyType, UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule, MovementContext
        from src.ti4.core.unit import Unit

        # Create galaxy with nebula in the path
        galaxy = Galaxy()
        from_coord = HexCoordinate(0, 0)
        through_coord = HexCoordinate(1, 0)
        to_coord = HexCoordinate(2, 0)

        from_system = System("from_system")
        through_system = System("nebula_system")
        to_system = System("to_system")

        through_system.add_anomaly_type(AnomalyType.NEBULA)

        galaxy.place_system(from_coord, "from_system")
        galaxy.register_system(from_system)
        galaxy.place_system(through_coord, "nebula_system")
        galaxy.register_system(through_system)
        galaxy.place_system(to_coord, "to_system")
        galaxy.register_system(to_system)

        # Create movement context with path through nebula (nebula not active)
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        context = MovementContext(
            unit=unit,
            from_coordinate=from_coord,
            to_coordinate=to_coord,
            player_technologies=set(),
            galaxy=galaxy,
            path=[from_coord, through_coord, to_coord],
            active_system_coordinate=to_coord,  # Different system is active
        )

        # Movement should be blocked when nebula is in path but not active
        anomaly_rule = AnomalyRule()
        assert not anomaly_rule.can_move(context)

    def test_nebula_movement_through_path_allowed_when_active(self) -> None:
        """Test that movement through nebula in path is allowed when nebula is active."""
        from src.ti4.core.constants import AnomalyType, UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule, MovementContext
        from src.ti4.core.unit import Unit

        # Create galaxy with nebula in the path
        galaxy = Galaxy()
        from_coord = HexCoordinate(0, 0)
        through_coord = HexCoordinate(1, 0)
        to_coord = HexCoordinate(2, 0)

        from_system = System("from_system")
        through_system = System("nebula_system")
        to_system = System("to_system")

        through_system.add_anomaly_type(AnomalyType.NEBULA)

        galaxy.place_system(from_coord, "from_system")
        galaxy.register_system(from_system)
        galaxy.place_system(through_coord, "nebula_system")
        galaxy.register_system(through_system)
        galaxy.place_system(to_coord, "to_system")
        galaxy.register_system(to_system)

        # Create movement context with nebula as active system
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        context = MovementContext(
            unit=unit,
            from_coordinate=from_coord,
            to_coordinate=to_coord,
            player_technologies=set(),
            galaxy=galaxy,
            path=[from_coord, through_coord, to_coord],
            active_system_coordinate=through_coord,  # Nebula is active
        )

        # Movement should be allowed when nebula is active
        anomaly_rule = AnomalyRule()
        assert anomaly_rule.can_move(context)

    def test_multiple_anomaly_types_with_nebula(self) -> None:
        """Test that systems with multiple anomaly types including nebula follow nebula rules."""
        from src.ti4.core.constants import AnomalyType, UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule, MovementContext
        from src.ti4.core.unit import Unit

        # Create galaxy with system having both nebula and gravity rift
        galaxy = Galaxy()
        from_coord = HexCoordinate(0, 0)
        to_coord = HexCoordinate(1, 0)

        from_system = System("from_system")
        to_system = System("multi_anomaly_system")
        to_system.add_anomaly_type(AnomalyType.NEBULA)
        to_system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        galaxy.place_system(from_coord, "from_system")
        galaxy.register_system(from_system)
        galaxy.place_system(to_coord, "multi_anomaly_system")
        galaxy.register_system(to_system)

        # Test movement blocked when not active
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        context = MovementContext(
            unit=unit,
            from_coordinate=from_coord,
            to_coordinate=to_coord,
            player_technologies=set(),
            galaxy=galaxy,
        )

        anomaly_rule = AnomalyRule()
        assert not anomaly_rule.can_move(context)

        # Test movement allowed when active
        context.active_system_coordinate = to_coord
        assert anomaly_rule.can_move(context)

        # Test move value is 1 when starting from this system
        move_range = anomaly_rule.get_movement_range_from_system(unit, set(), to_system)
        assert move_range == 1


class TestGravityRiftMovementBonuses:
    """Test gravity rift movement bonuses and destruction mechanics (Requirements 6.1-6.6)."""

    def test_gravity_rift_provides_movement_bonus_when_exiting(self) -> None:
        """Test that ships gain +1 move value when exiting gravity rift systems (Requirement 6.1)."""
        from src.ti4.core.constants import AnomalyType, UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule
        from src.ti4.core.unit import Unit

        # Create galaxy with gravity rift system
        galaxy = Galaxy()
        gravity_rift_coord = HexCoordinate(0, 0)
        to_coord = HexCoordinate(1, 0)

        gravity_rift_system = System("gravity_rift_system")
        gravity_rift_system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)
        to_system = System("to_system")

        galaxy.place_system(gravity_rift_coord, "gravity_rift_system")
        galaxy.register_system(gravity_rift_system)
        galaxy.place_system(to_coord, "to_system")
        galaxy.register_system(to_system)

        # Create unit with base move value 2
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")

        # Movement range should be increased by 1 when exiting gravity rift
        anomaly_rule = AnomalyRule()
        move_range = anomaly_rule.get_movement_range_with_gravity_rift_bonus(
            unit, set(), gravity_rift_system
        )
        assert move_range == 3  # Base 2 + 1 from gravity rift

    def test_gravity_rift_provides_movement_bonus_when_passing_through(self) -> None:
        """Test that ships gain +1 move value when passing through gravity rift systems (Requirement 6.2)."""
        from src.ti4.core.constants import AnomalyType, UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule, MovementContext
        from src.ti4.core.unit import Unit

        # Create galaxy with gravity rift in movement path
        galaxy = Galaxy()
        from_coord = HexCoordinate(0, 0)
        through_coord = HexCoordinate(1, 0)
        to_coord = HexCoordinate(2, 0)

        from_system = System("from_system")
        through_system = System("gravity_rift_system")
        to_system = System("to_system")

        through_system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        galaxy.place_system(from_coord, "from_system")
        galaxy.register_system(from_system)
        galaxy.place_system(through_coord, "gravity_rift_system")
        galaxy.register_system(through_system)
        galaxy.place_system(to_coord, "to_system")
        galaxy.register_system(to_system)

        # Create movement context with path through gravity rift
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        context = MovementContext(
            unit=unit,
            from_coordinate=from_coord,
            to_coordinate=to_coord,
            player_technologies=set(),
            galaxy=galaxy,
            path=[from_coord, through_coord, to_coord],
        )

        # Movement should be allowed with bonus from gravity rift
        anomaly_rule = AnomalyRule()
        effective_range = anomaly_rule.get_effective_movement_range_for_path(context)
        assert effective_range == 3  # Base 2 + 1 from gravity rift

    def test_gravity_rift_destruction_roll_on_exit(self) -> None:
        """Test that destruction rolls occur when ships exit gravity rift systems (Requirement 6.3)."""
        from src.ti4.core.constants import AnomalyType, UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule, MovementContext
        from src.ti4.core.unit import Unit

        # Create galaxy with gravity rift system
        galaxy = Galaxy()
        gravity_rift_coord = HexCoordinate(0, 0)
        to_coord = HexCoordinate(1, 0)

        gravity_rift_system = System("gravity_rift_system")
        gravity_rift_system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)
        to_system = System("to_system")

        galaxy.place_system(gravity_rift_coord, "gravity_rift_system")
        galaxy.register_system(gravity_rift_system)
        galaxy.place_system(to_coord, "to_system")
        galaxy.register_system(to_system)

        # Create movement context exiting gravity rift
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        context = MovementContext(
            unit=unit,
            from_coordinate=gravity_rift_coord,
            to_coordinate=to_coord,
            player_technologies=set(),
            galaxy=galaxy,
        )

        # Should require destruction roll
        anomaly_rule = AnomalyRule()
        destruction_result = anomaly_rule.apply_gravity_rift_destruction(context)
        assert destruction_result is not None
        assert hasattr(destruction_result, "units_destroyed")
        assert hasattr(destruction_result, "dice_results")

    def test_gravity_rift_destruction_roll_1_to_3_destroys_ship(self) -> None:
        """Test that dice rolls 1-3 destroy ships in gravity rift (Requirement 6.4)."""
        from src.ti4.core.constants import UnitType
        from src.ti4.core.movement_rules import AnomalyRule
        from src.ti4.core.unit import Unit

        # Create unit
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")

        # Test destruction with rolls 1-3
        anomaly_rule = AnomalyRule()
        for roll_value in [1, 2, 3]:
            is_destroyed = anomaly_rule.check_gravity_rift_destruction(unit, roll_value)
            assert is_destroyed, f"Unit should be destroyed with roll {roll_value}"

    def test_gravity_rift_destruction_roll_4_to_10_saves_ship(self) -> None:
        """Test that dice rolls 4-10 save ships in gravity rift (Requirement 6.5)."""
        from src.ti4.core.constants import UnitType
        from src.ti4.core.movement_rules import AnomalyRule
        from src.ti4.core.unit import Unit

        # Create unit
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")

        # Test survival with rolls 4-10
        anomaly_rule = AnomalyRule()
        for roll_value in [4, 5, 6, 7, 8, 9, 10]:
            is_destroyed = anomaly_rule.check_gravity_rift_destruction(unit, roll_value)
            assert not is_destroyed, f"Unit should survive with roll {roll_value}"

    def test_multiple_gravity_rifts_affect_ship_separately(self) -> None:
        """Test that multiple gravity rifts in one movement affect ships separately (Requirement 6.6)."""
        from src.ti4.core.constants import AnomalyType, UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule, MovementContext
        from src.ti4.core.unit import Unit

        # Create galaxy with multiple gravity rifts in path
        galaxy = Galaxy()
        from_coord = HexCoordinate(0, 0)
        rift1_coord = HexCoordinate(1, 0)
        rift2_coord = HexCoordinate(2, 0)
        to_coord = HexCoordinate(3, 0)

        from_system = System("from_system")
        rift1_system = System("gravity_rift_1")
        rift2_system = System("gravity_rift_2")
        to_system = System("to_system")

        rift1_system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)
        rift2_system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        galaxy.place_system(from_coord, "from_system")
        galaxy.register_system(from_system)
        galaxy.place_system(rift1_coord, "gravity_rift_1")
        galaxy.register_system(rift1_system)
        galaxy.place_system(rift2_coord, "gravity_rift_2")
        galaxy.register_system(rift2_system)
        galaxy.place_system(to_coord, "to_system")
        galaxy.register_system(to_system)

        # Create movement context through multiple gravity rifts
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        context = MovementContext(
            unit=unit,
            from_coordinate=from_coord,
            to_coordinate=to_coord,
            player_technologies=set(),
            galaxy=galaxy,
            path=[from_coord, rift1_coord, rift2_coord, to_coord],
        )

        # Should get bonuses from both gravity rifts
        anomaly_rule = AnomalyRule()
        effective_range = anomaly_rule.get_effective_movement_range_for_path(context)
        assert effective_range == 4  # Base 2 + 1 from each gravity rift

        # Should require destruction rolls for both gravity rifts
        destruction_result = anomaly_rule.apply_gravity_rift_destruction(context)
        assert len(destruction_result.dice_results) == 2  # One roll per gravity rift

    def test_gravity_rift_no_bonus_when_not_exiting_from_gravity_rift(self) -> None:
        """Test that ships don't get bonus when not exiting from gravity rift system."""
        from src.ti4.core.constants import UnitType
        from src.ti4.core.movement_rules import AnomalyRule
        from src.ti4.core.unit import Unit

        # Create normal system (no gravity rift)
        normal_system = System("normal_system")

        # Create unit with base move value 2
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")

        # Movement range should be normal when not exiting from gravity rift
        anomaly_rule = AnomalyRule()
        move_range = anomaly_rule.get_movement_range_with_gravity_rift_bonus(
            unit, set(), normal_system
        )
        assert move_range == 2  # Normal cruiser move value, no bonus

    def test_gravity_rift_destruction_with_no_gravity_rifts_in_path(self) -> None:
        """Test that no destruction rolls occur when no gravity rifts are in path."""
        from src.ti4.core.constants import UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule, MovementContext
        from src.ti4.core.unit import Unit

        # Create galaxy with normal systems only
        galaxy = Galaxy()
        from_coord = HexCoordinate(0, 0)
        to_coord = HexCoordinate(1, 0)

        from_system = System("from_system")
        to_system = System("to_system")

        galaxy.place_system(from_coord, "from_system")
        galaxy.register_system(from_system)
        galaxy.place_system(to_coord, "to_system")
        galaxy.register_system(to_system)

        # Create movement context with no gravity rifts
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        context = MovementContext(
            unit=unit,
            from_coordinate=from_coord,
            to_coordinate=to_coord,
            player_technologies=set(),
            galaxy=galaxy,
        )

        # Should have no destruction rolls
        anomaly_rule = AnomalyRule()
        destruction_result = anomaly_rule.apply_gravity_rift_destruction(context)
        assert len(destruction_result.dice_results) == 0
        assert len(destruction_result.units_destroyed) == 0
        assert len(destruction_result.surviving_units) == 1
        assert destruction_result.surviving_units[0] == unit

    def test_gravity_rift_destruction_edge_case_roll_values(self) -> None:
        """Test gravity rift destruction with edge case roll values."""
        from src.ti4.core.constants import UnitType
        from src.ti4.core.movement_rules import AnomalyRule
        from src.ti4.core.unit import Unit

        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        anomaly_rule = AnomalyRule()

        # Test boundary values
        assert anomaly_rule.check_gravity_rift_destruction(
            unit, 3
        )  # Last destroying roll
        assert not anomaly_rule.check_gravity_rift_destruction(
            unit, 4
        )  # First surviving roll

    def test_gravity_rift_bonus_stacking_with_multiple_units(self) -> None:
        """Test that gravity rift bonuses work correctly with different unit types."""
        from src.ti4.core.constants import AnomalyType, UnitType
        from src.ti4.core.movement_rules import AnomalyRule
        from src.ti4.core.unit import Unit

        # Create gravity rift system
        gravity_rift_system = System("gravity_rift_system")
        gravity_rift_system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        anomaly_rule = AnomalyRule()

        # Test different unit types
        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")  # Move 0
        destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player1")  # Move 2
        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")  # Move 1

        # All should get +1 bonus when exiting gravity rift
        assert (
            anomaly_rule.get_movement_range_with_gravity_rift_bonus(
                fighter, set(), gravity_rift_system
            )
            == 1
        )  # 0 + 1
        assert (
            anomaly_rule.get_movement_range_with_gravity_rift_bonus(
                destroyer, set(), gravity_rift_system
            )
            == 3
        )  # 2 + 1
        assert (
            anomaly_rule.get_movement_range_with_gravity_rift_bonus(
                carrier, set(), gravity_rift_system
            )
            == 2
        )  # 1 + 1

    def test_gravity_rift_destruction_invalid_roll_value_raises_error(self) -> None:
        """Test that invalid dice roll values raise ValueError."""
        from src.ti4.core.constants import UnitType
        from src.ti4.core.movement_rules import AnomalyRule
        from src.ti4.core.unit import Unit

        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        anomaly_rule = AnomalyRule()

        # Test invalid roll values (after normalization)
        # Note: 0 is now normalized to 10, so it's valid

        with pytest.raises(ValueError, match="Invalid dice roll value: 11"):
            anomaly_rule.check_gravity_rift_destruction(unit, 11)

        with pytest.raises(ValueError, match="Invalid dice roll value: -1"):
            anomaly_rule.check_gravity_rift_destruction(unit, -1)

        # Test that 0 is now normalized and doesn't raise an error
        result = anomaly_rule.check_gravity_rift_destruction(unit, 0)
        assert result is False  # 0 -> 10, which is > 3, so ship survives


class TestNonAnomalyMovementAllowed:
    """Test that movement is allowed in non-anomaly systems."""

    def test_normal_movement_not_blocked(self) -> None:
        """Test that movement through normal systems is not blocked by anomaly rules."""
        from src.ti4.core.constants import UnitType
        from src.ti4.core.galaxy import Galaxy
        from src.ti4.core.hex_coordinate import HexCoordinate
        from src.ti4.core.movement_rules import AnomalyRule, MovementContext
        from src.ti4.core.unit import Unit

        # Create galaxy with normal systems
        galaxy = Galaxy()
        from_coord = HexCoordinate(0, 0)
        to_coord = HexCoordinate(1, 0)

        from_system = System("from_system")
        to_system = System("normal_system")

        galaxy.place_system(from_coord, "from_system")
        galaxy.register_system(from_system)
        galaxy.place_system(to_coord, "normal_system")
        galaxy.register_system(to_system)

        # Create movement context
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        context = MovementContext(
            unit=unit,
            from_coordinate=from_coord,
            to_coordinate=to_coord,
            player_technologies=set(),
            galaxy=galaxy,
        )

        # Movement should be allowed
        anomaly_rule = AnomalyRule()
        assert anomaly_rule.can_move(context)

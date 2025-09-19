"""Test enemy ship blocking movement through systems (Rule 58.4b)."""

from src.ti4.core.constants import UnitType
from src.ti4.core.galaxy import Galaxy
from src.ti4.core.hex_coordinate import HexCoordinate
from src.ti4.core.movement import MovementOperation, MovementValidator
from src.ti4.core.system import System
from src.ti4.core.unit import Unit


class TestEnemyShipBlockingMovement:
    """Test Rule 58.4b: Ships cannot move through systems with enemy ships."""

    def test_cannot_move_through_system_with_enemy_ships(self) -> None:
        """Test that ships cannot move through systems containing enemy ships."""
        galaxy = Galaxy()

        # Create a linear path: A -> B -> C
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

        # Place friendly ship in system A with move value 2
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        system_a.place_unit_in_space(cruiser)

        # Place enemy ship in system B (blocking path)
        enemy_destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player2")
        system_b.place_unit_in_space(enemy_destroyer)

        # Try to move from A to C (through B with enemy ships)
        movement = MovementOperation(
            unit=cruiser,
            from_system_id="system_a",
            to_system_id="system_c",
            player_id="player1",
        )

        validator = MovementValidator(galaxy)

        # Should be blocked by enemy ships in system B
        assert validator.validate_movement(movement) is False

    def test_can_move_to_system_with_enemy_ships(self) -> None:
        """Test that ships can move to systems with enemy ships (combat will resolve)."""
        galaxy = Galaxy()

        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(1, 0)

        system_a = System("system_a")
        system_b = System("system_b")

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)

        # Place friendly ship in system A
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        system_a.place_unit_in_space(cruiser)

        # Place enemy ship in system B (destination)
        enemy_destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player2")
        system_b.place_unit_in_space(enemy_destroyer)

        # Move directly to system with enemy ships
        movement = MovementOperation(
            unit=cruiser,
            from_system_id="system_a",
            to_system_id="system_b",
            player_id="player1",
        )

        validator = MovementValidator(galaxy)

        # Should be allowed (combat will resolve)
        assert validator.validate_movement(movement) is True

    def test_can_move_through_system_with_own_ships(self) -> None:
        """Test that ships can move through systems with their own ships."""
        galaxy = Galaxy()

        # Create a linear path: A -> B -> C
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

        # Place friendly ship in system A
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        system_a.place_unit_in_space(cruiser)

        # Place own ship in system B
        own_destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player1")
        system_b.place_unit_in_space(own_destroyer)

        # Move from A to C (through B with own ships)
        movement = MovementOperation(
            unit=cruiser,
            from_system_id="system_a",
            to_system_id="system_c",
            player_id="player1",
        )

        validator = MovementValidator(galaxy)

        # Should be allowed (own ships don't block)
        assert validator.validate_movement(movement) is True

    def test_can_move_through_empty_system(self) -> None:
        """Test that ships can move through empty systems."""
        galaxy = Galaxy()

        # Create a linear path: A -> B -> C
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

        # Place friendly ship in system A
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        system_a.place_unit_in_space(cruiser)

        # System B is empty

        # Move from A to C (through empty B)
        movement = MovementOperation(
            unit=cruiser,
            from_system_id="system_a",
            to_system_id="system_c",
            player_id="player1",
        )

        validator = MovementValidator(galaxy)

        # Should be allowed (empty systems don't block)
        assert validator.validate_movement(movement) is True

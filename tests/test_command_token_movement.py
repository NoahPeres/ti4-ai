"""Tests for command token movement restrictions (Rules 58.4c, 58.4d)."""

from src.ti4.core.constants import UnitType
from src.ti4.core.galaxy import Galaxy
from src.ti4.core.hex_coordinate import HexCoordinate
from src.ti4.core.movement import MovementOperation, MovementValidator
from src.ti4.core.system import System
from src.ti4.core.unit import Unit


class TestCommandTokenMovementRestrictions:
    """Test command token movement restrictions."""

    def test_cannot_move_from_system_with_own_command_token(self) -> None:
        """Test Rule 58.4c: Cannot move from system with own command token."""
        galaxy = Galaxy()

        # Create systems
        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(1, 0)

        system_a = System("system_a")
        system_b = System("system_b")

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)

        # Place command token in system A for player1
        system_a.place_command_token("player1")

        # Create ship in system A
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        system_a.place_unit_in_space(cruiser)

        # Try to move from system with own command token
        movement = MovementOperation(
            unit=cruiser,
            from_system_id="system_a",
            to_system_id="system_b",
            player_id="player1",
        )

        validator = MovementValidator(galaxy)

        # Should be blocked by Rule 58.4c
        assert validator.validate_movement(movement) is False

    def test_can_move_through_system_with_own_command_token(self) -> None:
        """Test Rule 58.4d: Can move through systems with own command tokens."""
        galaxy = Galaxy()

        # Create systems A -> B -> C
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

        # Place command token in system B (intermediate system)
        system_b.place_command_token("player1")

        # Create ship in system A
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")  # Move value 2
        system_a.place_unit_in_space(cruiser)

        # Move from A to C (through B with own command token)
        movement = MovementOperation(
            unit=cruiser,
            from_system_id="system_a",
            to_system_id="system_c",
            player_id="player1",
        )

        validator = MovementValidator(galaxy)

        # Should be allowed by Rule 58.4d
        assert validator.validate_movement(movement) is True

    def test_cannot_move_from_system_without_command_token(self) -> None:
        """Test that movement is allowed from systems without command tokens."""
        galaxy = Galaxy()

        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(1, 0)

        system_a = System("system_a")
        system_b = System("system_b")

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)

        # No command token in system A

        # Create ship in system A
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        system_a.place_unit_in_space(cruiser)

        # Move from system without command token
        movement = MovementOperation(
            unit=cruiser,
            from_system_id="system_a",
            to_system_id="system_b",
            player_id="player1",
        )

        validator = MovementValidator(galaxy)

        # Should be allowed
        assert validator.validate_movement(movement) is True

    def test_can_move_from_system_with_other_players_command_token(self) -> None:
        """Test that movement is allowed from systems with other players' command tokens."""
        galaxy = Galaxy()

        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(1, 0)

        system_a = System("system_a")
        system_b = System("system_b")

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)

        # Place command token for player2 in system A
        system_a.place_command_token("player2")

        # Create ship for player1 in system A
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        system_a.place_unit_in_space(cruiser)

        # Player1 tries to move from system with player2's command token
        movement = MovementOperation(
            unit=cruiser,
            from_system_id="system_a",
            to_system_id="system_b",
            player_id="player1",
        )

        validator = MovementValidator(galaxy)

        # Should be allowed (only own command tokens block movement)
        assert validator.validate_movement(movement) is True


class TestEnemyShipBlocking:
    """Test enemy ship blocking movement (Rule 58.4b)."""

    def test_can_move_to_system_with_enemy_ships(self) -> None:
        """Test that movement to systems with enemy ships is allowed (combat will resolve)."""
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

        # Place enemy ship in system B
        enemy_destroyer = Unit(unit_type=UnitType.DESTROYER, owner="player2")
        system_b.place_unit_in_space(enemy_destroyer)

        # Move to system with enemy ships
        movement = MovementOperation(
            unit=cruiser,
            from_system_id="system_a",
            to_system_id="system_b",
            player_id="player1",
        )

        validator = MovementValidator(galaxy)

        # Should be allowed (combat will resolve)
        assert validator.validate_movement(movement) is True

    def test_system_has_enemy_ships_detection(self) -> None:
        """Test that system correctly detects enemy ships."""
        system = System("test_system")

        # Add friendly unit
        friendly_unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        system.place_unit_in_space(friendly_unit)

        # Should not have enemy ships for player1
        assert system.has_enemy_ships("player1") is False

        # Add enemy unit
        enemy_unit = Unit(unit_type=UnitType.DESTROYER, owner="player2")
        system.place_unit_in_space(enemy_unit)

        # Should now have enemy ships for player1
        assert system.has_enemy_ships("player1") is True

        # Should have enemy ships for player2 (player1's cruiser is enemy to player2)
        assert system.has_enemy_ships("player2") is True

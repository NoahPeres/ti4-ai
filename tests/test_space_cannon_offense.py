"""Tests for Rule 58.7: Space Cannon Offense Step.

This module tests the Space Cannon Offense step that occurs after the Move Ships step
in a tactical action, as defined in Rules 58.7 and 77.2-77.5.
"""

from unittest.mock import Mock, patch

from src.ti4.actions.tactical_action import SpaceCannonOffenseStep, TacticalAction
from src.ti4.core.galaxy import Galaxy, HexCoordinate
from src.ti4.core.planet import Planet
from src.ti4.core.system import System
from src.ti4.core.unit import Unit, UnitType


class TestRule58SpaceCannonOffenseStep:
    """Test Rule 58.7: Space Cannon Offense Step."""

    def test_space_cannon_offense_step_exists(self) -> None:
        """Test that SpaceCannonOffenseStep class exists and can be instantiated."""
        # RED: This should fail because SpaceCannonOffenseStep doesn't exist yet
        step = SpaceCannonOffenseStep()
        assert step.get_step_name() == "Space Cannon Offense"

    def test_space_cannon_offense_after_movement(self) -> None:
        """Test that Space Cannon Offense occurs after Move Ships step (Rule 58.7)."""
        galaxy = Galaxy()

        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(1, 0)

        system_a = System("system_a")
        system_b = System("system_b")

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)

        # Create tactical action
        tactical_action = TacticalAction(
            active_system_id="system_b", player_id="player1"
        )
        tactical_action.initialize_steps()

        # Get step names in order
        step_names = [step.get_step_name() for step in tactical_action.steps]

        # Space Cannon Offense should come after Movement
        movement_index = step_names.index("Movement")
        space_cannon_index = step_names.index("Space Cannon Offense")

        assert space_cannon_index == movement_index + 1

    def test_space_cannon_offense_can_execute_with_space_cannon_units(self) -> None:
        """Test that Space Cannon Offense step can execute when units with space cannon are present."""
        Galaxy()
        system = System("active_system")

        # Add a planet to the system
        planet = Planet("planet1", resources=2, influence=1)
        system.add_planet(planet)

        # Create PDS with space cannon ability
        pds = Unit(unit_type=UnitType.PDS, owner="player2")
        system.place_unit_on_planet(pds, "planet1")

        # Create enemy ships in the system
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        system.place_unit_in_space(cruiser)

        game_state = Mock()
        game_state.systems = {"active_system": system}

        context = {"active_system_id": "active_system", "player_id": "player1"}

        step = SpaceCannonOffenseStep()
        assert step.can_execute(game_state, context) is True

    def test_space_cannon_offense_cannot_execute_without_space_cannon_units(
        self,
    ) -> None:
        """Test that Space Cannon Offense step cannot execute when no space cannon units are present."""
        Galaxy()
        system = System("active_system")

        # Create units without space cannon ability
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="player2")
        system.place_unit_on_planet(infantry, "planet1")

        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        system.place_unit_in_space(cruiser)

        game_state = Mock()
        game_state.systems = {"active_system": system}

        context = {"active_system_id": "active_system", "player_id": "player1"}

        step = SpaceCannonOffenseStep()
        assert step.can_execute(game_state, context) is False


class TestRule77SpaceCannonOffenseMechanics:
    """Test Rule 77.2-77.5: Space Cannon Offense Mechanics."""

    def test_space_cannon_offense_player_order(self) -> None:
        """Test that Space Cannon Offense proceeds in player order starting with active player (Rule 77.2)."""
        Galaxy()
        system = System("active_system")

        # Add planets to the system
        from src.ti4.core.planet import Planet

        planet1 = Planet("planet1", resources=2, influence=1)
        planet2 = Planet("planet2", resources=1, influence=2)
        planet3 = Planet("planet3", resources=3, influence=0)
        system.add_planet(planet1)
        system.add_planet(planet2)
        system.add_planet(planet3)

        # Create PDS units for multiple players
        pds1 = Unit(unit_type=UnitType.PDS, owner="player1")  # Active player
        pds2 = Unit(unit_type=UnitType.PDS, owner="player2")
        pds3 = Unit(unit_type=UnitType.PDS, owner="player3")

        system.place_unit_on_planet(pds1, "planet1")
        system.place_unit_on_planet(pds2, "planet2")
        system.place_unit_on_planet(pds3, "planet3")

        # Create target ships
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player4")
        system.place_unit_in_space(cruiser)

        game_state = Mock()
        game_state.systems = {"active_system": system}
        game_state.players = ["player1", "player2", "player3", "player4"]

        context = {"active_system_id": "active_system", "player_id": "player1"}

        step = SpaceCannonOffenseStep()

        with patch.object(step, "_resolve_space_cannon_for_player") as mock_resolve:
            step.execute(game_state, context)

            # Should be called in order: active player first, then clockwise
            expected_calls = [
                (("player1", game_state, context),),
                (("player2", game_state, context),),
                (("player3", game_state, context),),
            ]

            assert mock_resolve.call_args_list == expected_calls

    def test_space_cannon_dice_rolling(self) -> None:
        """Test space cannon dice rolling mechanics (Rule 77.3)."""
        Galaxy()
        system = System("active_system")

        # Create PDS with space cannon 6 (x1)
        pds = Unit(unit_type=UnitType.PDS, owner="player1")
        system.place_unit_on_planet(pds, "planet1")

        # Create target ship
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player2")
        system.place_unit_in_space(cruiser)

        game_state = Mock()
        game_state.systems = {"active_system": system}

        context = {"active_system_id": "active_system", "player_id": "player1"}

        step = SpaceCannonOffenseStep()

        with patch("src.ti4.core.dice.roll_dice") as mock_roll:
            mock_roll.return_value = [6, 4, 3]  # One hit (6 >= 6)

            hits = step._roll_space_cannon_dice(pds, game_state, context)

            # PDS has space cannon 6 (x1), so should roll 1 die
            mock_roll.assert_called_once_with(1)
            assert hits == 1

    def test_space_cannon_hit_assignment_active_player_targets_others(self) -> None:
        """Test that active player can choose which player's ships to target (Rule 77.5b)."""
        Galaxy()
        system = System("active_system")

        # Active player has PDS
        pds = Unit(unit_type=UnitType.PDS, owner="player1")
        planet1 = Planet("planet1", resources=2, influence=1)
        system.add_planet(planet1)
        system.place_unit_on_planet(pds, "planet1")

        # Multiple players have ships in system
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player2")
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner="player3")
        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        game_state = Mock()
        game_state.systems = {"active_system": system}

        context = {"active_system_id": "active_system", "player_id": "player1"}

        step = SpaceCannonOffenseStep()

        # Active player should be able to choose target player
        target_players = step._get_valid_target_players("player1", system, context)
        assert "player2" in target_players
        assert "player3" in target_players
        assert "player1" not in target_players  # Can't target self

    def test_space_cannon_hit_assignment_non_active_targets_active(self) -> None:
        """Test that non-active players must target active player's ships (Rule 77.5a)."""
        Galaxy()
        system = System("active_system")

        # Non-active player has PDS
        pds = Unit(unit_type=UnitType.PDS, owner="player2")
        planet1 = Planet("planet1", resources=2, influence=1)
        system.add_planet(planet1)
        system.place_unit_on_planet(pds, "planet1")

        # Active player and other player have ships
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player1")  # Active
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner="player3")  # Other
        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        game_state = Mock()
        game_state.systems = {"active_system": system}

        context = {
            "active_system_id": "active_system",
            "player_id": "player1",  # Active player
        }

        step = SpaceCannonOffenseStep()

        # Non-active player must target active player only
        target_players = step._get_valid_target_players("player2", system, context)
        assert target_players == ["player1"]

    def test_space_cannon_works_without_ship_movement(self) -> None:
        """Test that Space Cannon Offense works even if no ships moved (Rule 77.4)."""
        Galaxy()
        system = System("active_system")

        # PDS already in active system
        pds = Unit(unit_type=UnitType.PDS, owner="player1")
        planet1 = Planet("planet1", resources=2, influence=1)
        system.add_planet(planet1)
        system.place_unit_on_planet(pds, "planet1")

        # Enemy ships already in active system
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player2")
        system.place_unit_in_space(cruiser)

        game_state = Mock()
        game_state.systems = {"active_system": system}

        context = {
            "active_system_id": "active_system",
            "player_id": "player1",
            "ships_moved": False,  # No ships moved this turn
        }

        step = SpaceCannonOffenseStep()

        # Should still be able to execute space cannon
        assert step.can_execute(game_state, context) is True

    def test_space_cannon_pds_ii_adjacent_systems(self) -> None:
        """Test that PDS II can fire from adjacent systems (Rule 77.3c)."""
        galaxy = Galaxy()

        coord_a = HexCoordinate(0, 0)
        coord_b = HexCoordinate(1, 0)

        system_a = System("system_a")
        system_b = System("system_b")  # Active system

        galaxy.place_system(coord_a, "system_a")
        galaxy.place_system(coord_b, "system_b")
        galaxy.register_system(system_a)
        galaxy.register_system(system_b)

        # PDS II in adjacent system
        pds_ii = Unit(unit_type=UnitType.PDS, owner="player1")
        # Mock PDS II upgrade (would normally be handled by technology system)
        pds_ii._has_pds_ii_upgrade = True
        planet1 = Planet("planet1", resources=2, influence=1)
        system_a.add_planet(planet1)
        system_a.place_unit_on_planet(pds_ii, "planet1")

        # Target ships in active system
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player2")
        system_b.place_unit_in_space(cruiser)

        game_state = Mock()
        game_state.systems = {"system_a": system_a, "system_b": system_b}
        game_state.galaxy = galaxy

        context = {"active_system_id": "system_b", "player_id": "player2"}

        step = SpaceCannonOffenseStep()

        # Should find PDS II in adjacent system
        space_cannon_units = step._get_space_cannon_units_for_player(
            "player1", game_state, context
        )
        assert pds_ii in space_cannon_units

    @patch("src.ti4.core.dice.roll_dice")
    def test_complete_space_cannon_offense_execution(self, mock_roll) -> None:
        """Test complete Space Cannon Offense step execution."""
        mock_roll.return_value = [6]  # One hit

        Galaxy()
        system = System("active_system")

        # Add planet to system
        planet = Planet("planet1", resources=2, influence=1)
        system.add_planet(planet)

        # Player 1 (active) has PDS
        pds = Unit(unit_type=UnitType.PDS, owner="player1")
        system.place_unit_on_planet(pds, "planet1")

        # Player 2 has ships to target
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player2")
        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player2")
        system.place_unit_in_space(cruiser)
        system.place_unit_in_space(fighter)

        game_state = Mock()
        game_state.systems = {"active_system": system}
        game_state.players = ["player1", "player2"]

        context = {"active_system_id": "active_system", "player_id": "player1"}

        step = SpaceCannonOffenseStep()

        with patch.object(step, "_assign_hits") as mock_assign:
            result_state = step.execute(game_state, context)

            # Should have rolled dice and assigned hits
            mock_roll.assert_called()
            mock_assign.assert_called()
            assert result_state == game_state

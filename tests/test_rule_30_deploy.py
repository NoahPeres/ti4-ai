"""Test Rule 30: DEPLOY - Deploy abilities for units.

This module tests the implementation of deploy abilities according to the LRR:
- Rule 30.1: Deploy ability usage and conditions
- Rule 30.2: Reinforcement requirement validation
- Rule 30.3: Timing window restrictions

Deploy abilities allow units to be placed on the game board without producing them normally.
"""

import pytest

from src.ti4.core.constants import UnitType
from src.ti4.core.exceptions import DeployError, ReinforcementError
from src.ti4.core.game_state import GameState
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.reinforcements import Reinforcements
from src.ti4.core.system import System
from src.ti4.core.unit import Unit


class TestRule30DeployAbilities:
    """Test Rule 30: DEPLOY - Deploy abilities for units."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.game_state = GameState()
        self.player = Player(id="player1", faction=None)
        self.system = System(system_id="test_system")
        self.planet = Planet(name="test_planet", resources=2, influence=1)
        self.system.add_planet(self.planet)

        # Add player to game state
        self.game_state.add_player(self.player)

        # Set up reinforcements with mechs available
        self.reinforcements = Reinforcements()
        pool = self.reinforcements.get_pool("player1")
        pool.set_unit_count(UnitType.MECH, 4)  # Standard mech count

    def test_rule_30_1_deploy_ability_usage_basic(self) -> None:
        """Test Rule 30.1: Basic deploy ability usage.

        A player can use a unit's deploy ability when the ability's conditions are met
        to place that unit on the game board.
        """
        # Create a mech in reinforcements
        mech = Unit(unit_type=UnitType.MECH, owner="player1")
        self.reinforcements.add_unit_instance(mech)

        # Player should be able to deploy mech to planet they control
        self.planet.set_control("player1")

        # This should work - deploy mech from reinforcements to planet
        deploy_result = self.player.deploy_unit(
            unit_type=UnitType.MECH,
            target_system=self.system,
            target_planet=self.planet.name,
            reinforcements=self.reinforcements,
        )

        assert deploy_result is True

        # Check that a mech was deployed to the planet
        planet_units = self.planet.get_units()
        assert len(planet_units) == 1
        deployed_unit = planet_units[0]
        assert deployed_unit.unit_type == UnitType.MECH
        assert deployed_unit.owner == "player1"

        # Check that reinforcements were decremented
        available_mechs = self.reinforcements.get_available_units(UnitType.MECH)
        assert len(available_mechs) == 0  # Should be empty after deployment

    def test_rule_30_1_deploy_ability_conditions_not_met(self) -> None:
        """Test Rule 30.1: Deploy ability fails when conditions not met.

        Deploy should fail if the player doesn't control the target planet.
        """
        # Create a mech in reinforcements
        mech = Unit(unit_type=UnitType.MECH, owner="player1")
        self.reinforcements.add_unit_instance(mech)

        # Planet is controlled by another player
        self.planet.set_control("player2")

        # Deploy should fail due to lack of control
        with pytest.raises(DeployError, match="Cannot deploy.*not controlled"):
            self.player.deploy_unit(
                unit_type=UnitType.MECH,
                target_system=self.system,
                target_planet=self.planet.name,
                reinforcements=self.reinforcements,
            )

    def test_rule_30_1_deploy_ability_non_deployable_unit(self) -> None:
        """Test Rule 30.1: Deploy ability only works for units with deploy ability.

        Only units with deploy ability (like mechs) can be deployed.
        """
        # Try to deploy infantry (no deploy ability)
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        self.reinforcements.add_unit_instance(infantry)
        self.planet.set_control("player1")

        # Deploy should fail for units without deploy ability
        with pytest.raises(DeployError, match="Unit.*does not have deploy ability"):
            self.player.deploy_unit(
                unit_type=UnitType.INFANTRY,
                target_system=self.system,
                target_planet=self.planet.name,
                reinforcements=self.reinforcements,
            )

    def test_rule_30_1a_resource_free_deployment(self) -> None:
        """Test Rule 30.1.a: Deploy doesn't require spending resources.

        A player does not have to spend resources to deploy a unit unless otherwise specified.
        """
        # Create a mech in reinforcements
        mech = Unit(unit_type=UnitType.MECH, owner="player1")
        self.reinforcements.add_unit_instance(mech)
        self.planet.set_control("player1")

        # Record initial planet state (deploy should not exhaust planets)
        initial_exhausted = self.planet._exhausted

        # Deploy mech
        self.player.deploy_unit(
            unit_type=UnitType.MECH,
            target_system=self.system,
            target_planet=self.planet.name,
            reinforcements=self.reinforcements,
        )

        # Planet should remain in same state (deploy is free - no resource spending)
        assert self.planet._exhausted == initial_exhausted

    def test_rule_30_2_reinforcement_requirement(self) -> None:
        """Test Rule 30.2: Deploy requires unit in reinforcements.

        A player can only resolve a deploy ability to place a unit that is in their reinforcements.
        """
        # Clear mechs from reinforcements
        pool = self.reinforcements.get_pool("player1")
        pool.set_unit_count(UnitType.MECH, 0)
        self.planet.set_control("player1")

        # Deploy should fail when no units available in reinforcements
        with pytest.raises(ReinforcementError, match="No.*available in reinforcements"):
            self.player.deploy_unit(
                unit_type=UnitType.MECH,
                target_system=self.system,
                target_planet=self.planet.name,
                reinforcements=self.reinforcements,
            )

    def test_rule_30_2a_no_deploy_units_available(self) -> None:
        """Test Rule 30.2.a: Deploy fails when no deploy units in reinforcements.

        If there are no units that have a deploy ability in a player's reinforcements,
        the deploy ability cannot be used.
        """
        # Clear all units from reinforcements first
        pool = self.reinforcements.get_pool("player1")
        pool.set_unit_count(UnitType.MECH, 0)

        # Add non-deployable units to reinforcements
        infantry = Unit(unit_type=UnitType.INFANTRY, owner="player1")
        self.reinforcements.add_unit_instance(infantry)
        self.planet.set_control("player1")

        # Deploy should fail when no deployable units available
        with pytest.raises(
            ReinforcementError,
            match="No units with deploy ability available.*reinforcements",
        ):
            self.player.deploy_unit(
                unit_type=UnitType.MECH,
                target_system=self.system,
                target_planet=self.planet.name,
                reinforcements=self.reinforcements,
            )

    def test_rule_30_3_timing_window_restriction(self) -> None:
        """Test Rule 30.3: Deploy ability once per timing window.

        A unit's deploy ability can be resolved only once per timing window.
        """
        # Create two mechs in reinforcements
        mech1 = Unit(unit_type=UnitType.MECH, owner="player1")
        mech2 = Unit(unit_type=UnitType.MECH, owner="player1")
        self.reinforcements.add_unit_instance(mech1)
        self.reinforcements.add_unit_instance(mech2)
        self.planet.set_control("player1")

        # First deploy should succeed
        deploy_result1 = self.player.deploy_unit(
            unit_type=UnitType.MECH,
            target_system=self.system,
            target_planet=self.planet.name,
            reinforcements=self.reinforcements,
        )
        assert deploy_result1 is True

        # Second deploy in same timing window should fail
        with pytest.raises(
            DeployError, match="Deploy ability already used.*timing window"
        ):
            self.player.deploy_unit(
                unit_type=UnitType.MECH,
                target_system=self.system,
                target_planet=self.planet.name,
                reinforcements=self.reinforcements,
            )

    def test_rule_30_3_timing_window_reset(self) -> None:
        """Test Rule 30.3: Deploy ability resets in new timing window.

        Deploy ability should be available again in a new timing window.
        """
        # Create two mechs in reinforcements
        mech1 = Unit(unit_type=UnitType.MECH, owner="player1")
        mech2 = Unit(unit_type=UnitType.MECH, owner="player1")
        self.reinforcements.add_unit_instance(mech1)
        self.reinforcements.add_unit_instance(mech2)
        self.planet.set_control("player1")

        # Deploy in first timing window
        self.player.deploy_unit(
            unit_type=UnitType.MECH,
            target_system=self.system,
            target_planet=self.planet.name,
            reinforcements=self.reinforcements,
        )

        # Advance to new timing window
        self.player.advance_timing_window()

        # Deploy should work again in new timing window
        deploy_result2 = self.player.deploy_unit(
            unit_type=UnitType.MECH,
            target_system=self.system,
            target_planet=self.planet.name,
            reinforcements=self.reinforcements,
        )
        assert deploy_result2 is True

    def test_deploy_ability_integration_with_game_state(self) -> None:
        """Test deploy ability integration with game state tracking."""
        # Create a mech in reinforcements
        mech = Unit(unit_type=UnitType.MECH, owner="player1")
        self.reinforcements.add_unit_instance(mech)
        self.planet.set_control("player1")

        # Deploy mech
        self.player.deploy_unit(
            unit_type=UnitType.MECH,
            target_system=self.system,
            target_planet=self.planet.name,
            reinforcements=self.reinforcements,
        )

        # Verify game state is updated correctly
        planet_units = self.planet.get_units()
        assert len(planet_units) == 1
        assert planet_units[0].unit_type == UnitType.MECH
        assert planet_units[0].owner == "player1"

        # Verify reinforcements are updated
        available_mechs = self.reinforcements.get_available_units(UnitType.MECH)
        assert mech not in available_mechs

    def test_deploy_ability_multiple_planets_same_system(self) -> None:
        """Test deploy ability works with multiple planets in same system."""
        # Add second planet to system
        planet2 = Planet(name="test_planet_2", resources=1, influence=2)
        self.system.add_planet(planet2)

        # Create two mechs in reinforcements
        mech1 = Unit(unit_type=UnitType.MECH, owner="player1")
        mech2 = Unit(unit_type=UnitType.MECH, owner="player1")
        self.reinforcements.add_unit_instance(mech1)
        self.reinforcements.add_unit_instance(mech2)

        # Player controls both planets
        self.planet.set_control("player1")
        planet2.set_control("player1")

        # Deploy to first planet
        self.player.deploy_unit(
            unit_type=UnitType.MECH,
            target_system=self.system,
            target_planet=self.planet.name,
            reinforcements=self.reinforcements,
        )

        # Advance timing window and deploy to second planet
        self.player.advance_timing_window()
        self.player.deploy_unit(
            unit_type=UnitType.MECH,
            target_system=self.system,
            target_planet=planet2.name,
            reinforcements=self.reinforcements,
        )

        # Verify both deployments worked
        assert len(self.planet.get_units()) == 1
        assert len(planet2.get_units()) == 1
        assert self.planet.get_units()[0].unit_type == UnitType.MECH
        assert planet2.get_units()[0].unit_type == UnitType.MECH

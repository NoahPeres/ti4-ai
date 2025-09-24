"""
Invasion system for Twilight Imperium 4th Edition

Implements LRR Rule 49: INVASION
"""

from typing import Any

from src.ti4.core.game_state import GameState
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.system import System
from src.ti4.core.unit import Unit


class InvasionController:
    """
    Controls the invasion step of tactical actions.

    Implements the five-step invasion process:
    1. Bombardment step (49.1)
    2. Commit ground forces step (49.2)
    3. Space cannon defense step (49.3)
    4. Ground combat step (49.4)
    5. Establish control step (49.5)
    """

    def __init__(self, game_state: GameState, system: System, active_player: Player):
        self.game_state = game_state
        self.system = system
        self.active_player = active_player
        self.invaded_planets: list[Planet] = []
        self.combat_results: dict[str, Any] = {}
        self.bombardment_results: dict[str, Any] = {}

    def execute_invasion(self) -> dict[str, Any]:
        """Execute the complete invasion sequence"""
        raise NotImplementedError("Invasion execution not implemented")

    def bombardment_step(self) -> str:
        """Execute bombardment step (49.1)"""
        from .bombardment import BombardmentSystem

        # Check if active player has bombardment units
        bombardment_units = [
            unit
            for unit in self.system.space_units
            if unit.owner == self.active_player.id and unit.has_bombardment()
        ]

        if bombardment_units:
            # Create bombardment system
            bombardment_system = BombardmentSystem()

            # For each planet being invaded, assign bombardment units
            planet_targets = {}
            for planet in self.invaded_planets:
                if planet and bombardment_system.can_bombard_planet(planet):
                    # Assign all bombardment units to this planet (simplified targeting)
                    planet_targets[planet.name] = bombardment_units

            # Execute bombardment if there are valid targets
            if planet_targets:
                bombardment_results = bombardment_system.execute_bombardment(
                    system=self.system,
                    attacking_player=self.active_player.id,
                    planet_targets=planet_targets,
                    player_faction=getattr(self.active_player, "faction", None),
                    player_technologies=getattr(self.active_player, "technologies", []),
                )

                # Store bombardment results
                self.bombardment_results = bombardment_results

        return "commit_ground_forces"

    def commit_ground_forces_step(self) -> str:
        """Execute commit ground forces step (49.2)"""
        # Check if active player has ground forces in space
        from src.ti4.core.constants import UnitType

        ground_forces_in_space = [
            unit
            for unit in self.system.space_units
            if unit.owner == self.active_player.id
            and unit.unit_type == UnitType.INFANTRY
        ]

        if not ground_forces_in_space:
            return "production"

        # For now, commit all ground forces to first available planet
        if self.system.planets:
            target_planet = self.system.planets[0]
            for unit in ground_forces_in_space[
                :
            ]:  # Copy to avoid modification during iteration
                self.system.remove_unit_from_space(unit)
                target_planet.place_unit(unit)

            # Track invaded planets
            if target_planet not in self.invaded_planets:
                self.invaded_planets.append(target_planet)

            return "space_cannon_defense"

        return "production"

    def space_cannon_defense_step(self) -> str:
        """Execute space cannon defense step (49.3)"""
        # Check each invaded planet for space cannon units
        for planet in self.invaded_planets:
            space_cannon_units = [
                unit
                for unit in planet.units
                if unit.owner != self.active_player.id
                and hasattr(unit, "has_space_cannon")
                and unit.has_space_cannon()
            ]

            if space_cannon_units:
                # Execute space cannon defense
                self._execute_space_cannon_defense(planet, space_cannon_units)

        return "ground_combat"

    def ground_combat_step(self) -> str:
        """Execute ground combat step (49.4)"""
        from src.ti4.core.combat import CombatResolver
        from src.ti4.core.ground_combat import GroundCombatController

        # Initialize combat resolver and controller
        combat_resolver = CombatResolver()
        ground_combat_controller = GroundCombatController(combat_resolver)

        # Resolve ground combat on each invaded planet
        for planet in self.invaded_planets:
            # Check if there are defending ground forces
            defending_forces = [
                unit
                for unit in planet.units
                if unit.owner != self.active_player.id
                and unit.unit_type.name in ["INFANTRY", "MECH"]
            ]

            attacking_forces = [
                unit
                for unit in planet.units
                if unit.owner == self.active_player.id
                and unit.unit_type.name in ["INFANTRY", "MECH"]
            ]

            # Only resolve combat if both sides have ground forces
            if defending_forces and attacking_forces:
                # Find the defending player ID
                defender_id = defending_forces[0].owner

                # Resolve ground combat
                combat_result = ground_combat_controller.resolve_ground_combat(
                    self.system, planet.name, self.active_player.id, defender_id
                )

                # Store combat result for later reference
                if not hasattr(self, "combat_results"):
                    self.combat_results = {}
                self.combat_results[planet.name] = combat_result

        return "establish_control"

    def establish_control_step(self) -> str:
        """Execute establish control step (49.5)"""
        # For each invaded planet, check if active player has ground forces remaining
        for planet in self.invaded_planets:
            # Check if active player has ground forces on this planet
            active_player_forces = [
                unit
                for unit in planet.units
                if unit.owner == self.active_player.id
                and unit.unit_type.name in ["INFANTRY", "MECH"]
            ]

            # If active player has ground forces, they gain control
            if active_player_forces:
                planet.controlled_by = self.active_player.id

        return "production"

    def _execute_bombardment(self) -> None:
        """Execute bombardment abilities"""
        # Placeholder for bombardment execution
        pass

    def _get_bombardment_targets(self, system: System) -> dict[str, list[Unit]]:
        """Get bombardment targets for the system"""
        targets = {}
        for planet in system.planets:
            if planet.controlled_by != self.active_player.id:
                # Get bombardment units that can target this planet
                bombardment_units = []
                for unit in system.space_units:
                    if (
                        unit.owner == self.active_player.id
                        and hasattr(unit, "bombardment")
                        and unit.bombardment > 0
                    ):
                        bombardment_units.append(unit)
                if bombardment_units:
                    targets[planet.name] = bombardment_units
        return targets

    def _execute_space_cannon_defense(
        self, planet: Planet, space_cannon_units: list[Unit]
    ) -> None:
        """Execute space cannon defense against committed ground forces"""
        # Get committed ground forces on this planet
        committed_forces = [
            unit for unit in planet.units if unit.owner == self.active_player.id
        ]

        # For each space cannon unit, roll dice
        for _space_cannon_unit in space_cannon_units:
            # Mock dice roll - in real implementation would use dice system
            from random import randint

            roll = randint(1, 10)

            if roll >= 6:  # Hit on 6+
                # Destroy a committed ground force if available
                if committed_forces:
                    target = committed_forces.pop(0)
                    planet.remove_unit(target)

    def _choose_space_cannon_order(self) -> list[Planet]:
        """Choose order for space cannon defense resolution"""
        # Placeholder - would involve player input in full implementation
        return self.invaded_planets

    def _choose_ground_combat_order(self) -> list[Planet]:
        """Choose order for ground combat resolution"""
        # Placeholder - would involve player input in full implementation
        return self.invaded_planets

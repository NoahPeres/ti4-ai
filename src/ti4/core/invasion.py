"""
Invasion system for Twilight Imperium 4th Edition

Implements LRR Rule 49: INVASION
Includes Rule 95.4: Ground force landing integration
"""

from typing import Any

from .constants import UnitType
from .game_state import GameState
from .planet import Planet
from .player import Player
from .system import System
from .unit import Unit


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
        self.transport_states: list[
            Any
        ] = []  # Will be typed properly when TransportState is imported

    def execute_invasion(self) -> dict[str, Any]:
        """Execute the complete invasion sequence"""
        results = {}

        # Step 1: Bombardment
        step1_result = self.bombardment_step()
        results["bombardment"] = step1_result

        # Step 2: Commit Ground Forces
        step2_result = self.commit_ground_forces_step()
        results["commit_ground_forces"] = step2_result

        if step2_result == "production":
            return results

        # Step 3: Space Cannon Defense
        step3_result = self.space_cannon_defense_step()
        results["space_cannon_defense"] = step3_result

        # Step 4: Ground Combat
        step4_result = self.ground_combat_step()
        results["ground_combat"] = step4_result

        # Step 5: Establish Control
        step5_result = self.establish_control_step()
        results["establish_control"] = step5_result

        return results

    def bombardment_step(self) -> str:
        """Execute bombardment step (49.1)"""
        from .bombardment import BombardmentSystem
        from .constants import UnitType

        # Get bombardment system
        bombardment_system = BombardmentSystem()

        # Find units with bombardment ability in the active system
        bombardment_units = [
            unit
            for unit in self.system.space_units
            if unit.owner == self.active_player.id and unit.has_bombardment()
        ]

        if bombardment_units:
            # Build eligible planet targets in this system (enemy ground forces, no planetary shield)
            targets = []
            for p in self.system.planets:
                if p.controlled_by == self.active_player.id:
                    continue
                if not bombardment_system.can_bombard_planet(p):
                    continue
                has_enemy_ground = any(
                    u.owner != self.active_player.id
                    and u.unit_type in {UnitType.INFANTRY, UnitType.MECH}
                    for u in p.units
                )
                if has_enemy_ground:
                    targets.append(p)
            planet_targets: dict[str, list[Unit]] = {p.name: [] for p in targets}
            for idx, unit in enumerate(bombardment_units):
                if not targets:
                    break
                planet = targets[idx % len(targets)]
                planet_targets[planet.name].append(unit)

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
        """Execute commit ground forces step (49.2)

        Enhanced to handle transported ground forces (Rule 95.4)
        """
        # Check if active player has ground forces in space
        ground_forces_in_space = [
            unit
            for unit in self.system.space_units
            if unit.owner == self.active_player.id
            and unit.unit_type in {UnitType.INFANTRY, UnitType.MECH}
        ]

        # Check for transported ground forces (Rule 95.4)
        has_transported_ground_forces = False
        for transport_state in self.transport_states:
            if self._has_ground_forces_in_transport(transport_state):
                has_transported_ground_forces = True
                break

        # If no ground forces available (in space or transported), proceed to production
        if not ground_forces_in_space and not has_transported_ground_forces:
            return "production"

        # For now, commit all ground forces to first available planet
        if self.system.planets:
            target_planet = self.system.planets[0]

            # Commit regular ground forces from space
            for unit in ground_forces_in_space[
                :
            ]:  # Copy to avoid modification during iteration
                self.system.remove_unit_from_space(unit)
                target_planet.place_unit(unit)

            # Commit transported ground forces (Rule 95.4)
            for transport_state in self.transport_states:
                if self.can_land_transported_ground_forces(
                    transport_state, target_planet.name
                ):
                    self.land_transported_ground_forces(
                        transport_state, target_planet.name
                    )

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
                if unit.owner != self.active_player.id and unit.has_space_cannon()
            ]

            if space_cannon_units:
                # Execute space cannon defense
                self._execute_space_cannon_defense(planet, space_cannon_units)

        return "ground_combat"

    def ground_combat_step(self) -> str:
        """Execute ground combat step (49.4)"""
        from .combat import CombatResolver
        from .constants import UnitType
        from .ground_combat import GroundCombatController

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
                and unit.unit_type in {UnitType.INFANTRY, UnitType.MECH}
            ]

            attacking_forces = [
                unit
                for unit in planet.units
                if unit.owner == self.active_player.id
                and unit.unit_type in {UnitType.INFANTRY, UnitType.MECH}
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
                if not self.combat_results:
                    self.combat_results = {}
                self.combat_results[planet.name] = combat_result

        return "establish_control"

    def establish_control_step(self) -> str:
        """Execute establish control step (49.5)"""
        from .constants import UnitType

        # For each invaded planet, check if active player has ground forces remaining
        for planet in self.invaded_planets:
            # Check if active player has ground forces on this planet
            active_player_forces = [
                unit
                for unit in planet.units
                if unit.owner == self.active_player.id
                and unit.unit_type in {UnitType.INFANTRY, UnitType.MECH}
            ]

            # If active player has ground forces, they gain control
            if active_player_forces:
                planet.set_control(self.active_player.id)

        return "production"

    def _execute_space_cannon_defense(
        self, planet: Planet, space_cannon_units: list[Unit]
    ) -> None:
        """Execute space cannon defense against committed ground forces"""
        # Target only committed ground forces (infantry/mechs) of the active player
        from .combat import CombatResolver
        from .constants import UnitType

        committed_forces = [
            u
            for u in planet.units
            if u.owner == self.active_player.id
            and u.unit_type in {UnitType.INFANTRY, UnitType.MECH}
        ]
        if not committed_forces:
            return

        resolver = CombatResolver()
        total_hits = 0
        for sc_unit in space_cannon_units:
            total_hits += resolver.perform_space_cannon(sc_unit, committed_forces)

        # Destroy up to total_hits committed ground forces (deterministic order)
        for _ in range(min(total_hits, len(committed_forces))):
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

    # Rule 95.4: Ground force landing integration methods

    # Constants for ground force types that can land during invasion
    _GROUND_FORCE_TYPES = {UnitType.INFANTRY, UnitType.MECH}

    def set_transport_states(self, transport_states: list[Any]) -> None:
        """Set transport states for invasion integration.

        Args:
            transport_states: List of TransportState objects with transported units

        Raises:
            ValueError: If transport_states is None

        LRR Reference: Rule 95.4 - Ground forces can land during invasion
        """
        if transport_states is None:
            raise ValueError("Transport states cannot be None")
        self.transport_states = transport_states

    def can_land_transported_ground_forces(
        self, transport_state: Any, planet_name: str
    ) -> bool:
        """Check if transported ground forces can land on a planet during invasion.

        Args:
            transport_state: TransportState with transported units
            planet_name: Name of the planet to land on

        Returns:
            True if there are ground forces that can land, False otherwise

        Raises:
            ValueError: If transport_state is None

        LRR Reference: Rule 95.4 - Ground forces can land during invasion
        """
        if transport_state is None:
            raise ValueError("Transport state cannot be None")

        if not planet_name:
            return False

        try:
            self._find_planet_by_name(planet_name)
        except ValueError:
            return False

        return self._has_ground_forces_in_transport(transport_state)

    def land_transported_ground_forces(
        self, transport_state: Any, planet_name: str
    ) -> list[Unit]:
        """Land transported ground forces on a planet during invasion.

        Args:
            transport_state: TransportState with transported units
            planet_name: Name of the planet to land on

        Returns:
            List of units that were landed on the planet

        Raises:
            ValueError: If transport_state is None, planet_name is None, or planet not found

        LRR Reference: Rule 95.4 - Ground forces can land during invasion
        """
        if transport_state is None:
            raise ValueError("Transport state cannot be None")
        if planet_name is None:
            raise ValueError("Planet name cannot be None")

        target_planet = self._find_planet_by_name(planet_name)
        return self._execute_ground_force_landing(transport_state, target_planet)

    def _has_ground_forces_in_transport(self, transport_state: Any) -> bool:
        """Check if transport state contains any ground forces.

        Args:
            transport_state: TransportState to check

        Returns:
            True if transport contains ground forces, False otherwise
        """
        for unit in transport_state.transported_units:
            if unit.unit_type in self._GROUND_FORCE_TYPES:
                return True
        return False

    def _find_planet_by_name(self, planet_name: str) -> Planet:
        """Find a planet in the system by name.

        Args:
            planet_name: Name of the planet to find

        Returns:
            The planet object

        Raises:
            ValueError: If planet is not found in system
        """
        for planet in self.system.planets:
            if planet.name == planet_name:
                return planet

        raise ValueError(
            f"Planet {planet_name} not found in system {self.system.system_id}"
        )

    def _execute_ground_force_landing(
        self, transport_state: Any, target_planet: Planet
    ) -> list[Unit]:
        """Execute the landing of ground forces from transport to planet.

        Args:
            transport_state: TransportState with transported units
            target_planet: Planet where units will land

        Returns:
            List of units that were landed on the planet
        """
        landed_units = []

        # Create a copy of transported units to avoid modification during iteration
        units_to_check = transport_state.transported_units.copy()

        for unit in units_to_check:
            if unit.unit_type in self._GROUND_FORCE_TYPES:
                # Remove from transport state
                transport_state.transported_units.remove(unit)
                # Place on planet
                target_planet.place_unit(unit)
                landed_units.append(unit)

        return landed_units

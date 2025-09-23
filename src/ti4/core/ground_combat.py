"""Ground combat resolution for Twilight Imperium 4."""

from dataclasses import dataclass
from typing import Optional

from ti4.core.combat import CombatResolver  # type: ignore
from ti4.core.system import System  # type: ignore
from ti4.core.unit import Unit  # type: ignore


@dataclass
class CombatRoundResult:
    """Result of a single round of ground combat."""

    attacker_hits: int
    defender_hits: int
    attacker_casualties: list[Unit]
    defender_casualties: list[Unit]
    combat_continues: bool


@dataclass
class GroundCombatResult:
    """Result of complete ground combat resolution."""

    winner: Optional[str]  # None if no winner (both sides eliminated)
    rounds_fought: int
    round_results: list[CombatRoundResult]


class GroundCombatController:
    """Controller for managing ground combat resolution."""

    def __init__(self, combat_resolver: CombatResolver):
        """Initialize the ground combat controller.

        Args:
            combat_resolver: The combat resolver to use for dice rolling
        """
        self.combat_resolver = combat_resolver

    def _get_ground_forces(
        self, system: System, planet_name: str, player_id: str
    ) -> list[Unit]:
        """Get all ground forces for a specific player on a planet."""
        ground_units = system.get_ground_forces_on_planet(planet_name)
        return [u for u in ground_units if u.owner == player_id]

    def _roll_dice_for_forces(self, units: list[Unit]) -> int:
        """Roll dice for all ground forces and return total hits."""
        total_hits = 0
        for unit in units:
            hits = self.combat_resolver.roll_dice_for_unit(unit)
            total_hits += hits
        return total_hits

    def _assign_hits_to_forces(
        self,
        units: list[Unit],
        hits: int,
        system: System,
        planet_name: str,
        sustain_choices: dict[str, bool] | None = None,
        hit_assignments: list[str] | None = None,
    ) -> list[Unit]:
        """Assign hits to ground forces and return destroyed units."""
        if hits <= 0 or not units:
            return []

        # First, resolve sustain damage if choices provided
        remaining_hits = (
            self.combat_resolver.resolve_sustain_damage_abilities(
                units, hits, sustain_choices
            )
            if sustain_choices is not None
            else hits
        )

        # If player provided explicit assignments, honor them
        if hit_assignments is not None and remaining_hits > 0:
            player_destroyed_units: list[Unit] = (
                self.combat_resolver.assign_hits_by_player_choice(
                    units, hit_assignments[:remaining_hits]
                )
            )
            for unit in player_destroyed_units:
                system.remove_unit_from_planet(unit, planet_name)
            return player_destroyed_units

        # Fallback: simple assignment in list order
        destroyed_units: list[Unit] = []
        for unit in units[:remaining_hits]:
            destroyed_units.append(unit)
            system.remove_unit_from_planet(unit, planet_name)
        return destroyed_units

    def _combat_should_continue(
        self, system: System, planet_name: str, attacker_id: str, defender_id: str
    ) -> bool:
        """Check if combat should continue based on remaining forces."""
        return (
            len(self._get_ground_forces(system, planet_name, attacker_id)) > 0
            and len(self._get_ground_forces(system, planet_name, defender_id)) > 0
        )

    def resolve_combat_round(
        self, system: System, planet_name: str, attacker_id: str, defender_id: str
    ) -> CombatRoundResult:
        """Resolve a single round of ground combat.

        Args:
            system: The system containing the planet
            planet_name: Name of the planet where combat occurs
            attacker_id: ID of the attacking player
            defender_id: ID of the defending player

        Returns:
            CombatRoundResult with the results of this round
        """
        # Get current forces
        attacker_forces = self._get_ground_forces(system, planet_name, attacker_id)
        defender_forces = self._get_ground_forces(system, planet_name, defender_id)

        # Roll dice for both sides
        attacker_hits = self._roll_dice_for_forces(attacker_forces)
        defender_hits = self._roll_dice_for_forces(defender_forces)

        # Assign hits and determine casualties
        defender_casualties = self._assign_hits_to_forces(
            defender_forces, attacker_hits, system, planet_name
        )
        attacker_casualties = self._assign_hits_to_forces(
            attacker_forces, defender_hits, system, planet_name
        )

        # Check if combat continues (both sides must have units remaining)
        combat_continues = self._combat_should_continue(
            system, planet_name, attacker_id, defender_id
        )

        return CombatRoundResult(
            attacker_hits=attacker_hits,
            defender_hits=defender_hits,
            attacker_casualties=attacker_casualties,
            defender_casualties=defender_casualties,
            combat_continues=combat_continues,
        )

    def resolve_ground_combat(
        self, system: System, planet_name: str, attacker_id: str, defender_id: str
    ) -> GroundCombatResult:
        """Resolve complete ground combat until one side is eliminated.

        Args:
            system: The system containing the planet
            planet_name: Name of the planet where combat occurs
            attacker_id: ID of the attacking player
            defender_id: ID of the defending player

        Returns:
            GroundCombatResult with complete combat resolution
        """
        round_results = []
        rounds_fought = 0

        # Continue combat until one side is eliminated
        while True:
            rounds_fought += 1
            round_result = self.resolve_combat_round(
                system, planet_name, attacker_id, defender_id
            )
            round_results.append(round_result)

            if not round_result.combat_continues:
                break

        # Determine winner based on remaining forces
        final_attackers = self._get_ground_forces(system, planet_name, attacker_id)
        final_defenders = self._get_ground_forces(system, planet_name, defender_id)

        winner = None
        if len(final_attackers) > 0 and len(final_defenders) == 0:
            winner = attacker_id
        elif len(final_defenders) > 0 and len(final_attackers) == 0:
            winner = defender_id
        # If both sides eliminated, winner remains None

        return GroundCombatResult(
            winner=winner, rounds_fought=rounds_fought, round_results=round_results
        )

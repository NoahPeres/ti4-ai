"""Bombardment system implementation for Rule 15.

This module implements the bombardment unit ability mechanics as defined in the LRR.
Bombardment allows ships to destroy ground forces on planets during invasion.

LRR Reference: Rule 15 - BOMBARDMENT (UNIT ABILITY)
"""

import random
from typing import TYPE_CHECKING, Dict, List, Optional

if TYPE_CHECKING:
    from .planet import Planet
    from .system import System
    from .unit import Unit


class BombardmentRoll:
    """Handles bombardment roll mechanics and hit calculation.

    LRR Reference: Rule 15.1 - Bombardment roll mechanics
    """

    def __init__(self, bombardment_value: int, dice_count: int, technologies: Optional[List[str]] = None) -> None:
        """Initialize bombardment roll.

        Args:
            bombardment_value: Minimum value needed for a hit (X in 'Bombardment X (xY)')
            dice_count: Number of dice to roll (Y in 'Bombardment X (xY)')
            technologies: List of technologies that may affect the roll
        """
        self.bombardment_value = bombardment_value
        self.dice_count = dice_count
        self.technologies = technologies or []

    def get_total_dice_count(self) -> int:
        """Get total dice count including technology bonuses.

        Returns:
            Total number of dice to roll
        """
        total_dice = self.dice_count

        # Plasma Scoring adds +1 die to bombardment rolls
        if "PLASMA_SCORING" in self.technologies:
            total_dice += 1

        return total_dice

    def calculate_hits(self, dice_results: List[int]) -> int:
        """Calculate hits from dice results.

        Args:
            dice_results: List of dice roll results

        Returns:
            Number of hits produced

        LRR Reference: Rule 15.1 - "A hit is produced for each die roll that is
        equal to or greater than the unit's 'Bombardment' value."
        """
        hits = 0
        for roll in dice_results:
            if roll >= self.bombardment_value:
                hits += 1
        return hits

    def roll_dice(self) -> List[int]:
        """Roll bombardment dice.

        Returns:
            List of dice results
        """
        total_dice = self.get_total_dice_count()
        return [random.randint(1, 10) for _ in range(total_dice)]

    def is_affected_by_combat_modifier(self, modifier) -> bool:
        """Check if bombardment is affected by combat modifiers.

        Args:
            modifier: Combat modifier to check

        Returns:
            False - bombardment rolls are separate from combat rolls

        LRR Reference: Rule 15.1c - "Game effects that reroll, modify, or
        otherwise affect combat rolls do not affect bombardment rolls."
        """
        return False


class BombardmentTargeting:
    """Handles planet targeting for bombardment.

    LRR Reference: Rule 15.1d - Multi-planet bombardment targeting
    """

    def assign_bombardment_targets(
        self,
        bombardment_units: List["Unit"],
        available_planets: List[str]
    ) -> Dict[str, List["Unit"]]:
        """Assign bombardment units to planet targets.

        Args:
            bombardment_units: Units with bombardment ability
            available_planets: List of planet names that can be targeted

        Returns:
            Dictionary mapping planet names to assigned bombardment units

        LRR Reference: Rule 15.1d - "Multiple planets in a system may be
        bombarded, but a player must declare which planet a unit is bombarding
        before making a bombardment roll."
        """
        # For now, return a simple assignment - this would be enhanced
        # with player choice mechanics in a full implementation
        targets: Dict[str, List[Unit]] = {}

        for i, unit in enumerate(bombardment_units):
            planet_index = i % len(available_planets)
            planet_name = available_planets[planet_index]

            if planet_name not in targets:
                targets[planet_name] = []
            targets[planet_name].append(unit)

        return targets


class BombardmentHitAssignment:
    """Handles assignment of bombardment hits to ground forces.

    LRR Reference: Rule 15.2 - Ground force destruction from bombardment hits
    """

    def assign_bombardment_hits(
        self,
        planet: "Planet",
        hits: int,
        defending_player: str,
        player_choice: Optional[List["Unit"]] = None
    ) -> List["Unit"]:
        """Assign bombardment hits to ground forces.

        Args:
            planet: Planet being bombarded
            hits: Number of hits to assign
            defending_player: Player controlling the planet
            player_choice: Optional list of units player chooses to destroy

        Returns:
            List of units destroyed by bombardment

        LRR Reference: Rule 15.2 - "The player who controls the planet that is
        being bombarded chooses and destroys one of their ground forces on that
        planet for each hit result the bombardment roll produced."
        """
        from .constants import GameConstants

        # Get ground forces belonging to defending player
        ground_forces = [
            unit for unit in planet.units
            if unit.owner == defending_player and
            unit.unit_type in GameConstants.GROUND_FORCE_TYPES
        ]

        # Rule 15.2a: If more hits than ground forces, excess hits have no effect
        actual_hits = min(hits, len(ground_forces))

        destroyed_units = []

        if player_choice:
            # Player has made specific choices about which units to destroy
            for i in range(actual_hits):
                if i < len(player_choice) and player_choice[i] in ground_forces:
                    destroyed_units.append(player_choice[i])
                    ground_forces.remove(player_choice[i])
        else:
            # Default assignment - take first available units
            # In a full implementation, this would prompt the player for choice
            for i in range(actual_hits):
                if ground_forces:
                    destroyed_units.append(ground_forces.pop(0))

        # Remove destroyed units from planet
        for unit in destroyed_units:
            planet.remove_unit(unit)

        return destroyed_units


class BombardmentSystem:
    """Main bombardment system coordinator.

    LRR Reference: Rule 15 - BOMBARDMENT (UNIT ABILITY)
    """

    def __init__(self) -> None:
        """Initialize bombardment system."""
        self.targeting = BombardmentTargeting()
        self.hit_assignment = BombardmentHitAssignment()

    def can_bombard_planet(self, planet: "Planet") -> bool:
        """Check if a planet can be bombarded.

        Args:
            planet: Planet to check

        Returns:
            True if planet can be bombarded, False if prevented by planetary shield

        LRR Reference: Rule 15.1f - "Planets that contain a unit with the
        'Planetary Shield' ability cannot be bombarded."
        """
        # Check for units with planetary shield ability
        for unit in planet.units:
            if unit.has_planetary_shield():
                return False

        return True

    def execute_bombardment(
        self,
        system: "System",
        attacking_player: str,
        planet_targets: Dict[str, List["Unit"]]
    ) -> Dict[str, List["Unit"]]:
        """Execute bombardment against specified planet targets.

        Args:
            system: System containing the planets
            attacking_player: Player executing bombardment
            planet_targets: Dictionary mapping planet names to bombardment units

        Returns:
            Dictionary mapping planet names to destroyed units

        Raises:
            ValueError: If targets are not properly declared
        """
        if not planet_targets:
            raise ValueError("Bombardment targets must be declared before rolling")

        results: Dict[str, List[Unit]] = {}

        for planet_name, bombardment_units in planet_targets.items():
            planet = system.get_planet_by_name(planet_name)
            if not planet:
                continue

            # Check if planet can be bombarded
            if not self.can_bombard_planet(planet):
                continue

            total_hits = 0

            # Roll for each bombardment unit
            for unit in bombardment_units:
                bombardment_value, dice_count = self._get_unit_bombardment_stats(unit)
                if bombardment_value > 0:  # Unit has bombardment ability
                    roll = BombardmentRoll(bombardment_value, dice_count)
                    dice_results = roll.roll_dice()
                    hits = roll.calculate_hits(dice_results)
                    total_hits += hits

            # Assign hits to ground forces
            if total_hits > 0:
                defending_player = planet.controlled_by or "neutral"
                destroyed_units = self.hit_assignment.assign_bombardment_hits(
                    planet, total_hits, defending_player
                )
                results[planet_name] = destroyed_units
            else:
                results[planet_name] = []

        return results

    def execute_bombardment_without_targets(self) -> None:
        """Attempt to execute bombardment without declaring targets.

        Raises:
            ValueError: Always raises as targets must be declared
        """
        raise ValueError("Bombardment targets must declare targets before execution")

    def can_bombard_own_ground_forces(self, faction: str, ability: str) -> bool:
        """Check if faction can bombard their own ground forces.

        Args:
            faction: Faction name
            ability: Ability name

        Returns:
            False for L1Z1X Harrow ability, True otherwise

        LRR Reference: Rule 15.1e - "The L1Z1X's 'Harrow' ability does not
        affect the L1Z1X player's own ground forces."
        """
        if faction == "L1Z1X" and ability.lower() == "harrow":
            return False
        return True

    def _get_unit_bombardment_stats(self, unit: "Unit") -> tuple[int, int]:
        """Get bombardment value and dice count for a unit.

        Args:
            unit: The unit to get bombardment stats for

        Returns:
            Tuple of (bombardment_value, dice_count)
        """
        if not unit.has_bombardment():
            return (0, 0)

        return (unit.get_bombardment_value(), unit.get_bombardment_dice_count())

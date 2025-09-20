"""Combat system for TI4."""

import random
from typing import Callable, Optional

from .constants import UnitType
from .system import System
from .unit import Unit
from .unit_stats import UnitStatsProvider


class CombatDetector:
    """Detects when combat should be initiated."""

    def __init__(self) -> None:
        """Initialize the combat detector."""
        pass

    def should_initiate_combat(self, system: System) -> bool:
        """Check if combat should be initiated in a system."""
        # Get all owners of units in the system
        owners = set()
        for unit in system.space_units:
            owners.add(unit.owner)

        # Combat occurs if there are units from different owners
        return len(owners) > 1


class CombatInitiator:
    """Initiates and manages combat encounters."""

    def __init__(self) -> None:
        """Initialize the combat initiator."""
        pass

    def get_combat_participants(self, system: System) -> dict[str, list[Unit]]:
        """Get combat participants grouped by owner."""
        participants: dict[str, list[Unit]] = {}

        for unit in system.space_units:
            owner = unit.owner
            if owner not in participants:
                participants[owner] = []
            participants[owner].append(unit)

        return participants


class CombatResolver:
    """Resolves combat encounters with dice rolling and hit calculation."""

    def __init__(self) -> None:
        """Initialize the combat resolver."""
        self.unit_stats_provider = UnitStatsProvider()

    def roll_dice_for_unit(self, unit: Unit, dice_count: Optional[int] = None) -> int:
        """Roll dice for a unit and return number of hits.

        Args:
            unit: The unit rolling dice
            dice_count: Optional override for number of dice (uses unit's combat_dice if None)
        """
        stats = unit.get_stats()
        if stats.combat_value is None:
            return 0

        # Use unit's combat dice if not overridden
        actual_dice_count = dice_count if dice_count is not None else stats.combat_dice

        if actual_dice_count < 0:
            raise ValueError("dice_count must be non-negative")

        if actual_dice_count == 0:
            return 0

        # Roll dice and calculate hits
        dice_results = [random.randint(1, 10) for _ in range(actual_dice_count)]
        return self.calculate_hits(dice_results, stats.combat_value)

    def roll_dice_for_unit_with_burst_icons(self, unit: Unit) -> int:
        """Roll dice for a unit using burst icon mechanics.

        Each burst icon on the unit's combat value represents one die to roll.
        The combat_dice stat contains the total number of dice including burst icons.

        Args:
            unit: The unit rolling dice

        Returns:
            Number of hits scored
        """
        # Delegate to main roll_dice_for_unit method
        return self.roll_dice_for_unit(unit)

    def calculate_hits_with_burst_icons(self, unit: Unit) -> int:
        """Calculate hits for a unit using burst icon mechanics.

        This is an alias for roll_dice_for_unit_with_burst_icons for clarity.
        """
        return self.roll_dice_for_unit_with_burst_icons(unit)

    def calculate_hits(self, dice_results: list[int], combat_value: int) -> int:
        """Calculate hits from dice results given a combat value."""
        if combat_value < 1 or combat_value > 10:
            raise ValueError("combat_value must be between 1 and 10")

        hits = 0
        for roll in dice_results:
            if roll >= combat_value:
                hits += 1
        return hits

    def resolve_sustain_damage_abilities(
        self, units: list[Unit], hits: int, sustain_choices: dict[str, bool]
    ) -> int:
        """Resolve sustain damage abilities before hit assignment.

        Args:
            units: List of units that can potentially sustain damage
            hits: Number of hits to potentially cancel
            sustain_choices: Dict mapping unit_id to whether player chooses to sustain

        Returns:
            Number of hits remaining after sustain damage resolution
        """
        remaining_hits = hits

        for unit in units:
            if remaining_hits <= 0:
                break

            unit_id = unit.id
            if (
                unit.has_sustain_damage()
                and not unit.has_sustained_damage
                and sustain_choices.get(unit_id, False)
            ):
                # Player chooses to use sustain damage ability
                unit.sustain_damage()
                remaining_hits -= 1

        return remaining_hits

    def assign_hits_by_player_choice(
        self, units: list[Unit], hit_assignments: list[str]
    ) -> list[Unit]:
        """Assign hits to units based on player choice.

        Args:
            units: List of available units
            hit_assignments: List of unit IDs chosen by player to take hits

        Returns:
            List of destroyed units
        """
        destroyed_units = []
        unit_dict = {unit.id: unit for unit in units}

        for unit_id in hit_assignments:
            if unit_id in unit_dict:
                unit = unit_dict[unit_id]
                # Unit is destroyed (assuming no other abilities prevent this)
                destroyed_units.append(unit)

        return destroyed_units

    def validate_hit_assignment_choices(
        self, units: list[Unit], hit_assignments: list[str], expected_hits: int
    ) -> bool:
        """Validate that player's hit assignment choices are legal.

        Args:
            units: List of available units
            hit_assignments: List of unit IDs chosen by player
            expected_hits: Number of hits that should be assigned

        Returns:
            True if assignment is valid, False otherwise
        """
        # Check if number of assignments matches expected hits
        if len(hit_assignments) != expected_hits:
            return False

        # Check if all assigned unit IDs are valid
        unit_ids = {unit.id for unit in units}
        for unit_id in hit_assignments:
            if unit_id not in unit_ids:
                return False

        return True

    def calculate_hits_with_modifiers(
        self, dice_results: list[int], combat_value: int, modifier: int = 0
    ) -> int:
        """Calculate hits from dice results with combat modifiers.

        Args:
            dice_results: List of dice roll results
            combat_value: Base combat value needed to hit
            modifier: Modifier to apply to hit calculation (+1 makes it easier to hit)

        Returns:
            Number of hits scored
        """
        # Apply modifier by adjusting the effective combat value
        effective_combat_value = max(1, min(10, combat_value - modifier))
        return self.calculate_hits(dice_results, effective_combat_value)

    def _perform_ability_attack(
        self,
        unit: Unit,
        target_units: list[Unit],
        ability_check_func: Callable[[Unit], bool],
        target_filter_func: Optional[Callable[[list[Unit]], list[Unit]]] = None,
    ) -> int:
        """Generic method for performing ability-based attacks.

        Args:
            unit: The unit performing the ability
            target_units: List of potential target units
            ability_check_func: Function to check if unit has the ability
            target_filter_func: Optional function to filter valid targets

        Returns:
            Number of hits scored
        """
        if not ability_check_func(unit):
            return 0

        # Filter targets if filter function provided
        valid_targets = target_units
        if target_filter_func:
            valid_targets = target_filter_func(target_units)

        if not valid_targets:
            return 0

        # Get unit stats and validate combat capability
        stats = unit.get_stats()
        if stats.combat_value is None:
            return 0

        # Roll dice and calculate hits
        dice_count = stats.combat_dice
        if dice_count <= 0:
            return 0

        dice_results = [random.randint(1, 10) for _ in range(dice_count)]
        return self.calculate_hits(dice_results, stats.combat_value)

    def perform_anti_fighter_barrage(self, unit: Unit, target_units: list[Unit]) -> int:
        """Perform anti-fighter barrage against fighters.

        Args:
            unit: The unit performing anti-fighter barrage
            target_units: List of potential target units

        Returns:
            Number of hits scored against fighters
        """

        def filter_fighters(units: list[Unit]) -> list[Unit]:
            return [u for u in units if u.unit_type == UnitType.FIGHTER]

        return self._perform_ability_attack(
            unit, target_units, Unit.has_anti_fighter_barrage, filter_fighters
        )

    def perform_space_cannon(self, unit: Unit, target_units: list[Unit]) -> int:
        """Perform space cannon defensive fire.

        Args:
            unit: The unit performing space cannon
            target_units: List of potential target units

        Returns:
            Number of hits scored
        """
        return self._perform_ability_attack(unit, target_units, Unit.has_space_cannon)

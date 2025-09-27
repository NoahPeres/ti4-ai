"""Dice rolling functionality for TI4 game mechanics."""

import random
from typing import Any


class DiceRoll:
    """Represents a collection of dice roll results that can be rerolled.

    LRR Reference: Rule 74 - REROLLS
    """

    def __init__(self, results: list[int]) -> None:
        """Initialize with dice roll results.

        Args:
            results: List of initial dice roll results
        """
        self._results = results.copy()
        self._reroll_history: dict[
            int, set[str]
        ] = {}  # die_index -> set of ability names

    def get_result(self, die_index: int) -> int:
        """Get the current result for a specific die.

        Args:
            die_index: Index of the die to get result for

        Returns:
            Current result of the die
        """
        return self._results[die_index]

    def set_result(self, die_index: int, new_result: int) -> None:
        """Set a new result for a specific die (used by reroll system).

        Args:
            die_index: Index of the die to set result for
            new_result: New result value
        """
        self._results[die_index] = new_result

    def mark_rerolled_by_ability(self, die_index: int, ability_name: str) -> None:
        """Mark that a die was rerolled by a specific ability.

        Args:
            die_index: Index of the die that was rerolled
            ability_name: Name of the ability that performed the reroll
        """
        if die_index not in self._reroll_history:
            self._reroll_history[die_index] = set()
        self._reroll_history[die_index].add(ability_name)

    def was_rerolled_by_ability(self, die_index: int, ability_name: str) -> bool:
        """Check if a die was already rerolled by a specific ability.

        Args:
            die_index: Index of the die to check
            ability_name: Name of the ability to check

        Returns:
            True if the die was already rerolled by this ability
        """
        return (
            die_index in self._reroll_history
            and ability_name in self._reroll_history[die_index]
        )


class RerollTimingEnforcer:
    """Enforces timing rules for rerolls according to Rule 74.3."""

    def __init__(self) -> None:
        self._in_reroll_phase = True

    def is_reroll_phase(self) -> bool:
        """Check if currently in the reroll phase."""
        return self._in_reroll_phase

    def can_use_post_roll_abilities(self) -> bool:
        """Check if post-roll abilities can be used."""
        return not self._in_reroll_phase

    def complete_reroll_phase(self) -> None:
        """Mark the reroll phase as complete."""
        self._in_reroll_phase = False


class RerollSystem:
    """Manages dice rerolls according to Rule 74.

    LRR Reference: Rule 74 - REROLLS
    74.1 When a die is rerolled, its new result is used instead of its previous result.
    74.2 The same ability cannot be used to reroll the same die multiple times,
         but multiple abilities can be used to reroll a single die.
    74.3 Die rerolls must occur after rolling the dice, before other abilities are resolved.
    """

    def __init__(self) -> None:
        self._timing_enforcer = RerollTimingEnforcer()

    def reroll_die(self, dice_roll: DiceRoll, die_index: int) -> None:
        """Reroll a single die, replacing its result.

        Args:
            dice_roll: The dice roll to modify
            die_index: Index of the die to reroll

        LRR Reference: Rule 74.1 - New result is used instead of previous result
        """
        if not self._timing_enforcer.is_reroll_phase():
            raise RuntimeError("Rerolls must occur during the reroll phase")
        new_result = random.randint(1, 10)  # nosec B311 - game RNG, not crypto
        dice_roll.set_result(die_index, new_result)

    def reroll_die_with_ability(
        self, dice_roll: DiceRoll, die_index: int, ability: Any
    ) -> bool:
        """Reroll a die using a specific ability, enforcing reroll restrictions.

        Args:
            dice_roll: The dice roll to modify
            die_index: Index of the die to reroll
            ability: The ability performing the reroll

        Returns:
            True if reroll was successful, False if blocked by restrictions

        LRR Reference: Rule 74.2 - Same ability cannot reroll same die multiple times
        """
        if not self._timing_enforcer.is_reroll_phase():
            return False
        ability_name = getattr(ability, "name", str(ability))

        # Check if this ability already rerolled this die
        if dice_roll.was_rerolled_by_ability(die_index, ability_name):
            return False

        # Perform the reroll
        new_result = random.randint(1, 10)  # nosec B311 - game RNG, not crypto
        dice_roll.set_result(die_index, new_result)
        dice_roll.mark_rerolled_by_ability(die_index, ability_name)

        return True

    def get_timing_enforcer(self) -> RerollTimingEnforcer:
        """Get the timing enforcer for this reroll system.

        Returns:
            The timing enforcer instance

        LRR Reference: Rule 74.3 - Rerolls occur before other abilities
        """
        return self._timing_enforcer


def roll_dice(count: int) -> list[int]:
    """Roll a specified number of 10-sided dice.

    Args:
        count: Number of dice to roll

    Returns:
        List of dice results (1-10)
    """
    if count < 0:
        raise ValueError("Dice count must be non-negative")

    if count == 0:
        return []

    return [random.randint(1, 10) for _ in range(count)]  # nosec B311 - game RNG, not crypto


def calculate_hits(dice_results: list[int], target_value: int) -> int:
    """Calculate hits from dice results.

    Args:
        dice_results: List of dice roll results
        target_value: Minimum value needed to score a hit

    Returns:
        Number of hits scored
    """
    if target_value < 1 or target_value > 10:
        raise ValueError("Target value must be between 1 and 10")

    return sum(1 for roll in dice_results if roll >= target_value)

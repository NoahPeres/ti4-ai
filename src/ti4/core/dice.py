"""Dice rolling functionality for TI4 game mechanics."""

import random


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

    return [random.randint(1, 10) for _ in range(count)]


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

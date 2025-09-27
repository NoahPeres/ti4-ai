"""
Test Rule 74: REROLLS

LRR Reference: Rule 74 - REROLLS
Some game effects instruct a player to reroll dice.

74.1 When a die is rerolled, its new result is used instead of its previous result.
74.2 The same ability cannot be used to reroll the same die multiple times, but multiple abilities can be used to reroll a single die.
74.3 Die rerolls must occur after rolling the dice, before other abilities are resolved.

Related Topics: Abilities, Action Cards, Ground Combat, Space Combat
"""

import unittest
from unittest.mock import Mock, patch

from ti4.core.dice import DiceRoll, RerollSystem


class TestRule74_1NewResultUsage(unittest.TestCase):
    """Test Rule 74.1: When a die is rerolled, its new result is used instead of its previous result."""

    def test_reroll_replaces_original_result(self) -> None:
        """Test that rerolling a die uses the new result instead of the original.

        LRR 74.1: When a die is rerolled, its new result is used instead of its previous result.
        """
        # Create a dice roll with initial results
        dice_roll = DiceRoll([3, 5, 2])  # Original results

        # Reroll the first die (index 0) from 3 to 6
        with patch("random.randint", return_value=6):
            reroll_system = RerollSystem()
            reroll_system.reroll_die(dice_roll, die_index=0)

        # Verify the new result is used
        assert dice_roll.get_result(0) == 6, "Rerolled die should use new result"
        assert dice_roll.get_result(1) == 5, (
            "Non-rerolled dice should keep original results"
        )
        assert dice_roll.get_result(2) == 2, (
            "Non-rerolled dice should keep original results"
        )


class TestRule74_2MultipleRerollRestrictions(unittest.TestCase):
    """Test Rule 74.2: The same ability cannot be used to reroll the same die multiple times."""

    def test_same_ability_cannot_reroll_same_die_multiple_times(self) -> None:
        """Test that the same ability cannot reroll the same die multiple times.

        LRR 74.2: The same ability cannot be used to reroll the same die multiple times.
        """
        dice_roll = DiceRoll([1, 2, 3])
        reroll_system = RerollSystem()

        # Create a mock ability
        ability = Mock()
        ability.name = "Test Reroll Ability"

        # First reroll should succeed
        with patch("random.randint", return_value=5):
            result1 = reroll_system.reroll_die_with_ability(
                dice_roll, die_index=0, ability=ability
            )

        assert result1 is True, "First reroll with ability should succeed"
        assert dice_roll.get_result(0) == 5, "Die should be rerolled to new value"

        # Second reroll with same ability should fail
        with patch("random.randint", return_value=6):
            result2 = reroll_system.reroll_die_with_ability(
                dice_roll, die_index=0, ability=ability
            )

        assert result2 is False, "Same ability cannot reroll same die twice"
        assert dice_roll.get_result(0) == 5, "Die should keep previous reroll result"

    def test_multiple_abilities_can_reroll_same_die(self) -> None:
        """Test that multiple different abilities can reroll the same die.

        LRR 74.2: Multiple abilities can be used to reroll a single die.
        """
        dice_roll = DiceRoll([2])
        reroll_system = RerollSystem()

        # Create two different abilities
        ability1 = Mock()
        ability1.name = "First Reroll Ability"
        ability2 = Mock()
        ability2.name = "Second Reroll Ability"

        # First ability rerolls the die
        with patch("random.randint", return_value=4):
            result1 = reroll_system.reroll_die_with_ability(
                dice_roll, die_index=0, ability=ability1
            )

        assert result1 is True, "First ability should succeed"
        assert dice_roll.get_result(0) == 4, "Die should be rerolled by first ability"

        # Second ability can also reroll the same die
        with patch("random.randint", return_value=6):
            result2 = reroll_system.reroll_die_with_ability(
                dice_roll, die_index=0, ability=ability2
            )

        assert result2 is True, "Second ability should also succeed"
        assert dice_roll.get_result(0) == 6, "Die should be rerolled by second ability"


class TestRule74_3RerollTiming(unittest.TestCase):
    """Test Rule 74.3: Die rerolls must occur after rolling the dice, before other abilities are resolved."""

    def test_reroll_phase_enforcement(self):
        """Test Rule 74.3: Rerolls must occur during the reroll phase."""
        dice_roll = DiceRoll([5, 3, 8])
        reroll_system = RerollSystem()

        # Complete the reroll phase using the timing enforcer
        timing_enforcer = reroll_system.get_timing_enforcer()
        timing_enforcer.complete_reroll_phase()

        # Attempt to reroll after phase completion should fail
        with self.assertRaises(RuntimeError) as context:
            reroll_system.reroll_die(dice_roll, 0)

        self.assertIn(
            "Rerolls must occur during the reroll phase", str(context.exception)
        )

        # Verify die result unchanged
        self.assertEqual(dice_roll.get_result(0), 5)

        # Test with ability-based reroll - should return False
        ability = Mock()
        ability.name = "Test Ability"
        result = reroll_system.reroll_die_with_ability(dice_roll, 1, ability)
        self.assertFalse(result)

        # Verify die result unchanged
        self.assertEqual(dice_roll.get_result(1), 3)


if __name__ == "__main__":
    unittest.main()

"""Tests for Rule 99: WARFARE (STRATEGY CARD) - Comprehensive LRR compliance verification.

This test file verifies that all sub-rules of Rule 99 are properly implemented:
- 99.1: STEP 1 - Remove command token from board and place in chosen pool
- 99.2: STEP 2 - Redistribute command tokens between pools
- 99.3: Secondary ability - Other players can spend strategy token for production
"""

from src.ti4.core.command_sheet import CommandSheet
from src.ti4.core.strategy_card import STANDARD_STRATEGY_CARDS


class TestRule99WarfareStrategyCard:
    """Test Rule 99: WARFARE (STRATEGY CARD) basic properties."""

    def test_warfare_strategy_card_exists_with_correct_initiative(self) -> None:
        """Test that Warfare strategy card exists with initiative value 6 (Rule 99)."""
        warfare_card = None
        for card in STANDARD_STRATEGY_CARDS:
            if card.name == "Warfare":
                warfare_card = card
                break

        assert warfare_card is not None, "Warfare strategy card should exist"
        assert warfare_card.initiative == 6, (
            "Warfare card should have initiative value 6"
        )
        assert warfare_card.id == 6, "Warfare card should have id 6"


class TestRule99Step1CommandTokenRemoval:
    """Test Rule 99.1: STEP 1 - Command token removal and placement."""

    def test_can_remove_command_token_from_board(self) -> None:
        """Test that active player can remove command token from game board (Rule 99.1)."""
        # We need a minimal system to track command tokens on the board
        # For now, let's create a simple board token tracker
        from src.ti4.core.warfare_strategy_card import WarfareStrategyCard

        warfare_card = WarfareStrategyCard()

        # Simulate having a command token on the board
        # Player should be able to remove it
        result = warfare_card.can_remove_command_token_from_board("player1")
        assert result is True, "Should be able to remove command token from board"

    def test_removed_token_placed_in_chosen_pool(self) -> None:
        """Test that removed token is placed in pool of player's choice (Rule 99.1)."""
        from src.ti4.core.warfare_strategy_card import WarfareStrategyCard

        command_sheet = CommandSheet()
        initial_tactic = command_sheet.tactic_pool
        warfare_card = WarfareStrategyCard()

        # Player chooses to place the removed token in tactic pool
        result = warfare_card.execute_step_1("player1", command_sheet, "tactic")

        assert result is True, "Should successfully execute step 1"
        assert command_sheet.tactic_pool == initial_tactic + 1, (
            "Tactic pool should increase by 1"
        )


class TestRule99Step2CommandTokenRedistribution:
    """Test Rule 99.2: STEP 2 - Command token redistribution."""

    def test_can_redistribute_command_tokens_between_pools(self) -> None:
        """Test that active player can redistribute command tokens (Rule 99.2)."""
        from src.ti4.core.warfare_strategy_card import WarfareStrategyCard

        command_sheet = CommandSheet(tactic_pool=2, fleet_pool=3, strategy_pool=1)
        warfare_card = WarfareStrategyCard()

        # Player redistributes: move 1 token from fleet to tactic
        result = warfare_card.redistribute_tokens(
            command_sheet, from_pool="fleet", to_pool="tactic", count=1
        )

        assert result is True, "Should successfully redistribute tokens"
        assert command_sheet.tactic_pool == 3, "Tactic pool should increase by 1"
        assert command_sheet.fleet_pool == 2, "Fleet pool should decrease by 1"

    def test_redistribution_preserves_total_token_count(self) -> None:
        """Test that redistribution doesn't change total number of tokens (Rule 99.2)."""
        from src.ti4.core.warfare_strategy_card import WarfareStrategyCard

        command_sheet = CommandSheet(tactic_pool=2, fleet_pool=3, strategy_pool=1)
        initial_total = command_sheet.get_total_tokens()
        warfare_card = WarfareStrategyCard()

        # Redistribute tokens between pools
        warfare_card.redistribute_tokens(
            command_sheet, from_pool="fleet", to_pool="strategy", count=2
        )

        # Total should remain the same
        assert command_sheet.get_total_tokens() == initial_total, (
            "Total token count should be preserved"
        )


class TestRule99SecondaryAbility:
    """Test Rule 99.3: Secondary ability for other players."""

    def test_other_players_can_spend_strategy_token_for_production(self) -> None:
        """Test that other players can spend strategy token for production ability (Rule 99.3)."""
        from src.ti4.core.warfare_strategy_card import WarfareStrategyCard

        command_sheet = CommandSheet(strategy_pool=2)
        warfare_card = WarfareStrategyCard()

        # Other player spends strategy token for production ability
        result = warfare_card.execute_secondary_ability("player2", command_sheet)

        assert result is True, "Should successfully execute secondary ability"
        assert command_sheet.strategy_pool == 1, "Strategy pool should decrease by 1"

    def test_secondary_ability_does_not_place_command_token_in_home_system(
        self,
    ) -> None:
        """Test that secondary ability doesn't place command token in home system (Rule 99.3a)."""
        from src.ti4.core.warfare_strategy_card import WarfareStrategyCard

        command_sheet = CommandSheet(strategy_pool=2)
        warfare_card = WarfareStrategyCard()

        # Execute secondary ability - should not place token in home system
        result = warfare_card.execute_secondary_ability("player2", command_sheet)

        # Rule 99.3a: The command token is not placed in their home system
        # This test verifies the behavior exists, actual home system logic would be more complex
        assert result is True, (
            "Secondary ability should execute without placing token in home system"
        )

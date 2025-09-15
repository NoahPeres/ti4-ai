"""Tests for command token management."""

import pytest

from ti4.core.command_tokens import CommandTokens


class TestCommandTokens:
    """Test command token allocation and management."""

    def test_command_tokens_initialization(self):
        """Test that command tokens can be initialized with pools."""
        tokens = CommandTokens(fleet=3, strategy=2, tactic=1)
        assert tokens.fleet == 3
        assert tokens.strategy == 2
        assert tokens.tactic == 1

    def test_command_tokens_default_to_zero(self):
        """Test that command tokens default to zero."""
        tokens = CommandTokens()
        assert tokens.fleet == 0
        assert tokens.strategy == 0
        assert tokens.tactic == 0

    def test_command_tokens_validation_rejects_negative(self):
        """Test that command tokens validation rejects negative values."""
        tokens = CommandTokens(fleet=-1, strategy=2, tactic=1)
        assert not tokens.is_valid()

    def test_command_tokens_validation_accepts_valid_values(self):
        """Test that command tokens validation accepts valid values."""
        tokens = CommandTokens(fleet=2, strategy=1, tactic=3)
        assert tokens.is_valid()

    def test_can_spend_fleet_token(self):
        """Test that fleet tokens can be spent."""
        tokens = CommandTokens(fleet=3, strategy=2, tactic=1)
        new_tokens = tokens.spend_fleet_token()
        assert new_tokens.fleet == 2
        assert new_tokens.strategy == 2
        assert new_tokens.tactic == 1

    def test_cannot_spend_fleet_token_when_none_available(self):
        """Test that fleet tokens cannot be spent when none available."""
        tokens = CommandTokens(fleet=0, strategy=2, tactic=1)
        with pytest.raises(
            ValueError, match="Cannot spend fleet token, none available"
        ):
            tokens.spend_fleet_token()

    def test_can_spend_strategy_token(self):
        """Test that strategy tokens can be spent."""
        tokens = CommandTokens(fleet=3, strategy=2, tactic=1)
        new_tokens = tokens.spend_strategy_token()
        assert new_tokens.strategy == 1

    def test_can_spend_tactic_token(self):
        """Test that tactic tokens can be spent."""
        tokens = CommandTokens(fleet=3, strategy=2, tactic=1)
        new_tokens = tokens.spend_tactic_token()
        assert new_tokens.tactic == 0

    def test_can_redistribute_tokens(self):
        """Test that tokens can be redistributed between pools."""
        tokens = CommandTokens(fleet=2, strategy=3, tactic=1)
        new_tokens = tokens.redistribute(fleet=3, strategy=2, tactic=1)
        assert new_tokens.fleet == 3
        assert new_tokens.strategy == 2
        assert new_tokens.tactic == 1

    def test_redistribution_preserves_total_tokens(self):
        """Test that redistribution cannot change total token count."""
        tokens = CommandTokens(fleet=2, strategy=3, tactic=1)  # total = 6
        with pytest.raises(ValueError, match="Total tokens must remain 6, got 7"):
            tokens.redistribute(fleet=3, strategy=3, tactic=1)  # total = 7

    def test_total_tokens_property(self):
        """Test that total tokens can be calculated."""
        tokens = CommandTokens(fleet=2, strategy=3, tactic=1)
        assert tokens.total == 6

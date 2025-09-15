"""Tests for player resource management."""

import pytest

from ti4.core.player import Player


class TestPlayerResources:
    """Test player resource tracking functionality."""

    def test_player_has_trade_goods_field(self):
        """Test that player has trade goods field."""
        player = Player(id="player1", faction="sol", trade_goods=3)
        assert player.trade_goods == 3

    def test_player_has_commodities_field(self):
        """Test that player has commodities field."""
        player = Player(id="player1", faction="sol", commodities=2)
        assert player.commodities == 2

    def test_player_resources_default_to_zero(self):
        """Test that resources default to zero when not specified."""
        player = Player(id="player1", faction="sol")
        assert player.trade_goods == 0
        assert player.commodities == 0

    def test_player_rejects_negative_trade_goods(self):
        """Test that player validation rejects negative trade goods."""
        player = Player(id="player1", faction="sol", trade_goods=-1)
        assert not player.is_valid()

    def test_player_rejects_negative_commodities(self):
        """Test that player validation rejects negative commodities."""
        player = Player(id="player1", faction="sol", commodities=-1)
        assert not player.is_valid()

    def test_player_accepts_valid_resources(self):
        """Test that player validation accepts valid resource values."""
        player = Player(id="player1", faction="sol", trade_goods=5, commodities=3)
        assert player.is_valid()

    def test_player_can_spend_trade_goods(self):
        """Test that player can spend trade goods."""
        player = Player(id="player1", faction="sol", trade_goods=5)
        new_player = player.spend_trade_goods(3)
        assert new_player.trade_goods == 2
        assert new_player.id == player.id
        assert new_player.faction == player.faction

    def test_player_can_gain_trade_goods(self):
        """Test that player can gain trade goods."""
        player = Player(id="player1", faction="sol", trade_goods=2)
        new_player = player.gain_trade_goods(3)
        assert new_player.trade_goods == 5

    def test_player_cannot_spend_more_trade_goods_than_available(self):
        """Test that player cannot spend more trade goods than they have."""
        player = Player(id="player1", faction="sol", trade_goods=2)
        with pytest.raises(ValueError, match="Cannot spend 5 trade goods, only have 2"):
            player.spend_trade_goods(5)

    def test_player_can_spend_commodities(self):
        """Test that player can spend commodities."""
        player = Player(id="player1", faction="sol", commodities=4)
        new_player = player.spend_commodities(2)
        assert new_player.commodities == 2

    def test_player_can_gain_commodities(self):
        """Test that player can gain commodities."""
        player = Player(id="player1", faction="sol", commodities=1)
        new_player = player.gain_commodities(2)
        assert new_player.commodities == 3

    def test_player_cannot_spend_more_commodities_than_available(self):
        """Test that player cannot spend more commodities than they have."""
        player = Player(id="player1", faction="sol", commodities=1)
        with pytest.raises(ValueError, match="Cannot spend 3 commodities, only have 1"):
            player.spend_commodities(3)

    def test_player_has_command_tokens(self):
        """Test that player has command tokens field."""
        from ti4.core.command_tokens import CommandTokens

        tokens = CommandTokens(fleet=2, strategy=1, tactic=3)
        player = Player(id="player1", faction="sol", command_tokens=tokens)
        assert player.command_tokens.fleet == 2
        assert player.command_tokens.strategy == 1
        assert player.command_tokens.tactic == 3

    def test_player_command_tokens_default_to_empty(self):
        """Test that command tokens default to empty when not specified."""
        player = Player(id="player1", faction="sol")
        assert player.command_tokens.fleet == 0
        assert player.command_tokens.strategy == 0
        assert player.command_tokens.tactic == 0

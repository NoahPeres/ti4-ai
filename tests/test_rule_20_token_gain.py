"""Test Rule 20.2: Token gain mechanics with pool choice."""

import pytest

from src.ti4.core.constants import Faction
from src.ti4.core.player import Player


class TestRule20TokenGain:
    """Test Rule 20.2: When a player gains a command token, they choose which of their three pools to place it in."""

    def test_can_gain_token_in_tactic_pool(self):
        """Test that player can choose to gain token in tactic pool."""
        player = Player(id="player1", faction=Faction.ARBOREC)
        initial_tactic = player.command_sheet.tactic_pool
        initial_reinforcements = player.reinforcements

        success = player.gain_command_token("tactic")

        assert success
        assert player.command_sheet.tactic_pool == initial_tactic + 1
        assert player.reinforcements == initial_reinforcements - 1
        # Other pools should remain unchanged
        assert player.command_sheet.fleet_pool == 3
        assert player.command_sheet.strategy_pool == 2

    def test_can_gain_token_in_fleet_pool(self):
        """Test that player can choose to gain token in fleet pool."""
        player = Player(id="player1", faction=Faction.ARBOREC)
        initial_fleet = player.command_sheet.fleet_pool
        initial_reinforcements = player.reinforcements

        success = player.gain_command_token("fleet")

        assert success
        assert player.command_sheet.fleet_pool == initial_fleet + 1
        assert player.reinforcements == initial_reinforcements - 1
        # Other pools should remain unchanged
        assert player.command_sheet.tactic_pool == 3
        assert player.command_sheet.strategy_pool == 2

    def test_can_gain_token_in_strategy_pool(self):
        """Test that player can choose to gain token in strategy pool."""
        player = Player(id="player1", faction=Faction.ARBOREC)
        initial_strategy = player.command_sheet.strategy_pool
        initial_reinforcements = player.reinforcements

        success = player.gain_command_token("strategy")

        assert success
        assert player.command_sheet.strategy_pool == initial_strategy + 1
        assert player.reinforcements == initial_reinforcements - 1
        # Other pools should remain unchanged
        assert player.command_sheet.tactic_pool == 3
        assert player.command_sheet.fleet_pool == 3

    def test_invalid_pool_raises_error(self):
        """Test that specifying an invalid pool raises an error."""
        player = Player(id="player1", faction=Faction.ARBOREC)

        with pytest.raises(ValueError, match="Invalid pool type"):
            player.gain_command_token("invalid_pool")

    def test_player_can_choose_different_pools_sequentially(self):
        """Test that player can gain tokens in different pools over multiple gains."""
        player = Player(id="player1", faction=Faction.ARBOREC)

        # Gain one in each pool
        assert player.gain_command_token("tactic")
        assert player.gain_command_token("fleet")
        assert player.gain_command_token("strategy")

        # Check all pools increased by 1
        assert player.command_sheet.tactic_pool == 4
        assert player.command_sheet.fleet_pool == 4
        assert player.command_sheet.strategy_pool == 3

        # Check reinforcements decreased by 3
        assert player.reinforcements == 5  # Started with 8, gained 3

    def test_gain_multiple_tokens_in_same_pool(self):
        """Test that player can gain multiple tokens in the same pool."""
        player = Player(id="player1", faction=Faction.ARBOREC)

        # Gain 3 tokens in tactic pool
        for _ in range(3):
            assert player.gain_command_token("tactic")

        assert player.command_sheet.tactic_pool == 6  # Started with 3, gained 3
        assert player.reinforcements == 5  # Started with 8, gained 3
        # Other pools unchanged
        assert player.command_sheet.fleet_pool == 3
        assert player.command_sheet.strategy_pool == 2

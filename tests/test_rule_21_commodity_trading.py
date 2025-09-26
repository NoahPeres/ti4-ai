"""Tests for Rule 21.5-21.6: Commodity trading and conversion mechanics."""

import pytest

from ti4.core.constants import Faction
from ti4.core.player import Player


class TestRule21CommodityTrading:
    """Test commodity trading mechanics (Rule 21.5-21.6)."""

    def test_commodity_converts_to_trade_good_when_received(self) -> None:
        """Test that commodities convert to trade goods when received from another player.

        LRR Reference: Rule 21.5 - When a player receives a commodity from another player,
        the player who received that token converts it into a trade good by placing it
        in the trade good area of their command sheet with the trade good side faceup.
        """
        player1 = Player("Player1", Faction.SOL)
        player2 = Player("Player2", Faction.HACAN)

        # Player1 has commodities
        player1.replenish_commodities()
        assert player1.get_commodities() == 4

        # Player2 starts with no trade goods
        assert player2.get_trade_goods() == 0

        # Player1 gives 2 commodities to Player2
        player1.give_commodities_to_player(player2, 2)

        # Player1 should have 2 commodities left
        assert player1.get_commodities() == 2

        # Player2 should have 2 trade goods (converted from commodities)
        assert player2.get_trade_goods() == 2

    def test_commodity_to_trade_good_conversion_rule(self) -> None:
        """Test that converted commodities become trade goods, not commodities.

        LRR Reference: Rule 21.5a - That token is no longer a commodity token;
        it is a trade good token.
        """
        player1 = Player("Player1", Faction.SOL)
        player2 = Player("Player2", Faction.HACAN)

        # Player1 has commodities
        player1.replenish_commodities()

        # Player2 starts with no commodities or trade goods
        assert player2.get_commodities() == 0
        assert player2.get_trade_goods() == 0

        # Player1 gives commodities to Player2
        player1.give_commodities_to_player(player2, 3)

        # Player2 should have trade goods, not commodities
        assert player2.get_commodities() == 0  # Still no commodities
        assert player2.get_trade_goods() == 3  # But has trade goods

    def test_can_trade_before_replenishment(self) -> None:
        """Test that players can trade commodities before replenishing.

        LRR Reference: Rule 21.5b - A player can trade commodity tokens before
        resolving a game effect that allows them to replenish commodities.
        """
        player1 = Player("Player1", Faction.SOL)
        player2 = Player("Player2", Faction.HACAN)

        # Player1 has some commodities (not at max)
        player1.add_commodities(2)
        assert player1.get_commodities() == 2

        # Player1 can trade before replenishing
        player1.give_commodities_to_player(player2, 1)
        assert player1.get_commodities() == 1
        assert player2.get_trade_goods() == 1

        # Now replenish
        player1.replenish_commodities()
        assert player1.get_commodities() == 4  # Sol's max

    def test_convert_commodities_when_instructed_by_game_effect(self) -> None:
        """Test converting commodities to trade goods when instructed by a game effect.

        LRR Reference: Rule 21.5c - If a game effect instructs a player to convert
        a number of their own commodities to trade goods, those trade goods are not
        treated as being gained for the purpose of triggering other abilities.

        This test verifies that conversion only happens when a specific game effect
        instructs it, not as a general player action.
        """
        player = Player("Player1", Faction.SOL)

        # Player has commodities
        player.replenish_commodities()
        assert player.get_commodities() == 4
        assert player.get_trade_goods() == 0

        # Convert 2 commodities to trade goods via a game effect
        player.convert_commodities_to_trade_goods(2, "Action Card: Trade")

        # Should have fewer commodities and more trade goods
        assert player.get_commodities() == 2
        assert player.get_trade_goods() == 2

    def test_convert_commodities_invalid_amounts(self) -> None:
        """Test that convert_commodities_to_trade_goods rejects invalid inputs."""
        player = Player("Player1", Faction.SOL)
        player.add_commodities(2)

        # Test negative amounts
        with pytest.raises(ValueError, match="Cannot convert negative commodities"):
            player.convert_commodities_to_trade_goods(-1, "Test Effect")

        # Test converting more than owned
        with pytest.raises(
            ValueError, match="Player only has 2 commodities, cannot convert 3"
        ):
            player.convert_commodities_to_trade_goods(3, "Test Effect")

        # Test missing game effect
        with pytest.raises(ValueError, match="game_effect must be specified"):
            player.convert_commodities_to_trade_goods(1, "")

        # Test empty game effect
        with pytest.raises(ValueError, match="game_effect must be specified"):
            player.convert_commodities_to_trade_goods(1, "   ")

    def test_any_commodity_gift_converts_to_trade_good(self) -> None:
        """Test that any commodity given to another player converts to trade good.

        LRR Reference: Rule 21.6 - Any game effect that instructs a player to give
        a commodity to another player causes that commodity to be converted into a trade good.
        """
        player1 = Player("Player1", Faction.SOL)
        player2 = Player("Player2", Faction.HACAN)

        # Player1 has commodities
        player1.replenish_commodities()

        # Any method of giving commodities should convert them
        player1.give_commodities_to_player(player2, 1)

        # The commodity becomes a trade good for the receiver
        assert player2.get_trade_goods() == 1
        assert player2.get_commodities() == 0  # Not a commodity anymore

    def test_cannot_give_more_commodities_than_owned(self) -> None:
        """Test that players cannot give more commodities than they own."""
        player1 = Player("Player1", Faction.SOL)
        player2 = Player("Player2", Faction.HACAN)
        player1.add_commodities(1)

        with pytest.raises(
            ValueError, match="Player only has 1 commodities, cannot give 2"
        ):
            player1.give_commodities_to_player(player2, 2)

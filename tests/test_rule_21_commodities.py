"""Tests for Rule 21: COMMODITIES mechanics.

This module tests the commodity system according to TI4 LRR Rule 21.

Rule 21 defines:
- Commodity token representation (dual-sided with trade goods)
- Faction-specific commodity value limits
- Commodity replenishment mechanics
- Commodity to trade good conversion when traded
- Commodity trading restrictions and rules
- Token supply management
- Token denomination system (1 and 3 values)

LRR Reference: Rule 21 - COMMODITIES
"""

import pytest

from src.ti4.core.constants import Faction
from src.ti4.core.player import Player


class TestRule21CommodityBasics:
    """Test basic commodity mechanics (Rule 21.1-21.2)."""

    def test_faction_has_commodity_value(self) -> None:
        """Test that factions have commodity values on their faction sheets.

        LRR Reference: Rule 21.2 - The commodity value on a player's faction sheet
        indicates the maximum number of commodities that player can have.
        """
        # Create a player with a faction
        player = Player("TestPlayer", Faction.SOL)

        # Each faction should have a commodity value
        commodity_value = player.get_commodity_value()

        # Sol Federation should have commodity value of 4
        assert commodity_value == 4

    def test_player_starts_with_zero_commodities(self) -> None:
        """Test that players start with zero commodities.

        LRR Reference: Rule 21.2 - Players have a maximum based on faction sheet,
        but start with zero commodities.
        """
        player = Player("TestPlayer", Faction.SOL)

        # Player should start with zero commodities
        current_commodities = player.get_commodities()
        assert current_commodities == 0

    def test_commodity_limit_enforcement(self) -> None:
        """Test that players cannot exceed their commodity value limit.

        LRR Reference: Rule 21.2 - The commodity value indicates the maximum
        number of commodities that player can have.
        """
        player = Player("TestPlayer", Faction.SOL)
        commodity_limit = player.get_commodity_value()

        # Should be able to add commodities up to the limit
        player.add_commodities(commodity_limit)
        assert player.get_commodities() == commodity_limit

        # Should not be able to exceed the limit
        with pytest.raises(ValueError, match="Cannot exceed commodity limit"):
            player.add_commodities(1)


class TestRule21CommodityReplenishment:
    """Test commodity replenishment mechanics (Rule 21.3-21.4)."""

    def test_commodity_replenishment_to_faction_value(self) -> None:
        """Test replenishing commodities to faction sheet value.

        LRR Reference: Rule 21.3 - When an effect instructs a player to replenish
        commodities, that player takes the number of commodity tokens necessary
        so that the amount of commodities equals the commodity value on their faction sheet.
        """
        player = Player("TestPlayer", Faction.SOL)

        # Player starts with 0 commodities, Sol has commodity value 4
        assert player.get_commodities() == 0

        # Replenish commodities
        player.replenish_commodities()

        # Should now have commodities equal to faction value
        assert player.get_commodities() == 4

    def test_partial_replenishment(self) -> None:
        """Test replenishing when player already has some commodities.

        LRR Reference: Rule 21.3 - Takes the number necessary so that the amount
        equals the commodity value on their faction sheet.
        """
        player = Player("TestPlayer", Faction.SOL)

        # Give player 2 commodities (Sol limit is 4)
        player.add_commodities(2)
        assert player.get_commodities() == 2

        # Replenish commodities
        player.replenish_commodities()

        # Should now have full amount (4)
        assert player.get_commodities() == 4

    def test_no_replenishment_when_at_max(self) -> None:
        """Test that replenishment does nothing when already at maximum.

        LRR Reference: Rule 21.3 - Takes the number necessary to equal the
        commodity value (zero if already at max).
        """
        player = Player("TestPlayer", Faction.SOL)

        # Fill commodities to max
        player.add_commodities(4)
        assert player.get_commodities() == 4

        # Replenish should not change anything
        player.replenish_commodities()
        assert player.get_commodities() == 4

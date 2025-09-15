"""Player management for TI4."""

from dataclasses import dataclass, field, replace

from ti4.core.command_tokens import CommandTokens


@dataclass(frozen=True)
class Player:
    """Represents a player in a TI4 game."""

    id: str
    faction: str
    trade_goods: int = 0
    commodities: int = 0
    command_tokens: CommandTokens = field(default_factory=CommandTokens)

    def is_valid(self) -> bool:
        """Validate the player data."""
        return (
            self.trade_goods >= 0
            and self.commodities >= 0
            and self.command_tokens.is_valid()
        )

    def spend_trade_goods(self, amount: int) -> "Player":
        """Spend trade goods, returning a new player instance."""
        if amount > self.trade_goods:
            raise ValueError(
                f"Cannot spend {amount} trade goods, only have {self.trade_goods}"
            )
        return replace(self, trade_goods=self.trade_goods - amount)

    def gain_trade_goods(self, amount: int) -> "Player":
        """Gain trade goods, returning a new player instance."""
        return replace(self, trade_goods=self.trade_goods + amount)

    def spend_commodities(self, amount: int) -> "Player":
        """Spend commodities, returning a new player instance."""
        if amount > self.commodities:
            raise ValueError(
                f"Cannot spend {amount} commodities, only have {self.commodities}"
            )
        return replace(self, commodities=self.commodities - amount)

    def gain_commodities(self, amount: int) -> "Player":
        """Gain commodities, returning a new player instance."""
        return replace(self, commodities=self.commodities + amount)

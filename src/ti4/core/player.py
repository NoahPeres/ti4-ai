"""Player implementation for TI4 game state management."""

from dataclasses import dataclass, field

from .command_sheet import CommandSheet, PoolType
from .constants import Faction
from .faction_data import FactionData


@dataclass(frozen=True)
class Player:
    """Represents a player in a TI4 game."""

    id: str
    faction: Faction
    command_sheet: CommandSheet = field(default_factory=CommandSheet)
    reinforcements: int = (
        8  # Rule 20.3: 16 total tokens - 8 on sheet = 8 in reinforcements
    )
    _commodity_count: int = field(default=0, init=False)  # Current commodity count

    def is_valid(self) -> bool:
        """Validate the player data."""
        return True

    def gain_command_token(self, pool: PoolType) -> bool:
        """Gain a command token in the specified pool (Rule 20.2, 20.3).

        Args:
            pool: The pool to place the token in ("tactic", "fleet", or "strategy")

        Returns:
            True if token was gained, False if no tokens available in reinforcements
        """
        # Rule 20.3a: If a player would gain a command token but has none available
        # in their reinforcements, that player cannot gain that command token.
        if self.reinforcements <= 0:
            return False

        # Gain the token and reduce reinforcements
        success = self.command_sheet.gain_command_token(pool)
        if success:
            # Create new player with updated reinforcements (immutable dataclass)
            object.__setattr__(self, "reinforcements", self.reinforcements - 1)

        return success

    def get_commodity_value(self) -> int:
        """Get the commodity value for this player's faction.

        LRR Reference: Rule 21.2 - The commodity value on a player's faction sheet
        indicates the maximum number of commodities that player can have.

        Returns:
            The maximum number of commodities this player can have
        """
        return FactionData.get_commodity_value(self.faction)

    def get_commodities(self) -> int:
        """Get the current number of commodities this player has.

        Returns:
            Current number of commodity tokens
        """
        return self._commodity_count

    def add_commodities(self, count: int) -> None:
        """Add commodity tokens to this player.

        Args:
            count: Number of commodity tokens to add (must be >= 0)

        Raises:
            ValueError: If adding would exceed commodity limit or if count is negative
        """
        if count < 0:
            raise ValueError("Cannot add negative commodities")
        new_count = self._commodity_count + count
        max_commodities = self.get_commodity_value()

        if new_count > max_commodities:
            raise ValueError(f"Cannot exceed commodity limit of {max_commodities}")

        # Since this is a frozen dataclass, we need to modify the field directly
        object.__setattr__(self, "_commodity_count", new_count)

    def replenish_commodities(self) -> None:
        """Replenish commodities to faction's commodity value (Rule 21.3)."""
        commodity_value = self.get_commodity_value()
        object.__setattr__(self, "_commodity_count", commodity_value)

    def get_trade_goods(self) -> int:
        """Get current number of trade goods (Rule 93.2)."""
        return self.command_sheet.get_trade_goods()

    def gain_trade_goods(self, amount: int) -> None:
        """Gain trade goods (Rule 93.2)."""
        self.command_sheet.gain_trade_goods(amount)

    def spend_trade_goods(self, amount: int) -> bool:
        """Spend trade goods for resources, influence, or game effects (Rule 19.2, 93.3, 93.4).

        Trade goods can be spent as resources or influence, or consumed by specific game
        effects that require trade goods. Returns True if successful, False if insufficient.
        Passing amount==0 is a no-op and returns True.

        Args:
            amount: Number of trade goods to spend

        Returns:
            bool: True if successful or amount==0, False if insufficient trade goods
        """
        return self.command_sheet.spend_trade_goods(amount)

    def give_commodities_to_player(self, other_player: "Player", amount: int) -> None:
        """Give commodities to another player, converting them to trade goods (Rule 21.5, 21.6).
        Passing amount==0 is a no-op.

        Args:
            other_player: The player receiving the commodities
            amount: Number of commodities to give

        Raises:
            ValueError: If player doesn't have enough commodities or trying to give to self
        """
        if amount < 0:
            raise ValueError("Cannot give negative commodities")
        if amount == 0:
            return
        if self is other_player:
            raise ValueError("Cannot give commodities to yourself")
        if self._commodity_count < amount:
            raise ValueError(
                f"Player only has {self._commodity_count} commodities, cannot give {amount}"
            )

        # Remove commodities from this player
        self._remove_commodities(amount)

        # Convert to trade goods for the receiving player (Rule 21.5)
        other_player.gain_trade_goods(amount)

    def convert_commodities_to_trade_goods(self, amount: int, game_effect: str) -> None:
        """Convert commodities to trade goods when instructed by a game effect (Rule 21.5c).

        Rule 21.5c: "If a game effect instructs a player to convert a number of their
        own commodities to trade goods, those trade goods are not treated as being
        gained for the purpose of triggering other abilities."

        Passing amount==0 is a no-op.

        Args:
            amount: Number of commodities to convert
            game_effect: Description of the game effect instructing this conversion
                        (e.g., "Action Card: Trade", "Technology: Sarween Tools")

        Raises:
            ValueError: If player doesn't have enough commodities or game_effect is empty
        """
        if amount < 0:
            raise ValueError("Cannot convert negative commodities")
        if not game_effect or not game_effect.strip():
            raise ValueError(
                "game_effect must be specified - conversion only allowed when instructed by game effect"
            )
        if amount == 0:
            return
        if self._commodity_count < amount:
            raise ValueError(
                f"Player only has {self._commodity_count} commodities, cannot convert {amount}"
            )

        # Remove commodities and add trade goods
        self._remove_commodities(amount)
        self.gain_trade_goods(amount)

    def _remove_commodities(self, amount: int) -> None:
        """Helper method to remove commodities (DRY principle)."""
        if amount < 0:
            raise ValueError("Cannot remove negative commodities")
        if self._commodity_count < amount:
            raise ValueError(
                f"Player only has {self._commodity_count} commodities, cannot remove {amount}"
            )
        object.__setattr__(self, "_commodity_count", self._commodity_count - amount)

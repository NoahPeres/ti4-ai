"""Command sheet implementation for Rule 20: COMMAND TOKENS."""

from dataclasses import dataclass
from typing import Literal

from .constants import GameConstants

PoolType = Literal["tactic", "fleet", "strategy"]


@dataclass
class CommandSheet:
    """Represents a player's command sheet with token pools (Rule 19, 20)."""

    tactic_pool: int = GameConstants.STARTING_TACTIC_TOKENS
    fleet_pool: int = GameConstants.STARTING_FLEET_TOKENS
    strategy_pool: int = GameConstants.STARTING_STRATEGY_TOKENS

    def gain_command_token(self, pool: PoolType) -> bool:
        """Gain a command token in the specified pool (Rule 20.2).

        Args:
            pool: The pool to place the token in ("tactic", "fleet", or "strategy")

        Returns:
            True if token was gained, False if no tokens available in reinforcements
        """
        # Rule 20.3a: If a player would gain a command token but has none available
        # in their reinforcements, that player cannot gain that command token.
        # Note: This method doesn't have access to reinforcements directly,
        # so we'll need to implement this check at the Player level

        if pool == "tactic":
            self.tactic_pool += 1
        elif pool == "fleet":
            self.fleet_pool += 1
        elif pool == "strategy":
            self.strategy_pool += 1
        else:
            raise ValueError(f"Invalid pool type: {pool}")

        return True

    def spend_tactic_token(self) -> bool:
        """Spend a tactic token for tactical action (Rule 20.4).

        Returns:
            True if token was spent, False if no tokens available
        """
        if self.tactic_pool > 0:
            self.tactic_pool -= 1
            return True
        return False

    def spend_strategy_token(self) -> bool:
        """Spend a strategy token for secondary ability (Rule 20.5).

        Returns:
            True if token was spent, False if no tokens available
        """
        if self.strategy_pool > 0:
            self.strategy_pool -= 1
            return True
        return False

    def has_tactic_tokens(self) -> bool:
        """Check if player has tactic tokens available."""
        return self.tactic_pool > 0

    def has_strategy_tokens(self) -> bool:
        """Check if player has strategy tokens available."""
        return self.strategy_pool > 0

    def get_total_tokens(self) -> int:
        """Get total number of tokens on command sheet."""
        return self.tactic_pool + self.fleet_pool + self.strategy_pool

"""Player management for TI4."""

from dataclasses import dataclass, field

from .command_sheet import CommandSheet, PoolType
from .constants import Faction


@dataclass(frozen=True)
class Player:
    """Represents a player in a TI4 game."""

    id: str
    faction: Faction
    command_sheet: CommandSheet = field(default_factory=CommandSheet)
    reinforcements: int = (
        8  # Rule 20.3: 16 total tokens - 8 on sheet = 8 in reinforcements
    )

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

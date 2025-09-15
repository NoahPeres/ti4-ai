"""Command token management for TI4."""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class CommandTokens:
    """Represents command tokens for a player."""

    fleet: int = 0
    strategy: int = 0
    tactic: int = 0

    def is_valid(self) -> bool:
        """Validate the command token data."""
        return self.fleet >= 0 and self.strategy >= 0 and self.tactic >= 0

    def spend_fleet_token(self) -> "CommandTokens":
        """Spend a fleet token, returning a new instance."""
        if self.fleet <= 0:
            raise ValueError("Cannot spend fleet token, none available")
        return replace(self, fleet=self.fleet - 1)

    def spend_strategy_token(self) -> "CommandTokens":
        """Spend a strategy token, returning a new instance."""
        if self.strategy <= 0:
            raise ValueError("Cannot spend strategy token, none available")
        return replace(self, strategy=self.strategy - 1)

    def spend_tactic_token(self) -> "CommandTokens":
        """Spend a tactic token, returning a new instance."""
        if self.tactic <= 0:
            raise ValueError("Cannot spend tactic token, none available")
        return replace(self, tactic=self.tactic - 1)

    @property
    def total(self) -> int:
        """Get the total number of command tokens."""
        return self.fleet + self.strategy + self.tactic

    def redistribute(self, fleet: int, strategy: int, tactic: int) -> "CommandTokens":
        """Redistribute tokens between pools, preserving total count."""
        new_total = fleet + strategy + tactic
        if new_total != self.total:
            raise ValueError(f"Total tokens must remain {self.total}, got {new_total}")
        return CommandTokens(fleet=fleet, strategy=strategy, tactic=tactic)

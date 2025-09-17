"""Strategy card management for TI4."""

from dataclasses import dataclass


@dataclass(frozen=True)
class StrategyCard:
    """Represents a strategy card in TI4."""

    id: int
    name: str
    initiative: int

    def is_valid(self) -> bool:
        """Validate the strategy card data."""
        return self.id > 0 and self.initiative > 0 and bool(self.name)


# Standard TI4 strategy cards
STANDARD_STRATEGY_CARDS = [
    StrategyCard(id=1, name="Leadership", initiative=1),
    StrategyCard(id=2, name="Diplomacy", initiative=2),
    StrategyCard(id=3, name="Politics", initiative=3),
    StrategyCard(id=4, name="Construction", initiative=4),
    StrategyCard(id=5, name="Trade", initiative=5),
    StrategyCard(id=6, name="Warfare", initiative=6),
    StrategyCard(id=7, name="Technology", initiative=7),
    StrategyCard(id=8, name="Imperial", initiative=8),
]

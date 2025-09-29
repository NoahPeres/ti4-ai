"""
Ability Cost Management System

This module handles the payment and validation of ability costs,
separating this concern from the main ability resolution logic.
"""

from typing import Any, Optional

from ti4.core.card_types import ExplorationCardProtocol, PlanetTrait


class AbilityCostManager:
    """Manages the payment and validation of ability costs"""

    def can_pay_cost(self, cost_type: str, amount: int, player: Any) -> bool:
        """Check if player can pay a specific cost type"""
        # Handle relic fragment costs
        if cost_type.startswith("purge_") and cost_type.endswith("_relic_fragments"):
            trait = self._extract_trait_from_cost_type(cost_type)
            if trait:
                return self._can_purge_relic_fragments(player, trait, amount)

        # Handle other cost types
        if cost_type == "resources":
            return getattr(player, "resources", 0) >= amount
        elif cost_type == "trade_goods":
            return getattr(player, "trade_goods", 0) >= amount
        elif cost_type == "command_tokens":
            return getattr(player, "command_tokens", 0) >= amount
        elif cost_type == "exhaust_card":
            return True  # Simplified - would need card_id context

        return False

    def pay_cost(self, cost_type: str, amount: int, player: Any) -> bool:
        """Pay a specific cost type"""
        if cost_type.startswith("purge_") and cost_type.endswith("_relic_fragments"):
            trait = self._extract_trait_from_cost_type(cost_type)
            if trait:
                return self._purge_relic_fragments(player, trait, amount)
        elif cost_type == "resources":
            # Simplified - would need actual resource spending logic
            return True
        elif cost_type == "trade_goods":
            # Simplified - would need actual trade goods spending logic
            return True
        elif cost_type == "command_tokens":
            # Simplified - would need actual command token spending logic
            return True

        return False

    def _extract_trait_from_cost_type(self, cost_type: str) -> Optional[PlanetTrait]:
        """Extract planet trait from cost type string"""
        prefix = "purge_"
        suffix = "_relic_fragments"
        if not (cost_type.startswith(prefix) and cost_type.endswith(suffix)):
            return None
        key = cost_type[len(prefix) : -len(suffix)]
        try:
            return PlanetTrait(key)
        except ValueError:
            return None

    def _can_purge_relic_fragments(
        self, player: Any, trait: PlanetTrait, amount: int
    ) -> bool:
        """Check if player can purge the required number of relic fragments"""
        if not hasattr(player, "relic_fragments"):
            return False

        matching_fragments = get_matching_fragments(player.relic_fragments, trait)
        return len(matching_fragments) >= amount

    def _purge_relic_fragments(
        self, player: Any, trait: PlanetTrait, amount: int
    ) -> bool:
        """Purge relic fragments of a specific trait"""
        if not self._can_purge_relic_fragments(player, trait, amount):
            return False

        to_remove = get_matching_fragments(player.relic_fragments, trait)[-amount:]
        for fragment in to_remove:
            player.relic_fragments.remove(fragment)

        return True


def get_matching_fragments(
    fragments: list[ExplorationCardProtocol], trait: PlanetTrait
) -> list[ExplorationCardProtocol]:
    """Get fragments that match the trait, including frontier fragments as wildcards"""
    matching = [fragment for fragment in fragments if fragment.trait == trait]

    # Add frontier fragments as wildcards (they can count as any trait)
    frontier_fragments = [
        fragment for fragment in fragments if fragment.trait == PlanetTrait.FRONTIER
    ]

    return frontier_fragments + matching

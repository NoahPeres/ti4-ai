"""Fleet pool system for TI4 Rule 37: FLEET POOL.

This module implements Rule 37: FLEET POOL mechanics according to the TI4 LRR.
Handles fleet pool token management, ship limits, exclusions, and enforcement.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from .constants import UnitType

if TYPE_CHECKING:
    from .command_sheet import CommandSheet
    from .system import System
    from .unit import Unit


@dataclass
class FleetPoolToken:
    """Represents a command token in the fleet pool."""

    ship_silhouette_faceup: bool = True
    in_fleet_pool: bool = True

    def is_ship_silhouette_faceup(self) -> bool:
        """Check if token has ship silhouette faceup."""
        return self.ship_silhouette_faceup

    def is_in_fleet_pool(self) -> bool:
        """Check if token is in fleet pool."""
        return self.in_fleet_pool


@dataclass
class FleetPool:
    """Represents a player's fleet pool."""

    tokens: list[FleetPoolToken]

    @property
    def token_count(self) -> int:
        """Get the number of tokens in the fleet pool."""
        return len(self.tokens)


# CommandSheet is imported from command_sheet.py - no duplicate needed


@dataclass
class SpendResult:
    """Result of attempting to spend a fleet pool token."""

    success: bool
    error_message: str = ""


class FleetPoolManager:
    """Manages fleet pool mechanics according to Rule 37.

    Handles:
    - Fleet pool ship limits (Rule 37.1)
    - Planet and capacity exclusions (Rule 37.1a)
    - Transport exclusions (Rule 37.1b)
    - Token orientation (Rule 37.2)
    - Excess ship removal (Rule 37.3)
    - Spending restrictions (Rule 37.4)
    """

    def __init__(self) -> None:
        """Initialize the fleet pool manager."""
        pass

    def is_fleet_pool_valid(
        self, system: "System", player: str, fleet_tokens: int
    ) -> bool:
        """Check if fleet pool limits are respected in a system.

        Args:
            system: The system to check
            player: The player whose fleet to validate
            fleet_tokens: Number of fleet pool tokens available

        Returns:
            True if fleet pool limits are respected

        LRR Reference: Rule 37.1 - Fleet pool ship limits
        """
        # Rule 37.1: Fleet pool tokens limit non-fighter ships per system
        non_fighter_ships = self._count_non_fighter_ships_in_system(system, player)
        return non_fighter_ships <= fleet_tokens

    def _count_non_fighter_ships_in_system(self, system: "System", player: str) -> int:
        """Count non-fighter ships belonging to a player in a system.

        Args:
            system: The system to check
            player: The player whose ships to count

        Returns:
            Number of non-fighter ships

        LRR Reference: Rule 37.1 - Non-fighter ship counting
        """
        count = 0

        # Count ships in space (exclude planet-based units per Rule 37.1a)
        for unit in system.space_units:
            if unit.owner == player and self._is_non_fighter_ship(unit):
                # Rule 37.1a: Units that count against capacity don't count against fleet pool
                if not self._counts_against_capacity(unit):
                    count += 1

        return count

    def _is_non_fighter_ship(self, unit: "Unit") -> bool:
        """Check if a unit is a non-fighter ship.

        Args:
            unit: The unit to check

        Returns:
            True if the unit is a non-fighter ship

        LRR Reference: Rule 37.1 - Non-fighter ship identification
        """
        # All ships except fighters count against fleet pool
        ship_types = {
            UnitType.CARRIER,
            UnitType.CRUISER,
            UnitType.DESTROYER,
            UnitType.DREADNOUGHT,
            UnitType.FLAGSHIP,
            UnitType.WAR_SUN,
        }
        return unit.unit_type in ship_types

    def _counts_against_capacity(self, unit: "Unit") -> bool:
        """Check if a unit counts against capacity.

        Args:
            unit: The unit to check

        Returns:
            True if the unit counts against capacity

        LRR Reference: Rule 37.1a - Capacity exclusions
        """
        # Rule 37.1a: Units that count against capacity don't count against fleet pool
        # Fighters and infantry count against capacity
        capacity_consuming_types = {UnitType.FIGHTER, UnitType.INFANTRY}
        return unit.unit_type in capacity_consuming_types

    def is_fleet_pool_valid_with_transport(
        self,
        system: "System",
        player: str,
        fleet_tokens: int,
        transported_units: list["Unit"],
    ) -> bool:
        """Check fleet pool validity excluding transported units.

        Args:
            system: The system to check
            player: The player whose fleet to validate
            fleet_tokens: Number of fleet pool tokens available
            transported_units: Units being transported through this system

        Returns:
            True if fleet pool limits are respected

        LRR Reference: Rule 37.1b - Transport exclusions
        """
        # Rule 37.1b: Transported units don't count in transit systems
        non_fighter_ships = self._count_non_fighter_ships_in_system(system, player)

        # Subtract transported non-fighter ships
        transported_non_fighters = sum(
            1
            for unit in transported_units
            if unit.owner == player and self._is_non_fighter_ship(unit)
        )

        effective_ships = non_fighter_ships - transported_non_fighters
        return effective_ships <= fleet_tokens

    def create_fleet_pool_tokens(self, count: int) -> list[FleetPoolToken]:
        """Create fleet pool tokens with proper orientation.

        Args:
            count: Number of tokens to create

        Returns:
            List of properly oriented fleet pool tokens

        LRR Reference: Rule 37.2 - Token orientation
        """
        # Rule 37.2: Fleet pool tokens placed with ship silhouette faceup
        return [
            FleetPoolToken(ship_silhouette_faceup=True, in_fleet_pool=True)
            for _ in range(count)
        ]

    def create_fleet_pool_token(self, ship_silhouette_faceup: bool) -> FleetPoolToken:
        """Create a single fleet pool token with specified orientation.

        Args:
            ship_silhouette_faceup: Whether ship silhouette should be faceup

        Returns:
            Fleet pool token with specified orientation

        LRR Reference: Rule 37.2 - Token orientation
        """
        return FleetPoolToken(
            ship_silhouette_faceup=ship_silhouette_faceup, in_fleet_pool=True
        )

    def is_fleet_pool_token_valid(self, token: FleetPoolToken) -> bool:
        """Check if a fleet pool token has proper orientation.

        Args:
            token: The token to validate

        Returns:
            True if token has proper orientation

        LRR Reference: Rule 37.2 - Token orientation validation
        """
        # Rule 37.2: Fleet pool tokens must have ship silhouette faceup
        return token.is_ship_silhouette_faceup() and token.is_in_fleet_pool()

    def enforce_fleet_pool_limit(
        self, system: "System", player: str, fleet_tokens: int
    ) -> list["Unit"]:
        """Enforce fleet pool limits by removing excess ships.

        Args:
            system: The system to enforce limits in
            player: The player whose fleet to limit
            fleet_tokens: Number of fleet pool tokens available

        Returns:
            List of ships that were removed

        LRR Reference: Rule 37.3 - Excess ship removal
        """
        # Rule 37.3: Remove excess ships when fleet pool exceeded
        non_fighter_ships = [
            unit
            for unit in system.space_units
            if unit.owner == player
            and self._is_non_fighter_ship(unit)
            and not self._counts_against_capacity(unit)
        ]

        excess_count = len(non_fighter_ships) - fleet_tokens
        if excess_count <= 0:
            return []

        # Remove excess ships (player choice would be handled by UI)
        removed_ships = non_fighter_ships[:excess_count]
        for ship in removed_ships:
            system.space_units.remove(ship)

        return removed_ships

    def enforce_fleet_pool_limit_with_choice(
        self,
        system: "System",
        player: str,
        fleet_tokens: int,
        ships_to_remove: list["Unit"],
    ) -> list["Unit"]:
        """Enforce fleet pool limits with player choice of which ships to remove.

        Args:
            system: The system to enforce limits in
            player: The player whose fleet to limit
            fleet_tokens: Number of fleet pool tokens available
            ships_to_remove: Specific ships the player chooses to remove

        Returns:
            List of ships that were removed

        LRR Reference: Rule 37.3 - Player choice in excess ship removal
        """
        # Rule 37.3: "they choose and remove excess ships"
        for ship in ships_to_remove:
            if ship in system.space_units:
                system.space_units.remove(ship)

        return ships_to_remove

    def enforce_fleet_pool_limit_and_return_to_reinforcements(
        self,
        system: "System",
        player: str,
        fleet_tokens: int,
        reinforcements: dict[UnitType, int],
    ) -> dict[UnitType, int]:
        """Enforce fleet pool limits and return excess ships to reinforcements.

        Args:
            system: The system to enforce limits in
            player: The player whose fleet to limit
            fleet_tokens: Number of fleet pool tokens available
            reinforcements: Current reinforcement counts

        Returns:
            Updated reinforcement counts

        LRR Reference: Rule 37.3 - Return excess ships to reinforcements
        """
        # Rule 37.3: "returning those units to their reinforcements"
        removed_ships = self.enforce_fleet_pool_limit(system, player, fleet_tokens)

        updated_reinforcements = reinforcements.copy()
        for ship in removed_ships:
            updated_reinforcements[ship.unit_type] = (
                updated_reinforcements.get(ship.unit_type, 0) + 1
            )

        return updated_reinforcements

    def can_spend_fleet_pool_token(
        self, fleet_pool: FleetPool, game_effect: Optional[str]
    ) -> bool:
        """Check if a fleet pool token can be spent.

        Args:
            fleet_pool: The fleet pool to spend from
            game_effect: Game effect that might allow spending

        Returns:
            True if token can be spent

        LRR Reference: Rule 37.4 - Spending restrictions
        """
        # Rule 37.4: Cannot spend unless game effect allows
        return game_effect is not None

    def can_spend_fleet_pool_token_for_tactical_action(
        self, fleet_pool: FleetPool
    ) -> bool:
        """Check if fleet pool token can be spent for tactical action.

        Args:
            fleet_pool: The fleet pool to spend from

        Returns:
            False - fleet pool tokens cannot be spent for tactical actions

        LRR Reference: Rule 37.4 - Spending restrictions
        """
        # Rule 37.4: Fleet pool tokens cannot be spent for tactical actions
        return False

    def attempt_spend_fleet_pool_token(
        self, fleet_pool: FleetPool, game_effect: Optional[str]
    ) -> SpendResult:
        """Attempt to spend a fleet pool token.

        Args:
            fleet_pool: The fleet pool to spend from
            game_effect: Game effect that might allow spending

        Returns:
            Result of the spending attempt

        LRR Reference: Rule 37.4 - Spending validation
        """
        # Rule 37.4: Validate spending restrictions
        if not self.can_spend_fleet_pool_token(fleet_pool, game_effect):
            return SpendResult(
                success=False,
                error_message="Fleet pool tokens cannot be spent unless a game effect specifically allows it",
            )

        # Spend the token (remove from fleet pool)
        if fleet_pool.tokens:
            fleet_pool.tokens.pop()
            return SpendResult(success=True)

        return SpendResult(
            success=False, error_message="No tokens available in fleet pool"
        )

    def create_fleet_pool(self, tokens: int) -> FleetPool:
        """Create a fleet pool with specified number of tokens.

        Args:
            tokens: Number of tokens to create

        Returns:
            Fleet pool with tokens

        LRR Reference: Rule 37.2 - Fleet pool creation
        """
        fleet_tokens = self.create_fleet_pool_tokens(tokens)
        return FleetPool(tokens=fleet_tokens)

    def create_command_sheet_with_fleet_pool(
        self, strategy_tokens: int, tactic_tokens: int, fleet_tokens: int
    ) -> "CommandSheet":
        """Create a command sheet with fleet pool.

        Args:
            strategy_tokens: Number of strategy tokens
            tactic_tokens: Number of tactic tokens
            fleet_tokens: Number of fleet pool tokens

        Returns:
            Command sheet with fleet pool

        LRR Reference: Rule 37.0 - Fleet pool as part of command sheet
        """
        from .command_sheet import CommandSheet

        # Create command sheet using the real CommandSheet class
        # The real CommandSheet uses fleet_pool as an integer count
        return CommandSheet(
            strategy_pool=strategy_tokens,
            tactic_pool=tactic_tokens,
            fleet_pool=fleet_tokens,
        )

    def is_command_sheet_fleet_pool_valid(self, command_sheet: "CommandSheet") -> bool:
        """Validate command sheet fleet pool state.

        Args:
            command_sheet: The command sheet to validate

        Returns:
            True if fleet pool state is valid

        LRR Reference: Rule 37.2 - Fleet pool validation
        """
        # The real CommandSheet uses fleet_pool as an integer count
        # Basic validation: ensure fleet_pool is non-negative
        return hasattr(command_sheet, "fleet_pool") and command_sheet.fleet_pool >= 0

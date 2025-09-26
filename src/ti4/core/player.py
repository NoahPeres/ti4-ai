"""Player implementation for TI4 game state management."""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .command_sheet import CommandSheet, PoolType
from .constants import Faction, UnitType
from .exceptions import DeployError, ReinforcementError
from .faction_data import FactionData

if TYPE_CHECKING:
    from .reinforcements import Reinforcements
    from .system import System


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
    _timing_window_id: int = field(default=0, init=False)  # Current timing window
    _deploy_used_this_window: set[str] = field(
        default_factory=set, init=False
    )  # Deploy abilities used this timing window

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

    def consume_reinforcement(self) -> bool:
        """Consume a command token from reinforcements (Rule 20.3).

        Returns:
            True if token was consumed, False if no reinforcements available
        """
        if self.reinforcements > 0:
            object.__setattr__(self, "reinforcements", self.reinforcements - 1)
            return True
        return False

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

    def advance_timing_window(self) -> None:
        """Advance to a new timing window, resetting deploy ability usage (Rule 30.3)."""
        object.__setattr__(self, "_timing_window_id", self._timing_window_id + 1)
        object.__setattr__(self, "_deploy_used_this_window", set())

    def deploy_unit(
        self,
        unit_type: UnitType,
        target_system: "System",
        target_planet: str | None = None,
        reinforcements: "Reinforcements | None" = None,
    ) -> bool:
        """Deploy a unit using deploy ability (Rule 30: DEPLOY).

        Args:
            unit_type: The type of unit to deploy
            target_system: The system to deploy to
            target_planet: The planet to deploy to (if applicable)
            reinforcements: The reinforcements pool to use (optional)

        Returns:
            True if deployment successful

        Raises:
            DeployError: If deployment conditions are not met
            ReinforcementError: If no units available in reinforcements
        """
        from .reinforcements import Reinforcements
        from .unit import Unit

        # Rule 30.1: Check if unit type has deploy ability
        temp_unit = Unit(unit_type=unit_type, owner=self.id, faction=self.faction)
        if not temp_unit.has_deploy():
            raise DeployError(f"Unit {unit_type.value} does not have deploy ability")

        # Rule 30.3: Check timing window restriction
        deploy_key = f"{unit_type.value}_deploy"
        if deploy_key in self._deploy_used_this_window:
            raise DeployError(
                f"Deploy ability already used for {unit_type} in this timing window"
            )

        # Rule 30.2: Check reinforcements for available units
        if reinforcements is None:
            reinforcements = Reinforcements()
        pool = reinforcements.get_pool(self.id)

        # Rule 30.2.a: Check if there are any units with deploy ability in reinforcements
        has_deployable_units = False
        for unit_type_in_pool in pool.get_all_unit_counts():
            if pool.get_unit_count(unit_type_in_pool) > 0:
                # Reuse the temp_unit for capability check instead of creating new instances
                if unit_type_in_pool == unit_type:
                    # We already have the temp_unit for this type
                    if temp_unit.has_deploy():
                        has_deployable_units = True
                        break
                else:
                    temp_check_unit = Unit(
                        unit_type=unit_type_in_pool, owner=self.id, faction=self.faction
                    )
                    if temp_check_unit.has_deploy():
                        has_deployable_units = True
                        break

        if not has_deployable_units:
            raise ReinforcementError(
                "No units with deploy ability available in reinforcements"
            )

        # Check if the specific unit type is available in reinforcements
        if not reinforcements.has_units_available(self.id, unit_type, 1):
            raise ReinforcementError(
                f"No {unit_type.value} available in reinforcements"
            )

        # For deploy ability, we need to deploy to a planet
        if target_planet is None:
            raise DeployError("Deploy ability requires a target planet")

        # Find the target planet in the system
        target_planet_obj = None
        for planet in target_system.planets:
            if planet.name == target_planet:
                target_planet_obj = planet
                break

        if target_planet_obj is None:
            raise DeployError(
                f"Planet {target_planet} not found in system {target_system.system_id}"
            )

        # Rule 30.1: Check if player controls the target planet
        if target_planet_obj.controlled_by != self.id:
            raise DeployError(
                f"Cannot deploy to {target_planet}: planet not controlled by player"
            )

        # Remove from reinforcements first to maintain atomicity
        pool.remove_units(unit_type, 1)

        # Create and place the unit
        try:
            unit_to_deploy = Unit(
                unit_type=unit_type, owner=self.id, faction=self.faction
            )
            target_planet_obj.place_unit(unit_to_deploy)
        except Exception:
            # If placement fails, restore the unit to reinforcements using proper API
            pool.return_destroyed_unit(unit_type)
            raise

        # Mark deploy ability as used in this timing window
        new_used_set = self._deploy_used_this_window.copy()
        new_used_set.add(deploy_key)
        object.__setattr__(self, "_deploy_used_this_window", new_used_set)

        return True

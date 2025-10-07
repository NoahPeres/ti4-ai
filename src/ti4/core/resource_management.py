"""Resource management data structures for TI4.

Implements data structures for Rule 26: COST, Rule 75: RESOURCES, and Rule 47: INFLUENCE.
These structures support planet-based resource/influence spending and cost validation.
"""

from __future__ import annotations

import logging
import math
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable

from .constants import Faction, Technology, UnitType

if TYPE_CHECKING:
    from .game_state import GameState
    from .planet import Planet
    from .player import Player
    from .unit_stats import UnitStatsProvider

# Set up logging for resource operations
logger = logging.getLogger(__name__)


# Custom exception classes for resource-related errors
class ResourceError(Exception):
    """Base exception for resource-related errors."""

    def __init__(self, message: str, context: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.context = context or {}
        self.context["timestamp"] = time.time()


class InsufficientResourcesError(ResourceError):
    """Raised when player lacks sufficient resources."""

    def __init__(
        self,
        required: int,
        available: int,
        shortfall: int,
        player_id: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.required = required
        self.available = available
        self.shortfall = shortfall
        self.player_id = player_id

        message = f"Insufficient resources for player {player_id}: need {required}, have {available} (shortfall: {shortfall})"
        super().__init__(message, context)


class InsufficientInfluenceError(ResourceError):
    """Raised when player lacks sufficient influence."""

    def __init__(
        self,
        required: int,
        available: int,
        shortfall: int,
        player_id: str,
        for_voting: bool = False,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.required = required
        self.available = available
        self.shortfall = shortfall
        self.player_id = player_id
        self.for_voting = for_voting

        voting_context = " (voting)" if for_voting else ""
        message = f"Insufficient influence{voting_context} for player {player_id}: need {required}, have {available} (shortfall: {shortfall})"
        super().__init__(message, context)


class InvalidSpendingPlanError(ResourceError):
    """Raised when spending plan is invalid."""

    def __init__(
        self,
        plan_id: str,
        reason: str,
        player_id: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.plan_id = plan_id
        self.reason = reason
        self.player_id = player_id

        message = f"Invalid spending plan {plan_id} for player {player_id}: {reason}"
        super().__init__(message, context)


class PlanetExhaustionError(ResourceError):
    """Raised when planet exhaustion fails."""

    def __init__(
        self,
        planet_name: str,
        player_id: str,
        operation: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.planet_name = planet_name
        self.player_id = player_id
        self.operation = operation

        message = f"Planet exhaustion failed for {planet_name} (player {player_id}) during {operation}"
        super().__init__(message, context)


class ResourceOperationError(ResourceError):
    """Raised when resource operations fail."""

    def __init__(
        self,
        operation: str,
        player_id: str,
        reason: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.operation = operation
        self.player_id = player_id
        self.reason = reason

        message = (
            f"Resource operation '{operation}' failed for player {player_id}: {reason}"
        )
        super().__init__(message, context)


class CostCalculationError(ResourceError):
    """Raised when cost calculations fail due to invalid data."""

    def __init__(
        self,
        unit_type: UnitType,
        reason: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.unit_type = unit_type
        self.reason = reason

        message = f"Cost calculation failed for {unit_type.name}: {reason}"
        super().__init__(message, context)


class GameStateIntegrityError(ResourceError):
    """Raised when game state integrity is compromised during resource operations."""

    def __init__(
        self,
        operation: str,
        integrity_issue: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.operation = operation
        self.integrity_issue = integrity_issue

        message = (
            f"Game state integrity compromised during {operation}: {integrity_issue}"
        )
        super().__init__(message, context)


@dataclass(frozen=True)
class ResourceSources:
    """Breakdown of available resource sources for a player.

    Tracks resources from controlled planets and trade goods.
    Used for Rule 75: RESOURCES calculations.
    """

    planets: dict[str, int]  # planet_name -> resource_value
    trade_goods: int
    total_available: int

    def get_planet_names(self) -> list[str]:
        """Get names of planets that can provide resources."""
        return list(self.planets.keys())


@dataclass(frozen=True)
class InfluenceSources:
    """Breakdown of available influence sources for a player.

    Tracks influence from controlled planets and trade goods.
    Used for Rule 47: INFLUENCE calculations.
    """

    planets: dict[str, int]  # planet_name -> influence_value
    trade_goods: int  # 0 if for_voting=True (Rule 47.3)
    total_available: int
    for_voting: bool

    def get_planet_names(self) -> list[str]:
        """Get names of planets that can provide influence."""
        return list(self.planets.keys())


@dataclass(frozen=True)
class ResourceSpending:
    """Details of resource spending from planets and trade goods.

    Specifies which planets to exhaust and how many trade goods to spend
    for resource payments.
    """

    planets_to_exhaust: dict[str, int]  # planet_name -> resource_value
    trade_goods_to_spend: int
    total_resources: int


@dataclass(frozen=True)
class InfluenceSpending:
    """Details of influence spending from planets and trade goods.

    Specifies which planets to exhaust and how many trade goods to spend
    for influence payments.
    """

    planets_to_exhaust: dict[str, int]  # planet_name -> influence_value
    trade_goods_to_spend: int  # 0 if for_voting=True (Rule 47.3)
    total_influence: int


@dataclass(frozen=True)
class SpendingPlan:
    """Represents a plan for spending resources/influence.

    Combines resource and influence spending details into a single
    executable plan that can be validated and executed atomically.
    """

    player_id: str
    resource_spending: ResourceSpending
    influence_spending: InfluenceSpending
    total_resource_cost: int
    total_influence_cost: int
    is_valid: bool
    error_message: str | None = None

    def get_total_planets_to_exhaust(self) -> set[str]:
        """Get all planet names that will be exhausted by this plan."""
        resource_planets = set(self.resource_spending.planets_to_exhaust.keys())
        influence_planets = set(self.influence_spending.planets_to_exhaust.keys())
        return resource_planets | influence_planets

    def get_total_trade_goods_to_spend(self) -> int:
        """Get total trade goods that will be consumed by this plan."""
        return (
            self.resource_spending.trade_goods_to_spend
            + self.influence_spending.trade_goods_to_spend
        )


@dataclass(frozen=True)
class SpendingResult:
    """Result of executing a spending plan.

    Tracks the outcome of spending plan execution including
    which planets were exhausted and trade goods spent.
    """

    success: bool
    planets_exhausted: list[str]
    trade_goods_spent: int
    error_message: str | None = None


@dataclass(frozen=True)
class ProductionCost:
    """Represents the cost of a production operation.

    Handles both normal production and dual production (Rule 26.2)
    where two units are produced for the cost of one.
    """

    unit_type: UnitType
    base_cost: float
    modified_cost: float
    quantity_requested: int
    units_produced: int  # May be different due to dual production
    total_cost: float
    is_dual_production: bool

    def get_cost_per_unit(self) -> float:
        """Get the cost per unit actually produced."""
        if self.units_produced == 0:
            return 0.0
        return self.total_cost / self.units_produced


class ResourceManager:
    """Central manager for resource and influence operations.

    Implements Rule 75: RESOURCES and Rule 47: INFLUENCE calculations
    based on controlled planets and trade goods.
    """

    def __init__(self, game_state: GameState) -> None:
        """Initialize with game state for planet and player access."""
        self.game_state = game_state

    def calculate_available_resources(self, player_id: str) -> int:
        """Calculate total resources available from ready planets + trade goods.

        Args:
            player_id: The player ID

        Returns:
            Total resources available (planets + trade goods)

        Raises:
            ResourceOperationError: If player is not found
        """
        logger.info(f"Calculating available resources for player {player_id}")

        # Validate player exists
        player = self._get_player(player_id)
        if not player:
            raise ResourceOperationError(
                operation="calculate_available_resources",
                player_id=player_id,
                reason="Player not found",
                context={"available_players": [p.id for p in self.game_state.players]},
            )

        # Get player's controlled planets
        planets = self.game_state.get_player_planets(player_id)

        # Sum resources from ready (unexhausted) planets
        planet_resources = sum(
            planet.resources for planet in planets if planet.can_spend_resources()
        )

        # Get player's trade goods
        trade_goods = player.get_trade_goods()

        total_resources = planet_resources + trade_goods
        logger.debug(
            f"Player {player_id} has {total_resources} resources ({planet_resources} from planets, {trade_goods} from trade goods)"
        )

        return total_resources

    def calculate_available_influence(
        self, player_id: str, for_voting: bool = False
    ) -> int:
        """Calculate total influence available, excluding trade goods if for_voting.

        Args:
            player_id: The player ID
            for_voting: If True, excludes trade goods per Rule 47.3

        Returns:
            Total influence available

        Raises:
            ResourceOperationError: If player is not found
        """
        logger.info(
            f"Calculating available influence for player {player_id} (for_voting={for_voting})"
        )

        # Validate player exists
        player = self._get_player(player_id)
        if not player:
            raise ResourceOperationError(
                operation="calculate_available_influence",
                player_id=player_id,
                reason="Player not found",
                context={
                    "available_players": [p.id for p in self.game_state.players],
                    "for_voting": for_voting,
                },
            )

        # Get player's controlled planets
        planets = self.game_state.get_player_planets(player_id)

        # Sum influence from ready (unexhausted) planets
        planet_influence = sum(
            planet.influence for planet in planets if planet.can_spend_influence()
        )

        # Get player's trade goods (0 if for voting per Rule 47.3)
        if for_voting:
            trade_goods = 0
        else:
            trade_goods = player.get_trade_goods()

        total_influence = planet_influence + trade_goods
        logger.debug(
            f"Player {player_id} has {total_influence} influence ({planet_influence} from planets, {trade_goods} from trade goods)"
        )

        return total_influence

    def get_resource_sources(self, player_id: str) -> ResourceSources:
        """Get detailed breakdown of resource sources (planets + trade goods).

        Args:
            player_id: The player ID

        Returns:
            ResourceSources with detailed breakdown

        Raises:
            ResourceOperationError: If player is not found
        """
        logger.debug(f"Getting resource sources for player {player_id}")

        # Validate player exists
        player = self._get_player(player_id)
        if not player:
            raise ResourceOperationError(
                operation="get_resource_sources",
                player_id=player_id,
                reason="Player not found",
                context={"available_players": [p.id for p in self.game_state.players]},
            )

        # Get player's controlled planets
        planets = self.game_state.get_player_planets(player_id)

        # Build planet resource mapping (only ready planets with resources > 0)
        planet_resources = {
            planet.name: planet.resources
            for planet in planets
            if planet.can_spend_resources() and planet.resources > 0
        }

        # Get player's trade goods
        trade_goods = player.get_trade_goods()

        total_available = sum(planet_resources.values()) + trade_goods

        return ResourceSources(
            planets=planet_resources,
            trade_goods=trade_goods,
            total_available=total_available,
        )

    def get_influence_sources(
        self, player_id: str, for_voting: bool = False
    ) -> InfluenceSources:
        """Get detailed breakdown of influence sources.

        Args:
            player_id: The player ID
            for_voting: If True, excludes trade goods per Rule 47.3

        Returns:
            InfluenceSources with detailed breakdown

        Raises:
            ResourceOperationError: If player is not found
        """
        logger.debug(
            f"Getting influence sources for player {player_id} (for_voting={for_voting})"
        )

        # Validate player exists
        player = self._get_player(player_id)
        if not player:
            raise ResourceOperationError(
                operation="get_influence_sources",
                player_id=player_id,
                reason="Player not found",
                context={
                    "available_players": [p.id for p in self.game_state.players],
                    "for_voting": for_voting,
                },
            )

        # Get player's controlled planets
        planets = self.game_state.get_player_planets(player_id)

        # Build planet influence mapping (only ready planets with influence > 0)
        planet_influence = {
            planet.name: planet.influence
            for planet in planets
            if planet.can_spend_influence() and planet.influence > 0
        }

        # Get player's trade goods (0 if for voting per Rule 47.3)
        if for_voting:
            trade_goods = 0
        else:
            trade_goods = player.get_trade_goods()

        total_available = sum(planet_influence.values()) + trade_goods

        return InfluenceSources(
            planets=planet_influence,
            trade_goods=trade_goods,
            total_available=total_available,
            for_voting=for_voting,
        )

    def create_spending_plan(
        self,
        player_id: str,
        resource_amount: int = 0,
        influence_amount: int = 0,
        for_voting: bool = False,
    ) -> SpendingPlan:
        """Create a plan for spending resources/influence from available sources.

        Args:
            player_id: The player ID
            resource_amount: Amount of resources needed
            influence_amount: Amount of influence needed
            for_voting: If True, excludes trade goods from influence per Rule 47.3

        Returns:
            SpendingPlan with details of how to spend resources/influence
        """
        # Get available sources
        resource_sources = self.get_resource_sources(player_id)
        influence_sources = self.get_influence_sources(player_id, for_voting)

        # Create resource spending plan
        resource_spending = self._create_resource_spending(
            resource_sources, resource_amount
        )

        # Create influence spending plan
        influence_spending = self._create_influence_spending(
            influence_sources, influence_amount
        )

        # Check if plan is valid
        is_valid = (
            resource_spending.total_resources >= resource_amount
            and influence_spending.total_influence >= influence_amount
        )

        error_message = None
        if not is_valid:
            errors = []
            if resource_spending.total_resources < resource_amount:
                shortfall = resource_amount - resource_spending.total_resources
                errors.append(
                    f"Insufficient resources for player {player_id}: need {resource_amount}, have {resource_spending.total_resources} (shortfall: {shortfall})"
                )
            if influence_spending.total_influence < influence_amount:
                shortfall = influence_amount - influence_spending.total_influence
                voting_context = " for voting" if for_voting else ""
                errors.append(
                    f"Insufficient influence{voting_context} for player {player_id}: need {influence_amount}, have {influence_spending.total_influence} (shortfall: {shortfall})"
                )
            error_message = "; ".join(errors)

        return SpendingPlan(
            player_id=player_id,
            resource_spending=resource_spending,
            influence_spending=influence_spending,
            total_resource_cost=resource_amount,
            total_influence_cost=influence_amount,
            is_valid=is_valid,
            error_message=error_message,
        )

    def can_afford_spending(
        self,
        player_id: str,
        resource_amount: int = 0,
        influence_amount: int = 0,
        for_voting: bool = False,
    ) -> bool:
        """Check if player can afford the specified spending.

        Args:
            player_id: The player ID
            resource_amount: Amount of resources needed
            influence_amount: Amount of influence needed
            for_voting: If True, excludes trade goods from influence per Rule 47.3

        Returns:
            True if player can afford the spending

        Raises:
            ResourceOperationError: If player is not found
        """
        logger.debug(
            f"Checking if player {player_id} can afford {resource_amount} resources and {influence_amount} influence (for_voting={for_voting})"
        )

        # These methods will raise ResourceOperationError if player doesn't exist
        available_resources = self.calculate_available_resources(player_id)
        available_influence = self.calculate_available_influence(player_id, for_voting)

        can_afford = (
            available_resources >= resource_amount
            and available_influence >= influence_amount
        )

        logger.debug(f"Player {player_id} can afford: {can_afford}")
        return can_afford

    def execute_spending_plan(self, plan: SpendingPlan) -> SpendingResult:
        """Execute a spending plan, exhausting planets and consuming trade goods.

        Performs atomic execution - either all operations succeed or all are rolled back.

        Args:
            plan: The spending plan to execute

        Returns:
            SpendingResult indicating success/failure and what was spent

        Raises:
            GameStateIntegrityError: If game state integrity is compromised
        """
        logger.info(f"Executing spending plan for player {plan.player_id}")
        logger.debug(
            f"Plan details: resources={plan.total_resource_cost}, influence={plan.total_influence_cost}"
        )

        # Validate plan first
        if not plan.is_valid:
            logger.warning(
                f"Spending plan for player {plan.player_id} is invalid: {plan.error_message}"
            )
            return SpendingResult(
                success=False,
                planets_exhausted=[],
                trade_goods_spent=0,
                error_message=plan.error_message or "Invalid spending plan",
            )

        # Additional integrity checks
        if plan.total_resource_cost < 0 or plan.total_influence_cost < 0:
            raise GameStateIntegrityError(
                operation="execute_spending_plan",
                integrity_issue=f"Negative costs detected: resources={plan.total_resource_cost}, influence={plan.total_influence_cost}",
                context={"plan": plan},
            )

        # Get player for trade goods operations
        player = self._get_player(plan.player_id)
        if not player:
            error_msg = f"Player {plan.player_id} not found"
            logger.error(error_msg)
            return SpendingResult(
                success=False,
                planets_exhausted=[],
                trade_goods_spent=0,
                error_message=error_msg,
            )

        # Track what we've done for rollback
        exhausted_planets: list[str] = []
        total_trade_goods_spent = 0

        try:
            logger.debug(f"Starting planet exhaustion for player {plan.player_id}")

            # Exhaust planets for resource spending
            for planet_name in plan.resource_spending.planets_to_exhaust:
                logger.debug(f"Exhausting planet {planet_name} for resources")
                planet = self._get_player_planet(plan.player_id, planet_name)
                if not planet:
                    raise ValueError(
                        f"Planet {planet_name} not found for player {plan.player_id}"
                    )
                if planet.is_exhausted():
                    raise ValueError(f"Planet {planet_name} is already exhausted")

                planet.exhaust()
                exhausted_planets.append(planet_name)
                logger.debug(f"Successfully exhausted planet {planet_name}")

            # Exhaust planets for influence spending (if not already exhausted)
            for planet_name in plan.influence_spending.planets_to_exhaust:
                if planet_name not in exhausted_planets:  # Don't double-exhaust
                    logger.debug(f"Exhausting planet {planet_name} for influence")
                    planet = self._get_player_planet(plan.player_id, planet_name)
                    if not planet:
                        raise ValueError(
                            f"Planet {planet_name} not found for player {plan.player_id}"
                        )
                    if planet.is_exhausted():
                        raise ValueError(f"Planet {planet_name} is already exhausted")

                    planet.exhaust()
                    exhausted_planets.append(planet_name)
                    logger.debug(f"Successfully exhausted planet {planet_name}")

            # Spend trade goods
            total_trade_goods_to_spend = plan.get_total_trade_goods_to_spend()
            if total_trade_goods_to_spend > 0:
                logger.debug(
                    f"Spending {total_trade_goods_to_spend} trade goods for player {plan.player_id}"
                )
                if not player.spend_trade_goods(total_trade_goods_to_spend):
                    raise ValueError(
                        f"Insufficient trade goods: need {total_trade_goods_to_spend}, have {player.get_trade_goods()}"
                    )
                total_trade_goods_spent = total_trade_goods_to_spend
                logger.debug(
                    f"Successfully spent {total_trade_goods_spent} trade goods"
                )

            # Success!
            logger.info(
                f"Successfully executed spending plan for player {plan.player_id}"
            )
            return SpendingResult(
                success=True,
                planets_exhausted=exhausted_planets,
                trade_goods_spent=total_trade_goods_spent,
                error_message=None,
            )

        except Exception as e:
            logger.warning(
                f"Spending plan execution failed for player {plan.player_id}: {str(e)}"
            )
            logger.info(f"Starting rollback for player {plan.player_id}")

            # Rollback: ready all planets we exhausted
            for planet_name in exhausted_planets:
                logger.debug(f"Rolling back planet exhaustion for {planet_name}")
                planet = self._get_player_planet(plan.player_id, planet_name)
                if planet and planet.is_exhausted():
                    planet.ready()
                    logger.debug(f"Successfully rolled back planet {planet_name}")

            # Rollback: restore trade goods
            if total_trade_goods_spent > 0:
                logger.debug(
                    f"Rolling back {total_trade_goods_spent} trade goods for player {plan.player_id}"
                )
                player.gain_trade_goods(total_trade_goods_spent)
                logger.debug(
                    f"Successfully rolled back {total_trade_goods_spent} trade goods"
                )

            logger.info(f"Rollback completed for player {plan.player_id}")
            return SpendingResult(
                success=False,
                planets_exhausted=[],
                trade_goods_spent=0,
                error_message=str(e),
            )

    def _get_player(self, player_id: str) -> Player | None:
        """Get player by ID from game state."""
        for player in self.game_state.players:
            if player.id == player_id:
                return player
        return None

    def _get_player_planet(self, player_id: str, planet_name: str) -> Planet | None:
        """Get a specific planet controlled by a player."""
        planets = self.game_state.get_player_planets(player_id)
        for planet in planets:
            if planet.name == planet_name:
                return planet
        return None

    def _create_resource_spending(
        self, sources: ResourceSources, amount: int
    ) -> ResourceSpending:
        """Create resource spending plan from available sources."""
        if amount == 0:
            return ResourceSpending(
                planets_to_exhaust={}, trade_goods_to_spend=0, total_resources=0
            )

        planets_to_exhaust = {}
        remaining = amount

        # Use planets first
        for planet_name, planet_resources in sources.planets.items():
            if remaining <= 0:
                break
            if remaining >= planet_resources:
                planets_to_exhaust[planet_name] = planet_resources
                remaining -= planet_resources
            else:
                # Can't partially exhaust a planet, so we'll use it fully
                planets_to_exhaust[planet_name] = planet_resources
                remaining -= planet_resources

        # Use trade goods if needed and available
        trade_goods_to_spend = 0
        if remaining > 0 and sources.trade_goods > 0:
            trade_goods_to_spend = min(remaining, sources.trade_goods)
            remaining -= trade_goods_to_spend

        total_resources = sum(planets_to_exhaust.values()) + trade_goods_to_spend

        return ResourceSpending(
            planets_to_exhaust=planets_to_exhaust,
            trade_goods_to_spend=trade_goods_to_spend,
            total_resources=total_resources,
        )

    def _create_influence_spending(
        self, sources: InfluenceSources, amount: int
    ) -> InfluenceSpending:
        """Create influence spending plan from available sources."""
        if amount == 0:
            return InfluenceSpending(
                planets_to_exhaust={}, trade_goods_to_spend=0, total_influence=0
            )

        planets_to_exhaust = {}
        remaining = amount

        # Use planets first
        for planet_name, planet_influence in sources.planets.items():
            if remaining <= 0:
                break
            if remaining >= planet_influence:
                planets_to_exhaust[planet_name] = planet_influence
                remaining -= planet_influence
            else:
                # Can't partially exhaust a planet, so we'll use it fully
                planets_to_exhaust[planet_name] = planet_influence
                remaining -= planet_influence

        # Use trade goods if needed and available (not for voting)
        trade_goods_to_spend = 0
        if remaining > 0 and sources.trade_goods > 0:
            trade_goods_to_spend = min(remaining, sources.trade_goods)
            remaining -= trade_goods_to_spend

        total_influence = sum(planets_to_exhaust.values()) + trade_goods_to_spend

        return InfluenceSpending(
            planets_to_exhaust=planets_to_exhaust,
            trade_goods_to_spend=trade_goods_to_spend,
            total_influence=total_influence,
        )


@dataclass(frozen=True)
class CostValidationResult:
    """Result of cost validation."""

    is_valid: bool
    required_resources: int
    available_resources: int
    shortfall: int
    error_message: str | None = None
    suggested_spending_plan: SpendingPlan | None = None
    reinforcement_shortfall: int = 0


class CostValidator:
    """Validates unit costs and resource availability.

    Implements Rule 26: COST validation with faction and technology modifiers.
    """

    def __init__(
        self, resource_manager: ResourceManager, stats_provider: UnitStatsProvider
    ) -> None:
        """Initialize with resource manager and unit stats provider."""
        self.resource_manager = resource_manager
        self.stats_provider = stats_provider

    def get_unit_cost(
        self,
        unit_type: UnitType,
        faction: Faction | None = None,
        technologies: set[Technology] | None = None,
    ) -> float:
        """Get the final cost of a unit with all modifiers applied.

        Args:
            unit_type: The type of unit
            faction: Optional faction for faction-specific modifiers
            technologies: Optional set of technologies for tech modifiers

        Returns:
            Final cost of the unit with all modifiers applied (minimum 0.0)

        Raises:
            CostCalculationError: If cost calculation fails due to invalid data
        """
        try:
            # Get unit stats with all modifiers applied
            unit_stats = self.stats_provider.get_unit_stats(
                unit_type, faction, technologies
            )

            # Validate that cost is a valid number
            if not isinstance(unit_stats.cost, (int, float)):
                raise CostCalculationError(
                    unit_type=unit_type,
                    reason=f"Invalid cost type: {type(unit_stats.cost)}",
                    context={
                        "faction": faction.name if faction else None,
                        "technologies": [t.name for t in technologies]
                        if technologies
                        else [],
                        "raw_cost": unit_stats.cost,
                    },
                )

            # Check for NaN or infinite values
            if math.isnan(unit_stats.cost) or math.isinf(unit_stats.cost):
                raise CostCalculationError(
                    unit_type=unit_type,
                    reason=f"Invalid cost value: {unit_stats.cost}",
                    context={
                        "faction": faction.name if faction else None,
                        "technologies": [t.name for t in technologies]
                        if technologies
                        else [],
                        "raw_cost": unit_stats.cost,
                    },
                )

            # Prevent negative costs (Requirement 8.4, 8.5)
            final_cost = max(0.0, unit_stats.cost)

            logger.debug(
                f"Calculated cost for {unit_type.name}: {final_cost} (raw: {unit_stats.cost})"
            )
            return final_cost

        except Exception as e:
            if isinstance(e, CostCalculationError):
                raise

            # Wrap unexpected errors
            raise CostCalculationError(
                unit_type=unit_type,
                reason=f"Unexpected error during cost calculation: {str(e)}",
                context={
                    "faction": faction.name if faction else None,
                    "technologies": [t.name for t in technologies]
                    if technologies
                    else [],
                    "error_type": type(e).__name__,
                },
            ) from e

    def get_production_cost(
        self,
        unit_type: UnitType,
        quantity: int,
        faction: Faction | None = None,
        technologies: set[Technology] | None = None,
    ) -> ProductionCost:
        """Get cost for producing a quantity of units, handling dual production.

        Args:
            unit_type: The type of unit to produce
            quantity: Number of units requested
            faction: Optional faction for faction-specific modifiers
            technologies: Optional set of technologies for tech modifiers

        Returns:
            ProductionCost with details of the production cost calculation
        """
        # Get base and modified unit cost
        base_cost = self.stats_provider.get_unit_stats(unit_type).cost
        modified_cost = self.get_unit_cost(unit_type, faction, technologies)

        # Check for dual production (Rule 26.2)
        is_dual_production = self._is_dual_production_unit(unit_type) and quantity == 2

        if is_dual_production:
            # Dual production: 2 units for the cost of 1
            units_produced = 2
            total_cost = modified_cost  # Cost of 1 unit for 2 units produced
        else:
            # Normal production: cost per unit
            units_produced = quantity
            total_cost = modified_cost * quantity

        return ProductionCost(
            unit_type=unit_type,
            base_cost=base_cost,
            modified_cost=modified_cost,
            quantity_requested=quantity,
            units_produced=units_produced,
            total_cost=total_cost,
            is_dual_production=is_dual_production,
        )

    def can_produce_without_cost(self, unit_type: UnitType) -> bool:
        """Check if unit can be produced without cost (structures via Construction).

        Args:
            unit_type: The type of unit to check

        Returns:
            True if unit can be produced without cost (Rule 26.3)
        """
        # Structures (PDS, Space Dock) can be produced without cost via Construction
        # Rule 26.3: Units without cost cannot be produced normally
        unit_stats = self.stats_provider.get_unit_stats(unit_type)
        return unit_stats.cost == 0

    def validate_production_cost(
        self, player_id: str, production_cost: ProductionCost
    ) -> CostValidationResult:
        """Validate that player can afford a production cost.

        Args:
            player_id: The player ID
            production_cost: The production cost to validate

        Returns:
            CostValidationResult indicating if the cost can be afforded
        """
        # Rule 26.3: Units without cost cannot be produced normally
        if production_cost.total_cost == 0:
            return CostValidationResult(
                is_valid=False,
                required_resources=0,
                available_resources=self.resource_manager.calculate_available_resources(
                    player_id
                ),
                shortfall=0,
                error_message="Units without cost cannot be produced normally (Rule 26.3)",
                suggested_spending_plan=None,
            )

        # Use ceiling to handle fractional costs (e.g., 0.5 fighter cost becomes 1 resource)
        required_resources = math.ceil(production_cost.total_cost)
        available_resources = self.resource_manager.calculate_available_resources(
            player_id
        )

        is_valid = available_resources >= required_resources
        shortfall = max(0, required_resources - available_resources)

        error_message = None
        suggested_spending_plan = None

        if not is_valid:
            unit_context = (
                f" for {production_cost.unit_type.name.lower()} production"
                if hasattr(production_cost.unit_type, "name")
                else " for production"
            )
            error_message = (
                f"Insufficient resources{unit_context}: need {required_resources}, "
                f"have {available_resources} (shortfall: {shortfall})"
            )
        else:
            # Create suggested spending plan
            suggested_spending_plan = self.resource_manager.create_spending_plan(
                player_id, resource_amount=required_resources
            )

        return CostValidationResult(
            is_valid=is_valid,
            required_resources=required_resources,
            available_resources=available_resources,
            shortfall=shortfall,
            error_message=error_message,
            suggested_spending_plan=suggested_spending_plan,
        )

    def validate_production_cost_with_reinforcements(
        self,
        player_id: str,
        production_cost: ProductionCost,
        available_reinforcements: int,
    ) -> CostValidationResult:
        """Validate that player can afford a production cost including reinforcement check.

        Args:
            player_id: The player ID
            production_cost: The production cost to validate
            available_reinforcements: Number of units available in reinforcements

        Returns:
            CostValidationResult indicating if the cost can be afforded and reinforcements are sufficient
        """
        # First validate resource cost
        base_validation = self.validate_production_cost(player_id, production_cost)

        # Check reinforcement availability
        units_needed = production_cost.units_produced
        reinforcement_shortfall = max(0, units_needed - available_reinforcements)

        # Combine validation results
        is_valid = base_validation.is_valid and reinforcement_shortfall == 0

        error_messages = []
        if base_validation.error_message:
            error_messages.append(base_validation.error_message)

        if reinforcement_shortfall > 0:
            error_messages.append(
                f"Insufficient reinforcements: need {units_needed}, have {available_reinforcements} (shortfall: {reinforcement_shortfall})"
            )

        error_message = "; ".join(error_messages) if error_messages else None

        return CostValidationResult(
            is_valid=is_valid,
            required_resources=base_validation.required_resources,
            available_resources=base_validation.available_resources,
            shortfall=base_validation.shortfall,
            error_message=error_message,
            suggested_spending_plan=base_validation.suggested_spending_plan
            if is_valid
            else None,
            reinforcement_shortfall=reinforcement_shortfall,
        )

    def validate_production_cost_with_construction_exemption(
        self, player_id: str, production_cost: ProductionCost
    ) -> CostValidationResult:
        """Validate production cost with Construction strategy card exemption.

        When Construction strategy card is active, structures (units with zero cost)
        can be produced without resource cost validation.

        Args:
            player_id: The player ID
            production_cost: The production cost to validate

        Returns:
            CostValidationResult indicating if the cost can be afforded
        """
        # Construction exemption: allow zero-cost units (structures) to be produced
        if production_cost.total_cost == 0:
            return CostValidationResult(
                is_valid=True,
                required_resources=0,
                available_resources=self.resource_manager.calculate_available_resources(
                    player_id
                ),
                shortfall=0,
                error_message=None,
                suggested_spending_plan=self.resource_manager.create_spending_plan(
                    player_id, resource_amount=0
                ),
            )

        # For non-zero cost units, use normal validation
        return self.validate_production_cost(player_id, production_cost)

    def _is_dual_production_unit(self, unit_type: UnitType) -> bool:
        """Check if unit type supports dual production (Rule 26.2).

        Args:
            unit_type: The unit type to check

        Returns:
            True if unit supports dual production (fighters and infantry)
        """
        return unit_type in {UnitType.FIGHTER, UnitType.INFANTRY}


# Performance optimization classes


@dataclass(frozen=True)
class CacheStatistics:
    """Statistics for cache performance monitoring."""

    total_requests: int
    cache_hits: int
    cache_misses: int

    @property
    def cache_hit_rate(self) -> float:
        """Calculate cache hit rate as a percentage."""
        if self.total_requests == 0:
            return 0.0
        return self.cache_hits / self.total_requests


class CachedResourceManager(ResourceManager):
    """ResourceManager with caching for improved performance.

    Caches resource/influence calculations when game state hasn't changed.
    Implements cache invalidation when game state is modified.
    """

    def __init__(self, game_state: GameState) -> None:
        """Initialize with game state and empty cache."""
        super().__init__(game_state)
        self._cache: dict[str, Any] = {}
        self._game_state_hash: int = self._calculate_game_state_hash()
        self._cache_stats = {"total_requests": 0, "cache_hits": 0, "cache_misses": 0}

    def calculate_available_resources(self, player_id: str) -> int:
        """Calculate total resources with caching."""
        cache_key = f"resources_{player_id}"
        result = self._get_cached_or_calculate(
            cache_key, lambda: self._calculate_available_resources_uncached(player_id)
        )
        return int(result)

    def calculate_available_influence(
        self, player_id: str, for_voting: bool = False
    ) -> int:
        """Calculate total influence with caching."""
        cache_key = f"influence_{player_id}_{for_voting}"
        result = self._get_cached_or_calculate(
            cache_key,
            lambda: self._calculate_available_influence_uncached(player_id, for_voting),
        )
        return int(result)

    def get_resource_sources(self, player_id: str) -> ResourceSources:
        """Get resource sources with caching."""
        cache_key = f"resource_sources_{player_id}"
        result = self._get_cached_or_calculate(
            cache_key, lambda: self._get_resource_sources_uncached(player_id)
        )
        assert isinstance(result, ResourceSources)
        return result

    def get_influence_sources(
        self, player_id: str, for_voting: bool = False
    ) -> InfluenceSources:
        """Get influence sources with caching."""
        cache_key = f"influence_sources_{player_id}_{for_voting}"
        result = self._get_cached_or_calculate(
            cache_key,
            lambda: self._get_influence_sources_uncached(player_id, for_voting),
        )
        assert isinstance(result, InfluenceSources)
        return result

    def get_cache_statistics(self) -> CacheStatistics:
        """Get cache performance statistics."""
        return CacheStatistics(
            total_requests=self._cache_stats["total_requests"],
            cache_hits=self._cache_stats["cache_hits"],
            cache_misses=self._cache_stats["cache_misses"],
        )

    def _get_cached_or_calculate(
        self, cache_key: str, calculate_func: Callable[[], Any]
    ) -> Any:
        """Get value from cache or calculate and cache it."""
        self._cache_stats["total_requests"] += 1

        # Check if game state has changed
        current_hash = self._calculate_game_state_hash()
        if current_hash != self._game_state_hash:
            self._invalidate_cache()
            self._game_state_hash = current_hash

        # Check cache
        if cache_key in self._cache:
            self._cache_stats["cache_hits"] += 1
            return self._cache[cache_key]

        # Calculate and cache
        self._cache_stats["cache_misses"] += 1
        result = calculate_func()
        self._cache[cache_key] = result
        return result

    def _calculate_game_state_hash(self) -> int:
        """Calculate a hash of the game state for cache invalidation."""
        # Simple hash based on player count, planet states, and trade goods
        # This is a simplified approach - in practice, you might want more sophisticated tracking
        hash_components = []

        for player in self.game_state.players:
            hash_components.append(f"player_{player.id}_{player.get_trade_goods()}")

            # Include planet states
            planets = self.game_state.get_player_planets(player.id)
            for planet in planets:
                hash_components.append(
                    f"planet_{planet.name}_{planet.is_exhausted()}_{planet.resources}_{planet.influence}"
                )

        return hash(tuple(sorted(hash_components)))

    def _invalidate_cache(self) -> None:
        """Clear the cache when game state changes."""
        self._cache.clear()
        logger.debug("Cache invalidated due to game state change")

    # Uncached versions of the original methods
    def _calculate_available_resources_uncached(self, player_id: str) -> int:
        """Uncached version of calculate_available_resources."""
        return super().calculate_available_resources(player_id)

    def _calculate_available_influence_uncached(
        self, player_id: str, for_voting: bool = False
    ) -> int:
        """Uncached version of calculate_available_influence."""
        return super().calculate_available_influence(player_id, for_voting)

    def _get_resource_sources_uncached(self, player_id: str) -> ResourceSources:
        """Uncached version of get_resource_sources."""
        return super().get_resource_sources(player_id)

    def _get_influence_sources_uncached(
        self, player_id: str, for_voting: bool = False
    ) -> InfluenceSources:
        """Uncached version of get_influence_sources."""
        return super().get_influence_sources(player_id, for_voting)


class LazyResourceSources:
    """Lazy evaluation wrapper for resource sources calculation."""

    def __init__(self, calculate_func: Callable[[], ResourceSources]) -> None:
        """Initialize with calculation function."""
        self._calculate_func = calculate_func
        self._cached_result: ResourceSources | None = None
        self._calculated = False

    def get_sources(self) -> ResourceSources:
        """Get sources, calculating only when first accessed."""
        if not self._calculated:
            self._cached_result = self._calculate_func()
            self._calculated = True
        assert self._cached_result is not None
        return self._cached_result


class LazyInfluenceSources:
    """Lazy evaluation wrapper for influence sources calculation."""

    def __init__(self, calculate_func: Callable[[], InfluenceSources]) -> None:
        """Initialize with calculation function."""
        self._calculate_func = calculate_func
        self._cached_result: InfluenceSources | None = None
        self._calculated = False

    def get_sources(self) -> InfluenceSources:
        """Get sources, calculating only when first accessed."""
        if not self._calculated:
            self._cached_result = self._calculate_func()
            self._calculated = True
        assert self._cached_result is not None
        return self._cached_result


class BatchCostValidator:
    """Batch operations for cost validation to improve performance."""

    def __init__(
        self, resource_manager: ResourceManager, stats_provider: UnitStatsProvider
    ) -> None:
        """Initialize with resource manager and stats provider."""
        self.resource_manager = resource_manager
        self.stats_provider = stats_provider
        self._cost_validator = CostValidator(resource_manager, stats_provider)

    def validate_batch_production_costs(
        self,
        player_id: str,
        production_requests: list[
            tuple[UnitType, int, Faction | None, set[Technology] | None]
        ],
    ) -> list[CostValidationResult]:
        """Validate multiple production costs in a single batch operation.

        Args:
            player_id: The player ID
            production_requests: List of (unit_type, quantity, faction, technologies) tuples

        Returns:
            List of CostValidationResult for each request
        """
        logger.debug(
            f"Batch validating {len(production_requests)} production costs for player {player_id}"
        )

        # Pre-calculate player resources once for all validations
        available_resources = self.resource_manager.calculate_available_resources(
            player_id
        )

        results = []
        for unit_type, quantity, faction, technologies in production_requests:
            try:
                # Calculate production cost
                production_cost = self._cost_validator.get_production_cost(
                    unit_type, quantity, faction, technologies
                )

                # Validate against pre-calculated resources
                required_resources = math.ceil(production_cost.total_cost)
                is_valid = available_resources >= required_resources
                shortfall = max(0, required_resources - available_resources)

                error_message = None
                suggested_spending_plan = None

                if not is_valid:
                    error_message = (
                        f"Insufficient resources for {unit_type.name.lower()} production: "
                        f"need {required_resources}, have {available_resources} (shortfall: {shortfall})"
                    )
                else:
                    # Create suggested spending plan
                    suggested_spending_plan = (
                        self.resource_manager.create_spending_plan(
                            player_id, resource_amount=required_resources
                        )
                    )

                results.append(
                    CostValidationResult(
                        is_valid=is_valid,
                        required_resources=required_resources,
                        available_resources=available_resources,
                        shortfall=shortfall,
                        error_message=error_message,
                        suggested_spending_plan=suggested_spending_plan,
                    )
                )

            except Exception as e:
                # Handle individual validation errors
                results.append(
                    CostValidationResult(
                        is_valid=False,
                        required_resources=0,
                        available_resources=available_resources,
                        shortfall=0,
                        error_message=f"Validation error for {unit_type.name}: {str(e)}",
                        suggested_spending_plan=None,
                    )
                )

        logger.debug(
            f"Batch validation completed: {sum(1 for r in results if r.is_valid)}/{len(results)} valid"
        )
        return results


class BatchResourceManager:
    """Batch operations for resource management to improve performance."""

    def __init__(self, game_state: GameState) -> None:
        """Initialize with game state."""
        self.resource_manager = ResourceManager(game_state)

    def create_batch_spending_plans(
        self,
        player_id: str,
        spending_requests: list[
            tuple[int, int, bool]
        ],  # (resource_amount, influence_amount, for_voting)
    ) -> list[SpendingPlan]:
        """Create multiple spending plans in a batch operation.

        Args:
            player_id: The player ID
            spending_requests: List of (resource_amount, influence_amount, for_voting) tuples

        Returns:
            List of SpendingPlan for each request
        """
        logger.debug(
            f"Batch creating {len(spending_requests)} spending plans for player {player_id}"
        )

        # Pre-calculate resource and influence sources once
        resource_sources = self.resource_manager.get_resource_sources(player_id)
        influence_sources_normal = self.resource_manager.get_influence_sources(
            player_id, for_voting=False
        )
        influence_sources_voting = self.resource_manager.get_influence_sources(
            player_id, for_voting=True
        )

        results = []
        for resource_amount, influence_amount, for_voting in spending_requests:
            try:
                # Use pre-calculated sources
                influence_sources = (
                    influence_sources_voting if for_voting else influence_sources_normal
                )

                # Create spending plans using pre-calculated sources
                resource_spending = self.resource_manager._create_resource_spending(
                    resource_sources, resource_amount
                )
                influence_spending = self.resource_manager._create_influence_spending(
                    influence_sources, influence_amount
                )

                # Check if plan is valid
                is_valid = (
                    resource_spending.total_resources >= resource_amount
                    and influence_spending.total_influence >= influence_amount
                )

                error_message = None
                if not is_valid:
                    errors = []
                    if resource_spending.total_resources < resource_amount:
                        shortfall = resource_amount - resource_spending.total_resources
                        errors.append(
                            f"Insufficient resources: need {resource_amount}, have {resource_spending.total_resources} (shortfall: {shortfall})"
                        )
                    if influence_spending.total_influence < influence_amount:
                        shortfall = (
                            influence_amount - influence_spending.total_influence
                        )
                        voting_context = " for voting" if for_voting else ""
                        errors.append(
                            f"Insufficient influence{voting_context}: need {influence_amount}, have {influence_spending.total_influence} (shortfall: {shortfall})"
                        )
                    error_message = "; ".join(errors)

                results.append(
                    SpendingPlan(
                        player_id=player_id,
                        resource_spending=resource_spending,
                        influence_spending=influence_spending,
                        total_resource_cost=resource_amount,
                        total_influence_cost=influence_amount,
                        is_valid=is_valid,
                        error_message=error_message,
                    )
                )

            except Exception as e:
                # Handle individual plan creation errors
                results.append(
                    SpendingPlan(
                        player_id=player_id,
                        resource_spending=ResourceSpending({}, 0, 0),
                        influence_spending=InfluenceSpending({}, 0, 0),
                        total_resource_cost=resource_amount,
                        total_influence_cost=influence_amount,
                        is_valid=False,
                        error_message=f"Plan creation error: {str(e)}",
                    )
                )

        logger.debug(
            f"Batch spending plan creation completed: {sum(1 for p in results if p.is_valid)}/{len(results)} valid"
        )
        return results

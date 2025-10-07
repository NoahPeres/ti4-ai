"""Production system for TI4 Rule 67: PRODUCING UNITS.

This module implements Rule 67: PRODUCING UNITS mechanics according to the TI4 LRR.
Handles unit production, cost validation, reinforcement limits, and production restrictions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

from .constants import Faction, Technology, UnitType
from .unit_stats import UnitStatsProvider

if TYPE_CHECKING:
    from .blockade import BlockadeManager
    from .game_state import GameState
    from .planet import Planet
    from .resource_management import (
        CostValidationResult,
        CostValidator,
        ProductionCost,
        ResourceManager,
        SpendingPlan,
        SpendingResult,
    )
    from .system import System
    from .unit import Unit


class ProductionLocation(Protocol):
    """Protocol for production placement locations."""

    def can_place_unit(self, unit_type: UnitType, quantity: int) -> bool:
        """Check if units can be placed at this location."""
        ...

    def place_unit(self, unit_type: UnitType, quantity: int) -> bool:
        """Place units at this location."""
        ...

    def get_placement_error(self) -> str:
        """Get error message for placement failure."""
        ...


@dataclass(frozen=True)
class ProductionValidationResult:
    """Result of production validation including cost, reinforcement, and placement checks."""

    is_valid: bool
    production_cost: ProductionCost | None = None
    cost_validation: CostValidationResult | None = None
    error_message: str | None = None


@dataclass(frozen=True)
class ProductionExecutionResult:
    """Result of production execution including cost payment and unit placement."""

    success: bool
    units_placed: int = 0
    spending_result: SpendingResult | None = None
    error_message: str | None = None


class ProductionManager:
    """Manages unit production mechanics according to Rule 67.

    Handles:
    - Unit cost validation (Rule 67.1)
    - Dual unit production (Rule 67.2)
    - Tactical action production (Rule 67.3)
    - Non-tactical production (Rule 67.4)
    - Reinforcement limits (Rule 67.5)
    - Ship production restrictions (Rule 67.6)

    Enhanced with integrated cost validation and execution when dependencies provided.
    """

    def __init__(
        self,
        resource_manager: ResourceManager | None = None,
        cost_validator: CostValidator | None = None,
    ) -> None:
        """Initialize the production manager.

        Args:
            resource_manager: Optional ResourceManager for enhanced cost integration
            cost_validator: Optional CostValidator for enhanced cost validation
        """
        self._stats_provider = UnitStatsProvider()
        self.resource_manager = resource_manager
        self.cost_validator = cost_validator

    def can_afford_unit(self, unit_type: UnitType, available_resources: int) -> bool:
        """Check if a player can afford to produce a unit.

        Args:
            unit_type: The type of unit to produce
            available_resources: The resources available to the player

        Returns:
            True if the player can afford the unit, False otherwise

        LRR Reference: Rule 67.1 - Must spend resources equal to or greater than cost
        """
        unit_stats = self._stats_provider.get_unit_stats(unit_type)
        unit_cost = unit_stats.cost

        # Rule 67.1: Must spend resources equal to or greater than cost
        return available_resources >= unit_cost

    def get_units_produced_for_cost(self, unit_type: UnitType) -> int:
        """Get the number of units produced for the cost of one unit.

        Args:
            unit_type: The type of unit to check

        Returns:
            Number of units produced for the cost (2 for fighters/infantry, 1 for others)

        LRR Reference: Rule 67.2 - Cost with two icons (fighters/infantry) produces two units
        """
        # Rule 67.2: Fighters and infantry produce two units for their cost
        if unit_type in {UnitType.FIGHTER, UnitType.INFANTRY}:
            return 2
        else:
            return 1

    def can_produce_ships_in_system(self, system: System, player_id: str) -> bool:
        """Check if a player can produce ships in a system.

        Args:
            system: The system to check for ship production
            player_id: The player attempting to produce ships

        Returns:
            True if ships can be produced, False if restricted by enemy ships

        LRR Reference: Rule 67.6 - Cannot produce ships in system containing other players' ships
        """
        # Rule 67.6: Cannot produce ships in system containing other players' ships
        for unit in system.space_units:
            if unit.owner != player_id and self._is_ship(unit):
                return False
        return True

    def _is_ship(self, unit: Unit) -> bool:
        """Check if a unit is a ship.

        Args:
            unit: The unit to check

        Returns:
            True if unit is a ship
        """
        ship_types = {
            UnitType.CARRIER,
            UnitType.CRUISER,
            UnitType.DESTROYER,
            UnitType.DREADNOUGHT,
            UnitType.FIGHTER,
            UnitType.FLAGSHIP,
            UnitType.WAR_SUN,
        }
        return unit.unit_type in ship_types

    def can_place_pds_on_planet(
        self, planet: Planet, player_id: str, game_state: GameState
    ) -> bool:
        """Check if a PDS unit can be placed on a planet.

        Args:
            planet: The planet to place the PDS on
            player_id: The player attempting to place the PDS
            game_state: Current game state (for law effect checking)

        Returns:
            True if PDS can be placed, False if restricted by laws or rules
        """
        # Check for law effects that might affect PDS placement
        law_effects = game_state.get_law_effects_for_action(
            "pds_placement_limit", player_id
        )

        # Check for Homeland Defense Act law
        for law_effect in law_effects:
            if law_effect.agenda_card.get_name() == "Homeland Defense Act":
                # Homeland Defense Act allows unlimited PDS on planets
                return True

        # Without the law, normal PDS placement rules apply (Rule 67 - Structure limits)
        # Check existing PDS count on the planet (maximum 2 PDS per planet)
        existing_pds_count = sum(
            1
            for unit in planet.units
            if unit.unit_type == UnitType.PDS and unit.owner == player_id
        )

        if existing_pds_count >= 2:
            return False  # Cannot place more than 2 PDS per planet

        return True

    def can_produce_from_reinforcements(
        self, unit_type: UnitType, available_reinforcements: int, units_to_produce: int
    ) -> bool:
        """Check if units can be produced from available reinforcements.

        Args:
            unit_type: The type of unit to produce
            available_reinforcements: Number of units available in reinforcements
            units_to_produce: Number of production actions (not final unit count)

        Returns:
            True if sufficient reinforcements are available

        LRR Reference: Rule 67.5 - Players limited by units in reinforcements
        """
        # Calculate total units that would be produced
        units_per_production = self.get_units_produced_for_cost(unit_type)
        total_units_needed = units_to_produce * units_per_production

        # Rule 67.5: Must have sufficient units in reinforcements
        return available_reinforcements >= total_units_needed

    def can_produce_ships_with_blockade_check(
        self, unit: Unit, blockade_manager: BlockadeManager
    ) -> bool:
        """Check if a unit can produce ships considering blockade restrictions.

        Args:
            unit: The production unit to check
            blockade_manager: The blockade manager for checking restrictions

        Returns:
            True if ships can be produced, False if restricted by blockade

        LRR Reference: Rule 67.6 + Rule 14.1 - Production restrictions with blockade integration
        """
        # Rule 67.6 + Rule 14.1: Blockaded units cannot produce ships
        return blockade_manager.can_produce_ships(unit)

    def validate_production(
        self,
        player_id: str,
        unit_type: UnitType,
        quantity: int,
        available_reinforcements: int,
        faction: Faction | None = None,
        technologies: set[Technology] | None = None,
    ) -> ProductionValidationResult:
        """Validate production including cost, reinforcement, and placement rules.

        Args:
            player_id: The player attempting production
            unit_type: The type of unit to produce
            quantity: Number of units requested
            available_reinforcements: Number of units available in reinforcements
            faction: Optional faction for cost modifiers
            technologies: Optional technologies for cost modifiers

        Returns:
            ProductionValidationResult with validation details

        Raises:
            ValueError: If ResourceManager and CostValidator not provided
        """
        if not self.resource_manager or not self.cost_validator:
            raise ValueError(
                "ResourceManager and CostValidator required for enhanced production validation"
            )

        if quantity <= 0:
            return ProductionValidationResult(
                is_valid=False, error_message="Quantity must be a positive integer"
            )

        try:
            # Get production cost with all modifiers
            production_cost = self.cost_validator.get_production_cost(
                unit_type, quantity, faction, technologies
            )

            # Validate cost and reinforcements
            cost_validation = (
                self.cost_validator.validate_production_cost_with_reinforcements(
                    player_id, production_cost, available_reinforcements
                )
            )

            return ProductionValidationResult(
                is_valid=cost_validation.is_valid,
                production_cost=production_cost,
                cost_validation=cost_validation,
                error_message=cost_validation.error_message,
            )

        except Exception as e:
            return ProductionValidationResult(
                is_valid=False,
                error_message=f"Production validation failed: {str(e)}",
            )

    def execute_production(
        self,
        player_id: str,
        unit_type: UnitType,
        quantity: int,
        spending_plan: SpendingPlan,
        placement_location: ProductionLocation,
    ) -> ProductionExecutionResult:
        """Execute production with atomic cost payment and unit placement.

        Args:
            player_id: The player executing production
            unit_type: The type of unit to produce
            quantity: Number of units requested
            spending_plan: The spending plan for cost payment
            placement_location: Location where units will be placed

        Returns:
            ProductionExecutionResult with execution details

        Raises:
            ValueError: If ResourceManager and CostValidator not provided
        """
        if not self.resource_manager or not self.cost_validator:
            raise ValueError(
                "ResourceManager and CostValidator required for enhanced production execution"
            )

        if quantity <= 0:
            return ProductionExecutionResult(
                success=False, units_placed=0, error_message="Quantity must be positive"
            )

        try:
            # Compute units and pre-validate placement before spending
            units_to_place = self._calculate_units_to_place(unit_type, quantity)
            if not placement_location.can_place_unit(unit_type, units_to_place):
                return ProductionExecutionResult(
                    success=False,
                    units_placed=0,
                    error_message=placement_location.get_placement_error(),
                )

            # Execute spending plan (pay costs)
            spending_result = self.resource_manager.execute_spending_plan(spending_plan)
            if not spending_result.success:
                return ProductionExecutionResult(
                    success=False,
                    units_placed=0,
                    spending_result=spending_result,
                    error_message=spending_result.error_message,
                )

            # Place units
            placement_success = placement_location.place_unit(unit_type, units_to_place)

            if not placement_success:
                # Rollback spending if placement fails
                self._rollback_spending(player_id, spending_result)
                return ProductionExecutionResult(
                    success=False,
                    units_placed=0,
                    error_message="Unit placement failed",
                )

            # Success!
            return ProductionExecutionResult(
                success=True,
                units_placed=units_to_place,
                spending_result=spending_result,
            )

        except Exception as e:
            return ProductionExecutionResult(
                success=False,
                units_placed=0,
                error_message=f"Production execution failed: {str(e)}",
            )

    def _calculate_units_to_place(self, unit_type: UnitType, quantity: int) -> int:
        """Calculate the actual number of units to place considering dual production."""
        # For dual production units, if quantity==2, produce 2 units for the cost of 1.
        # If quantity==1, produce 1 unit.
        if self._is_dual_production_unit(unit_type) and quantity == 2:
            return 2  # Dual production: 2 units for cost of 1
        else:
            return quantity  # Normal production: 1 unit per cost

    def _is_dual_production_unit(self, unit_type: UnitType) -> bool:
        """Check if unit type supports dual production."""
        return unit_type in {UnitType.FIGHTER, UnitType.INFANTRY}

    def _rollback_spending(
        self, player_id: str, spending_result: SpendingResult
    ) -> None:
        """Rollback spending by readying planets and restoring trade goods."""
        if self.resource_manager:
            self.resource_manager.rollback_spending(player_id, spending_result)

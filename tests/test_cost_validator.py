"""Tests for CostValidator unit cost calculations.

Tests the CostValidator class for Rule 26: COST calculations with faction and technology modifiers.
"""

from src.ti4.core.constants import Faction, Technology, UnitType
from src.ti4.core.game_state import GameState
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.resource_management import (
    CostValidator,
    ProductionCost,
    ResourceManager,
)
from src.ti4.core.unit_stats import UnitStatsProvider


class TestCostValidatorBasics:
    """Test basic CostValidator functionality."""

    def test_cost_validator_creation(self) -> None:
        """Test that CostValidator can be created with required dependencies."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()

        # Create CostValidator - this should fail initially
        cost_validator = CostValidator(resource_manager, stats_provider)

        assert cost_validator is not None

    def test_get_unit_cost_basic(self) -> None:
        """Test getting basic unit cost without modifiers."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test basic unit cost
        cruiser_cost = cost_validator.get_unit_cost(UnitType.CRUISER)
        assert cruiser_cost == 2.0  # Base cruiser cost

        fighter_cost = cost_validator.get_unit_cost(UnitType.FIGHTER)
        assert fighter_cost == 0.5  # Base fighter cost

    def test_get_unit_cost_with_faction_modifier(self) -> None:
        """Test getting unit cost with faction modifiers applied."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test with faction modifier (this will need faction-specific cost modifiers)
        cruiser_cost = cost_validator.get_unit_cost(
            UnitType.CRUISER, faction=Faction.SOL
        )
        # For now, should be same as base cost since no modifiers registered
        assert cruiser_cost == 2.0

    def test_get_unit_cost_with_technology_modifier(self) -> None:
        """Test getting unit cost with technology modifiers applied."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test with technology modifier
        technologies = {Technology.CRUISER_II}
        cruiser_cost = cost_validator.get_unit_cost(
            UnitType.CRUISER_II, technologies=technologies
        )
        # Should be base cost of cruiser_ii (which should be 2.0)
        assert cruiser_cost == 2.0


class TestProductionCostCalculation:
    """Test production cost calculations including dual production."""

    def test_get_production_cost_single_unit(self) -> None:
        """Test production cost calculation for single unit."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test single cruiser production
        production_cost = cost_validator.get_production_cost(UnitType.CRUISER, 1)

        assert isinstance(production_cost, ProductionCost)
        assert production_cost.unit_type == UnitType.CRUISER
        assert production_cost.base_cost == 2.0
        assert production_cost.modified_cost == 2.0
        assert production_cost.quantity_requested == 1
        assert production_cost.units_produced == 1
        assert production_cost.total_cost == 2.0
        assert production_cost.is_dual_production is False

    def test_get_production_cost_dual_production_fighter(self) -> None:
        """Test production cost calculation for dual production fighters."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test dual fighter production (2 fighters for cost of 1)
        production_cost = cost_validator.get_production_cost(UnitType.FIGHTER, 2)

        assert production_cost.unit_type == UnitType.FIGHTER
        assert production_cost.base_cost == 0.5
        assert production_cost.quantity_requested == 2
        assert production_cost.units_produced == 2
        assert production_cost.total_cost == 0.5  # Cost of 1 fighter for 2 units
        assert production_cost.is_dual_production is True

    def test_get_production_cost_dual_production_infantry(self) -> None:
        """Test production cost calculation for dual production infantry."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test dual infantry production (2 infantry for cost of 1)
        production_cost = cost_validator.get_production_cost(UnitType.INFANTRY, 2)

        assert production_cost.unit_type == UnitType.INFANTRY
        assert production_cost.base_cost == 0.5
        assert production_cost.quantity_requested == 2
        assert production_cost.units_produced == 2
        assert production_cost.total_cost == 0.5  # Cost of 1 infantry for 2 units
        assert production_cost.is_dual_production is True

    def test_get_production_cost_single_from_dual_production(self) -> None:
        """Test production cost when producing only 1 unit from dual production."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test single fighter from dual production (still costs full amount per Rule 26.2)
        production_cost = cost_validator.get_production_cost(UnitType.FIGHTER, 1)

        assert production_cost.unit_type == UnitType.FIGHTER
        assert production_cost.quantity_requested == 1
        assert production_cost.units_produced == 1
        assert production_cost.total_cost == 0.5  # Still pay full cost
        assert production_cost.is_dual_production is False  # Not dual since only 1 unit


class TestStructureCostValidation:
    """Test structure cost validation for Construction strategy card."""

    def test_can_produce_without_cost_space_dock(self) -> None:
        """Test that space docks can be produced without cost via Construction."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Space docks have cost=0 and should be producible without cost
        can_produce = cost_validator.can_produce_without_cost(UnitType.SPACE_DOCK)
        assert can_produce is True

    def test_can_produce_without_cost_pds(self) -> None:
        """Test that PDS can be produced without cost via Construction."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # PDS should be producible without cost (structures)
        can_produce = cost_validator.can_produce_without_cost(UnitType.PDS)
        assert can_produce is True

    def test_cannot_produce_ships_without_cost(self) -> None:
        """Test that ships cannot be produced without cost."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Ships should not be producible without cost
        can_produce = cost_validator.can_produce_without_cost(UnitType.CRUISER)
        assert can_produce is False

        can_produce = cost_validator.can_produce_without_cost(UnitType.FIGHTER)
        assert can_produce is False


class TestCostValidationIntegration:
    """Test cost validation integration with ResourceManager."""

    def test_validate_production_cost_sufficient_resources(self) -> None:
        """Test production cost validation when player has sufficient resources."""
        # Create game state with player and planets
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planet with resources
        jord = Planet("Jord", resources=4, influence=2)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, jord)

        # Give player some trade goods
        player.gain_trade_goods(2)

        # Create dependencies
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Create production cost for cruiser (cost 2)
        production_cost = cost_validator.get_production_cost(UnitType.CRUISER, 1)

        # Validate cost - should be valid
        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )

        assert validation_result.is_valid is True
        assert validation_result.required_resources == 2
        assert (
            validation_result.available_resources == 6
        )  # 4 (planet) + 2 (trade goods)
        assert validation_result.shortfall == 0
        assert validation_result.error_message is None
        assert validation_result.suggested_spending_plan is not None

    def test_validate_production_cost_insufficient_resources(self) -> None:
        """Test production cost validation when player has insufficient resources."""
        # Create game state with player and no resources
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Set up game state (no planets, no trade goods)
        game_state = game_state.add_player(player)

        # Create dependencies
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Create production cost for cruiser (cost 2)
        production_cost = cost_validator.get_production_cost(UnitType.CRUISER, 1)

        # Validate cost - should be invalid
        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )

        assert validation_result.is_valid is False
        assert validation_result.required_resources == 2
        assert validation_result.available_resources == 0
        assert validation_result.shortfall == 2
        assert "Insufficient resources" in validation_result.error_message
        assert validation_result.suggested_spending_plan is None

    def test_validate_production_cost_fractional_cost(self) -> None:
        """Test production cost validation with fractional costs (fighters)."""
        # Create game state with player and minimal resources
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Give player 1 trade good (should be enough for 1 fighter at 0.5 cost)
        player.gain_trade_goods(1)

        # Set up game state
        game_state = game_state.add_player(player)

        # Create dependencies
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Create production cost for fighter (cost 0.5)
        production_cost = cost_validator.get_production_cost(UnitType.FIGHTER, 1)

        # Validate cost - should be valid (1 trade good >= 0.5 cost)
        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )

        assert validation_result.is_valid is True
        assert validation_result.required_resources == 1  # ceil(0.5) = 1
        assert validation_result.available_resources == 1
        assert validation_result.shortfall == 0


class TestDualProductionEdgeCases:
    """Test edge cases for dual production rules."""

    def test_get_production_cost_multiple_dual_units(self) -> None:
        """Test production cost for multiple dual production units (4 fighters)."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test 4 fighters (should be 2 dual productions)
        production_cost = cost_validator.get_production_cost(UnitType.FIGHTER, 4)

        assert production_cost.unit_type == UnitType.FIGHTER
        assert production_cost.quantity_requested == 4
        assert production_cost.units_produced == 4
        assert (
            production_cost.total_cost == 2.0
        )  # 4 * 0.5 = 2.0 (not dual production for 4)
        assert (
            production_cost.is_dual_production is False
        )  # Only exactly 2 units trigger dual production

    def test_get_production_cost_three_dual_units(self) -> None:
        """Test production cost for odd number of dual production units (3 fighters)."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test 3 fighters (should not be dual production)
        production_cost = cost_validator.get_production_cost(UnitType.FIGHTER, 3)

        assert production_cost.unit_type == UnitType.FIGHTER
        assert production_cost.quantity_requested == 3
        assert production_cost.units_produced == 3
        assert production_cost.total_cost == 1.5  # 3 * 0.5 = 1.5
        assert production_cost.is_dual_production is False

    def test_get_production_cost_zero_units(self) -> None:
        """Test production cost for zero units."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test 0 fighters
        production_cost = cost_validator.get_production_cost(UnitType.FIGHTER, 0)

        assert production_cost.unit_type == UnitType.FIGHTER
        assert production_cost.quantity_requested == 0
        assert production_cost.units_produced == 0
        assert production_cost.total_cost == 0.0
        assert production_cost.is_dual_production is False

    def test_get_cost_per_unit_calculation(self) -> None:
        """Test the get_cost_per_unit method on ProductionCost."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test dual production cost per unit
        production_cost = cost_validator.get_production_cost(UnitType.FIGHTER, 2)
        cost_per_unit = production_cost.get_cost_per_unit()

        assert cost_per_unit == 0.25  # 0.5 total cost / 2 units = 0.25 per unit

        # Test single unit cost per unit
        production_cost = cost_validator.get_production_cost(UnitType.CRUISER, 1)
        cost_per_unit = production_cost.get_cost_per_unit()

        assert cost_per_unit == 2.0  # 2.0 total cost / 1 unit = 2.0 per unit

        # Test zero units (should return 0)
        production_cost = cost_validator.get_production_cost(UnitType.FIGHTER, 0)
        cost_per_unit = production_cost.get_cost_per_unit()

        assert cost_per_unit == 0.0


class TestDualProductionCostValidation:
    """Test dual production cost validation with reinforcement checks."""

    def test_validate_dual_production_sufficient_reinforcements(self) -> None:
        """Test dual production validation when sufficient reinforcements are available."""
        # Create game state with player and resources
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planet with resources
        jord = Planet("Jord", resources=4, influence=2)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, jord)

        # Create dependencies
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Create dual production cost for 2 fighters (produces 2, needs 2 reinforcements)
        production_cost = cost_validator.get_production_cost(UnitType.FIGHTER, 2)

        # Validate with reinforcement check - player has 3 fighters available
        validation_result = cost_validator.validate_production_cost_with_reinforcements(
            player.id, production_cost, available_reinforcements=3
        )

        assert validation_result.is_valid is True
        assert validation_result.reinforcement_shortfall == 0
        assert (
            "reinforcement" not in validation_result.error_message.lower()
            if validation_result.error_message
            else True
        )

    def test_validate_dual_production_insufficient_reinforcements(self) -> None:
        """Test dual production validation when insufficient reinforcements are available."""
        # Create game state with player and resources
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planet with resources
        jord = Planet("Jord", resources=4, influence=2)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, jord)

        # Create dependencies
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Create dual production cost for 2 fighters (produces 2, needs 2 reinforcements)
        production_cost = cost_validator.get_production_cost(UnitType.FIGHTER, 2)

        # Validate with reinforcement check - player has only 1 fighter available
        validation_result = cost_validator.validate_production_cost_with_reinforcements(
            player.id, production_cost, available_reinforcements=1
        )

        assert validation_result.is_valid is False
        assert validation_result.reinforcement_shortfall == 1
        assert "reinforcement" in validation_result.error_message.lower()

    def test_validate_single_unit_from_dual_production_cost(self) -> None:
        """Test that producing 1 unit from dual production still requires full cost (Rule 26.2)."""
        # Create game state with player and minimal resources
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Give player exactly 1 trade good (should be enough for 1 fighter at 0.5 cost)
        player.gain_trade_goods(1)

        # Set up game state
        game_state = game_state.add_player(player)

        # Create dependencies
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Create production cost for 1 fighter (still costs 0.5 per Rule 26.2)
        production_cost = cost_validator.get_production_cost(UnitType.FIGHTER, 1)

        # Validate cost - should be valid
        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )

        assert validation_result.is_valid is True
        assert production_cost.total_cost == 0.5  # Still pay full cost for 1 unit
        assert production_cost.units_produced == 1  # Only produce 1 unit
        assert production_cost.is_dual_production is False  # Not dual production

    def test_validate_production_cost_with_reinforcements_method_exists(self) -> None:
        """Test that the validate_production_cost_with_reinforcements method exists."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Check that the method exists
        assert hasattr(cost_validator, "validate_production_cost_with_reinforcements")


class TestReinforcementValidationResult:
    """Test the enhanced validation result with reinforcement information."""

    def test_cost_validation_result_has_reinforcement_fields(self) -> None:
        """Test that CostValidationResult includes reinforcement validation fields."""
        from src.ti4.core.resource_management import CostValidationResult

        # Create a validation result with reinforcement information
        result = CostValidationResult(
            is_valid=False,
            required_resources=2,
            available_resources=2,
            shortfall=0,
            reinforcement_shortfall=1,
            error_message="Insufficient reinforcements: need 2, have 1",
        )

        assert hasattr(result, "reinforcement_shortfall")
        assert result.reinforcement_shortfall == 1
        assert "reinforcement" in result.error_message.lower()


class TestProductionManagerIntegration:
    """Test integration with existing ProductionManager dual production logic."""

    def test_cost_validator_integrates_with_production_manager_logic(self) -> None:
        """Test that CostValidator uses same dual production logic as ProductionManager."""
        from src.ti4.core.production import ProductionManager

        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)
        production_manager = ProductionManager()

        # Test that both systems agree on dual production units
        for unit_type in [UnitType.FIGHTER, UnitType.INFANTRY]:
            # ProductionManager logic
            pm_units_produced = production_manager.get_units_produced_for_cost(
                unit_type
            )

            # CostValidator logic for dual production (2 units requested)
            production_cost = cost_validator.get_production_cost(unit_type, 2)

            assert pm_units_produced == 2  # ProductionManager says 2 units for cost
            assert (
                production_cost.is_dual_production is True
            )  # CostValidator recognizes dual production
            assert production_cost.units_produced == 2  # CostValidator produces 2 units

        # Test non-dual production units
        for unit_type in [UnitType.CRUISER, UnitType.DESTROYER]:
            pm_units_produced = production_manager.get_units_produced_for_cost(
                unit_type
            )
            production_cost = cost_validator.get_production_cost(unit_type, 1)

            assert pm_units_produced == 1  # ProductionManager says 1 unit for cost
            assert (
                production_cost.is_dual_production is False
            )  # CostValidator recognizes normal production
            assert production_cost.units_produced == 1  # CostValidator produces 1 unit

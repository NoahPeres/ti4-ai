"""Tests for CostValidator technology and faction cost modifiers.

Tests the CostValidator class for Rule 26: COST calculations with technology and faction modifiers.
Covers Requirements 8.1, 8.2, 8.3, 8.4, 8.5.
"""

from src.ti4.core.constants import Faction, Technology, UnitType
from src.ti4.core.game_state import GameState
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.resource_management import (
    CostValidator,
    ResourceManager,
)
from src.ti4.core.unit_stats import UnitStats, UnitStatsProvider


class TestTechnologyCostModifiers:
    """Test technology-based cost modifications (Requirement 8.1, 8.2)."""

    def test_technology_cost_reduction(self) -> None:
        """Test that technology can reduce unit costs."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()

        # Register a technology that reduces cruiser cost by 1
        stats_provider.register_technology_modifier(
            Technology.CRUISER_II,
            UnitType.CRUISER,
            UnitStats(cost=-1),  # Reduce cost by 1
        )

        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test base cost without technology
        base_cost = cost_validator.get_unit_cost(UnitType.CRUISER)
        assert base_cost == 2.0

        # Test cost with technology modifier
        modified_cost = cost_validator.get_unit_cost(
            UnitType.CRUISER, technologies={Technology.CRUISER_II}
        )
        assert modified_cost == 1.0  # 2.0 - 1.0 = 1.0

    def test_technology_cost_increase(self) -> None:
        """Test that technology can increase unit costs."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()

        # Register a technology that increases fighter cost by 0.5
        stats_provider.register_technology_modifier(
            Technology.FIGHTER_II,
            UnitType.FIGHTER,
            UnitStats(cost=0.5),  # Increase cost by 0.5
        )

        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test base cost without technology
        base_cost = cost_validator.get_unit_cost(UnitType.FIGHTER)
        assert base_cost == 0.5

        # Test cost with technology modifier
        modified_cost = cost_validator.get_unit_cost(
            UnitType.FIGHTER, technologies={Technology.FIGHTER_II}
        )
        assert modified_cost == 1.0  # 0.5 + 0.5 = 1.0

    def test_multiple_technology_modifiers(self) -> None:
        """Test that multiple technologies can modify the same unit cost."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()

        # Register multiple technologies that affect cruiser cost
        stats_provider.register_technology_modifier(
            Technology.CRUISER_II,
            UnitType.CRUISER,
            UnitStats(cost=-0.5),  # Reduce cost by 0.5
        )
        stats_provider.register_technology_modifier(
            Technology.GRAVITY_DRIVE,
            UnitType.CRUISER,
            UnitStats(cost=-0.5),  # Reduce cost by another 0.5
        )

        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test cost with both technologies
        modified_cost = cost_validator.get_unit_cost(
            UnitType.CRUISER,
            technologies={Technology.CRUISER_II, Technology.GRAVITY_DRIVE},
        )
        assert modified_cost == 1.0  # 2.0 - 0.5 - 0.5 = 1.0

    def test_technology_modifier_stacking(self) -> None:
        """Test that technology modifiers stack correctly (Requirement 8.3)."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()

        # Register technologies with different cost modifications
        stats_provider.register_technology_modifier(
            Technology.CRUISER_II,
            UnitType.CRUISER,
            UnitStats(cost=-1),  # Reduce by 1
        )
        stats_provider.register_technology_modifier(
            Technology.GRAVITY_DRIVE,
            UnitType.CRUISER,
            UnitStats(cost=0.5),  # Increase by 0.5
        )

        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test stacking: 2.0 - 1.0 + 0.5 = 1.5
        modified_cost = cost_validator.get_unit_cost(
            UnitType.CRUISER,
            technologies={Technology.CRUISER_II, Technology.GRAVITY_DRIVE},
        )
        assert modified_cost == 1.5


class TestFactionCostModifiers:
    """Test faction-specific cost modifications (Requirement 8.1, 8.2)."""

    def test_faction_cost_reduction(self) -> None:
        """Test that faction abilities can reduce unit costs."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()

        # Register a faction modifier that reduces fighter cost
        stats_provider.register_faction_modifier(
            Faction.SOL,
            UnitType.FIGHTER,
            UnitStats(cost=-0.25),  # Reduce fighter cost by 0.25
        )

        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test base cost without faction
        base_cost = cost_validator.get_unit_cost(UnitType.FIGHTER)
        assert base_cost == 0.5

        # Test cost with faction modifier
        modified_cost = cost_validator.get_unit_cost(
            UnitType.FIGHTER, faction=Faction.SOL
        )
        assert modified_cost == 0.25  # 0.5 - 0.25 = 0.25

    def test_faction_cost_increase(self) -> None:
        """Test that faction abilities can increase unit costs."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()

        # Register a faction modifier that increases dreadnought cost
        stats_provider.register_faction_modifier(
            Faction.HACAN,
            UnitType.DREADNOUGHT,
            UnitStats(cost=1),  # Increase dreadnought cost by 1
        )

        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test base cost without faction
        base_cost = cost_validator.get_unit_cost(UnitType.DREADNOUGHT)
        assert base_cost == 4.0

        # Test cost with faction modifier
        modified_cost = cost_validator.get_unit_cost(
            UnitType.DREADNOUGHT, faction=Faction.HACAN
        )
        assert modified_cost == 5.0  # 4.0 + 1.0 = 5.0

    def test_faction_specific_modifiers(self) -> None:
        """Test that faction modifiers only apply to the correct faction."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()

        # Register faction-specific modifier for Sol
        stats_provider.register_faction_modifier(
            Faction.SOL,
            UnitType.INFANTRY,
            UnitStats(cost=-0.25),  # Sol gets cheaper infantry
        )

        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test Sol faction gets the modifier
        sol_cost = cost_validator.get_unit_cost(UnitType.INFANTRY, faction=Faction.SOL)
        assert sol_cost == 0.25  # 0.5 - 0.25 = 0.25

        # Test other factions don't get the modifier
        hacan_cost = cost_validator.get_unit_cost(
            UnitType.INFANTRY, faction=Faction.HACAN
        )
        assert hacan_cost == 0.5  # Base cost, no modifier


class TestCombinedModifiers:
    """Test combined faction and technology modifiers (Requirement 8.3)."""

    def test_faction_and_technology_stacking(self) -> None:
        """Test that faction and technology modifiers stack correctly."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()

        # Register faction modifier
        stats_provider.register_faction_modifier(
            Faction.SOL,
            UnitType.CRUISER,
            UnitStats(cost=-0.5),  # Sol gets cheaper cruisers
        )

        # Register technology modifier
        stats_provider.register_technology_modifier(
            Technology.CRUISER_II,
            UnitType.CRUISER,
            UnitStats(cost=-1),  # Technology reduces cost further
        )

        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test combined modifiers: 2.0 - 0.5 - 1.0 = 0.5
        combined_cost = cost_validator.get_unit_cost(
            UnitType.CRUISER, faction=Faction.SOL, technologies={Technology.CRUISER_II}
        )
        assert combined_cost == 0.5

    def test_modifier_application_order(self) -> None:
        """Test that modifier application order doesn't affect final result."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()

        # Register modifiers in different orders
        stats_provider.register_faction_modifier(
            Faction.HACAN,
            UnitType.DESTROYER,
            UnitStats(cost=0.5),  # Increase by 0.5
        )
        stats_provider.register_technology_modifier(
            Technology.DESTROYER_II,
            UnitType.DESTROYER,
            UnitStats(cost=-0.25),  # Decrease by 0.25
        )

        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test final cost: 1.0 + 0.5 - 0.25 = 1.25
        final_cost = cost_validator.get_unit_cost(
            UnitType.DESTROYER,
            faction=Faction.HACAN,
            technologies={Technology.DESTROYER_II},
        )
        assert final_cost == 1.25


class TestNegativeCostPrevention:
    """Test negative cost prevention (Requirement 8.4, 8.5)."""

    def test_negative_cost_prevention(self) -> None:
        """Test that costs cannot go below zero."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()

        # Register modifiers that would make cost negative
        stats_provider.register_faction_modifier(
            Faction.SOL,
            UnitType.FIGHTER,
            UnitStats(cost=-1),  # Reduce by more than base cost
        )

        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test that cost doesn't go below zero
        modified_cost = cost_validator.get_unit_cost(
            UnitType.FIGHTER, faction=Faction.SOL
        )
        assert modified_cost == 0.0  # Should be 0, not -0.5

    def test_multiple_negative_modifiers(self) -> None:
        """Test negative cost prevention with multiple large reductions."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()

        # Register multiple large negative modifiers
        stats_provider.register_faction_modifier(
            Faction.SOL,
            UnitType.INFANTRY,
            UnitStats(cost=-2),  # Large reduction
        )
        stats_provider.register_technology_modifier(
            Technology.SPEC_OPS_II,
            UnitType.INFANTRY,
            UnitStats(cost=-3),  # Another large reduction
        )

        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test that cost doesn't go below zero
        modified_cost = cost_validator.get_unit_cost(
            UnitType.INFANTRY,
            faction=Faction.SOL,
            technologies={Technology.SPEC_OPS_II},
        )
        assert modified_cost == 0.0  # Should be 0, not negative

    def test_zero_cost_units_remain_zero(self) -> None:
        """Test that zero-cost units remain zero with modifiers."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()

        # Register modifier for zero-cost unit (Space Dock)
        stats_provider.register_faction_modifier(
            Faction.ARBOREC,
            UnitType.SPACE_DOCK,
            UnitStats(cost=1),  # Try to increase zero-cost unit
        )

        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test that space dock cost can be modified from zero
        modified_cost = cost_validator.get_unit_cost(
            UnitType.SPACE_DOCK, faction=Faction.ARBOREC
        )
        assert modified_cost == 1.0  # 0 + 1 = 1


class TestProductionCostWithModifiers:
    """Test production cost calculations with modifiers."""

    def test_production_cost_with_technology_modifier(self) -> None:
        """Test production cost calculation includes technology modifiers."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()

        # Register technology modifier
        stats_provider.register_technology_modifier(
            Technology.CRUISER_II,
            UnitType.CRUISER,
            UnitStats(cost=-0.5),  # Reduce cruiser cost
        )

        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test production cost with modifier
        production_cost = cost_validator.get_production_cost(
            UnitType.CRUISER, 1, technologies={Technology.CRUISER_II}
        )

        assert production_cost.base_cost == 2.0  # Original base cost
        assert production_cost.modified_cost == 1.5  # 2.0 - 0.5 = 1.5
        assert production_cost.total_cost == 1.5  # 1 unit * 1.5 = 1.5

    def test_production_cost_with_faction_modifier(self) -> None:
        """Test production cost calculation includes faction modifiers."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()

        # Register faction modifier
        stats_provider.register_faction_modifier(
            Faction.SOL,
            UnitType.FIGHTER,
            UnitStats(cost=-0.25),  # Reduce fighter cost
        )

        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test production cost with faction modifier
        production_cost = cost_validator.get_production_cost(
            UnitType.FIGHTER,
            2,  # Dual production
            faction=Faction.SOL,
        )

        assert production_cost.base_cost == 0.5  # Original base cost
        assert production_cost.modified_cost == 0.25  # 0.5 - 0.25 = 0.25
        assert (
            production_cost.total_cost == 0.25
        )  # Dual production: cost of 1 for 2 units
        assert production_cost.is_dual_production is True

    def test_production_cost_with_combined_modifiers(self) -> None:
        """Test production cost with both faction and technology modifiers."""
        # Create dependencies
        game_state = GameState()
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()

        # Register both types of modifiers
        stats_provider.register_faction_modifier(
            Faction.HACAN,
            UnitType.DESTROYER,
            UnitStats(cost=0.5),  # Increase cost
        )
        stats_provider.register_technology_modifier(
            Technology.DESTROYER_II,
            UnitType.DESTROYER,
            UnitStats(cost=-0.25),  # Decrease cost
        )

        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test production cost with combined modifiers
        production_cost = cost_validator.get_production_cost(
            UnitType.DESTROYER,
            3,
            faction=Faction.HACAN,
            technologies={Technology.DESTROYER_II},
        )

        assert production_cost.base_cost == 1.0  # Original base cost
        assert production_cost.modified_cost == 1.25  # 1.0 + 0.5 - 0.25 = 1.25
        assert production_cost.total_cost == 3.75  # 3 units * 1.25 = 3.75


class TestCostValidationWithModifiers:
    """Test cost validation integration with modifiers."""

    def test_validate_production_cost_with_modifiers(self) -> None:
        """Test that cost validation uses modified costs."""
        # Create game state with player and resources
        game_state = GameState()
        player = Player(id="player1", faction=Faction.SOL)

        # Create planet with limited resources
        planet = Planet("TestPlanet", resources=1, influence=0)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet)

        # Create dependencies
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()

        # Register faction modifier that reduces cruiser cost
        stats_provider.register_faction_modifier(
            Faction.SOL,
            UnitType.CRUISER,
            UnitStats(cost=-1),  # Reduce from 2 to 1
        )

        cost_validator = CostValidator(resource_manager, stats_provider)

        # Create production cost with faction modifier
        production_cost = cost_validator.get_production_cost(
            UnitType.CRUISER, 1, faction=Faction.SOL
        )

        # Validate cost - should be valid with 1 resource available and 1 cost
        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )

        assert validation_result.is_valid is True
        assert validation_result.required_resources == 1  # Modified cost
        assert validation_result.available_resources == 1  # Planet resource
        assert validation_result.shortfall == 0

    def test_validate_production_cost_insufficient_with_modifiers(self) -> None:
        """Test cost validation fails when modified cost exceeds resources."""
        # Create game state with player and limited resources
        game_state = GameState()
        player = Player(id="player1", faction=Faction.HACAN)

        # Create planet with limited resources
        planet = Planet("TestPlanet", resources=1, influence=0)

        # Set up game state
        game_state = game_state.add_player(player)
        game_state = game_state.add_player_planet(player.id, planet)

        # Create dependencies
        resource_manager = ResourceManager(game_state)
        stats_provider = UnitStatsProvider()

        # Register faction modifier that increases fighter cost
        stats_provider.register_faction_modifier(
            Faction.HACAN,
            UnitType.FIGHTER,
            UnitStats(cost=1),  # Increase from 0.5 to 1.5
        )

        cost_validator = CostValidator(resource_manager, stats_provider)

        # Create production cost with faction modifier
        production_cost = cost_validator.get_production_cost(
            UnitType.FIGHTER, 1, faction=Faction.HACAN
        )

        # Validate cost - should be invalid (need 2 resources, have 1)
        validation_result = cost_validator.validate_production_cost(
            player.id, production_cost
        )

        assert validation_result.is_valid is False
        assert validation_result.required_resources == 2  # ceil(1.5) = 2
        assert validation_result.available_resources == 1
        assert validation_result.shortfall == 1

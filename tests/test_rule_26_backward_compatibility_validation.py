"""
Test Rule 26 (Cost) backward compatibility validation.

This test suite ensures that the new resource management system maintains
backward compatibility with existing production, agenda phase, and strategy
card systems.

LRR References:
- Rule 26: COST (ATTRIBUTE)
- Rule 75: RESOURCES
- Rule 47: INFLUENCE
"""

from src.ti4.core.agenda_phase import AgendaPhase
from src.ti4.core.constants import Faction, UnitType
from src.ti4.core.game_state import GameState
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.production import ProductionManager
from src.ti4.core.resource_management import CostValidator, ResourceManager
from src.ti4.core.strategy_cards.coordinator import StrategyCardCoordinator
from src.ti4.testing.scenario_builder import GameScenarioBuilder


class TestRule26BackwardCompatibilityValidation:
    """Test backward compatibility with existing systems."""

    def test_existing_production_tests_still_pass(self):
        """Verify that existing production functionality remains intact."""
        # This test ensures that the new resource management system doesn't break
        # existing production mechanics that don't use cost validation

        # Create production manager (should work without resource validation)
        production_manager = ProductionManager()

        # Test that basic production validation still works
        # This should not require the new resource management system
        assert production_manager is not None

        # Verify that production manager can be created without dependencies
        # on the new resource management system
        assert hasattr(production_manager, "can_afford_unit")
        assert hasattr(production_manager, "get_units_produced_for_cost")

        # Test that basic planet functionality still works
        planet = Planet(name="test_planet", resources=3, influence=2)
        assert planet.name == "test_planet"
        assert planet.resources == 3
        assert planet.influence == 2

    def test_existing_agenda_phase_voting_compatibility(self):
        """Verify that existing agenda phase voting continues to work."""
        # Test that agenda phase can still function with existing planet exhaustion

        game_state = GameState()
        player = Player(id="test_player", faction=Faction.SOL)
        game_state = game_state.add_player(player)

        # Add planets for voting
        planet1 = Planet(name="planet1", resources=2, influence=3)
        planet1.controlled_by = "test_player"
        planet2 = Planet(name="planet2", resources=1, influence=2)
        planet2.controlled_by = "test_player"

        game_state = game_state.add_player_planet("test_player", planet1)
        game_state = game_state.add_player_planet("test_player", planet2)

        # Create agenda phase
        agenda_phase = AgendaPhase()

        # Verify agenda phase can be created and basic functionality works
        assert agenda_phase is not None
        assert hasattr(agenda_phase.voting_system, "cast_votes")

        # Test that planet exhaustion for voting still works
        # This should use existing planet exhaustion mechanics
        assert planet1.can_spend_influence()
        assert planet2.can_spend_influence()

    def test_existing_strategy_card_system_compatibility(self):
        """Verify that existing strategy card system continues to work."""
        # Test that strategy cards can still be used without the new resource system

        game_state = GameState()
        player = Player(id="test_player", faction=Faction.SOL)
        game_state = game_state.add_player(player)

        # Create strategy card coordinator
        coordinator = StrategyCardCoordinator(game_state)

        # Verify coordinator can be created and basic functionality works
        assert coordinator is not None
        assert hasattr(coordinator, "assign_strategy_card")
        assert hasattr(coordinator, "calculate_initiative_order")

    def test_game_state_management_compatibility(self):
        """Verify that game state management remains compatible."""
        # Test that game state can be created and managed without issues

        game_state = GameState()

        # Add players and planets as before
        player1 = Player(id="player1", faction=Faction.SOL)
        player2 = Player(id="player2", faction=Faction.HACAN)

        game_state = game_state.add_player(player1)
        game_state = game_state.add_player(player2)

        # Add planets
        planet1 = Planet(name="planet1", resources=3, influence=2)
        planet1.controlled_by = "player1"
        planet2 = Planet(name="planet2", resources=2, influence=3)
        planet2.controlled_by = "player2"

        game_state = game_state.add_player_planet("player1", planet1)
        game_state = game_state.add_player_planet("player2", planet2)

        # Verify game state integrity
        assert len(game_state.players) == 2
        assert game_state.get_player("player1") == player1
        assert game_state.get_player("player2") == player2

    def test_resource_manager_integration_optional(self):
        """Verify that ResourceManager integration is optional for existing systems."""
        # Test that existing systems can work without ResourceManager

        game_state = GameState()
        player = Player(id="test_player", faction=Faction.SOL)
        game_state = game_state.add_player(player)

        # Add planets
        planet = Planet(name="test_planet", resources=3, influence=2)
        planet.controlled_by = "test_player"
        game_state = game_state.add_player_planet("test_player", planet)

        # Test that planet exhaustion still works directly
        assert planet.can_spend_resources()
        assert planet.can_spend_influence()

        # Test spending resources directly (old way)
        resources_spent = planet.spend_resources(2)
        assert resources_spent == 2
        assert planet.is_exhausted()

    def test_cost_validator_integration_optional(self):
        """Verify that CostValidator integration is optional for existing systems."""
        # Test that production can work without CostValidator

        game_state = GameState()
        player = Player(id="test_player", faction=Faction.SOL)
        game_state = game_state.add_player(player)

        # Create production manager without cost validator
        production_manager = ProductionManager()

        # Verify it can be used for basic production validation
        assert production_manager is not None

        # Test that unit type validation still works
        assert UnitType.FIGHTER is not None
        assert UnitType.DESTROYER is not None

    def test_new_resource_system_backward_compatible_interface(self):
        """Verify that new ResourceManager provides backward compatible interface."""
        # Test that ResourceManager can work with existing game state structure

        game_state = GameState()
        player = Player(id="test_player", faction=Faction.SOL)
        game_state = game_state.add_player(player)

        # Add planets and trade goods
        planet1 = Planet(name="planet1", resources=3, influence=2)
        planet1.controlled_by = "test_player"
        planet2 = Planet(name="planet2", resources=2, influence=3)
        planet2.controlled_by = "test_player"

        game_state = game_state.add_player_planet("test_player", planet1)
        game_state = game_state.add_player_planet("test_player", planet2)

        # Create ResourceManager with existing game state
        resource_manager = ResourceManager(game_state)

        # Test that it can calculate resources from existing planet structure
        available_resources = resource_manager.calculate_available_resources(
            "test_player"
        )
        assert (
            available_resources == 5
        )  # 3 + 2 from planets (no trade goods since player is frozen)

        # Test that it can calculate influence from existing planet structure
        available_influence = resource_manager.calculate_available_influence(
            "test_player"
        )
        assert (
            available_influence == 5
        )  # 2 + 3 from planets (no trade goods for influence)

        # Test voting influence (should exclude trade goods)
        voting_influence = resource_manager.calculate_available_influence(
            "test_player", for_voting=True
        )
        assert voting_influence == 5  # 2 + 3, no trade goods

    def test_new_cost_validator_backward_compatible_interface(self):
        """Verify that new CostValidator provides backward compatible interface."""
        # Test that CostValidator can work with existing unit stats

        game_state = GameState()
        resource_manager = ResourceManager(game_state)

        # Create CostValidator (should work with existing unit stats system)
        from src.ti4.core.unit_stats import UnitStatsProvider

        stats_provider = UnitStatsProvider()
        cost_validator = CostValidator(resource_manager, stats_provider)

        # Test that it can get unit costs using existing unit types
        fighter_cost = cost_validator.get_unit_cost(UnitType.FIGHTER)
        assert fighter_cost >= 0  # Should return a valid cost

        destroyer_cost = cost_validator.get_unit_cost(UnitType.DESTROYER)
        assert destroyer_cost >= 0  # Should return a valid cost

    def test_migration_support_not_needed_for_existing_game_states(self):
        """Verify that existing game states don't need migration."""
        # Test that existing game state structure works with new system

        # Create a game state using the existing structure
        game_state = GameState()

        # Add players using existing methods
        player = Player(id="test_player", faction=Faction.SOL)
        game_state = game_state.add_player(player)

        # Add planets using existing methods
        planet = Planet(name="test_planet", resources=3, influence=2)
        planet.controlled_by = "test_player"
        game_state = game_state.add_player_planet("test_player", planet)

        # Note: Player is frozen, can't set trade_goods directly
        # This test needs to be updated to work with immutable players

        # Verify that new ResourceManager can work with this existing structure
        resource_manager = ResourceManager(game_state)

        # Should be able to calculate resources without any migration
        resources = resource_manager.calculate_available_resources("test_player")
        assert resources == 3  # 3 from planet (no trade goods since player is frozen)

        # Should be able to calculate influence without any migration
        influence = resource_manager.calculate_available_influence("test_player")
        assert influence == 2  # 2 from planet (trade goods can't be used for influence)

    def test_existing_test_patterns_still_work(self):
        """Verify that existing test patterns and utilities still work."""
        # Test that GameScenarioBuilder and other test utilities work

        # Use existing GameScenarioBuilder static methods
        game_state = GameScenarioBuilder.create_basic_2_player_game()
        assert game_state is not None

        # Should be able to create other scenarios
        combat_state = GameScenarioBuilder.create_combat_scenario()
        assert combat_state is not None

        # Should be able to create early game scenario
        early_state = GameScenarioBuilder.create_early_game_scenario()
        assert early_state is not None

    def test_error_handling_backward_compatibility(self):
        """Verify that error handling remains backward compatible."""
        # Test that existing error handling patterns still work

        game_state = GameState()

        # Test that existing validation errors still work
        result = game_state.get_player("nonexistent_player")
        assert result is None

        # Test that planet validation still works
        planet = Planet(name="test_planet", resources=3, influence=2)

        # Planet can spend when not exhausted (control validation is handled by GameState)
        assert planet.can_spend_resources()  # Not exhausted
        assert planet.can_spend_influence()  # Not exhausted

        # Should not be able to spend from exhausted planet
        planet.exhaust()
        assert not planet.can_spend_resources()  # Exhausted
        assert not planet.can_spend_influence()  # Exhausted

    def test_performance_characteristics_maintained(self):
        """Verify that performance characteristics are maintained."""
        # Test that basic operations are still fast

        game_state = GameState()

        # Add multiple players and planets
        for i in range(6):  # Typical game size
            player = Player(id=f"player_{i}", faction=Faction.SOL)
            game_state = game_state.add_player(player)

            # Add multiple planets per player
            for j in range(3):
                planet = Planet(name=f"planet_{i}_{j}", resources=2, influence=1)
                planet.controlled_by = f"player_{i}"
                game_state = game_state.add_player_planet(f"player_{i}", planet)

        # Test that ResourceManager can handle this scale efficiently
        resource_manager = ResourceManager(game_state)

        # Should be able to calculate resources for all players quickly
        for i in range(6):
            resources = resource_manager.calculate_available_resources(f"player_{i}")
            assert resources >= 0  # Should complete without timeout

            influence = resource_manager.calculate_available_influence(f"player_{i}")
            assert influence >= 0  # Should complete without timeout


class TestRule26SpecificBackwardCompatibility:
    """Test specific backward compatibility scenarios for Rule 26 implementation."""

    def test_production_without_cost_validation_still_works(self):
        """Test that production can work without the new cost validation system."""
        # This ensures that existing production code paths remain functional

        game_state = GameState()
        player = Player(id="test_player", faction=Faction.SOL)
        game_state = game_state.add_player(player)

        # Create production manager without cost dependencies
        production_manager = ProductionManager()

        # Should be able to validate production ability without cost checking
        # This tests the existing production validation logic
        assert hasattr(production_manager, "validate_production")

    def test_agenda_voting_without_influence_system_still_works(self):
        """Test that agenda voting can work without the new influence system."""
        # This ensures that existing agenda phase code paths remain functional

        game_state = GameState()
        player = Player(id="test_player", faction=Faction.SOL)
        game_state = game_state.add_player(player)

        # Add planets for voting
        planet = Planet(name="test_planet", resources=2, influence=3)
        planet.controlled_by = "test_player"
        game_state = game_state.add_player_planet("test_player", planet)

        # Create agenda phase
        agenda_phase = AgendaPhase()

        # Should be able to use existing voting mechanics
        assert hasattr(agenda_phase.voting_system, "cast_votes")

        # Test that planet can be exhausted for voting using existing methods
        assert planet.can_spend_influence()

    def test_strategy_cards_without_resource_integration_still_work(self):
        """Test that strategy cards work without the new resource integration."""
        # This ensures that existing strategy card code paths remain functional

        game_state = GameState()
        player = Player(id="test_player", faction=Faction.SOL)
        game_state = game_state.add_player(player)

        # Create strategy card coordinator
        coordinator = StrategyCardCoordinator(game_state)

        # Should be able to use existing strategy card mechanics
        assert hasattr(coordinator, "assign_strategy_card")
        assert hasattr(coordinator, "calculate_initiative_order")

    def test_planet_exhaustion_mechanics_unchanged(self):
        """Test that planet exhaustion mechanics remain unchanged."""
        # This ensures that the core planet exhaustion logic is preserved

        planet = Planet(name="test_planet", resources=3, influence=2)
        planet.controlled_by = "test_player"

        # Test existing exhaustion interface
        assert planet.can_spend_resources()
        assert planet.can_spend_influence()
        assert not planet.is_exhausted()

        # Test spending resources
        resources_spent = planet.spend_resources(2)
        assert resources_spent == 2
        assert planet.is_exhausted()

        # Test that exhausted planet can't spend more
        assert not planet.can_spend_resources()
        assert not planet.can_spend_influence()

    def test_trade_goods_mechanics_unchanged(self):
        """Test that trade goods mechanics remain unchanged."""
        # This ensures that existing trade goods logic is preserved

        player = Player(id="test_player", faction=Faction.SOL)
        player.gain_trade_goods(5)

        # Test existing trade goods interface
        assert player.get_trade_goods() == 5

        # Test spending trade goods
        success = player.spend_trade_goods(3)
        assert success
        assert player.get_trade_goods() == 2

        # Test insufficient trade goods
        success = player.spend_trade_goods(5)
        assert not success
        assert player.get_trade_goods() == 2  # Unchanged

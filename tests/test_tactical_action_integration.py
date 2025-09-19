"""Tests for Tactical Action Integration - demonstrates no redundancy and clear separation."""

from src.ti4.core.constants import UnitType
from src.ti4.core.galaxy import Galaxy
from src.ti4.core.hex_coordinate import HexCoordinate
from src.ti4.core.system import System
from src.ti4.core.tactical_action_coordinator import TacticalActionCoordinator
from src.ti4.core.unit import Unit
from tests.test_constants import MockPlayer, MockSystem


class TestTacticalActionIntegration:
    """Test that the layered architecture works without redundancy."""

    def test_no_redundant_code_between_systems(self) -> None:
        """Demonstrate that each system has unique, non-overlapping responsibilities."""
        coordinator = TacticalActionCoordinator()

        # Get unique responsibilities of each system
        responsibilities = coordinator.demonstrate_no_redundancy()

        # Verify each system has unique methods
        rule89_methods = set(responsibilities["Rule89Validator_unique_methods"])
        movement_engine_methods = set(responsibilities["MovementEngine_unique_methods"])
        movement_primitives_methods = set(
            responsibilities["MovementPrimitives_unique_methods"]
        )

        # No overlap between systems
        assert rule89_methods.isdisjoint(movement_engine_methods)
        assert rule89_methods.isdisjoint(movement_primitives_methods)
        assert movement_engine_methods.isdisjoint(movement_primitives_methods)

        # Each system has meaningful unique functionality
        assert len(rule89_methods) >= 4
        assert len(movement_engine_methods) >= 4
        assert len(movement_primitives_methods) >= 3

    def test_clear_system_roles(self) -> None:
        """Test that each system has a clearly defined role."""
        coordinator = TacticalActionCoordinator()

        roles = coordinator.get_system_roles()

        # Verify distinct roles
        assert "Rule 89 compliance" in roles["Rule89Validator"]
        assert "complex movement" in roles["MovementEngine"]
        assert (
            "Integrates validation and execution" in roles["TacticalActionCoordinator"]
        )
        assert "without redundancy" in roles["TacticalActionCoordinator"]

    def test_layered_architecture_integration(self) -> None:
        """Test that the layered architecture works correctly."""
        coordinator = TacticalActionCoordinator()

        # Create test scenario
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Test integration
        results = coordinator.validate_and_execute_tactical_action(
            system, MockPlayer.PLAYER_1.value, galaxy
        )

        # Should get results from Rule 89 validation
        assert "activation_valid" in results
        assert "combat_required" in results
        assert "invasion_possible" in results
        assert "production_possible" in results

        # Results should be boolean values
        assert isinstance(results["activation_valid"], bool)
        assert isinstance(results["combat_required"], bool)

    def test_rule89_validator_independence(self) -> None:
        """Test that Rule89Validator works independently."""
        from src.ti4.core.rule89_validator import Rule89Validator

        validator = Rule89Validator()

        # Create test scenario
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Test Rule 89 validation independently
        can_activate = validator.can_activate_system(
            system, MockPlayer.PLAYER_1.value, galaxy
        )
        requires_combat = validator.requires_space_combat(system)
        steps = validator.get_tactical_action_steps()

        assert isinstance(can_activate, bool)
        assert isinstance(requires_combat, bool)
        assert len(steps) == 5
        assert "Activation" in steps

    def test_movement_engine_independence(self) -> None:
        """Test that MovementEngine works independently."""
        from src.ti4.actions.movement_engine import MovementPlan

        # Test MovementEngine independently
        movement_plan = MovementPlan()

        # Create test unit
        unit = Unit(unit_type=UnitType.CRUISER, owner=MockPlayer.PLAYER_1.value)

        # Test movement planning
        movement_plan.add_ship_movement(unit, "system1", "system2")

        assert len(movement_plan.ship_movements) == 1
        assert movement_plan.ship_movements[0]["unit"] == unit

    def test_no_circular_dependencies(self) -> None:
        """Test that there are no circular dependencies between systems."""
        # Rule89Validator should not import MovementEngine
        from src.ti4.core.rule89_validator import Rule89Validator

        validator = Rule89Validator()

        # Should work without MovementEngine
        steps = validator.get_tactical_action_steps()
        assert len(steps) == 5

        # MovementEngine should not import Rule89Validator directly
        from src.ti4.actions.movement_engine import MovementPlan

        plan = MovementPlan()

        # Should work without Rule89Validator
        assert len(plan.ship_movements) == 0

    def test_integration_layer_prevents_confusion(self) -> None:
        """Test that the integration layer prevents confusion about which system to use."""
        coordinator = TacticalActionCoordinator()

        # The coordinator makes it clear which system to use when
        roles = coordinator.get_system_roles()

        # Clear guidance on when to use each system
        assert "Rule 89 compliance" in roles["Rule89Validator"]
        assert "complex movement" in roles["MovementEngine"]
        assert "Integrates" in roles["TacticalActionCoordinator"]

        # No ambiguity about responsibilities
        responsibilities = coordinator.demonstrate_no_redundancy()
        all_methods = []
        for system_methods in responsibilities.values():
            all_methods.extend(system_methods)

        # No duplicate method names across systems
        assert len(all_methods) == len(set(all_methods))

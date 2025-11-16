"""
Test Rule 89.5b: Production without movement or landing ground forces
"""

from unittest.mock import Mock, patch

from ti4.actions.movement_engine import MovementPlan
from ti4.core.galaxy import Galaxy
from ti4.core.planet import Planet
from ti4.core.player import Player
from ti4.core.system import System
from ti4.core.tactical_action_coordinator import TacticalActionCoordinator
from ti4.core.unit import Unit


class TestRule89_5b_ProductionWithoutMovementOrLanding:
    """Test Rule 89.5b: The active player may do production even if they did not move units or land ground forces during this tactical action."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.coordinator = TacticalActionCoordinator()
        self.galaxy = Galaxy()
        from ti4.core.constants import Faction

        self.player = Player("Test Player", Faction.SOL)

        # Create test systems
        self.active_system = System("active_system")
        # Galaxy does not require direct systems injection for production tests

        # Add a planet to the active system
        self.planet = Planet("test_planet", resources=1, influence=1)
        self.active_system.planets = [self.planet]

    def create_mock_unit_with_production(self, unit_type: str = "spacedock") -> Unit:
        """Create a mock unit with production capability."""
        unit = Mock(spec=Unit)
        # Create a mock unit_type that has a name attribute
        mock_unit_type = Mock()
        mock_unit_type.name = unit_type
        unit.unit_type = mock_unit_type
        unit.owner = "test_player"
        unit.has_production = Mock(return_value=True)
        unit.get_stats = Mock(return_value=Mock(production=True))
        return unit

    def test_production_allowed_without_movement_or_landing(self) -> None:
        """Test that production is allowed even when no units moved or ground forces landed."""
        # Arrange: Set up system with production unit but no movement or landing
        production_unit = self.create_mock_unit_with_production()
        self.active_system.space_units = [production_unit]

        # Create empty movement plan (no movement)
        movement_plan = MovementPlan()

        # No ground forces committed (no landing)

        # Act: Execute tactical action
        result = self.coordinator.validate_and_execute_tactical_action(
            player="test_player",
            active_system=self.active_system,
            movement_plan=movement_plan,
            galaxy=self.galaxy,
        )

        # Assert: Production should be allowed and executed
        assert result["production_allowed"] is True, (
            "Production should be allowed without movement or landing"
        )
        assert result["production_executed"] is True, (
            "Production should be executed when units with production exist"
        )
        assert result["production_result"]["units_with_production"] == 1, (
            "Should find 1 unit with production"
        )

    def test_production_allowed_with_movement_but_no_landing(self) -> None:
        """Test that production is allowed when units moved but no ground forces landed."""
        # Arrange: Set up system with production unit and movement but no landing
        production_unit = self.create_mock_unit_with_production()
        self.active_system.space_units = [production_unit]

        # Create movement plan with movement
        movement_plan = MovementPlan()
        # Ship movement added via proper API for typing compliance
        movement_plan.add_ship_movement(
            unit=Mock(), from_system="origin", to_system="active_system"
        )

        # No ground forces committed (no landing)

        # Act: Execute tactical action
        result = self.coordinator.validate_and_execute_tactical_action(
            player="test_player",
            active_system=self.active_system,
            movement_plan=movement_plan,
            galaxy=self.galaxy,
        )

        # Assert: Production should be allowed and executed
        assert result["production_allowed"] is True, (
            "Production should be allowed with movement but no landing"
        )
        assert result["production_executed"] is True, (
            "Production should be executed when units with production exist"
        )

    def test_production_allowed_with_landing_but_no_movement(self) -> None:
        """Test that production is allowed when ground forces landed but no units moved."""
        # Arrange: Set up system with production unit and landing but no movement
        production_unit = self.create_mock_unit_with_production()
        self.active_system.space_units = [production_unit]

        # Create empty movement plan (no movement)
        movement_plan = MovementPlan()

        # Mock invasion controller to simulate ground forces landing
        with patch("ti4.core.invasion.InvasionController") as mock_invasion_class:
            mock_invasion = Mock()
            mock_invasion.commit_ground_forces_step = Mock(
                return_value={
                    "ground_forces_committed": True,
                    "committed_forces": [Mock()],
                }
            )
            mock_invasion_class.return_value = mock_invasion

            # Act: Execute tactical action
            result = self.coordinator.validate_and_execute_tactical_action(
                player="test_player",
                active_system=self.active_system,
                movement_plan=movement_plan,
                galaxy=self.galaxy,
            )

        # Assert: Production should be allowed and executed
        assert result["production_allowed"] is True, (
            "Production should be allowed with landing but no movement"
        )
        assert result["production_executed"] is True, (
            "Production should be executed when units with production exist"
        )

    def test_production_allowed_with_neither_movement_nor_landing(self) -> None:
        """Test the core case: production allowed when neither movement nor landing occurred."""
        # Arrange: Set up system with production unit, no movement, no landing
        production_unit = self.create_mock_unit_with_production()
        self.active_system.space_units = [production_unit]

        # Create empty movement plan (no movement)
        movement_plan = MovementPlan()

        # Mock invasion controller to return no ground forces committed
        with patch("ti4.core.invasion.InvasionController") as mock_invasion_class:
            mock_invasion = Mock()
            mock_invasion.commit_ground_forces_step = Mock(
                return_value={"ground_forces_committed": False, "committed_forces": []}
            )
            mock_invasion_class.return_value = mock_invasion

            # Act: Execute tactical action
            result = self.coordinator.validate_and_execute_tactical_action(
                player="test_player",
                active_system=self.active_system,
                movement_plan=movement_plan,
                galaxy=self.galaxy,
            )

        # Assert: Production should be allowed and executed even with no movement/landing
        assert result["production_allowed"] is True, (
            "Production should be allowed even with no movement or landing"
        )
        assert result["production_executed"] is True, (
            "Production should be executed when units with production exist"
        )
        assert result["production_result"]["units_with_production"] == 1, (
            "Should find 1 unit with production"
        )

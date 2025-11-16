"""Strict TDD tests for TacticalActionCoordinator executing Rule 89 steps.

These tests target integration gaps and ensure movement plans are validated
and executed per LRR Rule 89, with post-execution flags updated correctly.

LRR References:
- Rule 89.1: Activation requirements
- Rule 89.2: Movement into the active system; ships may move from systems without own command tokens
- Rule 89.3: Space combat required if two players have ships in the active system
- Rule 89.4: Invasion step – bombardment and committing ground forces
- Rule 89.5: Production step – resolve production abilities in the active system
"""

from tests.test_constants import MockPlayer, MockSystem
from ti4.core.constants import LocationType, UnitType
from ti4.core.galaxy import Galaxy
from ti4.core.game_state import GameState
from ti4.core.hex_coordinate import HexCoordinate
from ti4.core.system import System
from ti4.core.tactical_action_coordinator import TacticalActionCoordinator
from ti4.core.unit import Unit


class TestCoordinatorMovementExecutionRule89:
    """Ensure coordinator validates and executes movement per Rule 89.2."""

    def test_coordinator_executes_movement_plan_and_moves_units(self) -> None:
        """Coordinator should validate and execute movement plan and move units.

        LRR 89.2: Movement into the active system using validated plan.
        """
        from ti4.actions.movement_engine import MovementPlan
        from ti4.core.tactical_actions import TacticalActionValidator

        # Setup galaxy and systems
        galaxy = Galaxy()
        source_system = System(MockSystem.TEST_SYSTEM.value)
        active_system = System(MockSystem.SYSTEM_2.value)

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)

        galaxy.place_system(coord1, MockSystem.TEST_SYSTEM.value)
        galaxy.place_system(coord2, MockSystem.SYSTEM_2.value)
        galaxy.register_system(source_system)
        galaxy.register_system(active_system)

        # Place ship in source system
        cruiser = Unit(unit_type=UnitType.CRUISER, owner=MockPlayer.PLAYER_1.value)
        source_system.place_unit_in_space(cruiser)

        # Build MovementPlan
        plan = MovementPlan()
        plan.add_ship_movement(
            cruiser, source_system.system_id, active_system.system_id
        )

        # Game state including systems mapping required by MovementStep
        game_state = GameState(
            galaxy=galaxy,
            systems={
                source_system.system_id: source_system,
                active_system.system_id: active_system,
            },
        )

        # Sanity: Rule 89 validator approves the activation and plan
        validator = TacticalActionValidator()
        assert validator.can_activate_system(
            active_system, MockPlayer.PLAYER_1.value, galaxy
        )
        is_valid, err = validator.validate_movement_plan(
            [cruiser], [source_system], active_system, MockPlayer.PLAYER_1.value, galaxy
        )
        assert is_valid is True
        assert err == ""

        # Execute via coordinator
        coordinator = TacticalActionCoordinator()
        results = coordinator.validate_and_execute_tactical_action(
            active_system,
            MockPlayer.PLAYER_1.value,
            galaxy,
            movement_plan=plan,
            player_technologies=None,
            game_state=game_state,
        )

        # Movement should be validated and executed
        assert results.get("movement_valid") is True
        assert results.get("movement_executed") is True

        # Unit should now be in the active system space
        assert cruiser in active_system.space_units
        assert cruiser not in source_system.space_units

    def test_coordinator_sets_combat_required_after_movement(self) -> None:
        """After movement, if two players have ships, combat_required must be True.

        LRR 89.3: Space combat required when two players have ships in active system.
        """
        from ti4.actions.movement_engine import MovementPlan

        galaxy = Galaxy()
        source_system = System("source")
        active_system = System("active")

        galaxy.place_system(HexCoordinate(0, 0), "source")
        galaxy.place_system(HexCoordinate(1, 0), "active")
        galaxy.register_system(source_system)
        galaxy.register_system(active_system)

        # Place ships: one already in active for player 2, one to move for player 1
        defender = Unit(unit_type=UnitType.DESTROYER, owner=MockPlayer.PLAYER_2.value)
        active_system.place_unit_in_space(defender)

        attacker = Unit(unit_type=UnitType.CRUISER, owner=MockPlayer.PLAYER_1.value)
        source_system.place_unit_in_space(attacker)

        plan = MovementPlan()
        plan.add_ship_movement(
            attacker, source_system.system_id, active_system.system_id
        )

        game_state = GameState(
            galaxy=galaxy,
            systems={
                source_system.system_id: source_system,
                active_system.system_id: active_system,
            },
        )

        coordinator = TacticalActionCoordinator()
        results = coordinator.validate_and_execute_tactical_action(
            active_system,
            MockPlayer.PLAYER_1.value,
            galaxy,
            movement_plan=plan,
            game_state=game_state,
        )

        # After movement, both players have ships in active system
        assert results.get("movement_executed") is True
        assert results.get("combat_required") is True

    def test_invasion_and_production_flags(self) -> None:
        """Coordinator should report invasion and production possibilities per LRR.

        LRR 89.4: Can commit ground forces; LRR 89.5: production in active system.
        """
        from ti4.actions.movement_engine import MovementPlan
        from ti4.core.planet import Planet

        galaxy = Galaxy()
        source_system = System("source")
        active_system = System("active")

        galaxy.place_system(HexCoordinate(0, 0), "source")
        galaxy.place_system(HexCoordinate(1, 0), "active")
        galaxy.register_system(source_system)
        galaxy.register_system(active_system)

        # Active system has a planet and a space dock for production
        planet = Planet("Ixth", resources=2, influence=1)
        active_system.add_planet(planet)
        space_dock = Unit(
            unit_type=UnitType.SPACE_DOCK, owner=MockPlayer.PLAYER_1.value
        )
        planet.place_unit(space_dock)

        # Source system contains a ground force that will be moved into active system space
        infantry = Unit(unit_type=UnitType.INFANTRY, owner=MockPlayer.PLAYER_1.value)
        source_system.place_unit_in_space(infantry)

        plan = MovementPlan()
        plan.add_ground_force_movement(
            infantry,
            source_system.system_id,
            active_system.system_id,
            LocationType.SPACE.value,
            LocationType.SPACE.value,
        )

        game_state = GameState(
            galaxy=galaxy,
            systems={
                source_system.system_id: source_system,
                active_system.system_id: active_system,
            },
        )

        coordinator = TacticalActionCoordinator()
        results = coordinator.validate_and_execute_tactical_action(
            active_system,
            MockPlayer.PLAYER_1.value,
            galaxy,
            movement_plan=plan,
            game_state=game_state,
        )

        # Movement executed; now invasion possible (ground forces in space), and production is possible
        assert results.get("movement_executed") is True
        assert results.get("invasion_possible") is True
        assert results.get("production_possible") is True

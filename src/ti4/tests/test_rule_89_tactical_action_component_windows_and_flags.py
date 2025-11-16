"""Strict TDD for Rule 89 component action windows and additional flags.

These tests extend the tactical action coordinator responsibilities to expose
timing windows (per LRR Rule 3, integrated with Rule 89 sequence) and add
missing flags for component steps like Space Cannon Offense and Bombardment.

LRR References:
- Rule 3: Action Phase timing windows and component actions
- Rule 58: Movement — adjacency, enemy ships, wormholes
- Rule 63: PDS (space cannon offense/defense)
- Rule 68: Production capabilities
- Rule 89: Tactical Action sequence (89.1–89.5)

Design references:
- LRR text: ti4_ai/LRR/lrr.txt
- Analysis notes: .trae/lrr_analysis/58_movement.md, 63_pds.md, 49_invasion.md
"""

from ti4.core.constants import UnitType
from ti4.core.galaxy import Galaxy
from ti4.core.hex_coordinate import HexCoordinate
from ti4.core.system import System
from ti4.core.tactical_action_coordinator import TacticalActionCoordinator
from ti4.core.unit import Unit


class TestComponentActionTimingWindows:
    """Expose component action timing windows via the coordinator (LRR §3 + §89)."""

    def test_coordinator_returns_timing_windows_for_tactical_action(self) -> None:
        """Coordinator should report timing windows aligned with LRR Rule 3 and Rule 89.

        Expected windows include at minimum:
        - after_activation (Rule 89.1)
        - after_movement (Rule 89.2)
        - start_of_space_combat (Rule 89.3)
        - before_invasion (Rule 89.4)
        - before_production (Rule 89.5)
        """
        galaxy = Galaxy()
        active_system = System("active_2")

        galaxy.place_system(HexCoordinate(1, 0), "active_2")
        galaxy.register_system(active_system)

        coordinator = TacticalActionCoordinator()
        results = coordinator.validate_and_execute_tactical_action(
            active_system,
            "player1",
            galaxy,
        )

        # The coordinator should expose timing windows for component actions.
        windows = results.get("timing_windows")
        assert isinstance(windows, list), (
            "Coordinator must return list of timing windows"
        )
        # At least the minimum set of expected tactical windows
        expected = {
            "after_activation",
            "after_movement",
            "start_of_space_combat",
            "before_invasion",
            "before_production",
        }
        assert expected.issubset(set(windows)), (
            "Missing required tactical action timing windows per LRR §3 and §89"
        )


class TestSpaceCannonOffenseFlag:
    """Space Cannon Offense possibility should be flagged post-movement (LRR §63, §89.2)."""

    def test_space_cannon_offense_possible_flag_is_set(self) -> None:
        """If opponent has PDS in an adjacent system, space cannon offense should be possible.

        This uses the MovementEngine's SpaceCannonOffenseStep semantics but expects the
        coordinator to expose a boolean flag `space_cannon_offense_possible` after movement.
        """
        from ti4.actions.movement_engine import MovementPlan

        galaxy = Galaxy()
        source_system = System("source")
        active_system = System("active")
        pds_system = System("adjacent_with_pds")

        # Place systems on a simple grid
        galaxy.place_system(HexCoordinate(0, 0), source_system.system_id)
        galaxy.place_system(HexCoordinate(1, 0), active_system.system_id)
        galaxy.place_system(HexCoordinate(1, 1), pds_system.system_id)
        galaxy.register_system(source_system)
        galaxy.register_system(active_system)
        galaxy.register_system(pds_system)

        # Defender PDS in adjacent system
        pds = Unit(unit_type=UnitType.PDS, owner="player2")
        pds_system.place_unit_on_planet(pds, planet_name=None)  # Simplified placement

        # Attacker moves a ship into the active system
        attacker_ship = Unit(unit_type=UnitType.CRUISER, owner="player1")
        source_system.place_unit_in_space(attacker_ship)

        plan = MovementPlan()
        plan.add_ship_movement(
            attacker_ship, source_system.system_id, active_system.system_id
        )

        from ti4.core.game_state import GameState

        game_state = GameState(
            galaxy=galaxy,
            systems={
                source_system.system_id: source_system,
                active_system.system_id: active_system,
                pds_system.system_id: pds_system,
            },
        )

        coordinator = TacticalActionCoordinator()
        results = coordinator.validate_and_execute_tactical_action(
            active_system,
            "player1",
            galaxy,
            movement_plan=plan,
            game_state=game_state,
        )

        assert results.get("movement_executed") is True
        # Expect the coordinator to compute and expose space cannon offense possibility
        assert results.get("space_cannon_offense_possible") is True, (
            "Coordinator must signal space cannon offense timing window per LRR §63 after movement"
        )


class TestSpaceCannonOffenseWormholes:
    """Space Cannon Offense should consider wormhole adjacency (LRR §101)."""

    def test_space_cannon_offense_considers_wormhole_adjacency(self) -> None:
        """Systems with matching wormholes are adjacent for offense timing.

        If the active system and a distant system share an ALPHA wormhole,
        offense should be possible even if not physically adjacent.
        """
        from ti4.actions.movement_engine import MovementPlan
        from ti4.core.constants import WormholeType

        galaxy = Galaxy()
        source_system = System("source_wh")
        active_system = System("active_wh")
        pds_system = System("distant_with_pds_wh")

        # Place systems far apart (not physically adjacent)
        galaxy.place_system(HexCoordinate(0, 0), source_system.system_id)
        galaxy.place_system(HexCoordinate(4, 0), active_system.system_id)
        galaxy.place_system(HexCoordinate(8, 0), pds_system.system_id)
        galaxy.register_system(source_system)
        galaxy.register_system(active_system)
        galaxy.register_system(pds_system)

        # Add matching ALPHA wormholes to active and PDS systems
        active_system.add_wormhole(WormholeType.ALPHA)
        pds_system.add_wormhole(WormholeType.ALPHA)

        # Defender PDS in distant system (placement simplified)
        pds = Unit(unit_type=UnitType.PDS, owner="player2")
        pds_system.place_unit_on_planet(
            pds, planet_name=None
        )  # May be no planet; adjacency is the focus

        # Attacker moves a ship into the active system
        attacker_ship = Unit(unit_type=UnitType.CRUISER, owner="player1")
        source_system.place_unit_in_space(attacker_ship)

        plan = MovementPlan()
        plan.add_ship_movement(
            attacker_ship, source_system.system_id, active_system.system_id
        )

        from ti4.core.game_state import GameState

        game_state = GameState(
            galaxy=galaxy,
            systems={
                source_system.system_id: source_system,
                active_system.system_id: active_system,
                pds_system.system_id: pds_system,
            },
        )

        coordinator = TacticalActionCoordinator()
        results = coordinator.validate_and_execute_tactical_action(
            active_system,
            "player1",
            galaxy,
            movement_plan=plan,
            game_state=game_state,
        )

        assert results.get("movement_executed") is True
        assert results.get("space_cannon_offense_possible") is True, (
            "Coordinator must consider wormhole adjacency (LRR §101) for space cannon offense"
        )

    def test_space_cannon_offense_mismatched_wormholes_not_adjacent(self) -> None:
        """Systems with different wormhole types are not adjacent for offense timing.

        If the active system has an ALPHA wormhole and the distant system has a BETA wormhole,
        offense should NOT be possible when they are not physically adjacent.
        """
        from ti4.actions.movement_engine import MovementPlan
        from ti4.core.constants import WormholeType

        galaxy = Galaxy()
        source_system = System("source_wh_mismatch")
        active_system = System("active_wh_alpha")
        pds_system = System("distant_with_pds_beta")

        # Place systems far apart (not physically adjacent)
        galaxy.place_system(HexCoordinate(0, 2), source_system.system_id)
        galaxy.place_system(HexCoordinate(5, 2), active_system.system_id)
        galaxy.place_system(HexCoordinate(10, 2), pds_system.system_id)
        galaxy.register_system(source_system)
        galaxy.register_system(active_system)
        galaxy.register_system(pds_system)

        # Add mismatched wormholes
        active_system.add_wormhole(WormholeType.ALPHA)
        pds_system.add_wormhole(WormholeType.BETA)

        # Defender PDS in distant system
        pds = Unit(unit_type=UnitType.PDS, owner="player2")
        pds_system.place_unit_on_planet(pds, planet_name=None)

        # Attacker moves a ship into the active system
        attacker_ship = Unit(unit_type=UnitType.CRUISER, owner="player1")
        source_system.place_unit_in_space(attacker_ship)

        plan = MovementPlan()
        plan.add_ship_movement(
            attacker_ship, source_system.system_id, active_system.system_id
        )

        from ti4.core.game_state import GameState

        game_state = GameState(
            galaxy=galaxy,
            systems={
                source_system.system_id: source_system,
                active_system.system_id: active_system,
                pds_system.system_id: pds_system,
            },
        )

        coordinator = TacticalActionCoordinator()
        results = coordinator.validate_and_execute_tactical_action(
            active_system,
            "player1",
            galaxy,
            movement_plan=plan,
            game_state=game_state,
        )

        assert results.get("movement_executed") is True
        assert results.get("space_cannon_offense_possible") is False, (
            "Coordinator must NOT consider mismatched wormhole types as adjacent for space cannon offense"
        )


class TestBombardmentFlag:
    """Bombardment possibility should be flagged for invasion step (LRR §89.4)."""

    def test_bombardment_possible_flag_is_set_when_heavy_ships_present(self) -> None:
        """If eligible ships are present in active system and planets exist, flag bombardment.

        Eligible bombardment ships include dreadnoughts and warsuns in standard TI4,
        subject to tech/law modifiers (LRR §49 invasion, §18 combat, §89.4 tactical).
        """
        galaxy = Galaxy()
        active_system = System("active")
        galaxy.place_system(HexCoordinate(0, 0), active_system.system_id)
        galaxy.register_system(active_system)

        # Add a planet and a dreadnought belonging to the acting player
        from ti4.core.planet import Planet

        planet = Planet("Target", resources=2, influence=1)
        active_system.add_planet(planet)

        dread = Unit(unit_type=UnitType.DREADNOUGHT, owner="player1")
        active_system.place_unit_in_space(dread)

        coordinator = TacticalActionCoordinator()
        results = coordinator.validate_and_execute_tactical_action(
            active_system,
            "player1",
            galaxy,
        )

        # Coordinator should expose bombardment possibility for the invasion step
        assert results.get("bombardment_possible") is True, (
            "Coordinator must expose bombardment eligibility per LRR §89.4 when heavy ships and planets are present"
        )

    def test_bombardment_flag_false_without_eligible_conditions(self) -> None:
        """Bombardment should be False if no planets or no bombardment-capable ships are present.

        Tighten the coordinator behavior to avoid over-reporting bombardment.
        """
        galaxy = Galaxy()
        active_system = System("active_no_bombard")
        galaxy.place_system(HexCoordinate(2, 0), active_system.system_id)
        galaxy.register_system(active_system)

        # Add a heavy ship without planets: should NOT allow bombardment
        dread = Unit(unit_type=UnitType.DREADNOUGHT, owner="player1")
        active_system.place_unit_in_space(dread)

        coordinator = TacticalActionCoordinator()
        results = coordinator.validate_and_execute_tactical_action(
            active_system,
            "player1",
            galaxy,
        )

        assert results.get("bombardment_possible") is False, (
            "Bombardment must be False when there are no planets in the active system, even if bombardment ships are present"
        )


class TestProductionFlag:
    """Production possibility should be correctly flagged for production step (LRR §89.5)."""

    def test_production_flag_false_without_production_units(self) -> None:
        """Production should be False if there are no production-capable units in the active system.

        Space docks (on planets) provide production; without them (and without tech-granted production),
        the coordinator must not report production as possible.
        """
        galaxy = Galaxy()
        active_system = System("active_no_production")
        galaxy.place_system(HexCoordinate(3, 0), active_system.system_id)
        galaxy.register_system(active_system)

        coordinator = TacticalActionCoordinator()
        results = coordinator.validate_and_execute_tactical_action(
            active_system,
            "player1",
            galaxy,
        )

        assert results.get("production_possible") is False, (
            "Production must be False when no units with PRODUCTION are present in the active system"
        )

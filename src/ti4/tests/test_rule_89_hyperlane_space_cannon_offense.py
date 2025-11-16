"""TDD for Rule 89 component window: Space Cannon Offense via hyperlanes.

This test ensures Space Cannon Offense possibility considers hyperlane adjacency
per LRR §6.4 in addition to physical and wormhole adjacency.

LRR References:
- Rule 6.4: Hyperlane adjacency
- Rule 63: PDS (space cannon offense)
- Rule 89.2: Tactical Action — after movement timing window
"""

from ti4.core.constants import UnitType
from ti4.core.galaxy import Galaxy
from ti4.core.hex_coordinate import HexCoordinate
from ti4.core.system import System
from ti4.core.tactical_action_coordinator import TacticalActionCoordinator
from ti4.core.unit import Unit


class TestSpaceCannonOffenseHyperlanes:
    """Space Cannon Offense should consider hyperlane adjacency (LRR §6.4)."""

    def test_space_cannon_offense_considers_hyperlane_adjacency(self) -> None:
        """Systems connected by hyperlanes are adjacent for offense timing.

        If the active system and a distant system are connected via hyperlane
        links, offense should be possible even if not physically adjacent.
        """
        from ti4.actions.movement_engine import MovementPlan

        galaxy = Galaxy()
        source_system = System("source_hl")
        active_system = System("active_hl")
        pds_system = System("distant_with_pds_hl")

        # Place systems far apart (not physically adjacent)
        galaxy.place_system(HexCoordinate(0, 0), source_system.system_id)
        galaxy.place_system(HexCoordinate(4, 0), active_system.system_id)
        galaxy.place_system(HexCoordinate(8, 0), pds_system.system_id)
        galaxy.register_system(source_system)
        galaxy.register_system(active_system)
        galaxy.register_system(pds_system)

        # Connect active system and PDS system via hyperlanes
        galaxy.add_hyperlane_connection(active_system.system_id, pds_system.system_id)

        # Defender PDS in distant system (placement simplified)
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
        assert results.get("space_cannon_offense_possible") is True, (
            "Coordinator must consider hyperlane adjacency (LRR §6.4) for space cannon offense"
        )

    def test_space_cannon_offense_does_not_consider_chained_hyperlane_links(
        self,
    ) -> None:
        """Systems connected via multiple hyperlane links are NOT adjacent for offense timing.

        Build a chain A - H1 - H2 - B using hyperlane connections and validate that
        offense is NOT possible from A to B unless there is a direct hyperlane link.
        This aligns with existing Rule 6 tests where adjacency via hyperlanes requires
        a direct connection, not transitive across intermediate systems.
        """
        from ti4.actions.movement_engine import MovementPlan

        galaxy = Galaxy()
        source_system = System("source_chain_hl")
        active_system = System("active_chain_hl")
        mid1 = System("hl_mid_1")
        mid2 = System("hl_mid_2")
        pds_system = System("distant_chain_pds_hl")

        # Place systems far apart (not physically adjacent)
        galaxy.place_system(HexCoordinate(0, 1), source_system.system_id)
        galaxy.place_system(HexCoordinate(4, 1), active_system.system_id)
        galaxy.place_system(HexCoordinate(6, 1), mid1.system_id)
        galaxy.place_system(HexCoordinate(8, 1), mid2.system_id)
        galaxy.place_system(HexCoordinate(12, 1), pds_system.system_id)
        galaxy.register_system(source_system)
        galaxy.register_system(active_system)
        galaxy.register_system(mid1)
        galaxy.register_system(mid2)
        galaxy.register_system(pds_system)

        # Connect active -> mid1 -> mid2 -> pds via hyperlanes
        galaxy.add_hyperlane_connection(active_system.system_id, mid1.system_id)
        galaxy.add_hyperlane_connection(mid1.system_id, mid2.system_id)
        galaxy.add_hyperlane_connection(mid2.system_id, pds_system.system_id)

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
                mid1.system_id: mid1,
                mid2.system_id: mid2,
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
            "Coordinator should NOT consider chained hyperlane links as adjacency; only direct hyperlane connections count"
        )

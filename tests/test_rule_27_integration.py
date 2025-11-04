from ti4.core.constants import Faction, SystemConstants, UnitType
from ti4.core.custodians_token import CustodiansToken
from ti4.core.game_state import GameState
from ti4.core.planet import Planet
from ti4.core.player import Player
from ti4.core.status_phase import RoundTransitionManager
from ti4.core.system_factory import SystemFactory
from ti4.core.unit import Unit


def build_state_for_integration() -> GameState:
    mec_system = SystemFactory.create_mecatol_rex_system()
    player_id = "player1"
    player = Player(id=player_id, faction=Faction.SOL)
    planet_a = Planet(name="Influence A", resources=1, influence=3)
    planet_b = Planet(name="Influence B", resources=0, influence=3)
    gs = GameState(
        players=[player],
        systems={SystemConstants.MECATOL_REX_ID: mec_system},
        player_planets={player_id: [planet_a, planet_b]},
        victory_points={player_id: 0},
    )
    return gs


def test_status_phase_next_phase_is_agenda_after_token_removal():
    gs = build_state_for_integration()
    player_id = "player1"

    # Satisfy ship requirement and commit ground force
    mec_system = gs.systems[SystemConstants.MECATOL_REX_ID]
    mec_system.place_unit_in_space(Unit(unit_type=UnitType.CRUISER, owner=player_id))
    ground = Unit(unit_type=UnitType.INFANTRY, owner=player_id)

    token = CustodiansToken()
    result, new_state = token.remove_with_ground_force_commitment(
        player_id=player_id, ground_force=ground, game_state=gs
    )
    assert result.success is True
    assert new_state.is_agenda_phase_active() is True

    transitions = RoundTransitionManager()
    assert transitions.determine_next_phase(new_state) == "agenda"


def test_status_phase_next_phase_is_strategy_without_token_removal():
    gs = build_state_for_integration()
    transitions = RoundTransitionManager()
    # Without agenda activation, next phase should be strategy
    assert gs.is_agenda_phase_active() is False
    assert transitions.determine_next_phase(gs) == "strategy"

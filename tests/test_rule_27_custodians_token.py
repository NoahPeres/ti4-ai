from ti4.core.constants import Faction, SystemConstants, UnitType
from ti4.core.custodians_token import CustodiansToken, TokenRemovalResult
from ti4.core.game_state import GameState
from ti4.core.planet import Planet
from ti4.core.player import Player
from ti4.core.system_factory import SystemFactory
from ti4.core.unit import Unit


def build_basic_game_state() -> GameState:
    """Create a minimal GameState with Mecatol Rex and a player with planets."""
    # Create Mecatol Rex system
    mec_system = SystemFactory.create_mecatol_rex_system()

    # Create a player and influence planets to afford 6 influence
    player_id = "player1"
    player = Player(id=player_id, faction=Faction.SOL)
    planet_a = Planet(name="Influence A", resources=1, influence=3)
    planet_b = Planet(name="Influence B", resources=0, influence=3)

    # Initialize game state
    gs = GameState(
        players=[player],
        systems={SystemConstants.MECATOL_REX_ID: mec_system},
        player_planets={player_id: [planet_a, planet_b]},
        victory_points={player_id: 0},
    )

    return gs


def test_custodians_token_cannot_be_removed_without_ships_or_influence():
    player_id = "player1"
    gs = build_basic_game_state()

    # Exhaust planets to remove available influence
    for p in gs.player_planets[player_id]:
        p.exhaust()

    token = CustodiansToken()

    # No ships present and no influence available
    assert token.can_be_removed_by_player(player_id, gs) is False


def test_custodians_token_can_be_removed_with_ships_and_influence():
    player_id = "player1"
    gs = build_basic_game_state()

    # Place a ship in Mecatol Rex space
    mec_system = gs.systems[SystemConstants.MECATOL_REX_ID]
    ship = Unit(unit_type=UnitType.CRUISER, owner=player_id)
    mec_system.place_unit_in_space(ship)

    token = CustodiansToken()
    assert token.can_be_removed_by_player(player_id, gs) is True


def test_remove_custodians_token_flow_awards_vp_and_activates_agenda_phase():
    player_id = "player1"
    gs = build_basic_game_state()

    # Place a ship in Mecatol Rex space
    mec_system = gs.systems[SystemConstants.MECATOL_REX_ID]
    ship = Unit(unit_type=UnitType.CRUISER, owner=player_id)
    mec_system.place_unit_in_space(ship)

    # Prepare a ground force to commit
    ground = Unit(unit_type=UnitType.INFANTRY, owner=player_id)

    token = CustodiansToken()
    result, new_state = token.remove_with_ground_force_commitment(
        player_id=player_id, ground_force=ground, game_state=gs
    )

    assert isinstance(result, TokenRemovalResult)
    assert result.success is True
    assert result.victory_points_awarded == 1
    assert result.agenda_phase_activated is True

    # VP updated
    assert new_state.get_victory_points(player_id) == 1

    # Agenda phase active
    assert new_state.is_agenda_phase_active() is True

    # Ground force placed on Mecatol Rex planet
    mec_system_post = new_state.systems[SystemConstants.MECATOL_REX_ID]
    units_on_planet = mec_system_post.get_units_on_planet("Mecatol Rex")
    assert any(
        u.owner == player_id and u.unit_type == UnitType.INFANTRY
        for u in units_on_planet
    )


def test_remove_fails_without_committed_ground_force_and_does_not_activate_agenda():
    player_id = "player1"
    gs = build_basic_game_state()

    # Place a ship in Mecatol Rex space to satisfy ship requirement
    mec_system = gs.systems[SystemConstants.MECATOL_REX_ID]
    ship = Unit(unit_type=UnitType.CRUISER, owner=player_id)
    mec_system.place_unit_in_space(ship)

    token = CustodiansToken()
    result, new_state = token.remove_with_ground_force_commitment(
        player_id=player_id, ground_force=None, game_state=gs
    )

    assert isinstance(result, TokenRemovalResult)
    assert result.success is False
    assert "ground force" in result.error_message.lower()
    # Agenda phase should remain inactive
    assert new_state.is_agenda_phase_active() is False
    # VP should remain unchanged
    assert new_state.get_victory_points(player_id) == 0


def test_mecatol_rex_landing_restriction_with_token_present_and_after_removal():
    player_id = "player1"
    gs = build_basic_game_state()
    mec_system = gs.systems[SystemConstants.MECATOL_REX_ID]

    # Attach custodians token to Mecatol Rex planet
    token = CustodiansToken()
    mecatol_planet = mec_system.get_planet_by_name("Mecatol Rex")
    assert mecatol_planet is not None
    mecatol_planet.set_custodians_token(token)

    # While token present, cannot land ground forces
    assert mecatol_planet.can_land_ground_forces(player_id) is False

    # Remove token (simulate removal) and verify landing becomes allowed
    token.remove_from_mecatol_rex()
    assert mecatol_planet.can_land_ground_forces(player_id) is True


def test_remove_fails_with_insufficient_influence_even_with_ships():
    player_id = "player1"
    gs = build_basic_game_state()

    # Place a ship in Mecatol Rex space to satisfy ship requirement
    mec_system = gs.systems[SystemConstants.MECATOL_REX_ID]
    ship = Unit(unit_type=UnitType.CRUISER, owner=player_id)
    mec_system.place_unit_in_space(ship)

    # Exhaust planets to remove available influence
    for p in gs.player_planets[player_id]:
        p.exhaust()

    # Prepare a ground force to commit
    ground = Unit(unit_type=UnitType.INFANTRY, owner=player_id)

    token = CustodiansToken()
    result, new_state = token.remove_with_ground_force_commitment(
        player_id=player_id, ground_force=ground, game_state=gs
    )

    assert isinstance(result, TokenRemovalResult)
    assert result.success is False
    # Generic requirements failure is acceptable here since can_be_removed_by_player
    # fails before spending plan creation due to lack of influence.
    assert "requirements" in result.error_message.lower()
    # VP should remain unchanged and agenda phase inactive
    assert new_state.get_victory_points(player_id) == 0
    assert new_state.is_agenda_phase_active() is False


def test_remove_fails_without_ships_even_with_influence():
    player_id = "player1"
    gs = build_basic_game_state()

    # Have sufficient influence (default from build_basic_game_state)
    # No ships placed in Mecatol Rex system

    ground = Unit(unit_type=UnitType.INFANTRY, owner=player_id)
    token = CustodiansToken()
    result, new_state = token.remove_with_ground_force_commitment(
        player_id=player_id, ground_force=ground, game_state=gs
    )

    assert isinstance(result, TokenRemovalResult)
    assert result.success is False
    assert (
        "requirements" in result.error_message.lower()
        or "ship" in result.error_message.lower()
    )
    assert new_state.get_victory_points(player_id) == 0
    assert new_state.is_agenda_phase_active() is False


def test_custodians_token_removal_is_idempotent_awarding_vp_once():
    player_id = "player1"
    gs = build_basic_game_state()

    mec_system = gs.systems[SystemConstants.MECATOL_REX_ID]
    ship = Unit(unit_type=UnitType.CRUISER, owner=player_id)
    mec_system.place_unit_in_space(ship)

    ground = Unit(unit_type=UnitType.INFANTRY, owner=player_id)
    token = CustodiansToken()

    # First removal succeeds
    result1, state1 = token.remove_with_ground_force_commitment(
        player_id=player_id, ground_force=ground, game_state=gs
    )
    assert result1.success is True
    assert state1.get_victory_points(player_id) == 1
    assert state1.is_agenda_phase_active() is True

    # Second removal attempt should fail and not change VP or agenda state
    ground2 = Unit(unit_type=UnitType.INFANTRY, owner=player_id)
    result2, state2 = token.remove_with_ground_force_commitment(
        player_id=player_id, ground_force=ground2, game_state=state1
    )
    assert result2.success is False
    assert state2.get_victory_points(player_id) == 1
    assert state2.is_agenda_phase_active() is True


def test_can_be_removed_returns_false_after_token_is_removed():
    player_id = "player1"
    gs = build_basic_game_state()

    mec_system = gs.systems[SystemConstants.MECATOL_REX_ID]
    ship = Unit(unit_type=UnitType.CRUISER, owner=player_id)
    mec_system.place_unit_in_space(ship)

    token = CustodiansToken()
    assert token.can_be_removed_by_player(player_id, gs) is True
    token.remove_from_mecatol_rex()
    assert token.can_be_removed_by_player(player_id, gs) is False

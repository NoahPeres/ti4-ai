"""
Test Rule 27: CUSTODIANS TOKEN

This module tests the implementation of Rule 27: CUSTODIANS TOKEN according to the LRR.

Key Requirements from LRR:
- 27.1: Players cannot land ground forces on Mecatol Rex while custodians token is on that planet
- 27.2: Token can be removed by spending 6 influence while having ships in Mecatol Rex system
- 27.2a: When removing token, must commit at least one ground force to land on Mecatol Rex
- 27.3: When removing token, player gains 1 victory point
- 27.4: After token removal, agenda phase is added to each game round

Test Coverage Plan:
- Token initialization and state management
- Ground force landing restrictions (Rule 27.1)
- Token removal requirements (Rule 27.2)
- Ground force commitment (Rule 27.2a)
- Victory point award (Rule 27.3)
- Agenda phase activation (Rule 27.4)
- Integration with existing systems
- Error conditions and edge cases
"""

from unittest.mock import Mock

from src.ti4.core.constants import UnitType
from src.ti4.core.custodians_token import CustodiansToken
from src.ti4.core.planet import Planet
from src.ti4.core.unit import Unit


class TestRule27CustodiansTokenInitialization:
    """Test Rule 27: Custodians token initialization and basic state management."""

    def test_custodians_token_starts_on_mecatol_rex(self):
        """
        Test that custodians token begins the game on Mecatol Rex.

        LRR 27: The custodians token begins the game on Mecatol Rex.
        """
        # Act: Create custodians token
        token = CustodiansToken()

        # Assert: Token should start on Mecatol Rex
        assert token.is_on_mecatol_rex() is True
        assert token.location == "mecatol_rex"

    def test_custodians_token_tracks_location_state(self):
        """
        Test that custodians token properly tracks its location state.

        This test ensures the token can track whether it's on Mecatol Rex or removed.
        """
        # Arrange: Create custodians token
        token = CustodiansToken()

        # Act & Assert: Initial state
        assert token.is_on_mecatol_rex() is True

        # Act: Remove token (basic removal for state testing)
        token.remove_from_mecatol_rex()

        # Assert: Token should no longer be on Mecatol Rex
        assert token.is_on_mecatol_rex() is False


class TestRule27GroundForceLandingRestriction:
    """Test Rule 27.1: Ground force landing restrictions while custodians token present."""

    def test_cannot_land_ground_forces_while_custodians_token_present(self):
        """
        Test that players cannot land ground forces on Mecatol Rex while custodians token is present.

        LRR 27.1: Players cannot land ground forces on Mecatol Rex while the custodians token is on that planet.
        """
        # Arrange: Create Mecatol Rex with custodians token
        mecatol_rex = Planet(name="Mecatol Rex", resources=1, influence=6)
        token = CustodiansToken()
        mecatol_rex.set_custodians_token(token)

        # Act: Attempt to check if ground forces can land
        can_land = mecatol_rex.can_land_ground_forces("player1")

        # Assert: Should not be able to land ground forces
        assert can_land is False

    def test_can_land_ground_forces_after_custodians_token_removed(self):
        """
        Test that players can land ground forces on Mecatol Rex after custodians token is removed.

        This test ensures the landing restriction is lifted when token is removed.
        """
        # Arrange: Create Mecatol Rex with custodians token
        mecatol_rex = Planet(name="Mecatol Rex", resources=1, influence=6)
        token = CustodiansToken()
        mecatol_rex.set_custodians_token(token)

        # Act: Remove custodians token
        token.remove_from_mecatol_rex()
        mecatol_rex.remove_custodians_token()

        # Act: Check if ground forces can land
        can_land = mecatol_rex.can_land_ground_forces("player1")

        # Assert: Should be able to land ground forces
        assert can_land is True


class TestRule27TokenRemovalRequirements:
    """Test Rule 27.2: Token removal requirements (6 influence + ships in system)."""

    def test_can_remove_token_with_sufficient_influence_and_ships(self):
        """
        Test that player can remove custodians token with 6 influence and ships in system.

        LRR 27.2: A player can remove the custodians token from Mecatol Rex by spending
        six influence while they have one or more ships in the Mecatol Rex system.
        """
        # Arrange: Create game state with player having 6 influence and ships in Mecatol Rex
        token = CustodiansToken()
        game_state = Mock()

        # Mock player has 6 influence available
        game_state.get_player_available_influence.return_value = 6

        # Mock player has ships in Mecatol Rex system
        game_state.player_has_ships_in_system.return_value = True

        # Act: Check if player can remove token
        can_remove = token.can_be_removed_by_player("player1", game_state)

        # Assert: Should be able to remove token
        assert can_remove is True

    def test_cannot_remove_token_with_insufficient_influence(self):
        """
        Test that player cannot remove custodians token with insufficient influence.

        LRR 27.2: Requires spending six influence to remove the token.
        """
        # Arrange: Create game state with player having insufficient influence
        token = CustodiansToken()
        game_state = Mock()

        # Mock player has only 5 influence available
        game_state.get_player_available_influence.return_value = 5

        # Mock player has ships in Mecatol Rex system
        game_state.player_has_ships_in_system.return_value = True

        # Act: Check if player can remove token
        can_remove = token.can_be_removed_by_player("player1", game_state)

        # Assert: Should not be able to remove token
        assert can_remove is False

    def test_cannot_remove_token_without_ships_in_system(self):
        """
        Test that player cannot remove custodians token without ships in Mecatol Rex system.

        LRR 27.2: Requires having one or more ships in the Mecatol Rex system.
        """
        # Arrange: Create game state with player having sufficient influence but no ships
        token = CustodiansToken()
        game_state = Mock()

        # Mock player has 6 influence available
        game_state.get_player_available_influence.return_value = 6

        # Mock player has no ships in Mecatol Rex system
        game_state.player_has_ships_in_system.return_value = False

        # Act: Check if player can remove token
        can_remove = token.can_be_removed_by_player("player1", game_state)

        # Assert: Should not be able to remove token
        assert can_remove is False


class TestRule27GroundForceCommitment:
    """Test Rule 27.2a: Mandatory ground force commitment when removing token."""

    def test_must_commit_ground_force_when_removing_token(self):
        """
        Test that player must commit at least one ground force when removing custodians token.

        LRR 27.2a: When a player removes the custodians token, they must commit
        at least one ground force to land on Mecatol Rex.
        """
        # Arrange: Create token and game state with available ground force
        token = CustodiansToken()
        game_state = Mock()
        ground_force = Unit(unit_type=UnitType.INFANTRY, owner="player1")

        # Mock removal requirements are met
        game_state.get_player_available_influence.return_value = 6
        game_state.player_has_ships_in_system.return_value = True
        game_state.get_player_available_ground_forces.return_value = [ground_force]

        # Act: Attempt to remove token with ground force commitment
        result, new_game_state = token.remove_with_ground_force_commitment(
            "player1", ground_force, game_state
        )

        # Assert: Removal should succeed
        assert result.success is True
        assert token.is_on_mecatol_rex() is False

    def test_cannot_remove_token_without_available_ground_force(self):
        """
        Test that player cannot remove custodians token without available ground force.

        LRR 27.2a: Must commit at least one ground force to land on Mecatol Rex.
        """
        # Arrange: Create token and game state with no available ground forces
        token = CustodiansToken()
        game_state = Mock()

        # Mock removal requirements are met except ground forces
        game_state.get_player_available_influence.return_value = 6
        game_state.player_has_ships_in_system.return_value = True
        game_state.get_player_available_ground_forces.return_value = []

        # Act: Attempt to remove token without ground force
        result, new_game_state = token.remove_with_ground_force_commitment(
            "player1", None, game_state
        )

        # Assert: Removal should fail
        assert result.success is False
        assert "ground force" in result.error_message.lower()
        assert token.is_on_mecatol_rex() is True


class TestRule27VictoryPointAward:
    """Test Rule 27.3: Victory point award when removing custodians token."""

    def test_player_gains_victory_point_when_removing_token(self):
        """
        Test that player gains 1 victory point when removing custodians token.

        LRR 27.3: When a player removes the custodians token, they gain one victory point.
        """
        # Arrange: Create token and game state
        token = CustodiansToken()
        game_state = Mock()
        ground_force = Unit(unit_type=UnitType.INFANTRY, owner="player1")

        # Mock removal requirements are met
        game_state.get_player_available_influence.return_value = 6
        game_state.player_has_ships_in_system.return_value = True
        game_state.get_player_available_ground_forces.return_value = [ground_force]
        game_state.get_player_victory_points.return_value = 0

        # Act: Remove token with ground force commitment
        result, new_game_state = token.remove_with_ground_force_commitment(
            "player1", ground_force, game_state
        )

        # Assert: Player should gain 1 victory point
        assert result.success is True
        assert result.victory_points_awarded == 1
        game_state.award_victory_points.assert_called_once_with("player1", 1)


class TestRule27AgendaPhaseActivation:
    """Test Rule 27.4: Agenda phase activation after token removal."""

    def test_agenda_phase_activated_after_token_removal(self):
        """
        Test that agenda phase is added to each game round after custodians token removal.

        LRR 27.4: After a player removes the custodians token, the agenda phase is added to each game round.
        """
        # Arrange: Create token and game state
        token = CustodiansToken()
        game_state = Mock()
        ground_force = Unit(unit_type=UnitType.INFANTRY, owner="player1")

        # Mock removal requirements are met
        game_state.get_player_available_influence.return_value = 6
        game_state.player_has_ships_in_system.return_value = True
        game_state.get_player_available_ground_forces.return_value = [ground_force]
        game_state.is_agenda_phase_active.return_value = False

        # Mock the chained method calls: award_victory_points returns a new state
        # that has activate_agenda_phase method
        intermediate_state = Mock()
        final_state = Mock()
        game_state.award_victory_points.return_value = intermediate_state
        intermediate_state.activate_agenda_phase.return_value = final_state

        # Act: Remove token with ground force commitment
        result, new_game_state = token.remove_with_ground_force_commitment(
            "player1", ground_force, game_state
        )

        # Assert: Agenda phase should be activated
        assert result.success is True
        assert result.agenda_phase_activated is True
        game_state.award_victory_points.assert_called_once_with("player1", 1)
        intermediate_state.activate_agenda_phase.assert_called_once()

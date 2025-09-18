"""
Comprehensive tests for Rule 61 secret objective system.

Tests the implementation of:
- Secret objective ownership and privacy
- Imperial strategy card secret objective mechanics
- 3 secret objective limit per player
- Secret objective scoring validation
"""

import pytest

from src.ti4.core.game_phase import GamePhase
from src.ti4.core.game_state import GameState
from src.ti4.core.objective import Objective


class TestSecretObjectiveOwnership:
    """Test secret objective ownership and privacy (Rule 61.19)."""

    def test_players_can_only_score_owned_secret_objectives(self):
        """Test that players can only score secret objectives they own."""
        game_state = GameState()

        secret_obj = Objective(
            "sec1", "Secret 1", "Player 1's secret", 1, False, GamePhase.STATUS
        )

        # Give secret objective to player1
        state_with_secret = game_state.assign_secret_objective("player1", secret_obj)

        # Player1 should be able to score their own secret objective
        state1 = state_with_secret.score_objective(
            "player1", secret_obj, GamePhase.STATUS
        )
        assert state1.is_objective_completed("player1", secret_obj)
        assert state1.get_victory_points("player1") == 1

        # Player2 should NOT be able to score player1's secret objective
        with pytest.raises(
            ValueError, match="Cannot score secret objective.*not owned by player"
        ):
            state_with_secret.score_objective("player2", secret_obj, GamePhase.STATUS)

    def test_secret_objectives_are_hidden_from_other_players(self):
        """Test that secret objectives are hidden from other players."""
        game_state = GameState()

        secret_obj1 = Objective(
            "sec1", "Secret 1", "Player 1's secret", 1, False, GamePhase.STATUS
        )
        secret_obj2 = Objective(
            "sec2", "Secret 2", "Player 2's secret", 1, False, GamePhase.STATUS
        )

        # Assign secret objectives to different players
        state1 = game_state.assign_secret_objective("player1", secret_obj1)
        state2 = state1.assign_secret_objective("player2", secret_obj2)

        # Player1 should only see their own secret objectives
        player1_secrets = state2.get_player_secret_objectives("player1")
        assert len(player1_secrets) == 1
        assert secret_obj1.id in [obj.id for obj in player1_secrets]
        assert secret_obj2.id not in [obj.id for obj in player1_secrets]

        # Player2 should only see their own secret objectives
        player2_secrets = state2.get_player_secret_objectives("player2")
        assert len(player2_secrets) == 1
        assert secret_obj2.id in [obj.id for obj in player2_secrets]
        assert secret_obj1.id not in [obj.id for obj in player2_secrets]

    def test_players_can_have_maximum_three_secret_objectives(self):
        """Test Rule 61.20: Players can have at most 3 secret objectives."""
        game_state = GameState()

        secret_objectives = [
            Objective(
                f"sec{i}",
                f"Secret {i}",
                f"Secret objective {i}",
                1,
                False,
                GamePhase.STATUS,
            )
            for i in range(1, 5)  # Create 4 secret objectives
        ]

        # Assign first 3 secret objectives - should succeed
        current_state = game_state
        for i in range(3):
            current_state = current_state.assign_secret_objective(
                "player1", secret_objectives[i]
            )

        # Verify player has 3 secret objectives
        player_secrets = current_state.get_player_secret_objectives("player1")
        assert len(player_secrets) == 3

        # Try to assign 4th secret objective - should fail
        with pytest.raises(
            ValueError, match="Player.*already has maximum.*3.*secret objectives"
        ):
            current_state.assign_secret_objective("player1", secret_objectives[3])

    def test_scoring_secret_objective_removes_it_from_hand(self):
        """Test that scoring a secret objective removes it from player's hand."""
        game_state = GameState()

        secret_obj = Objective(
            "sec1", "Secret 1", "Player's secret", 1, False, GamePhase.STATUS
        )

        # Assign secret objective to player
        state1 = game_state.assign_secret_objective("player1", secret_obj)
        assert len(state1.get_player_secret_objectives("player1")) == 1

        # Score the secret objective
        state2 = state1.score_objective("player1", secret_obj, GamePhase.STATUS)

        # Secret objective should be removed from hand
        assert len(state2.get_player_secret_objectives("player1")) == 0
        assert state2.is_objective_completed("player1", secret_obj)
        assert state2.get_victory_points("player1") == 1


class TestImperialStrategyCardSecretObjectives:
    """Test Imperial strategy card secret objective mechanics (Rule 45.4)."""

    def test_imperial_primary_ability_draws_secret_objective(self):
        """Test that Imperial primary ability allows drawing a secret objective."""
        game_state = GameState()

        # Create secret objective deck
        secret_obj = Objective(
            "sec1", "Secret 1", "New secret", 1, False, GamePhase.STATUS
        )
        state_with_deck = game_state.add_secret_objective_to_deck(secret_obj)

        # Execute Imperial primary ability
        state_after_imperial = state_with_deck.execute_imperial_primary_ability(
            "player1"
        )

        # Player should have drawn a secret objective
        player_secrets = state_after_imperial.get_player_secret_objectives("player1")
        assert len(player_secrets) == 1
        assert player_secrets[0].id == secret_obj.id

    def test_imperial_primary_ability_respects_three_objective_limit(self):
        """Test that Imperial primary ability respects the 3 secret objective limit."""
        game_state = GameState()

        # Give player 3 secret objectives (at limit)
        secret_objectives = [
            Objective(
                f"sec{i}", f"Secret {i}", f"Secret {i}", 1, False, GamePhase.STATUS
            )
            for i in range(1, 4)
        ]

        current_state = game_state
        for obj in secret_objectives:
            current_state = current_state.assign_secret_objective("player1", obj)

        # Add another secret to deck
        new_secret = Objective(
            "sec4", "Secret 4", "New secret", 1, False, GamePhase.STATUS
        )
        state_with_deck = current_state.add_secret_objective_to_deck(new_secret)

        # Try to execute Imperial primary ability - should fail or be ignored
        with pytest.raises(
            ValueError, match="Cannot draw secret objective.*already at maximum"
        ):
            state_with_deck.execute_imperial_primary_ability("player1")

    def test_imperial_secondary_ability_allows_secret_objective_draw(self):
        """Test that Imperial secondary ability allows drawing a secret objective for 1 influence."""
        game_state = GameState()

        # Give player some influence
        state_with_influence = game_state.set_player_influence("player1", 2)

        # Create secret objective deck
        secret_obj = Objective(
            "sec1", "Secret 1", "New secret", 1, False, GamePhase.STATUS
        )
        state_with_deck = state_with_influence.add_secret_objective_to_deck(secret_obj)

        # Execute Imperial secondary ability
        state_after_secondary = state_with_deck.execute_imperial_secondary_ability(
            "player1"
        )

        # Player should have drawn a secret objective and spent 1 influence
        player_secrets = state_after_secondary.get_player_secret_objectives("player1")
        assert len(player_secrets) == 1
        assert player_secrets[0].id == secret_obj.id
        assert state_after_secondary.get_player_influence("player1") == 1

    def test_imperial_secondary_ability_requires_influence(self):
        """Test that Imperial secondary ability requires 1 influence to draw secret objective."""
        game_state = GameState()

        # Player has no influence
        assert game_state.get_player_influence("player1") == 0

        # Create secret objective deck
        secret_obj = Objective(
            "sec1", "Secret 1", "New secret", 1, False, GamePhase.STATUS
        )
        state_with_deck = game_state.add_secret_objective_to_deck(secret_obj)

        # Try to execute Imperial secondary ability without influence - should fail
        with pytest.raises(
            ValueError, match="Insufficient influence.*requires 1 influence"
        ):
            state_with_deck.execute_imperial_secondary_ability("player1")


class TestSecretObjectiveDeck:
    """Test secret objective deck management."""

    def test_secret_objective_deck_starts_empty(self):
        """Test that secret objective deck starts empty."""
        game_state = GameState()
        assert game_state.get_secret_objective_deck_size() == 0

    def test_can_add_secret_objectives_to_deck(self):
        """Test adding secret objectives to the deck."""
        game_state = GameState()

        secret_objectives = [
            Objective(
                f"sec{i}", f"Secret {i}", f"Secret {i}", 1, False, GamePhase.STATUS
            )
            for i in range(1, 4)
        ]

        current_state = game_state
        for obj in secret_objectives:
            current_state = current_state.add_secret_objective_to_deck(obj)

        assert current_state.get_secret_objective_deck_size() == 3

    def test_drawing_from_empty_deck_fails(self):
        """Test that drawing from empty secret objective deck fails."""
        game_state = GameState()

        with pytest.raises(ValueError, match="Secret objective deck is empty"):
            game_state.execute_imperial_primary_ability("player1")

    def test_secret_objectives_are_shuffled_in_deck(self):
        """Test that secret objectives maintain deck order but can be shuffled."""
        game_state = GameState()

        secret_objectives = [
            Objective(
                f"sec{i}", f"Secret {i}", f"Secret {i}", 1, False, GamePhase.STATUS
            )
            for i in range(1, 6)
        ]

        # Add objectives to deck
        current_state = game_state
        for obj in secret_objectives:
            current_state = current_state.add_secret_objective_to_deck(obj)

        # Shuffle deck
        shuffled_state = current_state.shuffle_secret_objective_deck()

        # Deck size should remain the same
        assert shuffled_state.get_secret_objective_deck_size() == 5


class TestSecretObjectiveGameIntegration:
    """Test secret objective integration with game flow."""

    def test_secret_objectives_persist_across_phases(self):
        """Test that secret objectives persist across game phases."""
        game_state = GameState()

        secret_obj = Objective(
            "sec1", "Secret 1", "Persistent secret", 1, False, GamePhase.STATUS
        )

        # Assign secret objective in setup phase
        state1 = game_state.assign_secret_objective("player1", secret_obj)

        # Advance through multiple phases
        state2 = state1.advance_to_next_status_phase()

        # Secret objective should still be in player's hand
        player_secrets = state2.get_player_secret_objectives("player1")
        assert len(player_secrets) == 1
        assert player_secrets[0].id == secret_obj.id

    def test_completed_secret_objectives_count_toward_victory(self):
        """Test that completed secret objectives count toward victory points."""
        game_state = GameState()

        # Create high-value secret objective
        secret_obj = Objective(
            "sec1", "Secret 1", "High value secret", 3, False, GamePhase.STATUS
        )

        # Assign and score secret objective
        state1 = game_state.assign_secret_objective("player1", secret_obj)
        state2 = state1.score_objective("player1", secret_obj, GamePhase.STATUS)

        # Check victory points
        assert state2.get_victory_points("player1") == 3
        assert state2.is_objective_completed("player1", secret_obj)

    def test_secret_objectives_revealed_when_scored(self):
        """Test that secret objectives are revealed to all players when scored."""
        game_state = GameState()

        secret_obj = Objective(
            "sec1", "Secret 1", "Revealed secret", 1, False, GamePhase.STATUS
        )

        # Assign secret objective to player1
        state1 = game_state.assign_secret_objective("player1", secret_obj)

        # Initially, other players cannot see the secret objective
        assert not state1.can_player_see_objective("player2", secret_obj)

        # Score the secret objective
        state2 = state1.score_objective("player1", secret_obj, GamePhase.STATUS)

        # Now all players should be able to see the completed objective
        assert state2.can_player_see_objective("player2", secret_obj)
        assert state2.is_objective_completed("player1", secret_obj)


class TestSecretObjectiveEdgeCases:
    """Test edge cases in secret objective system."""

    def test_cannot_assign_duplicate_secret_objectives(self):
        """Test that players cannot receive duplicate secret objectives."""
        game_state = GameState()

        secret_obj = Objective(
            "sec1", "Secret 1", "Unique secret", 1, False, GamePhase.STATUS
        )

        # Assign secret objective first time - should succeed
        state1 = game_state.assign_secret_objective("player1", secret_obj)

        # Try to assign same secret objective again - should fail
        with pytest.raises(ValueError, match="Player.*already has secret objective"):
            state1.assign_secret_objective("player1", secret_obj)

    def test_secret_objectives_removed_on_player_elimination(self):
        """Test that secret objectives are removed when player is eliminated."""
        game_state = GameState()

        secret_obj = Objective(
            "sec1", "Secret 1", "Lost secret", 1, False, GamePhase.STATUS
        )

        # Assign secret objective to player
        state1 = game_state.assign_secret_objective("player1", secret_obj)
        assert len(state1.get_player_secret_objectives("player1")) == 1

        # Eliminate player
        state2 = state1.eliminate_player("player1")

        # Player should no longer have secret objectives
        assert len(state2.get_player_secret_objectives("player1")) == 0

    def test_multiple_players_can_have_same_secret_objective_type(self):
        """Test that multiple players can have the same type of secret objective."""
        game_state = GameState()

        # Create identical secret objectives (different instances)
        secret_obj1 = Objective(
            "sec1a", "Control Planets", "Control 6 planets", 1, False, GamePhase.STATUS
        )
        secret_obj2 = Objective(
            "sec1b", "Control Planets", "Control 6 planets", 1, False, GamePhase.STATUS
        )

        # Assign to different players
        state1 = game_state.assign_secret_objective("player1", secret_obj1)
        state2 = state1.assign_secret_objective("player2", secret_obj2)

        # Both players should have their respective secret objectives
        player1_secrets = state2.get_player_secret_objectives("player1")
        player2_secrets = state2.get_player_secret_objectives("player2")

        assert len(player1_secrets) == 1
        assert len(player2_secrets) == 1
        assert player1_secrets[0].id == secret_obj1.id
        assert player2_secrets[0].id == secret_obj2.id

"""Tests for Stage I/II objective progression mechanics."""

import pytest

from src.ti4.core.constants import Expansion
from src.ti4.core.game_phase import GamePhase
from src.ti4.core.game_state import GameState
from src.ti4.core.objective import (
    AllObjectivesRevealedError,
    ObjectiveCard,
    ObjectiveCategory,
    ObjectiveRevealState,
    ObjectiveType,
    PublicObjectiveManager,
)


class TestObjectiveProgressionMechanics:
    """Test class for objective progression mechanics."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.manager = PublicObjectiveManager()
        self.game_state = GameState()

        # Create mock objective cards for testing
        self.stage_i_objectives = [
            ObjectiveCard(
                id=f"stage_i_{i}",
                name=f"Stage I Objective {i}",
                condition="Test condition",
                points=1,
                expansion=Expansion.BASE,
                phase=GamePhase.STATUS,
                type=ObjectiveType.PUBLIC_STAGE_I,
                requirement_validator=lambda p, g: True,
                category=ObjectiveCategory.PLANET_CONTROL,
                dependencies=[],
            )
            for i in range(1, 6)  # 5 Stage I objectives
        ]

        self.stage_ii_objectives = [
            ObjectiveCard(
                id=f"stage_ii_{i}",
                name=f"Stage II Objective {i}",
                condition="Test condition",
                points=2,
                expansion=Expansion.BASE,
                phase=GamePhase.STATUS,
                type=ObjectiveType.PUBLIC_STAGE_II,
                requirement_validator=lambda p, g: True,
                category=ObjectiveCategory.RESOURCE_SPENDING,
                dependencies=[],
            )
            for i in range(1, 6)  # 5 Stage II objectives
        ]

    def test_reveal_next_objective_method_exists(self) -> None:
        """Test that reveal_next_objective method exists."""
        assert hasattr(self.manager, "reveal_next_objective")
        assert callable(self.manager.reveal_next_objective)

    def test_check_game_end_condition_method_exists(self) -> None:
        """Test that check_game_end_condition method exists."""
        assert hasattr(self.manager, "check_game_end_condition")
        assert callable(self.manager.check_game_end_condition)

    def test_reveal_next_objective_requires_setup(self) -> None:
        """Test that reveal_next_objective requires objectives to be set up first."""
        with pytest.raises(ValueError, match="Objectives must be set up"):
            self.manager.reveal_next_objective("speaker_1")

    def test_check_game_end_condition_requires_setup(self) -> None:
        """Test that check_game_end_condition requires objectives to be set up first."""
        with pytest.raises(ValueError, match="Objectives must be set up"):
            self.manager.check_game_end_condition()

    def test_reveal_stage_i_objective_first(self) -> None:
        """Test that Stage I objectives are revealed first."""
        # Setup objectives with mock data
        self.manager._reveal_state = ObjectiveRevealState(
            revealed_stage_i=[],
            revealed_stage_ii=[],
            remaining_stage_i=self.stage_i_objectives.copy(),
            remaining_stage_ii=self.stage_ii_objectives.copy(),
            current_stage="stage_i",
        )

        # Reveal next objective should return a Stage I objective
        revealed = self.manager.reveal_next_objective("speaker_1")

        assert revealed.type == ObjectiveType.PUBLIC_STAGE_I
        assert revealed.id == "stage_i_1"

        # Check that reveal state is updated
        state = self.manager.get_reveal_state()
        assert len(state.revealed_stage_i) == 1
        assert len(state.remaining_stage_i) == 4
        assert state.current_stage == "stage_i"

    def test_reveal_all_stage_i_objectives(self) -> None:
        """Test revealing all Stage I objectives before moving to Stage II."""
        # Setup objectives with mock data
        self.manager._reveal_state = ObjectiveRevealState(
            revealed_stage_i=[],
            revealed_stage_ii=[],
            remaining_stage_i=self.stage_i_objectives.copy(),
            remaining_stage_ii=self.stage_ii_objectives.copy(),
            current_stage="stage_i",
        )

        # Reveal all 5 Stage I objectives
        for _ in range(5):
            revealed = self.manager.reveal_next_objective("speaker_1")
            assert revealed.type == ObjectiveType.PUBLIC_STAGE_I

        # Check that we've moved to Stage II
        state = self.manager.get_reveal_state()
        assert len(state.revealed_stage_i) == 5
        assert len(state.remaining_stage_i) == 0
        assert state.current_stage == "stage_ii"

    def test_reveal_stage_ii_after_stage_i_complete(self) -> None:
        """Test that Stage II objectives are revealed after all Stage I are revealed."""
        # Setup with all Stage I revealed
        self.manager._reveal_state = ObjectiveRevealState(
            revealed_stage_i=self.stage_i_objectives.copy(),
            revealed_stage_ii=[],
            remaining_stage_i=[],
            remaining_stage_ii=self.stage_ii_objectives.copy(),
            current_stage="stage_ii",
        )

        # Reveal next objective should return a Stage II objective
        revealed = self.manager.reveal_next_objective("speaker_1")

        assert revealed.type == ObjectiveType.PUBLIC_STAGE_II
        assert revealed.id == "stage_ii_1"

        # Check that reveal state is updated
        state = self.manager.get_reveal_state()
        assert len(state.revealed_stage_ii) == 1
        assert len(state.remaining_stage_ii) == 4
        assert state.current_stage == "stage_ii"

    def test_cannot_reveal_stage_ii_before_stage_i_complete(self) -> None:
        """Test that Stage II objectives cannot be revealed before all Stage I are revealed."""
        # Setup with some Stage I objectives remaining
        self.manager._reveal_state = ObjectiveRevealState(
            revealed_stage_i=self.stage_i_objectives[:3],  # Only 3 revealed
            revealed_stage_ii=[],
            remaining_stage_i=self.stage_i_objectives[3:],  # 2 remaining
            remaining_stage_ii=self.stage_ii_objectives.copy(),
            current_stage="stage_i",
        )

        # Should still reveal Stage I objectives
        revealed = self.manager.reveal_next_objective("speaker_1")
        assert revealed.type == ObjectiveType.PUBLIC_STAGE_I

    def test_game_end_condition_false_when_objectives_remain(self) -> None:
        """Test that game end condition is false when objectives remain."""
        # Setup with objectives remaining
        self.manager._reveal_state = ObjectiveRevealState(
            revealed_stage_i=self.stage_i_objectives[:3],
            revealed_stage_ii=[],
            remaining_stage_i=self.stage_i_objectives[3:],
            remaining_stage_ii=self.stage_ii_objectives.copy(),
            current_stage="stage_i",
        )

        assert not self.manager.check_game_end_condition()

    def test_game_end_condition_false_when_stage_ii_remains(self) -> None:
        """Test that game end condition is false when Stage II objectives remain."""
        # Setup with all Stage I revealed but Stage II remaining
        self.manager._reveal_state = ObjectiveRevealState(
            revealed_stage_i=self.stage_i_objectives.copy(),
            revealed_stage_ii=self.stage_ii_objectives[:2],
            remaining_stage_i=[],
            remaining_stage_ii=self.stage_ii_objectives[2:],
            current_stage="stage_ii",
        )

        assert not self.manager.check_game_end_condition()

    def test_game_end_condition_true_when_all_objectives_revealed(self) -> None:
        """Test that game end condition is true when all objectives are revealed."""
        # Setup with all objectives revealed
        self.manager._reveal_state = ObjectiveRevealState(
            revealed_stage_i=self.stage_i_objectives.copy(),
            revealed_stage_ii=self.stage_ii_objectives.copy(),
            remaining_stage_i=[],
            remaining_stage_ii=[],
            current_stage="complete",
        )

        assert self.manager.check_game_end_condition()

    def test_reveal_objective_when_all_revealed_raises_error(self) -> None:
        """Test that revealing objective when all are revealed raises an error."""
        # Setup with all objectives revealed
        self.manager._reveal_state = ObjectiveRevealState(
            revealed_stage_i=self.stage_i_objectives.copy(),
            revealed_stage_ii=self.stage_ii_objectives.copy(),
            remaining_stage_i=[],
            remaining_stage_ii=[],
            current_stage="complete",
        )

        with pytest.raises(
            AllObjectivesRevealedError, match="All public objectives have been revealed"
        ):
            self.manager.reveal_next_objective("speaker_1")

    def test_reveal_objective_updates_current_stage_to_complete(self) -> None:
        """Test that revealing the last objective updates current_stage to complete."""
        # Setup with only one Stage II objective remaining
        self.manager._reveal_state = ObjectiveRevealState(
            revealed_stage_i=self.stage_i_objectives.copy(),
            revealed_stage_ii=self.stage_ii_objectives[:-1],  # All but last
            remaining_stage_i=[],
            remaining_stage_ii=[self.stage_ii_objectives[-1]],  # Only last one
            current_stage="stage_ii",
        )

        # Reveal the last objective
        revealed = self.manager.reveal_next_objective("speaker_1")
        assert revealed.type == ObjectiveType.PUBLIC_STAGE_II

        # Check that current_stage is now complete
        state = self.manager.get_reveal_state()
        assert state.current_stage == "complete"
        assert len(state.remaining_stage_ii) == 0

    def test_get_available_objectives_for_scoring_method_exists(self) -> None:
        """Test that get_available_objectives_for_scoring method exists."""
        assert hasattr(self.manager, "get_available_objectives_for_scoring")
        assert callable(self.manager.get_available_objectives_for_scoring)

    def test_get_available_objectives_returns_revealed_objectives(self) -> None:
        """Test that get_available_objectives_for_scoring returns revealed objectives."""
        # Setup with some objectives revealed
        revealed_stage_i = self.stage_i_objectives[:2]
        revealed_stage_ii = self.stage_ii_objectives[:1]

        self.manager._reveal_state = ObjectiveRevealState(
            revealed_stage_i=revealed_stage_i,
            revealed_stage_ii=revealed_stage_ii,
            remaining_stage_i=self.stage_i_objectives[2:],
            remaining_stage_ii=self.stage_ii_objectives[1:],
            current_stage="stage_ii",
        )

        available = self.manager.get_available_objectives_for_scoring()

        # Should return all revealed objectives
        assert len(available) == 3
        assert all(obj in available for obj in revealed_stage_i)
        assert all(obj in available for obj in revealed_stage_ii)

    def test_get_available_objectives_requires_setup(self) -> None:
        """Test that get_available_objectives_for_scoring requires setup."""
        with pytest.raises(ValueError, match="Objectives must be set up"):
            self.manager.get_available_objectives_for_scoring()

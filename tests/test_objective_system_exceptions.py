"""Tests for objective system custom exceptions and error handling.

This module tests all custom exception types and error handling scenarios
for the Rule 61 objective system implementation.

LRR References:
- Rule 61: OBJECTIVE CARDS
- Requirements 7.2, 7.3, 7.4, 7.5
"""

import pytest

from src.ti4.core.objective import (
    AllObjectivesRevealedError,
    HomeSystemControlError,
    InvalidObjectivePhaseError,
    ObjectiveAlreadyScoredError,
    ObjectiveNotEligibleError,
    ObjectiveSystemError,
)


class TestObjectiveSystemExceptions:
    """Test custom exception types for the objective system."""

    def test_objective_system_error_is_base_exception(self) -> None:
        """Test that ObjectiveSystemError is the base exception type."""
        error = ObjectiveSystemError("Test error")
        assert isinstance(error, Exception)
        assert str(error) == "Test error"

    def test_home_system_control_error_inherits_from_base(self) -> None:
        """Test that HomeSystemControlError inherits from ObjectiveSystemError."""
        error = HomeSystemControlError("Home system not controlled")
        assert isinstance(error, ObjectiveSystemError)
        assert isinstance(error, Exception)
        assert str(error) == "Home system not controlled"

    def test_objective_already_scored_error_inherits_from_base(self) -> None:
        """Test that ObjectiveAlreadyScoredError inherits from ObjectiveSystemError."""
        error = ObjectiveAlreadyScoredError("Objective already scored")
        assert isinstance(error, ObjectiveSystemError)
        assert str(error) == "Objective already scored"

    def test_objective_not_eligible_error_inherits_from_base(self) -> None:
        """Test that ObjectiveNotEligibleError inherits from ObjectiveSystemError."""
        error = ObjectiveNotEligibleError("Requirements not met")
        assert isinstance(error, ObjectiveSystemError)
        assert str(error) == "Requirements not met"

    def test_invalid_objective_phase_error_inherits_from_base(self) -> None:
        """Test that InvalidObjectivePhaseError inherits from ObjectiveSystemError."""
        error = InvalidObjectivePhaseError("Wrong phase for scoring")
        assert isinstance(error, ObjectiveSystemError)
        assert str(error) == "Wrong phase for scoring"

    def test_all_objectives_revealed_error_inherits_from_base(self) -> None:
        """Test that AllObjectivesRevealedError inherits from ObjectiveSystemError."""
        error = AllObjectivesRevealedError("All objectives revealed")
        assert isinstance(error, ObjectiveSystemError)
        assert str(error) == "All objectives revealed"


class TestObjectiveSystemErrorMessages:
    """Test error message formatting and content."""

    def test_home_system_control_error_with_planet_details(self) -> None:
        """Test HomeSystemControlError with specific planet information."""
        planets = ["Mecatol Rex", "Archon Ren"]
        error_msg = f"Player must control all home system planets. Missing: {', '.join(planets)}"
        error = HomeSystemControlError(error_msg)

        assert "Mecatol Rex" in str(error)
        assert "Archon Ren" in str(error)
        assert "must control all home system planets" in str(error)

    def test_objective_not_eligible_error_with_requirement_details(self) -> None:
        """Test ObjectiveNotEligibleError with specific requirement information."""
        error_msg = "Cannot score 'Corner the Market': Need 4 planets with same trait, currently have 2"
        error = ObjectiveNotEligibleError(error_msg)

        assert "Corner the Market" in str(error)
        assert "4 planets with same trait" in str(error)
        assert "currently have 2" in str(error)

    def test_invalid_objective_phase_error_with_phase_details(self) -> None:
        """Test InvalidObjectivePhaseError with phase information."""
        error_msg = "Cannot score objective during Action phase. Secret objectives can only be scored during Status phase."
        error = InvalidObjectivePhaseError(error_msg)

        assert "Action phase" in str(error)
        assert "Status phase" in str(error)
        assert "Secret objectives" in str(error)

    def test_objective_already_scored_error_with_objective_details(self) -> None:
        """Test ObjectiveAlreadyScoredError with objective information."""
        error_msg = "Objective 'Expand Borders' has already been scored by player_1"
        error = ObjectiveAlreadyScoredError(error_msg)

        assert "Expand Borders" in str(error)
        assert "already been scored" in str(error)
        assert "player_1" in str(error)

    def test_all_objectives_revealed_error_with_game_end_message(self) -> None:
        """Test AllObjectivesRevealedError with game end information."""
        error_msg = (
            "All public objectives have been revealed. The game ends immediately."
        )
        error = AllObjectivesRevealedError(error_msg)

        assert "All public objectives" in str(error)
        assert "game ends immediately" in str(error)


class TestExceptionHierarchy:
    """Test that exception hierarchy allows proper catching."""

    def test_can_catch_all_objective_errors_with_base_exception(self) -> None:
        """Test that all objective errors can be caught with ObjectiveSystemError."""
        exceptions = [
            HomeSystemControlError("test"),
            ObjectiveAlreadyScoredError("test"),
            ObjectiveNotEligibleError("test"),
            InvalidObjectivePhaseError("test"),
            AllObjectivesRevealedError("test"),
        ]

        for exception in exceptions:
            try:
                raise exception
            except ObjectiveSystemError:
                # Should catch all objective system errors
                pass
            except Exception:
                pytest.fail(
                    f"Failed to catch {type(exception).__name__} with ObjectiveSystemError"
                )

    def test_can_catch_specific_exception_types(self) -> None:
        """Test that specific exception types can be caught individually."""
        # Test HomeSystemControlError
        try:
            raise HomeSystemControlError("test")
        except HomeSystemControlError:
            pass
        except Exception:
            pytest.fail("Failed to catch HomeSystemControlError specifically")

        # Test ObjectiveNotEligibleError
        try:
            raise ObjectiveNotEligibleError("test")
        except ObjectiveNotEligibleError:
            pass
        except Exception:
            pytest.fail("Failed to catch ObjectiveNotEligibleError specifically")

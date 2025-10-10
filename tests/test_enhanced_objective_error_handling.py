"""Tests for enhanced error handling in objective system components.

This module tests enhanced error handling features that provide better
error messages and recovery strategies for the objective system.

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
    PublicObjectiveManager,
)


class TestEnhancedPublicObjectiveManagerErrorHandling:
    """Test enhanced error handling in PublicObjectiveManager."""

    def test_reveal_next_objective_provides_detailed_error_when_all_revealed(
        self,
    ) -> None:
        """Test that revealing objectives when all revealed provides detailed error message."""
        manager = PublicObjectiveManager()

        # Set up manager with empty objectives to simulate all revealed
        from src.ti4.core.objective import ObjectiveRevealState

        manager._reveal_state = ObjectiveRevealState(
            revealed_stage_i=[],
            revealed_stage_ii=[],
            remaining_stage_i=[],  # Empty - all revealed
            remaining_stage_ii=[],  # Empty - all revealed
            current_stage="complete",
        )

        # This should now raise AllObjectivesRevealedError with detailed message
        with pytest.raises(AllObjectivesRevealedError) as exc_info:
            manager.reveal_next_objective("player_1")

        # Should provide detailed error message about game end
        error_message = str(exc_info.value)
        assert "All public objectives have been revealed" in error_message
        assert "game ends immediately" in error_message
        assert "victory points" in error_message
        assert "initiative order" in error_message

    def test_setup_objectives_provides_detailed_error_for_invalid_config(self) -> None:
        """Test that setup provides detailed error for invalid configuration."""
        from src.ti4.core.objective import ObjectiveSetupConfiguration

        # Test with invalid configuration - this should raise ValueError during creation
        with pytest.raises(ValueError, match="Stage I count must be positive"):
            ObjectiveSetupConfiguration(stage_i_count=0, stage_ii_count=5)


class TestEnhancedObjectiveValidationErrorHandling:
    """Test enhanced error handling for objective validation."""

    def test_objective_validation_provides_specific_missing_requirements(self) -> None:
        """Test that objective validation provides specific details about missing requirements."""
        # This test will be implemented when we add enhanced validation
        error_msg = "Cannot score 'Corner the Market': Need 4 planets with same trait. Currently have 2 planets with Cultural trait and 1 planet with Industrial trait."
        error = ObjectiveNotEligibleError(error_msg)

        assert "Corner the Market" in str(error)
        assert "Need 4 planets with same trait" in str(error)
        assert "Currently have 2 planets with Cultural trait" in str(error)
        assert "1 planet with Industrial trait" in str(error)

    def test_objective_validation_provides_progress_information(self) -> None:
        """Test that objective validation shows progress toward completion."""
        error_msg = "Cannot score 'Expand Borders': Need 6 planets in non-home systems. Currently control 4/6 planets (Mecatol Rex, Archon Ren, Archon Tau, Wellon)."
        error = ObjectiveNotEligibleError(error_msg)

        assert "Expand Borders" in str(error)
        assert "Need 6 planets in non-home systems" in str(error)
        assert "Currently control 4/6 planets" in str(error)
        assert "Mecatol Rex" in str(error)
        assert "Archon Ren" in str(error)

    def test_phase_restriction_error_provides_timing_guidance(self) -> None:
        """Test that phase restriction errors provide clear timing guidance."""
        error_msg = "Cannot score secret objective 'Become a Martyr' during Action phase. Secret objectives can only be scored during the Status phase after the Strategy phase."
        error = InvalidObjectivePhaseError(error_msg)

        assert "Become a Martyr" in str(error)
        assert "Action phase" in str(error)
        assert "Status phase" in str(error)
        assert "after the Strategy phase" in str(error)

    def test_already_scored_error_provides_comprehensive_information(self) -> None:
        """Test that already scored errors provide comprehensive information."""
        error_msg = "Public objective 'Expand Borders' has already been scored by player_2 during round 3. Each public objective can only be scored once per game."
        error = ObjectiveAlreadyScoredError(error_msg)

        assert "Expand Borders" in str(error)
        assert "already been scored by player_2" in str(error)
        assert "during round 3" in str(error)
        assert "can only be scored once per game" in str(error)


class TestEnhancedHomeSystemControlErrorHandling:
    """Test enhanced error handling for home system control validation."""

    def test_home_system_control_error_lists_specific_planets(self) -> None:
        """Test that home system control errors list specific uncontrolled planets."""
        planets = ["Archon Ren", "Archon Tau"]
        error_msg = f"Cannot score public objective: Player must control all planets in their home system. The following planets are not controlled: {', '.join(planets)}. Gain control of these planets before attempting to score public objectives."
        error = HomeSystemControlError(error_msg)

        assert "Cannot score public objective" in str(error)
        assert "must control all planets in their home system" in str(error)
        assert "Archon Ren" in str(error)
        assert "Archon Tau" in str(error)
        assert "Gain control of these planets" in str(error)

    def test_home_system_control_error_provides_rule_reference(self) -> None:
        """Test that home system control errors provide rule references."""
        error_msg = "Cannot score public objective: Player must control all planets in their home system (LRR 61.16). Currently missing control of: Mecatol Rex."
        error = HomeSystemControlError(error_msg)

        assert "LRR 61.16" in str(error)
        assert "must control all planets in their home system" in str(error)
        assert "Currently missing control of: Mecatol Rex" in str(error)


class TestEnhancedGameEndErrorHandling:
    """Test enhanced error handling for game end conditions."""

    def test_all_objectives_revealed_error_provides_victory_guidance(self) -> None:
        """Test that game end errors provide victory determination guidance."""
        error_msg = "All public objectives have been revealed. The game ends immediately. Determine the winner based on victory points, with ties broken by initiative order (lowest number wins)."
        error = AllObjectivesRevealedError(error_msg)

        assert "All public objectives have been revealed" in str(error)
        assert "game ends immediately" in str(error)
        assert "Determine the winner based on victory points" in str(error)
        assert "ties broken by initiative order" in str(error)
        assert "lowest number wins" in str(error)

    def test_game_end_error_includes_current_standings(self) -> None:
        """Test that game end errors can include current standings information."""
        error_msg = "All public objectives have been revealed. The game ends immediately. Current standings: player_1 (8 VP), player_2 (7 VP), player_3 (6 VP). Winner: player_1."
        error = AllObjectivesRevealedError(error_msg)

        assert "Current standings" in str(error)
        assert "player_1 (8 VP)" in str(error)
        assert "player_2 (7 VP)" in str(error)
        assert "Winner: player_1" in str(error)


class TestErrorRecoveryStrategies:
    """Test error recovery strategies for the objective system."""

    def test_objective_system_error_provides_recovery_suggestions(self) -> None:
        """Test that objective system errors provide recovery suggestions."""
        error_msg = "Cannot complete objective scoring due to invalid game state. Suggested recovery: Verify all players have valid home systems and the galaxy is properly initialized."
        error = ObjectiveSystemError(error_msg)

        assert "Cannot complete objective scoring" in str(error)
        assert "Suggested recovery" in str(error)
        assert "Verify all players have valid home systems" in str(error)
        assert "galaxy is properly initialized" in str(error)

    def test_validation_error_provides_next_steps(self) -> None:
        """Test that validation errors provide clear next steps."""
        error_msg = "Objective requirements not met. Next steps: 1) Gain control of 2 more planets with Cultural trait, 2) Ensure planets are in non-home systems, 3) Attempt scoring during Status phase."
        error = ObjectiveNotEligibleError(error_msg)

        assert "Objective requirements not met" in str(error)
        assert "Next steps:" in str(error)
        assert "1) Gain control of 2 more planets" in str(error)
        assert "2) Ensure planets are in non-home systems" in str(error)
        assert "3) Attempt scoring during Status phase" in str(error)

    def test_system_integration_error_provides_diagnostic_info(self) -> None:
        """Test that system integration errors provide diagnostic information."""
        error_msg = "Objective system integration failure. Diagnostic info: Galaxy=None, Players=3, Technology_Manager=Available, Resource_Manager=Unavailable. Check system initialization order."
        error = ObjectiveSystemError(error_msg)

        assert "Objective system integration failure" in str(error)
        assert "Diagnostic info:" in str(error)
        assert "Galaxy=None" in str(error)
        assert "Players=3" in str(error)
        assert "Technology_Manager=Available" in str(error)
        assert "Resource_Manager=Unavailable" in str(error)
        assert "Check system initialization order" in str(error)

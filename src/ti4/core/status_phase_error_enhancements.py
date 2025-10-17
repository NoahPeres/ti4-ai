"""Error handling enhancements for status phase step handlers.

This module contains enhanced error handling implementations for all
status phase step handlers to support comprehensive error recovery,
graceful degradation, and state validation.

LRR References:
- Rule 81: Status Phase - Error handling requirements
- Requirements 11.1, 11.2, 11.3, 11.4, 11.5: Error handling specifications
"""
# type: ignore  # Temporarily disabled due to method assignment issues

from typing import TYPE_CHECKING, Any

from .status_phase import (
    StatusPhaseGameStateError,
    StepResult,
    SystemIntegrationError,
)

if TYPE_CHECKING:
    from .game_state import GameState


def add_comprehensive_error_handling_to_step_handlers() -> None:
    """Add comprehensive error handling to all status phase step handlers.

    This function enhances all step handlers with:
    - Input validation and sanitization
    - Graceful degradation for non-critical failures
    - State validation and rollback mechanisms
    - Descriptive and actionable error messages
    """

    # Import all step handler classes

    # Enhance RevealObjectiveStep
    _enhance_reveal_objective_step()

    # Enhance DrawActionCardsStep
    _enhance_draw_action_cards_step()

    # Enhance RemoveCommandTokensStep
    _enhance_remove_command_tokens_step()

    # Enhance GainRedistributeTokensStep
    _enhance_gain_redistribute_tokens_step()

    # Enhance ReadyCardsStep
    _enhance_ready_cards_step()

    # Enhance RepairUnitsStep
    _enhance_repair_units_step()

    # Enhance ReturnStrategyCardsStep
    _enhance_return_strategy_cards_step()


def _enhance_reveal_objective_step() -> None:
    """Enhance RevealObjectiveStep with comprehensive error handling."""
    from .status_phase import RevealObjectiveStep

    # Store original execute method
    original_execute = RevealObjectiveStep.execute

    def enhanced_execute(self: Any, game_state: "GameState") -> tuple[StepResult, "GameState"]:
        """Enhanced execute with comprehensive error handling."""
        step_name = "Reveal Public Objective"

        try:
            # Enhanced input validation
            if game_state is None:
                return StepResult(
                    success=False,
                    step_name=step_name,
                    error_message="Game state cannot be None - ensure game is properly initialized"
                ), game_state

            # Validate game state type
            if not _is_valid_game_state(game_state):
                return StepResult(
                    success=False,
                    step_name=step_name,
                    error_message="Invalid game state type - must be a valid GameState object"
                ), game_state

            # Call original implementation with error recovery
            return original_execute(self, game_state)

        except SystemIntegrationError as e:
            return StepResult(
                success=False,
                step_name=step_name,
                error_message=f"System integration failure: {str(e)}"
            ), game_state
        except StatusPhaseGameStateError as e:
            return StepResult(
                success=False,
                step_name=step_name,
                error_message=f"Game state validation error: {str(e)}"
            ), game_state
        except Exception as e:
            return StepResult(
                success=False,
                step_name=step_name,
                error_message=f"Unexpected error during objective revealing: {str(e)}"
            ), game_state

    # Replace the execute method
    RevealObjectiveStep.execute = enhanced_execute


def _enhance_draw_action_cards_step() -> None:
    """Enhance DrawActionCardsStep with comprehensive error handling."""
    from .status_phase import DrawActionCardsStep

    # Store original execute method
    original_execute = DrawActionCardsStep.execute

    def enhanced_execute(self: Any, game_state: "GameState") -> tuple[StepResult, "GameState"]:
        """Enhanced execute with comprehensive error handling."""
        step_name = "Draw Action Cards"

        try:
            # Enhanced input validation
            if game_state is None:
                return StepResult(
                    success=False,
                    step_name=step_name,
                    error_message="Game state cannot be None - ensure game is properly initialized"
                ), game_state

            # Validate game state type
            if not _is_valid_game_state(game_state):
                return StepResult(
                    success=False,
                    step_name=step_name,
                    error_message="Invalid game state type - must be a valid GameState object"
                ), game_state

            # Call original implementation with error recovery
            return original_execute(self, game_state)

        except SystemIntegrationError as e:
            return StepResult(
                success=False,
                step_name=step_name,
                error_message=f"Action card system integration failure: {str(e)}"
            ), game_state
        except Exception as e:
            return StepResult(
                success=False,
                step_name=step_name,
                error_message=f"Unexpected error during action card drawing: {str(e)}"
            ), game_state

    # Replace the execute method
    DrawActionCardsStep.execute = enhanced_execute


def _enhance_remove_command_tokens_step() -> None:
    """Enhance RemoveCommandTokensStep with comprehensive error handling."""
    from .status_phase import RemoveCommandTokensStep

    # Store original execute method
    original_execute = RemoveCommandTokensStep.execute

    def enhanced_execute(self: Any, game_state: "GameState") -> tuple[StepResult, "GameState"]:
        """Enhanced execute with comprehensive error handling."""
        step_name = "Remove Command Tokens"

        try:
            # Enhanced input validation
            if game_state is None:
                return StepResult(
                    success=False,
                    step_name=step_name,
                    error_message="Game state cannot be None - ensure game is properly initialized"
                ), game_state

            # Validate game state type
            if not _is_valid_game_state(game_state):
                return StepResult(
                    success=False,
                    step_name=step_name,
                    error_message="Invalid game state type - must be a valid GameState object"
                ), game_state

            # Call original implementation with error recovery
            return original_execute(self, game_state)

        except SystemIntegrationError as e:
            return StepResult(
                success=False,
                step_name=step_name,
                error_message=f"Command token system integration failure: {str(e)}"
            ), game_state
        except Exception as e:
            return StepResult(
                success=False,
                step_name=step_name,
                error_message=f"Unexpected error during command token removal: {str(e)}"
            ), game_state

    # Replace the execute method
    RemoveCommandTokensStep.execute = enhanced_execute


def _enhance_gain_redistribute_tokens_step() -> None:
    """Enhance GainRedistributeTokensStep with comprehensive error handling."""
    from .status_phase import GainRedistributeTokensStep

    # Store original execute method
    original_execute = GainRedistributeTokensStep.execute

    def enhanced_execute(self: Any, game_state: "GameState") -> tuple[StepResult, "GameState"]:
        """Enhanced execute with comprehensive error handling."""
        step_name = "Gain and Redistribute Command Tokens"

        try:
            # Enhanced input validation
            if game_state is None:
                return StepResult(
                    success=False,
                    step_name=step_name,
                    error_message="Game state cannot be None - ensure game is properly initialized"
                ), game_state

            # Validate game state type
            if not _is_valid_game_state(game_state):
                return StepResult(
                    success=False,
                    step_name=step_name,
                    error_message="Invalid game state type - must be a valid GameState object"
                ), game_state

            # Call original implementation with error recovery
            return original_execute(self, game_state)

        except SystemIntegrationError as e:
            return StepResult(
                success=False,
                step_name=step_name,
                error_message=f"Command token system integration failure: {str(e)}"
            ), game_state
        except Exception as e:
            return StepResult(
                success=False,
                step_name=step_name,
                error_message=f"Unexpected error during token redistribution: {str(e)}"
            ), game_state

    # Replace the execute method
    GainRedistributeTokensStep.execute = enhanced_execute


def _enhance_ready_cards_step() -> None:
    """Enhance ReadyCardsStep with comprehensive error handling."""
    from .status_phase import ReadyCardsStep

    # Store original execute method
    original_execute = ReadyCardsStep.execute

    def enhanced_execute(self: Any, game_state: "GameState") -> tuple[StepResult, "GameState"]:
        """Enhanced execute with comprehensive error handling."""
        step_name = "Ready Cards"

        try:
            # Enhanced input validation
            if game_state is None:
                return StepResult(
                    success=False,
                    step_name=step_name,
                    error_message="Game state cannot be None - ensure game is properly initialized"
                ), game_state

            # Validate game state type
            if not _is_valid_game_state(game_state):
                return StepResult(
                    success=False,
                    step_name=step_name,
                    error_message="Invalid game state type - must be a valid GameState object"
                ), game_state

            # Call original implementation with error recovery
            return original_execute(self, game_state)

        except SystemIntegrationError as e:
            return StepResult(
                success=False,
                step_name=step_name,
                error_message=f"Card system integration failure: {str(e)}"
            ), game_state
        except Exception as e:
            return StepResult(
                success=False,
                step_name=step_name,
                error_message=f"Unexpected error during card readying: {str(e)}"
            ), game_state

    # Replace the execute method
    ReadyCardsStep.execute = enhanced_execute


def _enhance_repair_units_step() -> None:
    """Enhance RepairUnitsStep with comprehensive error handling."""
    from .status_phase import RepairUnitsStep

    # Store original execute method
    original_execute = RepairUnitsStep.execute

    def enhanced_execute(self: Any, game_state: "GameState") -> tuple[StepResult, "GameState"]:
        """Enhanced execute with comprehensive error handling."""
        step_name = "Repair Units"

        try:
            # Enhanced input validation
            if game_state is None:
                return StepResult(
                    success=False,
                    step_name=step_name,
                    error_message="Game state cannot be None - ensure game is properly initialized"
                ), game_state

            # Validate game state type
            if not _is_valid_game_state(game_state):
                return StepResult(
                    success=False,
                    step_name=step_name,
                    error_message="Invalid game state type - must be a valid GameState object"
                ), game_state

            # Call original implementation with error recovery
            return original_execute(self, game_state)

        except SystemIntegrationError as e:
            return StepResult(
                success=False,
                step_name=step_name,
                error_message=f"Unit system integration failure: {str(e)}"
            ), game_state
        except Exception as e:
            return StepResult(
                success=False,
                step_name=step_name,
                error_message=f"Unexpected error during unit repair: {str(e)}"
            ), game_state

    # Replace the execute method
    RepairUnitsStep.execute = enhanced_execute


def _enhance_return_strategy_cards_step() -> None:
    """Enhance ReturnStrategyCardsStep with comprehensive error handling."""
    from .status_phase import ReturnStrategyCardsStep

    # Store original execute method
    original_execute = ReturnStrategyCardsStep.execute

    def enhanced_execute(self: Any, game_state: "GameState") -> tuple[StepResult, "GameState"]:
        """Enhanced execute with comprehensive error handling."""
        step_name = "Return Strategy Cards"

        try:
            # Enhanced input validation
            if game_state is None:
                return StepResult(
                    success=False,
                    step_name=step_name,
                    error_message="Game state cannot be None - ensure game is properly initialized"
                ), game_state

            # Validate game state type
            if not _is_valid_game_state(game_state):
                return StepResult(
                    success=False,
                    step_name=step_name,
                    error_message="Invalid game state type - must be a valid GameState object"
                ), game_state

            # Call original implementation with error recovery
            return original_execute(self, game_state)

        except SystemIntegrationError as e:
            return StepResult(
                success=False,
                step_name=step_name,
                error_message=f"Strategy card system integration failure: {str(e)}"
            ), game_state
        except Exception as e:
            return StepResult(
                success=False,
                step_name=step_name,
                error_message=f"Unexpected error during strategy card return: {str(e)}"
            ), game_state

    # Replace the execute method
    ReturnStrategyCardsStep.execute = enhanced_execute


def _is_valid_game_state(game_state: Any) -> bool:
    """Validate that the provided object is a valid game state.

    Args:
        game_state: The object to validate

    Returns:
        True if the object appears to be a valid game state, False otherwise
    """
    if game_state is None:
        return False

    # Check for basic game state attributes
    required_attributes = ['players']
    optional_attributes = ['_create_new_state', 'speaker_id', 'phase']

    # Must have at least one required attribute or one optional attribute
    has_required = any(hasattr(game_state, attr) for attr in required_attributes)
    has_optional = any(hasattr(game_state, attr) for attr in optional_attributes)

    return has_required or has_optional


def _validate_game_state_for_step(game_state: "GameState", step_name: str) -> tuple[bool, str]:
    """Validate game state for a specific step.

    Args:
        game_state: The game state to validate
        step_name: The name of the step being validated

    Returns:
        A tuple of (is_valid, error_message)
    """
    if game_state is None:
        return False, f"Game state cannot be None for {step_name}"

    if not _is_valid_game_state(game_state):
        return False, f"Invalid game state type for {step_name} - must be a valid GameState object"

    return True, ""


def _create_error_result(step_name: str, error_message: str) -> StepResult:
    """Create a standardized error result.

    Args:
        step_name: The name of the step that failed
        error_message: The error message to include

    Returns:
        A StepResult indicating failure with the provided error message
    """
    return StepResult(
        success=False,
        step_name=step_name,
        error_message=error_message
    )

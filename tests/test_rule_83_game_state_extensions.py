"""Tests for Rule 83: STRATEGY CARD game state extensions.

This module tests the minimal extensions to GameState for strategy card tracking.
All tests follow strict TDD methodology with RED-GREEN-REFACTOR cycles.

Rule 83 requirements tested:
- 1.3: Strategy card tracking in game state
- 4.5: State persistence for card assignments and exhaustion
- 6.2: State synchronization with StrategyCardCoordinator
- 10.2: Round management state tracking
"""

import pytest


class TestRule83GameStateExtensions:
    """Test GameState extensions for strategy card tracking."""

    def test_game_state_has_strategy_card_assignments_field(self) -> None:
        """Test that GameState has strategy card assignments field.

        Requirements: 1.3, 4.5 - Strategy card tracking in game state
        """
        from src.ti4.core.game_state import GameState

        # RED: This will fail until we add the field
        state = GameState()
        assert hasattr(state, 'strategy_card_assignments')
        assert isinstance(state.strategy_card_assignments, dict)

    def test_game_state_has_exhausted_strategy_cards_field(self) -> None:
        """Test that GameState has exhausted strategy cards field.

        Requirements: 4.5 - State persistence for card exhaustion
        """
        from src.ti4.core.game_state import GameState

        # RED: This will fail until we add the field
        state = GameState()
        assert hasattr(state, 'exhausted_strategy_cards')
        assert isinstance(state.exhausted_strategy_cards, set)

    def test_game_state_can_track_strategy_card_assignment(self) -> None:
        """Test that GameState can track strategy card assignments.

        Requirements: 1.3, 6.2 - Strategy card tracking and state synchronization
        """
        from src.ti4.core.game_state import GameState
        from src.ti4.core.strategic_action import StrategyCardType

        # RED: This will fail until we implement the functionality
        state = GameState()

        # Should be able to assign a strategy card to a player
        new_state = state.assign_strategy_card("player1", StrategyCardType.LEADERSHIP)
        assert new_state.strategy_card_assignments["player1"] == StrategyCardType.LEADERSHIP

    def test_game_state_can_track_strategy_card_exhaustion(self) -> None:
        """Test that GameState can track strategy card exhaustion.

        Requirements: 4.5 - State persistence for card exhaustion
        """
        from src.ti4.core.game_state import GameState
        from src.ti4.core.strategic_action import StrategyCardType

        # RED: This will fail until we implement the functionality
        state = GameState()

        # Should be able to exhaust a strategy card
        new_state = state.exhaust_strategy_card(StrategyCardType.LEADERSHIP)
        assert StrategyCardType.LEADERSHIP in new_state.exhausted_strategy_cards

    def test_game_state_can_ready_strategy_card(self) -> None:
        """Test that GameState can ready strategy cards.

        Requirements: 4.5, 10.2 - State persistence and round management
        """
        from src.ti4.core.game_state import GameState
        from src.ti4.core.strategic_action import StrategyCardType

        # RED: This will fail until we implement the functionality
        state = GameState()

        # Exhaust a card first
        exhausted_state = state.exhaust_strategy_card(StrategyCardType.LEADERSHIP)
        assert StrategyCardType.LEADERSHIP in exhausted_state.exhausted_strategy_cards

        # Then ready it
        readied_state = exhausted_state.ready_strategy_card(StrategyCardType.LEADERSHIP)
        assert StrategyCardType.LEADERSHIP not in readied_state.exhausted_strategy_cards

    def test_game_state_can_ready_all_strategy_cards(self) -> None:
        """Test that GameState can ready all strategy cards for round reset.

        Requirements: 10.2 - Round management state tracking
        """
        from src.ti4.core.game_state import GameState
        from src.ti4.core.strategic_action import StrategyCardType

        # RED: This will fail until we implement the functionality
        state = GameState()

        # Exhaust multiple cards
        state = state.exhaust_strategy_card(StrategyCardType.LEADERSHIP)
        state = state.exhaust_strategy_card(StrategyCardType.WARFARE)
        assert len(state.exhausted_strategy_cards) == 2

        # Ready all cards
        new_state = state.ready_all_strategy_cards()
        assert len(new_state.exhausted_strategy_cards) == 0

    def test_game_state_can_clear_strategy_card_assignments(self) -> None:
        """Test that GameState can clear strategy card assignments for round reset.

        Requirements: 10.2 - Round management state tracking
        """
        from src.ti4.core.game_state import GameState
        from src.ti4.core.strategic_action import StrategyCardType

        # RED: This will fail until we implement the functionality
        state = GameState()

        # Assign cards to players
        state = state.assign_strategy_card("player1", StrategyCardType.LEADERSHIP)
        state = state.assign_strategy_card("player2", StrategyCardType.WARFARE)
        assert len(state.strategy_card_assignments) == 2

        # Clear assignments
        new_state = state.clear_strategy_card_assignments()
        assert len(new_state.strategy_card_assignments) == 0

    def test_game_state_synchronizes_with_coordinator(self) -> None:
        """Test that GameState can synchronize with StrategyCardCoordinator.

        Requirements: 6.2 - State synchronization with StrategyCardCoordinator
        """
        from src.ti4.core.game_state import GameState
        from src.ti4.core.strategic_action import (
            StrategicActionManager,
            StrategyCardType,
        )
        from src.ti4.core.strategy_card_coordinator import StrategyCardCoordinator

        # RED: This will fail until we implement the functionality
        state = GameState()
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Assign cards in coordinator
        coordinator.assign_strategy_card("player1", StrategyCardType.LEADERSHIP)
        coordinator.exhaust_strategy_card("player1", StrategyCardType.LEADERSHIP)

        # Synchronize state
        new_state = state.synchronize_with_coordinator(coordinator)
        assert new_state.strategy_card_assignments["player1"] == StrategyCardType.LEADERSHIP
        assert StrategyCardType.LEADERSHIP in new_state.exhausted_strategy_cards

    def test_game_state_maintains_backward_compatibility(self) -> None:
        """Test that GameState extensions maintain backward compatibility.

        Requirements: Ensure backward compatibility with existing game state management
        """
        from src.ti4.core.game_state import GameState

        # Should be able to create GameState without strategy card fields
        state = GameState()

        # All existing functionality should still work
        assert state.is_valid()
        assert state.get_victory_points("player1") == 0

        # New fields should have sensible defaults
        assert isinstance(state.strategy_card_assignments, dict)
        assert isinstance(state.exhausted_strategy_cards, set)
        assert len(state.strategy_card_assignments) == 0
        assert len(state.exhausted_strategy_cards) == 0


class TestRule83GameStateValidation:
    """Test validation for strategy card state extensions."""

    def test_game_state_validates_strategy_card_assignment_inputs(self) -> None:
        """Test that GameState validates strategy card assignment inputs.

        Requirements: Input validation for robustness
        """
        from src.ti4.core.game_state import GameState
        from src.ti4.core.strategic_action import StrategyCardType

        state = GameState()

        # Should reject None player_id
        with pytest.raises(ValueError, match="Player ID cannot be None"):
            state.assign_strategy_card(None, StrategyCardType.LEADERSHIP)  # type: ignore

        # Should reject empty player_id
        with pytest.raises(ValueError, match="Player ID cannot be empty"):
            state.assign_strategy_card("", StrategyCardType.LEADERSHIP)

        # Should reject None strategy card
        with pytest.raises(ValueError, match="Strategy card cannot be None"):
            state.assign_strategy_card("player1", None)  # type: ignore

    def test_game_state_validates_strategy_card_exhaustion_inputs(self) -> None:
        """Test that GameState validates strategy card exhaustion inputs.

        Requirements: Input validation for robustness
        """
        from src.ti4.core.game_state import GameState

        state = GameState()

        # Should reject None strategy card
        with pytest.raises(ValueError, match="Strategy card cannot be None"):
            state.exhaust_strategy_card(None)  # type: ignore

    def test_game_state_prevents_duplicate_strategy_card_assignments(self) -> None:
        """Test that GameState prevents duplicate strategy card assignments.

        Requirements: 1.3 - Strategy card tracking validation
        """
        from src.ti4.core.game_state import GameState
        from src.ti4.core.strategic_action import StrategyCardType

        state = GameState()

        # Assign card to player1
        state = state.assign_strategy_card("player1", StrategyCardType.LEADERSHIP)

        # Should reject assignment of same card to different player
        with pytest.raises(ValueError, match="Strategy card .* is already assigned"):
            state.assign_strategy_card("player2", StrategyCardType.LEADERSHIP)

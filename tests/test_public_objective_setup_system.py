"""Tests for public objective setup and configuration system."""

import pytest

from src.ti4.core.constants import Expansion
from src.ti4.core.game_phase import GamePhase
from src.ti4.core.objective import ObjectiveCard, ObjectiveCategory, ObjectiveType


def test_objective_setup_configuration_dataclass():
    """Test that ObjectiveSetupConfiguration dataclass exists with proper fields."""
    from src.ti4.core.objective import ObjectiveSetupConfiguration

    config = ObjectiveSetupConfiguration(
        stage_i_count=5,
        stage_ii_count=5,
        include_expansions=[Expansion.BASE, Expansion.PROPHECY_OF_KINGS],
        random_seed=12345,
    )

    assert config.stage_i_count == 5
    assert config.stage_ii_count == 5
    assert config.include_expansions == [Expansion.BASE, Expansion.PROPHECY_OF_KINGS]
    assert config.random_seed == 12345


def test_objective_setup_configuration_defaults():
    """Test that ObjectiveSetupConfiguration has proper default values."""
    from src.ti4.core.objective import ObjectiveSetupConfiguration

    config = ObjectiveSetupConfiguration()

    assert config.stage_i_count == 5
    assert config.stage_ii_count == 5
    assert config.include_expansions == [Expansion.BASE]
    assert config.random_seed is None


def test_objective_reveal_state_dataclass():
    """Test that ObjectiveRevealState dataclass exists with proper fields."""
    from src.ti4.core.objective import ObjectiveRevealState

    # Create mock objective cards for testing
    mock_stage_i = ObjectiveCard(
        id="stage_i_1",
        name="Stage I Objective",
        condition="Test condition",
        points=1,
        expansion=Expansion.BASE,
        phase=GamePhase.STATUS,
        type=ObjectiveType.PUBLIC_STAGE_I,
        requirement_validator=lambda p, g: True,
        category=ObjectiveCategory.PLANET_CONTROL,
        dependencies=[],
    )

    mock_stage_ii = ObjectiveCard(
        id="stage_ii_1",
        name="Stage II Objective",
        condition="Test condition",
        points=2,
        expansion=Expansion.BASE,
        phase=GamePhase.STATUS,
        type=ObjectiveType.PUBLIC_STAGE_II,
        requirement_validator=lambda p, g: True,
        category=ObjectiveCategory.RESOURCE_SPENDING,
        dependencies=[],
    )

    reveal_state = ObjectiveRevealState(
        revealed_stage_i=[mock_stage_i],
        revealed_stage_ii=[],
        remaining_stage_i=[],
        remaining_stage_ii=[mock_stage_ii],
        current_stage="stage_i",
    )

    assert len(reveal_state.revealed_stage_i) == 1
    assert len(reveal_state.revealed_stage_ii) == 0
    assert len(reveal_state.remaining_stage_i) == 0
    assert len(reveal_state.remaining_stage_ii) == 1
    assert reveal_state.current_stage == "stage_i"


def test_public_objective_manager_exists():
    """Test that PublicObjectiveManager class exists."""
    from src.ti4.core.objective import PublicObjectiveManager

    manager = PublicObjectiveManager()
    assert manager is not None


def test_public_objective_manager_setup_objectives_method():
    """Test that PublicObjectiveManager has setup_objectives method."""
    from src.ti4.core.game_state import GameState
    from src.ti4.core.objective import PublicObjectiveManager

    manager = PublicObjectiveManager()

    # Create a minimal game state for testing
    game_state = GameState()

    # This should not raise an error
    manager.setup_objectives(game_state)


def test_public_objective_manager_setup_with_configuration():
    """Test that setup_objectives accepts configuration parameter."""
    from src.ti4.core.game_state import GameState
    from src.ti4.core.objective import (
        ObjectiveSetupConfiguration,
        PublicObjectiveManager,
    )

    manager = PublicObjectiveManager()
    config = ObjectiveSetupConfiguration(
        stage_i_count=3, stage_ii_count=3, include_expansions=[Expansion.BASE]
    )

    game_state = GameState()

    # This should not raise an error
    manager.setup_objectives(game_state, config)


def test_public_objective_manager_get_reveal_state():
    """Test that PublicObjectiveManager can return current reveal state."""
    from src.ti4.core.game_state import GameState
    from src.ti4.core.objective import PublicObjectiveManager

    manager = PublicObjectiveManager()
    game_state = GameState()

    # Setup objectives first
    manager.setup_objectives(game_state)

    # Should be able to get reveal state
    reveal_state = manager.get_reveal_state()
    assert reveal_state is not None
    assert hasattr(reveal_state, "current_stage")


def test_objective_setup_configuration_validation():
    """Test that ObjectiveSetupConfiguration validates input data."""
    from src.ti4.core.objective import ObjectiveSetupConfiguration

    # Test negative stage counts
    with pytest.raises(ValueError, match="Stage I count must be positive"):
        ObjectiveSetupConfiguration(stage_i_count=0)

    with pytest.raises(ValueError, match="Stage II count must be positive"):
        ObjectiveSetupConfiguration(stage_ii_count=-1)

    # Test empty expansions list
    with pytest.raises(ValueError, match="Must include at least one expansion"):
        ObjectiveSetupConfiguration(include_expansions=[])


def test_objective_reveal_state_validation():
    """Test that ObjectiveRevealState validates input data."""
    from src.ti4.core.objective import ObjectiveRevealState

    # Test invalid current_stage
    with pytest.raises(ValueError, match="Current stage must be one of"):
        ObjectiveRevealState(
            revealed_stage_i=[],
            revealed_stage_ii=[],
            remaining_stage_i=[],
            remaining_stage_ii=[],
            current_stage="invalid",  # type: ignore
        )


def test_objective_setup_configuration_frozen():
    """Test that ObjectiveSetupConfiguration is a frozen dataclass."""
    from src.ti4.core.objective import ObjectiveSetupConfiguration

    config = ObjectiveSetupConfiguration()

    # Should not be able to modify frozen dataclass
    with pytest.raises(AttributeError):
        config.stage_i_count = 10


def test_objective_reveal_state_frozen():
    """Test that ObjectiveRevealState is a frozen dataclass."""
    from src.ti4.core.objective import ObjectiveRevealState

    reveal_state = ObjectiveRevealState(
        revealed_stage_i=[],
        revealed_stage_ii=[],
        remaining_stage_i=[],
        remaining_stage_ii=[],
        current_stage="stage_i",
    )

    # Should not be able to modify frozen dataclass
    with pytest.raises(AttributeError):
        reveal_state.current_stage = "stage_ii"

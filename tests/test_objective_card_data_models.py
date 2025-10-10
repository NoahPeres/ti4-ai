"""Tests for enhanced objective card data models."""

import pytest

from src.ti4.core.constants import Expansion
from src.ti4.core.game_phase import GamePhase


# Test that ObjectiveCard dataclass exists with enhanced metadata
def test_objective_card_has_enhanced_metadata():
    """Test that ObjectiveCard includes all required enhanced metadata fields."""
    from src.ti4.core.objective import ObjectiveCard, ObjectiveCategory, ObjectiveType

    # This should fail initially - ObjectiveCard doesn't exist yet with these fields
    card = ObjectiveCard(
        id="test_objective",
        name="Test Objective",
        condition="Control 4 planets",
        points=1,
        expansion=Expansion.BASE,
        phase=GamePhase.STATUS,
        type=ObjectiveType.PUBLIC_STAGE_I,
        requirement_validator=lambda player_id, game_state: True,
        category=ObjectiveCategory.PLANET_CONTROL,
        dependencies=["planets", "control"],
    )

    assert card.id == "test_objective"
    assert card.name == "Test Objective"
    assert card.condition == "Control 4 planets"
    assert card.points == 1
    assert card.expansion == Expansion.BASE
    assert card.phase == GamePhase.STATUS
    assert card.type == ObjectiveType.PUBLIC_STAGE_I
    assert card.category == ObjectiveCategory.PLANET_CONTROL
    assert card.dependencies == ["planets", "control"]
    assert callable(card.requirement_validator)


def test_objective_requirement_dataclass():
    """Test that ObjectiveRequirement dataclass exists with proper fields."""
    from src.ti4.core.objective import ObjectiveRequirement

    requirement = ObjectiveRequirement(
        description="Control 4 planets with the same trait",
        validator_function="validate_corner_the_market",
        required_systems=["planets", "control"],
        validation_complexity="moderate",
    )

    assert requirement.description == "Control 4 planets with the same trait"
    assert requirement.validator_function == "validate_corner_the_market"
    assert requirement.required_systems == ["planets", "control"]
    assert requirement.validation_complexity == "moderate"


def test_player_standing_dataclass():
    """Test that PlayerStanding dataclass exists with proper fields."""
    from src.ti4.core.objective import (
        ObjectiveCard,
        ObjectiveCategory,
        ObjectiveType,
        PlayerStanding,
    )

    # Create a mock objective card for testing
    mock_objective = ObjectiveCard(
        id="test_obj",
        name="Test",
        condition="Test condition",
        points=1,
        expansion=Expansion.BASE,
        phase=GamePhase.STATUS,
        type=ObjectiveType.PUBLIC_STAGE_I,
        requirement_validator=lambda p, g: True,
        category=ObjectiveCategory.PLANET_CONTROL,
        dependencies=[],
    )

    standing = PlayerStanding(
        player_id="player1",
        victory_points=5,
        scored_objectives=[mock_objective],
        initiative_order=2,
    )

    assert standing.player_id == "player1"
    assert standing.victory_points == 5
    assert len(standing.scored_objectives) == 1
    assert standing.initiative_order == 2


def test_objective_type_enum():
    """Test that ObjectiveType enum exists with required values."""
    from src.ti4.core.objective import ObjectiveType

    assert ObjectiveType.PUBLIC_STAGE_I
    assert ObjectiveType.PUBLIC_STAGE_II
    assert ObjectiveType.SECRET


def test_objective_category_enum():
    """Test that ObjectiveCategory enum exists with required values."""
    from src.ti4.core.objective import ObjectiveCategory

    assert ObjectiveCategory.PLANET_CONTROL
    assert ObjectiveCategory.RESOURCE_SPENDING
    assert ObjectiveCategory.TECHNOLOGY
    assert ObjectiveCategory.UNIT_PRESENCE
    assert ObjectiveCategory.COMBAT
    assert ObjectiveCategory.SPECIAL


def test_validation_complexity_literal():
    """Test that validation complexity uses proper literal values."""
    from src.ti4.core.objective import ObjectiveRequirement

    # Test all valid complexity levels
    simple_req = ObjectiveRequirement(
        description="Simple test",
        validator_function="test_func",
        required_systems=[],
        validation_complexity="simple",
    )

    moderate_req = ObjectiveRequirement(
        description="Moderate test",
        validator_function="test_func",
        required_systems=[],
        validation_complexity="moderate",
    )

    complex_req = ObjectiveRequirement(
        description="Complex test",
        validator_function="test_func",
        required_systems=[],
        validation_complexity="complex",
    )

    assert simple_req.validation_complexity == "simple"
    assert moderate_req.validation_complexity == "moderate"
    assert complex_req.validation_complexity == "complex"


def test_objective_card_frozen_dataclass():
    """Test that ObjectiveCard is a frozen dataclass for immutability."""
    from src.ti4.core.objective import ObjectiveCard, ObjectiveCategory, ObjectiveType

    card = ObjectiveCard(
        id="test",
        name="Test",
        condition="Test condition",
        points=1,
        expansion=Expansion.BASE,
        phase=GamePhase.STATUS,
        type=ObjectiveType.SECRET,
        requirement_validator=lambda p, g: True,
        category=ObjectiveCategory.SPECIAL,
        dependencies=[],
    )

    # Should not be able to modify frozen dataclass
    with pytest.raises(AttributeError):
        card.points = 2


def test_objective_requirement_frozen_dataclass():
    """Test that ObjectiveRequirement is a frozen dataclass for immutability."""
    from src.ti4.core.objective import ObjectiveRequirement

    req = ObjectiveRequirement(
        description="Test",
        validator_function="test_func",
        required_systems=[],
        validation_complexity="simple",
    )

    # Should not be able to modify frozen dataclass
    with pytest.raises(AttributeError):
        req.description = "Modified"


def test_player_standing_frozen_dataclass():
    """Test that PlayerStanding is a frozen dataclass for immutability."""
    from src.ti4.core.objective import PlayerStanding

    standing = PlayerStanding(
        player_id="player1", victory_points=5, scored_objectives=[], initiative_order=1
    )

    # Should not be able to modify frozen dataclass
    with pytest.raises(AttributeError):
        standing.victory_points = 10


# Validation tests for enhanced data models
def test_objective_card_validation():
    """Test that ObjectiveCard validates input data properly."""
    from src.ti4.core.objective import ObjectiveCard, ObjectiveCategory, ObjectiveType

    # Test empty ID validation
    with pytest.raises(ValueError, match="Objective ID cannot be empty"):
        ObjectiveCard(
            id="",
            name="Test",
            condition="Test condition",
            points=1,
            expansion=Expansion.BASE,
            phase=GamePhase.STATUS,
            type=ObjectiveType.SECRET,
            requirement_validator=lambda p, g: True,
            category=ObjectiveCategory.SPECIAL,
            dependencies=[],
        )

    # Test empty name validation
    with pytest.raises(ValueError, match="Objective name cannot be empty"):
        ObjectiveCard(
            id="test",
            name="",
            condition="Test condition",
            points=1,
            expansion=Expansion.BASE,
            phase=GamePhase.STATUS,
            type=ObjectiveType.SECRET,
            requirement_validator=lambda p, g: True,
            category=ObjectiveCategory.SPECIAL,
            dependencies=[],
        )

    # Test empty condition validation
    with pytest.raises(ValueError, match="Objective condition cannot be empty"):
        ObjectiveCard(
            id="test",
            name="Test",
            condition="",
            points=1,
            expansion=Expansion.BASE,
            phase=GamePhase.STATUS,
            type=ObjectiveType.SECRET,
            requirement_validator=lambda p, g: True,
            category=ObjectiveCategory.SPECIAL,
            dependencies=[],
        )

    # Test negative points validation
    with pytest.raises(ValueError, match="Objective points must be positive"):
        ObjectiveCard(
            id="test",
            name="Test",
            condition="Test condition",
            points=0,
            expansion=Expansion.BASE,
            phase=GamePhase.STATUS,
            type=ObjectiveType.SECRET,
            requirement_validator=lambda p, g: True,
            category=ObjectiveCategory.SPECIAL,
            dependencies=[],
        )

    # Test non-callable validator
    with pytest.raises(ValueError, match="Requirement validator must be callable"):
        ObjectiveCard(
            id="test",
            name="Test",
            condition="Test condition",
            points=1,
            expansion=Expansion.BASE,
            phase=GamePhase.STATUS,
            type=ObjectiveType.SECRET,
            requirement_validator="not_callable",  # type: ignore
            category=ObjectiveCategory.SPECIAL,
            dependencies=[],
        )


def test_objective_requirement_validation():
    """Test that ObjectiveRequirement validates input data properly."""
    from src.ti4.core.objective import ObjectiveRequirement

    # Test empty description validation
    with pytest.raises(ValueError, match="Requirement description cannot be empty"):
        ObjectiveRequirement(
            description="",
            validator_function="test_func",
            required_systems=[],
            validation_complexity="simple",
        )

    # Test empty validator function validation
    with pytest.raises(ValueError, match="Validator function name cannot be empty"):
        ObjectiveRequirement(
            description="Test description",
            validator_function="",
            required_systems=[],
            validation_complexity="simple",
        )

    # Test invalid complexity validation
    with pytest.raises(ValueError, match="Validation complexity must be one of"):
        ObjectiveRequirement(
            description="Test description",
            validator_function="test_func",
            required_systems=[],
            validation_complexity="invalid",  # type: ignore
        )


def test_player_standing_validation():
    """Test that PlayerStanding validates input data properly."""
    from src.ti4.core.objective import PlayerStanding

    # Test empty player ID validation
    with pytest.raises(ValueError, match="Player ID cannot be empty"):
        PlayerStanding(
            player_id="", victory_points=5, scored_objectives=[], initiative_order=1
        )

    # Test negative victory points validation
    with pytest.raises(ValueError, match="Victory points cannot be negative"):
        PlayerStanding(
            player_id="player1",
            victory_points=-1,
            scored_objectives=[],
            initiative_order=1,
        )

    # Test invalid initiative order validation
    with pytest.raises(ValueError, match="Initiative order must be at least 1"):
        PlayerStanding(
            player_id="player1",
            victory_points=5,
            scored_objectives=[],
            initiative_order=0,
        )


def test_objective_card_whitespace_validation():
    """Test that ObjectiveCard properly handles whitespace-only strings."""
    from src.ti4.core.objective import ObjectiveCard, ObjectiveCategory, ObjectiveType

    # Test whitespace-only ID
    with pytest.raises(ValueError, match="Objective ID cannot be empty"):
        ObjectiveCard(
            id="   ",
            name="Test",
            condition="Test condition",
            points=1,
            expansion=Expansion.BASE,
            phase=GamePhase.STATUS,
            type=ObjectiveType.SECRET,
            requirement_validator=lambda p, g: True,
            category=ObjectiveCategory.SPECIAL,
            dependencies=[],
        )

    # Test whitespace-only name
    with pytest.raises(ValueError, match="Objective name cannot be empty"):
        ObjectiveCard(
            id="test",
            name="   ",
            condition="Test condition",
            points=1,
            expansion=Expansion.BASE,
            phase=GamePhase.STATUS,
            type=ObjectiveType.SECRET,
            requirement_validator=lambda p, g: True,
            category=ObjectiveCategory.SPECIAL,
            dependencies=[],
        )


def test_objective_requirement_whitespace_validation():
    """Test that ObjectiveRequirement properly handles whitespace-only strings."""
    from src.ti4.core.objective import ObjectiveRequirement

    # Test whitespace-only description
    with pytest.raises(ValueError, match="Requirement description cannot be empty"):
        ObjectiveRequirement(
            description="   ",
            validator_function="test_func",
            required_systems=[],
            validation_complexity="simple",
        )

    # Test whitespace-only validator function
    with pytest.raises(ValueError, match="Validator function name cannot be empty"):
        ObjectiveRequirement(
            description="Test description",
            validator_function="   ",
            required_systems=[],
            validation_complexity="simple",
        )


def test_player_standing_whitespace_validation():
    """Test that PlayerStanding properly handles whitespace-only strings."""
    from src.ti4.core.objective import PlayerStanding

    # Test whitespace-only player ID
    with pytest.raises(ValueError, match="Player ID cannot be empty"):
        PlayerStanding(
            player_id="   ", victory_points=5, scored_objectives=[], initiative_order=1
        )

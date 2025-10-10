"""Tests for ObjectiveCardFactory implementation."""

import pytest

from src.ti4.core.constants import Expansion
from src.ti4.core.game_phase import GamePhase
from src.ti4.core.objective import (
    ObjectiveCard,
    ObjectiveCardFactory,
    ObjectiveCategory,
    ObjectiveType,
)


class TestObjectiveCardFactory:
    """Test cases for ObjectiveCardFactory."""

    def test_create_all_objectives_returns_80_objectives(self):
        """Test that create_all_objectives returns exactly 80 objectives."""
        # RED: This test should fail because ObjectiveCardFactory doesn't exist yet
        factory = ObjectiveCardFactory()
        objectives = factory.create_all_objectives()

        assert len(objectives) == 80
        assert all(isinstance(obj, ObjectiveCard) for obj in objectives.values())

    def test_create_stage_i_objectives_returns_20_objectives(self):
        """Test that create_stage_i_objectives returns exactly 20 Stage I objectives."""
        factory = ObjectiveCardFactory()
        objectives = factory.create_stage_i_objectives()

        assert len(objectives) == 20
        assert all(obj.type == ObjectiveType.PUBLIC_STAGE_I for obj in objectives)
        assert all(obj.points == 1 for obj in objectives)

    def test_create_stage_ii_objectives_returns_20_objectives(self):
        """Test that create_stage_ii_objectives returns exactly 20 Stage II objectives."""
        factory = ObjectiveCardFactory()
        objectives = factory.create_stage_ii_objectives()

        assert len(objectives) == 20
        assert all(obj.type == ObjectiveType.PUBLIC_STAGE_II for obj in objectives)
        assert all(obj.points == 2 for obj in objectives)

    def test_create_secret_objectives_returns_40_objectives(self):
        """Test that create_secret_objectives returns exactly 40 secret objectives."""
        factory = ObjectiveCardFactory()
        objectives = factory.create_secret_objectives()

        assert len(objectives) == 40
        assert all(obj.type == ObjectiveType.SECRET for obj in objectives)
        assert all(obj.points == 1 for obj in objectives)

    def test_corner_the_market_objective_created_correctly(self):
        """Test that Corner the Market objective is created with correct metadata."""
        factory = ObjectiveCardFactory()
        objectives = factory.create_all_objectives()

        corner_market = objectives["corner_the_market"]
        assert corner_market.name == "Corner the Market"
        assert (
            corner_market.condition
            == "Control 4 planets that each have the same planet trait."
        )
        assert corner_market.points == 1
        assert corner_market.expansion == Expansion.BASE
        assert corner_market.phase == GamePhase.STATUS
        assert corner_market.type == ObjectiveType.PUBLIC_STAGE_I
        assert corner_market.category == ObjectiveCategory.PLANET_CONTROL
        assert callable(corner_market.requirement_validator)

    def test_all_objectives_have_valid_metadata(self):
        """Test that all objectives have valid metadata."""
        factory = ObjectiveCardFactory()
        objectives = factory.create_all_objectives()

        for obj_id, objective in objectives.items():
            # Check required fields are not empty
            assert obj_id.strip(), f"Objective ID cannot be empty: {obj_id}"
            assert objective.name.strip(), f"Name cannot be empty for {obj_id}"
            assert objective.condition.strip(), (
                f"Condition cannot be empty for {obj_id}"
            )

            # Check points are positive
            assert objective.points > 0, f"Points must be positive for {obj_id}"

            # Check enums are valid
            assert isinstance(objective.expansion, Expansion), (
                f"Invalid expansion for {obj_id}"
            )
            assert isinstance(objective.phase, GamePhase), f"Invalid phase for {obj_id}"
            assert isinstance(objective.type, ObjectiveType), (
                f"Invalid type for {obj_id}"
            )
            assert isinstance(objective.category, ObjectiveCategory), (
                f"Invalid category for {obj_id}"
            )

            # Check validator is callable
            assert callable(objective.requirement_validator), (
                f"Validator must be callable for {obj_id}"
            )

            # Check dependencies is a list
            assert isinstance(objective.dependencies, list), (
                f"Dependencies must be a list for {obj_id}"
            )

    def test_objective_id_creation(self):
        """Test that objective IDs are created correctly from names."""
        factory = ObjectiveCardFactory()

        # Test normal name
        assert factory._create_objective_id("Corner the Market") == "corner_the_market"

        # Test name with apostrophe
        assert (
            factory._create_objective_id("Destroy Their Greatest Ship")
            == "destroy_their_greatest_ship"
        )

        # Test name with hyphen
        assert (
            factory._create_objective_id("Anti-Fighter Barrage")
            == "anti_fighter_barrage"
        )

    def test_objective_id_creation_with_empty_name(self):
        """Test that empty names raise ValueError."""
        factory = ObjectiveCardFactory()

        with pytest.raises(ValueError, match="Objective name cannot be empty"):
            factory._create_objective_id("")

        with pytest.raises(ValueError, match="Objective name cannot be empty"):
            factory._create_objective_id("   ")

    def test_placeholder_validator_returns_false(self):
        """Test that the placeholder validator always returns False."""
        factory = ObjectiveCardFactory()

        # The validator should always return False as a placeholder
        result = factory._placeholder_validator("player1", None)  # type: ignore
        assert result is False

    def test_category_determination(self):
        """Test that objective categories are determined correctly."""
        factory = ObjectiveCardFactory()

        # Test planet control category
        assert (
            factory._determine_category("Control 4 planets")
            == ObjectiveCategory.PLANET_CONTROL
        )

        # Test resource spending category
        assert (
            factory._determine_category("Spend 8 resources")
            == ObjectiveCategory.RESOURCE_SPENDING
        )

        # Test technology category
        assert (
            factory._determine_category("Own 2 unit upgrade technologies")
            == ObjectiveCategory.TECHNOLOGY
        )

        # Test unit presence category
        assert (
            factory._determine_category("Have 5 ships in system")
            == ObjectiveCategory.UNIT_PRESENCE
        )

        # Test combat category
        assert (
            factory._determine_category("Destroy another player's flagship")
            == ObjectiveCategory.COMBAT
        )

        # Test special category (fallback)
        assert (
            factory._determine_category("Some unknown condition")
            == ObjectiveCategory.SPECIAL
        )

    def test_dependencies_determination(self):
        """Test that dependencies are determined correctly based on category."""
        factory = ObjectiveCardFactory()

        assert factory._determine_dependencies(ObjectiveCategory.PLANET_CONTROL) == [
            "planets",
            "galaxy",
        ]
        assert factory._determine_dependencies(ObjectiveCategory.RESOURCE_SPENDING) == [
            "resources",
            "trade_goods",
        ]
        assert factory._determine_dependencies(ObjectiveCategory.TECHNOLOGY) == [
            "technology"
        ]
        assert factory._determine_dependencies(ObjectiveCategory.UNIT_PRESENCE) == [
            "units",
            "fleet",
        ]
        assert factory._determine_dependencies(ObjectiveCategory.COMBAT) == [
            "combat",
            "units",
        ]
        assert factory._determine_dependencies(ObjectiveCategory.SPECIAL) == [
            "game_state"
        ]

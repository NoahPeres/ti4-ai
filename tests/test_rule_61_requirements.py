"""Tests for Rule 61: OBJECTIVE CARDS - Requirement validation system (Rules 61.9-61.10)."""

from src.ti4.core.constants import Faction
from src.ti4.core.game_state import GameState
from src.ti4.core.objective_requirements import (
    ControlPlanetsRequirement,
    DestroyUnitsRequirement,
    ObjectiveRequirementValidator,
    SpendInfluenceRequirement,
    SpendResourcesRequirement,
    SpendTokensRequirement,
    TechnologyRequirement,
    WinCombatRequirement,
)
from src.ti4.core.player import Player


class TestObjectiveRequirements:
    """Test objective requirement classes (Rules 61.9-61.10)."""

    def test_spend_resources_requirement_creation(self) -> None:
        """Test that resource spending requirements can be created."""
        # Rule 61.10: Players can score some objectives by spending resources
        req = SpendResourcesRequirement(amount=8)

        assert req.amount == 8
        assert req.get_description() == "Spend 8 resources"

    def test_spend_influence_requirement_creation(self) -> None:
        """Test that influence spending requirements can be created."""
        # Rule 61.10: Players can score some objectives by spending influence
        req = SpendInfluenceRequirement(amount=6)

        assert req.amount == 6
        assert req.get_description() == "Spend 6 influence"

    def test_spend_tokens_requirement_creation(self) -> None:
        """Test that token spending requirements can be created."""
        # Rule 61.10: Players can score some objectives by spending tokens
        req = SpendTokensRequirement(amount=3, token_type="command")

        assert req.amount == 3
        assert req.token_type == "command"
        assert req.get_description() == "Spend 3 command tokens"

    def test_control_planets_requirement_creation(self) -> None:
        """Test that planet control requirements can be created."""
        req = ControlPlanetsRequirement(count=6, exclude_home=True)

        assert req.count == 6
        assert req.exclude_home is True
        assert req.get_description() == "Control 6 any planets (excluding home system)"

    def test_destroy_units_requirement_creation(self) -> None:
        """Test that unit destruction requirements can be created."""
        # Rule 61.9: If an objective requires a player to destroy one or more units
        req = DestroyUnitsRequirement(count=3, unit_type="ship")

        assert req.count == 3
        assert req.unit_type == "ship"
        assert req.get_description() == "Destroy 3 ship"

    def test_win_combat_requirement_creation(self) -> None:
        """Test that combat victory requirements can be created."""
        req = WinCombatRequirement(
            count=2, combat_type="space", location_type="home_system"
        )

        assert req.count == 2
        assert req.combat_type == "space"
        assert req.location_type == "home_system"
        assert req.get_description() == "Win 2 space combat in home_system"

    def test_technology_requirement_creation(self) -> None:
        """Test that technology requirements can be created."""
        req = TechnologyRequirement(count=4, tech_type="unit_upgrade")

        assert req.count == 4
        assert req.tech_type == "unit_upgrade"
        assert req.get_description() == "Have 4 unit_upgrade technologies"


class TestObjectiveRequirementValidation:
    """Test objective requirement validation system."""

    def test_requirement_validator_creation(self) -> None:
        """Test that requirement validator can be created."""
        validator = ObjectiveRequirementValidator()
        assert validator is not None

    def test_validate_empty_requirements_list(self) -> None:
        """Test that empty requirements list is always valid."""
        game_state = GameState().add_player(Player("player1", Faction.SOL))
        validator = ObjectiveRequirementValidator()

        result = validator.validate_requirements(game_state, "player1", [])
        assert result is True

    def test_validate_single_unfulfilled_requirement(self) -> None:
        """Test that unfulfilled requirements return False."""
        game_state = GameState().add_player(Player("player1", Faction.SOL))
        validator = ObjectiveRequirementValidator()

        # Resource spending requirement that cannot be fulfilled yet
        req = SpendResourcesRequirement(amount=8)

        result = validator.validate_requirements(game_state, "player1", [req])
        assert result is False

    def test_validate_multiple_unfulfilled_requirements(self) -> None:
        """Test that multiple unfulfilled requirements return False."""
        game_state = GameState().add_player(Player("player1", Faction.SOL))
        validator = ObjectiveRequirementValidator()

        requirements = [
            SpendResourcesRequirement(amount=8),
            SpendInfluenceRequirement(amount=6),
            ControlPlanetsRequirement(count=6),
        ]

        result = validator.validate_requirements(game_state, "player1", requirements)
        assert result is False

    def test_get_unfulfilled_requirements_empty_list(self) -> None:
        """Test getting unfulfilled requirements from empty list."""
        game_state = GameState().add_player(Player("player1", Faction.SOL))
        validator = ObjectiveRequirementValidator()

        unfulfilled = validator.get_unfulfilled_requirements(game_state, "player1", [])
        assert unfulfilled == []

    def test_get_unfulfilled_requirements_all_unfulfilled(self) -> None:
        """Test getting unfulfilled requirements when all are unfulfilled."""
        game_state = GameState().add_player(Player("player1", Faction.SOL))
        validator = ObjectiveRequirementValidator()

        requirements = [
            SpendResourcesRequirement(amount=8),
            SpendInfluenceRequirement(amount=6),
        ]

        unfulfilled = validator.get_unfulfilled_requirements(
            game_state, "player1", requirements
        )
        assert len(unfulfilled) == 2
        assert unfulfilled == requirements


class TestRequirementFulfillmentStubs:
    """Test that requirement fulfillment methods exist and return appropriate stubs."""

    def test_spend_resources_requirement_not_fulfilled_by_default(self) -> None:
        """Test that resource spending requirements are not fulfilled by default."""
        game_state = GameState().add_player(Player("player1", Faction.SOL))
        req = SpendResourcesRequirement(amount=8)

        # Should return False until resource system is implemented
        assert req.is_fulfilled_by(game_state, "player1") is False

    def test_spend_influence_requirement_not_fulfilled_by_default(self) -> None:
        """Test that influence spending requirements are not fulfilled by default."""
        game_state = GameState().add_player(Player("player1", Faction.SOL))
        req = SpendInfluenceRequirement(amount=6)

        # Should return False until influence system is implemented
        assert req.is_fulfilled_by(game_state, "player1") is False

    def test_spend_tokens_requirement_not_fulfilled_by_default(self) -> None:
        """Test that token spending requirements are not fulfilled by default."""
        game_state = GameState().add_player(Player("player1", Faction.SOL))
        req = SpendTokensRequirement(amount=3, token_type="command")

        # Should return False until token system is implemented
        assert req.is_fulfilled_by(game_state, "player1") is False

    def test_control_planets_requirement_not_fulfilled_by_default(self) -> None:
        """Test that planet control requirements are not fulfilled by default."""
        game_state = GameState().add_player(Player("player1", Faction.SOL))
        req = ControlPlanetsRequirement(count=6)

        # Should return False until planet control system is implemented
        assert req.is_fulfilled_by(game_state, "player1") is False

    def test_destroy_units_requirement_not_fulfilled_by_default(self) -> None:
        """Test that unit destruction requirements are not fulfilled by default."""
        game_state = GameState().add_player(Player("player1", Faction.SOL))
        req = DestroyUnitsRequirement(count=3, unit_type="ship")

        # Should return False until unit destruction tracking is implemented
        assert req.is_fulfilled_by(game_state, "player1") is False

    def test_win_combat_requirement_not_fulfilled_by_default(self) -> None:
        """Test that combat victory requirements are not fulfilled by default."""
        game_state = GameState().add_player(Player("player1", Faction.SOL))
        req = WinCombatRequirement(count=2, combat_type="space")

        # Should return False until combat tracking is implemented
        assert req.is_fulfilled_by(game_state, "player1") is False

    def test_technology_requirement_not_fulfilled_by_default(self) -> None:
        """Test that technology requirements are not fulfilled by default."""
        game_state = GameState().add_player(Player("player1", Faction.SOL))
        req = TechnologyRequirement(count=4, tech_type="unit_upgrade")

        # Should return False until technology system is implemented
        assert req.is_fulfilled_by(game_state, "player1") is False


class TestRequirementDescriptions:
    """Test requirement description generation."""

    def test_spend_resources_description_variations(self) -> None:
        """Test resource spending requirement descriptions."""
        req1 = SpendResourcesRequirement(amount=1)
        req8 = SpendResourcesRequirement(amount=8)

        assert req1.get_description() == "Spend 1 resources"
        assert req8.get_description() == "Spend 8 resources"

    def test_control_planets_description_variations(self) -> None:
        """Test planet control requirement descriptions."""
        req_basic = ControlPlanetsRequirement(count=6)
        req_exclude_home = ControlPlanetsRequirement(count=6, exclude_home=True)
        req_cultural = ControlPlanetsRequirement(count=3, planet_type="cultural")

        assert req_basic.get_description() == "Control 6 any planets"
        assert (
            req_exclude_home.get_description()
            == "Control 6 any planets (excluding home system)"
        )
        assert req_cultural.get_description() == "Control 3 cultural planets"

    def test_destroy_units_description_variations(self) -> None:
        """Test unit destruction requirement descriptions."""
        req_any = DestroyUnitsRequirement(count=2, unit_type="any")
        req_ships = DestroyUnitsRequirement(count=3, unit_type="ship")

        assert req_any.get_description() == "Destroy 2 units"
        assert req_ships.get_description() == "Destroy 3 ship"

    def test_win_combat_description_variations(self) -> None:
        """Test combat victory requirement descriptions."""
        req_any = WinCombatRequirement(count=1, combat_type="any", location_type="any")
        req_space = WinCombatRequirement(
            count=2, combat_type="space", location_type="any"
        )
        req_home = WinCombatRequirement(
            count=1, combat_type="any", location_type="home_system"
        )
        req_specific = WinCombatRequirement(
            count=2, combat_type="space", location_type="anomaly"
        )

        assert req_any.get_description() == "Win 1 combat"
        assert req_space.get_description() == "Win 2 space combat"
        assert req_home.get_description() == "Win 1 combat in home_system"
        assert req_specific.get_description() == "Win 2 space combat in anomaly"

    def test_technology_description_variations(self) -> None:
        """Test technology requirement descriptions."""
        req_any = TechnologyRequirement(count=3, tech_type="any")
        req_upgrade = TechnologyRequirement(count=4, tech_type="unit_upgrade")

        assert req_any.get_description() == "Have 3 technologies"
        assert req_upgrade.get_description() == "Have 4 unit_upgrade technologies"

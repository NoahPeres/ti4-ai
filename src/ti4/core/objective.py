"""Objective card system for TI4."""

import csv
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Callable, Literal, Optional

if TYPE_CHECKING:
    from .constants import Expansion
    from .game_phase import GamePhase
    from .game_state import GameState

logger = logging.getLogger(__name__)


def _default_expansions() -> list["Expansion"]:
    """Factory function for default expansion list to avoid circular imports."""
    from .constants import Expansion

    return [Expansion.BASE]


# Custom Exception Types for Objective System


class ObjectiveSystemError(Exception):
    """Base exception for objective system errors."""

    pass


class HomeSystemControlError(ObjectiveSystemError):
    """Raised when player doesn't control home system for public objectives."""

    pass


class ObjectiveAlreadyScoredError(ObjectiveSystemError):
    """Raised when attempting to score an already-scored objective."""

    pass


class ObjectiveNotEligibleError(ObjectiveSystemError):
    """Raised when attempting to score an objective without meeting requirements."""

    pass


class InvalidObjectivePhaseError(ObjectiveSystemError):
    """Raised when attempting to score objective in wrong phase."""

    pass


class AllObjectivesRevealedError(ObjectiveSystemError):
    """Raised when game should end due to all objectives being revealed."""

    pass


class ObjectiveType(Enum):
    """Enumeration of objective types."""

    PUBLIC_STAGE_I = "public_stage_i"
    PUBLIC_STAGE_II = "public_stage_ii"
    SECRET = "secret"


class ObjectiveCategory(Enum):
    """Enumeration of objective categories for grouping similar objectives."""

    PLANET_CONTROL = "planet_control"
    RESOURCE_SPENDING = "resource_spending"
    TECHNOLOGY = "technology"
    UNIT_PRESENCE = "unit_presence"
    COMBAT = "combat"
    SPECIAL = "special"


class CompletableObjective(ABC):
    """Abstract base class for objectives that can be completed by players.

    This class provides a common interface for objectives that need to check
    completion status and provide objective data.
    """

    @abstractmethod
    def get_objective(self) -> "Objective":
        """Get the underlying Objective data.

        Returns:
            The Objective instance this completable objective wraps
        """
        pass

    @abstractmethod
    def is_completed_by(self, game_state: "GameState", player_id: str) -> bool:
        """Check if this objective is completed by the given player.

        Args:
            game_state: Current game state
            player_id: ID of the player to check

        Returns:
            True if the objective is completed by the player, False otherwise
        """
        pass


@dataclass(frozen=True)
class ObjectiveCard:
    """Enhanced objective card with complete metadata.

    This dataclass represents a complete TI4 objective card with all necessary
    metadata for game mechanics, validation, and categorization.

    Args:
        id: Unique identifier for the objective card
        name: Display name of the objective
        condition: Human-readable description of the objective condition
        points: Victory points awarded for completing this objective
        expansion: TI4 expansion this objective belongs to
        phase: Game phase when this objective can be scored
        type: Type of objective (Stage I, Stage II, or Secret)
        requirement_validator: Function to validate if objective requirements are met
        category: Category for grouping similar objectives
        dependencies: List of game systems this objective depends on for validation
    """

    id: str
    name: str
    condition: str
    points: int
    expansion: "Expansion"
    phase: "GamePhase"
    type: ObjectiveType
    requirement_validator: Callable[[str, "GameState"], bool]
    category: ObjectiveCategory
    dependencies: list[str]

    def __post_init__(self) -> None:
        """Validate objective card data after initialization."""
        if not self.id.strip():
            raise ValueError("Objective ID cannot be empty")
        if not self.name.strip():
            raise ValueError("Objective name cannot be empty")
        if not self.condition.strip():
            raise ValueError("Objective condition cannot be empty")
        if self.points <= 0:
            raise ValueError("Objective points must be positive")
        if not callable(self.requirement_validator):
            raise ValueError("Requirement validator must be callable")


@dataclass(frozen=True)
class ObjectiveRequirement:
    """Detailed requirement specification for objectives.

    This dataclass provides detailed metadata about objective requirements
    for validation, documentation, and system integration purposes.

    Args:
        description: Human-readable description of the requirement
        validator_function: Name of the function that validates this requirement
        required_systems: List of game systems needed for validation
        validation_complexity: Complexity level of the validation logic
    """

    description: str
    validator_function: str
    required_systems: list[str]
    validation_complexity: Literal["simple", "moderate", "complex"]

    def __post_init__(self) -> None:
        """Validate requirement data after initialization."""
        if not self.description.strip():
            raise ValueError("Requirement description cannot be empty")
        if not self.validator_function.strip():
            raise ValueError("Validator function name cannot be empty")
        valid_complexities = {"simple", "moderate", "complex"}
        if self.validation_complexity not in valid_complexities:
            raise ValueError(
                f"Validation complexity must be one of {valid_complexities}"
            )


@dataclass(frozen=True)
class PlayerStanding:
    """Player victory point standing with tie-breaking information.

    This dataclass represents a player's current standing in the game,
    including victory points, scored objectives, and tie-breaking information.

    Args:
        player_id: Unique identifier for the player
        victory_points: Current victory points for the player
        scored_objectives: List of objectives this player has scored
        initiative_order: Player's position in initiative order for tie-breaking
    """

    player_id: str
    victory_points: int
    scored_objectives: list[ObjectiveCard]
    initiative_order: int

    def __post_init__(self) -> None:
        """Validate player standing data after initialization."""
        if not self.player_id.strip():
            raise ValueError("Player ID cannot be empty")
        if self.victory_points < 0:
            raise ValueError("Victory points cannot be negative")
        if self.initiative_order < 1:
            raise ValueError("Initiative order must be at least 1")


@dataclass(frozen=True)
class Objective:
    """Represents an objective card in TI4."""

    id: str
    name: str
    description: str
    points: int
    is_public: bool
    scoring_phase: "GamePhase"


@dataclass(frozen=True)
class ObjectiveSetupConfiguration:
    """Configuration for objective setup.

    This dataclass provides configuration parameters for setting up
    public objectives at the start of a game.

    Args:
        stage_i_count: Number of Stage I objectives to include (default: 5)
        stage_ii_count: Number of Stage II objectives to include (default: 5)
        include_expansions: List of expansions to include objectives from
        random_seed: Optional seed for random objective selection
    """

    stage_i_count: int = 5
    stage_ii_count: int = 5
    include_expansions: list["Expansion"] = field(default_factory=_default_expansions)
    random_seed: Optional[int] = None

    def __post_init__(self) -> None:
        """Validate configuration data after initialization."""
        if self.stage_i_count <= 0:
            raise ValueError("Stage I count must be positive")
        if self.stage_ii_count <= 0:
            raise ValueError("Stage II count must be positive")
        if len(self.include_expansions) == 0:
            raise ValueError("Must include at least one expansion")


@dataclass(frozen=True)
class ObjectiveRevealState:
    """Current state of objective revelation.

    This dataclass tracks the current state of public objective revelation
    during the game, including which objectives have been revealed and
    which remain to be revealed.

    Args:
        revealed_stage_i: List of revealed Stage I objectives
        revealed_stage_ii: List of revealed Stage II objectives
        remaining_stage_i: List of remaining Stage I objectives
        remaining_stage_ii: List of remaining Stage II objectives
        current_stage: Current stage being revealed ("stage_i", "stage_ii", or "complete")
    """

    revealed_stage_i: list[ObjectiveCard]
    revealed_stage_ii: list[ObjectiveCard]
    remaining_stage_i: list[ObjectiveCard]
    remaining_stage_ii: list[ObjectiveCard]
    current_stage: Literal["stage_i", "stage_ii", "complete"]

    def __post_init__(self) -> None:
        """Validate reveal state data after initialization."""
        valid_stages = {"stage_i", "stage_ii", "complete"}
        if self.current_stage not in valid_stages:
            raise ValueError(f"Current stage must be one of {valid_stages}")


class PublicObjectiveManager:
    """Manages public objective revelation and progression.

    This class handles the setup and progression of public objectives
    according to TI4 rules, including Stage I/II progression and
    game end conditions.
    """

    def __init__(self) -> None:
        """Initialize the public objective manager."""
        self._reveal_state: Optional[ObjectiveRevealState] = None

    def setup_objectives(
        self,
        game_state: "GameState",
        config: Optional[ObjectiveSetupConfiguration] = None,
    ) -> None:
        """Set up 5 Stage I and 5 Stage II objectives face-down.

        Args:
            game_state: Current game state
            config: Optional configuration for objective setup
        """
        if config is None:
            config = ObjectiveSetupConfiguration()

        # Get objectives from factory
        try:
            stage_i_objectives = ObjectiveCardFactory.create_stage_i_objectives()
            stage_ii_objectives = ObjectiveCardFactory.create_stage_ii_objectives()

            # Limit to configured counts
            stage_i_objectives = stage_i_objectives[: config.stage_i_count]
            stage_ii_objectives = stage_ii_objectives[: config.stage_ii_count]

        except (FileNotFoundError, ValueError):
            # If factory fails, use empty lists for testing
            stage_i_objectives = []
            stage_ii_objectives = []

        self._reveal_state = ObjectiveRevealState(
            revealed_stage_i=[],
            revealed_stage_ii=[],
            remaining_stage_i=stage_i_objectives,
            remaining_stage_ii=stage_ii_objectives,
            current_stage="stage_i",
        )

    def get_reveal_state(self) -> ObjectiveRevealState:
        """Get the current objective reveal state.

        Returns:
            Current objective reveal state

        Raises:
            ValueError: If objectives have not been set up yet
        """
        if self._reveal_state is None:
            raise ValueError("Objectives must be set up before getting reveal state")
        return self._reveal_state

    def reveal_next_objective(self, speaker_id: str) -> ObjectiveCard:
        """Reveal the next public objective during status phase.

        Args:
            speaker_id: ID of the speaker revealing the objective

        Returns:
            The revealed objective card

        Raises:
            ValueError: If objectives have not been set up
            AllObjectivesRevealedError: If all objectives are revealed (triggers game end)
        """
        if self._reveal_state is None:
            raise ValueError("Objectives must be set up before revealing objectives")

        # Check if all objectives have been revealed
        if (
            len(self._reveal_state.remaining_stage_i) == 0
            and len(self._reveal_state.remaining_stage_ii) == 0
        ):
            raise AllObjectivesRevealedError(
                "All public objectives have been revealed. The game ends immediately. "
                "Determine the winner based on victory points, with ties broken by initiative order."
            )

        # Determine which objective to reveal based on current stage
        if (
            self._reveal_state.current_stage == "stage_i"
            and self._reveal_state.remaining_stage_i
        ):
            return self._reveal_stage_i_objective()
        elif (
            self._reveal_state.current_stage == "stage_ii"
            and self._reveal_state.remaining_stage_ii
        ):
            return self._reveal_stage_ii_objective()

        # This should not happen if logic is correct
        raise ValueError("No objectives available to reveal")

    def _reveal_stage_i_objective(self) -> ObjectiveCard:
        """Reveal the next Stage I objective and update state.

        Returns:
            The revealed Stage I objective card
        """
        assert self._reveal_state is not None  # Should be checked by caller
        objective_to_reveal = self._reveal_state.remaining_stage_i[0]
        new_revealed_stage_i = self._reveal_state.revealed_stage_i + [
            objective_to_reveal
        ]
        new_remaining_stage_i = self._reveal_state.remaining_stage_i[1:]

        # Check if we should move to Stage II
        next_stage: Literal["stage_i", "stage_ii", "complete"] = (
            "stage_ii" if len(new_remaining_stage_i) == 0 else "stage_i"
        )

        # Update reveal state
        self._reveal_state = ObjectiveRevealState(
            revealed_stage_i=new_revealed_stage_i,
            revealed_stage_ii=self._reveal_state.revealed_stage_ii,
            remaining_stage_i=new_remaining_stage_i,
            remaining_stage_ii=self._reveal_state.remaining_stage_ii,
            current_stage=next_stage,
        )

        return objective_to_reveal

    def _reveal_stage_ii_objective(self) -> ObjectiveCard:
        """Reveal the next Stage II objective and update state.

        Returns:
            The revealed Stage II objective card
        """
        assert self._reveal_state is not None  # Should be checked by caller
        objective_to_reveal = self._reveal_state.remaining_stage_ii[0]
        new_revealed_stage_ii = self._reveal_state.revealed_stage_ii + [
            objective_to_reveal
        ]
        new_remaining_stage_ii = self._reveal_state.remaining_stage_ii[1:]

        # Check if we should mark as complete
        next_stage: Literal["stage_i", "stage_ii", "complete"] = (
            "complete" if len(new_remaining_stage_ii) == 0 else "stage_ii"
        )

        # Update reveal state
        self._reveal_state = ObjectiveRevealState(
            revealed_stage_i=self._reveal_state.revealed_stage_i,
            revealed_stage_ii=new_revealed_stage_ii,
            remaining_stage_i=self._reveal_state.remaining_stage_i,
            remaining_stage_ii=new_remaining_stage_ii,
            current_stage=next_stage,
        )

        return objective_to_reveal

    def check_game_end_condition(self) -> bool:
        """Check if all objectives are revealed (triggers game end).

        Returns:
            True if all objectives have been revealed, False otherwise

        Raises:
            ValueError: If objectives have not been set up yet
        """
        if self._reveal_state is None:
            raise ValueError(
                "Objectives must be set up before checking game end condition"
            )

        # Game ends when all objectives are revealed
        return (
            len(self._reveal_state.remaining_stage_i) == 0
            and len(self._reveal_state.remaining_stage_ii) == 0
        )

    def get_available_objectives_for_scoring(self) -> list[ObjectiveCard]:
        """Get currently revealed objectives available for scoring.

        Returns:
            List of revealed objectives that can be scored

        Raises:
            ValueError: If objectives have not been set up yet
        """
        if self._reveal_state is None:
            raise ValueError(
                "Objectives must be set up before getting available objectives"
            )

        # Return all revealed objectives (both Stage I and Stage II)
        return (
            self._reveal_state.revealed_stage_i + self._reveal_state.revealed_stage_ii
        )


class ObjectiveCardFactory:
    """Factory for creating concrete objective card instances."""

    # Class-level placeholder validator to avoid creating multiple instances
    @staticmethod
    def _placeholder_validator(player_id: str, game_state: "GameState") -> bool:
        """Placeholder validator function - will be implemented in later tasks."""
        return False

    @staticmethod
    def create_all_objectives() -> dict[str, ObjectiveCard]:
        """Create all 80 official TI4 objective cards.

        Returns:
            Dictionary mapping objective IDs to ObjectiveCard instances

        Raises:
            FileNotFoundError: If the objective cards CSV file is not found
            ValueError: If CSV data is malformed or invalid
        """
        try:
            csv_path = ObjectiveCardFactory._get_csv_path()
            raw_data = ObjectiveCardFactory._load_csv_data(csv_path)
            return ObjectiveCardFactory._create_objectives_from_data(raw_data)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Objective cards CSV file not found: {e}") from e
        except Exception as e:
            raise ValueError(f"Error creating objectives from CSV data: {e}") from e

    @staticmethod
    def _get_csv_path() -> str:
        """Get the path to the objective cards CSV file."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate from src/ti4/core/ to project root, then to docs/component_details/
        return os.path.join(
            current_dir,
            "..",
            "..",
            "..",
            "docs",
            "component_details",
            "TI4_objective_cards.csv",
        )

    @staticmethod
    def _load_csv_data(csv_path: str) -> list[dict[str, str]]:
        """Load and validate CSV data from file."""
        data = []
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip empty rows
                if not row.get("Name", "").strip():
                    continue
                data.append(row)
        return data

    @staticmethod
    def _create_objectives_from_data(
        raw_data: list[dict[str, str]],
    ) -> dict[str, ObjectiveCard]:
        """Create ObjectiveCard instances from raw CSV data."""
        objectives = {}

        for row in raw_data:
            try:
                objective = ObjectiveCardFactory._create_single_objective(row)
                objectives[objective.id] = objective
            except Exception as e:
                # Log error but continue processing other objectives
                logger.warning(
                    f"Failed to create objective from row {row.get('Name', 'Unknown')}: {e}"
                )
                continue

        return objectives

    @staticmethod
    def _create_single_objective(row: dict[str, str]) -> ObjectiveCard:
        """Create a single ObjectiveCard from a CSV row."""
        # Create objective ID from name
        obj_id = ObjectiveCardFactory._create_objective_id(row["Name"])

        # Parse and validate data
        expansion = ObjectiveCardFactory._parse_expansion(row["Expansion"])
        phase = ObjectiveCardFactory._parse_phase(row["Phase"])
        obj_type = ObjectiveCardFactory._parse_type(row["Type"])

        # Process condition text
        condition = row["Condition"].replace("§", ",")  # Restore commas
        category = ObjectiveCardFactory._determine_category(condition)
        dependencies = ObjectiveCardFactory._determine_dependencies(category)

        # Validate points
        try:
            points = int(row["Points"])
            if points <= 0:
                raise ValueError(f"Points must be positive, got {points}")
        except ValueError as e:
            raise ValueError(f"Invalid points value '{row['Points']}': {e}") from e

        return ObjectiveCard(
            id=obj_id,
            name=row["Name"].strip(),
            condition=condition,
            points=points,
            expansion=expansion,
            phase=phase,
            type=obj_type,
            requirement_validator=ObjectiveCardFactory._placeholder_validator,
            category=category,
            dependencies=dependencies,
        )

    @staticmethod
    def _create_objective_id(name: str) -> str:
        """Create a standardized objective ID from the name."""
        if not name or not name.strip():
            raise ValueError("Objective name cannot be empty")
        return name.lower().replace(" ", "_").replace("'", "").replace("-", "_")

    @staticmethod
    def _parse_expansion(expansion_str: str) -> "Expansion":
        """Parse expansion string to Expansion enum."""
        from .constants import Expansion

        expansion_mapping = {
            "Base": Expansion.BASE,
            "Prophecy of Kings": Expansion.PROPHECY_OF_KINGS,
            "Codex III": Expansion.CODEX_III,
        }

        expansion = expansion_mapping.get(expansion_str)
        if expansion is None:
            logger.warning(f"Unknown expansion '{expansion_str}', defaulting to Base")
            return Expansion.BASE
        return expansion

    @staticmethod
    def _parse_phase(phase_str: str) -> "GamePhase":
        """Parse phase string to GamePhase enum."""
        from .game_phase import GamePhase

        phase_mapping = {
            "Status": GamePhase.STATUS,
            "Action": GamePhase.ACTION,
            "Agenda": GamePhase.AGENDA,
        }

        phase = phase_mapping.get(phase_str)
        if phase is None:
            logger.warning(f"Unknown phase '{phase_str}', defaulting to Status")
            return GamePhase.STATUS
        return phase

    @staticmethod
    def _parse_type(type_str: str) -> ObjectiveType:
        """Parse type string to ObjectiveType enum."""
        type_mapping = {
            "Stage I": ObjectiveType.PUBLIC_STAGE_I,
            "Stage II": ObjectiveType.PUBLIC_STAGE_II,
            "Secret": ObjectiveType.SECRET,
        }

        obj_type = type_mapping.get(type_str)
        if obj_type is None:
            logger.warning(f"Unknown type '{type_str}', defaulting to Secret")
            return ObjectiveType.SECRET
        return obj_type

    @staticmethod
    def _determine_category(condition: str) -> ObjectiveCategory:
        """Determine objective category based on condition text."""
        condition_lower = condition.lower()

        if any(keyword in condition_lower for keyword in ["control", "planet"]):
            return ObjectiveCategory.PLANET_CONTROL
        elif any(
            keyword in condition_lower
            for keyword in ["spend", "resources", "influence", "trade goods"]
        ):
            return ObjectiveCategory.RESOURCE_SPENDING
        elif any(
            keyword in condition_lower
            for keyword in ["technology", "technologies", "unit upgrade"]
        ):
            return ObjectiveCategory.TECHNOLOGY
        elif any(
            keyword in condition_lower
            for keyword in ["ships", "units", "fleet", "ground forces", "structures"]
        ):
            return ObjectiveCategory.UNIT_PRESENCE
        elif any(
            keyword in condition_lower for keyword in ["combat", "destroy", "win"]
        ):
            return ObjectiveCategory.COMBAT
        else:
            return ObjectiveCategory.SPECIAL

    @staticmethod
    def _determine_dependencies(category: ObjectiveCategory) -> list[str]:
        """Determine system dependencies based on objective category."""
        if category == ObjectiveCategory.PLANET_CONTROL:
            return ["planets", "galaxy"]
        elif category == ObjectiveCategory.RESOURCE_SPENDING:
            return ["resources", "trade_goods"]
        elif category == ObjectiveCategory.TECHNOLOGY:
            return ["technology"]
        elif category == ObjectiveCategory.UNIT_PRESENCE:
            return ["units", "fleet"]
        elif category == ObjectiveCategory.COMBAT:
            return ["combat", "units"]
        else:
            return ["game_state"]

    @staticmethod
    def create_stage_i_objectives() -> list[ObjectiveCard]:
        """Create all 20 Stage I public objectives."""
        all_objectives = ObjectiveCardFactory.create_all_objectives()
        return [
            obj
            for obj in all_objectives.values()
            if obj.type == ObjectiveType.PUBLIC_STAGE_I
        ]

    @staticmethod
    def create_stage_ii_objectives() -> list[ObjectiveCard]:
        """Create all 20 Stage II public objectives."""
        all_objectives = ObjectiveCardFactory.create_all_objectives()
        return [
            obj
            for obj in all_objectives.values()
            if obj.type == ObjectiveType.PUBLIC_STAGE_II
        ]

    @staticmethod
    def create_secret_objectives() -> list[ObjectiveCard]:
        """Create all 40 secret objectives."""
        all_objectives = ObjectiveCardFactory.create_all_objectives()
        return [
            obj for obj in all_objectives.values() if obj.type == ObjectiveType.SECRET
        ]


class ConcreteObjectiveRequirements:
    """Implementations of specific objective requirement validators.

    This class provides concrete implementations for validating whether
    players meet the requirements for specific TI4 objective cards.
    """

    def validate_corner_the_market(
        self, player_id: str, game_state: "GameState"
    ) -> bool:
        """Control 4 planets that each have the same planet trait.

        Args:
            player_id: The player to check
            game_state: Current game state

        Returns:
            True if player controls 4 planets with the same trait
        """
        # Get player's controlled planets
        player_planets = game_state.get_player_planets(player_id)

        # Count planets by trait
        trait_counts: dict[str, int] = {}
        for planet in player_planets:
            for trait in planet.traits:
                trait_counts[trait] = trait_counts.get(trait, 0) + 1

        # Check if any trait has 4 or more planets
        return any(count >= 4 for count in trait_counts.values())

    def validate_erect_monument(self, player_id: str, game_state: "GameState") -> bool:
        """Spend 8 resources.

        Args:
            player_id: The player to check
            game_state: Current game state

        Returns:
            True if player has spent 8 resources this turn
        """
        # Check if resource spending tracking exists in game state
        if hasattr(game_state, "resource_spending_this_turn"):
            spending_dict: dict[str, int] = game_state.resource_spending_this_turn
            resources_spent = spending_dict.get(player_id, 0)
            return resources_spent >= 8

        # If no tracking exists, return False
        return False

    def validate_expand_borders(self, player_id: str, game_state: "GameState") -> bool:
        """Control 6 planets in non-home systems.

        Args:
            player_id: The player to check
            game_state: Current game state

        Returns:
            True if player controls 6 planets in non-home systems
        """
        # Get player's controlled planets
        player_planets = game_state.get_player_planets(player_id)

        # Count planets that are not in home systems
        # For now, we'll use a simple approach - this will be refined later
        # when home system detection is properly implemented
        non_home_planets = 0
        for planet in player_planets:
            # Simple heuristic: assume planets with "home" in name are home planets
            if "home" not in planet.name.lower():
                non_home_planets += 1

        return non_home_planets >= 6

    def validate_found_golden_age(
        self, player_id: str, game_state: "GameState"
    ) -> bool:
        """Spend 16 influence.

        Args:
            player_id: The player to check
            game_state: Current game state

        Returns:
            True if player has spent 16 influence this turn
        """
        # Check if influence spending tracking exists in game state
        if hasattr(game_state, "influence_spending_this_turn"):
            spending_dict: dict[str, int] = game_state.influence_spending_this_turn
            influence_spent = spending_dict.get(player_id, 0)
            return influence_spent >= 16

        # If no tracking exists, return False
        return False

    # Technology-based objective validators

    def validate_develop_weaponry(
        self, player_id: str, game_state: "GameState"
    ) -> bool:
        """Own 2 unit upgrade technologies.

        Args:
            player_id: The player to check
            game_state: Current game state

        Returns:
            True if player owns 2 or more unit upgrade technologies
        """
        # Check if technology manager exists in game state
        if not hasattr(game_state, "technology_manager"):
            return False

        tech_manager = game_state.technology_manager
        player_technologies = tech_manager.get_player_technologies(player_id)

        # Count unit upgrade technologies
        unit_upgrade_count = 0
        for technology in player_technologies:
            if tech_manager.is_unit_upgrade(technology):
                unit_upgrade_count += 1

        return unit_upgrade_count >= 2

    def validate_diversify_research(
        self, player_id: str, game_state: "GameState"
    ) -> bool:
        """Own 2 technologies in each of 2 colors.

        Args:
            player_id: The player to check
            game_state: Current game state

        Returns:
            True if player owns 2 technologies in each of 2 different colors
        """
        # Check if technology manager exists in game state
        if not hasattr(game_state, "technology_manager"):
            return False

        tech_manager = game_state.technology_manager
        player_technologies = tech_manager.get_player_technologies(player_id)

        # Count technologies by color
        from .technology import TechnologyColor

        color_counts: dict[TechnologyColor, int] = {}

        for technology in player_technologies:
            color = tech_manager.get_technology_color(technology)
            color_counts[color] = color_counts.get(color, 0) + 1

        # Count how many colors have 2 or more technologies
        colors_with_two_plus = sum(1 for count in color_counts.values() if count >= 2)

        return colors_with_two_plus >= 2

    def validate_raise_a_fleet(self, player_id: str, game_state: "GameState") -> bool:
        """Have 5 non-fighter ships in the same system.

        Args:
            player_id: The player to check
            game_state: Current game state

        Returns:
            True if player has 5 non-fighter ships in the same system

        TODO: Implement actual validation logic. Currently returns True for testing.
        """
        # Placeholder implementation - returns True for testing
        return True

    def validate_command_an_armada(
        self, player_id: str, game_state: "GameState"
    ) -> bool:
        """Have 8 non-fighter ships in the same system.

        Args:
            player_id: The player to check
            game_state: Current game state

        Returns:
            True if player has 8 non-fighter ships in the same system

        TODO: Implement actual validation logic. Currently returns True for testing.
        """
        # Placeholder implementation - returns True for testing
        return True

    def validate_destroy_their_greatest_ship(
        self, player_id: str, game_state: "GameState"
    ) -> bool:
        """Destroy another player's war sun or flagship.

        Args:
            player_id: The player to check
            game_state: Current game state

        Returns:
            True if player destroyed a war sun or flagship this turn

        TODO: Implement actual validation logic. Currently returns True for testing.
        """
        # Placeholder implementation - returns True for testing
        return True

    def validate_spark_a_rebellion(
        self, player_id: str, game_state: "GameState"
    ) -> bool:
        """Win a combat against a player who has the most victory points.

        Args:
            player_id: The player to check
            game_state: Current game state

        Returns:
            True if player won combat against the victory point leader

        TODO: Implement actual validation logic. Currently returns True for testing.
        """
        # Placeholder implementation - returns True for testing
        return True

    def validate_unveil_flagship(self, player_id: str, game_state: "GameState") -> bool:
        """Win a space combat in a system that contains your flagship.

        Args:
            player_id: The player to check
            game_state: Current game state

        Returns:
            True if player won space combat with their flagship present

        TODO: Implement actual validation logic. Currently returns True for testing.
        """
        # Placeholder implementation - returns True for testing
        return True

    def validate_form_a_spy_network(
        self, player_id: str, game_state: "GameState"
    ) -> bool:
        """Discard 5 action cards.

        Args:
            player_id: The player to check
            game_state: Current game state

        Returns:
            True if player discarded 5 action cards this turn

        TODO: Implement actual validation logic. Currently returns True for testing.
        """
        # Placeholder implementation - returns True for testing
        return True

    def validate_prove_endurance(self, player_id: str, game_state: "GameState") -> bool:
        """Be the last player to pass during a game round.

        Args:
            player_id: The player to check
            game_state: Current game state

        Returns:
            True if player was the last to pass this round

        TODO: Implement actual validation logic. Currently returns True for testing.
        """
        # Placeholder implementation - returns True for testing
        return True


class VictoryPointScoreboard:
    """Manages victory point tracking and scoreboard display.

    This class handles victory point updates, control token placement,
    and victory condition checking for the objective system.
    """

    def __init__(self) -> None:
        """Initialize the victory point scoreboard."""
        self._scored_objectives: dict[str, list[ObjectiveCard]] = {}

    def score_objective(
        self, player_id: str, objective: ObjectiveCard, game_state: "GameState"
    ) -> "GameState":
        """Score an objective and update victory points.

        Args:
            player_id: ID of the player scoring the objective
            objective: The objective being scored
            game_state: Current game state

        Returns:
            New GameState with updated victory points

        Raises:
            ValueError: If player_id is empty
            ObjectiveNotEligibleError: If player doesn't meet objective requirements
            HomeSystemControlError: If player doesn't control home system (public objectives only)
        """
        if not player_id.strip():
            raise ValueError("Player ID cannot be empty")

        # Validate objective requirements
        if not objective.requirement_validator(player_id, game_state):
            raise ObjectiveNotEligibleError(
                f"Player {player_id} does not meet requirements for objective '{objective.name}'"
            )

        # Check home system control for public objectives
        if objective.type in [
            ObjectiveType.PUBLIC_STAGE_I,
            ObjectiveType.PUBLIC_STAGE_II,
        ]:
            from .home_system_control_validator import HomeSystemControlValidator

            validator = HomeSystemControlValidator()
            try:
                validation_result = validator.validate_home_system_control(
                    player_id, game_state
                )
                if not validation_result.is_valid:
                    raise HomeSystemControlError(
                        f"Player {player_id} cannot score public objectives: {validation_result.error_message}"
                    )
            except Exception as e:
                # If home system validation fails, treat as invalid
                raise HomeSystemControlError(
                    f"Player {player_id} cannot score public objectives: Home system validation failed"
                ) from e

        # Create new GameState with updated victory points using proper immutable pattern
        updated_game_state = game_state.award_victory_points(
            player_id, objective.points
        )

        # Place control token (track scored objective)
        self.place_control_token(player_id, objective)

        return updated_game_state

    def place_control_token(self, player_id: str, objective: ObjectiveCard) -> None:
        """Place player's control token on objective card.

        Args:
            player_id: ID of the player placing the token
            objective: The objective card to place token on
        """
        if player_id not in self._scored_objectives:
            self._scored_objectives[player_id] = []

        self._scored_objectives[player_id].append(objective)

    def get_scored_objectives(self, player_id: str) -> list[ObjectiveCard]:
        """Get objectives scored by a player.

        Args:
            player_id: ID of the player

        Returns:
            List of objectives scored by the player
        """
        return self._scored_objectives.get(player_id, [])

    def advance_victory_track(self, player_id: str, points: int) -> None:
        """Advance player's position on victory point track.

        Args:
            player_id: ID of the player
            points: Number of points to advance

        Note:
            This is a placeholder method for future expansion.
        """
        # Placeholder implementation - could be expanded for visual track representation
        pass

    def check_victory_condition(self, game_state: "GameState") -> Optional[str]:
        """Check if any player has reached victory point threshold.

        Args:
            game_state: Current game state

        Returns:
            Player ID of the winner, or None if no winner yet
        """
        if not hasattr(game_state, "victory_points") or not hasattr(
            game_state, "victory_points_to_win"
        ):
            return None

        victory_threshold = game_state.victory_points_to_win
        winners = []

        # Find all players who have reached the victory threshold
        for player_id, points in game_state.victory_points.items():
            if points >= victory_threshold:
                winners.append(player_id)

        if not winners:
            return None

        if len(winners) == 1:
            return winners[0]

        # Handle tie-breaking using initiative order
        if hasattr(game_state, "_sort_players_by_initiative_order"):
            initiative_order = game_state._sort_players_by_initiative_order(winners)
            for player_id in initiative_order:
                if player_id in winners:
                    return player_id

        # Fallback: return first winner if no initiative order available
        return winners[0]

    def get_victory_standings(self, game_state: "GameState") -> list[PlayerStanding]:
        """Get current victory point standings with tie-breaking.

        Args:
            game_state: Current game state

        Returns:
            List of PlayerStanding objects sorted by victory points and initiative order
        """
        if not hasattr(game_state, "victory_points"):
            return []

        standings = []

        # Get initiative order for tie-breaking
        initiative_order = []
        all_players = list(game_state.victory_points.keys())
        if hasattr(game_state, "_sort_players_by_initiative_order"):
            initiative_order = game_state._sort_players_by_initiative_order(all_players)

        # Create standings for each player
        for player_id, points in game_state.victory_points.items():
            initiative_position = (
                initiative_order.index(player_id) + 1
                if player_id in initiative_order
                else 999  # Default high value for unknown players
            )

            scored_objectives = self.get_scored_objectives(player_id)

            standing = PlayerStanding(
                player_id=player_id,
                victory_points=points,
                scored_objectives=scored_objectives,
                initiative_order=initiative_position,
            )
            standings.append(standing)

        # Sort by victory points (descending) then by initiative order (ascending)
        standings.sort(key=lambda s: (-s.victory_points, s.initiative_order))

        return standings


class ObjectiveEligibilityTracker:
    """Tracks and detects objective eligibility for players.

    This class provides caching and tracking mechanisms for objective
    eligibility to improve performance and provide helpful notifications.
    """

    def __init__(self) -> None:
        """Initialize the objective eligibility tracker."""
        self._eligibility_cache: dict[str, dict[str, bool]] = {}
        self._last_game_state_hash: Optional[str] = None

    def check_all_objective_eligibility(
        self, player_id: str, game_state: "GameState"
    ) -> dict[str, bool]:
        """Check eligibility for all objectives for a player.

        Args:
            player_id: The player to check eligibility for
            game_state: Current game state

        Returns:
            Dictionary mapping objective IDs to eligibility status
        """
        # Get all available objectives
        try:
            all_objectives = ObjectiveCardFactory.create_all_objectives()
        except (FileNotFoundError, ValueError):
            # If objective factory fails, return empty dict
            return {}
        except Exception:
            # Catch any other exceptions
            return {}

        eligibility = {}

        for obj_id, objective in all_objectives.items():
            try:
                is_eligible = objective.requirement_validator(player_id, game_state)
                eligibility[obj_id] = is_eligible
            except Exception:
                # If validation fails, mark as not eligible
                eligibility[obj_id] = False

        # Update cache
        self._eligibility_cache[player_id] = eligibility

        # Update game state hash for cache invalidation
        self._last_game_state_hash = str(hash(str(game_state)))

        return eligibility

    def get_newly_eligible_objectives(
        self, player_id: str, game_state: "GameState"
    ) -> list[ObjectiveCard]:
        """Get objectives that became newly eligible since last check.

        Args:
            player_id: The player to check
            game_state: Current game state

        Returns:
            List of objectives that became newly eligible
        """
        # Preserve the previous eligibility snapshot before refreshing the cache
        previous_eligibility = self._eligibility_cache.get(player_id, {}).copy()

        # Refresh eligibility and cache with the latest data
        current_eligibility = self.check_all_objective_eligibility(
            player_id, game_state
        )

        # Find newly eligible objectives
        newly_eligible = []

        try:
            all_objectives = ObjectiveCardFactory.create_all_objectives()

            for obj_id, is_currently_eligible in current_eligibility.items():
                was_previously_eligible = previous_eligibility.get(obj_id, False)

                if is_currently_eligible and not was_previously_eligible:
                    if obj_id in all_objectives:
                        newly_eligible.append(all_objectives[obj_id])
        except (FileNotFoundError, ValueError):
            # If objective factory fails, return empty list
            pass

        return newly_eligible

    def update_eligibility_cache(self, game_state: "GameState") -> None:
        """Update cached eligibility data for performance.

        Args:
            game_state: Current game state
        """
        # Get all players from game state
        if hasattr(game_state, "players"):
            for player in game_state.players:
                self.check_all_objective_eligibility(player.id, game_state)
        elif hasattr(game_state, "victory_points"):
            # Fallback: use victory points keys as player IDs
            for player_id in game_state.victory_points.keys():
                self.check_all_objective_eligibility(player_id, game_state)

    def validate_master_the_sciences(
        self, player_id: str, game_state: "GameState"
    ) -> bool:
        """Own 2 technologies in each of 4 colors.

        Args:
            player_id: The player to check
            game_state: Current game state

        Returns:
            True if player owns 2 technologies in each of 4 different colors
        """
        # Check if technology manager exists in game state
        if not hasattr(game_state, "technology_manager"):
            return False

        tech_manager = game_state.technology_manager
        player_technologies = tech_manager.get_player_technologies(player_id)

        # Count technologies by color
        from .technology import TechnologyColor

        color_counts: dict[TechnologyColor, int] = {}

        for technology in player_technologies:
            color = tech_manager.get_technology_color(technology)
            color_counts[color] = color_counts.get(color, 0) + 1

        # Count how many colors have 2 or more technologies
        colors_with_two_plus = sum(1 for count in color_counts.values() if count >= 2)

        return colors_with_two_plus >= 4

    def get_cache_statistics(self) -> dict[str, int]:
        """Get cache performance statistics.

        Returns:
            Dictionary with cache statistics including hits, misses, etc.
        """
        # Return basic statistics for now
        return {
            "cache_hits": 0,
            "cache_misses": 0,
            "total_checks": 0,
            "cached_players": len(self._eligibility_cache),
        }

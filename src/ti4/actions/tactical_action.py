"""TI4 Tactical Action implementation with extensible step-based architecture."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional


class MovementValidationError(Exception):
    """Raised when movement validation fails."""

    pass


@dataclass
class MovementPlan:
    """Represents a complete movement plan for a tactical action."""

    def __init__(self) -> None:
        self.ship_movements = []
        self.ground_force_movements = []

    def add_ship_movement(self, unit: Any, from_system: str, to_system: str) -> None:
        """Add a ship movement to the plan."""
        self.ship_movements.append(
            {"unit": unit, "from_system": from_system, "to_system": to_system}
        )

    def add_ground_force_movement(
        self,
        unit: Any,
        from_system: str,
        to_system: str,
        from_location: str,
        to_location: str,
    ) -> None:
        """Add a ground force movement to the plan."""
        # Validate that ground forces cannot move directly between planets
        if (
            from_location != "space"
            and to_location != "space"
            and from_location != to_location
        ):
            raise MovementValidationError(
                "Ground forces cannot move directly between planets"
            )

        self.ground_force_movements.append(
            {
                "unit": unit,
                "from_system": from_system,
                "to_system": to_system,
                "from_location": from_location,
                "to_location": to_location,
            }
        )


@dataclass
class CommitGroundForcesPlan:
    """Represents a plan for committing ground forces from space to planets."""

    def __init__(self) -> None:
        self.commitments = []

    def add_commitment(self, unit: Any, planet_name: str) -> None:
        """Add a ground force commitment to a planet."""
        self.commitments.append({"unit": unit, "planet_name": planet_name})


class TacticalActionStep(ABC):
    """Abstract base class for all tactical action steps."""

    @abstractmethod
    def can_execute(self, game_state: Any, context: dict[str, Any]) -> bool:
        """Check if this step can be executed in the current context."""
        pass

    @abstractmethod
    def execute(self, game_state: Any, context: dict[str, Any]) -> Any:
        """Execute this step and return the new game state."""
        pass

    @abstractmethod
    def get_step_name(self) -> str:
        """Get the name of this step for logging/debugging."""
        pass


class MovementStep(TacticalActionStep):
    """Handles the Movement Step of a Tactical Action."""

    def can_execute(self, game_state: Any, context: dict[str, Any]) -> bool:
        """Check if movement step can be executed."""
        return context.get("movement_plan") is not None

    def get_step_name(self) -> str:
        """Get the name of this step."""
        return "Movement"

    def execute(self, game_state: Any, context: dict[str, Any]) -> Any:
        """Execute the movement step."""
        movement_plan = context.get("movement_plan")
        if movement_plan is None:
            return game_state

        # Execute ship movements
        for movement in movement_plan.ship_movements:
            unit = movement["unit"]
            from_system_id = movement["from_system"]
            to_system_id = movement["to_system"]

            # Remove unit from source system
            from_system = game_state.systems[from_system_id]
            from_system.remove_unit_from_space(unit)

            # Add unit to destination system
            to_system = game_state.systems[to_system_id]
            to_system.place_unit_in_space(unit)

        # Execute ground force movements
        for movement in movement_plan.ground_force_movements:
            unit = movement["unit"]
            from_system_id = movement["from_system"]
            to_system_id = movement["to_system"]
            from_location = movement["from_location"]
            to_location = movement["to_location"]

            from_system = game_state.systems[from_system_id]
            to_system = game_state.systems[to_system_id]

            # Remove unit from source location
            if from_location == "space":
                from_system.remove_unit_from_space(unit)
            else:
                from_system.remove_unit_from_planet(unit, from_location)

            # Add unit to destination location
            if to_location == "space":
                to_system.place_unit_in_space(unit)
            else:
                to_system.place_unit_on_planet(unit, to_location)

        return game_state


class CommitGroundForcesStep(TacticalActionStep):
    """Handles the Commit Ground Forces Step of a Tactical Action."""

    def can_execute(self, game_state: Any, context: dict[str, Any]) -> bool:
        """Check if commit ground forces step can be executed."""
        commit_plan = context.get("commit_plan")
        return commit_plan is not None and len(commit_plan.commitments) > 0

    def get_step_name(self) -> str:
        """Get the name of this step."""
        return "Commit Ground Forces"

    def execute(self, game_state: Any, context: dict[str, Any]) -> Any:
        """Execute the commit ground forces step."""
        commit_plan = context.get("commit_plan")
        if commit_plan is None:
            return game_state

        # Execute each commitment
        for commitment in commit_plan.commitments:
            unit = commitment["unit"]
            planet_name = commitment["planet_name"]

            # Find which system the unit is currently in (should be in space)
            for system in game_state.systems.values():
                if unit in system.space_units:
                    # Remove from space and place on planet
                    system.remove_unit_from_space(unit)
                    system.place_unit_on_planet(unit, planet_name)
                    break

        return game_state


@dataclass
class ValidationResult:
    """Result of movement plan validation."""

    is_valid: bool
    transport_assignments: Optional[Any] = None
    errors: Optional[list[str]] = None
    technology_effects: Optional[dict[str, Any]] = None


class MovementValidator:
    """Validates movement plans according to TI4 rules."""

    def __init__(self, galaxy: Any):
        self.galaxy = galaxy

    def validate_movement_plan(
        self,
        movement_plan: MovementPlan,
        player_id: str,
        technologies: Optional[set[str]] = None,
    ) -> ValidationResult:
        """Validate an entire movement plan jointly."""
        technologies = technologies or set()
        errors = []
        technology_effects = {}

        # First pass: identify which ships need technology assistance
        ships_needing_help = []
        ships_valid_without_help = []

        for movement in movement_plan.ship_movements:
            unit = movement["unit"]
            from_system_id = movement["from_system"]
            to_system_id = movement["to_system"]

            # Get coordinates
            from_coord = self.galaxy.get_system_coordinate(from_system_id)
            to_coord = self.galaxy.get_system_coordinate(to_system_id)

            if from_coord is None or to_coord is None:
                errors.append(f"Invalid system coordinates for {unit.unit_type}")
                continue

            # Calculate distance and required movement
            distance = from_coord.distance_to(to_coord)
            base_movement = unit.get_movement()

            if distance > base_movement:
                # Ship needs technology assistance
                ships_needing_help.append(
                    {
                        "movement": movement,
                        "distance": distance,
                        "base_movement": base_movement,
                        "shortfall": distance - base_movement,
                    }
                )
            else:
                ships_valid_without_help.append(movement)

        # Apply technology effects optimally using extensible system
        remaining_ships_needing_help = self._apply_movement_technologies(
            ships_needing_help,
            technologies,
            technology_effects,
            ships_valid_without_help,
        )

        # Any remaining ships that couldn't be helped are invalid
        for ship_info in remaining_ships_needing_help:
            unit = ship_info["movement"]["unit"]
            errors.append(f"Insufficient movement for {unit.unit_type}")

        # Validate transport capacity for ground force movements
        transport_capacity = {}
        transport_usage = {}

        # Calculate available transport capacity
        for movement in movement_plan.ship_movements:
            unit = movement["unit"]
            capacity = unit.get_capacity()
            if capacity > 0:
                ship_key = f"{unit.unit_type}_{id(unit)}"
                transport_capacity[ship_key] = capacity
                transport_usage[ship_key] = 0

        # Check ground force transport requirements
        for movement in movement_plan.ground_force_movements:
            unit = movement["unit"]
            from_location = movement["from_location"]

            # Ground forces moving from planets need transport
            if from_location != "space":
                # Find available transport
                transport_found = False
                for ship_key in transport_capacity:
                    if transport_usage[ship_key] < transport_capacity[ship_key]:
                        transport_usage[ship_key] += 1
                        transport_found = True
                        break

                if not transport_found:
                    errors.append(
                        f"Insufficient transport capacity for {unit.unit_type}"
                    )

        is_valid = len(errors) == 0
        return ValidationResult(
            is_valid=is_valid,
            transport_assignments=transport_usage if is_valid else None,
            errors=errors if errors else None,
            technology_effects=technology_effects if technology_effects else None,
        )

    def _apply_movement_technologies(
        self,
        ships_needing_help: list[dict[str, Any]],
        technologies: set[str],
        technology_effects: dict[str, str],
        ships_valid_without_help: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Apply movement technologies optimally to help ships that need assistance.

        This method is designed to be extensible for future technologies.
        Returns the list of ships that still need help after applying technologies.
        """
        remaining_ships = ships_needing_help.copy()

        # Apply Gravity Drive (can only be used once per tactical action)
        if "gravity_drive" in technologies:
            remaining_ships = self._apply_gravity_drive(
                remaining_ships, technology_effects, ships_valid_without_help
            )

        # Future technologies can be added here:
        # if "future_movement_tech" in technologies:
        #     remaining_ships = self._apply_future_movement_tech(
        #         remaining_ships, technology_effects, ships_valid_without_help
        #     )

        return remaining_ships

    def _apply_gravity_drive(
        self,
        ships_needing_help: list[dict[str, Any]],
        technology_effects: dict[str, str],
        ships_valid_without_help: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Apply Gravity Drive technology to one ship that can benefit from it."""
        remaining_ships = []
        gravity_drive_applied = False

        for ship_info in ships_needing_help:
            if ship_info["shortfall"] <= 1 and not gravity_drive_applied:
                # Apply Gravity Drive to this ship
                unit = ship_info["movement"]["unit"]
                technology_effects["gravity_drive"] = f"Applied to {unit.unit_type}"
                gravity_drive_applied = True
                ships_valid_without_help.append(ship_info["movement"])
            else:
                # This ship cannot be helped by Gravity Drive
                remaining_ships.append(ship_info)

        return remaining_ships


class TacticalAction:
    """Represents a TI4 Tactical Action with extensible step-based architecture.

    This implementation supports the full TI4 tactical action sequence:
    1. Activation (place command token)
    2. Movement (move ships and ground forces)
    3. Space Combat (if applicable)
    4. Invasion (if applicable)
    5. Production (if applicable)

    Additional steps can be easily added by implementing TacticalActionStep.
    """

    def __init__(self, active_system_id: str, player_id: str) -> None:
        self.active_system_id = active_system_id
        self.player_id = player_id
        self.steps: list[TacticalActionStep] = []
        self.context: dict[str, Any] = {
            "active_system_id": active_system_id,
            "player_id": player_id,
            "movement_plan": None,
            "commit_plan": None,
        }

        # Initialize with default steps (can be customized)
        self._initialize_default_steps()

    def _initialize_default_steps(self) -> None:
        """Initialize the default tactical action steps."""
        # Note: Steps are defined after TacticalActionStep, so we need to create them here
        # For now, we'll use a lazy initialization approach
        pass

    def add_step(self, step: TacticalActionStep) -> None:
        """Add a custom step to the tactical action."""
        self.steps.append(step)

    def insert_step(self, index: int, step: TacticalActionStep) -> None:
        """Insert a step at a specific position."""
        self.steps.insert(index, step)

    def remove_step(self, step_name: str) -> bool:
        """Remove a step by name."""
        for i, step in enumerate(self.steps):
            if step.get_step_name() == step_name:
                del self.steps[i]
                return True
        return False

    def execute_all_steps(self, game_state: Any) -> Any:
        """Execute all applicable steps in sequence."""
        current_state = game_state

        for step in self.steps:
            if step.can_execute(current_state, self.context):
                current_state = step.execute(current_state, self.context)

        return current_state

    def execute_step(self, step_name: str, game_state: Any) -> Any:
        """Execute a specific step by name."""
        for step in self.steps:
            if step.get_step_name() == step_name:
                if step.can_execute(game_state, self.context):
                    return step.execute(game_state, self.context)
                else:
                    raise ValueError(
                        f"Step '{step_name}' cannot be executed in current context"
                    )

        raise ValueError(f"Step '{step_name}' not found")

    def get_executable_steps(self, game_state: Any) -> list[str]:
        """Get list of steps that can be executed in the current state."""
        return [
            step.get_step_name()
            for step in self.steps
            if step.can_execute(game_state, self.context)
        ]

    def set_movement_plan(self, movement_plan: MovementPlan) -> None:
        """Set the movement plan for this tactical action."""
        self.context["movement_plan"] = movement_plan

    def set_commit_plan(self, commit_plan: CommitGroundForcesPlan) -> None:
        """Set the commit ground forces plan for this tactical action."""
        self.context["commit_plan"] = commit_plan

    def initialize_steps(self) -> None:
        """Initialize the default steps. Call this after class definitions are complete."""
        if not self.steps:  # Only initialize if not already done
            self.steps = [
                MovementStep(),
                CommitGroundForcesStep(),
                # Future steps can be added here:
                # SpaceCombatStep(),
                # InvasionStep(),
                # ProductionStep(),
            ]

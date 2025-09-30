"""TI4 Movement Engine - Advanced movement planning and execution system.

This module handles complex movement operations with technology effects, transport capacity,
and multi-system movement planning. This is the EXECUTION layer for movement operations.

For Rule 89 compliance validation, use Rule89Validator in core/rule89_validator.py.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

from ..core.constants import LocationType


def _is_space_location(location: str) -> bool:
    """Check if a location string represents space."""
    return location == LocationType.SPACE.value


class MovementValidationError(Exception):
    """Raised when movement validation fails."""

    pass


@dataclass
class MovementPlan:
    """Represents a complete movement plan for a tactical action."""

    def __init__(self) -> None:
        self.ship_movements: list[dict[str, Any]] = []
        self.ground_force_movements: list[dict[str, Any]] = []

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
            not _is_space_location(from_location)
            and not _is_space_location(to_location)
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
        self.commitments: list[dict[str, Any]] = []

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
            if _is_space_location(from_location):
                from_system.remove_unit_from_space(unit)
            else:
                from_system.remove_unit_from_planet(unit, from_location)

            # Add unit to destination location
            if _is_space_location(to_location):
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


class SpaceCannonOffenseStep(TacticalActionStep):
    """Step for Space Cannon Offense during tactical action (Rule 58.7)."""

    def can_execute(self, game_state: Any, context: dict[str, Any]) -> bool:
        """Check if space cannon offense can be executed."""
        if game_state is None:
            return False

        active_system_id = context.get("active_system_id")
        if not active_system_id:
            return False

        system = game_state.systems.get(active_system_id)
        if not system:
            return False

        # Check if there are any units with space cannon ability
        space_cannon_units = self._get_space_cannon_units(system)
        return len(space_cannon_units) > 0

    def get_step_name(self) -> str:
        return "Space Cannon Offense"

    def execute(self, game_state: Any, context: dict[str, Any]) -> Any:
        """Execute space cannon offense step."""
        active_system_id = context.get("active_system_id")
        system = game_state.systems.get(active_system_id)

        if not system:
            return game_state

        # Get all players with space cannon units
        space_cannon_players = self._get_space_cannon_players(system)

        # Execute space cannon offense for each player in order
        for player_id in space_cannon_players:
            self._resolve_space_cannon_for_player(player_id, game_state, context)

        return game_state

    def _get_space_cannon_units(self, system: Any) -> list[Any]:
        """Get all units with space cannon ability in the system."""
        space_cannon_units = []

        # Check units on planets (PDS units have space cannon)
        for planet in system.planets:
            for unit in planet.units:
                # Check if unit has space cannon ability using unit stats
                if hasattr(unit, "unit_type"):
                    from ..core.constants import UnitType
                    from ..core.unit_stats import UnitStatsProvider

                    provider = UnitStatsProvider()
                    # Convert string unit_type back to enum
                    unit_type_enum = UnitType(unit.unit_type)
                    stats = provider.get_unit_stats(unit_type_enum)
                    if stats.space_cannon:
                        space_cannon_units.append(unit)

        return space_cannon_units

    def _get_space_cannon_players(self, system: Any) -> list[str]:
        """Get players who have space cannon units in order."""
        players = set()

        for unit in self._get_space_cannon_units(system):
            players.add(unit.owner)

        return sorted(players)  # Return in consistent order

    def _get_valid_target_players(
        self, shooting_player: str, system: Any, context: dict[str, Any]
    ) -> list[str]:
        """Get valid target players for space cannon offense."""
        active_player = context.get("player_id")
        if not isinstance(active_player, str):
            return []

        target_players = set()

        # Space cannon can target ships in space
        for unit in system.space_units:
            if unit.owner != shooting_player:
                target_players.add(unit.owner)

        target_list = sorted(target_players)

        # Rule 77.5: Non-active players can only target the active player
        if shooting_player != active_player:
            return [active_player] if active_player in target_list else []

        # Active player can target any other player
        return target_list

    def _execute_player_space_cannon(
        self, game_state: Any, system: Any, player_id: str, context: dict[str, Any]
    ) -> None:
        """Execute space cannon offense for a specific player."""
        # Get space cannon units for this player
        player_units = [
            unit
            for unit in self._get_space_cannon_units(system)
            if unit.owner == player_id
        ]

        if not player_units:
            return

        # Get valid targets
        target_players = self._get_valid_target_players(player_id, system, context)
        if not target_players:
            return

        # Roll dice for each space cannon unit
        total_hits = 0

        for unit in player_units:
            hits = self._roll_space_cannon_dice(unit, game_state, context)
            total_hits += hits

        # Assign hits to target units (simplified - target first available unit)
        if total_hits > 0:
            self._assign_hits(system, target_players, total_hits)

    def _assign_space_cannon_hits(
        self, system: Any, target_players: list[str], hits: int
    ) -> None:
        """Assign space cannon hits to target units."""
        # Get all targetable units (ships in space)
        target_units = []
        for unit in system.space_units:
            if unit.owner in target_players:
                target_units.append(unit)

        # Assign hits (simplified - destroy units in order)
        hits_to_assign = min(hits, len(target_units))
        for i in range(hits_to_assign):
            unit = target_units[i]
            system.remove_unit_from_space(unit)

    def _roll_space_cannon_dice(
        self, unit: Any, game_state: Any, context: dict[str, Any]
    ) -> int:
        """Roll space cannon dice for a unit and return hits."""
        from ..core.dice import calculate_hits, roll_dice

        # Get unit's space cannon stats
        stats = unit.get_stats()
        if not hasattr(stats, "space_cannon_value") or stats.space_cannon_value is None:
            return 0

        # Get number of dice to roll (default 1 if not specified)
        dice_count = getattr(stats, "space_cannon_dice", 1)

        # Roll dice
        dice_results = roll_dice(dice_count)

        # Calculate hits
        return calculate_hits(dice_results, stats.space_cannon_value)

    def _assign_hits(self, system: Any, target_players: list[str], hits: int) -> None:
        """Assign hits to target units (alias for _assign_space_cannon_hits)."""
        self._assign_space_cannon_hits(system, target_players, hits)

    def _get_space_cannon_units_for_player(
        self, player_id: str, game_state: Any, context: dict[str, Any]
    ) -> list[Any]:
        """Get all space cannon units for a player in the active system and adjacent systems (for PDS II)."""
        from ..core.constants import UnitType
        from ..core.unit_stats import UnitStatsProvider

        active_system_id = context["active_system_id"]
        active_system = game_state.systems[active_system_id]

        # Get units in the active system (space units)
        units = []
        for unit in active_system.space_units:
            if unit.owner == player_id and hasattr(unit, "unit_type"):
                provider = UnitStatsProvider()
                unit_type_enum = UnitType(unit.unit_type)
                stats = provider.get_unit_stats(unit_type_enum)
                if stats.space_cannon:
                    units.append(unit)

        # Get units on planets in the active system
        for planet in active_system.planets:
            for unit in planet.units:
                if unit.owner == player_id and hasattr(unit, "unit_type"):
                    provider = UnitStatsProvider()
                    unit_type_enum = UnitType(unit.unit_type)
                    stats = provider.get_unit_stats(unit_type_enum)
                    if stats.space_cannon:
                        units.append(unit)

        # For PDS II units, also check adjacent systems (Rule 77.3c)
        if hasattr(game_state, "galaxy") and game_state.galaxy:
            # Get all systems adjacent to the active system
            for system_id, system in game_state.systems.items():
                if system_id != active_system_id:
                    # Check if this system is adjacent to the active system
                    if game_state.galaxy.are_systems_adjacent(
                        system_id, active_system_id
                    ):
                        # Check for PDS units with PDS II upgrade on planets in adjacent system
                        for planet in system.planets:
                            for unit in planet.units:
                                if (
                                    unit.owner == player_id
                                    and hasattr(unit, "unit_type")
                                    and unit.unit_type == UnitType.PDS
                                    and hasattr(unit, "_has_pds_ii_upgrade")
                                    and unit._has_pds_ii_upgrade
                                ):
                                    units.append(unit)

        return units

    def _resolve_space_cannon_for_player(
        self, player_id: str, game_state: Any, context: dict[str, Any]
    ) -> None:
        """Resolve space cannon for a specific player."""
        active_system_id = context.get("active_system_id")
        system = game_state.systems.get(active_system_id)

        if system:
            self._execute_player_space_cannon(game_state, system, player_id, context)


@dataclass
class ValidationResult:
    """Result of movement plan validation."""

    is_valid: bool
    transport_assignments: Optional[Any] = None
    errors: Optional[list[str]] = None
    technology_effects: Optional[dict[str, Any]] = None


class MovementValidator:
    """Validates movement plans according to TI4 rules."""

    def __init__(self, galaxy: Any) -> None:
        self.galaxy = galaxy

    def validate_movement_plan(
        self,
        movement_plan: MovementPlan,
        player_id: str,
        technologies: Optional[set[Any]] = None,
    ) -> ValidationResult:
        """Validate an entire movement plan jointly."""
        technologies = technologies or set()
        errors = []
        technology_effects: dict[str, Any] = {}

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
            if not _is_space_location(from_location):
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
        technologies: set[Any],
        technology_effects: dict[str, str],
        ships_valid_without_help: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Apply movement technologies optimally to help ships that need assistance.

        This method is designed to be extensible for future technologies.
        Returns the list of ships that still need help after applying technologies.
        """
        from ..core.constants import Technology

        remaining_ships = ships_needing_help.copy()

        # Convert technologies to string values for comparison
        tech_values = set()
        for tech in technologies:
            if hasattr(tech, "value"):
                tech_values.add(tech.value)
            else:
                tech_values.add(str(tech))

        # Apply Gravity Drive (can only be used once per tactical action)
        if Technology.GRAVITY_DRIVE.value in tech_values:
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

    def activate_system(self, game_state: Any) -> Any:
        """Activate the system by placing a command token (Rule 20.4)."""
        system = game_state.systems.get(self.active_system_id)
        if system:
            system.place_command_token(self.player_id)
        return game_state

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
                SpaceCannonOffenseStep(),
                CommitGroundForcesStep(),
                # Future steps can be added here:
                # SpaceCombatStep(),
                # InvasionStep(),
                # ProductionStep(),
            ]

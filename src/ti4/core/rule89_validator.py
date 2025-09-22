"""Rule 89 validator for ground force placement."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from .constants import GameConstants

if TYPE_CHECKING:
    from .command_sheet import CommandSheet
    from .galaxy import Galaxy
    from .system import System
    from .unit import Unit


@dataclass
class ActivationResult:
    """Result of attempting to activate a system."""

    success: bool
    error_message: str = ""


@dataclass
class MovementResult:
    """Result of attempting to move units."""

    success: bool
    error_message: str = ""


class Rule89Validator:
    """Manages tactical action mechanics according to Rule 89.

    Handles:
    - Step 1: Activation (Rule 89.1) - Place command token
    - Step 2: Movement (Rule 89.2) - Move ships and ground forces
    - Step 3: Space Combat (Rule 89.3) - Resolve combat if applicable
    - Step 4: Invasion (Rule 89.4) - Bombardment and ground combat
    - Step 5: Production (Rule 89.5) - Resolve production abilities
    """

    def __init__(self) -> None:
        """Initialize the tactical action manager."""
        pass

    def _validate_inputs(self, system: "System", player: str) -> None:
        """Validate common inputs for tactical action methods.

        Args:
            system: The system to validate
            player: The player to validate

        Raises:
            ValueError: If inputs are invalid
        """
        if system is None:
            raise ValueError("System cannot be None")
        if not player or not isinstance(player, str):
            raise ValueError("Player must be a non-empty string")

    def _get_player_units_in_space(self, system: "System", player: str) -> list["Unit"]:
        """Get all units belonging to a player in the system's space area.

        Args:
            system: The system to check
            player: The player whose units to find

        Returns:
            List of units belonging to the player in space
        """
        return [unit for unit in system.space_units if unit.owner == player]

    def _get_player_units_on_planets(
        self, system: "System", player: str
    ) -> list["Unit"]:
        """Get all units belonging to a player on planets in the system.

        Args:
            system: The system to check
            player: The player whose units to find

        Returns:
            List of units belonging to the player on planets
        """
        units = []
        for planet in system.planets:
            for unit in planet.units:
                if unit.owner == player:
                    units.append(unit)
        return units

    def can_activate_system(
        self, system: "System", player: str, galaxy: "Galaxy"
    ) -> bool:
        """Check if a player can activate a system.

        Args:
            system: The system to activate
            player: The player attempting activation
            galaxy: The galaxy containing the system

        Returns:
            True if the system can be activated

        Raises:
            ValueError: If inputs are invalid

        LRR Reference: Rule 89.1 - System activation requirements
        """
        self._validate_inputs(system, player)
        if galaxy is None:
            raise ValueError("Galaxy cannot be None")

        # Rule 89.1: Cannot activate system that contains player's command token
        return not system.has_command_token(player)

    def activate_system(
        self,
        system: "System",
        player: str,
        command_sheet: "CommandSheet",
        galaxy: "Galaxy",
    ) -> ActivationResult:
        """Activate a system by placing a command token.

        Args:
            system: The system to activate
            player: The player activating the system
            command_sheet: The player's command sheet
            galaxy: The galaxy containing the system

        Returns:
            Result of the activation attempt

        LRR Reference: Rule 89.1 - System activation with command token placement
        """
        # Check if activation is allowed
        if not self.can_activate_system(system, player, galaxy):
            return ActivationResult(
                success=False, error_message="System already contains command token"
            )

        # Check if player has tactic tokens
        if command_sheet.tactic_pool <= 0:
            return ActivationResult(
                success=False, error_message="No tactic tokens available"
            )

        # Place command token and spend tactic token
        system.place_command_token(player)
        command_sheet.tactic_pool -= 1

        return ActivationResult(success=True)

    def can_move_ship_from_system(
        self,
        ship: "Unit",
        source_system: "System",
        target_system: "System",
        player: str,
        galaxy: "Galaxy",
    ) -> bool:
        """Check if a ship can move from source to target system.

        Args:
            ship: The ship to move
            source_system: The system the ship is moving from
            target_system: The system the ship is moving to
            player: The player moving the ship
            galaxy: The galaxy containing the systems

        Returns:
            True if the ship can move

        LRR Reference: Rule 89.2 - Movement restrictions
        """
        # Rule 89.2: Cannot move from systems with player's command tokens
        if source_system.has_command_token(player):
            return False

        # Ship must belong to the player
        if ship.owner != player:
            return False

        return True

    def execute_movement_step(
        self,
        source_system: "System",
        target_system: "System",
        ships: list["Unit"],
        player: str,
        galaxy: "Galaxy",
        player_technologies: set[str] | None = None,
    ) -> MovementResult:
        """Execute the movement step of tactical action using the advanced movement system.

        Args:
            source_system: The system ships are moving from
            target_system: The system ships are moving to
            ships: List of ships to move
            player: The player executing movement
            galaxy: The galaxy containing the systems
            player_technologies: Set of technologies the player has

        Returns:
            Result of the movement attempt

        LRR Reference: Rule 89.2 - Movement step execution
        """
        from .movement import MovementExecutor, MovementOperation, MovementValidator

        # Create movement validator and executor using existing advanced systems
        validator = MovementValidator(galaxy)

        # Create systems dictionary for executor
        systems_dict = {
            source_system.system_id: source_system,
            target_system.system_id: target_system,
        }
        executor = MovementExecutor(galaxy, systems_dict)

        # Validate and execute each ship movement using the advanced movement system
        for ship in ships:
            # First check Rule 89.2 restrictions
            if not self.can_move_ship_from_system(
                ship, source_system, target_system, player, galaxy
            ):
                return MovementResult(
                    success=False,
                    error_message=f"Cannot move {ship.unit_type} - Rule 89.2 violation",
                )

            # Create movement operation for advanced validation
            # Convert string technologies to Technology enum
            tech_enums = None
            if player_technologies:
                from .constants import Technology

                tech_enums = set()
                for tech_str in player_technologies:
                    if tech_str == "gravity_drive":
                        tech_enums.add(Technology.GRAVITY_DRIVE)
                    # Add other technology conversions as needed

            movement_op = MovementOperation(
                unit=ship,
                from_system_id=source_system.system_id,
                to_system_id=target_system.system_id,
                player_id=player,
                player_technologies=tech_enums,
            )

            # Use advanced movement validation (includes technology effects)
            if not validator.is_valid_movement(movement_op):
                return MovementResult(
                    success=False,
                    error_message=f"Cannot move {ship.unit_type} - insufficient movement range",
                )

            # Execute movement using advanced system
            if not executor.execute_movement(movement_op):
                return MovementResult(
                    success=False,
                    error_message=f"Failed to execute movement for {ship.unit_type}",
                )

        return MovementResult(success=True)

    def requires_space_combat(self, system: "System") -> bool:
        """Check if space combat is required in a system.

        Args:
            system: The system to check

        Returns:
            True if space combat is required

        LRR Reference: Rule 89.3 - Space combat requirements
        """
        # Rule 89.3: Combat required when two players have ships
        players_with_ships = set()
        for unit in system.space_units:
            players_with_ships.add(unit.owner)

        return len(players_with_ships) >= 2

    def can_use_bombardment(self, system: "System", player: str) -> bool:
        """Check if a player can use bombardment abilities.

        Args:
            system: The system to check
            player: The player attempting bombardment

        Returns:
            True if bombardment can be used

        LRR Reference: Rule 89.4 - Bombardment abilities
        """
        # Check if player has ships with bombardment ability in system
        for unit in system.space_units:
            if unit.owner == player:
                # Check if unit has bombardment (simplified for now)
                if hasattr(unit, "has_bombardment") and unit.has_bombardment():
                    return True
        return False

    def can_commit_ground_forces(self, system: "System", player: str) -> bool:
        """Check if a player can commit ground forces to planets.

        Args:
            system: The system to check
            player: The player attempting to commit forces

        Returns:
            True if ground forces can be committed

        Raises:
            ValueError: If inputs are invalid

        LRR Reference: Rule 89.4 - Ground force commitment
        """
        self._validate_inputs(system, player)

        # Check if player has ground forces in space area
        player_units = self._get_player_units_in_space(system, player)
        return any(
            unit.unit_type in GameConstants.GROUND_FORCE_TYPES for unit in player_units
        )

    def can_resolve_production_abilities(self, system: "System", player: str) -> bool:
        """Check if a player can resolve production abilities in a system.

        Args:
            system: The system to check
            player: The player attempting production

        Returns:
            True if production abilities can be resolved

        Raises:
            ValueError: If inputs are invalid

        LRR Reference: Rule 89.5 - Production abilities
        """
        self._validate_inputs(system, player)

        # Check planets for production units
        planet_units = self._get_player_units_on_planets(system, player)
        if any(unit.has_production() for unit in planet_units):
            return True

        # Check space for production units (like war suns with upgrades)
        space_units = self._get_player_units_in_space(system, player)
        return any(unit.has_production() for unit in space_units)

    def validate_galaxy_integration(self, galaxy: "Galaxy") -> bool:
        """Validate integration with galaxy system.

        Args:
            galaxy: The galaxy to validate

        Returns:
            True if integration is valid
        """
        return galaxy is not None

    def validate_command_sheet_integration(self, command_sheet: "CommandSheet") -> bool:
        """Validate integration with command sheet system.

        Args:
            command_sheet: The command sheet to validate

        Returns:
            True if integration is valid
        """
        return command_sheet is not None

    def validate_movement_plan(
        self,
        ships: list["Unit"],
        source_systems: list["System"],
        target_system: "System",
        player: str,
        galaxy: "Galaxy",
        player_technologies: set[str] | None = None,
    ) -> tuple[bool, str]:
        """Validate a complete movement plan using the advanced movement system.

        Args:
            ships: List of ships to move
            source_systems: List of systems ships are moving from
            target_system: The active system ships are moving to
            player: The player executing movement
            galaxy: The galaxy containing the systems
            player_technologies: Set of technologies the player has

        Returns:
            Tuple of (is_valid, error_message)

        LRR Reference: Rule 89.2 - Movement validation with advanced planning
        """
        from .movement import MovementOperation, MovementValidator

        validator = MovementValidator(galaxy)

        # Validate each ship movement
        for i, ship in enumerate(ships):
            source_system = (
                source_systems[i] if i < len(source_systems) else source_systems[0]
            )

            # Check Rule 89.2 restrictions first
            if not self.can_move_ship_from_system(
                ship, source_system, target_system, player, galaxy
            ):
                return (
                    False,
                    f"Rule 89.2 violation: Cannot move {ship.unit_type} from {source_system.system_id}",
                )

            # Create movement operation for advanced validation
            # Convert string technologies to Technology enum
            tech_enums = None
            if player_technologies:
                from .constants import Technology

                tech_enums = set()
                for tech_str in player_technologies:
                    if tech_str == "gravity_drive":
                        tech_enums.add(Technology.GRAVITY_DRIVE)
                    # Add other technology conversions as needed

            movement_op = MovementOperation(
                unit=ship,
                from_system_id=source_system.system_id,
                to_system_id=target_system.system_id,
                player_id=player,
                player_technologies=tech_enums,
            )

            # Use advanced movement validation
            if not validator.is_valid_movement(movement_op):
                return False, f"Insufficient movement range for {ship.unit_type}"

        return True, ""

    def create_movement_plan_integration(
        self,
        ships: list["Unit"],
        source_systems: list["System"],
        target_system: "System",
        player: str,
        galaxy: "Galaxy",
        player_technologies: set[str] | None = None,
    ) -> Any:
        """Create a movement plan using the actions system for complex scenarios.

        This bridges Rule 89 validation with the advanced movement planning system.

        Args:
            ships: List of ships to move
            source_systems: List of systems ships are moving from
            target_system: The active system ships are moving to
            player: The player executing movement
            galaxy: The galaxy containing the systems
            player_technologies: Set of technologies the player has

        Returns:
            MovementPlan from the actions system

        LRR Reference: Rule 89.2 + Advanced movement planning integration
        """
        # Import the actions system for complex movement planning
        from ..actions.movement_engine import MovementPlan

        # Validate the plan first using Rule 89 + advanced movement
        is_valid, error = self.validate_movement_plan(
            ships, source_systems, target_system, player, galaxy, player_technologies
        )

        if not is_valid:
            raise ValueError(f"Invalid movement plan: {error}")

        # Create movement plan using actions system
        movement_plan = MovementPlan()

        for i, ship in enumerate(ships):
            source_system = (
                source_systems[i] if i < len(source_systems) else source_systems[0]
            )
            movement_plan.add_ship_movement(
                ship, source_system.system_id, target_system.system_id
            )

        return movement_plan

    def get_tactical_action_steps(self) -> list[str]:
        """Get the list of tactical action steps.

        Returns:
            List of step names in order

        LRR Reference: Rule 89 - 5-step tactical action sequence
        """
        return ["Activation", "Movement", "Space Combat", "Invasion", "Production"]

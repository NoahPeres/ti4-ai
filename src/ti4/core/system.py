"""System structure for TI4 game board."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .unit import Unit

if TYPE_CHECKING:
    from .constants import AnomalyType, WormholeType
    from .fleet import Fleet
    from .planet import Planet


class System:
    """Represents a star system containing planets."""

    def __init__(self, system_id: str) -> None:
        from .exceptions import AnomalyStateConsistencyError

        if system_id is None:
            raise AnomalyStateConsistencyError("System ID cannot be None")
        if not system_id or (isinstance(system_id, str) and system_id.isspace()):
            raise AnomalyStateConsistencyError("System ID cannot be empty")

        self.system_id = system_id
        self.planets: list[Planet] = []
        self.space_units: list[Unit] = []  # Units in the space area of the system
        self.wormholes: list[str] = []  # List of wormhole types in this system
        self.fleets: list[Fleet] = []  # Fleets in this system
        self.command_tokens: dict[str, bool] = {}  # Player ID -> has command token
        self.anomaly_types: list[
            AnomalyType
        ] = []  # List of anomaly types in this system

    def place_command_token(self, player_id: str) -> None:
        """Place a command token for a player in this system (Rule 20.4)."""
        self.command_tokens[player_id] = True

    def remove_command_token(self, player_id: str) -> None:
        """Remove a command token for a player from this system."""
        self.command_tokens.pop(player_id, None)

    def has_command_token(self, player_id: str) -> bool:
        """Check if a player has a command token in this system."""
        return self.command_tokens.get(player_id, False)

    def get_players_with_command_tokens(self) -> list[str]:
        """Get list of players who have command tokens in this system."""
        return [
            player_id
            for player_id, has_token in self.command_tokens.items()
            if has_token
        ]

    def has_enemy_ships(self, player_id: str) -> bool:
        """Check if this system contains enemy movement-blocking ships (Rule 58.4b).

        Fighters are intentionally excluded: they do not block movement.
        For combat detection, use the combat-related API instead.
        """
        from .constants import GameConstants

        # Use NON_FIGHTER_SHIP_TYPES for movement blocking rules
        ship_types = GameConstants.NON_FIGHTER_SHIP_TYPES

        for unit in self.space_units:
            if unit.owner != player_id and unit.unit_type in ship_types:
                return True
        return False

    def place_unit_in_space(self, unit: Unit) -> None:
        """Place a unit in the space area of this system."""
        self.space_units.append(unit)

    def remove_unit_from_space(self, unit: Unit) -> None:
        """Remove a unit from the space area of this system."""
        self.space_units.remove(unit)

    def place_unit_on_planet(self, unit: Unit, planet_name: str) -> None:
        """Place a unit on a specific planet in this system."""
        planet = self.get_planet_by_name(planet_name)
        if planet:
            planet.place_unit(unit)

    def remove_unit_from_planet(self, unit: Unit, planet_name: str) -> None:
        """Remove a unit from a specific planet in this system."""
        planet = self.get_planet_by_name(planet_name)
        if planet:
            planet.remove_unit(unit)

    def get_planet_by_name(self, planet_name: str) -> Planet | None:
        """Get a planet by name from this system."""
        for planet in self.planets:
            if planet.name == planet_name:
                return planet
        return None

    def add_planet(self, planet: Planet) -> None:
        """Add a planet to this system."""
        self.planets.append(planet)

    def add_fleet(self, fleet: Fleet) -> None:
        """Add a fleet to this system."""
        self.fleets.append(fleet)

    def add_wormhole(self, wormhole_type: str | WormholeType) -> None:
        """
        Add a wormhole of the specified type to this system.

        Implements support for LRR 101 wormhole adjacency rules.
        Valid wormhole types: alpha, beta, gamma, delta

        Args:
            wormhole_type: Type of wormhole to add (WormholeType enum or string)

        Raises:
            ValueError: If wormhole_type is invalid
        """
        from .constants import WormholeType

        if not wormhole_type:
            raise ValueError("Wormhole type cannot be empty")

        # Convert enum to string value for internal storage
        if isinstance(wormhole_type, WormholeType):
            wormhole_str = wormhole_type.value
        else:
            wormhole_str = wormhole_type

        valid_types = {"alpha", "beta", "gamma", "delta"}
        if wormhole_str not in valid_types:
            raise ValueError(
                f"Invalid wormhole type: {wormhole_str}. Valid types: {valid_types}"
            )

        # Avoid duplicates
        if wormhole_str not in self.wormholes:
            self.wormholes.append(wormhole_str)

    def has_wormhole(self, wormhole_type: str) -> bool:
        """
        Check if this system has a wormhole of the specified type.

        Args:
            wormhole_type: Type of wormhole to check for

        Returns:
            True if system contains the specified wormhole type, False otherwise
        """
        return wormhole_type in self.wormholes

    def get_wormhole_types(self) -> list[str]:
        """
        Get all wormhole types present in this system.

        Returns:
            List of wormhole types in this system (copy to prevent external modification)
        """
        return self.wormholes.copy()

    def remove_wormhole(self, wormhole_type: str) -> bool:
        """
        Remove a wormhole of the specified type from this system.

        Args:
            wormhole_type: Type of wormhole to remove

        Returns:
            True if wormhole was removed, False if it wasn't present
        """
        if wormhole_type in self.wormholes:
            self.wormholes.remove(wormhole_type)
            return True
        return False

    def get_units_in_space(self) -> list[Unit]:
        """Get all units in the space area of this system."""
        return self.space_units.copy()

    def get_units_on_planet(self, planet_name: str) -> list[Unit]:
        """Get all units on a specific planet in this system."""
        planet = self.get_planet_by_name(planet_name)
        if planet:
            return planet.units.copy()
        return []

    def get_ground_forces_on_planet(self, planet_name: str) -> list[Unit]:
        """Get all ground force units on a specific planet in this system."""
        from .constants import GameConstants

        planet = self.get_planet_by_name(planet_name)
        if planet:
            # Filter for ground force units (infantry, mechs, etc.)
            return [
                unit
                for unit in planet.units
                if unit.unit_type in GameConstants.GROUND_FORCE_TYPES
            ]
        return []

    def _normalize_anomaly_type(self, anomaly_type: AnomalyType | str) -> AnomalyType:
        """Convert anomaly type to enum, with validation.

        Args:
            anomaly_type: Anomaly type as enum or string

        Returns:
            AnomalyType enum

        Raises:
            InvalidAnomalyTypeError: If anomaly_type is None, empty, or invalid
        """
        from .exceptions import InvalidAnomalyTypeError

        if anomaly_type is None:
            raise InvalidAnomalyTypeError("Anomaly type cannot be None")

        from .constants import AnomalyType as AnomalyTypeEnum

        if isinstance(anomaly_type, str):
            # Check for empty or whitespace-only strings
            if not anomaly_type or anomaly_type.isspace():
                raise InvalidAnomalyTypeError("Anomaly type cannot be empty")

            try:
                return AnomalyTypeEnum(anomaly_type)
            except ValueError as e:
                raise InvalidAnomalyTypeError(
                    f"Invalid anomaly type: {anomaly_type}"
                ) from e

        return anomaly_type

    def add_anomaly_type(self, anomaly_type: AnomalyType | str) -> None:
        """Add an anomaly type to this system.

        Implements Rule 9: ANOMALIES - Systems can have anomaly properties.
        Multiple anomaly types can exist on the same system (Rule 9.5).

        Args:
            anomaly_type: The anomaly type to add (enum or string)

        Raises:
            ValueError: If anomaly_type is None or invalid

        LRR References:
            - Rule 9: ANOMALIES - Core anomaly system
            - Rule 9.5: Multiple anomaly types on same system
        """
        normalized_type = self._normalize_anomaly_type(anomaly_type)

        if normalized_type not in self.anomaly_types:
            self.anomaly_types.append(normalized_type)

    def remove_anomaly_type(self, anomaly_type: AnomalyType | str) -> None:
        """Remove an anomaly type from this system.

        Args:
            anomaly_type: The anomaly type to remove (enum or string)

        Raises:
            ValueError: If anomaly_type is None or invalid

        Note:
            Does not raise error if anomaly type is not present.
        """
        normalized_type = self._normalize_anomaly_type(anomaly_type)

        if normalized_type in self.anomaly_types:
            self.anomaly_types.remove(normalized_type)

    def has_anomaly_type(self, anomaly_type: AnomalyType | str) -> bool:
        """Check if this system has a specific anomaly type.

        Args:
            anomaly_type: The anomaly type to check for (enum or string)

        Returns:
            True if system has the specified anomaly type, False otherwise

        Raises:
            ValueError: If anomaly_type is None or invalid
        """
        normalized_type = self._normalize_anomaly_type(anomaly_type)
        return normalized_type in self.anomaly_types

    def get_anomaly_types(self) -> list[AnomalyType]:
        """Get all anomaly types present in this system.

        Returns:
            Copy of anomaly types list to prevent external modification

        Raises:
            AnomalyStateConsistencyError: If anomaly types list is corrupted

        LRR References:
            - Rule 9.1: Anomaly identification
            - Rule 9.5: Multiple anomaly types
        """
        from .exceptions import AnomalyStateConsistencyError

        # Validate anomaly types list for corruption
        if any(anomaly_type is None for anomaly_type in self.anomaly_types):
            raise AnomalyStateConsistencyError(
                "Corrupted anomaly types: None values found"
            )

        return self.anomaly_types.copy()

    def is_anomaly(self) -> bool:
        """Check if this system is an anomaly (has any anomaly types).

        Returns:
            True if system has any anomaly types, False otherwise

        LRR References:
            - Rule 9: ANOMALIES - Core anomaly identification
            - Rule 88.4: Red-backed anomaly tiles
        """
        return len(self.anomaly_types) > 0

    def get_system_info_display(self) -> dict[str, Any]:
        """Get formatted system information for display purposes.

        Provides comprehensive system information including anomaly status,
        effects summary, and other system properties for user interfaces.

        Returns:
            Dictionary containing formatted system information

        Raises:
            ValueError: If system is in an invalid state

        LRR References:
            - Rule 9.1: Anomaly identification
            - Rule 9.3: Art identification (display requirements)
        """

        # Validate system state
        from .exceptions import AnomalyStateConsistencyError

        if not self.system_id:
            raise AnomalyStateConsistencyError("System ID cannot be empty")

        # Basic system information
        info: dict[str, Any] = {
            "system_id": self.system_id,
            "is_anomaly": self.is_anomaly(),
            "anomaly_status": self._format_anomaly_status(),
            "planets": self._format_planet_info(),
            "effects_summary": self._format_effects_summary(),
        }

        return info

    def _format_anomaly_status(self) -> str:
        """Format anomaly status for display.

        Returns:
            Human-readable string describing anomaly status
        """
        if not self.is_anomaly():
            return "Normal System"

        anomaly_names = []
        for anomaly_type in self.anomaly_types:
            # Handle corrupted anomaly types gracefully
            if anomaly_type is None:
                continue
            # Convert enum values to display names
            display_name = anomaly_type.value.replace("_", " ").title()
            anomaly_names.append(display_name)

        if len(anomaly_names) == 1:
            return f"Anomaly: {anomaly_names[0]}"
        else:
            return f"Multiple Anomalies: {', '.join(anomaly_names)}"

    def _format_planet_info(self) -> list[dict[str, Any]]:
        """Format planet information for display.

        Returns:
            List of dictionaries containing planet information
        """

        planet_info: list[dict[str, Any]] = []
        for planet in self.planets:
            if planet is not None:  # Defensive programming
                planet_info.append(
                    {
                        "name": getattr(planet, "name", "Unknown Planet"),
                        "resources": getattr(planet, "resources", 0),
                        "influence": getattr(planet, "influence", 0),
                    }
                )
        return planet_info

    def _format_effects_summary(self) -> list[str]:
        """Format anomaly effects summary for display.

        Returns:
            List of human-readable effect descriptions
        """
        if not self.is_anomaly():
            return []

        effects = []

        try:
            # Import AnomalyManager to get effects
            from .anomaly_manager import AnomalyManager

            manager = AnomalyManager()
            anomaly_effects = manager.get_anomaly_effects_summary(self)

            # Format movement effects
            if anomaly_effects.get("blocks_movement", False):
                if anomaly_effects.get("requires_active_system", False):
                    effects.append("Movement blocked (requires active system)")
                else:
                    effects.append("Movement completely blocked")

            # Format move value effects
            move_modifier = anomaly_effects.get("move_value_modifier", 0)
            if move_modifier < 0:
                effects.append("Move value reduced to 1")
            elif move_modifier > 0:
                effects.append(f"Move value bonus: +{move_modifier}")

            # Format combat effects
            combat_bonus = anomaly_effects.get("combat_bonus", 0)
            if combat_bonus > 0:
                effects.append(f"Combat bonus: +{combat_bonus} for defenders")

            # Add specific anomaly type effects
            for anomaly_type in self.anomaly_types:
                if anomaly_type.value == "gravity_rift":
                    effects.append("Destruction risk when exiting (roll 1-3)")

        except Exception:
            # Fallback to basic anomaly type listing if effects calculation fails
            effects.append("Anomaly effects available (calculation error)")

        return effects

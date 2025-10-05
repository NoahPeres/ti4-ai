"""
AnomalyManager - High-level interface for managing anomaly systems.

This module provides a high-level interface for managing anomaly systems
and coordinating anomaly operations, supporting dynamic anomaly assignment
and effect stacking.

LRR References:
- Rule 9.4: Ability-created anomalies
- Rule 9.5: Multiple anomaly types on same system
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .constants import AnomalyType
    from .system import System


class AnomalyEffectConstants:
    """Constants for anomaly effects and calculations."""

    # Movement blocking anomaly types
    MOVEMENT_BLOCKING_ANOMALIES = frozenset(["asteroid_field", "supernova", "nebula"])

    # Effect values
    NEBULA_MOVE_VALUE_MODIFIER = -1  # Simplified representation of "move value = 1"
    GRAVITY_RIFT_MOVE_VALUE_MODIFIER = 1  # +1 when exiting/passing through
    NEBULA_COMBAT_BONUS = 1  # +1 to defender combat rolls

    # Default values
    DEFAULT_MOVE_VALUE_MODIFIER = 0
    DEFAULT_COMBAT_BONUS = 0


class AnomalyManager:
    """Manages anomaly systems and effects.

    Provides a high-level interface for creating, modifying, and querying
    anomaly systems while maintaining system properties and supporting
    multiple anomaly types with effect stacking.

    LRR References:
        - Rule 9.4: Ability-created anomalies
        - Rule 9.5: Multiple anomaly types on same system
    """

    def create_anomaly_system(
        self, system_id: str, anomaly_types: list[AnomalyType]
    ) -> System:
        """Create a new system with the specified anomaly types.

        Args:
            system_id: Unique identifier for the system
            anomaly_types: List of anomaly types to add to the system

        Returns:
            System with the specified anomaly types

        Raises:
            ValueError: If system_id is empty or anomaly_types contains invalid types
        """
        from .exceptions import AnomalyStateConsistencyError

        if not system_id:
            raise AnomalyStateConsistencyError("System ID cannot be empty")

        from .system import System

        system = System(system_id)

        for anomaly_type in anomaly_types:
            system.add_anomaly_type(anomaly_type)

        return system

    def get_anomaly_effects_summary(self, system: System) -> dict[str, Any]:
        """Get a summary of all anomaly effects for a system.

        Args:
            system: The system to analyze

        Returns:
            Dictionary containing anomaly effects summary

        Raises:
            ValueError: If system is None
        """
        self._validate_system(system)

        anomaly_types = system.get_anomaly_types()

        return {
            "anomaly_types": anomaly_types,
            "blocks_movement": self._system_blocks_movement(anomaly_types),
            "requires_active_system": self._system_requires_active_system(
                anomaly_types
            ),
            "move_value_modifier": self._calculate_move_value_modifier(anomaly_types),
            "combat_bonus": self._calculate_combat_bonus(anomaly_types),
        }

    def _validate_system(self, system: System) -> None:
        """Validate that system is not None and has valid state.

        Args:
            system: The system to validate

        Raises:
            AnomalyStateConsistencyError: If system is None or has invalid state
        """
        from .exceptions import AnomalyStateConsistencyError

        if system is None:
            raise AnomalyStateConsistencyError("System cannot be None")

        # Check for invalid system state
        if hasattr(system, "system_id") and not system.system_id:
            raise AnomalyStateConsistencyError(
                "System has invalid state: empty system_id"
            )

    def _system_blocks_movement(self, anomaly_types: list[AnomalyType]) -> bool:
        """Check if anomaly types include movement-blocking anomalies.

        Args:
            anomaly_types: List of anomaly types to check

        Returns:
            True if any anomaly type blocks movement, False otherwise
        """
        return any(
            anomaly_type.value in AnomalyEffectConstants.MOVEMENT_BLOCKING_ANOMALIES
            for anomaly_type in anomaly_types
        )

    def _system_requires_active_system(self, anomaly_types: list[AnomalyType]) -> bool:
        """Check if anomaly types require the system to be active (nebula rule).

        Args:
            anomaly_types: List of anomaly types to check

        Returns:
            True if system requires being active, False otherwise
        """
        from .constants import AnomalyType

        return AnomalyType.NEBULA in anomaly_types

    def _calculate_move_value_modifier(self, anomaly_types: list[AnomalyType]) -> int:
        """Calculate move value modifier for anomaly types.

        Args:
            anomaly_types: List of anomaly types to analyze

        Returns:
            Move value modifier (positive for bonus, negative for penalty)
        """
        from .constants import AnomalyType

        if AnomalyType.NEBULA in anomaly_types:
            return AnomalyEffectConstants.NEBULA_MOVE_VALUE_MODIFIER
        elif AnomalyType.GRAVITY_RIFT in anomaly_types:
            return AnomalyEffectConstants.GRAVITY_RIFT_MOVE_VALUE_MODIFIER

        return AnomalyEffectConstants.DEFAULT_MOVE_VALUE_MODIFIER

    def _calculate_combat_bonus(self, anomaly_types: list[AnomalyType]) -> int:
        """Calculate combat bonus for anomaly types.

        Args:
            anomaly_types: List of anomaly types to analyze

        Returns:
            Combat bonus for defenders in this system
        """
        from .constants import AnomalyType

        if AnomalyType.NEBULA in anomaly_types:
            return AnomalyEffectConstants.NEBULA_COMBAT_BONUS

        return AnomalyEffectConstants.DEFAULT_COMBAT_BONUS

    def add_anomaly_to_system(
        self, system: System, anomaly_type: AnomalyType | str
    ) -> None:
        """Add an anomaly type to an existing system.

        Args:
            system: The system to modify
            anomaly_type: The anomaly type to add

        Raises:
            ValueError: If system is None or anomaly_type is invalid
        """
        self._validate_system(system)
        self._validate_anomaly_type(anomaly_type)
        system.add_anomaly_type(anomaly_type)

    def remove_anomaly_from_system(
        self, system: System, anomaly_type: AnomalyType | str
    ) -> None:
        """Remove an anomaly type from an existing system.

        Args:
            system: The system to modify
            anomaly_type: The anomaly type to remove

        Raises:
            ValueError: If system is None or anomaly_type is invalid
        """
        self._validate_system(system)
        self._validate_anomaly_type(anomaly_type)
        system.remove_anomaly_type(anomaly_type)

    def _validate_anomaly_type(self, anomaly_type: AnomalyType | str | None) -> None:
        """Validate that anomaly_type is not None.

        Args:
            anomaly_type: The anomaly type to validate

        Raises:
            ValueError: If anomaly_type is None
        """
        from .exceptions import InvalidAnomalyTypeError

        if anomaly_type is None:
            raise InvalidAnomalyTypeError("Anomaly type cannot be None")

    def clear_all_anomalies_from_system(self, system: System) -> None:
        """Remove all anomaly types from a system.

        Args:
            system: The system to modify

        Raises:
            ValueError: If system is None
        """
        self._validate_system(system)

        # Get copy of anomaly types to avoid modifying list while iterating
        anomaly_types = system.get_anomaly_types()
        for anomaly_type in anomaly_types:
            system.remove_anomaly_type(anomaly_type)

    def convert_system_to_anomaly_type(
        self, system: System, anomaly_type: AnomalyType | str
    ) -> None:
        """Convert a system to have only the specified anomaly type.

        Removes all existing anomaly types and adds the specified one.
        Preserves all other system properties (planets, wormholes, etc.).

        Args:
            system: The system to convert
            anomaly_type: The anomaly type to set

        Raises:
            ValueError: If system is None or anomaly_type is invalid
        """
        self._validate_system(system)
        self._validate_anomaly_type(anomaly_type)

        # Clear existing anomalies
        self.clear_all_anomalies_from_system(system)

        # Add new anomaly type
        system.add_anomaly_type(anomaly_type)

    def is_system_blocking_movement(self, system: System) -> bool:
        """Check if a system blocks movement.

        Args:
            system: The system to check

        Returns:
            True if system blocks movement, False otherwise

        Raises:
            ValueError: If system is None
        """
        self._validate_system(system)
        return self._system_blocks_movement(system.get_anomaly_types())

    def get_system_move_value_modifier(self, system: System) -> int:
        """Get the move value modifier for a system.

        Args:
            system: The system to check

        Returns:
            Move value modifier (positive for bonus, negative for penalty)

        Raises:
            ValueError: If system is None
        """
        self._validate_system(system)
        return self._calculate_move_value_modifier(system.get_anomaly_types())

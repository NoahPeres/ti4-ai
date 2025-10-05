"""
Enhanced movement validation with anomaly integration.

This module provides comprehensive movement validation that integrates
with the anomaly system to provide detailed error messages and
movement cost calculations.

LRR References:
- Rule 58: Movement integration with all anomaly types
- Requirements: 8.1, 8.2, 8.3, 8.4
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .constants import AnomalyType


@dataclass
class MovementValidationResult:
    """Result of comprehensive movement validation with anomaly effects."""

    is_valid: bool
    error_message: str
    blocked_systems: list[str]
    effective_movement_range: int
    anomaly_effects_applied: list[str]


@dataclass
class AnomalyMovementError:
    """Details about an anomaly that blocks movement."""

    system_id: str
    anomaly_type: AnomalyType
    error_message: str
    requires_active_system: bool = False

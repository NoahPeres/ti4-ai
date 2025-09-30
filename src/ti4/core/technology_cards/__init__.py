"""
Technology card framework for TI4.

This module provides the base protocols and interfaces for implementing
concrete technology cards in the TI4 game system.
"""

from .base import (
    BaseTechnologyCard,
    ExhaustibleTechnologyCard,
    PassiveTechnologyCard,
    UnitUpgradeTechnologyCard,
)
from .factory import TechnologyCardFactory
from .integration import (
    TechnologyFrameworkIntegration,
    get_technology_framework_integration,
    initialize_technology_framework,
)
from .protocols import (
    ExhaustibleTechnologyProtocol,
    TechnologyCardProtocol,
    UnitUpgradeTechnologyProtocol,
)
from .registry import TechnologyCardRegistry

__all__ = [
    # Protocols
    "TechnologyCardProtocol",
    "ExhaustibleTechnologyProtocol",
    "UnitUpgradeTechnologyProtocol",
    # Base implementations
    "BaseTechnologyCard",
    "ExhaustibleTechnologyCard",
    "PassiveTechnologyCard",
    "UnitUpgradeTechnologyCard",
    # Registry
    "TechnologyCardRegistry",
    # Factory
    "TechnologyCardFactory",
    # Integration
    "TechnologyFrameworkIntegration",
    "get_technology_framework_integration",
    "initialize_technology_framework",
]

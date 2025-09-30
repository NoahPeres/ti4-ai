"""
Technology card factory system.

This module provides the TechnologyCardFactory for instantiating technology cards
using enum-based specifications with caching functionality.

The factory follows the singleton pattern for technology card instances,
ensuring that each technology type has only one instance throughout the
application lifecycle.
"""

from ti4.core.constants import Technology
from ti4.core.technology_cards.protocols import TechnologyCardProtocol


class TechnologyCardFactory:
    """
    Factory for instantiating technology cards using enum-based specifications.

    This factory provides centralized creation of technology card instances
    with caching to ensure single instances per technology type. The factory
    automatically registers all available concrete implementations and provides
    methods for querying supported technologies.

    Example:
        >>> factory = TechnologyCardFactory()
        >>> dark_energy_tap = factory.create_card(Technology.DARK_ENERGY_TAP)
        >>> gravity_drive = factory.create_card(Technology.GRAVITY_DRIVE)
        >>>
        >>> # Same instance returned from cache
        >>> same_card = factory.create_card(Technology.DARK_ENERGY_TAP)
        >>> assert dark_energy_tap is same_card
    """

    def __init__(self) -> None:
        """
        Initialize the technology card factory.

        Automatically registers all available technology card implementations
        and initializes the instance cache.
        """
        self._cache: dict[Technology, TechnologyCardProtocol] = {}
        self._implementations: dict[Technology, type[TechnologyCardProtocol]] = {}
        self._register_implementations()

    def _validate_technology_enum(self, technology: Technology) -> None:
        """
        Validate that the provided technology is a valid Technology enum.

        Args:
            technology: The value to validate

        Raises:
            TypeError: If technology is not a Technology enum
        """
        if not isinstance(technology, Technology):
            raise TypeError(
                f"Expected Technology enum, got {type(technology).__name__}. "
                f"Received value: {technology!r}"
            )

    def _register_implementations(self) -> None:
        """
        Register all available technology card implementations.

        This method imports and registers concrete technology card implementations.
        New implementations should be added here to make them available through
        the factory.

        Note:
            Imports are done locally to avoid circular import issues and to
            keep the factory lightweight when not all implementations are needed.
        """
        # Import concrete implementations
        from ti4.core.technology_cards.concrete.dark_energy_tap import DarkEnergyTap
        from ti4.core.technology_cards.concrete.gravity_drive import GravityDrive

        # Register implementations with their corresponding Technology enum
        self._implementations[Technology.DARK_ENERGY_TAP] = DarkEnergyTap
        self._implementations[Technology.GRAVITY_DRIVE] = GravityDrive

    def create_card(self, technology: Technology) -> TechnologyCardProtocol:
        """
        Create a technology card instance with caching.

        This method returns a cached instance if one exists, otherwise creates
        a new instance and caches it for future use. This ensures that each
        technology type has only one instance throughout the application.

        Args:
            technology: The Technology enum to create a card for

        Returns:
            TechnologyCardProtocol implementation for the technology

        Raises:
            TypeError: If technology is not a Technology enum
            ValueError: If no implementation is found for the technology

        Example:
            >>> factory = TechnologyCardFactory()
            >>> card = factory.create_card(Technology.DARK_ENERGY_TAP)
            >>> assert card.name == "Dark Energy Tap"
        """
        self._validate_technology_enum(technology)

        # Return cached instance if available
        if technology in self._cache:
            return self._cache[technology]

        # Check if implementation exists
        if technology not in self._implementations:
            supported = [tech.name for tech in self._implementations.keys()]
            raise ValueError(
                f"No implementation found for {technology.name}. "
                f"Supported technologies: {', '.join(supported)}"
            )

        # Create new instance
        implementation_class = self._implementations[technology]
        try:
            instance = implementation_class()
        except Exception as e:
            raise ValueError(
                f"Failed to create instance of {technology.name}: {e}"
            ) from e

        # Cache the instance
        self._cache[technology] = instance

        return instance

    def clear_cache(self) -> None:
        """
        Clear the factory cache.

        This removes all cached technology card instances, forcing new instances
        to be created on the next call to create_card(). This is primarily
        useful for testing scenarios.

        Note:
            Clearing the cache does not affect the registered implementations,
            only the cached instances.
        """
        self._cache.clear()

    def is_supported(self, technology: Technology) -> bool:
        """
        Check if a technology is supported by the factory.

        Args:
            technology: The Technology enum to check

        Returns:
            True if the technology is supported, False otherwise

        Raises:
            TypeError: If technology is not a Technology enum

        Example:
            >>> factory = TechnologyCardFactory()
            >>> assert factory.is_supported(Technology.DARK_ENERGY_TAP)
            >>> assert not factory.is_supported(Technology.CRUISER_II)
        """
        self._validate_technology_enum(technology)
        return technology in self._implementations

    def get_supported_technologies(self) -> list[Technology]:
        """
        Get all technologies supported by the factory.

        Returns:
            List of supported Technology enums, sorted by name for consistency

        Example:
            >>> factory = TechnologyCardFactory()
            >>> supported = factory.get_supported_technologies()
            >>> assert Technology.DARK_ENERGY_TAP in supported
            >>> assert Technology.GRAVITY_DRIVE in supported
        """
        return sorted(self._implementations.keys(), key=lambda tech: tech.name)

    def get_cache_size(self) -> int:
        """
        Get the current number of cached technology card instances.

        Returns:
            Number of cached instances

        Note:
            This method is primarily useful for debugging and testing.
        """
        return len(self._cache)

    def is_cached(self, technology: Technology) -> bool:
        """
        Check if a technology card instance is currently cached.

        Args:
            technology: The Technology enum to check

        Returns:
            True if an instance is cached, False otherwise

        Raises:
            TypeError: If technology is not a Technology enum
        """
        self._validate_technology_enum(technology)
        return technology in self._cache

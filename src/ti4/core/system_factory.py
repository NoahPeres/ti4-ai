"""System factory for creating specific game systems."""

from .constants import SystemConstants
from .planet import Planet
from .system import System


class SystemFactory:
    """Factory for creating specific game systems with their planets."""

    @staticmethod
    def create_mecatol_rex_system() -> System:
        """Create the Mecatol Rex system (System ID: 18).

        Mecatol Rex is the galactic center with:
        - System ID: "18"
        - One planet: "Mecatol Rex"
        - Planet stats: 1 resource, 6 influence
        - No planet traits or technology specialties

        Returns:
            System containing the Mecatol Rex planet
        """
        system = System(SystemConstants.MECATOL_REX_ID)
        mecatol_rex_planet = Planet(name="Mecatol Rex", resources=1, influence=6)
        system.add_planet(mecatol_rex_planet)
        return system

    @staticmethod
    def create_system_with_planets(
        system_id: str, planet_configs: list[tuple[str, int, int]]
    ) -> System:
        """Create a system with multiple planets.

        Args:
            system_id: The system identifier
            planet_configs: List of (name, resources, influence) tuples

        Returns:
            System containing the specified planets
        """
        system = System(system_id)
        for name, resources, influence in planet_configs:
            planet = Planet(name=name, resources=resources, influence=influence)
            system.add_planet(planet)
        return system

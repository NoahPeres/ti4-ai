"""Tests for planet resource generation."""

import pytest

from ti4.core.planet import Planet


class TestPlanetResources:
    """Test planet resource collection and exhaustion mechanics."""

    def test_planet_starts_refreshed(self):
        """Test that planets start in refreshed state."""
        planet = Planet(name="Mecatol Rex", resources=1, influence=6)
        assert not planet.is_exhausted

    def test_planet_can_be_exhausted(self):
        """Test that planets can be exhausted."""
        planet = Planet(name="Mecatol Rex", resources=1, influence=6)
        exhausted_planet = planet.exhaust()
        assert exhausted_planet.is_exhausted
        assert exhausted_planet.name == planet.name
        assert exhausted_planet.resources == planet.resources

    def test_planet_can_be_refreshed(self):
        """Test that exhausted planets can be refreshed."""
        planet = Planet(name="Mecatol Rex", resources=1, influence=6)
        exhausted_planet = planet.exhaust()
        refreshed_planet = exhausted_planet.refresh()
        assert not refreshed_planet.is_exhausted

    def test_cannot_exhaust_already_exhausted_planet(self):
        """Test that already exhausted planets cannot be exhausted again."""
        planet = Planet(name="Mecatol Rex", resources=1, influence=6)
        exhausted_planet = planet.exhaust()
        with pytest.raises(ValueError, match="Planet Mecatol Rex is already exhausted"):
            exhausted_planet.exhaust()

    def test_cannot_refresh_already_refreshed_planet(self):
        """Test that already refreshed planets cannot be refreshed again."""
        planet = Planet(name="Mecatol Rex", resources=1, influence=6)
        with pytest.raises(ValueError, match="Planet Mecatol Rex is already refreshed"):
            planet.refresh()

    def test_can_collect_resources_from_refreshed_planet(self):
        """Test that resources can be collected from refreshed planets."""
        planet = Planet(name="Jord", resources=4, influence=2)
        assert planet.can_collect_resources()
        assert planet.get_resource_value() == 4

    def test_cannot_collect_resources_from_exhausted_planet(self):
        """Test that resources cannot be collected from exhausted planets."""
        planet = Planet(name="Jord", resources=4, influence=2)
        exhausted_planet = planet.exhaust()
        assert not exhausted_planet.can_collect_resources()

    def test_can_collect_influence_from_refreshed_planet(self):
        """Test that influence can be collected from refreshed planets."""
        planet = Planet(name="Jord", resources=4, influence=2)
        assert planet.can_collect_influence()
        assert planet.get_influence_value() == 2

    def test_cannot_collect_influence_from_exhausted_planet(self):
        """Test that influence cannot be collected from exhausted planets."""
        planet = Planet(name="Jord", resources=4, influence=2)
        exhausted_planet = planet.exhaust()
        assert not exhausted_planet.can_collect_influence()

    def test_planet_resource_spending_mechanics(self):
        """Test that planets can be used for spending resources/influence."""
        planet = Planet(name="Jord", resources=4, influence=2, controlled_by="player1")

        # Planet should be available for spending when refreshed
        assert planet.can_collect_resources()
        assert planet.can_collect_influence()
        assert planet.get_resource_value() == 4
        assert planet.get_influence_value() == 2

        # After exhausting, planet cannot provide resources/influence
        exhausted_planet = planet.exhaust()
        assert not exhausted_planet.can_collect_resources()
        assert not exhausted_planet.can_collect_influence()

    def test_planet_refresh_cycle(self):
        """Test the planet refresh cycle that happens during status phase."""
        planet = Planet(name="Jord", resources=4, influence=2, controlled_by="player1")

        # Exhaust planet (e.g., during spending for technology research)
        exhausted_planet = planet.exhaust()
        assert exhausted_planet.is_exhausted

        # Refresh during status phase
        refreshed_planet = exhausted_planet.refresh()
        assert not refreshed_planet.is_exhausted
        assert refreshed_planet.can_collect_resources()
        assert refreshed_planet.can_collect_influence()

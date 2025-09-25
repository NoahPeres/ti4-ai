"""Tests for system factory."""

import pytest

from src.ti4.core.system_factory import SystemFactory


class TestSystemFactory:
    """Test system factory functionality."""

    def test_create_mecatol_rex_system(self) -> None:
        """Test creation of Mecatol Rex system with correct properties."""
        system = SystemFactory.create_mecatol_rex_system()

        # Verify system ID
        assert system.system_id == "18"

        # Verify it has exactly one planet
        assert len(system.planets) == 1

        # Verify planet properties
        mecatol_rex = system.planets[0]
        assert mecatol_rex.name == "Mecatol Rex"
        assert mecatol_rex.resources == 1
        assert mecatol_rex.influence == 6

        # Verify planet is initially uncontrolled
        assert mecatol_rex.controlled_by is None

        # Verify planet starts ready (not exhausted)
        assert not mecatol_rex.is_exhausted()
        assert mecatol_rex.is_faceup()

    def test_mecatol_rex_planet_can_be_controlled(self) -> None:
        """Test that Mecatol Rex planet can be controlled by a player."""
        system = SystemFactory.create_mecatol_rex_system()
        mecatol_rex = system.planets[0]

        # Should be able to set control
        mecatol_rex.set_control("player1")
        assert mecatol_rex.controlled_by == "player1"

    def test_mecatol_rex_planet_can_be_exhausted(self) -> None:
        """Test that Mecatol Rex planet can be exhausted and readied."""
        system = SystemFactory.create_mecatol_rex_system()
        mecatol_rex = system.planets[0]

        # Should start ready
        assert not mecatol_rex.is_exhausted()

        # Should be able to exhaust
        mecatol_rex.exhaust()
        assert mecatol_rex.is_exhausted()
        assert not mecatol_rex.is_faceup()

        # Should be able to ready
        mecatol_rex.ready()
        assert not mecatol_rex.is_exhausted()
        assert mecatol_rex.is_faceup()

    def test_mecatol_rex_planet_double_exhaust_raises_error(self) -> None:
        """Test that double exhausting Mecatol Rex raises ValueError."""
        system = SystemFactory.create_mecatol_rex_system()
        mecatol_rex = system.planets[0]

        # Exhaust once
        mecatol_rex.exhaust()

        # Double exhaust should raise error
        with pytest.raises(ValueError, match="Card is already exhausted"):
            mecatol_rex.exhaust()

    def test_create_system_with_planets(self) -> None:
        """Test creation of system with multiple planets."""
        planet_configs = [("Planet A", 2, 1), ("Planet B", 1, 3), ("Planet C", 0, 2)]

        system = SystemFactory.create_system_with_planets("test_system", planet_configs)

        # Verify system ID
        assert system.system_id == "test_system"

        # Verify correct number of planets
        assert len(system.planets) == 3

        # Verify planet properties
        planet_a = system.get_planet_by_name("Planet A")
        assert planet_a is not None
        assert planet_a.resources == 2
        assert planet_a.influence == 1

        planet_b = system.get_planet_by_name("Planet B")
        assert planet_b is not None
        assert planet_b.resources == 1
        assert planet_b.influence == 3

        planet_c = system.get_planet_by_name("Planet C")
        assert planet_c is not None
        assert planet_c.resources == 0
        assert planet_c.influence == 2

    def test_create_system_with_no_planets(self) -> None:
        """Test creation of system with no planets."""
        system = SystemFactory.create_system_with_planets("empty_system", [])

        assert system.system_id == "empty_system"
        assert len(system.planets) == 0

    def test_mecatol_rex_system_has_no_space_units_initially(self) -> None:
        """Test that Mecatol Rex system starts with no space units."""
        system = SystemFactory.create_mecatol_rex_system()

        assert len(system.space_units) == 0

    def test_mecatol_rex_system_has_no_wormholes_initially(self) -> None:
        """Test that Mecatol Rex system starts with no wormholes."""
        system = SystemFactory.create_mecatol_rex_system()

        assert len(system.wormholes) == 0

    def test_mecatol_rex_system_has_no_command_tokens_initially(self) -> None:
        """Test that Mecatol Rex system starts with no command tokens."""
        system = SystemFactory.create_mecatol_rex_system()

        assert len(system.command_tokens) == 0
        assert system.get_players_with_command_tokens() == []

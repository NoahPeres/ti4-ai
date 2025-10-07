"""Integration tests for Mecatol Rex system with game mechanics."""

from ti4.core.galaxy import Galaxy
from ti4.core.game_state import GameState
from ti4.core.hex_coordinate import HexCoordinate
from ti4.core.strategy_cards.cards.diplomacy import DiplomacyStrategyCard
from ti4.core.system_factory import SystemFactory


class TestMecatolRexIntegration:
    """Test Mecatol Rex system integration with game mechanics."""

    def test_diplomacy_primary_ability_rejects_mecatol_rex_system(self) -> None:
        """Test that diplomacy primary ability rejects Mecatol Rex system.

        LRR Reference: Rule 32.2 - Cannot select Mecatol Rex system
        """
        # Create game state with Mecatol Rex system
        game_state = GameState()
        mecatol_system = SystemFactory.create_mecatol_rex_system()
        game_state.systems["18"] = mecatol_system

        # Create diplomacy card
        card = DiplomacyStrategyCard()

        # Attempt to use primary ability on Mecatol Rex
        result = card.execute_primary_ability("player1", game_state, system_id="18")

        # Should be rejected
        assert not result.success
        assert (
            "Cannot select Mecatol Rex system for Diplomacy primary ability"
            in result.error_message
        )

    def test_diplomacy_primary_ability_rejects_mecatol_rex_planet(self) -> None:
        """Test that diplomacy primary ability rejects Mecatol Rex planet.

        LRR Reference: Rule 32.1 - Cannot target Mecatol Rex
        """
        # Create game state with Mecatol Rex system
        game_state = GameState()
        mecatol_system = SystemFactory.create_mecatol_rex_system()
        game_state.systems["18"] = mecatol_system

        # Get the Mecatol Rex planet
        mecatol_planet = mecatol_system.planets[0]

        # Create diplomacy card
        card = DiplomacyStrategyCard()

        # Attempt to use primary ability on Mecatol Rex planet
        result = card.execute_primary_ability(
            "player1", game_state, system_id="18", target_planet=mecatol_planet
        )

        # Should be rejected
        assert not result.success
        assert (
            "Cannot select Mecatol Rex system for Diplomacy primary ability"
            in result.error_message
        )

    def test_mecatol_rex_system_can_be_placed_in_galaxy(self) -> None:
        """Test that Mecatol Rex system can be placed in galaxy."""
        galaxy = Galaxy()
        mecatol_system = SystemFactory.create_mecatol_rex_system()

        # Place at galactic center (0, 0)
        center_coord = HexCoordinate(0, 0)
        galaxy.place_system(center_coord, "18")
        galaxy.register_system(mecatol_system)

        # Verify placement
        placed_system_id = galaxy.system_coordinates.get("18")
        assert placed_system_id is not None

        # Verify system can be retrieved
        retrieved_system = galaxy.get_system("18")
        assert retrieved_system is not None
        assert retrieved_system.system_id == "18"
        assert len(retrieved_system.planets) == 1
        assert retrieved_system.planets[0].name == "Mecatol Rex"

    def test_mecatol_rex_planet_properties_match_specification(self) -> None:
        """Test that Mecatol Rex planet matches game specification."""
        system = SystemFactory.create_mecatol_rex_system()
        mecatol_rex = system.planets[0]

        # Verify exact specification
        assert mecatol_rex.name == "Mecatol Rex"
        assert mecatol_rex.resources == 1
        assert mecatol_rex.influence == 6

        # Set control to test spending capabilities
        mecatol_rex.set_control("player1")

        # Verify it can be used for resource/influence spending
        assert mecatol_rex.can_spend_resources()
        assert mecatol_rex.can_spend_influence()

        # Verify it can hold units
        assert mecatol_rex.can_hold_ground_forces()
        assert mecatol_rex.can_hold_structures()

    def test_mecatol_rex_system_id_is_correct(self) -> None:
        """Test that Mecatol Rex system has correct system ID."""
        system = SystemFactory.create_mecatol_rex_system()

        # System ID should be "18" as per TI4 rules
        assert system.system_id == "18"

    def test_multiple_mecatol_rex_systems_are_identical(self) -> None:
        """Test that multiple Mecatol Rex systems created are identical."""
        system1 = SystemFactory.create_mecatol_rex_system()
        system2 = SystemFactory.create_mecatol_rex_system()

        # Should have identical properties
        assert system1.system_id == system2.system_id
        assert len(system1.planets) == len(system2.planets)

        planet1 = system1.planets[0]
        planet2 = system2.planets[0]

        assert planet1.name == planet2.name
        assert planet1.resources == planet2.resources
        assert planet1.influence == planet2.influence

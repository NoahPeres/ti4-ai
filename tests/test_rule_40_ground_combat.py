"""Tests for Rule 40: Ground Combat."""

from ti4.core.combat import CombatResolver
from ti4.core.ground_combat import GroundCombatController
from ti4.core.planet import Planet
from ti4.core.system import System
from ti4.core.unit import Unit, UnitType


class TestRule40GroundCombat:
    """Test cases for ground combat mechanics."""

    def test_ground_combat_controller_exists(self):
        """Test that GroundCombatController can be instantiated."""
        combat_resolver = CombatResolver()
        controller = GroundCombatController(combat_resolver)
        assert controller is not None
        assert hasattr(controller, "resolve_combat_round")
        assert hasattr(controller, "resolve_ground_combat")

    def test_ground_combat_controller_resolves_single_round(self):
        """Test that ground combat controller can resolve a single round."""
        # Setup
        combat_resolver = CombatResolver()
        controller = GroundCombatController(combat_resolver)

        # Create a planet with ground forces
        planet = Planet("Test Planet", resources=2, influence=1)
        system = System("Test System")
        system.add_planet(planet)

        # Add attacking infantry
        attacker_infantry = Unit(unit_type=UnitType.INFANTRY, owner="attacker")
        planet.place_unit(attacker_infantry)

        # Add defending infantry
        defender_infantry = Unit(unit_type=UnitType.INFANTRY, owner="defender")
        planet.place_unit(defender_infantry)

        # Resolve single round
        result = controller.resolve_combat_round(
            system, "Test Planet", "attacker", "defender"
        )

        # Verify result structure
        assert hasattr(result, "attacker_hits")
        assert hasattr(result, "defender_hits")
        assert hasattr(result, "combat_continues")
        assert isinstance(result.attacker_hits, int)
        assert isinstance(result.defender_hits, int)
        assert isinstance(result.combat_continues, bool)

    def test_ground_combat_ends_when_one_side_eliminated(self):
        """Test that ground combat ends when one side has no units."""
        # Setup
        combat_resolver = CombatResolver()
        controller = GroundCombatController(combat_resolver)

        # Create a planet with uneven forces (attacker advantage)
        planet = Planet("Test Planet", resources=2, influence=1)
        system = System("Test System")
        system.add_planet(planet)

        # Single attacking infantry
        attacker_infantry = Unit(unit_type=UnitType.INFANTRY, owner="attacker")
        planet.place_unit(attacker_infantry)

        # Multiple defending infantry
        for _i in range(3):
            defender_infantry = Unit(unit_type=UnitType.INFANTRY, owner="defender")
            planet.place_unit(defender_infantry)

        # Resolve complete combat
        result = controller.resolve_ground_combat(
            system, "Test Planet", "attacker", "defender"
        )

        # Verify combat completed
        assert hasattr(result, "winner")
        assert hasattr(result, "rounds_fought")
        assert hasattr(result, "round_results")
        assert result.rounds_fought > 0
        assert len(result.round_results) == result.rounds_fought

        # Verify final state - one side should be eliminated
        final_attackers = controller._get_ground_forces(
            system, "Test Planet", "attacker"
        )
        final_defenders = controller._get_ground_forces(
            system, "Test Planet", "defender"
        )

        # At least one side should be eliminated
        assert len(final_attackers) == 0 or len(final_defenders) == 0

        # Winner should be determined correctly
        if len(final_attackers) > 0:
            assert result.winner == "attacker"
        elif len(final_defenders) > 0:
            assert result.winner == "defender"
        else:
            assert result.winner is None  # Both sides eliminated

    def test_ground_combat_multi_round_resolution(self):
        """Test that ground combat can resolve multiple rounds."""
        # Setup
        combat_resolver = CombatResolver()
        controller = GroundCombatController(combat_resolver)

        # Create a planet with equal forces for potential multi-round combat
        planet = Planet("Test Planet", resources=2, influence=1)
        system = System("Test System")
        system.add_planet(planet)

        # Two attacking infantry
        for _i in range(2):
            attacker_infantry = Unit(unit_type=UnitType.INFANTRY, owner="attacker")
            planet.place_unit(attacker_infantry)

        # Two defending infantry
        for _i in range(2):
            defender_infantry = Unit(unit_type=UnitType.INFANTRY, owner="defender")
            planet.place_unit(defender_infantry)

        # Resolve complete combat
        result = controller.resolve_ground_combat(
            system, "Test Planet", "attacker", "defender"
        )

        # Verify combat structure
        assert result.rounds_fought >= 1
        assert len(result.round_results) == result.rounds_fought

        # Verify each round result has proper structure
        for round_result in result.round_results:
            assert hasattr(round_result, "attacker_hits")
            assert hasattr(round_result, "defender_hits")
            assert hasattr(round_result, "combat_continues")

        # With equal forces, combat could go multiple rounds
        assert hasattr(result, "round_results")
        assert len(result.round_results) == result.rounds_fought

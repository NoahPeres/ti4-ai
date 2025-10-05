"""
Integration tests for nebula combat effects with existing combat systems.

LRR References:
- Rule 59: Nebula - covers combat bonuses for defenders in nebula systems
- Rule 78: Space Combat - integration with nebula effects
- Rule 40: Ground Combat - integration with nebula effects
"""

from src.ti4.core.combat import CombatResolver
from src.ti4.core.constants import AnomalyType, UnitType
from src.ti4.core.ground_combat import GroundCombatController
from src.ti4.core.planet import Planet
from src.ti4.core.space_combat import SpaceCombat
from src.ti4.core.system import System
from src.ti4.core.unit import Unit


class TestNebulaCombatIntegration:
    """Test nebula combat effects integration with existing combat systems."""

    def test_space_combat_with_nebula_defender_bonus(self) -> None:
        """Test that space combat can use nebula defender bonus."""
        # Create nebula system with space units
        nebula_system = System("nebula_system")
        nebula_system.add_anomaly_type(AnomalyType.NEBULA)

        # Add attacking and defending units
        attacker_unit = Unit(unit_type=UnitType.CRUISER, owner="attacker")
        defender_unit = Unit(unit_type=UnitType.CRUISER, owner="defender")

        nebula_system.place_unit_in_space(attacker_unit)
        nebula_system.place_unit_in_space(defender_unit)

        # Create combat resolver
        combat_resolver = CombatResolver()

        # Test that nebula provides defender bonus
        defender_bonus = combat_resolver.get_nebula_defender_bonus(nebula_system)
        assert defender_bonus == 1

        # Test that bonus applies to space combat
        applies_to_space = combat_resolver.nebula_bonus_applies_to_space_combat(
            nebula_system
        )
        assert applies_to_space is True

        # Test hit calculation with nebula bonus
        dice_results = [6, 7, 8]  # Would miss with combat value 7, hit with +1 bonus
        combat_value = 7
        hits_with_bonus = combat_resolver.calculate_hits_with_modifiers(
            dice_results, combat_value, defender_bonus
        )
        hits_without_bonus = combat_resolver.calculate_hits(dice_results, combat_value)

        assert hits_with_bonus > hits_without_bonus

    def test_ground_combat_with_nebula_defender_bonus(self) -> None:
        """Test that ground combat can use nebula defender bonus."""
        # Create nebula system with planet and ground forces
        nebula_system = System("nebula_system")
        nebula_system.add_anomaly_type(AnomalyType.NEBULA)

        planet = Planet("Test Planet", resources=2, influence=1)
        nebula_system.add_planet(planet)

        # Add attacking and defending ground forces
        attacker_unit = Unit(unit_type=UnitType.INFANTRY, owner="attacker")
        defender_unit = Unit(unit_type=UnitType.INFANTRY, owner="defender")

        nebula_system.place_unit_on_planet(attacker_unit, "Test Planet")
        nebula_system.place_unit_on_planet(defender_unit, "Test Planet")

        # Create combat resolver
        combat_resolver = CombatResolver()

        # Test that nebula provides defender bonus
        defender_bonus = combat_resolver.get_nebula_defender_bonus(nebula_system)
        assert defender_bonus == 1

        # Test that bonus applies to ground combat
        applies_to_ground = combat_resolver.nebula_bonus_applies_to_ground_combat(
            nebula_system
        )
        assert applies_to_ground is True

        # Test hit calculation with nebula bonus
        dice_results = [7, 8, 9]  # Would miss with combat value 8, hit with +1 bonus
        combat_value = 8
        hits_with_bonus = combat_resolver.calculate_hits_with_modifiers(
            dice_results, combat_value, defender_bonus
        )
        hits_without_bonus = combat_resolver.calculate_hits(dice_results, combat_value)

        assert hits_with_bonus > hits_without_bonus

    def test_space_combat_class_integration(self) -> None:
        """Test that SpaceCombat class can work with nebula systems."""
        # Create nebula system with space units
        nebula_system = System("nebula_system")
        nebula_system.add_anomaly_type(AnomalyType.NEBULA)

        # Add units for combat
        attacker_unit = Unit(unit_type=UnitType.CRUISER, owner="attacker")
        defender_unit = Unit(unit_type=UnitType.DESTROYER, owner="defender")

        nebula_system.place_unit_in_space(attacker_unit)
        nebula_system.place_unit_in_space(defender_unit)

        # Create space combat instance
        space_combat = SpaceCombat(nebula_system, "attacker", "defender")

        # Test that combat can be initiated
        assert space_combat.is_combat_required()

        # Start combat and verify system integration
        combat_round = space_combat.start_combat()
        assert combat_round.system == nebula_system
        assert len(combat_round.attacker_units) == 1
        assert len(combat_round.defender_units) == 1

        # Test that nebula effects can be queried during combat
        combat_resolver = CombatResolver()
        defender_bonus = combat_resolver.get_nebula_defender_bonus(nebula_system)
        assert defender_bonus == 1

    def test_ground_combat_controller_integration(self) -> None:
        """Test that GroundCombatController can work with nebula systems."""
        # Create nebula system with planet and ground forces
        nebula_system = System("nebula_system")
        nebula_system.add_anomaly_type(AnomalyType.NEBULA)

        planet = Planet("Test Planet", resources=2, influence=1)
        nebula_system.add_planet(planet)

        # Add ground forces for combat
        attacker_unit = Unit(unit_type=UnitType.INFANTRY, owner="attacker")
        defender_unit = Unit(unit_type=UnitType.INFANTRY, owner="defender")

        nebula_system.place_unit_on_planet(attacker_unit, "Test Planet")
        nebula_system.place_unit_on_planet(defender_unit, "Test Planet")

        # Create ground combat controller
        combat_resolver = CombatResolver()
        ground_combat = GroundCombatController(combat_resolver)

        # Test that ground forces are present
        attacker_forces = ground_combat._get_ground_forces(
            nebula_system, "Test Planet", "attacker"
        )
        defender_forces = ground_combat._get_ground_forces(
            nebula_system, "Test Planet", "defender"
        )

        assert len(attacker_forces) == 1
        assert len(defender_forces) == 1

        # Test that nebula effects can be queried during ground combat
        defender_bonus = combat_resolver.get_nebula_defender_bonus(nebula_system)
        assert defender_bonus == 1

    def test_multiple_anomaly_types_combat_integration(self) -> None:
        """Test combat integration with systems having multiple anomaly types."""
        # Create system with both nebula and gravity rift
        multi_anomaly_system = System("multi_anomaly_system")
        multi_anomaly_system.add_anomaly_type(AnomalyType.NEBULA)
        multi_anomaly_system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        # Add units for combat
        attacker_unit = Unit(unit_type=UnitType.FIGHTER, owner="attacker")
        defender_unit = Unit(unit_type=UnitType.FIGHTER, owner="defender")

        multi_anomaly_system.place_unit_in_space(attacker_unit)
        multi_anomaly_system.place_unit_in_space(defender_unit)

        # Create combat resolver
        combat_resolver = CombatResolver()

        # Test that nebula bonus still applies with multiple anomaly types
        defender_bonus = combat_resolver.get_nebula_defender_bonus(multi_anomaly_system)
        assert defender_bonus == 1

        # Test that both space and ground combat bonuses apply
        applies_to_space = combat_resolver.nebula_bonus_applies_to_space_combat(
            multi_anomaly_system
        )
        applies_to_ground = combat_resolver.nebula_bonus_applies_to_ground_combat(
            multi_anomaly_system
        )

        assert applies_to_space is True
        assert applies_to_ground is True

    def test_combat_modifier_stacking_with_nebula(self) -> None:
        """Test that nebula bonuses can stack with other combat modifiers."""
        # Create nebula system
        nebula_system = System("nebula_system")
        nebula_system.add_anomaly_type(AnomalyType.NEBULA)

        # Create combat resolver
        combat_resolver = CombatResolver()

        # Test nebula bonus
        nebula_bonus = combat_resolver.get_nebula_defender_bonus(nebula_system)
        assert nebula_bonus == 1

        # Test that nebula bonus can be combined with other modifiers
        dice_results = [5, 6, 7]  # Combat value 7
        combat_value = 7
        additional_modifier = 1  # From some other source (e.g., technology)

        # Total modifier should be nebula bonus + additional modifier
        total_modifier = nebula_bonus + additional_modifier

        hits_with_stacked_modifiers = combat_resolver.calculate_hits_with_modifiers(
            dice_results, combat_value, total_modifier
        )
        hits_with_nebula_only = combat_resolver.calculate_hits_with_modifiers(
            dice_results, combat_value, nebula_bonus
        )
        hits_without_modifiers = combat_resolver.calculate_hits(
            dice_results, combat_value
        )

        # Stacked modifiers should provide more hits than nebula alone
        assert (
            hits_with_stacked_modifiers
            >= hits_with_nebula_only
            >= hits_without_modifiers
        )

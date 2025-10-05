"""
Tests for nebula combat effects implementation.

LRR References:
- Rule 59: Nebula - covers combat bonuses for defenders in nebula systems
- Requirements 5.1, 5.2, 5.3, 5.4 from Rule 9 anomalies specification
"""

import pytest

from src.ti4.core.constants import AnomalyType, UnitType
from src.ti4.core.system import System
from src.ti4.core.unit import Unit


class TestNebulaCombatEffects:
    """Test nebula combat effects integration."""

    def test_nebula_provides_defender_combat_bonus(self) -> None:
        """Test that nebula systems provide +1 combat bonus to defenders (Requirement 5.1)."""
        # RED: Write a failing test for nebula combat bonus
        from src.ti4.core.combat import CombatResolver

        # Create nebula system
        nebula_system = System("nebula_system")
        nebula_system.add_anomaly_type(AnomalyType.NEBULA)

        # Create combat resolver
        combat_resolver = CombatResolver()

        # Test that nebula provides +1 combat bonus to defenders
        defender_bonus = combat_resolver.get_nebula_defender_bonus(nebula_system)
        assert defender_bonus == 1

    def test_non_nebula_system_provides_no_combat_bonus(self) -> None:
        """Test that non-nebula systems provide no combat bonus."""
        # RED: Write a failing test for non-nebula systems
        from src.ti4.core.combat import CombatResolver

        # Create normal system
        normal_system = System("normal_system")

        # Create combat resolver
        combat_resolver = CombatResolver()

        # Test that normal system provides no combat bonus
        defender_bonus = combat_resolver.get_nebula_defender_bonus(normal_system)
        assert defender_bonus == 0

    def test_nebula_combat_bonus_applies_to_space_combat(self) -> None:
        """Test that nebula combat bonus applies to space combat (Requirement 5.2)."""
        # RED: Write a failing test for space combat integration
        from src.ti4.core.combat import CombatResolver

        # Create nebula system with defending units
        nebula_system = System("nebula_system")
        nebula_system.add_anomaly_type(AnomalyType.NEBULA)

        defender_unit = Unit(unit_type=UnitType.CRUISER, owner="defender")
        nebula_system.place_unit_in_space(defender_unit)

        # Create combat resolver
        combat_resolver = CombatResolver()

        # Test that space combat gets nebula bonus
        applies_to_space = combat_resolver.nebula_bonus_applies_to_space_combat(
            nebula_system
        )
        assert applies_to_space is True

    def test_nebula_combat_bonus_applies_to_ground_combat(self) -> None:
        """Test that nebula combat bonus applies to ground combat (Requirement 5.3)."""
        # RED: Write a failing test for ground combat integration
        from src.ti4.core.combat import CombatResolver
        from src.ti4.core.planet import Planet

        # Create nebula system with planet and defending ground forces
        nebula_system = System("nebula_system")
        nebula_system.add_anomaly_type(AnomalyType.NEBULA)

        planet = Planet("Test Planet", resources=2, influence=1)
        nebula_system.add_planet(planet)

        defender_unit = Unit(unit_type=UnitType.INFANTRY, owner="defender")
        nebula_system.place_unit_on_planet(defender_unit, "Test Planet")

        # Create combat resolver
        combat_resolver = CombatResolver()

        # Test that ground combat gets nebula bonus
        applies_to_ground = combat_resolver.nebula_bonus_applies_to_ground_combat(
            nebula_system
        )
        assert applies_to_ground is True

    def test_nebula_bonus_applies_to_all_combat_rounds(self) -> None:
        """Test that nebula bonus applies to all combat rounds (Requirement 5.4)."""
        # RED: Write a failing test for multiple combat rounds
        from src.ti4.core.combat import CombatResolver

        # Create nebula system
        nebula_system = System("nebula_system")
        nebula_system.add_anomaly_type(AnomalyType.NEBULA)

        # Create combat resolver
        combat_resolver = CombatResolver()

        # Test that bonus applies consistently across rounds
        for round_number in range(1, 4):  # Test multiple rounds
            defender_bonus = combat_resolver.get_nebula_defender_bonus(nebula_system)
            assert defender_bonus == 1, (
                f"Nebula bonus should apply in round {round_number}"
            )

    def test_calculate_hits_with_nebula_bonus(self) -> None:
        """Test calculating hits with nebula defender bonus applied."""
        # RED: Write a failing test for hit calculation with nebula bonus
        from src.ti4.core.combat import CombatResolver

        combat_resolver = CombatResolver()

        # Test dice results that would normally miss but hit with +1 bonus
        dice_results = [
            6,
            7,
            8,
        ]  # Combat value 7 normally misses on 6, hits with +1 bonus
        combat_value = 7
        nebula_bonus = 1

        hits = combat_resolver.calculate_hits_with_modifiers(
            dice_results, combat_value, nebula_bonus
        )
        assert hits == 3  # All dice should hit with +1 bonus

    def test_multiple_anomaly_types_with_nebula_still_provide_bonus(self) -> None:
        """Test that systems with multiple anomaly types including nebula still provide combat bonus."""
        # RED: Write a failing test for multiple anomaly types
        from src.ti4.core.combat import CombatResolver

        # Create system with both nebula and gravity rift
        multi_anomaly_system = System("multi_anomaly_system")
        multi_anomaly_system.add_anomaly_type(AnomalyType.NEBULA)
        multi_anomaly_system.add_anomaly_type(AnomalyType.GRAVITY_RIFT)

        # Create combat resolver
        combat_resolver = CombatResolver()

        # Test that nebula bonus still applies
        defender_bonus = combat_resolver.get_nebula_defender_bonus(multi_anomaly_system)
        assert defender_bonus == 1

    def test_none_system_raises_error(self) -> None:
        """Test that None system raises ValueError for all nebula methods."""
        from src.ti4.core.combat import CombatResolver

        combat_resolver = CombatResolver()

        # Test all nebula methods raise ValueError for None system
        with pytest.raises(ValueError, match="System cannot be None"):
            combat_resolver.get_nebula_defender_bonus(None)  # type: ignore

        with pytest.raises(ValueError, match="System cannot be None"):
            combat_resolver.nebula_bonus_applies_to_space_combat(None)  # type: ignore

        with pytest.raises(ValueError, match="System cannot be None"):
            combat_resolver.nebula_bonus_applies_to_ground_combat(None)  # type: ignore

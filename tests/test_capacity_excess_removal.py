"""Tests for Rule 16.3a - Player choice in excess unit removal."""

import pytest

from src.ti4.core.constants import UnitType
from src.ti4.core.fleet import Fleet
from src.ti4.core.unit import Unit


class TestCapacityExcessRemoval:
    """Test Rule 16.3a - Player choice when removing excess units due to capacity violations."""

    def test_player_choice_excess_fighter_removal(self) -> None:
        """Test that player can choose which excess fighters to remove.

        LRR Reference: Rule 16.3a - A player can choose which of their excess units to remove.
        """
        # Create fleet with carrier (capacity 4) and 6 fighters (2 excess)
        fleet = Fleet(owner="player1", system_id="system1")

        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")
        fleet.add_unit(carrier)

        # Add 6 fighters - 2 more than capacity
        fighters = []
        for i in range(6):
            fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")
            fighter.unit_id = f"fighter_{i}"  # Give unique IDs for choice testing
            fighters.append(fighter)
            fleet.add_unit(fighter)

        # Verify capacity is exceeded
        assert fleet.get_carried_units_count() == 6
        assert fleet.get_total_capacity() == 4

        # Player chooses to remove fighters 2 and 4 (specific choice)
        chosen_units_to_remove = [fighters[2], fighters[4]]

        # This should work - remove player's chosen excess units
        from src.ti4.core.fleet import FleetCapacityEnforcer

        enforcer = FleetCapacityEnforcer()

        removed_units = enforcer.remove_excess_units_with_choice(
            fleet, chosen_units_to_remove
        )

        # Verify correct units were removed
        assert len(removed_units) == 2
        assert fighters[2] in removed_units
        assert fighters[4] in removed_units

        # Verify fleet is now within capacity
        assert fleet.get_carried_units_count() == 4
        assert fleet.get_total_capacity() == 4

        # Verify specific fighters remain
        remaining_fighters = [
            unit for unit in fleet.units if unit.unit_type == UnitType.FIGHTER
        ]
        assert len(remaining_fighters) == 4
        assert fighters[2] not in fleet.units
        assert fighters[4] not in fleet.units
        assert fighters[0] in fleet.units
        assert fighters[1] in fleet.units
        assert fighters[3] in fleet.units
        assert fighters[5] in fleet.units

    def test_player_choice_mixed_excess_unit_removal(self) -> None:
        """Test player choice when removing mix of fighters and infantry.

        LRR Reference: Rule 16.3a - A player can choose which of their excess units to remove.
        """
        # Create fleet with carrier (capacity 4), 3 fighters, and 3 infantry (2 excess total)
        fleet = Fleet(owner="player1", system_id="system1")

        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")
        fleet.add_unit(carrier)

        # Add 3 fighters
        fighters = []
        for i in range(3):
            fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")
            fighter.unit_id = f"fighter_{i}"
            fighters.append(fighter)
            fleet.add_unit(fighter)

        # Add 3 infantry
        infantry_units = []
        for i in range(3):
            infantry = Unit(unit_type=UnitType.INFANTRY, owner="player1")
            infantry.unit_id = f"infantry_{i}"
            infantry_units.append(infantry)
            fleet.add_unit(infantry)

        # Verify capacity is exceeded (6 carried units, 4 capacity)
        assert fleet.get_carried_units_count() == 6
        assert fleet.get_total_capacity() == 4

        # Player chooses to remove 1 fighter and 1 infantry
        chosen_units_to_remove = [fighters[1], infantry_units[2]]

        from src.ti4.core.fleet import FleetCapacityEnforcer

        enforcer = FleetCapacityEnforcer()

        removed_units = enforcer.remove_excess_units_with_choice(
            fleet, chosen_units_to_remove
        )

        # Verify correct units were removed
        assert len(removed_units) == 2
        assert fighters[1] in removed_units
        assert infantry_units[2] in removed_units

        # Verify fleet is now within capacity
        assert fleet.get_carried_units_count() == 4
        assert fleet.get_total_capacity() == 4

    def test_insufficient_units_chosen_for_removal(self) -> None:
        """Test error when player doesn't choose enough units to remove.

        LRR Reference: Rule 16.3 - Player must remove excess units.
        """
        # Create fleet with capacity violation (6 units, 4 capacity)
        fleet = Fleet(owner="player1", system_id="system1")

        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")
        fleet.add_unit(carrier)

        fighters = []
        for _ in range(6):
            fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")
            fighters.append(fighter)
            fleet.add_unit(fighter)

        # Player only chooses to remove 1 unit (need to remove 2)
        chosen_units_to_remove = [fighters[0]]

        from src.ti4.core.exceptions import FleetCapacityError
        from src.ti4.core.fleet import FleetCapacityEnforcer

        enforcer = FleetCapacityEnforcer()

        with pytest.raises(
            FleetCapacityError, match="Insufficient units chosen for removal"
        ):
            enforcer.remove_excess_units_with_choice(fleet, chosen_units_to_remove)

    def test_invalid_unit_choice_for_removal(self) -> None:
        """Test error when player chooses units that don't count against capacity.

        LRR Reference: Rule 16.3a - Only excess fighters and ground forces can be removed.
        """
        # Create fleet with capacity violation
        fleet = Fleet(owner="player1", system_id="system1")

        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")
        cruiser = Unit(unit_type=UnitType.CRUISER, owner="player1")
        fleet.add_unit(carrier)
        fleet.add_unit(cruiser)

        fighters = []
        for _ in range(6):  # 2 excess
            fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")
            fighters.append(fighter)
            fleet.add_unit(fighter)

        # Player tries to remove cruiser instead of fighters
        chosen_units_to_remove = [cruiser, fighters[0]]

        from src.ti4.core.exceptions import FleetCapacityError
        from src.ti4.core.fleet import FleetCapacityEnforcer

        enforcer = FleetCapacityEnforcer()

        with pytest.raises(
            FleetCapacityError,
            match="Cannot remove unit that doesn't count against capacity",
        ):
            enforcer.remove_excess_units_with_choice(fleet, chosen_units_to_remove)

    def test_no_excess_units_no_removal_needed(self) -> None:
        """Test that no removal occurs when fleet is within capacity.

        LRR Reference: Rule 16.3 - Only remove units when capacity is exceeded.
        """
        # Create fleet within capacity
        fleet = Fleet(owner="player1", system_id="system1")

        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")
        fleet.add_unit(carrier)

        # Add only 3 fighters (within capacity of 4)
        fighters = []
        for _ in range(3):
            fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")
            fighters.append(fighter)
            fleet.add_unit(fighter)

        from src.ti4.core.fleet import FleetCapacityEnforcer

        enforcer = FleetCapacityEnforcer()

        # Should return empty list - no removal needed
        removed_units = enforcer.remove_excess_units_with_choice(fleet, [])

        assert len(removed_units) == 0
        assert fleet.get_carried_units_count() == 3
        assert len(fleet.units) == 4  # carrier + 3 fighters

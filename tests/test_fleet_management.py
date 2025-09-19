"""Tests for fleet composition and capacity management."""

from src.ti4.core.constants import Faction, Technology, UnitType
from src.ti4.core.fleet import Fleet, FleetCapacityValidator
from src.ti4.core.unit import Unit


class TestFleet:
    def test_fleet_creation(self) -> None:
        """Test that a fleet can be created."""
        fleet = Fleet(owner="player1", system_id="system1")
        assert fleet.owner == "player1"
        assert fleet.system_id == "system1"
        assert len(fleet.units) == 0

    def test_add_unit_to_fleet(self) -> None:
        """Test that a unit can be added to a fleet."""
        fleet = Fleet(owner="player1", system_id="system1")
        unit = Unit(unit_type=UnitType.CRUISER, owner="player1")
        fleet.add_unit(unit)
        assert len(fleet.units) == 1
        assert unit in fleet.units

    def test_fleet_capacity_calculation(self) -> None:
        """Test that fleet capacity is calculated correctly."""
        fleet = Fleet(owner="player1", system_id="system1")

        # Add a carrier with capacity 4
        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")  # Capacity 4
        fleet.add_unit(carrier)

        # Fleet capacity should be 4
        assert fleet.get_total_capacity() == 4

        # Add another carrier
        carrier2 = Unit(unit_type=UnitType.CARRIER, owner="player1")
        fleet.add_unit(carrier2)

        # Fleet capacity should be 8
        assert fleet.get_total_capacity() == 8


class TestFleetCapacityValidator:
    def test_fleet_capacity_validator_creation(self) -> None:
        """Test that FleetCapacityValidator can be created."""
        validator = FleetCapacityValidator()
        assert validator is not None

    def test_validate_fleet_within_capacity(self) -> None:
        """Test that a fleet within capacity is valid."""
        validator = FleetCapacityValidator()
        fleet = Fleet(owner="player1", system_id="system1")

        # Add a carrier with capacity 4
        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")
        fighter1 = Unit(unit_type=UnitType.FIGHTER, owner="player1")
        fighter2 = Unit(unit_type=UnitType.FIGHTER, owner="player1")
        fighter3 = Unit(unit_type=UnitType.FIGHTER, owner="player1")

        fleet.add_unit(carrier)
        fleet.add_unit(fighter1)
        fleet.add_unit(fighter2)
        fleet.add_unit(fighter3)

        # Should be valid (3 fighters in carrier with capacity 4)
        assert validator.is_fleet_capacity_valid(fleet) is True

    def test_validate_fleet_exceeds_capacity(self) -> None:
        """Test that a fleet exceeding capacity is invalid."""
        validator = FleetCapacityValidator()
        fleet = Fleet(owner="player1", system_id="system1")

        # Add a carrier with capacity 4
        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")
        fleet.add_unit(carrier)

        # Add 5 fighters (exceeds capacity)
        for _ in range(5):
            fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")
            fleet.add_unit(fighter)

        # Should be invalid (5 fighters in carrier with capacity 4)
        assert validator.is_fleet_capacity_valid(fleet) is False

    def test_validate_fleet_supply_limit(self) -> None:
        """Test that fleet supply limits are enforced."""
        validator = FleetCapacityValidator()

        # Create multiple fleets with non-fighter ships
        fleet1 = Fleet(owner="player1", system_id="system1")
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        fleet1.add_unit(cruiser1)

        fleet2 = Fleet(owner="player1", system_id="system2")
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        fleet2.add_unit(cruiser2)

        fleets = [fleet1, fleet2]

        # Should be invalid with only 1 fleet token (2 fleets with non-fighters)
        assert validator.is_fleet_supply_valid(fleets, 1) is False

    def test_validate_fleet_supply_within_limit(self) -> None:
        """Test that fleet within supply limit is valid."""
        validator = FleetCapacityValidator()

        # Create multiple fleets with non-fighter ships
        fleet1 = Fleet(owner="player1", system_id="system1")
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        fleet1.add_unit(cruiser1)

        fleet2 = Fleet(owner="player1", system_id="system2")
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner="player1")
        fleet2.add_unit(cruiser2)

        fleets = [fleet1, fleet2]

        # Should be valid with 2 fleet tokens (2 fleets with non-fighters)
        assert validator.is_fleet_supply_valid(fleets, 2) is True

    def test_fleet_capacity_with_upgraded_cruiser(self) -> None:
        """Test fleet capacity calculation with upgraded units."""
        fleet = Fleet(owner="player1", system_id="system1")

        # Add upgraded cruiser with capacity 1
        cruiser_ii = Unit(unit_type=UnitType.CRUISER_II, owner="player1")  # Capacity 1
        carrier = Unit(unit_type=UnitType.CARRIER, owner="player1")  # Capacity 4

        fleet.add_unit(cruiser_ii)
        fleet.add_unit(carrier)

        # Total capacity should be 5
        assert fleet.get_total_capacity() == 5

    def test_faction_specific_unit_stats(self) -> None:
        """Test that faction-specific modifications work."""
        from src.ti4.core.unit_stats import UnitStats, UnitStatsProvider

        # Create custom stats provider with faction modifier
        stats_provider = UnitStatsProvider()
        stats_provider.register_faction_modifier(
            Faction.SOL,
            UnitType.INFANTRY,
            UnitStats(combat_value=7),  # Sol infantry (Spec Ops) are better
        )

        # Create Sol infantry unit with custom stats provider
        sol_infantry = Unit(
            unit_type=UnitType.INFANTRY,
            owner="player1",
            faction=Faction.SOL,
            stats_provider=stats_provider,
        )

        # Create regular infantry unit
        regular_infantry = Unit(unit_type=UnitType.INFANTRY, owner="player2")

        # Sol infantry should have better combat value
        assert sol_infantry.get_stats().combat_value == 7
        assert (
            regular_infantry.get_stats().combat_value == 8
        )  # Default infantry combat value

    def test_technology_unit_upgrades(self) -> None:
        """Test that technology upgrades affect unit stats."""
        from src.ti4.core.unit_stats import UnitStats, UnitStatsProvider

        # Create stats provider with technology modifier
        stats_provider = UnitStatsProvider()
        stats_provider.register_technology_modifier(
            Technology.CRUISER_II,
            UnitType.CRUISER,
            UnitStats(capacity=1, combat_value=6),
        )

        # Create cruiser with technology
        upgraded_cruiser = Unit(
            unit_type=UnitType.CRUISER,
            owner="player1",
            technologies={Technology.CRUISER_II},
            stats_provider=stats_provider,
        )

        # Should have upgraded stats
        assert upgraded_cruiser.get_stats().capacity == 1
        assert upgraded_cruiser.get_stats().combat_value == 6

    def test_fighter_ii_requires_fleet_supply(self) -> None:
        """Test that Fighter II (with independent movement) requires fleet supply."""
        from src.ti4.core.unit_stats import UnitStats, UnitStatsProvider

        validator = FleetCapacityValidator()

        # Create stats provider with Fighter II technology
        stats_provider = UnitStatsProvider()
        stats_provider.register_technology_modifier(
            Technology.FIGHTER_II,
            UnitType.FIGHTER,
            UnitStats(movement=1),  # Fighter II has independent movement
        )

        # Player has 3 fleet tokens available
        player_fleet_tokens = 2

        # Create 3 fleets with Fighter II (should exceed fleet supply)
        fleets = []
        for i in range(3):
            fleet = Fleet(owner="player1", system_id=f"system{i + 1}")
            fighter_ii = Unit(
                unit_type=UnitType.FIGHTER,
                owner="player1",
                technologies={Technology.FIGHTER_II},
                stats_provider=stats_provider,
            )
            fleet.add_unit(fighter_ii)
            fleets.append(fleet)

        # Should be invalid (3 Fighter II fleets exceed 2 fleet tokens)
        assert validator.is_fleet_supply_valid(fleets, player_fleet_tokens) is False

    def test_base_fighters_cannot_exist_alone(self) -> None:
        """Test that base fighters cannot exist without fleet supply."""
        fleet = Fleet(owner="player1", system_id="system1")

        # Add only a fighter (no carrier or supply)
        fighter = Unit(unit_type=UnitType.FIGHTER, owner="player1")
        fleet.add_unit(fighter)

        validator = FleetCapacityValidator()
        assert validator.is_fleet_capacity_valid(fleet) is False

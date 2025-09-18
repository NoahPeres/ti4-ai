"""Tests for fleet composition and capacity management."""

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
        """Test adding units to a fleet."""
        fleet = Fleet(owner="player1", system_id="system1")
        unit = Unit(unit_type="cruiser", owner="player1")

        fleet.add_unit(unit)

        assert unit in fleet.units
        assert len(fleet.units) == 1

    def test_fleet_capacity_calculation(self) -> None:
        """Test that fleet calculates its capacity correctly."""
        fleet = Fleet(owner="player1", system_id="system1")

        # Add ships with different capacities
        cruiser = Unit(
            unit_type="cruiser", owner="player1"
        )  # Capacity 0 (base cruiser)
        carrier = Unit(unit_type="carrier", owner="player1")  # Capacity 4

        fleet.add_unit(cruiser)
        fleet.add_unit(carrier)

        # Total capacity should be 4 (0 + 4)
        assert fleet.get_total_capacity() == 4


class TestFleetCapacityValidator:
    def test_fleet_capacity_validator_creation(self) -> None:
        """Test that FleetCapacityValidator can be created."""
        validator = FleetCapacityValidator()
        assert validator is not None

    def test_validate_fleet_within_capacity(self) -> None:
        """Test that a fleet within capacity is valid."""
        validator = FleetCapacityValidator()
        fleet = Fleet(owner="player1", system_id="system1")

        # Add a carrier (capacity 4) and 3 fighters
        carrier = Unit(unit_type="carrier", owner="player1")
        fighter1 = Unit(unit_type="fighter", owner="player1")
        fighter2 = Unit(unit_type="fighter", owner="player1")
        fighter3 = Unit(unit_type="fighter", owner="player1")

        fleet.add_unit(carrier)
        fleet.add_unit(fighter1)
        fleet.add_unit(fighter2)
        fleet.add_unit(fighter3)

        # Should be valid (3 fighters fit in carrier capacity of 4)
        assert validator.is_fleet_capacity_valid(fleet) is True

    def test_validate_fleet_exceeds_capacity(self) -> None:
        """Test that a fleet exceeding capacity is invalid."""
        validator = FleetCapacityValidator()
        fleet = Fleet(owner="player1", system_id="system1")

        # Add a carrier (capacity 4) and 5 fighters
        carrier = Unit(unit_type="carrier", owner="player1")
        fleet.add_unit(carrier)

        for _ in range(5):  # Add 5 fighters
            fighter = Unit(unit_type="fighter", owner="player1")
            fleet.add_unit(fighter)

        # Should be invalid (5 fighters exceed carrier capacity of 4)
        assert validator.is_fleet_capacity_valid(fleet) is False

    def test_validate_fleet_supply_limit(self) -> None:
        """Test that fleet supply (fleet pool tokens) limits are enforced."""
        validator = FleetCapacityValidator()

        # Player has 3 fleet tokens available (starting fleet pool per TI4 rules 20.1)
        player_fleet_tokens = 3

        # Create 4 fleets with non-fighter ships (exceeds fleet token limit)
        fleets = []
        for i in range(4):
            fleet = Fleet(owner="player1", system_id=f"system{i + 1}")
            cruiser = Unit(unit_type="cruiser", owner="player1")  # Non-fighter ship
            fleet.add_unit(cruiser)
            fleets.append(fleet)

        # Should be invalid (4 fleets with ships exceed 3 fleet tokens)
        assert validator.is_fleet_supply_valid(fleets, player_fleet_tokens) is False

    def test_validate_fleet_supply_within_limit(self) -> None:
        """Test that fleet supply within limits is valid."""
        validator = FleetCapacityValidator()

        # Player has 3 fleet tokens available (starting fleet pool per TI4 rules 20.1)
        player_fleet_tokens = 3

        # Create 2 fleets with ships (within fleet token limit)
        fleets = []
        for i in range(2):
            fleet = Fleet(owner="player1", system_id=f"system{i + 1}")
            cruiser = Unit(unit_type="cruiser", owner="player1")  # Non-fighter ship
            fleet.add_unit(cruiser)
            fleets.append(fleet)

        # Should be valid (2 fleets with ships within 3 fleet tokens)
        assert validator.is_fleet_supply_valid(fleets, player_fleet_tokens) is True

    def test_fleet_capacity_with_upgraded_cruiser(self) -> None:
        """Test that upgraded cruiser II has capacity."""
        fleet = Fleet(owner="player1", system_id="system1")

        # Add upgraded cruiser with capacity
        cruiser_ii = Unit(unit_type="cruiser_ii", owner="player1")  # Capacity 1
        carrier = Unit(unit_type="carrier", owner="player1")  # Capacity 4

        fleet.add_unit(cruiser_ii)
        fleet.add_unit(carrier)

        # Total capacity should be 5 (1 + 4)
        assert fleet.get_total_capacity() == 5

    def test_faction_specific_unit_stats(self) -> None:
        """Test that faction-specific modifications work."""
        from src.ti4.core.unit_stats import UnitStats, UnitStatsProvider

        # Create custom stats provider with faction modifier
        stats_provider = UnitStatsProvider()
        stats_provider.register_faction_modifier(
            "sol",
            "infantry",
            UnitStats(combat_value=7),  # Sol infantry (Spec Ops) are better
        )

        # Create Sol infantry (Spec Ops)
        sol_infantry = Unit(
            unit_type="infantry",
            owner="player1",
            faction="sol",
            stats_provider=stats_provider,
        )

        # Should have modified combat value
        assert sol_infantry.get_combat_value() == 7

        # Regular infantry should have default stats
        regular_infantry = Unit(unit_type="infantry", owner="player2")
        assert regular_infantry.get_combat_value() == 8  # Default value

    def test_technology_unit_upgrades(self) -> None:
        """Test that technology upgrades affect unit stats."""
        from src.ti4.core.unit_stats import UnitStats, UnitStatsProvider

        # Create stats provider with technology modifier
        stats_provider = UnitStatsProvider()
        stats_provider.register_technology_modifier(
            "cruiser_ii", "cruiser", UnitStats(capacity=1, combat_value=6)
        )

        # Create cruiser with technology
        upgraded_cruiser = Unit(
            unit_type="cruiser",
            owner="player1",
            technologies={"cruiser_ii"},
            stats_provider=stats_provider,
        )

        # Should have upgraded stats
        assert upgraded_cruiser.get_capacity() == 1
        assert upgraded_cruiser.get_combat_value() == 6

    def test_fighter_ii_requires_fleet_supply(self) -> None:
        """Test that Fighter II (with independent movement) requires fleet supply."""
        from src.ti4.core.unit_stats import UnitStats, UnitStatsProvider

        validator = FleetCapacityValidator()

        # Create stats provider with Fighter II technology
        stats_provider = UnitStatsProvider()
        stats_provider.register_technology_modifier(
            "fighter_ii",
            "fighter",
            UnitStats(movement=1),  # Fighter II has independent movement
        )

        # Player has 3 fleet tokens available
        player_fleet_tokens = 2

        # Create 3 fleets with Fighter II (should exceed fleet supply)
        fleets = []
        for i in range(3):
            fleet = Fleet(owner="player1", system_id=f"system{i + 1}")
            fighter_ii = Unit(
                unit_type="fighter",
                owner="player1",
                technologies={"fighter_ii"},
                stats_provider=stats_provider,
            )
            fleet.add_unit(fighter_ii)
            fleets.append(fleet)

        # Should be invalid (3 Fighter II fleets exceed 2 fleet tokens)
        assert validator.is_fleet_supply_valid(fleets, player_fleet_tokens) is False

    def test_base_fighters_cannot_exist_alone(self) -> None:
        """Test that base fighters cannot exist without carrier capacity."""
        validator = FleetCapacityValidator()
        fleet = Fleet(owner="player1", system_id="system1")

        # Add only a base fighter (no carrier)
        fighter = Unit(unit_type="fighter", owner="player1")
        fleet.add_unit(fighter)

        # Should be invalid (fighter needs capacity but fleet has none)
        assert validator.is_fleet_capacity_valid(fleet) is False

    def test_fleet_requires_supply_method(self) -> None:
        """Test the requires_fleet_supply method."""
        # Fleet with cruiser requires supply
        fleet_with_ship = Fleet(owner="player1", system_id="system1")
        cruiser = Unit(unit_type="cruiser", owner="player1")
        fleet_with_ship.add_unit(cruiser)
        assert fleet_with_ship.requires_fleet_supply() is True

        # Fleet with only fighters doesn't require supply
        fleet_with_fighters = Fleet(owner="player1", system_id="system2")
        fighter = Unit(unit_type="fighter", owner="player1")
        fleet_with_fighters.add_unit(fighter)
        assert fleet_with_fighters.requires_fleet_supply() is False

        # Empty fleet doesn't require supply
        empty_fleet = Fleet(owner="player1", system_id="system3")
        assert empty_fleet.requires_fleet_supply() is False

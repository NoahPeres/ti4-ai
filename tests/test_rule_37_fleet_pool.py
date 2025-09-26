"""Tests for Rule 37: FLEET POOL mechanics.

This module tests the fleet pool system according to TI4 LRR Rule 37.
All tests follow strict TDD methodology with RED-GREEN-REFACTOR cycles.

Rule 37 Sub-rules tested:
- 37.0: Fleet pool definition - command sheet area for fleet tokens
- 37.1: Fleet pool ship limits - command tokens limit non-fighter ships per system
- 37.1a: Planet/capacity exclusions - planet units don't count against fleet pool
- 37.1b: Transport exclusions - transported units don't count in transit systems
- 37.2: Token orientation - fleet pool tokens placed with ship silhouette faceup
- 37.3: Excess ship removal - automatic removal when fleet pool exceeded
- 37.4: Spending restrictions - fleet pool tokens cannot be spent unless allowed
"""

from tests.test_constants import MockPlanet, MockPlayer, MockSystem
from ti4.core.constants import UnitType
from ti4.core.fleet_pool import FleetPoolManager
from ti4.core.galaxy import Galaxy
from ti4.core.hex_coordinate import HexCoordinate
from ti4.core.planet import Planet
from ti4.core.system import System
from ti4.core.unit import Unit


class TestRule37FleetPoolBasics:
    """Test basic fleet pool mechanics (Rule 37.0)."""

    def test_fleet_pool_system_exists(self) -> None:
        """Test that fleet pool system can be imported and instantiated.

        This is the first RED test - it will fail until we create the system.

        LRR Reference: Rule 37.0 - Core fleet pool concept
        """
        # This will fail initially - RED phase
        manager = FleetPoolManager()
        assert manager is not None


class TestRule37FleetPoolLimits:
    """Test fleet pool ship limit mechanics (Rule 37.1)."""

    def test_fleet_pool_limits_non_fighter_ships(self) -> None:
        """Test that fleet pool tokens limit non-fighter ships per system.

        LRR Reference: Rule 37.1 - "command tokens in fleet pool indicates maximum number of non-fighter ships"
        """
        manager = FleetPoolManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Add 2 cruisers (non-fighter ships)
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner=MockPlayer.PLAYER_1.value)
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner=MockPlayer.PLAYER_1.value)
        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        # With 2 fleet pool tokens, should be valid
        is_valid_with_2_tokens = manager.is_fleet_pool_valid(
            system, MockPlayer.PLAYER_1.value, fleet_tokens=2
        )
        assert is_valid_with_2_tokens is True

        # With 1 fleet pool token, should be invalid (2 ships > 1 token)
        is_valid_with_1_token = manager.is_fleet_pool_valid(
            system, MockPlayer.PLAYER_1.value, fleet_tokens=1
        )
        assert is_valid_with_1_token is False

    def test_fighters_do_not_count_against_fleet_pool(self) -> None:
        """Test that fighters do not count against fleet pool limits.

        LRR Reference: Rule 37.1 - Only non-fighter ships count against fleet pool
        """
        manager = FleetPoolManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Add 1 cruiser and 5 fighters
        cruiser = Unit(unit_type=UnitType.CRUISER, owner=MockPlayer.PLAYER_1.value)
        system.place_unit_in_space(cruiser)

        for _ in range(5):
            fighter = Unit(unit_type=UnitType.FIGHTER, owner=MockPlayer.PLAYER_1.value)
            system.place_unit_in_space(fighter)

        # With 1 fleet pool token, should be valid (only cruiser counts)
        is_valid = manager.is_fleet_pool_valid(
            system, MockPlayer.PLAYER_1.value, fleet_tokens=1
        )
        assert is_valid is True

    def test_mixed_ships_fleet_pool_counting(self) -> None:
        """Test fleet pool counting with mixed ship types.

        LRR Reference: Rule 37.1 - Non-fighter ships count against fleet pool
        """
        manager = FleetPoolManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Add various ship types
        cruiser = Unit(unit_type=UnitType.CRUISER, owner=MockPlayer.PLAYER_1.value)
        destroyer = Unit(unit_type=UnitType.DESTROYER, owner=MockPlayer.PLAYER_1.value)
        carrier = Unit(unit_type=UnitType.CARRIER, owner=MockPlayer.PLAYER_1.value)
        fighter = Unit(unit_type=UnitType.FIGHTER, owner=MockPlayer.PLAYER_1.value)

        system.place_unit_in_space(cruiser)
        system.place_unit_in_space(destroyer)
        system.place_unit_in_space(carrier)
        system.place_unit_in_space(fighter)

        # 3 non-fighter ships (cruiser, destroyer, carrier) + 1 fighter
        # Should need 3 fleet pool tokens
        is_valid_with_3_tokens = manager.is_fleet_pool_valid(
            system, MockPlayer.PLAYER_1.value, fleet_tokens=3
        )
        assert is_valid_with_3_tokens is True

        is_valid_with_2_tokens = manager.is_fleet_pool_valid(
            system, MockPlayer.PLAYER_1.value, fleet_tokens=2
        )
        assert is_valid_with_2_tokens is False


class TestRule37PlanetExclusions:
    """Test planet and capacity unit exclusion mechanics (Rule 37.1a)."""

    def test_planet_units_do_not_count_against_fleet_pool(self) -> None:
        """Test that units on planets do not count against fleet pool.

        LRR Reference: Rule 37.1a - "Units that are on planets... do not count against fleet pool"
        """
        manager = FleetPoolManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Add planet with units
        planet = Planet(MockPlanet.PLANET_A.value, resources=2, influence=1)
        system.add_planet(planet)

        # Add space dock and infantry on planet (should not count)
        space_dock = Unit(
            unit_type=UnitType.SPACE_DOCK, owner=MockPlayer.PLAYER_1.value
        )
        infantry = Unit(unit_type=UnitType.INFANTRY, owner=MockPlayer.PLAYER_1.value)
        planet.place_unit(space_dock)
        planet.place_unit(infantry)

        # Add cruiser in space (should count)
        cruiser = Unit(unit_type=UnitType.CRUISER, owner=MockPlayer.PLAYER_1.value)
        system.place_unit_in_space(cruiser)

        # Should only need 1 fleet pool token (only cruiser counts)
        is_valid = manager.is_fleet_pool_valid(
            system, MockPlayer.PLAYER_1.value, fleet_tokens=1
        )
        assert is_valid is True

    def test_capacity_consuming_units_do_not_count_against_fleet_pool(self) -> None:
        """Test that units counting against capacity do not count against fleet pool.

        LRR Reference: Rule 37.1a - "Units that... count against a player's capacity do not count against fleet pool"
        """
        manager = FleetPoolManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Add carrier (provides capacity, counts against fleet pool)
        carrier = Unit(unit_type=UnitType.CARRIER, owner=MockPlayer.PLAYER_1.value)
        system.place_unit_in_space(carrier)

        # Add fighters and infantry (consume capacity, should not count against fleet pool)
        fighter = Unit(unit_type=UnitType.FIGHTER, owner=MockPlayer.PLAYER_1.value)
        infantry = Unit(unit_type=UnitType.INFANTRY, owner=MockPlayer.PLAYER_1.value)
        system.place_unit_in_space(fighter)
        system.place_unit_in_space(infantry)

        # Should only need 1 fleet pool token (only carrier counts)
        is_valid = manager.is_fleet_pool_valid(
            system, MockPlayer.PLAYER_1.value, fleet_tokens=1
        )
        assert is_valid is True


class TestRule37TransportExclusions:
    """Test transport exclusion mechanics (Rule 37.1b)."""

    def test_transported_units_do_not_count_in_transit_systems(self) -> None:
        """Test that transported units don't count against fleet pool in transit systems.

        LRR Reference: Rule 37.1b - "Units being transported through systems do not count against fleet pool in those systems"
        """
        manager = FleetPoolManager()

        # Create galaxy and systems
        galaxy = Galaxy()
        system1 = System(MockSystem.TEST_SYSTEM.value)
        system2 = System(MockSystem.SYSTEM_2.value)

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)

        galaxy.place_system(coord1, MockSystem.TEST_SYSTEM.value)
        galaxy.place_system(coord2, MockSystem.SYSTEM_2.value)
        galaxy.register_system(system1)
        galaxy.register_system(system2)

        # Add carrier in system1 (origin)
        carrier = Unit(unit_type=UnitType.CARRIER, owner=MockPlayer.PLAYER_1.value)
        system1.place_unit_in_space(carrier)

        # Add infantry being transported through system2 (should not count in system2)
        infantry = Unit(unit_type=UnitType.INFANTRY, owner=MockPlayer.PLAYER_1.value)

        # Mark infantry as being transported through system2
        is_valid_in_transit = manager.is_fleet_pool_valid_with_transport(
            system2,
            MockPlayer.PLAYER_1.value,
            fleet_tokens=0,
            transported_units=[infantry],
        )
        assert is_valid_in_transit is True


class TestRule37TokenOrientation:
    """Test token placement orientation mechanics (Rule 37.2)."""

    def test_fleet_pool_tokens_placed_with_ship_silhouette_faceup(self) -> None:
        """Test that fleet pool tokens are placed with ship silhouette faceup.

        LRR Reference: Rule 37.2 - "Players place command tokens in fleet pools with ship silhouette faceup"
        """
        manager = FleetPoolManager()

        # Create fleet pool with tokens
        fleet_pool_tokens = manager.create_fleet_pool_tokens(count=3)

        # All tokens should have ship silhouette faceup
        for token in fleet_pool_tokens:
            assert token.is_ship_silhouette_faceup() is True
            assert token.is_in_fleet_pool() is True

    def test_fleet_pool_token_orientation_validation(self) -> None:
        """Test validation of fleet pool token orientation.

        LRR Reference: Rule 37.2 - Token orientation requirements
        """
        manager = FleetPoolManager()

        # Create properly oriented token
        proper_token = manager.create_fleet_pool_token(ship_silhouette_faceup=True)
        assert manager.is_fleet_pool_token_valid(proper_token) is True

        # Create improperly oriented token
        improper_token = manager.create_fleet_pool_token(ship_silhouette_faceup=False)
        assert manager.is_fleet_pool_token_valid(improper_token) is False


class TestRule37ExcessShipRemoval:
    """Test excess ship removal mechanics (Rule 37.3)."""

    def test_excess_ships_removed_when_fleet_pool_exceeded(self) -> None:
        """Test that excess ships are removed when fleet pool is exceeded.

        LRR Reference: Rule 37.3 - "player choose and remove excess ships, returning to reinforcements"
        """
        manager = FleetPoolManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Add 3 cruisers (exceeds 2 token limit)
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner=MockPlayer.PLAYER_1.value)
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner=MockPlayer.PLAYER_1.value)
        cruiser3 = Unit(unit_type=UnitType.CRUISER, owner=MockPlayer.PLAYER_1.value)

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)
        system.place_unit_in_space(cruiser3)

        # Enforce fleet pool limit of 2 tokens
        removed_ships = manager.enforce_fleet_pool_limit(
            system, MockPlayer.PLAYER_1.value, fleet_tokens=2
        )

        # Should remove 1 ship (3 ships - 2 tokens = 1 excess)
        assert len(removed_ships) == 1
        assert removed_ships[0] in [cruiser1, cruiser2, cruiser3]

        # System should now have only 2 ships
        remaining_ships = [
            unit
            for unit in system.space_units
            if unit.owner == MockPlayer.PLAYER_1.value
        ]
        assert len(remaining_ships) == 2

    def test_player_chooses_which_excess_ships_to_remove(self) -> None:
        """Test that player can choose which excess ships to remove.

        LRR Reference: Rule 37.3 - "they choose and remove excess ships"
        """
        manager = FleetPoolManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Add 3 different ships
        cruiser = Unit(unit_type=UnitType.CRUISER, owner=MockPlayer.PLAYER_1.value)
        destroyer = Unit(unit_type=UnitType.DESTROYER, owner=MockPlayer.PLAYER_1.value)
        carrier = Unit(unit_type=UnitType.CARRIER, owner=MockPlayer.PLAYER_1.value)

        system.place_unit_in_space(cruiser)
        system.place_unit_in_space(destroyer)
        system.place_unit_in_space(carrier)

        # Player chooses to remove the destroyer
        removed_ships = manager.enforce_fleet_pool_limit_with_choice(
            system,
            MockPlayer.PLAYER_1.value,
            fleet_tokens=2,
            ships_to_remove=[destroyer],
        )

        assert len(removed_ships) == 1
        assert removed_ships[0] == destroyer

        # System should have cruiser and carrier remaining
        remaining_ships = [
            unit
            for unit in system.space_units
            if unit.owner == MockPlayer.PLAYER_1.value
        ]
        assert len(remaining_ships) == 2
        assert cruiser in remaining_ships
        assert carrier in remaining_ships

    def test_removed_ships_returned_to_reinforcements(self) -> None:
        """Test that removed ships are returned to reinforcements.

        LRR Reference: Rule 37.3 - "returning those units to their reinforcements"
        """
        manager = FleetPoolManager()

        # Create galaxy and system
        galaxy = Galaxy()
        system = System(MockSystem.TEST_SYSTEM.value)
        coord = HexCoordinate(0, 0)

        galaxy.place_system(coord, MockSystem.TEST_SYSTEM.value)
        galaxy.register_system(system)

        # Add 2 cruisers (exceeds 1 token limit)
        cruiser1 = Unit(unit_type=UnitType.CRUISER, owner=MockPlayer.PLAYER_1.value)
        cruiser2 = Unit(unit_type=UnitType.CRUISER, owner=MockPlayer.PLAYER_1.value)

        system.place_unit_in_space(cruiser1)
        system.place_unit_in_space(cruiser2)

        # Track reinforcements before
        reinforcements_before = {UnitType.CRUISER: 0}

        # Enforce fleet pool limit
        reinforcements_after = (
            manager.enforce_fleet_pool_limit_and_return_to_reinforcements(
                system,
                MockPlayer.PLAYER_1.value,
                fleet_tokens=1,
                reinforcements=reinforcements_before,
            )
        )

        # Should have 1 cruiser returned to reinforcements
        assert reinforcements_after[UnitType.CRUISER] == 1


class TestRule37SpendingRestrictions:
    """Test fleet pool token spending restriction mechanics (Rule 37.4)."""

    def test_fleet_pool_tokens_cannot_be_spent_normally(self) -> None:
        """Test that fleet pool tokens cannot be spent unless game effect allows.

        LRR Reference: Rule 37.4 - "Players do not spend command tokens from this pool unless a game effect specifically allows it"
        """
        manager = FleetPoolManager()

        # Create fleet pool with tokens
        fleet_pool = manager.create_fleet_pool(tokens=3)

        # Should not be able to spend tokens normally
        can_spend_normally = manager.can_spend_fleet_pool_token(
            fleet_pool, game_effect=None
        )
        assert can_spend_normally is False

        # Should not be able to spend for tactical actions
        can_spend_for_tactical = manager.can_spend_fleet_pool_token_for_tactical_action(
            fleet_pool
        )
        assert can_spend_for_tactical is False

    def test_fleet_pool_tokens_can_be_spent_with_game_effect(self) -> None:
        """Test that fleet pool tokens can be spent when game effect allows.

        LRR Reference: Rule 37.4 - "unless a game effect specifically allows it"
        """
        manager = FleetPoolManager()

        # Create fleet pool with tokens
        fleet_pool = manager.create_fleet_pool(tokens=3)

        # Mock game effect that allows spending
        game_effect = "Warfare Strategy Card Secondary"

        # Should be able to spend with valid game effect
        can_spend_with_effect = manager.can_spend_fleet_pool_token(
            fleet_pool, game_effect=game_effect
        )
        assert can_spend_with_effect is True

    def test_fleet_pool_token_spending_validation(self) -> None:
        """Test validation of fleet pool token spending attempts.

        LRR Reference: Rule 37.4 - Spending restriction enforcement
        """
        manager = FleetPoolManager()

        # Create fleet pool with tokens
        fleet_pool = manager.create_fleet_pool(tokens=2)

        # Attempt to spend without game effect (should fail)
        spend_result = manager.attempt_spend_fleet_pool_token(
            fleet_pool, game_effect=None
        )
        assert spend_result.success is False
        assert "game effect" in spend_result.error_message.lower()

        # Fleet pool should still have 2 tokens
        assert fleet_pool.token_count == 2


class TestRule37FleetPoolIntegration:
    """Test fleet pool integration with existing systems."""

    def test_fleet_pool_integrates_with_existing_fleet_system(self) -> None:
        """Test that fleet pool integrates with existing Fleet class.

        This ensures fleet pool works with existing fleet mechanics.
        """
        from ti4.core.fleet import Fleet, FleetCapacityValidator

        fleet_validator = FleetCapacityValidator()

        # Create fleet with ships
        fleet = Fleet(
            owner=MockPlayer.PLAYER_1.value, system_id=MockSystem.TEST_SYSTEM.value
        )

        cruiser = Unit(unit_type=UnitType.CRUISER, owner=MockPlayer.PLAYER_1.value)
        destroyer = Unit(unit_type=UnitType.DESTROYER, owner=MockPlayer.PLAYER_1.value)
        fleet.add_unit(cruiser)
        fleet.add_unit(destroyer)

        # Fleet should require 2 fleet supply tokens
        ships_requiring_supply = fleet.get_ships_requiring_fleet_supply()
        assert len(ships_requiring_supply) == 2

        # Fleet pool validation should work with existing fleet system
        # The existing system counts fleets, not individual ships
        is_valid = fleet_validator.is_fleet_supply_valid([fleet], fleet_tokens=1)
        assert is_valid is True

        # Create a second fleet to test the limit
        fleet2 = Fleet(
            owner=MockPlayer.PLAYER_1.value, system_id=MockSystem.SYSTEM_2.value
        )
        fleet2.add_unit(
            Unit(unit_type=UnitType.CRUISER, owner=MockPlayer.PLAYER_1.value)
        )

        # With 2 fleets requiring supply and only 1 token, should be invalid
        is_invalid = fleet_validator.is_fleet_supply_valid(
            [fleet, fleet2], fleet_tokens=1
        )
        assert is_invalid is False

    def test_fleet_pool_integrates_with_command_sheet_system(self) -> None:
        """Test that fleet pool integrates with command sheet mechanics.

        This ensures fleet pool tokens are properly managed on command sheet.
        """
        manager = FleetPoolManager()

        # Create command sheet with fleet pool
        command_sheet = manager.create_command_sheet_with_fleet_pool(
            strategy_tokens=2, tactic_tokens=3, fleet_tokens=4
        )

        # Fleet pool should have 4 tokens (stored as integer in real CommandSheet)
        assert command_sheet.fleet_pool == 4

        # Should be able to validate fleet pool state
        is_valid_state = manager.is_command_sheet_fleet_pool_valid(command_sheet)
        assert is_valid_state is True

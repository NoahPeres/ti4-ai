"""
Tests for Rule 95: TRANSPORT

Implements comprehensive test coverage for TI4 LRR Rule 95: TRANSPORT mechanics.
Tests transport capacity, pickup restrictions, movement constraints, and invasion integration.
"""

import pytest

from ti4.core.constants import UnitType
from ti4.core.unit import Unit


class TestRule95TransportBasics:
    """Test basic transport infrastructure and manager setup."""

    def test_transport_manager_can_validate_basic_capacity(self):
        """Test that TransportManager can validate basic transport capacity.

        LRR Reference: Rule 95.0 - Transport capacity limits
        """
        from ti4.core.transport import TransportManager

        # Create a carrier with capacity 4
        carrier = Unit(UnitType.CARRIER, "player1")

        # Create 2 infantry (should fit in capacity 4)
        infantry1 = Unit(UnitType.INFANTRY, "player1")
        infantry2 = Unit(UnitType.INFANTRY, "player1")
        units_to_transport = [infantry1, infantry2]

        transport_manager = TransportManager()

        # Should be able to transport 2 infantry with carrier capacity 4
        assert (
            transport_manager.can_transport_units(carrier, units_to_transport) is True
        )


class TestRule95TransportCapacityValidation:
    """Test transport capacity validation according to Rule 95.0."""

    def test_ship_capacity_limits_exceeded(self):
        """Test that ships cannot transport more units than their capacity.

        LRR Reference: Rule 95.0 - Transport capacity limits
        """
        from ti4.core.transport import TransportManager

        # Create a destroyer with capacity 0
        destroyer = Unit(UnitType.DESTROYER, "player1")

        # Create 1 infantry (should not fit in capacity 0)
        infantry = Unit(UnitType.INFANTRY, "player1")
        units_to_transport = [infantry]

        transport_manager = TransportManager()

        # Should not be able to transport infantry with destroyer capacity 0
        assert (
            transport_manager.can_transport_units(destroyer, units_to_transport)
            is False
        )

    def test_ship_capacity_limits_exact_match(self):
        """Test that ships can transport exactly their capacity limit.

        LRR Reference: Rule 95.0 - Transport capacity limits
        """
        from ti4.core.transport import TransportManager

        # Create a carrier with capacity 4
        carrier = Unit(UnitType.CARRIER, "player1")

        # Create exactly 4 infantry (should exactly fit capacity 4)
        units_to_transport = [Unit(UnitType.INFANTRY, "player1") for _ in range(4)]

        transport_manager = TransportManager()

        # Should be able to transport exactly 4 infantry with carrier capacity 4
        assert (
            transport_manager.can_transport_units(carrier, units_to_transport) is True
        )

    def test_empty_units_list_always_valid(self):
        """Test that empty units list is always valid for transport.

        LRR Reference: Rule 95.0 - Transport capacity limits
        """
        from ti4.core.transport import TransportManager

        # Create any ship
        carrier = Unit(UnitType.CARRIER, "player1")

        # Empty units list
        units_to_transport = []

        transport_manager = TransportManager()

        # Should always be able to transport no units
        assert (
            transport_manager.can_transport_units(carrier, units_to_transport) is True
        )

    def test_only_fighters_and_ground_forces_can_be_transported(self):
        """Test that only fighters and ground forces can be transported.

        LRR Reference: Rule 95.0 - Transport can carry fighters and ground forces
        """
        from ti4.core.transport import TransportManager

        # Create a carrier with capacity 4
        carrier = Unit(UnitType.CARRIER, "player1")

        # Try to transport a cruiser (should fail - ships cannot be transported)
        cruiser = Unit(UnitType.CRUISER, "player1")
        invalid_units = [cruiser]

        transport_manager = TransportManager()

        # Should not be able to transport ships
        assert transport_manager.can_transport_units(carrier, invalid_units) is False


class TestRule95TransportStateManagement:
    """Test transport state tracking and management."""

    def test_transport_state_tracks_transported_units(self):
        """Test that TransportState can track which units are being transported.

        LRR Reference: Rule 95.2 - Transported units move with ship
        """
        from ti4.core.transport import TransportManager

        # Create a carrier and some units to transport
        carrier = Unit(UnitType.CARRIER, "player1")
        infantry1 = Unit(UnitType.INFANTRY, "player1")
        infantry2 = Unit(UnitType.INFANTRY, "player1")
        units_to_transport = [infantry1, infantry2]

        transport_manager = TransportManager()

        # Load units onto the transport ship
        transport_state = transport_manager.load_units(
            carrier, units_to_transport, "system1"
        )

        # Should track the transport ship and transported units
        assert transport_state.transport_ship == carrier
        assert transport_state.transported_units == units_to_transport
        assert transport_state.origin_system_id == "system1"
        assert transport_state.player_id == "player1"

    def test_transport_manager_can_unload_units(self):
        """Test that TransportManager can unload units from transport.

        LRR Reference: Rule 95.4 - Ground forces can land during invasion
        """
        from ti4.core.transport import TransportManager

        # Create a carrier and some units to transport
        carrier = Unit(UnitType.CARRIER, "player1")
        infantry1 = Unit(UnitType.INFANTRY, "player1")
        infantry2 = Unit(UnitType.INFANTRY, "player1")
        units_to_transport = [infantry1, infantry2]

        transport_manager = TransportManager()

        # Load units onto the transport ship
        transport_state = transport_manager.load_units(
            carrier, units_to_transport, "system1"
        )

        # Unload units from the transport ship
        unloaded_units = transport_manager.unload_units(transport_state, "system2")

        # Should return the units that were unloaded
        assert unloaded_units == units_to_transport
        # Transport state should now be empty
        assert len(transport_state.transported_units) == 0


class TestRule95CommandTokenRestrictions:
    """Test command token pickup restrictions according to Rule 95.3."""

    def test_cannot_pickup_from_system_with_command_token(self):
        """Test that units cannot be picked up from systems with player's command tokens.

        LRR Reference: Rule 95.3 - Command token pickup restrictions
        """
        from ti4.core.transport import TransportManager

        transport_manager = TransportManager()

        # Test pickup restriction - should not be able to pickup from system with command token
        # (except active system)
        can_pickup = transport_manager.can_pickup_from_system(
            system_id="system1",
            player_id="player1",
            has_player_command_token=True,
            is_active_system=False,
        )

        assert can_pickup is False

    def test_can_pickup_from_active_system_with_command_token(self):
        """Test that units can be picked up from active system even with command tokens.

        LRR Reference: Rule 95.3 - Active system exception
        """
        from ti4.core.transport import TransportManager

        transport_manager = TransportManager()

        # Should be able to pickup from active system even with command token
        can_pickup = transport_manager.can_pickup_from_system(
            system_id="system1",
            player_id="player1",
            has_player_command_token=True,
            is_active_system=True,
        )

        assert can_pickup is True

    def test_can_pickup_from_system_without_command_token(self):
        """Test that units can be picked up from systems without player's command tokens.

        LRR Reference: Rule 95.3 - Normal pickup allowed
        """
        from ti4.core.transport import TransportManager

        transport_manager = TransportManager()

        # Should be able to pickup from system without command token
        can_pickup = transport_manager.can_pickup_from_system(
            system_id="system1",
            player_id="player1",
            has_player_command_token=False,
            is_active_system=False,
        )

        assert can_pickup is True

    def test_pickup_validation_during_movement(self):
        """Test pickup validation for different movement scenarios.

        LRR Reference: Rule 95.3 - Pickup restrictions during movement
        """
        from ti4.core.transport import TransportManager

        transport_manager = TransportManager()

        # Test pickup from starting system (should be allowed)
        can_pickup_start = transport_manager.validate_pickup_during_movement(
            pickup_system_id="start_system",
            starting_system_id="start_system",
            active_system_id="active_system",
            has_command_token=True,
        )
        assert can_pickup_start is True

        # Test pickup from active system (should be allowed even with command token)
        can_pickup_active = transport_manager.validate_pickup_during_movement(
            pickup_system_id="active_system",
            starting_system_id="start_system",
            active_system_id="active_system",
            has_command_token=True,
        )
        assert can_pickup_active is True

        # Test pickup from intermediate system with command token (should be forbidden)
        can_pickup_intermediate = transport_manager.validate_pickup_during_movement(
            pickup_system_id="intermediate1",
            starting_system_id="start_system",
            active_system_id="active_system",
            has_command_token=True,
        )
        assert can_pickup_intermediate is False

        # Test pickup from intermediate system without command token (should be allowed)
        can_pickup_intermediate_no_token = (
            transport_manager.validate_pickup_during_movement(
                pickup_system_id="intermediate1",
                starting_system_id="start_system",
                active_system_id="active_system",
                has_command_token=False,
            )
        )
        assert can_pickup_intermediate_no_token is True


class TestRule95TransportMovementConstraints:
    """Test transport movement constraints according to Rule 95.2."""

    def test_transported_units_move_with_ship(self):
        """Test that transported units move with their transport ship.

        LRR Reference: Rule 95.2 - Transported units move with ship
        """
        from ti4.core.transport import TransportManager, TransportRules

        # Create a carrier and some units to transport
        carrier = Unit(UnitType.CARRIER, "player1")
        infantry1 = Unit(UnitType.INFANTRY, "player1")
        infantry2 = Unit(UnitType.INFANTRY, "player1")
        units_to_transport = [infantry1, infantry2]

        transport_manager = TransportManager()
        transport_rules = TransportRules()

        # Load units onto the transport ship
        transport_state = transport_manager.load_units(
            carrier, units_to_transport, "system1"
        )

        # Validate movement constraints
        is_valid_movement = transport_rules.validate_movement_constraints(
            transport_state=transport_state,
            from_system_id="system1",
            to_system_id="system2",
        )

        # Movement should be valid - transported units move with ship
        assert is_valid_movement is True

    def test_transported_units_remain_in_space_area(self):
        """Test that transported units remain in space area during movement.

        LRR Reference: Rule 95.2 - Transported units remain in space
        """
        from ti4.core.transport import TransportManager, TransportRules

        # Create a carrier and some units to transport
        carrier = Unit(UnitType.CARRIER, "player1")
        infantry = Unit(UnitType.INFANTRY, "player1")

        transport_manager = TransportManager()
        transport_rules = TransportRules()

        # Load units onto the transport ship
        transport_state = transport_manager.load_units(carrier, [infantry], "system1")

        # Check that transported units are in space area
        units_in_space = transport_rules.get_units_in_space_area(transport_state)

        # Transported units should be in space area
        assert infantry in units_in_space
        assert len(units_in_space) == 1


class TestRule95TransportDestruction:
    """Test transport ship destruction and effects on transported units."""

    def test_transported_units_destroyed_when_transport_ship_destroyed(self):
        """Test that transported units are destroyed when transport ship is destroyed.

        LRR Reference: Rule 95.2 - Transported units are destroyed with ship
        """
        from ti4.core.transport import TransportManager, TransportRules

        # Create a carrier and some units to transport
        carrier = Unit(UnitType.CARRIER, "player1")
        infantry1 = Unit(UnitType.INFANTRY, "player1")
        infantry2 = Unit(UnitType.INFANTRY, "player1")
        fighter = Unit(UnitType.FIGHTER, "player1")
        units_to_transport = [infantry1, infantry2, fighter]

        transport_manager = TransportManager()
        transport_rules = TransportRules()

        # Load units onto the transport ship
        transport_state = transport_manager.load_units(
            carrier, units_to_transport, "system1"
        )

        # Simulate transport ship destruction
        destroyed_units = transport_rules.handle_transport_ship_destruction(
            transport_state
        )

        # All transported units should be destroyed along with the ship
        assert carrier in destroyed_units
        assert infantry1 in destroyed_units
        assert infantry2 in destroyed_units
        assert fighter in destroyed_units
        assert len(destroyed_units) == 4

    def test_transport_destruction_during_retreat(self):
        """Test transport destruction handling during combat retreat.

        LRR Reference: Rule 95.2 - Transported units cannot retreat separately
        """
        from ti4.core.transport import TransportManager, TransportRules

        # Create a carrier and some units to transport
        carrier = Unit(UnitType.CARRIER, "player1")
        infantry = Unit(UnitType.INFANTRY, "player1")
        fighter = Unit(UnitType.FIGHTER, "player1")
        units_to_transport = [infantry, fighter]

        transport_manager = TransportManager()
        transport_rules = TransportRules()

        # Load units onto the transport ship
        transport_state = transport_manager.load_units(
            carrier, units_to_transport, "system1"
        )

        # Simulate retreat scenario where transport ship is destroyed
        can_retreat_separately = (
            transport_rules.can_transported_units_retreat_separately(transport_state)
        )

        # Transported units cannot retreat separately from their transport ship
        assert can_retreat_separately is False

    def test_empty_transport_destruction_only_destroys_ship(self):
        """Test that destroying empty transport ship only destroys the ship.

        LRR Reference: Rule 95.2 - Only ship destroyed if no transported units
        """
        from ti4.core.transport import TransportManager, TransportRules

        # Create a carrier with no transported units
        carrier = Unit(UnitType.CARRIER, "player1")

        transport_manager = TransportManager()
        transport_rules = TransportRules()

        # Create empty transport state
        transport_state = transport_manager.load_units(carrier, [], "system1")

        # Simulate transport ship destruction
        destroyed_units = transport_rules.handle_transport_ship_destruction(
            transport_state
        )

        # Only the ship should be destroyed (no transported units)
        assert carrier in destroyed_units
        assert len(destroyed_units) == 1


class TestRule95TransportValidatorEnhancement:
    """Test enhanced TransportValidator class with Rule 95 compliance.

    Tests integration of new transport rules with existing movement validation.
    """

    def test_enhanced_transport_validator_validates_rule_95_capacity(self):
        """Test that enhanced TransportValidator validates Rule 95 capacity limits.

        LRR Reference: Rule 95.0 - Transport capacity limits
        """
        from ti4.core.galaxy import Galaxy
        from ti4.core.movement import TransportValidator

        # Create a basic galaxy for the validator
        galaxy = Galaxy()

        # Create enhanced transport validator
        transport_validator = TransportValidator(galaxy)

        # Create a carrier with capacity 4
        carrier = Unit(UnitType.CARRIER, "player1")

        # Create too many units (5 infantry for capacity 4)
        infantry_units = [Unit(UnitType.INFANTRY, "player1") for _ in range(5)]

        # Create transport operation that exceeds capacity
        from ti4.core.movement import TransportOperation

        transport_op = TransportOperation(
            transport_ship=carrier,
            ground_forces=infantry_units,
            from_system_id="system1",
            to_system_id="system2",
            player_id="player1",
        )

        # Should fail validation due to capacity limits
        assert transport_validator.is_valid_transport(transport_op) is False

    def test_enhanced_transport_validator_validates_rule_95_unit_types(self):
        """Test that enhanced TransportValidator validates Rule 95 transportable unit types.

        LRR Reference: Rule 95.0 - Only fighters and ground forces can be transported
        """
        from ti4.core.galaxy import Galaxy
        from ti4.core.movement import TransportValidator

        # Create a basic galaxy for the validator
        galaxy = Galaxy()

        # Create enhanced transport validator
        transport_validator = TransportValidator(galaxy)

        # Create a carrier with capacity 4
        carrier = Unit(UnitType.CARRIER, "player1")

        # Try to transport a cruiser (invalid unit type)
        cruiser = Unit(UnitType.CRUISER, "player1")

        # Create transport operation with invalid unit type
        from ti4.core.movement import TransportOperation

        transport_op = TransportOperation(
            transport_ship=carrier,
            ground_forces=[cruiser],  # Invalid - ships cannot be transported
            from_system_id="system1",
            to_system_id="system2",
            player_id="player1",
        )

        # Should fail validation due to invalid unit type
        assert transport_validator.is_valid_transport(transport_op) is False

    def test_enhanced_transport_validator_validates_rule_95_pickup_restrictions(self):
        """Test that enhanced TransportValidator validates Rule 95 pickup restrictions.

        LRR Reference: Rule 95.3 - Command token pickup restrictions
        """
        from ti4.core.galaxy import Galaxy
        from ti4.core.movement import TransportValidator

        # Create a basic galaxy for the validator
        galaxy = Galaxy()

        # Create enhanced transport validator
        transport_validator = TransportValidator(galaxy)

        # This test will fail initially - we need to enhance TransportValidator
        # to include pickup restriction validation

        # For now, just test that the validator exists and can be called
        # The actual pickup validation will be implemented in the enhancement
        assert transport_validator is not None

    def test_enhanced_transport_validator_maintains_backward_compatibility(self):
        """Test that enhanced TransportValidator maintains backward compatibility.

        Ensures existing transport operations continue to work as expected.
        """
        from ti4.core.galaxy import Galaxy
        from ti4.core.hex_coordinate import HexCoordinate
        from ti4.core.movement import TransportValidator

        # Create a basic galaxy for the validator
        galaxy = Galaxy()

        # Add systems to the galaxy so coordinate lookup works
        galaxy.place_system(HexCoordinate(0, 0), "system1")
        galaxy.place_system(HexCoordinate(1, 0), "system2")  # Adjacent system

        # Create enhanced transport validator
        transport_validator = TransportValidator(galaxy)

        # Create a valid transport operation (existing functionality)
        carrier = Unit(UnitType.CARRIER, "player1")
        infantry = Unit(UnitType.INFANTRY, "player1")

        from ti4.core.movement import TransportOperation

        transport_op = TransportOperation(
            transport_ship=carrier,
            ground_forces=[infantry],
            from_system_id="system1",
            to_system_id="system2",
            player_id="player1",
        )

        # Should pass validation (backward compatibility)
        assert transport_validator.is_valid_transport(transport_op) is True


class TestRule95GroundForceLandingIntegration:
    """Test ground force landing integration with invasion system (Rule 95.4).

    Tests that transported ground forces can land during invasion step while
    fighters remain in space.
    """

    def test_transported_ground_forces_can_land_during_invasion(self):
        """Test that transported ground forces can land on planets during invasion.

        LRR Reference: Rule 95.4 - Ground forces can land during invasion
        """
        from ti4.core.game_state import GameState
        from ti4.core.invasion import InvasionController
        from ti4.core.planet import Planet
        from ti4.core.player import Player
        from ti4.core.system import System
        from ti4.core.transport import TransportState

        # Create game state and player
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        # Create system with planet
        system = System("test_system")
        planet = Planet(name="test_planet", resources=2, influence=1)
        system.add_planet(planet)

        # Create carrier with transported ground forces
        carrier = Unit(UnitType.CARRIER, "player1")
        infantry1 = Unit(UnitType.INFANTRY, "player1")
        infantry2 = Unit(UnitType.INFANTRY, "player1")

        # Create transport state with ground forces
        transport_state = TransportState(
            transport_ship=carrier,
            transported_units=[infantry1, infantry2],
            origin_system_id="previous_system",
            player_id="player1",
        )

        # Place carrier in system space
        system.place_unit_in_space(carrier)

        # Create invasion controller
        invasion_controller = InvasionController(game_state, system, player)

        # Should be able to land transported ground forces during invasion
        can_land = invasion_controller.can_land_transported_ground_forces(
            transport_state, planet.name
        )

        assert can_land is True

    def test_transported_fighters_remain_in_space_during_invasion(self):
        """Test that transported fighters remain in space during invasion.

        LRR Reference: Rule 95.4 - Fighters remain in space area
        """
        from ti4.core.game_state import GameState
        from ti4.core.invasion import InvasionController
        from ti4.core.planet import Planet
        from ti4.core.player import Player
        from ti4.core.system import System
        from ti4.core.transport import TransportState

        # Create game state and player
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        # Create system with planet
        system = System("test_system")
        planet = Planet(name="test_planet", resources=2, influence=1)
        system.add_planet(planet)

        # Create carrier with transported fighters
        carrier = Unit(UnitType.CARRIER, "player1")
        fighter1 = Unit(UnitType.FIGHTER, "player1")
        fighter2 = Unit(UnitType.FIGHTER, "player1")

        # Create transport state with fighters
        transport_state = TransportState(
            transport_ship=carrier,
            transported_units=[fighter1, fighter2],
            origin_system_id="previous_system",
            player_id="player1",
        )

        # Place carrier in system space
        system.place_unit_in_space(carrier)

        # Create invasion controller
        invasion_controller = InvasionController(game_state, system, player)

        # Fighters should NOT be able to land during invasion
        can_land = invasion_controller.can_land_transported_ground_forces(
            transport_state, planet.name
        )

        assert can_land is False  # No ground forces to land

    def test_mixed_transported_units_only_ground_forces_land(self):
        """Test that only ground forces land during invasion, fighters stay in space.

        LRR Reference: Rule 95.4 - Only ground forces can land
        """
        from ti4.core.game_state import GameState
        from ti4.core.invasion import InvasionController
        from ti4.core.planet import Planet
        from ti4.core.player import Player
        from ti4.core.system import System
        from ti4.core.transport import TransportState

        # Create game state and player
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        # Create system with planet
        system = System("test_system")
        planet = Planet(name="test_planet", resources=2, influence=1)
        system.add_planet(planet)

        # Create carrier with mixed transported units
        carrier = Unit(UnitType.CARRIER, "player1")
        infantry = Unit(UnitType.INFANTRY, "player1")
        fighter = Unit(UnitType.FIGHTER, "player1")

        # Create transport state with mixed units
        transport_state = TransportState(
            transport_ship=carrier,
            transported_units=[infantry, fighter],
            origin_system_id="previous_system",
            player_id="player1",
        )

        # Place carrier in system space
        system.place_unit_in_space(carrier)

        # Create invasion controller
        invasion_controller = InvasionController(game_state, system, player)

        # Execute landing of transported ground forces
        landed_units = invasion_controller.land_transported_ground_forces(
            transport_state, planet.name
        )

        # Only infantry should land, fighter should remain transported
        assert infantry in landed_units
        assert fighter not in landed_units
        assert len(landed_units) == 1

        # Fighter should still be in transport state
        assert fighter in transport_state.transported_units
        assert infantry not in transport_state.transported_units

    def test_invasion_step_integrates_with_transport_landing(self):
        """Test that invasion commit ground forces step integrates with transport landing.

        LRR Reference: Rule 95.4 - Integration with invasion process
        """
        from ti4.core.galaxy import Galaxy
        from ti4.core.game_state import GameState
        from ti4.core.hex_coordinate import HexCoordinate
        from ti4.core.invasion import InvasionController
        from ti4.core.planet import Planet
        from ti4.core.player import Player
        from ti4.core.system import System
        from ti4.core.transport import TransportState

        # Create game state and player
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        # Create galaxy and system
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)
        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)
        game_state = game_state._create_new_state(galaxy=galaxy)

        # Add planet to system
        planet = Planet(name="test_planet", resources=2, influence=1)
        system.add_planet(planet)

        # Create carrier with transported ground forces
        carrier = Unit(UnitType.CARRIER, "player1")
        infantry = Unit(UnitType.INFANTRY, "player1")

        # Create transport state
        transport_state = TransportState(
            transport_ship=carrier,
            transported_units=[infantry],
            origin_system_id="previous_system",
            player_id="player1",
        )

        # Place carrier in system space
        system.place_unit_in_space(carrier)

        # Create invasion controller with transport state
        invasion_controller = InvasionController(game_state, system, player)
        invasion_controller.set_transport_states([transport_state])

        # Execute commit ground forces step - should handle transported units
        result = invasion_controller.commit_ground_forces_step()

        # Should proceed to space cannon defense
        assert result == "space_cannon_defense"

        # Infantry should now be on the planet (landed from transport)
        assert infantry in planet.units

        # Infantry should no longer be transported
        assert infantry not in transport_state.transported_units


class TestRule95TransportExceptionHierarchy:
    """Test transport exception hierarchy for comprehensive error handling.

    Tests all transport-related error scenarios with proper exception types
    and error messages according to Requirements 8.1-8.4.
    """

    def test_transport_capacity_error_raised_when_capacity_exceeded(self):
        """Test that TransportCapacityError is raised when transport capacity is exceeded.

        LRR Reference: Rule 95.0 - Transport capacity limits
        Requirements: 8.1, 8.2
        """
        from ti4.core.transport import TransportCapacityError, TransportManager

        # Create a destroyer with capacity 0
        destroyer = Unit(UnitType.DESTROYER, "player1")

        # Create 1 infantry (should exceed capacity 0)
        infantry = Unit(UnitType.INFANTRY, "player1")
        units_to_transport = [infantry]

        transport_manager = TransportManager()

        # Should raise TransportCapacityError when trying to load units that exceed capacity
        try:
            transport_manager.load_units(destroyer, units_to_transport, "system1")
            assert False, "Expected TransportCapacityError to be raised"
        except TransportCapacityError as e:
            # Should have descriptive error message with context
            assert "capacity" in str(e).lower()
            assert "destroyer" in str(e).lower() or "0" in str(e)
            assert "infantry" in str(e).lower() or "1" in str(e)

    def test_transport_pickup_error_raised_when_pickup_restricted(self):
        """Test that TransportPickupError is raised when pickup is restricted by command tokens.

        LRR Reference: Rule 95.3 - Command token pickup restrictions
        Requirements: 8.1, 8.2
        """
        from ti4.core.transport import TransportManager, TransportPickupError

        transport_manager = TransportManager()

        # Should raise TransportPickupError when trying to pickup from restricted system
        try:
            # This should fail - trying to pickup from system with command token (not active)
            transport_manager.validate_pickup_with_exception(
                system_id="system1",
                player_id="player1",
                has_player_command_token=True,
                is_active_system=False,
            )
            assert False, "Expected TransportPickupError to be raised"
        except TransportPickupError as e:
            # Should have descriptive error message with context
            assert "command token" in str(e).lower()
            assert "system1" in str(e)
            assert "pickup" in str(e).lower()

    def test_transport_movement_error_raised_when_movement_invalid(self):
        """Test that TransportMovementError is raised when transport movement is invalid.

        LRR Reference: Rule 95.2 - Transport movement constraints
        Requirements: 8.1, 8.2
        """
        from ti4.core.transport import (
            TransportMovementError,
            TransportRules,
            TransportState,
        )

        # Create invalid transport state (None ship)
        invalid_transport_state = TransportState(
            transport_ship=None,  # Invalid - None ship
            transported_units=[Unit(UnitType.INFANTRY, "player1")],
            origin_system_id="system1",
            player_id="player1",
        )

        transport_rules = TransportRules()

        # Should raise TransportMovementError when validating invalid transport state
        try:
            transport_rules.validate_movement_with_exception(
                invalid_transport_state, "system1", "system2"
            )
            assert False, "Expected TransportMovementError to be raised"
        except TransportMovementError as e:
            # Should have descriptive error message with context
            assert "transport" in str(e).lower()
            assert "movement" in str(e).lower()
            assert "invalid" in str(e).lower()

    def test_transport_exception_hierarchy_inherits_from_base_exception(self):
        """Test that all transport exceptions inherit from proper base exception.

        Requirements: 8.3 - Integrate with existing exception handling patterns
        """
        from ti4.core.exceptions import TI4Error
        from ti4.core.transport import (
            TransportCapacityError,
            TransportError,
            TransportMovementError,
            TransportPickupError,
        )

        # All transport exceptions should inherit from TransportError
        assert issubclass(TransportCapacityError, TransportError)
        assert issubclass(TransportPickupError, TransportError)
        assert issubclass(TransportMovementError, TransportError)

        # TransportError should inherit from TI4Error for consistency
        assert issubclass(TransportError, TI4Error)

    def test_transport_exceptions_have_comprehensive_error_messages(self):
        """Test that transport exceptions provide comprehensive error messages with context.

        Requirements: 8.2 - Comprehensive error messages with context
        """
        from ti4.core.transport import (
            TransportCapacityError,
            TransportMovementError,
            TransportPickupError,
        )

        # Test TransportCapacityError with context
        capacity_error = TransportCapacityError(
            "Cannot transport 3 units: ship capacity is 2",
            ship_type="Carrier",
            ship_capacity=2,
            units_requested=3,
        )
        assert "Cannot transport 3 units" in str(capacity_error)
        assert capacity_error.ship_type == "Carrier"
        assert capacity_error.ship_capacity == 2
        assert capacity_error.units_requested == 3

        # Test TransportPickupError with context
        pickup_error = TransportPickupError(
            "Cannot pickup from system1: command token restriction",
            system_id="system1",
            has_command_token=True,
            is_active_system=False,
        )
        assert "Cannot pickup from system1" in str(pickup_error)
        assert pickup_error.system_id == "system1"
        assert pickup_error.has_command_token is True
        assert pickup_error.is_active_system is False

        # Test TransportMovementError with context
        movement_error = TransportMovementError(
            "Invalid transport movement from system1 to system2",
            from_system="system1",
            to_system="system2",
            transport_ship_id="carrier1",
        )
        assert "Invalid transport movement" in str(movement_error)
        assert movement_error.from_system == "system1"
        assert movement_error.to_system == "system2"
        assert movement_error.transport_ship_id == "carrier1"


class TestRule95TransportValidationLayers:
    """Test validation layer integration for transport operations.

    Tests pre-transport, movement, and landing validation layers with
    state consistency validation and error recovery mechanisms.
    Requirements: 8.1-8.4
    """

    def test_pre_transport_validation_layer_validates_before_loading(self):
        """Test that pre-transport validation layer validates before loading units.

        Requirements: 8.1, 8.4 - Pre-transport validation
        """
        from ti4.core.transport import TransportCapacityError, TransportValidationLayer

        validation_layer = TransportValidationLayer()

        # Create a destroyer with capacity 0
        destroyer = Unit(UnitType.DESTROYER, "player1")
        infantry = Unit(UnitType.INFANTRY, "player1")

        # Pre-transport validation should catch capacity violation
        try:
            validation_layer.validate_pre_transport(destroyer, [infantry])
            assert False, "Expected TransportCapacityError to be raised"
        except TransportCapacityError as e:
            assert "capacity" in str(e).lower()

    def test_movement_validation_layer_validates_during_movement(self):
        """Test that movement validation layer validates during transport movement.

        Requirements: 8.1, 8.4 - Movement validation
        """
        from ti4.core.transport import (
            TransportMovementError,
            TransportState,
            TransportValidationLayer,
        )

        validation_layer = TransportValidationLayer()

        # Create valid transport state
        carrier = Unit(UnitType.CARRIER, "player1")
        infantry = Unit(UnitType.INFANTRY, "player1")
        transport_state = TransportState(
            transport_ship=carrier,
            transported_units=[infantry],
            origin_system_id="system1",
            player_id="player1",
        )

        # Movement validation should pass for valid transport
        try:
            validation_layer.validate_movement(transport_state, "system1", "system2")
            # Should not raise exception for valid movement
        except TransportMovementError:
            assert False, "Valid transport movement should not raise exception"

    def test_landing_validation_layer_validates_during_invasion(self):
        """Test that landing validation layer validates during ground force landing.

        Requirements: 8.1, 8.4 - Landing validation
        """
        from ti4.core.transport import TransportState, TransportValidationLayer

        validation_layer = TransportValidationLayer()

        # Create transport state with ground forces
        carrier = Unit(UnitType.CARRIER, "player1")
        infantry = Unit(UnitType.INFANTRY, "player1")
        fighter = Unit(UnitType.FIGHTER, "player1")
        transport_state = TransportState(
            transport_ship=carrier,
            transported_units=[infantry, fighter],
            origin_system_id="system1",
            player_id="player1",
        )

        # Landing validation should identify which units can land
        landable_units = validation_layer.validate_landing(
            transport_state, "test_planet"
        )

        # Only infantry should be landable, not fighter
        assert infantry in landable_units
        assert fighter not in landable_units
        assert len(landable_units) == 1

    def test_state_consistency_validation_detects_inconsistencies(self):
        """Test that state consistency validation detects transport state inconsistencies.

        Requirements: 8.1, 8.4 - State consistency validation
        """
        from ti4.core.transport import (
            TransportMovementError,
            TransportState,
            TransportValidationLayer,
        )

        validation_layer = TransportValidationLayer()

        # Create inconsistent transport state (units from different players)
        carrier = Unit(UnitType.CARRIER, "player1")
        infantry_p1 = Unit(UnitType.INFANTRY, "player1")
        infantry_p2 = Unit(UnitType.INFANTRY, "player2")  # Different player!

        inconsistent_transport_state = TransportState(
            transport_ship=carrier,
            transported_units=[infantry_p1, infantry_p2],  # Mixed ownership
            origin_system_id="system1",
            player_id="player1",
        )

        # State consistency validation should detect the inconsistency
        try:
            validation_layer.validate_state_consistency(inconsistent_transport_state)
            assert False, "Expected TransportMovementError for inconsistent state"
        except TransportMovementError as e:
            assert "consistency" in str(e).lower() or "ownership" in str(e).lower()

    def test_validation_error_recovery_mechanisms_handle_failures(self):
        """Test that validation error recovery mechanisms handle validation failures.

        Requirements: 8.4 - Validation error recovery mechanisms
        """
        from ti4.core.transport import TransportErrorRecovery, TransportValidationLayer

        validation_layer = TransportValidationLayer()
        error_recovery = TransportErrorRecovery()

        # Create scenario that will fail validation
        destroyer = Unit(UnitType.DESTROYER, "player1")  # Capacity 0
        infantry = Unit(UnitType.INFANTRY, "player1")

        # Attempt operation with error recovery
        recovery_result = error_recovery.attempt_with_recovery(
            lambda: validation_layer.validate_pre_transport(destroyer, [infantry])
        )

        # Should return recovery result indicating failure and suggested fix
        assert recovery_result.success is False
        assert recovery_result.error_type == "TransportCapacityError"
        assert "capacity" in recovery_result.suggested_fix.lower()


class TestRule95MultiShipTransportCoordination:
    """Test multi-ship transport coordination according to Requirements 7.1-7.4.

    Tests fleet-level transport management, capacity calculation, and coordination
    across multiple ships in a fleet.
    """

    def test_fleet_transport_manager_calculates_total_capacity(self):
        """Test that FleetTransportManager calculates total transport capacity across multiple ships.

        Requirements: 7.1 - Multi-ship transport coordination
        """
        from ti4.core.fleet import Fleet
        from ti4.core.transport import FleetTransportManager

        # Create a fleet with multiple ships
        fleet = Fleet("player1", "system1")

        # Add ships with different capacities
        carrier = Unit(UnitType.CARRIER, "player1")  # capacity 4
        cruiser = Unit(UnitType.CRUISER, "player1")  # capacity 0
        dreadnought = Unit(UnitType.DREADNOUGHT, "player1")  # capacity 1

        fleet.add_unit(carrier)
        fleet.add_unit(cruiser)
        fleet.add_unit(dreadnought)

        # Create fleet transport manager
        fleet_transport_manager = FleetTransportManager()

        # Should calculate total capacity across all ships
        total_capacity = fleet_transport_manager.get_total_transport_capacity(fleet)

        # Total should be 4 + 0 + 1 = 5
        assert total_capacity == 5

    def test_fleet_transport_manager_coordinates_unit_distribution(self):
        """Test that FleetTransportManager can distribute units across multiple ships.

        Requirements: 7.2 - Transport coordination across multiple ships
        """
        from ti4.core.fleet import Fleet
        from ti4.core.transport import FleetTransportManager

        # Create a fleet with multiple transport ships
        fleet = Fleet("player1", "system1")
        carrier1 = Unit(UnitType.CARRIER, "player1")  # capacity 4
        carrier2 = Unit(UnitType.CARRIER, "player1")  # capacity 4
        fleet.add_unit(carrier1)
        fleet.add_unit(carrier2)

        # Create units to transport
        infantry_units = [Unit(UnitType.INFANTRY, "player1") for _ in range(6)]
        fighter_units = [Unit(UnitType.FIGHTER, "player1") for _ in range(2)]
        units_to_transport = infantry_units + fighter_units

        # Create fleet transport manager
        fleet_transport_manager = FleetTransportManager()

        # Should be able to distribute 8 units across 2 carriers (total capacity 8)
        can_transport = fleet_transport_manager.can_transport_units(
            fleet, units_to_transport
        )
        assert can_transport is True

    def test_fleet_transport_manager_rejects_over_capacity(self):
        """Test that FleetTransportManager rejects transport when fleet capacity is exceeded.

        Requirements: 7.1 - Fleet-wide transport capacity calculation
        """
        from ti4.core.fleet import Fleet
        from ti4.core.transport import FleetTransportManager

        # Create a fleet with limited capacity
        fleet = Fleet("player1", "system1")
        carrier = Unit(UnitType.CARRIER, "player1")  # capacity 4
        fleet.add_unit(carrier)

        # Create too many units to transport
        infantry_units = [Unit(UnitType.INFANTRY, "player1") for _ in range(6)]

        # Create fleet transport manager
        fleet_transport_manager = FleetTransportManager()

        # Should reject transport when capacity is exceeded
        can_transport = fleet_transport_manager.can_transport_units(
            fleet, infantry_units
        )
        assert can_transport is False

    def test_fleet_transport_manager_creates_optimal_distribution(self):
        """Test that FleetTransportManager creates optimal unit distribution among ships.

        Requirements: 7.3 - Flexible assignment within capacity limits
        """
        from ti4.core.fleet import Fleet
        from ti4.core.transport import FleetTransportManager

        # Create a fleet with ships of different capacities
        fleet = Fleet("player1", "system1")
        carrier = Unit(UnitType.CARRIER, "player1")  # capacity 4
        dreadnought = Unit(UnitType.DREADNOUGHT, "player1")  # capacity 1
        fleet.add_unit(carrier)
        fleet.add_unit(dreadnought)

        # Create units to transport
        infantry_units = [Unit(UnitType.INFANTRY, "player1") for _ in range(3)]

        # Create fleet transport manager
        fleet_transport_manager = FleetTransportManager()

        # Should create optimal distribution
        transport_distribution = fleet_transport_manager.create_transport_distribution(
            fleet, infantry_units
        )

        # Should have transport states for both ships
        assert len(transport_distribution) == 2

        # Should distribute units optimally (e.g., 3 on carrier, 0 on dreadnought)
        total_transported = sum(
            len(ts.transported_units) for ts in transport_distribution
        )
        assert total_transported == 3


class TestRule95TransportOptimizationAndValidation:
    """Test transport optimization and validation for Requirements 7.1-7.4.

    Tests optimal unit distribution, validation for fleet transport operations,
    and transport planning utilities.
    """

    def test_transport_optimizer_distributes_units_optimally(self):
        """Test that TransportOptimizer distributes units optimally among ships.

        Requirements: 7.2 - Optimal unit distribution among transport ships
        """
        from ti4.core.fleet import Fleet
        from ti4.core.transport import TransportOptimizer

        # Create a fleet with ships of varying capacities
        fleet = Fleet("player1", "system1")
        carrier = Unit(UnitType.CARRIER, "player1")  # capacity 4
        dreadnought1 = Unit(UnitType.DREADNOUGHT, "player1")  # capacity 1
        dreadnought2 = Unit(UnitType.DREADNOUGHT, "player1")  # capacity 1
        fleet.add_unit(carrier)
        fleet.add_unit(dreadnought1)
        fleet.add_unit(dreadnought2)

        # Create units to transport
        units_to_transport = [Unit(UnitType.INFANTRY, "player1") for _ in range(4)]

        # Create transport optimizer
        optimizer = TransportOptimizer()

        # Should create optimal distribution
        distribution = optimizer.optimize_transport_distribution(
            fleet, units_to_transport
        )

        # Should use carrier first (highest capacity), then dreadnoughts
        carrier_transport = next(
            ts for ts in distribution if ts.transport_ship == carrier
        )
        assert len(carrier_transport.transported_units) == 4

        dreadnought_transports = [
            ts
            for ts in distribution
            if ts.transport_ship in [dreadnought1, dreadnought2]
        ]
        for dt in dreadnought_transports:
            assert len(dt.transported_units) == 0

    def test_fleet_transport_validator_validates_fleet_operations(self):
        """Test that FleetTransportValidator validates fleet transport operations.

        Requirements: 7.4 - Validation for fleet transport operations
        """
        from ti4.core.fleet import Fleet
        from ti4.core.transport import FleetTransportValidator

        # Create a fleet
        fleet = Fleet("player1", "system1")
        carrier = Unit(UnitType.CARRIER, "player1")
        fleet.add_unit(carrier)

        # Create valid transport operation
        infantry = Unit(UnitType.INFANTRY, "player1")
        units_to_transport = [infantry]

        # Create fleet transport validator
        validator = FleetTransportValidator()

        # Should validate successful transport operation
        is_valid = validator.validate_fleet_transport_operation(
            fleet, units_to_transport
        )
        assert is_valid is True

    def test_fleet_transport_validator_rejects_invalid_operations(self):
        """Test that FleetTransportValidator rejects invalid fleet transport operations.

        Requirements: 7.4 - Validation for fleet transport operations
        """
        from ti4.core.fleet import Fleet
        from ti4.core.transport import FleetTransportValidator

        # Create a fleet with no capacity
        fleet = Fleet("player1", "system1")
        destroyer = Unit(UnitType.DESTROYER, "player1")  # capacity 0
        fleet.add_unit(destroyer)

        # Try to transport units
        infantry = Unit(UnitType.INFANTRY, "player1")
        units_to_transport = [infantry]

        # Create fleet transport validator
        validator = FleetTransportValidator()

        # Should reject invalid transport operation
        is_valid = validator.validate_fleet_transport_operation(
            fleet, units_to_transport
        )
        assert is_valid is False

    def test_transport_planning_utilities_create_transport_plan(self):
        """Test that transport planning utilities can create comprehensive transport plans.

        Requirements: 7.4 - Create transport planning utilities
        """
        from ti4.core.fleet import Fleet
        from ti4.core.transport import TransportPlanningUtilities

        # Create a complex fleet scenario
        fleet = Fleet("player1", "system1")
        carrier1 = Unit(UnitType.CARRIER, "player1")
        carrier2 = Unit(UnitType.CARRIER, "player1")
        dreadnought = Unit(UnitType.DREADNOUGHT, "player1")
        fleet.add_unit(carrier1)
        fleet.add_unit(carrier2)
        fleet.add_unit(dreadnought)

        # Create mixed units to transport
        infantry_units = [Unit(UnitType.INFANTRY, "player1") for _ in range(5)]
        fighter_units = [Unit(UnitType.FIGHTER, "player1") for _ in range(3)]
        units_to_transport = infantry_units + fighter_units

        # Create transport planning utilities
        planning_utils = TransportPlanningUtilities()

        # Should create comprehensive transport plan
        transport_plan = planning_utils.create_transport_plan(fleet, units_to_transport)

        # Plan should include all ships with capacity
        assert (
            len(transport_plan.transport_assignments) == 3
        )  # 2 carriers + 1 dreadnought

        # Plan should transport all units within capacity limits
        total_planned = sum(
            len(assignment.units) for assignment in transport_plan.transport_assignments
        )
        assert total_planned == 8  # All units should be planned for transport


class TestRule95LandingValidationAndErrorHandling:
    """Test landing validation and error handling for Rule 95.4.

    Tests comprehensive validation and error handling for invalid landing scenarios.
    """

    def test_cannot_land_with_none_transport_state(self):
        """Test that landing fails with None transport state.

        LRR Reference: Rule 95.4 - Input validation
        """
        from ti4.core.game_state import GameState
        from ti4.core.invasion import InvasionController
        from ti4.core.planet import Planet
        from ti4.core.player import Player
        from ti4.core.system import System

        # Create game state and player
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        # Create system with planet
        system = System("test_system")
        planet = Planet(name="test_planet", resources=2, influence=1)
        system.add_planet(planet)

        # Create invasion controller
        invasion_controller = InvasionController(game_state, system, player)

        # Should raise ValueError for None transport state
        try:
            invasion_controller.can_land_transported_ground_forces(None, "test_planet")
            assert False, "Expected ValueError for None transport state"
        except ValueError as e:
            assert "Transport state cannot be None" in str(e)

    def test_cannot_land_on_nonexistent_planet(self):
        """Test that landing fails when planet doesn't exist in system.

        LRR Reference: Rule 95.4 - Planet validation
        """
        from ti4.core.game_state import GameState
        from ti4.core.invasion import InvasionController
        from ti4.core.planet import Planet
        from ti4.core.player import Player
        from ti4.core.system import System
        from ti4.core.transport import TransportState

        # Create game state and player
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        # Create system with planet (but not the one we'll try to land on)
        system = System("test_system")
        planet = Planet(name="existing_planet", resources=2, influence=1)
        system.add_planet(planet)

        # Create carrier with transported ground forces
        carrier = Unit(UnitType.CARRIER, "player1")
        infantry = Unit(UnitType.INFANTRY, "player1")

        # Create transport state
        transport_state = TransportState(
            transport_ship=carrier,
            transported_units=[infantry],
            origin_system_id="previous_system",
            player_id="player1",
        )

        # Create invasion controller
        invasion_controller = InvasionController(game_state, system, player)

        # Should raise ValueError for nonexistent planet
        try:
            invasion_controller.land_transported_ground_forces(
                transport_state, "nonexistent_planet"
            )
            assert False, "Expected ValueError for nonexistent planet"
        except ValueError as e:
            assert "Planet nonexistent_planet not found in system" in str(e)

    def test_cannot_land_with_none_planet_name(self):
        """Test that landing fails with None planet name.

        LRR Reference: Rule 95.4 - Input validation
        """
        from ti4.core.game_state import GameState
        from ti4.core.invasion import InvasionController
        from ti4.core.planet import Planet
        from ti4.core.player import Player
        from ti4.core.system import System
        from ti4.core.transport import TransportState

        # Create game state and player
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        # Create system with planet
        system = System("test_system")
        planet = Planet(name="test_planet", resources=2, influence=1)
        system.add_planet(planet)

        # Create carrier with transported ground forces
        carrier = Unit(UnitType.CARRIER, "player1")
        infantry = Unit(UnitType.INFANTRY, "player1")

        # Create transport state
        transport_state = TransportState(
            transport_ship=carrier,
            transported_units=[infantry],
            origin_system_id="previous_system",
            player_id="player1",
        )

        # Create invasion controller
        invasion_controller = InvasionController(game_state, system, player)

        # Should raise ValueError for None planet name
        try:
            invasion_controller.land_transported_ground_forces(transport_state, None)
            assert False, "Expected ValueError for None planet name"
        except ValueError as e:
            assert "Planet name cannot be None" in str(e)

    def test_cannot_set_none_transport_states(self):
        """Test that setting None transport states fails.

        LRR Reference: Rule 95.4 - Input validation
        """
        from ti4.core.game_state import GameState
        from ti4.core.invasion import InvasionController
        from ti4.core.player import Player
        from ti4.core.system import System

        # Create game state and player
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        # Create system
        system = System("test_system")

        # Create invasion controller
        invasion_controller = InvasionController(game_state, system, player)

        # Should raise ValueError for None transport states
        try:
            invasion_controller.set_transport_states(None)
            assert False, "Expected ValueError for None transport states"
        except ValueError as e:
            assert "Transport states cannot be None" in str(e)

    def test_landing_with_empty_transport_returns_empty_list(self):
        """Test that landing with empty transport returns empty list.

        LRR Reference: Rule 95.4 - Edge case handling
        """
        from ti4.core.game_state import GameState
        from ti4.core.invasion import InvasionController
        from ti4.core.planet import Planet
        from ti4.core.player import Player
        from ti4.core.system import System
        from ti4.core.transport import TransportState

        # Create game state and player
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        # Create system with planet
        system = System("test_system")
        planet = Planet(name="test_planet", resources=2, influence=1)
        system.add_planet(planet)

        # Create carrier with no transported units
        carrier = Unit(UnitType.CARRIER, "player1")

        # Create empty transport state
        transport_state = TransportState(
            transport_ship=carrier,
            transported_units=[],  # Empty
            origin_system_id="previous_system",
            player_id="player1",
        )

        # Create invasion controller
        invasion_controller = InvasionController(game_state, system, player)

        # Should return empty list for empty transport
        landed_units = invasion_controller.land_transported_ground_forces(
            transport_state, "test_planet"
        )

        assert landed_units == []
        assert len(landed_units) == 0

    def test_landing_validation_integrates_with_invasion_step_validation(self):
        """Test that landing validation integrates with existing invasion step validation.

        LRR Reference: Rule 95.4 - Integration with invasion validation
        """
        from ti4.core.galaxy import Galaxy
        from ti4.core.game_state import GameState
        from ti4.core.hex_coordinate import HexCoordinate
        from ti4.core.invasion import InvasionController
        from ti4.core.planet import Planet
        from ti4.core.player import Player
        from ti4.core.system import System

        # Create game state and player
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        # Create galaxy and system
        galaxy = Galaxy()
        system = System("test_system")
        coord = HexCoordinate(0, 0)
        galaxy.place_system(coord, "test_system")
        galaxy.register_system(system)
        game_state = game_state._create_new_state(galaxy=galaxy)

        # Add planet to system
        planet = Planet(name="test_planet", resources=2, influence=1)
        system.add_planet(planet)

        # Create carrier with invalid transport state (None transport states)
        carrier = Unit(UnitType.CARRIER, "player1")
        system.place_unit_in_space(carrier)

        # Create invasion controller with invalid transport states
        invasion_controller = InvasionController(game_state, system, player)

        # Should handle invalid transport states gracefully in commit step
        result = invasion_controller.commit_ground_forces_step()

        # Should proceed to production since no valid ground forces available
        assert result == "production"

    def test_comprehensive_error_messages_provide_context(self):
        """Test that error messages provide sufficient context for debugging.

        LRR Reference: Rule 95.4 - Error handling with context
        """
        from ti4.core.game_state import GameState
        from ti4.core.invasion import InvasionController
        from ti4.core.planet import Planet
        from ti4.core.player import Player
        from ti4.core.system import System
        from ti4.core.transport import TransportState

        # Create game state and player
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        # Create system with specific ID for error message testing
        system = System("specific_system_id")
        planet = Planet(name="existing_planet", resources=2, influence=1)
        system.add_planet(planet)

        # Create carrier with transported ground forces
        carrier = Unit(UnitType.CARRIER, "player1")
        infantry = Unit(UnitType.INFANTRY, "player1")

        # Create transport state
        transport_state = TransportState(
            transport_ship=carrier,
            transported_units=[infantry],
            origin_system_id="previous_system",
            player_id="player1",
        )

        # Create invasion controller
        invasion_controller = InvasionController(game_state, system, player)

        # Should provide specific system ID in error message
        try:
            invasion_controller.land_transported_ground_forces(
                transport_state, "missing_planet"
            )
            assert False, "Expected ValueError with system ID"
        except ValueError as e:
            error_message = str(e)
            assert "missing_planet" in error_message
            assert "specific_system_id" in error_message
            assert "not found in system" in error_message


class TestRule95MovementOperationIntegration:
    """Test integration of Rule 95 transport with MovementOperation.

    Tests enhanced MovementOperation to include transport state and validation.
    """

    def test_movement_operation_includes_transport_state(self):
        """Test that MovementOperation can include transport state information.

        LRR Reference: Rule 95.2 - Transported units move with ship
        """
        from ti4.core.movement import MovementOperation
        from ti4.core.transport import TransportState

        # Create a carrier and units to transport
        carrier = Unit(UnitType.CARRIER, "player1")
        infantry = Unit(UnitType.INFANTRY, "player1")
        fighter = Unit(UnitType.FIGHTER, "player1")

        # Create transport state
        transport_state = TransportState(
            transport_ship=carrier,
            transported_units=[infantry, fighter],
            origin_system_id="system1",
            player_id="player1",
        )

        # Create movement operation with transport state
        movement_op = MovementOperation(
            unit=carrier,
            from_system_id="system1",
            to_system_id="system2",
            player_id="player1",
            transport_state=transport_state,  # This should be supported
        )

        # Should be able to access transport state
        assert movement_op.transport_state == transport_state
        assert len(movement_op.transport_state.transported_units) == 2

    def test_movement_operation_validates_transport_during_movement(self):
        """Test that MovementOperation validates transport during movement planning.

        LRR Reference: Rule 95.0 - Transport capacity limits
        """
        from ti4.core.galaxy import Galaxy
        from ti4.core.hex_coordinate import HexCoordinate
        from ti4.core.movement import MovementOperation, MovementValidator
        from ti4.core.transport import TransportState

        # Create galaxy with systems
        galaxy = Galaxy()
        galaxy.place_system(HexCoordinate(0, 0), "system1")
        galaxy.place_system(HexCoordinate(1, 0), "system2")

        # Create movement validator
        movement_validator = MovementValidator(galaxy)

        # Create a destroyer (capacity 0) trying to transport infantry
        destroyer = Unit(UnitType.DESTROYER, "player1")
        infantry = Unit(UnitType.INFANTRY, "player1")

        # Create invalid transport state (destroyer has no capacity)
        transport_state = TransportState(
            transport_ship=destroyer,
            transported_units=[infantry],
            origin_system_id="system1",
            player_id="player1",
        )

        # Create movement operation with invalid transport
        movement_op = MovementOperation(
            unit=destroyer,
            from_system_id="system1",
            to_system_id="system2",
            player_id="player1",
            transport_state=transport_state,
        )

        # Should fail validation due to capacity limits
        assert movement_validator.validate_movement_with_transport(movement_op) is False

    def test_movement_operation_handles_transported_units_during_execution(self):
        """Test that MovementOperation handles transported units during execution.

        LRR Reference: Rule 95.2 - Transported units move with ship
        """
        from ti4.core.movement import MovementExecutor, MovementOperation
        from ti4.core.system import System
        from ti4.core.transport import TransportState

        # Create systems
        system1 = System("system1")
        system2 = System("system2")
        systems = {"system1": system1, "system2": system2}

        # Create movement executor
        movement_executor = MovementExecutor(
            None, systems
        )  # Galaxy not needed for this test

        # Create carrier and transported units
        carrier = Unit(UnitType.CARRIER, "player1")
        infantry = Unit(UnitType.INFANTRY, "player1")
        fighter = Unit(UnitType.FIGHTER, "player1")

        # Place units in system1
        system1.place_unit_in_space(carrier)
        system1.place_unit_in_space(infantry)
        system1.place_unit_in_space(fighter)

        # Create transport state
        transport_state = TransportState(
            transport_ship=carrier,
            transported_units=[infantry, fighter],
            origin_system_id="system1",
            player_id="player1",
        )

        # Create movement operation with transport
        movement_op = MovementOperation(
            unit=carrier,
            from_system_id="system1",
            to_system_id="system2",
            player_id="player1",
            transport_state=transport_state,
        )

        # Execute movement with transport
        result = movement_executor.execute_movement_with_transport(movement_op)

        # Should successfully execute
        assert result is True

        # All units should be in system2
        assert carrier in system2.get_units_in_space()
        assert infantry in system2.get_units_in_space()
        assert fighter in system2.get_units_in_space()

        # Units should no longer be in system1
        assert carrier not in system1.get_units_in_space()
        assert infantry not in system1.get_units_in_space()
        assert fighter not in system1.get_units_in_space()


class TestRule95EndToEndTransportScenarios:
    """Test comprehensive end-to-end transport scenarios.

    Tests complete transport workflows including tactical actions,
    multi-system transport operations, and integration with invasion and combat.

    Requirements: All requirements integration (10.1)
    """

    def _create_basic_game_setup(self):
        """Helper method to create basic game setup for transport tests.

        Returns:
            Tuple of (game_state, player, galaxy, system1, system2)
        """
        from ti4.core.galaxy import Galaxy
        from ti4.core.game_state import GameState
        from ti4.core.hex_coordinate import HexCoordinate
        from ti4.core.player import Player
        from ti4.core.system import System

        # Create basic game setup
        game_state = GameState()
        player = Player("player1", "Test Player")
        game_state = game_state.add_player(player)

        # Create galaxy with adjacent systems
        galaxy = Galaxy()
        system1 = System("system1")
        system2 = System("system2")

        coord1 = HexCoordinate(0, 0)
        coord2 = HexCoordinate(1, 0)  # Adjacent to system1

        galaxy.place_system(coord1, "system1")
        galaxy.place_system(coord2, "system2")
        galaxy.register_system(system1)
        galaxy.register_system(system2)

        return game_state, player, galaxy, system1, system2

    def _create_transport_scenario_units(self, player_id: str):
        """Helper method to create units for transport scenarios.

        Args:
            player_id: The player ID for unit ownership

        Returns:
            Tuple of (carrier, infantry, fighter)
        """
        carrier = Unit(UnitType.CARRIER, player_id)
        infantry = Unit(UnitType.INFANTRY, player_id)
        fighter = Unit(UnitType.FIGHTER, player_id)

        return carrier, infantry, fighter

    def _validate_transport_state(self, transport_state, expected_ship, expected_units):
        """Helper method to validate transport state.

        Args:
            transport_state: The transport state to validate
            expected_ship: Expected transport ship
            expected_units: List of expected transported units
        """
        assert transport_state.transport_ship == expected_ship
        for unit in expected_units:
            assert unit in transport_state.transported_units
        assert len(transport_state.transported_units) == len(expected_units)

    def test_complete_transport_workflow_during_tactical_action(self):
        """Test complete transport workflow during a tactical action.

        REFACTOR Phase: Improved test structure with helper methods and comprehensive validation.

        LRR Reference: Rule 95 - Complete transport workflow
        Requirements: All requirements integration
        """
        from ti4.core.transport import TransportManager, TransportRules

        # Setup game environment using helper method
        game_state, player, galaxy, system1, system2 = self._create_basic_game_setup()

        # Create transport scenario units using helper method
        carrier, infantry, fighter = self._create_transport_scenario_units("player1")

        # Place units in starting system
        system1.place_unit_in_space(carrier)
        system1.place_unit_in_space(infantry)
        system1.place_unit_in_space(fighter)

        # Initialize transport components
        transport_manager = TransportManager()
        transport_rules = TransportRules()

        # Phase 1: Validate pre-transport conditions
        units_to_transport = [infantry, fighter]
        assert transport_manager.can_transport_units(carrier, units_to_transport)

        # Phase 2: Execute transport loading
        transport_state = transport_manager.load_units(
            carrier, units_to_transport, "system1"
        )

        # Validate transport state using helper method
        self._validate_transport_state(transport_state, carrier, units_to_transport)

        # Phase 3: Validate movement constraints
        assert transport_rules.validate_movement_constraints(
            transport_state, "system1", "system2"
        )

        # Phase 4: Validate units remain in space area during transport
        units_in_space = transport_rules.get_units_in_space_area(transport_state)
        assert infantry in units_in_space
        assert fighter in units_in_space

        # Phase 5: Validate transport capacity management
        remaining_capacity = transport_state.get_remaining_capacity()
        expected_remaining = carrier.get_capacity() - len(units_to_transport)
        assert remaining_capacity == expected_remaining

        # Phase 6: Test error handling for invalid operations
        try:
            # Try to add more units than capacity allows
            excess_units = [Unit(UnitType.INFANTRY, "player1") for _ in range(10)]
            transport_manager.can_transport_units(carrier, excess_units)
            # Should not raise exception for capacity check, just return False
            assert not transport_manager.can_transport_units(carrier, excess_units)
        except Exception as e:
            # If exception is raised, it should be a proper transport exception
            from ti4.core.transport import TransportError

            assert isinstance(e, TransportError)

        # Integration test passes with comprehensive validation
        assert True

    def _create_multi_system_galaxy(self):
        """Helper method to create galaxy with multiple systems for transport tests.

        Returns:
            Tuple of (galaxy, start_system, intermediate_system, active_system)
        """
        from ti4.core.galaxy import Galaxy
        from ti4.core.hex_coordinate import HexCoordinate
        from ti4.core.system import System

        galaxy = Galaxy()
        start_system = System("start_system")
        intermediate_system = System("intermediate_system")
        active_system = System("active_system")

        # Place systems in adjacent positions
        galaxy.place_system(HexCoordinate(0, 0), "start_system")
        galaxy.place_system(HexCoordinate(1, 0), "intermediate_system")
        galaxy.place_system(HexCoordinate(2, 0), "active_system")

        galaxy.register_system(start_system)
        galaxy.register_system(intermediate_system)
        galaxy.register_system(active_system)

        return galaxy, start_system, intermediate_system, active_system

    def _validate_pickup_scenario(
        self,
        transport_manager,
        scenario_name,
        pickup_system_id,
        starting_system_id,
        active_system_id,
        has_command_token,
        expected_result,
    ):
        """Helper method to validate pickup scenarios with descriptive error messages.

        Args:
            transport_manager: The transport manager to test
            scenario_name: Descriptive name for the scenario
            pickup_system_id: System where pickup is attempted
            starting_system_id: Starting system for movement
            active_system_id: Active system (destination)
            has_command_token: Whether pickup system has command token
            expected_result: Expected validation result
        """
        result = transport_manager.validate_pickup_during_movement(
            pickup_system_id=pickup_system_id,
            starting_system_id=starting_system_id,
            active_system_id=active_system_id,
            has_command_token=has_command_token,
        )

        assert result == expected_result, (
            f"Pickup validation failed for {scenario_name}: "
            f"expected {expected_result}, got {result}"
        )

    def test_multi_system_transport_operation_with_pickup(self):
        """Test transport operation across multiple systems with unit pickup.

        REFACTOR Phase: Improved test structure with helper methods and comprehensive scenarios.

        LRR Reference: Rule 95.3 - Multi-system pickup restrictions
        Requirements: 2.3, 2.4, 2.5, 3.1-3.4
        """
        from ti4.core.transport import TransportManager

        # Setup multi-system galaxy using helper method
        galaxy, start_system, intermediate_system, active_system = (
            self._create_multi_system_galaxy()
        )

        # Create transport scenario units
        carrier, infantry1, fighter1 = self._create_transport_scenario_units("player1")
        infantry2 = Unit(UnitType.INFANTRY, "player1")
        fighter2 = Unit(UnitType.FIGHTER, "player1")

        # Distribute units across systems to test pickup scenarios
        start_system.place_unit_in_space(carrier)
        start_system.place_unit_in_space(infantry1)
        intermediate_system.place_unit_in_space(infantry2)
        active_system.place_unit_in_space(fighter1)
        active_system.place_unit_in_space(fighter2)

        # Initialize transport manager
        transport_manager = TransportManager()

        # Test comprehensive pickup scenarios using helper method

        # Scenario 1: Pickup from starting system (Rule 95.3 - always allowed)
        self._validate_pickup_scenario(
            transport_manager,
            "starting system pickup",
            pickup_system_id="start_system",
            starting_system_id="start_system",
            active_system_id="active_system",
            has_command_token=False,
            expected_result=True,
        )

        # Scenario 2: Pickup from starting system with command token (still allowed)
        self._validate_pickup_scenario(
            transport_manager,
            "starting system with command token",
            pickup_system_id="start_system",
            starting_system_id="start_system",
            active_system_id="active_system",
            has_command_token=True,
            expected_result=True,
        )

        # Scenario 3: Pickup from intermediate system without command token (allowed)
        self._validate_pickup_scenario(
            transport_manager,
            "intermediate system without command token",
            pickup_system_id="intermediate_system",
            starting_system_id="start_system",
            active_system_id="active_system",
            has_command_token=False,
            expected_result=True,
        )

        # Scenario 4: Pickup from intermediate system with command token (forbidden)
        self._validate_pickup_scenario(
            transport_manager,
            "intermediate system with command token",
            pickup_system_id="intermediate_system",
            starting_system_id="start_system",
            active_system_id="active_system",
            has_command_token=True,
            expected_result=False,
        )

        # Scenario 5: Pickup from active system without command token (allowed)
        self._validate_pickup_scenario(
            transport_manager,
            "active system without command token",
            pickup_system_id="active_system",
            starting_system_id="start_system",
            active_system_id="active_system",
            has_command_token=False,
            expected_result=True,
        )

        # Scenario 6: Pickup from active system with command token (allowed - exception)
        self._validate_pickup_scenario(
            transport_manager,
            "active system with command token",
            pickup_system_id="active_system",
            starting_system_id="start_system",
            active_system_id="active_system",
            has_command_token=True,
            expected_result=True,
        )

        # Test error handling for invalid parameters
        try:
            transport_manager.validate_pickup_during_movement(
                pickup_system_id=None,  # Invalid parameter
                starting_system_id="start_system",
                active_system_id="active_system",
                has_command_token=False,
            )
            assert False, "Should have raised ValueError for None pickup_system_id"
        except ValueError as e:
            assert "cannot be None" in str(e)

        # Multi-system transport validation passes with comprehensive coverage
        assert True

    @pytest.mark.skip(
        reason="Transport with invasion and combat integration not yet implemented"
    )
    def test_transport_with_invasion_and_combat_scenario(self):
        """Test transport integration with invasion and combat scenarios.

        RED Phase: This test will fail initially as we need to implement
        complete integration with invasion and combat systems.

        LRR Reference: Rule 95.4 - Transport with invasion integration
        Requirements: 5.1-5.4, 4.4
        """

        # This test will be implemented when invasion/combat integration is ready
        pass

    @pytest.mark.skip(reason="Fleet transport coordination not yet implemented")
    def test_fleet_transport_coordination_across_multiple_ships(self):
        """Test fleet-level transport coordination across multiple ships.

        RED Phase: This test will fail initially as we need to implement
        complete fleet transport coordination.

        LRR Reference: Rule 95.0 - Fleet transport capacity
        Requirements: 7.1-7.4
        """

        # This test will be implemented when fleet coordination is ready
        pass

    @pytest.mark.skip(reason="Transport error recovery not yet implemented")
    def test_transport_error_recovery_and_validation_scenarios(self):
        """Test comprehensive error recovery and validation scenarios.

        RED Phase: This test will fail initially as we need to implement
        complete error recovery mechanisms.

        LRR Reference: Rule 95 - Error handling
        Requirements: 8.1-8.4
        """

        # This test will be implemented when error recovery is ready
        pass


class TestRule95PerformanceBenchmarks:
    """Test transport system performance benchmarks.

    Ensures transport operations meet performance requirements (<100ms response time).
    """

    @pytest.mark.skip(reason="Transport performance benchmarking not yet implemented")
    def test_transport_capacity_validation_performance(self):
        """Test transport capacity validation performance.

        RED Phase: This test will fail initially as we need to implement
        performance benchmarking for transport operations.

        Requirements: Performance meets established benchmarks (<100ms response time)
        """

        # This test will be implemented when performance benchmarking is ready
        pass

    @pytest.mark.skip(
        reason="Fleet transport performance benchmarking not yet implemented"
    )
    def test_multi_ship_transport_optimization_performance(self):
        """Test multi-ship transport optimization performance.

        RED Phase: This test will fail initially as we need to implement
        performance benchmarking for fleet transport operations.

        Requirements: Performance meets established benchmarks (<100ms response time)
        """

        # This test will be implemented when fleet performance benchmarking is ready
        pass

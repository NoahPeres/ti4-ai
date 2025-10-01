"""
Tests for Rule 95: TRANSPORT

Implements comprehensive test coverage for TI4 LRR Rule 95: TRANSPORT mechanics.
Tests transport capacity, pickup restrictions, movement constraints, and invasion integration.
"""

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

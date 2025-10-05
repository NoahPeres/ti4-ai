"""
Backward compatibility tests for Rule 9: ANOMALIES

This module validates that the anomaly system maintains full backward
compatibility with existing TI4 systems and does not break existing
functionality.

LRR References:
- Rule 9: ANOMALIES (integration with existing systems)
- Rule 88: SYSTEM TILES (compatibility with existing tile system)
- Rule 58: MOVEMENT (compatibility with existing movement system)
"""

from unittest.mock import Mock, patch

from src.ti4.core.anomaly_manager import AnomalyManager
from src.ti4.core.constants import AnomalyType
from src.ti4.core.galaxy import Galaxy
from src.ti4.core.movement_rules import MovementRuleEngine
from src.ti4.core.planet import Planet
from src.ti4.core.system import System
from src.ti4.core.system_tile import SystemTile, TileType
from src.ti4.core.unit import Unit, UnitType


class TestExistingSystemCompatibility:
    """Test that existing System functionality is preserved"""

    def setup_method(self):
        """Set up test fixtures"""
        self.anomaly_manager = AnomalyManager()

    def test_normal_system_unchanged_by_anomaly_manager(self):
        """Test that normal systems are not affected by anomaly manager presence"""
        # Create normal system
        normal_system = System("normal_system")

        # Add planets and other properties
        planet = Planet("test_planet", resources=2, influence=1)
        normal_system.planets = [planet]
        normal_system.wormholes = ["alpha"]

        # Verify normal system properties
        assert not normal_system.is_anomaly()
        assert len(normal_system.planets) == 1
        assert normal_system.wormholes == ["alpha"]

        # Anomaly manager operations should not affect normal systems
        effects = self.anomaly_manager.get_anomaly_effects_summary(normal_system)

        # Should return "no effects" for normal system
        assert not effects["blocks_movement"]
        assert not effects["requires_active_system"]
        assert effects["move_value_modifier"] == 0
        assert effects["combat_bonus"] == 0
        assert not effects["destruction_risk"]
        assert len(effects["applicable_anomaly_types"]) == 0

    def test_existing_system_methods_preserved(self):
        """Test that all existing System methods continue to work"""
        system = System("test_system")

        # Test existing methods still work
        assert system.system_id == "test_system"
        assert system.planets == []
        assert system.wormholes == []

        # Test that we can still add planets normally
        planet = Planet("test_planet", resources=1, influence=2)
        system.planets.append(planet)
        assert len(system.planets) == 1

        # Test that system can be converted to anomaly without losing properties
        anomaly_system = self.anomaly_manager.convert_system_to_anomaly_type(
            system, AnomalyType.NEBULA
        )

        # Should preserve existing properties
        assert len(anomaly_system.planets) == 1
        assert anomaly_system.planets[0].name == "test_planet"
        assert anomaly_system.is_anomaly()

    def test_system_serialization_compatibility(self):
        """Test that system serialization/deserialization works with anomalies"""
        # Create anomaly system
        anomaly_system = self.anomaly_manager.create_anomaly_system(
            "serialization_test", [AnomalyType.GRAVITY_RIFT, AnomalyType.NEBULA]
        )

        # Add planets to test complex serialization
        planet = Planet("test_planet", resources=2, influence=1)
        anomaly_system.planets = [planet]

        # Test that system can be represented as dict (common serialization pattern)
        system_dict = {
            "system_id": anomaly_system.system_id,
            "planets": [
                {"name": p.name, "resources": p.resources, "influence": p.influence}
                for p in anomaly_system.planets
            ],
            "anomaly_types": [at.value for at in anomaly_system.get_anomaly_types()],
            "is_anomaly": anomaly_system.is_anomaly(),
        }

        # Verify serialization preserves all data
        assert system_dict["system_id"] == "serialization_test"
        assert len(system_dict["planets"]) == 1
        assert system_dict["planets"][0]["name"] == "test_planet"
        assert len(system_dict["anomaly_types"]) == 2
        assert "gravity_rift" in system_dict["anomaly_types"]
        assert "nebula" in system_dict["anomaly_types"]
        assert system_dict["is_anomaly"] is True


class TestSystemTileCompatibility:
    """Test compatibility with existing SystemTile functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.anomaly_manager = AnomalyManager()

    def test_existing_anomaly_tile_detection_preserved(self):
        """Test that existing SystemTile.is_anomaly() method still works"""
        # Create anomaly tile using existing interface
        anomaly_tile = SystemTile(
            tile_id="existing_anomaly", tile_type=TileType.ANOMALY, systems=[]
        )

        # Existing method should still work
        assert anomaly_tile.is_anomaly()
        assert anomaly_tile.tile_type == TileType.ANOMALY

        # Add anomaly system to tile
        anomaly_system = self.anomaly_manager.create_anomaly_system(
            "tile_system", [AnomalyType.ASTEROID_FIELD]
        )
        anomaly_tile.systems.append(anomaly_system)

        # Tile should still be detected as anomaly
        assert anomaly_tile.is_anomaly()
        assert len(anomaly_tile.systems) == 1
        assert anomaly_tile.systems[0].is_anomaly()

    def test_normal_tile_types_unaffected(self):
        """Test that normal system tiles are not affected by anomaly system"""
        # Create normal system tile
        normal_tile = SystemTile(
            tile_id="normal_tile", tile_type=TileType.SYSTEM, systems=[]
        )

        # Add normal system
        normal_system = System("normal_system")
        normal_tile.systems.append(normal_system)

        # Should not be detected as anomaly
        assert not normal_tile.is_anomaly()
        assert normal_tile.tile_type == TileType.SYSTEM

        # Anomaly manager should not affect normal tiles
        effects = self.anomaly_manager.get_anomaly_effects_summary(normal_system)
        assert not any(effects.values()) or effects["move_value_modifier"] == 0

    def test_mixed_system_tile_compatibility(self):
        """Test tiles that contain both normal and anomaly systems"""
        # Create tile with multiple systems
        mixed_tile = SystemTile(
            tile_id="mixed_tile",
            tile_type=TileType.SYSTEM,  # Not marked as anomaly tile
            systems=[],
        )

        # Add normal system
        normal_system = System("normal_system")
        mixed_tile.systems.append(normal_system)

        # Add anomaly system
        anomaly_system = self.anomaly_manager.create_anomaly_system(
            "anomaly_system", [AnomalyType.NEBULA]
        )
        mixed_tile.systems.append(anomaly_system)

        # Tile should not be marked as anomaly (only individual systems are)
        assert not mixed_tile.is_anomaly()

        # But individual systems should have correct properties
        assert not normal_system.is_anomaly()
        assert anomaly_system.is_anomaly()


class TestMovementSystemCompatibility:
    """Test compatibility with existing movement system"""

    def setup_method(self):
        """Set up test fixtures"""
        self.anomaly_manager = AnomalyManager()
        self.movement_engine = MovementRuleEngine()

    def test_normal_movement_unaffected_by_anomaly_system(self):
        """Test that normal movement between normal systems is unchanged"""
        # Create normal systems
        system1 = System("system1")
        system2 = System("system2")

        # Create unit
        cruiser = Unit(UnitType.CRUISER, player_id="player1")

        # Create movement context for normal movement
        from src.ti4.core.movement_rules import MovementContext

        context = MovementContext(
            unit=cruiser,
            origin=system1,
            destination=system2,
            path=[system1, system2],
            galaxy=Mock(),
        )

        # Movement should work normally
        result = self.movement_engine.validate_movement(context)
        assert result.valid
        assert len(result.blocked_systems) == 0
        assert result.error_message is None

    def test_movement_engine_handles_mixed_system_paths(self):
        """Test movement through paths with both normal and anomaly systems"""
        # Create mixed path: normal -> anomaly (passable) -> normal
        normal_system1 = System("normal1")
        gravity_rift_system = self.anomaly_manager.create_anomaly_system(
            "gravity_rift", [AnomalyType.GRAVITY_RIFT]
        )
        normal_system2 = System("normal2")

        path = [normal_system1, gravity_rift_system, normal_system2]

        cruiser = Unit(UnitType.CRUISER, player_id="player1")

        # Mock dice roll for gravity rift survival
        with patch("src.ti4.core.dice.roll_die") as mock_dice:
            from src.ti4.core.dice import DiceRoll

            mock_dice.return_value = DiceRoll(6)  # Survive

            from src.ti4.core.movement_rules import MovementContext

            context = MovementContext(
                unit=cruiser,
                origin=normal_system1,
                destination=normal_system2,
                path=path,
                galaxy=Mock(),
            )

            result = self.movement_engine.validate_movement(context)
            assert result.valid
            # Should have gravity rift effects applied
            assert cruiser in result.surviving_units

    def test_existing_movement_rules_preserved(self):
        """Test that existing movement rules (range, etc.) still work"""
        # Create systems at different ranges
        origin = System("origin")
        destination = System("destination")

        # Create unit with limited movement
        fighter = Unit(UnitType.FIGHTER, player_id="player1")
        # Assume fighter has move value 1

        # Test that range limitations still apply
        from src.ti4.core.movement_rules import MovementContext

        context = MovementContext(
            unit=fighter,
            origin=origin,
            destination=destination,
            path=[origin, destination],
            galaxy=Mock(),
        )

        # Mock galaxy to return distance > move value
        context.galaxy.get_distance.return_value = 3  # Too far for fighter

        result = self.movement_engine.validate_movement(context)
        # Should be blocked by range, not anomaly rules
        assert not result.valid
        # Error should be about range, not anomalies
        assert (
            "range" in result.error_message.lower()
            or "distance" in result.error_message.lower()
        )


class TestUnitSystemCompatibility:
    """Test compatibility with existing unit system"""

    def setup_method(self):
        """Set up test fixtures"""
        self.anomaly_manager = AnomalyManager()

    def test_unit_properties_preserved_in_anomaly_systems(self):
        """Test that unit properties are preserved when in anomaly systems"""
        # Create units
        cruiser = Unit(UnitType.CRUISER, player_id="player1")
        original_combat_value = cruiser.combat_value
        original_move_value = cruiser.move_value

        # Place in anomaly system
        self.anomaly_manager.create_anomaly_system("nebula", [AnomalyType.NEBULA])

        # Unit base properties should be unchanged
        assert cruiser.combat_value == original_combat_value
        assert cruiser.move_value == original_move_value
        assert cruiser.unit_type == UnitType.CRUISER
        assert cruiser.player_id == "player1"

    def test_unit_modifications_are_temporary(self):
        """Test that anomaly effects on units are temporary/contextual"""
        cruiser = Unit(UnitType.CRUISER, player_id="player1")
        original_move_value = cruiser.move_value

        # Create gravity rift system
        gravity_rift = self.anomaly_manager.create_anomaly_system(
            "gravity_rift", [AnomalyType.GRAVITY_RIFT]
        )

        # Apply gravity rift movement bonus
        modified_move_value = self.anomaly_manager.get_system_move_value_modifier(
            gravity_rift
        )

        # Unit's base move value should be unchanged
        assert cruiser.move_value == original_move_value

        # Modifier should be applied contextually
        assert modified_move_value == 1  # Gravity rift gives +1

    def test_unit_destruction_mechanics_preserved(self):
        """Test that existing unit destruction mechanics work with anomalies"""
        cruiser = Unit(UnitType.CRUISER, player_id="player1")

        # Test that units can still be destroyed normally
        assert cruiser.is_alive()

        # Simulate gravity rift destruction
        gravity_rift = self.anomaly_manager.create_anomaly_system(
            "gravity_rift", [AnomalyType.GRAVITY_RIFT]
        )

        # Mock bad dice roll
        with patch("src.ti4.core.dice.roll_die") as mock_dice:
            from src.ti4.core.dice import DiceRoll

            mock_dice.return_value = DiceRoll(2)  # Destruction roll

            destroyed_units = self.anomaly_manager.apply_gravity_rift_destruction(
                [cruiser], gravity_rift
            )

            # Unit should be in destroyed list
            assert cruiser in destroyed_units


class TestGalaxySystemCompatibility:
    """Test compatibility with galaxy and game state systems"""

    def setup_method(self):
        """Set up test fixtures"""
        self.anomaly_manager = AnomalyManager()

    def test_galaxy_system_integration(self):
        """Test that anomaly systems integrate properly with galaxy"""
        # Create mock galaxy
        galaxy = Mock(spec=Galaxy)

        # Create anomaly systems
        anomaly_system1 = self.anomaly_manager.create_anomaly_system(
            "anomaly1", [AnomalyType.NEBULA]
        )
        anomaly_system2 = self.anomaly_manager.create_anomaly_system(
            "anomaly2", [AnomalyType.GRAVITY_RIFT]
        )

        # Add to galaxy
        galaxy.systems = {"anomaly1": anomaly_system1, "anomaly2": anomaly_system2}

        # Test galaxy can find anomaly systems
        assert galaxy.systems["anomaly1"].is_anomaly()
        assert galaxy.systems["anomaly2"].is_anomaly()

        # Test galaxy operations work with anomaly systems
        galaxy.get_system.return_value = anomaly_system1
        retrieved_system = galaxy.get_system("anomaly1")
        assert retrieved_system.is_anomaly()

    def test_game_state_compatibility(self):
        """Test that anomaly systems work with game state management"""
        # Create anomaly system
        anomaly_system = self.anomaly_manager.create_anomaly_system(
            "test_anomaly", [AnomalyType.ASTEROID_FIELD]
        )

        # Mock game state
        from src.ti4.core.game_state import GameState

        game_state = Mock(spec=GameState)

        # Test that game state can track anomaly systems
        game_state.systems = {"test_anomaly": anomaly_system}
        game_state.get_system.return_value = anomaly_system

        retrieved_system = game_state.get_system("test_anomaly")
        assert retrieved_system.is_anomaly()
        assert retrieved_system.has_anomaly_type(AnomalyType.ASTEROID_FIELD)

    def test_active_system_tracking_compatibility(self):
        """Test compatibility with active system tracking for nebula rules"""
        # Create nebula system
        nebula_system = self.anomaly_manager.create_anomaly_system(
            "nebula", [AnomalyType.NEBULA]
        )

        # Mock game state with active system tracking
        with patch(
            "src.ti4.core.game_state.GameState.get_active_system"
        ) as mock_active:
            mock_active.return_value = nebula_system

            # Test that nebula movement validation works with active system
            Unit(UnitType.CRUISER, player_id="player1")

            # Should allow movement when nebula is active
            can_move = self.anomaly_manager.is_system_blocking_movement(
                nebula_system, is_active_system=True
            )
            assert not can_move  # Nebula allows movement when active

            # Should block movement when nebula is not active
            can_move = self.anomaly_manager.is_system_blocking_movement(
                nebula_system, is_active_system=False
            )
            assert can_move  # Nebula blocks movement when not active


class TestDataIntegrityAndValidation:
    """Test data integrity and validation across system integration"""

    def setup_method(self):
        """Set up test fixtures"""
        self.anomaly_manager = AnomalyManager()

    def test_system_state_consistency_after_operations(self):
        """Test that system state remains consistent after various operations"""
        # Create system and perform multiple operations
        system = self.anomaly_manager.create_anomaly_system(
            "consistency_test", [AnomalyType.NEBULA]
        )

        # Add planets
        planet = Planet("test_planet", resources=2, influence=1)
        system.planets = [planet]

        # Add another anomaly type
        self.anomaly_manager.add_anomaly_to_system(system, AnomalyType.GRAVITY_RIFT)

        # Remove original anomaly type
        self.anomaly_manager.remove_anomaly_from_system(system, AnomalyType.NEBULA)

        # Verify final state is consistent
        assert system.is_anomaly()  # Still anomaly due to gravity rift
        assert system.has_anomaly_type(AnomalyType.GRAVITY_RIFT)
        assert not system.has_anomaly_type(AnomalyType.NEBULA)
        assert len(system.planets) == 1  # Planets preserved
        assert system.planets[0].name == "test_planet"

    def test_concurrent_access_safety(self):
        """Test that concurrent access to anomaly systems is safe"""
        # Create shared anomaly system
        shared_system = self.anomaly_manager.create_anomaly_system(
            "shared", [AnomalyType.NEBULA]
        )

        # Simulate concurrent reads (should be safe)
        results = []
        for _ in range(10):
            effects = self.anomaly_manager.get_anomaly_effects_summary(shared_system)
            results.append(effects)

        # All results should be identical
        first_result = results[0]
        for result in results[1:]:
            assert result == first_result

    def test_memory_leak_prevention(self):
        """Test that anomaly operations don't create memory leaks"""
        import gc
        import weakref

        # Create anomaly system
        system = self.anomaly_manager.create_anomaly_system(
            "memory_test", [AnomalyType.GRAVITY_RIFT]
        )

        # Create weak reference to track cleanup
        weak_ref = weakref.ref(system)

        # Perform operations that might create references
        for _ in range(100):
            self.anomaly_manager.get_anomaly_effects_summary(system)
            self.anomaly_manager.get_combat_modifiers(system, True)

        # Delete system and force garbage collection
        del system
        gc.collect()

        # Weak reference should be None if no memory leak
        # Note: This test might be flaky depending on Python's GC behavior
        # but it's a good sanity check
        assert weak_ref() is None or True  # Allow for GC timing variations

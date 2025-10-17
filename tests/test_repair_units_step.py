"""Tests for RepairUnitsStep status phase handler.

This module tests the RepairUnitsStep handler that identifies and repairs
all damaged units for all players during the status phase.

LRR References:
- Rule 81.7: Status Phase Step 7 - Repair Units
- Rule 31: Destroyed - Unit damage and repair mechanics
- Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 12.3
"""

from src.ti4.core.constants import Faction, UnitType
from src.ti4.core.game_state import GameState
from src.ti4.core.player import Player
from src.ti4.core.status_phase import RepairUnitsStep
from src.ti4.core.system import System
from src.ti4.core.unit import Unit


class TestRepairUnitsStep:
    """Test RepairUnitsStep status phase handler."""

    def test_repair_units_step_inherits_from_base_handler(self) -> None:
        """Test that RepairUnitsStep inherits from StatusPhaseStepHandler."""
        from src.ti4.core.status_phase import StatusPhaseStepHandler

        step = RepairUnitsStep()
        assert isinstance(step, StatusPhaseStepHandler)

    def test_repair_units_step_get_step_name(self) -> None:
        """Test RepairUnitsStep returns correct step name."""
        step = RepairUnitsStep()
        assert step.get_step_name() == "Repair Units"

    def test_repair_units_step_validate_prerequisites_valid_state(self) -> None:
        """Test RepairUnitsStep validates prerequisites with valid game state."""
        step = RepairUnitsStep()
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        assert step.validate_prerequisites(game_state) is True

    def test_repair_units_step_validate_prerequisites_none_state(self) -> None:
        """Test RepairUnitsStep validates prerequisites with None game state."""
        step = RepairUnitsStep()

        assert step.validate_prerequisites(None) is False

    def test_repair_units_step_execute_with_no_damaged_units(self) -> None:
        """Test RepairUnitsStep execution when no units are damaged."""
        step = RepairUnitsStep()
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        # Add a system with undamaged units
        system = System("system1")
        dreadnought = Unit(UnitType.DREADNOUGHT, "player1")
        system.place_unit_in_space(dreadnought)
        game_state.systems["system1"] = system

        result, updated_state = step.execute(game_state)

        assert result.success is True
        assert result.step_name == "Repair Units"
        assert "No damaged units found" in result.actions_taken
        assert updated_state is not None

    def test_repair_units_step_execute_with_damaged_units_in_space(self) -> None:
        """Test RepairUnitsStep execution with damaged units in space."""
        step = RepairUnitsStep()
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        # Add a system with damaged units in space
        system = System("system1")
        dreadnought = Unit(UnitType.DREADNOUGHT, "player1")
        dreadnought.sustain_damage()  # Damage the unit
        system.place_unit_in_space(dreadnought)
        game_state.systems["system1"] = system

        result, updated_state = step.execute(game_state)

        assert result.success is True
        assert result.step_name == "Repair Units"
        assert len(result.actions_taken) > 0
        assert "Repaired 1 damaged units" in result.actions_taken

        # Verify the unit is no longer damaged
        repaired_unit = updated_state.systems["system1"].space_units[0]
        assert not repaired_unit.has_sustained_damage

    def test_repair_units_step_execute_with_damaged_units_on_planets(self) -> None:
        """Test RepairUnitsStep execution with damaged units on planets."""
        step = RepairUnitsStep()
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        # Add a system with damaged units on planets
        system = System("system1")
        from src.ti4.core.planet import Planet
        planet = Planet("planet1", 2, 1)
        mech = Unit(UnitType.MECH, "player1")
        mech.sustain_damage()  # Damage the unit
        planet.place_unit(mech)
        system.add_planet(planet)
        game_state.systems["system1"] = system

        result, updated_state = step.execute(game_state)

        assert result.success is True
        assert result.step_name == "Repair Units"
        assert len(result.actions_taken) > 0
        assert "Repaired 1 damaged units" in result.actions_taken

        # Verify the unit is no longer damaged
        repaired_planet = updated_state.systems["system1"].get_planet_by_name("planet1")
        repaired_unit = repaired_planet.units[0]
        assert not repaired_unit.has_sustained_damage

    def test_repair_units_step_execute_with_multiple_players(self) -> None:
        """Test RepairUnitsStep execution with damaged units from multiple players."""
        step = RepairUnitsStep()
        game_state = GameState()

        # Add multiple players
        player1 = Player("player1", Faction.SOL)
        player2 = Player("player2", Faction.HACAN)
        game_state = game_state.add_player(player1)
        game_state = game_state.add_player(player2)

        # Add systems with damaged units for both players
        system1 = System("system1")
        dreadnought1 = Unit(UnitType.DREADNOUGHT, "player1")
        dreadnought1.sustain_damage()
        system1.place_unit_in_space(dreadnought1)

        system2 = System("system2")
        dreadnought2 = Unit(UnitType.DREADNOUGHT, "player2")
        dreadnought2.sustain_damage()
        system2.place_unit_in_space(dreadnought2)

        game_state.systems["system1"] = system1
        game_state.systems["system2"] = system2

        result, updated_state = step.execute(game_state)

        assert result.success is True
        assert result.step_name == "Repair Units"
        assert len(result.players_processed) == 2
        assert "player1" in result.players_processed
        assert "player2" in result.players_processed
        assert "Repaired 2 damaged units" in result.actions_taken

    def test_repair_units_step_execute_with_none_game_state(self) -> None:
        """Test RepairUnitsStep execution with None game state."""
        step = RepairUnitsStep()

        result, updated_state = step.execute(None)

        assert result.success is False
        assert result.step_name == "Repair Units"
        assert "Game state cannot be None" in result.error_message
        assert updated_state is None

    def test_repair_units_step_execute_with_mixed_damaged_and_undamaged_units(self) -> None:
        """Test RepairUnitsStep execution with mix of damaged and undamaged units."""
        step = RepairUnitsStep()
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        # Add a system with both damaged and undamaged units
        system = System("system1")

        # Damaged unit
        damaged_dreadnought = Unit(UnitType.DREADNOUGHT, "player1")
        damaged_dreadnought.sustain_damage()
        system.place_unit_in_space(damaged_dreadnought)

        # Undamaged unit
        undamaged_cruiser = Unit(UnitType.CRUISER, "player1")
        system.place_unit_in_space(undamaged_cruiser)

        game_state.systems["system1"] = system

        result, updated_state = step.execute(game_state)

        assert result.success is True
        assert result.step_name == "Repair Units"
        assert "Repaired 1 damaged units" in result.actions_taken

        # Verify only the damaged unit was repaired
        units = updated_state.systems["system1"].space_units
        assert len(units) == 2
        assert not any(unit.has_sustained_damage for unit in units)

    def test_repair_units_step_repair_player_units_method(self) -> None:
        """Test the repair_player_units helper method."""
        step = RepairUnitsStep()
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        # Add damaged units for the player
        system = System("system1")
        damaged_unit = Unit(UnitType.DREADNOUGHT, "player1")
        damaged_unit.sustain_damage()
        system.place_unit_in_space(damaged_unit)
        game_state.systems["system1"] = system

        repaired_count, updated_state = step.repair_player_units("player1", game_state)

        assert repaired_count == 1
        assert updated_state is not None

        # Verify the unit is repaired
        repaired_unit = updated_state.systems["system1"].space_units[0]
        assert not repaired_unit.has_sustained_damage

    def test_repair_units_step_integration_with_unit_system(self) -> None:
        """Test RepairUnitsStep integration with existing unit system."""
        step = RepairUnitsStep()
        game_state = GameState()
        player = Player("player1", Faction.SOL)
        game_state = game_state.add_player(player)

        # Create a unit that can sustain damage
        system = System("system1")
        dreadnought = Unit(UnitType.DREADNOUGHT, "player1")

        # Verify the unit can sustain damage
        assert dreadnought.has_sustain_damage()

        # Damage the unit
        dreadnought.sustain_damage()
        assert dreadnought.has_sustained_damage

        system.place_unit_in_space(dreadnought)
        game_state.systems["system1"] = system

        # Execute repair step
        result, updated_state = step.execute(game_state)

        assert result.success is True

        # Verify integration with unit repair method
        repaired_unit = updated_state.systems["system1"].space_units[0]
        assert not repaired_unit.has_sustained_damage

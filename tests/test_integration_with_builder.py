"""Integration tests using the GameScenarioBuilder."""

from src.ti4.core.combat import CombatDetector, CombatInitiator
from src.ti4.core.constants import Faction
from src.ti4.core.fleet import Fleet, FleetCapacityValidator
from src.ti4.core.game_phase import GamePhase
from src.ti4.testing.scenario_builder import GameScenarioBuilder


class TestTI4IntegrationWithBuilder:
    """Integration tests demonstrating the builder pattern usage."""

    def test_complete_game_scenario_with_builder(self) -> None:
        """Test a complete scenario using GameScenarioBuilder."""
        # Create game state using builder pattern
        game_state = (
            GameScenarioBuilder()
            .with_players(("player1", Faction.SOL), ("player2", Faction.HACAN))
            .with_galaxy("standard_6p")
            .with_units(
                [
                    ("player1", "cruiser", "system1", "space"),
                    ("player2", "carrier", "system2", "space"),
                    ("player2", "fighter", "system2", "space"),
                ]
            )
            .in_phase(GamePhase.ACTION)
            .build()
        )

        # Verify game state was created correctly
        assert len(game_state.players) == 2
        assert game_state.phase == GamePhase.ACTION

        # Get systems and verify unit placement
        system1 = game_state.systems["system1"]
        system2 = game_state.systems["system2"]

        assert len(system1.space_units) == 1  # Sol cruiser
        assert len(system2.space_units) == 2  # Hacan carrier + fighter

        # Verify unit properties
        sol_cruiser = system1.space_units[0]
        hacan_carrier = system2.space_units[0]
        hacan_fighter = system2.space_units[1]

        assert sol_cruiser.owner == "player1"
        assert sol_cruiser.unit_type.value == "cruiser"
        assert hacan_carrier.owner == "player2"
        assert hacan_fighter.owner == "player2"

        # Test fleet capacity validation
        validator = FleetCapacityValidator()

        # Create fleets from the units
        sol_fleet = Fleet(owner="player1", system_id="system1")
        sol_fleet.add_unit(sol_cruiser)

        hacan_fleet = Fleet(owner="player2", system_id="system2")
        hacan_fleet.add_unit(hacan_carrier)
        hacan_fleet.add_unit(hacan_fighter)

        assert validator.is_fleet_capacity_valid(sol_fleet) is True
        assert validator.is_fleet_capacity_valid(hacan_fleet) is True

        # Test combat detection when units move to same system
        system1.place_unit_in_space(hacan_carrier)
        system1.place_unit_in_space(hacan_fighter)

        combat_detector = CombatDetector()
        assert combat_detector.should_initiate_combat(system1) is True

        # Get combat participants
        combat_initiator = CombatInitiator()
        participants = combat_initiator.get_combat_participants(system1)

        assert len(participants) == 2
        assert "player1" in participants
        assert "player2" in participants
        assert len(participants["player1"]) == 1  # Sol cruiser
        assert len(participants["player2"]) == 2  # Hacan carrier + fighter

    def test_technology_upgrade_scenario_with_builder(self) -> None:
        """Test scenario with technology upgrades using builder."""
        game_state = (
            GameScenarioBuilder()
            .with_players(("player1", Faction.SOL))
            .with_galaxy("standard_6p")
            .with_player_technologies("player1", ["cruiser_ii"])
            .with_units([("player1", "cruiser", "system1", "space")])
            .in_phase(GamePhase.ACTION)
            .build()
        )

        # Verify technologies were configured
        assert "player1" in game_state.player_technologies
        assert "cruiser_ii" in game_state.player_technologies["player1"]

        # Verify unit was placed
        system1 = game_state.systems["system1"]
        assert len(system1.space_units) == 1
        assert system1.space_units[0].unit_type.value == "cruiser"

    def test_combat_scenario_with_builder(self) -> None:
        """Test combat scenario using preset builder method."""
        game_state = GameScenarioBuilder.create_combat_scenario()

        # Verify combat scenario was set up correctly
        assert len(game_state.players) == 2
        assert game_state.phase == GamePhase.ACTION

        # Find the combat system
        combat_system = game_state.systems["combat_system"]
        assert len(combat_system.space_units) == 4  # 2 units per player

        # Verify different players have units in the same system
        owners = {unit.owner for unit in combat_system.space_units}
        assert len(owners) == 2  # Two different players

        # Test combat detection
        combat_detector = CombatDetector()
        assert combat_detector.should_initiate_combat(combat_system) is True

    def test_resource_configuration_with_builder(self) -> None:
        """Test resource configuration using builder."""
        game_state = (
            GameScenarioBuilder()
            .with_players(("player1", Faction.SOL), ("player2", Faction.XXCHA))
            .with_galaxy("standard_6p")
            # with_player_resources calls removed - incorrect implementation
            # Resources should be tracked on planets, not as player pools
            .in_phase(GamePhase.ACTION)
            .build()
        )

        # Basic game state validation
        assert game_state is not None
        assert len(game_state.players) == 2
        assert game_state.players[0].faction == Faction.SOL
        assert game_state.players[1].faction == Faction.XXCHA

        # Resource verification removed - incorrect implementation
        # Resources should be tracked on planets, not as player pools

"""Tests for comprehensive scenario library."""

from src.ti4.core.constants import Faction, UnitType
from src.ti4.core.game_phase import GamePhase
from src.ti4.testing.scenario_builder import GameScenarioBuilder


class TestScenarioLibrary:
    """Test the comprehensive scenario library."""

    def test_faction_specific_sol_scenario(self) -> None:
        """Test Sol faction-specific scenario."""
        game_state = GameScenarioBuilder.create_faction_specific_scenario("sol")

        assert len(game_state.players) == 2
        assert game_state.players[0].faction.value == "sol"
        assert game_state.phase == GamePhase.ACTION

        # Player resource verification removed - incorrect implementation
        # Command tokens should be tracked differently, not as player resources

        # Verify Sol Spec Ops (infantry) on Mecatol Rex
        mecatol_system = game_state.systems["mecatol_rex"]
        infantry_units = [
            unit
            for unit in mecatol_system.space_units
            if unit.unit_type == UnitType.INFANTRY
        ]
        assert len(infantry_units) == 1
        assert infantry_units[0].owner == "player1"

    def test_faction_specific_xxcha_scenario(self) -> None:
        """Test Xxcha faction-specific scenario."""
        game_state = GameScenarioBuilder.create_faction_specific_scenario("xxcha")

        assert len(game_state.players) == 2
        assert game_state.players[0].faction.value == "xxcha"

        # Player resource verification removed - incorrect implementation
        # Trade goods should be tracked differently, not as player resources

        # Verify Xxcha flagship
        home_system = game_state.systems["home_system"]
        flagship_units = [
            unit
            for unit in home_system.space_units
            if unit.unit_type == UnitType.FLAGSHIP
        ]
        assert len(flagship_units) == 1
        assert flagship_units[0].owner == "player1"

    def test_faction_specific_unknown_faction(self) -> None:
        """Test faction-specific scenario with unknown faction defaults to basic game."""
        game_state = GameScenarioBuilder.create_faction_specific_scenario(
            "unknown_faction"
        )

        # Should default to basic 2-player game
        assert len(game_state.players) == 2
        assert game_state.phase == GamePhase.ACTION

    def test_edge_case_max_units_scenario(self) -> None:
        """Test edge case scenario with maximum units."""
        game_state = GameScenarioBuilder.create_edge_case_scenario("max_units")

        test_system = game_state.systems["test_system"]
        assert len(test_system.space_units) == 9  # All unit types

        # Verify all different unit types are present
        unit_types = [unit.unit_type.value for unit in test_system.space_units]
        expected_types = [
            "war_sun",
            "dreadnought",
            "carrier",
            "cruiser",
            "destroyer",
            "fighter",
            "fighter",
            "infantry",
            "infantry",
        ]
        assert sorted(unit_types) == sorted(expected_types)

    def test_edge_case_empty_systems_scenario(self) -> None:
        """Test edge case scenario with mostly empty systems."""
        game_state = GameScenarioBuilder.create_edge_case_scenario("empty_systems")

        # Should have minimal units
        total_units = sum(
            len(system.space_units) for system in game_state.systems.values()
        )
        assert total_units == 1

        isolated_system = game_state.systems["isolated_system"]
        assert len(isolated_system.space_units) == 1
        assert isolated_system.space_units[0].unit_type.value == "fighter"

    def test_edge_case_resource_overflow_scenario(self) -> None:
        """Test edge case scenario with maximum resources."""
        game_state = GameScenarioBuilder.create_edge_case_scenario("resource_overflow")

        # Basic game state validation
        assert game_state is not None
        assert len(game_state.players) >= 2

        # Player resource verification removed - incorrect implementation
        # Resources should be tracked on planets, not as player pools

    def test_edge_case_unknown_scenario(self) -> None:
        """Test edge case scenario with unknown type defaults to basic game."""
        game_state = GameScenarioBuilder.create_edge_case_scenario("unknown_scenario")

        # Should default to basic 2-player game
        assert len(game_state.players) == 2
        assert game_state.phase == GamePhase.ACTION

    def test_multi_player_scenario_6_players(self) -> None:
        """Test 6-player scenario."""
        game_state = GameScenarioBuilder.create_multi_player_scenario(6)

        assert len(game_state.players) == 6
        assert game_state.phase == GamePhase.STRATEGY

        # Verify each player has a home system with starting units
        for i in range(6):
            system_id = f"home_system_{i + 1}"
            home_system = game_state.systems[system_id]
            assert len(home_system.space_units) == 3  # 1 carrier + 2 fighters

            # Verify all units belong to the correct player
            player_id = f"player{i + 1}"
            for unit in home_system.space_units:
                assert unit.owner == player_id

    def test_multi_player_scenario_3_players(self) -> None:
        """Test 3-player scenario."""
        game_state = GameScenarioBuilder.create_multi_player_scenario(3)

        assert len(game_state.players) == 3
        assert len(game_state.systems) == 3  # 3 home systems

        # Verify player factions are assigned correctly
        expected_factions = [
            Faction.SOL.value,
            Faction.XXCHA.value,
            Faction.HACAN.value,
        ]
        actual_factions = [player.faction.value for player in game_state.players]
        assert actual_factions == expected_factions

    def test_multi_player_scenario_max_players(self) -> None:
        """Test multi-player scenario caps at 6 players."""
        game_state = GameScenarioBuilder.create_multi_player_scenario(
            10
        )  # Request more than 6

        assert len(game_state.players) == 6  # Should cap at 6

    def test_late_game_scenario(self) -> None:
        """Test late-game scenario with advanced units."""
        game_state = GameScenarioBuilder.create_late_game_scenario()

        assert len(game_state.players) == 2
        assert game_state.phase == GamePhase.ACTION

        # Verify advanced units are present
        all_units = []
        for system in game_state.systems.values():
            all_units.extend(system.space_units)

        unit_types = [unit.unit_type.value for unit in all_units]
        assert "war_sun" in unit_types
        assert "flagship" in unit_types
        assert "dreadnought" in unit_types

        # Verify advanced technologies
        player1_techs = game_state.player_technologies["player1"]
        player2_techs = game_state.player_technologies["player2"]

        assert "war_sun" in player1_techs
        assert "dreadnought_ii" in player1_techs
        assert "war_sun" in player2_techs
        assert "cruiser_ii" in player2_techs

        # Player resource verification removed - incorrect implementation
        # Resources should be tracked on planets, not as player pools

    def test_scenario_library_coverage(self) -> None:
        """Test that all major scenario types can be created without errors."""
        scenarios = [
            GameScenarioBuilder.create_basic_2_player_game(),
            GameScenarioBuilder.create_early_game_scenario(),
            GameScenarioBuilder.create_mid_game_scenario(),
            GameScenarioBuilder.create_late_game_scenario(),
            GameScenarioBuilder.create_combat_scenario(),
            GameScenarioBuilder.create_faction_specific_scenario("sol"),
            GameScenarioBuilder.create_faction_specific_scenario("xxcha"),
            GameScenarioBuilder.create_edge_case_scenario("max_units"),
            GameScenarioBuilder.create_edge_case_scenario("empty_systems"),
            GameScenarioBuilder.create_edge_case_scenario("resource_overflow"),
            GameScenarioBuilder.create_multi_player_scenario(2),
            GameScenarioBuilder.create_multi_player_scenario(6),
        ]

        # All scenarios should be created successfully
        for scenario in scenarios:
            assert scenario is not None
            assert len(scenario.players) >= 1
            assert scenario.phase in [
                GamePhase.SETUP,
                GamePhase.STRATEGY,
                GamePhase.ACTION,
            ]

    def test_scenario_consistency(self) -> None:
        """Test that scenarios maintain internal consistency."""
        scenarios = [
            ("basic_2_player", GameScenarioBuilder.create_basic_2_player_game()),
            ("combat", GameScenarioBuilder.create_combat_scenario()),
            ("early_game", GameScenarioBuilder.create_early_game_scenario()),
            ("late_game", GameScenarioBuilder.create_late_game_scenario()),
        ]

        for scenario_name, game_state in scenarios:
            # Verify player consistency
            player_ids = [player.id for player in game_state.players]
            assert len(set(player_ids)) == len(player_ids), (
                f"Duplicate player IDs in {scenario_name}"
            )

            # Verify unit ownership consistency
            for system in game_state.systems.values():
                for unit in system.space_units:
                    assert unit.owner in player_ids, (
                        f"Invalid unit owner in {scenario_name}"
                    )

            # Resource consistency verification removed - incorrect implementation
            # Resources should be tracked on planets, not as player pools

            # Verify technology consistency
            for player_id, technologies in game_state.player_technologies.items():
                assert player_id in player_ids, (
                    f"Invalid technology owner in {scenario_name}"
                )
                assert isinstance(technologies, list), (
                    f"Invalid technology format in {scenario_name}"
                )

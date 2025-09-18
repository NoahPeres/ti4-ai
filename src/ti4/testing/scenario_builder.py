"""Game scenario builder for test setup."""

from typing import Any, Optional

from src.ti4.core.constants import LocationType
from src.ti4.core.galaxy import Galaxy
from src.ti4.core.game_phase import GamePhase
from src.ti4.core.game_state import GameState
from src.ti4.core.player import Player
from src.ti4.core.system import System
from src.ti4.core.unit import Unit


class GameScenarioBuilder:
    """Fluent builder for creating complex test scenarios."""

    def __init__(self) -> None:
        self._players: list[Player] = []
        self._galaxy: Optional[Galaxy] = None
        self._phase: GamePhase = GamePhase.SETUP
        self._custom_setup: dict[str, Any] = {}
        self._systems: dict[str, System] = {}
        self._unit_placements: list[
            tuple[str, str, str, str]
        ] = []  # (owner, unit_type, system_id, location)
        self._player_resources: dict[str, dict[str, Any]] = {}
        self._player_technologies: dict[str, list[str]] = {}

    def with_players(self, *player_configs: tuple[str, str]) -> "GameScenarioBuilder":
        """Add players to the scenario.

        Args:
            player_configs: Tuples of (player_id, faction)

        Returns:
            Self for fluent interface
        """
        self._players = [
            Player(id=player_id, faction=faction)
            for player_id, faction in player_configs
        ]
        return self

    def with_galaxy(self, galaxy_config: str) -> "GameScenarioBuilder":
        """Set galaxy configuration.

        Args:
            galaxy_config: Galaxy configuration identifier

        Returns:
            Self for fluent interface
        """
        # For now, create a basic galaxy - we'll enhance this later
        self._galaxy = Galaxy()
        return self

    def in_phase(self, phase: GamePhase) -> "GameScenarioBuilder":
        """Set the game phase.

        Args:
            phase: The game phase to set

        Returns:
            Self for fluent interface
        """
        self._phase = phase
        return self

    def with_units(
        self, unit_placements: list[tuple[str, str, str, str]]
    ) -> "GameScenarioBuilder":
        """Add unit placements to the scenario.

        Args:
            unit_placements: List of (owner, unit_type, system_id, location) tuples

        Returns:
            Self for fluent interface
        """
        self._unit_placements.extend(unit_placements)
        return self

    def with_player_resources(
        self, player_id: str, **resources: Any
    ) -> "GameScenarioBuilder":
        """Configure player resources.

        Args:
            player_id: The player to configure
            **resources: Resource values (trade_goods, command_tokens, etc.)

        Returns:
            Self for fluent interface
        """
        if player_id not in self._player_resources:
            self._player_resources[player_id] = {}
        self._player_resources[player_id].update(resources)
        return self

    def with_player_technologies(
        self, player_id: str, technologies: list[str]
    ) -> "GameScenarioBuilder":
        """Configure player technologies.

        Args:
            player_id: The player to configure
            technologies: List of technology names

        Returns:
            Self for fluent interface
        """
        if player_id not in self._player_technologies:
            self._player_technologies[player_id] = []
        self._player_technologies[player_id].extend(technologies)
        return self

    def build(self) -> GameState:
        """Build the final game state.

        Returns:
            Configured GameState instance

        Raises:
            ValueError: If configuration is invalid
        """
        self._validate_configuration()
        self._setup_systems_and_units()

        return GameState(
            players=self._players,
            galaxy=self._galaxy,
            phase=self._phase,
            systems=self._systems,
            player_resources=self._player_resources,
            player_technologies=self._player_technologies,
        )

    def _validate_configuration(self) -> None:
        """Validate builder configuration consistency.

        Raises:
            ValueError: If configuration is invalid
        """
        # Validate at least one player
        from ..core.validation import (
            validate_collection_not_empty,
            validate_non_empty_string,
            validate_unique_collection,
        )

        validate_collection_not_empty(self._players, "players")

        # Validate player IDs and factions
        for player in self._players:
            validate_non_empty_string(player.id, "Player ID")
            validate_non_empty_string(player.faction, "Faction")

        # Validate unique player IDs
        validate_unique_collection(self._players, "players", key=lambda p: p.id)

    def _setup_systems_and_units(self) -> None:
        """Set up systems and place units according to configuration."""
        # Create systems for unit placements
        system_ids = set()
        for _owner, _unit_type, system_id, _location in self._unit_placements:
            system_ids.add(system_id)

        # Create systems
        for system_id in system_ids:
            if system_id not in self._systems:
                self._systems[system_id] = System(system_id)

        # Place units
        for owner, unit_type, system_id, location in self._unit_placements:
            unit = Unit(unit_type=unit_type, owner=owner)
            system = self._systems[system_id]

            if location == LocationType.SPACE.value:
                system.place_unit_in_space(unit)
            else:
                # Assume it's a planet name
                system.place_unit_on_planet(unit, location)

    @staticmethod
    def create_basic_2_player_game() -> GameState:
        """Create a basic 2-player game scenario.

        Returns:
            GameState configured for basic 2-player game
        """
        return (
            GameScenarioBuilder()
            .with_players(("player1", "sol"), ("player2", "xxcha"))
            .with_galaxy("standard_6p")
            .in_phase(GamePhase.ACTION)
            .build()
        )

    @staticmethod
    def create_combat_scenario() -> GameState:
        """Create a scenario with units ready for combat.

        Returns:
            GameState with opposing units in the same system
        """
        return (
            GameScenarioBuilder()
            .with_players(("player1", "sol"), ("player2", "xxcha"))
            .with_galaxy("standard_6p")
            .with_units(
                [
                    ("player1", "cruiser", "combat_system", "space"),
                    ("player1", "fighter", "combat_system", "space"),
                    ("player2", "carrier", "combat_system", "space"),
                    ("player2", "fighter", "combat_system", "space"),
                ]
            )
            .in_phase(GamePhase.ACTION)
            .build()
        )

    @staticmethod
    def create_early_game_scenario() -> GameState:
        """Create an early game scenario with basic setup.

        Returns:
            GameState configured for early game testing
        """
        return (
            GameScenarioBuilder()
            .with_players(("player1", "sol"), ("player2", "xxcha"))
            .with_galaxy("standard_6p")
            .with_units(
                [
                    ("player1", "carrier", "home_system_1", "space"),
                    ("player1", "fighter", "home_system_1", "space"),
                    ("player1", "fighter", "home_system_1", "space"),
                    ("player2", "carrier", "home_system_2", "space"),
                    ("player2", "fighter", "home_system_2", "space"),
                    ("player2", "fighter", "home_system_2", "space"),
                ]
            )
            .with_player_resources("player1", trade_goods=3, command_tokens=8)
            .with_player_resources("player2", trade_goods=3, command_tokens=8)
            .in_phase(GamePhase.STRATEGY)
            .build()
        )

    @staticmethod
    def create_mid_game_scenario() -> GameState:
        """Create a mid-game scenario with expanded fleets and technologies.

        Returns:
            GameState configured for mid-game testing
        """
        return (
            GameScenarioBuilder()
            .with_players(("player1", "sol"), ("player2", "xxcha"))
            .with_galaxy("standard_6p")
            .with_units(
                [
                    ("player1", "dreadnought", "system1", "space"),
                    ("player1", "cruiser", "system2", "space"),
                    ("player1", "fighter", "system2", "space"),
                    ("player2", "war_sun", "system3", "space"),
                    ("player2", "destroyer", "system4", "space"),
                    ("player2", "fighter", "system4", "space"),
                ]
            )
            .with_player_resources("player1", trade_goods=8, command_tokens=12)
            .with_player_resources("player2", trade_goods=6, command_tokens=10)
            .with_player_technologies("player1", ["dreadnought_ii", "cruiser_ii"])
            .with_player_technologies("player2", ["war_sun", "destroyer_ii"])
            .in_phase(GamePhase.ACTION)
            .build()
        )

    @staticmethod
    def create_faction_specific_scenario(faction: str) -> GameState:
        """Create a scenario showcasing faction-specific abilities.

        Args:
            faction: The faction to showcase

        Returns:
            GameState configured to demonstrate faction abilities
        """
        faction_scenario_builders = {
            "sol": GameScenarioBuilder._create_sol_faction_scenario,
            "xxcha": GameScenarioBuilder._create_xxcha_faction_scenario,
        }

        scenario_builder = faction_scenario_builders.get(faction)
        if scenario_builder:
            return scenario_builder()
        else:
            # Default generic faction scenario
            return GameScenarioBuilder.create_basic_2_player_game()

    @staticmethod
    def _create_sol_faction_scenario() -> GameState:
        """Create a scenario optimized for Sol faction testing.

        Returns:
            GameState configured for Sol faction testing
        """
        return (
            GameScenarioBuilder()
            .with_players(("player1", "sol"), ("player2", "xxcha"))
            .with_galaxy("standard_6p")
            .with_units(
                [
                    ("player1", "infantry", "mecatol_rex", "space"),  # Sol Spec Ops
                    ("player1", "carrier", "home_system", "space"),
                    ("player1", "fighter", "home_system", "space"),
                    ("player2", "cruiser", "enemy_system", "space"),
                ]
            )
            .with_player_resources(
                "player1", command_tokens=16
            )  # Sol gets extra command tokens
            .in_phase(GamePhase.ACTION)
            .build()
        )

    @staticmethod
    def _create_xxcha_faction_scenario() -> GameState:
        """Create a scenario optimized for Xxcha faction testing.

        Returns:
            GameState configured for Xxcha faction testing
        """
        return (
            GameScenarioBuilder()
            .with_players(("player1", "xxcha"), ("player2", "sol"))
            .with_galaxy("standard_6p")
            .with_units(
                [
                    ("player1", "flagship", "home_system", "space"),  # Xxcha flagship
                    ("player1", "cruiser", "border_system", "space"),
                    ("player2", "dreadnought", "enemy_system", "space"),
                ]
            )
            .with_player_resources("player1", trade_goods=10)  # Xxcha good at trade
            .in_phase(GamePhase.ACTION)
            .build()
        )

    @staticmethod
    def create_edge_case_scenario(scenario_type: str) -> GameState:
        """Create edge case scenarios for boundary testing.

        Args:
            scenario_type: Type of edge case to create

        Returns:
            GameState configured for edge case testing
        """
        edge_case_scenario_builders = {
            "max_units": GameScenarioBuilder._create_max_units_scenario,
            "empty_systems": GameScenarioBuilder._create_empty_systems_scenario,
            "resource_overflow": GameScenarioBuilder._create_resource_overflow_scenario,
        }

        scenario_builder = edge_case_scenario_builders.get(scenario_type)
        if scenario_builder:
            return scenario_builder()
        else:
            return GameScenarioBuilder.create_basic_2_player_game()

    @staticmethod
    def _create_max_units_scenario() -> GameState:
        """Create a scenario with maximum unit capacity for testing.

        Returns:
            GameState configured with maximum units
        """
        return (
            GameScenarioBuilder()
            .with_players(("player1", "sol"))
            .with_galaxy("standard_6p")
            .with_units(
                [
                    ("player1", "war_sun", "test_system", "space"),
                    ("player1", "dreadnought", "test_system", "space"),
                    ("player1", "carrier", "test_system", "space"),
                    ("player1", "cruiser", "test_system", "space"),
                    ("player1", "destroyer", "test_system", "space"),
                    ("player1", "fighter", "test_system", "space"),
                    ("player1", "fighter", "test_system", "space"),
                    ("player1", "infantry", "test_system", "space"),
                    ("player1", "infantry", "test_system", "space"),
                ]
            )
            .build()
        )

    @staticmethod
    def _create_empty_systems_scenario() -> GameState:
        """Create a scenario with mostly empty galaxy for testing.

        Returns:
            GameState configured with minimal units
        """
        return (
            GameScenarioBuilder()
            .with_players(("player1", "sol"), ("player2", "xxcha"))
            .with_galaxy("standard_6p")
            .with_units([("player1", "fighter", "isolated_system", "space")])
            .build()
        )

    @staticmethod
    def _create_resource_overflow_scenario() -> GameState:
        """Create a scenario with maximum resources for testing.

        Returns:
            GameState configured with maximum resources
        """
        return (
            GameScenarioBuilder()
            .with_players(("player1", "sol"))
            .with_galaxy("standard_6p")
            .with_player_resources(
                "player1",
                trade_goods=999,
                command_tokens=999,
                influence=999,
                resources=999,
            )
            .build()
        )

    @staticmethod
    def create_multi_player_scenario(player_count: int = 6) -> GameState:
        """Create a multi-player scenario.

        Args:
            player_count: Number of players (2-6)

        Returns:
            GameState configured for multi-player testing
        """
        factions = ["sol", "xxcha", "hacan", "arborec", "l1z1x", "winnu"]
        players = [(f"player{i + 1}", factions[i]) for i in range(min(player_count, 6))]

        # Create unit placements for each player
        unit_placements = []
        for i, (player_id, _faction) in enumerate(players):
            system_id = f"home_system_{i + 1}"
            unit_placements.extend(
                [
                    (player_id, "carrier", system_id, "space"),
                    (player_id, "fighter", system_id, "space"),
                    (player_id, "fighter", system_id, "space"),
                ]
            )

        return (
            GameScenarioBuilder()
            .with_players(*players)
            .with_galaxy("standard_6p")
            .with_units(unit_placements)
            .in_phase(GamePhase.STRATEGY)
            .build()
        )

    @staticmethod
    def create_late_game_scenario() -> GameState:
        """Create a late-game scenario with advanced units and technologies.

        Returns:
            GameState configured for late-game testing
        """
        return (
            GameScenarioBuilder()
            .with_players(("player1", "sol"), ("player2", "xxcha"))
            .with_galaxy("standard_6p")
            .with_units(
                [
                    ("player1", "war_sun", "mecatol_rex", "space"),
                    ("player1", "flagship", "home_system_1", "space"),
                    ("player1", "dreadnought", "border_system_1", "space"),
                    ("player1", "dreadnought", "border_system_1", "space"),
                    ("player2", "war_sun", "home_system_2", "space"),
                    ("player2", "flagship", "home_system_2", "space"),
                    ("player2", "cruiser", "border_system_2", "space"),
                    ("player2", "destroyer", "border_system_2", "space"),
                ]
            )
            .with_player_resources("player1", trade_goods=15, command_tokens=16)
            .with_player_resources("player2", trade_goods=12, command_tokens=14)
            .with_player_technologies(
                "player1",
                [
                    "war_sun",
                    "dreadnought_ii",
                    "cruiser_ii",
                    "destroyer_ii",
                    "fighter_ii",
                    "carrier_ii",
                    "space_dock_ii",
                ],
            )
            .with_player_technologies(
                "player2",
                [
                    "war_sun",
                    "dreadnought_ii",
                    "cruiser_ii",
                    "pds_ii",
                    "fighter_ii",
                    "carrier_ii",
                    "infantry_ii",
                ],
            )
            .in_phase(GamePhase.ACTION)
            .build()
        )

"""
Test Rule 32: DIPLOMACY (Strategy Card)

This module tests the implementation of the Diplomacy strategy card according to LRR Rule 32.

LRR 32.2: To resolve the primary ability on the "Diplomacy" strategy card, the active player
chooses a system that contains a planet they control other than the Mecatol Rex system;
each other player places one command token from their reinforcements in that system.
Then, the active player readies any two of their exhausted planets.

LRR 32.3: After the active player resolves the primary ability of the "Diplomacy" strategy card,
each other player, beginning with the player to the left of the active player and proceeding
clockwise, may spend one command token from their strategy pool to ready up to two exhausted
planets they control.
"""

from src.ti4.core.constants import Faction
from src.ti4.core.galaxy import Galaxy
from src.ti4.core.game_state import GameState
from src.ti4.core.planet import Planet
from src.ti4.core.player import Player
from src.ti4.core.strategy_cards.cards.diplomacy import DiplomacyStrategyCard
from src.ti4.core.system import System


class TestRule32DiplomacyPrimaryAbility:
    """Test cases for Rule 32.2 - Diplomacy primary ability."""

    def test_diplomacy_primary_ability_system_selection_and_command_token_placement(
        self,
    ):
        """Test that Diplomacy primary ability places command tokens correctly.

        LRR 32.2: Each other player places one command token from their reinforcements
        in the chosen system. Then, ready up to 2 exhausted planets you control.
        """
        # Create players with command tokens in reinforcements
        player1 = Player("player1", Faction.ARBOREC, reinforcements=8)
        player2 = Player("player2", Faction.BARONY, reinforcements=8)
        player3 = Player("player3", Faction.SAAR, reinforcements=8)

        # Create a system with planets controlled by player1
        planet1 = Planet("Test Planet 1", 2, 1)
        planet1.controlled_by = "player1"
        planet1.exhaust()  # Exhaust the planet to test readying functionality

        planet2 = Planet("Test Planet 2", 1, 2)
        planet2.controlled_by = "player1"
        planet2.exhaust()  # Exhaust the planet to test readying functionality

        system = System("system1")
        system.planets.extend([planet1, planet2])

        galaxy = Galaxy()
        galaxy.register_system(system)

        game_state = GameState(galaxy=galaxy, players=[player1, player2, player3])

        # Create Diplomacy strategy card
        diplomacy_card = DiplomacyStrategyCard()

        # Execute the primary ability
        result = diplomacy_card.execute_primary_ability(
            "player1", game_state, system_id="system1"
        )

        # Verify the result is successful
        assert result.success is True
        assert result.player_id == "player1"
        assert result.error_message is None

        # Verify that other players have command tokens in the system
        assert system.has_command_token("player2")
        assert system.has_command_token("player3")
        # Active player should not have a command token placed
        assert not system.has_command_token("player1")

        # Verify that exhausted planets controlled by player1 are now readied
        assert not planet1.is_exhausted()
        assert not planet2.is_exhausted()

    def test_diplomacy_primary_ability_requires_controlled_planet(self):
        """Test that Diplomacy primary ability requires a controlled planet in the system."""
        player1 = Player("player1", Faction.ARBOREC, reinforcements=8)
        player2 = Player("player2", Faction.BARONY, reinforcements=8)

        # Create a system with a planet NOT controlled by player1
        planet = Planet("Test Planet", 2, 1)
        planet.controlled_by = "player2"  # Different player controls the planet
        system = System("system1")
        system.planets.append(planet)

        galaxy = Galaxy()
        galaxy.register_system(system)

        game_state = GameState(galaxy=galaxy, players=[player1, player2])

        diplomacy_card = DiplomacyStrategyCard()

        # Execute the primary ability - should fail
        result = diplomacy_card.execute_primary_ability(
            "player1", game_state, system_id="system1"
        )

        assert result.success is False
        assert "does not control any planet" in result.error_message

    def test_diplomacy_primary_ability_requires_system_id(self):
        """Test that Diplomacy primary ability requires a system_id parameter."""
        player1 = Player("player1", Faction.ARBOREC, reinforcements=8)
        game_state = GameState(players=[player1])

        diplomacy_card = DiplomacyStrategyCard()

        # Execute without system_id - should fail
        result = diplomacy_card.execute_primary_ability("player1", game_state)

        assert result.success is False
        assert "System ID must be provided" in result.error_message

    def test_diplomacy_primary_ability_requires_game_state(self):
        """Test that Diplomacy primary ability requires game state."""
        diplomacy_card = DiplomacyStrategyCard()

        # Execute without game_state - should fail
        result = diplomacy_card.execute_primary_ability(
            "player1", None, system_id="system1"
        )

        assert result.success is False
        assert "Game state is required" in result.error_message

    def test_diplomacy_primary_ability_invalid_system(self):
        """Test that Diplomacy primary ability fails with invalid system."""
        player1 = Player("player1", Faction.ARBOREC, reinforcements=8)
        galaxy = Galaxy()
        game_state = GameState(galaxy=galaxy, players=[player1])

        diplomacy_card = DiplomacyStrategyCard()

        # Execute with non-existent system - should fail
        result = diplomacy_card.execute_primary_ability(
            "player1", game_state, system_id="nonexistent"
        )

        assert result.success is False
        assert "System nonexistent not found" in result.error_message


class TestRule32DiplomacySecondaryAbility:
    """Test cases for Rule 32.3 - Diplomacy secondary ability."""

    def test_diplomacy_secondary_ability_ready_planets(self):
        """Test that secondary ability allows players to ready exhausted planets.

        LRR 32.3: Each other player may spend one command token from their strategy
        pool to ready up to two exhausted planets they control.
        """
        # Create player with exhausted planets and strategy pool tokens
        from src.ti4.core.command_sheet import CommandSheet

        command_sheet = CommandSheet(strategy_pool=3)
        player1 = Player("player1", Faction.ARBOREC, command_sheet=command_sheet)

        # Create exhausted planets controlled by player1
        planet1 = Planet("Planet 1", 2, 1)
        planet1.controlled_by = "player1"
        planet1.exhaust()

        planet2 = Planet("Planet 2", 1, 2)
        planet2.controlled_by = "player1"
        planet2.exhaust()

        planet3 = Planet("Planet 3", 3, 0)
        planet3.controlled_by = "player1"
        planet3.exhaust()

        system = System("system1")
        system.planets.extend([planet1, planet2, planet3])

        galaxy = Galaxy()
        galaxy.register_system(system)

        game_state = GameState(galaxy=galaxy, players=[player1])

        diplomacy_card = DiplomacyStrategyCard()

        # Execute secondary ability to ready 2 planets
        result = diplomacy_card.execute_secondary_ability(
            "player1", game_state, planet_ids=["Planet 1", "Planet 2"]
        )

        # Verify the result is successful
        assert result.success is True
        assert result.player_id == "player1"

        # Verify planets are readied
        assert not planet1.is_exhausted()
        assert not planet2.is_exhausted()
        # Third planet should remain exhausted
        assert planet3.is_exhausted()

        # Verify command token was spent from strategy pool
        assert player1.command_sheet.strategy_pool == 2

    def test_diplomacy_secondary_ability_requires_strategy_token(self):
        """Test that secondary ability requires a command token in strategy pool."""
        # Create player with no strategy pool tokens
        from src.ti4.core.command_sheet import CommandSheet

        command_sheet = CommandSheet(strategy_pool=0)
        player1 = Player("player1", Faction.ARBOREC, command_sheet=command_sheet)

        planet = Planet("Planet 1", 2, 1)
        planet.controlled_by = "player1"
        planet.exhaust()

        system = System("system1")
        system.planets.append(planet)

        galaxy = Galaxy()
        galaxy.register_system(system)

        game_state = GameState(galaxy=galaxy, players=[player1])

        diplomacy_card = DiplomacyStrategyCard()

        # Execute secondary ability - should fail due to no strategy tokens
        result = diplomacy_card.execute_secondary_ability(
            "player1", game_state, planet_ids=["Planet 1"]
        )

        assert result.success is False
        assert "no command tokens in strategy pool" in result.error_message

    def test_diplomacy_secondary_ability_max_two_planets(self):
        """Test that secondary ability can ready at most two planets."""
        from src.ti4.core.command_sheet import CommandSheet

        command_sheet = CommandSheet(strategy_pool=3)
        player1 = Player("player1", Faction.ARBOREC, command_sheet=command_sheet)

        # Create three exhausted planets
        planets = []
        for i in range(3):
            planet = Planet(f"Planet {i + 1}", 1, 1)
            planet.controlled_by = "player1"
            planet.exhaust()
            planets.append(planet)

        system = System("system1")
        system.planets.extend(planets)

        galaxy = Galaxy()
        galaxy.register_system(system)

        game_state = GameState(galaxy=galaxy, players=[player1])

        diplomacy_card = DiplomacyStrategyCard()

        # Try to ready 3 planets - should fail
        result = diplomacy_card.execute_secondary_ability(
            "player1", game_state, planet_ids=["Planet 1", "Planet 2", "Planet 3"]
        )

        assert result.success is False
        assert "can ready at most 2 planets" in result.error_message

    def test_diplomacy_secondary_ability_only_controlled_planets(self):
        """Test that secondary ability only readies planets controlled by the player."""
        from src.ti4.core.command_sheet import CommandSheet

        command_sheet1 = CommandSheet(strategy_pool=3)
        command_sheet2 = CommandSheet(strategy_pool=3)
        player1 = Player("player1", Faction.ARBOREC, command_sheet=command_sheet1)
        player2 = Player("player2", Faction.BARONY, command_sheet=command_sheet2)

        # Create planet controlled by different player
        planet = Planet("Planet 1", 2, 1)
        planet.controlled_by = "player2"  # Different player
        planet.exhaust()

        system = System("system1")
        system.planets.append(planet)

        galaxy = Galaxy()
        galaxy.register_system(system)

        game_state = GameState(galaxy=galaxy, players=[player1, player2])

        diplomacy_card = DiplomacyStrategyCard()

        # Try to ready planet not controlled by player1 - should fail
        result = diplomacy_card.execute_secondary_ability(
            "player1", game_state, planet_ids=["Planet 1"]
        )

        assert result.success is False
        assert "does not control planet" in result.error_message


class TestRule32DiplomacyCardProperties:
    """Test cases for Diplomacy strategy card properties."""

    def test_diplomacy_card_type(self):
        """Test that Diplomacy card returns correct type."""
        diplomacy_card = DiplomacyStrategyCard()

        from src.ti4.core.strategy_cards.strategic_action import StrategyCardType

        assert diplomacy_card.get_card_type() == StrategyCardType.DIPLOMACY

    def test_diplomacy_initiative_value(self):
        """Test that Diplomacy card has initiative value 2."""
        diplomacy_card = DiplomacyStrategyCard()

        assert diplomacy_card.get_initiative_value() == 2

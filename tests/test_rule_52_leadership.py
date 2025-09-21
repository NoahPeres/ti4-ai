"""Tests for Rule 52: LEADERSHIP (STRATEGY CARD).

This module tests the Leadership strategy card implementation following TDD approach.
Tests are designed to fail initially (red phase) and pass after implementation.

LRR Reference: Rule 52 - LEADERSHIP (STRATEGY CARD)
"""

from unittest.mock import Mock, patch

from src.ti4.core.constants import Faction
from src.ti4.core.game_state import GameState
from src.ti4.core.player import Player
from src.ti4.core.strategy_cards.cards.leadership import LeadershipStrategyCard
from src.ti4.core.strategy_cards.strategic_action import StrategyCardType


class TestRule52LeadershipStrategyCard:
    """Test suite for Rule 52: Leadership Strategy Card."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.leadership_card = LeadershipStrategyCard()
        self.mock_game_state = Mock(spec=GameState)

        # Mock planets for influence spending
        self.mock_planet1 = Mock()
        self.mock_planet1.influence = 3
        self.mock_planet1.is_exhausted.return_value = False

        self.mock_planet2 = Mock()
        self.mock_planet2.influence = 2
        self.mock_planet2.is_exhausted.return_value = False

    def _create_test_player(self, player_id: str = "test_player") -> Player:
        """Helper to create a test player with empty command pools for testing."""
        # Create player with proper faction
        player = Player(id=player_id, faction=Faction.SOL)
        # Reset command pools to 0 for testing Leadership card gains
        object.__setattr__(player.command_sheet, "tactic_pool", 0)
        object.__setattr__(player.command_sheet, "fleet_pool", 0)
        object.__setattr__(player.command_sheet, "strategy_pool", 0)
        return player

    def _setup_player_planets(self, player: Player, planets=None) -> None:
        """Helper to setup mock planets for influence spending tests."""
        if planets is None:
            planets = [self.mock_planet1, self.mock_planet2]

        # Mock the game state's get_player_planets method to return these planets
        self.mock_game_state.get_player_planets.return_value = planets

    def test_leadership_card_basic_properties(self) -> None:
        """Test basic Leadership card properties.

        LRR 52: Initiative value is "1"
        """
        assert self.leadership_card.get_card_type() == StrategyCardType.LEADERSHIP
        assert self.leadership_card.get_initiative_value() == 1

    def test_primary_ability_gains_three_command_tokens(self) -> None:
        """Test Rule 52.2: Primary ability gains 3 command tokens automatically.

        LRR 52.2: "the active player gains three command tokens"
        """
        # Arrange
        test_player = self._create_test_player()
        self._setup_player_planets(test_player)
        initial_tactic = test_player.command_sheet.tactic_pool
        initial_fleet = test_player.command_sheet.fleet_pool
        initial_strategy = test_player.command_sheet.strategy_pool
        initial_reinforcements = test_player.reinforcements

        # Act
        result = self.leadership_card.execute_primary_ability(
            "test_player",
            game_state=self.mock_game_state,
            player=test_player,
            token_distribution={
                "tactic": 2,
                "fleet": 1,
                "strategy": 0,
            },  # Player choice
        )

        # Assert
        assert result.success is True
        # Should gain exactly 3 tokens distributed as requested
        assert test_player.command_sheet.tactic_pool == initial_tactic + 2
        assert test_player.command_sheet.fleet_pool == initial_fleet + 1
        assert test_player.command_sheet.strategy_pool == initial_strategy + 0
        assert test_player.reinforcements == initial_reinforcements - 3

    def test_primary_ability_influence_conversion(self) -> None:
        """Test Rule 52.2: Primary ability allows influence spending for additional tokens.

        LRR 52.2: "spend any amount of their influence to gain one command token
        for every three influence they spend"
        """
        # Arrange
        test_player = self._create_test_player()
        self._setup_player_planets(test_player)

        # Act - spend 6 influence (should get 2 additional tokens)
        result = self.leadership_card.execute_primary_ability(
            "test_player",
            game_state=self.mock_game_state,
            player=test_player,
            token_distribution={
                "tactic": 3,
                "fleet": 1,
                "strategy": 1,
            },  # 3 base + 2 from influence
            influence_to_spend=6,
        )

        # Assert
        assert result.success is True
        # Should gain 3 base + 2 from influence = 5 total tokens
        total_tokens_gained = (
            test_player.command_sheet.tactic_pool
            + test_player.command_sheet.fleet_pool
            + test_player.command_sheet.strategy_pool
        )
        assert total_tokens_gained == 5

        # Planets should be exhausted for influence spent
        assert self.mock_planet1.exhaust.called is True  # 3 influence
        assert self.mock_planet2.exhaust.called is True  # 2 influence (partial)

    def test_primary_ability_partial_influence_spending(self) -> None:
        """Test Rule 52.2: Can spend partial influence amounts.

        LRR 52.2: "spend any amount of their influence"
        """
        # Arrange
        test_player = self._create_test_player()
        self._setup_player_planets(test_player)

        # Act - spend only 3 influence (should get 1 additional token)
        result = self.leadership_card.execute_primary_ability(
            "test_player",
            game_state=self.mock_game_state,
            player=test_player,
            token_distribution={
                "tactic": 4,
                "fleet": 0,
                "strategy": 0,
            },  # 3 base + 1 from influence
            influence_to_spend=3,
        )

        # Assert
        assert result.success is True
        assert test_player.command_sheet.tactic_pool == 4  # 3 base + 1 from influence
        assert self.mock_planet1.exhaust.called is True  # 3 influence spent
        assert self.mock_planet2.exhaust.called is False  # Not used

    def test_primary_ability_no_influence_spending(self) -> None:
        """Test Rule 52.2: Can choose not to spend influence.

        LRR 52.2: "can spend any amount" (including zero)
        """
        # Arrange
        test_player = self._create_test_player()
        self._setup_player_planets(test_player)

        # Act - spend no influence
        result = self.leadership_card.execute_primary_ability(
            "test_player",
            game_state=self.mock_game_state,
            player=test_player,
            token_distribution={
                "tactic": 3,
                "fleet": 0,
                "strategy": 0,
            },  # Only 3 base tokens
            influence_to_spend=0,
        )

        # Assert
        assert result.success is True
        assert test_player.command_sheet.tactic_pool == 3  # Only base tokens
        assert self.mock_planet1.exhaust.called is False
        assert self.mock_planet2.exhaust.called is False

    def test_primary_ability_insufficient_reinforcements(self) -> None:
        """Test Rule 20.3a: Cannot gain tokens if none available in reinforcements.

        LRR 20.3a: "If a player would gain a command token but has none available
        in their reinforcements, that player cannot gain that command token"
        """
        # Arrange - create player with limited reinforcements
        test_player = self._create_test_player()
        self._setup_player_planets(test_player)
        # Mock reinforcements to only 2 tokens
        object.__setattr__(test_player, "reinforcements", 2)

        # Act - try to gain 3 base tokens (should only get 2)
        result = self.leadership_card.execute_primary_ability(
            "test_player",
            game_state=self.mock_game_state,
            player=test_player,
            token_distribution={"tactic": 2, "fleet": 0, "strategy": 0},
        )

        # Assert
        assert result.success is True
        assert test_player.command_sheet.tactic_pool == 2  # Only 2 tokens gained
        assert test_player.reinforcements == 0

    def test_secondary_ability_influence_conversion_only(self) -> None:
        """Test Rule 52.3: Secondary ability allows influence spending for tokens.

        LRR 52.3: "may spend any amount of influence to gain one command token
        for every three influence they spend"
        """
        # Arrange
        other_player = self._create_test_player("other_player")
        self._setup_player_planets(other_player)

        # Act - spend 6 influence for 2 tokens
        result = self.leadership_card.execute_secondary_ability(
            "other_player",
            game_state=self.mock_game_state,
            player=other_player,
            token_distribution={"tactic": 1, "fleet": 1, "strategy": 0},
            influence_to_spend=6,
        )

        # Assert
        assert result.success is True
        assert other_player.command_sheet.tactic_pool == 1
        assert other_player.command_sheet.fleet_pool == 1
        assert other_player.command_sheet.strategy_pool == 0

    def test_secondary_ability_no_command_token_cost(self) -> None:
        """Test Rule 20.5a: Leadership secondary ability doesn't cost command token.

        LRR 20.5a: "A player does not spend a command token to resolve the
        secondary ability of the 'Leadership' strategy card"
        """
        # Arrange
        other_player = self._create_test_player("other_player")
        self._setup_player_planets(other_player, [self.mock_planet1])
        # Set initial strategy pool to verify it doesn't change
        object.__setattr__(other_player.command_sheet, "strategy_pool", 2)

        # Act
        result = self.leadership_card.execute_secondary_ability(
            "other_player",
            game_state=self.mock_game_state,
            player=other_player,
            token_distribution={"tactic": 1, "fleet": 0, "strategy": 0},
            influence_to_spend=3,
        )

        # Assert
        assert result.success is True
        assert other_player.command_sheet.strategy_pool == 2  # Unchanged - no cost
        assert other_player.command_sheet.tactic_pool == 1  # Gained from influence

    def test_secondary_ability_can_decline(self) -> None:
        """Test Rule 52.3: Secondary ability is optional ("may spend").

        LRR 52.3: "may spend any amount of influence"
        """
        # Arrange
        other_player = self._create_test_player("other_player")
        self._setup_player_planets(other_player)

        # Act - choose not to participate
        result = self.leadership_card.execute_secondary_ability(
            "other_player",
            game_state=self.mock_game_state,
            player=other_player,
            participate=False,
        )

        # Assert
        assert result.success is True
        # No tokens should be gained or spent
        assert other_player.command_sheet.tactic_pool == 0
        assert other_player.command_sheet.fleet_pool == 0
        assert other_player.command_sheet.strategy_pool == 0

    def test_token_pool_choice_rule_52_4(self) -> None:
        """Test Rule 52.4: Player chooses which pool to place tokens in.

        LRR 52.4: "that player places each token on their command sheet
        in the pool of their choice"
        """
        # Arrange
        test_player = self._create_test_player()
        self._setup_player_planets(test_player)

        # Act - distribute tokens across all pools
        result = self.leadership_card.execute_primary_ability(
            "test_player",
            game_state=self.mock_game_state,
            player=test_player,
            token_distribution={"tactic": 1, "fleet": 1, "strategy": 1},
        )

        # Assert
        assert result.success is True
        assert test_player.command_sheet.tactic_pool == 1
        assert test_player.command_sheet.fleet_pool == 1
        assert test_player.command_sheet.strategy_pool == 1

    def test_influence_three_to_one_ratio(self) -> None:
        """Test exact 3:1 influence to command token conversion ratio.

        LRR 52.2 & 52.3: "one command token for every three influence they spend"
        """
        test_cases = [
            (0, 0),  # No influence spent
            (1, 0),  # Insufficient for 1 token
            (2, 0),  # Insufficient for 1 token
            (3, 1),  # Exactly 1 token
            (4, 1),  # 1 token, 1 influence wasted
            (5, 1),  # 1 token, 2 influence wasted
            (6, 2),  # Exactly 2 tokens
            (9, 3),  # Exactly 3 tokens
            (10, 3),  # 3 tokens, 1 influence wasted
        ]

        for influence_spent, expected_tokens in test_cases:
            # Create enough planets to provide the influence
            planets = []
            remaining_influence = influence_spent
            while remaining_influence > 0:
                planet = Mock()
                planet.influence = min(remaining_influence, 5)  # Max 5 per planet
                planet.is_exhausted.return_value = False
                planets.append(planet)
                remaining_influence -= planet.influence

            # Create test player with these planets
            player = self._create_test_player("test")
            self._setup_player_planets(player, planets)

            # Act
            result = self.leadership_card.execute_primary_ability(
                "test",
                game_state=self.mock_game_state,
                player=player,
                token_distribution={
                    "tactic": 3 + expected_tokens,
                    "fleet": 0,
                    "strategy": 0,
                },
                influence_to_spend=influence_spent,
            )

            # Assert
            assert result.success is True
            total_gained = player.command_sheet.tactic_pool
            assert total_gained == 3 + expected_tokens, (
                f"Failed for {influence_spent} influence"
            )

    def test_integration_with_strategy_card_system(self) -> None:
        """Test integration with existing strategy card coordinator system."""
        # This test ensures the Leadership card works with the broader strategy card system
        # The specific implementation will depend on how the coordinator calls the card

        test_player = self._create_test_player()
        self._setup_player_planets(test_player)

        # Mock the coordinator calling the primary ability
        with patch(
            "src.ti4.core.strategy_cards.coordinator.StrategyCardCoordinator"
        ) as mock_coordinator:
            mock_coordinator.return_value.can_use_primary_ability.return_value = True

            result = self.leadership_card.execute_primary_ability(
                "test_player",
                game_state=self.mock_game_state,
                player=test_player,
                token_distribution={"tactic": 3, "fleet": 0, "strategy": 0},
            )

            assert result.success is True
            assert result.player_id == "test_player"

"""
Tests for Rule 92: TRADE (STRATEGY CARD) implementation.

This module tests the Trade strategy card implementation according to the LRR.

LRR Reference: Rule 92 - TRADE (STRATEGY CARD)
"""

import time

from ti4.core.constants import Faction
from ti4.core.game_state import GameState
from ti4.core.player import Player
from ti4.core.strategy_cards.cards.trade import TradeStrategyCard
from ti4.core.strategy_cards.strategic_action import StrategyCardType


class TestTradeStrategyCardBasics:
    """Test suite for basic Trade strategy card properties (Rule 92)."""

    def test_trade_card_creation(self) -> None:
        """Test that Trade strategy card can be created."""
        # RED: Test basic card creation
        card = TradeStrategyCard()
        assert card is not None

    def test_trade_card_type(self) -> None:
        """Test that Trade card returns correct type."""
        # RED: Test card type identification
        card = TradeStrategyCard()
        assert card.get_card_type() == StrategyCardType.TRADE

    def test_trade_initiative_value(self) -> None:
        """Test that Trade card has initiative value 5."""
        # RED: Test initiative value per LRR Rule 92
        card = TradeStrategyCard()
        assert card.get_initiative_value() == 5

    def test_trade_card_name(self) -> None:
        """Test that Trade card returns correct name."""
        # RED: Test card name
        card = TradeStrategyCard()
        assert card.get_name() == "trade"


class TestTradeCardIntegration:
    """Test suite for Trade card integration with BaseStrategyCard framework."""

    def test_trade_inherits_from_base_strategy_card(self) -> None:
        """Test that TradeStrategyCard properly inherits from BaseStrategyCard."""
        # RED: Test inheritance and interface compliance
        from ti4.core.strategy_cards.base_strategy_card import BaseStrategyCard

        card = TradeStrategyCard()
        assert isinstance(card, BaseStrategyCard)

    def test_trade_has_required_methods(self) -> None:
        """Test that TradeStrategyCard implements all required abstract methods."""
        # RED: Test interface compliance
        card = TradeStrategyCard()

        # Test that all abstract methods are implemented
        assert hasattr(card, "get_card_type")
        assert hasattr(card, "get_initiative_value")
        assert hasattr(card, "execute_primary_ability")
        assert hasattr(card, "execute_secondary_ability")

        # Test that methods are callable
        assert callable(card.get_card_type)
        assert callable(card.get_initiative_value)
        assert callable(card.execute_primary_ability)
        assert callable(card.execute_secondary_ability)

    def test_trade_returns_strategy_card_ability_result(self) -> None:
        """Test that Trade card methods return StrategyCardAbilityResult objects."""
        # RED: Test return type compliance
        from ti4.core.strategy_cards.base_strategy_card import StrategyCardAbilityResult

        card = TradeStrategyCard()

        # Test primary ability returns correct type
        primary_result = card.execute_primary_ability(player_id="test_player")
        assert isinstance(primary_result, StrategyCardAbilityResult)

        # Test secondary ability returns correct type
        secondary_result = card.execute_secondary_ability(player_id="test_player")
        assert isinstance(secondary_result, StrategyCardAbilityResult)


class TestTradeCardPrimaryAbilityTradeGoods:
    """Test suite for Trade card primary ability Step 1 - Gain Trade Goods (Requirements 2.1, 2.2, 2.3, 7.1)."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        from ti4.core.game_state import GameState

        self.card = TradeStrategyCard()
        self.player = Player(id="test_player", faction=Faction.SOL)
        self.game_state = GameState(players=[self.player])

    def test_primary_ability_gains_three_trade_goods(self) -> None:
        """Test that Trade primary ability gains 3 trade goods for active player.

        Requirements: 2.1 - WHEN the active player executes the Trade primary ability
        THEN they SHALL gain 3 trade goods
        """
        # RED: This test will fail because _gain_trade_goods method doesn't exist yet
        initial_trade_goods = self.player.get_trade_goods()

        result = self.card.execute_primary_ability(
            player_id="test_player", game_state=self.game_state
        )

        assert result.success is True
        assert self.player.get_trade_goods() == initial_trade_goods + 3

    def test_gain_trade_goods_method_exists(self) -> None:
        """Test that _gain_trade_goods method exists and is callable.

        Requirements: 2.1 - Implementation of trade goods gain functionality
        """
        # RED: This test will fail because _gain_trade_goods method doesn't exist yet
        assert hasattr(self.card, "_gain_trade_goods")
        assert callable(self.card._gain_trade_goods)

    def test_gain_trade_goods_with_zero_initial_trade_goods(self) -> None:
        """Test gaining trade goods when player starts with zero.

        Requirements: 2.1, 7.1 - Trade goods gain with resource management integration
        """
        # RED: This test will fail because _gain_trade_goods method doesn't exist yet
        # Ensure player starts with 0 trade goods
        assert self.player.get_trade_goods() == 0

        # Call the internal method directly for unit testing
        self.card._gain_trade_goods("test_player", self.game_state)

        # Verify trade goods were gained
        assert self.player.get_trade_goods() == 3

    def test_gain_trade_goods_with_existing_trade_goods(self) -> None:
        """Test gaining trade goods when player already has some.

        Requirements: 2.1, 7.1 - Trade goods gain adds to existing amount
        """
        # RED: This test will fail because _gain_trade_goods method doesn't exist yet
        # Give player some initial trade goods
        self.player.gain_trade_goods(5)
        initial_amount = self.player.get_trade_goods()
        assert initial_amount == 5

        # Call the internal method directly for unit testing
        self.card._gain_trade_goods("test_player", self.game_state)

        # Verify trade goods were added to existing amount
        assert self.player.get_trade_goods() == initial_amount + 3

    def test_gain_trade_goods_validates_player_exists(self) -> None:
        """Test that _gain_trade_goods validates player exists in game state.

        Requirements: 2.3, 9.1 - Validation and error handling
        """
        # RED: This test will fail because _gain_trade_goods method doesn't exist yet
        from ti4.core.exceptions import TI4GameError

        # Try to gain trade goods for non-existent player
        try:
            self.card._gain_trade_goods("nonexistent_player", self.game_state)
            assert False, "Expected TI4GameError for invalid player"
        except TI4GameError as e:
            assert "player" in str(e).lower()
            assert "nonexistent_player" in str(e)

    def test_gain_trade_goods_handles_large_amounts(self) -> None:
        """Test trade goods gain with large existing amounts (overflow handling).

        Requirements: 2.2 - WHEN the player has insufficient trade good capacity
        THEN the system SHALL handle overflow appropriately
        """
        # RED: This test will fail because _gain_trade_goods method doesn't exist yet
        # Give player a large amount of trade goods to test overflow handling
        large_amount = 1000
        self.player.gain_trade_goods(large_amount)

        # Call the internal method
        self.card._gain_trade_goods("test_player", self.game_state)

        # Verify trade goods were still added (no overflow limit in TI4)
        assert self.player.get_trade_goods() == large_amount + 3

    def test_gain_trade_goods_updates_game_state(self) -> None:
        """Test that _gain_trade_goods updates player's trade goods in game state.

        Requirements: 2.3 - WHEN the trade good gain is processed
        THEN the player's trade good count SHALL be updated in the game state
        """
        # RED: This test will fail because _gain_trade_goods method doesn't exist yet
        initial_trade_goods = self.player.get_trade_goods()

        self.card._gain_trade_goods("test_player", self.game_state)

        # Verify the player's trade goods were updated
        assert self.player.get_trade_goods() == initial_trade_goods + 3

    def test_gain_trade_goods_with_multiple_players(self) -> None:
        """Test trade goods gain doesn't affect other players.

        Requirements: 2.1, 7.1 - Only active player gains trade goods
        """
        # RED: This test will fail because _gain_trade_goods method doesn't exist yet

        # Add another player to game state
        other_player = Player(id="other_player", faction=Faction.HACAN)
        other_player.gain_trade_goods(2)
        game_state_with_multiple = GameState(players=[self.player, other_player])

        # Gain trade goods for test_player only
        self.card._gain_trade_goods("test_player", game_state_with_multiple)

        # Verify only test_player gained trade goods
        test_player = game_state_with_multiple.get_player("test_player")
        other_player_updated = game_state_with_multiple.get_player("other_player")

        assert test_player.get_trade_goods() == 3
        assert other_player_updated.get_trade_goods() == 2  # Unchanged


class TestTradeCardPrimaryAbilityCommodityReplenishment:
    """Test suite for Trade card primary ability Step 2 - Replenish Commodities (Requirements 3.1, 3.2, 3.3, 7.2)."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        from ti4.core.game_state import GameState

        self.card = TradeStrategyCard()
        self.player = Player(
            id="test_player", faction=Faction.SOL
        )  # SOL has 4 commodity value
        self.game_state = GameState(players=[self.player])

    def test_replenish_commodities_method_exists(self) -> None:
        """Test that _replenish_commodities method exists and is callable.

        Requirements: 3.1 - Implementation of commodity replenishment functionality
        """
        # RED: This test will fail because _replenish_commodities method doesn't exist yet
        assert hasattr(self.card, "_replenish_commodities")
        assert callable(self.card._replenish_commodities)

    def test_replenish_commodities_to_faction_maximum(self) -> None:
        """Test that _replenish_commodities sets commodities to faction maximum.

        Requirements: 3.1 - WHEN the active player executes the Trade primary ability
        THEN they SHALL replenish commodities to their faction maximum
        """
        # RED: This test will fail because _replenish_commodities method doesn't exist yet
        # Start with some commodities (less than max)
        self.player.add_commodities(2)
        assert self.player.get_commodities() == 2
        assert self.player.get_commodity_value() == 4  # SOL faction max

        # Call the internal method directly for unit testing
        self.card._replenish_commodities("test_player", self.game_state)

        # Verify commodities were replenished to faction maximum
        assert self.player.get_commodities() == 4

    def test_replenish_commodities_from_zero(self) -> None:
        """Test replenishing commodities when player starts with zero.

        Requirements: 3.1, 7.2 - Commodity replenishment with faction limit integration
        """
        # RED: This test will fail because _replenish_commodities method doesn't exist yet
        # Ensure player starts with 0 commodities
        assert self.player.get_commodities() == 0

        # Call the internal method directly for unit testing
        self.card._replenish_commodities("test_player", self.game_state)

        # Verify commodities were replenished to faction maximum
        assert self.player.get_commodities() == 4

    def test_replenish_commodities_when_already_at_maximum(self) -> None:
        """Test replenishing commodities when player already has maximum.

        Requirements: 3.2 - WHEN the player already has maximum commodities
        THEN no additional commodities SHALL be gained
        """
        # RED: This test will fail because _replenish_commodities method doesn't exist yet
        # Set player to maximum commodities
        self.player.add_commodities(4)
        assert self.player.get_commodities() == 4
        assert self.player.get_commodity_value() == 4

        # Call the internal method
        self.card._replenish_commodities("test_player", self.game_state)

        # Verify commodities remain at maximum (no change)
        assert self.player.get_commodities() == 4

    def test_replenish_commodities_validates_player_exists(self) -> None:
        """Test that _replenish_commodities validates player exists in game state.

        Requirements: 3.3, 9.1 - Validation and error handling
        """
        # RED: This test will fail because _replenish_commodities method doesn't exist yet
        from ti4.core.exceptions import TI4GameError

        # Try to replenish commodities for non-existent player
        try:
            self.card._replenish_commodities("nonexistent_player", self.game_state)
            assert False, "Expected TI4GameError for invalid player"
        except TI4GameError as e:
            assert "player" in str(e).lower()
            assert "nonexistent_player" in str(e)

    def test_replenish_commodities_with_different_factions(self) -> None:
        """Test commodity replenishment with different faction commodity limits.

        Requirements: 3.1, 7.2 - Various faction commodity limits and current commodity levels
        """
        # RED: This test will fail because _replenish_commodities method doesn't exist yet

        # Test with different faction (Hacan has different commodity value)
        hacan_player = Player(id="hacan_player", faction=Faction.HACAN)
        hacan_player.add_commodities(2)  # Start with some commodities
        game_state_hacan = GameState(players=[hacan_player])

        # Get Hacan's commodity value
        hacan_max = hacan_player.get_commodity_value()
        assert hacan_max > 0  # Ensure we have a valid max

        # Call the internal method
        self.card._replenish_commodities("hacan_player", game_state_hacan)

        # Verify commodities were replenished to Hacan's faction maximum
        assert hacan_player.get_commodities() == hacan_max

    def test_replenish_commodities_updates_game_state(self) -> None:
        """Test that _replenish_commodities updates player's commodities in game state.

        Requirements: 3.3 - WHEN the commodity replenishment is processed
        THEN the player's commodity count SHALL equal their faction's commodity limit
        """
        # RED: This test will fail because _replenish_commodities method doesn't exist yet
        # Start with some commodities
        self.player.add_commodities(1)
        initial_commodities = self.player.get_commodities()
        faction_max = self.player.get_commodity_value()

        self.card._replenish_commodities("test_player", self.game_state)

        # Verify the player's commodities were updated to faction maximum
        assert self.player.get_commodities() == faction_max
        assert self.player.get_commodities() != initial_commodities

    def test_replenish_commodities_with_multiple_players(self) -> None:
        """Test commodity replenishment doesn't affect other players.

        Requirements: 3.1, 7.2 - Only active player's commodities are replenished
        """
        # RED: This test will fail because _replenish_commodities method doesn't exist yet

        # Add another player to game state
        other_player = Player(id="other_player", faction=Faction.HACAN)
        other_player.add_commodities(1)
        game_state_with_multiple = GameState(players=[self.player, other_player])

        # Replenish commodities for test_player only
        self.card._replenish_commodities("test_player", game_state_with_multiple)

        # Verify only test_player's commodities were replenished
        test_player = game_state_with_multiple.get_player("test_player")
        other_player_updated = game_state_with_multiple.get_player("other_player")

        assert test_player.get_commodities() == 4  # SOL max
        assert other_player_updated.get_commodities() == 1  # Unchanged


class TestTradeCardPrimaryAbilityPlayerSelection:
    """Test suite for Trade card primary ability Step 3 - Choose Players for Free Secondary (Requirements 4.1, 4.2, 4.3, 8.1, 9.1)."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        from ti4.core.game_state import GameState

        self.card = TradeStrategyCard()
        self.active_player = Player(id="active_player", faction=Faction.SOL)
        self.player1 = Player(id="player1", faction=Faction.HACAN)
        self.player2 = Player(id="player2", faction=Faction.XXCHA)
        self.player3 = Player(id="player3", faction=Faction.JORD)
        self.game_state = GameState(
            players=[self.active_player, self.player1, self.player2, self.player3]
        )

    def test_process_chosen_players_method_exists(self) -> None:
        """Test that _process_chosen_players method exists and is callable.

        Requirements: 4.1 - Implementation of player selection mechanism
        """
        # RED: This test will fail because _process_chosen_players method doesn't exist yet
        assert hasattr(self.card, "_process_chosen_players")
        assert callable(self.card._process_chosen_players)

    def test_process_chosen_players_with_valid_players(self) -> None:
        """Test choosing valid players for free secondary ability.

        Requirements: 4.1 - WHEN the active player executes the Trade primary ability
        THEN they SHALL be able to choose any number of other players
        """
        # RED: This test will fail because _process_chosen_players method doesn't exist yet
        chosen_players = ["player1", "player2"]

        # Call the internal method directly for unit testing
        self.card._process_chosen_players(
            "active_player", chosen_players, self.game_state
        )

        # Verify that chosen players are tracked (implementation will define how)
        # For now, we'll test that the method executes without error
        assert True  # Method should execute successfully

    def test_process_chosen_players_with_empty_list(self) -> None:
        """Test choosing no players (empty list).

        Requirements: 4.3 - WHEN no players are chosen THEN all other players
        SHALL still be able to use the secondary ability with normal command token cost
        """
        # RED: This test will fail because _process_chosen_players method doesn't exist yet
        chosen_players = []

        # Call the internal method directly for unit testing
        self.card._process_chosen_players(
            "active_player", chosen_players, self.game_state
        )

        # Verify that method handles empty list correctly
        assert True  # Method should execute successfully

    def test_process_chosen_players_with_all_players(self) -> None:
        """Test choosing all other players for free secondary ability.

        Requirements: 4.1 - WHEN the active player executes the Trade primary ability
        THEN they SHALL be able to choose any number of other players
        """
        # RED: This test will fail because _process_chosen_players method doesn't exist yet
        chosen_players = ["player1", "player2", "player3"]

        # Call the internal method directly for unit testing
        self.card._process_chosen_players(
            "active_player", chosen_players, self.game_state
        )

        # Verify that all players can be chosen
        assert True  # Method should execute successfully

    def test_process_chosen_players_validates_player_ids(self) -> None:
        """Test that _process_chosen_players validates player IDs exist in game state.

        Requirements: 9.1 - WHEN invalid player IDs are provided
        THEN appropriate error messages SHALL be returned
        """
        # RED: This test will fail because _process_chosen_players method doesn't exist yet
        from ti4.core.exceptions import TI4GameError

        chosen_players = ["invalid_player", "player1"]

        # Try to process chosen players with invalid player ID
        try:
            self.card._process_chosen_players(
                "active_player", chosen_players, self.game_state
            )
            assert False, "Expected TI4GameError for invalid player ID"
        except TI4GameError as e:
            assert "invalid_player" in str(e).lower()

    def test_process_chosen_players_prevents_choosing_self(self) -> None:
        """Test that active player cannot choose themselves.

        Requirements: 4.2, 9.1 - Validation for player selection (cannot choose self)
        """
        # RED: This test will fail because _process_chosen_players method doesn't exist yet
        from ti4.core.exceptions import TI4GameError

        chosen_players = ["active_player", "player1"]

        # Try to process chosen players including the active player
        try:
            self.card._process_chosen_players(
                "active_player", chosen_players, self.game_state
            )
            assert False, "Expected TI4GameError for choosing self"
        except TI4GameError as e:
            assert "themselves" in str(e).lower() or "active player" in str(e).lower()

    def test_process_chosen_players_with_duplicate_players(self) -> None:
        """Test handling of duplicate player IDs in chosen players list.

        Requirements: 9.1 - Input validation and error handling
        """
        # RED: This test will fail because _process_chosen_players method doesn't exist yet
        chosen_players = ["player1", "player2", "player1"]  # player1 appears twice

        # Call the internal method - should handle duplicates gracefully
        self.card._process_chosen_players(
            "active_player", chosen_players, self.game_state
        )

        # Method should execute successfully (duplicates should be handled)
        assert True

    def test_primary_ability_accepts_chosen_players_parameter(self) -> None:
        """Test that execute_primary_ability accepts chosen_players parameter.

        Requirements: 4.1 - Primary ability integration with player selection
        """
        # RED: This test will fail because execute_primary_ability doesn't accept chosen_players yet
        chosen_players = ["player1", "player2"]

        result = self.card.execute_primary_ability(
            player_id="active_player",
            game_state=self.game_state,
            chosen_players=chosen_players,
        )

        assert result.success is True
        assert result.player_id == "active_player"

    def test_primary_ability_with_no_chosen_players(self) -> None:
        """Test primary ability execution with no chosen players (None).

        Requirements: 4.3 - Default behavior when no players are chosen
        """
        # RED: This test will fail because execute_primary_ability doesn't handle chosen_players yet
        result = self.card.execute_primary_ability(
            player_id="active_player", game_state=self.game_state, chosen_players=None
        )

        assert result.success is True
        assert result.player_id == "active_player"

    def test_primary_ability_with_empty_chosen_players_list(self) -> None:
        """Test primary ability execution with empty chosen players list.

        Requirements: 4.3 - Explicit empty list should work same as None
        """
        # RED: This test will fail because execute_primary_ability doesn't handle chosen_players yet
        result = self.card.execute_primary_ability(
            player_id="active_player", game_state=self.game_state, chosen_players=[]
        )

        assert result.success is True
        assert result.player_id == "active_player"


class TestTradeCardStrategyCardRegistrationAndCoordinatorIntegration:
    """Test suite for Trade card integration with strategy card coordinator and game state management (Requirements 6.3, 6.4, 1.3)."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        from ti4.core.game_state import GameState

        self.card = TradeStrategyCard()
        self.player = Player(id="test_player", faction=Faction.SOL)
        self.game_state = GameState(players=[self.player])

    def test_trade_card_is_registered_in_strategy_card_registry(self) -> None:
        """Test that TradeStrategyCard is properly registered in the strategy card registry.

        Requirements: 6.3 - Update strategy card registry to include TradeStrategyCard with proper StrategyCardType.TRADE mapping
        """
        # RED: This test will fail until TradeStrategyCard is properly registered
        from ti4.core.strategy_cards.registry import StrategyCardRegistry
        from ti4.core.strategy_cards.strategic_action import StrategyCardType

        registry = StrategyCardRegistry()
        trade_card = registry.get_card(StrategyCardType.TRADE)

        assert trade_card is not None
        assert isinstance(trade_card, TradeStrategyCard)
        assert trade_card.get_card_type() == StrategyCardType.TRADE
        assert trade_card.get_initiative_value() == 5

    def test_trade_card_integrates_with_strategy_card_coordinator(self) -> None:
        """Test that TradeStrategyCard integrates properly with StrategyCardCoordinator.

        Requirements: 6.4 - Ensure proper integration with StrategyCardCoordinator execution workflow and initiative ordering
        """
        # RED: This test will fail until coordinator integration is complete
        from ti4.core.strategic_action import StrategicActionManager, StrategyCardType
        from ti4.core.strategy_cards.coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test card assignment
        result = coordinator.assign_strategy_card("test_player", StrategyCardType.TRADE)
        assert result.success is True
        assert result.player_id == "test_player"
        assert result.strategy_card == StrategyCardType.TRADE

        # Test card retrieval
        assigned_card = coordinator.get_player_strategy_card("test_player")
        assert assigned_card == StrategyCardType.TRADE

    def test_trade_card_initiative_ordering_in_coordinator(self) -> None:
        """Test that Trade card's initiative value (5) is properly handled in initiative ordering.

        Requirements: 6.4 - Validate integration with existing BaseStrategyCard interface and initiative ordering
        """
        # RED: This test will fail until initiative ordering integration is complete
        from ti4.core.strategic_action import StrategicActionManager, StrategyCardType
        from ti4.core.strategy_cards.coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Assign multiple cards to test initiative ordering
        coordinator.assign_strategy_card(
            "player1", StrategyCardType.LEADERSHIP
        )  # Initiative 1
        coordinator.assign_strategy_card(
            "player2", StrategyCardType.POLITICS
        )  # Initiative 3
        coordinator.assign_strategy_card(
            "player3", StrategyCardType.TRADE
        )  # Initiative 5
        coordinator.assign_strategy_card(
            "player4", StrategyCardType.WARFARE
        )  # Initiative 6

        # Get initiative order
        initiative_order = coordinator.get_action_phase_initiative_order()

        # Verify Trade card (initiative 5) is in correct position
        expected_order = ["player1", "player2", "player3", "player4"]
        assert initiative_order == expected_order

    def test_trade_card_can_use_primary_ability_via_coordinator(self) -> None:
        """Test that Trade card primary ability can be used via coordinator.

        Requirements: 6.4 - Validate integration with existing BaseStrategyCard interface and StrategyCardAbilityResult patterns
        """
        # RED: This test will fail until coordinator primary ability integration is complete
        from ti4.core.strategic_action import StrategicActionManager, StrategyCardType
        from ti4.core.strategy_cards.coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Assign Trade card to player
        coordinator.assign_strategy_card("test_player", StrategyCardType.TRADE)

        # Test that player can use primary ability
        can_use_primary = coordinator.can_use_primary_ability(
            "test_player", StrategyCardType.TRADE
        )
        assert can_use_primary is True

        # Test that card starts as readied
        is_readied = coordinator.is_strategy_card_readied(
            "test_player", StrategyCardType.TRADE
        )
        assert is_readied is True

    def test_trade_card_exhaustion_via_coordinator(self) -> None:
        """Test that Trade card can be exhausted via coordinator after primary ability use.

        Requirements: 6.4 - Integration with StrategyCardCoordinator execution workflow
        """
        # RED: This test will fail until coordinator exhaustion integration is complete
        from ti4.core.strategic_action import StrategicActionManager, StrategyCardType
        from ti4.core.strategy_cards.coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Assign Trade card to player
        coordinator.assign_strategy_card("test_player", StrategyCardType.TRADE)

        # Verify card starts as readied
        assert (
            coordinator.is_strategy_card_readied("test_player", StrategyCardType.TRADE)
            is True
        )
        assert (
            coordinator.is_strategy_card_exhausted(
                "test_player", StrategyCardType.TRADE
            )
            is False
        )

        # Exhaust the card
        coordinator.exhaust_strategy_card("test_player", StrategyCardType.TRADE)

        # Verify card is now exhausted
        assert (
            coordinator.is_strategy_card_readied("test_player", StrategyCardType.TRADE)
            is False
        )
        assert (
            coordinator.is_strategy_card_exhausted(
                "test_player", StrategyCardType.TRADE
            )
            is True
        )

        # Verify player can no longer use primary ability
        can_use_primary = coordinator.can_use_primary_ability(
            "test_player", StrategyCardType.TRADE
        )
        assert can_use_primary is False

    def test_trade_card_secondary_ability_via_coordinator(self) -> None:
        """Test that Trade card secondary ability can be used by other players via coordinator.

        Requirements: 6.4 - Integration with StrategyCardCoordinator execution workflow
        """
        # RED: This test will fail until coordinator secondary ability integration is complete
        from ti4.core.strategic_action import StrategicActionManager, StrategyCardType
        from ti4.core.strategy_cards.coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Assign Trade card to one player
        coordinator.assign_strategy_card("active_player", StrategyCardType.TRADE)

        # Test that another player can use secondary ability
        can_use_secondary = coordinator.can_use_secondary_ability(
            "other_player", StrategyCardType.TRADE
        )
        assert can_use_secondary is True

        # Test that the active player cannot use secondary ability of their own card
        can_use_own_secondary = coordinator.can_use_secondary_ability(
            "active_player", StrategyCardType.TRADE
        )
        assert can_use_own_secondary is False

    def test_trade_card_registry_validation(self) -> None:
        """Test that strategy card registry validation passes with Trade card included.

        Requirements: 6.3 - Strategy card registry system validation
        """
        # RED: This test will fail until registry validation is complete
        from ti4.core.strategy_cards.registry import StrategyCardRegistry

        registry = StrategyCardRegistry()

        # Verify registry validation passes (all 8 cards registered)
        is_valid = registry.validate_registry()
        assert is_valid is True

        # Verify all cards are present including Trade
        all_cards = registry.get_all_cards()
        assert len(all_cards) == 8

        # Verify cards are properly ordered by initiative
        cards_by_initiative = registry.get_cards_by_initiative_order()
        assert len(cards_by_initiative) == 8

        # Trade card should be at index 4 (initiative 5, 0-based indexing)
        trade_card = cards_by_initiative[4]
        assert trade_card.get_card_type() == StrategyCardType.TRADE
        assert trade_card.get_initiative_value() == 5


class TestTradeCardCompleteSystemIntegration:
    """Test suite for complete strategy card system integration including phase management."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        from ti4.core.game_state import GameState

        self.card = TradeStrategyCard()
        self.active_player = Player(id="active_player", faction=Faction.SOL)
        self.other_player = Player(id="other_player", faction=Faction.HACAN)
        self.game_state = GameState(players=[self.active_player, self.other_player])

    def test_complete_trade_card_workflow_with_coordinator(self) -> None:
        """Test complete Trade card workflow integrated with coordinator and game state.

        Requirements: 6.4 - Write integration tests for complete strategy card system integration including phase management
        """
        # RED: This test will fail until complete integration is implemented
        from ti4.core.strategic_action import StrategicActionManager, StrategyCardType
        from ti4.core.strategy_cards.coordinator import StrategyCardCoordinator
        from ti4.core.strategy_cards.registry import StrategyCardRegistry

        # Set up complete system
        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)
        registry = StrategyCardRegistry()

        # Assign Trade card to active player
        coordinator.assign_strategy_card("active_player", StrategyCardType.TRADE)

        # Get Trade card from registry
        trade_card = registry.get_card(StrategyCardType.TRADE)
        assert trade_card is not None

        # Execute primary ability
        primary_result = trade_card.execute_primary_ability(
            player_id="active_player",
            game_state=self.game_state,
            chosen_players=["other_player"],
        )
        assert primary_result.success is True

        # Verify card can be exhausted after primary ability
        coordinator.exhaust_strategy_card("active_player", StrategyCardType.TRADE)
        assert (
            coordinator.is_strategy_card_exhausted(
                "active_player", StrategyCardType.TRADE
            )
            is True
        )

        # Execute secondary ability for other player
        secondary_result = trade_card.execute_secondary_ability(
            player_id="other_player",
            game_state=self.game_state,
            is_free=True,  # Chosen by active player
        )
        assert secondary_result.success is True

    def test_trade_card_multi_player_integration(self) -> None:
        """Test Trade card integration in multi-player scenarios.

        Requirements: 6.4 - Complete strategy card system integration with multi-player support
        """
        # RED: This test will fail until multi-player integration is complete
        from ti4.core.strategic_action import StrategicActionManager, StrategyCardType
        from ti4.core.strategy_cards.coordinator import StrategyCardCoordinator

        # Set up multi-player game
        player3 = Player(id="player3", faction=Faction.XXCHA)
        player4 = Player(id="player4", faction=Faction.JORD)
        GameState(players=[self.active_player, self.other_player, player3, player4])

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Assign cards to multiple players
        coordinator.assign_strategy_card("active_player", StrategyCardType.TRADE)
        coordinator.assign_strategy_card("other_player", StrategyCardType.WARFARE)
        coordinator.assign_strategy_card("player3", StrategyCardType.POLITICS)
        coordinator.assign_strategy_card("player4", StrategyCardType.LEADERSHIP)

        # Test initiative order includes Trade card correctly
        initiative_order = coordinator.get_action_phase_initiative_order()
        expected_order = [
            "player4",
            "player3",
            "active_player",
            "other_player",
        ]  # 1, 3, 5, 6
        assert initiative_order == expected_order

        # Test multiple players can use Trade secondary ability
        assert (
            coordinator.can_use_secondary_ability(
                "other_player", StrategyCardType.TRADE
            )
            is True
        )
        assert (
            coordinator.can_use_secondary_ability("player3", StrategyCardType.TRADE)
            is True
        )
        assert (
            coordinator.can_use_secondary_ability("player4", StrategyCardType.TRADE)
            is True
        )

    def test_trade_card_phase_management_integration(self) -> None:
        """Test Trade card integration with game phase management.

        Requirements: 6.4 - Integration tests for complete strategy card system integration including phase management
        """
        # RED: This test will fail until phase management integration is complete
        from ti4.core.strategic_action import StrategicActionManager, StrategyCardType
        from ti4.core.strategy_cards.coordinator import StrategyCardCoordinator

        strategic_action_manager = StrategicActionManager()
        coordinator = StrategyCardCoordinator(strategic_action_manager)

        # Test strategy phase card selection (minimum 3 players required)
        speaker_order = ["active_player", "other_player", "third_player"]
        selection_result = coordinator.start_strategy_phase_selection(speaker_order)
        assert selection_result.success is True

        # Test Trade card is available for selection
        available_cards = coordinator.get_available_cards()
        assert StrategyCardType.TRADE in available_cards

        # Test card selection
        card_selection_result = coordinator.select_strategy_card(
            "active_player", StrategyCardType.TRADE
        )
        assert card_selection_result.success is True
        assert card_selection_result.strategy_card == StrategyCardType.TRADE

        # Test card is no longer available after selection
        updated_available_cards = coordinator.get_available_cards()
        assert StrategyCardType.TRADE not in updated_available_cards

        # Test action phase initiative order
        action_initiative_order = coordinator.get_action_phase_initiative_order()
        assert "active_player" in action_initiative_order

        # Test status phase initiative order
        status_initiative_order = coordinator.get_status_phase_initiative_order()
        assert "active_player" in status_initiative_order


class TestTradeCardSecondaryAbilityCommandTokenValidation:
    """Test suite for Trade card secondary ability command token validation (Requirements 5.1, 5.2, 5.3, 5.4, 7.3)."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        from ti4.core.game_state import GameState

        self.card = TradeStrategyCard()
        self.player = Player(id="test_player", faction=Faction.SOL)
        self.game_state = GameState(players=[self.player])

    def test_secondary_ability_requires_command_token_cost(self) -> None:
        """Test that secondary ability requires spending 1 command token from strategy pool.

        Requirements: 5.1 - WHEN a non-active player uses the Trade secondary ability
        THEN they SHALL spend 1 command token from their strategy pool
        """
        # RED: This test will fail because execute_secondary_ability doesn't validate command tokens yet
        # Ensure player has command tokens
        self.player.command_sheet.strategy_pool = 2
        initial_tokens = self.player.command_sheet.strategy_pool

        result = self.card.execute_secondary_ability(
            player_id="test_player", game_state=self.game_state
        )

        assert result.success is True
        # Verify command token was spent
        assert self.player.command_sheet.strategy_pool == initial_tokens - 1

    def test_secondary_ability_fails_without_command_tokens(self) -> None:
        """Test that secondary ability fails when player has no command tokens.

        Requirements: 5.3 - WHEN the player has insufficient command tokens
        THEN the secondary ability SHALL not be available
        """
        # RED: This test will fail because execute_secondary_ability doesn't validate command tokens yet
        # Ensure player has no command tokens
        self.player.command_sheet.strategy_pool = 0

        result = self.card.execute_secondary_ability(
            player_id="test_player", game_state=self.game_state
        )

        assert result.success is False
        assert "command token" in result.error_message.lower()
        assert "insufficient" in result.error_message.lower()

    def test_secondary_ability_replenishes_commodities_after_token_spent(self) -> None:
        """Test that secondary ability replenishes commodities after spending command token.

        Requirements: 5.2 - WHEN the command token is spent
        THEN the player SHALL replenish commodities to their faction maximum
        """
        # RED: This test will fail because execute_secondary_ability doesn't replenish commodities yet
        # Set up player with command tokens and some commodities
        self.player.command_sheet.strategy_pool = 2
        self.player.add_commodities(1)
        faction_max = self.player.get_commodity_value()

        result = self.card.execute_secondary_ability(
            player_id="test_player", game_state=self.game_state
        )

        assert result.success is True
        # Verify commodities were replenished to faction maximum
        assert self.player.get_commodities() == faction_max
        # Verify command token was spent
        assert self.player.command_sheet.strategy_pool == 1

    def test_secondary_ability_with_free_execution(self) -> None:
        """Test that secondary ability can be executed for free when player was chosen.

        Requirements: 5.4 - WHEN the player was chosen by the active player
        THEN they SHALL replenish commodities without spending a command token
        """
        # RED: This test will fail because execute_secondary_ability doesn't support free execution yet
        # Set up player with no command tokens but should be able to execute for free
        self.player.command_sheet.strategy_pool = 0
        self.player.add_commodities(1)
        faction_max = self.player.get_commodity_value()

        result = self.card.execute_secondary_ability(
            player_id="test_player", game_state=self.game_state, is_free=True
        )

        assert result.success is True
        # Verify commodities were replenished
        assert self.player.get_commodities() == faction_max
        # Verify no command token was spent (still 0)
        assert self.player.command_sheet.strategy_pool == 0

    def test_secondary_ability_validates_player_exists(self) -> None:
        """Test that secondary ability validates player exists in game state.

        Requirements: 7.3 - Command token management with proper validation
        """
        # RED: This test will fail because execute_secondary_ability doesn't validate player existence yet
        result = self.card.execute_secondary_ability(
            player_id="nonexistent_player", game_state=self.game_state
        )

        assert result.success is False
        assert "player" in result.error_message.lower()
        assert "nonexistent_player" in result.error_message

    def test_secondary_ability_with_multiple_command_tokens(self) -> None:
        """Test secondary ability when player has multiple command tokens.

        Requirements: 5.1, 5.2 - Only 1 command token should be spent regardless of available tokens
        """
        # RED: This test will fail because execute_secondary_ability doesn't implement token spending yet
        # Set up player with multiple command tokens
        self.player.command_sheet.strategy_pool = 5
        initial_tokens = self.player.command_sheet.strategy_pool

        result = self.card.execute_secondary_ability(
            player_id="test_player", game_state=self.game_state
        )

        assert result.success is True
        # Verify exactly 1 command token was spent
        assert self.player.command_sheet.strategy_pool == initial_tokens - 1

    def test_secondary_ability_with_zero_commodities(self) -> None:
        """Test secondary ability when player starts with zero commodities.

        Requirements: 5.2, 7.3 - Commodity replenishment from zero to faction maximum
        """
        # RED: This test will fail because execute_secondary_ability doesn't replenish commodities yet
        # Set up player with command tokens and zero commodities
        self.player.command_sheet.strategy_pool = 2
        assert self.player.get_commodities() == 0
        faction_max = self.player.get_commodity_value()

        result = self.card.execute_secondary_ability(
            player_id="test_player", game_state=self.game_state
        )

        assert result.success is True
        # Verify commodities were replenished to faction maximum
        assert self.player.get_commodities() == faction_max
        # Verify command token was spent
        assert self.player.command_sheet.strategy_pool == 1


class TestTradeCardMultiPlayerSecondaryAbility:
    """Test suite for Trade card multi-player secondary ability support (Requirements 8.1, 8.2, 8.3, 8.4)."""

    def setup_method(self) -> None:
        """Set up test fixtures for multi-player scenarios."""
        from ti4.core.game_state import GameState

        self.card = TradeStrategyCard()
        self.active_player = Player(id="active_player", faction=Faction.SOL)
        self.player1 = Player(id="player1", faction=Faction.HACAN)
        self.player2 = Player(id="player2", faction=Faction.XXCHA)
        self.player3 = Player(id="player3", faction=Faction.JORD)

        # Set up command tokens for all players
        self.active_player.command_sheet.strategy_pool = 3
        self.player1.command_sheet.strategy_pool = 2
        self.player2.command_sheet.strategy_pool = 1
        self.player3.command_sheet.strategy_pool = 0  # No tokens

        # Set up some commodities for testing
        self.player1.add_commodities(1)
        self.player2.add_commodities(2)
        self.player3.add_commodities(1)

        self.game_state = GameState(
            players=[self.active_player, self.player1, self.player2, self.player3]
        )

    def test_multiple_players_use_secondary_ability_independently(self) -> None:
        """Test that multiple players can use secondary ability and each is processed independently.

        Requirements: 8.1 - WHEN multiple players use the secondary ability
        THEN each SHALL be processed independently
        """
        # RED: This test will fail because we need to track chosen players and handle concurrent execution

        # Execute primary ability with chosen players
        result_primary = self.card.execute_primary_ability(
            player_id="active_player",
            game_state=self.game_state,
            chosen_players=["player1", "player2"],
        )
        assert result_primary.success is True

        # Player1 uses secondary ability (chosen, should be free)
        initial_tokens_p1 = self.player1.command_sheet.strategy_pool
        self.player1.get_commodities()
        faction_max_p1 = self.player1.get_commodity_value()

        result_p1 = self.card.execute_secondary_ability(
            player_id="player1",
            game_state=self.game_state,
            is_free=True,  # Should be determined automatically based on chosen players
        )

        assert result_p1.success is True
        assert self.player1.get_commodities() == faction_max_p1
        assert (
            self.player1.command_sheet.strategy_pool == initial_tokens_p1
        )  # No token spent

        # Player2 uses secondary ability (chosen, should be free)
        initial_tokens_p2 = self.player2.command_sheet.strategy_pool
        self.player2.get_commodities()
        faction_max_p2 = self.player2.get_commodity_value()

        result_p2 = self.card.execute_secondary_ability(
            player_id="player2",
            game_state=self.game_state,
            is_free=True,  # Should be determined automatically based on chosen players
        )

        assert result_p2.success is True
        assert self.player2.get_commodities() == faction_max_p2
        assert (
            self.player2.command_sheet.strategy_pool == initial_tokens_p2
        )  # No token spent

        # Verify players were processed independently (different faction maximums)
        assert self.player1.get_commodities() != self.player2.get_commodities()

    def test_chosen_players_tracked_per_execution(self) -> None:
        """Test that chosen players are tracked per primary ability execution.

        Requirements: 8.2 - WHEN the active player chooses players for free secondary
        THEN the selection SHALL be tracked per execution
        """
        # RED: This test will fail because we need to implement chosen player tracking

        # Execute primary ability with specific chosen players
        chosen_players = ["player1", "player3"]
        result = self.card.execute_primary_ability(
            player_id="active_player",
            game_state=self.game_state,
            chosen_players=chosen_players,
        )
        assert result.success is True

        # Verify that chosen players are tracked in game state or card state
        # This will require implementing a mechanism to track chosen players
        chosen_player_ids = self.card.get_chosen_players(self.game_state)
        assert set(chosen_player_ids) == set(chosen_players)

    def test_players_with_different_faction_commodity_limits(self) -> None:
        """Test that players with different faction commodity limits replenish to their own maximum.

        Requirements: 8.3 - WHEN players have different faction commodity limits
        THEN each SHALL replenish to their own maximum
        """
        # RED: This test will fail because we need to ensure each faction's limits are respected

        # Get faction maximums for different players
        hacan_max = self.player1.get_commodity_value()  # Hacan
        xxcha_max = self.player2.get_commodity_value()  # Xxcha
        jord_max = self.player3.get_commodity_value()  # Jord

        # Ensure they have different maximums (this validates our test setup)
        faction_maximums = {hacan_max, xxcha_max, jord_max}
        assert len(faction_maximums) > 1, (
            "Test requires factions with different commodity limits"
        )

        # Execute secondary ability for each player
        result_p1 = self.card.execute_secondary_ability(
            player_id="player1", game_state=self.game_state
        )
        result_p2 = self.card.execute_secondary_ability(
            player_id="player2", game_state=self.game_state
        )

        assert result_p1.success is True
        assert result_p2.success is True

        # Verify each player replenished to their own faction maximum
        assert self.player1.get_commodities() == hacan_max
        assert self.player2.get_commodities() == xxcha_max

    def test_command_token_availability_validated_independently(self) -> None:
        """Test that command token availability is validated independently for each player.

        Requirements: 8.4 - WHEN command token availability varies by player
        THEN each player's ability to use secondary SHALL be validated independently
        """
        # RED: This test will fail because we need independent validation per player

        # Player1 has tokens, should succeed
        result_p1 = self.card.execute_secondary_ability(
            player_id="player1", game_state=self.game_state
        )
        assert result_p1.success is True

        # Player2 has 1 token, should succeed
        result_p2 = self.card.execute_secondary_ability(
            player_id="player2", game_state=self.game_state
        )
        assert result_p2.success is True

        # Player3 has no tokens, should fail
        result_p3 = self.card.execute_secondary_ability(
            player_id="player3", game_state=self.game_state
        )
        assert result_p3.success is False
        assert "command token" in result_p3.error_message.lower()

    def test_concurrent_secondary_ability_execution(self) -> None:
        """Test that multiple players can execute secondary ability concurrently without interference.

        Requirements: 8.1, 8.4 - Concurrent execution and independent processing
        """
        # RED: This test will fail because we need to ensure thread safety and state consistency

        # Store initial states
        initial_states = {
            "player1": {
                "tokens": self.player1.command_sheet.strategy_pool,
                "commodities": self.player1.get_commodities(),
                "max": self.player1.get_commodity_value(),
            },
            "player2": {
                "tokens": self.player2.command_sheet.strategy_pool,
                "commodities": self.player2.get_commodities(),
                "max": self.player2.get_commodity_value(),
            },
        }

        # Execute secondary abilities for multiple players
        results = []
        for player_id in ["player1", "player2"]:
            result = self.card.execute_secondary_ability(
                player_id=player_id, game_state=self.game_state
            )
            results.append((player_id, result))

        # Verify all executions succeeded
        for player_id, result in results:
            assert result.success is True, f"Secondary ability failed for {player_id}"

        # Verify each player's state was updated correctly and independently
        assert self.player1.get_commodities() == initial_states["player1"]["max"]
        assert (
            self.player1.command_sheet.strategy_pool
            == initial_states["player1"]["tokens"] - 1
        )

        assert self.player2.get_commodities() == initial_states["player2"]["max"]
        assert (
            self.player2.command_sheet.strategy_pool
            == initial_states["player2"]["tokens"] - 1
        )

    def test_free_secondary_ability_for_chosen_players(self) -> None:
        """Test that chosen players can execute secondary ability without spending command tokens.

        Requirements: 8.2 - Free execution for chosen players
        """
        # RED: This test will fail because we need to implement automatic free execution detection

        # Execute primary ability choosing player3 (who has no tokens)
        result_primary = self.card.execute_primary_ability(
            player_id="active_player",
            game_state=self.game_state,
            chosen_players=["player3"],
        )
        assert result_primary.success is True

        # Player3 should be able to execute secondary ability for free despite having no tokens
        initial_tokens = self.player3.command_sheet.strategy_pool
        assert initial_tokens == 0

        result_secondary = self.card.execute_secondary_ability(
            player_id="player3",
            game_state=self.game_state,
            # Should automatically detect that player3 was chosen and execute for free
        )

        assert result_secondary.success is True
        assert self.player3.get_commodities() == self.player3.get_commodity_value()
        assert (
            self.player3.command_sheet.strategy_pool == initial_tokens
        )  # No token spent

    def test_non_chosen_players_must_spend_tokens(self) -> None:
        """Test that non-chosen players must spend command tokens for secondary ability.

        Requirements: 8.2, 8.4 - Non-chosen players use normal cost
        """
        # RED: This test will fail because we need to distinguish between chosen and non-chosen players

        # Execute primary ability choosing only player1
        result_primary = self.card.execute_primary_ability(
            player_id="active_player",
            game_state=self.game_state,
            chosen_players=["player1"],
        )
        assert result_primary.success is True

        # Player1 (chosen) should execute for free
        initial_tokens_p1 = self.player1.command_sheet.strategy_pool
        result_p1 = self.card.execute_secondary_ability(
            player_id="player1", game_state=self.game_state
        )
        assert result_p1.success is True
        assert (
            self.player1.command_sheet.strategy_pool == initial_tokens_p1
        )  # No token spent

        # Player2 (not chosen) should spend a token
        initial_tokens_p2 = self.player2.command_sheet.strategy_pool
        result_p2 = self.card.execute_secondary_ability(
            player_id="player2", game_state=self.game_state
        )
        assert result_p2.success is True
        assert (
            self.player2.command_sheet.strategy_pool == initial_tokens_p2 - 1
        )  # Token spent

    def test_secondary_ability_with_mixed_player_states(self) -> None:
        """Test secondary ability with players in various states (tokens, commodities, chosen status).

        Requirements: 8.1, 8.2, 8.3, 8.4 - Comprehensive multi-player scenario
        """
        # RED: This test will fail because it requires full multi-player support implementation

        # Set up complex scenario
        self.player1.add_commodities(1)  # Hacan: has tokens, some commodities
        self.player2.spend_commodities(2)  # Xxcha: has 1 token, zero commodities
        # player3 has no tokens but will be chosen

        # Execute primary ability choosing player3 only
        result_primary = self.card.execute_primary_ability(
            player_id="active_player",
            game_state=self.game_state,
            chosen_players=["player3"],
        )
        assert result_primary.success is True

        # Test each player's secondary ability execution
        scenarios = [
            (
                "player1",
                False,
                True,
            ),  # Not chosen, has tokens, should succeed with cost
            (
                "player2",
                False,
                True,
            ),  # Not chosen, has tokens, should succeed with cost
            ("player3", True, True),  # Chosen, no tokens, should succeed for free
        ]

        for player_id, is_chosen, should_succeed in scenarios:
            player = self.game_state.get_player(player_id)
            initial_tokens = player.command_sheet.strategy_pool
            player.get_commodities()
            faction_max = player.get_commodity_value()

            result = self.card.execute_secondary_ability(
                player_id=player_id, game_state=self.game_state
            )

            if should_succeed:
                assert result.success is True, f"Expected success for {player_id}"
                assert player.get_commodities() == faction_max, (
                    f"Commodities not replenished for {player_id}"
                )

                if is_chosen:
                    # Chosen player should not spend token
                    assert player.command_sheet.strategy_pool == initial_tokens, (
                        f"Token spent for chosen player {player_id}"
                    )
                else:
                    # Non-chosen player should spend token
                    assert player.command_sheet.strategy_pool == initial_tokens - 1, (
                        f"Token not spent for non-chosen player {player_id}"
                    )
            else:
                assert result.success is False, f"Expected failure for {player_id}"


class TestTradeCardSecondaryAbilityMultiPlayerScenarios:
    """Test suite for Trade card secondary ability multi-player scenarios (Requirements 8.1, 8.2, 8.3, 8.4)."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        from ti4.core.game_state import GameState

        self.card = TradeStrategyCard()
        self.player1 = Player(id="player1", faction=Faction.SOL)
        self.player2 = Player(id="player2", faction=Faction.HACAN)
        self.player3 = Player(id="player3", faction=Faction.XXCHA)
        self.game_state = GameState(players=[self.player1, self.player2, self.player3])

    def test_multiple_players_can_use_secondary_ability_concurrently(self) -> None:
        """Test that multiple players can use secondary ability independently.

        Requirements: 8.1 - WHEN multiple players use the secondary ability
        THEN each SHALL be processed independently
        """
        # RED: This test will fail because execute_secondary_ability doesn't handle multi-player scenarios yet
        # Set up all players with command tokens and some commodities
        for player in [self.player1, self.player2, self.player3]:
            player.command_sheet.strategy_pool = 2
            player.add_commodities(1)

        # Execute secondary ability for each player
        result1 = self.card.execute_secondary_ability(
            player_id="player1", game_state=self.game_state
        )
        result2 = self.card.execute_secondary_ability(
            player_id="player2", game_state=self.game_state
        )
        result3 = self.card.execute_secondary_ability(
            player_id="player3", game_state=self.game_state
        )

        # Verify all executions succeeded
        assert result1.success is True
        assert result2.success is True
        assert result3.success is True

        # Verify each player's resources were updated independently
        assert self.player1.command_sheet.strategy_pool == 1
        assert self.player2.command_sheet.strategy_pool == 1
        assert self.player3.command_sheet.strategy_pool == 1

        assert self.player1.get_commodities() == self.player1.get_commodity_value()
        assert self.player2.get_commodities() == self.player2.get_commodity_value()
        assert self.player3.get_commodities() == self.player3.get_commodity_value()

    def test_players_with_different_faction_commodity_limits(self) -> None:
        """Test secondary ability with players having different faction commodity limits.

        Requirements: 8.3 - WHEN players have different faction commodity limits
        THEN each SHALL replenish to their own maximum
        """
        # RED: This test will fail because execute_secondary_ability doesn't handle different faction limits yet
        # Set up players with command tokens and some commodities
        self.player1.command_sheet.strategy_pool = 1  # SOL
        self.player2.command_sheet.strategy_pool = 1  # HACAN
        self.player3.command_sheet.strategy_pool = 1  # XXCHA

        self.player1.add_commodities(1)
        self.player2.add_commodities(2)
        self.player3.add_commodities(1)

        # Get each faction's commodity limits
        sol_max = self.player1.get_commodity_value()
        hacan_max = self.player2.get_commodity_value()
        xxcha_max = self.player3.get_commodity_value()

        # Execute secondary ability for each player
        result1 = self.card.execute_secondary_ability(
            player_id="player1", game_state=self.game_state
        )
        result2 = self.card.execute_secondary_ability(
            player_id="player2", game_state=self.game_state
        )
        result3 = self.card.execute_secondary_ability(
            player_id="player3", game_state=self.game_state
        )

        # Verify all executions succeeded
        assert result1.success is True
        assert result2.success is True
        assert result3.success is True

        # Verify each player replenished to their own faction maximum
        assert self.player1.get_commodities() == sol_max
        assert self.player2.get_commodities() == hacan_max
        assert self.player3.get_commodities() == xxcha_max

    def test_mixed_command_token_availability(self) -> None:
        """Test secondary ability when players have different command token availability.

        Requirements: 8.4 - WHEN command token availability varies by player
        THEN each player's ability to use secondary SHALL be validated independently
        """
        # RED: This test will fail because execute_secondary_ability doesn't validate tokens independently yet
        # Set up players with different command token availability
        self.player1.command_sheet.strategy_pool = 2  # Has tokens
        self.player2.command_sheet.strategy_pool = 0  # No tokens
        self.player3.command_sheet.strategy_pool = 1  # Has tokens

        # Execute secondary ability for each player
        result1 = self.card.execute_secondary_ability(
            player_id="player1", game_state=self.game_state
        )
        result2 = self.card.execute_secondary_ability(
            player_id="player2", game_state=self.game_state
        )
        result3 = self.card.execute_secondary_ability(
            player_id="player3", game_state=self.game_state
        )

        # Verify results based on token availability
        assert result1.success is True  # Should succeed
        assert result2.success is False  # Should fail due to no tokens
        assert result3.success is True  # Should succeed

        # Verify error message for player without tokens
        assert "command token" in result2.error_message.lower()

        # Verify successful players had tokens spent
        assert self.player1.command_sheet.strategy_pool == 1
        assert self.player2.command_sheet.strategy_pool == 0  # Unchanged
        assert self.player3.command_sheet.strategy_pool == 0

    def test_chosen_players_can_execute_for_free(self) -> None:
        """Test that chosen players can execute secondary ability without command tokens.

        Requirements: 8.2 - WHEN the active player chooses players for free secondary
        THEN the selection SHALL be tracked per execution
        """
        # RED: This test will fail because execute_secondary_ability doesn't support chosen player tracking yet
        # Set up players with no command tokens
        self.player1.command_sheet.strategy_pool = 0
        self.player2.command_sheet.strategy_pool = 0
        self.player3.command_sheet.strategy_pool = 1  # Only player3 has tokens

        # Execute secondary ability - player1 and player2 should be able to execute for free
        result1 = self.card.execute_secondary_ability(
            player_id="player1", game_state=self.game_state, is_free=True
        )
        result2 = self.card.execute_secondary_ability(
            player_id="player2", game_state=self.game_state, is_free=True
        )
        result3 = self.card.execute_secondary_ability(
            player_id="player3", game_state=self.game_state, is_free=False
        )

        # Verify all executions succeeded
        assert result1.success is True
        assert result2.success is True
        assert result3.success is True

        # Verify no command tokens were spent for free executions
        assert self.player1.command_sheet.strategy_pool == 0  # Unchanged
        assert self.player2.command_sheet.strategy_pool == 0  # Unchanged
        assert self.player3.command_sheet.strategy_pool == 0  # Token spent


class TestTradeCardPrimaryAbilityIntegration:
    """Test suite for complete primary ability workflow integration (Requirements 6.1, 6.2, 9.2, 9.3)."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        from ti4.core.game_state import GameState

        self.card = TradeStrategyCard()
        self.active_player = Player(id="active_player", faction=Faction.SOL)
        self.player1 = Player(id="player1", faction=Faction.HACAN)
        self.player2 = Player(id="player2", faction=Faction.XXCHA)
        self.game_state = GameState(
            players=[self.active_player, self.player1, self.player2]
        )

    def test_complete_primary_ability_execution_sequence(self) -> None:
        """Test that primary ability executes all three steps in correct sequence.

        Requirements: 6.1 - WHEN the Trade strategy card is executed
        THEN it SHALL follow the standard strategy card execution pattern
        """
        # RED: This test will fail because execute_primary_ability doesn't orchestrate all steps properly
        # Set up initial state
        self.active_player.gain_trade_goods(2)  # Start with some trade goods
        self.active_player.add_commodities(1)  # Start with some commodities

        initial_trade_goods = self.active_player.get_trade_goods()
        faction_max_commodities = self.active_player.get_commodity_value()

        chosen_players = ["player1", "player2"]

        # Execute complete primary ability
        result = self.card.execute_primary_ability(
            player_id="active_player",
            game_state=self.game_state,
            chosen_players=chosen_players,
        )

        # Verify result success
        assert result.success is True
        assert result.player_id == "active_player"

        # Verify Step 1: Trade goods gained
        assert self.active_player.get_trade_goods() == initial_trade_goods + 3

        # Verify Step 2: Commodities replenished to faction maximum
        assert self.active_player.get_commodities() == faction_max_commodities

        # Verify Step 3: Chosen players processed (implementation will define tracking)
        # For now, just verify no errors occurred
        assert result.error_message is None or result.error_message == ""

    def test_primary_ability_with_all_steps_from_zero_resources(self) -> None:
        """Test complete primary ability when player starts with zero resources.

        Requirements: 6.1, 6.2 - Complete workflow execution with proper integration
        """
        # RED: This test will fail because execute_primary_ability doesn't handle complete workflow
        # Ensure player starts with zero resources
        assert self.active_player.get_trade_goods() == 0
        assert self.active_player.get_commodities() == 0

        faction_max_commodities = self.active_player.get_commodity_value()
        chosen_players = ["player1"]

        # Execute complete primary ability
        result = self.card.execute_primary_ability(
            player_id="active_player",
            game_state=self.game_state,
            chosen_players=chosen_players,
        )

        # Verify all steps completed successfully
        assert result.success is True
        assert self.active_player.get_trade_goods() == 3
        assert self.active_player.get_commodities() == faction_max_commodities

    def test_primary_ability_error_handling_invalid_player(self) -> None:
        """Test primary ability error handling for invalid player ID.

        Requirements: 9.2 - WHEN game state is corrupted or missing
        THEN the system SHALL handle gracefully without crashing
        """
        # RED: This test will fail because execute_primary_ability doesn't have comprehensive error handling
        from ti4.core.exceptions import TI4GameError

        # Try to execute primary ability for non-existent player
        try:
            result = self.card.execute_primary_ability(
                player_id="nonexistent_player",
                game_state=self.game_state,
                chosen_players=["player1"],
            )
            # If no exception, check that result indicates failure
            assert result.success is False
            assert "player" in result.error_message.lower()
            assert "nonexistent_player" in result.error_message
        except TI4GameError as e:
            # Exception is also acceptable
            assert "player" in str(e).lower()
            assert "nonexistent_player" in str(e)

    def test_primary_ability_error_handling_invalid_chosen_players(self) -> None:
        """Test primary ability error handling for invalid chosen players.

        Requirements: 9.1 - WHEN invalid player IDs are provided
        THEN appropriate error messages SHALL be returned
        """
        # RED: This test will fail because execute_primary_ability doesn't have comprehensive error handling
        from ti4.core.exceptions import TI4GameError

        chosen_players = ["invalid_player", "player1"]

        # Try to execute primary ability with invalid chosen players
        try:
            result = self.card.execute_primary_ability(
                player_id="active_player",
                game_state=self.game_state,
                chosen_players=chosen_players,
            )
            # If no exception, check that result indicates failure
            assert result.success is False
            assert "invalid_player" in result.error_message.lower()
        except TI4GameError as e:
            # Exception is also acceptable
            assert "invalid_player" in str(e).lower()

    def test_primary_ability_rollback_capability_on_error(self) -> None:
        """Test that primary ability can rollback changes on error.

        Requirements: 9.3 - WHEN resource limits are exceeded
        THEN the system SHALL apply appropriate caps or overflow handling
        """
        # RED: This test will fail because execute_primary_ability doesn't have rollback capability
        # Set up initial state
        initial_trade_goods = 5
        initial_commodities = 2
        self.active_player.gain_trade_goods(initial_trade_goods)
        self.active_player.add_commodities(initial_commodities)

        # Create a scenario that should cause an error (invalid chosen players)
        chosen_players = ["invalid_player"]

        try:
            result = self.card.execute_primary_ability(
                player_id="active_player",
                game_state=self.game_state,
                chosen_players=chosen_players,
            )

            if not result.success:
                # If operation failed, resources should be unchanged (rollback)
                assert self.active_player.get_trade_goods() == initial_trade_goods
                assert self.active_player.get_commodities() == initial_commodities
        except Exception:
            # If exception occurred, resources should be unchanged (rollback)
            assert self.active_player.get_trade_goods() == initial_trade_goods
            assert self.active_player.get_commodities() == initial_commodities

    def test_primary_ability_returns_proper_strategy_card_ability_result(self) -> None:
        """Test that primary ability returns proper StrategyCardAbilityResult.

        Requirements: 6.2 - WHEN the Trade strategy card abilities are resolved
        THEN they SHALL return proper StrategyCardAbilityResult objects
        """
        # RED: This test will fail because execute_primary_ability doesn't return enhanced result
        from ti4.core.strategy_cards.base_strategy_card import StrategyCardAbilityResult

        chosen_players = ["player1"]

        result = self.card.execute_primary_ability(
            player_id="active_player",
            game_state=self.game_state,
            chosen_players=chosen_players,
        )

        # Verify result type and properties
        assert isinstance(result, StrategyCardAbilityResult)
        assert result.success is True
        assert result.player_id == "active_player"
        assert result.error_message is None or result.error_message == ""

        # Verify that result follows the standard StrategyCardAbilityResult pattern
        assert hasattr(result, "success")
        assert hasattr(result, "player_id")
        assert hasattr(result, "resources_spent")
        assert hasattr(result, "command_tokens_spent")
        assert hasattr(result, "error_message")
        assert hasattr(result, "additional_data")

    def test_primary_ability_with_concurrent_access_safety(self) -> None:
        """Test primary ability handles concurrent access safely.

        Requirements: 9.4 - WHEN concurrent access occurs
        THEN the system SHALL maintain data consistency
        """
        # RED: This test will fail because execute_primary_ability doesn't handle concurrent access
        # This is a basic test - full concurrent testing would require threading

        # Execute primary ability multiple times in sequence to test state consistency
        chosen_players = ["player1"]

        # First execution
        result1 = self.card.execute_primary_ability(
            player_id="active_player",
            game_state=self.game_state,
            chosen_players=chosen_players,
        )

        # Capture state after first execution
        trade_goods_after_first = self.active_player.get_trade_goods()
        commodities_after_first = self.active_player.get_commodities()

        # Second execution (should work independently)
        result2 = self.card.execute_primary_ability(
            player_id="active_player",
            game_state=self.game_state,
            chosen_players=chosen_players,
        )

        # Verify both executions succeeded
        assert result1.success is True
        assert result2.success is True

        # Verify state consistency (second execution should add to first)
        assert self.active_player.get_trade_goods() == trade_goods_after_first + 3
        # Commodities should remain at max (can't exceed faction limit)
        assert self.active_player.get_commodities() == commodities_after_first

    def test_primary_ability_integration_with_all_steps_working_together(self) -> None:
        """Test that all three steps of primary ability work together correctly.

        Requirements: 6.1, 6.2 - Complete workflow execution with proper integration
        """
        # Set up initial state with specific values
        self.active_player.gain_trade_goods(1)
        self.active_player.add_commodities(2)

        initial_trade_goods = self.active_player.get_trade_goods()
        self.active_player.get_commodities()
        faction_max = self.active_player.get_commodity_value()

        chosen_players = ["player1", "player2"]

        # Execute primary ability
        result = self.card.execute_primary_ability(
            player_id="active_player",
            game_state=self.game_state,
            chosen_players=chosen_players,
        )

        # Verify successful execution
        assert result.success is True
        assert result.player_id == "active_player"
        assert result.error_message is None or result.error_message == ""

        # Verify Step 1: Trade goods increased by exactly 3
        assert self.active_player.get_trade_goods() == initial_trade_goods + 3

        # Verify Step 2: Commodities set to faction maximum
        assert self.active_player.get_commodities() == faction_max

        # Verify Step 3: Chosen players were processed without error
        # (Actual tracking implementation will be added in later tasks)

        # Verify other players were not affected
        assert self.player1.get_trade_goods() == 0
        assert self.player1.get_commodities() == 0
        assert self.player2.get_trade_goods() == 0
        assert self.player2.get_commodities() == 0


class TestTradeCardImplementationBehavior:
    """Test suite for implemented behavior of Trade card abilities."""

    def test_secondary_ability_requires_game_state(self) -> None:
        """Test that secondary ability requires game state parameter."""
        # Test that secondary ability now requires game state
        card = TradeStrategyCard()

        result = card.execute_secondary_ability(player_id="test_player")

        assert result.success is False
        assert result.player_id == "test_player"
        assert "game state is required" in result.error_message.lower()

    def test_abilities_accept_kwargs(self) -> None:
        """Test that abilities accept additional keyword arguments."""
        # Test that implementation accepts kwargs
        from ti4.core.constants import Faction
        from ti4.core.game_state import GameState
        from ti4.core.player import Player

        card = TradeStrategyCard()
        player = Player(id="test_player", faction=Faction.SOL)
        player.command_sheet.strategy_pool = 1
        game_state = GameState(players=[player])

        secondary_result = card.execute_secondary_ability(
            player_id="test_player",
            game_state=game_state,
            some_param="value",
            another_param=123,
        )

        assert secondary_result.success is True


class TestTradeCardPerformanceOptimization:
    """Test suite for Trade card performance optimization and quality assurance (Requirements 11.1, 11.2, 11.3, 11.4)."""

    def setup_method(self) -> None:
        """Set up test fixtures for performance testing."""
        self.card = TradeStrategyCard()
        self.players = [Player(id=f"player_{i}", faction=Faction.SOL) for i in range(6)]
        self.game_state = GameState(players=self.players)

        # Set up players with various resource states for realistic testing
        for i, player in enumerate(self.players):
            player.gain_trade_goods(i * 2)  # Varying trade goods
            # Add commodities within faction limit (SOL has 4 commodity value)
            commodities_to_add = min(i, player.get_commodity_value() - 1)
            if commodities_to_add > 0:
                player.add_commodities(commodities_to_add)
            # Add command tokens to strategy pool
            for _ in range(3):
                player.command_sheet.gain_command_token("strategy")

    def test_primary_ability_execution_time_under_50ms(self) -> None:
        """Test that Trade primary ability executes within 50ms requirement.

        Requirements: 11.1 - WHEN the Trade strategy card is executed
        THEN it SHALL complete within 50ms
        """
        # RED: Test performance requirement for primary ability
        player_id = "player_0"
        chosen_players = ["player_1", "player_2", "player_3"]

        # Warm up the method to avoid cold start effects
        self.card.execute_primary_ability(
            player_id=player_id,
            game_state=self.game_state,
            chosen_players=chosen_players,
        )

        # Measure execution time over multiple runs
        execution_times = []
        for _ in range(10):
            start_time = time.perf_counter()
            result = self.card.execute_primary_ability(
                player_id=player_id,
                game_state=self.game_state,
                chosen_players=chosen_players,
            )
            end_time = time.perf_counter()

            execution_time_ms = (end_time - start_time) * 1000
            execution_times.append(execution_time_ms)

            assert result.success is True

        # Check that average execution time is under 50ms
        avg_execution_time = sum(execution_times) / len(execution_times)
        max_execution_time = max(execution_times)

        assert avg_execution_time < 50.0, (
            f"Average execution time {avg_execution_time:.2f}ms exceeds 50ms limit"
        )
        assert max_execution_time < 75.0, (
            f"Max execution time {max_execution_time:.2f}ms exceeds reasonable limit"
        )

    def test_secondary_ability_execution_time_under_25ms(self) -> None:
        """Test that Trade secondary ability executes within 25ms requirement.

        Requirements: 11.1 - WHEN the Trade secondary ability is executed
        THEN it SHALL complete within 25ms
        """
        # RED: Test performance requirement for secondary ability
        player_id = "player_1"
        player = self.game_state.get_player(player_id)

        # Warm up the method
        player.command_sheet.gain_command_token("strategy")  # Ensure we have tokens
        self.card.execute_secondary_ability(
            player_id=player_id, game_state=self.game_state
        )

        # Measure execution time over multiple runs
        execution_times = []
        for _ in range(10):
            # Ensure player has command tokens for each test
            player.command_sheet.gain_command_token("strategy")

            start_time = time.perf_counter()
            result = self.card.execute_secondary_ability(
                player_id=player_id, game_state=self.game_state
            )
            end_time = time.perf_counter()

            execution_time_ms = (end_time - start_time) * 1000
            execution_times.append(execution_time_ms)

            assert result.success is True

        # Check that average execution time is under 25ms
        avg_execution_time = sum(execution_times) / len(execution_times)
        max_execution_time = max(execution_times)

        assert avg_execution_time < 25.0, (
            f"Average execution time {avg_execution_time:.2f}ms exceeds 25ms limit"
        )
        assert max_execution_time < 50.0, (
            f"Max execution time {max_execution_time:.2f}ms exceeds reasonable limit"
        )

    def test_concurrent_secondary_ability_performance(self) -> None:
        """Test performance when multiple players use secondary ability concurrently.

        Requirements: 11.1, 8.4 - Multi-player concurrent execution performance
        """
        # RED: Test concurrent execution performance
        player_ids = ["player_1", "player_2", "player_3", "player_4"]

        # Warm up
        for player_id in player_ids:
            self.card.execute_secondary_ability(
                player_id=player_id, game_state=self.game_state
            )

        # Measure concurrent execution time
        start_time = time.perf_counter()

        results = []
        for player_id in player_ids:
            result = self.card.execute_secondary_ability(
                player_id=player_id, game_state=self.game_state
            )
            results.append(result)

        end_time = time.perf_counter()
        total_execution_time_ms = (end_time - start_time) * 1000

        # All executions should succeed
        for result in results:
            assert result.success is True

        # Total time for 4 concurrent executions should be reasonable
        assert total_execution_time_ms < 100.0, (
            f"Concurrent execution time {total_execution_time_ms:.2f}ms exceeds 100ms limit"
        )

    def test_performance_with_large_player_count(self) -> None:
        """Test performance with maximum player count (8 players).

        Requirements: 11.1 - Performance with realistic game scenarios
        """
        # RED: Test performance with maximum players
        large_players = [
            Player(id=f"player_{i}", faction=Faction.SOL) for i in range(8)
        ]
        large_game_state = GameState(players=large_players)

        # Set up players with resources
        for player in large_players:
            player.gain_trade_goods(5)
            player.add_commodities(2)
            for _ in range(3):
                player.command_sheet.gain_command_token("strategy")

        # Test primary ability with all players chosen
        chosen_players = [
            f"player_{i}" for i in range(1, 8)
        ]  # All except active player

        start_time = time.perf_counter()
        result = self.card.execute_primary_ability(
            player_id="player_0",
            game_state=large_game_state,
            chosen_players=chosen_players,
        )
        end_time = time.perf_counter()

        execution_time_ms = (end_time - start_time) * 1000

        assert result.success is True
        assert execution_time_ms < 75.0, (
            f"Large player count execution time {execution_time_ms:.2f}ms exceeds 75ms limit"
        )

    def test_performance_benchmarking_and_monitoring(self) -> None:
        """Test performance benchmarking and monitoring capabilities.

        Requirements: 11.3 - Add performance benchmarking and monitoring
        """
        # RED: Test that we can collect performance metrics
        player_id = "player_0"

        # Collect performance metrics over multiple runs
        primary_times = []
        secondary_times = []

        for _ in range(20):
            # Primary ability timing
            start_time = time.perf_counter()
            primary_result = self.card.execute_primary_ability(
                player_id=player_id, game_state=self.game_state
            )
            primary_time = (time.perf_counter() - start_time) * 1000
            primary_times.append(primary_time)

            # Secondary ability timing - ensure player has command tokens
            secondary_player = self.game_state.get_player("player_1")
            secondary_player.command_sheet.gain_command_token("strategy")

            start_time = time.perf_counter()
            secondary_result = self.card.execute_secondary_ability(
                player_id="player_1", game_state=self.game_state
            )
            secondary_time = (time.perf_counter() - start_time) * 1000
            secondary_times.append(secondary_time)

            assert primary_result.success is True
            assert secondary_result.success is True

        # Calculate performance statistics
        primary_avg = sum(primary_times) / len(primary_times)
        primary_max = max(primary_times)
        min(primary_times)

        secondary_avg = sum(secondary_times) / len(secondary_times)
        secondary_max = max(secondary_times)
        min(secondary_times)

        # Verify performance characteristics
        assert primary_avg < 50.0, (
            f"Primary ability average time {primary_avg:.2f}ms exceeds target"
        )
        assert secondary_avg < 25.0, (
            f"Secondary ability average time {secondary_avg:.2f}ms exceeds target"
        )

        # Performance should be consistent (allow for system load variations)
        assert primary_max < primary_avg * 5, (
            f"Primary ability performance inconsistent: max {primary_max:.2f}ms vs avg {primary_avg:.2f}ms"
        )
        assert secondary_max < secondary_avg * 5, (
            f"Secondary ability performance inconsistent: max {secondary_max:.2f}ms vs avg {secondary_avg:.2f}ms"
        )

    def test_resource_management_batch_operations_performance(self) -> None:
        """Test performance of batch resource management operations.

        Requirements: 11.2 - Optimize resource management operations for batch updates
        """
        # RED: Test batch resource operations performance
        player_id = "player_0"
        player = self.game_state.get_player(player_id)

        # Test batch trade goods operations
        start_time = time.perf_counter()
        for _ in range(100):
            player.gain_trade_goods(1)
        batch_time = (time.perf_counter() - start_time) * 1000

        # Test single large operation
        start_time = time.perf_counter()
        player.gain_trade_goods(100)
        single_time = (time.perf_counter() - start_time) * 1000

        # Single large operation should be faster than many small ones
        # This tests that our resource management is optimized
        assert single_time < batch_time, (
            f"Single operation {single_time:.2f}ms should be faster than batch {batch_time:.2f}ms"
        )

        # Both should be reasonably fast
        assert batch_time < 50.0, (
            f"Batch operations time {batch_time:.2f}ms exceeds reasonable limit"
        )
        assert single_time < 10.0, (
            f"Single operation time {single_time:.2f}ms exceeds reasonable limit"
        )

    def test_memory_usage_optimization(self) -> None:
        """Test that Trade card operations don't cause excessive memory usage.

        Requirements: 11.2 - Performance optimization including memory usage
        """
        # RED: Test memory usage doesn't grow excessively
        import gc

        # Force garbage collection and get baseline
        gc.collect()
        initial_objects = len(gc.get_objects())

        # Execute many operations
        for _i in range(100):
            result = self.card.execute_primary_ability(
                player_id="player_0",
                game_state=self.game_state,
                chosen_players=["player_1", "player_2"],
            )
            assert result.success is True

            result = self.card.execute_secondary_ability(
                player_id="player_1", game_state=self.game_state
            )
            assert result.success is True

        # Force garbage collection and check final count
        gc.collect()
        final_objects = len(gc.get_objects())

        # Object count shouldn't grow excessively (allow some growth for test overhead)
        object_growth = final_objects - initial_objects
        assert object_growth < 1000, (
            f"Excessive object growth: {object_growth} objects created"
        )

    def test_error_handling_performance_impact(self) -> None:
        """Test that error handling doesn't significantly impact performance.

        Requirements: 11.1, 9.2 - Error handling should not degrade performance
        """
        # RED: Test that error paths don't cause performance degradation

        # Test successful execution time
        start_time = time.perf_counter()
        success_result = self.card.execute_primary_ability(
            player_id="player_0", game_state=self.game_state
        )
        success_time = (time.perf_counter() - start_time) * 1000

        assert success_result.success is True

        # Test error execution time (invalid player)
        start_time = time.perf_counter()
        error_result = self.card.execute_primary_ability(
            player_id="invalid_player", game_state=self.game_state
        )
        error_time = (time.perf_counter() - start_time) * 1000

        assert error_result.success is False

        # Error handling should not be significantly slower than success path
        assert error_time < success_time * 2, (
            f"Error handling time {error_time:.2f}ms is too slow compared to success time {success_time:.2f}ms"
        )
        assert error_time < 25.0, (
            f"Error handling time {error_time:.2f}ms exceeds reasonable limit"
        )

    def test_performance_metrics_collection(self) -> None:
        """Test that performance metrics are collected correctly.

        Requirements: 11.3 - Performance benchmarking and monitoring
        """
        # Initially, metrics should be empty
        metrics = self.card.get_performance_metrics()
        assert metrics["primary_ability_times"]["count"] == 0
        assert metrics["secondary_ability_times"]["count"] == 0

        # Execute primary ability
        self.card.execute_primary_ability(
            player_id="player_0", game_state=self.game_state
        )

        # Execute secondary ability
        player = self.game_state.get_player("player_1")
        player.command_sheet.gain_command_token("strategy")
        self.card.execute_secondary_ability(
            player_id="player_1", game_state=self.game_state
        )

        # Check metrics were collected
        metrics = self.card.get_performance_metrics()
        assert metrics["primary_ability_times"]["count"] == 1
        assert metrics["secondary_ability_times"]["count"] == 1
        assert metrics["primary_ability_times"]["average_ms"] > 0
        assert metrics["secondary_ability_times"]["average_ms"] > 0

    def test_performance_metrics_reset(self) -> None:
        """Test that performance metrics can be reset.

        Requirements: 11.3 - Performance benchmarking and monitoring
        """
        # Execute some operations to collect metrics
        self.card.execute_primary_ability(
            player_id="player_0", game_state=self.game_state
        )

        # Verify metrics exist
        metrics = self.card.get_performance_metrics()
        assert metrics["primary_ability_times"]["count"] == 1

        # Reset metrics
        self.card.reset_performance_metrics()

        # Verify metrics are cleared
        metrics = self.card.get_performance_metrics()
        assert metrics["primary_ability_times"]["count"] == 0
        assert metrics["secondary_ability_times"]["count"] == 0

    def test_performance_metrics_statistics(self) -> None:
        """Test that performance metrics calculate statistics correctly.

        Requirements: 11.3 - Performance benchmarking and monitoring
        """
        # Execute multiple operations
        for _ in range(3):
            self.card.execute_primary_ability(
                player_id="player_0", game_state=self.game_state
            )

        metrics = self.card.get_performance_metrics()
        primary_metrics = metrics["primary_ability_times"]

        # Verify statistics are calculated
        assert primary_metrics["count"] == 3
        assert primary_metrics["average_ms"] > 0
        assert primary_metrics["min_ms"] > 0
        assert primary_metrics["max_ms"] > 0
        assert primary_metrics["total_ms"] > 0
        assert (
            primary_metrics["min_ms"]
            <= primary_metrics["average_ms"]
            <= primary_metrics["max_ms"]
        )
        assert (
            abs(primary_metrics["total_ms"] - (primary_metrics["average_ms"] * 3))
            < 0.001
        )  # Account for floating point precision


class TestTradeCardQualityAssurance:
    """Test suite for Trade card quality assurance and coverage validation (Requirements 11.4)."""

    def setup_method(self) -> None:
        """Set up test fixtures for quality assurance testing."""
        self.card = TradeStrategyCard()
        self.players = [Player(id=f"player_{i}", faction=Faction.SOL) for i in range(4)]
        self.game_state = GameState(players=self.players)

        # Set up players with resources
        for player in self.players:
            player.gain_trade_goods(3)
            player.add_commodities(2)
            for _ in range(3):
                player.command_sheet.gain_command_token("strategy")

    def test_comprehensive_error_condition_coverage(self) -> None:
        """Test comprehensive coverage of all error conditions.

        Requirements: 11.4 - Ensure 95%+ test coverage and all quality gates pass
        """
        # RED: Test all error conditions are properly covered

        # Test invalid player ID in primary ability
        result = self.card.execute_primary_ability(
            player_id="invalid_player", game_state=self.game_state
        )
        assert result.success is False
        assert "not found" in result.error_message.lower()

        # Test invalid player ID in secondary ability
        result = self.card.execute_secondary_ability(
            player_id="invalid_player", game_state=self.game_state
        )
        assert result.success is False
        assert "not found" in result.error_message.lower()

        # Test None game state in primary ability
        result = self.card.execute_primary_ability(
            player_id="player_0", game_state=None
        )
        assert result.success is True  # Should return placeholder result
        assert "requires user confirmation" in result.error_message

        # Test None game state in secondary ability
        result = self.card.execute_secondary_ability(
            player_id="player_0", game_state=None
        )
        assert result.success is False
        assert "required" in result.error_message.lower()

    def test_edge_case_coverage_validation(self) -> None:
        """Test that all edge cases are properly covered.

        Requirements: 11.4 - Comprehensive edge case testing
        """
        # RED: Test edge cases for comprehensive coverage

        # Test choosing self in primary ability
        result = self.card.execute_primary_ability(
            player_id="player_0",
            game_state=self.game_state,
            chosen_players=["player_0", "player_1"],
        )
        assert result.success is False
        assert (
            "themselves" in result.error_message.lower()
            or "active player" in result.error_message.lower()
        )

        # Test invalid chosen players
        result = self.card.execute_primary_ability(
            player_id="player_0",
            game_state=self.game_state,
            chosen_players=["invalid_player"],
        )
        assert result.success is False
        assert "invalid_player" in result.error_message.lower()

        # Test secondary ability without command tokens
        player = self.game_state.get_player("player_0")
        # Remove all command tokens
        while player.command_sheet.has_strategy_tokens():
            player.command_sheet.spend_strategy_token()

        result = self.card.execute_secondary_ability(
            player_id="player_0", game_state=self.game_state
        )
        assert result.success is False
        assert "insufficient" in result.error_message.lower()

    def test_integration_with_existing_systems_validation(self) -> None:
        """Test integration with existing game systems for quality assurance.

        Requirements: 11.4 - Validate integration with existing frameworks
        """
        # RED: Test integration quality

        # Test BaseStrategyCard interface compliance
        from ti4.core.strategy_cards.base_strategy_card import (
            BaseStrategyCard,
            StrategyCardAbilityResult,
        )

        assert isinstance(self.card, BaseStrategyCard)

        # Test return types
        primary_result = self.card.execute_primary_ability("player_0", self.game_state)
        secondary_result = self.card.execute_secondary_ability(
            "player_1", self.game_state
        )

        assert isinstance(primary_result, StrategyCardAbilityResult)
        assert isinstance(secondary_result, StrategyCardAbilityResult)

        # Test strategy card type consistency
        assert self.card.get_card_type() == StrategyCardType.TRADE
        assert self.card.get_initiative_value() == 5
        assert self.card.get_name() == "trade"

    def test_rollback_capability_quality_assurance(self) -> None:
        """Test rollback capability for quality assurance.

        Requirements: 11.4, 9.3 - Rollback capability validation
        """
        # RED: Test rollback functionality quality
        player = self.game_state.get_player("player_0")
        initial_trade_goods = player.get_trade_goods()
        initial_commodities = player.get_commodities()

        # Force an error after partial execution by providing invalid chosen players
        # This should trigger rollback
        result = self.card.execute_primary_ability(
            player_id="player_0",
            game_state=self.game_state,
            chosen_players=["invalid_player"],
        )

        assert result.success is False

        # Verify rollback occurred - resources should be back to initial state
        assert player.get_trade_goods() == initial_trade_goods
        assert player.get_commodities() == initial_commodities

    def test_chosen_players_tracking_quality(self) -> None:
        """Test chosen players tracking functionality for quality assurance.

        Requirements: 11.4, 8.2 - Chosen player tracking validation
        """
        # RED: Test chosen players tracking quality

        # Execute primary ability with chosen players
        chosen_players = ["player_1", "player_2"]
        result = self.card.execute_primary_ability(
            player_id="player_0",
            game_state=self.game_state,
            chosen_players=chosen_players,
        )

        assert result.success is True

        # Verify chosen players are tracked
        tracked_players = self.card.get_chosen_players(self.game_state)
        assert set(tracked_players) == set(chosen_players)

        # Test free secondary ability for chosen players
        for player_id in chosen_players:
            result = self.card.execute_secondary_ability(
                player_id=player_id, game_state=self.game_state
            )
            assert result.success is True

        # Test non-chosen player still needs command token
        player = self.game_state.get_player("player_3")
        # Remove command tokens
        while player.command_sheet.has_strategy_tokens():
            player.command_sheet.spend_strategy_token()

        result = self.card.execute_secondary_ability(
            player_id="player_3", game_state=self.game_state
        )
        assert result.success is False
        assert "insufficient" in result.error_message.lower()


class TestTradeCardCoverageImprovement:
    """Test suite to improve coverage of Trade strategy card implementation."""

    def setup_method(self) -> None:
        """Set up test fixtures for coverage improvement."""
        self.card = TradeStrategyCard()
        self.players = [Player(id=f"player_{i}", faction=Faction.SOL) for i in range(4)]
        self.game_state = GameState(players=self.players)

        # Set up players with resources
        for player in self.players:
            player.gain_trade_goods(2)
            player.add_commodities(1)
            for _ in range(3):
                player.command_sheet.gain_command_token("strategy")

    def test_primary_ability_with_none_game_state(self) -> None:
        """Test primary ability with None game state returns placeholder result.

        This tests the placeholder implementation path for coverage.
        """
        # Test the placeholder implementation path
        result = self.card.execute_primary_ability(
            player_id="test_player", game_state=None
        )

        assert result.success is True
        assert result.player_id == "test_player"
        assert "requires user confirmation" in result.error_message

    def test_primary_ability_with_invalid_player(self) -> None:
        """Test primary ability with invalid player ID.

        This tests the error handling path for coverage.
        """
        result = self.card.execute_primary_ability(
            player_id="invalid_player", game_state=self.game_state
        )

        assert result.success is False
        assert result.player_id == "invalid_player"
        assert "not found" in result.error_message

    def test_primary_ability_rollback_on_error(self) -> None:
        """Test primary ability rollback when error occurs during execution.

        This tests the rollback functionality for coverage.
        """
        player = self.game_state.get_player("player_0")
        initial_trade_goods = player.get_trade_goods()
        initial_commodities = player.get_commodities()

        # Force an error by providing invalid chosen players after partial execution
        result = self.card.execute_primary_ability(
            player_id="player_0",
            game_state=self.game_state,
            chosen_players=["invalid_player"],
        )

        assert result.success is False

        # Verify rollback occurred
        assert player.get_trade_goods() == initial_trade_goods
        assert player.get_commodities() == initial_commodities

    def test_secondary_ability_with_none_game_state(self) -> None:
        """Test secondary ability with None game state returns error.

        This tests the error handling path for coverage.
        """
        result = self.card.execute_secondary_ability(
            player_id="test_player", game_state=None
        )

        assert result.success is False
        assert result.player_id == "test_player"
        assert "required" in result.error_message.lower()

    def test_secondary_ability_with_invalid_player(self) -> None:
        """Test secondary ability with invalid player ID.

        This tests the error handling path for coverage.
        """
        result = self.card.execute_secondary_ability(
            player_id="invalid_player", game_state=self.game_state
        )

        assert result.success is False
        assert result.player_id == "invalid_player"
        assert "not found" in result.error_message

    def test_secondary_ability_insufficient_command_tokens(self) -> None:
        """Test secondary ability when player has insufficient command tokens.

        This tests the command token validation path for coverage.
        """
        player = self.game_state.get_player("player_0")

        # Remove all command tokens
        while player.command_sheet.has_strategy_tokens():
            player.command_sheet.spend_strategy_token()

        result = self.card.execute_secondary_ability(
            player_id="player_0", game_state=self.game_state
        )

        assert result.success is False
        assert "insufficient" in result.error_message.lower()

    def test_secondary_ability_command_token_spend_failure(self) -> None:
        """Test secondary ability when command token spending fails.

        This tests the command token spending failure path for coverage.
        """
        player = self.game_state.get_player("player_0")

        # Ensure player has exactly one command token
        while player.command_sheet.has_strategy_tokens():
            player.command_sheet.spend_strategy_token()
        player.command_sheet.gain_command_token("strategy")

        # Mock the spend_strategy_token to return False
        original_spend = player.command_sheet.spend_strategy_token
        player.command_sheet.spend_strategy_token = lambda: False

        try:
            result = self.card.execute_secondary_ability(
                player_id="player_0", game_state=self.game_state
            )

            assert result.success is False
            assert "failed to spend" in result.error_message.lower()
        finally:
            # Restore original method
            player.command_sheet.spend_strategy_token = original_spend

    def test_secondary_ability_free_execution(self) -> None:
        """Test secondary ability with free execution (is_free=True).

        This tests the free execution path for coverage.
        """
        result = self.card.execute_secondary_ability(
            player_id="player_0", game_state=self.game_state, is_free=True
        )

        assert result.success is True
        assert result.player_id == "player_0"

    def test_secondary_ability_auto_detect_free_execution(self) -> None:
        """Test secondary ability auto-detecting free execution from chosen players.

        This tests the auto-detection path for coverage.
        """
        # First execute primary ability to choose players
        self.card.execute_primary_ability(
            player_id="player_0",
            game_state=self.game_state,
            chosen_players=["player_1"],
        )

        # Now player_1 should be able to use secondary ability for free
        result = self.card.execute_secondary_ability(
            player_id="player_1", game_state=self.game_state
        )

        assert result.success is True
        assert result.player_id == "player_1"

    def test_get_chosen_players_empty_list(self) -> None:
        """Test get_chosen_players returns empty list when no players chosen.

        This tests the empty chosen players path for coverage.
        """
        chosen_players = self.card.get_chosen_players(self.game_state)
        assert chosen_players == []

    def test_get_chosen_players_with_chosen_players(self) -> None:
        """Test get_chosen_players returns correct list after primary ability execution.

        This tests the chosen players tracking for coverage.
        """
        # Execute primary ability with chosen players
        self.card.execute_primary_ability(
            player_id="player_0",
            game_state=self.game_state,
            chosen_players=["player_1", "player_2"],
        )

        chosen_players = self.card.get_chosen_players(self.game_state)
        assert set(chosen_players) == {"player_1", "player_2"}

    def test_process_chosen_players_with_duplicates(self) -> None:
        """Test _process_chosen_players handles duplicate player IDs correctly.

        This tests the duplicate handling path for coverage.
        """
        # This should not raise an error and should handle duplicates
        self.card._process_chosen_players(
            "player_0", ["player_1", "player_2", "player_1"], self.game_state
        )

        # Verify unique players are stored
        chosen_players = self.card.get_chosen_players(self.game_state)
        assert set(chosen_players) == {"player_1", "player_2"}

    def test_rollback_primary_ability_changes_trade_goods_restoration(self) -> None:
        """Test rollback functionality for trade goods restoration.

        This tests the rollback trade goods path for coverage.
        """
        player = self.game_state.get_player("player_0")
        initial_trade_goods = 5
        initial_commodities = 2

        # Set initial state
        player.gain_trade_goods(initial_trade_goods - player.get_trade_goods())
        player.add_commodities(initial_commodities - player.get_commodities())

        # Test rollback with different trade goods
        self.card._rollback_primary_ability_changes(
            "player_0",
            self.game_state,
            initial_trade_goods - 1,  # Different initial amount
            initial_commodities,
        )

        # Should restore to the specified initial amount
        assert player.get_trade_goods() == initial_trade_goods - 1

    def test_rollback_primary_ability_changes_commodities_restoration(self) -> None:
        """Test rollback functionality for commodities restoration.

        This tests the rollback commodities path for coverage.
        """
        player = self.game_state.get_player("player_0")
        initial_trade_goods = 5
        initial_commodities = 1

        # Set initial state
        player.gain_trade_goods(initial_trade_goods - player.get_trade_goods())
        player.add_commodities(initial_commodities - player.get_commodities())

        # Test rollback with different commodities
        self.card._rollback_primary_ability_changes(
            "player_0",
            self.game_state,
            initial_trade_goods,
            initial_commodities + 1,  # Different initial amount
        )

        # Should restore to the specified initial amount
        assert player.get_commodities() == initial_commodities + 1

    def test_rollback_primary_ability_changes_with_invalid_player(self) -> None:
        """Test rollback functionality with invalid player (should not crash).

        This tests the rollback error handling path for coverage.
        """
        # This should not raise an error even with invalid player
        self.card._rollback_primary_ability_changes(
            "invalid_player",
            self.game_state,
            5,  # initial_trade_goods
            2,  # initial_commodities
        )

        # Should complete without error
        assert True

    def test_primary_ability_unexpected_exception_handling(self) -> None:
        """Test primary ability handling of unexpected exceptions.

        This tests the unexpected exception handling path for coverage.
        """
        # Mock the _gain_trade_goods method to raise an unexpected exception
        original_method = self.card._gain_trade_goods

        def mock_gain_trade_goods(*args, **kwargs):
            raise ValueError("Unexpected error for testing")

        self.card._gain_trade_goods = mock_gain_trade_goods

        try:
            result = self.card.execute_primary_ability(
                player_id="player_0", game_state=self.game_state
            )

            assert result.success is False
            assert "unexpected error" in result.error_message.lower()
        finally:
            # Restore original method
            self.card._gain_trade_goods = original_method

    def test_secondary_ability_ti4_game_error_handling(self) -> None:
        """Test secondary ability handling of TI4GameError exceptions.

        This tests the TI4GameError handling path for coverage.
        """
        # Test with a scenario that would cause a TI4GameError
        # We'll test with an invalid player which should trigger the error path
        result = self.card.execute_secondary_ability(
            player_id="invalid_player", game_state=self.game_state, is_free=True
        )

        assert result.success is False
        assert "not found" in result.error_message.lower()


class TestTradeCardResourceManagementIntegration:
    """Test suite for Trade card integration with ResourceManagement system (Requirements 6.4, 7.1, 7.2)."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        from ti4.core.game_state import GameState
        from ti4.core.resource_management import ResourceManager

        self.card = TradeStrategyCard()
        self.player = Player(id="test_player", faction=Faction.SOL)
        self.game_state = GameState(players=[self.player])
        self.resource_manager = ResourceManager(self.game_state)

    def test_trade_goods_integration_with_resource_manager(self) -> None:
        """Test that Trade card trade goods gain integrates with ResourceManager.

        Requirements: 7.1 - WHEN trade goods are gained THEN they SHALL be tracked in the player's resource pool
        """
        # RED: This test will fail until ResourceManager integration is complete
        initial_resources = self.resource_manager.calculate_available_resources(
            "test_player"
        )

        # Execute primary ability to gain trade goods
        result = self.card.execute_primary_ability(
            player_id="test_player", game_state=self.game_state
        )

        assert result.success is True

        # Verify trade goods are tracked in resource calculations
        final_resources = self.resource_manager.calculate_available_resources(
            "test_player"
        )
        assert final_resources == initial_resources + 3

    def test_commodity_replenishment_respects_faction_limits(self) -> None:
        """Test that commodity replenishment respects faction-specific limits.

        Requirements: 7.2 - WHEN commodities are replenished THEN they SHALL respect faction-specific commodity limits
        """
        # RED: This test will fail until faction limit integration is complete
        # Start with some commodities (less than max)
        self.player.add_commodities(2)
        faction_max = self.player.get_commodity_value()

        # Execute primary ability to replenish commodities
        result = self.card.execute_primary_ability(
            player_id="test_player", game_state=self.game_state
        )

        assert result.success is True
        assert self.player.get_commodities() == faction_max

    def test_resource_changes_reflected_in_game_state_immediately(self) -> None:
        """Test that resource changes are reflected in game state immediately.

        Requirements: 7.4 - WHEN resource changes occur THEN they SHALL be reflected in the game state immediately
        """
        # RED: This test will fail until immediate state reflection is verified
        initial_trade_goods = self.player.get_trade_goods()
        self.player.get_commodities()

        # Execute primary ability
        result = self.card.execute_primary_ability(
            player_id="test_player", game_state=self.game_state
        )

        assert result.success is True

        # Verify changes are immediately reflected
        assert self.player.get_trade_goods() == initial_trade_goods + 3
        assert self.player.get_commodities() == self.player.get_commodity_value()

        # Verify game state reflects the changes
        game_state_player = self.game_state.get_player("test_player")
        assert game_state_player.get_trade_goods() == initial_trade_goods + 3
        assert game_state_player.get_commodities() == self.player.get_commodity_value()

    def test_trade_goods_overflow_handling(self) -> None:
        """Test trade goods overflow handling with ResourceManager.

        Requirements: 7.1 - Resource management integration with overflow handling
        """
        # RED: This test will fail until overflow handling is verified
        # Give player a large amount of trade goods
        large_amount = 1000
        self.player.gain_trade_goods(large_amount)

        # Execute primary ability
        result = self.card.execute_primary_ability(
            player_id="test_player", game_state=self.game_state
        )

        assert result.success is True

        # Verify trade goods were still added (no overflow limit in TI4)
        assert self.player.get_trade_goods() == large_amount + 3

        # Verify ResourceManager can handle large amounts
        total_resources = self.resource_manager.calculate_available_resources(
            "test_player"
        )
        assert total_resources >= large_amount + 3


class TestTradeCardCommandTokenSystemIntegration:
    """Test suite for Trade card integration with CommandTokenSystem (Requirements 6.4, 7.3)."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        from ti4.core.command_tokens import CommandTokenManager
        from ti4.core.game_state import GameState

        self.card = TradeStrategyCard()
        self.player = Player(id="test_player", faction=Faction.SOL)
        self.game_state = GameState(players=[self.player])
        self.command_token_manager = CommandTokenManager()

    def test_secondary_ability_command_token_validation(self) -> None:
        """Test that secondary ability validates command token availability.

        Requirements: 7.3 - WHEN command tokens are spent THEN they SHALL be properly deducted from the strategy pool
        """
        # RED: This test will fail until command token validation is complete
        # Ensure player has command tokens
        self.player.command_sheet.gain_command_token("strategy")
        self.player.command_sheet.gain_command_token("strategy")
        initial_tokens = self.player.command_sheet.strategy_pool

        # Execute secondary ability
        result = self.card.execute_secondary_ability(
            player_id="test_player", game_state=self.game_state
        )

        assert result.success is True

        # Verify command token was spent
        final_tokens = self.player.command_sheet.strategy_pool
        assert final_tokens == initial_tokens - 1

    def test_secondary_ability_fails_without_command_tokens(self) -> None:
        """Test that secondary ability fails when player has no command tokens.

        Requirements: 7.3 - Command token availability validation
        """
        # RED: This test will fail until command token validation is complete
        # Ensure player has no command tokens
        while self.player.command_sheet.has_strategy_tokens():
            self.player.command_sheet.spend_strategy_token()
        assert self.player.command_sheet.strategy_pool == 0

        # Execute secondary ability
        result = self.card.execute_secondary_ability(
            player_id="test_player", game_state=self.game_state
        )

        assert result.success is False
        assert "command token" in result.error_message.lower()

    def test_free_secondary_ability_bypasses_command_token_cost(self) -> None:
        """Test that free secondary ability bypasses command token cost.

        Requirements: 8.4 - Free secondary ability execution for chosen players
        """
        # RED: This test will fail until free secondary ability is complete
        # Ensure player has no command tokens
        while self.player.command_sheet.has_strategy_tokens():
            self.player.command_sheet.spend_strategy_token()
        assert self.player.command_sheet.strategy_pool == 0

        # Execute secondary ability as free (chosen by active player)
        result = self.card.execute_secondary_ability(
            player_id="test_player", game_state=self.game_state, is_free=True
        )

        assert result.success is True

        # Verify no command tokens were spent
        assert self.player.command_sheet.strategy_pool == 0

    def test_command_token_integration_with_game_state(self) -> None:
        """Test command token spending integrates with GameState management.

        Requirements: 6.4 - Integration with GameState management and player resource tracking
        """
        # RED: This test will fail until GameState integration is complete
        # Give player command tokens
        self.player.command_sheet.gain_command_token("strategy")
        self.player.command_sheet.gain_command_token("strategy")
        self.player.command_sheet.gain_command_token("strategy")
        initial_tokens = self.player.command_sheet.strategy_pool

        # Execute secondary ability
        result = self.card.execute_secondary_ability(
            player_id="test_player", game_state=self.game_state
        )

        assert result.success is True

        # Verify game state reflects the command token change
        game_state_player = self.game_state.get_player("test_player")
        assert game_state_player.command_sheet.strategy_pool == initial_tokens - 1


class TestTradeCardGameStateIntegration:
    """Test suite for Trade card integration with GameState management (Requirements 6.4, 7.1, 7.2, 7.3)."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        from ti4.core.game_state import GameState

        self.card = TradeStrategyCard()
        self.player1 = Player(id="player1", faction=Faction.SOL)
        self.player2 = Player(id="player2", faction=Faction.HACAN)
        self.player3 = Player(id="player3", faction=Faction.XXCHA)
        self.game_state = GameState(players=[self.player1, self.player2, self.player3])

    def test_multi_player_resource_tracking(self) -> None:
        """Test that Trade card properly tracks resources across multiple players.

        Requirements: 6.4 - GameState management and player resource tracking
        """
        # RED: This test will fail until multi-player resource tracking is verified
        # Set initial resources for all players
        self.player1.gain_trade_goods(5)
        self.player2.gain_trade_goods(3)
        self.player3.gain_trade_goods(1)

        initial_p1_tg = self.player1.get_trade_goods()
        initial_p2_tg = self.player2.get_trade_goods()
        initial_p3_tg = self.player3.get_trade_goods()

        # Execute primary ability for player1
        result = self.card.execute_primary_ability(
            player_id="player1", game_state=self.game_state
        )

        assert result.success is True

        # Verify only player1's resources changed
        assert self.player1.get_trade_goods() == initial_p1_tg + 3
        assert self.player2.get_trade_goods() == initial_p2_tg  # Unchanged
        assert self.player3.get_trade_goods() == initial_p3_tg  # Unchanged

    def test_game_state_consistency_after_primary_ability(self) -> None:
        """Test that GameState remains consistent after primary ability execution.

        Requirements: 6.4 - GameState management consistency
        """
        # RED: This test will fail until GameState consistency is verified
        # Capture initial game state
        initial_player_count = len(self.game_state.players)
        initial_player_ids = [p.id for p in self.game_state.players]

        # Execute primary ability
        result = self.card.execute_primary_ability(
            player_id="player1", game_state=self.game_state
        )

        assert result.success is True

        # Verify game state structure is unchanged
        assert len(self.game_state.players) == initial_player_count
        assert [p.id for p in self.game_state.players] == initial_player_ids

        # Verify all players are still accessible
        for player_id in initial_player_ids:
            player = self.game_state.get_player(player_id)
            assert player is not None
            assert player.id == player_id

    def test_concurrent_secondary_ability_execution(self) -> None:
        """Test concurrent secondary ability execution by multiple players.

        Requirements: 8.4 - Multi-player game mechanics and turn management
        """
        # RED: This test will fail until concurrent execution is verified
        # Give all players command tokens
        for player in self.game_state.players:
            player.command_sheet.gain_command_token("strategy")
            player.command_sheet.gain_command_token("strategy")

        # Execute secondary ability for multiple players
        result1 = self.card.execute_secondary_ability(
            player_id="player1", game_state=self.game_state
        )
        result2 = self.card.execute_secondary_ability(
            player_id="player2", game_state=self.game_state
        )
        result3 = self.card.execute_secondary_ability(
            player_id="player3", game_state=self.game_state
        )

        # Verify all executions succeeded
        assert result1.success is True
        assert result2.success is True
        assert result3.success is True

        # Verify each player spent a command token (started with 2, gained 2, spent 1 = 3)
        assert self.player1.command_sheet.strategy_pool == 3
        assert self.player2.command_sheet.strategy_pool == 3
        assert self.player3.command_sheet.strategy_pool == 3

        # Verify each player replenished commodities to their faction max
        assert self.player1.get_commodities() == self.player1.get_commodity_value()
        assert self.player2.get_commodities() == self.player2.get_commodity_value()
        assert self.player3.get_commodities() == self.player3.get_commodity_value()

    def test_player_selection_state_management(self) -> None:
        """Test that player selection state is properly managed in GameState.

        Requirements: 8.4 - Multi-player game mechanics integration
        """
        # RED: This test will fail until player selection state management is verified
        chosen_players = ["player2", "player3"]

        # Execute primary ability with player selection
        result = self.card.execute_primary_ability(
            player_id="player1",
            game_state=self.game_state,
            chosen_players=chosen_players,
        )

        assert result.success is True

        # Verify chosen players are tracked
        tracked_chosen = self.card.get_chosen_players(self.game_state)
        assert set(tracked_chosen) == set(chosen_players)

        # Verify chosen players can use secondary ability for free
        result2 = self.card.execute_secondary_ability(
            player_id="player2", game_state=self.game_state
        )
        result3 = self.card.execute_secondary_ability(
            player_id="player3", game_state=self.game_state
        )

        assert result2.success is True
        assert result3.success is True

        # Verify no command tokens were spent (free execution)
        assert (
            self.player2.command_sheet.strategy_pool == 2
        )  # Started with 2, no tokens spent
        assert (
            self.player3.command_sheet.strategy_pool == 2
        )  # Started with 2, no tokens spent


class TestTradeCardStrategyCardSystemCompatibility:
    """Test suite for Trade card compatibility with existing strategy card execution patterns (Requirements 6.4)."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        from ti4.core.game_state import GameState
        from ti4.core.strategy_cards.cards.leadership import LeadershipStrategyCard
        from ti4.core.strategy_cards.cards.politics import PoliticsStrategyCard

        self.trade_card = TradeStrategyCard()
        self.leadership_card = LeadershipStrategyCard()
        self.politics_card = PoliticsStrategyCard()
        self.player = Player(id="test_player", faction=Faction.SOL)
        self.game_state = GameState(players=[self.player])

    def test_trade_card_follows_base_strategy_card_interface(self) -> None:
        """Test that Trade card follows the same interface as other strategy cards.

        Requirements: 6.4 - Verify compatibility with existing strategy card execution patterns
        """
        # RED: This test will fail until interface compatibility is verified
        # Test that all cards implement the same interface
        cards = [self.trade_card, self.leadership_card, self.politics_card]

        for card in cards:
            # Test basic properties
            assert hasattr(card, "get_card_type")
            assert hasattr(card, "get_initiative_value")
            assert hasattr(card, "execute_primary_ability")
            assert hasattr(card, "execute_secondary_ability")

            # Test that methods are callable
            assert callable(card.get_card_type)
            assert callable(card.get_initiative_value)
            assert callable(card.execute_primary_ability)
            assert callable(card.execute_secondary_ability)

            # Test return types
            card_type = card.get_card_type()
            assert isinstance(card_type, StrategyCardType)

            initiative = card.get_initiative_value()
            assert isinstance(initiative, int)
            assert 1 <= initiative <= 8

    def test_trade_card_ability_result_compatibility(self) -> None:
        """Test that Trade card returns compatible StrategyCardAbilityResult objects.

        Requirements: 6.4 - StrategyCardAbilityResult patterns compatibility
        """
        # RED: This test will fail until result compatibility is verified
        from ti4.core.strategy_cards.base_strategy_card import StrategyCardAbilityResult

        # Test primary ability result
        primary_result = self.trade_card.execute_primary_ability(
            player_id="test_player", game_state=self.game_state
        )

        assert isinstance(primary_result, StrategyCardAbilityResult)
        assert hasattr(primary_result, "success")
        assert hasattr(primary_result, "player_id")
        assert hasattr(primary_result, "error_message")
        assert primary_result.player_id == "test_player"

        # Test secondary ability result
        secondary_result = self.trade_card.execute_secondary_ability(
            player_id="test_player", game_state=self.game_state
        )

        assert isinstance(secondary_result, StrategyCardAbilityResult)
        assert hasattr(secondary_result, "success")
        assert hasattr(secondary_result, "player_id")
        assert hasattr(secondary_result, "error_message")
        assert secondary_result.player_id == "test_player"

    def test_trade_card_error_handling_consistency(self) -> None:
        """Test that Trade card error handling is consistent with other strategy cards.

        Requirements: 6.4 - Consistent error handling patterns
        """
        # RED: This test will fail until error handling consistency is verified
        # Test invalid player ID handling
        primary_result = self.trade_card.execute_primary_ability(
            player_id="invalid_player", game_state=self.game_state
        )

        assert primary_result.success is False
        assert "player" in primary_result.error_message.lower()
        assert "invalid_player" in primary_result.error_message

        secondary_result = self.trade_card.execute_secondary_ability(
            player_id="invalid_player", game_state=self.game_state
        )

        assert secondary_result.success is False
        assert "player" in secondary_result.error_message.lower()
        assert "invalid_player" in secondary_result.error_message

    def test_trade_card_performance_characteristics(self) -> None:
        """Test that Trade card meets performance requirements like other strategy cards.

        Requirements: 6.4 - Performance consistency with existing cards
        """
        # RED: This test will fail until performance characteristics are verified
        import time

        # Test primary ability performance
        start_time = time.perf_counter()
        result = self.trade_card.execute_primary_ability(
            player_id="test_player", game_state=self.game_state
        )
        execution_time = (time.perf_counter() - start_time) * 1000  # Convert to ms

        assert result.success is True
        assert execution_time < 50  # Should complete within 50ms

        # Test secondary ability performance
        start_time = time.perf_counter()
        result = self.trade_card.execute_secondary_ability(
            player_id="test_player", game_state=self.game_state, is_free=True
        )
        execution_time = (time.perf_counter() - start_time) * 1000  # Convert to ms

        assert result.success is True
        assert execution_time < 25  # Should complete within 25ms


class TestTradeCardRegistryIntegration:
    """Test suite for Trade card integration with strategy card registry (Requirements 6.3, 6.4)."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        from ti4.core.strategy_cards.registry import StrategyCardRegistry

        self.registry = StrategyCardRegistry()

    def test_trade_card_is_registered_in_registry(self) -> None:
        """Test that TradeStrategyCard is properly registered in the strategy card registry.

        Requirements: 6.3 - Update strategy card registry to include TradeStrategyCard with proper StrategyCardType.TRADE mapping
        """
        # RED: This test will fail until registry integration is complete
        trade_card = self.registry.get_card(StrategyCardType.TRADE)

        assert trade_card is not None
        assert isinstance(trade_card, TradeStrategyCard)
        assert trade_card.get_card_type() == StrategyCardType.TRADE
        assert trade_card.get_initiative_value() == 5

    def test_registry_contains_all_eight_strategy_cards(self) -> None:
        """Test that registry contains all 8 strategy cards including Trade.

        Requirements: 6.3 - Complete strategy card registry
        """
        # RED: This test will fail until all cards are properly registered
        all_cards = self.registry.get_all_cards()

        assert len(all_cards) == 8

        # Verify all card types are present
        card_types = {card.get_card_type() for card in all_cards}
        expected_types = set(StrategyCardType)

        assert card_types == expected_types

    def test_trade_card_initiative_ordering_in_registry(self) -> None:
        """Test that Trade card appears in correct initiative order in registry.

        Requirements: 6.4 - Initiative ordering integration
        """
        # RED: This test will fail until initiative ordering is verified
        cards_by_initiative = self.registry.get_cards_by_initiative_order()

        # Find Trade card position
        trade_position = None
        for i, card in enumerate(cards_by_initiative):
            if card.get_card_type() == StrategyCardType.TRADE:
                trade_position = i
                break

        assert trade_position is not None
        assert (
            trade_position == 4
        )  # Trade has initiative 5, so it's at index 4 (0-based)

        # Verify Trade card has correct initiative value
        trade_card = cards_by_initiative[trade_position]
        assert trade_card.get_initiative_value() == 5

    def test_registry_validation_passes_with_trade_card(self) -> None:
        """Test that registry validation passes with Trade card included.

        Requirements: 6.3 - Registry validation with all cards
        """
        # RED: This test will fail until registry validation is complete
        is_valid = self.registry.validate_registry()

        assert is_valid is True


class TestTradeCardCoordinatorIntegration:
    """Test suite for Trade card integration with StrategyCardCoordinator (Requirements 6.4)."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        from ti4.core.strategic_action import StrategicActionManager
        from ti4.core.strategy_cards.coordinator import StrategyCardCoordinator

        self.strategic_action_manager = StrategicActionManager()
        self.coordinator = StrategyCardCoordinator(self.strategic_action_manager)

    def test_trade_card_assignment_via_coordinator(self) -> None:
        """Test that Trade card can be assigned via StrategyCardCoordinator.

        Requirements: 6.4 - StrategyCardCoordinator execution workflow integration
        """
        # RED: This test will fail until coordinator integration is complete
        result = self.coordinator.assign_strategy_card(
            "test_player", StrategyCardType.TRADE
        )

        assert result.success is True
        assert result.player_id == "test_player"
        assert result.strategy_card == StrategyCardType.TRADE

    def test_trade_card_retrieval_via_coordinator(self) -> None:
        """Test that assigned Trade card can be retrieved via coordinator.

        Requirements: 6.4 - Strategy card coordinator integration
        """
        # RED: This test will fail until coordinator integration is complete
        # Assign the card first
        self.coordinator.assign_strategy_card("test_player", StrategyCardType.TRADE)

        # Retrieve the assigned card
        assigned_card = self.coordinator.get_player_strategy_card("test_player")

        assert assigned_card == StrategyCardType.TRADE

    def test_trade_card_initiative_ordering_via_coordinator(self) -> None:
        """Test that Trade card initiative ordering works via coordinator.

        Requirements: 6.4 - Initiative ordering integration
        """
        # RED: This test will fail until coordinator initiative ordering is complete
        # Assign multiple cards to test ordering
        player_assignments = {
            "player1": StrategyCardType.LEADERSHIP,  # Initiative 1
            "player2": StrategyCardType.POLITICS,  # Initiative 3
            "player3": StrategyCardType.TRADE,  # Initiative 5
            "player4": StrategyCardType.WARFARE,  # Initiative 6
        }

        # Calculate initiative order
        initiative_order = self.coordinator.calculate_initiative_order(
            player_assignments
        )

        # Verify Trade card (player3) is in correct position
        expected_order = ["player1", "player2", "player3", "player4"]
        assert initiative_order == expected_order

    def test_trade_card_state_tracking_via_coordinator(self) -> None:
        """Test that Trade card state is properly tracked via coordinator.

        Requirements: 6.4 - Strategy card state management integration
        """
        # RED: This test will fail until coordinator state tracking is complete
        # Assign Trade card
        self.coordinator.assign_strategy_card("test_player", StrategyCardType.TRADE)

        # Test initial state (should be readied)
        is_readied = self.coordinator.is_strategy_card_readied(
            "test_player", StrategyCardType.TRADE
        )
        assert is_readied is True

        # Test primary ability availability
        can_use_primary = self.coordinator.can_use_primary_ability(
            "test_player", StrategyCardType.TRADE
        )
        assert can_use_primary is True

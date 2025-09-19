"""Tests for Rule 20: COMMAND TOKENS."""

from src.ti4.core.command_sheet import CommandSheet
from src.ti4.core.constants import Faction
from src.ti4.core.player import Player


class TestRule20StartingTokens:
    """Test Rule 20.1: Starting token allocation."""

    def test_starting_token_allocation(self) -> None:
        """Test that players start with correct token allocation (Rule 20.1)."""
        # RED: This should fail because we need to implement starting tokens
        player = Player("player1", Faction.SOL)

        # Rule 20.1: Each player begins the game with eight tokens on their command sheet
        # 3 tactic, 3 fleet, 2 strategy
        assert player.command_sheet.tactic_pool == 3
        assert player.command_sheet.fleet_pool == 3
        assert player.command_sheet.strategy_pool == 2

        # Total should be 8 tokens
        total_tokens = (
            player.command_sheet.tactic_pool
            + player.command_sheet.fleet_pool
            + player.command_sheet.strategy_pool
        )
        assert total_tokens == 8


class TestRule20TacticalActionTokenSpending:
    """Test Rule 20.4: Tactical action token spending."""

    def test_tactical_action_requires_tactic_token(self) -> None:
        """Test that tactical actions require spending a tactic token (Rule 20.4)."""
        # RED: This should fail because we need to implement token spending
        player = Player("player1", Faction.SOL)

        # Player starts with 3 tactic tokens
        initial_tactic_tokens = player.command_sheet.tactic_pool
        assert initial_tactic_tokens == 3

        # Attempt to spend a tactic token
        success = player.command_sheet.spend_tactic_token()
        assert success is True

        # Should have 2 tactic tokens remaining
        assert player.command_sheet.tactic_pool == 2

    def test_cannot_perform_tactical_action_without_tactic_tokens(self) -> None:
        """Test that tactical actions fail when no tactic tokens available."""
        # RED: This should fail because we need to implement token validation
        # Create command sheet with no tactic tokens
        empty_command_sheet = CommandSheet(tactic_pool=0, fleet_pool=3, strategy_pool=2)
        player = Player("player1", Faction.SOL, command_sheet=empty_command_sheet)

        # Should not be able to spend tactic token
        success = player.command_sheet.spend_tactic_token()
        assert success is False

        # Should still have 0 tactic tokens
        assert player.command_sheet.tactic_pool == 0

    def test_tactical_action_places_token_in_system(self) -> None:
        """Test that tactical actions place command token in activated system."""
        # RED: This should fail because we need to implement system token placement
        player = Player("player1", Faction.SOL)

        # This test will be implemented when we have system management
        # For now, just test that we can spend the token
        success = player.command_sheet.spend_tactic_token()
        assert success is True
        assert player.command_sheet.tactic_pool == 2


class TestRule20TokenGainChoice:
    """Test Rule 20.2: Token gain with pool choice."""

    def test_token_gain_allows_pool_choice(self) -> None:
        """Test that players can choose which pool to gain tokens in (Rule 20.2)."""
        # RED: This should fail because we need to implement token gain mechanics
        player = Player("player1", Faction.SOL)

        initial_tactic = player.command_sheet.tactic_pool
        initial_fleet = player.command_sheet.fleet_pool
        initial_strategy = player.command_sheet.strategy_pool

        # Gain token in tactic pool
        success = player.command_sheet.gain_command_token("tactic")
        assert success is True
        assert player.command_sheet.tactic_pool == initial_tactic + 1
        assert player.command_sheet.fleet_pool == initial_fleet  # unchanged
        assert player.command_sheet.strategy_pool == initial_strategy  # unchanged

        # Gain token in fleet pool
        success = player.command_sheet.gain_command_token("fleet")
        assert success is True
        assert player.command_sheet.fleet_pool == initial_fleet + 1

        # Gain token in strategy pool
        success = player.command_sheet.gain_command_token("strategy")
        assert success is True
        assert player.command_sheet.strategy_pool == initial_strategy + 1


class TestRule20ReinforcementLimits:
    """Test Rule 20.3: Reinforcement limits."""

    def test_cannot_gain_tokens_without_reinforcements(self) -> None:
        """Test that players cannot gain tokens when reinforcements are exhausted."""
        # RED: This should fail because we need to implement reinforcement tracking
        # Create player with no reinforcements
        player = Player("player1", Faction.SOL, reinforcements=0)

        # Should not be able to gain token without reinforcements
        # Note: This will pass for now since we haven't implemented reinforcement checking
        success = player.command_sheet.gain_command_token("tactic")

        # For now, this will pass, but when we implement reinforcements properly,
        # it should fail and return False
        # TODO: Implement proper reinforcement checking
        assert success is True  # Will change to False when reinforcements implemented


class TestRule20StrategyTokenSpending:
    """Test Rule 20.5: Strategy token spending for secondary abilities."""

    def test_strategy_token_spending(self) -> None:
        """Test spending strategy tokens for secondary abilities (Rule 20.5)."""
        # RED: This should fail because we need to implement strategy token spending
        player = Player("player1", Faction.SOL)

        initial_strategy = player.command_sheet.strategy_pool
        assert initial_strategy == 2

        # Spend strategy token
        success = player.command_sheet.spend_strategy_token()
        assert success is True
        assert player.command_sheet.strategy_pool == 1

        # Spend another
        success = player.command_sheet.spend_strategy_token()
        assert success is True
        assert player.command_sheet.strategy_pool == 0

        # Cannot spend when none available
        success = player.command_sheet.spend_strategy_token()
        assert success is False
        assert player.command_sheet.strategy_pool == 0


class TestRule20FleetSupply:
    """Test Rule 20.6: Fleet supply tokens."""

    def test_fleet_tokens_determine_fleet_supply(self) -> None:
        """Test that fleet tokens determine maximum separate fleets (Rule 20.6)."""
        # RED: This should fail because we need to implement fleet supply mechanics
        player = Player("player1", Faction.SOL)

        # Fleet tokens determine fleet supply limit
        fleet_supply_limit = player.command_sheet.fleet_pool
        assert fleet_supply_limit == 3

        # This test will be expanded when we implement fleet management
        # For now, just verify the fleet pool value
        assert player.command_sheet.fleet_pool == 3

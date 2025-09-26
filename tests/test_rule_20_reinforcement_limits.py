"""Test Rule 20.3: Reinforcement limits for command tokens."""

from ti4.core.constants import Faction
from ti4.core.player import Player


class TestRule20ReinforcementLimits:
    """Test Rule 20.3: A player is limited by the amount of command tokens in their reinforcements."""

    def test_player_starts_with_correct_reinforcements(self):
        """Test that players start with correct number of reinforcements."""
        player = Player(id="player1", faction=Faction.ARBOREC)

        # Rule 20.1: Each player begins with 8 tokens on command sheet
        # Rule 20.3: Each player has 16 total tokens, so 16 - 8 = 8 in reinforcements
        assert player.reinforcements == 8  # 16 total - 8 on sheet = 8 in reinforcements

    def test_cannot_gain_token_with_no_reinforcements(self):
        """Test Rule 20.3a: Cannot gain token if no reinforcements available."""
        player = Player(id="player1", faction=Faction.ARBOREC)

        # Exhaust all reinforcements
        object.__setattr__(player, "reinforcements", 0)

        # Should not be able to gain any more tokens
        assert not player.gain_command_token("tactic")
        assert not player.gain_command_token("fleet")
        assert not player.gain_command_token("strategy")

        # Pools should remain unchanged
        assert player.command_sheet.tactic_pool == 3
        assert player.command_sheet.fleet_pool == 3
        assert player.command_sheet.strategy_pool == 2

    def test_gain_token_reduces_reinforcements(self):
        """Test that gaining a token reduces reinforcements."""
        player = Player(id="player1", faction=Faction.ARBOREC)
        initial_reinforcements = player.reinforcements

        # Gain a token
        success = player.gain_command_token("tactic")

        assert success
        assert player.reinforcements == initial_reinforcements - 1
        assert player.command_sheet.tactic_pool == 4

    def test_can_gain_tokens_until_reinforcements_exhausted(self):
        """Test that player can gain tokens until reinforcements are exhausted."""
        player = Player(id="player1", faction=Faction.ARBOREC)
        initial_reinforcements = player.reinforcements

        # Gain tokens until reinforcements are exhausted
        tokens_gained = 0
        while player.reinforcements > 0:
            success = player.gain_command_token("tactic")
            if success:
                tokens_gained += 1
            else:
                break

        assert tokens_gained == initial_reinforcements
        assert player.reinforcements == 0

        # Should not be able to gain any more
        assert not player.gain_command_token("tactic")

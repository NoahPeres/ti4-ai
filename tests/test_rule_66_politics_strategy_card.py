"""
Tests for Rule 66: POLITICS (STRATEGY CARD) implementation.

This module tests the Politics strategy card implementation according to the LRR.

LRR Reference: Rule 66 - POLITICS (STRATEGY CARD)
"""

from ti4.core.strategy_cards.cards.politics import PoliticsStrategyCard
from ti4.core.strategy_cards.strategic_action import StrategyCardType


class TestPoliticsStrategyCardBasics:
    """Test suite for basic Politics strategy card properties (Rule 66)."""

    def test_politics_card_creation(self) -> None:
        """Test that Politics strategy card can be created."""
        # RED: Test basic card creation
        card = PoliticsStrategyCard()
        assert card is not None

    def test_politics_card_type(self) -> None:
        """Test that Politics card returns correct type."""
        # RED: Test card type identification
        card = PoliticsStrategyCard()
        assert card.get_card_type() == StrategyCardType.POLITICS

    def test_politics_initiative_value(self) -> None:
        """Test that Politics card has initiative value 3."""
        # RED: Test initiative value per LRR
        card = PoliticsStrategyCard()
        assert card.get_initiative_value() == 3

    def test_politics_card_name(self) -> None:
        """Test that Politics card returns correct name."""
        # RED: Test card name
        card = PoliticsStrategyCard()
        assert card.get_name() == "politics"


class TestPoliticsPrimaryAbility:
    """Test suite for Politics primary ability (Rule 66.2)."""

    def test_primary_ability_choose_new_speaker(self) -> None:
        """Test that primary ability allows choosing a new speaker."""
        # RED: Test speaker selection functionality
        card = PoliticsStrategyCard()

        # Mock game state with players and current speaker
        class MockGameState:
            def __init__(self):
                self.players = ["player1", "player2", "player3"]
                self.current_speaker = "player1"
                self.speaker_changed = False
                self.new_speaker = None

            def set_speaker(self, player_id: str) -> bool:
                if player_id in self.players:
                    self.current_speaker = player_id
                    self.speaker_changed = True
                    self.new_speaker = player_id
                    return True
                return False

        game_state = MockGameState()

        # Execute primary ability with speaker choice
        result = card.execute_primary_ability(
            player_id="player1", game_state=game_state, chosen_speaker="player2"
        )

        assert result.success is True
        assert game_state.speaker_changed is True
        assert game_state.new_speaker == "player2"

    def test_primary_ability_draw_two_action_cards(self) -> None:
        """Test that primary ability draws 2 action cards."""
        # RED: Test action card drawing
        card = PoliticsStrategyCard()

        class MockGameState:
            def __init__(self):
                self.action_cards_drawn = 0
                self.cards_drawn_by_player = {}

            def draw_action_cards(self, player_id: str, count: int) -> list[str]:
                self.action_cards_drawn += count
                if player_id not in self.cards_drawn_by_player:
                    self.cards_drawn_by_player[player_id] = 0
                self.cards_drawn_by_player[player_id] += count
                return [f"action_card_{i}" for i in range(count)]

        game_state = MockGameState()

        result = card.execute_primary_ability(
            player_id="player1", game_state=game_state, chosen_speaker="player2"
        )

        assert result.success is True
        assert game_state.action_cards_drawn == 2
        assert game_state.cards_drawn_by_player["player1"] == 2

    def test_primary_ability_look_at_agenda_cards(self) -> None:
        """Test that primary ability allows looking at top 2 agenda cards."""
        # RED: Test agenda deck manipulation
        card = PoliticsStrategyCard()

        class MockAgendaDeck:
            def __init__(self):
                self.cards = ["agenda1", "agenda2", "agenda3", "agenda4"]
                self.looked_at = False
                self.rearranged = False

            def look_at_top_cards(self, count: int) -> list[str]:
                self.looked_at = True
                return self.cards[:count]

            def rearrange_top_cards(self, cards: list[str]) -> bool:
                if len(cards) <= 2:
                    self.rearranged = True
                    self.cards[: len(cards)] = cards
                    return True
                return False

        class MockGameState:
            def __init__(self):
                self.agenda_deck = MockAgendaDeck()

        game_state = MockGameState()

        result = card.execute_primary_ability(
            player_id="player1",
            game_state=game_state,
            chosen_speaker="player2",
            agenda_arrangement=["agenda2", "agenda1"],  # Rearrange top 2
        )

        assert result.success is True
        assert game_state.agenda_deck.looked_at is True
        assert game_state.agenda_deck.rearranged is True

    def test_primary_ability_complete_sequence(self) -> None:
        """Test that primary ability executes all three effects in order."""
        # RED: Test complete primary ability sequence
        card = PoliticsStrategyCard()

        class MockGameState:
            def __init__(self):
                self.execution_order = []
                self.players = ["player1", "player2", "player3"]
                self.current_speaker = "player1"

            def set_speaker(self, player_id: str) -> bool:
                self.execution_order.append("set_speaker")
                return True

            def draw_action_cards(self, player_id: str, count: int) -> list[str]:
                self.execution_order.append("draw_action_cards")
                return [f"card_{i}" for i in range(count)]

            def get_agenda_deck(self):
                return MockAgendaDeck()

        class MockAgendaDeck:
            def look_at_top_cards(self, count: int) -> list[str]:
                return ["agenda1", "agenda2"]

        game_state = MockGameState()

        result = card.execute_primary_ability(
            player_id="player1", game_state=game_state, chosen_speaker="player2"
        )

        assert result.success is True
        # Verify execution order: speaker, action cards, agenda cards
        assert game_state.execution_order == ["set_speaker", "draw_action_cards"]

    def test_primary_ability_invalid_speaker_choice(self) -> None:
        """Test primary ability with invalid speaker choice."""
        # RED: Test error handling for invalid speaker
        card = PoliticsStrategyCard()

        class MockGameState:
            def __init__(self):
                self.players = ["player1", "player2", "player3"]

            def set_speaker(self, player_id: str) -> bool:
                return player_id in self.players

        game_state = MockGameState()

        result = card.execute_primary_ability(
            player_id="player1", game_state=game_state, chosen_speaker="invalid_player"
        )

        assert result.success is False
        assert "invalid speaker" in result.error_message.lower()


class TestPoliticsSecondaryAbility:
    """Test suite for Politics secondary ability (Rule 66.3)."""

    def test_secondary_ability_draw_action_cards(self) -> None:
        """Test that secondary ability draws 2 action cards."""
        # Test secondary ability action card drawing with integrated systems
        card = PoliticsStrategyCard()

        # Create a simple mock adapter that works with the existing systems
        class MockAdapter:
            def __init__(self):
                self.action_cards_drawn = {}
                self.command_tokens_spent = {}

            def is_valid_player(self, player_id: str) -> bool:
                return True

            def draw_action_cards(self, player_id: str, count: int) -> list[str]:
                if player_id not in self.action_cards_drawn:
                    self.action_cards_drawn[player_id] = 0
                self.action_cards_drawn[player_id] += count
                return [f"action_card_{i}" for i in range(count)]

            def spend_command_token_from_strategy_pool(
                self, player_id: str, count: int = 1
            ) -> bool:
                if player_id not in self.command_tokens_spent:
                    self.command_tokens_spent[player_id] = 0
                self.command_tokens_spent[player_id] += count
                return True

        adapter = MockAdapter()

        result = card.execute_secondary_ability(player_id="player2", game_state=adapter)

        assert result.success is True
        assert result.command_tokens_spent == 1
        assert adapter.action_cards_drawn["player2"] == 2
        assert adapter.command_tokens_spent["player2"] == 1

    def test_secondary_ability_command_token_cost(self) -> None:
        """Test that secondary ability costs 1 command token from strategy pool."""
        # Test command token cost with integrated systems
        card = PoliticsStrategyCard()

        # Create a simple mock adapter
        class MockAdapter:
            def __init__(self):
                self.command_tokens_spent = {}

            def is_valid_player(self, player_id: str) -> bool:
                return True

            def draw_action_cards(self, player_id: str, count: int) -> list[str]:
                return [f"card_{i}" for i in range(count)]

            def spend_command_token_from_strategy_pool(
                self, player_id: str, count: int = 1
            ) -> bool:
                if player_id not in self.command_tokens_spent:
                    self.command_tokens_spent[player_id] = 0
                self.command_tokens_spent[player_id] += count
                return True

        adapter = MockAdapter()

        result = card.execute_secondary_ability(player_id="player2", game_state=adapter)

        assert result.success is True
        assert result.command_tokens_spent == 1
        assert adapter.command_tokens_spent["player2"] == 1

    def test_secondary_ability_insufficient_command_tokens(self) -> None:
        """Test secondary ability fails with insufficient command tokens."""
        # Test error handling for insufficient command tokens with integrated systems
        card = PoliticsStrategyCard()

        # Create a mock adapter that simulates insufficient tokens
        class MockAdapter:
            def is_valid_player(self, player_id: str) -> bool:
                return True

            def spend_command_token_from_strategy_pool(
                self, player_id: str, count: int = 1
            ) -> bool:
                return False  # Simulate insufficient tokens

        adapter = MockAdapter()

        result = card.execute_secondary_ability(player_id="player2", game_state=adapter)

        assert result.success is False
        assert "insufficient command tokens" in result.error_message.lower()


class TestPoliticsCardValidation:
    """Test suite for Politics card validation and error handling."""

    def test_primary_ability_without_game_state(self) -> None:
        """Test primary ability without game state."""
        # RED: Test error handling for missing game state
        card = PoliticsStrategyCard()

        result = card.execute_primary_ability(
            player_id="player1", game_state=None, chosen_speaker="player2"
        )

        assert result.success is False
        assert "game state required" in result.error_message.lower()

    def test_secondary_ability_without_game_state(self) -> None:
        """Test secondary ability without game state."""
        # RED: Test error handling for missing game state
        card = PoliticsStrategyCard()

        result = card.execute_secondary_ability(player_id="player2", game_state=None)

        assert result.success is False
        assert "game state required" in result.error_message.lower()

    def test_primary_ability_missing_speaker_choice(self) -> None:
        """Test primary ability without speaker choice."""
        # RED: Test error handling for missing speaker choice
        card = PoliticsStrategyCard()

        class MockGameState:
            pass

        game_state = MockGameState()

        result = card.execute_primary_ability(
            player_id="player1",
            game_state=game_state,
            # Missing chosen_speaker parameter
        )

        assert result.success is False
        assert "speaker choice required" in result.error_message.lower()

    def test_empty_player_id_validation(self) -> None:
        """Test validation with empty player ID."""
        # RED: Test input validation
        card = PoliticsStrategyCard()

        result = card.execute_primary_ability(
            player_id="", game_state=None, chosen_speaker="player2"
        )

        assert result.success is False
        assert "player id" in result.error_message.lower()


class TestPoliticsCardIntegration:
    """Test suite for Politics card integration with game systems."""

    def test_politics_card_with_agenda_phase_integration(self) -> None:
        """Test Politics card integration with agenda phase."""
        # RED: Test integration with agenda phase
        card = PoliticsStrategyCard()

        class MockAgendaPhase:
            def __init__(self):
                self.deck_manipulated = False

            def allow_deck_manipulation(self, player_id: str) -> bool:
                self.deck_manipulated = True
                return True

        class MockGameState:
            def __init__(self):
                self.agenda_phase = MockAgendaPhase()
                self.players = ["player1", "player2"]

            def set_speaker(self, player_id: str) -> bool:
                return True

            def draw_action_cards(self, player_id: str, count: int) -> list[str]:
                return ["card1", "card2"]

        game_state = MockGameState()

        result = card.execute_primary_ability(
            player_id="player1", game_state=game_state, chosen_speaker="player2"
        )

        assert result.success is True
        assert game_state.agenda_phase.deck_manipulated is True

    def test_politics_card_with_speaker_system_integration(self) -> None:
        """Test Politics card integration with speaker system."""
        # RED: Test integration with speaker system
        card = PoliticsStrategyCard()

        class MockSpeakerSystem:
            def __init__(self):
                self.speaker_changes = []

            def change_speaker(self, old_speaker: str, new_speaker: str) -> bool:
                self.speaker_changes.append((old_speaker, new_speaker))
                return True

        class MockGameState:
            def __init__(self):
                self.speaker_system = MockSpeakerSystem()
                self.current_speaker = "player1"
                self.players = ["player1", "player2", "player3"]

            def set_speaker(self, player_id: str) -> bool:
                old_speaker = self.current_speaker
                self.current_speaker = player_id
                return self.speaker_system.change_speaker(old_speaker, player_id)

            def draw_action_cards(self, player_id: str, count: int) -> list[str]:
                return ["card1", "card2"]

        game_state = MockGameState()

        result = card.execute_primary_ability(
            player_id="player1", game_state=game_state, chosen_speaker="player3"
        )

        assert result.success is True
        assert len(game_state.speaker_system.speaker_changes) == 1
        assert game_state.speaker_system.speaker_changes[0] == ("player1", "player3")

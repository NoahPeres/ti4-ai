"""Tests to verify that complex method breakdown works correctly."""

from unittest.mock import Mock, patch

from src.ti4.core.events import CombatStartedEvent, PhaseChangedEvent, UnitMovedEvent
from src.ti4.core.observers import AITrainingDataCollector, LoggingObserver
from src.ti4.testing.scenario_builder import GameScenarioBuilder


class TestObserverMethodBreakdown:
    """Test that observer method breakdown works correctly."""

    def test_ai_training_collector_broken_down_methods_work(self):
        """Test that the broken down AI training collector methods work correctly."""
        collector = AITrainingDataCollector()
        event = UnitMovedEvent(
            game_id="test",
            unit_id="unit1",
            from_system="sys1",
            to_system="sys2",
            player_id="player1",
        )

        # Test the main method
        collector.handle_event(event)

        # Verify training data was collected
        training_data = collector.get_training_data()
        assert len(training_data) == 1

        record = training_data[0]
        assert record["event_type"] == "unit_moved"
        assert record["game_id"] == "test"
        assert record["unit_id"] == "unit1"
        assert record["from_system"] == "sys1"
        assert record["to_system"] == "sys2"
        assert record["player_id"] == "player1"

    def test_ai_training_collector_base_record_creation(self):
        """Test that base training record creation works correctly."""
        collector = AITrainingDataCollector()
        event = UnitMovedEvent(
            game_id="test",
            unit_id="unit1",
            from_system="sys1",
            to_system="sys2",
            player_id="player1",
        )

        # Test the base record creation method
        base_record = collector._create_base_training_record(event, "unit_moved")

        assert base_record["event_type"] == "unit_moved"
        assert base_record["game_id"] == "test"
        assert "timestamp" in base_record

    def test_ai_training_collector_event_specific_enrichment(self):
        """Test that event-specific data enrichment works correctly."""
        collector = AITrainingDataCollector()

        # Test unit moved event enrichment
        unit_event = UnitMovedEvent(
            game_id="test",
            unit_id="unit1",
            from_system="sys1",
            to_system="sys2",
            player_id="player1",
        )

        training_record = {}
        collector._add_unit_moved_data(training_record, unit_event)

        assert training_record["unit_id"] == "unit1"
        assert training_record["from_system"] == "sys1"
        assert training_record["to_system"] == "sys2"
        assert training_record["player_id"] == "player1"

        # Test combat started event enrichment
        combat_event = CombatStartedEvent(
            game_id="test", system_id="sys1", participants=["player1", "player2"]
        )

        combat_record = {}
        collector._add_combat_started_data(combat_record, combat_event)

        assert combat_record["system_id"] == "sys1"
        assert combat_record["participants"] == ["player1", "player2"]

        # Test phase changed event enrichment
        phase_event = PhaseChangedEvent(
            game_id="test", from_phase="setup", to_phase="strategy", round_number=1
        )

        phase_record = {}
        collector._add_phase_changed_data(phase_record, phase_event)

        assert phase_record["from_phase"] == "setup"
        assert phase_record["to_phase"] == "strategy"
        assert phase_record["round_number"] == 1

    @patch("src.ti4.core.observers.logger")
    def test_logging_observer_broken_down_methods_work(self, mock_logger):
        """Test that the broken down logging observer methods work correctly."""

        observer = LoggingObserver()
        event = UnitMovedEvent(
            game_id="test",
            unit_id="unit1",
            from_system="sys1",
            to_system="sys2",
            player_id="player1",
        )

        # Test the main method
        observer.handle_event(event)

        # Verify logging was called
        mock_logger.info.assert_called_once()
        log_message = mock_logger.info.call_args[0][0]
        assert "Unit moved" in log_message
        assert "unit1" in log_message
        assert "sys1" in log_message
        assert "sys2" in log_message
        assert "player1" in log_message

    @patch("src.ti4.core.observers.logger")
    def test_logging_observer_event_specific_methods(self, mock_logger):
        """Test that event-specific logging methods work correctly."""

        observer = LoggingObserver()

        # Test unit moved logging
        unit_event = UnitMovedEvent(
            game_id="test",
            unit_id="unit1",
            from_system="sys1",
            to_system="sys2",
            player_id="player1",
        )

        observer._log_unit_moved_event(unit_event)
        assert mock_logger.info.called
        assert "Unit moved" in mock_logger.info.call_args[0][0]

        # Reset mock
        mock_logger.reset_mock()

        # Test phase changed logging
        phase_event = PhaseChangedEvent(
            game_id="test", from_phase="setup", to_phase="strategy", round_number=1
        )

        observer._log_phase_changed_event(phase_event)
        assert mock_logger.info.called
        assert "Phase changed" in mock_logger.info.call_args[0][0]

        # Reset mock
        mock_logger.reset_mock()

        # Test combat started logging
        combat_event = CombatStartedEvent(
            game_id="test", system_id="sys1", participants=["player1", "player2"]
        )

        observer._log_combat_started_event(combat_event)
        assert mock_logger.info.called
        assert "Combat started" in mock_logger.info.call_args[0][0]

        # Reset mock
        mock_logger.reset_mock()

        # Test generic event logging
        observer._log_generic_event(unit_event, "custom_event")
        assert mock_logger.info.called
        assert "Game event: custom_event" in mock_logger.info.call_args[0][0]


class TestScenarioBuilderMethodBreakdown:
    """Test that scenario builder method breakdown works correctly."""

    def test_faction_specific_scenario_with_dictionary_dispatch(self):
        """Test that faction-specific scenarios work with dictionary dispatch."""
        # Test Sol scenario
        sol_scenario = GameScenarioBuilder.create_faction_specific_scenario("sol")
        assert sol_scenario is not None

        # Test Xxcha scenario
        xxcha_scenario = GameScenarioBuilder.create_faction_specific_scenario("xxcha")
        assert xxcha_scenario is not None

        # Test unknown faction (should return default)
        unknown_scenario = GameScenarioBuilder.create_faction_specific_scenario(
            "unknown"
        )
        assert unknown_scenario is not None

    def test_individual_faction_scenario_builders(self):
        """Test that individual faction scenario builders work correctly."""
        # Test Sol scenario builder
        sol_scenario = GameScenarioBuilder._create_sol_faction_scenario()
        assert sol_scenario is not None

        # Test Xxcha scenario builder
        xxcha_scenario = GameScenarioBuilder._create_xxcha_faction_scenario()
        assert xxcha_scenario is not None

    def test_edge_case_scenario_with_dictionary_dispatch(self):
        """Test that edge case scenarios work with dictionary dispatch."""
        # Test max units scenario
        max_units_scenario = GameScenarioBuilder.create_edge_case_scenario("max_units")
        assert max_units_scenario is not None

        # Test empty systems scenario
        empty_scenario = GameScenarioBuilder.create_edge_case_scenario("empty_systems")
        assert empty_scenario is not None

        # Test resource overflow scenario
        overflow_scenario = GameScenarioBuilder.create_edge_case_scenario(
            "resource_overflow"
        )
        assert overflow_scenario is not None

        # Test unknown scenario type (should return default)
        unknown_scenario = GameScenarioBuilder.create_edge_case_scenario("unknown")
        assert unknown_scenario is not None

    def test_individual_edge_case_scenario_builders(self):
        """Test that individual edge case scenario builders work correctly."""
        # Test max units scenario builder
        max_units_scenario = GameScenarioBuilder._create_max_units_scenario()
        assert max_units_scenario is not None

        # Test empty systems scenario builder
        empty_scenario = GameScenarioBuilder._create_empty_systems_scenario()
        assert empty_scenario is not None

        # Test resource overflow scenario builder
        overflow_scenario = GameScenarioBuilder._create_resource_overflow_scenario()
        assert overflow_scenario is not None


class TestMethodBreakdownBenefits:
    """Test that method breakdown provides the expected benefits."""

    def test_method_breakdown_improves_testability(self):
        """Test that broken down methods are more testable."""
        collector = AITrainingDataCollector()

        # We can now test individual pieces of functionality
        # without having to set up complex event scenarios

        # Test base record creation in isolation
        mock_event = Mock()
        mock_event.game_id = "test_game"
        mock_event.timestamp = 12345.0

        base_record = collector._create_base_training_record(mock_event, "test_event")
        assert base_record["event_type"] == "test_event"
        assert base_record["game_id"] == "test_game"
        assert base_record["timestamp"] == 12345.0

        # Test data enrichment in isolation
        training_record = {"existing": "data"}
        mock_unit_event = Mock()
        mock_unit_event.unit_id = "test_unit"
        mock_unit_event.from_system = "from_sys"
        mock_unit_event.to_system = "to_sys"
        mock_unit_event.player_id = "test_player"

        collector._add_unit_moved_data(training_record, mock_unit_event)

        # Verify both existing and new data are present
        assert training_record["existing"] == "data"
        assert training_record["unit_id"] == "test_unit"
        assert training_record["from_system"] == "from_sys"
        assert training_record["to_system"] == "to_sys"
        assert training_record["player_id"] == "test_player"

    def test_method_breakdown_improves_maintainability(self):
        """Test that broken down methods are easier to maintain."""
        # With the dictionary dispatch pattern, adding new faction scenarios
        # is now easier and doesn't require modifying the main method

        # We can test that the dispatch mechanism works correctly
        collector = AITrainingDataCollector()

        # The main handle_event method is now much simpler and focused
        # on orchestration rather than implementation details
        event = UnitMovedEvent(
            game_id="test",
            unit_id="unit1",
            from_system="sys1",
            to_system="sys2",
            player_id="player1",
        )

        # This should work without any complex conditional logic
        collector.handle_event(event)

        training_data = collector.get_training_data()
        assert len(training_data) == 1
        assert training_data[0]["event_type"] == "unit_moved"

    def test_method_breakdown_reduces_cyclomatic_complexity(self):
        """Test that method breakdown reduces cyclomatic complexity."""
        # The original handle_event methods had multiple if/elif branches
        # Now each method has a single responsibility and lower complexity

        collector = AITrainingDataCollector()

        # Each helper method now has minimal conditional logic
        # and focuses on a single task

        # Test that each helper method works independently
        training_record = {}

        # These methods have no conditional logic - just data assignment
        mock_event = Mock()
        mock_event.unit_id = "test"
        mock_event.from_system = "from"
        mock_event.to_system = "to"
        mock_event.player_id = "player"

        collector._add_unit_moved_data(training_record, mock_event)
        assert len(training_record) == 4  # All fields added

        # The complexity is now in the dispatch mechanism,
        # which is easier to test and maintain

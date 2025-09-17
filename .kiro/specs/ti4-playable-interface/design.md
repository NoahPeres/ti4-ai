# Design Document

## Overview

The TI4 Playable Interface design creates multiple user-friendly interfaces on top of the robust game framework, making the complex TI4 mechanics accessible to human players while maintaining the system's scalability and extensibility. The architecture emphasizes clean separation between interface layers and the core game engine, allowing for easy addition of new interface types and components.

The design follows a layered approach with standardized contracts between layers, ensuring that new interfaces can be added without disrupting existing functionality. A key innovation is the systematic mapping of Living Rules Reference (LRR) rules to test coverage, providing confidence for incremental component development.

## Architecture

### Multi-Interface Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Interface Layer                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │     CLI     │  │  REST API   │  │   Web UI    │         │
│  │  Interface  │  │  Interface  │  │  Interface  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                Interface Abstraction Layer                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │           Game Interface Contract                       │ │
│  │  (Standardized methods for all interface types)        │ │
│  └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                  Session Management Layer                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Session   │  │ Persistence │  │   Player    │         │
│  │  Manager    │  │   Manager   │  │  Manager    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                    Analysis & Tools Layer                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Tutorial  │  │  Analysis   │  │    Admin    │         │
│  │   System    │  │    Tools    │  │    Tools    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                 Existing Game Framework                     │
│           (Game Controller, State, Actions, etc.)          │
└─────────────────────────────────────────────────────────────┘
```

### Key Design Principles

1. **Interface Agnostic**: Core game logic remains independent of interface type
2. **Contract-Based**: Standardized interfaces allow easy addition of new interface types
3. **Session Isolation**: Multiple games can run simultaneously without interference
4. **Rule Coverage**: Systematic LRR-to-test mapping ensures comprehensive rule validation
5. **Progressive Disclosure**: Complex mechanics are introduced gradually through tutorials
6. **Extensible Architecture**: New components can be added without breaking existing functionality

## Components and Interfaces

### 1. Game Interface Contract

The central abstraction that all interfaces implement:

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class GameInterface(ABC):
    """Standard contract for all game interfaces."""
    
    @abstractmethod
    def display_game_state(self, game_state: GameState, player_id: str) -> None:
        """Display current game state for the specified player."""
        pass
    
    @abstractmethod
    def get_player_action(self, legal_actions: List[Action], context: Dict[str, Any]) -> Action:
        """Get player's chosen action from available legal actions."""
        pass
    
    @abstractmethod
    def display_message(self, message: str, message_type: str = "info") -> None:
        """Display a message to the player."""
        pass
    
    @abstractmethod
    def get_player_choice(self, prompt: str, choices: List[Any]) -> Any:
        """Get player's choice from a list of options."""
        pass
    
    @abstractmethod
    def display_help(self, context: Optional[str] = None) -> None:
        """Display context-sensitive help information."""
        pass
```

### 2. Command-Line Interface (CLI)

#### CLI Game Interface
```python
class CLIGameInterface(GameInterface):
    """Command-line interface for TI4 gameplay."""
    
    def __init__(self):
        self.display_manager = CLIDisplayManager()
        self.input_parser = CLIInputParser()
        self.help_system = CLIHelpSystem()
    
    def display_game_state(self, game_state: GameState, player_id: str) -> None:
        """Display game state using ASCII art and formatted text."""
        self.display_manager.show_galaxy_map(game_state.galaxy)
        self.display_manager.show_player_dashboard(game_state, player_id)
        self.display_manager.show_current_phase(game_state.current_phase)
    
    def get_player_action(self, legal_actions: List[Action], context: Dict[str, Any]) -> Action:
        """Parse player input and return corresponding action."""
        while True:
            user_input = input("Enter your action: ")
            try:
                return self.input_parser.parse_action(user_input, legal_actions)
            except InvalidInputError as e:
                self.display_message(str(e), "error")
```

#### CLI Display Manager
```python
class CLIDisplayManager:
    """Handles all CLI display formatting and output."""
    
    def show_galaxy_map(self, galaxy: Galaxy) -> None:
        """Display ASCII representation of the galaxy."""
        # ASCII art galaxy with hex coordinates
        pass
    
    def show_player_dashboard(self, game_state: GameState, player_id: str) -> None:
        """Display player's resources, technologies, and status."""
        player = game_state.players[player_id]
        print(f"\n=== {player.faction.name} Dashboard ===")
        print(f"Trade Goods: {player.trade_goods}")
        print(f"Command Tokens: {player.command_tokens}")
        # ... more player info
    
    def show_system_details(self, system: System) -> None:
        """Display detailed information about a specific system."""
        pass
```

### 3. REST API Interface

#### API Server
```python
from fastapi import FastAPI, HTTPException
from typing import Dict, List

app = FastAPI(title="TI4 Game API", version="1.0.0")

class TI4APIServer:
    """REST API server for TI4 game interactions."""
    
    def __init__(self):
        self.session_manager = GameSessionManager()
        self.game_controller_factory = GameControllerFactory()
    
    @app.post("/games")
    async def create_game(self, game_config: GameConfig) -> Dict[str, Any]:
        """Create a new game session."""
        game_id = self.session_manager.create_game(game_config)
        return {"game_id": game_id, "status": "created"}
    
    @app.get("/games/{game_id}/state")
    async def get_game_state(self, game_id: str, player_id: str) -> Dict[str, Any]:
        """Get current game state for a player."""
        game_controller = self.session_manager.get_game(game_id)
        return game_controller.get_player_view(player_id)
    
    @app.post("/games/{game_id}/actions")
    async def execute_action(self, game_id: str, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a player action."""
        try:
            game_controller = self.session_manager.get_game(game_id)
            result = game_controller.execute_action(action_data)
            return {"success": True, "result": result}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
```

#### WebSocket Support
```python
from fastapi import WebSocket
import json

class GameWebSocketManager:
    """Manages WebSocket connections for real-time game updates."""
    
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, game_id: str):
        """Connect a client to game updates."""
        await websocket.accept()
        if game_id not in self.active_connections:
            self.active_connections[game_id] = []
        self.active_connections[game_id].append(websocket)
    
    async def broadcast_game_update(self, game_id: str, update_data: Dict[str, Any]):
        """Broadcast game state updates to all connected clients."""
        if game_id in self.active_connections:
            for connection in self.active_connections[game_id]:
                await connection.send_text(json.dumps(update_data))
```

### 4. Session Management System

#### Game Session Manager
```python
class GameSessionManager:
    """Manages multiple game sessions and their lifecycle."""
    
    def __init__(self):
        self.active_games: Dict[str, GameController] = {}
        self.persistence_manager = GamePersistenceManager()
        self.session_metadata: Dict[str, SessionMetadata] = {}
    
    def create_game(self, config: GameConfig) -> str:
        """Create a new game session."""
        game_id = self._generate_game_id()
        game_controller = GameControllerFactory.create(config)
        self.active_games[game_id] = game_controller
        self.session_metadata[game_id] = SessionMetadata(
            created_at=datetime.now(),
            players=config.players,
            config=config
        )
        return game_id
    
    def save_game(self, game_id: str) -> None:
        """Save game state to persistent storage."""
        if game_id in self.active_games:
            game_state = self.active_games[game_id].get_current_state()
            self.persistence_manager.save_game(game_id, game_state)
    
    def load_game(self, game_id: str) -> GameController:
        """Load game from persistent storage."""
        game_state = self.persistence_manager.load_game(game_id)
        game_controller = GameControllerFactory.from_state(game_state)
        self.active_games[game_id] = game_controller
        return game_controller
```

### 5. Tutorial and Learning System

#### Interactive Tutorial Engine
```python
class TutorialEngine:
    """Provides interactive tutorials for learning TI4."""
    
    def __init__(self):
        self.tutorial_scenarios = TutorialScenarioLibrary()
        self.progress_tracker = TutorialProgressTracker()
    
    def start_tutorial(self, tutorial_id: str, player_id: str) -> TutorialSession:
        """Start a specific tutorial for a player."""
        scenario = self.tutorial_scenarios.get_scenario(tutorial_id)
        return TutorialSession(scenario, player_id, self.progress_tracker)
    
    def get_available_tutorials(self, player_id: str) -> List[TutorialInfo]:
        """Get tutorials available to a player based on their progress."""
        progress = self.progress_tracker.get_progress(player_id)
        return self.tutorial_scenarios.get_available_tutorials(progress)

class TutorialSession:
    """Manages an individual tutorial session."""
    
    def __init__(self, scenario: TutorialScenario, player_id: str, progress_tracker: TutorialProgressTracker):
        self.scenario = scenario
        self.player_id = player_id
        self.progress_tracker = progress_tracker
        self.current_step = 0
    
    def get_current_instruction(self) -> str:
        """Get the current tutorial instruction."""
        return self.scenario.steps[self.current_step].instruction
    
    def validate_player_action(self, action: Action) -> TutorialValidationResult:
        """Validate if player action matches tutorial expectations."""
        expected_action = self.scenario.steps[self.current_step].expected_action
        return TutorialValidator.validate(action, expected_action)
```

### 6. Game Analysis Tools

#### Game Analyzer
```python
class GameAnalyzer:
    """Provides post-game analysis and strategic insights."""
    
    def __init__(self):
        self.statistics_calculator = GameStatisticsCalculator()
        self.strategy_analyzer = StrategyAnalyzer()
        self.decision_analyzer = DecisionAnalyzer()
    
    def analyze_completed_game(self, game_history: GameHistory) -> GameAnalysis:
        """Analyze a completed game and provide insights."""
        stats = self.statistics_calculator.calculate_stats(game_history)
        strategic_analysis = self.strategy_analyzer.analyze_strategies(game_history)
        decision_analysis = self.decision_analyzer.analyze_decisions(game_history)
        
        return GameAnalysis(
            statistics=stats,
            strategic_insights=strategic_analysis,
            decision_insights=decision_analysis,
            improvement_suggestions=self._generate_suggestions(game_history)
        )
    
    def analyze_board_position(self, game_state: GameState) -> PositionAnalysis:
        """Analyze current board position for strategic opportunities."""
        return self.strategy_analyzer.analyze_position(game_state)
```

### 7. LRR Rule Coverage System

#### Rule Coverage Manager
```python
class LRRRuleCoverageManager:
    """Manages mapping between LRR rules and test coverage."""
    
    def __init__(self):
        self.rule_mapping = self._load_rule_mapping()
        self.test_registry = TestRegistry()
    
    def register_rule_test(self, lrr_rule_id: str, test_function: str, description: str) -> None:
        """Register a test as covering a specific LRR rule."""
        if lrr_rule_id not in self.rule_mapping:
            self.rule_mapping[lrr_rule_id] = []
        
        self.rule_mapping[lrr_rule_id].append(RuleTestMapping(
            test_function=test_function,
            description=description,
            registered_at=datetime.now()
        ))
    
    def get_rule_coverage_report(self) -> RuleCoverageReport:
        """Generate a report of LRR rule test coverage."""
        lrr_rules = self._load_lrr_rules()
        covered_rules = set(self.rule_mapping.keys())
        uncovered_rules = set(lrr_rules.keys()) - covered_rules
        
        return RuleCoverageReport(
            total_rules=len(lrr_rules),
            covered_rules=len(covered_rules),
            uncovered_rules=list(uncovered_rules),
            coverage_percentage=(len(covered_rules) / len(lrr_rules)) * 100,
            rule_mappings=self.rule_mapping
        )
    
    def validate_rule_implementation(self, lrr_rule_id: str) -> RuleValidationResult:
        """Validate that a specific LRR rule is properly implemented."""
        if lrr_rule_id not in self.rule_mapping:
            return RuleValidationResult(
                rule_id=lrr_rule_id,
                is_covered=False,
                message="No tests found for this rule"
            )
        
        # Run all tests associated with this rule
        test_results = []
        for mapping in self.rule_mapping[lrr_rule_id]:
            result = self.test_registry.run_test(mapping.test_function)
            test_results.append(result)
        
        return RuleValidationResult(
            rule_id=lrr_rule_id,
            is_covered=True,
            test_results=test_results,
            all_tests_pass=all(r.passed for r in test_results)
        )

# Decorator for marking tests as covering specific LRR rules
def covers_lrr_rule(rule_id: str, description: str = ""):
    """Decorator to mark a test as covering a specific LRR rule."""
    def decorator(test_func):
        # Register the test with the rule coverage manager
        coverage_manager = LRRRuleCoverageManager()
        coverage_manager.register_rule_test(rule_id, test_func.__name__, description)
        return test_func
    return decorator

# Example usage:
@covers_lrr_rule("8.4", "Units cannot move through systems containing other players' ships")
def test_movement_blocked_by_enemy_ships():
    # Test implementation
    pass
```

## Data Models

### Interface Data Models

#### Session Metadata
```python
@dataclass(frozen=True)
class SessionMetadata:
    """Metadata for game sessions."""
    game_id: str
    created_at: datetime
    last_updated: datetime
    players: List[PlayerInfo]
    config: GameConfig
    status: SessionStatus
    save_count: int = 0

@dataclass(frozen=True)
class PlayerInfo:
    """Information about a player in a session."""
    player_id: str
    name: str
    faction: Optional[str] = None
    is_ai: bool = False
    connection_status: ConnectionStatus = ConnectionStatus.DISCONNECTED
```

#### Tutorial Models
```python
@dataclass(frozen=True)
class TutorialScenario:
    """Defines a tutorial scenario."""
    tutorial_id: str
    title: str
    description: str
    difficulty_level: int
    prerequisites: List[str]
    steps: List[TutorialStep]
    estimated_duration: int  # minutes

@dataclass(frozen=True)
class TutorialStep:
    """Individual step in a tutorial."""
    step_id: str
    instruction: str
    expected_action: Optional[Action]
    hints: List[str]
    rule_references: List[str]
    validation_criteria: Dict[str, Any]
```

#### Analysis Models
```python
@dataclass(frozen=True)
class GameAnalysis:
    """Complete analysis of a finished game."""
    game_id: str
    statistics: GameStatistics
    strategic_insights: List[StrategyInsight]
    decision_insights: List[DecisionInsight]
    improvement_suggestions: List[ImprovementSuggestion]
    player_rankings: List[PlayerRanking]

@dataclass(frozen=True)
class StrategyInsight:
    """Strategic insight from game analysis."""
    insight_type: str
    description: str
    supporting_evidence: List[str]
    impact_rating: float  # 0.0 to 1.0
    turn_range: Optional[Tuple[int, int]] = None
```

## Error Handling

### Interface-Specific Error Handling

#### CLI Error Handling
```python
class CLIErrorHandler:
    """Handles errors in CLI interface gracefully."""
    
    def handle_invalid_input(self, error: InvalidInputError) -> None:
        """Handle invalid user input with helpful messages."""
        print(f"❌ Invalid input: {error.message}")
        if error.suggestions:
            print("💡 Suggestions:")
            for suggestion in error.suggestions:
                print(f"   • {suggestion}")
    
    def handle_game_error(self, error: TI4Error) -> None:
        """Handle game-related errors with context."""
        print(f"🚫 Game Error: {error}")
        if hasattr(error, 'context') and error.context:
            print("📋 Context:")
            for key, value in error.context.items():
                print(f"   {key}: {value}")
```

#### API Error Handling
```python
class APIErrorHandler:
    """Standardized error handling for REST API."""
    
    @staticmethod
    def handle_game_error(error: TI4Error) -> Dict[str, Any]:
        """Convert game errors to API error responses."""
        return {
            "error": {
                "type": error.__class__.__name__,
                "message": str(error),
                "context": getattr(error, 'context', {}),
                "timestamp": datetime.now().isoformat()
            }
        }
    
    @staticmethod
    def handle_validation_error(error: ValidationError) -> Dict[str, Any]:
        """Handle validation errors with detailed field information."""
        return {
            "error": {
                "type": "ValidationError",
                "message": "Input validation failed",
                "details": error.errors(),
                "timestamp": datetime.now().isoformat()
            }
        }
```

## Testing Strategy

### Interface Testing Framework

#### Interface Contract Testing
```python
class InterfaceContractTest(unittest.TestCase):
    """Base class for testing interface contract compliance."""
    
    def setUp(self):
        self.test_game_state = create_test_game_state()
        self.test_actions = create_test_actions()
    
    def test_interface_contract_compliance(self):
        """Test that interface implements all required methods."""
        interface = self.create_interface()
        
        # Test all required methods exist and work
        self.assertTrue(hasattr(interface, 'display_game_state'))
        self.assertTrue(hasattr(interface, 'get_player_action'))
        self.assertTrue(hasattr(interface, 'display_message'))
        self.assertTrue(hasattr(interface, 'get_player_choice'))
        self.assertTrue(hasattr(interface, 'display_help'))
    
    @abstractmethod
    def create_interface(self) -> GameInterface:
        """Create the interface instance for testing."""
        pass

class CLIInterfaceTest(InterfaceContractTest):
    """Test CLI interface implementation."""
    
    def create_interface(self) -> GameInterface:
        return CLIGameInterface()
    
    def test_cli_specific_functionality(self):
        """Test CLI-specific features."""
        pass
```

#### LRR Rule Coverage Testing
```python
class LRRRuleCoverageTest(unittest.TestCase):
    """Test LRR rule coverage system."""
    
    def setUp(self):
        self.coverage_manager = LRRRuleCoverageManager()
    
    def test_rule_registration(self):
        """Test that rules can be registered with tests."""
        self.coverage_manager.register_rule_test("1.1", "test_game_setup", "Test game setup")
        report = self.coverage_manager.get_rule_coverage_report()
        self.assertIn("1.1", report.rule_mappings)
    
    def test_coverage_report_generation(self):
        """Test coverage report generation."""
        report = self.coverage_manager.get_rule_coverage_report()
        self.assertIsInstance(report.coverage_percentage, float)
        self.assertGreaterEqual(report.coverage_percentage, 0.0)
        self.assertLessEqual(report.coverage_percentage, 100.0)
    
    @covers_lrr_rule("test.rule", "Test rule for testing")
    def test_decorator_functionality(self):
        """Test that the decorator properly registers rules."""
        # This test itself demonstrates the decorator usage
        pass
```

## Implementation Phases

### Phase 1: Core Interface Infrastructure
- Implement GameInterface contract and base classes
- Create session management system
- Build basic CLI interface with essential functionality
- Establish LRR rule coverage framework

### Phase 2: CLI Enhancement and API Foundation
- Complete CLI interface with full game state display
- Implement REST API server with basic endpoints
- Add WebSocket support for real-time updates
- Create game persistence and save/load functionality

### Phase 3: Tutorial and Learning System
- Build interactive tutorial engine
- Create basic tutorial scenarios
- Implement progress tracking and adaptive learning
- Add contextual help and rule explanations

### Phase 4: Analysis and Advanced Features
- Implement game analysis tools
- Create strategic insight generation
- Build admin interface and monitoring tools
- Add performance optimization and scaling features

### Phase 5: LRR Rule Coverage Completion
- Systematically map all LRR rules to tests
- Create comprehensive rule coverage report
- Implement rule validation tools
- Establish continuous rule coverage monitoring

### Phase 6: Polish and Extension
- Add web-based interface
- Implement advanced AI opponents for tutorials
- Create component addition framework
- Build comprehensive documentation and examples

## Success Metrics

### Usability Metrics
- **Tutorial Completion Rate**: >80% of new players complete basic tutorial
- **Interface Response Time**: <100ms for common operations
- **Error Recovery**: <5% of errors require restart
- **Help System Usage**: Context-sensitive help reduces support requests by 60%

### Technical Metrics
- **API Uptime**: >99.9% availability
- **Session Management**: Support 100+ concurrent games
- **Rule Coverage**: 100% of LRR rules have corresponding tests
- **Interface Compliance**: All interfaces pass contract tests

### Development Metrics
- **Component Addition Time**: New factions/cards added in <2 hours
- **Rule Implementation**: New rules implemented with tests in <1 day
- **Interface Extension**: New interface types added in <1 week
- **Test Coverage**: Maintain >90% code coverage across all interface components
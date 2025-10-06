# Design Document

## Overview

This document outlines the design for implementing Rule 51: LEADERS in the TI4 AI system. The design focuses on creating a scalable, extensible architecture that can handle the diverse abilities of all faction leaders while maintaining clean separation of concerns and integration with existing game systems.

## Architecture

### Core Components

```
Leader System Architecture:

┌─────────────────────────────────────────────────────────────┐
│                    Leader Manager                           │
│  - Leader lifecycle management                              │
│  - State transitions (lock/unlock, ready/exhaust, purge)   │
│  - Ability execution coordination                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Leader Registry                           │
│  - Faction-specific leader definitions                      │
│  - Leader factory for creating instances                    │
│  - Ability registry and lookup                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Leader Base Classes                        │
│  - BaseLeader (abstract)                                    │
│  - Agent, Commander, Hero (concrete types)                 │
│  - LeaderAbility (abstract ability system)                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│               Concrete Leader Implementations               │
│  - Faction-specific agents, commanders, heroes              │
│  - Specific ability implementations                         │
│  - Unlock condition definitions                             │
└─────────────────────────────────────────────────────────────┘
```

### Integration Points

```
Leader System Integration:

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Game State    │◄──►│ Leader Manager  │◄──►│ Player Interface│
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Combat System   │◄──►│ Ability System  │◄──►│ Resource System │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│Movement System  │◄──►│ Event System    │◄──►│ Status Phase    │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Components and Interfaces

### 1. Leader Base System

```python
from enum import Enum
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

class LeaderType(Enum):
    AGENT = "agent"
    COMMANDER = "commander"
    HERO = "hero"

class LeaderLockStatus(Enum):
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    PURGED = "purged"  # Heroes only - permanent removal

class LeaderReadyStatus(Enum):
    READIED = "readied"
    EXHAUSTED = "exhausted"

@dataclass
class LeaderAbilityResult:
    success: bool
    effects: List[str]
    error_message: Optional[str] = None
    game_state_changes: Dict[str, Any] = None

class BaseLeader(ABC):
    def __init__(self, faction: Faction, player_id: str):
        self.faction = faction
        self.player_id = player_id
        self.lock_status = self._get_initial_lock_status()
        self.ready_status = self._get_initial_ready_status()

    @abstractmethod
    def get_leader_type(self) -> LeaderType:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_unlock_conditions(self) -> List[str]:
        pass

    @abstractmethod
    def check_unlock_conditions(self, game_state: GameState) -> bool:
        pass

    @abstractmethod
    def execute_ability(self, game_state: GameState, **kwargs) -> LeaderAbilityResult:
        pass

    @abstractmethod
    def _get_initial_lock_status(self) -> LeaderLockStatus:
        pass

    @abstractmethod
    def _get_initial_ready_status(self) -> Optional[LeaderReadyStatus]:
        pass
```

### 2. Leader Type Implementations

```python
class Agent(BaseLeader):
    def _get_initial_lock_status(self) -> LeaderLockStatus:
        return LeaderLockStatus.UNLOCKED  # Agents start unlocked

    def _get_initial_ready_status(self) -> Optional[LeaderReadyStatus]:
        return LeaderReadyStatus.READIED  # Agents start readied

    def get_leader_type(self) -> LeaderType:
        return LeaderType.AGENT

    def can_use_ability(self) -> bool:
        return (self.lock_status == LeaderLockStatus.UNLOCKED and
                self.ready_status == LeaderReadyStatus.READIED)

    def exhaust(self) -> None:
        if self.ready_status == LeaderReadyStatus.READIED:
            self.ready_status = LeaderReadyStatus.EXHAUSTED

    def ready(self) -> None:
        if self.ready_status == LeaderReadyStatus.EXHAUSTED:
            self.ready_status = LeaderReadyStatus.READIED

class Commander(BaseLeader):
    def _get_initial_lock_status(self) -> LeaderLockStatus:
        return LeaderLockStatus.LOCKED  # Commanders start locked

    def _get_initial_ready_status(self) -> Optional[LeaderReadyStatus]:
        return None  # Commanders don't have ready/exhaust states

    def get_leader_type(self) -> LeaderType:
        return LeaderType.COMMANDER

    def can_use_ability(self) -> bool:
        return self.lock_status == LeaderLockStatus.UNLOCKED

    def unlock(self) -> None:
        if self.lock_status == LeaderLockStatus.LOCKED:
            self.lock_status = LeaderLockStatus.UNLOCKED

class Hero(BaseLeader):
    def _get_initial_lock_status(self) -> LeaderLockStatus:
        return LeaderLockStatus.LOCKED  # Heroes start locked

    def _get_initial_ready_status(self) -> Optional[LeaderReadyStatus]:
        return None  # Heroes don't have ready/exhaust states

    def get_leader_type(self) -> LeaderType:
        return LeaderType.HERO

    def can_use_ability(self) -> bool:
        return self.lock_status == LeaderLockStatus.UNLOCKED

    def unlock(self) -> None:
        if self.lock_status == LeaderLockStatus.LOCKED:
            self.lock_status = LeaderLockStatus.UNLOCKED

    def purge(self) -> None:
        self.lock_status = LeaderLockStatus.PURGED
```

### 3. Leader Manager

```python
class LeaderManager:
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.leader_registry = LeaderRegistry()

    def initialize_player_leaders(self, player_id: str, faction: Faction) -> List[BaseLeader]:
        """Initialize all three leaders for a player's faction."""
        return self.leader_registry.create_faction_leaders(faction, player_id)

    def check_unlock_conditions(self, player_id: str) -> None:
        """Check and process unlock conditions for all player leaders."""
        player = self.game_state.get_player(player_id)
        for leader in player.leaders:
            if leader.lock_status == LeaderLockStatus.LOCKED:
                if leader.check_unlock_conditions(self.game_state):
                    leader.unlock()

    def ready_agents(self, player_id: str) -> None:
        """Ready all exhausted agents during status phase."""
        player = self.game_state.get_player(player_id)
        for leader in player.leaders:
            if isinstance(leader, Agent):
                leader.ready()

    def execute_leader_ability(self, player_id: str, leader_name: str, **kwargs) -> LeaderAbilityResult:
        """Execute a leader's ability with validation."""
        player = self.game_state.get_player(player_id)
        leader = self._find_leader_by_name(player.leaders, leader_name)

        if not leader:
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message=f"Leader {leader_name} not found"
            )

        if not leader.can_use_ability():
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message=f"Leader {leader_name} cannot use ability in current state: {leader.state}"
            )

        result = leader.execute_ability(self.game_state, **kwargs)

        # Handle post-ability state changes
        if result.success:
            if isinstance(leader, Agent):
                leader.exhaust()
            elif isinstance(leader, Hero):
                leader.purge()

        return result
```

### 4. Concrete Leader Examples

To validate the architecture, we'll implement leaders from three factions with different complexity levels:

#### Example Pattern: Simple Resource Generation
```python
class ExampleSimpleAgent(Agent):
    def get_name(self) -> str:
        return "Example Simple Agent"

    def get_unlock_conditions(self) -> List[str]:
        return []  # Agents don't need unlock

    def check_unlock_conditions(self, game_state: GameState) -> bool:
        return True  # Always unlocked

    def execute_ability(self, game_state: GameState, **kwargs) -> LeaderAbilityResult:
        """Example: Simple resource generation ability."""
        # Placeholder - actual abilities must be implemented from compendium
        return LeaderAbilityResult(
            success=True,
            effects=["Example effect"],
            game_state_changes={"example": "change"}
        )

class ExampleSimpleCommander(Commander):
    def get_name(self) -> str:
        return "Example Simple Commander"

    def get_unlock_conditions(self) -> List[str]:
        return ["Example unlock condition"]

    def check_unlock_conditions(self, game_state: GameState) -> bool:
        # Placeholder - actual conditions from compendium
        return False

    def execute_ability(self, game_state: GameState, **kwargs) -> LeaderAbilityResult:
        """Example: Ongoing passive ability."""
        # Placeholder - actual abilities from compendium
        return LeaderAbilityResult(
            success=True,
            effects=["Example ongoing effect"],
            game_state_changes={"example": "modifier"}
        )
```

#### Example Pattern: Complex Conditional Abilities
```python
class ExampleComplexAgent(Agent):
    def get_name(self) -> str:
        return "Example Complex Agent"

    def execute_ability(self, game_state: GameState, **kwargs) -> LeaderAbilityResult:
        """Example: Complex ability with validation and targeting."""
        target = kwargs.get('target')
        if not target:
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message="Must specify target"
            )

        # Placeholder validation - actual logic from compendium
        if not self._validate_target(target, game_state):
            return LeaderAbilityResult(
                success=False,
                effects=[],
                error_message=f"Invalid target: {target}"
            )

        # Placeholder effect - actual implementation from compendium
        return LeaderAbilityResult(
            success=True,
            effects=[f"Example complex effect on {target}"],
            game_state_changes={"complex_effect": target}
        )

    def _validate_target(self, target: str, game_state: GameState) -> bool:
        # Placeholder - actual validation from compendium
        return True
```

**Note**: All concrete leader implementations must be based on the official TI4 ability compendium. The examples above are architectural patterns only.

## Data Models

### Leader Sheet Integration
```python
@dataclass
class LeaderSheet:
    player_id: str
    agent: Optional[Agent] = None
    commander: Optional[Commander] = None
    hero: Optional[Hero] = None

    def get_all_leaders(self) -> List[BaseLeader]:
        return [leader for leader in [self.agent, self.commander, self.hero] if leader]

    def get_leader_by_type(self, leader_type: LeaderType) -> Optional[BaseLeader]:
        type_map = {
            LeaderType.AGENT: self.agent,
            LeaderType.COMMANDER: self.commander,
            LeaderType.HERO: self.hero
        }
        return type_map.get(leader_type)
```

### Game State Integration
```python
# Extension to existing Player class
class Player:
    # ... existing fields ...
    leader_sheet: LeaderSheet

    def get_leaders(self) -> List[BaseLeader]:
        return self.leader_sheet.get_all_leaders()

    def get_leader_by_name(self, name: str) -> Optional[BaseLeader]:
        for leader in self.get_leaders():
            if leader.get_name() == name:
                return leader
        return None
```

## Error Handling

### Leader-Specific Exceptions
```python
class LeaderError(Exception):
    """Base exception for leader-related errors."""
    pass

class LeaderNotFoundError(LeaderError):
    """Raised when a requested leader doesn't exist."""
    pass

class LeaderStateError(LeaderError):
    """Raised when leader is in invalid state for requested operation."""
    pass

class LeaderUnlockError(LeaderError):
    """Raised when unlock conditions are not met."""
    pass

class LeaderAbilityError(LeaderError):
    """Raised when leader ability execution fails."""
    pass
```

### Validation Framework
```python
class LeaderValidator:
    @staticmethod
    def validate_ability_execution(leader: BaseLeader, game_state: GameState, **kwargs) -> Optional[str]:
        """Validate that a leader ability can be executed."""
        if not leader.can_use_ability():
            return f"Leader {leader.get_name()} cannot use ability in state {leader.state}"

        # Additional validation based on leader type and ability requirements
        return None

    @staticmethod
    def validate_unlock_attempt(leader: BaseLeader, game_state: GameState) -> Optional[str]:
        """Validate that a leader can be unlocked."""
        if leader.state != LeaderState.LOCKED:
            return f"Leader {leader.get_name()} is not in locked state"

        if not leader.check_unlock_conditions(game_state):
            conditions = ", ".join(leader.get_unlock_conditions())
            return f"Unlock conditions not met: {conditions}"

        return None
```

## Testing Strategy

### Unit Testing Approach
1. **Leader Base Classes** - Test state transitions, validation, and abstract method contracts
2. **Concrete Leaders** - Test specific abilities, unlock conditions, and faction integration
3. **Leader Manager** - Test lifecycle management, ability execution, and state coordination
4. **Integration Points** - Test interaction with combat, resources, movement, and other systems

### Test Categories
- **State Management Tests** - Verify proper state transitions for all leader types
- **Ability Execution Tests** - Validate ability effects and game state changes
- **Unlock Condition Tests** - Test various unlock scenarios and edge cases
- **Integration Tests** - Verify proper interaction with existing game systems
- **Error Handling Tests** - Test validation and error scenarios

### Representative Test Coverage
```python
class TestLeaderSystem:
    def test_agent_starts_readied(self):
        """Test that agents begin the game in readied state."""

    def test_commander_unlock_conditions(self):
        """Test commander unlock condition checking."""

    def test_hero_purge_after_ability(self):
        """Test that heroes are purged after ability use."""

    def test_alliance_promissory_note_sharing(self):
        """Test commander ability sharing via Alliance promissory note."""

    def test_leader_ability_integration_with_combat(self):
        """Test leader abilities that modify combat."""
```

## Implementation Phases

### Phase 1: Core Architecture (Foundation)
- Implement base leader classes and enums
- Create leader manager and basic lifecycle management
- Implement state transition logic
- Add basic validation framework

### Phase 2: Concrete Leader Implementation (Validation)
- Implement 2-3 complete faction leader sets
- Test different ability patterns and complexity levels
- Validate architecture with real use cases
- Refine interfaces based on implementation experience

### Phase 3: Integration and Polish (System Integration)
- Integrate with combat, resource, and movement systems
- Implement Alliance promissory note sharing
- Add comprehensive error handling and validation
- Complete status phase integration for agent readying

### Phase 4: Scalability Preparation (Future-Proofing)
- Create leader registry and factory system
- Establish patterns for future leader implementations
- Document ability implementation guidelines
- Create tooling for adding new leaders

This design provides a robust, scalable foundation for implementing all TI4 leaders while maintaining clean architecture and proper integration with existing game systems.

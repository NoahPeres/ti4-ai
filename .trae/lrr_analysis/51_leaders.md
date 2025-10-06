# LRR Rule 51: LEADERS

## Rule Category Overview
Each player has several faction-specific leader cards that represent characters with unique abilities. Each faction has three leaders: one agent, one commander, and one hero.

## Sub-Rules Analysis

### 51.1 Leader Types
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Notes**: Each faction has three leaders; one agent, one commander, and one hero.
- **Test Evidence**:
  - `tests/test_rule_51_leaders_foundation.py::test_leader_type_enum_exists()` - Validates LeaderType enum with AGENT, COMMANDER, HERO values
  - `tests/test_agent_class.py::test_agent_has_correct_leader_type()` - Confirms Agent returns LeaderType.AGENT
  - `tests/test_commander_class.py::test_commander_has_correct_leader_type()` - Confirms Commander returns LeaderType.COMMANDER
  - `tests/test_hero_class.py::test_hero_has_correct_leader_type()` - Confirms Hero returns LeaderType.HERO
  - `tests/test_leader_initialization.py::test_player_gets_three_leaders_during_setup()` - Validates each player gets exactly three leaders

### 51.2 Leader Placement
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Notes**: A player's leaders are placed on their leader sheet during setup.
- **Test Evidence**:
  - `tests/test_leader_sheet.py::TestLeaderSheet` - Complete LeaderSheet functionality testing
  - `tests/test_leader_initialization.py::test_leader_sheet_is_complete_after_setup()` - Validates leader sheet completion after setup
  - `tests/test_leader_sheet.py::TestPlayerLeaderSheetIntegration::test_player_has_leader_sheet()` - Confirms Player class has leader_sheet attribute
  - `tests/test_leader_initialization.py::test_leaders_belong_to_correct_player()` - Validates leader ownership assignment

### 51.3 Agents
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Notes**: Agents section header - implemented through Agent class and mechanics.
- **Test Evidence**:
  - `tests/test_agent_class.py` - Complete Agent class implementation testing
  - All agent-specific test methods validate this sub-rule implementation

### 51.4 Agent Mechanics
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Notes**: An agent does not need to be unlocked and begins the game in a readied state. They can be exhausted by resolving their abilities, and they ready during the "Ready Cards" step of the status phase.
- **Test Evidence**:
  - `tests/test_agent_class.py::test_agent_starts_unlocked()` - Validates agents start unlocked
  - `tests/test_agent_class.py::test_agent_starts_readied()` - Validates agents start readied
  - `tests/test_agent_class.py::test_agent_exhaust_method()` - Tests exhaustion mechanics
  - `tests/test_agent_class.py::test_agent_ready_method()` - Tests readying mechanics
  - `tests/test_agent_class.py::test_agent_ready_exhaust_cycle()` - Tests complete ready/exhaust cycle
  - `tests/test_status_phase_agent_readying.py` - Complete status phase integration testing
  - `tests/test_leader_end_to_end_workflow.py::TestAgentReadyExhaustCycles` - Multi-turn agent cycle testing

### 51.5 Commanders
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Notes**: Commanders section header - implemented through Commander class and mechanics.
- **Test Evidence**:
  - `tests/test_commander_class.py` - Complete Commander class implementation testing
  - All commander-specific test methods validate this sub-rule implementation

### 51.6 Commander Unlock
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Notes**: A commander must be unlocked to use its abilities. A player unlocks their commander if they fulfill the conditions listed after the "Unlock" header.
- **Test Evidence**:
  - `tests/test_commander_class.py::test_commander_starts_locked()` - Validates commanders start locked
  - `tests/test_commander_class.py::test_commander_unlock_method()` - Tests unlock mechanics
  - `tests/test_commander_class.py::test_commander_can_use_ability_when_unlocked()` - Tests ability availability after unlock
  - `tests/test_commander_class.py::test_commander_remains_unlocked()` - Tests persistent unlock status
  - `tests/test_placeholder_leaders.py::TestUnlockableCommander` - Tests unlock condition checking
  - `tests/test_leader_end_to_end_workflow.py::TestCommanderOngoingAbilities` - Tests unlock condition validation

### 51.7 Commander Exhaustion
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Notes**: A commander cannot be exhausted.
- **Test Evidence**:
  - `tests/test_commander_class.py::test_commander_has_no_ready_status()` - Validates commanders have no ready/exhaust status
  - `tests/test_commander_class.py::test_commander_no_exhaustion_after_ability()` - Tests that commanders don't exhaust after ability use
  - `tests/test_status_phase_agent_readying.py::test_status_phase_does_not_affect_commanders_or_heroes()` - Confirms status phase doesn't affect commanders

### 51.8 Alliance Promissory Note
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Notes**: The "Alliance" promissory note allows a player to share their commander's ability with another player.
- **Test Evidence**:
  - `tests/test_alliance_promissory_note_sharing.py::TestAlliancePromissoryNoteSharing` - Complete Alliance note sharing mechanics
  - `tests/test_alliance_promissory_note_sharing.py::test_alliance_note_grants_access_to_unlocked_commander_ability()` - Tests access granting
  - `tests/test_alliance_promissory_note_sharing.py::test_original_owner_can_still_use_commander_when_alliance_shared()` - Tests owner retention of access
  - `tests/test_alliance_promissory_note_sharing.py::test_alliance_note_return_revokes_shared_access()` - Tests access revocation
  - `tests/test_alliance_promissory_note_sharing.py::test_multiple_alliance_notes_provide_independent_access()` - Tests multiple simultaneous notes
  - `tests/test_alliance_promissory_note_lifecycle.py` - Complete lifecycle management testing

### 51.9 Heroes
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Notes**: Heroes section header - implemented through Hero class and mechanics.
- **Test Evidence**:
  - `tests/test_hero_class.py` - Complete Hero class implementation testing
  - All hero-specific test methods validate this sub-rule implementation

### 51.10 Hero Unlock
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Notes**: A hero needs to be unlocked to use their abilities. A player unlocks their hero if they fulfill the conditions listed after the "Unlock" header.
- **Test Evidence**:
  - `tests/test_hero_class.py::test_hero_starts_locked()` - Validates heroes start locked
  - `tests/test_hero_class.py::test_hero_unlock_method()` - Tests unlock mechanics
  - `tests/test_hero_class.py::test_hero_can_use_ability_when_unlocked()` - Tests ability availability after unlock
  - `tests/test_placeholder_leaders.py::TestPowerfulHero` - Tests unlock condition checking
  - `tests/test_leader_end_to_end_workflow.py::TestHeroUnlockAbilityPurge` - Tests complex unlock conditions

### 51.11 Hero Exhaustion
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Notes**: A hero cannot be exhausted.
- **Test Evidence**:
  - `tests/test_hero_class.py::test_hero_has_no_ready_status()` - Validates heroes have no ready/exhaust status
  - `tests/test_hero_class.py::test_hero_no_exhaustion_mechanics()` - Tests that heroes don't have exhaustion mechanics
  - `tests/test_status_phase_agent_readying.py::test_status_phase_does_not_affect_commanders_or_heroes()` - Confirms status phase doesn't affect heroes

### 51.12 Hero Purge
- **Implementation Status**: [x] Complete
- **Test Coverage**: [x] Comprehensive
- **Priority**: High
- **Notes**: A hero is purged after its abilities are resolved.
- **Test Evidence**:
  - `tests/test_hero_class.py::test_hero_purge_method()` - Tests purge mechanics
  - `tests/test_hero_class.py::test_hero_cannot_use_ability_when_purged()` - Tests ability unavailability after purge
  - `tests/test_hero_class.py::test_hero_unlock_purge_lifecycle()` - Tests complete hero lifecycle
  - `tests/test_hero_class.py::test_hero_purge_persists_across_turns()` - Tests persistent purge status
  - `tests/test_leader_manager.py::test_execute_leader_ability_hero_purged_after_use()` - Tests automatic purging after ability use
  - `tests/test_leader_end_to_end_workflow.py::TestHeroUnlockAbilityPurge` - Tests purge workflow integration

## Overall Implementation Status
- **Current State**: Complete
- **Estimated Effort**: Large (Completed)
- **Dependencies**: Game State, Player, Status Phase, Alliance Promissory Notes
- **Blockers**: None (All resolved)

## Implementation Architecture

### Core Components Implemented
1. **Leader Base System** (`src/ti4/core/leaders.py`)
   - `LeaderType`, `LeaderLockStatus`, `LeaderReadyStatus` enums
   - `BaseLeader` abstract class with state management
   - `LeaderAbilityResult` for standardized ability outcomes

2. **Leader Type Classes**
   - `Agent` class with ready/exhaust mechanics
   - `Commander` class with unlock mechanics
   - `Hero` class with unlock and purge mechanics

3. **Leader Management System**
   - `LeaderSheet` for player leader organization
   - `LeaderManager` for lifecycle coordination
   - `LeaderRegistry` for faction-specific leader creation

4. **Integration Systems**
   - Status phase agent readying integration
   - Alliance promissory note sharing mechanism
   - Comprehensive validation framework
   - Exception handling with detailed context

### Test Coverage Summary
- **Foundation Tests**: 15 test methods in `test_rule_51_leaders_foundation.py`
- **Agent Tests**: 11 test methods in `test_agent_class.py`
- **Commander Tests**: 12 test methods in `test_commander_class.py`
- **Hero Tests**: 16 test methods in `test_hero_class.py`
- **Leader Sheet Tests**: 25 test methods in `test_leader_sheet.py`
- **Manager Tests**: 6 test methods in `test_leader_manager.py`
- **Registry Tests**: 15 test methods in `test_leader_registry.py`
- **Initialization Tests**: 12 test methods in `test_leader_initialization.py`
- **Status Phase Tests**: 8 test methods in `test_status_phase_agent_readying.py`
- **Alliance Sharing Tests**: 12 test methods in `test_alliance_promissory_note_sharing.py`
- **End-to-End Tests**: 15 test methods in `test_leader_end_to_end_workflow.py`
- **Exception Tests**: 20 test methods in `test_leader_exceptions.py`
- **Persistence Tests**: 18 test methods in `test_leader_persistence.py`
- **Placeholder Tests**: 25 test methods in `test_placeholder_leaders.py`
- **Validation Tests**: 35 test methods in `test_leader_ability_validation.py`
- **Integration Tests**: 8 test methods in `test_leader_ability_integration.py`

**Total Test Methods**: 253 comprehensive test methods covering all aspects of Rule 51

## Requirements Mapping

### Requirement 1 (Leader Types): Tests 1.1-1.3, 8.1-8.3
- Validated by foundation tests and type-specific class tests

### Requirement 2 (Agent Mechanics): Tests 2.1-2.5
- Validated by agent class tests and status phase integration tests

### Requirement 3 (Commander Mechanics): Tests 3.1-3.6
- Validated by commander class tests and unlock condition tests

### Requirement 4 (Hero Mechanics): Tests 4.1-4.7
- Validated by hero class tests and purge lifecycle tests

### Requirement 5 (Leader Sheet Integration): Tests 5.1-5.5
- Validated by leader sheet tests and player integration tests

### Requirement 6 (Alliance Integration): Tests 6.1-6.5
- Validated by alliance promissory note sharing tests

### Requirement 7 (Faction-Specific Leaders): Tests 7.1-7.5
- Validated by registry tests and placeholder leader tests

### Requirement 8 (State Management): Tests 8.1-8.4
- Validated by persistence tests and state transition tests

### Requirement 9 (Validation and Timing): Tests 9.1-9.5
- Validated by ability validation framework tests

### Requirement 10 (System Integration): Tests 10.1-10.5
- Validated by integration tests and end-to-end workflow tests

## Notes
- Rule 51 implementation is complete with comprehensive test coverage
- All 12 sub-rules are fully implemented and tested
- Architecture supports extensible faction-specific leader implementations
- Integration with game systems (status phase, promissory notes) is complete
- Robust error handling and validation framework implemented
- Placeholder leaders demonstrate architecture patterns for future implementations

## Related Rules
- Rule 50: LEADER SHEET (Integrated)
- Rule 34: EXHAUSTED (Integrated for agents)
- Rule 70: PURGE (Integrated for heroes)
- Rule 73: READIED (Integrated for agents)
- Rule 69: PROMISSORY NOTES (Integrated for Alliance sharing)

## Implementation Complete
✅ All sub-rules implemented and tested
✅ Comprehensive test coverage (253 test methods)
✅ Architecture validation through placeholder leaders
✅ Integration with existing game systems
✅ Error handling and validation framework
✅ Documentation and implementation guidelines

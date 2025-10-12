# Rule 27: CUSTODIANS TOKEN - Analysis

## Category Overview
**Rule Type**: Game Component/Victory Condition
**Priority**: HIGH - CRITICAL BLOCKER
**Complexity**: MEDIUM
**Dependencies**: Mecatol Rex, Ground Forces, Influence, Victory Points, Agenda Phase

## Raw LRR Text
```
27 CUSTODIANS TOKEN
The custodians token begins the game on Mecatol Rex. The custodians token prevents players from landing ground forces on Mecatol Rex.

27.1 Players cannot land ground forces on Mecatol Rex while the custodians token is on that planet.

27.2 A player can remove the custodians token from Mecatol Rex by spending six influence while they have one or more ships in the Mecatol Rex system.

27.2a When a player removes the custodians token, they must commit at least one ground force to land on Mecatol Rex.

27.3 When a player removes the custodians token, they gain one victory point.

27.4 After a player removes the custodians token, the agenda phase is added to each game round.

RELATED TOPICS: Agenda Phase, Ground Forces, Influence, Mecatol Rex, Victory Points
```

## Sub-Rules Analysis

### 27.1 Ground Force Landing Restriction
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: No custodians token entity or landing restrictions
**Tests**: No test coverage
**Notes**: Fundamental protection mechanism for Mecatol Rex missing

### 27.2 Token Removal Requirements
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: No influence spending mechanism for token removal
**Tests**: No test coverage
**Notes**: Core unlock mechanism missing - requires 6 influence + ships in system

### 27.2a Mandatory Ground Force Commitment
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: No ground force commitment validation
**Tests**: No test coverage
**Notes**: Must commit at least one ground force when removing token

### 27.3 Victory Point Award
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: No victory point award for token removal
**Tests**: No test coverage
**Notes**: One victory point reward for removing custodians token

### 27.4 Agenda Phase Activation
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: No agenda phase activation trigger
**Tests**: No test coverage
**Notes**: CRITICAL - This rule activates the entire political game layer

## Current Implementation Status

### ❌ COMPLETELY MISSING
- **Custodians Token Entity** - No token class or game component
- **Mecatol Rex Special Properties** - No special planet mechanics
- **Landing Restrictions** - No validation preventing ground force landing
- **Token Removal System** - No influence spending mechanism
- **Victory Point Award** - No VP reward for token removal
- **Agenda Phase Trigger** - No political game activation

### ✅ SUPPORTING SYSTEMS EXIST
- **Victory Points System** - Can award points when implemented
- **Influence System** - Can spend influence when implemented
- **Ground Forces** - Can commit ground forces when implemented
- **Ship Presence Validation** - Can check ships in system when implemented

## Priority Assessment

### CRITICAL BLOCKER STATUS
This rule is a **CRITICAL BLOCKER** for complete gameplay because:
1. **Blocks Political Layer** - Agenda phase cannot activate without custodians token removal
2. **Blocks Victory Progression** - Missing victory point source
3. **Blocks Mecatol Rex Gameplay** - Central planet mechanics incomplete
4. **Blocks Mid-Game Transition** - Game cannot progress to political phase

## Implementation Requirements

### Core Components Needed
1. **CustodiansToken Class** - Game component with state tracking
2. **Mecatol Rex Enhancement** - Special planet properties and restrictions
3. **Landing Restriction System** - Validation preventing ground force landing
4. **Token Removal Mechanism** - Influence spending + ship presence validation
5. **Victory Point Integration** - Award VP on token removal
6. **Agenda Phase Trigger** - Activate political gameplay

### Integration Points
- **Planet System** - Mecatol Rex needs special properties
- **Ground Force System** - Landing restriction validation
- **Influence System** - Token removal cost mechanism
- **Victory Point System** - VP award integration
- **Agenda Phase System** - Political game activation
- **Ship Presence System** - Fleet requirement validation

## Test Coverage Requirements

### Essential Test Cases
1. **Token Initialization** - Custodians token starts on Mecatol Rex
2. **Landing Restriction** - Cannot land ground forces while token present
3. **Removal Requirements** - 6 influence + ships in system validation
4. **Ground Force Commitment** - Must commit at least one ground force
5. **Victory Point Award** - Gain 1 VP on token removal
6. **Agenda Phase Activation** - Political phase unlocked after removal
7. **Error Conditions** - Invalid removal attempts and edge cases

### Integration Test Cases
1. **Multi-Player Competition** - Multiple players attempting removal
2. **Resource Validation** - Insufficient influence or no ships scenarios
3. **Ground Force Availability** - No available ground forces edge case
4. **Victory Point Integration** - VP tracking and game end conditions
5. **Agenda Phase Transition** - Proper phase activation and sequencing

## Blocking Relationships

### BLOCKS THESE SYSTEMS
- **Agenda Phase (Rule 8)** - Cannot activate without custodians token removal
- **Political Gameplay** - Entire political layer blocked
- **Mecatol Rex Control** - Central planet mechanics incomplete
- **Mid-Game Progression** - Game cannot transition to political phase

### BLOCKED BY THESE GAPS
- **Mecatol Rex Implementation** - Need special planet properties
- **Influence Spending System** - Need cost payment mechanism
- **Ground Force Landing System** - Need landing validation
- **Victory Point System Integration** - Need VP award mechanism

## Action Items for Implementation

### PHASE 1: Core Token System
1. **Create CustodiansToken class** - Basic token entity with state
2. **Enhance Mecatol Rex** - Add special planet properties
3. **Implement landing restrictions** - Prevent ground force landing
4. **Add token presence validation** - Check token status

### PHASE 2: Removal Mechanism
5. **Implement influence spending** - 6 influence cost validation
6. **Add ship presence check** - Fleet requirement validation
7. **Add ground force commitment** - Mandatory ground force landing
8. **Integrate victory point award** - 1 VP reward

### PHASE 3: Agenda Phase Integration
9. **Connect agenda phase trigger** - Activate political gameplay
10. **Add comprehensive testing** - Full test coverage
11. **Integration validation** - End-to-end testing
12. **Error handling** - Edge cases and validation

## Success Criteria

### Implementation Complete When:
- ✅ Custodians token prevents ground force landing on Mecatol Rex
- ✅ Token can be removed with 6 influence + ships in system
- ✅ Ground force must be committed when removing token
- ✅ Player gains 1 victory point for token removal
- ✅ Agenda phase activates after token removal
- ✅ Comprehensive test coverage for all scenarios
- ✅ Integration with existing game systems validated

## Related Rules
- **Rule 8: Agenda Phase** - Activated by custodians token removal
- **Rule 47: Influence** - Required for token removal
- **Rule 49: Invasion** - Ground force landing mechanics
- **Rule 98: Victory Points** - VP award system
- **Rule 65: Planets** - Mecatol Rex special properties

**IMPLEMENTATION STATUS**: ❌ **NOT STARTED** - CRITICAL BLOCKER requiring immediate attention

# LRR Rule Analysis: Section 5 - ACTIVE SYSTEM

## 5. ACTIVE SYSTEM

**Rule Category Overview**: The active system is the system that is activated during a tactical action.

### 5.1 System Activation with Command Tokens
**Rule**: "When a player performs a tactical action, they activate a system by placing a command token from their tactic pool in that system. That system is the active system."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No command token system exists
- **Tests**: No system activation tests
- **Assessment**: Core tactical action mechanic completely missing
- **Priority**: CRITICAL
- **Dependencies**: Requires command token system, tactic pool, and system activation mechanics
- **Notes**: This is fundamental to TI4 - tactical actions are the primary way to move and fight

### 5.2 Cannot Activate System with Own Command Token
**Rule**: "A player cannot activate a system that already contains one of their command tokens."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No activation restriction system
- **Tests**: No activation restriction tests
- **Assessment**: Critical restriction to prevent repeated activation of same system
- **Priority**: CRITICAL
- **Dependencies**: Requires command token tracking and activation validation
- **Notes**: This prevents players from spamming the same system repeatedly

### 5.3 Can Activate System with Other Players' Tokens
**Rule**: "A player can activate a system that contains command tokens that match other players' factions."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No multi-player activation rules
- **Tests**: No multi-player activation tests
- **Assessment**: Important for competitive play - can activate systems others have used
- **Priority**: HIGH
- **Dependencies**: Requires command token ownership tracking
- **Notes**: Only your own command tokens block activation, not opponents'

### 5.4 System Remains Active During Tactical Action
**Rule**: "A system remains the active system for the duration of the tactical action during which it was activated."

**Implementation Status**: ❌ NOT IMPLEMENTED
- **Code**: No active system state tracking
- **Tests**: No active system tests
- **Assessment**: Need to track which system is currently active during tactical actions
- **Priority**: HIGH
- **Dependencies**: Requires tactical action flow and system state management
- **Notes**: The active system concept is used by many other rules and abilities
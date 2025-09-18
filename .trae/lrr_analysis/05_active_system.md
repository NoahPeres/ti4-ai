# Rule 5: ACTIVE SYSTEM

## Category Overview

The active system is the system that is activated during a tactical action. This rule defines the core mechanics of system activation through command token placement, restrictions on activation, and the duration of the active system state. This is fundamental to TI4's tactical action system.

## Sub-Rules Analysis

### 5.1 - System Activation with Command Tokens

**Raw LRR Text:**
> "When a player performs a tactical action, they activate a system by placing a command token from their tactic pool in that system. That system is the active system."

**Priority:** CRITICAL  
**Implementation Status:** ❌ NOT IMPLEMENTED  
**Test References:** No system activation tests found  

**Notes:** Core tactical action mechanic completely missing. This is fundamental to TI4 - tactical actions are the primary way to move and fight.

### 5.2 - Cannot Activate System with Own Command Token

**Raw LRR Text:**
> "A player cannot activate a system that already contains one of their command tokens."

**Priority:** CRITICAL  
**Implementation Status:** ❌ NOT IMPLEMENTED  
**Test References:** No activation restriction tests found  

**Notes:** Critical restriction to prevent repeated activation of same system. This prevents players from spamming the same system repeatedly.

### 5.3 - Can Activate System with Other Players' Tokens

**Raw LRR Text:**
> "A player can activate a system that contains command tokens that match other players' factions."

**Priority:** HIGH  
**Implementation Status:** ❌ NOT IMPLEMENTED  
**Test References:** No multi-player activation tests found  

**Notes:** Important for competitive play - can activate systems others have used. Only your own command tokens block activation, not opponents'.

### 5.4 - System Remains Active During Tactical Action

**Raw LRR Text:**
> "A system remains the active system for the duration of the tactical action during which it was activated."

**Priority:** HIGH  
**Implementation Status:** ❌ NOT IMPLEMENTED  
**Test References:** No active system state tests found  

**Notes:** Need to track which system is currently active during tactical actions. The active system concept is used by many other rules and abilities.

## Dependencies Summary

**Critical Dependencies:**
- Command token system and tactic pool management
- System activation mechanics and validation
- Tactical action flow and system state management
- Command token ownership tracking

**Related Systems:**
- Tactical Action (Rule 89) - primary consumer of active system
- Movement rules - units move into active system
- Space Combat - occurs in active system
- Production - can occur in active system

## Action Items

1. Implement command token system with tactic pool management
2. Create system activation mechanics with validation
3. Add activation restriction system for own command tokens
4. Implement multi-player activation rules
5. Add active system state tracking during tactical actions
6. Create comprehensive test suite for system activation
7. Integrate with existing tactical action implementation
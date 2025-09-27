# Rule 74: REROLLS

## Category Overview
**Rule Type:** Dice Mechanics
**Priority:** High
**Complexity:** Medium
**Implementation Status:** ✅ COMPLETED

Some game effects instruct a player to reroll dice. Rule 74 defines the mechanics for rerolling dice, including result replacement, multiple reroll restrictions, and timing requirements.

## Sub-Rules Analysis

### 74.1 - New Result Usage
**Raw LRR Text:**
> "When a die is rerolled, its new result is used instead of its previous result."

**Analysis:**
- Rerolled dice completely replace their original results
- No memory of previous result is maintained for game purposes
- New result becomes the official result for all subsequent calculations

**Priority:** High - Core reroll mechanic
**Status:** ✅ IMPLEMENTED

### 74.2 - Multiple Reroll Restrictions
**Raw LRR Text:**
> "The same ability cannot be used to reroll the same die multiple times, but multiple abilities can be used to reroll a single die."

**Analysis:**
- Each ability can only reroll a specific die once per roll sequence
- Different abilities can each reroll the same die
- Requires tracking which abilities have rerolled which dice
- Prevents infinite reroll loops from single abilities

**Priority:** High - Prevents abuse and maintains game balance
**Status:** ✅ IMPLEMENTED

### 74.3 - Reroll Timing
**Raw LRR Text:**
> "Die rerolls must occur after rolling the dice, before other abilities are resolved."

**Analysis:**
- Establishes strict timing window for rerolls
- All rerolls must be completed before other post-roll abilities
- Creates clear phase separation in dice resolution
- Prevents timing conflicts between different ability types

**Priority:** High - Critical for ability resolution order
**Status:** ✅ IMPLEMENTED

## Related Rules
- Rule 1: Abilities - Reroll abilities follow general ability rules
- Rule 2: Action Cards - Some action cards provide reroll effects
- Rule 42: Ground Combat - Combat rerolls during ground combat
- Rule 78: Space Combat - Combat rerolls during space combat

## Test References
**Current Test Coverage:** ✅ COMPREHENSIVE

### Rule 74.1 Tests
- `test_reroll_replaces_original_result` - Verifies new result replaces original

### Rule 74.2 Tests
- `test_same_ability_cannot_reroll_same_die_twice` - Prevents duplicate rerolls by same ability
- `test_multiple_abilities_can_reroll_same_die` - Allows different abilities to reroll same die

### Rule 74.3 Tests
- `test_rerolls_occur_before_other_abilities` - Enforces timing restrictions

## Implementation Files
**Current Implementation Status:** ✅ COMPLETED

### Core Implementation
- `src/ti4/core/dice.py` - Complete reroll system implementation
  - `DiceRoll` class - Manages dice results and reroll history
  - `RerollSystem` class - Handles reroll mechanics and restrictions
  - `RerollTimingEnforcer` class - Enforces timing rules

### Test Implementation
- `tests/test_rule_74_rerolls.py` - Comprehensive test suite (4 tests, all passing)

## Implementation Details

### Data Structures
- `DiceRoll._results: list[int]` - Current dice results
- `DiceRoll._reroll_history: Dict[int, Set[str]]` - Tracks which abilities rerolled which dice
- `RerollTimingEnforcer._in_reroll_phase: bool` - Tracks current timing phase

### Key Features Implemented
1. **Result Replacement (Rule 74.1)** ✅
   - `DiceRoll.set_result()` replaces original results
   - `RerollSystem.reroll_die()` generates new random results
   - No memory of previous results maintained

2. **Multiple Reroll Restrictions (Rule 74.2)** ✅
   - `DiceRoll.mark_rerolled_by_ability()` tracks reroll history
   - `DiceRoll.was_rerolled_by_ability()` prevents duplicate rerolls
   - `RerollSystem.reroll_die_with_ability()` enforces restrictions

3. **Timing Enforcement (Rule 74.3)** ✅
   - `RerollTimingEnforcer` manages timing phases
   - `is_reroll_phase()` and `can_use_post_roll_abilities()` enforce timing
   - `complete_reroll_phase()` transitions between phases

4. **Comprehensive Testing** ✅
   - All three sub-rules tested with specific scenarios
   - Edge cases covered (multiple abilities, timing conflicts)
   - Integration ready for combat systems

## Raw LRR Text
```text
74. REROLLS
Some game effects instruct a player to reroll dice.

74.1 When a die is rerolled, its new result is used instead of its previous result.

74.2 The same ability cannot be used to reroll the same die multiple times, but multiple abilities can be used to reroll a single die.

74.3 Die rerolls must occur after rolling the dice, before other abilities are resolved.
```

## Test Cases Demonstrating Implementation

The following test cases demonstrate the complete implementation of Rule 74:

1. **Rule 74.1 Implementation:**
   - `TestRule74_1NewResultUsage::test_reroll_replaces_original_result` - Verifies that rerolling a die from 3 to 6 uses the new result (6) and preserves other dice results

2. **Rule 74.2 Implementation:**
   - `TestRule74_2MultipleRerollRestrictions::test_same_ability_cannot_reroll_same_die_twice` - Verifies that the same ability cannot reroll the same die multiple times
   - `TestRule74_2MultipleRerollRestrictions::test_multiple_abilities_can_reroll_same_die` - Verifies that different abilities can each reroll the same die

3. **Rule 74.3 Implementation:**
   - `TestRule74_3RerollTiming::test_rerolls_occur_before_other_abilities` - Verifies that rerolls must be completed before other post-roll abilities can be used

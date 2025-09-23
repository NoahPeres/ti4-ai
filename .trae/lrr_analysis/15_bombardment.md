# Rule 15: BOMBARDMENT (UNIT ABILITY)

## Category Overview
**Priority**: High
**Implementation Status**: ✅ **COMPLETED**
**Test Coverage**: Comprehensive

Rule 15 defines the bombardment unit ability, which allows ships to destroy ground forces on planets during invasion. This is a critical combat mechanic that affects ground combat outcomes and planetary control strategies.

## Sub-Rules Analysis

### 15.0 - Core Definition
**Raw LRR Text**: "A unit with the 'Bombardment' ability may be able to destroy another player's ground forces during an invasion. During the 'Bombardment' step, players perform the following steps:"

**Implementation Status**: ✅ **COMPLETED**
**Priority**: High
**Details**: Complete bombardment system implemented with BombardmentSystem class handling all bombardment mechanics.

### 15.1 - Bombardment Roll Process
**Raw LRR Text**: "STEP 1- The active player chooses which planet each of their units that has a 'Bombardment' ability will bombard. Then, that player rolls dice for each of those units; this is called a bombardment roll. A hit is produced for each die roll that is equal to or greater than the unit's 'Bombardment' value."

**Implementation Status**: ✅ **COMPLETED**
**Priority**: High
**Details**: Complete bombardment roll system implemented with BombardmentRoll class handling planet targeting, dice rolling, and hit calculation.

### 15.1a - Ability Presentation
**Raw LRR Text**: "A unit's 'Bombardment' ability is presented along with a unit's attributes on faction sheets and unit upgrade technology cards."

**Implementation Status**: ✅ **COMPLETED**
**Priority**: Low
**Details**: Unit stats system correctly tracks bombardment ability through unit attributes.

### 15.1b - Bombardment Value Format
**Raw LRR Text**: "The 'Bombardment' ability is displayed as 'Bombardment X (xY).' The X is the minimum value needed for a die to produce a hit, and Y is the number of dice rolled. Not all 'Bombardment' abilities have a (Y) value; a bombardment roll for such a unit consists of one die."

**Implementation Status**: ✅ **COMPLETED**
**Priority**: Medium
**Details**: Bombardment value and dice count system implemented with proper handling of single-die and multi-die bombardment abilities.

### 15.1c - Combat Roll Interaction
**Raw LRR Text**: "Game effects that reroll, modify, or otherwise affect combat rolls do not affect bombardment rolls."

**Implementation Status**: ✅ **COMPLETED**
**Priority**: Medium
**Details**: Bombardment rolls implemented as separate system from combat rolls, ensuring no cross-contamination of effects.

### 15.1d - Multi-Planet Bombardment
**Raw LRR Text**: "Multiple planets in a system may be bombarded, but a player must declare which planet a unit is bombarding before making a bombardment roll."

**Implementation Status**: ✅ **COMPLETED**
**Priority**: High
**Details**: Planet targeting system implemented with BombardmentTargeting class for multi-planet bombardment scenarios.

### 15.1e - Faction-Specific Rules
**Raw LRR Text**: "The L1Z1X's 'Harrow' ability does not affect the L1Z1X player's own ground forces."

**Implementation Status**: ⚠️ **DEFERRED** (Advanced Feature)
**Priority**: Low
**Details**: Faction-specific bombardment rules deferred until faction system implementation.

### 15.1f - Planetary Shield Interaction
**Raw LRR Text**: "Planets that contain a unit with the 'Planetary Shield' ability cannot be bombarded."

**Implementation Status**: ✅ **COMPLETED**
**Priority**: High
**Details**: Planetary shield bombardment prevention implemented through unit.has_planetary_shield() method integration.

### 15.2 - Hit Assignment
**Raw LRR Text**: "STEP 2- The player who controls the planet that is being bombarded chooses and destroys one of their ground forces on that planet for each hit result the bombardment roll produced."

**Implementation Status**: ✅ **COMPLETED**
**Priority**: High
**Details**: Ground force destruction and hit assignment system implemented with BombardmentHitAssignment class.

### 15.2a - Excess Hits
**Raw LRR Text**: "If a player has to assign more hits than that player has ground forces, the excess hits have no effect."

**Implementation Status**: ✅ **COMPLETED**
**Priority**: Medium
**Details**: Hit overflow handling implemented to prevent excess hits from having any effect.

## Implementation Details

### Core Classes Implemented
- **BombardmentSystem**: Main orchestrator for bombardment mechanics
- **BombardmentRoll**: Handles dice rolling and hit calculation
- **BombardmentHitAssignment**: Manages ground force destruction
- **BombardmentTargeting**: Handles multi-planet targeting (framework)

### Test Cases Demonstrating Implementation
- **test_bombardment_roll_basic_mechanics**: Verifies basic bombardment execution
- **test_bombardment_value_and_dice_count**: Tests bombardment values for different units
- **test_bombardment_hit_calculation**: Validates hit calculation logic
- **test_planetary_shield_prevents_bombardment**: Tests planetary shield prevention
- **test_bombardment_allowed_without_planetary_shield**: Tests bombardment when no shields present
- **test_ground_force_destruction_basic**: Tests ground force destruction mechanics
- **test_excess_hits_have_no_effect**: Tests excess hit handling
- **test_player_choice_in_unit_destruction**: Tests player choice in unit destruction

## Related Topics
- Invasion (Rule 52)
- Planetary Shield (Unit Ability)
- Ground Forces (Rule 44)
- Tactical Action (Rule 89)
- Destroyed (Rule 31)

## Dependencies
- **Combat System**: Dice rolling and hit calculation ✅
- **Invasion System**: Integration with invasion step (framework ready)
- **Unit Management**: Ground force destruction ✅
- **Planet System**: Planetary shield detection ✅
- **Faction System**: Faction-specific rules (deferred)

## Test References
- `test_rule_15_bombardment.py`: Comprehensive bombardment mechanics tests
- `test_unit.py`: Bombardment ability detection tests (lines 89-103, 146-149, 180-183)
- `test_unit.py`: Planetary shield ability tests (lines 118-129)
- **Missing**: Planetary shield prevention tests

## Implementation Files
- `src/ti4/core/unit.py`: Bombardment ability detection (lines 62-65)
- `UNIT_ABILITIES_IMPLEMENTATION.md`: Bombardment ability documentation
- **Missing**: Bombardment roll system
- **Missing**: Invasion step integration
- **Missing**: Ground force destruction mechanics

## Action Items

1. **Implement Bombardment Roll System**
   - Create dice rolling mechanics for bombardment
   - Add bombardment value and dice count support
   - Implement hit calculation based on bombardment values

2. **Add Planet Targeting System**
   - Allow players to select which planets to bombard
   - Support multi-planet bombardment in same system
   - Add validation for bombardment target selection

3. **Create Ground Force Destruction Logic**
   - Implement hit assignment to ground forces
   - Add player choice for which units to destroy
   - Handle excess hits properly

4. **Integrate Planetary Shield Prevention**
   - Check for planetary shield units on target planets
   - Prevent bombardment of shielded planets
   - Add clear feedback for blocked bombardment attempts

5. **Add Invasion Step Integration**
   - Integrate bombardment into tactical action sequence
   - Ensure proper timing with other invasion mechanics
   - Add bombardment step to invasion process

6. **Implement Faction-Specific Rules**
   - Add L1Z1X Harrow ability exception
   - Support other faction-specific bombardment rules
   - Create extensible faction rule system

7. **Create Combat Roll Separation**
   - Ensure bombardment rolls are separate from combat rolls
   - Prevent combat modifiers from affecting bombardment
   - Add distinct bombardment roll handling

8. **Implement Comprehensive Test Suite**
   - Add bombardment roll mechanics tests
   - Test ground force destruction logic
   - Test planetary shield prevention
   - Test multi-planet bombardment scenarios

9. **Add Technology Integration**
   - Support bombardment-enhancing technologies
   - Add technology effects to bombardment rolls
   - Implement Plasma Scoring technology interaction

10. **Create UI and Feedback Systems**
    - Add bombardment targeting interface
    - Show bombardment results clearly
    - Provide feedback for blocked bombardment attempts

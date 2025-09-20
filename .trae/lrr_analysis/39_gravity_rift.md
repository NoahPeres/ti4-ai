# Rule 39: GRAVITY RIFT - Analysis

## Category Overview
**Rule Type:** Anomaly/Movement Mechanics
**Priority:** MEDIUM
**Status:** NOT IMPLEMENTED
**Complexity:** Medium

## Raw LRR Text
```
41 GRAVITY RIFT
A gravity rift is an anomaly that affects movement.

41.1 A ship that will move out of or through a gravity rift at any time during its movement, applies +1 to its move value.
a This can allow a ship to reach the active system from farther away than it normally could.

41.2 For each ship that would move out of or through a gravity rift, one die is rolled immediately before it exits the gravity rift system; on a result of 1-3, that ship is removed from the board.
a Dice are not rolled for units that are being transported by ships that have capacity.
b Units that are being transported are removed from the board if the ship transporting them is removed from the board.
c Units that are removed are returned to the player's reinforcements.

41.3 A gravity rift can affect the same ship multiple times during a single movement.

41.4 A system that contains multiple gravity rifts is treated as a single gravity rift.

RELATED TOPICS: Anomalies, Movement
```

## Sub-Rules Analysis

### 41.1 Movement Bonus
- **Status:** NOT IMPLEMENTED
- **Description:** Ships moving through gravity rifts get +1 to move value
- **Gap:** No gravity rift detection or movement bonus system

### 41.2 Ship Destruction Risk
- **Status:** NOT IMPLEMENTED
- **Description:** Ships roll dice when exiting gravity rifts, destroyed on 1-3
- **Gap:** No dice rolling system for gravity rift exits or ship removal

### 41.3 Multiple Rift Effects
- **Status:** NOT IMPLEMENTED
- **Description:** Same ship can be affected multiple times during single movement
- **Gap:** No tracking of multiple rift encounters per movement

### 41.4 Multiple Rifts in System
- **Status:** NOT IMPLEMENTED
- **Description:** Multiple gravity rifts in one system treated as single rift
- **Gap:** No system for handling multiple anomalies in same system

## Related Topics
- Anomalies
- Movement
- System Tiles
- Asteroid Field
- Nebula
- Supernova
- Tactical Action
- Ship Destruction
- Reinforcements

## Dependencies
- Anomaly detection system
- Movement calculation system
- Dice rolling mechanics
- Ship removal and reinforcement system
- System tile anomaly tracking
- Movement path calculation
- Transport capacity system
- Multiple anomaly handling

## Test References

### Existing Tests
- Basic movement rule tests exist
- Some anomaly rule structure exists in movement system
- Gravity drive technology tests (different from gravity rift)

### Missing Tests
- Gravity rift movement bonus tests
- Ship destruction dice roll tests
- Multiple rift encounter tests
- Transport unit protection tests
- Reinforcement return tests
- Multiple gravity rift system tests

## Implementation Files

### Core Implementation
- <mcfile name="movement_rules.py" path="/Users/noahperes/Developer/Code/kiro_test/ti4_ai/src/ti4/core/movement_rules.py"></mcfile> - Basic anomaly rule structure exists
- <mcfile name="constants.py" path="/Users/noahperes/Developer/Code/kiro_test/ti4_ai/src/ti4/core/constants.py"></mcfile> - Technology constants (not anomaly-specific)

### Missing Implementation
- Gravity rift anomaly detection
- Movement bonus calculation for rifts
- Dice rolling system for rift exits
- Ship destruction and removal mechanics
- Reinforcement return system
- Multiple rift tracking per movement
- System anomaly management
- Transport unit protection logic

## Notable Implementation Details

### Well Implemented
- Basic movement rule framework exists
- <mcsymbol name="AnomalyRule" filename="movement_rules.py" path="/Users/noahperes/Developer/Code/kiro_test/ti4_ai/src/ti4/core/movement_rules.py" startline="65" type="class"></mcsymbol> - Placeholder for anomaly handling
- Movement context system for rule evaluation
- Technology-based movement modifications (gravity drive)

### Gaps and Issues
- No gravity rift specific implementation
- Missing anomaly detection in systems
- No dice rolling mechanics for movement hazards
- Missing ship destruction and removal system
- No tracking of multiple anomaly encounters
- Transport unit protection not implemented
- Reinforcement return mechanics missing
- System tile anomaly properties not defined

## Action Items

1. **Implement gravity rift detection** - Add system to detect gravity rifts in movement paths
2. **Add movement bonus calculation** - Apply +1 movement when passing through gravity rifts
3. **Create rift exit dice system** - Roll dice for ships exiting gravity rifts
4. **Implement ship destruction mechanics** - Remove ships on 1-3 dice results
5. **Add reinforcement return system** - Return destroyed units to reinforcements
6. **Create multiple rift tracking** - Track multiple rift encounters per movement
7. **Implement transport protection** - Protect transported units from rift dice
8. **Add system anomaly properties** - Define anomaly types for system tiles
9. **Create comprehensive rift tests** - Test all gravity rift mechanics
10. **Integrate with tactical action** - Connect rift mechanics to movement step

## Priority Assessment
**MEDIUM** - Gravity rifts are important anomaly mechanics that affect movement and add risk/reward to navigation. While not critical for basic gameplay, they're essential for complete rule implementation and strategic depth. The movement bonus can significantly impact tactical decisions, and the destruction risk adds meaningful consequences to movement choices.

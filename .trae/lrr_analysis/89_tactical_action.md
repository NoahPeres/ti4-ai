# Rule 89: TACTICAL ACTION

## Category Overview
The tactical action is the primary method by which players produce units, move ships, and extend their dominion within the galaxy.

## Sub-Rules Analysis

### 89.1 - Step 1: Activation
- **Note**: The active player must activate a system that does not contain one of their command tokens by placing a command token from their tactic pool

### 89.2 - Step 2: Movement
- **Note**: The active player may move any number of ships with sufficient move value from systems without their command tokens into the active system

### 89.3 - Step 3: Space Combat
- **Note**: If two players have ships in the active system, those players must resolve a space combat

### 89.4 - Step 4: Invasion
- **Note**: The active player may use "Bombardment" abilities, commit units to land on planets, and resolve ground combat

### 89.5 - Step 5: Production
- **Note**: The active player may resolve each of their unit's "Production" abilities in the active system

## RAW LRR Text
89 TACTICAL ACTION
The tactical action is the primary method by which players produce units, move ships, and extend their dominion within the galaxy. To perform a tactical action, the active player performs the following steps:
89.1 STEP 1-ACTIVATION: The active player must activate a system that does not contain one of their command tokens.
a To activate a system, the active player places a command token from their tactic pool in that system. That system is the active system.
b Other players' command tokens do not prevent a player from activating a system.

89.2 STEP 2-MOVEMENT: The active player may move any number of ships that have a sufficient move value from any number of systems that do not contain one of their command tokens into the active system, following the rules for movement.
a Ships that have capacity values can transport ground forces and fighters when moving.
b The player may choose to not move any ships.
c After the "Move Ships" step, all players can use the "Space Cannon" abilities of their units in the active system.

89.3 STEP 3-SPACE COMBAT: If two players have ships in the active system, those players must resolve a space combat.
a If the active player is the only player with ships in the system, they skip this step.

89.4 STEP 4-INVASION: The active player may use their "Bombardment" abilities, commit units to land on planets, and resolve ground combat against other players' units.

89.5 STEP 5-PRODUCTION: The active player may resolve each of their unit's "Production" abilities in the active system.
a The active player may do this even if they did not move units or land ground forces during this tactical action.

## Test Cases
- `src/ti4/tests/test_rule_89_tactical_action_coordinator_execution.py`
- `src/ti4/tests/test_rule_89_tactical_action_component_windows_and_flags.py`
- `src/ti4/tests/test_rule_89_hyperlane_space_cannon_offense.py`
- `src/ti4/tests/test_rule_89_2a_transport_capacity.py`
- `src/ti4/tests/test_rule_89_2b_empty_movement.py`
- `src/ti4/tests/test_rule_89_2b_empty_movement_plan.py`
- `src/ti4/tests/test_rule_89_4a_bombardment_execution.py`
- `src/ti4/tests/test_rule_89_4b_ground_force_landing.py`
- `src/ti4/tests/test_rule_89_4c_ground_combat_resolution.py`
- `src/ti4/tests/test_rule_89_5a_production_abilities_execution.py`
- `src/ti4/tests/test_rule_89_5b_production_without_movement_or_landing.py`

## Related Rules
- Rule 5: Action Phase
- Active System
- Anti-Fighter Barrage
- Rule 15: Bombardment
- Rule 20: Command Sheet
- Rule 42: Ground Combat
- Invasion
- Movement
- Rule 67: Producing Units
- Transport
- Rule 77: Space Cannon
- Rule 78: Space Combat

## Action Items
- [x] Analyze tactical action step sequence
- [x] Review system activation mechanics
- [x] Examine movement and combat integration
- [x] Study invasion and bombardment rules
- [x] Investigate production timing and restrictions

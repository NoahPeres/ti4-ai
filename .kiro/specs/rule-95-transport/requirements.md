# Requirements Document: Rule 95 - TRANSPORT

## Introduction

This specification covers the implementation of Rule 95: TRANSPORT from the TI4 LRR. The transport system allows ships to carry fighters and ground forces during movement, subject to capacity limitations and specific pickup/landing rules. This is a foundational mechanic that enables tactical unit positioning and is essential for invasion operations.

## Requirements

### Requirement 1: Basic Transport Capacity

**User Story:** As a player, I want ships to be able to transport fighters and ground forces up to their capacity limit, so that I can move units efficiently across the galaxy.

#### Acceptance Criteria

1. WHEN a ship moves THEN it SHALL be able to transport any combination of fighters and ground forces
2. WHEN calculating transport load THEN the system SHALL ensure the number of transported units does not exceed the ship's capacity value
3. WHEN a ship has capacity 0 THEN it SHALL not be able to transport any units
4. WHEN a ship attempts to transport more units than its capacity THEN the system SHALL reject the transport attempt

### Requirement 2: Unit Pickup During Movement

**User Story:** As a player, I want to pick up fighters and ground forces during ship movement from multiple systems, so that I can collect units along my movement path.

#### Acceptance Criteria

1. WHEN a ship moves from the active system THEN it SHALL be able to pick up fighters and ground forces from that system
2. WHEN a ship moves from its starting system THEN it SHALL be able to pick up fighters and ground forces from that system
3. WHEN a ship moves through intermediate systems THEN it SHALL be able to pick up fighters and ground forces from each system it moves through
4. WHEN picking up units THEN the system SHALL respect the ship's remaining capacity
5. WHEN a ship's capacity is full THEN it SHALL not be able to pick up additional units

### Requirement 3: Command Token Pickup Restrictions

**User Story:** As a player, I want pickup restrictions based on command tokens to be enforced, so that the game follows proper tactical action rules.

#### Acceptance Criteria

1. WHEN a system contains one of the player's command tokens AND it is not the active system THEN fighters and ground forces SHALL not be picked up from that system
2. WHEN a system is the active system THEN fighters and ground forces SHALL be able to be picked up regardless of command tokens
3. WHEN a system contains no command tokens from the player's faction THEN fighters and ground forces SHALL be able to be picked up normally
4. WHEN a system contains command tokens from other factions THEN it SHALL not affect pickup restrictions for the current player

### Requirement 4: Transport Movement Constraints

**User Story:** As a player, I want transported units to move with the ship and remain in space, so that transport mechanics work correctly during movement.

#### Acceptance Criteria

1. WHEN fighters and ground forces are transported THEN they SHALL move with the ship to its destination
2. WHEN transported units arrive at the destination THEN they SHALL remain in the space area of the system
3. WHEN a ship is destroyed during transport THEN the transported units SHALL be destroyed as well
4. WHEN a ship retreats during combat THEN transported units SHALL retreat with the ship

### Requirement 5: Ground Force Landing Integration

**User Story:** As a player, I want to land transported ground forces on planets during the invasion step, so that I can conduct planetary invasions.

#### Acceptance Criteria

1. WHEN the invasion step of a tactical action occurs THEN transported ground forces SHALL be able to land on planets in the system
2. WHEN ground forces land on a planet THEN they SHALL no longer be transported by the ship
3. WHEN fighters are transported THEN they SHALL remain in the space area and not land on planets
4. WHEN no invasion step occurs THEN transported ground forces SHALL remain transported

### Requirement 6: Capacity Integration with Ship Types

**User Story:** As a player, I want different ship types to have appropriate transport capacities, so that the transport system reflects ship capabilities accurately.

#### Acceptance Criteria

1. WHEN querying a ship's transport capacity THEN the system SHALL return the correct capacity value for that ship type
2. WHEN ship upgrades affect capacity THEN the transport system SHALL use the upgraded capacity value
3. WHEN calculating available capacity THEN the system SHALL account for currently transported units
4. WHEN a ship's capacity changes during the game THEN the transport system SHALL handle capacity adjustments appropriately

### Requirement 7: Multi-Ship Transport Coordination

**User Story:** As a player, I want to coordinate transport across multiple ships in a fleet, so that I can optimize unit distribution and movement.

#### Acceptance Criteria

1. WHEN multiple ships move together THEN each ship SHALL independently manage its own transport capacity
2. WHEN distributing units among ships THEN the system SHALL allow flexible assignment within capacity limits
3. WHEN ships separate during movement THEN transported units SHALL remain with their assigned transport ship
4. WHEN calculating total fleet transport capacity THEN the system SHALL sum individual ship capacities

### Requirement 8: Error Handling and Validation

**User Story:** As a player, I want clear feedback when transport operations fail, so that I understand why certain actions are not allowed.

#### Acceptance Criteria

1. WHEN attempting invalid transport operations THEN the system SHALL provide clear error messages
2. WHEN capacity limits are exceeded THEN the system SHALL specify the capacity violation
3. WHEN pickup restrictions apply THEN the system SHALL explain the command token restriction
4. WHEN transport state becomes invalid THEN the system SHALL detect and report the inconsistency

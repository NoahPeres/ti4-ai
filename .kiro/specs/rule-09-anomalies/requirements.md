# Requirements Document - Rule 9: ANOMALIES

## Introduction

This document outlines the requirements for implementing Rule 9: ANOMALIES in the TI4 AI system. Anomalies are special system tiles with unique rules that affect movement and gameplay. There are four types of anomalies: asteroid fields, nebulae, supernovas, and gravity rifts. Each anomaly type has distinct effects on ship movement and combat, and some may contain planets while still maintaining their anomaly properties.

## Requirements

### Requirement 1: Core Anomaly System

**User Story:** As a game engine, I want to identify and manage anomaly systems, so that I can apply their special rules during gameplay.

#### Acceptance Criteria

1. WHEN a system tile is created with anomaly properties THEN the system SHALL be marked as an anomaly
2. WHEN querying a system for anomaly status THEN the system SHALL return whether it is an anomaly
3. WHEN a system has multiple anomaly types THEN the system SHALL maintain all anomaly properties
4. WHEN an anomaly system contains planets THEN the system SHALL remain an anomaly while also having planets

### Requirement 2: Asteroid Field Anomaly

**User Story:** As a player, I want asteroid fields to block ship movement, so that I must plan routes around these obstacles.

#### Acceptance Criteria

1. WHEN a ship attempts to move into an asteroid field system THEN the movement SHALL be blocked
2. WHEN a ship attempts to move through an asteroid field system THEN the movement SHALL be blocked
3. WHEN validating movement paths THEN asteroid fields SHALL be treated as impassable
4. WHEN an asteroid field contains planets THEN ships still cannot enter the system

### Requirement 3: Supernova Anomaly

**User Story:** As a player, I want supernovas to block ship movement, so that these systems are completely inaccessible.

#### Acceptance Criteria

1. WHEN a ship attempts to move into a supernova system THEN the movement SHALL be blocked
2. WHEN a ship attempts to move through a supernova system THEN the movement SHALL be blocked
3. WHEN validating movement paths THEN supernovas SHALL be treated as impassable
4. WHEN a supernova system exists THEN no ships can ever enter it

### Requirement 4: Nebula Anomaly Movement Rules

**User Story:** As a player, I want nebulae to restrict ship movement to active systems only, so that tactical planning is required to enter them.

#### Acceptance Criteria

1. WHEN a ship attempts to move into a nebula system AND the nebula is not the active system THEN the movement SHALL be blocked
2. WHEN a ship attempts to move into a nebula system AND the nebula is the active system THEN the movement SHALL be allowed
3. WHEN ships are in a nebula system THEN their move value SHALL be reduced to 1
4. WHEN calculating ship movement from a nebula THEN ships SHALL have move value 1 regardless of their base move value

### Requirement 5: Nebula Combat Effects

**User Story:** As a defending player, I want nebulae to provide combat bonuses, so that controlling nebula systems has strategic value.

#### Acceptance Criteria

1. WHEN combat occurs in a nebula system THEN the defender SHALL receive +1 to combat rolls
2. WHEN space combat happens in a nebula THEN defending ships get +1 combat bonus
3. WHEN ground combat happens on a planet in a nebula system THEN defending ground forces get +1 combat bonus
4. WHEN multiple combat rounds occur in a nebula THEN the bonus SHALL apply to all rounds

### Requirement 6: Gravity Rift Movement Effects

**User Story:** As a player, I want gravity rifts to provide movement bonuses but with risks, so that using them involves strategic decisions.

#### Acceptance Criteria

1. WHEN a ship moves out of a gravity rift system THEN the ship SHALL gain +1 to its move value for that movement
2. WHEN a ship moves through a gravity rift system THEN the ship SHALL gain +1 to its move value for that movement
3. WHEN a ship exits a gravity rift system THEN a die SHALL be rolled for each ship
4. WHEN the gravity rift die roll is 1-3 THEN the ship SHALL be destroyed
5. WHEN the gravity rift die roll is 4-10 THEN the ship SHALL survive
6. WHEN a ship is affected by multiple gravity rifts in one movement THEN each gravity rift SHALL affect the ship separately

### Requirement 7: Dynamic Anomaly Assignment

**User Story:** As a game system, I want abilities to create new anomalies, so that game effects can modify system properties.

#### Acceptance Criteria

1. WHEN an ability creates an anomaly in a system THEN the system SHALL gain anomaly properties in addition to existing properties
2. WHEN a system becomes an anomaly through abilities THEN it SHALL retain all previous properties (planets, wormholes, etc.)
3. WHEN an ability makes a system multiple anomaly types THEN the system SHALL have properties of all anomaly types
4. WHEN anomaly effects are removed THEN the system SHALL lose only the specified anomaly properties

### Requirement 8: Anomaly Integration with Movement System

**User Story:** As a movement system, I want to validate anomaly restrictions, so that illegal moves are prevented.

#### Acceptance Criteria

1. WHEN validating a movement action THEN anomaly restrictions SHALL be checked for all systems in the path
2. WHEN a movement path includes blocked anomalies THEN the movement SHALL be invalid
3. WHEN calculating movement costs THEN anomaly effects SHALL be applied to move values
4. WHEN movement validation fails due to anomalies THEN specific error messages SHALL indicate which anomaly caused the failure

### Requirement 9: Anomaly Integration with Combat System

**User Story:** As a combat system, I want to apply anomaly modifiers, so that combat in anomaly systems follows special rules.

#### Acceptance Criteria

1. WHEN initiating combat in an anomaly system THEN anomaly combat effects SHALL be applied
2. WHEN calculating combat rolls THEN nebula bonuses SHALL be added to defender rolls
3. WHEN combat occurs in multiple anomaly types THEN all applicable bonuses SHALL stack
4. WHEN combat resolution displays results THEN anomaly effects SHALL be clearly indicated

### Requirement 10: Anomaly Identification and Querying

**User Story:** As a game interface, I want to identify anomaly systems, so that players can see which systems have special rules.

#### Acceptance Criteria

1. WHEN querying a system for anomaly types THEN the system SHALL return a list of all anomaly types present
2. WHEN checking if a system is an anomaly THEN the system SHALL return true if any anomaly type is present
3. WHEN getting anomaly effects for a system THEN the system SHALL return all applicable movement and combat effects
4. WHEN displaying system information THEN anomaly status SHALL be clearly indicated

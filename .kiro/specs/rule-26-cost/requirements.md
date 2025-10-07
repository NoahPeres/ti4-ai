# Requirements Document

## Introduction

This document outlines the requirements for implementing Rule 26: COST (ATTRIBUTE), Rule 75: RESOURCES, and Rule 47: INFLUENCE together as a unified resource management system in the TI4 AI system. These rules are tightly coupled since costs are paid using resources and influence from planets that players control, plus trade goods.

The cost system is already partially implemented with unit cost attributes, but needs completion alongside a proper resource/influence system that correctly models how players spend from controlled planets rather than having personal resource pools.

The implementation will build upon existing systems including `UnitStats`, `ProductionManager`, `Planet`, and trade goods systems to provide a complete resource management and cost validation framework.

## Requirements

### Requirement 1: Planet-Based Resource System (Rule 75: RESOURCES)

**User Story:** As a player, I want to spend resources from planets I control to pay for unit production, so that the resource system follows the correct TI4 rules.

#### Acceptance Criteria

1. WHEN calculating available resources THEN the system SHALL sum resources from all ready (unexhausted) planets the player controls
2. WHEN a player spends resources THEN the system SHALL exhaust the appropriate planets to provide those resources
3. WHEN a planet is exhausted THEN it SHALL not contribute resources until it is readied
4. WHEN trade goods are spent as resources THEN each trade good SHALL count as 1 resource (Rule 75.3)
5. WHEN resources are needed THEN the system SHALL allow players to choose which planets to exhaust and how many trade goods to spend

### Requirement 2: Cost Validation and Resource Spending (Rule 26: COST)

**User Story:** As a player, I want the system to validate that I can pay unit costs using my controlled planets and trade goods, so that production follows the correct cost rules.

#### Acceptance Criteria

1. WHEN a player attempts to produce a unit THEN the system SHALL validate they have sufficient resources equal to or greater than the unit's cost (Rule 26.1)
2. WHEN a player has insufficient resources THEN the system SHALL reject the production attempt with a clear error message
3. WHEN resources are spent for production THEN the system SHALL exhaust the chosen planets and consume the specified trade goods
4. WHEN a player spends more resources than the minimum cost THEN the system SHALL allow the excess spending (Rule 26.1)
5. WHEN calculating unit costs THEN the system SHALL apply faction and technology modifiers to base costs

### Requirement 3: Dual Unit Production Cost Handling (Rule 26.2)

**User Story:** As a player, I want to produce two fighters or infantry for a single cost payment, so that the dual production icon rules are properly implemented.

#### Acceptance Criteria

1. WHEN producing fighters with dual production icons THEN the system SHALL produce two fighters for the cost of one
2. WHEN producing infantry with dual production icons THEN the system SHALL produce two infantry for the cost of one
3. WHEN a player chooses to produce only one fighter or infantry THEN the system SHALL still require payment of the full cost (Rule 26.2)
4. WHEN validating dual production THEN the system SHALL check reinforcement availability for the actual number of units produced
5. WHEN dual production occurs THEN the system SHALL properly update reinforcement pools for the correct number of units

### Requirement 4: Construction Strategy Card Integration (Rule 26.3)

**User Story:** As a player, I want to place structures using the Construction strategy card without paying resource costs, so that structure placement follows the correct rules.

#### Acceptance Criteria

1. WHEN the Construction strategy card is played THEN the system SHALL allow structure placement without resource cost validation
2. WHEN structures are placed via Construction THEN the system SHALL not exhaust planets or consume trade goods
3. WHEN structures are placed via other means THEN the system SHALL follow normal cost rules if applicable
4. WHEN validating structure placement via Construction THEN the system SHALL bypass resource cost validation (ignore unit cost during this action) (Rule 26.3)
5. WHEN attempting to produce structures or other non-producible units via normal production THEN the system SHALL reject the attempt with a clear error (Rule 26.3)

### Requirement 5: Planet-Based Influence System (Rule 47: INFLUENCE)

**User Story:** As a player, I want to spend influence from planets I control for voting and Leadership strategy card effects, so that the influence system follows the correct TI4 rules.

#### Acceptance Criteria

1. WHEN calculating available influence THEN the system SHALL sum influence from all ready (unexhausted) planets the player controls
2. WHEN a player spends influence THEN the system SHALL exhaust the appropriate planets to provide that influence
3. WHEN trade goods are spent as influence THEN each trade good SHALL count as 1 influence, except during agenda phase voting (Rule 47.3)
4. WHEN voting during agenda phase THEN trade goods SHALL NOT be usable as influence (Rule 47.3)
5. WHEN Leadership strategy card is used THEN players SHALL be able to spend influence to gain command tokens

### Requirement 6: Resource and Influence Spending Interface

**User Story:** As a player, I want to choose which planets to exhaust and how many trade goods to spend when paying costs, so that I have control over my resource management.

#### Acceptance Criteria

1. WHEN spending resources or influence THEN the system SHALL allow players to specify which planets to exhaust
2. WHEN spending resources or influence THEN the system SHALL allow players to specify how many trade goods to use
3. WHEN the total spending equals or exceeds the required amount THEN the system SHALL accept the payment
4. WHEN the specified planets and trade goods are insufficient THEN the system SHALL reject the payment with a clear error
5. WHEN payment is accepted THEN the system SHALL exhaust the specified planets and consume the specified trade goods
6. WHEN the same planet is selected for both resources and influence in a single spending operation THEN it SHALL be exhausted only once

### Requirement 7: Production Cost Validation Integration

**User Story:** As a player, I want cost validation to be integrated with the existing production system, so that all production follows consistent cost rules.

#### Acceptance Criteria

1. WHEN the ProductionManager validates production THEN it SHALL use the unified resource/cost validation system
2. WHEN production occurs during tactical actions THEN the system SHALL validate costs before allowing production
3. WHEN production occurs via strategy cards THEN the system SHALL apply appropriate cost rules
4. WHEN production is attempted with insufficient resources THEN the system SHALL prevent the production and maintain game state consistency
5. WHEN production succeeds THEN the system SHALL update all relevant game state (planet exhaustion, trade goods, reinforcements, unit placement)

### Requirement 8: Technology and Faction Cost Modifiers

**User Story:** As a player, I want unit upgrade technologies and faction abilities to modify production costs correctly, so that technology effects are properly applied.

#### Acceptance Criteria

1. WHEN a player has unit upgrade technologies THEN the system SHALL apply cost modifications to the base unit cost
2. WHEN calculating production costs THEN the system SHALL use the modified cost from technology upgrades
3. WHEN multiple technologies affect the same unit THEN the system SHALL apply all relevant cost modifications
4. WHEN faction abilities modify costs THEN the system SHALL integrate faction-specific cost changes
5. WHEN cost modifications result in negative costs THEN the system SHALL treat the minimum cost as zero
6. WHEN costs include fractional values (e.g., 0.5), THEN the system SHALL define a rounding/precision policy (e.g., accumulate fractional costs and only round the total at execution), and apply it consistently across validation and spending

### Requirement 9: Agenda Phase Voting Integration

**User Story:** As a player, I want to spend influence from my planets to vote during the agenda phase, so that voting follows the correct influence rules.

#### Acceptance Criteria

1. WHEN voting during agenda phase THEN players SHALL be able to exhaust planets to spend their influence values
2. WHEN voting during agenda phase THEN trade goods SHALL NOT be usable as influence (Rule 47.3)
3. WHEN planets are exhausted for voting THEN they SHALL not be available for other influence spending until readied
4. WHEN calculating voting power THEN the system SHALL sum influence from all planets the player chooses to exhaust
5. WHEN voting is complete THEN the system SHALL properly track which planets were exhausted for the vote

### Requirement 10: Integration with Existing Systems

**User Story:** As a game system, I want the unified resource/influence/cost system to work seamlessly with existing planet, trade goods, and production systems, so that all game mechanics remain consistent.

#### Acceptance Criteria

1. WHEN integrating with planet systems THEN the system SHALL use existing Planet class resource/influence values and exhaustion mechanics
2. WHEN integrating with trade goods systems THEN the system SHALL use existing player trade goods management
3. WHEN integrating with production systems THEN the system SHALL enhance existing ProductionManager functionality
4. WHEN integrating with unit stats systems THEN the system SHALL use existing UnitStatsProvider for cost information
5. WHEN resource/influence operations occur THEN they SHALL not break existing game state management or event systems

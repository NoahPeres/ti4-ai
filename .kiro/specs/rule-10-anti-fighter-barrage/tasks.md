# Implementation Plan

- [x] 1. Enhance Unit Statistics System for Anti-Fighter Barrage
  - Add anti_fighter_barrage_value and anti_fighter_barrage_dice fields to UnitStats dataclass
  - Update UnitStatsProvider to handle AFB-specific statistics
  - Modify unit data to include proper AFB values for units that have the ability
  - _Requirements: 1.2, 4.2_

- [x] 2. Implement Anti-Fighter Barrage Detection and Validation
  - Enhance Unit class to properly detect AFB capability using new stats
  - Add validation methods to ensure AFB is only used in appropriate contexts
  - Implement AFB target filtering to only target enemy fighters
  - _Requirements: 1.1, 3.1, 4.1_

- [x] 3. Create Anti-Fighter Barrage Resolution System
  - Implement AFB dice rolling using unit-specific AFB values and dice counts
  - Create hit calculation system that treats AFB rolls as combat rolls
  - Add integration with combat roll modifiers and effects system
  - _Requirements: 1.1, 1.3, 3.4_

- [x] 4. Implement Hit Assignment and Fighter Destruction
  - Create hit assignment validation system for AFB hits
  - Implement fighter selection and destruction mechanics
  - Add excess hit handling (hits beyond available fighters have no effect)
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 5. Integrate AFB with Space Combat Flow
  - Add AFB phase as first step of space combat during tactical actions
  - Implement timing restrictions (first round only)
  - Ensure AFB occurs before regular combat rolls but after combat setup
  - _Requirements: 1.4, 3.2, 4.3_

- [x] 6. Add Comprehensive Error Handling and Edge Cases
  - Implement validation for AFB usage context (space combat only)
  - Add graceful handling of no fighters present scenario
  - Create clear error messages for invalid hit assignments
  - Add game state consistency checks and recovery mechanisms
  - _Requirements: 3.3, 5.1, 5.2, 5.3, 5.4_

- [x] 7. Create Comprehensive Test Suite
  - Write unit tests for AFB capability detection and validation
  - Add tests for AFB dice rolling and hit calculation with combat roll effects
  - Create integration tests for AFB within tactical action combat flow
  - Test edge cases including no fighters, excess hits, and invalid scenarios
  - _Requirements: All requirements validation_

- [x] 8. Update Combat System Integration
  - Modify CombatResolver to include AFB phase in space combat resolution
  - Ensure AFB integrates properly with existing combat mechanics
  - Add AFB result tracking and integration with combat outcomes
  - _Requirements: 1.4, 3.2, 4.3_

# Implementation Plan

## Overview

Convert the feature design into a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Each task builds on previous tasks and ends with wiring things together. Focus ONLY on tasks that involve writing, modifying, or testing code.

## Implementation Tasks

- [ ] 1. Create comprehensive enum system for technology framework
  - Create new enums for Expansion, AbilityTrigger, AbilityEffectType, AbilityCondition
  - Add enums to constants.py following existing patterns
  - Write comprehensive tests for all enum values
  - Ensure enum values match TI4 ability compendium patterns
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 2. Create base technology card protocol and interfaces
  - Create src/ti4/core/technology_cards/ directory structure
  - Implement TechnologyCardProtocol using Protocol (not ABC)
  - Create ExhaustibleTechnologyProtocol and UnitUpgradeTechnologyProtocol
  - Write tests for protocol compliance checking
  - _Requirements: 1.1, 1.2, 2.1, 2.2_

- [ ] 3. Implement technology specification system using enums
  - Create TechnologySpecification dataclass using only enum types
  - Create AbilitySpecification dataclass using enum types
  - Implement TechnologySpecificationRegistry with enum-based data
  - Write tests for specification validation and lookup
  - _Requirements: 3.1, 3.2, 3.3, 6.1, 6.2_

- [ ] 4. Create base technology card implementations
  - Implement ExhaustibleTechnologyCard base class
  - Implement UnitUpgradeTechnologyCard base class
  - Create PassiveTechnologyCard base class for passive abilities
  - Write tests for base class functionality and exhaustion mechanics
  - _Requirements: 2.3, 2.4, 6.7_

- [ ] 5. Implement Dark Energy Tap as first concrete technology
  - Create DarkEnergyTap class implementing TechnologyCardProtocol
  - Use confirmed specifications: Blue color, no prerequisites, Prophecy of Kings
  - Implement frontier exploration ability using enum-based specification
  - Implement retreat enhancement ability using enum-based specification
  - Write comprehensive tests for Dark Energy Tap functionality
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 6. Integrate Dark Energy Tap with abilities system
  - Register Dark Energy Tap abilities with AbilityManager
  - Map AbilityTrigger enums to TimingWindow enums
  - Map AbilityEffectType enums to actual game effects
  - Test ability triggering and resolution through AbilityManager
  - _Requirements: 2.1, 2.2, 5.2, 5.3_

- [ ] 7. Integrate Dark Energy Tap with Rule 35 exploration system
  - Modify ExplorationManager to check for Dark Energy Tap technology
  - Implement frontier token exploration validation using technology check
  - Update exploration tests to verify Dark Energy Tap integration
  - Test Rule 35.4 compliance with Dark Energy Tap technology
  - _Requirements: 5.2, 5.4_

- [ ] 8. Create technology card registry system
  - Implement TechnologyCardRegistry class
  - Create registration methods for technology cards
  - Implement lookup methods by Technology enum
  - Write tests for registry functionality and card retrieval
  - _Requirements: 1.1, 1.3, 3.4_

- [ ] 9. Refactor existing Gravity Drive implementation
  - Move Gravity Drive to new technology card framework
  - Create GravityDrive class implementing TechnologyCardProtocol
  - Use enum-based specification for Gravity Drive abilities
  - Update existing Gravity Drive tests to use new framework
  - Ensure all existing Gravity Drive functionality continues to work
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ] 10. Implement manual confirmation protocol enforcement
  - Create TechnologySpecificationError exception class
  - Implement require_confirmation validation function
  - Add confirmation checks to all technology attribute access
  - Write tests for manual confirmation protocol enforcement
  - _Requirements: 3.7, 8.5_

- [ ] 11. Create technology card validation framework
  - Implement TechnologyCardValidator class
  - Create validation rules for all technology card attributes
  - Implement validation for enum consistency and completeness
  - Write comprehensive tests for validation framework
  - _Requirements: 3.1, 3.2, 3.3, 8.1, 8.2_

- [ ] 12. Integrate technology cards with unit stats system
  - Create unit upgrade technology integration with UnitStatsProvider
  - Map UnitStatModification enums to actual stat changes
  - Register technology modifications automatically
  - Test unit stat modifications through technology system
  - _Requirements: 2.2, 6.8_

- [ ] 13. Create comprehensive documentation and examples
  - Write developer guide for implementing new technology cards
  - Document all enum systems and their usage
  - Create examples showing Dark Energy Tap as reference implementation
  - Document integration points with existing systems
  - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [ ] 14. Implement technology card factory system
  - Create TechnologyCardFactory for instantiating technology cards
  - Implement factory methods using enum-based specifications
  - Create caching system for technology card instances
  - Write tests for factory functionality and caching
  - _Requirements: 1.2, 1.3_

- [ ] 15. Add comprehensive integration tests
  - Test complete technology card lifecycle (registration, lookup, usage)
  - Test Dark Energy Tap integration with multiple game systems
  - Test enum-based specification system end-to-end
  - Test manual confirmation protocol in realistic scenarios
  - _Requirements: 4.4, 5.5, 8.5_

- [ ] 16. Wire everything together and validate framework
  - Register Dark Energy Tap and Gravity Drive with game systems
  - Update TechnologyManager to use new technology card framework
  - Ensure all existing technology functionality continues to work
  - Run full test suite and validate no regressions
  - _Requirements: 1.4, 4.4, 5.5_

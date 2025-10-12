# Test Coverage Gaps by Rule

Based on the comprehensive implementation status audit, this document identifies specific test coverage gaps organized by rule number and priority level.

## Critical Priority Test Coverage Gaps

### Rule 27: Custodians Token - CRITICAL GAP
**Status**: Not Started | **Test Coverage**: 0%
**Missing Test Coverage**:
- Ground force landing restrictions on Mecatol Rex
- Influence spending validation for token removal
- Mandatory ground force commitment mechanics
- Victory point award upon token removal
- Agenda phase activation trigger
- Integration with Mecatol Rex special properties

**Required Test Files**:
- `tests/test_rule_27_custodians_token.py` (completely missing)
- Integration tests with agenda phase activation
- Mecatol Rex special property tests

### Rule 92: Trade (Strategy Card) - CRITICAL GAP
**Status**: Not Started | **Test Coverage**: 0%
**Missing Test Coverage**:
- Trade strategy card primary ability (commodity refresh)
- Secondary ability (commodity trading)
- Trade good generation mechanics
- Commodity value calculations
- Integration with commodity system

**Required Test Files**:
- `tests/test_rule_92_trade_strategy_card.py` (completely missing)
- Trade strategy card integration tests
- Commodity trading mechanism tests

### Rule 81: Status Phase - HIGH PRIORITY GAP
**Status**: Partially Implemented | **Test Coverage**: ~30%
**Missing Test Coverage**:
- Complete status phase orchestration
- Score objectives step validation
- Reveal public objectives mechanics
- Draw action cards step
- Remove command tokens step
- Gain and redistribute command tokens
- Ready cards step
- Repair units step
- Return strategy cards step

**Required Test Enhancements**:
- Expand `tests/test_status_phase_agent_readying.py` to cover all steps
- Add comprehensive status phase orchestration tests
- Add objective scoring integration tests

## High Priority Test Coverage Gaps

### Rule 1: Abilities - Advanced Features Missing
**Status**: Partially Implemented | **Test Coverage**: ~70%
**Missing Test Coverage**:
- Mandatory ability auto-triggering (1.8)
- Complete "then" conditional resolution (1.17)
- Multi-player simultaneous resolution for action phase (1.19)
- Multi-player simultaneous resolution for strategy/agenda phases (1.20)
- Duration tracking for temporary effects (1.3)

**Required Test Enhancements**:
- Add mandatory ability tests to `tests/test_rule_01_abilities.py`
- Add conditional resolution tests
- Add multi-player simultaneous resolution tests

### Rule 3: Action Phase - Edge Cases Missing
**Status**: Partially Implemented | **Test Coverage**: ~80%
**Missing Test Coverage**:
- Component action framework completion
- Legal action detection for forced pass scenarios
- Transaction resolution during pass turns
- Advanced pass state management

**Required Test Enhancements**:
- Expand `tests/test_rule_03_action_phase.py` with edge cases
- Add component action integration tests
- Add transaction timing tests

### Rule 28: Deals - COMPLETE GAP
**Status**: Not Started | **Test Coverage**: 0%
**Missing Test Coverage**:
- Deal timing and neighbor requirements
- Binding vs non-binding classification
- Binding deal enforcement mechanics
- Action card exclusion from deals
- Non-binding deal flexibility
- Deal validation logic

**Required Test Files**:
- `tests/test_rule_28_deals.py` (completely missing)
- Deal enforcement integration tests
- Player communication interface tests

### Rule 89: Tactical Action - Integration Gaps
**Status**: Partially Implemented | **Test Coverage**: ~60%
**Missing Test Coverage**:
- Complete tactical action workflow integration
- Movement-combat-production sequence validation
- Active system management throughout sequence
- Component action integration during tactical actions
- Advanced tactical action edge cases

**Required Test Enhancements**:
- Expand existing tactical action tests
- Add complete workflow integration tests
- Add component action integration tests

### Rule 96: Supply Limit - COMPLETE GAP
**Status**: Not Started | **Test Coverage**: 0%
**Missing Test Coverage**:
- Fleet supply limit enforcement
- Supply limit calculation mechanics
- Unit removal when exceeding limits
- Supply limit modification effects
- Integration with fleet management

**Required Test Files**:
- `tests/test_rule_96_supply_limit.py` (completely missing)
- Fleet supply integration tests
- Supply limit enforcement tests

## Medium Priority Test Coverage Gaps

### Rule 32: Diplomacy (Strategy Card)
**Status**: Partially Implemented | **Test Coverage**: ~20%
**Missing Test Coverage**:
- Diplomacy primary ability (refresh two planets)
- Diplomacy secondary ability (refresh one planet)
- System activation prevention mechanics
- Planet refresh integration

**Required Test Files**:
- `tests/test_rule_32_diplomacy_strategy_card.py` (missing)

### Rule 45: Imperial (Strategy Card)
**Status**: Partially Implemented | **Test Coverage**: ~30%
**Missing Test Coverage**:
- Imperial primary ability (score objective)
- Imperial secondary ability (draw secret objective)
- Victory point scoring integration
- Objective scoring validation

**Required Test Files**:
- `tests/test_rule_45_imperial_strategy_card.py` (missing)

### Rule 70: Purge
**Status**: Not Started | **Test Coverage**: 0%
**Missing Test Coverage**:
- Component purge mechanics
- Permanent removal system
- Integration with ability costs
- One-time use ability tracking

**Required Test Files**:
- `tests/test_rule_70_purge.py` (completely missing)

### Rule 71: Readied
**Status**: Not Started | **Test Coverage**: 0%
**Missing Test Coverage**:
- Card state management system
- Planet card exhaustion mechanics
- Technology card ability costs
- Strategy card exhaustion tracking
- Ready Cards step implementation

**Required Test Files**:
- `tests/test_rule_71_readied.py` (completely missing)

### Rule 72: Reinforcements
**Status**: Not Started | **Test Coverage**: 0%
**Missing Test Coverage**:
- Reinforcement supply tracking
- Component limitation system
- Unit availability management
- Command token supply management

**Required Test Files**:
- `tests/test_rule_72_reinforcements.py` (completely missing)

### Rule 73: Relics
**Status**: Not Started | **Test Coverage**: 0%
**Missing Test Coverage**:
- Relic fragment system
- Relic deck management
- Relic ability framework
- Exploration integration

**Required Test Files**:
- `tests/test_rule_73_relics.py` (completely missing)

## Specific Test Coverage Enhancement Recommendations

### Existing Test Files Needing Expansion

#### Rule 10: Anti-Fighter Barrage
**Current Coverage**: ~60% | **Files**: Multiple AFB test files exist
**Missing Coverage**:
- Anti-fighter barrage value parsing
- Hit assignment mechanics
- Space combat timing integration
- First round only restriction

#### Rule 16: Capacity
**Current Coverage**: ~70% | **Files**: `tests/test_capacity_excess_removal.py`
**Missing Coverage**:
- Combat capacity exceptions
- Post-combat excess unit removal
- Capacity calculation edge cases

#### Rule 22: Component Action
**Current Coverage**: ~40% | **Files**: Action card tests exist
**Missing Coverage**:
- Technology card component actions
- Leader component actions
- Exploration card component actions
- Relic component actions
- Promissory note component actions

#### Rule 61: Objective Cards
**Current Coverage**: ~85% | **Files**: Multiple objective test files exist
**Missing Coverage**:
- Public objective setup system
- Stage I/II progression mechanics
- Home system control validation for scoring

## Test Coverage Quality Standards

### Required Test Categories per Rule
1. **Basic Functionality Tests** - Core rule mechanics
2. **Edge Case Tests** - Boundary conditions and error cases
3. **Integration Tests** - Interaction with other systems
4. **Error Handling Tests** - Invalid input and error conditions
5. **Performance Tests** - For computationally intensive rules

### Test Coverage Metrics Targets
- **Critical Rules**: 95%+ line coverage
- **High Priority Rules**: 90%+ line coverage
- **Medium Priority Rules**: 85%+ line coverage
- **Low Priority Rules**: 80%+ line coverage

### Test Quality Indicators
- [ ] All public methods tested
- [ ] All error conditions tested
- [ ] All integration points tested
- [ ] All edge cases covered
- [ ] Performance characteristics validated

## Implementation Timeline

### Phase 1: Critical Gaps (Weeks 1-2)
- Implement Rule 27 (Custodians Token) tests
- Implement Rule 92 (Trade Strategy Card) tests
- Enhance Rule 81 (Status Phase) test coverage

### Phase 2: High Priority Gaps (Weeks 3-4)
- Implement Rule 28 (Deals) tests
- Implement Rule 96 (Supply Limit) tests
- Enhance Rule 1, 3, 89 test coverage

### Phase 3: Medium Priority Gaps (Weeks 5-6)
- Implement missing strategy card tests (Rules 32, 45)
- Implement system tests (Rules 70, 71, 72, 73)
- Enhance existing test coverage for Rules 10, 16, 22, 61

### Phase 4: Quality Assurance (Week 7)
- Review all test coverage metrics
- Ensure quality standards compliance
- Add performance and integration tests

## Success Metrics

### Coverage Completion Indicators
- [ ] All critical rules have 95%+ test coverage
- [ ] All high priority rules have 90%+ test coverage
- [ ] No rules have 0% test coverage
- [ ] All integration points are tested
- [ ] All error conditions are covered

### Quality Assurance Indicators
- [ ] All tests pass consistently
- [ ] Test execution time remains reasonable
- [ ] Tests provide clear failure messages
- [ ] Test code follows project standards
- [ ] Tests are maintainable and readable

This comprehensive test coverage enhancement will ensure robust validation of all implemented features and provide confidence in system reliability and correctness.

# Critical Gaps and High-Priority Next Steps

Based on the comprehensive implementation status audit, this document identifies the most critical gaps blocking core gameplay functionality and provides specific next steps for resolution.

## CRITICAL BLOCKING GAPS

### 1. Rule 27: Custodians Token - GAME FLOW BLOCKER
**Impact**: Completely blocks agenda phase activation and political gameplay
**Status**: Not Started (0% implementation)
**Blocking Effects**:
- Agenda phase cannot be activated
- Political gameplay completely unavailable
- Victory point progression blocked
- Game flow incomplete

**Immediate Next Steps**:
1. **Week 1**: Implement `CustodiansToken` entity class
   - Token placement on Mecatol Rex
   - Ground force landing restriction mechanics
   - Token removal validation system

2. **Week 2**: Implement influence spending mechanics
   - Influence cost calculation (6 influence)
   - Mandatory ground force commitment
   - Player choice validation

3. **Week 3**: Implement victory point award and agenda phase trigger
   - Victory point award upon removal
   - Agenda phase activation integration
   - Game state transition logic

**Dependencies**: Requires agenda phase system (Rule 8) completion
**Success Criteria**: Agenda phase can be activated through custodians token removal

### 2. Rule 92: Trade Strategy Card - ✅ COMPLETE
**Impact**: Critical economic strategy option fully implemented
**Status**: Production Ready (100% implementation)
**Resolved Issues**:
- ✅ Complete strategy card system with all 8 strategy cards
- ✅ Full economic strategy options available to players
- ✅ Commodity system fully utilized with refresh mechanics
- ✅ Enhanced player interaction through chosen player mechanics

**Completed Implementation**:
1. **Week 1**: Trade strategy card framework completed
   - ✅ Strategy card entity with initiative value 5
   - ✅ Primary ability structure with 3-step workflow
   - ✅ Secondary ability structure with command token validation

2. **Week 2**: Commodity refresh mechanics fully implemented
   - ✅ Commodity replenishment to faction maximum
   - ✅ 3 trade goods generation with resource management
   - ✅ Comprehensive resource validation and error handling

3. **Week 3**: Advanced trading system completed
   - ✅ Multi-player secondary ability usage
   - ✅ Player selection for free secondary abilities
   - ✅ Complete integration with strategy card coordinator
   - ✅ Performance optimization and comprehensive testing

**Dependencies**: ✅ Commodity system (Rule 21) - successfully integrated
**Success Criteria Met**: ✅ Players can use Trade strategy card for complete economic gameplay

### 3. Rule 81: Status Phase - ROUND MANAGEMENT GAP
**Impact**: Incomplete round progression and game state management
**Status**: Partially Implemented (~30% complete)
**Blocking Effects**:
- Incomplete round transitions
- Objective scoring issues
- Card management problems
- Game state inconsistencies

**Immediate Next Steps**:
1. **Week 1**: Complete status phase orchestration
   - Score objectives step
   - Reveal public objectives step
   - Draw action cards step

2. **Week 2**: Implement resource management steps
   - Remove command tokens step
   - Gain and redistribute command tokens step
   - Ready cards step

3. **Week 3**: Complete cleanup and preparation steps
   - Repair units step
   - Return strategy cards step
   - Round transition logic

**Dependencies**: Requires objective system (Rule 61) and card systems
**Success Criteria**: Complete round progression with all status phase steps

## HIGH PRIORITY SYSTEM GAPS

### 4. Rule 89: Tactical Action - CORE GAMEPLAY GAP
**Impact**: Incomplete tactical gameplay workflow
**Status**: Partially Implemented (~60% complete)
**Blocking Effects**:
- Tactical action sequence incomplete
- Movement-combat-production integration issues
- Active system management problems

**Next Steps**:
1. **Week 1**: Complete tactical action workflow integration
   - Movement step completion
   - Combat step integration
   - Production step finalization

2. **Week 2**: Implement component action integration
   - Component actions during tactical actions
   - Timing window management
   - Action validation

**Dependencies**: Requires movement (Rule 58), combat (Rule 18), production (Rule 67)
**Success Criteria**: Complete tactical action workflow from activation to completion

### 5. Rule 28: Deals - DIPLOMATIC SYSTEM GAP
**Impact**: Missing diplomatic framework entirely
**Status**: Not Started (0% implementation)
**Blocking Effects**:
- No player negotiation system
- Reduced diplomatic depth
- Limited alliance mechanics

**Next Steps**:
1. **Week 1**: Implement deal entity system
   - Deal data structure
   - Binding vs non-binding classification
   - Deal validation logic

2. **Week 2**: Implement deal enforcement
   - Binding deal enforcement mechanics
   - Non-binding deal flexibility
   - Deal violation handling

**Dependencies**: Requires neighbor system (Rule 60) and transaction system (Rule 94)
**Success Criteria**: Players can create and enforce binding deals

### 6. Rule 96: Supply Limit - GAME BALANCE GAP
**Impact**: Fleet composition and resource management issues
**Status**: Not Started (0% implementation)
**Blocking Effects**:
- No fleet size limitations
- Game balance problems
- Resource management incomplete

**Next Steps**:
1. **Week 1**: Implement supply limit calculation
   - Fleet supply limit mechanics
   - Supply limit modification tracking
   - Limit calculation validation

2. **Week 2**: Implement limit enforcement
   - Unit removal when exceeding limits
   - Player choice in excess unit removal
   - Integration with fleet management

**Dependencies**: Requires fleet system and command token system (Rule 20)
**Success Criteria**: Fleet sizes properly limited by supply values

## MEDIUM PRIORITY COMPLETIONS

### 7. Rule 1: Abilities - ADVANCED FEATURES
**Impact**: Incomplete ability system functionality
**Status**: Partially Implemented (~70% complete)
**Next Steps**:
- Complete mandatory ability auto-triggering
- Implement "then" conditional resolution
- Add multi-player simultaneous resolution

### 8. Rule 3: Action Phase - EDGE CASES
**Impact**: Action phase edge case handling
**Status**: Partially Implemented (~80% complete)
**Next Steps**:
- Complete component action framework
- Implement legal action detection
- Add transaction resolution timing

### 9. Strategy Card Completions
**Impact**: Incomplete strategy card system
**Missing Cards**: Diplomacy (Rule 32), Imperial (Rule 45)
**Next Steps**:
- Implement Diplomacy strategy card mechanics
- Implement Imperial strategy card mechanics

## IMPLEMENTATION PRIORITY MATRIX

### Phase 1: Critical Blockers (Weeks 1-6)
**Priority**: CRITICAL - Must complete for basic gameplay
1. Rule 27: Custodians Token (Weeks 1-3)
2. ✅ Rule 92: Trade Strategy Card (COMPLETE - Production Ready)

### Phase 2: Core Systems (Weeks 7-12)
**Priority**: HIGH - Required for complete gameplay
3. Rule 81: Status Phase (Weeks 7-9)
4. Rule 89: Tactical Action (Weeks 10-12)

### Phase 3: System Enhancements (Weeks 13-18)
**Priority**: HIGH - Important for game balance
5. Rule 28: Deals (Weeks 13-15)
6. Rule 96: Supply Limit (Weeks 16-18)

### Phase 4: Advanced Features (Weeks 19-24)
**Priority**: MEDIUM - Polish and completeness
7. Rule 1: Abilities advanced features (Weeks 19-21)
8. Rule 3: Action Phase edge cases (Weeks 22-24)

## RESOURCE ALLOCATION RECOMMENDATIONS

### Development Team Allocation
- **60% effort**: Critical blockers (Rules 27, 92, 81)
- **30% effort**: Core systems (Rules 89, 28, 96)
- **10% effort**: Advanced features (Rules 1, 3, strategy cards)

### Skill Requirements
- **Backend Systems**: Rules 27, 81, 89, 96
- **Game Logic**: Rules 92, 28, 1, 3
- **Integration**: All rules require integration testing
- **UI/UX**: Rules 28 (deals interface), 92 (trading interface)

## SUCCESS METRICS AND MILESTONES

### Phase 1 Success Criteria (Weeks 1-6)
- [ ] Agenda phase can be activated via custodians token
- [x] Trade strategy card provides economic options
- [ ] Basic political and economic gameplay functional

### Phase 2 Success Criteria (Weeks 7-12)
- [ ] Complete round progression through status phase
- [ ] Full tactical action workflow functional
- [ ] Core turn-based gameplay complete

### Phase 3 Success Criteria (Weeks 13-18)
- [ ] Diplomatic deals system operational
- [ ] Fleet supply limits enforced
- [ ] Game balance mechanisms functional

### Phase 4 Success Criteria (Weeks 19-24)
- [ ] Advanced ability features complete
- [ ] All action phase edge cases handled
- [ ] System polish and optimization complete

## RISK MITIGATION STRATEGIES

### Technical Risks
1. **Integration Complexity**: Start with isolated implementations, then integrate
2. **Performance Issues**: Implement with performance monitoring from start
3. **Test Coverage**: Maintain 90%+ test coverage throughout development

### Project Risks
1. **Scope Creep**: Focus strictly on identified critical gaps
2. **Resource Constraints**: Prioritize critical blockers over nice-to-have features
3. **Timeline Pressure**: Allow buffer time for integration and testing

### Quality Risks
1. **Regression Issues**: Comprehensive regression testing after each phase
2. **Type Safety**: Maintain strict mypy compliance throughout
3. **Documentation**: Update documentation concurrent with implementation

## MONITORING AND REPORTING

### Weekly Progress Metrics
- Implementation completion percentage per rule
- Test coverage percentage per rule
- Integration test pass rate
- Performance benchmark results

### Monthly Milestone Reviews
- Phase completion assessment
- Resource allocation adjustment
- Timeline and scope validation
- Quality metrics review

### Success Indicators
- **Green**: On schedule, quality metrics met, tests passing
- **Yellow**: Minor delays, quality concerns, some test failures
- **Red**: Major delays, quality issues, significant test failures

This roadmap provides a clear path from the current state to a fully functional TI4 AI system with complete core gameplay mechanics. The focus on critical blockers ensures that the most impactful gaps are addressed first, enabling progressive gameplay functionality improvements.
### Rule 27: Custodians Token – Remaining Gaps

- Integration coverage: Verify that activating the agenda phase after token removal correctly affects subsequent rounds in the full game loop (GameController/GameStateMachine), including speaker order and phase transitions.
- Multi-player sequencing: Ensure removal by one player correctly prevents others from attempting removal and that VP accounting remains consistent across multiple players in complex scenarios.
- Interaction checks: Validate interactions with political/agenda-related strategy cards and status-phase behaviors once the agenda phase is active.
- Robustness: Confirm error handling and rollback behavior if ground force placement fails in complex board states (currently non-fatal, but should be observable in logs/events).

Action Items:
1) Author integration tests covering round progression with agenda phase enabled post-removal.
2) Add tests for competing removal attempts and confirm idempotency across players.
3) Expand event logging around token removal and agenda activation for easier debugging.

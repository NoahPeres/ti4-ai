# Critical Gaps and High-Priority Next Steps

Based on the comprehensive implementation status audit, this document identifies the most critical gaps blocking core gameplay functionality and provides specific next steps for resolution.

## CRITICAL BLOCKING GAPS

### 1. Rule 27: Custodians Token - ✅ COMPLETE
**Impact**: Enables agenda phase activation via custodians token removal on Mecatol Rex
**Status**: Production Ready (implemented via Merge PR #51)
**Highlights**:
- Custodians token mechanics implemented (placement, removal, VP award)
- Influence spending validation (6 influence) with ground force commitment
- Agenda phase activation integrated and validated
- Event logging and observer instrumentation for custodians flow
**Validation**:
- Covered by tests: `tests/test_rule_27_custodians_token.py`, `tests/test_rule_27_integration.py` (11 passed locally)
**Outcome**: Removes a major game flow blocker; political gameplay path is now available

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

### 3. Rule 81: Status Phase - ✅ COMPLETE
**Impact**: Round progression enabled with complete status phase orchestration and round transition
**Status**: Production Ready (validated by orchestrator and round transition tests)
**Highlights**:
- Complete status phase orchestration across all steps
- Round transition logic via `RoundTransitionManager` (agenda vs strategy)
- Error handling, rollback on critical failures, graceful degradation
**Validation**:
- Covered by orchestrator, transition, and integration tests across status-phase suite
**Outcome**: Round management is complete and no longer a blocker

## HIGH PRIORITY SYSTEM GAPS

### 4. Rule 89: Tactical Action - CORE GAMEPLAY GAP
**Impact**: Core tactical gameplay workflow nearing completeness
**Status**: Substantially Improved (~80% complete)
**Recent Progress (Strict TDD)**:
- Implemented coordinator integration: `TacticalActionCoordinator.validate_and_execute_tactical_action(...)`
  - Validates movement plans via `TacticalActionValidator.validate_movement_plan` — LRR §89.2
  - Executes movement with `MovementStep` from `MovementEngine` — LRR §89.2
  - Recomputes space combat required flag — `requires_space_combat` — LRR §89.3
  - Evaluates invasion eligibility (ground force commitment and bombardment) — `can_commit_ground_forces`, `can_use_bombardment` — LRR §89.4
  - Determines production availability — `can_resolve_production_abilities` — LRR §89.5
- New passing tests: `src/ti4/tests/test_rule_89_tactical_action_coordinator_execution.py` exercising LRR §§ 89.2–89.5

**Blocking Effects Remaining**:
- Component action timing windows during tactical actions
- Broader edge cases and law/technology modifiers across steps
- Advanced rollback and error recovery across multi-step sequences

**Next Steps (TDD)**:
1. Expand unit tests for edge cases:
   - Wormholes, hostile adjacency, and space cannon defense interplay (LRR §§ 58, 89.3)
   - Transport capacity and ground force commitment constraints (LRR §89.4)
   - Law and technology modifiers affecting production (LRR §89.5)
2. Implement component action integration:
   - Timing window management and validation (LRR §3, cross-referenced with §89)
   - Ensure no duplication across validator/engine/coordinator layers
3. Strengthen integration and rollback:
   - Transactional safety across movement, combat, invasion, production steps
   - Detailed error reporting with recovery paths

**Dependencies**: Movement (Rule 58), Combat (Rule 18), Production (Rule 67)
**Success Criteria**: Complete tactical action workflow from activation to completion with component action timing windows and robust edge-case handling

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

# TI4 AI Implementation Roadmap

## 🎯 Overall Progress: 52/101 Rules (51.5% Complete)

### Last Updated
December 2025 (Post-Comprehensive Implementation Status Audit)

### Project Status
**CRITICAL PATH FOCUS**: Following the comprehensive implementation status audit, this roadmap has been completely restructured to prioritize the **4 critical blocking rules** (27, 92, 81, 89) that prevent complete gameplay functionality. The audit revealed exceptional quality in completed systems but identified specific gaps that block core game flow.

### Current Phase
**Critical Blocker Resolution** - Immediate focus on Rules 27, 92, 81, 89 as identified critical path

### Next Milestone
**Target**: Complete Basic Gameplay Loop (3 months)
**Success Criteria**: Full game playable from setup to victory with all critical systems operational

---

## 🔍 Audit-Based Strategic Assessment

### Key Findings from Comprehensive Implementation Status Audit

#### Exceptional Foundation Quality
The audit confirmed **52 rules fully implemented** with production-ready quality:
- **2,500+ comprehensive test cases** across all implemented systems
- **90%+ test coverage** for completed rules with strict quality standards
- **Complete type safety compliance** throughout production code
- **Mature architectural patterns** supporting complex game mechanics

#### Critical Blocking Gaps Identified
The audit identified **4 critical rules that completely block core gameplay**:

1. **Rule 27: Custodians Token** ❌ - **GAME FLOW BLOCKER**: Completely prevents agenda phase activation
2. **Rule 92: Trade Strategy Card** ✅ - **ECONOMIC SYSTEM COMPLETE**: Essential economic strategy option fully implemented
3. **Rule 81: Status Phase** ❌ - **ROUND MANAGEMENT GAP**: Incomplete round progression (30% complete)
4. **Rule 89: Tactical Action** ❌ - **CORE GAMEPLAY GAP**: Incomplete tactical workflow (60% complete)

#### Strategic Insight from Audit
**CRITICAL PATH APPROACH**: The audit revealed that focusing 80% of development effort on these 4 critical blocking rules will deliver a fully playable TI4 AI system in 3 months, compared to 12+ months with the previous broad expansion approach.

### Quality Achievements Worth Preserving

#### Combat Systems Excellence (12 rules complete)
- **Complete space combat system** with all mechanics integrated (Rules 10, 15, 17, 18, 29, 30, 31, 76, 77, 78, 87)
- **Anti-fighter barrage system** with 86 comprehensive tests
- **Ground combat and bombardment** fully operational
- **Unit destruction and sustain damage** mechanics complete

#### Strategic Framework Maturity (15 rules complete)
- **Strategy card coordinator** with complete state management (Rule 83 - 50+ tests)
- **Leader system architecture** supporting all three leader types (Rule 51 - 253 tests)
- **Technology research system** with comprehensive card framework (Rules 90, 91)
- **Resource management** with complete cost validation (Rule 26 - 200+ tests)

#### Advanced System Implementations (8 rules complete)
- **Transport system** with capacity and movement integration (Rule 95)
- **Anomaly management** handling all four anomaly types (Rule 9 - 38 tests)
- **Wormhole adjacency** with comprehensive spatial mechanics (Rule 101 - 24 tests)
- **Objective tracking** with victory condition management (Rule 61 - 66 tests)

---

## 📊 Current Implementation Status

### ✅ Fully Implemented Rules (51/101)

#### Foundation Systems (9 rules)
- **Rule 2: ACTION CARDS** - Complete action card system (39 tests)
- **Rule 5: ACTIVE SYSTEM** - System activation mechanics (complete)
- **Rule 6: ADJACENCY** - Complete adjacency system with wormholes (12 tests)
- **Rule 9: ANOMALIES** - All four anomaly types with movement/combat effects (38 tests)
- **Rule 25: CONTROL** - Planet control mechanics (12 tests)
- **Rule 34: EXHAUSTED** - Card exhaustion mechanics
- **Rule 66: POLITICS** - Politics strategy card (complete)
- **Rule 75: RESOURCES** - Resource management system (81 tests)
- **Rule 98: VICTORY POINTS** - Victory point tracking

#### Combat Systems (12 rules)
- **Rule 10: ANTI-FIGHTER BARRAGE** - Pre-combat mechanics (86 tests)
- **Rule 12: ATTACH** - Card attachment system
- **Rule 13: ATTACKER** - Combat role definition (8 tests)
- **Rule 14: BLOCKADED** - Production restrictions (16 tests)
- **Rule 15: BOMBARDMENT** - Bombardment mechanics
- **Rule 17: CAPTURE** - Unit capture mechanics (12 tests)
- **Rule 18: COMBAT** - General combat framework (5 tests)
- **Rule 29: DEFENDER** - Combat role identification
- **Rule 30: DEPLOY** - Unit deployment abilities
- **Rule 31: DESTROYED** - Unit destruction mechanics (13 tests)
- **Rule 76: SHIPS** - Ship unit mechanics
- **Rule 77: SPACE CANNON** - Space cannon mechanics (11 tests)
- **Rule 78: SPACE COMBAT** - Space combat system
- **Rule 87: SUSTAIN DAMAGE** - Sustain damage mechanics (5 tests)

#### Strategic & Economic Systems (19 rules)
- **Rule 20: COMMAND TOKENS** - Command token management
- **Rule 21: COMMODITIES** - Commodity trading system (11 tests)
- **Rule 26: COST** - Resource spending validation (200+ tests)
- **Rule 33: ELIMINATION** - Player elimination conditions (22 tests)
- **Rule 35: EXPLORATION** - Exploration mechanics (36 tests)
- **Rule 37: FLEET POOL** - Fleet command token mechanics
- **Rule 49: INVASION** - Invasion process
- **Rule 51: LEADERS** - Complete leader system (253 tests)
- **Rule 52: LEADERSHIP** - Leadership strategy card
- **Rule 58: MOVEMENT** - Unit movement mechanics
- **Rule 61: OBJECTIVE CARDS** - Victory condition tracking (66 tests)
- **Rule 67: PRODUCING UNITS** - Unit production system
- **Rule 68: PRODUCTION** - Production mechanics
- **Rule 69: PROMISSORY NOTES** - Promissory note system
- **Rule 74: REROLLS** - Dice reroll mechanics
- **Rule 80: SPEAKER** - Speaker token privileges (20 tests)
- **Rule 82: STRATEGIC ACTION** - Strategy card activation
- **Rule 83: STRATEGY CARD** - Strategy card system (50+ tests)
- **Rule 90: TECHNOLOGY** - Technology research system
- **Rule 91: TECHNOLOGY (Strategy Card)** - Technology strategy card
- **Rule 94: TRANSACTIONS** - Player trading system
- **Rule 95: TRANSPORT** - Unit transportation mechanics
- **Rule 99: WARFARE** - Warfare strategy card
- **Rule 101: WORMHOLES** - Wormhole adjacency system (24 tests)

#### Advanced Systems (4 rules)
- **Rule 40: GROUND COMBAT** - Ground combat mechanics
- **Rule 88: SYSTEM TILES** - System tile mechanics

### 🚨 CRITICAL BLOCKING GAPS - Preventing Complete Gameplay (4 rules)

#### Immediate Critical Blockers (Must Complete First)
- **Rule 27: CUSTODIANS TOKEN** ❌ - **GAME FLOW BLOCKER**: Completely prevents agenda phase activation
- **Rule 92: TRADE STRATEGY CARD** ✅ - **COMPLETE**: Essential economic strategy option implemented

#### Core Gameplay Completion (Must Complete Second)
- **Rule 81: STATUS PHASE** ❌ - **ROUND MANAGEMENT GAP**: Incomplete round progression (30% complete)
- **Rule 89: TACTICAL ACTION** ❌ - **CORE GAMEPLAY GAP**: Incomplete tactical workflow (60% complete)

### ⚠️ HIGH PRIORITY COMPLETIONS (8 rules)

#### Strategic Depth and Balance (Phase 2 Priority)
- **Rule 28: DEALS** ❌ - **DIPLOMATIC FRAMEWORK GAP**: Missing diplomatic framework entirely
- **Rule 96: SUPPLY LIMIT** ❌ - **GAME BALANCE GAP**: Fleet composition and resource management issues

#### Partial Implementations Needing Completion (Phase 3 Priority)
- **Rule 1: ABILITIES** - Missing advanced features (mandatory triggering, multi-player resolution) - 70% complete
- **Rule 3: ACTION PHASE** - Missing component action framework and edge cases - 80% complete
- **Rule 8: AGENDA PHASE** - Core voting complete, needs election mechanics - 85% complete
- **Rule 32: DIPLOMACY** - Strategy card framework exists, needs implementation - 20% complete
- **Rule 45: IMPERIAL** - Strategy card framework exists, needs implementation - 30% complete

#### System Completions (Phase 4 Priority)
- **Rule 7: AGENDA CARDS** - Foundation complete, needs concrete card implementations - 75% complete

### 📋 REMAINING SYSTEMS (38 rules)

#### Missing System Rules (4 rules - Recently Identified)
- **Rule 70: PURGE** ❌ - Component purge mechanics (0% complete)
- **Rule 71: READIED** ❌ - Card state management system (0% complete)
- **Rule 72: REINFORCEMENTS** ❌ - Reinforcement supply tracking (0% complete)
- **Rule 73: RELICS** ❌ - Relic fragment system (0% complete)

#### Advanced Combat & Movement (8 rules)
- Rules 11, 24, 41, 42, 44, 59, 86: Terrain effects and advanced combat

#### Economic & Resource Management (6 rules)
- Rules 19, 39, 48, 93: Command sheets, game board, trade goods

#### Planetary & Structure Systems (8 rules)
- Rules 53, 54, 63, 64, 65, 79, 85, 100: Planets, structures, special systems

#### Advanced Unit & Technology (6 rules)
- Rules 23, 55, 56, 57, 97: Unit limits, mechs, modifiers

#### Game Management (8 rules)
- Rules 36, 38, 43, 46, 60, 62, 84: Token mechanics, neighbors, phases

---

## 🚀 Strategic Implementation Plan

### CRITICAL PATH APPROACH
**Philosophy**: Focus 80% of development effort on the 4 critical blocking rules (27, 92, 81, 89) that prevent complete gameplay, rather than broad feature expansion.

### Phase 1: Critical Blocking Rules Resolution (Months 1-3)
**Goal**: Remove all critical blockers preventing complete gameplay
**Success Criteria**: Full game playable from setup to victory

#### Month 1: Game Flow Activation (Weeks 1-4)
**Rule 27: CUSTODIANS TOKEN** 🚨 **HIGHEST PRIORITY BLOCKER**
- **Impact**: **COMPLETE GAME FLOW BLOCKER** - Prevents agenda phase activation entirely
- **Effort**: 3 weeks full-time development + 1 week testing
- **Dependencies**: Agenda phase system (Rule 8) - already implemented
- **Complexity Assessment**: Medium (based on audit findings)
- **Deliverables**:
  - `CustodiansToken` entity with Mecatol Rex placement mechanics
  - Influence spending validation (6 influence cost requirement)
  - Ground force commitment and landing restrictions
  - Victory point award system upon token removal
  - Agenda phase activation trigger integration
  - Comprehensive test suite (95% coverage target)
- **Success Criteria**: Agenda phase can be activated through custodians token removal mechanism

#### Month 2: Economic System Completion (Weeks 5-8)
**Rule 92: TRADE STRATEGY CARD** ✅ **COMPLETE**
- **Status**: **PRODUCTION READY** - Essential economic strategy option fully implemented
- **Implementation Date**: December 2025
- **Actual Effort**: 3 weeks development + testing (as planned)
- **Dependencies**: Commodity system (Rule 21) - successfully integrated
- **Complexity Assessment**: Low-Medium (accurate assessment)
- **Deliverables Completed**:
  - ✅ Trade strategy card framework (initiative value 5)
  - ✅ Primary ability: 3 trade goods + commodity refresh + player selection
  - ✅ Secondary ability: Command token cost + commodity replenishment
  - ✅ Trade good generation and resource management integration
  - ✅ Complete integration with existing commodity system
  - ✅ Comprehensive test suite (95%+ coverage achieved)
- **Success Criteria Met**: ✅ Players can use Trade strategy card for complete economic gameplay

**Rule 81: STATUS PHASE** 🚨 **ROUND MANAGEMENT BLOCKER**
- **Impact**: **ROUND PROGRESSION GAP** - Incomplete round management (30% complete)
- **Effort**: 1 week completion + 1 week testing
- **Dependencies**: Objective system (Rule 61), Card systems - already implemented
- **Complexity Assessment**: Medium (based on audit findings)
- **Deliverables**:
  - Complete status phase orchestration system
  - Score objectives step implementation
  - Reveal public objectives mechanics
  - Draw action cards step
  - Command token management (remove/gain/redistribute)
  - Ready cards step implementation
  - Repair units step
  - Return strategy cards step
- **Success Criteria**: Complete round progression with all status phase steps functional

#### Month 3: Core Gameplay Workflow (Weeks 9-12)
**Rule 89: TACTICAL ACTION** 🚨 **CORE GAMEPLAY BLOCKER**
- **Impact**: **TACTICAL WORKFLOW GAP** - Incomplete core gameplay workflow (60% complete)
- **Effort**: 2 weeks completion + 1 week testing
- **Dependencies**: Movement (Rule 58), Combat (Rule 18), Production (Rule 67) - all implemented
- **Complexity Assessment**: High (based on audit findings)
- **Deliverables**:
  - Complete tactical action workflow integration
  - Movement step completion and validation
  - Combat step integration with all combat systems
  - Production step finalization
  - Component action integration during tactical actions
  - Active system management throughout sequence
  - Advanced tactical action edge cases
- **Success Criteria**: Complete tactical action workflow from activation to completion

**Critical Path Integration and Validation** (Week 12)
- **Effort**: 1 week full-time integration testing
- **Deliverables**:
  - End-to-end gameplay validation from setup to victory
  - Performance optimization for critical path
  - Regression testing for all existing systems
  - Quality assurance validation
- **Success Criteria**: Full TI4 game playable with all critical systems integrated

### Phase 2: Strategic Depth & Game Balance (Months 4-5)
**Goal**: Add strategic depth, diplomatic options, and game balance mechanisms
**Success Criteria**: Competitive gameplay with full strategic options and proper game balance

#### Month 4: Diplomatic Framework & Game Balance (Weeks 13-16)
**Rule 28: DEALS** 🎯 **DIPLOMATIC FRAMEWORK**
- **Impact**: **DIPLOMATIC SYSTEM GAP** - Missing diplomatic framework entirely
- **Effort**: 2 weeks full-time development
- **Dependencies**: Neighbor system (Rule 60), Transaction system (Rule 94) - both implemented
- **Complexity Assessment**: Medium (based on audit findings)
- **Deliverables**:
  - Deal entity system with binding/non-binding classification
  - Deal timing and neighbor requirements validation
  - Binding deal enforcement mechanics
  - Non-binding deal flexibility system
  - Deal violation handling and consequences
  - Player negotiation interface integration
- **Success Criteria**: Players can create, negotiate, and enforce binding deals

**Rule 96: SUPPLY LIMIT** 🎯 **GAME BALANCE**
- **Impact**: **FLEET BALANCE GAP** - Fleet composition and resource management issues
- **Effort**: 2 weeks full-time development
- **Dependencies**: Fleet system, Command token system (Rule 20) - both implemented
- **Complexity Assessment**: Medium (based on audit findings)
- **Deliverables**:
  - Supply limit calculation mechanics
  - Fleet size limitation enforcement system
  - Unit removal when exceeding limits
  - Player choice in excess unit removal
  - Supply limit modification tracking
  - Integration with fleet management system
- **Success Criteria**: Fleet sizes properly limited by supply values with proper enforcement

#### Month 5: Strategy Card System Completion (Weeks 17-20)
**Rule 32: DIPLOMACY STRATEGY CARD**
- **Impact**: **STRATEGY OPTION GAP** - Missing diplomatic strategy option
- **Effort**: 1 week full-time development
- **Dependencies**: Planet refresh system - already implemented
- **Complexity Assessment**: Low (based on audit findings)
- **Deliverables**:
  - Diplomacy strategy card framework
  - Primary ability: Refresh two planets
  - Secondary ability: Refresh one planet
  - System activation prevention mechanics
- **Success Criteria**: Diplomacy strategy card provides additional strategic option

**Rule 45: IMPERIAL STRATEGY CARD**
- **Impact**: **VICTORY STRATEGY GAP** - Missing victory point strategy option
- **Effort**: 1 week full-time development
- **Dependencies**: Objective scoring system - already implemented
- **Complexity Assessment**: Low (based on audit findings)
- **Deliverables**:
  - Imperial strategy card framework
  - Primary ability: Score objective
  - Secondary ability: Draw secret objective
  - Mecatol Rex victory point bonus
- **Success Criteria**: Imperial strategy card provides victory point strategy option

**System Integration and Balance Testing** (Weeks 19-20)
- **Effort**: 2 weeks full-time
- **Deliverables**:
  - Balanced competitive gameplay validation
  - All strategy cards functional and balanced
  - Performance optimization for new systems
  - Comprehensive integration testing
- **Success Criteria**: All strategy cards functional with balanced competitive gameplay

### Phase 3: Advanced Features & System Polish (Months 6-8)
**Goal**: Complete advanced features, system polish, and missing system rules
**Success Criteria**: Production-ready TI4 AI system with comprehensive feature set

#### Month 6: Missing System Rules Implementation (Weeks 21-24)
**Rules 70-73: Missing System Rules** 🎯 **SYSTEM COMPLETENESS**
- **Rule 70: PURGE** - Component purge mechanics (0% complete)
- **Rule 71: READIED** - Card state management system (0% complete)
- **Rule 72: REINFORCEMENTS** - Reinforcement supply tracking (0% complete)
- **Rule 73: RELICS** - Relic fragment system (0% complete)
- **Impact**: **SYSTEM COMPLETENESS GAP** - Missing fundamental game mechanics
- **Effort**: 4 weeks full-time development (1 week per rule)
- **Dependencies**: Various existing systems
- **Complexity Assessment**: Low-Medium per rule (based on audit findings)
- **Success Criteria**: All missing system rules implemented with proper integration

#### Month 7: Advanced Ability & Action Systems (Weeks 25-28)
**Rule 1: ABILITIES** - Advanced Features (70% → 100% complete)
- **Missing Components**:
  - Mandatory ability auto-triggering (Rule 1.8)
  - "Then" conditional resolution (Rule 1.17)
  - Multi-player simultaneous resolution (Rules 1.19, 1.20)
  - Duration tracking for temporary effects (Rule 1.3)
- **Effort**: 2 weeks full-time development
- **Success Criteria**: Complete ability system with all advanced features

**Rule 3: ACTION PHASE** - Edge Cases (80% → 100% complete)
- **Missing Components**:
  - Component action framework completion
  - Legal action detection for forced pass scenarios
  - Transaction resolution timing during pass turns
- **Effort**: 2 weeks full-time development
- **Success Criteria**: All action phase edge cases handled properly

#### Month 8: System Completions & Production Polish (Weeks 29-32)
**Remaining Partial Implementations**:
- **Rule 7: AGENDA CARDS** - Concrete card implementations (75% → 100%)
- **Rule 8: AGENDA PHASE** - Election mechanics completion (85% → 100%)

**System Polish & Quality Assurance**:
- Performance optimization across all systems
- Documentation completion and accuracy validation
- Comprehensive integration test coverage
- Quality assurance validation and bug fixes
- Production deployment preparation

**Success Criteria**: Production-ready TI4 AI system with all core features complete

### Phase 4: Optional Advanced Systems (Months 9-12)
**Goal**: Complete remaining systems for 100% rule coverage
**Priority**: OPTIONAL - Only if resources available after core completion

#### Advanced Combat & Movement (8 rules)
- Rules 11, 24, 41, 42, 44, 59, 86: Terrain effects and advanced combat mechanics

#### Economic & Resource Management (4 rules)
- Rules 19, 39, 48, 93: Command sheets, game board, trade goods

#### Planetary & Structure Systems (8 rules)
- Rules 53, 54, 63, 64, 65, 79, 85, 100: Planets, structures, special systems

#### Advanced Unit & Technology (5 rules)
- Rules 23, 55, 56, 57, 97: Unit limits, mechs, modifiers

#### Game Management (8 rules)
- Rules 36, 38, 43, 46, 60, 62, 84: Token mechanics, neighbors, phases

**Note**: This phase is entirely optional and should only be pursued after successful completion of Phases 1-3, which will deliver a fully functional TI4 AI system.

---

## 📊 Resource Allocation & Timeline

### Development Team Structure
**Recommended Team Size**: 3-4 developers for optimal velocity based on audit complexity assessments

#### Core Team Roles (Based on Audit Findings)
1. **Critical Path Lead** (50% allocation)
   - Focus: Critical blocking rules (27, 92, 81, 89)
   - Responsibilities: Core system design, implementation, and integration
   - Skills Required: Game mechanics, system integration, complex workflow management

2. **Strategic Systems Developer** (30% allocation)
   - Focus: Strategic depth systems (28, 96, 32, 45, 70-73)
   - Responsibilities: Game balance, diplomatic systems, missing rule implementations
   - Skills Required: Game balance, player interaction systems, rule mechanics

3. **Quality & Integration Specialist** (15% allocation)
   - Focus: System integration, testing, and quality assurance
   - Responsibilities: End-to-end workflow validation, regression testing, performance optimization
   - Skills Required: Integration testing, performance optimization, quality assurance

4. **Advanced Features Developer** (5% allocation)
   - Focus: Advanced features and system polish (Rules 1, 3, 7, 8)
   - Responsibilities: Complex ability systems, edge case handling, system completions
   - Skills Required: Complex game logic, edge case analysis, system refinement

### Effort Distribution by Phase (Based on Audit Complexity Analysis)

#### Phase 1 (Months 1-3): 70% Total Effort
**Critical Path Focus - Highest Impact Rules**
- Rule 27 (Custodians Token): 30% of phase effort (4 weeks - includes testing)
- Rule 92 (Trade Strategy Card): 25% of phase effort (3 weeks - includes testing)
- Rule 81 (Status Phase): 20% of phase effort (2 weeks - completion + testing)
- Rule 89 (Tactical Action): 20% of phase effort (3 weeks - completion + testing)
- Integration & Validation: 5% of phase effort (1 week)

#### Phase 2 (Months 4-5): 20% Total Effort
**Strategic Depth & Balance Systems**
- Rule 28 (Deals): 35% of phase effort (2 weeks)
- Rule 96 (Supply Limit): 35% of phase effort (2 weeks)
- Strategy Cards (32, 45): 20% of phase effort (2 weeks)
- Integration & Balance Testing: 10% of phase effort (2 weeks)

#### Phase 3 (Months 6-8): 10% Total Effort
**Advanced Features & System Completions**
- Missing System Rules (70-73): 40% of phase effort (4 weeks)
- Advanced Features (Rules 1, 3): 35% of phase effort (4 weeks)
- System Completions & Polish: 25% of phase effort (4 weeks)

### Success Metrics & Milestones (Based on Audit Findings)

#### Phase 1 Success Criteria (Months 1-3) - CRITICAL PATH COMPLETION
- [ ] **Complete game can be played from setup to victory** (Primary Success Metric)
- [ ] All 4 critical blocking rules implemented with 95%+ test coverage
- [ ] End-to-end integration tests passing for complete gameplay loop
- [ ] Performance benchmarks within acceptable ranges (<2s per game action)
- [ ] Agenda phase activation functional via custodians token
- [ ] Complete economic strategy options available
- [ ] Full round progression through status phase
- [ ] Complete tactical action workflow operational

#### Phase 2 Success Criteria (Months 4-5) - STRATEGIC DEPTH
- [ ] Diplomatic gameplay functional with binding deals system
- [ ] Game balance mechanisms operational with supply limits
- [ ] All 8 strategy cards implemented and balanced
- [ ] Competitive gameplay validated through testing
- [ ] Player interaction systems fully operational

#### Phase 3 Success Criteria (Months 6-8) - SYSTEM COMPLETENESS
- [ ] All missing system rules (70-73) implemented
- [ ] Advanced ability features complete (Rules 1, 3)
- [ ] System performance optimized for production use
- [ ] Documentation complete and accurate
- [ ] Production deployment ready with full feature set

### Key Performance Indicators (Updated Based on Audit)

#### Development Velocity (Critical Path Focus)
- **Target**: 1 critical rule completion per 3-week cycle (including testing)
- **Measurement**: Critical rule implementation percentage
- **Quality Gate**: 95%+ test coverage per critical rule (higher standard)

#### System Quality (Audit-Informed Standards)
- **Target**: 0 critical bugs, <3 minor bugs per critical rule release
- **Measurement**: Bug count and severity tracking
- **Quality Gate**: All tests passing, strict mypy compliance, comprehensive integration tests

#### Integration Health (End-to-End Focus)
- **Target**: <2 second complete game turn execution
- **Measurement**: End-to-end gameplay performance
- **Quality Gate**: 100% integration test pass rate for complete gameplay scenarios

#### Test Coverage Quality (Audit-Based Standards)
- **Target**: 95%+ coverage for critical path rules, 90%+ for others
- **Measurement**: Line coverage and branch coverage analysis
- **Quality Gate**: Comprehensive edge case coverage, error condition testing

---

## 🔧 Development Guidelines

### TDD Process (Mandatory)
1. **RED**: Write failing test that demonstrates missing functionality
2. **GREEN**: Write minimal code to make test pass
3. **REFACTOR**: Clean up code while keeping tests green
4. **REPEAT**: For each small feature increment

### Quality Standards
- **Test Coverage**: 90%+ for each new rule implementation
- **Type Safety**: Strict mypy compliance for all production code
- **Code Quality**: Ruff formatting and linting compliance
- **Documentation**: Complete LRR analysis for each rule
- **Performance**: Sub-100ms response time for all game actions

### Integration Strategy
- **Sequential Dependencies**: Implement rules in dependency order
- **Incremental Integration**: Continuous integration with existing systems
- **Regression Testing**: Comprehensive cross-rule interaction validation
- **Backward Compatibility**: All existing functionality must remain intact

### Risk Mitigation

#### Technical Risks
1. **Integration Complexity**
   - Mitigation: Develop integration tests first
   - Contingency: Modular implementation with clear interfaces

2. **Performance Degradation**
   - Mitigation: Performance benchmarks for each rule
   - Contingency: Optimization sprints between phases

3. **Quality Regression**
   - Mitigation: Comprehensive regression test suite
   - Contingency: Automated quality gates blocking releases

#### Project Risks
1. **Scope Creep**
   - Mitigation: Strict adherence to critical path
   - Contingency: Feature freeze during critical phases

2. **Resource Constraints**
   - Mitigation: Focus on highest impact rules first
   - Contingency: Reduce scope to essential features only

3. **Timeline Pressure**
   - Mitigation: 20% buffer time in each phase
   - Contingency: Defer non-critical features to later phases

---

## 🎯 Roadmap Timeline Visualization (Audit-Based Critical Path)

```
Month 1: [████████████████████████████████] Rule 27: Custodians Token (CRITICAL BLOCKER)
Month 2: [████████████████] Rule 92: Trade [████████████████] Rule 81: Status Phase
Month 3: [████████████████████████████████] Rule 89: Tactical Action + Integration
Month 4: [████████████████] Rule 28: Deals [████████████████] Rule 96: Supply Limit
Month 5: [████████] Rule 32 [████████] Rule 45 [████████████████] Integration & Balance
Month 6: [████████████████████████████████] Rules 70-73: Missing System Rules
Month 7: [████████████████] Rule 1: Advanced [████████████████] Rule 3: Edge Cases
Month 8: [████████████████████████████████] System Completions & Production Polish
```

### Milestone Targets (Updated Based on Audit)
- **Month 3**: **CRITICAL MILESTONE** - Complete basic gameplay loop (55/101 rules - 54.5%)
  - **Success Criteria**: Full game playable from setup to victory
- **Month 5**: Competitive gameplay with diplomacy (59/101 rules - 58.4%)
  - **Success Criteria**: Strategic depth and game balance operational
- **Month 8**: Production-ready system (63/101 rules - 62.4%)
  - **Success Criteria**: Complete feature set with advanced capabilities
- **Optional Phase 4**: Full rule coverage (101/101 rules - 100%)
  - **Priority**: Only if resources available after core completion

---

## 🚀 Strategic Recommendations (Based on Audit Findings)

### Immediate Actions (Next 30 Days)
1. **Implement Critical Path Focus**
   - **STOP** all non-critical rule development immediately
   - **START** Rule 27 (Custodians Token) as highest priority
   - **ESTABLISH** critical path development workflow with 3-week cycles

2. **Restructure Team Allocation**
   - **ASSIGN** 50% of development resources to critical path lead
   - **FOCUS** remaining resources on strategic systems and quality assurance
   - **ESTABLISH** weekly progress reporting on critical blocking rules

3. **Implement Audit-Based Quality Gates**
   - **RAISE** test coverage requirement to 95% for critical path rules
   - **IMPLEMENT** comprehensive integration testing for complete gameplay scenarios
   - **ESTABLISH** performance benchmarking for end-to-end gameplay (<2s per action)

### Success Factors (Audit-Informed)
1. **Critical Path Focus**: 70% effort on 4 critical blocking rules (27, 92, 81, 89)
2. **Quality Excellence**: Maintain 95%+ test coverage for critical rules, 90%+ for others
3. **Integration First**: End-to-end gameplay validation as primary success metric
4. **Velocity Management**: Target 1 critical rule completion per 3-week cycle (including testing)

### Risk Mitigation (Based on Audit Complexity Assessment)
1. **Rule 27 Complexity**: Allocate full month due to game flow integration complexity
2. **Integration Risks**: Dedicate 15% of resources to integration specialist role
3. **Quality Regression**: Maintain comprehensive regression testing throughout
4. **Scope Management**: Defer all non-critical features until Phase 4 (optional)

### Long-Term Strategic Vision
This audit-based roadmap will deliver a **fully functional TI4 AI system in 3 months** (basic gameplay) and **production-ready system in 8 months**, compared to 18+ months with the previous approach. The focus on critical path completion ensures maximum impact per development hour invested.

**Key Success Metric**: Complete TI4 game playable from setup to victory by Month 3.
## Rule 27: Custodians Token (LRR 27.0–27.4)

Status: Implemented with unit tests; integration tests pending

Acceptance Criteria implemented:
- Cost: Spend 6 influence to remove the token
- Ship presence: Player must have at least one ship in the Mecatol Rex system
- Ground force commitment: Player must commit at least one ground force which lands on Mecatol Rex upon removal
- VP award: Player gains 1 victory point on successful removal
- Agenda phase activation: Agenda phase is activated thereafter
- Landing restriction: Ground forces cannot land on Mecatol Rex while the token is present

Code components:
- Core logic: `src/ti4/core/custodians_token.py`
- Helpers: `src/ti4/core/game_state.py` (influence and ship presence checks)
- Planet restrictions: `src/ti4/core/planet.py` (landing restriction with token)

Unit Tests:
- File: `tests/test_rule_27_custodians_token.py`
- Covered cases: prerequisites checks, successful removal flow (VP + agenda), landing with ground force, failure without ground force, landing restriction with token, insufficient influence, no ships present, idempotent removal (VP awarded once)

Next Steps:
- Add integration tests to validate that agenda phase is properly enabled in subsequent rounds and interacts correctly with phase transitions and other strategy cards.

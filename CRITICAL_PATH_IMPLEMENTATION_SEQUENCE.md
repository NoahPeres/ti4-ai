# Critical Path Implementation Sequence

## Overview

This document provides detailed implementation sequence documentation for the 4 critical blocking rules identified in the comprehensive implementation status audit: **Rules 27, 92, 81, and 89**. These rules represent the critical path to achieving complete TI4 AI gameplay functionality.

**Strategic Priority**: These 4 rules block core gameplay functionality and must be completed before any other development work to achieve maximum impact per development hour invested.

## Critical Path Rules Summary

| Rule | Title | Status | Impact | Complexity | Timeline |
|------|-------|--------|---------|------------|----------|
| **27** | Custodians Token | ❌ Not Started (0%) | **GAME FLOW BLOCKER** | Medium | 4 weeks |
| **92** | Trade Strategy Card | ✅ Complete (100%) | **ECONOMIC SYSTEM COMPLETE** | Low-Medium | 3 weeks |
| **81** | Status Phase | ⚠️ Partial (30%) | **ROUND MANAGEMENT GAP** | Medium | 2 weeks |
| **89** | Tactical Action | ⚠️ Partial (60%) | **CORE GAMEPLAY GAP** | High | 3 weeks |

**Total Critical Path Timeline**: 12 weeks (3 months) for complete basic gameplay functionality

---

## Rule 27: Custodians Token - HIGHEST PRIORITY BLOCKER

### Impact Analysis
**CRITICAL BLOCKER**: Completely prevents agenda phase activation, blocking the entire political gameplay layer.

### Current Implementation Status
- **Implementation**: ❌ **0% Complete** - No custodians token entity exists
- **Test Coverage**: ❌ **0% Coverage** - No test files found
- **Dependencies**: ✅ **Ready** - All supporting systems implemented (agenda phase, influence, victory points)

### Technical Dependencies (All Available)
- ✅ **Agenda Phase System** (`src/ti4/core/agenda_phase.py`) - Ready for integration
- ✅ **Victory Points System** (`src/ti4/core/objective.py`) - Ready for VP awards
- ✅ **Influence System** (`src/ti4/core/resource_management.py`) - Ready for spending validation
- ✅ **Ground Forces System** (`src/ti4/core/unit.py`) - Ready for commitment validation
- ✅ **Planet System** (`src/ti4/core/planet.py`) - Ready for Mecatol Rex enhancement

### Implementation Sequence (4 weeks)

#### Week 1: Core Token System Foundation
**Goal**: Create custodians token entity and basic mechanics

**Tasks**:
1. **Create CustodiansToken Class** (2 days)
   ```python
   # File: src/ti4/core/custodians_token.py
   class CustodiansToken:
       def __init__(self, location: str = "mecatol_rex")
       def is_on_mecatol_rex(self) -> bool
       def can_be_removed_by_player(self, player_id: str, game_state: GameState) -> bool
   ```

2. **Enhance Mecatol Rex Planet** (2 days)
   ```python
   # Enhancement to src/ti4/core/planet.py
   class Planet:
       def has_custodians_token(self) -> bool
       def prevents_ground_force_landing(self) -> bool
   ```

3. **Implement Landing Restrictions** (1 day)
   ```python
   # Enhancement to ground force landing validation
   def can_land_ground_forces(planet: Planet, player_id: str) -> bool:
       if planet.has_custodians_token():
           return False
       return True
   ```

**Success Criteria Week 1**:
- ✅ CustodiansToken class created with basic state management
- ✅ Mecatol Rex enhanced with special properties
- ✅ Ground force landing restrictions implemented
- ✅ Basic unit tests passing (>90% coverage)

#### Week 2: Token Removal Mechanism
**Goal**: Implement influence spending and ship presence validation

**Tasks**:
1. **Implement Influence Spending Validation** (2 days)
   ```python
   # Enhancement to src/ti4/core/resource_management.py
   def can_spend_influence_for_custodians_token(
       player_id: str,
       game_state: GameState
   ) -> bool:
       return get_available_influence(player_id, game_state) >= 6
   ```

2. **Implement Ship Presence Validation** (2 days)
   ```python
   # Enhancement to system validation
   def has_ships_in_mecatol_rex(player_id: str, game_state: GameState) -> bool:
       mecatol_system = game_state.get_system_by_name("mecatol_rex")
       return any(unit.owner == player_id for unit in mecatol_system.space_units)
   ```

3. **Implement Token Removal Logic** (1 day)
   ```python
   def remove_custodians_token(
       player_id: str,
       game_state: GameState
   ) -> GameState:
       # Validate requirements (6 influence + ships)
       # Remove token from Mecatol Rex
       # Spend influence
       # Return updated game state
   ```

**Success Criteria Week 2**:
- ✅ Influence spending validation (6 influence requirement)
- ✅ Ship presence validation in Mecatol Rex system
- ✅ Token removal mechanism functional
- ✅ Comprehensive test coverage for removal requirements

#### Week 3: Ground Force Commitment and Victory Points
**Goal**: Complete token removal with ground force commitment and VP award

**Tasks**:
1. **Implement Ground Force Commitment** (2 days)
   ```python
   def commit_ground_force_to_mecatol_rex(
       player_id: str,
       ground_force_unit: Unit,
       game_state: GameState
   ) -> GameState:
       # Validate ground force availability
       # Land ground force on Mecatol Rex
       # Update game state
   ```

2. **Implement Victory Point Award** (2 days)
   ```python
   def award_custodians_token_victory_point(
       player_id: str,
       game_state: GameState
   ) -> GameState:
       # Award 1 victory point to player
       # Update victory point tracking
       # Check victory conditions
   ```

3. **Integration Testing** (1 day)
   - End-to-end token removal workflow
   - Multi-player competition scenarios
   - Error condition handling

**Success Criteria Week 3**:
- ✅ Ground force commitment mandatory and functional
- ✅ Victory point award system integrated
- ✅ Complete token removal workflow operational
- ✅ Integration tests passing for all scenarios

#### Week 4: Agenda Phase Activation and Quality Assurance
**Goal**: Complete agenda phase integration and comprehensive testing

**Tasks**:
1. **Implement Agenda Phase Trigger** (2 days)
   ```python
   # Enhancement to src/ti4/core/agenda_phase.py
   def activate_agenda_phase_after_custodians_removal(
       game_state: GameState
   ) -> GameState:
       # Mark agenda phase as active for future rounds
       # Update game phase progression
       # Notify all players of political game activation
   ```

2. **Comprehensive Quality Assurance** (2 days)
   - Performance testing (token removal <100ms)
   - Edge case validation (multiple players, insufficient resources)
   - Integration with existing systems validation
   - Documentation completion

3. **Production Readiness** (1 day)
   - Code review and refactoring
   - Final test coverage validation (target: 95%+)
   - Performance benchmarking

**Success Criteria Week 4**:
- ✅ Agenda phase activates after custodians token removal
- ✅ Complete end-to-end gameplay integration
- ✅ 95%+ test coverage achieved
- ✅ Performance benchmarks met (<100ms per operation)
- ✅ **CRITICAL MILESTONE**: Political gameplay layer unlocked

### Integration Points
1. **Game State Integration**: Token state tracked in main game state
2. **Phase Management**: Agenda phase activation trigger
3. **Resource Management**: Influence spending validation
4. **Victory Conditions**: VP tracking and game end detection
5. **Multi-Player Support**: Competition for token removal

### Success Validation
**Complete When**:
- ✅ Custodians token prevents ground force landing on Mecatol Rex
- ✅ Token removable with 6 influence + ships in system + ground force commitment
- ✅ Player gains 1 victory point for token removal
- ✅ Agenda phase activates for all future rounds after removal
- ✅ Multi-player competition scenarios work correctly
- ✅ 95%+ test coverage with comprehensive edge case handling

---

## Rule 92: Trade Strategy Card - ECONOMIC SYSTEM COMPLETE ✅

### Impact Analysis
**ECONOMIC SYSTEM COMPLETE**: Essential economic strategy option fully implemented, completing player economic strategies.

### Implementation Status: ✅ COMPLETE
- **Implementation**: ✅ **100% Complete** - Full production-ready implementation
- **Test Coverage**: ✅ **95%+ Coverage** - Comprehensive test suite with edge cases
- **Dependencies**: ✅ **Integrated** - Complete integration with commodity and resource systems
- **Performance**: ✅ **Optimized** - Primary <50ms, Secondary <25ms execution times
- **Quality**: ✅ **Production Ready** - Full type safety, error handling, and documentation

### Technical Dependencies (All Available)
- ✅ **Commodity System** (`src/ti4/core/resource_management.py`) - Ready for replenishment
- ✅ **Strategy Card Framework** (`src/ti4/core/strategy_cards/`) - Ready for Trade implementation
- ✅ **Command Token System** (`src/ti4/core/command_tokens.py`) - Ready for secondary ability costs
- ✅ **Trade Goods System** - Ready for trade good generation

### Implementation Sequence (3 weeks)

#### Week 1: Primary Ability Implementation
**Goal**: Implement Trade strategy card primary ability (gain trade goods + replenish commodities)

**Tasks**:
1. **Implement Trade Good Generation** (2 days)
   ```python
   # Enhancement to src/ti4/core/strategy_cards/cards/trade.py
   def execute_primary_ability(self, player_id: str, game_state: GameState) -> StrategyCardAbilityResult:
       # Step 1: Gain 3 trade goods
       new_state = self._gain_trade_goods(player_id, game_state, 3)
       # Step 2: Replenish commodities to faction maximum
       new_state = self._replenish_commodities(player_id, new_state)
       # Step 3: Choose players for free secondary ability
       return StrategyCardAbilityResult(success=True, new_game_state=new_state)
   ```

2. **Implement Commodity Replenishment** (2 days)
   ```python
   def _replenish_commodities(self, player_id: str, game_state: GameState) -> GameState:
       faction_max = game_state.get_player_faction_commodity_limit(player_id)
       current_commodities = game_state.get_player_commodities(player_id)
       commodities_to_add = faction_max - current_commodities
       return game_state.add_commodities(player_id, commodities_to_add)
   ```

3. **Unit Testing** (1 day)
   - Primary ability execution tests
   - Trade good generation validation
   - Commodity replenishment validation

**Success Criteria Week 1**:
- ✅ Primary ability gains 3 trade goods
- ✅ Primary ability replenishes commodities to faction maximum
- ✅ Unit tests passing with >90% coverage

#### Week 2: Secondary Ability and Player Selection
**Goal**: Implement secondary ability and player selection mechanics

**Tasks**:
1. **Implement Secondary Ability** (2 days)
   ```python
   def execute_secondary_ability(self, player_id: str, game_state: GameState) -> StrategyCardAbilityResult:
       # Validate command token cost
       if not self._can_pay_command_token(player_id, game_state):
           return StrategyCardAbilityResult(success=False, error_message="No command tokens")

       # Spend command token and replenish commodities
       new_state = game_state.spend_command_token(player_id, "strategy")
       new_state = self._replenish_commodities(player_id, new_state)
       return StrategyCardAbilityResult(success=True, new_game_state=new_state)
   ```

2. **Implement Player Selection for Free Secondary** (2 days)
   ```python
   def choose_players_for_free_secondary(
       self,
       active_player_id: str,
       chosen_players: list[str],
       game_state: GameState
   ) -> GameState:
       # Allow chosen players to use secondary ability without command token cost
       for player_id in chosen_players:
           game_state = self._replenish_commodities(player_id, game_state)
       return game_state
   ```

3. **Integration Testing** (1 day)
   - Secondary ability with command token cost
   - Free secondary ability for chosen players
   - Multi-player interaction scenarios

**Success Criteria Week 2**:
- ✅ Secondary ability costs 1 command token from strategy pool
- ✅ Secondary ability replenishes commodities
- ✅ Active player can choose players for free secondary ability
- ✅ Integration tests passing

#### Week 3: Strategy Card Integration and Quality Assurance
**Goal**: Complete integration with strategy card system and comprehensive testing

**Tasks**:
1. **Strategy Card System Integration** (2 days)
   ```python
   # Integration with src/ti4/core/strategy_card_coordinator.py
   def register_trade_strategy_card():
       coordinator.register_card(StrategyCardType.TRADE, TradeStrategyCard())

   # Ensure proper initiative value (5) and sequencing
   def get_initiative_value(self) -> int:
       return 5
   ```

2. **Comprehensive Testing and Quality Assurance** (2 days)
   - Performance testing (strategy card execution <50ms)
   - Edge case validation (no commodities to replenish, insufficient command tokens)
   - Multi-player economic balance testing
   - Integration with existing economic systems

3. **Documentation and Production Readiness** (1 day)
   - Complete LRR analysis update
   - Code documentation and examples
   - Performance benchmarking

**Success Criteria Week 3**:
- ✅ Trade strategy card fully integrated with strategy card system
- ✅ Initiative value 5 properly sequenced
- ✅ 95%+ test coverage achieved
- ✅ Performance benchmarks met (<50ms execution)
- ✅ **MILESTONE**: Complete economic strategy options available

### Integration Points
1. **Strategy Card System**: Full integration with coordinator and registry
2. **Economic Systems**: Commodity and trade good management
3. **Command Token System**: Secondary ability cost validation
4. **Multi-Player Interaction**: Player selection and free abilities

### Success Validation
**Complete When**:
- ✅ Primary ability: Gain 3 trade goods + replenish commodities + choose players
- ✅ Secondary ability: Spend 1 command token + replenish commodities
- ✅ Initiative value 5 properly integrated
- ✅ Multi-player economic interactions functional
- ✅ 95%+ test coverage with comprehensive economic scenarios

---

## Rule 81: Status Phase - ROUND MANAGEMENT COMPLETION

### Impact Analysis
**ROUND MANAGEMENT GAP**: Incomplete round progression preventing proper game flow and objective management.

### Current Implementation Status
- **Implementation**: ⚠️ **30% Complete** - Basic card readying implemented, missing core steps
- **Test Coverage**: ⚠️ **Limited** - Only agent readying tests found
- **Dependencies**: ✅ **Ready** - Objective and card systems implemented

### Technical Dependencies (All Available)
- ✅ **Objective System** (`src/ti4/core/objective.py`) - Ready for scoring
- ✅ **Action Card System** (`src/ti4/core/action_cards.py`) - Ready for drawing
- ✅ **Command Token System** (`src/ti4/core/command_tokens.py`) - Ready for redistribution
- ✅ **Strategy Card System** (`src/ti4/core/strategy_card.py`) - Ready for return

### Existing Implementation Analysis
```python
# Current: src/ti4/core/status_phase.py (30% complete)
class StatusPhaseManager:
    def ready_all_cards(self, game_state: GameState) -> GameState:  # ✅ Implemented
    def speaker_reveal_objective(self, game_state: GameState) -> GameState:  # ❌ TODO
    def speaker_setup_objectives(self, game_state: GameState) -> GameState:  # ❌ TODO
```

### Implementation Sequence (2 weeks)

#### Week 1: Core Status Phase Steps Implementation
**Goal**: Implement missing status phase steps (score objectives, reveal objectives, draw action cards)

**Tasks**:
1. **Implement Step 1: Score Objectives** (2 days)
   ```python
   def execute_score_objectives_step(self, game_state: GameState) -> GameState:
       # Following initiative order, each player may score objectives
       for player_id in game_state.get_initiative_order():
           # Allow scoring up to 1 public and 1 secret objective
           game_state = self._allow_objective_scoring(player_id, game_state)
       return game_state
   ```

2. **Implement Step 2: Reveal Public Objective** (1 day)
   ```python
   def execute_reveal_objective_step(self, game_state: GameState) -> GameState:
       speaker_id = game_state.get_speaker()
       # Speaker reveals next unrevealed public objective
       return game_state.reveal_next_public_objective(speaker_id)
   ```

3. **Implement Step 3: Draw Action Cards** (2 days)
   ```python
   def execute_draw_action_cards_step(self, game_state: GameState) -> GameState:
       # Following initiative order, each player draws one action card
       for player_id in game_state.get_initiative_order():
           game_state = game_state.draw_action_card(player_id)
       return game_state
   ```

**Success Criteria Week 1**:
- ✅ Step 1: Score objectives functional with initiative order
- ✅ Step 2: Speaker reveals public objectives
- ✅ Step 3: Action card drawing for all players
- ✅ Unit tests passing for all new steps

#### Week 2: Command Token Management and Complete Integration
**Goal**: Complete remaining steps and integrate full status phase workflow

**Tasks**:
1. **Implement Steps 4-5: Command Token Management** (2 days)
   ```python
   def execute_remove_command_tokens_step(self, game_state: GameState) -> GameState:
       # Step 4: Remove all command tokens from game board
       for player_id in game_state.players:
           game_state = game_state.remove_all_command_tokens_from_board(player_id)
       return game_state

   def execute_gain_redistribute_tokens_step(self, game_state: GameState) -> GameState:
       # Step 5: Gain 2 command tokens and redistribute
       for player_id in game_state.players:
           game_state = game_state.gain_command_tokens(player_id, 2)
           # Allow redistribution among strategy, tactic, fleet pools
           game_state = self._allow_token_redistribution(player_id, game_state)
       return game_state
   ```

2. **Implement Steps 6-8: Cleanup and Preparation** (2 days)
   ```python
   def execute_repair_units_step(self, game_state: GameState) -> GameState:
       # Step 7: Repair all damaged units
       for player_id in game_state.players:
           game_state = game_state.repair_all_damaged_units(player_id)
       return game_state

   def execute_return_strategy_cards_step(self, game_state: GameState) -> GameState:
       # Step 8: Return strategy cards to common area
       return game_state.return_all_strategy_cards()
   ```

3. **Complete Status Phase Orchestration** (1 day)
   ```python
   def execute_complete_status_phase(self, game_state: GameState) -> GameState:
       # Execute all 8 steps in sequence
       new_state = self.execute_score_objectives_step(game_state)
       new_state = self.execute_reveal_objective_step(new_state)
       new_state = self.execute_draw_action_cards_step(new_state)
       new_state = self.execute_remove_command_tokens_step(new_state)
       new_state = self.execute_gain_redistribute_tokens_step(new_state)
       new_state = self.ready_all_cards(new_state)  # Step 6 - already implemented
       new_state = self.execute_repair_units_step(new_state)
       new_state = self.execute_return_strategy_cards_step(new_state)

       # Check if agenda phase should be added (if custodians token removed)
       if new_state.is_agenda_phase_active():
           new_state = new_state.set_next_phase("agenda")
       else:
           new_state = new_state.set_next_phase("strategy")

       return new_state
   ```

**Success Criteria Week 2**:
- ✅ Steps 4-8: All remaining status phase steps implemented
- ✅ Complete status phase orchestration functional
- ✅ Round progression with proper phase transitions
- ✅ 95%+ test coverage for complete status phase workflow
- ✅ **MILESTONE**: Complete round management operational

### Integration Points
1. **Objective System**: Scoring and revealing objectives
2. **Action Card System**: Drawing cards for all players
3. **Command Token System**: Removal, gain, and redistribution
4. **Strategy Card System**: Card return and readying
5. **Phase Management**: Transition to next round or agenda phase

### Success Validation
**Complete When**:
- ✅ All 8 status phase steps execute in proper sequence
- ✅ Initiative order respected for player actions
- ✅ Objective scoring and revealing functional
- ✅ Command token management complete
- ✅ Round transitions properly to next phase
- ✅ Integration with agenda phase activation (custodians token dependency)

---

## Rule 89: Tactical Action - CORE GAMEPLAY COMPLETION

### Impact Analysis
**CORE GAMEPLAY GAP**: Incomplete tactical action workflow preventing complete turn-based gameplay.

### Current Implementation Status
- **Implementation**: ⚠️ **60% Complete** - Validation logic exists, missing workflow integration
- **Test Coverage**: ⚠️ **Partial** - Integration tests exist but incomplete
- **Dependencies**: ✅ **Ready** - Movement, combat, and production systems implemented

### Technical Dependencies (All Available)
- ✅ **Movement System** (`src/ti4/core/movement.py`) - Advanced movement engine ready
- ✅ **Combat System** (`src/ti4/core/combat.py`) - Space and ground combat ready
- ✅ **Production System** (`src/ti4/core/production.py`) - Production abilities ready
- ✅ **Command Token System** (`src/ti4/core/command_tokens.py`) - System activation ready

### Existing Implementation Analysis
```python
# Current: src/ti4/core/tactical_actions.py (60% complete)
class TacticalActionValidator:
    def can_activate_system(self, system, player, galaxy) -> bool:  # ✅ Implemented
    def activate_system(self, system, player, command_sheet, galaxy) -> ActivationResult:  # ✅ Implemented
    def execute_movement_step(self, source, target, ships, player, galaxy) -> MovementResult:  # ✅ Implemented
    def requires_space_combat(self, system) -> bool:  # ✅ Implemented
    def can_use_bombardment(self, system, player) -> bool:  # ✅ Implemented
    def can_resolve_production_abilities(self, system, player) -> bool:  # ✅ Implemented
    # ❌ Missing: Complete workflow orchestration and integration
```

### Implementation Sequence (3 weeks)

#### Week 1: Tactical Action Workflow Orchestration
**Goal**: Create complete tactical action workflow integrating all 5 steps

**Tasks**:
1. **Create Tactical Action Orchestrator** (2 days)
   ```python
   # New: src/ti4/core/tactical_action_orchestrator.py
   class TacticalActionOrchestrator:
       def execute_complete_tactical_action(
           self,
           player_id: str,
           target_system_id: str,
           game_state: GameState
       ) -> TacticalActionResult:
           # Step 1: Activation
           result = self._execute_activation_step(player_id, target_system_id, game_state)
           if not result.success:
               return result

           # Step 2: Movement
           result = self._execute_movement_step(player_id, target_system_id, result.game_state)
           if not result.success:
               return result

           # Step 3: Space Combat (if required)
           if self._requires_space_combat(target_system_id, result.game_state):
               result = self._execute_space_combat_step(target_system_id, result.game_state)

           # Step 4: Invasion (if applicable)
           result = self._execute_invasion_step(player_id, target_system_id, result.game_state)

           # Step 5: Production (if applicable)
           result = self._execute_production_step(player_id, target_system_id, result.game_state)

           return result
   ```

2. **Implement Step Integration Logic** (2 days)
   ```python
   def _execute_activation_step(self, player_id: str, system_id: str, game_state: GameState) -> TacticalActionResult:
       # Use existing TacticalActionValidator.activate_system
       validator = TacticalActionValidator()
       system = game_state.get_system(system_id)
       command_sheet = game_state.get_player_command_sheet(player_id)

       result = validator.activate_system(system, player_id, command_sheet, game_state.galaxy)
       if result.success:
           return TacticalActionResult(success=True, game_state=game_state.place_command_token(player_id, system_id))
       return TacticalActionResult(success=False, error_message=result.error_message)
   ```

3. **Unit Testing for Orchestration** (1 day)
   - Complete tactical action workflow tests
   - Step-by-step validation tests
   - Error handling and rollback tests

**Success Criteria Week 1**:
- ✅ Complete tactical action orchestrator created
- ✅ All 5 steps integrated in proper sequence
- ✅ Error handling and validation at each step
- ✅ Unit tests passing for workflow orchestration

#### Week 2: Combat and Invasion Integration
**Goal**: Complete integration with combat and invasion systems

**Tasks**:
1. **Integrate Space Combat Step** (2 days)
   ```python
   def _execute_space_combat_step(self, system_id: str, game_state: GameState) -> TacticalActionResult:
       # Use existing space combat system
       from .space_combat import SpaceCombatManager

       combat_manager = SpaceCombatManager()
       system = game_state.get_system(system_id)

       if combat_manager.requires_space_combat(system):
           combat_result = combat_manager.resolve_space_combat(system, game_state)
           return TacticalActionResult(success=True, game_state=combat_result.game_state)

       return TacticalActionResult(success=True, game_state=game_state)
   ```

2. **Integrate Invasion Step** (2 days)
   ```python
   def _execute_invasion_step(self, player_id: str, system_id: str, game_state: GameState) -> TacticalActionResult:
       # Use existing invasion system
       from .invasion import InvasionManager
       from .bombardment import BombardmentManager

       # Execute bombardment if applicable
       bombardment_manager = BombardmentManager()
       if bombardment_manager.can_use_bombardment(system, player_id):
           game_state = bombardment_manager.execute_bombardment(player_id, system_id, game_state)

       # Execute ground force landing and ground combat
       invasion_manager = InvasionManager()
       invasion_result = invasion_manager.execute_invasion(player_id, system_id, game_state)

       return TacticalActionResult(success=True, game_state=invasion_result.game_state)
   ```

3. **Integration Testing** (1 day)
   - Combat integration scenarios
   - Invasion workflow validation
   - Multi-step tactical action scenarios

**Success Criteria Week 2**:
- ✅ Space combat integrated into tactical action workflow
- ✅ Invasion step with bombardment and ground combat integrated
- ✅ Complex tactical action scenarios working
- ✅ Integration tests passing

#### Week 3: Production Integration and Complete Workflow
**Goal**: Complete production integration and finalize tactical action system

**Tasks**:
1. **Integrate Production Step** (2 days)
   ```python
   def _execute_production_step(self, player_id: str, system_id: str, game_state: GameState) -> TacticalActionResult:
       # Use existing production system
       from .production import ProductionManager

       production_manager = ProductionManager()
       system = game_state.get_system(system_id)

       if production_manager.can_resolve_production_abilities(system, player_id):
           production_result = production_manager.resolve_production_abilities(
               player_id, system_id, game_state
           )
           return TacticalActionResult(success=True, game_state=production_result.game_state)

       return TacticalActionResult(success=True, game_state=game_state)
   ```

2. **Component Action Integration** (2 days)
   ```python
   def allow_component_actions_during_tactical_action(
       self,
       player_id: str,
       system_id: str,
       game_state: GameState
   ) -> GameState:
       # Allow component actions during appropriate timing windows
       # Integrate with existing component action system
       from .component_action import ComponentActionManager

       component_manager = ComponentActionManager()
       return component_manager.process_component_actions_during_tactical_action(
           player_id, system_id, game_state
       )
   ```

3. **Comprehensive Quality Assurance** (1 day)
   - End-to-end tactical action testing
   - Performance optimization (target: <200ms per tactical action)
   - Edge case validation and error handling
   - Integration with existing game systems

**Success Criteria Week 3**:
- ✅ Production step fully integrated
- ✅ Component actions during tactical actions supported
- ✅ Complete tactical action workflow operational
- ✅ 95%+ test coverage achieved
- ✅ Performance benchmarks met (<200ms per action)
- ✅ **MILESTONE**: Complete tactical gameplay functional

### Integration Points
1. **Command Token System**: System activation and token placement
2. **Movement System**: Advanced movement engine integration
3. **Combat Systems**: Space combat and ground combat integration
4. **Production System**: Unit production during tactical actions
5. **Component Action System**: Timing window management

### Success Validation
**Complete When**:
- ✅ All 5 tactical action steps execute in proper sequence
- ✅ System activation with command token placement functional
- ✅ Movement, combat, invasion, and production fully integrated
- ✅ Component actions supported during appropriate timing windows
- ✅ Complete tactical action workflow from activation to completion
- ✅ Performance and quality standards met

---

## Dependencies and Integration Matrix

### Critical Path Dependencies
```
Rule 27 (Custodians Token) → Rule 81 (Status Phase) → Complete Round Management
Rule 92 (Trade Strategy Card) → Complete Economic Strategy Options
Rule 89 (Tactical Action) → Complete Turn-Based Gameplay
All 4 Rules → Complete Basic Gameplay Loop
```

### System Integration Requirements

#### Shared Systems (All Rules Depend On)
- ✅ **Game State Management** - Central state coordination
- ✅ **Player Management** - Multi-player support
- ✅ **Resource Management** - Influence, commodities, trade goods
- ✅ **Command Token System** - Strategy and tactic token management

#### Cross-Rule Integration Points
1. **Rule 27 → Rule 81**: Custodians token removal triggers agenda phase in status phase
2. **Rule 81 → Rule 89**: Status phase prepares for next round of tactical actions
3. **Rule 92 → Rule 89**: Trade strategy card provides resources for tactical actions
4. **All Rules → Game Flow**: Complete turn sequence and round progression

### Quality Assurance Standards

#### Test Coverage Requirements
- **Rule 27**: 95%+ coverage (critical blocker priority)
- **Rule 92**: 95%+ coverage (economic system completion)
- **Rule 81**: 95%+ coverage (round management critical)
- **Rule 89**: 95%+ coverage (core gameplay critical)

#### Performance Benchmarks
- **Rule 27**: Custodians token operations <100ms
- **Rule 92**: Trade strategy card execution <50ms
- **Rule 81**: Complete status phase <500ms
- **Rule 89**: Complete tactical action <200ms

#### Integration Testing
- **End-to-End Gameplay**: Complete game from setup to victory
- **Multi-Player Scenarios**: 2-6 player game validation
- **Performance Testing**: Full game performance under load
- **Regression Testing**: All existing functionality preserved

---

## Success Criteria and Validation

### Phase 1 Success Criteria (Month 1: Rule 27)
- [ ] **CRITICAL MILESTONE**: Agenda phase can be activated via custodians token removal
- [ ] Custodians token prevents ground force landing on Mecatol Rex
- [ ] Token removal requires 6 influence + ships in system + ground force commitment
- [ ] Player gains 1 victory point for token removal
- [ ] Political gameplay layer unlocked for complete game experience

### Phase 2 Success Criteria (Month 2: Rules 92 + 81)
- [ ] **ECONOMIC MILESTONE**: Complete economic strategy options available
- [ ] Trade strategy card provides commodity replenishment and trade good generation
- [ ] **ROUND MANAGEMENT MILESTONE**: Complete round progression functional
- [ ] Status phase executes all 8 steps in proper sequence
- [ ] Round transitions properly between strategy, action, and status phases

### Phase 3 Success Criteria (Month 3: Rule 89)
- [ ] **CORE GAMEPLAY MILESTONE**: Complete tactical action workflow operational
- [ ] All 5 tactical action steps integrated and functional
- [ ] Movement, combat, invasion, and production systems fully integrated
- [ ] Component actions supported during tactical actions

### Final Integration Success Criteria (End of Month 3)
- [ ] **COMPLETE BASIC GAMEPLAY**: Full TI4 game playable from setup to victory
- [ ] All critical path rules implemented with 95%+ test coverage
- [ ] Performance benchmarks met for all critical operations
- [ ] Multi-player gameplay validated and functional
- [ ] **PROJECT MILESTONE**: TI4 AI system provides complete basic gameplay experience

---

## Risk Mitigation and Contingency Planning

### Technical Risks

#### High Complexity Integration (Rule 89)
- **Risk**: Tactical action integration more complex than estimated
- **Mitigation**: Allocate 3 weeks with buffer time, start with simplest integration
- **Contingency**: Reduce scope to core workflow, defer advanced features

#### Performance Issues
- **Risk**: Complex workflows exceed performance benchmarks
- **Mitigation**: Performance testing throughout development, optimization focus
- **Contingency**: Implement caching and optimization strategies

#### Integration Conflicts
- **Risk**: New implementations conflict with existing systems
- **Mitigation**: Comprehensive regression testing, incremental integration
- **Contingency**: Rollback capability and isolated development branches

### Project Risks

#### Timeline Pressure
- **Risk**: Critical path takes longer than 3 months
- **Mitigation**: Focus strictly on critical path, defer all non-essential features
- **Contingency**: Reduce scope to absolute minimum for basic gameplay

#### Resource Constraints
- **Risk**: Insufficient development resources for parallel work
- **Mitigation**: Sequential implementation with clear priorities
- **Contingency**: Focus on highest impact rule (Rule 27) first

#### Quality Regression
- **Risk**: New implementations break existing functionality
- **Mitigation**: Comprehensive test coverage and continuous integration
- **Contingency**: Automated rollback and quality gate enforcement

### Success Factors

#### Critical Path Focus
- **80% of development effort** on these 4 critical rules
- **No feature creep** - strict adherence to critical path
- **Quality over speed** - ensure each rule is production-ready before moving to next

#### Integration-First Approach
- **End-to-end testing** from day one
- **Incremental integration** with existing systems
- **Performance monitoring** throughout development

#### Quality Assurance Excellence
- **95%+ test coverage** for all critical path rules
- **Comprehensive edge case testing** for multi-player scenarios
- **Performance benchmarking** for production readiness

---

## Conclusion

This critical path implementation sequence provides a clear roadmap to achieve **complete TI4 AI basic gameplay functionality in 3 months** by focusing exclusively on the 4 critical blocking rules identified in the comprehensive implementation status audit.

**Key Success Factors**:
1. **Strict Critical Path Focus**: 80% effort on Rules 27, 92, 81, 89
2. **Quality Excellence**: 95%+ test coverage and performance benchmarks
3. **Integration-First**: End-to-end gameplay validation throughout
4. **Sequential Implementation**: Complete each rule before moving to next

**Expected Outcome**: By following this sequence, the TI4 AI system will progress from 50.5% complete (51/101 rules) to **complete basic gameplay functionality**, enabling full games from setup to victory with all critical systems operational.

This represents the most efficient path to delivering a fully functional TI4 AI system, providing maximum value per development hour invested.

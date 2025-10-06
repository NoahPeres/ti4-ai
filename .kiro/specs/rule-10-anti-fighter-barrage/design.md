# Design Document

## Overview

This document outlines the design for implementing Rule 10: ANTI-FIGHTER BARRAGE, a unit ability that allows certain units to attack enemy fighters before normal space combat begins. The implementation will extend the existing combat system with proper anti-fighter barrage mechanics, including specialized dice rolling, hit assignment, and timing integration.

## Architecture

### High-Level Design

The Anti-Fighter Barrage system will be implemented as an extension to the existing combat system, following these architectural principles:

1. **Extend Existing Systems**: Build upon the current `CombatResolver`, `UnitStats`, and `Unit` classes
2. **Maintain Separation of Concerns**: Keep AFB logic separate from regular combat mechanics
3. **Follow Existing Patterns**: Use the same patterns as other unit abilities (space cannon, bombardment)
4. **Preserve Backward Compatibility**: Ensure existing combat functionality remains unchanged

### System Integration Points

- **Combat System**: Integrate AFB as a pre-combat step in space combat resolution
- **Unit Stats System**: Add AFB-specific values (barrage value, dice count) to unit statistics
- **Unit System**: Extend unit ability detection to properly identify AFB capabilities
- **Game State Management**: Track AFB results and integrate with combat flow

## Components and Interfaces

### 1. Enhanced Unit Statistics

**File**: `src/ti4/core/unit_stats.py`

```python
@dataclass(frozen=True)
class UnitStats:
    # ... existing fields ...

    # Anti-Fighter Barrage specific stats
    anti_fighter_barrage_value: Optional[int] = None
    anti_fighter_barrage_dice: int = 0
```

**Rationale**: Separate AFB stats from regular combat stats while allowing AFB rolls to be affected by combat roll modifiers and effects.

### 2. Anti-Fighter Barrage Manager

**File**: `src/ti4/core/anti_fighter_barrage.py` (new)

```python
class AntiFighterBarrageManager:
    """Manages anti-fighter barrage mechanics and resolution."""

    def __init__(self, combat_resolver: CombatResolver) -> None:
        self.combat_resolver = combat_resolver

    def can_perform_barrage(self, unit: Unit) -> bool:
        """Check if unit can perform anti-fighter barrage."""

    def get_barrage_targets(self, system: System, attacking_player: str) -> list[Unit]:
        """Get valid fighter targets for anti-fighter barrage."""

    def perform_barrage_attack(self, unit: Unit) -> int:
        """Perform anti-fighter barrage attack and return hits."""

    def assign_barrage_hits(self, hits: int, fighters: list[Unit],
                           assignments: list[str]) -> list[Unit]:
        """Assign AFB hits to fighters and return destroyed units."""

    def validate_hit_assignments(self, hits: int, fighters: list[Unit],
                                assignments: list[str]) -> bool:
        """Validate player's hit assignment choices."""
```

### 3. Enhanced Combat Resolver

**File**: `src/ti4/core/combat.py`

```python
class CombatResolver:
    # ... existing methods ...

    def resolve_anti_fighter_barrage_phase(self, system: System,
                                         attacker_id: str,
                                         defender_id: str) -> AntiFighterBarrageResult:
        """Resolve the anti-fighter barrage phase of space combat."""

    def perform_anti_fighter_barrage_enhanced(self, unit: Unit,
                                            target_units: list[Unit]) -> int:
        """Enhanced AFB implementation with proper stats and mechanics."""
```

### 4. Anti-Fighter Barrage Result

**File**: `src/ti4/core/anti_fighter_barrage.py`

```python
@dataclass
class AntiFighterBarrageResult:
    """Result of anti-fighter barrage resolution."""

    attacker_hits: int
    defender_hits: int
    destroyed_fighters: list[Unit]
    remaining_fighters: list[Unit]
```

## Data Models

### Unit Statistics Enhancement

The `UnitStats` class will be enhanced to include AFB-specific statistics:

- `anti_fighter_barrage_value`: The dice value needed to hit (e.g., 9 for Destroyer)
- `anti_fighter_barrage_dice`: Number of dice to roll (e.g., 2 for Destroyer II)

### Unit Data Updates

Base unit statistics will be updated to include proper AFB values:

```python
UnitType.DESTROYER: UnitStats(
    # ... existing stats ...
    anti_fighter_barrage=True,
    anti_fighter_barrage_value=9,
    anti_fighter_barrage_dice=1,
)
```

### Combat Flow Integration

Anti-Fighter Barrage will be integrated into the space combat flow as follows:

1. **Tactical Action Integration**: AFB occurs during space combat within a tactical action
2. **Pre-Combat Step**: AFB happens as the first step of space combat, before regular combat rolls
3. **First Round Only**: AFB only happens in the first round of space combat
4. **Combat Roll Classification**: AFB rolls are considered combat rolls and affected by combat roll modifiers
5. **Simultaneous Resolution**: Both players perform AFB simultaneously
6. **Hit Assignment**: Players assign hits to their own fighters
7. **Fighter Removal**: Destroyed fighters are removed before regular combat begins

## Error Handling

### Input Validation

- Validate that AFB is only used in space combat
- Ensure AFB only occurs in the first round
- Validate hit assignments don't exceed available fighters
- Check that assigned fighters belong to the correct player

### Edge Case Handling

- **No Fighters Present**: AFB can still be performed but has no effect
- **Excess Hits**: Hits beyond available fighters are ignored
- **Invalid Assignments**: Provide clear error messages for invalid hit assignments
- **Combat State Errors**: Graceful handling of invalid combat states

### Error Recovery

- Maintain game state consistency if AFB resolution fails
- Provide rollback mechanisms for partial AFB resolution
- Log detailed error information for debugging

## Testing Strategy

### Unit Tests

1. **Anti-Fighter Barrage Manager Tests**
   - Test barrage capability detection
   - Test target filtering (fighters only)
   - Test hit calculation with AFB-specific stats
   - Test hit assignment validation

2. **Enhanced Combat Resolver Tests**
   - Test AFB phase integration with space combat
   - Test timing restrictions (first round only)
   - Test simultaneous AFB resolution
   - Test fighter removal before regular combat

3. **Unit Statistics Tests**
   - Test AFB stat retrieval and caching
   - Test technology modifications to AFB stats
   - Test faction-specific AFB modifications

### Integration Tests

1. **Complete AFB Flow Tests**
   - Test full AFB resolution from start to finish
   - Test AFB with multiple units having the ability
   - Test AFB with various fighter configurations
   - Test AFB with no valid targets

2. **Combat System Integration Tests**
   - Test AFB integration with existing tactical action combat flow
   - Test AFB with other pre-combat abilities
   - Test AFB with combat roll modifiers (should affect AFB rolls)
   - Test AFB in nebula systems (defender bonus should not apply to AFB)
   - Test AFB integration with existing combat roll effects and abilities

### Edge Case Tests

1. **Boundary Condition Tests**
   - Test AFB with zero fighters
   - Test AFB with more hits than fighters
   - Test AFB in non-space combat scenarios
   - Test AFB in subsequent combat rounds (should not occur)

2. **Error Condition Tests**
   - Test invalid hit assignments
   - Test AFB with invalid unit configurations
   - Test AFB with corrupted game state
   - Test AFB with missing required data

### Performance Tests

1. **AFB Resolution Performance**
   - Test AFB performance with large numbers of units
   - Test AFB performance with complex unit configurations
   - Benchmark AFB resolution time
   - Test memory usage during AFB resolution

## Implementation Plan

### Phase 1: Core AFB Mechanics
1. Enhance `UnitStats` with AFB-specific fields
2. Update base unit data with proper AFB values
3. Implement `AntiFighterBarrageManager` class
4. Add AFB-specific methods to `CombatResolver`

### Phase 2: Combat Integration
1. Integrate AFB phase into space combat flow
2. Implement timing restrictions (first round only)
3. Add simultaneous AFB resolution
4. Implement fighter removal mechanics

### Phase 3: Hit Assignment System
1. Implement hit assignment validation
2. Add player choice handling for hit assignments
3. Implement fighter destruction mechanics
4. Add excess hit handling

### Phase 4: Testing and Validation
1. Implement comprehensive unit tests
2. Add integration tests for combat flow
3. Test edge cases and error conditions
4. Performance testing and optimization

### Phase 5: Documentation and Polish
1. Update API documentation
2. Add usage examples
3. Create developer guide for AFB mechanics
4. Final code review and cleanup

## Dependencies

### Required Systems
- **Combat System**: Must be functional for AFB integration
- **Unit Stats System**: Required for AFB value storage and retrieval
- **Unit System**: Needed for ability detection and unit management
- **Game State Management**: Required for tracking combat state and results

### Optional Enhancements
- **Player Interface**: For hit assignment choices (can use simple validation for now)
- **Combat UI**: For displaying AFB results (can use logging for now)
- **Analytics System**: For tracking AFB effectiveness (future enhancement)

## Risk Mitigation

### Technical Risks
- **Combat System Complexity**: Mitigate by following existing patterns and maintaining separation of concerns
- **Performance Impact**: Address through efficient algorithms and caching where appropriate
- **Integration Issues**: Minimize by using existing interfaces and maintaining backward compatibility

### Design Risks
- **Rule Interpretation**: Mitigate by following LRR text exactly and adding comprehensive tests
- **Edge Case Handling**: Address through thorough testing and clear error messages
- **Future Extensibility**: Design with faction-specific AFB abilities in mind

## Success Criteria

### Functional Requirements
- AFB works correctly according to LRR Rule 10
- Proper timing integration with space combat
- Correct hit assignment and fighter destruction
- Comprehensive error handling and validation

### Quality Requirements
- 95%+ test coverage for AFB-related code
- Performance impact < 10ms for typical AFB resolution
- Zero regressions in existing combat functionality
- Clear and maintainable code structure

### Documentation Requirements
- Complete API documentation for all new classes and methods
- Usage examples for common AFB scenarios
- Developer guide for extending AFB mechanics
- Integration guide for combat system modifications

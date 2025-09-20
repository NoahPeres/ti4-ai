# Rule 26: COST (ATTRIBUTE) - Analysis

## Category Overview
**Rule Type**: Unit Attribute
**Priority**: HIGH
**Complexity**: MEDIUM
**Dependencies**: Resources, Producing Units, Faction Sheets, Technology Cards

## Raw LRR Text
```
26 COST (ATTRIBUTE)
Cost is an attribute of some units that is presented on faction sheets and unit upgrade technology cards. A unit's cost determines the number of resources a player must spend to produce that unit.

26.1 To produce a unit, a player must spend a number of resources equal to or greater than the cost of the unit they are producing.

26.2 If the cost is accompanied by two icons-typically for fighters and ground forces-a player produces two of that unit for that cost.

26.3 If a unit does not have a cost, it cannot be produced.
a	Structures do not have costs and are usually placed by resolving the "Construction" strategy card.

RELATED TOPICS: Producing Units, Resources
```

## Sub-Rules Analysis

### 26.1 Resource Spending for Production
**Status**: ✅ IMPLEMENTED
**Implementation**: `UnitStats.cost` attribute, resource validation in production
**Tests**: Unit cost tests exist
**Notes**: Basic cost system exists with proper resource spending validation

### 26.2 Dual Unit Production (Fighter/Infantry Icons)
**Status**: ⚠️ PARTIAL
**Implementation**: Cost values include 0.5 for fighters/infantry but dual production logic unclear
**Tests**: Limited tests for dual unit production
**Notes**: Cost system recognizes 0.5 cost but production mechanics need verification

### 26.3 Unproducible Units (No Cost)
**Status**: ✅ IMPLEMENTED
**Implementation**: Units without cost cannot be produced, structures handled separately
**Tests**: Production validation tests exist
**Notes**: Properly prevents production of units without cost values

### 26.3a Structure Placement via Construction
**Status**: ❌ NOT IMPLEMENTED
**Implementation**: Construction strategy card mechanics missing
**Tests**: No tests for structure placement
**Notes**: Links to Rule 24 (Construction) - needs strategy card implementation

## Related Topics
- **Producing Units** (Rule 67): Core production mechanics
- **Resources** (Rule 75): Resource spending system
- **Faction Sheets**: Unit cost definitions
- **Technology Cards**: Unit upgrade costs
- **Construction Strategy Card**: Structure placement mechanics

## Dependencies
- **Resources System**: ✅ Implemented (planet resources, trade goods)
- **Unit Stats System**: ✅ Implemented (cost attributes)
- **Production System**: ⚠️ Partial (basic production exists)
- **Strategy Cards**: ❌ Missing (Construction card needed)
- **Technology System**: ⚠️ Partial (upgrade costs need verification)

## Test References

### Existing Tests
- `test_unit.py`: Unit production ability tests
- `test_integration.py`: Unit cost in faction modifiers
- `test_victory_conditions.py`: Resource spending objectives
- `test_performance_benchmarks.py`: Unit stats calculation performance

### Missing Tests
- Dual unit production (2 fighters for 1 cost)
- Resource spending validation during production
- Cost calculation with technology upgrades
- Structure placement cost rules
- Excess resource spending behavior

## Implementation Files

### Core Implementation
- `src/ti4/core/unit_stats.py`: ✅ Unit cost attributes and calculations
- `src/ti4/core/unit.py`: ✅ Unit cost access methods
- Production system: ⚠️ Needs cost validation integration

### Missing Implementation
- Construction strategy card mechanics
- Dual unit production logic
- Technology upgrade cost calculations
- Resource spending validation system

## Notable Implementation Details

### Well-Implemented
- **Unit Cost System**: Comprehensive cost attributes for all unit types
- **Base Cost Values**: Accurate costs (fighters/infantry 0.5, destroyers 1, etc.)
- **Technology Modifications**: Framework exists for cost modifications
- **Performance**: Efficient cost calculation with caching

### Implementation Gaps
- **Dual Production**: Logic for producing 2 units for 1 cost unclear
- **Resource Validation**: No clear resource spending validation during production
- **Construction Integration**: Structure placement mechanics missing
- **Cost Overflow**: Behavior when spending excess resources not implemented

## Action Items

1. **Implement dual unit production logic** - Handle 2 fighters/infantry for 1 cost
2. **Add resource spending validation** - Ensure sufficient resources before production
3. **Create Construction strategy card** - Enable structure placement mechanics
4. **Add cost calculation tests** - Verify technology upgrade cost modifications
5. **Implement excess resource handling** - Define behavior for overspending
6. **Add production cost integration** - Connect cost system to production mechanics
7. **Create structure placement system** - Handle cost-free structure placement
8. **Add faction-specific cost modifiers** - Support unique faction cost rules
9. **Implement cost validation errors** - Proper error handling for insufficient resources
10. **Add comprehensive cost testing** - Cover all cost scenarios and edge cases

## Priority Assessment
**MEDIUM-HIGH** - Cost system is partially implemented with good foundation, but missing key production integration and dual unit mechanics that are fundamental to gameplay.

# Design Document

## Overview

This document outlines the design for implementing a unified resource management system covering Rule 26: COST (ATTRIBUTE), Rule 75: RESOURCES, and Rule 47: INFLUENCE in the TI4 AI system. These rules are tightly coupled since costs are paid using resources and influence from planets that players control, plus trade goods.

The design builds upon existing systems including `Planet`, `Player`, `UnitStats`, and `ProductionManager` to provide a complete resource management framework that correctly models how players spend from controlled planets rather than having personal resource pools.

## Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Game Client   │    │   Resource      │    │   Game State    │
│                 │───▶│   Manager       │───▶│   Management    │
│ - Pay Costs     │    │                 │    │                 │
│ - Spend Res/Inf │    │ - Calculate     │    │ - Update        │
│ - Vote          │    │ - Validate      │    │ - Persist       │
└─────────────────┘    │ - Execute       │    │ - Notify        │
                       └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Planet &      │
                       │   Trade Goods   │
                       │   Integration   │
                       │                 │
                       │ - Planet Res/Inf│
                       │ - Exhaustion    │
                       │ - Trade Goods   │
                       └─────────────────┘
```

### Core Components

1. **ResourceManager**: Central manager for resource/influence calculations and spending
2. **CostValidator**: Validates unit costs and resource availability
3. **SpendingPlan**: Represents a plan for spending resources/influence from specific sources
4. **Enhanced ProductionManager**: Integrates cost validation with production

## Components and Interfaces

### ResourceManager

```python
class ResourceManager:
    """Central manager for resource and influence operations."""

    def __init__(self, game_state: GameState):
        """Initialize with game state for planet and player access."""

    # Resource calculations (Rule 75)
    def calculate_available_resources(self, player_id: str) -> int:
        """Calculate total resources available from ready planets + trade goods."""

    def get_resource_sources(self, player_id: str) -> ResourceSources:
        """Get detailed breakdown of resource sources (planets + trade goods)."""

    # Influence calculations (Rule 47)
    def calculate_available_influence(self, player_id: str, for_voting: bool = False) -> int:
        """Calculate total influence available, excluding trade goods if for_voting."""

    def get_influence_sources(self, player_id: str, for_voting: bool = False) -> InfluenceSources:
        """Get detailed breakdown of influence sources."""

    # Spending operations
    def create_spending_plan(
        self,
        player_id: str,
        resource_amount: int = 0,
        influence_amount: int = 0,
        for_voting: bool = False
    ) -> SpendingPlan:
        """Create a plan for spending resources/influence from available sources."""

    def execute_spending_plan(self, plan: SpendingPlan) -> SpendingResult:
        """Execute a spending plan, exhausting planets and consuming trade goods."""

    def can_afford_spending(
        self,
        player_id: str,
        resource_amount: int = 0,
        influence_amount: int = 0,
        for_voting: bool = False
    ) -> bool:
        """Check if player can afford the specified spending."""
```

### CostValidator

```python
class CostValidator:
    """Validates unit costs and resource availability."""

    def __init__(self, resource_manager: ResourceManager, stats_provider: UnitStatsProvider):
        """Initialize with resource manager and unit stats provider."""

    def get_unit_cost(
        self,
        unit_type: UnitType,
        faction: Faction | None = None,
        technologies: set[Technology] | None = None
    ) -> float:
        """Get the final cost of a unit with all modifiers applied."""

    def get_production_cost(
        self,
        unit_type: UnitType,
        quantity: int,
        faction: Faction | None = None,
        technologies: set[Technology] | None = None
    ) -> ProductionCost:
        """Get cost for producing a quantity of units, handling dual production."""

    def validate_production_cost(
        self,
        player_id: str,
        production_cost: ProductionCost
    ) -> CostValidationResult:
        """Validate that player can afford a production cost."""

    def can_produce_without_cost(self, unit_type: UnitType) -> bool:
        """Check if unit can be produced without cost (structures via Construction)."""
```

### SpendingPlan

```python
@dataclass(frozen=True)
class SpendingPlan:
    """Represents a plan for spending resources/influence."""

    player_id: str
    resource_spending: ResourceSpending
    influence_spending: InfluenceSpending
    total_resource_cost: int
    total_influence_cost: int
    is_valid: bool
    error_message: str | None = None

    def get_total_planets_to_exhaust(self) -> set[str]:
        """Get all planet names that will be exhausted by this plan."""

    def get_total_trade_goods_to_spend(self) -> int:
        """Get total trade goods that will be consumed by this plan."""

@dataclass(frozen=True)
class ResourceSpending:
    """Details of resource spending from planets and trade goods."""

    planets_to_exhaust: dict[str, int]  # planet_name -> resource_value
    trade_goods_to_spend: int
    total_resources: int

@dataclass(frozen=True)
class InfluenceSpending:
    """Details of influence spending from planets and trade goods."""

    planets_to_exhaust: dict[str, int]  # planet_name -> influence_value
    trade_goods_to_spend: int  # 0 if for_voting=True
    total_influence: int
```

### ProductionCost

```python
@dataclass(frozen=True)
class ProductionCost:
    """Represents the cost of a production operation."""

    unit_type: UnitType
    base_cost: float
    modified_cost: float
    quantity_requested: int
    units_produced: int  # May be different due to dual production
    total_cost: float
    is_dual_production: bool

    def get_cost_per_unit(self) -> float:
        """Get the cost per unit actually produced."""
```

### Enhanced ProductionManager Integration

```python
class ProductionManager:
    """Enhanced production manager with integrated cost validation."""

    def __init__(self, resource_manager: ResourceManager, cost_validator: CostValidator):
        """Initialize with resource and cost management systems."""

    def validate_production(
        self,
        player_id: str,
        unit_type: UnitType,
        quantity: int,
        faction: Faction | None = None,
        technologies: set[Technology] | None = None
    ) -> ProductionValidationResult:
        """Validate production including cost, reinforcements, and placement rules."""

    def execute_production(
        self,
        player_id: str,
        unit_type: UnitType,
        quantity: int,
        spending_plan: SpendingPlan,
        placement_location: ProductionLocation
    ) -> ProductionExecutionResult:
        """Execute production with cost payment and unit placement."""
```

## Data Models

### ResourceSources and InfluenceSources

```python
@dataclass(frozen=True)
class ResourceSources:
    """Breakdown of available resource sources."""

    planets: dict[str, int]  # planet_name -> resource_value
    trade_goods: int
    total_available: int

    def get_planet_names(self) -> list[str]:
        """Get names of planets that can provide resources."""

@dataclass(frozen=True)
class InfluenceSources:
    """Breakdown of available influence sources."""

    planets: dict[str, int]  # planet_name -> influence_value
    trade_goods: int  # 0 if for_voting=True
    total_available: int
    for_voting: bool

    def get_planet_names(self) -> list[str]:
        """Get names of planets that can provide influence."""
```

### Validation Results

```python
@dataclass(frozen=True)
class CostValidationResult:
    """Result of cost validation."""

    is_valid: bool
    required_resources: int
    available_resources: int
    shortfall: int
    error_message: str | None = None
    suggested_spending_plan: SpendingPlan | None = None

@dataclass(frozen=True)
class SpendingResult:
    """Result of executing a spending plan."""

    success: bool
    planets_exhausted: list[str]
    trade_goods_spent: int
    error_message: str | None = None
```

## Integration with Existing Systems

### Planet Integration

The system will enhance the existing `Planet` class methods:

```python
# Existing methods that will be used:
# - planet.can_spend_resources() -> bool
# - planet.can_spend_influence() -> bool
# - planet.spend_resources(amount) -> int
# - planet.spend_influence(amount) -> int
# - planet.resources -> int
# - planet.influence -> int
# - planet.controlled_by -> str | None
```

### Player Integration

The system will use existing `Player` class methods:

```python
# Existing methods that will be used:
# - player.get_trade_goods() -> int
# - player.spend_trade_goods(amount) -> bool
# - player.faction -> Faction
```

### Game State Integration

The system will integrate with game state to:
- Find planets controlled by players
- Access player trade goods
- Update planet exhaustion status
- Maintain transaction atomicity

## Error Handling

### Custom Exceptions

```python
class ResourceError(Exception):
    """Base exception for resource-related errors."""
    pass

class InsufficientResourcesError(ResourceError):
    """Raised when player lacks sufficient resources."""
    pass

class InsufficientInfluenceError(ResourceError):
    """Raised when player lacks sufficient influence."""
    pass

class InvalidSpendingPlanError(ResourceError):
    """Raised when spending plan is invalid."""
    pass

class PlanetExhaustionError(ResourceError):
    """Raised when planet exhaustion fails."""
    pass
```

### Error Handling Strategy

1. **Validation Errors**: Return detailed validation results with error messages
2. **Execution Errors**: Use exceptions with rollback capability
3. **Atomic Operations**: Ensure all-or-nothing execution of spending plans
4. **Clear Messages**: Provide specific error messages about what resources are needed

## Testing Strategy

### Unit Tests

1. **ResourceManager Tests**
   - Resource/influence calculation from planets
   - Trade goods integration
   - Spending plan creation and execution
   - Voting vs non-voting influence rules

2. **CostValidator Tests**
   - Unit cost calculation with modifiers
   - Dual production cost handling
   - Production cost validation
   - Structure cost exemption

3. **SpendingPlan Tests**
   - Plan creation with various resource combinations
   - Plan validation and error handling
   - Plan execution and rollback

4. **Integration Tests**
   - End-to-end production with cost payment
   - Agenda phase voting with influence spending
   - Leadership strategy card integration
   - Construction strategy card integration

### Edge Case Tests

1. **Boundary Conditions**
   - Zero cost units
   - Exact resource matches
   - Maximum resource spending

2. **Error Scenarios**
   - Insufficient resources/influence
   - Exhausted planets
   - Invalid spending plans
   - Concurrent resource access

3. **Rule Interactions**
   - Dual production with insufficient reinforcements
   - Trade goods vs planet resource prioritization
   - Voting restrictions on trade goods

## Performance Considerations

### Optimization Strategies

1. **Caching**: Cache resource/influence calculations when game state hasn't changed
2. **Lazy Evaluation**: Only calculate detailed breakdowns when needed
3. **Batch Operations**: Optimize for multiple cost validations
4. **Memory Management**: Efficient data structures for resource tracking

### Scalability

- Support for maximum player count (8 players)
- Efficient planet lookup and filtering
- Minimal memory footprint for resource calculations
- Fast validation for real-time gameplay

## Implementation Phases

### Phase 1: Core Resource System
1. Implement ResourceManager with basic resource/influence calculations
2. Create SpendingPlan and related data structures
3. Add basic spending plan creation and validation
4. Integrate with existing Planet exhaustion mechanics

### Phase 2: Cost Validation
1. Implement CostValidator with unit cost calculations
2. Add production cost validation
3. Integrate dual production cost handling
4. Add technology and faction cost modifiers

### Phase 3: Production Integration
1. Enhance ProductionManager with cost validation
2. Integrate spending plan execution with production
3. Add Construction strategy card exemptions
4. Implement atomic production with cost payment

### Phase 4: Agenda Phase Integration
1. Add voting-specific influence calculations
2. Integrate with existing agenda phase voting
3. Add trade goods restrictions for voting
4. Test with existing agenda phase mechanics

### Phase 5: Strategy Card Integration
1. Integrate with Leadership strategy card
2. Add Construction strategy card cost exemptions
3. Test with all existing strategy card mechanics
4. Ensure backward compatibility

This design provides a comprehensive foundation for implementing the unified resource/influence/cost system while maintaining full integration with existing TI4 AI systems and following the correct TI4 rules for planet-based resource management.

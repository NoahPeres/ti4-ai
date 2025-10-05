# Design Document - Rule 9: ANOMALIES

## Overview

This design document outlines the implementation of Rule 9: ANOMALIES for the TI4 AI system. The design builds upon the existing system architecture, extending the current `SystemTile`, `System`, and movement validation systems to support the four types of anomalies: asteroid fields, nebulae, supernovas, and gravity rifts.

The implementation will integrate with the existing movement rules engine and provide a foundation for combat system integration.

## Architecture

### Core Components

1. **AnomalyType Enum**: Defines the four anomaly types
2. **AnomalySystem Class**: Extends system functionality with anomaly properties
3. **AnomalyMovementRule Class**: Replaces the stub `AnomalyRule` with full implementation
4. **AnomalyCombatEffects Class**: Handles combat modifications in anomaly systems
5. **AnomalyManager Class**: Coordinates anomaly operations and validation

### Integration Points

- **SystemTile**: Already supports anomaly identification via `TileType.ANOMALY`
- **System**: Will be extended to track anomaly types and effects
- **MovementRuleEngine**: Will use enhanced `AnomalyMovementRule`
- **Combat System**: Will integrate with `AnomalyCombatEffects` (future)

## Components and Interfaces

### AnomalyType Enum

```python
class AnomalyType(Enum):
    """Types of anomalies as defined in Rule 9.2"""
    ASTEROID_FIELD = "asteroid_field"
    NEBULA = "nebula"
    SUPERNOVA = "supernova"
    GRAVITY_RIFT = "gravity_rift"
```

### AnomalySystem Class

Extends the existing `System` class with anomaly-specific functionality:

```python
class AnomalySystem(System):
    """System with anomaly properties and effects"""

    def __init__(self, system_id: str, anomaly_types: list[AnomalyType]):
        super().__init__(system_id)
        self.anomaly_types = anomaly_types

    def is_anomaly(self) -> bool
    def get_anomaly_types(self) -> list[AnomalyType]
    def has_anomaly_type(self, anomaly_type: AnomalyType) -> bool
    def add_anomaly_type(self, anomaly_type: AnomalyType) -> None
    def remove_anomaly_type(self, anomaly_type: AnomalyType) -> None
    def blocks_movement(self) -> bool
    def allows_movement_when_active(self) -> bool
    def modifies_move_value(self) -> bool
    def get_move_value_modifier(self) -> int
    def provides_combat_bonus(self) -> bool
    def get_combat_bonus(self) -> int
    def requires_destruction_roll(self) -> bool
```

### AnomalyMovementRule Class

Replaces the existing stub with full anomaly movement validation:

```python
class AnomalyMovementRule(MovementRule):
    """Comprehensive anomaly movement rule implementation"""

    def can_move(self, context: MovementContext) -> bool
    def can_move_into_system(self, system: System, is_active_system: bool) -> bool
    def can_move_through_system(self, system: System) -> bool
    def get_movement_range(self, unit: Unit, technologies: set[Technology]) -> int
    def apply_gravity_rift_effects(self, unit: Unit, path: list[System]) -> MovementResult
    def calculate_modified_move_value(self, unit: Unit, current_system: System) -> int
```

### AnomalyCombatEffects Class

Handles combat modifications in anomaly systems:

```python
class AnomalyCombatEffects:
    """Manages combat effects for anomaly systems"""

    def get_defender_bonus(self, system: System) -> int
    def applies_to_space_combat(self, system: System) -> bool
    def applies_to_ground_combat(self, system: System) -> bool
    def get_combat_modifiers(self, system: System, is_defender: bool) -> dict[str, int]
```

### AnomalyManager Class

Coordinates anomaly operations and provides high-level interface:

```python
class AnomalyManager:
    """Manages anomaly systems and effects"""

    def create_anomaly_system(self, system_id: str, anomaly_types: list[AnomalyType]) -> AnomalySystem
    def validate_movement_through_anomalies(self, path: list[System], active_system: System) -> ValidationResult
    def apply_gravity_rift_destruction(self, units: list[Unit], system: System) -> list[Unit]
    def get_anomaly_effects_summary(self, system: System) -> dict[str, Any]
```

## Data Models

### MovementResult

```python
@dataclass
class MovementResult:
    """Result of movement through anomaly systems"""
    allowed: bool
    modified_move_value: int
    destroyed_units: list[Unit]
    effects_applied: list[str]
    error_message: str | None = None
```

### ValidationResult

```python
@dataclass
class ValidationResult:
    """Result of anomaly movement validation"""
    valid: bool
    blocked_systems: list[System]
    required_active_systems: list[System]
    error_messages: list[str]
```

### AnomalyEffects

```python
@dataclass
class AnomalyEffects:
    """Summary of all anomaly effects for a system"""
    blocks_movement: bool
    requires_active_system: bool
    move_value_modifier: int
    combat_bonus: int
    destruction_risk: bool
    applicable_anomaly_types: list[AnomalyType]
```

## Error Handling

### Custom Exceptions

```python
class AnomalyMovementError(Exception):
    """Raised when movement is blocked by anomaly rules"""
    pass

class InvalidAnomalyTypeError(Exception):
    """Raised when an invalid anomaly type is specified"""
    pass

class GravityRiftDestructionError(Exception):
    """Raised when gravity rift destruction occurs"""
    pass
```

### Error Scenarios

1. **Movement into blocked anomaly**: Clear message indicating which anomaly type blocks movement
2. **Nebula movement without active system**: Specific error about nebula activation requirement
3. **Invalid anomaly type assignment**: Validation error for unsupported anomaly types
4. **Gravity rift destruction**: Detailed information about destroyed units

## Testing Strategy

### Unit Tests

1. **AnomalyType enum validation**
2. **AnomalySystem creation and property management**
3. **Movement rule validation for each anomaly type**
4. **Combat effect calculation**
5. **Gravity rift destruction mechanics**
6. **Multiple anomaly type stacking**
7. **Dynamic anomaly assignment**

### Integration Tests

1. **Movement validation with anomaly systems**
2. **Combat system integration with nebula bonuses**
3. **Galaxy setup with anomaly systems**
4. **End-to-end movement scenarios through multiple anomalies**

### Edge Cases

1. **Systems with multiple anomaly types**
2. **Anomaly systems containing planets**
3. **Gravity rift effects on multiple units**
4. **Nebula movement when system becomes active mid-turn**
5. **Anomaly removal and restoration**

## Implementation Phases

### Phase 1: Core Anomaly System
- Implement `AnomalyType` enum
- Create `AnomalySystem` class
- Basic anomaly identification and querying

### Phase 2: Movement Integration
- Implement `AnomalyMovementRule` class
- Replace stub in `MovementRuleEngine`
- Add movement validation for asteroid fields and supernovas

### Phase 3: Nebula Mechanics
- Implement nebula movement restrictions
- Add active system validation
- Implement move value modification in nebulae

### Phase 4: Gravity Rift Mechanics
- Implement gravity rift movement bonuses
- Add destruction roll mechanics
- Handle multiple gravity rift effects

### Phase 5: Combat Integration
- Implement `AnomalyCombatEffects` class
- Add nebula combat bonuses
- Integrate with existing combat system

### Phase 6: Advanced Features
- Dynamic anomaly assignment
- Multiple anomaly type stacking
- Comprehensive error handling and validation

## Dependencies

### Required Systems
- **System and SystemTile**: Core system representation (✅ Available)
- **Movement System**: Movement validation and rules (✅ Available)
- **Unit System**: Unit properties and management (✅ Available)
- **Dice System**: For gravity rift destruction rolls (✅ Available)

### Future Dependencies
- **Combat System**: For nebula combat bonuses (⚠️ Partial)
- **Active System Tracking**: For nebula movement validation (❌ Needs Implementation)
- **Ability System**: For dynamic anomaly creation (❌ Future)

## Performance Considerations

1. **Caching**: Cache anomaly effects calculations for frequently accessed systems
2. **Lazy Loading**: Only calculate complex effects when needed
3. **Batch Operations**: Process multiple units through gravity rifts efficiently
4. **Memory Management**: Avoid storing redundant anomaly state information

## Security and Validation

1. **Input Validation**: Validate all anomaly type assignments and system references
2. **State Consistency**: Ensure anomaly properties remain consistent with system state
3. **Immutability**: Protect critical anomaly properties from unauthorized modification
4. **Error Recovery**: Graceful handling of invalid anomaly configurations

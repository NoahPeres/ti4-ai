# Design Document: Rule 95 - TRANSPORT

## Overview

This design document outlines the implementation of Rule 95: TRANSPORT, which enables ships to carry fighters and ground forces during movement. The transport system integrates with existing movement, capacity, fleet management, and invasion systems to provide comprehensive unit transportation mechanics.

## Architecture

### Integration with Existing Systems

The transport implementation leverages several existing components:

- **Unit System** (`src/ti4/core/unit.py`): Already provides `get_capacity()` method and unit type identification
- **Ship System** (`src/ti4/core/ships.py`): Already provides ship identification and capacity validation
- **Movement System** (`src/ti4/core/movement.py`): Already has `TransportOperation` and `TransportValidator` classes (partial implementation)
- **Fleet System** (`src/ti4/core/fleet.py`): Already provides capacity calculation and validation
- **Invasion System** (`src/ti4/core/invasion.py`): Already handles ground force landing during invasion step

### New Components Required

1. **TransportManager** - Central coordinator for transport operations
2. **TransportState** - Tracks which units are being transported by which ships
3. **TransportRules** - Validates transport operations according to Rule 95
4. **Enhanced TransportValidator** - Extends existing partial implementation

## Components and Interfaces

### TransportManager

```python
class TransportManager:
    """Manages unit transport operations according to Rule 95."""

    def can_transport_units(self, ship: Unit, units: list[Unit]) -> bool:
        """Check if ship can transport the given units."""

    def load_units(self, ship: Unit, units: list[Unit], system: System) -> TransportState:
        """Load units onto a transport ship."""

    def unload_units(self, transport_state: TransportState, system: System) -> None:
        """Unload units from transport ship."""

    def get_transported_units(self, ship: Unit) -> list[Unit]:
        """Get all units currently transported by a ship."""

    def validate_pickup_location(self, system: System, player_id: str,
                                is_active_system: bool) -> bool:
        """Validate pickup restrictions based on command tokens."""
```

### TransportState

```python
@dataclass
class TransportState:
    """Represents the current transport state of units."""

    transport_ship: Unit
    transported_units: list[Unit]
    origin_system_id: str
    player_id: str

    def get_remaining_capacity(self) -> int:
        """Get remaining transport capacity."""

    def can_add_unit(self, unit: Unit) -> bool:
        """Check if unit can be added to transport."""
```

### TransportRules

```python
class TransportRules:
    """Validates transport operations according to Rule 95."""

    def can_pickup_from_system(self, system: System, player_id: str,
                              is_active_system: bool) -> bool:
        """Rule 95.3: Command token pickup restrictions."""

    def can_transport_unit_type(self, unit: Unit) -> bool:
        """Check if unit type can be transported."""

    def validate_capacity_limits(self, ship: Unit, units: list[Unit]) -> bool:
        """Rule 95.0: Capacity limit validation."""

    def validate_movement_constraints(self, transport_state: TransportState) -> bool:
        """Rule 95.2: Transport movement constraints."""
```

## Data Models

### Enhanced Unit Class

The existing `Unit` class already provides the necessary methods:
- `get_capacity()` - Returns transport capacity
- Unit type identification for transportable units
- Owner identification for command token validation

### Enhanced System Class

The existing `System` class likely provides:
- `has_command_token(player_id)` - Command token checking
- Unit placement and removal methods
- Space area unit management

### Transport Integration Points

1. **Movement Integration**: Extend existing `MovementOperation` to include transport information
2. **Fleet Integration**: Use existing `Fleet.get_total_capacity()` for system-wide capacity
3. **Invasion Integration**: Use existing invasion system for ground force landing

## Error Handling

### Transport Exceptions

```python
class TransportCapacityError(Exception):
    """Raised when transport capacity is exceeded."""

class TransportPickupError(Exception):
    """Raised when pickup restrictions are violated."""

class TransportMovementError(Exception):
    """Raised when transport movement constraints are violated."""
```

### Validation Layers

1. **Pre-transport Validation**: Check capacity and unit types before loading
2. **Movement Validation**: Ensure transported units move with ship
3. **Command Token Validation**: Enforce pickup restrictions
4. **Landing Validation**: Validate ground force landing during invasion

## Testing Strategy

### Unit Tests

1. **TransportManager Tests**
   - Basic transport capacity validation
   - Unit loading and unloading
   - Multi-ship transport coordination
   - Error handling for invalid operations

2. **TransportRules Tests**
   - Command token pickup restrictions (Rule 95.3)
   - Capacity limit enforcement (Rule 95.0)
   - Unit type validation
   - Movement constraint validation

3. **Integration Tests**
   - Transport during movement operations
   - Ground force landing during invasion
   - Multi-system transport scenarios
   - Fleet capacity integration

### Test Data

Leverage existing test infrastructure:
- Use existing `Unit` creation helpers
- Use existing `System` and `Galaxy` test fixtures
- Integrate with existing movement test scenarios

## Implementation Plan

### Phase 1: Core Transport Mechanics
1. Implement `TransportManager` class
2. Create `TransportState` data structure
3. Implement basic capacity validation
4. Add unit loading/unloading functionality

### Phase 2: Rule Validation
1. Implement `TransportRules` class
2. Add command token pickup restrictions (Rule 95.3)
3. Implement movement constraint validation (Rule 95.2)
4. Add comprehensive error handling

### Phase 3: System Integration
1. Enhance existing `TransportValidator` class
2. Integrate with movement system
3. Integrate with invasion system for ground force landing
4. Add fleet-level transport coordination

### Phase 4: Advanced Features
1. Multi-ship transport optimization
2. Transport state persistence
3. Advanced validation scenarios
4. Performance optimization

## Integration Points

### Existing Movement System

The existing `movement.py` already has partial transport implementation:
- `TransportOperation` dataclass
- `TransportValidator` class (basic implementation)
- `TransportExecutor` class (basic implementation)

**Enhancement Strategy**: Extend these existing classes rather than replacing them.

### Existing Fleet System

The existing `fleet.py` provides:
- `Fleet.get_total_capacity()` - System-wide capacity calculation
- `FleetCapacityValidator` - Capacity validation
- Unit capacity tracking

**Integration Strategy**: Use existing fleet capacity system for transport validation.

### Existing Invasion System

The existing `invasion.py` provides:
- Ground force landing during invasion step
- Unit placement on planets
- Combat integration

**Integration Strategy**: Extend invasion system to handle transported ground forces.

## Performance Considerations

1. **Capacity Caching**: Cache capacity calculations for frequently accessed ships
2. **Transport State Optimization**: Use efficient data structures for transport tracking
3. **Validation Optimization**: Minimize redundant validation checks
4. **Memory Management**: Efficient cleanup of transport states

## Security and Validation

1. **Input Validation**: Validate all transport parameters
2. **State Consistency**: Ensure transport state remains consistent
3. **Rule Enforcement**: Strict enforcement of LRR transport rules
4. **Error Recovery**: Graceful handling of invalid transport states

## Future Enhancements

1. **Technology Integration**: Support for transport-enhancing technologies
2. **Faction Abilities**: Support for faction-specific transport abilities
3. **Advanced Transport**: Multi-hop transport operations
4. **Transport Optimization**: AI-assisted transport planning

This design leverages the existing robust foundation while adding the specific transport mechanics required by Rule 95, ensuring seamless integration with the current codebase architecture.

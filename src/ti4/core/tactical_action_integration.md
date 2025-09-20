# Tactical Action System Integration

## Architecture Decision

We maintain TWO complementary tactical action systems:

### 1. Rule 89 Compliance System (`core/tactical_action.py`)
**Purpose**: Validate Rule 89 5-step sequence compliance
**When to Use**:
- Validating if a tactical action step is allowed
- Checking Rule 89.1 activation restrictions
- Verifying Rule 89.2 movement restrictions
- Detecting Rule 89.3 space combat requirements
- Validating Rule 89.4 invasion capabilities
- Checking Rule 89.5 production abilities

**Example Usage**:
```python
manager = TacticalActionManager()
can_activate = manager.can_activate_system(system, player, galaxy)
requires_combat = manager.requires_space_combat(system)
```

### 2. Advanced Movement System (`actions/tactical_action.py`)
**Purpose**: Execute complex movement with technology effects
**When to Use**:
- Planning multi-system movement with technology effects
- Validating movement range with Gravity Drive
- Complex transport capacity calculations
- Movement execution with validation

**Example Usage**:
```python
tactical_action = TacticalAction("system1", "player1")
movement_plan = MovementPlan()
validator = MovementValidator(galaxy)
```

## Integration Points

### Core Game Loop Usage
1. **Rule Validation**: Use `core/tactical_action.py` for rule compliance
2. **Movement Execution**: Use `actions/tactical_action.py` for complex movement
3. **Technology Effects**: Advanced system handles Gravity Drive, etc.

### Clear Separation of Concerns
- **Rule 89 System**: "Is this allowed by the rules?"
- **Advanced System**: "How do we execute this complex movement?"

## Future Integration
- Rule 89 system can call advanced system for movement execution
- Advanced system validates against Rule 89 restrictions
- Both systems remain independently testable and maintainable

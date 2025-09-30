# Technology Card Framework Documentation

## Overview

This directory contains comprehensive documentation for the Technology Card Framework, a type-safe, extensible system for implementing all TI4 technology cards.

## Documentation Structure

### 📚 Core Documentation

#### [Technology Card Framework Developer Guide](technology_card_framework_guide.md)
**Start here!** Comprehensive guide covering everything you need to implement technology cards.

- Framework architecture and design principles
- Step-by-step implementation process
- Base class selection guide
- Integration with existing systems
- Manual confirmation protocol
- Testing guidelines
- Best practices and troubleshooting

#### [Quick Reference](quick_reference.md)
**Essential cheat sheet** for developers implementing technology cards.

- Implementation checklist
- Common patterns and code snippets
- Enum quick reference
- Testing commands
- Common mistakes to avoid
- File locations and debug commands

### 🔧 Technical References

#### [API Reference](api_reference.md)
**Complete API documentation** for all classes, methods, and interfaces.

- Core protocols and base classes
- Registry and specification systems
- Integration classes and utilities
- Exception classes and error handling
- Comprehensive method signatures and examples

#### [Enum Systems Reference](enum_systems_reference.md)
**Comprehensive guide to the enum system** that powers the framework.

- All enum types and their usage
- Enum-first design philosophy
- Mapping functions and validation
- Adding new enum values
- Best practices for type safety

### 📖 Examples and Integration

#### [Dark Energy Tap Reference Implementation](dark_energy_tap_reference.md)
**Complete walkthrough** of the reference implementation showing all framework capabilities.

- Detailed implementation analysis
- Key patterns and design decisions
- System integration examples
- Testing patterns and best practices
- Usage as a template for new implementations

#### [Integration Points Guide](integration_points_guide.md)
**Detailed guide** to how the framework integrates with existing game systems.

- Abilities system integration
- Unit stats system integration
- Exploration and combat system integration
- Game state and registry integration
- Manual confirmation enforcement
- Integration testing patterns

## Getting Started

### For New Developers

1. **Start with**: [Technology Card Framework Developer Guide](technology_card_framework_guide.md)
2. **Reference**: [Quick Reference](quick_reference.md) for common patterns
3. **Study**: [Dark Energy Tap Reference Implementation](dark_energy_tap_reference.md)
4. **Use**: [API Reference](api_reference.md) for detailed method documentation

### For Experienced Developers

1. **Quick Start**: [Quick Reference](quick_reference.md)
2. **Integration**: [Integration Points Guide](integration_points_guide.md)
3. **Enums**: [Enum Systems Reference](enum_systems_reference.md)
4. **API Details**: [API Reference](api_reference.md)

## Key Concepts

### Enum-First Design
The framework uses comprehensive enums for all game concepts to provide:
- **Type Safety**: Compile-time checking of all game references
- **Discoverability**: IDE autocomplete for all game elements
- **Centralized Registry**: Single source of truth for all game data

### Manual Confirmation Protocol
**CRITICAL**: All technology specifications must be user-confirmed before implementation:
```python
# NEVER assume - ALWAYS ask user for confirmation:
# "I need to implement [Technology Name]. Before proceeding, I need confirmation:
# - What color is this technology?
# - What are its prerequisites?
# - What abilities does it have?"
```

### Base Class Hierarchy
```
BaseTechnologyCard
├── PassiveTechnologyCard      # For passive abilities
├── ExhaustibleTechnologyCard  # For ACTION abilities that exhaust
└── UnitUpgradeTechnologyCard  # For unit stat modifications
```

### System Integration
The framework integrates seamlessly with:
- **Abilities System**: Technology abilities participate in standard ability system
- **Unit Stats System**: Unit upgrades automatically modify unit statistics
- **Exploration System**: Technologies like Dark Energy Tap enhance exploration
- **Combat System**: Technologies can modify combat mechanics
- **Game State**: Technologies integrate with player state and game management

## Implementation Workflow

### 1. Planning Phase
- Identify technology requirements
- Determine base class needed
- Plan ability specifications
- **Get user confirmation for all specifications**

### 2. Implementation Phase
- Add technology to enum system
- Add specification to registry
- Create concrete implementation
- Implement abilities and integration

### 3. Testing Phase
- Write comprehensive unit tests
- Test system integration
- Test edge cases and error conditions
- Validate manual confirmation protocol

### 4. Documentation Phase
- Document confirmed specifications
- Update enum documentation if needed
- Add usage examples
- Update integration guides

## Framework Architecture

```
Technology Card Framework
├── Core Protocols (interfaces all technologies must implement)
├── Base Classes (common functionality for different technology types)
├── Specification System (enum-based data definitions)
├── Registry System (management of technology instances)
├── Integration Layer (connections to existing game systems)
├── Confirmation System (manual confirmation protocol enforcement)
└── Concrete Implementations (actual technology cards)
```

## File Organization

```
src/ti4/core/technology_cards/
├── __init__.py                 # Public API
├── protocols.py                # Core interfaces
├── specifications.py           # Enum-based specifications
├── registry.py                 # Technology management
├── confirmation.py             # Manual confirmation protocol
├── exceptions.py               # Framework exceptions
├── abilities_integration.py    # Abilities system integration
├── unit_stats_integration.py   # Unit stats integration
├── base/                       # Base implementations
│   ├── technology_card.py      # Abstract base
│   ├── exhaustible_tech.py     # Exhaustible technologies
│   ├── passive_tech.py         # Passive technologies
│   └── unit_upgrade_tech.py    # Unit upgrades
└── concrete/                   # Concrete implementations
    ├── dark_energy_tap.py      # Reference implementation
    └── gravity_drive.py        # Refactored implementation
```

## Testing Strategy

### Test Categories
1. **Unit Tests**: Test individual technology implementations
2. **Integration Tests**: Test framework integration with game systems
3. **Protocol Tests**: Test protocol compliance and validation
4. **Confirmation Tests**: Test manual confirmation enforcement

### Test Commands
```bash
# Run all technology tests
uv run pytest tests/test_technology_* -v

# Run specific technology tests
uv run pytest tests/test_dark_energy_tap.py -v

# Run with coverage
uv run pytest tests/test_technology_* --cov=src/ti4/core/technology_cards -v

# Type checking
uv run mypy src/ti4/core/technology_cards/

# Linting
uv run ruff check src/ti4/core/technology_cards/
```

## Current Implementations

### Confirmed Technologies
- **Dark Energy Tap**: Blue, no prerequisites, Prophecy of Kings
  - Frontier exploration ability
  - Retreat enhancement ability
  - Reference implementation demonstrating all framework capabilities

- **Gravity Drive**: Blue, 1 Blue prerequisite, Base game
  - Movement enhancement ability
  - Refactored to use new framework

### Implementation Status
- ✅ Framework architecture complete
- ✅ Enum system implemented
- ✅ Base classes implemented
- ✅ Registry system implemented
- ✅ Manual confirmation protocol enforced
- ✅ Dark Energy Tap reference implementation
- ✅ Gravity Drive refactored implementation
- ✅ System integration complete
- ✅ Comprehensive documentation

## Best Practices

### Implementation
1. **Always get user confirmation** before implementing any technology
2. **Use enum types** for all game concepts
3. **Follow the reference implementation** (Dark Energy Tap) as a template
4. **Write tests first** using TDD approach
5. **Document confirmed specifications** clearly in code

### Code Quality
1. **Type hints**: Use proper type hints for all methods
2. **Docstrings**: Document all public methods and classes
3. **Error handling**: Handle edge cases and invalid inputs
4. **Validation**: Validate inputs and state transitions
5. **Testing**: Comprehensive test coverage including edge cases

### Framework Usage
1. **Protocol compliance**: Ensure all implementations follow protocols
2. **System integration**: Test integration with all relevant game systems
3. **Enum consistency**: Use enums consistently throughout
4. **Confirmation enforcement**: Never bypass manual confirmation protocol

## Contributing

### Adding New Technologies
1. Read the [Developer Guide](technology_card_framework_guide.md)
2. Get user confirmation for all specifications
3. Follow the implementation workflow
4. Use Dark Energy Tap as a reference
5. Write comprehensive tests
6. Update documentation as needed

### Extending the Framework
1. Understand the current architecture
2. Follow enum-first design principles
3. Maintain backward compatibility
4. Add comprehensive tests
5. Update all relevant documentation

## Troubleshooting

### Common Issues
- **TechnologySpecificationError**: Technology needs user confirmation
- **Missing enum values**: Add to appropriate enum in constants.py
- **Integration failures**: Check integration points documentation
- **Test failures**: Follow TDD practices and reference implementations

### Getting Help
1. Check the [Developer Guide](technology_card_framework_guide.md)
2. Review the [API Reference](api_reference.md)
3. Study the [Dark Energy Tap Reference](dark_energy_tap_reference.md)
4. Look at existing test files for patterns
5. When in doubt, ask for user confirmation

## Framework Benefits

### For Developers
- **Type Safety**: Enum-based system prevents runtime errors
- **Clear Patterns**: Consistent implementation patterns across all technologies
- **Comprehensive Testing**: Built-in testing patterns and utilities
- **Integration Support**: Seamless integration with existing systems
- **Documentation**: Extensive documentation and examples

### For the Codebase
- **Consistency**: All technology implementations follow the same patterns
- **Maintainability**: Clear separation of concerns and modular design
- **Extensibility**: Easy to add new technologies and extend functionality
- **Reliability**: Manual confirmation protocol ensures accuracy
- **Performance**: Efficient enum-based lookups and caching

The Technology Card Framework provides a robust, type-safe foundation for implementing all TI4 technology cards with confidence and consistency.

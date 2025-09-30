# Technology Card Framework Quick Reference

## Implementation Checklist

### 🚨 MANDATORY: Manual Confirmation Protocol
**NEVER implement without user confirmation!**

```python
# ALWAYS ask user first:
# "I need to implement [Technology Name]. Before proceeding, I need confirmation:
# - What color is this technology?
# - What are its prerequisites?
# - What abilities does it have?
# - Is it faction-specific?"
```

### ✅ Implementation Steps

1. **Add Technology Enum**
   ```python
   # In src/ti4/core/technology_cards/specifications.py
   class Technology(Enum):
       YOUR_NEW_TECH = "your_new_tech"
   ```

2. **Get User Confirmation** (MANDATORY)
   - Color, prerequisites, abilities, faction restriction

3. **Add Specification**
   ```python
   # In specifications.py
   self._specifications[Technology.YOUR_NEW_TECH] = TechnologySpecification(...)
   ```

4. **Create Implementation**
   ```python
   # In src/ti4/core/technology_cards/concrete/your_new_tech.py
   class YourNewTech(PassiveTechnologyCard):  # or ExhaustibleTechnologyCard
       # Implementation
   ```

5. **Write Tests**
   ```python
   # In tests/test_your_new_tech.py
   class TestYourNewTech:
       def test_basic_properties(self): ...
       def test_abilities(self): ...
   ```

## Base Class Selection

| Technology Type | Base Class | Use When |
|----------------|------------|----------|
| **Passive abilities** | `PassiveTechnologyCard` | No ACTION abilities that exhaust |
| **ACTION abilities** | `ExhaustibleTechnologyCard` | Has ACTION abilities that exhaust card |
| **Unit upgrades** | `UnitUpgradeTechnologyCard` | Modifies unit statistics |

## Common Patterns

### Basic Technology Structure
```python
class MyTech(PassiveTechnologyCard):
    def __init__(self):
        super().__init__(Technology.MY_TECH, "My Tech")

    @property
    def color(self) -> Optional[TechnologyColor]:
        return TechnologyColor.BLUE  # CONFIRMED by user

    @property
    def prerequisites(self) -> list[TechnologyColor]:
        return [TechnologyColor.BLUE]  # CONFIRMED by user

    @property
    def faction_restriction(self) -> Optional[Faction]:
        return None  # CONFIRMED by user

    def get_abilities(self) -> list[Ability]:
        return [self._create_my_ability()]
```

### Ability Creation
```python
def _create_my_ability(self) -> Ability:
    from ti4.core.technology_cards.abilities_integration import EnhancedAbility

    ability = EnhancedAbility(
        name="My Ability",
        timing=TimingWindow.ACTION,  # or AFTER, WHEN, etc.
        trigger="my_trigger",
        effect=AbilityEffect(
            type="my_effect_type",
            value=True,
        ),
        conditions=[AbilityCondition.HAS_SHIPS_IN_SYSTEM]  # if needed
    )
    ability.source = "My Tech"
    return ability
```

## Enum Quick Reference

### AbilityTrigger
```python
ACTION                    # ACTION: Do something
AFTER_TACTICAL_ACTION     # After you perform tactical action
WHEN_RETREAT_DECLARED     # When retreat is declared
START_OF_TURN            # At start of turn
# ... see full list in enum_systems_reference.md
```

### AbilityEffectType
```python
EXPLORE_FRONTIER_TOKEN           # Explore frontier token
MODIFY_UNIT_STATS               # Modify unit statistics
GAIN_TRADE_GOODS                # Gain trade goods
ALLOW_RETREAT_TO_EMPTY_ADJACENT # Enhanced retreat
# ... see full list in enum_systems_reference.md
```

### AbilityCondition
```python
HAS_SHIPS_IN_SYSTEM        # Must have ships in system
SYSTEM_CONTAINS_FRONTIER   # System must have frontier token
CONTROL_PLANET            # Must control a planet
# ... see full list in enum_systems_reference.md
```

## Testing Patterns

### Basic Test Structure
```python
class TestMyTech:
    def test_basic_properties(self):
        tech = MyTech()
        assert tech.technology_enum == Technology.MY_TECH
        assert tech.name == "My Tech"
        assert tech.color == TechnologyColor.BLUE
        assert tech.prerequisites == [TechnologyColor.BLUE]
        assert tech.faction_restriction is None

    def test_abilities(self):
        tech = MyTech()
        abilities = tech.get_abilities()
        assert len(abilities) == 1
        assert abilities[0].name == "My Ability"

    def test_system_integration(self):
        # Test integration with game systems
        pass
```

### Test Commands
```bash
# Run single test
uv run pytest tests/test_my_tech.py::TestMyTech::test_basic_properties -v

# Run all tests for technology
uv run pytest tests/test_my_tech.py -v

# Run with coverage
uv run pytest tests/test_my_tech.py --cov=src/ti4/core/technology_cards -v
```

## Registry Usage

### Register Technology
```python
registry = TechnologyCardRegistry()
registry.register_card(MyTech())
```

### Get Technology
```python
tech = registry.get_card(Technology.MY_TECH)
```

### With Confirmation
```python
tech = registry.get_card_with_confirmation(Technology.MY_TECH)
```

## Specification System

### Create Specification
```python
spec = TechnologySpecification(
    technology=Technology.MY_TECH,
    name="My Tech",
    color=TechnologyColor.BLUE,
    prerequisites=[TechnologyColor.BLUE],
    faction_restriction=None,
    expansion=Expansion.BASE,
    abilities=[
        AbilitySpecification(
            trigger=AbilityTrigger.ACTION,
            effect=AbilityEffectType.GAIN_TRADE_GOODS,
            conditions=[],
            mandatory=True,
            passive=False,
        )
    ]
)
```

### Query Specifications
```python
spec_registry = TechnologySpecificationRegistry()

# Get specific
spec = spec_registry.get_specification(Technology.MY_TECH)

# Filter by color
blue_specs = spec_registry.get_specifications_by_color(TechnologyColor.BLUE)

# Filter by expansion
pok_specs = spec_registry.get_specifications_by_expansion(Expansion.PROPHECY_OF_KINGS)
```

## Common Mistakes

### ❌ Don't Do This
```python
# Using strings instead of enums
tech_name = "my_tech"  # NO!
color = "blue"         # NO!

# Implementing without confirmation
class MyTech(PassiveTechnologyCard):
    @property
    def color(self):
        return TechnologyColor.BLUE  # Did you confirm this?

# Missing type hints
def get_abilities(self):  # NO! Missing return type
    return []

# Not using EnhancedAbility
ability = Ability(...)  # NO! Use EnhancedAbility
```

### ✅ Do This
```python
# Using enums
tech = Technology.MY_TECH
color = TechnologyColor.BLUE

# With confirmation documentation
class MyTech(PassiveTechnologyCard):
    """
    CONFIRMED SPECIFICATIONS - DO NOT MODIFY WITHOUT USER APPROVAL:
    - Color: Blue technology
    - Prerequisites: 1 Blue
    """
    @property
    def color(self) -> Optional[TechnologyColor]:
        return TechnologyColor.BLUE  # CONFIRMED by user

# Proper type hints
def get_abilities(self) -> list[Ability]:
    return []

# Using EnhancedAbility
ability = EnhancedAbility(...)
```

## File Locations

```text
src/ti4/core/technology_cards/
├── concrete/your_new_tech.py     # Your implementation
├── specifications.py             # Add specification here
└── __init__.py                   # Export if needed

tests/
├── test_your_new_tech.py         # Your tests
└── test_technology_integration.py # Integration tests

docs/
├── technology_card_framework_guide.md  # Main guide
├── dark_energy_tap_reference.md        # Reference example
└── api_reference.md                     # API docs
```

## Debug Commands

```bash
# Type checking
uv run mypy src/ti4/core/technology_cards/

# Linting
uv run ruff check src/ti4/core/technology_cards/

# Format code
uv run ruff format src/ti4/core/technology_cards/

# All checks
make check-all
```

## Reference Implementations

### Dark Energy Tap (Passive, Multiple Abilities)
- **File**: `src/ti4/core/technology_cards/concrete/dark_energy_tap.py`
- **Features**: Passive abilities, condition validation, system integration
- **Use as template for**: Technologies with passive abilities

### Gravity Drive (Passive, Movement)
- **File**: `src/ti4/core/technology_cards/concrete/gravity_drive.py`
- **Features**: Movement enhancement, refactored implementation
- **Use as template for**: Movement-related technologies

## Key Enums Summary

| Enum | Purpose | Examples |
|------|---------|----------|
| `Technology` | Technology identification | `DARK_ENERGY_TAP`, `GRAVITY_DRIVE` |
| `TechnologyColor` | Technology colors | `BLUE`, `GREEN`, `YELLOW`, `RED` |
| `Expansion` | Content source | `BASE`, `PROPHECY_OF_KINGS` |
| `AbilityTrigger` | When abilities trigger | `ACTION`, `AFTER_TACTICAL_ACTION` |
| `AbilityEffectType` | What abilities do | `EXPLORE_FRONTIER_TOKEN`, `GAIN_TRADE_GOODS` |
| `AbilityCondition` | Ability requirements | `HAS_SHIPS_IN_SYSTEM`, `CONTROL_PLANET` |
| `UnitStatModification` | Unit stat changes | `COMBAT_VALUE`, `MOVEMENT`, `CAPACITY` |
| `Faction` | Faction restrictions | `SOL`, `HACAN`, `XXCHA` |

## Emergency Contacts

- **Framework Documentation**: `docs/technology_card_framework_guide.md`
- **API Reference**: `docs/api_reference.md`
- **Integration Guide**: `docs/integration_points_guide.md`
- **Enum Reference**: `docs/enum_systems_reference.md`
- **Example Implementation**: `docs/dark_energy_tap_reference.md`

## Remember

1. **ALWAYS get user confirmation** before implementing
2. **Use enums** for all game concepts
3. **Write tests first** (TDD approach)
4. **Follow Dark Energy Tap** as reference
5. **Document confirmed specifications** in code
6. **Use proper type hints** everywhere
7. **Test integration points** thoroughly

---

**When in doubt, ask for confirmation rather than guessing!**

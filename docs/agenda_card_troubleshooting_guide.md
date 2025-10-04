# Agenda Card Framework Troubleshooting Guide

## Overview

This guide helps developers diagnose and resolve common issues when working with the Agenda Card Framework. It covers error messages, debugging techniques, and solutions to frequently encountered problems.

## Table of Contents

1. [Common Error Messages](#common-error-messages)
2. [Debugging Techniques](#debugging-techniques)
3. [Framework-Specific Issues](#framework-specific-issues)
4. [Integration Problems](#integration-problems)
5. [Performance Issues](#performance-issues)
6. [Testing Problems](#testing-problems)
7. [Quick Reference](#quick-reference)

## Common Error Messages

### AgendaCardValidationError

#### Error: "Agenda card name cannot be empty"

**Cause**: Attempting to create an agenda card with an empty or None name.

**Solution**:
```python
# ❌ Wrong
card = MyAgendaCard("")  # or None

# ✅ Correct
card = MyAgendaCard("My Agenda Card")
```

#### Error: "Invalid outcome 'X' for agenda card 'Y'"

**Cause**: Trying to resolve an agenda with an outcome not in `get_voting_outcomes()`.

**Solution**:
```python
class MyAgendaCard(LawCard):
    def get_voting_outcomes(self) -> list[str]:
        return ["For", "Against"]  # Must include all valid outcomes

    def resolve_outcome(self, outcome: str, vote_result, game_state):
        if outcome not in self.get_voting_outcomes():
            raise ValueError(f"Invalid outcome '{outcome}' for {self.name}")
        # Handle valid outcomes...
```

### AgendaCardRegistrationError

#### Error: "Agenda card 'X' is already registered"

**Cause**: Attempting to register the same agenda card name twice.

**Solution**:
```python
# Check if already registered before registering
registry = AgendaCardRegistry()
if not registry.is_registered("My Card"):
    registry.register_card(my_card)
```

#### Error: "Cannot register None as an agenda card"

**Cause**: Passing None to `register_card()`.

**Solution**:
```python
# ❌ Wrong
registry.register_card(None)

# ✅ Correct
card = MyAgendaCard("My Card")
registry.register_card(card)
```

### AgendaDeckEmptyError

#### Error: "Cannot draw from empty agenda deck with no discard pile"

**Cause**: Attempting to draw from an empty deck when discard pile is also empty.

**Solution**:
```python
# Check deck state before drawing
if deck.is_empty() and deck.discard_pile_empty():
    # Handle empty deck scenario
    print("No more agenda cards available")
else:
    card = deck.draw_top_card()
```

### LawConflictError

#### Error: "Law 'X' conflicts with active law 'Y'"

**Cause**: Attempting to enact a law that conflicts with an existing active law.

**Solution**:
```python
class MyLawCard(LawCard):
    def conflicts_with_law(self, other_law: ActiveLaw) -> bool:
        # Define conflict detection logic
        if other_law.agenda_card.name == "Conflicting Law":
            return True
        return False

    def get_conflicting_laws(self) -> list[str]:
        # Return list of law names this law conflicts with
        return ["Conflicting Law"]
```

## Debugging Techniques

### 1. Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Framework components will log debug information
card = MyAgendaCard("Test")
result = card.resolve_outcome("For", vote_result, game_state)
```

### 2. Inspect Card State

```python
def debug_agenda_card(card: BaseAgendaCard):
    """Debug helper to inspect agenda card state."""
    print(f"Card Name: {card.name}")
    print(f"Card Type: {card.get_agenda_type()}")
    print(f"Voting Outcomes: {card.get_voting_outcomes()}")

    if isinstance(card, LawCard):
        print(f"Law Effects: {card.get_law_effects()}")

    if isinstance(card, DirectiveCard):
        print(f"Should Discard on Reveal: {card.should_discard_on_reveal(game_state)}")
```

### 3. Validate Registry State

```python
def debug_registry(registry: AgendaCardRegistry):
    """Debug helper to inspect registry state."""
    print(f"Registered Cards: {len(registry)}")
    for name in registry.get_all_card_names():
        card = registry.get_card(name)
        print(f"  - {name}: {type(card).__name__}")
```

### 4. Check Law Manager State

```python
def debug_law_manager(law_manager: LawManager):
    """Debug helper to inspect law manager state."""
    active_laws = law_manager.get_active_laws()
    print(f"Active Laws: {len(active_laws)}")
    for law in active_laws:
        print(f"  - {law.agenda_card.name} (Round {law.enacted_round})")
        print(f"    Effect: {law.effect_description}")
        if law.elected_target:
            print(f"    Target: {law.elected_target}")
```

### 5. Trace Outcome Resolution

```python
def debug_outcome_resolution(card: BaseAgendaCard, outcome: str, vote_result, game_state):
    """Debug helper to trace outcome resolution."""
    print(f"Resolving {card.name} with outcome: {outcome}")
    print(f"Valid outcomes: {card.get_voting_outcomes()}")

    try:
        result = card.resolve_outcome(outcome, vote_result, game_state)
        print(f"Resolution successful: {result.success}")
        print(f"Description: {result.description}")
        if result.law_enacted:
            print("Law was enacted")
        if result.directive_executed:
            print("Directive was executed")
    except Exception as e:
        print(f"Resolution failed: {e}")
        raise
```

## Framework-Specific Issues

### Issue: Card Not Found in Registry

**Symptoms**: `get_card()` returns None for a card you expect to be registered.

**Diagnosis**:
```python
# Check if card is registered
registry = AgendaCardRegistry()
if "My Card" not in registry:
    print("Card not registered")

# Check all registered cards
print("Registered cards:", registry.get_all_card_names())
```

**Solutions**:
1. Ensure card is properly imported and registered
2. Check for typos in card name
3. Verify registration happens before lookup

### Issue: Law Not Persisting

**Symptoms**: Law effects not applying after enactment.

**Diagnosis**:
```python
# Check if law was actually enacted
active_laws = game_state.law_manager.get_active_laws()
law_names = [law.agenda_card.name for law in active_laws]
print(f"Active laws: {law_names}")

# Check if law applies to current context
context = GameContext(...)  # Create appropriate context
relevant_laws = game_state.law_manager.get_laws_affecting_context(context)
print(f"Laws affecting context: {[law.agenda_card.name for law in relevant_laws]}")
```

**Solutions**:
1. Verify `create_active_law()` is called correctly
2. Check `applies_to_context()` logic
3. Ensure law manager is properly integrated with game state

### Issue: Directive Effects Not Executing

**Symptoms**: Directive cards resolve but effects don't apply.

**Diagnosis**:
```python
# Check if directive execution is reported
result = card.resolve_outcome(outcome, vote_result, game_state)
if not result.directive_executed:
    print("Directive was not marked as executed")

# Check for exceptions in effect execution
try:
    card.execute_immediate_effect(outcome, vote_result, game_state)
except Exception as e:
    print(f"Effect execution failed: {e}")
```

**Solutions**:
1. Implement `execute_immediate_effect()` method
2. Ensure method is called during resolution
3. Check for exceptions in effect logic

### Issue: Planet Attachment Failing

**Symptoms**: Planet attachable cards not attaching to planets.

**Diagnosis**:
```python
# Check if planet can accept attachment
planet = game_state.get_planet(planet_name)
if not card.can_attach_to_planet(planet):
    print(f"Card cannot attach to planet {planet_name}")
    print(f"Planet type: {planet.planet_type}")
    print(f"Required type: {card.get_required_planet_type()}")

# Check attachment system
attachment_manager = game_state.planet_attachment_manager
attachments = attachment_manager.get_attachments_for_planet(planet_name)
print(f"Current attachments: {[att.name for att in attachments]}")
```

**Solutions**:
1. Implement `can_attach_to_planet()` correctly
2. Verify planet type matching
3. Check attachment manager integration

## Integration Problems

### Issue: Voting System Integration

**Symptoms**: Voting outcomes not recognized by agenda cards.

**Diagnosis**:
```python
# Check outcome validation
valid_outcomes = card.get_voting_outcomes()
if outcome not in valid_outcomes:
    print(f"Outcome '{outcome}' not in valid outcomes: {valid_outcomes}")

# Check vote result structure
print(f"Vote result type: {type(vote_result)}")
print(f"Vote result attributes: {dir(vote_result)}")
```

**Solutions**:
1. Ensure `get_voting_outcomes()` returns all valid outcomes
2. Verify vote result structure matches expectations
3. Check voting system integration points

### Issue: Agenda Phase Integration

**Symptoms**: Agenda cards not appearing in agenda phase.

**Diagnosis**:
```python
# Check deck state
deck = game_state.agenda_deck
print(f"Deck size: {len(deck)}")
print(f"Discard pile size: {len(deck.discard_pile)}")

# Check card revelation
try:
    card = deck.draw_top_card()
    print(f"Drew card: {card.name}")
except AgendaDeckEmptyError:
    print("Deck is empty")
```

**Solutions**:
1. Verify deck initialization with all cards
2. Check deck shuffling and drawing logic
3. Ensure proper integration with agenda phase

### Issue: Game State Persistence

**Symptoms**: Active laws not persisting across game saves/loads.

**Diagnosis**:
```python
# Check game state serialization
import json
try:
    state_dict = game_state.to_dict()
    json.dumps(state_dict)  # Test serialization
    print("Game state serialization successful")
except Exception as e:
    print(f"Serialization failed: {e}")

# Check law manager serialization
law_data = game_state.law_manager.to_dict()
print(f"Law manager data: {law_data}")
```

**Solutions**:
1. Implement proper serialization for `ActiveLaw`
2. Ensure law manager state is included in game state
3. Test save/load functionality

## Performance Issues

### Issue: Slow Agenda Card Resolution

**Symptoms**: Long delays when resolving agenda outcomes.

**Diagnosis**:
```python
import time

start_time = time.time()
result = card.resolve_outcome(outcome, vote_result, game_state)
end_time = time.time()

print(f"Resolution took {end_time - start_time:.3f} seconds")
```

**Solutions**:
1. Profile resolution methods to find bottlenecks
2. Optimize complex effect calculations
3. Cache frequently accessed data

### Issue: Memory Usage Growth

**Symptoms**: Memory usage increases over time with agenda cards.

**Diagnosis**:
```python
import tracemalloc

tracemalloc.start()
# Perform agenda operations
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 1024 / 1024:.1f} MB")
print(f"Peak memory usage: {peak / 1024 / 1024:.1f} MB")
```

**Solutions**:
1. Check for memory leaks in card implementations
2. Ensure proper cleanup of temporary objects
3. Review data structure choices

## Testing Problems

### Issue: Tests Failing Unexpectedly

**Symptoms**: Tests that previously passed now fail.

**Diagnosis**:
```python
# Run tests with verbose output
pytest tests/test_rule_07_agenda_cards.py -v -s

# Run specific test with debugging
pytest tests/test_rule_07_agenda_cards.py::TestMyCard::test_method -v -s --pdb
```

**Solutions**:
1. Check for changes in dependencies
2. Verify test data and mocks are still valid
3. Review recent code changes for breaking changes

### Issue: Mock Objects Not Working

**Symptoms**: Tests fail because mock objects don't behave as expected.

**Diagnosis**:
```python
# Check mock configuration
from unittest.mock import Mock

mock_game_state = Mock()
mock_vote_result = Mock()

# Verify mock attributes
print(f"Mock game state type: {type(mock_game_state)}")
print(f"Mock vote result attributes: {dir(mock_vote_result)}")
```

**Solutions**:
1. Configure mocks with proper attributes and return values
2. Use `spec` parameter to ensure mock matches real object interface
3. Verify mock calls with `assert_called_with()`

### Issue: Integration Tests Failing

**Symptoms**: Unit tests pass but integration tests fail.

**Diagnosis**:
```python
# Test individual components
registry = AgendaCardRegistry()
deck = AgendaDeck([])
law_manager = LawManager()

# Test component interactions
card = MyAgendaCard("Test")
registry.register_card(card)
deck.add_card(card)
```

**Solutions**:
1. Test each integration point separately
2. Verify component initialization order
3. Check for missing dependencies

## Quick Reference

### Essential Debug Commands

```python
# Check card registration
registry.is_registered("Card Name")

# Inspect card state
debug_agenda_card(card)

# Check active laws
law_manager.get_active_laws()

# Validate outcomes
card.get_voting_outcomes()

# Test resolution
card.resolve_outcome(outcome, vote_result, game_state)
```

### Common Fix Patterns

```python
# Fix empty name error
if not name or not name.strip():
    raise ValueError("Name cannot be empty")

# Fix invalid outcome error
if outcome not in self.get_voting_outcomes():
    raise ValueError(f"Invalid outcome: {outcome}")

# Fix registration error
if not registry.is_registered(card.name):
    registry.register_card(card)

# Fix law conflict
def conflicts_with_law(self, other_law):
    return other_law.agenda_card.name in self.get_conflicting_laws()
```

### Validation Checklist

Before deploying agenda card changes:

- [ ] All cards have unique names
- [ ] All voting outcomes are handled
- [ ] Law cards implement `create_active_law()`
- [ ] Directive cards implement `execute_immediate_effect()`
- [ ] Cards are registered with registry
- [ ] Tests cover all outcomes
- [ ] Integration tests pass
- [ ] Performance is acceptable
- [ ] Documentation is updated

### Emergency Fixes

If the agenda system is completely broken:

1. **Check registry initialization**:
   ```python
   registry = AgendaCardRegistry()
   print(f"Registry has {len(registry)} cards")
   ```

2. **Verify deck state**:
   ```python
   deck = game_state.agenda_deck
   if deck.is_empty():
       deck.reshuffle_if_needed()
   ```

3. **Reset law manager**:
   ```python
   game_state.law_manager.clear_all_laws()
   ```

4. **Reload card implementations**:
   ```python
   importlib.reload(agenda_cards_module)
   ```

This troubleshooting guide should help you diagnose and resolve most issues with the Agenda Card Framework. When in doubt, start with the debugging techniques and work through the common issues systematically.

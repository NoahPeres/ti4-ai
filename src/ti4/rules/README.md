# LRR Rule Coverage System

This module provides a comprehensive system for tracking test coverage of Living Rules Reference (LRR) rules in the TI4 framework.

## Overview

The LRR Rule Coverage system allows developers to:

1. **Mark tests as covering specific LRR rules** using the `@covers_lrr_rule` decorator
2. **Generate coverage reports** showing which rules are tested and which are not
3. **Validate rule implementations** to ensure comprehensive rule coverage
4. **Track rule-to-test mappings** for systematic rule validation

## Key Components

### LRRRuleCoverageManager

The main class that manages rule-to-test mappings and generates coverage reports.

```python
from ti4.rules.lrr_coverage import LRRRuleCoverageManager

manager = LRRRuleCoverageManager()

# Register a test as covering a rule
manager.register_rule_test("1.1", "test_abilities_basic", "Test basic ability resolution")

# Generate coverage report
report = manager.get_rule_coverage_report()
print(f"Coverage: {report.coverage_percentage:.1f}%")

# Validate specific rule
result = manager.validate_rule_implementation("1.1")
print(f"Rule 1.1: {result.message}")

# Search for rules
results = manager.search_rules("ability")
for result in results[:5]:
    print(f"{result.rule_id}: {result.rule_text[:50]}...")

# Get detailed coverage report
detailed_report = manager.get_detailed_coverage_report()
print(f"Rules with multiple tests: {len(detailed_report.rules_with_multiple_tests)}")
```

### @covers_lrr_rule Decorator

A decorator that automatically registers tests as covering specific LRR rules.

```python
from ti4.rules.lrr_coverage import covers_lrr_rule

@covers_lrr_rule("1.1", "Test basic ability resolution")
def test_abilities_basic():
    """Test that basic abilities can be resolved."""
    # Test implementation here
    pass

@covers_lrr_rule("1.2", "Test card ability precedence")
def test_card_precedence():
    """Test that card abilities take precedence over base rules."""
    # Test implementation here
    pass
```

### Rule Search and Lookup

Search for rules by keyword or get specific rules by ID.

```python
from ti4.rules.lrr_coverage import LRRRuleCoverageManager, RuleSearchQuery

manager = LRRRuleCoverageManager()

# Simple keyword search
results = manager.search_rules("combat")
for result in results:
    print(f"{result.rule_id}: {result.rule_text}")

# Get specific rule by ID
rule = manager.get_rule_by_id("1.1")
if rule:
    print(f"Rule {rule.rule_id}: {rule.rule_text}")

# Advanced search with query object
query = RuleSearchQuery(
    keyword="ability",
    max_results=10,
    case_sensitive=False
)
results = manager.search_rules_advanced(query)
```

### Enhanced Coverage Reports

Generate detailed coverage reports with statistics and analysis.

```python
# Get detailed coverage statistics
stats = manager.get_coverage_statistics()
print(f"Total rules: {stats.total_rules}")
print(f"Coverage: {stats.coverage_percentage:.1f}%")
print(f"Rules with multiple tests: {stats.rules_with_multiple_tests}")

# Get coverage gaps
gaps = manager.get_coverage_gaps()
print(f"Uncovered rules: {len(gaps)}")

# Get rules by coverage status
covered_rules = manager.get_rules_by_coverage_status(covered=True)
uncovered_rules = manager.get_rules_by_coverage_status(covered=False)

# Generate human-readable summary
summary = manager.generate_coverage_summary()
print(summary)
```

### Rule Validation Tools

Validate rule parsing accuracy and coverage calculations.

```python
from ti4.rules.lrr_coverage import RuleValidationTool

validator = RuleValidationTool(manager)

# Validate rule parsing
result = validator.validate_rule_parsing()
print(f"Rule parsing: {result.message}")

# Validate coverage calculation
result = validator.validate_coverage_calculation()
print(f"Coverage calculation: {result.message}")

# Run comprehensive validation
results = validator.run_comprehensive_validation()
for result in results:
    status = "✓" if result.is_valid else "✗"
    print(f"{status} {result.validation_type}: {result.message}")
```

### Data Models

- **RuleTestMapping**: Links a test function to an LRR rule
- **RuleCoverageReport**: Basic coverage statistics and mappings
- **DetailedCoverageReport**: Enhanced coverage report with detailed analysis
- **CoverageStatistics**: Detailed coverage statistics
- **RuleValidationResult**: Result of validating a specific rule implementation
- **RuleSearchResult**: Result of searching for rules
- **RuleSearchQuery**: Query parameters for advanced rule search
- **ValidationResult**: Result of validation checks

## Usage Examples

### Basic Usage

```python
from ti4.rules.lrr_coverage import covers_lrr_rule, get_global_coverage_manager

# Mark tests with the decorator
@covers_lrr_rule("8.4", "Units cannot move through systems containing other players' ships")
def test_movement_blocked_by_enemy_ships():
    # Test implementation
    pass

# Generate coverage report
manager = get_global_coverage_manager()
report = manager.get_rule_coverage_report()

print(f"Total rules: {report.total_rules}")
print(f"Covered rules: {report.covered_rules}")
print(f"Coverage: {report.coverage_percentage:.1f}%")
```

### Advanced Usage

```python
# Manual rule registration (for programmatic use)
manager = LRRRuleCoverageManager()
manager.register_rule_test("1.1", "test_abilities_basic", "Test basic ability resolution")

# Validate specific rules
result = manager.validate_rule_implementation("1.1")
if result.is_covered:
    print(f"✓ Rule {result.rule_id}: {result.message}")
else:
    print(f"✗ Rule {result.rule_id}: {result.message}")

# Get uncovered rules by category
uncovered_by_category = manager.get_uncovered_rules_by_category()
for category, rules in uncovered_by_category.items():
    print(f"Category {category}: {len(rules)} uncovered rules")

# Search for specific types of rules
combat_rules = manager.search_rules("combat")
movement_rules = manager.search_rules("movement")
ability_rules = manager.search_rules("ability")

# Generate detailed analysis
detailed_report = manager.get_detailed_coverage_report()
print(f"Coverage by category:")
for category, percentage in detailed_report.coverage_by_category.items():
    print(f"  Category {category}: {percentage:.1f}%")
```

## LRR Rule Parsing

The system automatically parses the Living Rules Reference document (`LRR/lrr.txt`) to extract all numbered rules. It supports:

- Numbered rules (e.g., "1.1", "2.3", "10.15")
- Hierarchical rule structure
- Fallback rules if LRR file is not available
- Robust error handling for parsing issues

## Integration with Testing

The system integrates seamlessly with existing test frameworks:

```python
import pytest
from ti4.rules.lrr_coverage import covers_lrr_rule

class TestAbilities:
    @covers_lrr_rule("1.1", "Basic ability resolution")
    def test_abilities_basic(self):
        """Test basic ability resolution."""
        # Your test code here
        assert True

    @covers_lrr_rule("1.2", "Card ability precedence")
    def test_card_precedence(self):
        """Test card ability precedence."""
        # Your test code here
        assert True
```

## Benefits

1. **Systematic Rule Coverage**: Ensures all LRR rules are properly tested
2. **Confidence in Component Addition**: New factions, cards, and abilities can be added with confidence that existing rules won't break
3. **Rule Validation**: Provides tools to validate that specific rules are properly implemented
4. **Coverage Tracking**: Tracks progress toward complete rule coverage
5. **Documentation**: Creates a living mapping between rules and their tests

## Future Enhancements

- **Automated Test Execution**: Run tests associated with specific rules
- **CI/CD Integration**: Automated coverage reporting in continuous integration
- **Rule Change Detection**: Detect when LRR rules change and identify affected tests
- **Coverage Regression Detection**: Alert when rule coverage decreases

## Files

- `lrr_coverage.py`: Main implementation
- `README.md`: This documentation
- `../../../tests/test_lrr_rule_coverage.py`: Unit tests
- `../../../tests/test_lrr_integration.py`: Integration tests
- `../../../examples/lrr_coverage_example.py`: Usage examples
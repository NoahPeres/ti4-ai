# Design Document

## Overview

This design addresses the critical issues identified in PR 33 code review by implementing systematic fixes across four key areas: hook configuration, documentation consistency, ability trigger system, and ability condition validation. The design prioritizes backward compatibility where possible while ensuring system reliability.

## Architecture

### Component Overview

The fixes span multiple system components:

1. **Kiro Hook System** - Configuration files that control automated workflows
2. **Documentation System** - Markdown files providing developer guidance
3. **Ability System** - Technology card abilities and their trigger mechanisms
4. **Validation System** - Condition checking and error handling

### Design Principles

- **Fail-Safe Design**: When validation cannot be performed, fail closed rather than allowing potentially invalid operations
- **Canonical References**: Use enum values consistently instead of hardcoded strings
- **Documentation Consistency**: Maintain single source of truth for file locations and procedures
- **Test-Production Alignment**: Ensure tests use the same mechanisms as production code

## Components and Interfaces

### Hook Configuration Component

**Purpose**: Restore proper file pattern matching for automated quality checks

**Interface**:
```json
{
  "patterns": ["**/*.py", "**/*.md", "**/*.toml"]
}
```

**Behavior**:
- Replaces empty patterns array with comprehensive file type coverage
- Ensures hook triggers for relevant development files
- Maintains existing hook functionality

### Documentation Consistency Component

**Purpose**: Align all documentation references to use consistent file paths

**Files Affected**:
- `docs/README.md` (lines ~180 and ~275-278)

**Changes**:
- Update troubleshooting sections to reference `specifications.py` instead of `constants.py`
- Ensure file organization and troubleshooting sections are aligned
- Maintain consistent terminology throughout

### Ability Trigger System Component

**Purpose**: Replace hardcoded trigger strings with canonical enum values

**Current State**:
```python
trigger="tactical_action_in_frontier_system"  # Hardcoded string
```

**Target State**:
```python
trigger=AbilityTrigger.AFTER_TACTICAL_ACTION.value  # Canonical enum
```

**Files Affected**:
- `src/ti4/core/technology_cards/concrete/dark_energy_tap.py`
- `tests/test_technology_card_framework_integration.py`

**Interface Changes**:
- Import `AbilityTrigger` from `ti4.core.constants`
- Replace hardcoded strings with enum values
- Update tests to use same trigger values as production

### Ability Condition Validation Component

**Purpose**: Implement fail-closed validation for all ability conditions

**Current State**:
```python
# Unhandled conditions fall through and return True
# Add more condition validations as needed
```

**Target State**:
```python
else:
    raise NotImplementedError(
        f"AbilityCondition {condition} lacks validation; fail closed instead of silently passing."
    )
```

**Behavior**:
- Explicit handling for each `AbilityCondition` enum value
- Fail-closed approach for unimplemented conditions
- Clear error messages indicating missing validation

## Data Models

### Hook Configuration Model
```json
{
  "name": "Subtask Quality Check",
  "trigger": "fileEdited",
  "patterns": ["**/*.py", "**/*.md", "**/*.toml"],
  "agent": "...",
  "prompt": "..."
}
```

### Ability Trigger Mapping
```python
CANONICAL_TRIGGERS = {
    "tactical_action_in_frontier_system": AbilityTrigger.AFTER_TACTICAL_ACTION.value,
    "when_retreat_declared": AbilityTrigger.WHEN_RETREAT_DECLARED.value,
    # Additional mappings as needed
}
```

### Validation Result Model
```python
@dataclass
class ValidationResult:
    is_valid: bool
    condition: AbilityCondition
    error_message: Optional[str] = None
```

## Error Handling

### Hook Configuration Errors
- **Empty Patterns**: Log warning and suggest restoration
- **Invalid Patterns**: Validate glob syntax before saving

### Documentation Inconsistencies
- **Automated Checks**: Add validation to ensure cross-references are consistent
- **Review Process**: Include documentation consistency in PR review checklist

### Ability Trigger Errors
- **Missing Enum Import**: Clear import error with suggested fix
- **Invalid Trigger**: Runtime error with available trigger options
- **Test Mismatch**: Test failure with clear message about trigger alignment

### Ability Condition Validation Errors
- **Unimplemented Condition**: `NotImplementedError` with specific condition name
- **Invalid Context**: Clear error message indicating required context keys
- **Validation Failure**: Detailed error explaining why condition was not met

## Testing Strategy

### Hook Configuration Testing
- **Unit Tests**: Verify pattern matching logic
- **Integration Tests**: Confirm hook triggers on file edits
- **Manual Testing**: Edit files and verify hook execution

### Documentation Testing
- **Automated Checks**: Script to verify cross-reference consistency
- **Link Validation**: Ensure all internal links resolve correctly
- **Review Checklist**: Manual verification of documentation updates

### Ability System Testing
- **Unit Tests**: Test individual ability trigger mechanisms
- **Integration Tests**: End-to-end ability activation scenarios
- **Regression Tests**: Ensure existing abilities continue to work
- **Performance Tests**: Verify trigger performance with enum values

### Validation System Testing
- **Comprehensive Coverage**: Test all `AbilityCondition` enum values
- **Error Handling**: Verify proper error messages for unimplemented conditions
- **Edge Cases**: Test boundary conditions and invalid inputs
- **Fail-Safe Behavior**: Confirm system fails closed for unknown conditions

## Implementation Phases

### Phase 1: Critical Fixes
1. Fix hook configuration (immediate impact on development workflow)
2. Fix ability trigger system (critical for gameplay functionality)

### Phase 2: Validation Improvements
1. Implement fail-closed ability condition validation
2. Add comprehensive error handling

### Phase 3: Documentation and Testing
1. Fix documentation inconsistencies
2. Add comprehensive test coverage
3. Update development guidelines

## Migration Strategy

### Backward Compatibility
- Existing ability definitions will continue to work during transition
- Deprecation warnings for hardcoded trigger strings
- Gradual migration of all ability definitions

### Rollback Plan
- Git-based rollback for each component
- Independent deployment of fixes allows selective rollback
- Comprehensive test suite ensures safe deployment

## Quality Assurance

### Code Quality Metrics
- All tests must pass after each fix
- No new linting errors introduced
- Type checking must pass with mypy
- Documentation must be consistent across all files

### Validation Criteria
- Hook triggers correctly for target file types
- All ability triggers use canonical enum values
- All ability conditions have explicit validation
- Documentation cross-references are consistent

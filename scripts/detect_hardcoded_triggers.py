#!/usr/bin/env python3
"""
Script to detect hardcoded trigger strings and other anti-patterns.

This script helps enforce the development guidelines by detecting:
1. Hardcoded trigger strings instead of enum usage
2. Missing AbilityTrigger imports
3. Fallthrough validation behavior
4. Other common anti-patterns
"""

import ast
import re
import sys
from pathlib import Path
from typing import Any


class TriggerPatternDetector(ast.NodeVisitor):
    """AST visitor to detect hardcoded trigger patterns."""

    def __init__(self, filename: str):
        self.filename = filename
        self.issues: list[dict[str, Any]] = []
        self.has_ability_trigger_import = False
        self.has_ability_condition_import = False

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Check for proper enum imports."""
        if node.module == "ti4.core.constants" and any(
            alias.name == "AbilityTrigger" for alias in node.names or []
        ):
            self.has_ability_trigger_import = True

        if node.module == "ti4.core.constants" and any(
            alias.name == "AbilityCondition" for alias in node.names or []
        ):
            self.has_ability_condition_import = True

        self.generic_visit(node)

    def visit_Str(self, node: ast.Str) -> None:
        """Check string literals for hardcoded triggers."""
        self._check_string_for_triggers(node.s, node.lineno)
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> None:
        """Check constant values for hardcoded triggers (Python 3.8+)."""
        if isinstance(node.value, str):
            self._check_string_for_triggers(node.value, node.lineno)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Check function definitions for validation anti-patterns."""
        if node.name == "validate_ability_conditions":
            self._check_validation_function(node)
        self.generic_visit(node)

    def _check_string_for_triggers(self, value: str, lineno: int) -> None:
        """Check if string value looks like a hardcoded trigger."""
        # Common hardcoded trigger patterns
        trigger_patterns = [
            r"tactical_action.*",
            r".*_in_.*_system",
            r"when_.*_declared",
            r"after_.*_action",
            r"before_.*_combat",
            r"start_of_.*",
            r"end_of_.*",
        ]

        for pattern in trigger_patterns:
            if re.match(pattern, value, re.IGNORECASE):
                self.issues.append(
                    {
                        "type": "hardcoded_trigger",
                        "line": lineno,
                        "message": f"Potential hardcoded trigger string: '{value}'. Use AbilityTrigger enum instead.",
                        "severity": "error",
                    }
                )
                break

    def _check_validation_function(self, node: ast.FunctionDef) -> None:
        """Check validation function for fail-closed behavior."""
        # Look for return True without explicit condition handling
        has_explicit_else = False
        has_not_implemented_error = False

        for child in ast.walk(node):
            if isinstance(child, ast.Raise):
                if (
                    isinstance(child.exc, ast.Call)
                    and isinstance(child.exc.func, ast.Name)
                    and child.exc.func.id == "NotImplementedError"
                ):
                    has_not_implemented_error = True

            # Check for else clause in if-elif chains
            if isinstance(child, ast.If) and child.orelse:
                if (
                    isinstance(child.orelse[0], ast.Raise)
                    and isinstance(child.orelse[0].exc, ast.Call)
                    and isinstance(child.orelse[0].exc.func, ast.Name)
                    and child.orelse[0].exc.func.id == "NotImplementedError"
                ):
                    has_explicit_else = True

        if not has_not_implemented_error or not has_explicit_else:
            self.issues.append(
                {
                    "type": "validation_fallthrough",
                    "line": node.lineno,
                    "message": "Validation function should implement fail-closed behavior with explicit NotImplementedError for unhandled conditions.",
                    "severity": "warning",
                }
            )


def check_file(filepath: Path) -> list[dict[str, Any]]:
    """Check a single Python file for issues."""
    # Skip constants.py as it contains enum definitions
    if filepath.name == "constants.py":
        return []

    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content, filename=str(filepath))
        detector = TriggerPatternDetector(str(filepath))
        detector.visit(tree)

        # Check for missing imports if triggers are used
        if any(issue["type"] == "hardcoded_trigger" for issue in detector.issues):
            if not detector.has_ability_trigger_import:
                detector.issues.append(
                    {
                        "type": "missing_import",
                        "line": 1,
                        "message": "Missing 'from ti4.core.constants import AbilityTrigger' import. Required when using ability triggers.",
                        "severity": "error",
                    }
                )

        return detector.issues

    except SyntaxError as e:
        return [
            {
                "type": "syntax_error",
                "line": e.lineno or 1,
                "message": f"Syntax error: {e.msg}",
                "severity": "error",
            }
        ]
    except Exception as e:
        return [
            {
                "type": "analysis_error",
                "line": 1,
                "message": f"Error analyzing file: {e}",
                "severity": "error",
            }
        ]


def check_directory(
    directory: Path, pattern: str = "*.py"
) -> dict[str, list[dict[str, Any]]]:
    """Check all Python files in a directory."""
    results = {}

    for filepath in directory.rglob(pattern):
        if filepath.is_file():
            issues = check_file(filepath)
            if issues:
                results[str(filepath)] = issues

    return results


def format_results(results: dict[str, list[dict[str, Any]]]) -> str:
    """Format results for display."""
    if not results:
        return "✅ No issues found!"

    output = []
    total_errors = 0
    total_warnings = 0

    for filepath, issues in results.items():
        output.append(f"\n📄 {filepath}")
        output.append("=" * (len(filepath) + 3))

        for issue in issues:
            severity_icon = "❌" if issue["severity"] == "error" else "⚠️"
            output.append(f"  {severity_icon} Line {issue['line']}: {issue['message']}")

            if issue["severity"] == "error":
                total_errors += 1
            else:
                total_warnings += 1

    output.append(f"\n📊 Summary: {total_errors} errors, {total_warnings} warnings")

    return "\n".join(output)


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
    else:
        target = Path("src")

    if not target.exists():
        print(f"❌ Target path '{target}' does not exist")
        sys.exit(1)

    print(f"🔍 Checking for hardcoded triggers and anti-patterns in {target}...")

    if target.is_file():
        issues = check_file(target)
        results = {str(target): issues} if issues else {}
    else:
        results = check_directory(target)

    output = format_results(results)
    print(output)

    # Exit with error code if issues found
    if results:
        error_count = sum(
            1
            for issues in results.values()
            for issue in issues
            if issue["severity"] == "error"
        )
        sys.exit(1 if error_count > 0 else 0)


if __name__ == "__main__":
    main()

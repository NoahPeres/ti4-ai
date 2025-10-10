#!/usr/bin/env python3
"""Script to update test files to use new ObjectiveCard system."""

import os
import re


def update_objective_constructor(content):
    """Update Objective() constructor calls to use ObjectiveTestHelpers."""

    # Pattern to match Objective constructor calls
    pattern = r'Objective\(\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*(\d+),\s*(True|False),\s*GamePhase\.(\w+)\s*\)'

    def replacement(match):
        obj_id, name, description, points, is_public, phase = match.groups()
        if is_public == "True":
            return f'ObjectiveTestHelpers.create_public_objective(\n            "{obj_id}", "{name}", GamePhase.{phase}, {points}\n        )'
        else:
            return f'ObjectiveTestHelpers.create_secret_objective(\n            "{obj_id}", "{name}", GamePhase.{phase}, {points}\n        )'

    return re.sub(pattern, replacement, content)


def update_imports(content):
    """Update imports to include ObjectiveTestHelpers."""
    if "from ti4.core.objective import Objective" in content:
        content = content.replace(
            "from ti4.core.objective import Objective",
            "from ti4.core.objective import ObjectiveCard\nfrom tests.test_rule_61_test_helpers import ObjectiveTestHelpers",
        )
    return content


def update_file(filepath):
    """Update a single test file."""
    print(f"Updating {filepath}...")

    with open(filepath) as f:
        content = f.read()

    # Update imports
    content = update_imports(content)

    # Update Objective constructor calls
    content = update_objective_constructor(content)

    with open(filepath, "w") as f:
        f.write(content)

    print(f"Updated {filepath}")


# Files to update
test_files = [
    "tests/test_rule_61_scoring_limits.py",
    "tests/test_rule_61_secret_objectives.py",
    "tests/test_rule_98_victory_points.py",
]

for filepath in test_files:
    if os.path.exists(filepath):
        update_file(filepath)
    else:
        print(f"File not found: {filepath}")

print("Done!")

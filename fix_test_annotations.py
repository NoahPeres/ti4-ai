#!/usr/bin/env python3
"""Script to automatically add -> None return type annotations to test functions."""

import re
from pathlib import Path


def fix_test_file(file_path):
    """Add -> None annotations to test functions in a file."""
    with open(file_path) as f:
        content = f.read()

    # Pattern to match test function definitions without return type annotations
    pattern = r"(\s+def test_[^(]+\([^)]*\))(\s*:)"

    def replace_func(match):
        func_def = match.group(1)
        colon = match.group(2)
        # Add -> None before the colon
        return func_def + " -> None" + colon

    # Apply the replacement
    new_content = re.sub(pattern, replace_func, content)

    # Also handle class method test functions
    pattern2 = r"(\s+def test_[^(]+\([^)]*self[^)]*\))(\s*:)"
    new_content = re.sub(pattern2, replace_func, new_content)

    if new_content != content:
        with open(file_path, "w") as f:
            f.write(new_content)
        return True
    return False


# Get all test files
test_files = list(Path("tests").glob("test_*.py"))

fixed_count = 0
for test_file in test_files:
    if fix_test_file(test_file):
        print(f"Fixed: {test_file}")
        fixed_count += 1

print(f"Fixed {fixed_count} files")

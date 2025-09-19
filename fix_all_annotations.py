#!/usr/bin/env python3
"""Script to automatically add return type annotations to functions."""

import re
from pathlib import Path


def fix_file(file_path):
    """Add return type annotations to functions in a file."""
    with open(file_path) as f:
        content = f.read()

    original_content = content

    # Pattern 1: Functions without any return type annotation
    # Matches: def function_name(...): but not def function_name(...) -> ...:
    pattern1 = r"(\s*def\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\))(\s*):(?!\s*->)"

    def replace_func(match):
        func_def = match.group(1)
        spaces = match.group(2)
        return func_def + " -> None" + spaces + ":"

    content = re.sub(pattern1, replace_func, content)

    # Pattern 2: Async functions without return type annotation
    pattern2 = r"(\s*async\s+def\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\))(\s*):(?!\s*->)"
    content = re.sub(pattern2, replace_func, content)

    if content != original_content:
        with open(file_path, "w") as f:
            f.write(content)
        return True
    return False


# Get all Python files in src/ and tests/
src_files = list(Path("src").rglob("*.py"))
test_files = list(Path("tests").rglob("*.py"))
all_files = src_files + test_files

fixed_count = 0
for py_file in all_files:
    if fix_file(py_file):
        print(f"Fixed: {py_file}")
        fixed_count += 1

print(f"Fixed {fixed_count} files")

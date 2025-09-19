#!/usr/bin/env python3
"""Script to fix missing parameter type annotations."""

import re
from pathlib import Path


def fix_file(file_path):
    """Fix missing parameter type annotations in a file."""
    with open(file_path) as f:
        content = f.read()

    original_content = content

    # Pattern for parameters without type annotations
    # Common patterns to fix:
    # is_legal_result=True -> is_legal_result: bool = True
    # count=0 -> count: int = 0
    # name="" -> name: str = ""
    # items=[] -> items: list = []
    # data={} -> data: dict = {}
    # value=None -> value: Any = None

    patterns = [
        (r"(\w+)=True\b", r"\1: bool = True"),
        (r"(\w+)=False\b", r"\1: bool = False"),
        (r"(\w+)=0\b", r"\1: int = 0"),
        (r"(\w+)=1\b", r"\1: int = 1"),
        (r"(\w+)=2\b", r"\1: int = 2"),
        (r"(\w+)=3\b", r"\1: int = 3"),
        (r"(\w+)=4\b", r"\1: int = 4"),
        (r"(\w+)=5\b", r"\1: int = 5"),
        (r'(\w+)=""', r'\1: str = ""'),
        (r"(\w+)=''", r"\1: str = ''"),
        (r"(\w+)=\[\]", r"\1: list = []"),
        (r"(\w+)=\{\}", r"\1: dict = {}"),
        (r"(\w+)=None\b", r"\1: Any = None"),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    # Add Any import if we used it and it's not already imported
    if (
        ": Any" in content
        and "from typing import" in content
        and "Any" not in content.split("from typing import")[1].split("\n")[0]
    ):
        # Find the typing import line and add Any
        content = re.sub(r"(from typing import [^)]*)", r"\1, Any", content)
    elif ": Any" in content and "from typing import" not in content:
        # Add the import at the top
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("from ") or line.startswith("import "):
                lines.insert(i, "from typing import Any")
                break
        content = "\n".join(lines)

    if content != original_content:
        with open(file_path, "w") as f:
            f.write(content)
        return True
    return False


# Get all Python files
src_files = list(Path("src").rglob("*.py"))
test_files = list(Path("tests").rglob("*.py"))
all_files = src_files + test_files

fixed_count = 0
for py_file in all_files:
    if fix_file(py_file):
        print(f"Fixed: {py_file}")
        fixed_count += 1

print(f"Fixed {fixed_count} files")

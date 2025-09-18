#!/usr/bin/env python3
"""Script to fix dataclass syntax errors."""

import os
import re
from pathlib import Path

def fix_file(file_path):
    """Fix dataclass syntax errors in a file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Fix @dataclass(frozen: bool = True) -> @dataclass(frozen=True)
    content = re.sub(r'@dataclass\(frozen: bool = True\)', '@dataclass(frozen=True)', content)
    
    # Fix other similar patterns if they exist
    content = re.sub(r'@dataclass\(frozen: bool = False\)', '@dataclass(frozen=False)', content)
    
    if content != original_content:
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    return False

# Get all Python files
src_files = list(Path('src').rglob('*.py'))
test_files = list(Path('tests').rglob('*.py'))
all_files = src_files + test_files

fixed_count = 0
for py_file in all_files:
    if fix_file(py_file):
        print(f"Fixed: {py_file}")
        fixed_count += 1

print(f"Fixed {fixed_count} files")

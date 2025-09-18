#!/usr/bin/env python3
"""Script to fix all type annotation syntax errors."""

import os
import re
from pathlib import Path

def fix_file(file_path):
    """Fix type annotation syntax errors in a file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Fix function call parameters with type annotations
    # Pattern: function(param: type = value) -> function(param=value)
    patterns = [
        # Common patterns in function calls
        (r'(\w+)\(([^)]*?)(\w+): int = (\d+)', r'\1(\2\3=\4'),
        (r'(\w+)\(([^)]*?)(\w+): str = ([^,)]+)', r'\1(\2\3=\4'),
        (r'(\w+)\(([^)]*?)(\w+): bool = (True|False)', r'\1(\2\3=\4'),
        (r'(\w+)\(([^)]*?)(\w+): dict = \{\}', r'\1(\2\3={}'),
        (r'(\w+)\(([^)]*?)(\w+): list = \[\]', r'\1(\2\3=[])'),
        
        # Fix StrategyCard constructor calls
        (r'StrategyCard\(id: int = (\d+)', r'StrategyCard(id=\1'),
        (r'initiative: int = (\d+)', r'initiative=\1'),
        (r'name="([^"]+)"', r'name="\1"'),
        
        # Fix other common patterns
        (r'(\w+): int = (\d+)', r'\1=\2'),
        (r'(\w+): str = "([^"]*)"', r'\1="\2"'),
        (r'(\w+): bool = (True|False)', r'\1=\2'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
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

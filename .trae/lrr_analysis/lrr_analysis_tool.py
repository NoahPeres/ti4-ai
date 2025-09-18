#!/usr/bin/env python3
"""
LRR Analysis Tool

This script helps with the manual analysis of LRR rules by:
1. Extracting rule categories and sub-rules from the LRR text file
2. Creating template markdown files for each rule category
3. Searching the codebase for potential test coverage

Usage:
    python lrr_analysis_tool.py --extract-rules
    python lrr_analysis_tool.py --create-templates
    python lrr_analysis_tool.py --search-tests RULE_NUMBER

Note: This tool does NOT automate the analysis itself, only assists with the manual process.
"""

import argparse
import os
import re
import sys
from pathlib import Path


def extract_rules(lrr_file_path):
    """Extract rule categories and sub-rules from the LRR text file."""
    print(f"Extracting rules from {lrr_file_path}")
    
    try:
        with open(lrr_file_path, 'r') as f:
            lrr_text = f.read()
    except FileNotFoundError:
        print(f"Error: LRR file not found at {lrr_file_path}")
        return None
    
    # Extract rule categories (numbered sections)
    rule_categories = []
    category_pattern = r'(\d+)\s+([A-Z][A-Z\s]+)'
    for match in re.finditer(category_pattern, lrr_text):
        rule_num = match.group(1)
        rule_name = match.group(2).strip()
        rule_categories.append((rule_num, rule_name))
    
    print(f"Found {len(rule_categories)} rule categories")
    return rule_categories


def create_template_files(rule_categories, output_dir):
    """Create template markdown files for each rule category."""
    print(f"Creating template files in {output_dir}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    for rule_num, rule_name in rule_categories:
        filename = f"rule_{rule_num:02d}_{rule_name.lower().replace(' ', '_')}.md"
        file_path = os.path.join(output_dir, filename)
        
        with open(file_path, 'w') as f:
            f.write(f"# LRR Rule Analysis: {rule_num} {rule_name}\n\n")
            f.write("## Overview\n")
            f.write(f"Analysis of rule category {rule_num}: {rule_name}\n\n")
            f.write("## Sub-Rules Analysis\n\n")
            f.write("### [Sub-rule number] [Sub-rule name]\n")
            f.write("**Rule Text:** [Exact text from LRR]\n\n")
            f.write("**Implementation Status:** Unstarted\n\n")
            f.write("**Priority:** [High | Medium | Low]\n\n")
            f.write("**Test Coverage:**\n- None identified\n\n")
            f.write("**Implementation Notes:**\n- Manual analysis required\n\n")
            f.write("**Action Items:**\n- Complete manual analysis\n- Identify relevant tests\n")
        
        print(f"Created {filename}")


def search_tests_for_rule(rule_number, tests_dir):
    """Search the tests directory for potential test coverage of a specific rule."""
    print(f"Searching for tests related to rule {rule_number}")
    
    # This is intentionally basic - it only helps identify potential matches
    # The actual analysis must be done manually as per requirements
    
    matches = []
    rule_pattern = re.compile(rf'{rule_number}[.\s]')
    
    for root, _, files in os.walk(tests_dir):
        for file in files:
            if file.endswith('.py') and file.startswith('test_'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        if rule_pattern.search(content):
                            matches.append(file_path)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    print(f"Found {len(matches)} potential test files")
    for match in matches:
        print(f"  - {match}")
    
    return matches


def main():
    parser = argparse.ArgumentParser(description="LRR Analysis Tool")
    parser.add_argument('--extract-rules', action='store_true', help='Extract rule categories from LRR')
    parser.add_argument('--create-templates', action='store_true', help='Create template files for rule categories')
    parser.add_argument('--search-tests', type=str, help='Search for tests related to a specific rule number')
    
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent.parent
    lrr_file_path = project_root / "LRR" / "lrr.txt"
    output_dir = project_root / ".trae" / "lrr_analysis"
    tests_dir = project_root / "tests"
    
    if args.extract_rules:
        rule_categories = extract_rules(lrr_file_path)
        if rule_categories:
            for rule_num, rule_name in rule_categories:
                print(f"{rule_num}: {rule_name}")
    
    if args.create_templates:
        rule_categories = extract_rules(lrr_file_path)
        if rule_categories:
            create_template_files(rule_categories, output_dir)
    
    if args.search_tests:
        search_tests_for_rule(args.search_tests, tests_dir)


if __name__ == "__main__":
    main()
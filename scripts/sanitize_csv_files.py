#!/usr/bin/env python3
"""
CSV Sanitization Script for TI4 Game Data

This script sanitizes CSV files by replacing commas within quoted text fields
with a unique separator (§) to enable proper CSV parsing. It handles different
CSV structures and preserves data integrity.

Usage: python scripts/sanitize_csv_files.py
"""

import csv
import re
from pathlib import Path
from typing import Any


def analyze_csv_structure(file_path: str) -> dict[str, Any]:
    """Analyze CSV structure to understand field types and content."""
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    lines = [line.strip() for line in lines if line.strip()]

    if not lines:
        return {"header": [], "field_analysis": {}, "total_fields": 0}

    # Parse header
    header = lines[0].split(",")

    # Analyze field content types
    field_analysis = {}
    for i, field_name in enumerate(header):
        field_analysis[field_name] = {
            "index": i,
            "has_long_text": False,
            "has_commas_in_quotes": False,
            "sample_values": [],
        }

    # Check entire content for quoted fields with commas
    quoted_fields_with_commas = re.findall(r'"([^"]*,[^"]*)"', content)
    has_problematic_quotes = len(quoted_fields_with_commas) > 0

    if has_problematic_quotes:
        # Mark the condition field as problematic (most likely field for game text)
        for field_name in ["Condition", "Effect", "Flavor Text", "Flavour"]:
            if field_name in field_analysis:
                field_analysis[field_name]["has_commas_in_quotes"] = True
                field_analysis[field_name]["sample_values"] = quoted_fields_with_commas[
                    :3
                ]
                break

    return {
        "header": header,
        "field_analysis": field_analysis,
        "total_fields": len(header),
        "has_quoted_commas": has_problematic_quotes,
        "quoted_samples": quoted_fields_with_commas[:5],
    }


def sanitize_csv_content(content: str, separator: str = "§") -> str:
    """
    Sanitize CSV content by replacing commas in quoted fields with separator.
    Also fixes missing trailing commas and other CSV formatting issues.

    Args:
        content: Raw CSV content
        separator: Character to replace commas with (default: §)

    Returns:
        Sanitized CSV content
    """
    lines = content.split("\n")
    sanitized_lines = []

    # Get expected field count from header
    header_line = lines[0] if lines else ""
    expected_fields = len(header_line.split(",")) if header_line else 0

    for i, line in enumerate(lines):
        if not line.strip():
            sanitized_lines.append(line)
            continue

        # Find all quoted fields and replace commas within them
        def replace_comma_in_quotes(match):
            quoted_content = match.group(1)
            return f'"{quoted_content.replace(",", separator)}"'

        # Replace commas within quoted fields
        sanitized_line = re.sub(r'"([^"]*)"', replace_comma_in_quotes, line)

        # Fix missing trailing commas if this is a data row (not header)
        if i > 0 and expected_fields > 0:
            current_fields = len(sanitized_line.split(","))
            if current_fields < expected_fields:
                # Add missing trailing commas
                missing_commas = expected_fields - current_fields
                sanitized_line += "," * missing_commas

        sanitized_lines.append(sanitized_line)

    return "\n".join(sanitized_lines)


def create_backup(file_path: str) -> str:
    """Create a backup of the original file."""
    backup_path = f"{file_path}.backup"
    with open(file_path, encoding="utf-8") as original:
        with open(backup_path, "w", encoding="utf-8") as backup:
            backup.write(original.read())
    return backup_path


def sanitize_csv_file(file_path: str, separator: str = "§") -> dict[str, Any]:
    """
    Sanitize a single CSV file.

    Args:
        file_path: Path to CSV file
        separator: Character to replace commas with

    Returns:
        Dictionary with sanitization results
    """
    print(f"\n=== Analyzing {file_path} ===")

    # Analyze structure
    analysis = analyze_csv_structure(file_path)
    print(f"Fields: {len(analysis['header'])}")

    # Show fields with problematic content
    problematic_fields = []
    for field_name, info in analysis["field_analysis"].items():
        if info["has_commas_in_quotes"]:
            problematic_fields.append(field_name)
            print(f"  - {field_name}: Contains commas in quoted text")
            if info["sample_values"]:
                sample = info["sample_values"][0]
                print(f"    Sample: {sample[:80]}...")

    if not problematic_fields and not analysis["has_quoted_commas"]:
        print("  No problematic fields found - file is already clean")
        return {
            "file_path": file_path,
            "backup_created": False,
            "changes_made": False,
            "problematic_fields": [],
        }

    # If we have quoted commas but no problematic fields from our known list,
    # populate problematic_fields from all fields that have commas in quotes
    if not problematic_fields and analysis["has_quoted_commas"]:
        for field_name, info in analysis["field_analysis"].items():
            if info["has_commas_in_quotes"]:
                problematic_fields.append(field_name)
                print(f"  - {field_name}: Contains commas in quoted text")
                if info["sample_values"]:
                    sample = info["sample_values"][0]
                    print(f"    Sample: {sample[:80]}...")

    # Create backup
    backup_path = create_backup(file_path)
    print(f"  Backup created: {backup_path}")

    # Read and sanitize content
    with open(file_path, encoding="utf-8") as f:
        original_content = f.read()

    sanitized_content = sanitize_csv_content(original_content, separator)

    # Write sanitized content
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(sanitized_content)

    print(f"  Sanitized: Replaced commas in quoted fields with '{separator}'")

    return {
        "file_path": file_path,
        "backup_created": True,
        "backup_path": backup_path,
        "changes_made": True,
        "problematic_fields": problematic_fields,
        "separator_used": separator,
    }


def verify_sanitization(file_path: str, separator: str = "§") -> bool:
    """Verify that sanitization worked correctly."""
    try:
        with open(file_path, encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Check if we can parse all rows
        header = rows[0]
        expected_fields = len(header)

        for i, row in enumerate(rows[1:], 2):
            if len(row) != expected_fields:
                print(
                    f"  WARNING: Row {i} has {len(row)} fields, expected {expected_fields}"
                )
                return False

        print(
            f"  Verification: Successfully parsed {len(rows)} rows with {expected_fields} fields each"
        )
        return True

    except Exception as e:
        print(f"  ERROR: Verification failed: {e}")
        return False


def main():
    """Main function to sanitize all CSV files."""
    print("TI4 CSV Sanitization Script")
    print("=" * 40)

    # Find all CSV files
    csv_files = list(Path("docs/component_details").glob("*.csv"))

    if not csv_files:
        print("No CSV files found in docs/component_details/")
        return

    print(f"Found {len(csv_files)} CSV files:")
    for file_path in csv_files:
        print(f"  - {file_path}")

    # Sanitize each file
    results = []
    separator = "§"  # Using section symbol as separator

    for file_path in csv_files:
        result = sanitize_csv_file(str(file_path), separator)
        results.append(result)

        # Verify sanitization
        if result["changes_made"]:
            verify_sanitization(str(file_path), separator)

    # Summary
    print("\n=== Summary ===")
    print(f"Files processed: {len(results)}")
    files_changed = sum(1 for r in results if r["changes_made"])
    print(f"Files modified: {files_changed}")

    if files_changed > 0:
        print(f"\nSeparator used: '{separator}'")
        print("Backups created for all modified files")
        print("\nTo parse these files in Python, use:")
        print("  import csv")
        print("  with open('file.csv', 'r') as f:")
        print("      reader = csv.reader(f)")
        print("      for row in reader:")
        print(f"          # Replace '{separator}' back to ',' in text fields if needed")
        print(
            f"          processed_row = [field.replace('{separator}', ',') for field in row]"
        )


if __name__ == "__main__":
    main()

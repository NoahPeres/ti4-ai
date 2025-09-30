#!/usr/bin/env python3
"""
Documentation consistency checker.

This script verifies that all documentation references are consistent across files,
including enum file locations, API references, and cross-references.
"""

import re
import sys
from pathlib import Path


def find_enum_references(file_path: Path) -> list[tuple[int, str]]:
    """Find all references to enum files in a documentation file."""
    references = []

    try:
        with open(file_path, encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                # Look for references to constants.py or specifications.py in enum contexts
                if re.search(r"enum.*constants\.py", line, re.IGNORECASE):
                    references.append((line_num, line.strip()))
                elif re.search(r"constants\.py.*enum", line, re.IGNORECASE):
                    references.append((line_num, line.strip()))
                elif re.search(r"Add.*enum.*constants\.py", line, re.IGNORECASE):
                    references.append((line_num, line.strip()))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return references


def find_file_references(file_path: Path) -> list[tuple[int, str, str]]:
    """Find all file references in documentation."""
    references = []

    try:
        with open(file_path, encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                # Look for file path references
                matches = re.finditer(r"([a-zA-Z_][a-zA-Z0-9_/]*\.py)", line)
                for match in matches:
                    file_ref = match.group(1)
                    references.append((line_num, line.strip(), file_ref))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return references


def find_broken_links(
    file_path: Path, project_root: Path
) -> list[tuple[int, str, str]]:
    """Find broken internal links in documentation."""
    broken_links = []

    try:
        with open(file_path, encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                # Look for markdown links to other files
                matches = re.finditer(r"\[([^\]]+)\]\(([^)]+\.md)\)", line)
                for match in matches:
                    match.group(1)
                    link_path = match.group(2)

                    # Resolve relative path
                    if not link_path.startswith("/"):
                        full_path = (file_path.parent / link_path).resolve()
                    else:
                        full_path = (project_root / link_path.lstrip("/")).resolve()

                    if not full_path.exists():
                        broken_links.append((line_num, line.strip(), link_path))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return broken_links


def check_cross_references(docs_files: list[Path]) -> dict[str, list[str]]:
    """Check for inconsistent cross-references between documentation files."""
    inconsistencies = {}

    # Common terms that should be referenced consistently
    terms_to_check = {
        "specifications.py": [],
        "constants.py": [],
        "Technology Card Framework": [],
        "Manual Confirmation Protocol": [],
        "enum-first": [],
        "type safety": [],
    }

    # Collect all references to these terms
    for file_path in docs_files:
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read().lower()
                for term in terms_to_check:
                    if term.lower() in content:
                        terms_to_check[term].append(str(file_path))
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    # Check for inconsistencies
    if terms_to_check["constants.py"] and terms_to_check["specifications.py"]:
        inconsistencies["enum_file_references"] = {
            "constants.py": terms_to_check["constants.py"],
            "specifications.py": terms_to_check["specifications.py"],
        }

    return inconsistencies


def check_documentation_consistency() -> bool:
    """Check all documentation files for consistency issues."""
    project_root = Path(__file__).parent.parent
    docs_dir = project_root / "docs"

    all_issues = []
    all_docs_files = []

    # Collect all documentation files
    for md_file in docs_dir.rglob("*.md"):
        all_docs_files.append(md_file)

    readme_path = project_root / "README.md"
    if readme_path.exists():
        all_docs_files.append(readme_path)

    print("🔍 Checking documentation consistency...")

    # Check 1: Enum file references
    print("\n1. Checking enum file references...")
    inconsistent_enum_refs = []

    for md_file in all_docs_files:
        references = find_enum_references(md_file)
        if references:
            for line_num, line in references:
                if "constants.py" in line and "enum" in line.lower():
                    inconsistent_enum_refs.append((md_file, line_num, line))

    if inconsistent_enum_refs:
        print("   ❌ Found inconsistent enum file references:")
        for file_path, line_num, line in inconsistent_enum_refs:
            print(f"     {file_path.relative_to(project_root)}:{line_num} - {line}")
        all_issues.extend(inconsistent_enum_refs)
    else:
        print("   ✅ All enum file references are consistent")

    # Check 2: Broken internal links
    print("\n2. Checking for broken internal links...")
    broken_links = []

    for md_file in all_docs_files:
        file_broken_links = find_broken_links(md_file, project_root)
        if file_broken_links:
            broken_links.extend(
                [
                    (md_file, line_num, line, link)
                    for line_num, line, link in file_broken_links
                ]
            )

    if broken_links:
        print("   ❌ Found broken internal links:")
        for file_path, line_num, _line, link in broken_links:
            print(
                f"     {file_path.relative_to(project_root)}:{line_num} - Broken link: {link}"
            )
        all_issues.extend(broken_links)
    else:
        print("   ✅ All internal links are valid")

    # Check 3: File reference consistency
    print("\n3. Checking file reference consistency...")
    file_refs = {}

    for md_file in all_docs_files:
        references = find_file_references(md_file)
        for line_num, line, file_ref in references:
            if file_ref not in file_refs:
                file_refs[file_ref] = []
            file_refs[file_ref].append((md_file, line_num, line))

    # Check if referenced files actually exist
    missing_files = []
    for file_ref, locations in file_refs.items():
        # Skip template/example files that are not meant to exist
        if any(
            template in file_ref
            for template in ["your_new_tech", "test_your_new_tech", "my_tech"]
        ):
            continue

        # Check common locations for the file
        possible_paths = [
            project_root / file_ref,
            project_root / "src" / file_ref,
            project_root / "src" / "ti4" / file_ref,
            project_root / "src" / "ti4" / "core" / file_ref,
            project_root / "src" / "ti4" / "actions" / file_ref,
            project_root / "src" / "ti4" / "commands" / file_ref,
            project_root / "src" / "ti4" / "performance" / file_ref,
            project_root / "src" / "ti4" / "testing" / file_ref,
            project_root / "src" / "ti4" / "core" / "technology_cards" / file_ref,
            project_root
            / "src"
            / "ti4"
            / "core"
            / "technology_cards"
            / "base"
            / file_ref,
            project_root
            / "src"
            / "ti4"
            / "core"
            / "technology_cards"
            / "concrete"
            / file_ref,
            project_root / "tests" / file_ref,
        ]

        if not any(path.exists() for path in possible_paths):
            missing_files.extend(
                [(loc[0], loc[1], loc[2], file_ref) for loc in locations]
            )

    if missing_files:
        print("   ❌ Found references to non-existent files:")
        for file_path, line_num, _line, missing_file in missing_files:
            print(
                f"     {file_path.relative_to(project_root)}:{line_num} - Missing: {missing_file}"
            )
        all_issues.extend(missing_files)
    else:
        print("   ✅ All file references point to existing files")

    # Check 4: Cross-reference consistency
    print("\n4. Checking cross-reference consistency...")
    cross_ref_issues = check_cross_references(all_docs_files)

    if cross_ref_issues:
        print("   ❌ Found cross-reference inconsistencies:")
        for issue_type, details in cross_ref_issues.items():
            print(f"     {issue_type}: {details}")
        all_issues.append(cross_ref_issues)
    else:
        print("   ✅ Cross-references are consistent")

    # Summary
    if all_issues:
        print("\n❌ DOCUMENTATION CONSISTENCY CHECK FAILED")
        print(f"Found {len(all_issues)} consistency issues that need to be addressed.")
        print("\nPlease fix these issues to maintain documentation quality.")
        return False
    else:
        print("\n✅ DOCUMENTATION CONSISTENCY CHECK PASSED")
        print("All documentation is consistent and well-maintained!")
        return True


if __name__ == "__main__":
    success = check_documentation_consistency()
    sys.exit(0 if success else 1)

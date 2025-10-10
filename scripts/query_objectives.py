#!/usr/bin/env python3
"""
Objective Cards Query Utility

Simple utility to query and analyze TI4 objective cards data.
"""

import csv
import sys
from collections import defaultdict
from pathlib import Path


def load_objectives() -> list[dict[str, str]]:
    """Load objective cards from CSV file."""
    objectives = []
    # Get script directory and construct path relative to repo root
    script_dir = Path(__file__).parent
    csv_path = (
        script_dir.parent / "docs" / "component_details" / "TI4_objective_cards.csv"
    )
    try:
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            required_columns = {
                "Name",
                "Condition",
                "Points",
                "Expansion",
                "Type",
                "Phase",
            }

            for row in reader:
                # Validate required columns on first row
                if not objectives and not required_columns.issubset(row.keys()):
                    missing = required_columns - set(row.keys())
                    raise ValueError(f"CSV missing required columns: {missing}")

                # Restore commas in condition text
                if "Condition" in row:
                    row["Condition"] = row["Condition"].replace("§", ",")
                objectives.append(row)
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_path}")
        print("Please ensure you're running this script from the repository root.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid CSV format - {e}")
        sys.exit(1)
    return objectives


def print_summary():
    """Print summary of objective cards."""
    objectives = load_objectives()

    print("TI4 Objective Cards Summary")
    print("=" * 40)
    print(f"Total objectives: {len(objectives)}")
    print()

    # Count by expansion and type
    counts = defaultdict(lambda: defaultdict(int))
    for obj in objectives:
        expansion = obj.get("Expansion", "Unknown")
        obj_type = obj.get("Type", "Unknown")
        counts[expansion][obj_type] += 1

    print("By Expansion and Type:")
    for expansion in sorted(counts.keys()):
        print(f"  {expansion}:")
        for obj_type in sorted(counts[expansion].keys()):
            print(f"    {obj_type}: {counts[expansion][obj_type]}")
        print()

    # Count by phase
    phase_counts = defaultdict(int)
    for obj in objectives:
        phase = obj.get("Phase", "Unknown")
        phase_counts[phase] += 1

    print("By Phase:")
    for phase in sorted(phase_counts.keys()):
        print(f"  {phase}: {phase_counts[phase]}")
    print()


def list_objectives_by_type(obj_type: str, expansion: str = None):
    """List objectives by type and optionally expansion."""
    objectives = load_objectives()

    filtered = [obj for obj in objectives if obj.get("Type") == obj_type]
    if expansion:
        filtered = [obj for obj in filtered if obj.get("Expansion") == expansion]

    print(f"{obj_type} Objectives" + (f" ({expansion})" if expansion else ""))
    print("=" * 50)

    for obj in filtered:
        name = obj.get("Name", "Unknown")
        condition = obj.get("Condition", "No condition")
        points = obj.get("Points", "?")
        exp = obj.get("Expansion", "Unknown")

        print(f"{name} ({points} VP) - {exp}")
        print(f"  {condition}")
        print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help"]:
        print("Usage:")
        print("  python scripts/query_objectives.py                    # Summary")
        print("  python scripts/query_objectives.py 'Stage I'          # All Stage I")
        print("  python scripts/query_objectives.py 'Stage I' Base     # Base Stage I")
        print("  python scripts/query_objectives.py Secret             # All Secret")
        sys.exit(0)
    elif len(sys.argv) == 1:
        print_summary()
    elif len(sys.argv) == 2:
        obj_type = sys.argv[1]
        list_objectives_by_type(obj_type)
    elif len(sys.argv) == 3:
        obj_type = sys.argv[1]
        expansion = sys.argv[2]
        list_objectives_by_type(obj_type, expansion)
    else:
        print("Usage:")
        print("  python scripts/query_objectives.py                    # Summary")
        print("  python scripts/query_objectives.py 'Stage I'          # All Stage I")
        print("  python scripts/query_objectives.py 'Stage I' Base     # Base Stage I")
        print("  python scripts/query_objectives.py Secret             # All Secret")

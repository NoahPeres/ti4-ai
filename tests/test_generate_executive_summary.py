"""
Tests for LRRAnalysisSummaryGenerator.

Testing library and framework: pytest
- We use pytest fixtures (tmp_path) and simple assertions.
- No new dependencies introduced; tests rely on standard library + pytest.

Focus:
- parse_rule_file: filename parsing, content extraction, defaults, robustness
- _categorize_rule: boundary classification
- load_all_rules: filtering and sorting
- generate_summary_stats: distribution and averages
- generate_executive_summary: key sections and computed metrics presence

Note: No <diff> tag provided; proceeding with comprehensive coverage of current behavior with a bias for action.
"""

from __future__ import annotations

import sys
import types
from pathlib import Path
import importlib
import importlib.util
import textwrap
import re

import pytest

# Helper: resolve module path dynamically by scanning repo for the defining class
def _resolve_module():
    """
    Try to import the module that defines LRRAnalysisSummaryGenerator.
    We search common locations; fall back to dynamic import by scanning files.
    """
    candidates = []

    # Search likely places relative to repo root
    roots = [
        Path("."), Path("src"), Path("scripts"), Path("tools"), Path("app"), Path("bin"),
    ]

    patterns = [
        "generate_executive_summary.py",
        "lrr_analysis_summary.py",
        "lrr_summary.py",
        "summary_generator.py",
    ]

    for root in roots:
        for pat in patterns:
            p = root / pat
            if p.is_file():
                candidates.append(p)

    # Fallback: brute-force scan for class declaration
    if not candidates:
        for p in Path(".").rglob("*.py"):
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if re.search(r"\bclass\s+LRRAnalysisSummaryGenerator\b", txt):
                candidates.append(p)

    if not candidates:
        pytest.skip("Could not locate implementation file for LRRAnalysisSummaryGenerator")

    # Prefer the shortest path (closest to root)
    candidates.sort(key=lambda p: (len(str(p).split("/")), len(str(p))))
    return candidates[0]

def _import_from_path(path: Path):
    spec = importlib.util.spec_from_file_location("lrr_summary_module", str(path))
    assert spec and spec.loader, f"Cannot load spec for {path}"
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)  # type: ignore[attr-defined]
    return mod

@pytest.fixture(scope="session")
def impl_module():
    path = _resolve_module()
    return _import_from_path(path)

@pytest.fixture
def Generator(impl_module):
    return impl_module.LRRAnalysisSummaryGenerator

@pytest.fixture
def RuleAnalysis(impl_module):
    return impl_module.RuleAnalysis

# ---------- parse_rule_file tests ----------

def test_parse_rule_file_happy_path(tmp_path: Path, Generator, RuleAnalysis):
    md = tmp_path / "06_adjacency_and_movement.md"
    md.write_text(textwrap.dedent("""
        # Rule 6 - Adjacency and Movement

        **Overall Priority**: High
        **Implementation Status**: In Progress - ~45% complete
        **Current Coverage**: 75% lines, 60% branches

        ### 6.1 Sub-rule One
        Text

        ### 6.2 Sub-rule Two
        Text

        ### High Priority
        - [ ] Implement adjacency graph checks
        - [x] Validate wormhole adjacency

        ### Medium Priority
        - [ ] Movement costs edge cases

        **Strengths**:
        - Clear core parsing
        - Good modularity

        **Areas Needing Attention**:
        - Edge cases not covered
        - Performance under large maps
    """).strip(), encoding="utf-8")

    g = Generator(str(tmp_path))
    rule = g.parse_rule_file(md)
    assert rule is not None
    assert rule.rule_number == 6
    assert rule.rule_name == "Adjacency And Movement"  # filename -> title-cased with spaces
    assert rule.priority == "High"
    assert rule.implementation_status.startswith("In Progress")
    assert rule.implementation_percentage == 45
    assert rule.category == "Core Mechanics"
    assert rule.sub_rules_count == 2
    assert "75% lines" in rule.test_coverage

    # Current implementation counts number of sections, not checklist items (behavioral test)
    assert rule.action_items_high == 1
    assert rule.action_items_medium == 1
    assert rule.action_items_low == 0

    assert rule.notable_strengths == ["Clear core parsing", "Good modularity"]
    assert rule.notable_issues == ["Edge cases not covered", "Performance under large maps"]

def test_parse_rule_file_invalid_filename_returns_none(tmp_path: Path, Generator):
    md = tmp_path / "invalid_filename.md"
    md.write_text("**Overall Priority**: High", encoding="utf-8")
    g = Generator(str(tmp_path))
    assert g.parse_rule_file(md) is None

def test_parse_rule_file_missing_fields_defaults(tmp_path: Path, Generator):
    md = tmp_path / "95_strategy.md"
    md.write_text(textwrap.dedent("""
        # Rule 95 - Strategy

        (no explicit priority/status/coverage)
    """).strip(), encoding="utf-8")

    g = Generator(str(tmp_path))
    rule = g.parse_rule_file(md)
    assert rule is not None
    assert rule.priority == "Unknown"
    assert rule.implementation_status == "Unknown"
    assert rule.implementation_percentage == 0
    assert rule.test_coverage == "Unknown"
    assert rule.category == "Strategy & Victory"

def test_parse_rule_file_non_file_path_safe_failure(tmp_path: Path, Generator):
    g = Generator(str(tmp_path))
    # Passing a directory path triggers exception internally and returns None
    assert g.parse_rule_file(tmp_path) is None

# ---------- _categorize_rule tests ----------

@pytest.mark.parametrize("num,expected", [
    (1, "Core Mechanics"),
    (10, "Core Mechanics"),
    (11, "Combat & Actions"),
    (30, "Combat & Actions"),
    (31, "Game Flow & Phases"),
    (50, "Game Flow & Phases"),
    (51, "Components & Resources"),
    (70, "Components & Resources"),
    (71, "Advanced Mechanics"),
    (90, "Advanced Mechanics"),
    (91, "Strategy & Victory"),
    (101, "Strategy & Victory"),
    (0, "Other"),
    (102, "Other"),
])
def test_categorize_boundaries(num, expected, Generator):
    g = Generator(".")
    assert g._categorize_rule(num) == expected

# ---------- load_all_rules tests ----------

def _write_rule(tmp_path: Path, fname: str, content: str):
    p = tmp_path / fname
    p.write_text(textwrap.dedent(content).strip(), encoding="utf-8")
    return p

def test_load_all_rules_filters_and_sorts(tmp_path: Path, Generator):
    _write_rule(tmp_path, "01_setup.md", """
        **Overall Priority**: Low
        **Implementation Status**: Done (100%)
        ### 1.1
        **Current Coverage**: 100%
    """)

    # Files that must be skipped by prefix rules
    for skip in ("README_something.md", "template_rule.md", "implementation_status.md", "lrr_rule_template.md"):
        _write_rule(tmp_path, skip, "**Overall Priority**: High")

    _write_rule(tmp_path, "11_combat.md", """
        **Overall Priority**: High
        **Implementation Status**: Started 30%
        ### 11.1
        **Current Coverage**: 40%
    """)

    g = Generator(str(tmp_path))
    g.load_all_rules()
    assert [r.rule_number for r in g.rules] == [1, 11]
    # Sorted ascending
    assert g.rules[0].rule_number < g.rules[1].rule_number

# ---------- generate_summary_stats tests ----------

def test_generate_summary_stats_counts_and_average(RuleAnalysis, Generator):
    g = Generator(".")
    g.rules = [
        RuleAnalysis(1, "Setup", "Low", "Done (100%)", 100, "Core Mechanics", 1, "100%", 0, 0, 0, [], []),
        RuleAnalysis(11, "Combat", "High", "In Progress (30%)", 30, "Combat & Actions", 2, "40%", 1, 0, 0, [], []),
        RuleAnalysis(31, "Initiative", "Medium", "Not Started (0%)", 0, "Game Flow & Phases", 0, "Unknown", 0, 1, 0, [], []),
    ]
    stats = g.generate_summary_stats()
    assert stats["total_rules"] == 3
    assert pytest.approx(stats["avg_implementation"], 0.01) == (100 + 30 + 0) / 3
    assert stats["implementation_dist"]["Done (100%)"] == 1
    assert stats["implementation_dist"]["In Progress (30%)"] == 1
    assert stats["implementation_dist"]["Not Started (0%)"] == 1
    assert stats["priority_dist"] == {"High": 1, "Low": 1, "Medium": 1}
    assert stats["category_dist"]["Core Mechanics"] == 1
    assert stats["category_dist"]["Combat & Actions"] == 1
    assert stats["category_dist"]["Game Flow & Phases"] == 1
    assert stats["high_priority_count"] == 1
    assert stats["medium_priority_count"] == 1
    assert stats["low_priority_count"] == 1

# ---------- generate_executive_summary tests ----------

def test_generate_executive_summary_includes_key_sections_and_metrics(tmp_path: Path, Generator):
    # Compose three rules
    (tmp_path / "06_adjacency.md").write_text(textwrap.dedent("""
        **Overall Priority**: High
        **Implementation Status**: In Progress (20%)
        **Current Coverage**: 10%

        ### 6.1
        ### 6.2

        ### High Priority
        - [ ] A
    """).strip(), encoding="utf-8")

    (tmp_path / "12_battle.md").write_text(textwrap.dedent("""
        **Overall Priority**: Medium
        **Implementation Status**: Started 50%
        **Current Coverage**: 30%

        ### 12.1

        ### Medium Priority
        - [ ] B
    """).strip(), encoding="utf-8")

    (tmp_path / "95_victory.md").write_text(textwrap.dedent("""
        **Overall Priority**: Low
        **Implementation Status**: Completed 100%
        **Current Coverage**: 90%

        ### 95.1

        ### Low Priority
        - [ ] C
    """).strip(), encoding="utf-8")

    g = Generator(str(tmp_path))
    summary = g.generate_executive_summary()

    # Headers present
    assert "# TI4 AI - LRR Implementation Executive Summary" in summary
    assert "## Executive Overview" in summary
    assert "## Implementation Status Distribution" in summary
    assert "## Priority Distribution" in summary
    assert "## Category Analysis" in summary
    assert "## Critical Implementation Gaps (High Priority, Low Implementation)" in summary
    assert "## Most Complete Implementations" in summary
    assert "## Detailed Rule Analysis" in summary
    assert "## Recommendations" in summary
    assert "## Progress Tracking" in summary

    # Totals and averages
    assert "Total Rules Analyzed: 3/101" in summary
    # Average should be (20 + 50 + 100)/3 = 56.666.. -> 56.7%
    assert "**Average Implementation**: 56.7%" in summary

    # Distributions present (by labels we used)
    assert "- **In Progress (20%)**:" in summary or "- **In Progress**:" in summary
    assert "- **Started 50%**:" in summary or "- **Started**:" in summary or "Started 50%" in summary
    assert "- **Completed 100%**:" in summary or "Completed 100%" in summary

    # Priority distribution lines
    assert "- **High Priority**:" in summary
    assert "- **Medium Priority**:" in summary
    assert "- **Low Priority**:" in summary

    # Category analysis for categories implied by rule numbers
    assert "- **Core Mechanics**:" in summary
    assert "- **Combat & Actions**:" in summary
    assert "- **Strategy & Victory**:" in summary

    # Critical gaps list should include the high priority low implementation rule 6
    assert re.search(r"\*\*Rule 6: .*Adjacency.*\*\s*-\s*20% implemented", summary)

    # Most complete implementations should include rule 95 at 100%
    assert re.search(r"\*\*Rule 95: .*Victory.*\*\s*-\s*100% implemented", summary)

    # Detailed table should include a row for each with computed action items count.
    # According to current implementation, action item counters count sections (1 each here)
    assert "| 6 | Adjacency" in summary
    assert "| 12 | Battle" in summary
    assert "| 95 | Victory" in summary

def test_generate_executive_summary_is_deterministic_given_same_inputs(tmp_path: Path, Generator):
    # Two identical runs should include identical computed metrics sections
    content = """
        **Overall Priority**: High
        **Implementation Status**: 40%
        ### 6.1
        **Current Coverage**: 10%
        ### High Priority
        - [ ] Task
    """
    (tmp_path / "06_rule.md").write_text(textwrap.dedent(content).strip(), encoding="utf-8")
    g = Generator(str(tmp_path))
    s1 = g.generate_executive_summary()
    s2 = g.generate_executive_summary()
    # Ignore timestamp; compare key stable fragments
    for frag in [
        "# TI4 AI - LRR Implementation Executive Summary",
        "Total Rules Analyzed: 1/101",
        "**Average Implementation**: 40.0%",
        "## Implementation Status Distribution",
        "## Detailed Rule Analysis",
    ]:
        assert frag in s1 and frag in s2
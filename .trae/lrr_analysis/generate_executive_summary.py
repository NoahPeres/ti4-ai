#!/usr/bin/env python3
"""
LRR Analysis Executive Summary Generator

This script analyzes all individual LRR rule analysis files and generates
a comprehensive executive summary with implementation status, priority metrics,
and progress tracking.
"""

import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class RuleAnalysis:
    """Data structure for individual rule analysis."""

    rule_number: int
    rule_name: str
    priority: str
    implementation_status: str
    implementation_percentage: int
    category: str
    sub_rules_count: int
    test_coverage: str
    action_items_high: int
    action_items_medium: int
    action_items_low: int
    notable_strengths: list[str]
    notable_issues: list[str]


class LRRAnalysisSummaryGenerator:
    """Generator for LRR analysis executive summaries."""

    def __init__(self, analysis_dir: str):
        self.analysis_dir = Path(analysis_dir)
        self.rules: list[RuleAnalysis] = []

    def parse_rule_file(self, file_path: Path) -> RuleAnalysis | None:
        """Parse an individual rule analysis file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Extract rule number and name from filename
            filename = file_path.stem
            rule_match = re.match(r"(\d+)_(.+)", filename)
            if not rule_match:
                return None

            rule_number = int(rule_match.group(1))
            rule_name = rule_match.group(2).replace("_", " ").title()

            # Extract priority assessment
            priority_match = re.search(r"\*\*Overall Priority\*\*:\s*(\w+)", content)
            priority = priority_match.group(1) if priority_match else "Unknown"

            # Extract implementation status
            status_match = re.search(
                r"\*\*Implementation Status\*\*:\s*([^*\n]+)", content
            )
            implementation_status = (
                status_match.group(1).strip() if status_match else "Unknown"
            )

            # Extract implementation percentage
            percentage_match = re.search(r"(\d+)%", implementation_status)
            implementation_percentage = (
                int(percentage_match.group(1)) if percentage_match else 0
            )

            # Count sub-rules
            sub_rules_count = len(re.findall(r"###\s+\d+\.\d+", content))

            # Extract test coverage
            test_coverage_match = re.search(
                r"\*\*Current Coverage\*\*:\s*([^\n]+)", content
            )
            test_coverage = (
                test_coverage_match.group(1).strip()
                if test_coverage_match
                else "Unknown"
            )

            # Count action items by priority
            action_items_high = len(
                re.findall(
                    r"### High Priority\s*\n((?:- \[[ x]\][^\n]*\n?)*)",
                    content,
                    re.MULTILINE,
                )
            )
            action_items_medium = len(
                re.findall(
                    r"### Medium Priority\s*\n((?:- \[[ x]\][^\n]*\n?)*)",
                    content,
                    re.MULTILINE,
                )
            )
            action_items_low = len(
                re.findall(
                    r"### Low Priority\s*\n((?:- \[[ x]\][^\n]*\n?)*)",
                    content,
                    re.MULTILINE,
                )
            )

            # Extract notable details
            strengths = []
            issues = []

            strengths_section = re.search(
                r"\*\*Strengths\*\*:\s*\n((?:- [^\n]*\n?)*)", content, re.MULTILINE
            )
            if strengths_section:
                strengths = [
                    line.strip("- ").strip()
                    for line in strengths_section.group(1).split("\n")
                    if line.strip().startswith("-")
                ]

            issues_section = re.search(
                r"\*\*Areas Needing Attention\*\*:\s*\n((?:- [^\n]*\n?)*)",
                content,
                re.MULTILINE,
            )
            if issues_section:
                issues = [
                    line.strip("- ").strip()
                    for line in issues_section.group(1).split("\n")
                    if line.strip().startswith("-")
                ]

            # Determine category based on rule number ranges
            category = self._categorize_rule(rule_number)

            return RuleAnalysis(
                rule_number=rule_number,
                rule_name=rule_name,
                priority=priority,
                implementation_status=implementation_status,
                implementation_percentage=implementation_percentage,
                category=category,
                sub_rules_count=sub_rules_count,
                test_coverage=test_coverage,
                action_items_high=action_items_high,
                action_items_medium=action_items_medium,
                action_items_low=action_items_low,
                notable_strengths=strengths,
                notable_issues=issues,
            )

        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None

    def _categorize_rule(self, rule_number: int) -> str:
        """Categorize rules by number ranges."""
        if 1 <= rule_number <= 10:
            return "Core Mechanics"
        elif 11 <= rule_number <= 30:
            return "Combat & Actions"
        elif 31 <= rule_number <= 50:
            return "Game Flow & Phases"
        elif 51 <= rule_number <= 70:
            return "Components & Resources"
        elif 71 <= rule_number <= 90:
            return "Advanced Mechanics"
        elif 91 <= rule_number <= 101:
            return "Strategy & Victory"
        else:
            return "Other"

    def load_all_rules(self):
        """Load and parse all rule analysis files."""
        self.rules = []

        for file_path in self.analysis_dir.glob("*.md"):
            if file_path.name.startswith(
                ("README", "template", "implementation_status", "lrr_rule")
            ):
                continue

            rule = self.parse_rule_file(file_path)
            if rule:
                self.rules.append(rule)

        # Sort by rule number
        self.rules.sort(key=lambda r: r.rule_number)

    def generate_summary_stats(self) -> dict:
        """Generate summary statistics."""
        total_rules = len(self.rules)

        # Implementation status distribution
        implementation_dist = defaultdict(int)
        priority_dist = defaultdict(int)
        category_dist = defaultdict(int)

        total_percentage = 0
        high_priority_count = 0
        medium_priority_count = 0
        low_priority_count = 0

        for rule in self.rules:
            implementation_dist[rule.implementation_status] += 1
            priority_dist[rule.priority] += 1
            category_dist[rule.category] += 1
            total_percentage += rule.implementation_percentage

            if rule.priority.lower() == "high":
                high_priority_count += 1
            elif rule.priority.lower() == "medium":
                medium_priority_count += 1
            elif rule.priority.lower() == "low":
                low_priority_count += 1

        avg_implementation = total_percentage / total_rules if total_rules > 0 else 0

        return {
            "total_rules": total_rules,
            "avg_implementation": avg_implementation,
            "implementation_dist": dict(implementation_dist),
            "priority_dist": dict(priority_dist),
            "category_dist": dict(category_dist),
            "high_priority_count": high_priority_count,
            "medium_priority_count": medium_priority_count,
            "low_priority_count": low_priority_count,
        }

    def generate_executive_summary(self) -> str:
        """Generate the complete executive summary."""
        self.load_all_rules()
        stats = self.generate_summary_stats()

        summary = f"""# TI4 AI - LRR Implementation Executive Summary

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Total Rules Analyzed**: {stats["total_rules"]}/101
**Overall Implementation Progress**: {stats["avg_implementation"]:.1f}%

## Executive Overview

This executive summary provides a comprehensive analysis of the Twilight Imperium 4th Edition Living Rules Reference (LRR) implementation status across all {stats["total_rules"]} analyzed rules. The analysis serves as the primary metric for tracking development progress and identifying critical implementation gaps.

### Key Metrics

- **Average Implementation**: {stats["avg_implementation"]:.1f}%
- **High Priority Rules**: {stats["high_priority_count"]} ({stats["high_priority_count"] / stats["total_rules"] * 100:.1f}%)
- **Medium Priority Rules**: {stats["medium_priority_count"]} ({stats["medium_priority_count"] / stats["total_rules"] * 100:.1f}%)
- **Low Priority Rules**: {stats["low_priority_count"]} ({stats["low_priority_count"] / stats["total_rules"] * 100:.1f}%)

## Implementation Status Distribution

"""

        # Add implementation status breakdown
        for status, count in sorted(stats["implementation_dist"].items()):
            percentage = count / stats["total_rules"] * 100
            summary += f"- **{status}**: {count} rules ({percentage:.1f}%)\n"

        summary += """
## Priority Distribution

"""

        # Add priority breakdown
        for priority, count in sorted(stats["priority_dist"].items()):
            percentage = count / stats["total_rules"] * 100
            summary += f"- **{priority} Priority**: {count} rules ({percentage:.1f}%)\n"

        summary += """
## Category Analysis

"""

        # Add category breakdown
        for category, count in sorted(stats["category_dist"].items()):
            percentage = count / stats["total_rules"] * 100
            summary += f"- **{category}**: {count} rules ({percentage:.1f}%)\n"

        # Add top priority rules
        high_priority_rules = [r for r in self.rules if r.priority.lower() == "high"]
        high_priority_rules.sort(key=lambda r: r.implementation_percentage)

        summary += """
## Critical Implementation Gaps (High Priority, Low Implementation)

"""

        for rule in high_priority_rules[:10]:  # Top 10 critical gaps
            summary += f"- **Rule {rule.rule_number}: {rule.rule_name}** - {rule.implementation_percentage}% implemented\n"

        # Add most complete implementations
        complete_rules = sorted(
            self.rules, key=lambda r: r.implementation_percentage, reverse=True
        )

        summary += """
## Most Complete Implementations

"""

        for rule in complete_rules[:10]:  # Top 10 most complete
            summary += f"- **Rule {rule.rule_number}: {rule.rule_name}** - {rule.implementation_percentage}% implemented\n"

        # Add detailed rule breakdown
        summary += """
## Detailed Rule Analysis

| Rule | Name | Priority | Implementation | Test Coverage | Action Items |
|------|------|----------|----------------|---------------|--------------|
"""

        for rule in self.rules:
            total_actions = (
                rule.action_items_high
                + rule.action_items_medium
                + rule.action_items_low
            )
            summary += f"| {rule.rule_number} | {rule.rule_name} | {rule.priority} | {rule.implementation_percentage}% | {rule.test_coverage} | {total_actions} |\n"

        summary += """
## Recommendations

### Immediate Actions (High Priority)
1. Focus on high-priority rules with <25% implementation
2. Implement core adjacency and movement mechanics (Rules 6, 58, 101)
3. Add comprehensive test coverage for combat systems
4. Complete strategy card implementations (Rules 83, 84, 91, 92, 99)

### Medium-Term Goals
1. Achieve 50%+ implementation across all high-priority rules
2. Complete faction-specific mechanics and abilities
3. Implement advanced game mechanics (exploration, relics, leaders)
4. Add UI components for all implemented mechanics

### Long-Term Objectives
1. Achieve 80%+ overall implementation coverage
2. Complete all edge cases and advanced scenarios
3. Optimize performance for complex game states
4. Add comprehensive documentation and debugging tools

## Progress Tracking

This summary should be regenerated regularly to track implementation progress. Key metrics to monitor:

- **Overall Implementation Percentage**: Target 80%+ for production readiness
- **High Priority Rule Coverage**: Target 90%+ completion for core gameplay
- **Test Coverage**: Target comprehensive test suites for all implemented rules
- **Action Item Completion**: Track and prioritize remaining implementation tasks

---

*This executive summary serves as the primary success metric for the TI4 AI implementation project. Regular updates will track progress toward full LRR compliance and production readiness.*
"""

        return summary


def main():
    """Main execution function."""
    analysis_dir = "/Users/noahperes/Developer/Code/kiro_test/ti4_ai/.trae/lrr_analysis"
    generator = LRRAnalysisSummaryGenerator(analysis_dir)

    summary = generator.generate_executive_summary()

    # Write to file
    output_path = Path(analysis_dir) / "executive_summary.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"Executive summary generated: {output_path}")
    print(f"Total rules analyzed: {len(generator.rules)}")
    print(
        f"Average implementation: {generator.generate_summary_stats()['avg_implementation']:.1f}%"
    )


if __name__ == "__main__":
    main()

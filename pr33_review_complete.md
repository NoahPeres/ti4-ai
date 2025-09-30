Latest review for PR #33 in NoahPeres/ti4-ai:

============================================================
GITHUB PR REVIEW SUMMARY
============================================================
Reviewer: coderabbitai[bot]
State: COMMENTED
Submitted: 2025-09-30T10:24:01Z
Review ID: 3283826952

REVIEW BODY:
----------------------------------------
**Actionable comments posted: 7**

<details>
<summary>♻️ Duplicate comments (2)</summary><blockquote>

<details>
<summary>docs/README.md (1)</summary><blockquote>

`296-296`: **Past issue already flagged: enum file path guidance.**

A previous review comment already identified the contradiction between the troubleshooting guidance and file organization section regarding where enum definitions live. The troubleshooting section has been corrected to reference `specifications.py` consistently.

</blockquote></details>
<details>
<summary>src/ti4/core/technology_cards/concrete/dark_energy_tap.py (1)</summary><blockquote>

`73-73`: **Past trigger issues resolved.**

The past review comments flagged hardcoded trigger strings, but the current implementation correctly uses `AbilityTrigger.AFTER_TACTICAL_ACTION.value` (line 73) and `AbilityTrigger.WHEN_RETREAT_DECLARED.value` (line 100). These changes align with the development guidelines.





Also applies to: 100-100

</blockquote></details>

</blockquote></details>

<details>
<summary>🧹 Nitpick comments (17)</summary><blockquote>

<details>
<summary>pyproject.toml (1)</summary><blockquote>

`86-91`: **Scope S101 ignores to tests.**

The inline note says asserts are allowed in tests, but the global ignore disables S101 everywhere—including production code—so Ruff/Bandit will silently miss asserts outside the test suite. Please move this suppression into the `tests` per-file block (e.g., add `"S101"` under `"tests/**/*"`), so production remains covered while tests get the intended exemption.



```diff
 ignore = [
     "E501",
     "B008",
     "C901",
-    "S101",
     "S105",
     "S106",
     "S311",
     "T201",
 ]

 [tool.ruff.lint.per-file-ignores]
-"tests/**/*" = ["B011"]
+"tests/**/*" = ["B011", "S101"]
```

</blockquote></details>
<details>
<summary>.kiro/specs/pr33-review-fixes/design.md (2)</summary><blockquote>

`66-67`: **Prefer passing Enum members over their `.value` for type‑safety**

Suggest using `AbilityTrigger.AFTER_TACTICAL_ACTION` (Enum) throughout domain logic and only converting to `.value` at serialization boundaries. This avoids accidental string drift and preserves exhaustiveness checks.

---

`33-36`: **Broaden example hook patterns**

Consider adding YAML/YML to the example patterns: `**/*.yaml`, `**/*.yml`. The repo includes YAML configs (e.g., pre-commit), so showing them here prevents future omissions.

</blockquote></details>
<details>
<summary>Makefile (2)</summary><blockquote>

`35-38`: **Run docs check inside the managed env for consistency**

Use `uv run python` (or just `uv run`) so dependencies and Python version match the project env.
```diff
-docs-check: ## Check documentation consistency
-	@echo "Checking documentation consistency..."
-	python scripts/check_documentation_consistency.py
+docs-check: ## Check documentation consistency
+	@echo "Checking documentation consistency..."
+	uv run python scripts/check_documentation_consistency.py
```

---

`39-42`: **Ditto for trigger check**

Align with other targets by executing under `uv run`.
```diff
-trigger-check: ## Check for hardcoded triggers and anti-patterns
-	@echo "Checking for hardcoded triggers and anti-patterns..."
-	python scripts/detect_hardcoded_triggers.py src
+trigger-check: ## Check for hardcoded triggers and anti-patterns
+	@echo "Checking for hardcoded triggers and anti-patterns..."
+	uv run python scripts/detect_hardcoded_triggers.py src
```

</blockquote></details>
<details>
<summary>templates/new_condition_validation_template.py (4)</summary><blockquote>

`116-120`: **Use logging instead of print for library code**

Swap `print(...)` for module‑scoped logger warnings to avoid noisy stdout during tests and allow users to configure log levels.
```diff
-    except (AttributeError, KeyError) as e:
-        # Handle missing game state components gracefully
-        print(f"Warning: Could not validate condition due to missing game state: {e}")
-        return False
+    except (AttributeError, KeyError) as e:
+        # Handle missing game state components gracefully
+        logger = logging.getLogger(__name__)
+        logger.warning("Could not validate condition due to missing game state: %s", e)
+        return False
```

---

`88-115`: **Avoid AttributeError paths; guard `system` and `units` access; don’t assume `unit.is_ship()` exists**

Check for `system is None`, default `units` to `[]`, and call `is_ship` only if present; this keeps the template compatible with varying Unit APIs.
```diff
-    system = game_state.get_system(system_id)
-
-    # Check for ships in the system
-    player_ships = [
-        unit for unit in system.units if unit.owner == player_id and unit.is_ship()
-    ]
-
-    return len(player_ships) > 0
+    system = game_state.get_system(system_id)
+    if system is None:
+        return False
+    units = getattr(system, "units", []) or []
+    def _is_ship(u: Any) -> bool:
+        fn = getattr(u, "is_ship", None)
+        try:
+            return bool(fn()) if callable(fn) else False
+        except Exception:
+            return False
+    player_ships = [u for u in units if getattr(u, "owner", None) == player_id and _is_ship(u)]
+    return bool(player_ships)
```

---

`142-145`: **Avoid `all([...])` for presence checks**

`all([...])` treats falsy values (like 0 or "") as missing. Use `is None` tests for required keys.
```diff
-    if not all([system_id, required_feature, game_state]):
-        return False
+    if system_id is None or required_feature is None or game_state is None:
+        return False
```

---

`150-156`: **Guard against dynamic attribute lookups**

Accessing `getattr(system, required_feature)` from a string is brittle. Prefer an explicit allow‑list (Enum → attribute map) or a dedicated query method on `system`. If keeping dynamic access, use a default to avoid double lookups.
```diff
-        return hasattr(system, required_feature) and getattr(system, required_feature)
+        return bool(getattr(system, str(required_feature), False))
```

</blockquote></details>
<details>
<summary>scripts/check_documentation_consistency.py (3)</summary><blockquote>

`21-28`: **Also detect (and prefer) enum references to `constants.py` explicitly**

Right now you only collect references involving `constants.py`. Add `specifications.py` matches so we can flag enum mentions pointing there as inconsistent.
```diff
-                # Look for references to constants.py or specifications.py in enum contexts
+                # Look for references to constants.py or specifications.py in enum contexts
                 if re.search(r"enum.*constants\.py", line, re.IGNORECASE):
                     references.append((line_num, line.strip()))
                 elif re.search(r"constants\.py.*enum", line, re.IGNORECASE):
                     references.append((line_num, line.strip()))
-                elif re.search(r"Add.*enum.*constants\.py", line, re.IGNORECASE):
+                elif re.search(r"Add.*enum.*constants\.py", line, re.IGNORECASE):
                     references.append((line_num, line.strip()))
+                elif re.search(r"enum.*specifications\.py", line, re.IGNORECASE):
+                    references.append((line_num, line.strip()))
+                elif re.search(r"specifications\.py.*enum", line, re.IGNORECASE):
+                    references.append((line_num, line.strip()))
```

---

`62-75`: **Support anchors in markdown links and remove unused group**

Anchor fragments like `doc.md#section` aren’t checked today. Also drop the unused `group(1)` access.
```diff
-                matches = re.finditer(r"\[([^\]]+)\]\(([^)]+\.md)\)", line)
+                matches = re.finditer(r"\[([^\]]+)\]\(([^)#]+\.md)(#[^)]+)?\)", line)
                 for match in matches:
-                    match.group(1)
-                    link_path = match.group(2)
+                    link_path = match.group(2)
```

---

`242-251`: **Don’t fail the run on high‑level cross‑reference presence**

The current “both mentioned” heuristic isn’t a strong inconsistency signal and can cause spurious failures. Consider logging a warning instead of appending to `all_issues`, or refine by context.
```diff
-    if cross_ref_issues:
-        print("   ❌ Found cross-reference inconsistencies:")
-        for issue_type, details in cross_ref_issues.items():
-            print(f"     {issue_type}: {details}")
-        all_issues.append(cross_ref_issues)
+    if cross_ref_issues:
+        print("   ⚠️ Cross-reference observations (review manually):")
+        for issue_type, details in cross_ref_issues.items():
+            print(f"     {issue_type}: {details}")
```

</blockquote></details>
<details>
<summary>.pre-commit-config.yaml (1)</summary><blockquote>

`59-64`: **Run docs checker inside project env**

Align with Makefile by invoking via `uv run` to ensure consistent interpreter and deps.
```diff
-      - id: docs-consistency-check
-        name: docs-consistency-check
-        entry: python scripts/check_documentation_consistency.py
+      - id: docs-consistency-check
+        name: docs-consistency-check
+        entry: uv run python scripts/check_documentation_consistency.py
         language: system
         pass_filenames: false
         files: ^(docs/.*\.md|README\.md)$
```

</blockquote></details>
<details>
<summary>src/ti4/core/technology_cards/concrete/dark_energy_tap.py (2)</summary><blockquote>

`45-51`: **Consider caching the registry instance.**

The `prerequisites()` property creates a new `TechnologySpecificationRegistry` instance on every access. Since the registry is immutable after initialization, consider caching it as a class-level or instance-level attribute to avoid repeated instantiation overhead.



Apply this pattern:

```python
def __init__(self) -> None:
    """Initialize Dark Energy Tap technology."""
    super().__init__(Technology.DARK_ENERGY_TAP, "Dark Energy Tap")
    self._registry = TechnologySpecificationRegistry()

@property
def prerequisites(self) -> list[TechnologyColor]:
    """Required prerequisite colors from specification."""
    spec = self._registry.get_specification(Technology.DARK_ENERGY_TAP)
    return list(spec.prerequisites) if spec else []
```

---

`67-68`: **Lazy imports are unnecessary here.**

The imports for `AbilityCondition` and `EnhancedAbility` within the helper methods (lines 67-68, 94-95) add no benefit since these methods are always called together during `get_abilities()`. Moving imports to the module top-level improves readability and aligns with PEP 8 guidance.



Move these imports to the top of the file with the other imports:

```diff
 from ti4.core.abilities import Ability, AbilityEffect, TimingWindow
-from ti4.core.constants import AbilityTrigger, Faction, Technology
+from ti4.core.constants import AbilityCondition, AbilityTrigger, Faction, Technology
 from ti4.core.technology import TechnologyColor
 from ti4.core.technology_cards.base.passive_tech import PassiveTechnologyCard
+from ti4.core.technology_cards.abilities_integration import EnhancedAbility
```


Also applies to: 94-95

</blockquote></details>
<details>
<summary>scripts/detect_hardcoded_triggers.py (2)</summary><blockquote>

`62-70`: **Trigger detection patterns may produce false positives.**

The regex patterns (lines 62-70) will flag any string matching patterns like `tactical_action.*` or `.*_in_.*_system`, including legitimate enum `.value` accesses, comments, or documentation strings. Consider adding context-aware filtering to reduce false positives, such as checking if the string appears in an assignment to a `trigger=` parameter or within specific AST node types.



Example enhancement to reduce false positives:

```python
def _check_string_for_triggers(self, value: str, lineno: int, parent_node: Optional[ast.AST] = None) -> None:
    """Check if string value looks like a hardcoded trigger."""
    # Skip if this is likely an enum .value access (e.g., part of a Call or Attribute chain)
    # or if it's in a comment/docstring context

    trigger_patterns = [
        r"tactical_action.*",
        r".*_in_.*_system",
        r"when_.*_declared",
        r"after_.*_action",
        r"before_.*_combat",
        r"start_of_.*",
        r"end_of_.*",
    ]

    # Only flag if pattern matches AND context suggests direct string usage
    for pattern in trigger_patterns:
        if re.match(pattern, value, re.IGNORECASE):
            # Add heuristic: check if preceded by AbilityTrigger. to reduce false positives
            # This is simplified; full implementation would track parent AST context
            self.issues.append(...)
```

---

`99-117`: **Fail-closed detection logic may miss valid patterns.**

The validation for fail-closed behavior (lines 99-117) requires both `has_not_implemented_error` anywhere in the function AND `has_explicit_else` in an if-elif-else chain. However, valid fail-closed implementations might raise `NotImplementedError` directly within the else block without being part of an if-elif chain (e.g., a single if-else or match statement). This could produce false warnings for correct code.



Consider relaxing the check to accept `NotImplementedError` in any else clause or at the function's end:

```diff
-        if not has_not_implemented_error or not has_explicit_else:
+        # Accept if NotImplementedError is raised anywhere in an else context or at end
+        if not has_not_implemented_error:
             self.issues.append(
                 {
                     "type": "validation_fallthrough",
                     "line": node.lineno,
-                    "message": "Validation function should implement fail-closed behavior with explicit NotImplementedError for unhandled conditions.",
+                    "message": "Validation function should implement fail-closed behavior by raising NotImplementedError for unhandled conditions.",
                     "severity": "warning",
                 }
             )
```

</blockquote></details>

</blockquote></details>

<details>
<summary>📜 Review details</summary>

**Configuration used**: CodeRabbit UI

**Review profile**: CHILL

**Plan**: Pro

<details>
<summary>📥 Commits</summary>

Reviewing files that changed from the base of the PR and between 5ffa43eac94432c5c5baf1593c6d741943842126 and 9679b31f607952a1144101322a1de3f3974000ea.

</details>

<details>
<summary>📒 Files selected for processing (22)</summary>

* `.kiro/hooks/subtask-quality-check.kiro.hook` (1 hunks)
* `.kiro/specs/pr33-review-fixes/design.md` (1 hunks)
* `.kiro/specs/pr33-review-fixes/requirements.md` (1 hunks)
* `.kiro/specs/pr33-review-fixes/tasks.md` (1 hunks)
* `.pre-commit-config.yaml` (1 hunks)
* `Makefile` (3 hunks)
* `docs/README.md` (1 hunks)
* `docs/api_reference.md` (1 hunks)
* `docs/development_guidelines.md` (1 hunks)
* `docs/quick_reference.md` (1 hunks)
* `docs/technology_card_framework_guide.md` (1 hunks)
* `docs/validation_requirements.md` (1 hunks)
* `pyproject.toml` (1 hunks)
* `scripts/check_documentation_consistency.py` (1 hunks)
* `scripts/detect_hardcoded_triggers.py` (1 hunks)
* `src/ti4/core/technology_cards/abilities_integration.py` (1 hunks)
* `src/ti4/core/technology_cards/concrete/dark_energy_tap.py` (1 hunks)
* `templates/new_ability_template.py` (1 hunks)
* `templates/new_condition_validation_template.py` (1 hunks)
* `tests/test_dark_energy_tap.py` (1 hunks)
* `tests/test_dark_energy_tap_abilities_integration.py` (1 hunks)
* `tests/test_technology_card_framework_integration.py` (1 hunks)

</details>

<details>
<summary>✅ Files skipped from review due to trivial changes (4)</summary>

* .kiro/specs/pr33-review-fixes/tasks.md
* docs/quick_reference.md
* docs/validation_requirements.md
* .kiro/specs/pr33-review-fixes/requirements.md

</details>

<details>
<summary>🚧 Files skipped from review as they are similar to previous changes (4)</summary>

* tests/test_dark_energy_tap.py
* docs/technology_card_framework_guide.md
* docs/api_reference.md
* tests/test_dark_energy_tap_abilities_integration.py

</details>

<details>
<summary>🧰 Additional context used</summary>

<details>
<summary>🧬 Code graph analysis (5)</summary>

<details>
<summary>templates/new_condition_validation_template.py (3)</summary><blockquote>

<details>
<summary>src/ti4/core/constants.py (1)</summary>

* `AbilityCondition` (193-206)

</details>
<details>
<summary>src/ti4/core/galaxy.py (1)</summary>

* `get_system` (36-38)

</details>
<details>
<summary>src/ti4/core/ships.py (1)</summary>

* `is_ship` (34-55)

</details>

</blockquote></details>
<details>
<summary>src/ti4/core/technology_cards/concrete/dark_energy_tap.py (7)</summary><blockquote>

<details>
<summary>src/ti4/core/abilities.py (3)</summary>

* `Ability` (142-253)
* `AbilityEffect` (71-89)
* `TimingWindow` (34-47)

</details>
<details>
<summary>src/ti4/core/constants.py (4)</summary>

* `AbilityTrigger` (157-172)
* `Faction` (234-248)
* `Technology` (96-128)
* `AbilityCondition` (193-206)

</details>
<details>
<summary>src/ti4/core/technology.py (1)</summary>

* `TechnologyColor` (13-19)

</details>
<details>
<summary>src/ti4/core/technology_cards/base/passive_tech.py (1)</summary>

* `PassiveTechnologyCard` (15-31)

</details>
<details>
<summary>src/ti4/core/technology_cards/concrete/gravity_drive.py (4)</summary>

* `color` (69-71)
* `prerequisites` (74-76)
* `faction_restriction` (79-81)
* `get_abilities` (83-95)

</details>
<details>
<summary>src/ti4/core/technology_cards/specifications.py (2)</summary>

* `TechnologySpecificationRegistry` (68-246)
* `get_specification` (133-150)

</details>
<details>
<summary>src/ti4/core/technology_cards/abilities_integration.py (1)</summary>

* `EnhancedAbility` (202-243)

</details>

</blockquote></details>
<details>
<summary>src/ti4/core/technology_cards/abilities_integration.py (3)</summary><blockquote>

<details>
<summary>src/ti4/core/abilities.py (3)</summary>

* `Ability` (142-253)
* `AbilityEffect` (71-89)
* `TimingWindow` (34-47)

</details>
<details>
<summary>src/ti4/core/constants.py (3)</summary>

* `AbilityEffectType` (175-190)
* `AbilityTrigger` (157-172)
* `AbilityCondition` (193-206)

</details>
<details>
<summary>src/ti4/core/technology_cards/specifications.py (1)</summary>

* `AbilitySpecification` (35-47)

</details>

</blockquote></details>
<details>
<summary>templates/new_ability_template.py (5)</summary><blockquote>

<details>
<summary>src/ti4/core/constants.py (3)</summary>

* `AbilityCondition` (193-206)
* `AbilityEffectType` (175-190)
* `AbilityTrigger` (157-172)

</details>
<details>
<summary>src/ti4/core/technology.py (1)</summary>

* `TechnologyColor` (13-19)

</details>
<details>
<summary>src/ti4/core/technology_cards/base/passive_tech.py (1)</summary>

* `PassiveTechnologyCard` (15-31)

</details>
<details>
<summary>src/ti4/core/technology_cards/specifications.py (2)</summary>

* `AbilitySpecification` (35-47)
* `TechnologySpecification` (51-65)

</details>
<details>
<summary>src/ti4/core/technology_cards/abilities_integration.py (1)</summary>

* `validate_ability_conditions` (246-318)

</details>

</blockquote></details>
<details>
<summary>tests/test_technology_card_framework_integration.py (10)</summary><blockquote>

<details>
<summary>src/ti4/core/abilities.py (3)</summary>

* `AbilityManager` (268-615)
* `TimingWindow` (34-47)
* `trigger_event` (297-352)

</details>
<details>
<summary>src/ti4/core/constants.py (4)</summary>

* `AbilityCondition` (193-206)
* `AbilityEffectType` (175-190)
* `AbilityTrigger` (157-172)
* `Technology` (96-128)

</details>
<details>
<summary>src/ti4/core/technology_cards/concrete/dark_energy_tap.py (5)</summary>

* `DarkEnergyTap` (22-110)
* `color` (40-42)
* `prerequisites` (45-51)
* `get_abilities` (58-63)
* `faction_restriction` (54-56)

</details>
<details>
<summary>src/ti4/core/technology_cards/concrete/gravity_drive.py (5)</summary>

* `GravityDrive` (29-95)
* `color` (69-71)
* `prerequisites` (74-76)
* `get_abilities` (83-95)
* `faction_restriction` (79-81)

</details>
<details>
<summary>src/ti4/core/technology_cards/exceptions.py (1)</summary>

* `TechnologySpecificationError` (9-28)

</details>
<details>
<summary>src/ti4/core/technology_cards/factory.py (4)</summary>

* `TechnologyCardFactory` (16-209)
* `create_card` (82-131)
* `get_supported_technologies` (168-181)
* `is_supported` (147-166)

</details>
<details>
<summary>src/ti4/core/technology_cards/registry.py (3)</summary>

* `TechnologyCardRegistry` (14-142)
* `register_card` (26-40)
* `get_card` (42-52)

</details>
<details>
<summary>src/ti4/core/technology_cards/specifications.py (2)</summary>

* `TechnologySpecificationRegistry` (68-246)
* `get_specification` (133-150)

</details>
<details>
<summary>src/ti4/core/technology_cards/abilities_integration.py (3)</summary>

* `map_trigger_to_timing` (15-50)
* `map_effect_to_handler` (53-150)
* `validate_ability_conditions` (246-318)

</details>
<details>
<summary>src/ti4/core/technology_cards/confirmation.py (1)</summary>

* `require_confirmation` (12-44)

</details>

</blockquote></details>

</details>

</details>

<details>
<summary>🔇 Additional comments (5)</summary><blockquote>

<details>
<summary>.kiro/hooks/subtask-quality-check.kiro.hook (1)</summary><blockquote>

`9-15`: **Hook patterns restored and broadened effectively**

Good call expanding the glob list—this guarantees the hook fires for code, specs, and docs instead of silently idling behind an empty pattern set. ✅

</blockquote></details>
<details>
<summary>Makefile (2)</summary><blockquote>

`70-70`: **LGTM: check-all aggregation**

Including `docs-check` and `trigger-check` here makes the baseline gate comprehensive.

---

`73-73`: **LGTM: quality-gate**

Good to keep both docs and trigger validation in the full gate.

</blockquote></details>
<details>
<summary>docs/development_guidelines.md (1)</summary><blockquote>

`1-406`: **Excellent comprehensive development guidelines.**

This documentation provides clear, actionable standards for the framework with excellent positive/negative examples, templates, and migration guidance. The fail-closed validation approach and enum-first design principles are well-articulated and align with the broader PR objectives.

</blockquote></details>
<details>
<summary>scripts/detect_hardcoded_triggers.py (1)</summary><blockquote>

`120-146`: **LGTM: File analysis with appropriate exemptions.**

The `check_file` function correctly skips `constants.py` (line 123) to avoid flagging enum definitions themselves, and it properly links missing imports to detected hardcoded triggers (lines 135-144). Error handling for syntax and analysis errors is comprehensive.

</blockquote></details>

</blockquote></details>

</details>

<!-- This is an auto-generated comment by CodeRabbit for review status -->

DETAILED COMMENTS:
----------------------------------------
Comment 1:
  File: Makefile
  Line: 5
  Body: _⚠️ Potential issue_ | _🟡 Minor_

**Add `trigger-check` to .PHONY**

Without it, a file named `trigger-check` could short‑circuit the target.
```diff
-.PHONY: all help install test lint lint-fix format type-check check-all clean dev-setup strict-check security-check runtime-check quality-gate pre-commit-install pre-commit-autoupdate format-check docs-check
+.PHONY: all help install test lint lint-fix format type-check check-all clean dev-setup strict-check security-check runtime-check quality-gate pre-commit-install pre-commit-autoupdate format-check docs-check trigger-check
```

<!-- suggestion_start -->

<details>
<summary>📝 Committable suggestion</summary>

> ‼️ **IMPORTANT**
> Carefully review the code before committing. Ensure that it accurately replaces the highlighted code, contains no missing lines, and has no issues with indentation. Thoroughly test & benchmark the code to ensure it meets the requirements.

```suggestion
.PHONY: all help install test lint lint-fix format type-check check-all clean dev-setup strict-check security-check runtime-check quality-gate pre-commit-install pre-commit-autoupdate format-check docs-check trigger-check
```

</details>

<!-- suggestion_end -->

<details>
<summary>🤖 Prompt for AI Agents</summary>

```
In Makefile at line 4, the .PHONY declaration is missing the trigger-check
target so an actual file named "trigger-check" could satisfy that make target;
update the .PHONY list to include trigger-check alongside the existing targets
to ensure the phony target cannot be short-circuited by a same-named file.
```

</details>

<!-- fingerprinting:phantom:poseidon:chinchilla -->

<!-- This is an auto-generated comment by CodeRabbit -->

Comment 2:
  File: scripts/check_documentation_consistency.py
  Line: 149
  Body: _⚠️ Potential issue_ | _🔴 Critical_

<details>
<summary>🧩 Analysis chain</summary>

**Flip the inconsistency rule: enums live in `constants.py`**

Given `AbilityCondition` is defined in `src/ti4/core/constants.py`, treat enum mentions pointing to `specifications.py` as inconsistent, not the other way around. This avoids false failures.
```diff
-                if "constants.py" in line and "enum" in line.lower():
-                    inconsistent_enum_refs.append((md_file, line_num, line))
+                if "specifications.py" in line and "enum" in line.lower():
+                    inconsistent_enum_refs.append((md_file, line_num, line))
```

---

🏁 Script executed:

```shell
#!/bin/bash
# Verify where AbilityCondition is defined
rg -nP --type=py '\bclass\s+AbilityCondition\b' -C2
```

Length of output: 599

---

<!-- [scratchpad]
[task verify_spec_file_and_refs_1/2]
[observations]
- `AbilityCondition` enum defined in `templates/new_condition_validation_template.py` and `src/ti4/core/constants.py`.
[analysis]
- To flip the rule correctly, need to confirm that `specifications.py` exists and is referenced in documentation (`.md`) files.
[pending]
- Check for the presence of `specifications.py`.
- Search for markdown references to `specifications.py`.
[actions]
- Run `fd` to locate `specifications.py`.
- Run `rg` to find references in `.md` files.
</scratchpad>

---

🏁 Script executed:

```shell
#!/bin/bash
# Verify existence of specifications.py
fd -g "specifications.py"

# Find references to specifications.py in markdown files
rg -n "specifications.py" -C2 -g '*.md'
```

Length of output: 7482

---



</details>

**Swap enum consistency check to flag `specifications.py`**
Replace the rule so it looks for `"specifications.py"` (not `"constants.py"`) when matching `"enum"`, ensuring doc refs to the old file are caught:
```diff
-                if "constants.py" in line and "enum" in line.lower():
-                    inconsistent_enum_refs.append((md_file, line_num, line))
+                if "specifications.py" in line and "enum" in line.lower():
+                    inconsistent_enum_refs.append((md_file, line_num, line))
```

<!-- suggestion_start -->

<details>
<summary>📝 Committable suggestion</summary>

> ‼️ **IMPORTANT**
> Carefully review the code before committing. Ensure that it accurately replaces the highlighted code, contains no missing lines, and has no issues with indentation. Thoroughly test & benchmark the code to ensure it meets the requirements.

```suggestion
                if "specifications.py" in line and "enum" in line.lower():
                    inconsistent_enum_refs.append((md_file, line_num, line))

    if inconsistent_enum_refs:
        print("   ❌ Found inconsistent enum file references:")
        for file_path, line_num, line in inconsistent_enum_refs:
            print(f"     {file_path.relative_to(project_root)}:{line_num} - {line}")
        all_issues.extend(inconsistent_enum_refs)
```

</details>

<!-- suggestion_end -->

<details>
<summary>🤖 Prompt for AI Agents</summary>

```
In scripts/check_documentation_consistency.py around lines 142 to 149, update
the enum consistency check to look for references to "specifications.py" instead
of "constants.py": replace the condition so it checks if "specifications.py" is
contained in the line and "enum" appears in line.lower(), leaving the rest of
the logic (collecting and reporting inconsistent_enum_refs) unchanged.
```

</details>

<!-- fingerprinting:phantom:poseidon:chinchilla -->

<!-- This is an auto-generated comment by CodeRabbit -->

Comment 3:
  File: src/ti4/core/technology_cards/abilities_integration.py
  Line: 229
  Body: _⚠️ Potential issue_ | _🔴 Critical_

**Restore fail-closed condition validation even when context is empty**

`AbilityManager.trigger_event` normalizes a missing context to `{}`, which is falsy. Once that empty dict reaches `EnhancedAbility.can_trigger`, the `if context and self.conditions` guard short-circuits, so `_validate_conditions` is never invoked and every conditional ability fires regardless of requirements. That reopens the bug we just closed in `_validate_conditions`: Dark Energy Tap will now trigger outside frontier systems as soon as the event string matches. Please drop the truthiness check and validate whenever conditions exist, defaulting `context` to `{}` so missing keys still fail closed.

```diff
-        if context and self.conditions:
-            return self._validate_conditions(context)
+        if self.conditions:
+            return self._validate_conditions(context or {})
```

<!-- suggestion_start -->

<details>
<summary>📝 Committable suggestion</summary>

> ‼️ **IMPORTANT**
> Carefully review the code before committing. Ensure that it accurately replaces the highlighted code, contains no missing lines, and has no issues with indentation. Thoroughly test & benchmark the code to ensure it meets the requirements.

```suggestion
    def can_trigger(self, event: str, context: Optional[dict[str, Any]] = None) -> bool:
        """Check if ability can trigger, including condition validation."""
        # First check base ability triggering
        if not super().can_trigger(event, context):
            return False

        # Then validate technology-specific conditions
        if self.conditions:
            return self._validate_conditions(context or {})

        return True
```

</details>

<!-- suggestion_end -->

<details>
<summary>🤖 Prompt for AI Agents</summary>

```
In src/ti4/core/technology_cards/abilities_integration.py around lines 219 to
229, the current guard uses the truthiness of context so an empty dict skips
condition checks; remove that truthiness check and ensure conditions are always
validated when self.conditions exists by calling _validate_conditions with a
defaulted context (context or {}) so missing keys still fail closed. Replace the
`if context and self.conditions:` branch with a check that only tests for
`self.conditions` and pass a guaranteed dict into _validate_conditions.
```

</details>

<!-- fingerprinting:phantom:medusa:sabertoothed -->

<!-- This is an auto-generated comment by CodeRabbit -->

Comment 4:
  File: templates/new_ability_template.py
  Line: 24
  Body: _⚠️ Potential issue_ | _🔴 Critical_

<details>
<summary>🧩 Analysis chain</summary>

**Verify TechnologyType enum exists.**

The template imports `TechnologyType` from `ti4.core.constants` (line 24) and uses it in the specification (line 63), but this enum is not visible in the provided context or relevant code snippets. Confirm that `TechnologyType` exists in the actual codebase, or replace it with the correct enum.






Also applies to: 63-63

---

🏁 Script executed:

```shell
#!/bin/bash
# Search for TechnologyType enum definition
ast-grep --pattern 'class TechnologyType'
```

Length of output: 0

---

🏁 Script executed:

```shell
#!/bin/bash
# Search for enum/class definition of TechnologyType
rg -nP 'class\s+TechnologyType\b' -g '*.py'

# Search for any occurrences (imports, usage) of TechnologyType
rg -nI 'TechnologyType'
```

Length of output: 97

---



</details>

**Undefined TechnologyType import**

The enum `TechnologyType` is imported from `ti4.core.constants` (templates/new_ability_template.py:24) and used at line 63, but no such class or enum exists in the codebase. Define `TechnologyType` in `ti4.core.constants` or update the import to reference the correct enum.

<details>
<summary>🤖 Prompt for AI Agents</summary>

```
In templates/new_ability_template.py around line 24 (usage at line 63), the
import of TechnologyType from ti4.core.constants is invalid because that enum
doesn't exist; either add a TechnologyType enum to ti4/core/constants.py with
the expected members and update exports (and adjust any type hints/usages to
match), or change the import to the correct existing enum name (search
ti4.core.constants for the intended enum, update the import and all references
in this file to that name). After making the change, run linters/tests to ensure
imports and type hints resolve.
```

</details>

<!-- This is an auto-generated comment by CodeRabbit -->

Comment 5:
  File: templates/new_ability_template.py
  Line: 66
  Body: _⚠️ Potential issue_ | _🟠 Major_

**Template uses incorrect TechnologySpecification constructor.**

The template constructs `TechnologySpecification` with fields like `name`, `color`, `prerequisites`, `type`, `expansion`, and `abilities` (lines 59-66), but the actual `TechnologySpecification` dataclass from the relevant snippets (specifications.py lines 50-64) has a different signature: `technology`, `name`, `color`, `prerequisites`, `faction_restriction`, `expansion`, `abilities`. The `type` field doesn't exist, and `technology` (a Technology enum) is required.



Update the template to match the actual API:

```diff
-        tech_spec = TechnologySpecification(
-            name="[USER_CONFIRMED_NAME]",
-            color=TechnologyColor.BLUE,  # Replace with confirmed color
-            prerequisites=[],  # Replace with confirmed prerequisites
-            type=TechnologyType.PASSIVE,  # Replace with confirmed type
-            expansion="base",  # Replace with confirmed expansion
-            abilities=self._create_abilities(),
-        )
+        # NOTE: Template requires user to add Technology enum first
+        from ti4.core.constants import Technology, Expansion
+
+        tech_spec = TechnologySpecification(
+            technology=Technology.YOUR_TECHNOLOGY_ENUM,  # Add to Technology enum first
+            name="[USER_CONFIRMED_NAME]",
+            color=TechnologyColor.BLUE,  # Replace with confirmed color
+            prerequisites=(),  # Tuple of TechnologyColor values
+            faction_restriction=None,  # Or specific Faction enum
+            expansion=Expansion.BASE,  # Use Expansion enum
+            abilities=tuple(self._create_abilities()),  # Returns tuple
+        )
```

<!-- suggestion_start -->

<details>
<summary>📝 Committable suggestion</summary>

> ‼️ **IMPORTANT**
> Carefully review the code before committing. Ensure that it accurately replaces the highlighted code, contains no missing lines, and has no issues with indentation. Thoroughly test & benchmark the code to ensure it meets the requirements.

```suggestion
        # NOTE: Template requires user to add Technology enum first
        from ti4.core.constants import Technology, Expansion

        tech_spec = TechnologySpecification(
            technology=Technology.YOUR_TECHNOLOGY_ENUM,  # Add to Technology enum first
            name="[USER_CONFIRMED_NAME]",
            color=TechnologyColor.BLUE,  # Replace with confirmed color
            prerequisites=(),  # Tuple of Technology enum values
            faction_restriction=None,  # Or specific Faction enum
            expansion=Expansion.BASE,  # Use Expansion enum
            abilities=tuple(self._create_abilities()),  # Returns tuple
        )
```

</details>

<!-- suggestion_end -->

<details>
<summary>🤖 Prompt for AI Agents</summary>

```
In templates/new_ability_template.py around lines 59 to 66, the
TechnologySpecification is being constructed with an incorrect signature (using
name, color, prerequisites, type, expansion, abilities). Update the call to
match the actual dataclass signature: provide the required technology (a
Technology enum member) as the first arg, keep name, color, prerequisites, add
faction_restriction (use None or an empty list as appropriate), then expansion
and abilities; remove the non‑existent type field and ensure parameter
names/order align with TechnologySpecification(technology, name, color,
prerequisites, faction_restriction, expansion, abilities).
```

</details>

<!-- This is an auto-generated comment by CodeRabbit -->

Comment 6:
  File: templates/new_ability_template.py
  Line: 95
  Body: _⚠️ Potential issue_ | _🟠 Major_

**Return type should be tuple, not list.**

The `_create_abilities()` method returns `list[AbilitySpecification]` (line 70), but `TechnologySpecification.abilities` expects a tuple per the dataclass definition (specifications.py line 64: `abilities: tuple[AbilitySpecification, ...]`). This mismatch will cause type errors.



```diff
-    def _create_abilities(self) -> list[AbilitySpecification]:
+    def _create_abilities(self) -> tuple[AbilitySpecification, ...]:
         """
         Create ability specifications for this technology.

         Returns:
-            List of AbilitySpecification objects
+            Tuple of AbilitySpecification objects
         """
-        abilities = []
+        abilities_list = []

         # STEP 2: Define each ability with confirmed specifications
         # Example ability - replace with user-confirmed specifications
         ability = AbilitySpecification(
             trigger=AbilityTrigger.AFTER_TACTICAL_ACTION,  # Use enum!
             effect=AbilityEffectType.EXPLORE_FRONTIER_TOKEN,  # Use enum!
-            conditions=[  # Use enum values!
+            conditions=(  # Use tuple of enum values!
                 AbilityCondition.SYSTEM_CONTAINS_FRONTIER
-            ],
+            ),
             mandatory=False,  # Confirm with user
+            passive=True,  # Confirm with user
         )
-        abilities.append(ability)
+        abilities_list.append(ability)

         # Add additional abilities as confirmed by user
         # ability2 = AbilitySpecification(...)
-        # abilities.append(ability2)
+        # abilities_list.append(ability2)

-        return abilities
+        return tuple(abilities_list)
```


> Committable suggestion skipped: line range outside the PR's diff.

<details>
<summary>🤖 Prompt for AI Agents</summary>

```
In templates/new_ability_template.py around lines 70 to 95, the
_create_abilities() function is annotated to return list[AbilitySpecification]
and builds a list, but TechnologySpecification.abilities expects a tuple; change
the function signature to return tuple[AbilitySpecification, ...] (and update
the docstring if needed) and convert the collected abilities to a tuple before
returning (e.g., return tuple(abilities)); ensure any type hints for local
variables reflect the tuple/ellipsis form so it matches the dataclass
expectation.
```

</details>

<!-- This is an auto-generated comment by CodeRabbit -->

Comment 7:
  File: templates/new_ability_template.py
  Line: 88
  Body: _⚠️ Potential issue_ | _🟠 Major_

**Template AbilitySpecification is missing required `passive` field.**

The template constructs `AbilitySpecification` without the `passive` field (lines 81-88), but the actual dataclass (specifications.py lines 34-46) requires both `mandatory` and `passive` boolean fields. This will cause instantiation errors.



Add the missing field:

```diff
         ability = AbilitySpecification(
             trigger=AbilityTrigger.AFTER_TACTICAL_ACTION,  # Use enum!
             effect=AbilityEffectType.EXPLORE_FRONTIER_TOKEN,  # Use enum!
-            conditions=[  # Use enum values!
+            conditions=(  # Use tuple of enum values!
                 AbilityCondition.SYSTEM_CONTAINS_FRONTIER
-            ],
+            ),
             mandatory=False,  # Confirm with user
+            passive=True,  # Confirm with user (True for passive effects, False for active)
         )
```

<!-- suggestion_start -->

<details>
<summary>📝 Committable suggestion</summary>

> ‼️ **IMPORTANT**
> Carefully review the code before committing. Ensure that it accurately replaces the highlighted code, contains no missing lines, and has no issues with indentation. Thoroughly test & benchmark the code to ensure it meets the requirements.

```suggestion
        ability = AbilitySpecification(
            trigger=AbilityTrigger.AFTER_TACTICAL_ACTION,  # Use enum!
            effect=AbilityEffectType.EXPLORE_FRONTIER_TOKEN,  # Use enum!
            conditions=(  # Use tuple of enum values!
                AbilityCondition.SYSTEM_CONTAINS_FRONTIER
            ),
            mandatory=False,  # Confirm with user
            passive=True,  # Confirm with user (True for passive effects, False for active)
        )
```

</details>

<!-- suggestion_end -->

<details>
<summary>🤖 Prompt for AI Agents</summary>

```
In templates/new_ability_template.py around lines 81 to 88, the
AbilitySpecification instantiation omits the required passive boolean field; add
a passive=<bool> entry (e.g., passive=False) alongside mandatory=False so the
dataclass constructor matches the specification and the template will
instantiate without errors.
```

</details>

<!-- This is an auto-generated comment by CodeRabbit -->

============================================================

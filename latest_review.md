Warning: No GitHub token provided. API rate limits may apply.
Consider setting GITHUB_TOKEN environment variable or using --token

Latest review for PR #8 in NoahPeres/ti4-ai:

============================================================
GITHUB PR REVIEW SUMMARY
============================================================
Reviewer: coderabbitai[bot]
State: COMMENTED
Submitted: 2025-09-20T00:42:07Z
Review ID: 3247794728

REVIEW BODY:
----------------------------------------
**Actionable comments posted: 7**

> [!CAUTION]
> Some comments are outside the diff and can’t be posted inline due to platform limitations.
> 
> 
> 
> <details>
> <summary>⚠️ Outside diff range comments (2)</summary><blockquote>
> 
> <details>
> <summary>src/ti4/core/combat.py (2)</summary><blockquote>
> 
> `64-64`: **Stop re-wrapping UnitType; use the unit’s own stats (keeps faction/tech mods).**
> 
> `UnitType(unit.unit_type)` will raise when `unit.unit_type` is already an enum, and it drops faction/tech modifiers by bypassing `Unit.get_stats()`.
> 
> Apply:
> 
> ```diff
> -        stats = self.unit_stats_provider.get_unit_stats(UnitType(unit.unit_type))
> +        stats = unit.get_stats()
> ```
> 
> ---
> 
> `251-257`: **Same enum/stats issue here; use unit.get_stats().**
> 
> Avoid `UnitType(unit.unit_type)` and respect modifiers.
> 
> Apply:
> 
> ```diff
> -        stats = self.unit_stats_provider.get_unit_stats(UnitType(unit.unit_type))
> +        stats = unit.get_stats()
> ```
> 
> </blockquote></details>
> 
> </blockquote></details>

<details>
<summary>🧹 Nitpick comments (18)</summary><blockquote>

<details>
<summary>IMPLEMENTATION_ROADMAP.md (2)</summary><blockquote>

`11-18`: **Align progress figures and status claims.**

Section shows “Overall Progress: 28.7%” and several “NEWLY COMPLETED” items, while earlier header still reflects older totals/dates. Please reconcile all progress numbers and “newly completed” badges to the current state to avoid contradictions.

---

`38-46`: **“Next Up” list contains already-completed items.**

Items 7 and 9 are marked “COMPLETE” under “Next Up.” Move them to a completed section or remove from “Next Up” for clarity.

</blockquote></details>
<details>
<summary>.trae/lrr_analysis/78_space_combat.md (2)</summary><blockquote>

`51-58`: **Retreat eligibility not enforced in implementation.**

Docs require an “eligible system” for retreat; implementation currently moves units without validating adjacency/ownership/command‑token constraints. Add the rule checks or note the limitation here.

---

`102-108`: **Anti‑fighter barrage and step order details.**

Consider documenting the exact prerequisites for AFB (first round only; units with AFB; fighter-only targets) and match that to code-level checks.

</blockquote></details>
<details>
<summary>src/ti4/core/unit_stats.py (1)</summary><blockquote>

`11-17`: **Fix flake8 W293: trailing whitespace on blank lines.**

The CI warns about whitespace-only lines (12, 17, 25). Strip trailing spaces.



Also applies to: 25-25

</blockquote></details>
<details>
<summary>.trae/lrr_analysis/18_combat.md (2)</summary><blockquote>

`41-45`: **Clarify burst‑icon vs. combat_dice source of dice.**

This section says “burst icons are visual; actual dice from combat_dice,” which conflicts with 18.2 stating each burst icon adds a die. Please reconcile: either define combat_dice to already include burst icons or specify how burst icons modify the per‑unit dice pool.

---

`75-77`: **Replace placeholder dates.**

Update 2024-01-XX entries with real dates for auditability.

</blockquote></details>
<details>
<summary>src/ti4/core/space_combat.py (4)</summary><blockquote>

`42-45`: **AFB should check presence of AFB units.**

Limit AFB availability to round 1 and only if any participating unit has the ability.


```diff
 def can_use_anti_fighter_barrage(self) -> bool:
-        """Anti-fighter barrage only available in first round (Rule 78.3b)."""
-        return self.round_number == 1
+        """AFB only in first round and only if any unit has AFB (Rule 78.3b)."""
+        if self.round_number != 1:
+            return False
+        return any(
+            u.has_anti_fighter_barrage() for u in (self.attacker_units + self.defender_units)
+        )
```

---

`87-96`: **Dice count should use units’ combat_dice, not unit count.**

Count only units with a combat value.


```diff
 def get_attacker_dice_count(self) -> int:
-        """Get number of dice attacker should roll."""
-        # For now, return number of units (simplified)
-        return len(self.attacker_units)
+        """Total dice from attacker units."""
+        return sum(
+            u.get_combat_dice() for u in self.attacker_units if u.get_combat_value() is not None
+        )
@@
 def get_defender_dice_count(self) -> int:
-        """Get number of dice defender should roll."""
-        # For now, return number of units (simplified)
-        return len(self.defender_units)
+        """Total dice from defender units."""
+        return sum(
+            u.get_combat_dice() for u in self.defender_units if u.get_combat_value() is not None
+        )
```

---

`106-121`: **Use default_factory for list field and drop __post_init__.**

Safer and cleaner dataclass for mutable default.


```diff
-from dataclasses import dataclass
+from dataclasses import dataclass, field
@@
-    units_destroyed: list[Unit] = None
-
-    def __post_init__(self) -> None:
-        if self.units_destroyed is None:
-            self.units_destroyed = []
+    units_destroyed: list[Unit] = field(default_factory=list)
```

---

`254-254`: **Add trailing newline (CI warning W292).**

</blockquote></details>
<details>
<summary>src/ti4/core/combat.py (1)</summary><blockquote>

`83-83`: **Strip trailing whitespace (W293).**

CI warns about whitespace on blank lines. Remove trailing spaces to quiet lint.



Also applies to: 86-86, 89-89, 96-96, 99-99, 102-102, 109-109

</blockquote></details>
<details>
<summary>tests/test_rule_18_burst_icons.py (2)</summary><blockquote>

`46-46`: **Remove unused variable (F841).**

`stats_provider` is unused and fails CI.

Apply:

```diff
-        stats_provider = UnitStatsProvider()
```

---

`47-47`: **Trim trailing whitespace (W293) and add EOF newline (W292).**

Clean up lint nits to get CI green.

Apply:

```diff
@@
-        
+
@@
-        
+
@@
-        
+
@@
-        
+
@@
-        
+
+```
(Ensure the file ends with a newline.)
```


Also applies to: 53-53, 60-60, 64-64, 73-73

</blockquote></details>
<details>
<summary>tests/test_rule_78_space_combat.py (4)</summary><blockquote>

`254-260`: **Fix unused import (F401) while still asserting ImportError.**

Use `importlib.import_module` within the `raises` block.

Apply:

```diff
-        with pytest.raises(ImportError):
-            from src.ti4.core.tactical_action import TacticalAction
-            # This import should fail since tactical action integration isn't implemented yet
+        with pytest.raises(ImportError):
+            import importlib
+            importlib.import_module("src.ti4.core.tactical_action")
```

---

`305-305`: **Remove trailing whitespace (W293).**

Trim spaces on these blank lines to satisfy CI.



Also applies to: 321-321, 342-342, 350-350, 374-374, 414-414, 438-438, 462-462

---

`469-469`: **Add newline at end of file (W292).**

Add a trailing newline.

---

`245-249`: **end_combat winner param appears unused in implementation.**

If `SpaceCombat.end_combat(winner)` ignores the argument, either remove the param or use it. Not a blocker for tests.

</blockquote></details>

</blockquote></details>

<details>
<summary>📜 Review details</summary>

**Configuration used**: CodeRabbit UI

**Review profile**: CHILL

**Plan**: Pro

<details>
<summary>📥 Commits</summary>

Reviewing files that changed from the base of the PR and between e58dfb846b5bd476c12e126334430856082b4bd1 and 2f73104c82f8a049b00c73681a5b0cf2fd585164.

</details>

<details>
<summary>📒 Files selected for processing (8)</summary>

* `.trae/lrr_analysis/18_combat.md` (1 hunks)
* `.trae/lrr_analysis/78_space_combat.md` (1 hunks)
* `IMPLEMENTATION_ROADMAP.md` (3 hunks)
* `src/ti4/core/combat.py` (1 hunks)
* `src/ti4/core/space_combat.py` (1 hunks)
* `src/ti4/core/unit_stats.py` (3 hunks)
* `tests/test_rule_18_burst_icons.py` (1 hunks)
* `tests/test_rule_78_space_combat.py` (1 hunks)

</details>

<details>
<summary>🧰 Additional context used</summary>

<details>
<summary>🧬 Code graph analysis (5)</summary>

<details>
<summary>src/ti4/core/combat.py (3)</summary><blockquote>

<details>
<summary>src/ti4/core/unit.py (1)</summary>

* `Unit` (10-187)

</details>
<details>
<summary>src/ti4/core/unit_stats.py (1)</summary>

* `get_unit_stats` (141-156)

</details>
<details>
<summary>src/ti4/core/constants.py (1)</summary>

* `UnitType` (6-20)

</details>

</blockquote></details>
<details>
<summary>tests/test_rule_78_space_combat.py (4)</summary><blockquote>

<details>
<summary>src/ti4/core/combat.py (2)</summary>

* `CombatDetector` (12-27)
* `should_initiate_combat` (19-27)

</details>
<details>
<summary>src/ti4/core/space_combat.py (15)</summary>

* `CombatStep` (17-25)
* `SpaceCombat` (124-254)
* `start_combat` (135-152)
* `can_use_anti_fighter_barrage` (42-44)
* `can_defender_announce_retreat` (46-48)
* `defender_announces_retreat` (56-58)
* `can_attacker_announce_retreat` (50-54)
* `get_attacker_dice_count` (87-90)
* `get_defender_dice_count` (92-95)
* `assign_hits_to_attacker` (97-99)
* `assign_hits_to_defender` (101-103)
* `should_continue` (154-167)
* `next_round` (169-186)
* `end_combat` (188-227)
* `execute_retreat_step` (64-85)

</details>
<details>
<summary>src/ti4/core/system.py (1)</summary>

* `System` (12-168)

</details>
<details>
<summary>src/ti4/core/unit.py (1)</summary>

* `Unit` (10-187)

</details>

</blockquote></details>
<details>
<summary>src/ti4/core/space_combat.py (3)</summary><blockquote>

<details>
<summary>src/ti4/core/constants.py (1)</summary>

* `UnitType` (6-20)

</details>
<details>
<summary>src/ti4/core/system.py (1)</summary>

* `System` (12-168)

</details>
<details>
<summary>src/ti4/core/unit.py (1)</summary>

* `Unit` (10-187)

</details>

</blockquote></details>
<details>
<summary>tests/test_rule_18_burst_icons.py (4)</summary><blockquote>

<details>
<summary>src/ti4/core/combat.py (3)</summary>

* `CombatResolver` (50-291)
* `roll_dice_for_unit_with_burst_icons` (81-105)
* `calculate_hits` (114-123)

</details>
<details>
<summary>src/ti4/core/constants.py (1)</summary>

* `UnitType` (6-20)

</details>
<details>
<summary>src/ti4/core/unit.py (1)</summary>

* `Unit` (10-187)

</details>
<details>
<summary>src/ti4/core/unit_stats.py (3)</summary>

* `UnitStats` (10-59)
* `UnitStatsProvider` (62-235)
* `get_unit_stats` (141-156)

</details>

</blockquote></details>
<details>
<summary>src/ti4/core/unit_stats.py (1)</summary><blockquote>

<details>
<summary>src/ti4/core/unit.py (1)</summary>

* `sustain_damage` (130-134)

</details>

</blockquote></details>

</details><details>
<summary>🪛 GitHub Actions: CI</summary>

<details>
<summary>src/ti4/core/combat.py</summary>

[warning] 83-83: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 86-86: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 89-89: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 96-96: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 99-99: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 102-102: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 109-109: W293 Blank line contains whitespace. Remove whitespace from blank line.

</details>
<details>
<summary>tests/test_rule_78_space_combat.py</summary>

[error] 258-258: F401 Unused import. Remove unused import: TacticalAction (src.ti4.core.tactical_action.TacticalAction).

---

[warning] 305-305: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 321-321: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 342-342: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 350-350: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 374-374: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 414-414: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 438-438: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 462-462: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 75-75: W292 No newline at end of file. Add trailing newline.

---

[warning] 342-342: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 305-305: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 321-321: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 374-374: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 414-414: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 438-438: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 462-462: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 342-342: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 374-374: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 414-414: W293 Blank line contains whitespace. Remove whitespace from blank line.

</details>
<details>
<summary>src/ti4/core/space_combat.py</summary>

[warning] 254-254: W292 No newline at end of file. Add trailing newline.

</details>
<details>
<summary>tests/test_rule_18_burst_icons.py</summary>

[error] 46-46: F841 Local variable 'stats_provider' is assigned to but never used. Remove assignment or use the variable.

---

[warning] 47-47: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 53-53: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 60-60: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 64-64: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 73-73: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 75-75: W292 No newline at end of file. Add trailing newline.

---

[error] 46-46: F841 Local variable 'stats_provider' is assigned to but never used. Remove assignment or use the variable.

</details>
<details>
<summary>src/ti4/core/unit_stats.py</summary>

[warning] 12-12: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 17-17: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 25-25: W293 Blank line contains whitespace. Remove whitespace from blank line.

</details>

</details>

</details>

<details>
<summary>🔇 Additional comments (6)</summary><blockquote>

<details>
<summary>IMPLEMENTATION_ROADMAP.md (1)</summary><blockquote>

`49-55`: **Metrics narrative consistency.**

Ensure the Core layer count (13/15) and total completed rules (20/101) align with earlier progress bullets and any dashboards you publish externally.

</blockquote></details>
<details>
<summary>.trae/lrr_analysis/78_space_combat.md (1)</summary><blockquote>

`23-29`: **Docs say attacker cannot announce retreat; code allows it.**

The analysis and tests here assert only the defender can announce retreat. src/ti4/core/space_combat.py exposes can_attacker_announce_retreat()/attacker_announces_retreat(). Please align docs or gate attacker retreat behind a rule/flag.

</blockquote></details>
<details>
<summary>src/ti4/core/space_combat.py (1)</summary><blockquote>

`242-254`: **Ship set looks good; consider using constants.System.has_enemy_ships semantics.**

No action required; just a note to keep structure types (PDS/space_dock) out of space area so this stays accurate.

</blockquote></details>
<details>
<summary>src/ti4/core/combat.py (2)</summary><blockquote>

`107-113`: **Alias method OK.**

`calculate_hits_with_burst_icons` delegating to the roll method is fine after the refactor above.

---

`145-149`: **Resolved — has_sustained_damage property exists**  
Unit defines @property has_sustained_damage (src/ti4/core/unit.py:126) and sustain_damage()/repair_damage(); tests and docs reference it, so the conditional in src/ti4/core/combat.py is valid.

</blockquote></details>
<details>
<summary>tests/test_rule_18_burst_icons.py (1)</summary><blockquote>

`15-29`: **Test is fine but non-deterministic.**

Acceptable as a smoke test. If you want determinism later, monkeypatch `random.randint` or seed RNG.

</blockquote></details>

</blockquote></details>

</details>

<!-- This is an auto-generated comment by CodeRabbit for review status -->

DETAILED COMMENTS:
----------------------------------------
Comment 1:
  File: src/ti4/core/combat.py
  Line: Unknown
  Body: _🛠️ Refactor suggestion_

**Deduplicate burst-icon roll; delegate to roll_dice_for_unit (and fix enum/stats bug).**

No need to reimplement the same logic; delegate so both paths stay consistent and respect unit modifiers.

Apply:

```diff
-    def roll_dice_for_unit_with_burst_icons(self, unit: Unit) -> int:
-        """Roll dice for a unit using burst icon mechanics.
-        
-        Each burst icon on the unit's combat value represents one die to roll.
-        Burst icons are purely visual - the actual number of dice is combat_dice.
-        
-        Args:
-            unit: The unit rolling dice
-            
-        Returns:
-            Number of hits scored
-        """
-        stats = self.unit_stats_provider.get_unit_stats(UnitType(unit.unit_type))
-        if stats.combat_value is None:
-            return 0
-            
-        # Use combat_dice to determine number of dice (burst icons are visual only)
-        dice_count = stats.combat_dice
-        
-        if dice_count <= 0:
-            return 0
-            
-        # Roll dice and calculate hits
-        dice_results = [random.randint(1, 10) for _ in range(dice_count)]
-        return self.calculate_hits(dice_results, stats.combat_value)
+    def roll_dice_for_unit_with_burst_icons(self, unit: Unit) -> int:
+        """Roll dice using burst-icon semantics (visual only). Delegates to roll_dice_for_unit."""
+        return self.roll_dice_for_unit(unit)
```

<!-- suggestion_start -->

<details>
<summary>📝 Committable suggestion</summary>

> ‼️ **IMPORTANT**
> Carefully review the code before committing. Ensure that it accurately replaces the highlighted code, contains no missing lines, and has no issues with indentation. Thoroughly test & benchmark the code to ensure it meets the requirements.

```suggestion
    def roll_dice_for_unit_with_burst_icons(self, unit: Unit) -> int:
        """Roll dice using burst-icon semantics (visual only). Delegates to roll_dice_for_unit."""
        return self.roll_dice_for_unit(unit)

    def calculate_hits_with_burst_icons(self, unit: Unit) -> int:
        """Calculate hits for a unit using burst icon mechanics.
        
        This is an alias for roll_dice_for_unit_with_burst_icons for clarity.
        """
        return self.roll_dice_for_unit_with_burst_icons(unit)
```

</details>

<!-- suggestion_end -->

<details>
<summary>🧰 Tools</summary>

<details>
<summary>🪛 GitHub Actions: CI</summary>

[warning] 83-83: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 86-86: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 89-89: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 96-96: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 99-99: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 102-102: W293 Blank line contains whitespace. Remove whitespace from blank line.

---

[warning] 109-109: W293 Blank line contains whitespace. Remove whitespace from blank line.

</details>

</details>

<!-- fingerprinting:phantom:medusa:chinchilla -->

<!-- This is an auto-generated comment by CodeRabbit -->

Comment 2:
  File: src/ti4/core/space_combat.py
  Line: Unknown
  Body: _⚠️ Potential issue_

**Attacker retreat policy contradicts docs/tests.**

If base rules disallow attacker retreat, make this always return False (gate later behind a variant/tech).


```diff
 def can_attacker_announce_retreat(self) -> bool:
-        """Attacker can announce retreat if defender hasn't announced retreat (Rule 78.4b)."""
-        return (
-            not self.attacker_announced_retreat and not self.defender_announced_retreat
-        )
+        """Attacker retreat disabled under base rules; enable via variant if needed."""
+        return False
```

<!-- suggestion_start -->

<details>
<summary>📝 Committable suggestion</summary>

> ‼️ **IMPORTANT**
> Carefully review the code before committing. Ensure that it accurately replaces the highlighted code, contains no missing lines, and has no issues with indentation. Thoroughly test & benchmark the code to ensure it meets the requirements.

```suggestion
    def can_attacker_announce_retreat(self) -> bool:
        """Attacker retreat disabled under base rules; enable via variant if needed."""
        return False
```

</details>

<!-- suggestion_end -->

<details>
<summary>🤖 Prompt for AI Agents</summary>

```
In src/ti4/core/space_combat.py around lines 50 to 55, the current
can_attacker_announce_retreat() allows attacker retreat by checking
attacker_announced_retreat and defender_announced_retreat, which contradicts
base rules; change this method to always return False (disallow attacker
retreats under base rules) and add a clear TODO comment noting that support for
attacker retreat should be reintroduced behind a variant/tech gate (e.g., check
a future self.rules.allow_attacker_retreat flag) so the gating can be
implemented later.
```

</details>

<!-- fingerprinting:phantom:medusa:chinchilla -->

<!-- This is an auto-generated comment by CodeRabbit -->

Comment 3:
  File: src/ti4/core/space_combat.py
  Line: Unknown
  Body: _⚠️ Potential issue_

**Retreat moves units without removing them from the origin system.**

Units are appended to retreat_system but never removed from the current system, so they remain in both systems, and should_continue() may loop incorrectly. Use System.remove_unit_from_space()/place_unit_in_space() and give CombatRound a reference to the current system.

Apply this diff:

```diff
@@
-@dataclass
+@dataclass
 class CombatRound:
@@
-    attacker_id: str
+    attacker_id: str
     defender_id: str
     attacker_units: list[Unit]
     defender_units: list[Unit]
+    system: System
@@
-    def execute_retreat_step(self, retreat_system: System) -> bool:
+    def execute_retreat_step(self, retreat_system: System) -> bool:
         """Execute retreat step - move retreating units to retreat system."""
         if self.defender_announced_retreat:
@@
-            for unit in retreating_units:
-                if unit in self.defender_units:
-                    self.defender_units.remove(unit)
-                # Remove from current system (need to access the system from combat context)
-                # This is a simplified implementation - in full game would need proper system reference
-                retreat_system.space_units.append(unit)
+            for unit in retreating_units:
+                if unit in self.defender_units:
+                    self.defender_units.remove(unit)
+                # Move between systems
+                self.system.remove_unit_from_space(unit)
+                retreat_system.place_unit_in_space(unit)
             return True
         elif self.attacker_announced_retreat:
@@
-            for unit in retreating_units:
-                if unit in self.attacker_units:
-                    self.attacker_units.remove(unit)
-                # Remove from current system and add to retreat system
-                retreat_system.space_units.append(unit)
+            for unit in retreating_units:
+                if unit in self.attacker_units:
+                    self.attacker_units.remove(unit)
+                self.system.remove_unit_from_space(unit)
+                retreat_system.place_unit_in_space(unit)
             return True
         return False
```

And pass system when constructing rounds (see separate diff).

<!-- suggestion_start -->

<details>
<summary>📝 Committable suggestion</summary>

> ‼️ **IMPORTANT**
> Carefully review the code before committing. Ensure that it accurately replaces the highlighted code, contains no missing lines, and has no issues with indentation. Thoroughly test & benchmark the code to ensure it meets the requirements.

```suggestion
    def execute_retreat_step(self, retreat_system: System) -> bool:
        """Execute retreat step - move retreating units to retreat system."""
        if self.defender_announced_retreat:
            # Move defender units to retreat system
            retreating_units = [u for u in self.defender_units if u.owner == self.defender_id]
            for unit in retreating_units:
                if unit in self.defender_units:
                    self.defender_units.remove(unit)
                # Move between systems
                self.system.remove_unit_from_space(unit)
                retreat_system.place_unit_in_space(unit)
            return True
        elif self.attacker_announced_retreat:
            # Move attacker units to retreat system
            retreating_units = [u for u in self.attacker_units if u.owner == self.attacker_id]
            for unit in retreating_units:
                if unit in self.attacker_units:
                    self.attacker_units.remove(unit)
                self.system.remove_unit_from_space(unit)
                retreat_system.place_unit_in_space(unit)
            return True
        return False
```

</details>

<!-- suggestion_end -->

<details>
<summary>🤖 Prompt for AI Agents</summary>

```
In src/ti4/core/space_combat.py around lines 64 to 85, retreating units are
appended to retreat_system.space_units but never removed from their origin
system; update execute_retreat_step to call the origin system's
remove_unit_from_space(unit) and retreat_system.place_unit_in_space(unit)
instead of directly manipulating lists, and ensure CombatRound (or whatever
constructs this method) is given a reference to the current system so you can
call current_system.remove_unit_from_space(...) for each moved unit; also remove
units from self.attacker_units/self.defender_units only after using the System
APIs to keep state consistent.
```

</details>

<!-- fingerprinting:phantom:medusa:chinchilla -->

<!-- This is an auto-generated comment by CodeRabbit -->

Comment 4:
  File: src/ti4/core/space_combat.py
  Line: Unknown
  Body: _🛠️ Refactor suggestion_

**Pass system into CombatRound to support safe retreats.**

Include the system reference in round construction so execute_retreat_step can mutate the origin system safely.


```diff
@@ def start_combat(self) -> CombatRound:
-        return CombatRound(
+        return CombatRound(
             round_number=self.current_round,
             current_step=CombatStep.BEFORE_COMBAT,
             attacker_id=self.attacker_id,
             defender_id=self.defender_id,
             attacker_units=attacker_units,
             defender_units=defender_units,
+            system=self.system,
         )
```

<!-- suggestion_start -->

<details>
<summary>📝 Committable suggestion</summary>

> ‼️ **IMPORTANT**
> Carefully review the code before committing. Ensure that it accurately replaces the highlighted code, contains no missing lines, and has no issues with indentation. Thoroughly test & benchmark the code to ensure it meets the requirements.

```suggestion
    def start_combat(self) -> CombatRound:
        """Start the first round of combat."""
        self.current_round = 1
        attacker_units = [
            u for u in self.system.space_units if u.owner == self.attacker_id
        ]
        defender_units = [
            u for u in self.system.space_units if u.owner == self.defender_id
        ]

        return CombatRound(
            round_number=self.current_round,
            current_step=CombatStep.BEFORE_COMBAT,
            attacker_id=self.attacker_id,
            defender_id=self.defender_id,
            attacker_units=attacker_units,
            defender_units=defender_units,
            system=self.system,
        )
```

</details>

<!-- suggestion_end -->

<details>
<summary>🤖 Prompt for AI Agents</summary>

```
In src/ti4/core/space_combat.py around lines 135 to 153, the CombatRound is
constructed without a reference to the originating system; update the call to
include system=self.system so retreat logic can mutate the system safely (e.g.,
add system=self.system to the CombatRound constructor). If CombatRound's
signature or dataclass does not accept a system parameter, add a typed field for
the system there and propagate the change to any other constructors/usages.
```

</details>

<!-- fingerprinting:phantom:medusa:chinchilla -->

<!-- This is an auto-generated comment by CodeRabbit -->

Comment 5:
  File: src/ti4/core/space_combat.py
  Line: Unknown
  Body: _🛠️ Refactor suggestion_

**Also pass system on subsequent rounds.**


```diff
@@ def next_round(self) -> CombatRound:
-        return CombatRound(
+        return CombatRound(
             round_number=self.current_round,
             current_step=CombatStep.ANNOUNCE_RETREATS,  # Rule 78.8: Next round starts with retreat announcement
             attacker_id=self.attacker_id,
             defender_id=self.defender_id,
             attacker_units=attacker_units,
             defender_units=defender_units,
+            system=self.system,
         )
```

<!-- suggestion_start -->

<details>
<summary>📝 Committable suggestion</summary>

> ‼️ **IMPORTANT**
> Carefully review the code before committing. Ensure that it accurately replaces the highlighted code, contains no missing lines, and has no issues with indentation. Thoroughly test & benchmark the code to ensure it meets the requirements.

```suggestion
    def next_round(self) -> CombatRound:
        """Start the next round of combat."""
        self.current_round += 1
        attacker_units = [
            u for u in self.system.space_units if u.owner == self.attacker_id
        ]
        defender_units = [
            u for u in self.system.space_units if u.owner == self.defender_id
        ]

        return CombatRound(
            round_number=self.current_round,
            current_step=CombatStep.ANNOUNCE_RETREATS,  # Rule 78.8: Next round starts with retreat announcement
            attacker_id=self.attacker_id,
            defender_id=self.defender_id,
            attacker_units=attacker_units,
            defender_units=defender_units,
            system=self.system,
        )
```

</details>

<!-- suggestion_end -->

<details>
<summary>🤖 Prompt for AI Agents</summary>

```
In src/ti4/core/space_combat.py around lines 169 to 187, the next_round() method
constructs a CombatRound for subsequent rounds but does not pass the current
system into the CombatRound; update the CombatRound constructor call to include
system=self.system so the new round has the same system context (ensure the
CombatRound signature accepts a system parameter if not already).
```

</details>

<!-- fingerprinting:phantom:medusa:chinchilla -->

<!-- This is an auto-generated comment by CodeRabbit -->

Comment 6:
  File: src/ti4/core/unit_stats.py
  Line: Unknown
  Body: _⚠️ Potential issue_

**Default values make modifiers add unintended +1 to multiple stats.**

UnitStats is used for both base stats and “modifiers.” With defaults like cost=1, combat_dice=1, movement=1, _apply_modifications() will add +1 even when a modifier intends “no change.” Make additive fields default to 0 for modifier usage.

Apply this diff:

```diff
-    cost: float = 1
+    cost: float = 0
@@
-    combat_dice: int = 1
+    combat_dice: int = 0
@@
-    movement: int = 1
+    movement: int = 0
```

BASE_STATS already sets all explicit values, so this will not alter base units but will fix modifier math.

<!-- suggestion_start -->

<details>
<summary>📝 Committable suggestion</summary>

> ‼️ **IMPORTANT**
> Carefully review the code before committing. Ensure that it accurately replaces the highlighted code, contains no missing lines, and has no issues with indentation. Thoroughly test & benchmark the code to ensure it meets the requirements.

```suggestion
    # === FUNDAMENTAL UNIT PROPERTIES ===
    cost: float = 0
    combat_value: Optional[int] = None
    combat_dice: int = 0
    movement: int = 0
    capacity: int = 0
    production: int = 0
    
    # === UNIT ABILITIES ===
```

</details>

<!-- suggestion_end -->

<details>
<summary>🧰 Tools</summary>

<details>
<summary>🪛 GitHub Actions: CI</summary>

[warning] 25-25: W293 Blank line contains whitespace. Remove whitespace from blank line.

</details>

</details>

<details>
<summary>🤖 Prompt for AI Agents</summary>

```
In src/ti4/core/unit_stats.py around lines 18 to 26, the default additive fields
(cost, combat_dice, movement) are set to 1 which causes modifiers to
unintentionally add +1 when they mean "no change"; change those defaults to 0
(leave combat_value as Optional[int]=None and keep capacity and production as 0)
so that modifier instances apply zero by default and BASE_STATS (which sets all
values explicitly) remains unaffected.
```

</details>

<!-- fingerprinting:phantom:medusa:chinchilla -->

<!-- This is an auto-generated comment by CodeRabbit -->

Comment 7:
  File: src/ti4/core/unit_stats.py
  Line: Unknown
  Body: _🛠️ Refactor suggestion_

**Modifier application should treat absent fields as 0/None.**

With the defaults fixed to 0, this logic becomes correct. Also, keep “value replacement” semantics only for Optional fields (e.g., combat_value, space_cannon_value).

Optionally harden against negative dice/movement:

```diff
-            combat_dice=base.combat_dice + modifications.combat_dice,
+            combat_dice=max(0, base.combat_dice + modifications.combat_dice),
@@
-            movement=base.movement + modifications.movement,
+            movement=max(0, base.movement + modifications.movement),
```

<!-- suggestion_start -->

<details>
<summary>📝 Committable suggestion</summary>

> ‼️ **IMPORTANT**
> Carefully review the code before committing. Ensure that it accurately replaces the highlighted code, contains no missing lines, and has no issues with indentation. Thoroughly test & benchmark the code to ensure it meets the requirements.

```suggestion
            # Fundamental properties
            cost=base.cost + modifications.cost,
            combat_value=modifications.combat_value
            if modifications.combat_value is not None
            else base.combat_value,
            combat_dice=max(0, base.combat_dice + modifications.combat_dice),
            movement=max(0, base.movement + modifications.movement),
            capacity=base.capacity + modifications.capacity,
            production=base.production + modifications.production,
            # Unit abilities
            sustain_damage=base.sustain_damage or modifications.sustain_damage,
            anti_fighter_barrage=base.anti_fighter_barrage
            or modifications.anti_fighter_barrage,
            bombardment=base.bombardment or modifications.bombardment,
            deploy=base.deploy or modifications.deploy,
            planetary_shield=base.planetary_shield or modifications.planetary_shield,
            space_cannon=base.space_cannon or modifications.space_cannon,
            space_cannon_value=modifications.space_cannon_value
            if modifications.space_cannon_value is not None
            else base.space_cannon_value,
            space_cannon_dice=base.space_cannon_dice + modifications.space_cannon_dice,
        )
```

</details>

<!-- suggestion_end -->

<!-- fingerprinting:phantom:medusa:chinchilla -->

<!-- This is an auto-generated comment by CodeRabbit -->

============================================================

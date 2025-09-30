Latest review for PR #33 in NoahPeres/ti4-ai:

============================================================
GITHUB PR REVIEW SUMMARY
============================================================
Reviewer: coderabbitai[bot]
State: COMMENTED
Submitted: 2025-09-30T10:41:09Z
Review ID: 3283926147

REVIEW BODY:
----------------------------------------
**Actionable comments posted: 2**

<details>
<summary>♻️ Duplicate comments (2)</summary><blockquote>

<details>
<summary>scripts/check_documentation_consistency.py (1)</summary><blockquote>

`22-28`: **Restore enum mismatch detection for `specifications.py`.**

Line 22 still only matches `constants.py`, so the new check at Line 142 for `specifications.py` never fires and we stop flagging the doc references we meant to catch. Please flip the regexes (and the inline comment) so `find_enum_references` records `specifications.py` mentions.


```diff
-                # Look for references to constants.py or specifications.py in enum contexts
-                if re.search(r"enum.*constants\.py", line, re.IGNORECASE):
+                # Look for references to specifications.py in enum contexts
+                if re.search(r"enum.*specifications\.py", line, re.IGNORECASE):
                     references.append((line_num, line.strip()))
-                elif re.search(r"constants\.py.*enum", line, re.IGNORECASE):
+                elif re.search(r"specifications\.py.*enum", line, re.IGNORECASE):
                     references.append((line_num, line.strip()))
-                elif re.search(r"Add.*enum.*constants\.py", line, re.IGNORECASE):
+                elif re.search(r"Add.*enum.*specifications\.py", line, re.IGNORECASE):
                     references.append((line_num, line.strip()))
```

</blockquote></details>
<details>
<summary>src/ti4/core/technology_cards/abilities_integration.py (1)</summary><blockquote>

`219-229`: **LGTM: fail‑closed guard restored**

Condition checks now run even with an empty context via `context or {}`. This closes the earlier bypass.

</blockquote></details>

</blockquote></details>

<details>
<summary>🧹 Nitpick comments (5)</summary><blockquote>

<details>
<summary>templates/new_ability_template.py (2)</summary><blockquote>

`131-136`: **Use logging instead of print for library warnings**

Replace print with a module logger so callers can control verbosity.

```diff
-        except NotImplementedError:
-            # Log the unimplemented condition for development
-            print(f"Warning: Unimplemented condition in {self.specification.name}")
-            return False
+        except NotImplementedError:
+            logger = logging.getLogger(__name__)
+            logger.warning("Unimplemented condition in %s", self.specification.name)
+            return False
```

Add the import once:
```python
# at top of file
import logging
```

---

`101-103`: **Tighten context typing for clarity**

Annotate context as dict[str, Any] to document expected usage and aid tooling.

```diff
-        self, ability_index: int = 0, context: Optional[dict] = None
+        self, ability_index: int = 0, context: Optional[dict[str, Any]] = None
```
```diff
-        self, ability_index: int = 0, context: Optional[dict] = None
+        self, ability_index: int = 0, context: Optional[dict[str, Any]] = None
```

Add Any to imports:
```python
from typing import Optional, Any
```


Also applies to: 139-141

</blockquote></details>
<details>
<summary>src/ti4/core/technology_cards/abilities_integration.py (3)</summary><blockquote>

`246-249`: **Tighten condition parameter typing**

Use Sequence[AbilityCondition] to improve type safety without constraining callers.

```diff
-def validate_ability_conditions(conditions: list[Any], context: dict[str, Any]) -> bool:
+def validate_ability_conditions(
+    conditions: Sequence["AbilityCondition"], context: dict[str, Any]
+) -> bool:
```

Add import once:
```python
from typing import Any, Callable, Optional, Sequence
```

---

`210-214`: **Narrow `conditions` type on EnhancedAbility**

Reflect actual enum type rather than Any for better linting and IDE help.

```diff
-    def __init__(self, conditions: Optional[list[Any]] = None, **kwargs: Any) -> None:
+    def __init__(self, conditions: Optional[Sequence["AbilityCondition"]] = None, **kwargs: Any) -> None:
```

---

`32-46`: **Optional: hoist trigger map to a module constant**

Avoid rebuilding the mapping on every call; keeps function hot‑path lean.

Example:
```python
_TRIGGER_TO_TIMING = {
    AbilityTrigger.ACTION: TimingWindow.ACTION,
    # ...
}

def map_trigger_to_timing(trigger: AbilityTrigger) -> TimingWindow:
    if not isinstance(trigger, AbilityTrigger):
        raise TypeError(f"Expected AbilityTrigger enum, got {type(trigger)}")
    try:
        return _TRIGGER_TO_TIMING[trigger]
    except KeyError as e:
        raise ValueError(f"Cannot map trigger {trigger} to TimingWindow") from e
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

Reviewing files that changed from the base of the PR and between 9679b31f607952a1144101322a1de3f3974000ea and a13813b85f8a1d436bf92b26ad5a96a62dc2fd0c.

</details>

<details>
<summary>📒 Files selected for processing (5)</summary>

* `Makefile` (3 hunks)
* `pr33_review_complete.md` (1 hunks)
* `scripts/check_documentation_consistency.py` (1 hunks)
* `src/ti4/core/technology_cards/abilities_integration.py` (1 hunks)
* `templates/new_ability_template.py` (1 hunks)

</details>

<details>
<summary>🚧 Files skipped from review as they are similar to previous changes (1)</summary>

* Makefile

</details>

<details>
<summary>🧰 Additional context used</summary>

<details>
<summary>🧬 Code graph analysis (2)</summary>

<details>
<summary>templates/new_ability_template.py (6)</summary><blockquote>

<details>
<summary>src/ti4/core/constants.py (5)</summary>

* `AbilityCondition` (193-206)
* `AbilityEffectType` (175-190)
* `AbilityTrigger` (157-172)
* `Expansion` (147-154)
* `Technology` (96-128)

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
<summary>src/ti4/core/technology_cards/concrete/dark_energy_tap.py (3)</summary>

* `color` (40-42)
* `prerequisites` (45-51)
* `faction_restriction` (54-56)

</details>
<details>
<summary>src/ti4/core/technology_cards/abilities_integration.py (1)</summary>

* `validate_ability_conditions` (246-318)

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

</details><details>
<summary>🪛 markdownlint-cli2 (0.18.1)</summary>

<details>
<summary>pr33_review_complete.md</summary>

13-13: Emphasis used instead of a heading

(MD036, no-emphasis-as-heading)

---

95-95: Hard tabs
Column: 2

(MD010, no-hard-tabs)

---

96-96: Hard tabs
Column: 2

(MD010, no-hard-tabs)

---

98-98: Hard tabs
Column: 2

(MD010, no-hard-tabs)

---

99-99: Hard tabs
Column: 2

(MD010, no-hard-tabs)

---

109-109: Hard tabs
Column: 2

(MD010, no-hard-tabs)

---

110-110: Hard tabs
Column: 2

(MD010, no-hard-tabs)

---

112-112: Hard tabs
Column: 2

(MD010, no-hard-tabs)

---

113-113: Hard tabs
Column: 2

(MD010, no-hard-tabs)

---

757-757: Fenced code blocks should have a language specified

(MD040, fenced-code-language)

---

872-872: Fenced code blocks should have a language specified

(MD040, fenced-code-language)

---

891-891: Emphasis used instead of a heading

(MD036, no-emphasis-as-heading)

---

931-931: Fenced code blocks should have a language specified

(MD040, fenced-code-language)

---

999-999: Emphasis used instead of a heading

(MD036, no-emphasis-as-heading)

---

1006-1006: Fenced code blocks should have a language specified

(MD040, fenced-code-language)

---

1087-1087: Fenced code blocks should have a language specified

(MD040, fenced-code-language)

---

1158-1158: Fenced code blocks should have a language specified

(MD040, fenced-code-language)

---

1227-1227: Fenced code blocks should have a language specified

(MD040, fenced-code-language)

</details>

</details>

</details>

</details>

<!-- This is an auto-generated comment by CodeRabbit for review status -->

DETAILED COMMENTS:
----------------------------------------
Comment 1:
  File: templates/new_ability_template.py
  Line: 71
  Body: _⚠️ Potential issue_ | _🔴 Critical_

<details>
<summary>🧩 Analysis chain</summary>

**Fix constructor: wrong base signature; also persist spec on the instance**

PassiveTechnologyCard expects (technology_enum, name). Passing the spec object will break at runtime. Initialize with the enum and name, then store the spec for later methods.


Apply:

```diff
-        super().__init__(tech_spec)
+        super().__init__(Technology.YOUR_TECHNOLOGY_ENUM, "[USER_CONFIRMED_NAME]")
+        # Keep the confirmed specification accessible to methods below
+        self.specification = tech_spec
```

Verify ctor signatures in the codebase:

---

🏁 Script executed:

```shell
#!/bin/bash
# Show PassiveTechnologyCard and BaseTechnologyCard ctors to confirm expected args
rg -nP -C2 'class\s+PassiveTechnologyCard\b|def\s+__init__\s*\(' src | sed -n '1,140p'
rg -nP -C2 'class\s+BaseTechnologyCard\b|def\s+__init__\s*\(' src | sed -n '1,200p'
```

Length of output: 19968

---

🏁 Script executed:

```shell
#!/bin/bash
# Locate the template file
fd new_ability_template.py || find . -type f -name 'new_ability_template.py'

# Search for PassiveTechnologyCard and BaseTechnologyCard across the repo
rg -nP 'class\s+PassiveTechnologyCard' -C3 .
rg -nP 'class\s+BaseTechnologyCard' -C3 .
```

Length of output: 2926

---

🏁 Script executed:

```shell
#!/bin/bash
# Show lines 50-100 of new_ability_template.py
sed -n '50,100p' templates/new_ability_template.py

# Show BaseTechnologyCard __init__ signature
sed -n '1,200p' src/ti4/core/technology_cards/base/technology_card.py | sed -n '1,60p'

# Show PassiveTechnologyCard __init__ (if any)
sed -n '1,200p' src/ti4/core/technology_cards/base/passive_tech.py | sed -n '1,60p'
```

Length of output: 4510

---



</details>

**Incorrect `super().__init__` signature in constructor**
In `templates/new_ability_template.py` (line 71), `super().__init__` is called with a `TechnologySpecification` but `BaseTechnologyCard.__init__` requires a `Technology` enum and a `str`. Update to:

```diff
-        super().__init__(tech_spec)
+        super().__init__(Technology.YOUR_TECHNOLOGY_ENUM, "[USER_CONFIRMED_NAME]")
+        self._specification = tech_spec
```

<!-- suggestion_start -->

<details>
<summary>📝 Committable suggestion</summary>

> ‼️ **IMPORTANT**
> Carefully review the code before committing. Ensure that it accurately replaces the highlighted code, contains no missing lines, and has no issues with indentation. Thoroughly test & benchmark the code to ensure it meets the requirements.

```suggestion
        # Initialize base class with the Technology enum and name, then store the full spec
        super().__init__(Technology.YOUR_TECHNOLOGY_ENUM, "[USER_CONFIRMED_NAME]")
        self._specification = tech_spec
```

</details>

<!-- suggestion_end -->

<details>
<summary>🤖 Prompt for AI Agents</summary>

```
In templates/new_ability_template.py around line 71, the constructor calls
super().__init__(tech_spec) but BaseTechnologyCard.__init__ expects a Technology
enum and a str; change the call to pass the two required fields from tech_spec
(e.g., super().__init__(tech_spec.technology, tech_spec.name) or the equivalent
fields on TechnologySpecification such as .technology and
.name/.short_description) so the first argument is the Technology enum and the
second is the descriptive string.
```

</details>

<!-- fingerprinting:phantom:poseidon:chinchilla -->

<!-- This is an auto-generated comment by CodeRabbit -->

Comment 2:
  File: templates/new_ability_template.py
  Line: 126
  Body: _⚠️ Potential issue_ | _🔴 Critical_

**Avoid relying on an undefined `self.specification` unless you set it**

As written, accessing `self.specification.abilities` will fail unless you assign it in __init__ (see prior comment) or fetch from the registry on demand. Choose one and keep it consistent.


Option A (instance-held spec): keep using `self.specification` after assigning it in __init__.
Option B (registry): resolve spec at use sites:
```python
from ti4.core.technology_cards.specifications import TechnologySpecificationRegistry
spec = TechnologySpecificationRegistry().get_specification(Technology.YOUR_TECHNOLOGY_ENUM)
```

<details>
<summary>🤖 Prompt for AI Agents</summary>

```
In templates/new_ability_template.py around lines 120 to 126, the code accesses
self.specification.abilities but self.specification may be undefined; either
initialize and assign self.specification in __init__ (Option A) so all methods
can safely use it, or remove the instance dependency and fetch the spec at each
use site (Option B) via TechnologySpecificationRegistry().get_specification(...)
before accessing .abilities; implement one consistent approach and add a clear
error path (raise or return False) if the spec lookup fails.
```

</details>

<!-- fingerprinting:phantom:poseidon:chinchilla -->

<!-- This is an auto-generated comment by CodeRabbit -->

============================================================

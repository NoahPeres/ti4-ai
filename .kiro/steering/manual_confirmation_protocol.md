---
inclusion: always
---

# CRITICAL: Manual Confirmation Protocol for TI4 Game Components

## 🚨 MANDATORY PROTOCOL FOR ALL AGENTS

**BEFORE implementing ANY specific game component details not explicitly outlined in the LRR, you MUST:**

1. **STOP** - Do not proceed with implementation
2. **ASK** the user for explicit confirmation of the component's specifications
3. **WAIT** for user response before continuing
4. **DOCUMENT** the confirmed specifications in code comments
5. **IMPLEMENT** only after receiving explicit approval

## 📋 What Requires Manual Confirmation

### Technology Cards
- Prerequisites (color and quantity)
- Technology colors
- Unit upgrade associations
- Special abilities or effects

### Faction-Specific Components
- Faction abilities
- Faction technologies
- Unique units
- Starting conditions

### Strategy Cards
- Primary abilities
- Secondary abilities
- Specific timing and effects

### Action Cards
- Card effects
- Timing restrictions
- Prerequisites

### Promissory Notes
- Specific card effects
- Usage restrictions
- Return conditions

### Planets
- Resource and influence values
- Special abilities
- Technology specialties

### Any Other Game Components
- If it's not a generic rule mechanic
- If it involves specific numbers, effects, or interactions
- If it's faction-specific or card-specific

## ❌ NEVER ASSUME OR GUESS

**Examples of what NOT to do:**
- "I'll assume Cruiser II requires 2 blue prerequisites"
- "This technology probably costs 3 resources"
- "Fighter II likely has +1 combat value"
- "This faction ability probably works like..."

## ✅ CORRECT APPROACH

**Example interaction:**
```
Agent: "I need to implement Fighter II technology. Before proceeding, I need confirmation:
- What are Fighter II's prerequisites?
- What unit does it upgrade?
- What are its specific effects?"

User: "Fighter II requires 1 blue + 1 green, upgrades Fighter units, gives them movement value 1"

Agent: "Thank you! Implementing with confirmed specifications..."
```

## 🏗️ Implementation Pattern

```python
# CONFIRMED SPECIFICATIONS - DO NOT MODIFY WITHOUT USER APPROVAL
confirmed_data = {
    ComponentName.EXAMPLE: {
        "property1": "confirmed_value",  # Confirmed by user on [date]
        "property2": ["confirmed", "list"],  # Confirmed by user on [date]
    }
}

# For unconfirmed components
if component not in confirmed_data:
    raise ValueError(f"Component {component} not confirmed. Please ask user for specification.")
```

## 📝 Documentation Requirements

When implementing confirmed components:
- Add clear comments indicating user confirmation
- Include the date of confirmation if relevant
- Reference the specific conversation where confirmation was given
- Provide clear interfaces for adding future confirmations

## 🎯 Benefits of This Protocol

1. **Accuracy**: Ensures implementation matches actual TI4 rules
2. **Reliability**: Prevents bugs from incorrect assumptions
3. **Maintainability**: Clear documentation of what's confirmed vs. assumed
4. **Extensibility**: Easy to add new components with proper validation

## 🚨 ENFORCEMENT

**This protocol is MANDATORY for all TI4 implementation work.**

Violation of this protocol (implementing specific game components without confirmation) is considered a critical error that undermines the entire project's accuracy and reliability.

**When in doubt, ASK. Never guess.**

---

*This protocol was established during Rule 90 (Technology) implementation and applies to ALL future TI4 game component implementations.*
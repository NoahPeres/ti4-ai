---
inclusion: always
---

# TDD Refactor Phase Reminder

## CRITICAL: Always Explicitly Consider Refactoring

After each GREEN phase (making tests pass), you MUST explicitly consider the REFACTOR phase:

### Questions to Ask Every Time:
1. **Code Duplication**: Is there repeated logic that could be extracted?
2. **Error Handling**: Are there edge cases or error conditions not handled?
3. **Validation**: Should inputs be validated for robustness?
4. **Naming**: Are variable/method names clear and descriptive?
5. **Single Responsibility**: Is each class/method doing one thing well?
6. **Readability**: Would another developer easily understand this code?

### Decision Process:
- **If refactoring is needed**: Do it now while the context is fresh
- **If no refactoring needed**: Explicitly state why (e.g., "code is minimal and clear", "no duplication yet", "YAGNI applies")

### Common Early-Stage Refactoring Opportunities:
- Input validation and error handling
- Extracting magic numbers/strings to constants
- Breaking up complex methods
- Adding defensive programming checks

### Remember:
- The REFACTOR phase is where good design emerges
- Don't skip this step - it's as important as RED and GREEN
- Make an intentional decision every time, even if it's "no refactoring needed"

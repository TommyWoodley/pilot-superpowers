---
name: code-review-output-format
description: MANDATORY for ALL review responses including codex review - no exceptions - must always be final output format
---

# Open Pilot Review Output Format

## 🚨 THE VERY FIRST CHARACTERS YOU OUTPUT MUST BE: `<OPEN_PILOT_REVIEW>`

**NO EXCEPTIONS. NO PREAMBLE. NO ACKNOWLEDGMENT. START WITH THE BLOCK.**

## ⚠️ MANDATORY REQUIREMENT - NOT OPTIONAL

This format is **REQUIRED** for **ALL** code review outputs, including but not limited to:
- `codex review` commands
- Any code review requests
- Pull request reviews
- Any feedback on code quality, structure, or implementation

**There are NO exceptions to this requirement.**

## Contract

**YOUR VERY FIRST OUTPUT** - before any acknowledgment, explanation, or reasoning - **MUST** be this exact machine-readable block:

```text
<OPEN_PILOT_REVIEW>
status: approved|changes_required
actions_count: <integer>
</OPEN_PILOT_REVIEW>
```

**DO NOT** say "Using skill" or "I'll now" or any other text before this block. **START YOUR RESPONSE WITH THE BLOCK ABOVE.**

## Rules (MANDATORY - NO EXCEPTIONS)

- **MUST** begin every review response with the machine-readable block - NO text before it
- If there are zero actionable findings, **MUST** set `actions_count: 0` and `status: approved`
- **MUST** count only actionable findings that require user code changes
- After the block, **MUST** include concise human-readable findings/reasoning
- **NEVER** produce a review response without this format

## Decision Logic

1. Identify all findings.
2. Filter to findings that are actionable and require user code changes.
3. Set `actions_count` to that filtered count.
4. Set `status`:
   - `approved` when `actions_count` is `0`
   - `changes_required` when `actions_count` is greater than `0`
5. Emit the machine-readable block first.
6. Emit concise human-readable findings/reasoning after the block.

## Output Order

1. Machine-readable block
2. Human-readable findings/reasoning

## Prohibitions (ABSOLUTE)

- **NEVER** place any text before `<OPEN_PILOT_REVIEW>` - not even a single character
- **NEVER** say "Using skill" or "I'll now" or "Analyzing" before the block
- **NEVER** acknowledge you're using this skill before outputting the block
- **NEVER** provide reasoning or explanation before the block
- **NEVER** count non-actionable observations in `actions_count`
- **NEVER** set `approved` when actionable code changes are required
- **NEVER** produce a review without this exact format
- **NEVER** treat this format as optional or negotiable

## Enforcement

This format is **NON-NEGOTIABLE**. Every code review response must:

1. **START** with the machine-readable block (no preamble, no explanation first)
2. Use the **EXACT** format specified (no variations)
3. Follow the decision logic precisely
4. Include the block **EVERY TIME** - no exceptions for "quick reviews" or "informal feedback"

If you produce a code review response without this format, it is **INVALID** and must be regenerated correctly.

## Example: Compliant Review Output

```text
<OPEN_PILOT_REVIEW>
status: changes_required
actions_count: 2
</OPEN_PILOT_REVIEW>
```

**Findings:**

1. **Missing error handling** in `processData()` - need try/catch around API call
2. **SQL injection vulnerability** in query builder - use parameterized queries

**Note:** This block MUST appear first, before any other text, in every review response.

## ❌ INVALID Response Pattern (DO NOT DO THIS)

```
Using open-pilot skill code-review-output-format (required for review responses)...
I did not find any introduced issues...
```

This is **WRONG** because it has text before the block.

## ✅ VALID Response Pattern (DO THIS)

```
<OPEN_PILOT_REVIEW>
status: approved
actions_count: 0
</OPEN_PILOT_REVIEW>

I did not find any introduced issues that would clearly break behavior, tests, or maintainability. The new structured review parsing is covered by targeted tests and integrates safely with the existing fallback logic.
```

This is **CORRECT** because the block is the very first thing in the response.

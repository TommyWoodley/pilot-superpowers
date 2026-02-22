---
name: code-review-output-format
description: Use when producing ALL review responses
---

# Open Pilot Review Output Format

## Contract
Always return review output with this exact machine-readable block first:

```text
<OPEN_PILOT_REVIEW>
status: approved|changes_required
actions_count: <integer>
</OPEN_PILOT_REVIEW>
```

## Rules

- If there are zero actionable findings, set `actions_count: 0` and `status: approved`.
- Count only actionable findings that require user code changes.
- After the block, include concise human-readable findings/reasoning.

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

## Prohibitions

- Do not place any text before `<OPEN_PILOT_REVIEW>`.
- Do not count non-actionable observations in `actions_count`.
- Do not set `approved` when actionable code changes are required.

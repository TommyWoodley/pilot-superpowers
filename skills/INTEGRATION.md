# Skills Integration Guide

This document describes how the pilot-superpowers skills work together to create a complete, safe development workflow.

## The Complete Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    FEATURE DEVELOPMENT                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│           TEST-DRIVEN DEVELOPMENT (TDD) CYCLE               │
│                                                             │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐             │
│  │   RED    │ →   │  GREEN   │ →   │ REFACTOR │             │
│  │ Failing  │     │ Passing  │     │ Clean up │             │
│  │  Test    │     │   Code   │     │   Code   │             │
│  └──────────┘     └──────────┘     └──────────┘             │
│                                           ↓                 │
│                                    ┌──────────┐             │
│                                    │  COMMIT  │             │
│                                    │ Changes  │             │
│                                    └──────────┘             │
│                                           ↓                 │
│                         (Repeat for next behavior)          │
└─────────────────────────────────────────────────────────────┘
                            ↓
                  (All TDD cycles complete)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│         VERIFICATION-BEFORE-COMPLETION                      │
│                                                             │
│  ┌──────────────────────────────────────────┐               │
│  │ Run full test suite                      │               │
│  │ Run build                                │               │
│  │ Run linter                               │               │
│  │ Check requirements against plan          │               │
│  └──────────────────────────────────────────┘               │
│                     ↓                                       │
│              All checks pass?                               │
│                     ↓                                       │
│         <DEVELOPMENT_WORK_COMPLETE>                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    (Immediately after)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              SAFE-PILOT-COMMITTING                           │
│                                                              │
│  ┌──────────────────────────────────────────┐              │
│  │ git status, git diff                      │              │
│  │ Security scan (secrets, logs, etc.)       │              │
│  │ Group changes into logical commits        │              │
│  │ Generate conventional commit messages     │              │
│  └──────────────────────────────────────────┘              │
│                     ↓                                        │
│         Output structured YAML recommendation                │
│                     ↓                                        │
│              User approval required                          │
│                     ↓                                        │
│            Execute git add + git commit                      │
└─────────────────────────────────────────────────────────────┘
```

## Skill Responsibilities

### 1. Test-Driven Development (TDD)
**Purpose:** Ensure code is developed with tests first

**Triggers:**
- Any feature implementation
- Any bug fix
- Any refactoring
- Any behavior change

**Outputs:**
- Tested, working code
- Regression tests that prove the fix
- **Commits after each RED-GREEN-REFACTOR cycle**

**Integration points:**
- **Invokes safe-pilot-committing after each TDD cycle**
- Invokes verification-before-completion when all cycles are done

**Tags:**
- `<TEST_DRIVEN_DEVELOPMENT_START>`
- `<TEST_DRIVEN_DEVELOPMENT_END>`

---

### 2. Verification-Before-Completion
**Purpose:** Prove the entire system works before claiming completion

**Triggers:**
- After TDD workflow completes
- Before any completion claim
- Before committing (if not already committed in TDD)
- Before creating PRs

**Outputs:**
- Evidence that all tests pass
- Evidence that build succeeds
- Evidence that requirements are met
- `<DEVELOPMENT_WORK_COMPLETE>` tag

**Integration points:**
- **Immediately invokes safe-pilot-committing after successful verification**

**Tags:**
- `<VERIFICATION_BEFORE_COMPLETION_START>`
- `<VERIFICATION_BEFORE_COMPLETION_END>`
- `<DEVELOPMENT_WORK_COMPLETE>`

---

### 3. Safe-Pilot-Committing
**Purpose:** Ensure all commits are secure, meaningful, and properly formatted

**Triggers:**
- After each TDD cycle (RED-GREEN-REFACTOR)
- After verification-before-completion succeeds
- Any time agent wants to commit changes
- **MANDATORY** before any `git add` or `git commit`

**Outputs:**
- Structured YAML recommendation with:
  - Security scan results
  - File lists per commit
  - Conventional commit messages
  - Breaking change flags
  - Issue references

**Integration points:**
- Called by TDD after each cycle
- Called by verification-before-completion after success

**Tags:**
- `<SAFE_PILOT_COMMITTING_START>`
- `<COMMIT_RECOMMENDATION>...</COMMIT_RECOMMENDATION>`
- `<SAFE_PILOT_COMMITTING_END>`

---

## Commit Patterns

### During TDD (Frequent, Small Commits)

Each RED-GREEN-REFACTOR cycle produces a commit:

```bash
$ git log --oneline
a1b2c3d test(auth): add password reset token expiry tests
e4f5g6h feat(auth): implement token expiry for password reset
i7j8k9l refactor(auth): extract token generation logic
m0n1o2p test(auth): add token generation tests
q3r4s5t feat(auth): add password reset token generation
```

**Characteristics:**
- Small, focused changes
- Clear progression of feature development
- Easy to review
- Easy to revert if needed
- Tests and implementation together

### After Verification (Optional Cleanup Commit)

If there are any final adjustments after full system verification:

```bash
$ git log --oneline -1
u6v7w8x chore(auth): update password reset documentation
```

**Characteristics:**
- Documentation updates
- Minor polish
- Integration fixes
- Usually not needed if TDD was thorough

---

## Example: Complete Feature Development

### Scenario: Add password strength validation

**1. TDD Cycle 1 - Weak Password Rejection**

```
RED → GREEN → REFACTOR → COMMIT
```

**Commit:**
```yaml
type: feat
scope: auth
subject: reject weak passwords
files:
  - src/auth/validation.ts
  - tests/auth/validation.test.ts
```

**2. TDD Cycle 2 - Length Requirement**

```
RED → GREEN → REFACTOR → COMMIT
```

**Commit:**
```yaml
type: feat
scope: auth
subject: require minimum 8 character passwords
files:
  - src/auth/validation.ts
  - tests/auth/validation.test.ts
```

**3. TDD Cycle 3 - Special Character Requirement**

```
RED → GREEN → REFACTOR → COMMIT
```

**Commit:**
```yaml
type: feat
scope: auth
subject: require special characters in passwords
files:
  - src/auth/validation.ts
  - tests/auth/validation.test.ts
```

**4. Verification**

```
<VERIFICATION_BEFORE_COMPLETION_START>
[Run full test suite: PASS]
[Run build: PASS]
[Check requirements: MET]
<VERIFICATION_BEFORE_COMPLETION_END>

<DEVELOPMENT_WORK_COMPLETE>
```

**5. Final Commit (if needed)**

Safe-pilot-committing scans the workspace:
- Finds documentation updates
- Produces commit recommendation

```yaml
type: docs
scope: auth
subject: add password validation requirements to README
files:
  - README.md
```

**Final git log:**
```bash
$ git log --oneline -4
x9y0z1a docs(auth): add password validation requirements to README
u6v7w8x feat(auth): require special characters in passwords
q3r4s5t feat(auth): require minimum 8 character passwords
m0n1o2p feat(auth): reject weak passwords
```

---

## Security Guarantees

Safe-pilot-committing provides these guarantees at every commit point:

✅ **No API keys or secrets committed**
✅ **No log files or debug output committed**
✅ **No build artifacts committed**
✅ **No environment files with credentials committed**
✅ **All commits follow conventional format**
✅ **All commits are atomic and focused**
✅ **All commits have clear, descriptive messages**

If any security issue is found, the commit is **blocked** and the user is informed.

---

## Benefits of This Integration

### 1. Safety
- Security scanning at every commit point
- Verification before completion claims
- No secrets ever committed
- No untested code shipped

### 2. Quality
- TDD ensures code correctness
- Frequent commits create checkpoints
- Small commits are easy to review
- Clear history shows development progression

### 3. Traceability
- Each feature broken into logical commits
- Git history shows test-first development
- Commit messages explain the "why"
- Easy to understand what changed and when

### 4. Confidence
- Tests prove behavior
- Verification proves integration
- Security scan proves safety
- User approval proves intent

### 5. Efficiency
- Automated security scanning (no manual review needed)
- Structured output (easy to parse and automate)
- Clear workflows (no decision fatigue)
- Immediate feedback (catch issues early)

---

## Common Scenarios

### Scenario 1: Single TDD Cycle

```
User: "Fix the bug where empty emails are accepted"

TDD:
  RED → Test for empty email rejection
  GREEN → Implement validation
  REFACTOR → Clean up validation logic
  COMMIT → "fix(forms): reject empty email input"

Verification:
  Run tests: PASS
  Run build: PASS
  <DEVELOPMENT_WORK_COMPLETE>

Safe-Pilot-Committing:
  Scan: PASS (no uncommitted changes, already committed during TDD)
```

### Scenario 2: Multi-Cycle Feature

```
User: "Add user authentication"

TDD Cycle 1:
  RED → Test for login endpoint
  GREEN → Implement login
  REFACTOR → Extract auth logic
  COMMIT → "feat(auth): add login endpoint"

TDD Cycle 2:
  RED → Test for token generation
  GREEN → Implement JWT tokens
  REFACTOR → Extract token utils
  COMMIT → "feat(auth): generate JWT tokens"

TDD Cycle 3:
  RED → Test for token validation
  GREEN → Implement validation middleware
  REFACTOR → Clean up middleware
  COMMIT → "feat(auth): add token validation middleware"

Verification:
  Run tests: PASS (all auth tests)
  Run build: PASS
  Check requirements: MET
  <DEVELOPMENT_WORK_COMPLETE>

Safe-Pilot-Committing:
  Scan: PASS (no uncommitted changes)
```

### Scenario 3: Security Issue Found

```
User: "Add API integration for payments"

TDD Cycle 1:
  RED → Test for API call
  GREEN → Implement API call
  REFACTOR → Extract API client
  COMMIT → (about to commit)

Safe-Pilot-Committing:
  Scan: FAIL
  Issues found: 1
  - API key in src/payment/client.ts (line 5)
  
  <COMMIT_RECOMMENDATION>
  status: blocked
  security_scan: fail
  issues_found: 1
  commits_proposed: 0
  commits: []
  </COMMIT_RECOMMENDATION>

Agent: "BLOCKED - API key detected. Please move to environment variable."

User: [fixes issue]

TDD Cycle 1 (retry):
  COMMIT → "feat(payment): add payment API client"
  
Safe-Pilot-Committing:
  Scan: PASS
  
  <COMMIT_RECOMMENDATION>
  status: safe
  ...
  </COMMIT_RECOMMENDATION>
```

---

## Integration Checklist

When implementing a feature, ensure:

- [ ] TDD skill invoked before writing implementation
- [ ] Each TDD cycle produces a commit via safe-pilot-committing
- [ ] No TDD cycle skips the commit step
- [ ] All commits pass security scanning
- [ ] Verification-before-completion invoked after all TDD cycles
- [ ] Verification produces evidence (not assumptions)
- [ ] Final commit (if any) also scanned for security
- [ ] All machine-readable tags are present in output

## Related Skills

- **brainstorming** - Use before TDD to clarify requirements
- **writing-plans** - Use to break down large features into TDD cycles
- **executing-plans** - Use to systematically work through planned TDD cycles
- **finishing-a-development-branch** - Use after all work verified and committed

---

## Machine-Readable Output

All skills produce machine-readable tags that can be parsed by tooling:

**TDD:**
```
<TEST_DRIVEN_DEVELOPMENT_START>
[TDD work happens]
<TEST_DRIVEN_DEVELOPMENT_END>
```

**Verification:**
```
<VERIFICATION_BEFORE_COMPLETION_START>
[Verification evidence]
<VERIFICATION_BEFORE_COMPLETION_END>
<DEVELOPMENT_WORK_COMPLETE>
```

**Committing:**
```
<SAFE_PILOT_COMMITTING_START>
<COMMIT_RECOMMENDATION>
[YAML data]
</COMMIT_RECOMMENDATION>
[Analysis]
<SAFE_PILOT_COMMITTING_END>
```

These tags enable:
- Automated workflow tracking
- Quality gates in CI/CD
- Audit trails
- Integration with external tools
- Metrics and analytics

---

## Summary

The three skills work together to provide:

1. **TDD** - Ensures code correctness through test-first development
2. **Verification** - Proves system-level integration works
3. **Safe-Pilot-Committing** - Guarantees security and quality of every commit

Together, they create a workflow that is:
- **Safe** (no secrets, verified behavior)
- **Traceable** (clear history, logical commits)
- **Efficient** (automated checks, structured output)
- **Reliable** (evidence-based, not assumption-based)

The integration is **mandatory** and **automatic** - the agent will invoke these skills at the appropriate times to ensure quality and safety.

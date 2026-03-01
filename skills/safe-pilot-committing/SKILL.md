---
name: safe-pilot-committing
description: Use whenever the agent wants to commit changes - scans all changes for secrets/logs/unwanted files, ensures commits are small and meaningful, produces file list and conventional commit messages; MANDATORY before any git commit or add operation
---

# Safe Pilot Committing

## Overview

Committing without scanning for secrets is a security incident waiting to happen.

**Core principle:** Scan before staging, always.

**Output requirement:** All commit recommendations MUST use the structured YAML format (see "MANDATORY OUTPUT FORMAT" section) for machine parseability.

## Machine-Readable Session Tags

For external tooling, safe-pilot-committing sessions MUST be explicitly delimited with these exact tags:

- Start tag: `<SAFE_PILOT_COMMITTING_START>`
- End tag: `<SAFE_PILOT_COMMITTING_END>`

Rules:
- Emit `<SAFE_PILOT_COMMITTING_START>` in the first safe-pilot-committing response before change analysis.
- Emit `<SAFE_PILOT_COMMITTING_END>` in the final safe-pilot-committing response after producing commit recommendation.
- Put each tag on its own line with no extra characters on that line.
- Emit each tag exactly once per committing session.

## 🚨 MANDATORY OUTPUT FORMAT

**After the `<SAFE_PILOT_COMMITTING_START>` tag and completing the security scan, you MUST output this structured format:**

```yaml
<COMMIT_RECOMMENDATION>
status: safe|blocked
security_scan: pass|fail
issues_found: <integer>
commits_proposed: <integer>

commits:
  - id: 1
    type: <feat|fix|docs|style|refactor|perf|test|chore|ci|build>
    scope: <scope or empty>
    subject: <subject line>
    body: |
      <body text>
    files:
      - path/to/file1.js
      - path/to/file2.js
    breaking: <true|false>
    closes: <issue numbers or empty>
</COMMIT_RECOMMENDATION>
```

**Rules:**
- MUST output the structured block after scanning and before human-readable analysis
- `status`: `safe` if no security issues; `blocked` if secrets/logs/unwanted files found
- `security_scan`: `pass` if clean; `fail` if issues found
- `issues_found`: Count of security issues (secrets, logs, unwanted files)
- `commits_proposed`: Number of logical commits recommended
- Each commit MUST include: `id`, `type`, `subject`, `files` list
- `scope`, `body`, `breaking`, `closes` are optional but recommended
- If `status: blocked`, include empty `commits: []` and explain issues in human-readable section

**Example: Safe commit (single)**
```yaml
<COMMIT_RECOMMENDATION>
status: safe
security_scan: pass
issues_found: 0
commits_proposed: 1

commits:
  - id: 1
    type: feat
    scope: auth
    subject: implement JWT-based authentication
    body: |
      Add login endpoint and token validation middleware.
      Tokens expire after 24 hours and include user role.
    files:
      - src/auth/login.js
      - src/middleware/validateToken.js
      - tests/auth.test.js
    breaking: false
    closes: "#234"
</COMMIT_RECOMMENDATION>
```

**Example: Multiple commits**
```yaml
<COMMIT_RECOMMENDATION>
status: safe
security_scan: pass
issues_found: 0
commits_proposed: 2

commits:
  - id: 1
    type: feat
    scope: parser
    subject: add XML parsing support
    body: |
      Implement XML parser with error handling.
    files:
      - src/parser/xml.js
      - src/parser/index.js
    breaking: false
    closes: ""
  - id: 2
    type: test
    scope: parser
    subject: add tests for XML parser
    body: |
      Add comprehensive test suite for XML parsing.
    files:
      - tests/parser/xml.test.js
    breaking: false
    closes: ""
</COMMIT_RECOMMENDATION>
```

**Example: Blocked (security issues)**
```yaml
<COMMIT_RECOMMENDATION>
status: blocked
security_scan: fail
issues_found: 2
commits_proposed: 0

commits: []
</COMMIT_RECOMMENDATION>

**SECURITY ISSUES FOUND:**
1. API key detected in `src/config.js` (line 23): `AKIA...`
2. Log file included: `debug.log` (should be gitignored)

**ACTION REQUIRED:**
- Remove API key from source code, use environment variables
- Add `debug.log` to `.gitignore`
- Run security scan again after fixes
```

## The Iron Law

```
NO COMMITS WITHOUT SECURITY SCAN
```

If you haven't scanned the full diff for secrets, log files, and unwanted artifacts, you cannot propose a commit.

## The Gate Function

```
BEFORE proposing any commit:

1. RUN: git status to see all changes
2. RUN: git diff to see full changes
3. SCAN: Every changed file for security issues
4. VERIFY: No secrets, logs, or unwanted files
5. GROUP: Related changes into logical commit
6. COMPOSE: Conventional commit message
7. ONLY THEN: Propose the commit
```

## Security Scan Checklist

**MUST scan for:**

### Secrets and Credentials
- [ ] API keys (patterns: `AKIA`, `AIza`, `sk_live_`, `pk_live_`, `ghp_`, `gho_`)
- [ ] Passwords (variable names: `password`, `passwd`, `pwd`)
- [ ] Tokens (patterns: `token`, `auth`, `bearer`, JWT format)
- [ ] Private keys (`-----BEGIN PRIVATE KEY-----`, `.pem`, `.key` files)
- [ ] Connection strings (URLs with credentials like `mongodb://user:pass@`)
- [ ] Secret keys (variable names: `secret`, `SECRET_KEY`, `API_SECRET`)
- [ ] Certificates (`.crt`, `.cer` files unless intentional)
- [ ] Environment variable exposures (`.env` files)

### Unwanted Files
- [ ] Log files (`.log`, `*.logs`, log directories)
- [ ] Debug files (`debug.log`, `*.debug`)
- [ ] Compiled artifacts (`*.pyc`, `*.class`, `node_modules/`, `target/`, `build/`)
- [ ] Temporary files (`*.tmp`, `*.swp`, `.DS_Store`)
- [ ] IDE files (`.idea/`, `.vscode/settings.json`, `*.iml`)
- [ ] Large binary files (check size)
- [ ] Backup files (`*.bak`, `*~`)
- [ ] Test output files

### Code Quality Issues
- [ ] Commented-out debug code with secrets
- [ ] Hardcoded credentials in code
- [ ] TODO comments with sensitive info
- [ ] Personal paths or usernames

## Red Flags - STOP IMMEDIATELY

If you find ANY of these, **DO NOT COMMIT**:

- API keys or tokens in plain text
- Password strings (not hashes)
- Private key material
- `.env` files with secrets
- Log files
- Debug output with sensitive data
- Personal identifying information
- Large binary files without justification

**Action:** Inform user, suggest fixes, DO NOT proceed with commit.

## Commit Size Guidelines

**Good commits are small and atomic:**

```
✅ Single feature or fix
✅ Related changes only
✅ Can be reverted cleanly
✅ Reviewable in < 10 minutes

❌ Multiple unrelated changes
❌ Mix of features and fixes
❌ Would break if partially reverted
❌ Too large to review effectively
```

**When to split commits:**
- Feature + refactor = 2 commits
- Multiple bug fixes = separate commits
- Feature + tests = can be 1 commit (related)
- Config + code = evaluate (usually split)

## Conventional Commit Format

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code change that neither fixes bug nor adds feature
- `perf`: Performance improvement
- `test`: Adding/modifying tests
- `chore`: Build process, dependencies, tooling
- `ci`: CI configuration
- `build`: Build system changes

**Scope (optional):**
- Component or module name
- Examples: `auth`, `api`, `parser`, `ui`

**Subject:**
- Imperative mood: "add" not "adds" or "added"
- No capitalization of first letter
- No period at end
- Max 50 characters

**Body (optional but recommended):**
- Explain what and why, not how
- Wrap at 72 characters
- Separate from subject with blank line

**Footer (optional):**
- Breaking changes: `BREAKING CHANGE:`
- Issue references: `Closes #123`, `Fixes #456`

## Examples

**Good commit message:**
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware.
Tokens expire after 24 hours and include user role.

Closes #234
```

**Good commit message (small fix):**
```
fix(parser): handle empty input gracefully

Return empty result instead of throwing when input is empty string.
```

**Good commit message (refactor):**
```
refactor(utils): extract date formatting logic

Move date formatting from 3 components into shared utility.
No behavior change, improves maintainability.
```

**Bad commit messages:**
```
❌ "Updated files"           (too vague)
❌ "Fixed bug"               (which bug?)
❌ "WIP"                     (not ready)
❌ "asdfasdf"                (meaningless)
❌ "Fixed typo in README.md" (should be "docs: fix typo in README")
```

## Workflow

**Step 1: Examine changes**
```bash
git status
git diff
```

**Step 2: Security scan**
- Review EVERY changed line
- Check against security checklist
- If issues found: STOP and inform user

**Step 3: Group changes**
- Identify logical units
- Plan separate commits if needed
- Ensure each commit is atomic

**Step 4: Compose message**
- Choose appropriate type
- Write clear subject
- Add body if needed
- Reference issues

**Step 5: Present recommendation**

**MUST output the structured YAML block (see "MANDATORY OUTPUT FORMAT" above) followed by human-readable explanation.**

The structured block provides machine-parseable data:
- Security scan status
- List of files per commit
- Commit type, scope, subject
- Issue references

After the structured block, provide human-readable context:
- Explanation of grouping decisions
- Why commits were split (if applicable)
- Any notable patterns in changes

**Step 6: User approval**
- Wait for explicit user approval
- Do NOT execute git commands without approval

## Common Patterns

**Feature with tests (single commit):**
```
feat(parser): add XML parsing support

Implement XML parser with error handling.
Add comprehensive test suite.
```

**Bug fix (single commit):**
```
fix(api): correct timezone handling

Convert all timestamps to UTC before storage.
Fixes incorrect date display in reports.

Fixes #456
```

**Refactor (split commits):**
```
Commit 1:
refactor(utils): extract common validation logic

Commit 2:
refactor(api): use shared validation utilities
```

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Just this once" | Every breach starts with one exception |
| "It's just a test file" | Test files with secrets are leaked too |
| "I'll fix it later" | Later never comes, secrets get exposed |
| "It's a private repo" | Private repos get made public |
| "Quick commit" | Speed doesn't excuse security |
| "The file is gitignored" | Check actual status, not assumptions |

## Final Checklist

Before proposing commit:
- [ ] Full git diff reviewed
- [ ] Security scan completed (no secrets, logs, unwanted files)
- [ ] Commit is atomic and focused
- [ ] Conventional commit format used
- [ ] Message is clear and descriptive
- [ ] Related issue referenced (if applicable)
- [ ] **Structured YAML block output (MANDATORY)**
- [ ] User approval required before execution

## When To Apply

**ALWAYS before:**
- ANY `git add` command
- ANY `git commit` command
- ANY proposal to commit changes
- Moving work to staging area
- Creating pull requests (implies commits)

**Rule applies even when:**
- User asks to "quickly commit"
- Changes seem small
- You're confident there are no issues
- You've done this many times before

## The Bottom Line

**No shortcuts for security scanning.**

Scan the changes. Verify the safety. THEN propose the commit.

This is non-negotiable.

## Error Recovery

**If secrets are found after commit:**
```
1. STOP immediately
2. DO NOT push
3. Inform user
4. Suggest: git reset --soft HEAD~1
5. Remove secrets
6. Re-scan
7. Commit safely
```

**If secrets are pushed:**
```
1. CRITICAL: Secrets are compromised
2. Inform user immediately
3. Secrets must be rotated
4. Consider: git history rewrite (complex)
5. Force push if absolutely necessary (dangerous)
6. Better: Rotate secrets and move forward
```

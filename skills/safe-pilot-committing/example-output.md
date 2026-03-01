# Example Outputs for Safe Pilot Committing

This document shows example outputs in the structured format that the skill will produce.

## Example 1: Single Safe Commit

```
<SAFE_PILOT_COMMITTING_START>

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
      
      This implements the authentication requirements from the spec.
    files:
      - src/auth/login.js
      - src/auth/jwt.js
      - src/middleware/validateToken.js
      - tests/auth/login.test.js
      - tests/auth/jwt.test.js
    breaking: false
    closes: "#234"
</COMMIT_RECOMMENDATION>

**Analysis:**
All changes are related to the authentication feature. Files include implementation and tests together, which is appropriate as they're part of the same logical unit. Security scan found no hardcoded secrets or unwanted files.

<SAFE_PILOT_COMMITTING_END>
```

---

## Example 2: Multiple Commits (Split by Concern)

```
<SAFE_PILOT_COMMITTING_START>

<COMMIT_RECOMMENDATION>
status: safe
security_scan: pass
issues_found: 0
commits_proposed: 2

commits:
  - id: 1
    type: refactor
    scope: database
    subject: extract connection pooling logic
    body: |
      Move database connection pooling into separate module.
      This makes the code more maintainable and testable.
    files:
      - src/database/connection.js
      - src/database/pool.js
    breaking: false
    closes: ""
  - id: 2
    type: feat
    scope: database
    subject: add connection retry logic
    body: |
      Implement exponential backoff for failed connections.
      Retry up to 3 times with increasing delays.
    files:
      - src/database/retry.js
      - src/database/connection.js
      - tests/database/retry.test.js
    breaking: false
    closes: "#189"
</COMMIT_RECOMMENDATION>

**Analysis:**
Changes split into two logical commits:
1. Refactor to extract existing logic (no behavior change)
2. New feature that adds retry capability (new behavior)

This separation makes it easier to review and potentially revert if needed. Security scan found no issues.

<SAFE_PILOT_COMMITTING_END>
```

---

## Example 3: Blocked Due to Security Issues

```
<SAFE_PILOT_COMMITTING_START>

<COMMIT_RECOMMENDATION>
status: blocked
security_scan: fail
issues_found: 3
commits_proposed: 0

commits: []
</COMMIT_RECOMMENDATION>

**SECURITY ISSUES FOUND - COMMIT BLOCKED:**

1. **API Key in source code** 
   - File: `src/services/stripe.js`
   - Line: 12
   - Pattern: `sk_live_51H...` (Stripe live secret key)
   - **Action:** Remove from source, use environment variable

2. **Log file included**
   - File: `debug.log`
   - Size: 2.3 MB
   - **Action:** Add to `.gitignore`, remove from staging

3. **Environment file with credentials**
   - File: `.env`
   - Contains: Database password, API keys
   - **Action:** Add `.env` to `.gitignore`, use `.env.example` template instead

**NEXT STEPS:**
1. Fix all security issues above
2. Run `git reset` to unstage problematic files
3. Add files to `.gitignore` as needed
4. Re-run commit process after fixes

**DO NOT PROCEED WITH COMMIT UNTIL THESE ISSUES ARE RESOLVED.**

<SAFE_PILOT_COMMITTING_END>
```

---

## Example 4: Feature with Breaking Change

```
<SAFE_PILOT_COMMITTING_START>

<COMMIT_RECOMMENDATION>
status: safe
security_scan: pass
issues_found: 0
commits_proposed: 1

commits:
  - id: 1
    type: feat
    scope: api
    subject: change user endpoint to return UUID instead of integer ID
    body: |
      BREAKING CHANGE: User ID field now returns UUID string instead of integer.
      
      This improves security by making IDs non-enumerable.
      Migration guide added to docs.
      
      Clients must update their ID handling to use strings.
    files:
      - src/api/users.js
      - src/models/user.js
      - tests/api/users.test.js
      - docs/migration-guide.md
    breaking: true
    closes: "#456"
</COMMIT_RECOMMENDATION>

**Analysis:**
This is a breaking change that affects API consumers. The commit properly:
- Declares `breaking: true` 
- Includes "BREAKING CHANGE:" in the body
- Adds migration documentation
- Updates tests to reflect new behavior

Security scan passed with no issues.

<SAFE_PILOT_COMMITTING_END>
```

---

## Parsing the Output

The structured YAML block can be parsed programmatically:

```python
import yaml
import re

def parse_commit_recommendation(output: str) -> dict:
    """Extract and parse the commit recommendation block."""
    match = re.search(
        r'<COMMIT_RECOMMENDATION>(.*?)</COMMIT_RECOMMENDATION>',
        output,
        re.DOTALL
    )
    if not match:
        return None
    
    yaml_content = match.group(1).strip()
    return yaml.safe_load(yaml_content)

# Usage
recommendation = parse_commit_recommendation(agent_output)

if recommendation['status'] == 'blocked':
    print(f"Cannot commit: {recommendation['issues_found']} security issues found")
else:
    for commit in recommendation['commits']:
        print(f"Commit {commit['id']}: {commit['type']}({commit['scope']}): {commit['subject']}")
        print(f"  Files: {', '.join(commit['files'])}")
```

---

## Field Reference

### Top-level fields:
- `status`: `"safe"` (can commit) or `"blocked"` (security issues found)
- `security_scan`: `"pass"` or `"fail"`
- `issues_found`: Integer count of security issues
- `commits_proposed`: Integer count of commits recommended

### Per-commit fields:
- `id`: Integer, unique within this recommendation
- `type`: One of: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`, `build`
- `scope`: String (optional), component/module name
- `subject`: String, imperative mood, no period, max 50 chars
- `body`: String (optional), detailed explanation, wrapped at 72 chars
- `files`: Array of file paths to include in this commit
- `breaking`: Boolean, true if this is a breaking change
- `closes`: String (optional), issue references like "#123" or "Fixes #456"

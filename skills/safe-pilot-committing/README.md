# Safe Pilot Committing

A skill that ensures all commits are secure, meaningful, and follow git conventions.

## Overview

This skill is **mandatory** and will be automatically triggered whenever the agent wants to commit changes. It provides:

- **Security scanning** for secrets, API keys, log files, and unwanted artifacts
- **Conventional commit formatting** following git best practices
- **Atomic commit recommendations** that are small and focused
- **Structured, machine-parseable output** in YAML format

## Key Features

### 🔒 Security First
Scans every changed file for:
- API keys (AWS, Stripe, GitHub, Google, etc.)
- Passwords and authentication tokens
- Private keys and certificates
- Log files and debug output
- Build artifacts and temporary files
- Environment files with credentials

### 📝 Conventional Commits
Produces properly formatted commit messages:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types supported: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`, `build`

### 🔧 Structured Output
All recommendations use a machine-parseable YAML format:

```yaml
<COMMIT_RECOMMENDATION>
status: safe|blocked
security_scan: pass|fail
issues_found: <integer>
commits_proposed: <integer>

commits:
  - id: 1
    type: feat
    scope: auth
    subject: implement JWT authentication
    body: |
      Detailed explanation...
    files:
      - src/auth.js
      - tests/auth.test.js
    breaking: false
    closes: "#123"
</COMMIT_RECOMMENDATION>
```

## Usage

The agent will automatically use this skill before any commit. You don't need to invoke it manually.

When the agent proposes a commit, you'll receive:
1. A structured YAML block with all commit details
2. Human-readable analysis and explanations
3. Security scan results

**Example agent output:**

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
    subject: add password reset functionality
    files:
      - src/auth/reset.js
      - tests/auth/reset.test.js
    breaking: false
    closes: "#234"
</COMMIT_RECOMMENDATION>

**Analysis:**
Changes implement password reset feature. All files are related to the same 
feature, making this an appropriate single commit. Security scan found no issues.

<SAFE_PILOT_COMMITTING_END>
```

## Parsing the Output

### Using the Python Parser

The included `parse_commit.py` script can parse the structured output:

```bash
# From file
python skills/safe-pilot-committing/parse_commit.py agent_output.txt

# From clipboard (macOS)
pbpaste | python skills/safe-pilot-committing/parse_commit.py

# From stdin
cat agent_output.txt | python skills/safe-pilot-committing/parse_commit.py
```

**Output:**
```
============================================================
COMMIT RECOMMENDATION SUMMARY
============================================================
Status: SAFE
Security Scan: PASS
Issues Found: 0
Commits Proposed: 1

--- Commit 1 ---
Type: feat
Scope: auth
Subject: add password reset functionality
Files (2):
  - src/auth/reset.js
  - tests/auth/reset.test.js

============================================================
GIT COMMANDS TO EXECUTE
============================================================
git add "src/auth/reset.js" "tests/auth/reset.test.js"
git commit -m "feat(auth): add password reset functionality"

⚠️  Review these commands before executing!
⚠️  Ensure you have user approval before running.
```

### Using as a Library

```python
from parse_commit import parse_commit_recommendation, generate_git_commands

# Parse the agent output
recommendation = parse_commit_recommendation(agent_output)

# Check if safe to proceed
if recommendation['status'] == 'safe':
    # Generate git commands
    commands = generate_git_commands(recommendation)
    
    # Execute (with user approval)
    for cmd in commands:
        if cmd:  # Skip blank lines
            print(f"Executing: {cmd}")
            # subprocess.run(cmd, shell=True)
else:
    print(f"Blocked: {recommendation['issues_found']} security issues found")
```

## Files

- **SKILL.md** - The main skill instructions for the agent
- **example-output.md** - Examples of different output scenarios
- **parse_commit.py** - Python script to parse structured output
- **README.md** - This file

## Security Guarantees

This skill will **block commits** if it finds:
- Hardcoded API keys or secrets
- Private key material
- Password strings (not hashes)
- Log files or debug output
- `.env` files with credentials
- Large binary files without justification

When blocked, the agent will:
1. Clearly identify all security issues
2. Provide file paths and line numbers
3. Suggest remediation steps
4. Refuse to proceed until issues are fixed

## Workflow Integration

Typical flow:
1. Agent completes development work
2. Safe-pilot-committing skill is automatically triggered
3. Agent runs `git status` and `git diff`
4. Security scan is performed on all changes
5. Changes are grouped into logical commits
6. Structured recommendation is produced
7. User reviews and approves
8. User executes git commands (manually or via script)

## Best Practices

### For Users
- **Always review** the structured output before executing commands
- **Verify** that file groupings make sense
- **Check** that commit messages are clear and accurate
- **Use the parser** to generate git commands automatically

### For Integration
- Parse the `<COMMIT_RECOMMENDATION>` block using YAML parser
- Check `status` field: only execute if `"safe"`
- Check `security_scan` field: must be `"pass"`
- Always require explicit user approval before executing git commands
- Log all commits and their associated files for audit trail

## Examples

See `example-output.md` for complete examples of:
- Single safe commit
- Multiple commits (split by concern)
- Blocked commit (security issues found)
- Breaking changes
- Various commit types

## Troubleshooting

**"No COMMIT_RECOMMENDATION block found"**
- The agent may not have completed the skill workflow
- Check that the full agent response is captured
- Look for `<SAFE_PILOT_COMMITTING_START>` and `<SAFE_PILOT_COMMITTING_END>` tags

**"Security scan failed but I need to commit"**
- **Do not bypass security checks**
- Fix the identified issues first
- Use environment variables for secrets
- Add unwanted files to `.gitignore`
- Re-run the commit process after fixes

**"Commits are split too much/too little"**
- Provide feedback to the agent about your preferences
- The agent learns from your feedback
- You can always adjust the grouping manually

## Version

Skill version: 1.0.0
Compatible with: pilot-superpowers skills framework

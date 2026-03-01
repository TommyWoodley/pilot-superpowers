#!/usr/bin/env python3
"""
Parser for Safe Pilot Committing structured output.

Usage:
    python parse_commit.py < agent_output.txt
    
Or use as a library:
    from parse_commit import parse_commit_recommendation
    
    recommendation = parse_commit_recommendation(agent_output)
    if recommendation['status'] == 'safe':
        for commit in recommendation['commits']:
            print(f"Execute: git add {' '.join(commit['files'])}")
            print(f"Execute: git commit -m '{format_commit_message(commit)}'")
"""

import re
import sys
import yaml
from typing import Dict, List, Optional


def parse_commit_recommendation(text: str) -> Optional[Dict]:
    """
    Extract and parse the COMMIT_RECOMMENDATION block from agent output.
    
    Args:
        text: Full agent output containing the structured block
        
    Returns:
        Dict with parsed recommendation, or None if not found
    """
    match = re.search(
        r'<COMMIT_RECOMMENDATION>(.*?)</COMMIT_RECOMMENDATION>',
        text,
        re.DOTALL
    )
    if not match:
        return None
    
    yaml_content = match.group(1).strip()
    return yaml.safe_load(yaml_content)


def format_commit_message(commit: Dict) -> str:
    """
    Format a commit dict into a conventional commit message.
    
    Args:
        commit: Dict with type, scope, subject, body, etc.
        
    Returns:
        Formatted commit message string
    """
    # Build subject line
    scope = f"({commit['scope']})" if commit.get('scope') else ""
    subject = f"{commit['type']}{scope}: {commit['subject']}"
    
    # Build full message
    parts = [subject]
    
    if commit.get('body'):
        parts.append("")  # Blank line
        parts.append(commit['body'].strip())
    
    if commit.get('closes'):
        if not commit.get('body'):
            parts.append("")  # Blank line if no body
        parts.append("")  # Blank line before footer
        parts.append(commit['closes'])
    
    return '\n'.join(parts)


def print_summary(recommendation: Dict) -> None:
    """Print a human-readable summary of the recommendation."""
    print("=" * 60)
    print("COMMIT RECOMMENDATION SUMMARY")
    print("=" * 60)
    print(f"Status: {recommendation['status'].upper()}")
    print(f"Security Scan: {recommendation['security_scan'].upper()}")
    print(f"Issues Found: {recommendation['issues_found']}")
    print(f"Commits Proposed: {recommendation['commits_proposed']}")
    print()
    
    if recommendation['status'] == 'blocked':
        print("⛔ BLOCKED - Cannot proceed with commit")
        print("Review the security issues in the agent output above.")
        return
    
    if not recommendation['commits']:
        print("No commits proposed.")
        return
    
    for commit in recommendation['commits']:
        print(f"--- Commit {commit['id']} ---")
        print(f"Type: {commit['type']}")
        if commit.get('scope'):
            print(f"Scope: {commit['scope']}")
        print(f"Subject: {commit['subject']}")
        print(f"Files ({len(commit['files'])}):")
        for file_path in commit['files']:
            print(f"  - {file_path}")
        if commit.get('breaking'):
            print("⚠️  BREAKING CHANGE")
        if commit.get('closes'):
            print(f"Closes: {commit['closes']}")
        print()


def generate_git_commands(recommendation: Dict) -> List[str]:
    """
    Generate the git commands needed to execute the commits.
    
    Args:
        recommendation: Parsed recommendation dict
        
    Returns:
        List of shell commands to execute
    """
    if recommendation['status'] != 'safe':
        return []
    
    commands = []
    
    for commit in recommendation['commits']:
        # Add files
        files = ' '.join(f'"{f}"' for f in commit['files'])
        commands.append(f"git add {files}")
        
        # Create commit message
        message = format_commit_message(commit)
        # Escape quotes for shell
        message_escaped = message.replace('"', '\\"')
        commands.append(f'git commit -m "{message_escaped}"')
        commands.append("")  # Blank line between commits
    
    return commands


def main():
    """Main entry point when run as a script."""
    # Read from stdin or file
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    
    # Parse the recommendation
    recommendation = parse_commit_recommendation(text)
    
    if not recommendation:
        print("ERROR: No COMMIT_RECOMMENDATION block found in input", file=sys.stderr)
        sys.exit(1)
    
    # Print summary
    print_summary(recommendation)
    
    # Generate git commands
    if recommendation['status'] == 'safe':
        print("=" * 60)
        print("GIT COMMANDS TO EXECUTE")
        print("=" * 60)
        commands = generate_git_commands(recommendation)
        for cmd in commands:
            if cmd:  # Skip blank lines
                print(cmd)
        print()
        print("⚠️  Review these commands before executing!")
        print("⚠️  Ensure you have user approval before running.")


if __name__ == '__main__':
    main()

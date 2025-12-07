#!/usr/bin/env python3
"""
spawn_agents.py - Dispatch ready beads to GitHub Copilot coding agent

This script automates the spawn workflow:
1. Query ready beads (no blockers)
2. Check for existing GitHub Issues (avoid duplicates)
3. Create GitHub Issues with proper format
4. Assign @copilot to each issue
5. Update beads with external references
6. Commit changes

Usage:
    python spawn_agents.py --dry-run          # Preview what would be spawned
    python spawn_agents.py                    # Execute spawn
    python spawn_agents.py --wave 2           # Force wave number
    python spawn_agents.py --limit 5          # Limit to 5 issues
"""

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Bead:
    """Represents a beads issue."""
    id: str
    title: str
    description: str
    status: str
    priority: int
    issue_type: str
    acceptance: Optional[str] = None
    external_ref: Optional[str] = None
    created_at: Optional[str] = None


def run_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error running command: {' '.join(cmd)}", file=sys.stderr)
        print(f"stderr: {result.stderr}", file=sys.stderr)
        if check:
            sys.exit(1)
    return result


def get_ready_beads(limit: int = 50) -> list[Bead]:
    """Query beads for issues with no blockers."""
    result = run_command(["bd", "ready", "--json", "--limit", str(limit)])
    
    if not result.stdout.strip():
        return []
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"Error parsing bd ready output: {e}", file=sys.stderr)
        return []
    
    beads = []
    for item in data:
        bead = Bead(
            id=item.get("id", ""),
            title=item.get("title", ""),
            description=item.get("description", ""),
            status=item.get("status", ""),
            priority=item.get("priority", 2),
            issue_type=item.get("issue_type", "task"),
            acceptance=item.get("acceptance"),
            external_ref=item.get("external_ref"),
            created_at=item.get("created_at"),
        )
        beads.append(bead)
    
    return beads


def is_already_spawned(bead: Bead) -> bool:
    """Check if bead already has a GitHub Issue reference."""
    if bead.external_ref and bead.external_ref.startswith("gh-"):
        return True
    return False


def check_github_issue_exists(bead_id: str) -> Optional[int]:
    """Check if a GitHub Issue already exists for this bead."""
    result = run_command(
        ["gh", "issue", "list", "--search", f"[{bead_id}] in:title", "--state", "all", "--json", "number"],
        check=False
    )
    
    if result.returncode != 0:
        return None
    
    try:
        issues = json.loads(result.stdout)
        if issues:
            return issues[0]["number"]
    except (json.JSONDecodeError, KeyError, IndexError):
        pass
    
    return None


def get_current_wave() -> int:
    """Determine the current wave number from existing issues."""
    result = run_command(
        ["gh", "issue", "list", "--label", "beads-spawned", "--state", "open", "--json", "labels"],
        check=False
    )
    
    if result.returncode != 0:
        return 1
    
    try:
        issues = json.loads(result.stdout)
        max_wave = 0
        for issue in issues:
            for label in issue.get("labels", []):
                name = label.get("name", "")
                if name.startswith("wave-"):
                    try:
                        wave_num = int(name.replace("wave-", ""))
                        max_wave = max(max_wave, wave_num)
                    except ValueError:
                        pass
        return max_wave + 1 if max_wave > 0 else 1
    except json.JSONDecodeError:
        return 1


def slugify(text: str, max_length: int = 40) -> str:
    """Convert text to a URL-safe slug."""
    # Remove special characters, replace spaces with hyphens
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', text.lower())
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    return slug[:max_length]


def format_issue_body(bead: Bead, wave: int) -> str:
    """Format the GitHub Issue body according to the contract."""
    acceptance_text = bead.acceptance or "See description."
    if acceptance_text and not acceptance_text.startswith("-"):
        # Convert to checklist format
        lines = acceptance_text.split("\n")
        acceptance_text = "\n".join(f"- [ ] {line.strip('- ')}" for line in lines if line.strip())
    
    body = f"""## Beads Metadata
| Field | Value |
|-------|-------|
| Bead ID | `{bead.id}` |
| Priority | {bead.priority} |
| Type | {bead.issue_type} |
| Wave | {wave} |
| Created | {bead.created_at or datetime.now().isoformat()} |

## Description
{bead.description or 'No description provided.'}

## Acceptance Criteria
{acceptance_text}

## Context
This issue was automatically spawned from the beads task tracker.
Complete this task and create a PR linking to this issue.

---
<!-- beads-sync-marker: {bead.id} -->
"""
    return body


def create_github_issue(bead: Bead, wave: int, dry_run: bool = False) -> Optional[int]:
    """Create a GitHub Issue for the bead."""
    title = f"[{bead.id}] {bead.title}"
    body = format_issue_body(bead, wave)
    
    if dry_run:
        print(f"  [DRY RUN] Would create issue: {title}")
        return 0
    
    cmd = [
        "gh", "issue", "create",
        "--title", title,
        "--body", body,
        "--label", "beads-spawned",
        "--label", f"wave-{wave}",
        "--assignee", "@copilot",
    ]
    
    result = run_command(cmd, check=False)
    
    if result.returncode != 0:
        print(f"  Error creating issue: {result.stderr}", file=sys.stderr)
        return None
    
    # Parse issue number from URL
    issue_url = result.stdout.strip()
    try:
        issue_num = int(issue_url.split("/")[-1])
        return issue_num
    except (ValueError, IndexError):
        print(f"  Could not parse issue number from: {issue_url}", file=sys.stderr)
        return None


def update_bead(bead_id: str, issue_num: int, dry_run: bool = False) -> bool:
    """Update bead with external reference and status."""
    if dry_run:
        print(f"  [DRY RUN] Would update {bead_id} with external-ref gh-{issue_num}")
        return True
    
    result = run_command(
        ["bd", "update", bead_id, "--external-ref", f"gh-{issue_num}", "--status", "in_progress", "--json"],
        check=False
    )
    
    return result.returncode == 0


def ensure_labels_exist(dry_run: bool = False) -> None:
    """Ensure required labels exist in the repository."""
    labels = [
        ("beads-spawned", "Issue spawned from beads tracker", "0052CC"),
        ("wave-1", "Execution wave 1", "1D76DB"),
        ("wave-2", "Execution wave 2", "5319E7"),
        ("wave-3", "Execution wave 3", "0E8A16"),
    ]
    
    for name, description, color in labels:
        if dry_run:
            print(f"  [DRY RUN] Would ensure label exists: {name}")
            continue
        
        run_command(
            ["gh", "label", "create", name, "--description", description, "--color", color, "--force"],
            check=False
        )


def commit_beads_changes(wave: int, count: int, dry_run: bool = False) -> None:
    """Commit the beads database changes."""
    if dry_run:
        print(f"  [DRY RUN] Would commit .beads/issues.jsonl")
        return
    
    # Check if there are changes
    result = run_command(["git", "diff", "--quiet", ".beads/issues.jsonl"], check=False)
    if result.returncode == 0:
        print("  No changes to commit")
        return
    
    run_command(["git", "add", ".beads/issues.jsonl"])
    run_command(["git", "commit", "-m", f"chore(beads): spawn wave-{wave} ({count} issues)"])
    print("  Committed beads changes")


def main():
    parser = argparse.ArgumentParser(description="Spawn ready beads to GitHub Copilot agents")
    parser.add_argument("--dry-run", action="store_true", help="Preview without making changes")
    parser.add_argument("--wave", type=int, help="Force specific wave number")
    parser.add_argument("--limit", type=int, default=50, help="Maximum issues to spawn")
    parser.add_argument("--skip-labels", action="store_true", help="Skip label creation")
    parser.add_argument("--no-commit", action="store_true", help="Don't commit beads changes")
    args = parser.parse_args()
    
    print("=" * 60)
    print("Beads → GitHub Issue Spawner")
    print("=" * 60)
    
    # Ensure labels exist
    if not args.skip_labels:
        print("\n📌 Ensuring labels exist...")
        ensure_labels_exist(args.dry_run)
    
    # Get ready beads
    print("\n🔍 Querying ready beads...")
    beads = get_ready_beads(args.limit)
    
    if not beads:
        print("  No ready beads found. Nothing to spawn.")
        print("\n  Tip: Run 'bd list' to see all issues, or 'bd ready' for ready ones.")
        return
    
    print(f"  Found {len(beads)} ready bead(s)")
    
    # Determine wave number
    wave = args.wave or get_current_wave()
    print(f"\n🌊 Wave number: {wave}")
    
    # Process each bead
    spawned = []
    skipped = []
    failed = []
    
    print("\n🚀 Spawning issues...")
    for bead in beads:
        print(f"\n  Processing: {bead.id} - {bead.title[:50]}...")
        
        # Check if already spawned via beads
        if is_already_spawned(bead):
            print(f"    ⏭️  Already spawned ({bead.external_ref})")
            skipped.append((bead, bead.external_ref))
            continue
        
        # Check if GitHub Issue exists
        existing_issue = check_github_issue_exists(bead.id)
        if existing_issue:
            print(f"    ⏭️  GitHub Issue #{existing_issue} exists")
            # Update bead with the reference
            update_bead(bead.id, existing_issue, args.dry_run)
            skipped.append((bead, f"gh-{existing_issue}"))
            continue
        
        # Create the issue
        issue_num = create_github_issue(bead, wave, args.dry_run)
        if issue_num is None:
            print(f"    ❌ Failed to create issue")
            failed.append(bead)
            continue
        
        # Update bead
        if not args.dry_run:
            if update_bead(bead.id, issue_num, args.dry_run):
                print(f"    ✅ Created #{issue_num}, assigned @copilot")
            else:
                print(f"    ⚠️  Created #{issue_num} but failed to update bead")
        
        spawned.append((bead, issue_num))
    
    # Commit changes
    if not args.no_commit and spawned and not args.dry_run:
        print("\n📝 Committing beads changes...")
        commit_beads_changes(wave, len(spawned), args.dry_run)
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"Spawn Summary — Wave {wave}")
    print("=" * 60)
    
    if spawned:
        print(f"\n✅ Spawned {len(spawned)} issue(s):")
        print("| Bead | GitHub Issue | Status |")
        print("|------|--------------|--------|")
        for bead, issue_num in spawned:
            print(f"| {bead.id} | #{issue_num} | Created |")
    
    if skipped:
        print(f"\n⏭️  Skipped {len(skipped)} issue(s) (already spawned):")
        for bead, ref in skipped:
            print(f"  - {bead.id}: {ref}")
    
    if failed:
        print(f"\n❌ Failed {len(failed)} issue(s):")
        for bead in failed:
            print(f"  - {bead.id}: {bead.title}")
    
    print("\n" + "=" * 60)
    if args.dry_run:
        print("This was a dry run. No changes were made.")
        print("Run without --dry-run to execute.")
    else:
        print("All issues assigned to @copilot for parallel execution.")
        print("Run '@loop.sync' to monitor progress.")


if __name__ == "__main__":
    main()

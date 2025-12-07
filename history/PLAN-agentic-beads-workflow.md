# Plan: Agentic Workflow Using Beads and GitHub Cloud Agents

> **Implementation Status**: ✅ IMPLEMENTED
> 
> This workflow is now fully implemented. See:
> - **Agents**: `.github/agents/loop.{plan,decompose,spawn,sync}.agent.md`
> - **Scripts**: `.github/scripts/spawn_agents.py`, `.github/scripts/setup-labels.sh`
> - **Workflow**: `.github/workflows/beads-auto-close.yml`
>
> **Quick Start**:
> 1. Run `@loop.plan` with your request
> 2. Review the generated `history/PLAN-*.md`
> 3. Run `@loop.decompose` to create beads issues
> 4. Run `@loop.spawn` to dispatch to GitHub Copilot
> 5. Run `@loop.sync` to monitor progress

## Executive Summary

This document provides a complete technical design for a system where:
1. **Beads** is the single source of truth for all work
2. **GitHub Issues** are ephemeral "execution tickets" for cloud agents
3. **GitHub Copilot coding agent** performs the actual work in parallel
4. **State flows one direction** (beads → GitHub → PR → beads) to avoid sync conflicts

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AGENTIC WORKFLOW SYSTEM                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    PHASE 1: LOCAL PLANNING                          │   │
│   │                                                                     │   │
│   │   User Request                                                      │   │
│   │        │                                                            │   │
│   │        ▼                                                            │   │
│   │   ┌──────────┐     ┌──────────┐     ┌──────────┐                   │   │
│   │   │ @loop    │ ──► │  Draft   │ ──► │  User    │                   │   │
│   │   │  .plan   │     │  PLAN.md │     │  Review  │                   │   │
│   │   └──────────┘     └──────────┘     └────┬─────┘                   │   │
│   │                                          │                          │   │
│   │                                          ▼                          │   │
│   │   ┌──────────┐     ┌────────────────────────────────┐              │   │
│   │   │ @loop    │ ◄── │  Approved Plan (PLAN.md)       │              │   │
│   │   │.decompose│     └────────────────────────────────┘              │   │
│   │   └────┬─────┘                                                      │   │
│   │        │                                                            │   │
│   │        ▼                                                            │   │
│   │   ┌─────────────────────────────────────────────────────────────┐  │   │
│   │   │                    BEADS DATABASE                           │  │   │
│   │   │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐            │  │   │
│   │   │  │ bd-a1b │  │ bd-c2d │  │ bd-e3f │  │ bd-g4h │            │  │   │
│   │   │  │ ready  │  │ blocked│  │ ready  │  │ blocked│            │  │   │
│   │   │  └────┬───┘  └───▲────┘  └────┬───┘  └────▲───┘            │  │   │
│   │   │       │          │            │           │                 │  │   │
│   │   │       └──────────┘            └───────────┘                 │  │   │
│   │   │        (dependency)            (dependency)                 │  │   │
│   │   └─────────────────────────────────────────────────────────────┘  │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                   PHASE 2: AGENT DISPATCH                           │   │
│   │                                                                     │   │
│   │   ┌──────────┐     ┌─────────────────────────────────────────────┐ │   │
│   │   │ @loop    │     │           GITHUB ISSUES                     │ │   │
│   │   │  .spawn  │ ──► │  ┌─────────┐ ┌─────────┐ ┌─────────┐       │ │   │
│   │   └──────────┘     │  │ #42     │ │ #43     │ │ #44     │       │ │   │
│   │        │           │  │[bd-a1b] │ │[bd-e3f] │ │[bd-xxx] │       │ │   │
│   │        │           │  │@copilot │ │@copilot │ │@copilot │       │ │   │
│   │        │           │  └────┬────┘ └────┬────┘ └────┬────┘       │ │   │
│   │        │           └───────│───────────│───────────│─────────────┘ │   │
│   │        │                   │           │           │               │   │
│   │        │           ┌───────▼───────────▼───────────▼─────────────┐ │   │
│   │        │           │         PARALLEL CLOUD EXECUTION           │ │   │
│   │        │           │                                             │ │   │
│   │   bd update        │  ┌────────┐  ┌────────┐  ┌────────┐        │ │   │
│   │   --status         │  │ PR #78 │  │ PR #79 │  │ PR #80 │        │ │   │
│   │   in_progress      │  │ [WIP]  │  │ [WIP]  │  │ [WIP]  │        │ │   │
│   │        │           │  └────────┘  └────────┘  └────────┘        │ │   │
│   │        ▼           └─────────────────────────────────────────────┘ │   │
│   │   BEADS: in_progress                                               │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                  PHASE 3: COMPLETION SYNC                           │   │
│   │                                                                     │   │
│   │   PR Merged ──► GitHub Action ──► bd close <id> ──► BEADS: closed  │   │
│   │                                                                     │   │
│   │   ┌───────────────────────────────────────────────────────────────┐│   │
│   │   │ .github/workflows/beads-sync.yml                              ││   │
│   │   │                                                               ││   │
│   │   │ on: pull_request: [closed]                                    ││   │
│   │   │   if: merged == true                                          ││   │
│   │   │   → Extract bd-XXX from PR body                               ││   │
│   │   │   → bd close bd-XXX --reason "PR merged"                      ││   │
│   │   │   → Commit .beads/issues.jsonl                                ││   │
│   │   └───────────────────────────────────────────────────────────────┘│   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Components

| Component | Type | Purpose |
|-----------|------|---------|
| `bd` CLI | Existing | Local issue tracking with dependency DAG |
| `loop.plan` | Agent | Breaks down requests into PLAN.md drafts |
| `loop.decompose` | Agent | Converts PLAN.md into beads issues |
| `loop.spawn` | Agent | Creates GitHub Issues from ready beads, assigns Copilot |
| `loop.sync` | Agent | Monitors PRs, resolves conflicts, updates beads |
| GitHub Action | Workflow | Auto-closes beads when PRs merge |
| GitHub MCP | Integration | Issue creation, PR management via MCP tools |

---

## Bead Data Model

### Schema (JSONL format in `.beads/issues.jsonl`)

```json
{
  "id": "bd-a1b",
  "title": "Implement user authentication",
  "description": "Create login/logout endpoints using JWT tokens. Use bcrypt for password hashing. Follow REST conventions.",
  "acceptance": "- Users can register\n- Users can login\n- Protected routes reject unauthenticated requests",
  "design": "Use passport.js with local strategy. Store refresh tokens in Redis.",
  "status": "ready",
  "priority": 1,
  "issue_type": "feature",
  "assignee": null,
  "labels": ["auth", "backend"],
  "estimate": 120,
  "dependencies": [
    {
      "issue_id": "bd-a1b",
      "depends_on_id": "bd-xyz",
      "type": "blocks",
      "created_at": "2025-12-07T10:00:00Z"
    }
  ],
  "external_ref": "gh-42",
  "created_at": "2025-12-07T10:00:00Z",
  "updated_at": "2025-12-07T10:00:00Z"
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | ✅ | Unique identifier (e.g., `bd-a1b`) |
| `title` | string | ✅ | Concise, action-oriented title |
| `description` | string | ✅ | **Detailed technical context** sufficient for an AI agent |
| `acceptance` | string | ❌ | Checklist of success criteria |
| `design` | string | ❌ | Implementation notes, architecture decisions |
| `status` | enum | ✅ | `planned`, `ready`, `in_progress`, `blocked`, `closed` |
| `priority` | int | ✅ | 0 (critical) → 4 (backlog) |
| `issue_type` | enum | ✅ | `bug`, `feature`, `task`, `epic`, `chore` |
| `assignee` | string | ❌ | User or agent handle |
| `labels` | array | ❌ | Tags for categorization |
| `estimate` | int | ❌ | Time estimate in minutes |
| `dependencies` | array | ❌ | List of blocking issues |
| `external_ref` | string | ❌ | GitHub Issue reference (e.g., `gh-42`) |
| `created_at` | datetime | ✅ | Creation timestamp |
| `updated_at` | datetime | ✅ | Last update timestamp |

### Dependency Types

| Type | Meaning |
|------|---------|
| `blocks` | This issue must complete before the dependent can start |
| `parent-child` | Hierarchical relationship (epic → tasks) |
| `discovered-from` | Issue discovered while working on another |
| `relates-to` | Informational link |

---

## Planning Flow (Phase 1)

### Step 1: User Request Intake

User provides a high-level goal:
```
"I need a REST API for a todo application with user authentication"
```

### Step 2: Generate PLAN.md (Complex Requests)

The `@loop.plan` agent creates `history/PLAN-todo-api.md`:

```markdown
# Plan: Todo API with Authentication

## Overview
Build a REST API for a todo application with JWT-based authentication.

## Work Breakdown

### Epic: User Authentication (bd-auth)
1. **Setup auth infrastructure** (bd-auth-1)
   - Dependencies: None
   - Description: Install passport.js, configure JWT strategy
   - Acceptance: Auth middleware functional
   
2. **Implement registration** (bd-auth-2)
   - Dependencies: bd-auth-1
   - Description: POST /api/auth/register endpoint
   - Acceptance: Users can register with email/password

3. **Implement login/logout** (bd-auth-3)
   - Dependencies: bd-auth-1
   - Description: POST /api/auth/login, POST /api/auth/logout
   - Acceptance: JWT issued on login, invalidated on logout

### Epic: Todo CRUD (bd-todo)
1. **Todo model and migrations** (bd-todo-1)
   - Dependencies: None
   - Description: Create Todo schema with user foreign key
   
2. **CRUD endpoints** (bd-todo-2)
   - Dependencies: bd-todo-1, bd-auth-3 (auth required)
   - Description: GET/POST/PUT/DELETE /api/todos
   
## Dependency Graph

```
bd-auth-1 ───► bd-auth-2
    │              
    └──────► bd-auth-3 ───┐
                          │
bd-todo-1 ────────────────┼──► bd-todo-2
```

## Execution Waves

| Wave | Issues | Can Run In Parallel |
|------|--------|---------------------|
| 1 | bd-auth-1, bd-todo-1 | ✅ Yes |
| 2 | bd-auth-2, bd-auth-3 | ✅ Yes |
| 3 | bd-todo-2 | Single |
```

### Step 3: User Review

User reviews and edits `PLAN.md`. May:
- Remove unnecessary items
- Add missing requirements
- Adjust dependencies
- Modify descriptions for clarity

### Step 4: Decompose into Beads

User runs `@loop.decompose` which:

```bash
# Creates epic
bd create "User Authentication" -t epic -p 1 --json
# Returns: bd-a1b

# Creates tasks with dependencies
bd create "Setup auth infrastructure" -t task -p 1 \
  --parent bd-a1b \
  -d "Install passport.js, configure JWT strategy..." \
  --acceptance "Auth middleware functional" \
  --json
# Returns: bd-c2d

bd create "Implement registration" -t task -p 1 \
  --parent bd-a1b \
  --deps bd-c2d \
  -d "POST /api/auth/register endpoint..." \
  --json
# Returns: bd-e3f

# ... continues for all items
```

### Step 5: Validate Dependency Graph

```bash
# Check for cycles
bd dep cycles

# View dependency tree
bd dep tree bd-todo-2
# Output:
# bd-todo-2: CRUD endpoints
#   └─ depends on: bd-todo-1: Todo model and migrations
#   └─ depends on: bd-auth-3: Implement login/logout
#       └─ depends on: bd-auth-1: Setup auth infrastructure
```

---

## Dispatch Flow (Phase 2)

### The `loop.spawn` Agent

This agent bridges beads and GitHub Issues:

```
┌────────────────────────────────────────────────────────────────┐
│                     SPAWN WORKFLOW                             │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  1. Query ready beads         bd ready --json                  │
│                                    │                           │
│  2. Filter already-spawned        │                           │
│     (has external_ref)            ▼                           │
│                            ┌────────────┐                      │
│  3. For each ready bead:   │  bd-a1b    │                      │
│                            │  bd-e3f    │ (parallel-safe)      │
│                            └─────┬──────┘                      │
│                                  │                             │
│  4. Create GitHub Issue          ▼                             │
│     via MCP/gh CLI        ┌───────────────┐                    │
│                           │ GitHub Issue  │                    │
│                           │ #42 [bd-a1b]  │                    │
│                           └───────┬───────┘                    │
│                                   │                            │
│  5. Assign Copilot               ▼                             │
│                           @copilot assigned                    │
│                                   │                            │
│  6. Update bead                  ▼                             │
│     bd update bd-a1b      status: in_progress                  │
│     --external-ref gh-42  external_ref: gh-42                  │
│     --status in_progress                                       │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### GitHub Issue Format Contract

All spawned issues MUST follow this format:

**Title:**
```
[bd-<id>] <issue-title>
```

**Labels:**
- `beads-spawned` (required)
- `wave-<n>` (wave number)
- `priority-<level>` (optional)
- `type-<kind>` (optional)

**Body Template:**
```markdown
## Beads Metadata
| Field | Value |
|-------|-------|
| Bead ID | `bd-a1b` |
| Priority | 1 (High) |
| Type | feature |
| Wave | 1 |
| Created | 2025-12-07T10:00:00Z |

## Description
Install passport.js, configure JWT strategy. Use bcrypt for password hashing.

## Acceptance Criteria
- [ ] Auth middleware is functional
- [ ] JWT tokens are properly signed
- [ ] Refresh token mechanism works

## Context
This is part of the User Authentication epic. The following issues depend on this:
- bd-e3f: Implement registration
- bd-g4h: Implement login/logout

---
<!-- beads-sync-marker: bd-a1b -->
```

### Parallel Execution

GitHub Copilot coding agent handles each issue independently:

```
Wave 1 (parallel):
  bd-a1b → Issue #42 → Copilot → PR #78 (branch: copilot/bd-a1b-auth-setup)
  bd-c2d → Issue #43 → Copilot → PR #79 (branch: copilot/bd-c2d-todo-model)

Wave 2 (after Wave 1 merges):
  bd-e3f → Issue #44 → Copilot → PR #80
  bd-g4h → Issue #45 → Copilot → PR #81
```

### Spawning Script (Python)

```python
#!/usr/bin/env python3
"""
spawn_agents.py - Dispatch ready beads to GitHub Copilot coding agent
"""

import json
import subprocess
from dataclasses import dataclass
from typing import Optional

@dataclass
class Bead:
    id: str
    title: str
    description: str
    acceptance: Optional[str]
    priority: int
    issue_type: str
    external_ref: Optional[str]

def get_ready_beads() -> list[Bead]:
    """Query beads for issues with no blockers."""
    result = subprocess.run(
        ["bd", "ready", "--json"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"bd ready failed: {result.stderr}")
    
    data = json.loads(result.stdout)
    return [Bead(**item) for item in data]

def bead_already_spawned(bead: Bead) -> bool:
    """Check if bead already has a GitHub Issue."""
    return bead.external_ref is not None and bead.external_ref.startswith("gh-")

def create_github_issue(bead: Bead, wave: int) -> int:
    """Create GitHub Issue and return issue number."""
    body = f"""## Beads Metadata
| Field | Value |
|-------|-------|
| Bead ID | `{bead.id}` |
| Priority | {bead.priority} |
| Type | {bead.issue_type} |
| Wave | {wave} |

## Description
{bead.description}

## Acceptance Criteria
{bead.acceptance or 'See description.'}

---
<!-- beads-sync-marker: {bead.id} -->
"""
    
    result = subprocess.run([
        "gh", "issue", "create",
        "--title", f"[{bead.id}] {bead.title}",
        "--body", body,
        "--label", "beads-spawned",
        "--label", f"wave-{wave}",
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"Failed to create issue: {result.stderr}")
    
    # Parse issue URL to get number
    issue_url = result.stdout.strip()
    issue_num = int(issue_url.split("/")[-1])
    return issue_num

def assign_copilot(issue_num: int):
    """Assign Copilot coding agent to the issue."""
    # Use GitHub MCP or gh CLI
    subprocess.run([
        "gh", "issue", "edit", str(issue_num),
        "--add-assignee", "@copilot"
    ], check=True)

def update_bead(bead_id: str, issue_num: int):
    """Mark bead as in_progress with external reference."""
    subprocess.run([
        "bd", "update", bead_id,
        "--status", "in_progress",
        "--external-ref", f"gh-{issue_num}",
        "--json"
    ], check=True)

def main():
    beads = get_ready_beads()
    wave = determine_current_wave()  # Query existing wave labels
    
    spawned = []
    skipped = []
    
    for bead in beads:
        if bead_already_spawned(bead):
            skipped.append(bead)
            continue
        
        issue_num = create_github_issue(bead, wave)
        assign_copilot(issue_num)
        update_bead(bead.id, issue_num)
        spawned.append((bead, issue_num))
    
    # Print summary
    print(f"## Spawn Summary — Wave {wave}\n")
    print(f"Spawned {len(spawned)} issues ({len(skipped)} skipped):\n")
    print("| Bead | GitHub Issue | Status |")
    print("|------|--------------|--------|")
    for bead, issue_num in spawned:
        print(f"| {bead.id} | #{issue_num} | ✅ Created |")
    for bead in skipped:
        print(f"| {bead.id} | {bead.external_ref} | ⏭️ Already spawned |")

if __name__ == "__main__":
    main()
```

---

## Completion Sync (Phase 3)

### GitHub Action Workflow

`.github/workflows/beads-sync.yml`:

```yaml
name: Sync Beads on PR Merge

on:
  pull_request:
    types: [closed]

jobs:
  close-beads:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: write
      
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          ref: main
          fetch-depth: 0
          
      - name: Install bd CLI
        run: |
          # Install beads CLI (adjust for your installation method)
          curl -sSL https://install.beads.dev | bash
          echo "$HOME/.beads/bin" >> $GITHUB_PATH
          
      - name: Extract Beads ID
        id: extract
        run: |
          # Look for beads-sync-marker in PR body
          BEADS_ID=$(echo "${{ github.event.pull_request.body }}" | \
            grep -oP '(?<=beads-sync-marker: )[a-z]+-[a-z0-9]+' | head -1)
          echo "beads_id=$BEADS_ID" >> $GITHUB_OUTPUT
          echo "Found beads ID: $BEADS_ID"
          
      - name: Close Beads Issue
        if: steps.extract.outputs.beads_id != ''
        env:
          BEADS_ID: ${{ steps.extract.outputs.beads_id }}
          PR_NUM: ${{ github.event.pull_request.number }}
        run: |
          bd close "$BEADS_ID" --reason "PR #$PR_NUM merged"
          
      - name: Commit Beads State
        if: steps.extract.outputs.beads_id != ''
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add .beads/issues.jsonl
          git commit -m "chore: close ${{ steps.extract.outputs.beads_id }} (PR #${{ github.event.pull_request.number }})"
          git push
          
      - name: Close GitHub Issue
        if: steps.extract.outputs.beads_id != ''
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Find and close the spawned GitHub Issue
          ISSUE_NUM=$(gh pr view ${{ github.event.pull_request.number }} \
            --json closingIssuesReferences \
            -q '.closingIssuesReferences[0].number')
          if [ -n "$ISSUE_NUM" ]; then
            gh issue close "$ISSUE_NUM" \
              --comment "✅ Completed by PR #${{ github.event.pull_request.number }}"
          fi
```

---

## Status Updates and Failure Handling

### Monitoring Active Work

```bash
# See all in-progress issues
bd list --status in_progress --json

# Check for stale spawned issues (no activity > 24h)
bd stale --days 1 --json
```

### Handling Failures

| Scenario | Detection | Action |
|----------|-----------|--------|
| Copilot can't complete | PR has "blocked" label or no commits after 1h | Manual review, reassign |
| PR has merge conflicts | GitHub reports conflict | Run `loop.sync` to rebase |
| Action fails to close beads | Beads still `in_progress` after merge | Manual `bd close` |
| GitHub Issue orphaned | Issue open but no linked PR | Close issue, reset bead status |

### Retry Logic

```bash
# Reset a failed bead to try again
bd update bd-a1b --status ready

# Remove external reference to allow re-spawn
bd update bd-a1b --external-ref ""
```

---

## Setup Instructions

### Prerequisites

1. **GitHub Copilot Pro+/Business/Enterprise** with coding agent enabled
2. **`bd` CLI** installed and initialized
3. **`gh` CLI** authenticated with repo access
4. **Repository permissions**: Actions enabled, Copilot agent allowed

### Step-by-Step Setup

#### 1. Install bd CLI

```bash
# Via Homebrew (macOS/Linux)
brew install beads-cli/tap/bd

# Or via curl
curl -sSL https://install.beads.dev | bash
```

#### 2. Initialize Beads in Repository

```bash
cd your-repo
bd init
# Creates .beads/ directory with config.yaml and beads.db
```

#### 3. Configure Git Integration

```bash
# Setup auto-sync hooks
bd hooks install

# Verify
bd doctor
```

#### 4. Add GitHub Action

Create `.github/workflows/beads-sync.yml` with the content from Phase 3 above.

#### 5. Configure MCP (Optional but Recommended)

Add to `.vscode/mcp.json` or Claude settings:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${env:GITHUB_TOKEN}"
      }
    },
    "beads": {
      "command": "beads-mcp",
      "args": ["--db", ".beads/beads.db"]
    }
  }
}
```

#### 6. Create Agent Files

Create `.github/agents/loop.spawn.agent.md` (already provided in repo).

#### 7. Verify Setup

```bash
# Check bd is working
bd status

# Check gh is authenticated
gh auth status

# Check Copilot coding agent is available
gh copilot --help  # (or check repo settings)
```

---

## End-to-End Example

### Project: Simple Blog API

#### User Request
```
Create a simple blog API with posts and comments. Include basic validation.
```

#### Generated Beads

```bash
# Check what was created
bd list --json
```

```json
[
  {
    "id": "bd-a1b",
    "title": "Setup Express project structure",
    "description": "Initialize package.json, install Express, create src/index.js with basic server",
    "status": "ready",
    "priority": 1,
    "dependencies": []
  },
  {
    "id": "bd-c2d", 
    "title": "Create Post model and routes",
    "description": "POST /posts, GET /posts, GET /posts/:id. Use in-memory array for storage.",
    "status": "ready",
    "priority": 2,
    "dependencies": [{"depends_on_id": "bd-a1b", "type": "blocks"}]
  },
  {
    "id": "bd-e3f",
    "title": "Create Comment model and routes",
    "description": "POST /posts/:id/comments, GET /posts/:id/comments. Link to parent post.",
    "status": "ready",
    "priority": 2,
    "dependencies": [{"depends_on_id": "bd-c2d", "type": "blocks"}]
  },
  {
    "id": "bd-g4h",
    "title": "Add request validation",
    "description": "Use Joi or express-validator. Validate title required, body length.",
    "status": "ready",
    "priority": 3,
    "dependencies": [{"depends_on_id": "bd-c2d", "type": "blocks"}]
  }
]
```

#### Dependency Graph

```
bd-a1b (Setup Express)
    │
    ▼
bd-c2d (Post routes)
    │
    ├───────────────┐
    ▼               ▼
bd-e3f (Comments)  bd-g4h (Validation)
```

#### Wave Execution

```
Wave 1: bd-a1b → Issue #10 → Copilot → PR #15 (merged)
Wave 2: bd-c2d → Issue #11 → Copilot → PR #16 (merged)
Wave 3: bd-e3f, bd-g4h → Issues #12, #13 → PRs #17, #18 (parallel)
```

#### Final State

```bash
bd list
# All issues show status: closed
```

---

## MCP Integration Details

### GitHub MCP Server Tools

The GitHub MCP server provides these relevant tools:

| Tool | Purpose |
|------|---------|
| `mcp_io_github_git_issue_write` | Create GitHub Issues |
| `mcp_io_github_git_list_issues` | Query existing issues |
| `mcp_io_github_git_update_pull_request` | Assign reviewers |
| `mcp_io_github_git_assign_copilot_to_issue` | Trigger Copilot coding agent |
| `mcp_io_github_git_pull_request_read` | Check PR status |

### Using MCP from Agents

```typescript
// In loop.spawn agent, use MCP tool:
mcp_io_github_git_issue_write({
  method: "create",
  owner: "your-org",
  repo: "your-repo",
  title: `[${bead.id}] ${bead.title}`,
  body: formatBeadBody(bead),
  labels: ["beads-spawned", `wave-${wave}`]
})

// Then assign Copilot:
mcp_io_github_git_assign_copilot_to_issue({
  owner: "your-org",
  repo: "your-repo",
  issueNumber: createdIssue.number
})
```

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Copilot fails to complete task | Medium | Medium | Timeout monitoring, manual fallback |
| Parallel PRs conflict on files | Medium | High | Beads dependencies prevent conflicting tasks |
| GitHub Action fails to sync | Low | Medium | Manual `bd close` backup, alerting |
| Beads/GitHub drift | Low | High | One-way flow design eliminates sync conflicts |
| Rate limiting on spawning | Low | Low | Batch spawning, respect API limits |

---

## Future Enhancements

1. **Wave Orchestration Dashboard**: VS Code extension showing live wave status
2. **Auto-Retry**: Automatically retry failed Copilot tasks with adjusted prompts
3. **Cost Tracking**: Monitor GitHub Actions minutes and Copilot usage
4. **Custom Agents**: Create specialized agents (frontend, backend, docs) with different behaviors
5. **Conflict Detection**: Pre-spawn check for potential file conflicts between parallel beads

---

## Summary

This system provides:

- ✅ **Beads as single source of truth** for all work tracking
- ✅ **Structured decomposition** of high-level goals into agent-executable tasks
- ✅ **Explicit dependency graphs** determining parallel vs serial execution
- ✅ **One-way data flow** eliminating sync conflicts
- ✅ **Parallel cloud execution** via GitHub Copilot coding agent
- ✅ **Automatic completion tracking** via GitHub Actions
- ✅ **Clean, reliable setup** with minimal infrastructure

The key insight is treating GitHub Issues as **ephemeral execution tickets** rather than a second source of truth. Beads orchestrates, GitHub executes, and the state flows back through PR merges.

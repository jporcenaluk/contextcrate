# Plan: Hub-and-Spoke Implementation with Beads Orchestration

## Critique & Issues (Added by Plan Reviewer)

1.  **Missing Directory**: The plan requires `.github/workflows/` for the GitHub Action, but this directory does not exist. It must be created.
2.  **Tool Dependency**: The appendix uses `jq` for JSON processing, but `jq` is not currently installed in the environment.
3.  **File Paths**: The plan references agent files (e.g., `loop.spawn.agent.md`) without specifying their location. Based on the repository structure, these should be placed in `.github/agents/`.

---

## Executive Summary

This plan implements **Option 4** from the parallel agents strategy document. Beads is the **single source of truth**, and GitHub Issues are ephemeral "execution tickets" that trigger cloud-based Copilot work. The key innovation is a **wave-based execution model** that respects dependency ordering while maximizing parallelism.

---

## Core Principles

1. **Beads is Truth**: All planning, dependencies, and final state live in beads
2. **GitHub Issues are Spokes**: Ephemeral execution tickets, not records
3. **One-Way Flow**: Beads → GitHub Issue → PR → Merge → Beads (close)
4. **Wave Execution**: Dependencies determine execution order in "waves"
5. **VS Code First**: Manage everything from VS Code, visit GitHub only for PR review/merge

---

## The Wave Execution Model

### Problem: Dependencies vs. Parallelism

Consider this dependency graph:
```
bd-1 (Create schema) ──┐
                       ├──► bd-3 (Run migrations) ──► bd-5 (Seed data)
bd-2 (Setup DB)  ──────┘
                       
bd-4 (Write API docs) ──► (independent)
```

**Wave 1** (no blockers): bd-1, bd-2, bd-4 — run in parallel  
**Wave 2** (depends on wave 1): bd-3 — runs after bd-1 and bd-2 complete  
**Wave 3** (depends on wave 2): bd-5 — runs after bd-3 completes

### The Algorithm

```
WHILE issues with status != closed exist:
    wave = bd ready --json  # Returns issues with no unresolved blockers
    
    IF wave is empty AND open issues exist:
        ERROR: Circular dependency or stuck state
    
    FOR EACH issue in wave (PARALLEL):
        spawn_github_issue(issue)
    
    WAIT for all PRs in wave to merge
    
    # GitHub Action auto-closes beads issues on merge
    # Next iteration: bd ready returns next wave
```

### Why This Works for Database Migrations

- `bd-1: Create schema migration` (independent)
- `bd-2: Create user table migration` depends on bd-1
- `bd-3: Create posts table migration` depends on bd-2

Beads' dependency system ensures:
1. Only bd-1 appears in `bd ready` initially
2. After bd-1 merges and closes, bd-2 becomes ready
3. After bd-2 merges and closes, bd-3 becomes ready

**Serial work is enforced by dependencies. Parallel work happens naturally when dependencies allow.**

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           VS CODE (Your Workstation)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │                         BEADS (Source of Truth)                      │  │
│   │                                                                      │  │
│   │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐         │  │
│   │  │ bd-1   │  │ bd-2   │  │ bd-3   │  │ bd-4   │  │ bd-5   │         │  │
│   │  │ ready  │  │ ready  │  │blocked │  │ ready  │  │blocked │         │  │
│   │  └────┬───┘  └────┬───┘  └────────┘  └────┬───┘  └────────┘         │  │
│   │       │           │                       │                          │  │
│   └───────┼───────────┼───────────────────────┼──────────────────────────┘  │
│           │           │                       │                             │
│           ▼           ▼                       ▼                             │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │                      @loop.spawn (New Agent)                         │  │
│   │                                                                      │  │
│   │  1. Reads `bd ready --json`                                          │  │
│   │  2. Creates GitHub Issues with beads ID embedded                     │  │
│   │  3. Updates beads: `bd update <id> --external-ref gh-<num>`          │  │
│   │  4. Assigns @copilot to each issue                                   │  │
│   │                                                                      │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ gh issue create + assign
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              GITHUB (Cloud)                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                     │
│   │ Issue #45   │    │ Issue #46   │    │ Issue #47   │                     │
│   │ [bd-1]      │    │ [bd-2]      │    │ [bd-4]      │                     │
│   │ @copilot    │    │ @copilot    │    │ @copilot    │                     │
│   └──────┬──────┘    └──────┬──────┘    └──────┬──────┘                     │
│          │                  │                  │                            │
│          │ PARALLEL         │ PARALLEL         │ PARALLEL                   │
│          ▼                  ▼                  ▼                            │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                     │
│   │   PR #78    │    │   PR #79    │    │   PR #80    │                     │
│   │ Closes #45  │    │ Closes #46  │    │ Closes #47  │                     │
│   └──────┬──────┘    └──────┬──────┘    └──────┬──────┘                     │
│          │                  │                  │                            │
│          └──────────────────┴──────────────────┘                            │
│                             │                                               │
│                             ▼                                               │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │              GitHub Action: on pull_request merged                  │   │
│   │                                                                     │   │
│   │  1. Extract beads ID from PR body/branch name                       │   │
│   │  2. Run: bd close <beads-id> --reason "PR #X merged"                │   │
│   │  3. Commit .beads/issues.jsonl                                      │   │
│   │  4. Close the GitHub Issue (optional cleanup)                       │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ git pull (user syncs)
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           VS CODE (Back to You)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   1. Pull latest changes (includes .beads/issues.jsonl updates)             │
│   2. `bd ready` now shows NEXT WAVE of issues                               │
│   3. Run @loop.spawn again to dispatch next wave                            │
│   4. Repeat until all issues closed                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## New Agents to Create

### 1. `.github/agents/loop.spawn.agent.md` — The Dispatcher

**Purpose**: Bridge between beads and GitHub Issues. Spawns cloud execution.

**Key Behaviors**:
- Reads `bd ready --json` to get parallelizable issues
- Creates GitHub Issues with standardized format (beads ID in title + body)
- Links beads to GitHub: `bd update <id> --external-ref gh-<issue-num>`
- Assigns `@copilot` (or specified agent) to each issue
- Sets beads status to `in_progress`

### 2. `.github/agents/loop.monitor.agent.md` — The Watcher

**Purpose**: Monitor spawned work and report status.

**Key Behaviors**:
- Lists all beads issues with `external-ref` set
- Checks corresponding GitHub Issues/PRs for status
- Reports: "Wave 1: 2/3 complete, 1 PR open"
- Alerts on: stalled issues, failed PRs, merge conflicts

### 3. `.github/agents/loop.sync.agent.md` — The Reconciler

**Purpose**: Pull remote changes and reconcile state.

**Key Behaviors**:
- Runs `git pull` to get latest .beads/issues.jsonl
- Runs `bd sync` to import any changes
- Reports what changed: "bd-1, bd-2, bd-4 now closed. bd-3, bd-5 now ready."
- Optionally triggers `@loop.spawn` for next wave

---

## GitHub Issue Format (Contract)

When `@loop.spawn` creates a GitHub Issue, it MUST follow this format:

### Title
```
[bd-<id>] <issue-title>
```

Example: `[bd-hrs] Create prompt tuner meta-prompt`

### Body
```markdown
## Beads Issue: bd-<id>

**Priority**: P<n>
**Type**: <feature|bug|task>
**Parent**: <parent-id or "None">

---

## Description

<description from beads>

---

## Acceptance Criteria

<acceptance from beads, or "None specified">

---

## Context

<Any additional context, file references, etc.>

---

<!-- BEADS_METADATA
beads_id: bd-<id>
spawned_at: <ISO timestamp>
spawned_by: loop.spawn
-->
```

### Labels
- `beads-spawned` — Marks this as a spawned execution ticket
- `wave-<n>` — Which execution wave (for tracking)

### Branch Name (Convention for PRs)
```
beads/bd-<id>-<short-slug>
```

Example: `beads/bd-hrs-prompt-tuner`

---

## GitHub Action: Auto-Close Beads

### `.github/workflows/beads-auto-close.yml`

```yaml
name: Auto-Close Beads on PR Merge

on:
  pull_request:
    types: [closed]

jobs:
  close-beads-issue:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          # Checkout the base branch (main) to update beads
          ref: ${{ github.event.pull_request.base.ref }}
          # Need write access to push the beads update
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Install beads (bd)
        run: |
          # Install bd CLI - adjust based on your installation method
          curl -sSL https://raw.githubusercontent.com/jporcenaluk/beads/main/install.sh | bash
          echo "$HOME/.local/bin" >> $GITHUB_PATH
      
      - name: Extract Beads ID from PR
        id: extract
        run: |
          # Try branch name first (most reliable)
          BRANCH="${{ github.event.pull_request.head.ref }}"
          BEADS_ID=$(echo "$BRANCH" | grep -oP 'bd-[a-zA-Z0-9]+' | head -1)
          
          # Fallback to PR body
          if [ -z "$BEADS_ID" ]; then
            BEADS_ID=$(echo "${{ github.event.pull_request.body }}" | grep -oP 'beads_id:\s*\Kbd-[a-zA-Z0-9]+' | sed 's/beads_id:\s*//' | head -1)
          fi
          
          # Fallback to PR title
          if [ -z "$BEADS_ID" ]; then
            BEADS_ID=$(echo "${{ github.event.pull_request.title }}" | grep -oP '\[bd-[a-zA-Z0-9]+\]' | tr -d '[]' | head -1)
          fi
          
          echo "beads_id=$BEADS_ID" >> $GITHUB_OUTPUT
          echo "Found beads ID: $BEADS_ID"
      
      - name: Close Beads Issue
        if: steps.extract.outputs.beads_id != ''
        env:
          BEADS_ID: ${{ steps.extract.outputs.beads_id }}
          PR_NUM: ${{ github.event.pull_request.number }}
        run: |
          # Close the beads issue
          bd close "$BEADS_ID" --reason "PR #$PR_NUM merged" --json || echo "Warning: Could not close $BEADS_ID"
          
          # Commit the updated beads database
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          
          if git diff --quiet .beads/issues.jsonl; then
            echo "No changes to beads database"
          else
            git add .beads/issues.jsonl
            git commit -m "chore(beads): close $BEADS_ID after PR #$PR_NUM merge"
            git push
          fi
      
      - name: Close Linked GitHub Issue
        if: steps.extract.outputs.beads_id != ''
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          BEADS_ID: ${{ steps.extract.outputs.beads_id }}
        run: |
          # Find and close the GitHub Issue that spawned this PR
          ISSUE_NUM=$(gh issue list --search "$BEADS_ID in:title" --state open --json number -q '.[0].number')
          
          if [ -n "$ISSUE_NUM" ]; then
            gh issue close "$ISSUE_NUM" --comment "✅ Closed by PR #${{ github.event.pull_request.number }} merge. Beads issue $BEADS_ID complete."
          fi
```

---

## VS Code Workflow (Your Daily Flow)

### Morning: Check Status

```bash
# See what's currently in-flight
bd list --status in_progress --json

# See what's ready to spawn
bd ready --json

# Check for blocked issues (debugging)
bd blocked --json
```

Or use `@loop.monitor`:
> "@loop.monitor show me the status of all active work"

### Spawn a Wave

> "@loop.spawn dispatch all ready issues to GitHub"

The agent will:
1. Run `bd ready --json`
2. For each issue, create a GitHub Issue with proper format
3. Assign @copilot
4. Update beads with `--external-ref gh-<num>`
5. Report: "Spawned 3 issues: bd-1 → #45, bd-2 → #46, bd-4 → #47"

### Monitor Progress

Check GitHub for PR status. When PRs are approved:
1. Merge them (you can do this in VS Code with GitHub extension)
2. GitHub Action runs automatically
3. Beads issues are closed

### Sync and Repeat

```bash
git pull
bd sync
```

Or: `@loop.sync` to pull and report what changed.

Then: `@loop.spawn` again to dispatch the next wave.

---

## Handling Dependencies: The Critical Detail

### Creating Issues with Dependencies

When using `@loop.decompose` or `@loop.plan`, dependencies MUST be set:

```bash
# Independent issues
bd create "Create schema migration" -t task -p 1 --json
# Returns: bd-a1b

# Dependent issue
bd create "Create user table migration" -t task -p 1 --deps "bd-a1b" --json
# Returns: bd-c2d (blocked by bd-a1b)

# Chain continues
bd create "Create posts table migration" -t task -p 1 --deps "bd-c2d" --json
# Returns: bd-e3f (blocked by bd-c2d)
```

### Verification

```bash
# Show dependency tree
bd dep tree bd-e3f

# Output:
# bd-e3f: Create posts table migration
#   └─ depends on: bd-c2d: Create user table migration
#       └─ depends on: bd-a1b: Create schema migration
```

### What `bd ready` Returns

```bash
bd ready --json
# Returns ONLY: bd-a1b (the unblocked root)

# After bd-a1b closes:
bd ready --json
# Returns ONLY: bd-c2d (now unblocked)

# After bd-c2d closes:
bd ready --json
# Returns ONLY: bd-e3f (now unblocked)
```

**This is how serial execution is enforced.**

---

## Edge Cases and Mitigations

### 1. PR Merge Conflicts

**Problem**: Parallel PRs might conflict on the same files.

**Mitigation**: 
- Beads dependencies should prevent this at the planning stage
- If issues CAN conflict, they should have a dependency relationship
- `@loop.plan` should detect potential conflicts and add dependencies

### 2. Copilot Fails to Complete

**Problem**: Copilot assigned but issue stalls.

**Mitigation**:
- `@loop.monitor` checks issue age
- After N hours, alert: "bd-1 / #45 stalled — Copilot has not responded"
- Manual intervention: reassign or close/recreate

### 3. GitHub Action Fails to Close Beads

**Problem**: PR merges but Action fails.

**Mitigation**:
- Manual fallback: `bd close bd-xxx --reason "Manual close"`
- `@loop.sync` can detect orphaned issues (GitHub closed, beads open)

### 4. Race Condition on .beads/issues.jsonl

**Problem**: Multiple PRs merge simultaneously, both try to update beads.

**Mitigation**:
- GitHub Actions run serially per branch by default
- Use `concurrency` in workflow:
  ```yaml
  concurrency:
    group: beads-update
    cancel-in-progress: false
  ```
- Beads has merge driver support: `bd merge`

### 5. Out-of-Order Merges

**Problem**: bd-c2d PR is ready before bd-a1b PR (human merges wrong order).

**Mitigation**:
- The dependency is in BEADS, not GitHub
- Even if PRs merge out of order, beads won't show bd-c2d as ready until bd-a1b closes
- The Action will close beads issues in merge order, not spawn order
- Next wave only spawns when dependencies are ACTUALLY satisfied in beads

---

## Agent Modifications

### Update: `.github/agents/loop.plan.agent.md`

Add dependency awareness:

```markdown
# Dependency Planning

When breaking down work:
1. Identify which tasks MUST complete before others
2. Use `--deps` flag when creating dependent issues
3. Validate with `bd dep tree <id>` before confirming

**Example prompt to user:**
"Task B depends on Task A. I'll create them with a dependency so B won't start until A completes."
```

### Update: `.github/agents/loop.decompose.agent.md`

Add dependency parsing:

```markdown
# Parsing Dependencies

When parsing PLAN.md:
- Look for: "depends on", "after", "requires", "blocked by"
- Look for: numbered sequences (1, 2, 3...) implying order
- Look for: explicit dependency markers (→, ->, "then")

**Create with:**
```bash
bd create "First task" -t task --json  # bd-1
bd create "Second task" -t task --deps "bd-1" --json  # bd-2
```
```

### Update: `.github/agents/loop.implement.agent.md`

Add spawn mode:

```markdown
# Execution Modes

**Local Mode** (default): Work on issues directly in VS Code.

**Cloud Mode** (via @loop.spawn): Hand off to GitHub/Copilot.

When user says "spawn", "dispatch", "cloud", or "parallel":
→ Handoff to @loop.spawn instead of implementing locally.
```

---

## Implementation Checklist

### Phase 1: Core Infrastructure

- [ ] Create directory `.github/workflows/`
- [ ] Create `.github/agents/loop.spawn.agent.md`
- [ ] Create `.github/agents/loop.monitor.agent.md`  
- [ ] Create `.github/agents/loop.sync.agent.md`
- [ ] Create `.github/workflows/beads-auto-close.yml`
- [ ] Test: Single issue spawn → PR → merge → auto-close

### Phase 2: Wave Execution

- [ ] Test: Multiple independent issues spawn in parallel
- [ ] Test: Dependent issues respect ordering
- [ ] Test: Mixed parallel/serial wave execution
- [ ] Create `loop.wave.agent.md` (orchestrates full wave cycle)

### Phase 3: Agent Updates

- [ ] Update `loop.plan` with dependency guidance
- [ ] Update `loop.decompose` with dependency parsing
- [ ] Update `loop.implement` with cloud mode handoff
- [ ] Update `loop.verify` to work with cloud PRs

### Phase 4: Polish

- [ ] Add beads label management (wave-1, wave-2, etc.)
- [ ] Add stale issue detection and alerting
- [ ] Add conflict detection in planning
- [ ] Document workflow in README

---

## Limitations to Acknowledge

1. **No Deterministic Hooks in GitHub Copilot**: Unlike Claude Code, we can't inject pre/post hooks. The GitHub Action is our "post-merge hook" substitute.

2. **Manual PR Merge Required**: You must visit GitHub to review and merge PRs. This is by design (human in the loop for code review).

3. **Sync Latency**: After merging, you must `git pull` to see updated beads state. `@loop.sync` automates this.

4. **Copilot Assignment Variability**: Copilot may take varying time to respond. No SLA guarantees.

---

## Success Criteria

- [ ] Can spawn 5 independent issues simultaneously
- [ ] Can enforce serial execution for 3-step migration chain
- [ ] Beads state updates automatically on PR merge
- [ ] Entire workflow manageable from VS Code terminal + agents
- [ ] No manual beads updates required (except planning phase)

---

## Next Steps

1. **Approve this plan** or request modifications
2. I'll create the new agents (`loop.spawn`, `loop.monitor`, `loop.sync`)
3. I'll create the GitHub Action workflow
4. We'll test with a simple case (2 independent + 1 dependent issue)
5. Iterate based on results

---

## Appendix: Example Session

```bash
# You've planned work with dependencies
$ bd list --json | jq '.[] | {id, title, status, dependency_count}'
{"id":"bd-a1b","title":"Create schema migration","status":"open","dependency_count":0}
{"id":"bd-c2d","title":"Create user table migration","status":"open","dependency_count":1}
{"id":"bd-e3f","title":"Create posts table migration","status":"open","dependency_count":1}
{"id":"bd-g4h","title":"Write API docs","status":"open","dependency_count":0}

# Wave 1: Ready issues (no blockers)
$ bd ready --json | jq '.[].id'
"bd-a1b"  # Schema migration
"bd-g4h"  # API docs (independent)

# Spawn Wave 1
> @loop.spawn dispatch ready issues

# Agent creates:
#   GitHub Issue #50: [bd-a1b] Create schema migration → @copilot
#   GitHub Issue #51: [bd-g4h] Write API docs → @copilot

# ...time passes, you review and merge PRs #100 and #101...

# Sync
$ git pull
# GitHub Action already closed bd-a1b and bd-g4h

# Wave 2: New ready issues
$ bd ready --json | jq '.[].id'
"bd-c2d"  # User table (now unblocked)

# Spawn Wave 2
> @loop.spawn dispatch ready issues

# Repeat...
```

---

*Plan generated by @loop.plan for contextcrate hub-spoke implementation.*

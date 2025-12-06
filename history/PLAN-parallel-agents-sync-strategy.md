# Plan: Parallel Agent Execution with Beads ↔ GitHub Issues Sync

## Executive Summary

You want to:
1. Use **beads** as the local source of truth for work tracking
2. Use **GitHub Issues** to trigger cloud-based Copilot agents
3. Run agents **in parallel** (multiple issues being worked simultaneously)
4. Keep everything **in sync**

**Critical Problem**: You're right to be concerned. This creates a **dual-source-of-truth anti-pattern** that will inevitably cause drift, confusion, and stale state.

---

## The Fundamental Tension

| System | Strengths | Weaknesses |
|--------|-----------|------------|
| **Beads** | Local, fast, git-native, dependency tracking, hierarchical (parent/child) | No native cloud agent trigger, no GitHub visibility |
| **GitHub Issues** | Copilot assignment, cloud execution, visibility, API-triggerable | No dependency DAG, no local-first workflow, slower |

**The core question**: Which is the source of truth?

---

## Option Analysis

### Option 1: Beads is Truth, GitHub Issues are Ephemeral Work Orders

**Concept**: Beads remains the canonical tracker. GitHub Issues are created *only* to trigger Copilot work, then closed/deleted when done.

```
┌─────────────────────────────────────────────────────────────────┐
│                         WORKFLOW                                │
├─────────────────────────────────────────────────────────────────┤
│  1. Planner creates issues in beads                             │
│  2. When ready to execute, agent creates GitHub Issue           │
│     with body containing beads ID + full context                │
│  3. Assigns @github-copilot to the issue                        │
│  4. Cloud agent works, creates PR                               │
│  5. On PR merge → webhook/action closes beads issue             │
│  6. GitHub Issue is closed (or deleted)                         │
└─────────────────────────────────────────────────────────────────┘
```

**Pros**:
- Single source of truth (beads)
- GitHub Issues are transient work orders, not records
- No long-term sync needed

**Cons**:
- Requires automation to sync state back
- GitHub Issues become "noise" in the repo
- Harder to reason about state during execution

**Sync Risk**: LOW (GitHub Issues are disposable)

---

### Option 2: GitHub Issues is Truth, Beads is Cache/Planning Layer

**Concept**: Use beads only for *planning* (drafting structure, dependencies). Once ready, export to GitHub Issues and use that as truth.

```
┌─────────────────────────────────────────────────────────────────┐
│                         WORKFLOW                                │
├─────────────────────────────────────────────────────────────────┤
│  1. Planner drafts structure in beads (offline, fast)           │
│  2. "Decomposer" exports to GitHub Issues via API               │
│  3. Dependencies become GitHub Issue links/sub-issues           │
│  4. Beads DB is abandoned/archived for this batch               │
│  5. Copilot assigned to GitHub Issues directly                  │
│  6. All tracking happens in GitHub                              │
└─────────────────────────────────────────────────────────────────┘
```

**Pros**:
- GitHub becomes single source of truth
- Full visibility in GitHub
- No sync problem

**Cons**:
- Lose beads' dependency DAG and priority system
- GitHub Issues are slower/clunkier for rapid planning
- Requires abandoning beads' strengths

**Sync Risk**: NONE (beads is discarded after planning)

---

### Option 3: Bidirectional Sync (Danger Zone)

**Concept**: Keep both in sync with bidirectional webhooks/automation.

```
┌─────────────────────────────────────────────────────────────────┐
│                         WORKFLOW                                │
├─────────────────────────────────────────────────────────────────┤
│  beads ←────────────────────────────────→ GitHub Issues         │
│    │                                           │                │
│    └─ bd daemon watches for changes ───────────┘                │
│    └─ GitHub webhook pushes state back ────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

**Pros**:
- Best of both worlds (in theory)

**Cons**:
- **MASSIVE sync complexity**
- Conflict resolution nightmares
- Race conditions with parallel agents
- Stale state guarantees confusion
- Engineering cost is high

**Sync Risk**: EXTREME (this is a distributed systems problem)

**My Recommendation**: Avoid this unless you want to build/maintain sync infrastructure.

---

### Option 4: Hub-and-Spoke with Beads as Orchestrator (Recommended)

**Concept**: Beads is the orchestrator and source of truth. GitHub Issues are created as "execution tickets" with embedded beads metadata. State flows *one direction* until completion.

```
┌─────────────────────────────────────────────────────────────────┐
│                      ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐                                              │
│   │    BEADS     │ ◄─── Source of Truth                         │
│   │  (Local DB)  │                                              │
│   └──────┬───────┘                                              │
│          │                                                      │
│          │ "spawn" (one-way push)                               │
│          ▼                                                      │
│   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │
│   │ GitHub Issue │      │ GitHub Issue │      │ GitHub Issue │  │
│   │   bd-123     │      │   bd-124     │      │   bd-125     │  │
│   │ @copilot     │      │ @copilot     │      │ @copilot     │  │
│   └──────┬───────┘      └──────┬───────┘      └──────┬───────┘  │
│          │                     │                     │          │
│          │ work                │ work                │ work     │
│          ▼                     ▼                     ▼          │
│   ┌──────────────┐      ┌────────────┐       ┌──────────────┐   │
│   │     PR       │      │     PR     │       │     PR       │   │
│   └──────┬───────┘      └──────┬─────┘       └──────┬───────┘   │
│          │                     │                     │          │
│          └─────────────────────┼─────────────────────┘          │
│                                │                                │
│                                ▼                                │
│                    ┌────────────────────┐                       │
│                    │  GitHub Action     │                       │
│                    │  "on: pull_request │                       │
│                    │   merged"          │                       │
│                    │                    │                       │
│                    │  → bd close <id>   │                       │
│                    └────────────────────┘                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Key Insight**: One-way data flow eliminates sync conflicts.

---

## Detailed Design for Option 4

### Phase 1: Spawn Execution Tickets

Add a new agent or command: `loop.spawn` or extend `loop.implement`:

```bash
# For each ready beads issue, create a GitHub Issue
bd ready --json | jq -r '.[].id' | while read id; do
  # Create GitHub Issue with beads context embedded
  gh issue create \
    --title "[bd-$id] $(bd show $id --json | jq -r '.title')" \
    --body "$(bd show $id --json | jq -r '.body')

---
**Beads ID**: $id
**Do not modify this issue manually. Managed by beads.**
" \
    --assignee "@me" \
    --label "copilot-spawn"
  
  # Track the GitHub Issue number in beads
  bd update $id --status in_progress --json
done
```

### Phase 2: Parallel Execution

GitHub Issues with `@copilot` or your custom agent assigned run **in parallel** automatically:

- Each issue is independent
- Copilot creates separate PRs/branches
- No coordination needed (the issues are self-contained)

**Parallelism is free** — GitHub runs each assigned issue independently.

### Phase 3: Completion Callback

Create `.github/workflows/beads-close.yml`:

```yaml
name: Close Beads on PR Merge
on:
  pull_request:
    types: [closed]

jobs:
  close-beads:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Extract beads ID from PR body
        id: extract
        run: |
          # Look for "bd-XXX" pattern in PR body or linked issue
          BEADS_ID=$(echo "${{ github.event.pull_request.body }}" | grep -oP 'bd-\w+' | head -1)
          echo "beads_id=$BEADS_ID" >> $GITHUB_OUTPUT
      
      - name: Close beads issue
        if: steps.extract.outputs.beads_id != ''
        run: |
          # Install bd or use existing
          bd close ${{ steps.extract.outputs.beads_id }} --reason "PR #${{ github.event.pull_request.number }} merged"
          git add .beads/issues.jsonl
          git commit -m "chore: close ${{ steps.extract.outputs.beads_id }}"
          git push
```

### Phase 4: GitHub Issue Cleanup

After beads issue is closed, optionally close the GitHub Issue:

```yaml
      - name: Close GitHub Issue
        run: |
          # Find linked issue and close it
          ISSUE_NUM=$(gh pr view ${{ github.event.pull_request.number }} --json closingIssuesReferences -q '.closingIssuesReferences[0].number')
          if [ -n "$ISSUE_NUM" ]; then
            gh issue close $ISSUE_NUM --comment "Closed by PR merge. Beads issue ${{ steps.extract.outputs.beads_id }} complete."
          fi
```

---

## Addressing Your Specific Questions

### Q: How can I get agents to run in parallel?

**Answer**: You already can. Each GitHub Issue assigned to Copilot runs independently. The parallelism happens at the GitHub Issue level, not the agent level.

```
bd-123 → GitHub Issue #45 → Copilot works → PR #78
bd-124 → GitHub Issue #46 → Copilot works → PR #79  (parallel)
bd-125 → GitHub Issue #47 → Copilot works → PR #80  (parallel)
```

**Key**: Create multiple GitHub Issues simultaneously. They execute in parallel.

### Q: How do I prevent beads ↔ GitHub Issues drift?

**Answer**: Don't sync bidirectionally. Use **one-way flow**:

1. Beads → GitHub Issue (spawn)
2. GitHub Issue → PR (work)
3. PR Merge → Beads (close via Action)

The GitHub Issue is ephemeral. It exists only during execution.

### Q: What about MCP servers?

**Answer**: MCP is useful for *local* agent orchestration (Claude, Copilot Chat). For *cloud* execution, GitHub's issue assignment is simpler. 

Use MCP for:
- Local planning sessions
- Interactive refinement
- Beads queries

Use GitHub Issues for:
- Cloud execution
- Parallel work
- Async operations

---

## Implementation Checklist

### New Agents/Components

- [ ] `loop.spawn.agent.md` — Creates GitHub Issues from ready beads
- [ ] `.github/workflows/beads-close.yml` — Closes beads on PR merge
- [ ] Convention: PR body must include `bd-XXX` reference

### Agent Modifications

- [ ] `loop.implement` — When in "cloud mode", hand off to `loop.spawn` instead of local work
- [ ] `loop.verify` — Can trigger from PR webhook, not just local

### Beads Metadata

Consider adding a `github_issue` field to beads to track the spawned issue:
```bash
bd update bd-123 --meta github_issue=45
```

---

## Risk Assessment

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| GitHub Issue created but Copilot fails | Medium | Add timeout monitoring, manual fallback |
| PR merged but Action fails to close beads | Low | Manual `bd close` as backup, alerting |
| Parallel PRs conflict on same files | Medium | Beads dependencies should prevent this |
| Beads issue closed prematurely | Low | Only Action can close, not manual |

---

## Alternative: Subissues API (Newer GitHub Feature)

GitHub now supports **sub-issues** natively. This could replace beads' parent-child model if you want GitHub as truth:

```bash
gh api repos/{owner}/{repo}/issues/{issue_number}/sub_issues \
  --method POST \
  --field sub_issue_id={sub_issue_number}
```

**Tradeoff**: More GitHub lock-in, but eliminates sync problem entirely.

---

## Recommendation

**Start with Option 4** (Hub-and-Spoke):

1. Keep beads as source of truth for planning
2. Create ephemeral GitHub Issues to trigger cloud work
3. Use GitHub Actions to close beads on PR merge
4. Accept that GitHub Issues are "fire and forget" execution tickets

This gives you:
- ✅ Beads for sophisticated planning/dependencies
- ✅ GitHub for cloud execution/visibility
- ✅ Parallelism (multiple issues = parallel work)
- ✅ No sync conflicts (one-way flow)

---

## Next Steps

If you approve this plan:

1. I'll create `loop.spawn.agent.md`
2. I'll create the GitHub Action workflow
3. I'll update existing loop agents to integrate
4. We can test with a small batch of issues

Let me know your thoughts.

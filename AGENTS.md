# Agent Instructions for Context Crate

## Project Overview

**Context Crate** is a curated library of prompts, agents, meta-prompts, and operating instructions designed to supercharge GitHub Copilot users. The primary purpose of this project is to provide useful prompts and meta-prompts for use by agents and users (GitHub Copilot, Claude Code, etc.).

## Repository Structure

- `.github/prompts/`: Meta-prompts that instruct Copilot to generate downstream prompts or agent behaviors.
- `AGENTS.md`: Operational instructions for agents working on this repository.
- `.beads/`: Internal issue tracking data (JSONL).
- `history/`: Ephemeral AI planning documents.

## Issue Tracking with bd (beads)

**IMPORTANT**: This project uses **bd (beads)** for ALL issue tracking. Do NOT use markdown TODOs, task lists, or other tracking methods. The issue tracker is used to improve the generation of prompts and manage the evolution of the crate.

### Quick Start

**Check for ready work:**
```bash
bd ready --json
bd stale --days 30 --json  # Check for forgotten issues
```

**Create new issues:**
```bash
bd create "Issue title" -t bug|feature|task -p 0-4 --json
bd create "Issue title" -p 1 --deps discovered-from:bd-123 --json
bd create "Subtask" --parent <epic-id> --json
```

**Claim and update:**
```bash
bd update bd-42 --status in_progress --json
bd update bd-42 --priority 1 --json
```

**View issue details:**
```bash
bd show bd-42 --json
```

**Complete work:**
```bash
bd close bd-42 --reason "Completed" --json
```

### Workflow for AI Agents

1. **Check ready work**: `bd ready` shows unblocked issues.
2. **Claim your task**: `bd update <id> --status in_progress`.
3. **Work on it**: Create/edit prompts, update documentation.
4. **Discover new work?** Create linked issue:
   - `bd create "Found gap in prompts" -p 1 --deps discovered-from:<parent-id>`
5. **Complete**: `bd close <id> --reason "Done"`.
6. **Commit together**: **CRITICAL** - Always commit the `.beads/issues.jsonl` file together with the code changes so issue state stays in sync with the repository state.

### Issue Types & Priorities

**Types:**
- `feature`: New prompt or meta-prompt.
- `bug`: Fix in existing prompt or documentation.
- `task`: General work item.
- `chore`: Maintenance.

**Priorities:**
- `0` - Critical
- `1` - High
- `2` - Medium
- `3` - Low
- `4` - Backlog

### Auto-Sync & Git Hooks

`bd` automatically syncs with git.
- Exports to `.beads/issues.jsonl` after changes.
- Imports from JSONL when newer.
- Run `bd sync` at the end of a session to force immediate synchronization.

### MCP Server (Recommended)

If using Claude or MCP-compatible clients, use the `beads-mcp` server for native function calls (`mcp__beads__*`).

### Managing AI-Generated Planning Documents

Store ALL AI-generated planning/design docs (PLAN.md, etc.) in the `history/` directory. Keep the root clean.

### Important Rules

- ✅ Use bd for ALL task tracking.
- ✅ Always use `--json` flag for programmatic use.
- ✅ Link discovered work with `discovered-from` dependencies.
- ✅ Store AI planning docs in `history/` directory.
- ✅ **Commit `.beads/issues.jsonl` with your changes.**

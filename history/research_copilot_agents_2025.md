# Research: GitHub Copilot Agent Capabilities (Late 2024/2025)

## Executive Summary
As of late 2024/early 2025, GitHub Copilot in VS Code has evolved into a more autonomous "Agent Mode" capable of multi-step execution, tool use, and terminal interaction. While true parallel sub-agents are not yet a native feature, the "Planning" capability allows for structured, sequential task execution that mimics a supervisor-worker model.

## 1. Parallelism & Sub-agents
*   **Capability:** Agents cannot currently spin up independent, parallel "sub-agents" in the OS sense (i.e., spawning multiple VS Code instances or background worker processes that report back asynchronously).
*   **Workaround:** The "Planning" feature (Preview) acts as a supervisor. It breaks a complex request into a list of steps (Markdown/JSON plan) and executes them sequentially.
*   **Design Implication:** Your `plan.implement.agent` should not rely on "fire and forget" sub-tasks. Instead, it should generate a linear plan and execute it step-by-step, maintaining state in a file (e.g., `CURRENT_PLAN.md`).

## 2. Git & Worktree Management
*   **Capability:** Agents running in "Agent Mode" have full access to the terminal. They can execute `git` commands just like a human.
*   **Integration:** The Azure Boards integration demonstrates this capability by automatically creating branches and draft PRs.
*   **Design Implication:**
    *   **Worktrees:** Agents *can* effectively manage worktrees to isolate their work. This is a strong pattern for an "Implementation Agent" to avoid polluting the user's current view.
    *   **Context:** When switching worktrees, the agent needs to be aware that the VS Code workspace context might not automatically follow the terminal's directory change unless the workspace folder itself is changed.

## 3. Best Practice: "Implementation Agent"
*   **Concept:** An agent that takes a task from a tracker (like `beads`) and drives it to completion.
*   **Recommended Architecture:**
    1.  **Fetch Task:** Query the task tracker (e.g., `bd show <id>`).
    2.  **Create Plan:** Generate a `history/PLAN-<id>.md` file outlining the steps.
    3.  **Isolate:** Create a git worktree or branch: `git worktree add ...`.
    4.  **Execute Loop:**
        *   Read current step from Plan.
        *   Perform Edit/Command.
        *   Verify (compile/lint).
        *   Update Plan.
    5.  **Submit:** Push branch and mark task as "Review" in tracker.

## 4. Best Practice: "Verification Agent"
*   **Concept:** An agent dedicated to ensuring code quality and correctness.
*   **Recommended Architecture:**
    1.  **Test Generation:** Use Copilot's `@Test` participant to generate unit tests for new code.
    2.  **Iterative Repair:**
        *   Run tests (e.g., `npm test`).
        *   If failure: Feed output back to Copilot with a "Fix this" prompt.
        *   Repeat (Max 3-5 retries).
    3.  **Validation:** Ensure the "Plan" was actually followed by comparing the `PLAN.md` against the git diff.

## Summary for Agent Design

| Feature | `plan.implement.agent` | `verify.work.agent` |
| :--- | :--- | :--- |
| **Core Loop** | Plan -> Act -> Update State | Test -> Analyze -> Fix |
| **State** | `history/PLAN.md` | Test Results / Terminal Output |
| **Git Strategy** | Active Worktree / Feature Branch | Clean Checkout / CI Environment |
| **Tools** | `beads` (Task Tracker), `git`, Editor | Test Runner, Linter, `@Test` |

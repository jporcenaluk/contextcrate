#!/bin/bash
#
# setup-labels.sh - Create required GitHub labels for beads spawning workflow
#
# Usage:
#   ./setup-labels.sh              # Create labels in current repo
#   ./setup-labels.sh owner/repo   # Create labels in specific repo
#
# This script creates the labels needed for the beads → GitHub Issue spawning workflow.
# It uses --force to update existing labels if they already exist.
#

set -e

# Default to current repo
REPO="${1:-}"

# Build repo flag if specified
REPO_FLAG=""
if [ -n "$REPO" ]; then
    REPO_FLAG="-R $REPO"
fi

echo "=============================================="
echo "Setting up GitHub labels for beads workflow"
echo "=============================================="
echo ""

# Check gh is authenticated
if ! gh auth status &>/dev/null; then
    echo "Error: gh CLI is not authenticated."
    echo "Run 'gh auth login' first."
    exit 1
fi

# Function to create label
create_label() {
    local name="$1"
    local description="$2"
    local color="$3"
    
    echo -n "  Creating label '$name'... "
    if gh label create "$name" --description "$description" --color "$color" --force $REPO_FLAG 2>/dev/null; then
        echo "✓"
    else
        echo "✗ (may already exist)"
    fi
}

echo "📌 Core labels:"
create_label "beads-spawned" "Issue spawned from beads task tracker" "0052CC"

echo ""
echo "🌊 Wave labels:"
create_label "wave-1" "Execution wave 1 (no dependencies)" "1D76DB"
create_label "wave-2" "Execution wave 2" "5319E7"
create_label "wave-3" "Execution wave 3" "0E8A16"
create_label "wave-4" "Execution wave 4" "FBCA04"
create_label "wave-5" "Execution wave 5" "D93F0B"

echo ""
echo "⚡ Priority labels:"
create_label "priority-critical" "Priority 0: Critical" "B60205"
create_label "priority-high" "Priority 1: High" "D93F0B"
create_label "priority-medium" "Priority 2: Medium" "FBCA04"
create_label "priority-low" "Priority 3: Low" "0E8A16"
create_label "priority-backlog" "Priority 4: Backlog" "C5DEF5"

echo ""
echo "🏷️ Type labels:"
create_label "type-feature" "New feature" "A2EEEF"
create_label "type-bug" "Bug fix" "D73A4A"
create_label "type-task" "General task" "7057FF"
create_label "type-chore" "Maintenance/chore" "E4E669"
create_label "type-epic" "Epic/parent issue" "3E4B9E"

echo ""
echo "🔄 Status labels:"
create_label "stale" "Issue has no recent activity" "EDEDED"
create_label "blocked" "Issue is blocked by something" "B60205"
create_label "needs-attention" "Needs human attention" "FBCA04"

echo ""
echo "=============================================="
echo "Label setup complete!"
echo ""
echo "You can now run '@loop.spawn' to dispatch beads to GitHub."
echo "=============================================="

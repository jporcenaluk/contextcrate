#!/bin/bash

# This script indexes the prompts in the .github/prompts folder.
# It extracts the name and description from each prompt file
# that starts with 'cc.' and injects them into a cc.index.prompt.md file.

set -e

PROMPT_DIR=".github/prompts"
INDEX_FILE="$PROMPT_DIR/cc.index.prompt.md"

# Create or clear the index file
> "$INDEX_FILE"

# Add frontmatter
echo "---" >> "$INDEX_FILE"
echo "name: \"cc.index\"" >> "$INDEX_FILE"
echo "description: \"An index of all available Copilot Chat prompts for easy reference.\"" >> "$INDEX_FILE"
echo "---" >> "$INDEX_FILE"
echo "" >> "$INDEX_FILE"
echo "\`\`\`prompt" >> "$INDEX_FILE"

echo "# Copilot Chat Prompt Index" >> "$INDEX_FILE"
echo "" >> "$INDEX_FILE"
echo "This file contains a list of all the prompts available to Copilot Chat." >> "$INDEX_FILE"
echo "Each prompt is listed with its name and a brief description." >> "$INDEX_FILE"
echo "" >> "$INDEX_FILE"

# Find all prompt files starting with 'cc.'
for file in $(find "$PROMPT_DIR" -type f -name "cc.*.prompt.md"); do
  # Skip the index file itself
  if [ "$file" == "$INDEX_FILE" ]; then
    continue
  fi

  echo "Processing $file..."
  # Extract name and description from the frontmatter
  name=$(grep -m 1 '^name:' "$file" | sed 's/^name: //')
  description=$(grep -m 1 '^description:' "$file" | sed 's/^description: //')

  # Append to the index file
  echo "## $name" >> "$INDEX_FILE"
  echo "" >> "$INDEX_FILE"
  echo "**Description:** $description" >> "$INDEX_FILE"
  echo "" >> "$INDEX_FILE"
  echo "**File:** \`$(basename "$file")\`" >> "$INDEX_FILE"
  echo "" >> "$INDEX_FILE"
  echo "---" >> "$INDEX_FILE"
  echo "" >> "$INDEX_FILE"
done

echo "\`\`\`" >> "$INDEX_FILE"

echo "Prompt index created at $INDEX_FILE"

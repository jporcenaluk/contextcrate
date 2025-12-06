#!/bin/bash

# Find the next sequential plan number in .github/.cc/plan/
# Plans are expected to start with ###-plan-name/ (e.g., 001-*, 002-*, etc.)
# Returns the next number in sequence (up to 999), handling gaps gracefully

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PLAN_DIR="${1:-$SCRIPT_DIR/../plan}"

if [ ! -d "$PLAN_DIR" ]; then
  echo "001"
  exit 0
fi

# Find all feature directories and extract the numeric prefix
# Filter for directories matching the pattern ###-*
max_num=0
for dir in "$PLAN_DIR"/*; do
  if [ -d "$dir" ] && [[ "$(basename "$dir")" =~ ^[0-9]{3}- ]]; then
    # Extract the numeric prefix (first 3 characters)
    num="$(basename "$dir" | cut -c1-3)"
    
    # Convert to integer for numeric comparison
    num=$((10#$num))
    
    if [ "$num" -gt "$max_num" ]; then
      max_num=$num
    fi
  fi
done

# Calculate next number
next_num=$((max_num + 1))

# Format with zero-padding to 3 digits
printf "%03d\n" "$next_num"

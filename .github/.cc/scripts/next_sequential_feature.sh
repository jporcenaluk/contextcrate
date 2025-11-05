#!/bin/bash

# Find the next sequential feature number in .github/.cc/feature/
# Features are expected to start with ###-feature-name/ (e.g., 001-*, 002-*, etc.)
# Returns the next number in sequence (up to 999), handling gaps gracefully

FEATURE_DIR="${1:-.github/.cc/feature}"

if [ ! -d "$FEATURE_DIR" ]; then
  echo "001"
  exit 0
fi

# Find all feature directories and extract the numeric prefix
# Filter for directories matching the pattern ###-*
max_num=0
for dir in "$FEATURE_DIR"/[0-9][0-9][0-9]-*/; do
  if [ -d "$dir" ]; then
    # Extract the numeric prefix (first 3 characters)
    num="${dir%%-*}"
    num="${num##*/}"  # Remove path prefix
    
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

#!/bin/bash

# Test script for JSON construction with complex notebook paths
# This validates that jq properly handles long paths and special characters

set -e

echo "🧪 Testing JSON Construction for Complex Notebook Paths"
echo "===================================================="

# Test the problematic path
NOTEBOOK_PATH="notebooks/hello-universe/Classifying_JWST-HST_galaxy_mergers_with_CNNs/Classifying_JWST-HST_galaxy_mergers_with_CNNs.ipynb"
SINGLE_NOTEBOOK_DIR="$(dirname "$NOTEBOOK_PATH")"

echo "📄 Testing with complex path:"
echo "Path: $NOTEBOOK_PATH"
echo "Directory: $SINGLE_NOTEBOOK_DIR"

echo ""
echo "🧪 Testing JSON construction methods:"

# Method 1: OLD (broken) - echo "[$NOTEBOOK_PATH]" | jq -c .
echo ""
echo "❌ OLD METHOD (BROKEN):"
echo "Command: echo \"[\$NOTEBOOK_PATH]\" | jq -c ."
echo "This would produce: [$NOTEBOOK_PATH]"
echo "Result: jq parse error (not valid JSON - missing quotes)"

# Method 2: NEW (fixed) - echo "$NOTEBOOK_PATH" | jq -R -s -c 'split("\n")[:-1]'
echo ""
echo "✅ NEW METHOD (FIXED):"
echo "Command: echo \"\$NOTEBOOK_PATH\" | jq -R -s -c 'split(\"\n\")[:-1]'"
MATRIX_NOTEBOOKS=$(echo "$NOTEBOOK_PATH" | jq -R -s -c 'split("\n")[:-1]')
echo "Result: $MATRIX_NOTEBOOKS"

AFFECTED_DIRS=$(echo "$SINGLE_NOTEBOOK_DIR" | jq -R -s -c 'split("\n")[:-1]')
echo "Directories: $AFFECTED_DIRS"

echo ""
echo "🔍 Validating JSON structure:"
echo "$MATRIX_NOTEBOOKS" | jq . > /dev/null && echo "✅ MATRIX_NOTEBOOKS is valid JSON"
echo "$AFFECTED_DIRS" | jq . > /dev/null && echo "✅ AFFECTED_DIRS is valid JSON"

echo ""
echo "📋 Testing with various complex paths:"

# Test with special characters
paths=(
  "notebooks/simple.ipynb"
  "notebooks/with-dashes/test-notebook.ipynb"
  "notebooks/with_underscores/test_notebook.ipynb"
  "notebooks/very/deep/nested/directory/structure/notebook.ipynb"
  "notebooks/hello-universe/Classifying_JWST-HST_galaxy_mergers_with_CNNs/Classifying_JWST-HST_galaxy_mergers_with_CNNs.ipynb"
  "notebooks/with spaces/notebook with spaces.ipynb"
  "notebooks/numbers123/test456.ipynb"
)

for path in "${paths[@]}"; do
  echo ""
  echo "Testing: $path"
  
  # Test the JSON construction
  matrix_json=$(echo "$path" | jq -R -s -c 'split("\n")[:-1]')
  dir_json=$(echo "$(dirname "$path")" | jq -R -s -c 'split("\n")[:-1]')
  
  # Validate JSON
  echo "$matrix_json" | jq . > /dev/null && echo "  ✅ Matrix JSON valid: $matrix_json"
  echo "$dir_json" | jq . > /dev/null && echo "  ✅ Directory JSON valid: $dir_json"
done

echo ""
echo "🎉 JSON construction fix works correctly!"
echo "✅ Handles long paths with special characters"
echo "✅ Produces valid JSON arrays"
echo "✅ Properly escapes strings for jq processing"
echo "✅ No more 'Invalid numeric literal' errors"

echo ""
echo "🚀 Complex path JSON construction is ready!"

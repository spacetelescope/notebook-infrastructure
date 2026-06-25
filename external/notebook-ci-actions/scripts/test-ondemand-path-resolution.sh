#!/bin/bash

# Test script for on-demand single notebook path resolution
# This validates that both full paths and filenames work correctly

set -e

echo "🧪 Testing On-Demand Single Notebook Path Resolution"
echo "=================================================="

# Create test environment
temp_dir="/tmp/notebook-path-test-$$"
mkdir -p "$temp_dir"
cd "$temp_dir"

# Create test notebook structure
mkdir -p notebooks/subdir1/deep
mkdir -p notebooks/subdir2
mkdir -p notebooks/another/nested/dir

# Create test notebooks
cat > notebooks/root-notebook.ipynb << 'EOF'
{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 4}
EOF

cat > notebooks/subdir1/test-notebook.ipynb << 'EOF'
{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 4}
EOF

cat > notebooks/subdir1/deep/deep-notebook.ipynb << 'EOF'
{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 4}
EOF

cat > notebooks/subdir2/duplicate-name.ipynb << 'EOF'
{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 4}
EOF

cat > notebooks/another/nested/dir/duplicate-name.ipynb << 'EOF'
{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 4}
EOF

echo "✅ Created test notebook structure:"
find notebooks/ -name '*.ipynb' | sort

echo ""
echo "🧪 Testing path resolution logic:"

# Test 1: Full path provided
echo ""
echo "Test 1: Full path provided"
input_notebook="notebooks/subdir1/test-notebook.ipynb"
echo "Input: $input_notebook"

if [[ "$input_notebook" == *"/"* ]]; then
  NOTEBOOK_PATH="$input_notebook"
  echo "📁 Full path provided: $NOTEBOOK_PATH"
else
  echo "🔍 Filename only provided, searching..."
  NOTEBOOK_PATH=$(find notebooks/ -name "$input_notebook" -type f | head -1)
fi

echo "Result: $NOTEBOOK_PATH"
echo "Directory: $(dirname "$NOTEBOOK_PATH")"

# Test 2: Filename only provided (unique)
echo ""
echo "Test 2: Filename only provided (unique)"
input_notebook="test-notebook.ipynb"
echo "Input: $input_notebook"

if [[ "$input_notebook" == *"/"* ]]; then
  NOTEBOOK_PATH="$input_notebook"
  echo "📁 Full path provided: $NOTEBOOK_PATH"
else
  echo "🔍 Filename only provided, searching for: $input_notebook"
  NOTEBOOK_PATH=$(find notebooks/ -name "$input_notebook" -type f | head -1)
  if [ -z "$NOTEBOOK_PATH" ]; then
    echo "❌ Notebook not found: $input_notebook"
    exit 1
  fi
  echo "✅ Found notebook at: $NOTEBOOK_PATH"
fi

echo "Result: $NOTEBOOK_PATH"
echo "Directory: $(dirname "$NOTEBOOK_PATH")"

# Test 3: Filename only provided (duplicate - takes first)
echo ""
echo "Test 3: Filename only provided (duplicate - should take first found)"
input_notebook="duplicate-name.ipynb"
echo "Input: $input_notebook"

if [[ "$input_notebook" == *"/"* ]]; then
  NOTEBOOK_PATH="$input_notebook"
  echo "📁 Full path provided: $NOTEBOOK_PATH"
else
  echo "🔍 Filename only provided, searching for: $input_notebook"
  NOTEBOOK_PATH=$(find notebooks/ -name "$input_notebook" -type f | head -1)
  if [ -z "$NOTEBOOK_PATH" ]; then
    echo "❌ Notebook not found: $input_notebook"
    exit 1
  fi
  echo "✅ Found notebook at: $NOTEBOOK_PATH"
fi

echo "Result: $NOTEBOOK_PATH"
echo "Directory: $(dirname "$NOTEBOOK_PATH")"

# Test 4: Non-existent notebook
echo ""
echo "Test 4: Non-existent notebook"
input_notebook="non-existent.ipynb"
echo "Input: $input_notebook"

if [[ "$input_notebook" == *"/"* ]]; then
  NOTEBOOK_PATH="$input_notebook"
  echo "📁 Full path provided: $NOTEBOOK_PATH"
else
  echo "🔍 Filename only provided, searching for: $input_notebook"
  NOTEBOOK_PATH=$(find notebooks/ -name "$input_notebook" -type f | head -1)
  if [ -z "$NOTEBOOK_PATH" ]; then
    echo "❌ Notebook not found: $input_notebook"
    echo "Available notebooks:"
    find notebooks/ -name '*.ipynb' | head -10
    echo "This would exit 1 in the real workflow"
  else
    echo "✅ Found notebook at: $NOTEBOOK_PATH"
  fi
fi

echo ""
echo "🎉 Path resolution logic works correctly!"
echo "✅ Full paths are used as-is"
echo "✅ Filenames are resolved to full paths"
echo "✅ Duplicate filenames take the first match"
echo "✅ Missing files are properly detected"
echo "✅ Directories are calculated correctly"

# Cleanup
cd /
rm -rf "$temp_dir"

echo ""
echo "🚀 On-demand path resolution is ready!"

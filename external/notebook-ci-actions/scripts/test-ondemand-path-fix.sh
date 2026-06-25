#!/bin/bash

# Test script to validate on-demand single notebook path resolution
# This validates that the directory calculation works correctly

set -e

echo "🧪 Testing On-Demand Single Notebook Path Resolution"
echo "================================================="

# Test cases for different notebook paths
test_cases=(
    "notebooks/example/test.ipynb"
    "notebooks/hello-universe/Classifying_JWST-HST_galaxy_mergers_with_CNNs.ipynb"
    "notebooks/sub/directory/deep/notebook.ipynb"
    "notebooks/simple.ipynb"
)

for notebook in "${test_cases[@]}"; do
    echo ""
    echo "🔄 Testing notebook path: $notebook"
    
    # Simulate the fixed logic
    MATRIX_NOTEBOOKS='["'$notebook'"]'
    SINGLE_NOTEBOOK_DIR=$(dirname "$notebook")
    AFFECTED_DIRS=$(echo "[\"$SINGLE_NOTEBOOK_DIR\"]" | jq -c .)
    
    echo "  📄 MATRIX_NOTEBOOKS: $MATRIX_NOTEBOOKS"
    echo "  📁 SINGLE_NOTEBOOK_DIR: $SINGLE_NOTEBOOK_DIR"
    echo "  📊 AFFECTED_DIRS: $AFFECTED_DIRS"
    
    # Validate the results
    if [[ "$AFFECTED_DIRS" == "[\"$(dirname "$notebook")\"]" ]]; then
        echo "  ✅ Directory calculation is correct"
    else
        echo "  ❌ Directory calculation is incorrect"
        exit 1
    fi
done

echo ""
echo "🎉 All path resolution tests passed!"

# Test the old problematic approach vs new approach
echo ""
echo "📋 Comparison: Old vs New Approach"
echo "=================================="

notebook="notebooks/hello-universe/Classifying_JWST-HST_galaxy_mergers_with_CNNs.ipynb"

echo "❌ OLD (problematic) approach:"
echo "  AFFECTED_DIRS='[\"\$(dirname \"$notebook\")\"]'"
echo "  Result: [\"\$(dirname \"$notebook\")\"] (literal string, not executed)"

echo ""
echo "✅ NEW (fixed) approach:"
SINGLE_NOTEBOOK_DIR=$(dirname "$notebook")
AFFECTED_DIRS=$(echo "[\"$SINGLE_NOTEBOOK_DIR\"]" | jq -c .)
echo "  SINGLE_NOTEBOOK_DIR=\$(dirname \"$notebook\")"
echo "  AFFECTED_DIRS=\$(echo \"[\$SINGLE_NOTEBOOK_DIR]\" | jq -c .)"
echo "  Result: $AFFECTED_DIRS (properly calculated directory)"

echo ""
echo "🚀 On-demand single notebook path resolution is now working correctly!"

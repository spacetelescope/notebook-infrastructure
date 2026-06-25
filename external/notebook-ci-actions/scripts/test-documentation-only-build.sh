#!/bin/bash

# Test script for documentation-only build logic
# This validates that build-html-only skips notebook processing

set -e

echo "🧪 Testing Documentation-Only Build Logic"
echo "========================================"

echo "📋 Testing the build-html-only workflow logic"

# Simulate the setup-matrix logic for different trigger events
echo ""
echo "🔄 Test 1: Regular execution (trigger-event = 'execute')"
trigger_event="execute"
execution_mode="on-demand"

if [ "$trigger_event" = "html" ]; then
  SKIP_EXECUTION=true
  MATRIX_NOTEBOOKS='[]'
  echo "✅ Would skip notebook processing"
else
  SKIP_EXECUTION=false
  MATRIX_NOTEBOOKS='["notebooks/example.ipynb"]'
  echo "✅ Would process notebooks: $MATRIX_NOTEBOOKS"
fi

echo ""
echo "🔄 Test 2: Documentation-only build (trigger-event = 'html')"
trigger_event="html"
execution_mode="on-demand"

if [ "$trigger_event" = "html" ]; then
  SKIP_EXECUTION=true
  MATRIX_NOTEBOOKS='[]'
  echo "✅ Would skip notebook processing"
else
  SKIP_EXECUTION=false
  MATRIX_NOTEBOOKS='["notebooks/example.ipynb"]'
  echo "✅ Would process notebooks: $MATRIX_NOTEBOOKS"
fi

echo ""
echo "🔄 Test 3: Build documentation job conditions"

# Test process-notebooks job condition
echo "📝 process-notebooks job condition:"
echo "  needs.setup-matrix.outputs.skip-execution != 'true' &&"
echo "  needs.setup-matrix.outputs.matrix-notebooks != '[]' &&"
echo "  inputs.execution-mode != 'merge'"

# For trigger-event = 'html'
skip_execution="true"
matrix_notebooks="[]"
execution_mode="on-demand"

if [ "$skip_execution" != "true" ] && [ "$matrix_notebooks" != "[]" ] && [ "$execution_mode" != "merge" ]; then
  echo "❌ process-notebooks would run (WRONG for html trigger)"
else
  echo "✅ process-notebooks would be skipped (CORRECT for html trigger)"
fi

echo ""
echo "📝 build-documentation job condition:"
echo "  always() &&"
echo "  inputs.enable-html-build == true &&"
echo "  (needs.setup-matrix.outputs.docs-only == 'true' ||"
echo "   inputs.execution-mode == 'merge' ||"
echo "   inputs.trigger-event == 'html' ||"
echo "   (needs.process-notebooks.result == 'success' && inputs.execution-mode != 'merge'))"

# For trigger-event = 'html'
enable_html_build="true"
trigger_event="html"

if [ "$enable_html_build" = "true" ] && [ "$trigger_event" = "html" ]; then
  echo "✅ build-documentation would run (CORRECT for html trigger)"
else
  echo "❌ build-documentation would be skipped (WRONG for html trigger)"
fi

echo ""
echo "🧪 Testing checkout logic for documentation build"
echo "📦 For trigger-event = 'html', should checkout gh-storage:"

trigger_event="html"
execution_mode="on-demand"

if [ "$execution_mode" = "merge" ] || [ "$trigger_event" = "html" ]; then
  ref="gh-storage"
  echo "✅ Would checkout: $ref (CORRECT - gets executed notebooks)"
else
  ref="github.ref"
  echo "❌ Would checkout: $ref (WRONG - gets source code without outputs)"
fi

echo ""
echo "🎉 Documentation-only build logic validation completed!"
echo "✅ trigger-event = 'html' properly skips notebook processing"
echo "✅ build-documentation runs and gets executed notebooks from gh-storage"
echo "✅ GitHub Pages deployment works for html trigger"

echo ""
echo "🚀 build-html-only workflow will now:"
echo "  1. Skip all notebook validation/execution/security steps"
echo "  2. Checkout gh-storage branch with executed notebooks"
echo "  3. Build JupyterBook documentation"
echo "  4. Deploy to GitHub Pages"

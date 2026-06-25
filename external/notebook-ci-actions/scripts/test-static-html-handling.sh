#!/bin/bash

# Test script to demonstrate static HTML file handling in merge mode
# This shows how the enhanced workflow ensures static files are available

echo "🧪 Testing Static HTML File Handling in Merge Mode"
echo "================================================="

# Create a test scenario
mkdir -p test-repo
cd test-repo
git init

echo ""
echo "📋 Setting up test scenario:"
echo "1. Main branch has static HTML files and _toc.yml"
echo "2. gh-storage branch has only executed notebooks"
echo "3. Merge workflow needs to build docs with both"

# Create main branch content
mkdir -p docs notebooks/examples
echo "<h1>Overview Page</h1><p>This is updated content!</p>" > docs/overview.html
echo "# Getting Started" > docs/getting-started.md
cat > _toc.yml << 'EOF'
format: jb-book
root: index
chapters:
- file: docs/overview
- file: docs/getting-started  
- file: notebooks/examples/analysis
EOF

echo "Updated main content" > index.md
git add .
git commit -m "Main branch with static files"

# Create gh-storage branch with only notebooks
git checkout --orphan gh-storage
git rm -rf .
mkdir -p notebooks/examples
echo '{"cells": [{"cell_type": "markdown", "source": "# Analysis Notebook"}]}' > notebooks/examples/analysis.ipynb
git add .
git commit -m "Executed notebooks only"

# Back to main
git checkout main

echo ""
echo "📁 Current repository structure:"
echo "Main branch:"
find . -type f | grep -v .git | sort

echo ""
git checkout gh-storage
echo "gh-storage branch:"
find . -type f | grep -v .git | sort

echo ""
echo "🔍 Testing the enhanced merge logic:"
echo "======================================"

git checkout gh-storage
echo "✅ Switched to gh-storage branch (simulating workflow)"

echo ""
echo "📦 Current gh-storage content (before merge):"
ls -la

echo ""
echo "🔄 Merging static files from main branch (simulating workflow fix):"

# Simulate the workflow commands
git checkout main -- docs/ 2>/dev/null || echo "No docs/ directory in main"
git checkout main -- *.md 2>/dev/null || echo "No markdown files in main root"  
git checkout main -- _config.yml 2>/dev/null || echo "No _config.yml in main"
git checkout main -- _toc.yml 2>/dev/null || echo "No _toc.yml in main"
git checkout main -- *.html 2>/dev/null || echo "No HTML files in main root"

echo ""
echo "📦 Final content available for Jupyter Book build:"
find . -type f | grep -v .git | sort

echo ""
echo "✅ Analysis Results:"
echo "==================="

if [ -f "docs/overview.html" ]; then
    echo "✅ Static HTML file available: docs/overview.html"
    echo "   Content: $(cat docs/overview.html)"
else
    echo "❌ Static HTML file missing!"
fi

if [ -f "_toc.yml" ]; then
    echo "✅ Table of contents available: _toc.yml"
else
    echo "❌ Table of contents missing!"
fi

if [ -f "notebooks/examples/analysis.ipynb" ]; then
    echo "✅ Executed notebook available: notebooks/examples/analysis.ipynb"
else
    echo "❌ Executed notebook missing!"
fi

echo ""
echo "🎯 Expected Workflow Behavior:"
echo "=============================="
echo "1. PR Mode (docs-only): ✅ Uses current branch - HTML files available"
echo "2. Merge Mode (before fix): ❌ Uses gh-storage only - HTML files missing"  
echo "3. Merge Mode (after fix): ✅ Uses gh-storage + merges static files from main"
echo ""
echo "📖 Jupyter Book will now have access to:"
echo "   - Executed notebooks from gh-storage"
echo "   - Updated static HTML files from main branch"
echo "   - Current _toc.yml configuration"
echo ""
echo "🚀 Result: Complete documentation with both executed notebooks AND updated static content!"

# Cleanup
cd ..
rm -rf test-repo

#!/bin/bash

# Release Preparation Script
# This script cleans up the repository for release by organizing development files

set -e

echo "🧹 Preparing repository for release..."

# Create development directories if they don't exist
mkdir -p dev/{status,testing,implementation,notes}
mkdir -p archive

# Move JupyterBook development files
if [ -f "_config.yml" ] && grep -q "Local Test" "_config.yml"; then
    echo "📚 Moving development JupyterBook config to dev/..."
    mv _config.yml dev/ 2>/dev/null || true
    mv _toc.yml dev/ 2>/dev/null || true
fi

echo "📁 Organizing development files..."

# Move status and fix files
find . -maxdepth 1 -name "*FIX*.md" -exec mv {} dev/status/ \; 2>/dev/null || true
find . -maxdepth 1 -name "*COMPLETE*.md" -exec mv {} dev/status/ \; 2>/dev/null || true  
find . -maxdepth 1 -name "*WORKFLOW*.md" -exec mv {} dev/status/ \; 2>/dev/null || true
find . -maxdepth 1 -name "*READY*.md" -exec mv {} dev/status/ \; 2>/dev/null || true

# Move implementation files
find . -maxdepth 1 -name "*IMPLEMENTATION*.md" -exec mv {} dev/implementation/ \; 2>/dev/null || true
find . -maxdepth 1 -name "JIRA_TASK*.md" -exec mv {} dev/implementation/ \; 2>/dev/null || true

# Move testing files  
find . -maxdepth 1 -name "*TEST*.md" -exec mv {} dev/testing/ \; 2>/dev/null || true

# Move other development files
find . -maxdepth 1 -name "*SUMMARY*.md" -exec mv {} dev/status/ \; 2>/dev/null || true
find . -maxdepth 1 -name "*CLEANUP*.md" -exec mv {} dev/status/ \; 2>/dev/null || true

# Organize development scripts
mkdir -p dev/scripts
mv scripts/test-*-fix.sh dev/scripts/ 2>/dev/null || true
mv scripts/test-*-deprecation*.sh dev/scripts/ 2>/dev/null || true  
mv scripts/test-*-storage*.sh dev/scripts/ 2>/dev/null || true
mv scripts/test-*-summary*.sh dev/scripts/ 2>/dev/null || true
mv scripts/diagnose-*.sh dev/scripts/ 2>/dev/null || true
mv scripts/validate-*-fix.sh dev/scripts/ 2>/dev/null || true
mv scripts/cleanup-*.sh dev/scripts/ 2>/dev/null || true
mv scripts/deploy-to-*.sh dev/scripts/ 2>/dev/null || true
mv scripts/*.backup dev/scripts/ 2>/dev/null || true
mv scripts/.actrc scripts/.env dev/scripts/ 2>/dev/null || true
[ -d "scripts/.github" ] && mv scripts/.github dev/scripts/ 2>/dev/null || true

# Move version-specific files
mv README-*.md dev/notes/ 2>/dev/null || true

# Move backup files to archive
mkdir -p archive/{docs,examples}
mv docs/*-old.* archive/docs/ 2>/dev/null || true
mv examples/*-old.* archive/examples/ 2>/dev/null || true
find . -maxdepth 1 -name "*-backup.*" -exec mv {} archive/ \; 2>/dev/null || true
find . -maxdepth 1 -name "*.bak" -exec mv {} archive/ \; 2>/dev/null || true

echo "📊 Release directory structure:"
echo "📦 Production files (included in release):"
echo "  ✅ README.md"
echo "  ✅ .github/workflows/"
echo "  ✅ examples/"
echo "  ✅ docs/"
echo "  ✅ scripts/ (production scripts only)"
echo ""
echo "🔧 Development files (excluded from release):"
echo "  📁 dev/ - Development documentation and status files"
echo "  📁 dev/scripts/ - Development and testing scripts"
echo "  📁 archive/ - Archived historical files"
echo "  📁 _build/ - Generated documentation builds"
echo ""

# Count files in each category
PROD_FILES=$(find . -maxdepth 1 -name "*.md" -not -path "./dev/*" -not -path "./archive/*" | wc -l)
DEV_FILES=$(find dev/ -name "*.md" 2>/dev/null | wc -l || echo "0")
PROD_SCRIPTS=$(find scripts/ -name "*.sh" -not -name "test-*-fix.sh" -not -name "test-*-deprecation*.sh" -not -name "diagnose-*.sh" 2>/dev/null | wc -l || echo "0")
DEV_SCRIPTS=$(find dev/scripts/ -name "*.sh" 2>/dev/null | wc -l || echo "0")

echo "📈 File organization summary:"
echo "  Production docs: $PROD_FILES files"
echo "  Production scripts: $PROD_SCRIPTS files" 
echo "  Development docs: $DEV_FILES files"
echo "  Development scripts: $DEV_SCRIPTS files"
echo ""

echo "✅ Repository is ready for release!"
echo ""
echo "💡 To create a clean release:"
echo "   git add ."
echo "   git commit -m 'Organize development files for release'"
echo "   git tag v3.0.0"
echo "   git push origin v3.0.0"

#!/bin/bash

# Script to update all repository references from mgough-970/dev-actions to spacetelescope/notebook-ci-actions
# Also updates version tags from @dev-actions-v2 to @v3

set -e

echo "=========================================="
echo "Repository Reference Update Script"
echo "=========================================="
echo "From: mgough-970/dev-actions"
echo "To: spacetelescope/notebook-ci-actions"
echo "Version: @dev-actions-v2 → @v3"
echo ""

# Function to update references in a file
update_file_references() {
    local file="$1"
    local updated=false
    
    if [[ -f "$file" ]]; then
        # Create backup
        cp "$file" "$file.backup"
        
        # Update repository references
        if grep -q "mgough-970/dev-actions" "$file" 2>/dev/null; then
            sed -i 's|mgough-970/dev-actions|spacetelescope/notebook-ci-actions|g' "$file"
            updated=true
        fi
        
        # Update version tags
        if grep -q "@dev-actions-v2" "$file" 2>/dev/null; then
            sed -i 's|@dev-actions-v2|@v3|g' "$file"
            updated=true
        fi
        
        # Update specific old patterns that might still exist
        if grep -q "mgrough-970/dev-actions" "$file" 2>/dev/null; then
            sed -i 's|mgrough-970/dev-actions|spacetelescope/notebook-ci-actions|g' "$file"
            updated=true
        fi
        
        if $updated; then
            echo "✅ Updated: $file"
        else
            # Remove backup if no changes were made
            rm "$file.backup"
        fi
    fi
}

# Function to find and update all relevant files
update_all_references() {
    echo "Updating repository references in all files..."
    echo ""
    
    # Update markdown files
    echo "📝 Updating documentation files..."
    find . -name "*.md" -not -path "./_build/*" -not -path "./dev/*" -not -path "./archive/*" | while read -r file; do
        update_file_references "$file"
    done
    
    # Update YAML workflow files
    echo ""
    echo "⚙️ Updating workflow files..."
    find . -name "*.yml" -o -name "*.yaml" | while read -r file; do
        update_file_references "$file"
    done
    
    # Update shell scripts
    echo ""
    echo "🔧 Updating shell scripts..."
    find . -name "*.sh" -not -path "./scripts/update-repository-references.sh" | while read -r file; do
        update_file_references "$file"
    done
    
    # Update other text files that might contain references
    echo ""
    echo "📄 Updating other text files..."
    for file in README* QUICK_START* *.txt *.json; do
        if [[ -f "$file" ]]; then
            update_file_references "$file"
        fi
    done
}

# Function to verify updates
verify_updates() {
    echo ""
    echo "🔍 Verifying updates..."
    
    # Check for remaining old references
    echo "Checking for remaining 'mgough-970/dev-actions' references..."
    old_refs=$(grep -r "mgough-970/dev-actions" . --exclude-dir=_build --exclude-dir=dev --exclude-dir=archive --exclude="*.backup" 2>/dev/null | wc -l)
    
    echo "Checking for remaining 'mgrough-970/dev-actions' references..."
    old_refs2=$(grep -r "mgrough-970/dev-actions" . --exclude-dir=_build --exclude-dir=dev --exclude-dir=archive --exclude="*.backup" 2>/dev/null | wc -l)
    
    echo "Checking for remaining '@dev-actions-v2' references..."
    old_versions=$(grep -r "@dev-actions-v2" . --exclude-dir=_build --exclude-dir=dev --exclude-dir=archive --exclude="*.backup" 2>/dev/null | wc -l)
    
    echo "Results:"
    echo "- mgough-970/dev-actions references: $old_refs"
    echo "- mgrough-970/dev-actions references: $old_refs2"
    echo "- @dev-actions-v2 references: $old_versions"
    
    if [[ $old_refs -gt 0 ]] || [[ $old_refs2 -gt 0 ]] || [[ $old_versions -gt 0 ]]; then
        echo ""
        echo "⚠️ Some old references may still exist. Manual review recommended."
        if [[ $old_refs -gt 0 ]]; then
            echo "Remaining mgough-970/dev-actions references:"
            grep -r "mgough-970/dev-actions" . --exclude-dir=_build --exclude-dir=dev --exclude-dir=archive --exclude="*.backup" 2>/dev/null | head -10
        fi
        if [[ $old_refs2 -gt 0 ]]; then
            echo "Remaining mgrough-970/dev-actions references:"
            grep -r "mgrough-970/dev-actions" . --exclude-dir=_build --exclude-dir=dev --exclude-dir=archive --exclude="*.backup" 2>/dev/null | head -10
        fi
        if [[ $old_versions -gt 0 ]]; then
            echo "Remaining @dev-actions-v2 references:"
            grep -r "@dev-actions-v2" . --exclude-dir=_build --exclude-dir=dev --exclude-dir=archive --exclude="*.backup" 2>/dev/null | head -10
        fi
    else
        echo "✅ All references have been successfully updated!"
    fi
}

# Function to clean up backup files
cleanup_backups() {
    echo ""
    echo "🧹 Cleaning up backup files..."
    find . -name "*.backup" -delete
    echo "✅ Backup files removed"
}

# Main execution
main() {
    # Change to repository root
    cd "$(dirname "$0")/.."
    
    echo "Working directory: $(pwd)"
    echo ""
    
    # Perform updates
    update_all_references
    
    # Verify results
    verify_updates
    
    # Ask user if they want to clean up backups
    echo ""
    read -p "Clean up backup files? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cleanup_backups
    else
        echo "Backup files preserved for review"
    fi
    
    echo ""
    echo "=========================================="
    echo "Reference update completed!"
    echo "=========================================="
    echo ""
    echo "Summary of changes:"
    echo "- Repository: mgough-970/dev-actions → spacetelescope/notebook-ci-actions"
    echo "- Version tags: @dev-actions-v2 → @v3"
    echo ""
    echo "Next steps:"
    echo "1. Review the changes: git diff"
    echo "2. Test the workflows if needed"
    echo "3. Commit the changes: git add . && git commit -m 'Update references to spacetelescope/notebook-ci-actions@v3'"
    echo "4. Create and push the v3.0.0 release"
}

# Run main function
main "$@"

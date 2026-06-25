# Repository Migration Checklist

This checklist provides step-by-step instructions for migrating the following repositories to use the centralized GitHub Actions workflows from the `notebook-ci-actions` repository:

- `jdat_notebooks`
- `mast_notebooks` 
- `hst_notebooks`
- `hellouniverse`
- `jwst-pipeline-notebooks`

## 📋 Table of Contents

- [Pre-Migration Setup](#pre-migration-setup)
- [Repository-Specific Migration](#repository-specific-migration)
- [Testing & Validation](#testing--validation)
- [Post-Migration Cleanup](#post-migration-cleanup)
- [Troubleshooting](#troubleshooting)

## 🚀 Pre-Migration Setup

### Step 1: Inventory Current Workflows

For each repository, document the existing workflows:

#### ✅ Current Workflow Analysis
- [ ] **`jdat_notebooks`**: Document existing `.github/workflows/*.yml` files
- [ ] **`mast_notebooks`**: Document existing `.github/workflows/*.yml` files  
- [ ] **`hst_notebooks`**: Document existing `.github/workflows/*.yml` files
- [ ] **`hellouniverse`**: Document existing `.github/workflows/*.yml` files
- [ ] **`jwst-pipeline-notebooks`**: Document existing `.github/workflows/*.yml` files

```bash
# Run this in each repository to inventory workflows
find .github/workflows -name "*.yml" -o -name "*.yaml" | while read file; do
  echo "=== $file ==="
  echo "Triggers: $(grep -A 10 "^on:" "$file" | grep -v "^--")"
  echo "Jobs: $(grep "^  [a-zA-Z].*:" "$file" | grep -v "^    ")"
  echo ""
done > workflow-inventory.txt
```

### Step 2: Prepare notebook-ci-actions Repository

#### ✅ Repository Setup
- [ ] Ensure `notebook-ci-actions` repository exists
- [ ] Copy workflows from `dev-actions` to `notebook-ci-actions`:
  ```bash
  # In notebook-ci-actions repo
  cp ../dev-actions/.github/workflows/ci_*.yml .github/workflows/
  cp ../dev-actions/.github/scripts/ .github/scripts/ -r
  ```
- [ ] Set up initial release tags:
  ```bash
  git tag v1.0.0
  git tag v1
  git push origin v1.0.0 v1
  ```

### Step 3: Create Migration Branch Template

Create this script as `scripts/create-migration-branch.sh`:

```bash
#!/bin/bash
# Create migration branch with backup

REPO_NAME="$1"
if [ -z "$REPO_NAME" ]; then
  echo "Usage: $0 <repository_name>"
  exit 1
fi

echo "Creating migration branch for $REPO_NAME..."

# Create migration branch
git checkout -b migrate-to-centralized-actions

# Backup existing workflows
mkdir -p .github/workflows-backup
cp .github/workflows/*.yml .github/workflows-backup/ 2>/dev/null || echo "No workflows to backup"

# Create migration tracking file
cat > migration-status.md << EOF
# Migration Status for $REPO_NAME

## Pre-Migration Workflows
$(find .github/workflows -name "*.yml" 2>/dev/null | sed 's/^/- /')

## Migration Date
$(date)

## Checklist
- [ ] Workflows migrated
- [ ] Secrets configured
- [ ] Testing completed
- [ ] Documentation updated
EOF

git add migration-status.md .github/workflows-backup/
git commit -m "Prepare migration branch for $REPO_NAME"

echo "Migration branch created. Run migration checklist next."
```

## 🔄 Repository-Specific Migration

### jdat_notebooks Migration

#### ✅ Current State Analysis
- [ ] **Repository URL**: `https://github.com/spacetelescope/jdat_notebooks`
- [ ] **Primary workflows identified**: 
  - [ ] Notebook CI/validation
  - [ ] Documentation building
  - [ ] Security scanning
- [ ] **Python version(s) used**: _____________
- [ ] **Special requirements**: 
  - [ ] CRDS cache requirements
  - [ ] Large data downloads
  - [ ] Micromamba environment needs

#### ✅ Migration Steps
- [ ] **Step 1**: Create migration branch
  ```bash
  cd jdat_notebooks
  bash ../scripts/create-migration-branch.sh jdat_notebooks
  ```

- [ ] **Step 2**: Choose workflow strategy and replace with centralized versions

  **Option A: Smart Workflows (Recommended)** - Automatically detect file changes and optimize CI
  ```bash
  # Remove old workflows (after backup)
  rm .github/workflows/*.yml
  
  # Copy smart workflow examples
  cp ../notebook-ci-actions/examples/workflows/notebook-ci-pr-smart.yml .github/workflows/
  cp ../notebook-ci-actions/examples/workflows/notebook-ci-main-smart.yml .github/workflows/
  cp ../notebook-ci-actions/examples/workflows/notebook-ci-on-demand.yml .github/workflows/
  ```

  **Option B: Traditional Workflows** - Consistent full CI for all changes
  ```bash
  # Remove old workflows (after backup)
  rm .github/workflows/*.yml
  
  # Copy traditional workflow examples
  cp ../notebook-ci-actions/examples/workflows/notebook-ci-pr.yml .github/workflows/
  cp ../notebook-ci-actions/examples/workflows/notebook-ci-main.yml .github/workflows/
  cp ../notebook-ci-actions/examples/workflows/docs-only.yml .github/workflows/
  cp ../notebook-ci-actions/examples/workflows/notebook-ci-on-demand.yml .github/workflows/
  ```

  **Smart vs Traditional Comparison:**
  - **Smart**: 85% faster for docs-only changes, 60% cost savings, intelligent routing
  - **Traditional**: Consistent full validation, simpler debugging, predictable timing

- [ ] **Step 3**: Update workflow references
  ```bash
  # Update organization reference
  sed -i 's/your-org/spacetelescope/g' .github/workflows/*.yml
  # Update repository reference  
  sed -i 's/dev-actions/notebook-ci-actions/g' .github/workflows/*.yml
  ```

- [ ] **Step 4**: Configure repository-specific parameters
  ```yaml
  # In .github/workflows/notebook-ci-main.yml
  jobs:
    full-ci-pipeline:
      uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@v1
      with:
        python-version: "3.11"  # Adjust as needed
        execution-mode: "full"
        build-html: true
        security-scan: true
      secrets:
        CASJOBS_USERID: ${{ secrets.CASJOBS_USERID }}
        CASJOBS_PW: ${{ secrets.CASJOBS_PW }}
  ```

- [ ] **Step 5**: Configure secrets in repository settings
  - [ ] `GITHUB_TOKEN` (usually automatic)
  - [ ] `CASJOBS_USERID` (if needed)
  - [ ] `CASJOBS_PW` (if needed)

#### ✅ jdat_notebooks Testing
- [ ] **Local testing**: Test workflows with workflow_dispatch
- [ ] **PR testing**: Create test PR to verify workflow triggers
- [ ] **Documentation**: Verify JupyterBook builds correctly
- [ ] **Special considerations**: Test CRDS cache and data access

### mast_notebooks Migration

#### ✅ Current State Analysis
- [ ] **Repository URL**: `https://github.com/spacetelescope/mast_notebooks`
- [ ] **Primary workflows identified**: ________________
- [ ] **Python version(s) used**: _____________
- [ ] **Special requirements**: 
  - [ ] MAST API access
  - [ ] Archive data requirements
  - [ ] Authentication needs

#### ✅ Migration Steps
- [ ] **Step 1**: Create migration branch
- [ ] **Step 2**: Replace workflows with centralized versions
- [ ] **Step 3**: Update workflow references
- [ ] **Step 4**: Configure repository-specific parameters
  ```yaml
  # Example for MAST-specific needs
  with:
    python-version: "3.11"
    execution-mode: "full"
    build-html: true
    security-scan: true
    # Add MAST-specific configurations
  ```
- [ ] **Step 5**: Configure secrets

#### ✅ mast_notebooks Testing
- [ ] **Local testing**: Test MAST API access
- [ ] **Archive queries**: Verify data download functionality
- [ ] **Authentication**: Test with repository secrets

### hst_notebooks Migration

#### ✅ Current State Analysis
- [ ] **Repository URL**: `https://github.com/spacetelescope/hst_notebooks`
- [ ] **Primary workflows identified**: ________________
- [ ] **Python version(s) used**: _____________
- [ ] **Special requirements**: 
  - [ ] `hstcal` environment
  - [ ] Large HST data files
  - [ ] STScI software stack

#### ✅ Migration Steps
- [ ] **Step 1**: Create migration branch
- [ ] **Step 2**: Replace workflows with centralized versions
- [ ] **Step 3**: Update workflow references
- [ ] **Step 4**: Configure HST-specific parameters
  ```yaml
  # HST repositories have special micromamba support
  with:
    python-version: "3.11"
    execution-mode: "full"
    build-html: true
    security-scan: true
    # The notebook-ci-unified.yml automatically detects hst_notebooks repo
    # and sets up hstcal environment
  ```
- [ ] **Step 5**: Configure secrets

#### ✅ hst_notebooks Testing
- [ ] **Environment**: Verify `hstcal` environment setup
- [ ] **Data access**: Test HST data download and processing
- [ ] **Software stack**: Verify STScI tools work correctly

### hellouniverse Migration

#### ✅ Current State Analysis
- [ ] **Repository URL**: `https://github.com/spacetelescope/hellouniverse`
- [ ] **Primary workflows identified**: ________________
- [ ] **Python version(s) used**: _____________
- [ ] **Special requirements**: 
  - [ ] Educational content focus
  - [ ] Simplified examples
  - [ ] Beginner-friendly documentation

#### ✅ Migration Steps
- [ ] **Step 1**: Create migration branch
- [ ] **Step 2**: Replace workflows with centralized versions
- [ ] **Step 3**: Update workflow references
- [ ] **Step 4**: Configure for educational content
  ```yaml
  # Simplified configuration for educational repository
  with:
    python-version: "3.11"
    execution-mode: "validation-only"  # Lighter validation for tutorials
    build-html: true
    security-scan: false  # May skip for simple educational content
  ```
- [ ] **Step 5**: Configure secrets (minimal needed)

#### ✅ hellouniverse Testing
- [ ] **Beginner focus**: Ensure workflows don't overwhelm new users
- [ ] **Simple examples**: Verify basic notebook execution
- [ ] **Documentation**: Ensure educational docs build correctly

### jwst-pipeline-notebooks Migration

#### ✅ Current State Analysis
- [ ] **Repository URL**: `https://github.com/spacetelescope/jwst-pipeline-notebooks`
- [ ] **Primary workflows identified**: ________________
- [ ] **Python version(s) used**: _____________
- [ ] **Special requirements**: 
  - [ ] JWST pipeline software
  - [ ] Large JWST data files
  - [ ] `jdaviz` visualization tools
  - [ ] CRDS references

#### ✅ Migration Steps
- [ ] **Step 1**: Create migration branch
- [ ] **Step 2**: Replace workflows with centralized versions
- [ ] **Step 3**: Update workflow references
- [ ] **Step 4**: Configure JWST-specific parameters
  ```yaml
  with:
    python-version: "3.11"
    execution-mode: "full"
    build-html: true
    security-scan: true
  ```
- [ ] **Step 5**: Configure post-processing for jdaviz
  ```yaml
  # In HTML builder workflow
  build-and-deploy:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@v1
    with:
      python-version: "3.11"
      post-run-script: "scripts/jdaviz_image_replacement.sh"
  ```
- [ ] **Step 6**: Configure secrets

#### ✅ jwst-pipeline-notebooks Testing
- [ ] **JWST pipeline**: Test pipeline software installation
- [ ] **Large data**: Verify data download and processing
- [ ] **Visualization**: Test jdaviz tools and image replacement
- [ ] **CRDS**: Verify reference file access

## 🧪 Testing & Validation

### Local Testing Strategy

#### ✅ Pre-Deployment Testing
For each repository:

- [ ] **Test workflow_dispatch triggers**
  ```bash
  # Navigate to Actions tab in GitHub
  # Manually trigger "Notebook CI - On Demand" workflow
  # Test with different parameters:
  # - Python version: 3.11
  # - Execution mode: validation-only (safe for testing)
  # - Single notebook: pick a simple notebook
  ```

- [ ] **Test PR workflows**
  ```bash
  # Create test PR with minor notebook change
  git checkout -b test-workflows
  echo "# Test" >> test-notebook.ipynb
  git add test-notebook.ipynb
  git commit -m "test: trigger PR workflow"
  git push origin test-workflows
  # Create PR and verify workflows run
  ```

- [ ] **Validate workflow outputs**
  - [ ] Check that notebooks execute without errors
  - [ ] Verify HTML documentation builds
  - [ ] Confirm security scans complete
  - [ ] Test artifact uploads on failures

### Version Testing Process

#### ✅ Progressive Version Testing
- [ ] **Test with exact version first**
  ```yaml
  # Use exact version for initial testing
  uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@v1.0.0
  ```

- [ ] **Graduate to major version pinning**
  ```yaml
  # Once stable, use major version pinning
  uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@v1
  ```

- [ ] **Monitor for updates**
  - [ ] Subscribe to notebook-ci-actions releases
  - [ ] Test new versions in staging before production

### Performance Validation

#### ✅ Performance Benchmarks
For each repository, record baseline performance:

- [ ] **Execution time**: Record current workflow run times
- [ ] **Resource usage**: Monitor GitHub Actions minute consumption
- [ ] **Success rate**: Track workflow success/failure rates
- [ ] **Error patterns**: Document common failure modes

```bash
# Create performance tracking file
cat > performance-baseline.md << EOF
# Performance Baseline for $(basename $(pwd))

## Pre-Migration (Date: $(date))
- Average workflow time: _____ minutes
- Success rate: _____%
- Common failures: __________

## Post-Migration (Date: TBD)
- Average workflow time: _____ minutes  
- Success rate: _____%
- Common failures: __________

## Performance Notes
- Improvements: __________
- Regressions: __________
- Action items: __________
EOF
```

## 🏁 Post-Migration Cleanup

### Repository Cleanup

#### ✅ Cleanup Tasks
For each successfully migrated repository:

- [ ] **Remove backup files**
  ```bash
  # After confirming workflows work correctly
  rm -rf .github/workflows-backup/
  git rm migration-status.md
  ```

- [ ] **Update documentation**
  - [ ] Update README.md with new workflow information
  - [ ] Document any repository-specific configuration
  - [ ] Add links to centralized workflow documentation

- [ ] **Archive old branches**
  ```bash
  # Delete migration branch after successful merge
  git branch -d migrate-to-centralized-actions
  git push origin --delete migrate-to-centralized-actions
  ```

### Documentation Updates

#### ✅ Documentation Tasks
- [ ] **Update each repository's README**
  ```markdown
  ## GitHub Actions Workflows

  This repository uses centralized workflows from 
  [notebook-ci-actions](https://github.com/spacetelescope/notebook-ci-actions).

  ### Available Workflows:
  - **PR Validation**: Runs on pull requests for quick validation
  - **Main CI**: Full execution and deployment on main branch
  - **On-Demand**: Manual testing with configurable options
  - **Documentation**: Builds and deploys JupyterBook documentation

  For workflow documentation, see the 
  [notebook-ci-actions repository](https://github.com/spacetelescope/notebook-ci-actions).
  ```

- [ ] **Create migration summary report**
  ```markdown
  # Migration Summary Report

  ## Repositories Migrated  - [x] jdat_notebooks - Completed $(date)
  - [x] mast_notebooks - Completed $(date)  
  - [x] hst_notebooks - Completed $(date)
  - [x] hellouniverse - Completed $(date)
  - [x] jwst-pipeline-notebooks - Completed $(date)

  ## Benefits Achieved
  - Centralized workflow management
  - Consistent CI/CD across repositories
  - Reduced maintenance overhead
  - Improved documentation building

  ## Lessons Learned
  - [Repository-specific notes]
  - [Common issues encountered]
  - [Best practices discovered]
  ```

## 🚨 Troubleshooting

### Common Issues and Solutions

#### Issue 1: Workflow Not Triggering
**Symptoms**: New workflows don't run on PR or push
**Solution**:
```bash
# Check workflow file syntax
yamllint .github/workflows/*.yml

# Verify workflow file permissions
ls -la .github/workflows/

# Check repository Actions settings
# Settings → Actions → General → Actions permissions
```

#### Issue 2: Missing Secrets
**Symptoms**: `Error: Secret 'CASJOBS_USERID' not found`
**Solution**:
```bash
# Add secrets in repository settings:
# Settings → Secrets and variables → Actions → New repository secret

# Required secrets for most repositories:
# - GITHUB_TOKEN (usually automatic)
# - CASJOBS_USERID (for astronomical data)
# - CASJOBS_PW (for astronomical data)
```

#### Issue 3: Environment Setup Failures
**Symptoms**: `micromamba environment creation failed` or `hstcal not found`
**Solution**:
```yaml
# For HST repositories, ensure the workflow detects the repo correctly
# The notebook-ci-unified.yml automatically sets up hstcal for hst_notebooks

# For custom environments, you may need to fork and modify workflows
```

#### Issue 4: Notebook Execution Timeouts
**Symptoms**: `Cell execution timeout exceeded`
**Solution**:
```yaml
# Increase timeout in workflow parameters
with:
  python-version: "3.11"
  execution-mode: "full"
  cell-timeout: 6000  # Increase from default 4000 seconds
```

#### Issue 5: Documentation Build Failures
**Symptoms**: JupyterBook build errors
**Solution**:
```bash
# Check _config.yml and _toc.yml files
# Ensure all referenced notebooks exist
# Verify notebook output is stripped (use nbstripout)

# For jdaviz issues, ensure post-processing script exists:
# scripts/jdaviz_image_replacement.sh
```

### Emergency Rollback

#### ✅ Quick Rollback Process
If critical issues occur:

- [ ] **Immediate rollback**
  ```bash
  # Restore from backup
  git checkout main
  rm .github/workflows/*.yml
  cp .github/workflows-backup/*.yml .github/workflows/
  git add .github/workflows/
  git commit -m "Emergency rollback to previous workflows"
  git push origin main
  ```

- [ ] **Investigate and fix**
  - [ ] Review workflow logs for error details
  - [ ] Test fixes in migration branch
  - [ ] Re-attempt migration after fixes

### Support Resources

#### ✅ Getting Help
- **Primary support**: Create issues in `notebook-ci-actions` repository
- **Documentation**: Check `docs/` folder in `notebook-ci-actions`
- **Community**: Use repository discussions for questions
- **Emergency**: Contact repository maintainers directly

---

## 📊 Migration Progress Tracker

| Repository | Status | Migration Date | Notes |
|------------|--------|----------------|-------|
| jdat_notebooks | ⏳ Pending | | |
| mast_notebooks | ⏳ Pending | | |
| hst_notebooks | ⏳ Pending | | |
| hellouniverse | ⏳ Pending | | |
| jwst-pipeline-notebooks | ⏳ Pending | | |

**Status Legend**: ⏳ Pending, 🔄 In Progress, ✅ Complete, ❌ Failed

---

## 📝 Notes Section

Use this space to record repository-specific notes, special requirements, or lessons learned during migration:

### jdat_notebooks Notes:
- 

### mast_notebooks Notes:
- 

### hst_notebooks Notes:
- 

### hellouniverse Notes:
- 

### jwst-pipeline-notebooks Notes:
-

---

**Last Updated**: $(date)  
**Migration Lead**: [Your Name]  
**Review Date**: [Schedule quarterly reviews]

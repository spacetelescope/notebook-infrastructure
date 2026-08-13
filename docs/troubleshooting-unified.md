# Troubleshooting Guide - Unified Notebook CI/CD System

This guide provides comprehensive troubleshooting information for the unified notebook CI/CD system.

## :material-alert: Common Issues and Solutions

### Workflow Issues

#### Issue: Workflow Not Triggering

**Symptoms:**
- PR or push doesn't trigger workflows
- No actions appear in the Actions tab

**Solutions:**
```bash
# 1. Check workflow file syntax
yamllint .github/workflows/*.yml

# 2. Verify paths configuration
# Ensure your paths match your repository structure
git ls-files | grep -E '\.(ipynb|py|txt|yml)$'

# 3. Check branch configuration
# Verify the target branches exist and match workflow configuration
git branch -a
```

**Example Fix:**
```yaml
# In your workflow file, ensure paths are correct
on:
  pull_request:
    branches: [ main ]  # Change to 'master' if that's your default
    paths:
      - 'notebooks/**'       # Adjust to your notebook directory
      - 'requirements*.txt'  # Include all requirements files
```

#### Issue: Permission Denied Errors

**Symptoms:**
- `Error: Permission denied (publickey)`
- `Error: Insufficient permissions to access workflow`

`Permission denied (publickey)` is a git/SSH problem, not the workflow: confirm your SSH key is registered with GitHub (`ssh -T git@github.com`) or switch the remote to HTTPS.

**For insufficient workflow permissions:**
```bash
# 1. Verify GITHUB_TOKEN permissions
# In repository settings: Settings → Actions → General
# Set "Workflow permissions" to "Read and write permissions"

# 2. Check if repository is private
# Private repos may need additional configuration

# 3. Verify the caller references the workflow correctly (see below)
```

```yaml
uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@v1
```

### Environment Issues

#### Issue: Python Environment Setup Failures

**Symptoms:**
- `ModuleNotFoundError` for basic packages
- Conda environment creation fails
- Package installation timeouts

**Solutions:**
```yaml
# 1. Specify exact Python version
python-version: '3.11'  # Not '3.11.x' or 'latest'

# 2. For conda environments, use explicit names
conda-environment: 'hstcal'  # Pre-defined environment
# OR
custom-requirements: 'environment.yml'  # Custom conda file

# 3. For package conflicts, use exact versions
# In requirements.txt:
numpy==1.24.3
matplotlib==3.7.1
```

#### Issue: Conda Environment Detection

**Symptoms:**
- System uses pip instead of conda for hst_notebooks
- `hstcal` environment not found

**Solutions:**
```yaml
# The system auto-detects hst_notebooks repositories
# For manual override:
conda-environment: 'hstcal'

# For custom conda environments:
custom-requirements: 'environment.yml'
```

### Notebook Execution Issues

#### Issue: Notebook Execution Timeouts

**Symptoms:**
- Workflows cancelled after 6 hours
- "Runner timeout" errors
- Long-running data downloads

**Solutions:**
```yaml
# 1. Use execution mode optimization
execution-mode: 'pr'  # Faster validation for PRs

# 2. For large datasets, consider validation-only
enable-execution: false  # Skip execution, just validate syntax

# 3. Use single notebook testing for debugging
single-notebook: 'notebooks/problematic/example.ipynb'
```

#### Issue: Notebook Validation Failures

**Symptoms:**
- `nbval` failures on working notebooks
- Cell execution order problems
- Missing outputs in notebooks

**Solutions:**
```bash
# 1. Clean notebook outputs locally
pip install nbstripout
nbstripout notebooks/**/*.ipynb

# 2. Test notebooks locally first
pytest --nbval notebooks/

# 3. Check for cell execution dependencies
# Ensure notebooks can run from top to bottom
```

### Storage and Output Issues

#### Issue: gh-storage Upload Failures

**Symptoms:**
- "Failed to push to gh-storage branch"
- "Branch not found" errors

**Solutions:**
```yaml
# 1. Ensure storage is enabled correctly
enable-storage: true

# 2. Check repository permissions
# Repository needs write access to create gh-storage branch

# 3. For first-time setup, manually create branch
git checkout --orphan gh-storage
git rm -rf .
echo "# Storage branch" > README.md
git add README.md
git commit -m "Initial storage branch"
git push origin gh-storage
```

#### Issue: HTML Build Failures

**Symptoms:**
- JupyterBook build errors
- Missing `_config.yml` or `_toc.yml`
- Image not found errors

**Solutions:**
```bash
# 1. Verify JupyterBook configuration
ls -la _config.yml _toc.yml

# 2. Check notebook outputs
# Ensure notebooks have been executed with outputs
jupyter nbconvert --execute --inplace notebooks/*.ipynb

# 3. For jdaviz images, ensure post-processing script exists
ls -la scripts/jdaviz_image_replacement.sh
chmod +x scripts/jdaviz_image_replacement.sh
```

### Security and Secrets Issues

#### Issue: Missing Secrets

**Symptoms:**
- `Error: Secret 'CASJOBS_USERID' not found`
- `Error: Secret 'CASJOBS_PW' not found`

**Solutions:**
```bash
# 1. Add secrets in repository settings
# Navigate to: Settings → Secrets and variables → Actions
# Click "New repository secret"

# Required secrets:
# - CASJOBS_USERID (if using CasJobs)
# - CASJOBS_PW (if using CasJobs)

# 2. Verify secret names match workflow
# In workflow file:
secrets:
  CASJOBS_USERID: ${{ secrets.CASJOBS_USERID }}
  CASJOBS_PW: ${{ secrets.CASJOBS_PW }}
```

#### Issue: Security Scan Failures

**Symptoms:**
- `bandit` security warnings
- High severity security issues block deployment

**Solutions:**
```yaml
# 1. For educational repositories, disable security scanning
enable-security: false

# 2. For development, use lower security threshold
# (This requires modifying the reusable workflow)

# 3. Fix security issues in code
# Review bandit output and address high-severity issues
```

## :material-wrench: Debugging Strategies

### Enable Debug Mode

```yaml
# Add to your workflow for verbose logging
jobs:
  debug-run:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@v1
    with:
      execution-mode: 'on-demand'
      trigger-event: 'validate'  # Start with validation only
      # Add other parameters...
```

### Local Testing

```bash
# 1. Clone the actions repository
git clone https://github.com/spacetelescope/notebook-ci-actions.git

# 2. Use local testing scripts
cd your-repository
../notebook-ci-actions/scripts/test-local-ci.sh

# 3. Test specific notebooks
jupyter nbconvert --execute --to notebook notebooks/example.ipynb
```

### Step-by-Step Debugging

```yaml
# Test each component separately using on-demand workflow
on:
  workflow_dispatch:
    inputs:
      debug_step:
        type: choice
        options: ['validate', 'execute', 'security', 'html']

jobs:
  debug:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@v1
    with:
      execution-mode: 'on-demand'
      trigger-event: ${{ inputs.debug_step }}
```

## :material-chart-box: Performance Optimization

### Workflow Performance Issues

**Symptoms:**
- Workflows take longer than expected
- High GitHub Actions minutes usage
- Frequent timeouts

**Solutions:**
```yaml
# 1. Use smart execution for PRs
execution-mode: 'pr'  # Only processes changed files

# 2. Optimize feature flags
enable-validation: true   # Keep for safety
enable-security: false   # Disable for faster PRs
enable-execution: true   # Keep for testing
enable-storage: false    # Disable for PRs, enable for main

# 3. Use selective execution
# System automatically detects docs-only changes
```

### Resource Usage Optimization

```yaml
# For repositories with large notebooks or datasets
execution-mode: 'pr'        # PR validation
enable-execution: false     # skip execution on PRs
enable-html-build: false          # Build only on main branch

# For educational repositories
enable-security: false    # Less critical for tutorials
enable-storage: true      # Keep for examples
```

!!! tip "Resource-heavy notebooks need bigger runners"
    If a notebook exceeds the default runner's memory (~7 GB) or CPU (2 cores) - out-of-memory kills (exit code 137), `MemoryError`, or long timeouts - assign it a larger runner with `custom-runner-config` and a `ci_config.txt` mapping. See [Custom Runner Configuration](custom-runner-configuration.md).

## :material-help-circle: Emergency Procedures

### Rollback to Previous Workflows

```bash
# If unified system causes critical issues
cd your-repository

# 1. Restore your previous workflows from a backup branch
rm .github/workflows/*.yml
cp .github/workflows-backup/*.yml .github/workflows/
git add .github/workflows/
git commit -m "Emergency rollback to previous workflows"
git push origin main

# 2. Or revert specific commits
git log --oneline -10  # Find commit to revert
git revert <commit-hash>
```

### Disable Workflows Temporarily

```yaml
# Add to the top of any workflow file to disable it
name: Notebook CI - Disabled
on: []  # Empty trigger list disables the workflow

# Or rename the file
mv .github/workflows/notebook-pr.yml .github/workflows/notebook-pr.yml.disabled
```

## :material-lifebuoy: Getting Help

### Information to Include

When reporting issues, include:

1. **Repository information:**
   - Repository name and organization
   - Repository type (hst_notebooks, jdat_notebooks, etc.)
   - Default branch name

2. **Workflow information:**
   - Workflow file names
   - Execution mode used
   - Feature flags enabled

3. **Error information:**
   - Complete error messages
   - Workflow run URL
   - Steps that failed

4. **Environment information:**
   - Python version specified
   - Conda environment (if used)
   - Custom requirements files

### Support Channels

- **STScI staff:** [Submit a ticket to SPB](https://innerspace.stsci.edu/pages/viewpage.action?pageId=637400835&spaceKey=DDP&title=DMD%2BDev%2BPortal%2BHome)
- **GitHub Issues**: [Create issue in notebook-ci-actions](https://github.com/spacetelescope/notebook-ci-actions/issues)
- **Documentation**: Check `docs/` folder for detailed guides

### Emergency Contact

For critical production issues:
- Create issue with `priority:high` label
- Include "URGENT" in issue title
- Provide comprehensive error information

---

**System Version**: Unified workflow (`@v1`)  
**Compatibility**: All STScI notebook repositories

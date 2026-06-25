# Notebook CI/CD System - Operator User Guide

## Table of Contents
1. [System Overview](#system-overview)
2. [How the System Works](#how-the-system-works)
3. [Operator Interactions](#operator-interactions)
4. [Monitoring and Logs](#monitoring-and-logs)
5. [Common Issues and Troubleshooting](#common-issues-and-troubleshooting)
6. [Best Practices](#best-practices)

## System Overview

The centralized notebook CI/CD system provides automated testing, building, and deployment for Jupyter notebooks across multiple repositories. It consists of reusable GitHub Actions workflows that handle:

- **Notebook Execution**: Running notebooks to validate they work correctly
- **Documentation Building**: Generating HTML documentation from notebooks
- **Environment Management**: Setting up Python/conda environments
- **Artifact Management**: Publishing built documentation and assets
- **Smart Path Detection**: Only running CI when relevant files change

### Supported Repositories
- `jdat_notebooks` - JWST Data Analysis Tools notebooks
- `hst_notebooks` - Hubble Space Telescope notebooks  
- `mast_notebooks` - Mikulski Archive for Space Telescopes notebooks
- `hellouniverse` - Educational/introductory notebooks
- `jwst-pipeline-notebooks` - JWST Pipeline processing notebooks

## How the System Works

### Architecture

```
Repository (e.g., jdat_notebooks)
├── .github/workflows/
│   ├── ci-pr.yml          # Calls centralized PR workflow
│   └── ci-main.yml        # Calls centralized main workflow
├── _config.yml            # Jupyter Book configuration
├── _toc.yml               # Jupyter Book table of contents
├── requirements.txt       # Python dependencies (if needed)
└── notebooks/             # Jupyter notebooks to test
```

### Workflow Types

#### 1. Pull Request (PR) Workflows
- **Trigger**: When PRs are opened, updated, or synchronized
- **Purpose**: Validate changes before merging
- **Scope**: Can run full CI or docs-only based on changed files
- **Artifacts**: Temporary preview builds (not published)

#### 2. Main Branch Workflows  
- **Trigger**: When code is merged to main branch
- **Purpose**: Build and deploy production documentation
- **Scope**: Always runs full CI pipeline
- **Artifacts**: Published to GitHub Pages or artifact storage

#### 3. On-Demand Workflows
- **Trigger**: Manual workflow dispatch
- **Purpose**: Testing, debugging, or rebuilding on demand
- **Scope**: Configurable (full CI or docs-only)

### Smart Path Detection

The system automatically determines what to run based on file changes:

- **Docs-only path**: Triggered by changes to:
  - `*.md` files
  - `docs/` directory
  - `README` files
  - `.github/workflows/` (workflow changes)

- **Full CI path**: Triggered by changes to:
  - `*.ipynb` notebooks
  - `requirements.txt` or `pyproject.toml`
  - Python source files (`*.py`)
  - `_config.yml` or `_toc.yml` (Jupyter Book configuration)
  - Any other code files

## Operator Interactions

### 1. Monitoring Repository Health

#### Check CI Status
Navigate to any supported repository and look for:
- ✅ Green checkmarks = All workflows passing
- ❌ Red X marks = Workflow failures
- 🟡 Yellow dots = Workflows running

#### Repository Pages
Each repository has automatically built documentation available at:
- `https://{org}.github.io/{repository-name}/`

### 2. Manual Workflow Triggers

#### Triggering On-Demand Builds
1. Go to repository → Actions tab
2. Select "Notebook CI (On-Demand)" workflow
3. Click "Run workflow"
4. Choose options:
   - **Branch**: Which branch to build from
   - **Force full CI**: Override smart detection
   - **Debug mode**: Enable verbose logging

#### Re-running Failed Workflows
1. Click on the failed workflow run
2. Click "Re-run all jobs" or "Re-run failed jobs"
3. Monitor the new run for resolution

### 3. Environment Management

#### Understanding Dependency Files
- **`requirements.txt`**: Python package dependencies
- **`pyproject.toml`**: Modern Python project configuration
- **`_config.yml`**: Jupyter Book configuration
- **`_toc.yml`**: Jupyter Book table of contents

#### Common Dependency Patterns
```text
# requirements.txt example
jupyter
numpy
matplotlib
astropy
# Add project-specific packages

# _config.yml (Jupyter Book configuration)
title: My Notebook Collection
author: Your Name
logo: logo.png

# _toc.yml (Table of contents)
format: jb-book
root: index
chapters:
- file: notebooks/intro
- file: notebooks/analysis
```

## Monitoring and Logs

### 1. Accessing Action Logs

#### Via GitHub UI
1. Navigate to repository → **Actions** tab
2. Click on specific workflow run
3. Click on job name (e.g., "notebook-ci")
4. Expand log sections to see details

#### Log Structure
```
Setup Environment
├── Checkout code
├── Setup Python/Conda
└── Install dependencies

Execute Notebooks  
├── Find notebook files
├── Run each notebook
└── Collect outputs

Build Documentation
├── Convert notebooks to HTML
├── Build docs site
└── Prepare artifacts

Deploy/Upload
├── Upload to GitHub Pages
└── Store artifacts
```

### 2. Key Log Sections to Monitor

#### Environment Setup Issues
Look for:
- `Setup Python` step failures
- `Install dependencies` errors
- Package resolution conflicts

#### Notebook Execution Issues  
Look for:
- `Execute notebooks` step failures
- Individual notebook error messages
- Timeout errors (notebooks taking too long)

#### Documentation Build Issues
Look for:
- `Build documentation` failures
- Sphinx/Jekyll build errors
- Missing file references

### 3. Workflow Status API

For programmatic monitoring:
```bash
# Check latest workflow status
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/{org}/{repo}/actions/runs

# Get specific workflow run logs
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/{org}/{repo}/actions/runs/{run_id}/logs
```

## Common Issues and Troubleshooting

### 1. Environment and Dependencies

#### Issue: Package Installation Fails
```
Failed to install package 'xyz'
```

**Diagnosis**: 
- Check the "Setup Python" or "Install dependencies" log section
- Look for package conflicts or unavailable packages

**Solutions**:
1. **Pin specific versions**: Update `requirements.txt` with exact versions
2. **Remove problematic packages**: Temporarily remove and test
3. **Use alternative packages**: Find equivalent packages
4. **Check package spelling**: Verify correct package names

**Example Fix**:
```text
# Before (problematic)
some-package

# After (fixed)  
some-package==1.2.3
```

#### Issue: Package Not Found
```
ERROR: No matching distribution found for package 'xyz'
```

**Solutions**:
1. **Check package name**: Verify correct spelling and name
2. **Use alternative packages**: Find packages with similar functionality
3. **Check availability**: Ensure package exists on PyPI
4. **Try dev versions**: Use pre-release or development versions

### 2. Notebook Execution Failures

#### Issue: Notebook Kernel Errors
```
Kernel died while executing notebook.ipynb
```

**Diagnosis**:
- Look in "Execute notebooks" section
- Check specific notebook error messages
- Review notebook cell outputs

**Solutions**:
1. **Memory issues**: Reduce data size or add memory limits
2. **Missing dependencies**: Add required packages to environment
3. **Code errors**: Fix syntax or logic errors in notebooks
4. **Timeout issues**: Optimize slow-running cells

#### Issue: Import Errors in Notebooks
```
ModuleNotFoundError: No module named 'xyz'
```

**Solutions**:
1. **Add to requirements**: Include missing package in `requirements.txt`
2. **Check spelling**: Verify correct package/module names
3. **Virtual environment**: Ensure package is in correct environment

#### Issue: Data File Not Found
```
FileNotFoundError: No such file or directory: 'data/file.fits'
```

**Solutions**:
1. **Check paths**: Use relative paths from notebook location
2. **Add data files**: Include required data in repository
3. **Download data**: Add cells to download required datasets
4. **Mock data**: Use synthetic data for CI testing

### 3. Documentation Build Issues

#### Issue: Sphinx Build Failures
```
Warning, treated as error: document isn't included in any toctree
```

**Solutions**:
1. **Update index**: Add notebook to `docs/index.rst` or similar
2. **Fix references**: Ensure all cross-references are valid
3. **Check syntax**: Validate reStructuredText syntax

#### Issue: Missing Static Files
```
Static file not found: _static/image.png
```

**Solutions**:
1. **Add files**: Include missing static files in repository
2. **Fix paths**: Update file paths in notebooks or docs
3. **Remove references**: Remove references to missing files

### 4. GitHub Actions Infrastructure

#### Issue: Workflow Not Triggering
**Check**:
1. **File paths**: Ensure workflow files are in `.github/workflows/`
2. **Syntax**: Validate YAML syntax in workflow files
3. **Permissions**: Verify repository has Actions enabled
4. **Branch protection**: Check if branch rules block workflows

#### Issue: Secrets/Tokens Not Working
```
Error: Authentication failed
```

**Solutions**:
1. **Check secrets**: Verify secrets are set in repository settings
2. **Token permissions**: Ensure tokens have required scopes
3. **Renewal**: Check if tokens have expired

#### Issue: Runner Out of Disk Space
```
No space left on device
```

**Solutions**:
1. **Clean up**: Remove unnecessary files in workflow
2. **Smaller data**: Reduce dataset sizes for testing
3. **Stream processing**: Process data in chunks rather than loading all

### 5. Performance Issues

#### Issue: Workflows Taking Too Long
**Common causes**:
- Large datasets being processed
- Complex computations in notebooks
- Slow dependency installation

**Solutions**:
1. **Optimize notebooks**: Reduce computation complexity
2. **Cache dependencies**: Use action caching for faster builds
3. **Parallel execution**: Split notebooks across multiple jobs
4. **Skip slow notebooks**: Use conditional execution

#### Issue: Rate Limiting
```
API rate limit exceeded
```

**Solutions**:
1. **Reduce frequency**: Limit workflow triggers
2. **Use tokens**: Authenticate API calls with tokens
3. **Cache results**: Avoid repeated API calls

## Best Practices

### 1. Repository Maintenance

#### Keep Dependencies Updated
- Regularly review and update `requirements.txt`
- Test with latest package versions
- Pin critical package versions

#### Optimize Notebooks for CI
- Keep execution time under 10 minutes per notebook
- Use small sample datasets
- Include error handling
- Clear outputs before committing

#### Monitor Resource Usage
- Watch for memory and disk usage trends
- Optimize data processing algorithms
- Use efficient data formats

### 2. Troubleshooting Workflow

#### Step 1: Identify the Failure Point
1. Check workflow run status
2. Identify which job failed
3. Find specific step that failed

#### Step 2: Examine Logs
1. Read error messages carefully
2. Look for stack traces
3. Check preceding steps for context

#### Step 3: Reproduce Locally
1. Check out the failing branch
2. Set up same environment locally
3. Run the failing command manually

#### Step 4: Test Fix
1. Make minimal changes to fix issue
2. Test locally first
3. Push and verify CI passes

### 3. Getting Help

#### Internal Resources
- Check this documentation
- Review workflow logs
- Consult repository README files

#### External Resources
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Jupyter Book Documentation](https://jupyterbook.org/)
- [Jupyter Documentation](https://jupyter.org/documentation)

#### Escalation
If issues persist after troubleshooting:
1. Create GitHub issue in affected repository
2. Include relevant log excerpts
3. Describe steps already attempted
4. Tag relevant team members

---

*This guide covers the most common scenarios. For repository-specific issues or advanced troubleshooting, consult the individual repository documentation or contact the development team.*

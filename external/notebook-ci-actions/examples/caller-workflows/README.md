# Notebook CI/CD Caller Workflows

This directory contains example caller workflows organized by repository type. Each repository subfolder contains four production-ready workflow files that can be copied directly to your repository's `.github/workflows/` directory.

## 📁 Repository-Specific Examples

Each repository folder contains four workflow types tailored for that specific repository:

### Available Repository Examples

- **`hellouniverse/`** - Basic educational notebook repository
- **`jdat_notebooks/`** - JDAT (JWST Data Analysis Tools) notebooks with conda environments
- **`mast_notebooks/`** - MAST (Mikulski Archive) notebooks with mission-specific filters
- **`hst_notebooks/`** - Hubble Space Telescope notebooks with instrument filters
- **`jwst_pipeline_notebooks/`** - JWST Pipeline notebooks with stage/instrument filters

### Core Workflow Types (in each folder)

- **`notebook-pr.yml`** - Pull request validation workflow
- **`notebook-merge.yml`** - Main branch merge/push workflow  
- **`notebook-scheduled.yml`** - Scheduled execution workflow
- **`notebook-on-demand.yml`** - Manual/on-demand execution workflow

## 🚀 Quick Setup

1. **Choose your repository** from the examples above
2. **Copy workflow files**: 
   ```bash
   cp examples/caller-workflows/your_repo_name/*.yml .github/workflows/
   ```
3. **Customize settings** in each workflow file as needed
4. **Commit and push** to activate the workflows

All workflows reference `spacetelescope/notebook-ci-actions@dev-actions-v2` and are production-ready.

## Quick Start

1. **Choose your repository type** from the available examples above
2. **Copy the appropriate workflow files** from that subfolder to your repository's `.github/workflows/` directory
3. **Customize the configuration** parameters as needed for your specific repository
4. **Set up required secrets** in your repository settings

## Legacy Workflows (Deprecated)

The files `notebook-pr.yml`, `notebook-merge.yml`, `notebook-scheduled.yml`, and `notebook-on-demand.yml` in this root directory are maintained for backward compatibility but are deprecated. Please use the repository-specific examples instead.

## Available Workflows

### 1. Pull Request Workflow (`notebook-pr.yml`)
- **Purpose**: Validates and tests notebooks on pull requests
- **Features**:
  - Validates notebooks with pytest nbval
  - Runs security scans with bandit
  - Executes notebooks to test functionality
  - Stores executed outputs to `gh-storage` branch
  - Detects docs-only changes to skip unnecessary processing

### 2. Merge/Main Branch Workflow (`notebook-merge.yml`)
- **Purpose**: Full CI/CD pipeline after merging to main branch
- **Features**:
  - Complete notebook validation and execution
  - Builds and deploys JupyterBook documentation
  - Supports post-processing scripts
  - Respects deprecated notebook flags

### 3. Scheduled Maintenance (`notebook-scheduled.yml`)
- **Purpose**: Weekly maintenance and health checks
- **Features**:
  - Weekly validation of all notebooks
  - Automatic deprecation management
  - Moves expired notebooks to deprecated branch
  - No storage or HTML generation (validation only)

### 4. On-Demand Actions (`notebook-on-demand.yml`)
- **Purpose**: Manual workflow triggers with multiple options
- **Features**:
  - Validate all notebooks
  - Execute all notebooks
  - Security scan all notebooks
  - Single notebook operations
  - Full pipeline execution
  - HTML-only builds
  - Notebook deprecation tagging

## Configuration Options

### Common Parameters

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `python-version` | Python version to use | `'3.11'` | `'3.10'`, `'3.12'` |
| `conda-environment` | Custom conda environment | None | `'hstcal'`, `'stenv'` |
| `custom-requirements` | Path to custom requirements | None | `'custom-reqs.txt'` |
| `enable-validation` | Enable pytest nbval | `true` | `false` |
| `enable-security` | Enable bandit scanning | `true` | `false` |
| `enable-execution` | Enable notebook execution | `true` | `false` |
| `enable-storage` | Store outputs to gh-storage | `true` | `false` |
| `enable-html-build` | Build HTML documentation | Varies | `true`, `false` |
| `post-processing-script` | Post-processing script path | None | `'scripts/process.sh'` |

### Repository-Specific Customization

#### For HST Notebooks
```yaml
conda-environment: 'hstcal'
post-processing-script: 'scripts/hst_processing.sh'
```

#### For JWST Notebooks  
```yaml
conda-environment: 'stenv'
post-processing-script: 'scripts/jwst_processing.sh'
```

#### For Custom Environments
```yaml
custom-requirements: 'environment/requirements.txt'
```

## Required Secrets

Set these secrets in your repository settings (`Settings > Secrets and variables > Actions`):

| Secret | Required | Description |
|--------|----------|-------------|
| `CASJOBS_USERID` | Optional | CasJobs user ID for database access |
| `CASJOBS_PW` | Optional | CasJobs password for database access |

## File Triggers

### Paths That Trigger Workflows
- `notebooks/**` - Any notebook files
- `requirements.txt` - Root requirements
- `pyproject.toml` - Python project configuration
- `*.yml`, `*.yaml` - Configuration files
- `*.md` - Documentation files
- `*.html`, `*.css`, `*.js` - Web assets

### Smart Detection
The system automatically detects:
- **Docs-only changes**: Skips notebook execution for faster builds
- **Requirements changes**: Triggers full repository validation
- **Notebook changes**: Selective execution of affected directories
- **Deprecated notebooks**: Prevents overwriting with new outputs

## Deprecation Workflow

### Tagging a Notebook for Deprecation
1. Use the on-demand workflow with `deprecate-notebook` action
2. Specify the notebook path and days until deprecation
3. A deprecation banner will be added to the notebook

### Automatic Deprecation Management
- Scheduled workflow checks weekly for expired notebooks
- Expired notebooks are moved to the `deprecated` branch
- Original notebooks are removed from `main` branch

## Best Practices

### 1. Repository Setup
```yaml
# Use consistent Python version across workflows
python-version: '3.11'

# Set appropriate conda environment for your domain
conda-environment: 'hstcal'  # or 'stenv', etc.
```

### 2. Conditional Features
```yaml
# Disable features not needed for your repository
enable-security: false      # If no security scanning needed
enable-storage: false       # If no output storage needed
```

### 3. Performance Optimization
```yaml
# For documentation repositories
enable-execution: false     # Skip execution for docs-only repos
enable-html-build: true     # Focus on HTML generation
```

### 4. Custom Processing
```yaml
# Add post-processing for specialized workflows
post-processing-script: 'scripts/custom_processing.sh'
```

## Troubleshooting

### Common Issues

#### 1. Workflows Not Triggering
- Check that files are in the correct `paths:` configuration
- Verify branch names match your repository's default branch

#### 2. Conda Environment Issues
- Ensure the specified conda environment exists on conda-forge
- Check environment spelling and capitalization

#### 3. Requirements Installation Failures
- Verify requirements file paths are correct
- Check for conflicting package versions

#### 4. Permission Issues
- Ensure `GITHUB_TOKEN` has appropriate permissions
- Check that secrets are properly configured

### Getting Help

1. Check the [main repository documentation](https://github.com/spacetelescope/notebook-ci-actions)
2. Review workflow run logs for specific error messages
3. Open an issue in the notebook-ci-actions repository

## Migration from Existing Workflows

### From Individual Workflows
1. Replace multiple workflow files with these unified callers
2. Update configuration parameters to match your needs
3. Test with a draft PR to ensure functionality

### From Custom CI Systems
1. Map your existing steps to the appropriate configuration options
2. Move custom scripts to the `post-processing-script` parameter
3. Adjust triggers and paths as needed

## Examples

### Minimal Configuration
```yaml
jobs:
  notebook-ci:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@main
    with:
      execution-mode: 'pr'
      python-version: '3.11'
```

### Full-Featured Configuration
```yaml
jobs:
  notebook-ci:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@main
    with:
      execution-mode: 'merge'
      python-version: '3.11'
      conda-environment: 'hstcal'
      enable-validation: true
      enable-security: true
      enable-execution: true
      enable-storage: true
      enable-html-build: true
      post-processing-script: 'scripts/custom_processing.sh'
    secrets:
      CASJOBS_USERID: ${{ secrets.CASJOBS_USERID }}
      CASJOBS_PW: ${{ secrets.CASJOBS_PW }}
```

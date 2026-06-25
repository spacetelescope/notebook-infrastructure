# Quick Reference Guide - Unified Notebook CI/CD

A concise reference for using the unified notebook CI/CD system.

## 🚀 Setup Commands

### Automated Setup (Recommended)
```bash
# Clone the actions repository
git clone https://github.com/spacetelescope/notebook-ci-actions.git

# Navigate to your repository and run migration
cd your-repository
../notebook-ci-actions/scripts/migrate-to-unified.sh
```

### Manual Setup
```bash
# Create workflows directory
mkdir -p .github/workflows

# Copy basic workflows
cp examples/caller-workflows/notebook-pr.yml .github/workflows/
cp examples/caller-workflows/notebook-merge.yml .github/workflows/

# Optional: Add advanced workflows
cp examples/caller-workflows/notebook-scheduled.yml .github/workflows/
cp examples/caller-workflows/notebook-on-demand.yml .github/workflows/
```

## ⚙️ Configuration Templates

### Standard Python Repository
```yaml
uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@{current version}
with:
  execution-mode: 'pr'
  python-version: '3.11'
  enable-validation: true
  enable-security: true
  enable-execution: true
  enable-storage: true
  enable-html-build: false
```

### HST Notebooks (Conda)
```yaml
uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@{current version}
with:
  execution-mode: 'pr'
  python-version: '3.11'
  conda-environment: 'hstcal'  # Auto-detected
  enable-validation: true
  enable-security: true
  enable-execution: true
  enable-storage: true
  enable-html-build: false
```

### Educational Repository
```yaml
uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@{current version}
with:
  execution-mode: 'pr'
  python-version: '3.11'
  enable-validation: true
  enable-security: false      # Lighter for tutorials
  enable-execution: true
  enable-storage: true
  enable-html-build: true     # Build documentation
```

## 🎛️ Input Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `execution-mode` | string | required | `pr`, `merge`, `scheduled`, `on-demand` |
| `trigger-event` | string | `all` | `validate`, `execute`, `security`, `html`, `deprecate` |
| `python-version` | string | `3.11` | Python version to use |
| `conda-environment` | string | - | Custom conda environment |
| `single-notebook` | string | - | Path to single notebook |
| `enable-validation` | boolean | `true` | Enable pytest nbval |
| `enable-security` | boolean | `true` | Enable bandit scanning |
| `enable-execution` | boolean | `true` | Enable notebook execution |
| `enable-storage` | boolean | `true` | Store outputs to gh-storage |
| `enable-html-build` | boolean | `false` | Build HTML documentation |
| `post-processing-script` | string | - | Custom post-processing script |
| `deprecation-days` | number | `60` | Days until deprecation |

## 🔧 Common Configurations

### PR Workflow (Fast Validation)
```yaml
execution-mode: 'pr'
enable-validation: true
enable-security: false    # Skip for faster PRs
enable-execution: true
enable-storage: false     # Skip storage for PRs
enable-html-build: false
```

### Main Branch (Full Pipeline)
```yaml
execution-mode: 'merge'
enable-validation: true
enable-security: true
enable-execution: true
enable-storage: true
enable-html-build: true
post-processing-script: 'scripts/post_process.sh'
```

### Debug Mode (Single Notebook)
```yaml
execution-mode: 'on-demand'
trigger-event: 'validate'
single-notebook: 'notebooks/debug/example.ipynb'
enable-validation: true
enable-security: false
enable-execution: false
enable-storage: false
enable-html-build: false
```

## 🏃‍♂️ Quick Commands

### Test Locally
```bash
# Test workflows locally (requires Act)
../notebook-ci-actions/scripts/test-with-act.sh pull_request

# Validate repository setup
../notebook-ci-actions/scripts/validate-repository.sh $(basename $(pwd))

# Test local CI simulation
../notebook-ci-actions/scripts/test-local-ci.sh
```

### Troubleshooting
```bash
# Check workflow syntax
yamllint .github/workflows/*.yml

# Validate notebooks
pytest --nbval notebooks/

# Clean notebook outputs
nbstripout notebooks/**/*.ipynb

# Check git status
git status --porcelain
```

## 🆘 Quick Fixes

### Workflow Not Triggering
```yaml
# Check paths in workflow file
on:
  pull_request:
    paths:
      - 'notebooks/**'      # Adjust to match your structure
      - 'requirements*.txt'
      - '*.yml'
      - '*.md'
```

### Permission Errors
```bash
# Repository Settings → Actions → General
# Set "Workflow permissions" to "Read and write permissions"
```

### Python Environment Issues
```yaml
# Use exact Python version
python-version: '3.11'  # Not '3.11.x'

# For conda environments
conda-environment: 'hstcal'  # Pre-defined
# OR
custom-requirements: 'environment.yml'  # Custom file
```

### Missing Secrets
```bash
# Repository Settings → Secrets and variables → Actions
# Add required secrets:
# - CASJOBS_USERID (if needed)
# - CASJOBS_PW (if needed)
```

## 📋 Workflow Examples

### Minimal PR Workflow
```yaml
name: Notebook CI - PR
on:
  pull_request:
    branches: [ main ]
    paths: ['notebooks/**', '*.txt', '*.yml']

jobs:
  ci:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@{current version}
    with:
      execution-mode: 'pr'
      python-version: '3.11'
    secrets:
      CASJOBS_USERID: ${{ secrets.CASJOBS_USERID }}
      CASJOBS_PW: ${{ secrets.CASJOBS_PW }}
```

### Full Deploy Workflow
```yaml
name: Notebook CI - Deploy
on:
  push:
    branches: [ main ]
    paths: ['notebooks/**', '*.txt', '*.yml']

jobs:
  deploy:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@{current version}
    with:
      execution-mode: 'merge'
      python-version: '3.11'
      enable-validation: true
      enable-security: true
      enable-execution: true
      enable-storage: true
      enable-html-build: true
    secrets:
      CASJOBS_USERID: ${{ secrets.CASJOBS_USERID }}
      CASJOBS_PW: ${{ secrets.CASJOBS_PW }}
```

## 📁 Repository Structure

```text
your-repository/
├── .github/
│   └── workflows/
│       ├── notebook-pr.yml        # PR validation
│       ├── notebook-merge.yml     # Main branch deploy
│       ├── notebook-scheduled.yml # Optional: scheduled runs
│       └── notebook-on-demand.yml # Optional: manual testing
├── notebooks/
│   ├── directory1/
│   │   ├── notebook1.ipynb
│   │   └── requirements.txt       # Directory-specific deps
│   └── directory2/
│       ├── notebook2.ipynb
│       └── requirements.txt
├── scripts/                       # Optional post-processing
│   └── custom_processing.sh
├── _config.yml                    # JupyterBook config (optional)
├── _toc.yml                       # JupyterBook TOC (optional)
└── requirements.txt               # Global requirements
```

## 🔗 Useful Links

- **Main Documentation**: [README-unified.md](../README-unified.md)
- **Migration Guide**: [docs/migration-guide-unified.md](../docs/migration-guide-unified.md)
- **Troubleshooting**: [docs/troubleshooting-unified.md](../docs/troubleshooting-unified.md)
- **Complete Examples**: [examples/complete-setup-example.md](../examples/complete-setup-example.md)
- **Configuration Reference**: [docs/configuration-reference.md](../docs/configuration-reference.md)

## 🏷️ Version Information

- **System**: Unified Notebook CI/CD v1.0
- **Last Updated**: July 2025
- **Compatibility**: All STScI notebook repositories
- **Workflow Version**: `@{current version}` (recommended)

---

For detailed information, see the complete documentation in the repository.

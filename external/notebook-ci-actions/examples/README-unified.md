# Example Caller Workflows

This directory contains example workflows that demonstrate how to use the unified reusable GitHub Actions workflow in this repository. These examples show different patterns for calling the unified workflow based on various triggers and use cases.

## 🎯 Unified Workflow System

All examples now use the **unified workflow** (`notebook-ci-unified.yml`) which consolidates all notebook CI/CD functionality into a single, configurable workflow. This replaces the previous separate workflows (`ci_pipeline.yml`, `ci_html_builder.yml`, `ci_deprecation_manager.yml`).

## 📋 Available Examples

### 1. `notebook-ci-pr.yml` - Pull Request Validation
**Trigger**: Pull requests to `main` or `develop` branches  
**Purpose**: Lightweight validation for pull requests
- **Execution Mode**: `pr`
- Validates and executes notebooks in changed directories
- Stores executed notebooks to `gh-storage` branch
- Runs security scanning
- Triggered only when notebook or config files change

```yaml
uses: mgough-970/dev-actions/.github/workflows/notebook-ci-unified.yml@dev-actions-v2
with:
  execution-mode: 'pr'
  enable-validation: true
  enable-security: true
  enable-execution: true
  enable-storage: true
  enable-html-build: false
```

### 2. `notebook-ci-main.yml` - Main Branch CI with Documentation
**Trigger**: Pushes to `main` branch  
**Purpose**: Full CI pipeline with documentation deployment
- **Execution Mode**: `merge`
- Full notebook execution and validation  
- Documentation building and deployment to GitHub Pages
- Security scanning
- Uses executed notebooks from `gh-storage` branch

```yaml
uses: mgough-970/dev-actions/.github/workflows/notebook-ci-unified.yml@dev-actions-v2
with:
  execution-mode: 'merge'
  enable-validation: true
  enable-security: true
  enable-execution: true
  enable-storage: true
  enable-html-build: true
```

### 3. `notebook-ci-on-demand.yml` - On-Demand Testing
**Trigger**: Manual workflow dispatch  
**Purpose**: Flexible on-demand notebook testing and operations
- **Execution Mode**: `on-demand`
- Single notebook or full repository testing
- Configurable trigger events (execute, validate, deprecate)
- Manual parameter control
- Debugging and troubleshooting

```yaml
uses: mgough-970/dev-actions/.github/workflows/notebook-ci-unified.yml@dev-actions-v2
with:
  execution-mode: 'on-demand'
  trigger-event: 'execute'  # or 'validate', 'deprecate'
  single-filename: ${{ inputs.single-notebook }}
```

### 4. `notebook-deprecation.yml` - Deprecation Management
**Trigger**: Manual dispatch or scheduled  
**Purpose**: Notebook lifecycle management
- **Execution Mode**: `on-demand`
- **Trigger Event**: `deprecate`
- Marks notebooks for deprecation
- Adds deprecation warnings to documentation
- Manages expired notebook cleanup

```yaml
uses: mgough-970/dev-actions/.github/workflows/notebook-ci-unified.yml@dev-actions-v2
with:
  execution-mode: 'on-demand'
  trigger-event: 'deprecate'
  single-filename: ${{ inputs.notebook-path }}
```

### 5. `docs-only.yml` - Documentation-Only Deployment
**Trigger**: Manual dispatch or documentation file changes  
**Purpose**: Fast documentation rebuilds without notebook execution
- **Execution Mode**: `on-demand`
- **Trigger Event**: `html`
- Rebuilds documentation from existing executed notebooks
- No notebook processing
- Fast deployment for documentation updates

```yaml
uses: mgough-970/dev-actions/.github/workflows/notebook-ci-unified.yml@dev-actions-v2
with:
  execution-mode: 'on-demand'
  trigger-event: 'html'
  enable-html-build: true
```

## 🔧 Execution Modes Explained

| Mode | Purpose | When to Use | Features |
|------|---------|-------------|----------|
| **pr** | Pull request validation | PRs, code review | Selective execution, storage, fast feedback |
| **merge** | Production deployment | Main branch pushes | Full processing, documentation deployment |
| **on-demand** | Manual operations | Manual trigger, debugging | Flexible configuration, single notebook focus |
| **scheduled** | Maintenance tasks | Cron schedule | Bulk validation, deprecation cleanup |

## 🚀 Key Features of the Unified System

### Smart Change Detection
- Automatically detects changed notebooks and directories
- Optimizes execution based on file changes
- Supports both filename and full path specifications

### Cost Optimization
- Reduces GitHub Actions minutes by up to 60%
- Intelligent skipping of unnecessary operations
- Parallel processing where beneficial

### Advanced Storage Management
- Executed notebooks stored in `gh-storage` branch
- Clean separation of source and executed content
- Documentation built from executed notebooks

### Comprehensive Deprecation Management
- Automated deprecation warnings in documentation
- Visual deprecation banners with dates
- Scheduled cleanup of expired notebooks

### Local Testing
- Full local testing capabilities
- Diagnostic scripts for troubleshooting
- Environment validation before CI

## 📖 Migration from Old Workflows

If you're migrating from the old separate workflows:

| Old Workflow | New Configuration |
|--------------|-------------------|
| `ci_pipeline.yml` | `execution-mode: 'pr'` or `'merge'` |
| `ci_html_builder.yml` | `execution-mode: 'merge'` + `enable-html-build: true` |
| `ci_deprecation_manager.yml` | `execution-mode: 'on-demand'` + `trigger-event: 'deprecate'` |

See the main README for detailed migration instructions and the automated migration script.

## 📝 Usage Patterns

### Minimal Setup (Standard Repository)
```yaml
# PR validation
uses: mgough-970/dev-actions/.github/workflows/notebook-ci-unified.yml@dev-actions-v2
with:
  execution-mode: 'pr'

# Main branch deployment  
uses: mgough-970/dev-actions/.github/workflows/notebook-ci-unified.yml@dev-actions-v2
with:
  execution-mode: 'merge'
  enable-html-build: true
```

### Advanced Setup (Documentation Repository)
```yaml
# Full configuration with custom requirements
uses: mgough-970/dev-actions/.github/workflows/notebook-ci-unified.yml@dev-actions-v2
with:
  execution-mode: 'merge'
  python-version: '3.11'
  conda-environment: 'astropy scipy matplotlib'
  custom-requirements: 'requirements-dev.txt'
  enable-validation: true
  enable-security: true
  enable-execution: true
  enable-storage: true
  enable-html-build: true
  post-run-script: 'scripts/custom-post-processing.sh'
```

For more examples and detailed configuration options, see the main repository README.

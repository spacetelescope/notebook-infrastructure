# JWST Pipeline Notebooks - Workflow Configuration

This directory contains a complete set of GitHub Actions workflows specifically configured for the JWST pipeline notebooks repository. These workflows leverage custom runner configuration to optimize computational resources for different types of JWST data processing.

## 📁 Workflow Files

### Core Workflows

1. **`notebook-pr.yml`** - Pull Request Validation
   - Validates notebooks in PRs before merge
   - Uses custom runners based on `ci_config.txt`
   - Fast feedback for developers
   - Stores executed notebooks for comparison

2. **`notebook-merge.yml`** - Production Build & Deploy
   - Builds and deploys documentation on main branch merges
   - Optional performance benchmarking
   - Uses pre-executed notebooks from gh-storage
   - Full production deployment pipeline

3. **`notebook-scheduled.yml`** - Scheduled Maintenance
   - Weekly validation of all notebooks
   - Security audits and deprecation management
   - Environment compatibility testing
   - Performance monitoring

4. **`notebook-on-demand.yml`** - Manual Control
   - Flexible manual execution for development
   - Stage-specific and instrument-specific filtering
   - Runner override capabilities
   - Comprehensive debugging and testing options

## 🚀 Setup Instructions

### 1. Copy Workflow Files

```bash
# Create workflows directory in your repository
mkdir -p .github/workflows

# Copy all workflow files
cp examples/caller-workflows/jwst-pipeline/*.yml .github/workflows/
```

### 2. Create Custom Runner Configuration

Copy the example `ci_config.txt` to your repository root:

```bash
cp examples/jwst-pipeline-ci_config.txt ci_config.txt
```

#### Editing the Configuration File

The `ci_config.txt` file maps notebooks to appropriate runners:

```ini
# Light tutorials
notebooks/tutorials/jwst_pipeline_overview.ipynb:ubuntu-latest

# Moderate processing
notebooks/NIRCam/stage1/nircam_stage1_imaging.ipynb:jwst-pipeline-notebooks-16gb

# Heavy processing  
notebooks/MIRI/stage2/miri_stage2_mrs.ipynb:jwst-pipeline-notebooks-64gb
```

**Configuration format:**

- One mapping per line: `notebook_path:runner_label`
- Comments supported with `#`
- Wildcards supported: `notebooks/tutorials/*.ipynb:ubuntu-latest`
- Relative paths from repository root

**Runner recommendations:**

- `ubuntu-latest`: Tutorials, light analysis (< 2GB memory)
- `jwst-pipeline-notebooks-16gb`: Stage 1 processing, moderate analysis
- `jwst-pipeline-notebooks-32gb`: Stage 2 processing, complex analysis  
- `jwst-pipeline-notebooks-64gb`: Stage 3 processing, large datasets
- `jwst-pipeline-notebooks-128gb`: Performance testing, extreme cases

For detailed configuration guidance, see [Custom Runner Configuration Guide](../../docs/custom-runner-configuration.md).

### 3. Configure Repository Secrets

Add the following secrets to your repository:

- `CASJOBS_USERID` - For CASJOBS database access
- `CASJOBS_PW` - CASJOBS password
- `GITHUB_TOKEN` - Automatically provided by GitHub

### 4. Set Up Custom Runners

Ensure your organization has configured the following runner labels:

- `ubuntu-latest` (standard GitHub runner)
- `jwst-pipeline-notebooks-16gb` (16GB RAM, 4 cores)
- `jwst-pipeline-notebooks-32gb` (32GB RAM, 8 cores)  
- `jwst-pipeline-notebooks-64gb` (64GB RAM, 16 cores)

## 🛠️ Workflow Features

### Custom Runner Integration

All workflows use the `custom-runner-config: true` setting to automatically select appropriate runners based on your `ci_config.txt` configuration:

```yaml
# Light tutorials
notebooks/tutorials/jwst_pipeline_overview.ipynb:ubuntu-latest

# Moderate processing
notebooks/NIRCam/stage1/nircam_stage1_imaging.ipynb:jwst-pipeline-notebooks-16gb

# Heavy processing
notebooks/MIRI/stage2/miri_stage2_mrs.ipynb:jwst-pipeline-notebooks-64gb
```

### JWST-Specific Optimizations

- **STScI Environment**: Uses `conda-environment: 'stenv'` for JWST pipeline dependencies
- **Extended Timeouts**: Up to 6 hours for complex pipeline processing
- **Controlled Parallelism**: Limited parallel jobs to avoid overwhelming runners
- **Stage-Based Processing**: Separate handling for Stage 1, 2, and 3 processing

### Intelligent Resource Management

- **PR Workflows**: Fast feedback with balanced resource usage
- **Merge Workflows**: Conservative settings for production stability
- **Scheduled Workflows**: Higher parallelism for comprehensive validation
- **On-Demand Workflows**: Flexible resource allocation based on task

## 📋 Usage Examples

### Development Workflow

1. **Create PR** → `notebook-pr.yml` validates changes
2. **Merge PR** → `notebook-merge.yml` builds and deploys
3. **Weekly** → `notebook-scheduled.yml` performs maintenance

### Manual Testing

```yaml
# Test specific instrument notebooks
workflow_dispatch:
  inputs:
    action_type: 'execute-stage2'
    instrument_filter: 'nircam'
    runner_override: 'jwst-pipeline-notebooks-32gb'
```

### Performance Benchmarking

```yaml
# Run performance tests on merge
workflow_dispatch:
  inputs:
    rebuild_all: false
    enable_performance_tests: true
```

## 🔧 Customization Options

### Workflow Triggers

Each workflow can be customized by modifying the `on:` section:

```yaml
# Add additional trigger paths
on:
  pull_request:
    paths:
      - 'notebooks/**'
      - 'requirements.txt'
      - 'ci_config.txt'
      - 'custom_scripts/**'  # Add custom paths
```

### Runner Configuration

Modify `ci_config.txt` to adjust runner assignments:

```bash
# Use more powerful runners for specific notebooks
notebooks/heavy-processing/complex-analysis.ipynb:jwst-pipeline-notebooks-64gb

# Use standard runners for tutorials
notebooks/tutorials/*.ipynb:ubuntu-latest
```

### Environment Settings

Adjust conda environment and Python version:

```yaml
with:
  python-version: '3.11'
  conda-environment: 'stenv'  # or 'jwst-dev', 'custom-env', etc.
```

## 📊 Monitoring and Debugging

### Workflow Status

- **PR Workflows**: Check status in pull request checks
- **Merge Workflows**: Monitor in Actions tab after merge
- **Scheduled Workflows**: Review weekly execution reports
- **On-Demand Workflows**: Monitor manual execution progress

### Debug Options

Use the on-demand workflow with debug settings:

```yaml
inputs:
  action_type: 'execute-single'
  single_notebook: 'notebooks/problematic/failing-notebook.ipynb'
  runner_override: 'jwst-pipeline-notebooks-64gb'
  enable_debug: true
```

### Performance Analysis

Track resource usage through:

- Workflow execution times
- Runner selection patterns
- Memory and CPU utilization
- Cost optimization opportunities

## 🔗 Integration with JWST Pipeline

These workflows are specifically designed for:

- **JWST Calibration Pipeline** processing notebooks
- **STScI Science Platforms** integration
- **CRDS Reference Data** access
- **MAST Archive** data retrieval
- **Astronomical data formats** (FITS, ASDF, etc.)

## 📚 Additional Resources

- [Custom Runner Configuration Guide](../../docs/custom-runner-configuration.md)
- [JWST Pipeline Documentation](https://jwst-pipeline.readthedocs.io/)
- [STScI Environments](https://stenv.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

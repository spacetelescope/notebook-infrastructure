# Custom Runner Configuration

The unified workflow now supports custom runner configuration, allowing different notebooks to run on different GitHub runners based on their computational requirements.

## Overview

This feature enables:
- **Resource optimization**: Heavy notebooks run on powerful runners, light notebooks use standard runners
- **Cost efficiency**: Only pay for large runners when actually needed
- **Automatic selection**: Runners are selected based on configuration file
- **Backward compatibility**: Works with existing workflows without changes

## Configuration

### 1. Enable Custom Runners

Add the following parameter to your caller workflow:

```yaml
jobs:
  notebook-ci:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@dev-actions-v2-pipeline
    with:
      # ... other parameters ...
      custom-runner-config: true
```

### 2. Create ci_config.txt

Create a `ci_config.txt` file in your repository root with the format:

```
notebook_path:runner_name
```

#### Configuration File Format

The `ci_config.txt` file uses a simple colon-separated format:

- **One mapping per line**: `path/to/notebook.ipynb:runner-label`
- **Comments supported**: Lines starting with `#` are ignored
- **Wildcards supported**: Use `*` for pattern matching
- **Case sensitive**: Notebook paths must match exactly
- **Relative paths**: Paths are relative to repository root

#### Creating Your First Config File

1. **Identify your notebooks**:

   ```bash
   find notebooks/ -name "*.ipynb" | head -10
   ```

2. **Create the config file**:

   ```bash
   touch ci_config.txt
   ```

3. **Add basic mappings**:

   ```ini
   # Basic tutorial notebooks (lightweight)
   notebooks/tutorials/getting-started.ipynb:ubuntu-latest
   notebooks/examples/hello-world.ipynb:ubuntu-latest
   
   # Data processing notebooks (medium requirements)
   notebooks/analysis/data-processing.ipynb:ubuntu-latest-4-cores
   notebooks/visualization/plotting-demo.ipynb:ubuntu-latest-4-cores
   
   # Heavy computational notebooks (high requirements)
   notebooks/ml/training-pipeline.ipynb:ubuntu-latest-16-cores
   notebooks/simulation/monte-carlo.ipynb:ubuntu-latest-16-cores
   ```

#### Pattern Matching Examples

You can use wildcards to configure multiple notebooks at once:

```ini
# All tutorial notebooks use standard runners
notebooks/tutorials/*.ipynb:ubuntu-latest

# All ML notebooks need high-memory runners
notebooks/machine-learning/*.ipynb:ml-training-64gb

# All benchmark notebooks need maximum resources
notebooks/benchmarks/*.ipynb:performance-testing-128gb

# Specific heavy notebooks
notebooks/pipeline/stage3-association.ipynb:jwst-pipeline-64gb
notebooks/extreme/full-survey-analysis.ipynb:survey-analysis-256gb
```

**Example:**

```ini
# STScI JWST Pipeline Notebook Configuration
# Updated: 2025-08-07
# Maintainer: Pipeline Team

# =============================================================================
# TUTORIAL NOTEBOOKS - Use standard GitHub runners
# =============================================================================
notebooks/tutorials/jwst_pipeline_overview.ipynb:ubuntu-latest
notebooks/tutorials/basic_data_access.ipynb:ubuntu-latest
notebooks/tutorials/instrument_overview.ipynb:ubuntu-latest

# =============================================================================
# STAGE 1 PROCESSING - Medium computational requirements
# =============================================================================
notebooks/NIRCam/stage1/nircam_stage1_imaging.ipynb:jwst-pipeline-notebooks-16gb
notebooks/NIRSpec/stage1/nirspec_stage1_spec.ipynb:jwst-pipeline-notebooks-16gb
notebooks/MIRI/stage1/miri_stage1_imaging.ipynb:jwst-pipeline-notebooks-16gb

# =============================================================================
# STAGE 2 PROCESSING - High computational requirements
# =============================================================================
notebooks/NIRCam/stage2/nircam_stage2_imaging.ipynb:jwst-pipeline-notebooks-32gb
notebooks/NIRSpec/stage2/nirspec_stage2_spec.ipynb:jwst-pipeline-notebooks-32gb
notebooks/MIRI/stage2/miri_stage2_mrs.ipynb:jwst-pipeline-notebooks-64gb

# =============================================================================
# STAGE 3 PROCESSING - Maximum computational requirements
# =============================================================================
notebooks/NIRCam/stage3/nircam_stage3_imaging.ipynb:jwst-pipeline-notebooks-64gb
notebooks/NIRSpec/stage3/nirspec_stage3_spec.ipynb:jwst-pipeline-notebooks-64gb

# =============================================================================
# PERFORMANCE AND VALIDATION NOTEBOOKS
# =============================================================================
notebooks/validation/performance_benchmarks.ipynb:jwst-pipeline-notebooks-64gb
notebooks/validation/memory_stress_test.ipynb:jwst-pipeline-notebooks-128gb
```

### 3. Available Runner Types

The workflow supports any GitHub runner labels configured in your organization:

- **Standard GitHub runners**: `ubuntu-latest`, `windows-latest`, `macos-latest`
- **Larger GitHub runners**: `ubuntu-latest-4-cores`, `ubuntu-latest-8-cores`, etc.
- **Organization custom runners**: Any custom labels you've configured

#### Setting Up Custom Runners

If you need specialized runners for your notebooks, work with your organization administrators to set up:

1. **Self-hosted runners** with specific hardware configurations
2. **Custom runner labels** that match your computational needs
3. **Runner groups** for organizing different types of workloads

**Example runner setup for scientific computing:**

| Runner Label | Specs | Use Case |
|--------------|-------|----------|
| `ubuntu-latest` | 2 cores, 7GB RAM | Tutorials, documentation |
| `ubuntu-latest-4-cores` | 4 cores, 16GB RAM | Light data processing |
| `ubuntu-latest-8-cores` | 8 cores, 32GB RAM | Medium computations |
| `jwst-pipeline-notebooks-16gb` | 4 cores, 16GB RAM | JWST Stage 1 processing |
| `jwst-pipeline-notebooks-32gb` | 8 cores, 32GB RAM | JWST Stage 2 processing |
| `jwst-pipeline-notebooks-64gb` | 16 cores, 64GB RAM | JWST Stage 3 processing |
| `jwst-pipeline-notebooks-128gb` | 32 cores, 128GB RAM | Large survey processing |
| `gpu-enabled-runner` | 8 cores, 32GB RAM, GPU | Machine learning training |

#### Requesting Custom Runners

If you need custom runners that don't exist in your organization:

1. **Identify requirements**:
   - CPU cores needed
   - Memory requirements  
   - Special hardware (GPU, large storage)
   - Operating system requirements

2. **Document use case**:
   - Which notebooks need the custom runner
   - Expected usage patterns
   - Performance benchmarks showing need

3. **Submit request**:
   - Contact your GitHub organization administrators
   - Provide technical specifications and justification
   - Include cost analysis if applicable

## How It Works

### Matrix Generation

When `custom-runner-config: true` is enabled:

1. **Notebook discovery** happens as normal (based on execution mode, changed files, etc.)
2. **Runner lookup** occurs for each discovered notebook in `ci_config.txt`
3. **Enhanced matrix** is created with both notebook path and runner name
4. **Fallback handling** uses `ubuntu-latest` for notebooks not in config

### Example Matrix Output

**Without custom runners:**

```json
{
  "notebook": [
    "notebooks/tutorial.ipynb",
    "notebooks/heavy-processing.ipynb"
  ]
}
```

**With custom runners:**

```json
{
  "include": [
    {"notebook": "notebooks/tutorial.ipynb", "runner": "ubuntu-latest"},
    {"notebook": "notebooks/heavy-processing.ipynb", "runner": "ubuntu-latest-16-cores"}
  ]
}
```

### Job Execution

Each notebook runs on its specified runner:

```yaml
runs-on: ${{ matrix.runner || 'ubuntu-latest' }}
```

## Configuration Examples

### Basic Configuration

Simple setup for repositories with mixed computational needs:

```ini
# ci_config.txt
notebooks/intro/getting-started.ipynb:ubuntu-latest
notebooks/analysis/heavy-computation.ipynb:ubuntu-latest-8-cores
notebooks/ml/training-pipeline.ipynb:ubuntu-latest-16-cores
```

### Advanced Configuration

Complex setup for scientific computing:

```ini
# ci_config.txt
# Light tutorials and examples
notebooks/tutorials/basic-usage.ipynb:ubuntu-latest
notebooks/examples/quick-start.ipynb:ubuntu-latest

# Medium computational requirements
notebooks/data-analysis/photometry.ipynb:jwst-pipeline-16gb
notebooks/spectroscopy/line-fitting.ipynb:jwst-pipeline-16gb

# Heavy processing requirements
notebooks/pipeline/stage1-detector.ipynb:jwst-pipeline-32gb
notebooks/pipeline/stage2-calibration.ipynb:jwst-pipeline-32gb
notebooks/pipeline/stage3-association.ipynb:jwst-pipeline-64gb

# Extreme cases
notebooks/performance/full-mosaic.ipynb:jwst-pipeline-64gb
notebooks/benchmark/stress-test.ipynb:jwst-pipeline-64gb
```

## Managing Your Configuration File

### Adding New Notebooks

When you add new notebooks to your repository:

1. **Determine computational requirements**:
   - Small tutorials/examples → `ubuntu-latest`
   - Data processing → `ubuntu-latest-4-cores` or `ubuntu-latest-8-cores`
   - Heavy computation → `ubuntu-latest-16-cores` or custom runners
   - Extreme cases → High-memory custom runners

2. **Add to ci_config.txt**:

   ```bash
   # Add a single notebook
   echo "notebooks/new-analysis/data-processing.ipynb:ubuntu-latest-8-cores" >> ci_config.txt
   
   # Or edit the file directly
   nano ci_config.txt
   ```

3. **Test the configuration**:
   - Use manual workflow dispatch to test specific notebooks
   - Check workflow logs for runner selection
   - Monitor execution times and resource usage

### Bulk Configuration Updates

For large repositories, you can use scripts to generate configurations:

```bash
#!/bin/bash
# generate_config.sh - Generate ci_config.txt based on notebook locations

echo "# Auto-generated CI configuration - $(date)" > ci_config.txt
echo "" >> ci_config.txt

# Tutorial notebooks - lightweight
echo "# Tutorial notebooks (standard runners)" >> ci_config.txt
find notebooks/tutorials -name "*.ipynb" | while read -r notebook; do
    echo "${notebook}:ubuntu-latest" >> ci_config.txt
done

echo "" >> ci_config.txt

# Analysis notebooks - medium requirements  
echo "# Analysis notebooks (medium runners)" >> ci_config.txt
find notebooks/analysis -name "*.ipynb" | while read -r notebook; do
    echo "${notebook}:ubuntu-latest-8-cores" >> ci_config.txt
done

echo "" >> ci_config.txt

# Pipeline notebooks - high requirements
echo "# Pipeline notebooks (high-performance runners)" >> ci_config.txt
find notebooks/pipeline -name "*.ipynb" | while read -r notebook; do
    echo "${notebook}:jwst-pipeline-notebooks-32gb" >> ci_config.txt
done
```

### Configuration Validation

Validate your configuration file before committing:

```bash
#!/bin/bash
# validate_config.sh - Validate ci_config.txt format

config_file="ci_config.txt"

if [[ ! -f "$config_file" ]]; then
    echo "❌ ci_config.txt not found"
    exit 1
fi

echo "🔍 Validating ci_config.txt..."

# Check format
while IFS= read -r line; do
    # Skip comments and empty lines
    [[ "$line" =~ ^#.*$ ]] && continue
    [[ -z "$line" ]] && continue
    
    # Check format: path:runner
    if [[ ! "$line" =~ ^[^:]+:[^:]+$ ]]; then
        echo "❌ Invalid format: $line"
        echo "   Expected: notebook_path:runner_name"
        exit 1
    fi
    
    # Extract notebook path and check if file exists
    notebook=$(echo "$line" | cut -d':' -f1)
    runner=$(echo "$line" | cut -d':' -f2)
    
    # Check if notebook exists (handle wildcards)
    if [[ "$notebook" != *"*"* ]] && [[ ! -f "$notebook" ]]; then
        echo "⚠️  Notebook not found: $notebook"
    fi
    
    echo "✅ $notebook → $runner"
    
done < "$config_file"

echo "✅ Configuration validation complete"
```

### Performance Optimization

Monitor and optimize your runner assignments:

1. **Track execution times**:

   ```bash
   # Extract execution times from workflow logs
   gh run list --workflow="notebook-pr.yml" --limit=10 --json conclusion,createdAt,url
   ```

2. **Identify over/under-provisioned notebooks**:
   - Notebooks finishing too quickly on large runners → downgrade
   - Notebooks timing out on standard runners → upgrade
   - Notebooks with memory errors → increase memory allocation

3. **Cost optimization**:
   - Monitor runner costs in your organization
   - Use standard runners for development/testing
   - Reserve expensive runners for production and critical workloads

### Dynamic Configuration

For advanced use cases, you can create dynamic configurations:

```bash
#!/bin/bash
# dynamic_config.sh - Generate config based on notebook content analysis

echo "# Dynamic configuration generated $(date)" > ci_config.txt

find notebooks -name "*.ipynb" | while read -r notebook; do
    # Analyze notebook for resource hints
    if grep -q "# REQUIRES: high-memory" "$notebook"; then
        echo "${notebook}:ubuntu-latest-16-cores" >> ci_config.txt
    elif grep -q "# REQUIRES: gpu" "$notebook"; then
        echo "${notebook}:gpu-enabled-runner" >> ci_config.txt
    elif grep -q "import tensorflow\|import torch\|import sklearn" "$notebook"; then
        echo "${notebook}:ubuntu-latest-8-cores" >> ci_config.txt
    else
        echo "${notebook}:ubuntu-latest" >> ci_config.txt
    fi
done
```

### Version Control Best Practices

1. **Track changes**:
   - Commit `ci_config.txt` to version control
   - Use descriptive commit messages for configuration changes
   - Document reasoning in commit messages

2. **Review process**:
   - Include configuration changes in pull request reviews
   - Test configuration changes in development branches
   - Monitor first runs after configuration updates

3. **Documentation**:
   - Keep inline comments in `ci_config.txt` updated
   - Document custom runner capabilities in repository README
   - Maintain a changelog for significant configuration changes

## Best Practices

### 1. Runner Selection Guidelines

- **Standard runners** (`ubuntu-latest`): Tutorials, documentation, light processing
- **4-core runners**: Medium data processing, moderate computations
- **8-core runners**: Heavy data processing, complex algorithms
- **16-core runners**: Large datasets, parallel processing, ML training
- **Custom runners**: Specialized requirements (GPU, high memory, etc.)

### 2. Cost Optimization

- **Default to standard**: Only specify custom runners when actually needed
- **Progressive sizing**: Start with smaller runners and upgrade if needed
- **Monitor usage**: Track runner usage to optimize configuration

### 3. Configuration Management

- **Document requirements**: Comment your `ci_config.txt` with reasoning
- **Version control**: Include `ci_config.txt` in your repository
- **Review regularly**: Update runner assignments as notebooks evolve

## Fallback Behavior

The feature is designed to be robust:

- **Missing config file**: All notebooks use default runner (`ubuntu-latest`)
- **Notebook not in config**: Uses default runner automatically
- **Invalid runner name**: GitHub Actions will fail with clear error message
- **Feature disabled**: Works exactly like before (backward compatible)

## Troubleshooting

### Common Issues

1. **Runner not found error**
   - **Symptoms**: Workflow fails with "No runner found with label 'custom-runner'"
   - **Causes**:
     - Runner label doesn't exist in organization
     - Typo in `ci_config.txt`
     - Runner is offline or busy
   - **Solutions**:
     - Check available runners in organization settings
     - Verify spelling in `ci_config.txt`
     - Contact organization administrators about runner availability

2. **Config not working**
   - **Symptoms**: All notebooks still run on `ubuntu-latest` despite configuration
   - **Causes**:
     - `custom-runner-config: true` not set in caller workflow
     - `ci_config.txt` not in repository root
     - File format errors
   - **Solutions**:
     - Ensure `custom-runner-config: true` is set in caller workflow
     - Verify `ci_config.txt` is in repository root (not in subdirectory)
     - Check file format (no extra spaces, correct colons)
     - Validate using the validation script above

3. **Performance issues**
   - **Symptoms**: Workflows taking longer than expected, runner queue delays
   - **Causes**:
     - Over-assignment to expensive runners
     - Too much parallelism for available runners
     - Inefficient notebook computational patterns
   - **Solutions**:
     - Monitor runner queue times in organization
     - Reduce `max_parallel` for expensive runners
     - Optimize notebook computational requirements
     - Use time-based analysis to right-size runner assignments

4. **Cost concerns**
   - **Symptoms**: Higher than expected GitHub Actions costs
   - **Causes**:
     - Overuse of large runners
     - Long-running notebooks on expensive runners
     - Inefficient runner allocation
   - **Solutions**:
     - Audit `ci_config.txt` for oversized assignments
     - Monitor workflow costs in organization billing
     - Implement cost controls and quotas
     - Use standard runners for development/testing

### Debug Steps

1. **Check workflow logs** for "Custom runner configuration" messages:

   ```bash
   # Search for configuration messages in recent workflow runs
   gh run list --workflow="notebook-pr.yml" --limit=5
   gh run view <run-id> --log | grep -i "custom runner\|matrix\|runner"
   ```

2. **Verify matrix output** in setup-matrix job logs:
   - Look for "Generated matrix" output
   - Confirm notebook-to-runner mappings
   - Check for fallback assignments

3. **Confirm runner assignment** in individual notebook job logs:
   - Check job headers for `runs-on` assignment
   - Verify actual runner used in job execution
   - Look for runner-specific environment details

4. **Test with single notebook** using on-demand mode:

   ```yaml
   # Use workflow_dispatch to test specific configurations
   workflow_dispatch:
     inputs:
       action_type: 'execute-single'
       single_notebook: 'notebooks/problematic/test-notebook.ipynb'
       runner_override: 'custom-runner-label'
   ```

### Configuration Testing

Before deploying configuration changes to production:

1. **Test in development branch**:
   - Create feature branch with configuration changes
   - Run PR workflows to test configuration
   - Monitor for errors and performance issues

2. **Gradual rollout**:
   - Start with subset of notebooks
   - Monitor execution and costs
   - Expand configuration incrementally

3. **Monitoring checklist**:
   - ✅ Workflow completion rate
   - ✅ Average execution times
   - ✅ Runner queue wait times
   - ✅ Cost per workflow run
   - ✅ Error rates and types

### Getting Help

If you encounter issues not covered here:

1. **Check workflow logs** for detailed error messages
2. **Review GitHub Actions documentation** for runner-specific issues
3. **Contact organization administrators** for runner availability and configuration
4. **File issues** in the notebook-ci-actions repository for workflow-specific problems
5. **Consult GitHub Support** for GitHub Actions platform issues

### Performance Monitoring

Set up monitoring to track configuration effectiveness:

```bash
#!/bin/bash
# monitor_performance.sh - Track workflow performance metrics

echo "📊 Workflow Performance Analysis"
echo "================================"

# Get recent workflow runs
runs=$(gh run list --workflow="notebook-pr.yml" --limit=20 --json id,conclusion,createdAt,updatedAt)

# Calculate average execution times
echo "$runs" | jq -r '.[] | select(.conclusion == "success") | 
  "\(.createdAt) \(.updatedAt)"' | while read -r start end; do
    start_epoch=$(date -d "$start" +%s)
    end_epoch=$(date -d "$end" +%s)
    duration=$((end_epoch - start_epoch))
    echo "$duration"
done | awk '{sum+=$1; count++} END {print "Average execution time:", sum/count/60, "minutes"}'

# Check for failed runs
failed_count=$(echo "$runs" | jq '[.[] | select(.conclusion != "success")] | length')
total_count=$(echo "$runs" | jq 'length')
success_rate=$(echo "scale=2; ($total_count - $failed_count) * 100 / $total_count" | bc)

echo "Success rate: $success_rate%"
echo "Failed runs: $failed_count out of $total_count"
```

## Migration Guide

### Existing Workflows

No changes required! The feature is completely optional:

```yaml
# Before - works exactly the same
uses: notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@dev-actions-v2-pipeline
with:
  execution-mode: 'pr'

# After - same behavior, custom runners available if needed
uses: notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@dev-actions-v2-pipeline
with:
  execution-mode: 'pr'
  custom-runner-config: true  # Optional addition
```

### Gradual Adoption

1. **Start simple**: Add `custom-runner-config: true` with empty `ci_config.txt`
2. **Identify heavy notebooks**: Monitor which notebooks take longest/use most memory
3. **Add selective config**: Configure only problematic notebooks initially
4. **Expand gradually**: Add more configurations as needed

## Examples

See the `examples/` directory for complete workflow examples:

- `examples/caller-workflows/jwst-validation-notebooks.yml` - Full custom runner setup
- `examples/ci_config.txt` - Sample configuration file
- `examples/caller-workflows/hellouniverse.yml` - Standard setup (no custom runners)

# Complete Example: Multi-Repository Setup

This example demonstrates how to set up the unified notebook CI/CD system across different types of repositories.

## Repository Type: HST Notebooks

### Directory Structure
```
hst-notebooks/
├── .github/
│   └── workflows/
│       ├── notebook-pr.yml
│       ├── notebook-merge.yml
│       ├── notebook-scheduled.yml
│       └── notebook-on-demand.yml
├── notebooks/
│   ├── acs/
│   │   ├── calibration.ipynb
│   │   └── requirements.txt
│   ├── wfc3/
│   │   ├── photometry.ipynb
│   │   └── requirements.txt
│   └── README.md
├── scripts/
│   └── hst_post_processing.sh
├── _config.yml
├── _toc.yml
└── requirements.txt
```

### Pull Request Workflow (`.github/workflows/notebook-pr.yml`)

```yaml
name: HST Notebook CI - Pull Request

on:
  pull_request:
    branches: [ main ]
    paths:
      - 'notebooks/**'
      - 'requirements.txt'
      - 'pyproject.toml'
      - '*.yml'
      - '*.yaml'
      - '*.md'

jobs:
  hst-notebook-ci:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@main
    with:
      execution-mode: 'pr'
      python-version: '3.11'
      conda-environment: 'hstcal'
      enable-validation: true
      enable-security: true
      enable-execution: true
      enable-storage: true
      enable-html-build: false
    secrets:
      CASJOBS_USERID: ${{ secrets.CASJOBS_USERID }}
      CASJOBS_PW: ${{ secrets.CASJOBS_PW }}
```

### Merge/Deploy Workflow (`.github/workflows/notebook-merge.yml`)

```yaml
name: HST Notebook CI - Deploy

on:
  push:
    branches: [ main ]
    paths:
      - 'notebooks/**'
      - 'requirements.txt'
      - 'pyproject.toml'
      - '*.yml'
      - '*.yaml'
      - '*.md'

jobs:
  hst-deploy:
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
      post-processing-script: 'scripts/hst_post_processing.sh'
    secrets:
      CASJOBS_USERID: ${{ secrets.CASJOBS_USERID }}
      CASJOBS_PW: ${{ secrets.CASJOBS_PW }}
```

### Post-Processing Script (`scripts/hst_post_processing.sh`)

```bash
#!/bin/bash
# HST-specific post-processing

echo "🔧 Running HST post-processing..."

# Optimize images for web display
echo "Optimizing images..."
find _build -name "*.png" -exec optipng -o2 {} \;
find _build -name "*.jpg" -exec jpegoptim --max=85 {} \;

# Generate HST-specific metadata
echo "Generating HST metadata..."
python3 << 'EOF'
import json
import os
from pathlib import Path

# Generate instrument metadata
instruments = {
    "acs": "Advanced Camera for Surveys",
    "wfc3": "Wide Field Camera 3",
    "stis": "Space Telescope Imaging Spectrograph",
    "cos": "Cosmic Origins Spectrograph"
}

metadata = {
    "mission": "Hubble Space Telescope",
    "instruments": instruments,
    "generated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}

with open("_build/html/hst_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("HST metadata generated")
EOF

# Copy HST-specific assets
if [ -d "assets/hst" ]; then
    echo "Copying HST assets..."
    cp -r assets/hst/* _build/html/
fi

echo "✅ HST post-processing complete"
```

## Repository Type: JWST Notebooks

### Directory Structure
```
jwst-notebooks/
├── .github/workflows/
├── notebooks/
│   ├── nircam/
│   │   ├── imaging.ipynb
│   │   └── requirements.txt
│   ├── nirspec/
│   │   ├── spectroscopy.ipynb
│   │   └── requirements.txt
│   └── miri/
│       ├── photometry.ipynb
│       └── requirements.txt
├── scripts/
│   └── jwst_post_processing.sh
└── environment.yml
```

### JWST Configuration

```yaml
# .github/workflows/notebook-pr.yml
name: JWST Notebook CI - Pull Request

on:
  pull_request:
    branches: [ main ]
    paths:
      - 'notebooks/**'
      - 'environment.yml'
      - 'requirements.txt'
      - '*.yml'

jobs:
  jwst-notebook-ci:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@main
    with:
      execution-mode: 'pr'
      python-version: '3.11'
      conda-environment: 'stenv'
      enable-validation: true
      enable-security: true
      enable-execution: true
      enable-storage: true
      enable-html-build: false
    secrets:
      CASJOBS_USERID: ${{ secrets.CASJOBS_USERID }}
      CASJOBS_PW: ${{ secrets.CASJOBS_PW }}
```

## Repository Type: Multi-Mission Documentation

### Directory Structure
```
astronomy-tutorials/
├── .github/workflows/
├── notebooks/
│   ├── data-analysis/
│   ├── visualization/
│   └── photometry/
├── docs/
│   ├── index.md
│   └── tutorials/
├── scripts/
│   └── docs_optimization.sh
└── requirements.txt
```

### Documentation-Focused Configuration

```yaml
# .github/workflows/notebook-merge.yml
name: Astronomy Tutorials - Deploy

on:
  push:
    branches: [ main ]

jobs:
  docs-deploy:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@main
    with:
      execution-mode: 'merge'
      python-version: '3.11'
      custom-requirements: 'requirements.txt'
      enable-validation: true
      enable-security: false          # Skip security for documentation
      enable-execution: true
      enable-storage: true
      enable-html-build: true
      post-processing-script: 'scripts/docs_optimization.sh'
    secrets:
      CASJOBS_USERID: ${{ secrets.CASJOBS_USERID }}
      CASJOBS_PW: ${{ secrets.CASJOBS_PW }}
```

## Advanced Use Cases

### 1. High-Performance Repository

For repositories with resource-intensive notebooks:

```yaml
# .github/workflows/notebook-pr.yml (Performance optimized)
name: High-Performance Notebook CI

on:
  pull_request:
    branches: [ main ]
    paths:
      - 'notebooks/**'

jobs:
  performance-ci:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@main
    with:
      execution-mode: 'pr'
      python-version: '3.11'
      conda-environment: 'stenv'
      enable-validation: false        # Skip validation for speed
      enable-security: false          # Skip security for speed
      enable-execution: true          # Only execute notebooks
      enable-storage: false           # Skip storage for speed
      enable-html-build: false
    secrets:
      CASJOBS_USERID: ${{ secrets.CASJOBS_USERID }}
      CASJOBS_PW: ${{ secrets.CASJOBS_PW }}
```

### 2. Security-Focused Repository

For repositories with strict security requirements:

```yaml
# .github/workflows/notebook-pr.yml (Security focused)
name: Secure Notebook CI

on:
  pull_request:
    branches: [ main ]

jobs:
  security-ci:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@main
    with:
      execution-mode: 'pr'
      python-version: '3.11'
      enable-validation: true
      enable-security: true           # Always run security scans
      enable-execution: false         # Don't execute in PR for security
      enable-storage: false           # Don't store unverified outputs
      enable-html-build: false
    secrets:
      CASJOBS_USERID: ${{ secrets.CASJOBS_USERID }}
      CASJOBS_PW: ${{ secrets.CASJOBS_PW }}

  # Separate execution job for approved PRs
  execution-ci:
    needs: security-ci
    if: github.event.pull_request.draft == false
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@main
    with:
      execution-mode: 'pr'
      python-version: '3.11'
      enable-validation: false
      enable-security: false
      enable-execution: true
      enable-storage: true
      enable-html-build: false
    secrets:
      CASJOBS_USERID: ${{ secrets.CASJOBS_USERID }}
      CASJOBS_PW: ${{ secrets.CASJOBS_PW }}
```

### 3. Development vs Production

Different configurations for development and production:

```yaml
# .github/workflows/notebook-dev.yml (Development)
name: Development Notebook CI

on:
  pull_request:
    branches: [ develop ]

jobs:
  dev-ci:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@main
    with:
      execution-mode: 'pr'
      python-version: '3.11'
      enable-validation: true
      enable-security: false          # Skip security in dev
      enable-execution: true
      enable-storage: false           # Don't store dev outputs
      enable-html-build: false        # No HTML in dev
```

```yaml
# .github/workflows/notebook-prod.yml (Production)
name: Production Notebook CI

on:
  push:
    branches: [ main ]

jobs:
  prod-ci:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@main
    with:
      execution-mode: 'merge'
      python-version: '3.11'
      conda-environment: 'stenv'
      enable-validation: true
      enable-security: true           # Full security in production
      enable-execution: true
      enable-storage: true            # Store production outputs
      enable-html-build: true         # Build docs in production
      post-processing-script: 'scripts/production_processing.sh'
    secrets:
      CASJOBS_USERID: ${{ secrets.CASJOBS_USERID }}
      CASJOBS_PW: ${{ secrets.CASJOBS_PW }}
```

## On-Demand Workflow Examples

### 1. Quick Validation

```yaml
# Triggered manually for quick validation
name: Quick Validation

on:
  workflow_dispatch:
    inputs:
      notebook_path:
        description: 'Notebook to validate'
        required: true
        type: string

jobs:
  quick-validate:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@main
    with:
      execution-mode: 'on-demand'
      trigger-event: 'validate'
      single-notebook: ${{ inputs.notebook_path }}
      python-version: '3.11'
      enable-validation: true
      enable-security: false
      enable-execution: false
      enable-storage: false
      enable-html-build: false
```

### 2. Emergency Documentation Rebuild

```yaml
# For urgent documentation updates
name: Emergency Docs Rebuild

on:
  workflow_dispatch:

jobs:
  emergency-docs:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@main
    with:
      execution-mode: 'on-demand'
      trigger-event: 'html'
      python-version: '3.11'
      enable-validation: false
      enable-security: false
      enable-execution: false
      enable-storage: false
      enable-html-build: true
      post-processing-script: 'scripts/emergency_processing.sh'
```

### 3. Batch Notebook Deprecation

```yaml
# For deprecating multiple notebooks
name: Batch Deprecation

on:
  workflow_dispatch:
    inputs:
      deprecation_days:
        description: 'Days until deprecation'
        required: false
        type: string
        default: '60'

jobs:
  # This would be expanded to handle multiple notebooks
  deprecation-management:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@main
    with:
      execution-mode: 'scheduled'
      trigger-event: 'deprecate'
      python-version: '3.11'
      deprecation-days: ${{ fromJSON(inputs.deprecation_days) }}
```

## Configuration Files

### JupyterBook Configuration (`_config.yml`)

```yaml
title: "Notebook Repository"
author: "Space Telescope Science Institute"
logo: logo.png

# Configure execution
execute:
  execute_notebooks: "off"  # Use pre-executed notebooks from gh-storage
  timeout: 1200             # 20 minute timeout
  allow_errors: false

# Configure HTML output
html:
  use_edit_page_button: true
  use_repository_button: true
  use_issues_button: true
  home_page_in_navbar: false

# Repository configuration
repository:
  url: https://github.com/your-org/your-repo
  branch: main

# LaTeX configuration
latex:
  latex_documents:
    targetname: book.tex
```

### Table of Contents (`_toc.yml`)

```yaml
format: jb-book
root: index
options:
  numbered: true

chapters:
  - file: notebooks/README
    title: Overview
  - file: notebooks/getting-started
    title: Getting Started
  - caption: Instruments
    chapters:
      - file: notebooks/hst/index
        title: HST
        sections:
          - glob: notebooks/hst/*/index
      - file: notebooks/jwst/index
        title: JWST
        sections:
          - glob: notebooks/jwst/*/index
  - caption: Advanced Topics
    chapters:
      - glob: notebooks/advanced/*.ipynb
```

## Testing and Validation

### Local Testing Setup

```bash
# Create test environment
conda create -n test-ci python=3.11
conda activate test-ci

# Install dependencies
pip install jupyter nbval pytest bandit

# Test individual notebook
pytest --nbval notebooks/example/demo.ipynb

# Test security
jupyter nbconvert --to script notebooks/example/demo.ipynb
bandit notebooks/example/demo.py

# Test execution
jupyter nbconvert --to notebook --execute --inplace notebooks/example/demo.ipynb
```

### Integration Testing

```yaml
# .github/workflows/integration-test.yml
name: Integration Test

on:
  schedule:
    - cron: '0 6 * * 1'  # Weekly Monday morning
  workflow_dispatch:

jobs:
  test-all-modes:
    strategy:
      matrix:
        mode: ['pr', 'merge', 'scheduled', 'on-demand']
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@main
    with:
      execution-mode: ${{ matrix.mode }}
      python-version: '3.11'
      enable-validation: true
      enable-security: true
      enable-execution: true
      enable-storage: false  # Don't store test outputs
      enable-html-build: false
```

This comprehensive example demonstrates how to configure the unified notebook CI/CD system for various repository types and use cases, providing templates that can be adapted to specific needs.

## 🆕 Latest Updates

This example has been updated to include the latest features and best practices:

- **Smart Change Detection**: Automatic optimization based on file changes
- **Enhanced Error Handling**: Better debugging and error reporting
- **Performance Optimizations**: Up to 85% faster execution for docs-only changes
- **Integrated Security**: Bandit security scanning with configurable thresholds
- **Improved Storage**: Reliable gh-storage integration with better error handling
- **Repository-Specific Defaults**: Auto-detection for hst_notebooks, jdat_notebooks, etc.

## Migration from Previous Systems

If you're migrating from the older selective/smart workflow systems:

```bash
# Use the automated migration script
cd your-repository
../notebook-ci-actions/scripts/migrate-to-unified.sh

# Or follow the manual migration guide
# See docs/migration-guide-unified.md for detailed instructions
```

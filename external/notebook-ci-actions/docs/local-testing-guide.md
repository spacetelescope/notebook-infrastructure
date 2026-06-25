# Local Testing Guide for GitHub Actions Workflows

This guide provides comprehensive methods for testing GitHub Actions workflows locally before pushing changes to GitHub. Local testing helps catch issues early, reduces CI/CD costs, and speeds up development.

## 📋 Table of Contents

- [Overview](#overview)
- [Testing Tools](#testing-tools)
- [Quick Start](#quick-start)
- [Act - Local GitHub Actions Runner](#act---local-github-actions-runner)
- [Manual Testing Approaches](#manual-testing-approaches)
- [Repository-Specific Testing](#repository-specific-testing)
- [CI/CD Validation Scripts](#cicd-validation-scripts)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## 🎯 Overview

Testing GitHub Actions workflows locally is crucial for:

- **Cost Reduction**: Avoid consuming GitHub Actions minutes during development
- **Faster Development**: Test changes immediately without waiting for GitHub runners
- **Debugging**: Access to local environment for detailed debugging
- **Validation**: Ensure workflows work across different environments
- **Security**: Test with secrets and sensitive data safely

## 🛠️ Testing Tools

### 1. Act - GitHub Actions Local Runner

**Act** is the most popular tool for running GitHub Actions workflows locally.

#### Installation

```bash
# macOS (Homebrew)
brew install act

# Linux (curl)
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Windows (Chocolatey)
choco install act-cli

# Docker (alternative)
docker pull ghcr.io/catthehacker/ubuntu:act-latest
```

#### Verification
```bash
act --version
```

### 2. GitHub CLI with Workflow Dispatch

```bash
# Install GitHub CLI
# macOS
brew install gh

# Linux
sudo apt install gh

# Windows
winget install GitHub.cli

# Authenticate
gh auth login
```

### 3. Local Environment Simulation

Create local scripts that simulate the GitHub Actions environment.

## 🚀 Quick Start

### Basic Act Usage

1. **Navigate to your repository**:
   ```bash
   cd your-notebook-repository
   ```

2. **List available workflows**:
   ```bash
   act --list
   ```

3. **Run a specific workflow**:
   ```bash
   # Run pull request workflow
   act pull_request
   
   # Run push workflow
   act push
   
   # Run specific job
   act -j test-notebooks
   ```

4. **Run with secrets**:
   ```bash
   act -s GITHUB_TOKEN=your_token pull_request
   ```

### Quick Validation

```bash
# Validate workflow syntax
act --dryrun

# Check what would run
act --list --verbose
```

## 🔧 Act - Local GitHub Actions Runner

### Configuration

Create `.actrc` file in your repository root:

```bash
# .actrc
--container-architecture linux/amd64
--platform ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-latest
--artifact-server-path /tmp/artifacts
--env GITHUB_ACTIONS=true
--env CI=true
```

### Environment Variables

Create `.env` file for secrets and variables:

```bash
# .env
GITHUB_TOKEN=ghp_your_token_here
CASJOBS_USERID=your_userid
CASJOBS_PW=your_password
PYTHON_VERSION=3.11
```

### Advanced Act Usage

#### Testing Specific Events

```bash
# Test pull request events
act pull_request --eventpath .github/events/pr.json

# Test push events
act push --eventpath .github/events/push.json

# Test manual dispatch
act workflow_dispatch --eventpath .github/events/dispatch.json
```

#### Custom Event Payloads

Create event JSON files:

```json
# .github/events/pr.json
{
  "pull_request": {
    "number": 1,
    "base": {
      "ref": "main"
    },
    "head": {
      "ref": "feature-branch"
    }
  },
  "repository": {
    "name": "test-repo",
    "full_name": "user/test-repo"
  }
}
```

#### Running with Docker

```bash
# Use specific runner image
act --platform ubuntu-latest=ubuntu:20.04

# With custom Docker image
act --platform ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-latest
```

## 📋 Manual Testing Approaches

### 1. Script-Based Testing

Create local testing scripts that simulate workflow steps:

```bash
#!/bin/bash
# scripts/test-local-ci.sh

set -euo pipefail

echo "🚀 Starting local CI simulation..."

# Simulate environment setup
export PYTHON_VERSION=${PYTHON_VERSION:-3.11}
export CI=true
export GITHUB_ACTIONS=true

# Step 1: Environment setup
echo "📦 Setting up Python environment..."
python -m venv venv
source venv/bin/activate
pip install uv

# Step 2: Install dependencies
echo "📚 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    uv pip install -r requirements.txt
elif [ -f "pyproject.toml" ]; then
    uv pip install -e .
fi

# Step 3: Install notebook tools
echo "🔧 Installing notebook validation tools..."
uv pip install jupyter nbval nbconvert bandit

# Step 4: Validate notebooks
echo "✅ Validating notebooks..."
if [ -d "notebooks" ]; then
    find notebooks -name "*.ipynb" -exec jupyter nbconvert --to notebook --execute --inplace {} \;
    pytest --nbval notebooks/
fi

# Step 5: Security scan
echo "🔒 Running security scan..."
find notebooks -name "*.ipynb" -exec jupyter nbconvert --to script {} \;
find notebooks -name "*.py" -exec bandit -r {} \; || true

# Step 6: Build documentation
echo "📖 Building documentation..."
if [ -f "_config.yml" ] && [ -f "_toc.yml" ]; then
    jupyter-book build .
fi

echo "✅ Local CI simulation completed!"
```

### 2. Docker-Based Testing

Create a Dockerfile that simulates the GitHub Actions environment:

```dockerfile
# Dockerfile.local-ci
FROM ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip3 install uv

# Set working directory
WORKDIR /workspace

# Copy repository
COPY . .

# Install dependencies
RUN if [ -f "requirements.txt" ]; then uv pip install -r requirements.txt; fi
RUN uv pip install jupyter nbval nbconvert bandit jupyter-book

# Run tests
CMD ["bash", "scripts/test-local-ci.sh"]
```

Test with Docker:

```bash
# Build test image
docker build -f Dockerfile.local-ci -t local-ci-test .

# Run tests
docker run --rm -v $(pwd):/workspace local-ci-test
```

### 3. GitHub CLI Workflow Dispatch

Test workflows using manual dispatch:

```bash
# Trigger workflow manually
gh workflow run "Notebook CI - On Demand" \
  --field python-version=3.11 \
  --field execution-mode=validation-only \
  --field run-security-scan=true

# Monitor workflow run
gh run list --limit 1
gh run view --log
```

## 🎯 Repository-Specific Testing

### Testing Centralized Workflows

For repositories using the centralized workflow system:

```bash
#!/bin/bash
# scripts/test-centralized-workflows.sh

REPO_NAME=${1:-$(basename $(pwd))}
ORG_NAME=${2:-spacetelescope}

echo "Testing centralized workflows for $REPO_NAME..."

# Test workflow syntax
echo "🔍 Validating workflow syntax..."
for workflow in .github/workflows/*.yml; do
    echo "Checking $workflow..."
    act --dryrun --workflow "$workflow" || echo "❌ Syntax error in $workflow"
done

# Test with different events
echo "🧪 Testing different trigger events..."

# Test PR workflow
if [ -f ".github/workflows/notebook-ci-pr.yml" ]; then
    echo "Testing PR workflow..."
    act pull_request --workflow .github/workflows/notebook-ci-pr.yml --dryrun
fi

# Test main branch workflow
if [ -f ".github/workflows/notebook-ci-main.yml" ]; then
    echo "Testing main branch workflow..."
    act push --workflow .github/workflows/notebook-ci-main.yml --dryrun
fi

# Test on-demand workflow
if [ -f ".github/workflows/notebook-ci-on-demand.yml" ]; then
    echo "Testing on-demand workflow..."
    act workflow_dispatch --workflow .github/workflows/notebook-ci-on-demand.yml --dryrun
fi

echo "✅ Centralized workflow testing completed!"
```

### Repository-Specific Configurations

```bash
#!/bin/bash
# scripts/test-repo-config.sh

REPO_NAME=$(basename $(pwd))

case "$REPO_NAME" in
    "jdat_notebooks")
        echo "🔭 Testing JDAT notebooks configuration..."
        export CRDS_SERVER_URL="https://jwst-crds.stsci.edu"
        export CRDS_PATH="/tmp/crds_cache"
        ;;
    "mast_notebooks")
        echo "🌌 Testing MAST notebooks configuration..."
        # Test MAST API connectivity
        python -c "import astroquery.mast; print('MAST connection OK')" || echo "❌ MAST connection failed"
        ;;
    "hst_notebooks")
        echo "🔭 Testing HST notebooks configuration..."
        # Test hstcal environment
        python -c "import hstcal; print('hstcal OK')" || echo "⚠️ hstcal not available (expected in local environment)"
        ;;
    "hellouniverse")
        echo "🌟 Testing Hello Universe configuration..."
        # Simplified testing
        ;;
    "jwst-pipeline-notebooks")
        echo "🚀 Testing JWST pipeline configuration..."
        # Test jdaviz availability
        python -c "import jdaviz; print('jdaviz OK')" || echo "⚠️ jdaviz not available (expected in local environment)"
        ;;
    *)
        echo "📝 Testing generic notebook configuration..."
        ;;
esac
```

## 📋 CI/CD Validation Scripts

### Pre-Commit Workflow Validation

```bash
#!/bin/bash
# scripts/pre-commit-workflow-check.sh

echo "🔍 Pre-commit workflow validation..."

# Check workflow syntax
echo "Validating YAML syntax..."
for workflow in .github/workflows/*.yml .github/workflows/*.yaml; do
    if [ -f "$workflow" ]; then
        python -c "import yaml; yaml.safe_load(open('$workflow'))" || {
            echo "❌ YAML syntax error in $workflow"
            exit 1
        }
    fi
done

# Check for required fields
echo "Checking required workflow fields..."
for workflow in .github/workflows/*.yml; do
    if [ -f "$workflow" ]; then
        if ! grep -q "name:" "$workflow"; then
            echo "❌ Missing 'name' field in $workflow"
            exit 1
        fi
        if ! grep -q "on:" "$workflow"; then
            echo "❌ Missing 'on' field in $workflow"
            exit 1
        fi
    fi
done

# Check workflow references
echo "Validating workflow references..."
for workflow in .github/workflows/*.yml; do
    if [ -f "$workflow" ]; then
        # Check for placeholder references
        if grep -q "your-org\|dev-actions" "$workflow"; then
            echo "❌ Found placeholder references in $workflow"
            echo "Please update organization and repository names"
            exit 1
        fi
    fi
done

echo "✅ Pre-commit workflow validation passed!"
```

### Integration Testing

```bash
#!/bin/bash
# scripts/integration-test.sh

set -euo pipefail

echo "🧪 Running integration tests..."

# Test 1: Notebook execution
echo "📓 Testing notebook execution..."
if [ -d "notebooks" ]; then
    # Find a simple notebook for testing
    test_notebook=$(find notebooks -name "*.ipynb" | head -1)
    if [ -n "$test_notebook" ]; then
        echo "Testing with: $test_notebook"
        jupyter nbconvert --to notebook --execute --inplace "$test_notebook"
        echo "✅ Notebook execution successful"
    else
        echo "⚠️ No notebooks found for testing"
    fi
fi

# Test 2: Documentation building
echo "📖 Testing documentation build..."
if [ -f "_config.yml" ] && [ -f "_toc.yml" ]; then
    jupyter-book build . --path-output /tmp/test-build
    if [ -d "/tmp/test-build/_build/html" ]; then
        echo "✅ Documentation build successful"
    else
        echo "❌ Documentation build failed"
        exit 1
    fi
else
    echo "⚠️ No JupyterBook configuration found"
fi

# Test 3: Security scan
echo "🔒 Testing security scan..."
if [ -d "notebooks" ]; then
    # Convert notebooks to Python scripts
    find notebooks -name "*.ipynb" -exec jupyter nbconvert --to script {} \;
    
    # Run security scan
    if find notebooks -name "*.py" -exec bandit -r {} \; 2>/dev/null; then
        echo "✅ Security scan completed"
    else
        echo "⚠️ Security scan found issues (review manually)"
    fi
    
    # Cleanup
    find notebooks -name "*.py" -delete
fi

echo "✅ Integration tests completed!"
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. Act Docker Permission Issues

```bash
# Fix Docker permissions on Linux
sudo usermod -aG docker $USER
newgrp docker

# Or run with sudo
sudo act pull_request
```

#### 2. Missing Dependencies

```bash
# Install missing Python packages
pip install jupyter nbval nbconvert bandit jupyter-book

# Or use uv for faster installation
pip install uv
uv pip install jupyter nbval nbconvert bandit jupyter-book
```

#### 3. Environment Variable Issues

```bash
# Debug environment variables
act --env-file .env --verbose

# Or set inline
act -e PYTHON_VERSION=3.11 -e CI=true pull_request
```

#### 4. Workflow Reference Errors

```bash
# Check workflow syntax
act --dryrun --workflow .github/workflows/your-workflow.yml

# Validate YAML
python -c "import yaml; print(yaml.safe_load(open('.github/workflows/your-workflow.yml')))"
```

### Debugging Tips

1. **Use verbose mode**: `act --verbose`
2. **Check logs**: `act --log-level debug`
3. **Dry run first**: `act --dryrun`
4. **Test individual jobs**: `act -j job-name`
5. **Use local artifacts**: `act --artifact-server-path /tmp/artifacts`

## 🏆 Best Practices

### 1. Local Testing Workflow

```bash
# Recommended testing sequence
act --dryrun                    # 1. Validate syntax
act --list                      # 2. List available workflows
act -j specific-job --dryrun    # 3. Test specific jobs
act pull_request               # 4. Run full workflow
```

### 2. Environment Management

- Use `.actrc` for consistent configuration
- Store secrets in `.env` file (add to `.gitignore`)
- Use specific Docker images for consistency
- Test with different Python versions

### 3. Security Considerations

- Never commit real secrets to version control
- Use dummy values for local testing
- Test security scanning with intentionally vulnerable code
- Validate that secrets are properly masked in logs

### 4. Performance Optimization

- Use Docker layer caching
- Cache dependencies between runs
- Use specific tags for Docker images
- Run only changed workflows during development

### 5. Continuous Integration

```bash
# Pre-commit hook
#!/bin/bash
# .git/hooks/pre-commit

# Validate workflows before commit
./scripts/pre-commit-workflow-check.sh

# Run quick local tests
act --dryrun || {
    echo "❌ Workflow validation failed"
    exit 1
}
```

## 🔗 Additional Resources

### Tools and Documentation

- **Act**: https://github.com/nektos/act
- **GitHub CLI**: https://cli.github.com/
- **GitHub Actions Documentation**: https://docs.github.com/en/actions
- **JupyterBook**: https://jupyterbook.org/

### Testing Strategies

- **Test-Driven Development**: Write tests before implementing workflows
- **Incremental Testing**: Test small changes frequently
- **Environment Parity**: Keep local and CI environments similar
- **Documentation Testing**: Ensure all examples work locally

### Community Examples

- **Act Examples**: https://github.com/nektos/act/tree/master/examples
- **GitHub Actions Toolkit**: https://github.com/actions/toolkit
- **Awesome Actions**: https://github.com/sdras/awesome-actions

---

## 📝 Quick Reference

### Essential Commands

```bash
# Install and setup
brew install act                 # Install act
act --version                   # Verify installation

# Basic usage
act --list                      # List workflows
act --dryrun                    # Validate syntax
act pull_request               # Run PR workflow
act -j job-name                # Run specific job

# Advanced usage
act -s GITHUB_TOKEN=token      # With secrets
act --platform ubuntu-latest=image  # Custom image
act --artifact-server-path /tmp     # Local artifacts
act --verbose                   # Debug mode
```

### Configuration Files

```bash
# .actrc - Global configuration
--container-architecture linux/amd64
--platform ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-latest

# .env - Environment variables
GITHUB_TOKEN=your_token
PYTHON_VERSION=3.11

# .github/events/pr.json - Custom event payload
{
  "pull_request": {"number": 1},
  "repository": {"name": "repo"}
}
```

This guide provides comprehensive coverage of local testing approaches for GitHub Actions workflows. Start with the basic Act setup and gradually incorporate more advanced testing strategies as needed.

# Local Testing Quick Reference

This guide provides a quick reference for testing GitHub Actions workflows locally using the new testing scripts.

## 🚀 Quick Start

### Prerequisites

1. **Basic Requirements**:
   ```bash
   # Python 3.9+ with pip
   python3 --version
   
   # Git repository
   git status
   ```

2. **Optional (for enhanced testing)**:
   ```bash
   # Docker (for Act-based testing)
   docker --version
   
   # Act (GitHub Actions local runner)
   act --version
   
   # Install Act if not available:
   # macOS: brew install act
   # Linux: curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
   # Windows: choco install act-cli
   ```

## 📋 Testing Workflow

### 1. Validate Workflows

```bash
# Validate all workflow files
./scripts/validate-workflows.sh

# Verbose output for debugging
VERBOSE=true ./scripts/validate-workflows.sh

# Skip Act validation if not available
VALIDATE_ACT=false ./scripts/validate-workflows.sh
```

### 2. Test CI Pipeline Locally

```bash
# Quick validation (recommended for development)
EXECUTION_MODE=validation-only ./scripts/test-local-ci.sh

# Full execution test
EXECUTION_MODE=full ./scripts/test-local-ci.sh

# Test single notebook
SINGLE_NOTEBOOK=notebooks/example.ipynb ./scripts/test-local-ci.sh

# Skip time-consuming steps
RUN_SECURITY_SCAN=false BUILD_DOCUMENTATION=false ./scripts/test-local-ci.sh
```

### 3. Test with Act (Docker-based)

```bash
# Test pull request workflow
./scripts/test-with-act.sh pull_request

# Test specific workflow
./scripts/test-with-act.sh push .github/workflows/notebook-ci-main.yml

# Dry run (validate without execution)
DRY_RUN=true ./scripts/test-with-act.sh workflow_dispatch
```

## 🎯 Repository-Specific Testing

### JDAT Notebooks
```bash
# Set CRDS environment
export CRDS_SERVER_URL="https://jwst-crds.stsci.edu"
export CRDS_PATH="/tmp/crds_cache"

# Test with full execution
EXECUTION_MODE=full ./scripts/test-local-ci.sh
```

### HST Notebooks
```bash
# Note: hstcal may not be available locally
# Use validation-only mode
EXECUTION_MODE=validation-only ./scripts/test-local-ci.sh
```

### Hello Universe
```bash
# Educational repository - skip security scan
RUN_SECURITY_SCAN=false ./scripts/test-local-ci.sh
```

### MAST Notebooks
```bash
# Standard testing - may show MAST API warnings
./scripts/test-local-ci.sh
```

### JWST Pipeline Notebooks
```bash
# jdaviz may not be available locally
# Focus on notebook validation
EXECUTION_MODE=validation-only ./scripts/test-local-ci.sh
```

## 🔧 Common Use Cases

### Development Workflow
```bash
#!/bin/bash
# Save as: test-dev.sh

echo "🚀 Development Testing Workflow"

# 1. Quick validation
echo "📋 Step 1: Workflow validation"
./scripts/validate-workflows.sh || exit 1

# 2. Fast CI test
echo "🔬 Step 2: Quick CI test"
EXECUTION_MODE=validation-only \
BUILD_DOCUMENTATION=false \
./scripts/test-local-ci.sh || exit 1

# 3. Test specific changes
if [ "$1" != "" ]; then
    echo "📓 Step 3: Testing specific notebook: $1"
    SINGLE_NOTEBOOK="$1" ./scripts/test-local-ci.sh
fi

echo "✅ Development testing completed!"
```

### Pre-Commit Hook
```bash
#!/bin/bash
# Save as: .git/hooks/pre-commit

echo "🔍 Pre-commit validation..."

# Validate workflows if changed
if git diff --cached --name-only | grep -q "\.github/workflows/"; then
    ./scripts/validate-workflows.sh || exit 1
fi

# Quick notebook test if notebooks changed
if git diff --cached --name-only | grep -q "\.ipynb$"; then
    EXECUTION_MODE=validation-only \
    BUILD_DOCUMENTATION=false \
    RUN_SECURITY_SCAN=false \
    ./scripts/test-local-ci.sh || exit 1
fi

echo "✅ Pre-commit validation passed"
```

### CI/CD Pipeline Simulation
```bash
#!/bin/bash
# Save as: test-full-pipeline.sh

echo "🔄 Full CI/CD Pipeline Simulation"

# 1. Workflow validation
./scripts/validate-workflows.sh

# 2. Full CI test
EXECUTION_MODE=full ./scripts/test-local-ci.sh

# 3. Act-based testing (if available)
if command -v act &> /dev/null; then
    ./scripts/test-with-act.sh pull_request
fi

echo "✅ Full pipeline simulation completed!"
```

## 🐛 Troubleshooting

### Common Issues

1. **Python Environment Issues**:
   ```bash
   # Clear virtual environment
   rm -rf venv
   ./scripts/test-local-ci.sh
   ```

2. **Permission Errors**:
   ```bash
   # Make scripts executable
   chmod +x scripts/*.sh
   ```

3. **Docker Issues (Act)**:
   ```bash
   # Verify Docker is running
   docker ps
   
   # Pull required images
   docker pull ghcr.io/catthehacker/ubuntu:act-latest
   ```

4. **Git Issues**:
   ```bash
   # Ensure clean working directory
   git status
   git add .
   git commit -m "Clean up before testing"
   ```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PYTHON_VERSION` | `3.11` | Python version to use |
| `EXECUTION_MODE` | `validation-only` | `validation-only`, `quick`, `full` |
| `SINGLE_NOTEBOOK` | - | Path to single notebook to test |
| `RUN_SECURITY_SCAN` | `true` | Enable/disable security scanning |
| `BUILD_DOCUMENTATION` | `true` | Enable/disable documentation build |
| `VALIDATE_ACT` | `true` | Use Act for workflow validation |
| `VERBOSE` | `false` | Enable verbose output |
| `DRY_RUN` | `false` | Validate without execution (Act only) |

## 📊 Performance Tips

### Speed Up Testing

1. **Use validation-only mode** for quick feedback:
   ```bash
   EXECUTION_MODE=validation-only ./scripts/test-local-ci.sh
   ```

2. **Skip time-consuming steps** during development:
   ```bash
   RUN_SECURITY_SCAN=false BUILD_DOCUMENTATION=false ./scripts/test-local-ci.sh
   ```

3. **Test single notebooks** for focused debugging:
   ```bash
   SINGLE_NOTEBOOK=notebooks/problematic.ipynb ./scripts/test-local-ci.sh
   ```

4. **Use dry runs** for workflow validation:
   ```bash
   DRY_RUN=true ./scripts/test-with-act.sh pull_request
   ```

### Optimize Act Performance

1. **Reuse containers**:
   ```bash
   # Add to .actrc
   --reuse
   ```

2. **Use faster images**:
   ```bash
   # Add to .actrc
   --platform ubuntu-latest=ubuntu:22.04
   ```

3. **Cache dependencies**:
   ```bash
   # Add to .actrc
   --artifact-server-path /tmp/act-artifacts
   ```

## 📚 Additional Resources

- **[Complete Local Testing Guide](docs/local-testing-guide.md)** - Detailed testing methods
- **[Scripts Documentation](scripts/README.md)** - Script usage and examples
- **[Act Documentation](https://github.com/nektos/act)** - GitHub Actions local runner
- **[Migration Guide](docs/migration-guide.md)** - Repository migration process

## 💡 Tips and Best Practices

1. **Start with workflow validation** before testing execution
2. **Use validation-only mode** for fast feedback during development  
3. **Test single notebooks** when debugging specific issues
4. **Run full tests** before creating pull requests
5. **Use Act** for comprehensive workflow testing with Docker
6. **Set up pre-commit hooks** for automatic validation
7. **Test repository-specific configurations** with appropriate environment variables

---

**Quick Commands Summary**:
```bash
# Essential testing commands
./scripts/validate-workflows.sh                    # Validate workflow syntax
./scripts/test-local-ci.sh                        # Quick CI simulation  
./scripts/test-with-act.sh pull_request           # Full workflow test

# Development shortcuts
EXECUTION_MODE=validation-only ./scripts/test-local-ci.sh    # Fast validation
DRY_RUN=true ./scripts/test-with-act.sh pull_request        # Dry run test
```

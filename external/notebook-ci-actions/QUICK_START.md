# 🚀 Quick Start: Local Testing

Get up and running with local GitHub Actions testing in under 5 minutes!

## ⚡ TL;DR - Essential Commands

```bash
# 1. Validate workflows (30 seconds)
./scripts/validate-workflows.sh

# 2. Test notebooks locally (2-5 minutes) 
./scripts/test-local-ci.sh

# 3. Full workflow test with Docker (optional - 5-10 minutes)
./scripts/test-with-act.sh pull_request
```

## 📋 Prerequisites Check

Quick verification that you have what you need:

```bash
# Required (minimum setup)
python3 --version    # Should be 3.9+
git status           # Should show a git repository

# Optional (enhanced testing)
docker --version     # For Act-based testing
act --version        # GitHub Actions local runner
```

**Missing Act?** Install it quickly:
```bash
# macOS
brew install act

# Linux  
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Windows (WSL/PowerShell)
choco install act-cli
```

## 🎯 Three Testing Approaches

### 1. 🔍 Workflow Validation (Fastest - ~30 seconds)

**What it does**: Checks YAML syntax, structure, and common issues
**When to use**: Before every commit, quick sanity check

```bash
./scripts/validate-workflows.sh
```

**Expected output**:
```
🔍 GitHub Actions Workflow Validation
=====================================
✅ notebook-ci-pr.yml: PASSED
✅ notebook-ci-main.yml: PASSED  
✅ All workflows validated successfully!
```

### 2. 🧪 Local CI Simulation (Fast - 2-5 minutes)

**What it does**: Simulates the complete CI pipeline locally
**When to use**: Testing notebook changes, development workflow

```bash
# Quick validation (recommended for development)
./scripts/test-local-ci.sh

# OR specify execution mode
EXECUTION_MODE=validation-only ./scripts/test-local-ci.sh
```

**Expected output**:
```
🚀 Starting Local CI Simulation
================================
✅ Environment validation: PASSED
✅ Dependencies installation: COMPLETED
✅ Notebook validation: COMPLETED
✅ Local CI simulation completed successfully!
```

### 3. 🎭 Full Workflow Testing (Complete - 5-10 minutes)

**What it does**: Runs actual GitHub Actions workflows using Docker
**When to use**: Final testing before push, comprehensive validation

```bash
./scripts/test-with-act.sh pull_request
```

**Expected output**:
```
🎭 Act-based Local Testing
==========================
✅ Act execution completed successfully!
```

## 🔧 Common Usage Patterns

### Development Workflow
```bash
# Make changes to notebooks or workflows
# Then run quick validation
./scripts/validate-workflows.sh && ./scripts/test-local-ci.sh
```

### Pre-Commit Testing
```bash
# Test only what changed
EXECUTION_MODE=validation-only ./scripts/test-local-ci.sh
```

### Full Pre-Push Testing
```bash
# Complete validation before pushing
./scripts/validate-workflows.sh
./scripts/test-local-ci.sh  
./scripts/test-with-act.sh pull_request
```

## ⚙️ Quick Configuration

### Speed Up Testing

Skip time-consuming steps during development:

```bash
# Skip security scan and docs for faster testing
RUN_SECURITY_SCAN=false BUILD_DOCUMENTATION=false ./scripts/test-local-ci.sh
```

### Test Single Notebook

Focus on a specific notebook:

```bash
SINGLE_NOTEBOOK=notebooks/example.ipynb ./scripts/test-local-ci.sh
```

### Repository-Specific Quick Setup

```bash
# JDAT Notebooks (JWST/CRDS)
export CRDS_SERVER_URL="https://jwst-crds.stsci.edu"
export CRDS_PATH="/tmp/crds_cache"
./scripts/test-local-ci.sh

# Educational repositories (skip security scan)
RUN_SECURITY_SCAN=false ./scripts/test-local-ci.sh

# HST Notebooks (validation only - conda packages may not be available)
EXECUTION_MODE=validation-only ./scripts/test-local-ci.sh
```

## 🐛 Quick Troubleshooting

### Script Hanging During Package Installation

**Problem**: `test-local-ci.sh` hangs on "Installing dependencies..."

**Quick Solutions**:

```bash
# 1. Skip dependency installation (fastest fix)
SKIP_DEPS=true ./scripts/test-local-ci.sh

# 2. Use validation-only mode (no package execution needed)
EXECUTION_MODE=validation-only ./scripts/test-local-ci.sh

# 3. Kill hanging processes
pkill -f "test-local-ci"

# 4. Run diagnostic tool
./scripts/diagnose-local-ci.sh
```

**Root Causes**:
- Large scientific packages (astropy, numpy, scipy) taking 10-30 minutes
- Network issues downloading packages
- Virtual environment conflicts
- Package compilation on ARM/M1 Macs

### Script Permission Issues
```bash
chmod +x scripts/*.sh
```

### Python Environment Issues
```bash
# Clear and restart
rm -rf venv
./scripts/test-local-ci.sh
```

### Docker/Act Issues
```bash
# Verify Docker is running
docker ps

# Test Act with dry run
DRY_RUN=true ./scripts/test-with-act.sh pull_request
```

## 📊 Execution Modes Quick Reference

| Mode | Duration | Use Case | Command |
|------|----------|----------|---------|
| **validation-only** | ~1-2 min | Development, quick check | `EXECUTION_MODE=validation-only ./scripts/test-local-ci.sh` |
| **quick** | ~2-5 min | Sample testing (first 3 notebooks) | `EXECUTION_MODE=quick ./scripts/test-local-ci.sh` |
| **full** | ~5-30 min | Complete testing (all notebooks) | `EXECUTION_MODE=full ./scripts/test-local-ci.sh` |

## 🎯 Recommended Workflows

### 🏃‍♂️ Quick Development Loop
```bash
# 1. Make changes
# 2. Quick validation (30 seconds)
./scripts/validate-workflows.sh

# 3. Fast notebook check (1-2 minutes)  
EXECUTION_MODE=validation-only ./scripts/test-local-ci.sh

# 4. Commit if passed
git add . && git commit -m "Update notebooks"
```

### 🔬 Thorough Pre-Push Testing
```bash
# 1. Validate workflows
./scripts/validate-workflows.sh

# 2. Full local CI test
./scripts/test-local-ci.sh

# 3. Simulate GitHub Actions (if Act available)
if command -v act &> /dev/null; then
    ./scripts/test-with-act.sh pull_request
fi

# 4. Push with confidence
git push origin feature-branch
```

### 🎯 Single Notebook Focus
```bash
# Test only the notebook you're working on
SINGLE_NOTEBOOK=notebooks/my-analysis.ipynb \
EXECUTION_MODE=full \
./scripts/test-local-ci.sh
```

## 💡 Pro Tips

1. **Start with workflow validation** - it's fast and catches syntax errors
2. **Use validation-only mode** during active development for quick feedback
3. **Test single notebooks** when debugging specific issues
4. **Run full tests before creating PRs** to ensure everything works
5. **Set up aliases** for common commands:

```bash
# Add to your .bashrc or .zshrc
alias validate-wf='./scripts/validate-workflows.sh'
alias test-ci='./scripts/test-local-ci.sh'
alias test-act='./scripts/test-with-act.sh pull_request'
alias quick-test='EXECUTION_MODE=validation-only ./scripts/test-local-ci.sh'
```

## 🎉 Success Indicators

**Workflow Validation Success**:
```
✅ All workflows validated successfully!
```

**Local CI Success**:
```
✅ Local CI simulation completed successfully!
```

**Act Testing Success**:
```
✅ Act execution completed successfully!
```

## 📚 Next Steps

Once you're comfortable with basic testing:

- **Read the complete guide**: [`docs/local-testing-guide.md`](docs/local-testing-guide.md)
- **Explore advanced features**: [`docs/local-testing-quick-reference.md`](docs/local-testing-quick-reference.md)
- **Set up automation**: Create pre-commit hooks and development scripts
- **Repository migration**: Use [`scripts/migrate-repository.sh`](scripts/README.md) for full workflow setup

---

**⏱️ Time Investment vs. Benefits**:
- **5 minutes setup** → **Hours saved** in GitHub Actions minutes
- **30 second validation** → **Catch issues before CI**
- **2 minute local testing** → **Immediate feedback vs. 5-10 minute CI wait**

Start with the basic workflow validation and work your way up to full testing as needed! 🚀

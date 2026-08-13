# Semantic Versioning for GitHub Actions Workflows

!!! info "For maintainers"
    This page is reference material for repository maintainers and infrastructure owners. If you just write notebooks, start with the [Quick Reference](authors/quick-reference.md).


This document explains how to implement semantic versioning for reusable GitHub Actions workflows and how to automate the versioning process using GitHub Actions.

## :material-clipboard-text: Table of Contents

- [Overview](#overview)
- [Semantic Versioning Basics](#semantic-versioning-basics)
- [Versioning Strategy for Actions](#versioning-strategy-for-actions)
- [Automated Versioning Workflow](#automated-versioning-workflow)
- [Using Versioned Workflows](#using-versioned-workflows)
- [Upgrading between versions](#upgrading-between-versions)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## :material-target: Overview

Semantic versioning (SemVer) provides a systematic way to version your reusable GitHub Actions workflows, ensuring:

- **Backwards compatibility** for existing consumers
- **Clear communication** about changes and their impact
- **Safe upgrades** with confidence in stability
- **Automated release management** through GitHub Actions

## :material-ruler: Semantic Versioning Basics

### Version Format: `MAJOR.MINOR.PATCH`

- **MAJOR** (`1.0.0` → `2.0.0`): Breaking changes that require caller updates
- **MINOR** (`1.0.0` → `1.1.0`): New features that are backwards compatible
- **PATCH** (`1.0.0` → `1.0.1`): Bug fixes that are backwards compatible

### Pre-release Versions
- **Alpha**: `1.0.0-alpha.1` - Early development, unstable
- **Beta**: `1.0.0-beta.1` - Feature complete, testing phase
- **Release Candidate**: `1.0.0-rc.1` - Production ready candidate

## :material-tag: Versioning Strategy for Actions

### When to Bump Each Version Component

#### MAJOR Version (Breaking Changes)
- Removing or renaming workflow inputs
- Changing input types (string → boolean)
- Removing workflow outputs
- Changing default behavior significantly
- Requiring new secrets or permissions

**Example Breaking Changes:**
```yaml
# v1.x.x
inputs:
  python-version:
    required: true
    type: string

# v2.0.0 - BREAKING: changed required to optional
inputs:
  python-version:
    required: false  # ← Breaking change
    type: string
    default: "3.11"
```

#### MINOR Version (New Features)
- Adding new optional inputs
- Adding new workflow outputs
- Adding new optional features
- Improving performance without changing interface

**Example New Features:**
```yaml
# v1.2.0 - NEW: Added post-processing-script input
inputs:
  python-version:
    required: false
    type: string
    default: "3.11"
  post-processing-script:  # ← New optional input
    required: false
    type: string
```

#### PATCH Version (Bug Fixes)
- Fixing bugs without changing interface
- Security updates
- Documentation improvements
- Internal refactoring

### Git Tag Strategy

```bash
# Create semantic version tags
git tag v1.0.0
git tag v1.1.0
git tag v1.1.1
git tag v2.0.0

# Create major version tags (auto-updated)
git tag v1      # Points to latest v1.x.x
git tag v2      # Points to latest v2.x.x
```

## :material-robot: Automated Versioning Workflow

### 1. Release Workflow with Semantic Versioning

Create `.github/workflows/release.yml`:

```yaml
name: Release and Version Management

on:
  pull_request:
    types: [closed]
    branches: [main]

jobs:
  release:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: write
      pull-requests: write
    
    steps:
    - name: Checkout
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
        token: ${{ secrets.GITHUB_TOKEN }}

    - name: Determine Version Bump
      id: version
      uses: mathieudutour/github-tag-action@v6.1
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        default_bump: patch

    - name: Create Release
      uses: softprops/action-gh-release@v2
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ steps.version.outputs.new_tag }}
        name: Release ${{ steps.version.outputs.new_tag }}
        body: |
          ## Changes in ${{ steps.version.outputs.new_tag }}
          
          ${{ github.event.pull_request.body }}
          
          **Full Changelog**: ${{ steps.version.outputs.changelog }}
        draft: false
        prerelease: false

    - name: Update Major Version Tag
      run: |
        MAJOR_VERSION=$(echo ${{ steps.version.outputs.new_tag }} | cut -d. -f1)
        git tag -fa ${MAJOR_VERSION} -m "Update ${MAJOR_VERSION} to ${{ steps.version.outputs.new_tag }}"
        git push origin ${MAJOR_VERSION} --force
```

### 2. PR-based Version Bump Detection

Add this workflow to automatically determine version bumps based on PR labels:

Create `.github/workflows/version-check.yml`:

```yaml
name: Version Bump Check

on:
  pull_request:
    types: [opened, synchronize, labeled, unlabeled]

jobs:
  version-check:
    runs-on: ubuntu-latest
    steps:
    - name: Check Version Bump Label
      uses: actions/github-script@v7
      with:
        script: |
          const labels = context.payload.pull_request.labels.map(l => l.name);
          
          const versionLabels = labels.filter(l => 
            l.startsWith('version:') || 
            ['breaking-change', 'feature', 'bugfix'].includes(l)
          );
          
          if (versionLabels.length === 0) {
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `⚠️ **Version Label Missing**
              
              Please add one of these labels to indicate the type of change:
              - \`version:major\` or \`breaking-change\` - Breaking changes
              - \`version:minor\` or \`feature\` - New features  
              - \`version:patch\` or \`bugfix\` - Bug fixes
              `
            });
            
            core.setFailed('PR must have a version bump label');
          }
          
          core.info(`Version labels found: ${versionLabels.join(', ')}`);
```

### 3. Conventional Commits Integration

For automatic version detection based on commit messages:

```yaml
name: Semantic Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Semantic Release
      uses: cycjimmy/semantic-release-action@v4
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        semantic_version: 19
        extra_plugins: |
          @semantic-release/changelog@6.0.0
          @semantic-release/git@10.0.0
```

## :material-sync: Using Versioned Workflows

### Pinning to Specific Versions

#### Recommended: Pin to Major Version
```yaml
# Automatically gets latest v1.x.x (safe, gets bug fixes)
uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@v1
```

#### Conservative: Pin to Exact Version
```yaml
# Pinned to exact version (most stable, but misses bug fixes)
uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@v1.2.3
```

#### Development: Use Branch
```yaml
# Use for testing only, not production
uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@main
```

### Version Range Examples

```yaml
# Good practices for different scenarios:

# Production environments - pin to major version
uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@v1

# Critical systems - pin to exact version
uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@v1.2.3

# Testing environments - use latest
uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@main

# Feature branches - use pre-release
uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@v2.0.0-beta.1
```

## :material-rocket-launch: Upgrading between versions

### Upgrading from v1 to v2 (Breaking Changes)

#### Step 1: Review Breaking Changes
Check the release notes for breaking changes:

```yaml
# v1.x.x (old)
jobs:
  ci:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@v1
    with:
      python-version: "3.11"
      execution-mode: "merge"
      enable-html-build: true

# v2.0.0 (new) - Example breaking changes
jobs:
  ci:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@v2
    with:
      python-version: "3.11"
      execution-mode: "merge"
      # BREAKING: example breaking change
      enable-security: true  # NEW: required parameter
```

#### Step 2: Test in Feature Branch
```bash
# Create feature branch for upgrade
git checkout -b upgrade-to-v2

# Update workflow files
# Test thoroughly
# Create PR with version upgrade
```

#### Step 3: Gradual Migration Strategy
```yaml
# Option 1: Parallel workflows during transition
jobs:
  # Keep v1 for critical paths
  ci-v1:
    if: github.ref != 'refs/heads/main'
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@v1
    
  # Test v2 on main branch
  ci-v2:
    if: github.ref == 'refs/heads/main'
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@v2

# Option 2: Feature flag approach
jobs:
  ci:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@${{ github.event.inputs.workflow_version || 'v1' }}
```

### Minor Version Updates (v1.0.0 → v1.1.0)

Minor updates are backwards compatible, so you can update safely:

```yaml
# Before: Pinned to exact version
uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@v1.0.0

# After: Pin to major version to get updates automatically
uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@v1
```

## :material-check-circle: Best Practices

### For Workflow Maintainers

1. **Always use semantic versioning**
   ```bash
   # Good
   git tag v1.2.3
   
   # Bad
   git tag release-2023-06-11
   ```

2. **Maintain backwards compatibility within major versions**
3. **Document breaking changes clearly**
4. **Use pre-release versions for testing**
5. **Keep major version tags updated**

### For Workflow Consumers

1. **Pin to major versions in production**
   ```yaml
   # Recommended
   uses: org/repo/.github/workflows/workflow.yml@v1
   ```

2. **Test upgrades in feature branches**
3. **Monitor release notes and changelogs**
4. **Use exact versions for critical systems**
5. **Update dependencies regularly**

### Release Communication

#### PR Title Conventions
```
feat: add post-processing script support (#123)      # Minor version
fix: resolve timeout issues in notebook execution   # Patch version  
feat!: remove deprecated python-version input       # Major version
```

#### PR Body Template
```markdown
## Type of Change
- [ ] 🐛 Bug fix (patch version)
- [ ] ✨ New feature (minor version) 
- [ ] 💥 Breaking change (major version)

## Description
Brief description of changes...

## Breaking Changes (if any)
- List any breaking changes
- Include migration steps

## Testing
- [ ] Tested in development environment
- [ ] Backwards compatibility verified
```

## :material-wrench: Troubleshooting

### Common Issues

#### 1. Version Tag Not Found
```yaml
# Error: Reference does not exist
uses: org/repo/.github/workflows/workflow.yml@v1.2.3

# Solution: Check if tag exists
git ls-remote --tags origin
```

#### 2. Major Version Tag Out of Date
```bash
# Update major version tag to point to latest
git tag -fa v1 -m "Update v1 to v1.2.3"
git push origin v1 --force
```

#### 3. Breaking Changes Not Detected
```yaml
# Add this to your PR template
## Breaking Changes Checklist
- [ ] Input parameters changed
- [ ] Output format changed  
- [ ] New required secrets
- [ ] Behavior significantly altered
```

### Debugging Version Issues

```yaml
# Add version info to workflow outputs
jobs:
  debug-version:
    runs-on: ubuntu-latest
    steps:
    - name: Show Version Info
      run: |
        echo "Workflow version: ${GITHUB_REF#refs/tags/}"
        echo "Called from: ${{ github.repository }}"
        echo "Caller ref: ${{ github.ref }}"
```

## :material-bookshelf: Additional Resources

- [Semantic Versioning Specification](https://semver.org/)
- [GitHub Actions Versioning Guide](https://docs.github.com/en/actions/creating-actions/about-custom-actions#using-release-management-for-actions)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Release Automation](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes)

---


For the latest version information, see the [Releases page](https://github.com/spacetelescope/notebook-ci-actions/releases).

## Pinning and rollback

Callers reference the unified workflow by tag:

- **`@v1`** (recommended): a moving major tag that always points at the latest `v1.x.x`. You get bug fixes automatically and only opt into breaking changes by moving to `@v2`.
- **`@v1.2.3`**: an exact release. Most stable, but you miss fixes until you bump.
- **`@<commit-sha>`**: immutable and maximally certain about exactly what runs. Use for repositories with stricter supply-chain requirements; update deliberately.

**Rolling back a bad release.** If a new `v1.x.x` breaks callers, either pin the affected caller to the last known-good exact tag (e.g. `@v1.2.2`) or commit SHA until the issue is fixed, or, as a maintainer of `notebook-ci-actions`, repoint the moving `@v1` tag to the previous release commit so every caller recovers at once.

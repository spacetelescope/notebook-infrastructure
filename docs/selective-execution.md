# Selective Execution & Smart Workflows

Two complementary ways the CI does less work when less has changed: **smart routing** (skip notebook execution for docs/config-only changes) and **selective execution** (run only the notebook subdirectory that changed).

!!! note "Source of truth"
    The canonical implementation is the unified workflow in
    [`spacetelescope/notebook-ci-actions`](https://github.com/spacetelescope/notebook-ci-actions)
    (`notebook-ci-unified.yml`). The patterns below show how a repository's caller
    workflows drive it; see the [Configuration Reference](configuration-reference.md)
    for every input.

## Overview

| Mechanism | Decides based on | Effect |
| --- | --- | --- |
| **Smart routing** | The *type* of file changed | Docs/config-only changes do a docs rebuild and skip notebook execution; notebook/requirements changes run full CI |
| **Selective execution** | *Which* notebook subdirectory changed | Only notebooks in the affected directory run; other directories are skipped |

Both cut GitHub Actions minutes substantially (commonly 60-85% on docs-only or single-directory changes) while keeping full validation for anything that affects notebooks.

## Smart routing: docs-only vs full CI

The workflow categorizes the changed files and picks a path:

| File category | Examples | Path |
| --- | --- | --- |
| Notebooks | `notebooks/**/*.ipynb`, `*.py`, `*.R` | Full CI |
| Requirements | `requirements.txt`, `pyproject.toml`, `setup.py` | Full CI |
| Documentation / config | `*.md`, `_config.yml`, `_toc.yml`, `*.css`, `*.js` | Docs-only rebuild |
| Workflow files | `.github/workflows/*` | Minimal / skip |

### Decision matrix

| Files changed | PR | Main branch | Reason |
| --- | --- | --- | --- |
| Only `.ipynb` | Full CI (validation) | Full CI + execution | Notebooks need validation/execution |
| Only requirements | Full CI (validation) | Full CI + execution | Dependencies affect execution |
| Only `_config.yml` / `.md` | Docs rebuild | Docs rebuild + deploy | Documentation only |
| Mixed changes | Full CI | Full CI + execution | Safety: validate everything |
| Workflow files only | Minimal / skip | Skip | No content change |

## Selective execution: per-directory

When a repository organizes notebooks into subdirectories with their own `requirements.txt`, a change inside one directory only runs that directory.

```
your-repo/
├── notebooks/
│   ├── data_analysis/
│   │   ├── requirements.txt      # directory-specific dependencies
│   │   ├── analysis1.ipynb
│   │   └── data_prep.py
│   ├── visualization/
│   │   ├── requirements.txt
│   │   └── dashboard.ipynb
│   └── shared_utils/
│       └── utils.py
├── requirements.txt              # root-level deps (affects all notebooks)
├── _config.yml
└── _toc.yml
```

### How detection works

| Change | Strategy | Scope | Typical time |
| --- | --- | --- | --- |
| `notebooks/data_analysis/requirements.txt` | selective-directories | only `data_analysis/` | 5-10 min |
| `notebooks/viz/plot1.ipynb` | selective-directories | only `viz/` | 3-8 min |
| `requirements.txt` (root) | full-repository | all notebooks | 15-25 min |
| `_config.yml` | docs-only | documentation | 2-5 min |

A change to the **root** `requirements.txt` deliberately runs everything (safety first). Multiple affected directories run in parallel.

## Implementation

1. **Use the smart/selective caller workflows.** Point your `.github/workflows/` callers at `notebook-ci-unified.yml` (see the [examples in notebook-ci-actions](https://github.com/spacetelescope/notebook-ci-actions/tree/main/examples)).
2. **Organize directory dependencies.** Give each notebook subdirectory a self-contained `requirements.txt`, optionally inheriting from the root with `-r ../../requirements.txt`.
3. **Repository-specific customization:**
   - `jwst-pipeline-notebooks`: set a `post-processing-script` (e.g. `scripts/jdaviz_image_replacement.sh`).
   - `hst_notebooks`: micromamba is auto-detected; no extra config.
   - `hellouniverse`: consider `enable-security: false` for the educational repo.
4. **Test both paths:** open a docs-only PR (expect a docs rebuild) and a notebook PR (expect full CI), and a single-directory change (expect only that directory).

### Limiting parallelism

```yaml
strategy:
  matrix:
    directory: ${{ fromJson(needs.detect-changes.outputs.affected-directories) }}
  max-parallel: 3
  fail-fast: false
```

## Performance and cost

| Repository size | Full every time | Selective / smart | Savings |
| --- | --- | --- | --- |
| Small (5 dirs, 20 notebooks) | 15 min | 3-5 min | 67-80% |
| Medium (10 dirs, 50 notebooks) | 25 min | 5-8 min | 68-80% |
| Large (20 dirs, 100 notebooks) | 45 min | 8-12 min | 73-82% |

At roughly $0.008/Actions-minute, a repo seeing mostly docs-only and single-directory changes typically saves on the order of $50/month versus running full CI on every change. Changes to the root requirements still cost the same as a full run, by design.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| A subdirectory change doesn't trigger selective run | Path doesn't match `notebooks/*/` | Move the notebook under a `notebooks/<dir>/` directory |
| All notebooks run when you expected one directory | Root `requirements.txt` changed | Expected: root changes run everything |
| Directory notebooks fail on missing packages | Incomplete directory `requirements.txt` | Complete it, or inherit from root with `-r` |
| Empty-matrix / matrix strategy error | `affected-directories` output empty | Confirm changed files resolve to valid directories |
| Docs change triggers full CI (false positive) | File not in the docs category | Add the extension to the docs file patterns |
| Docs-only build fails | Build needs notebooks present | Ensure the docs build doesn't depend on executed notebooks |

Enable debug output in the `detect-changes` job to see the categorized files and the chosen strategy.

## Best practices

- **Logical grouping:** organize directories by function, not arbitrary splits.
- **Dependency isolation:** each directory's `requirements.txt` is self-contained (or inherits from root).
- **Test both paths:** always exercise selective *and* full execution before relying on it.
- **Roll out gradually:** validate on one repo, monitor accuracy and savings, then expand.
- **Communicate:** document the behavior for contributors so a skipped path isn't mistaken for a missing check.

## Related documentation

- [notebook-ci-actions](https://github.com/spacetelescope/notebook-ci-actions) - the unified workflow (source of truth)
- [Configuration Reference](configuration-reference.md) - every workflow input
- [Example workflows](https://github.com/spacetelescope/notebook-ci-actions/tree/main/examples) - caller templates

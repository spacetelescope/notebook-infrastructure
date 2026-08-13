# Reviewing Notebooks

All notebooks supported by STScI are expected to undergo some level of review to ensure they follow sustainable software practices and meet learning goals for users. In practice, most notebooks need both a **science review** (focused on content and correctness) and a **technical review** (focused on code, style, and reproducibility). These may be combined into a single review; exactly how is up to each repository and team. This page describes a baseline process flexible enough to apply across repositories.

## The two reviews

- **Science review** confirms the notebook is scientifically correct and useful: the analysis is sound, the explanation is clear, and it meets the intended learning goals for its audience.
- **Technical review** confirms the notebook is sustainable software: it runs top to bottom in a clean environment, declares its dependencies, follows the [notebook style guide](https://github.com/spacetelescope/style-guides/blob/master/guides/jupyter-notebooks.md), and passes CI.

A single reviewer may cover both, or two reviewers may split them, depending on the repository.

## How a review works

1. The author opens a pull request (see [Contributing Notebooks](contributing_notebooks.md)).
2. CI runs automatically: validation, execution, and a security scan. A reviewer should not start until CI is green, since many issues are caught there.
3. Reviewers leave comments on the PR. The author responds and pushes updates, which re-trigger CI.
4. When both the science and technical concerns are satisfied and CI passes, a maintainer merges to `main`, which publishes the notebook.

## What reviewers look for

- **Runs clean:** Restart and Run All completes in order with no errors (CI enforces this).
- **Dependencies declared:** everything imported is in `requirements.txt` or the repo's environment.
- **No secrets or unsafe calls:** the `bandit` scan is clean.
- **Clear narrative:** markdown cells explain the what and why, not just the code.
- **Style:** consistent with the [notebook](https://github.com/spacetelescope/style-guides/blob/master/guides/jupyter-notebooks.md) and [Python](https://github.com/spacetelescope/style-guides/blob/master/guides/python.md) style guides.

## Related

- [Contributing Notebooks](contributing_notebooks.md)
- [Notebook Style](style.md)
- [Full Guide for notebook authors](authors/guide.md)

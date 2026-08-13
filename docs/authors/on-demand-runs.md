# On-Demand Runs

*For scientists who want to trigger the CI manually, without opening a pull
request or merging.*

An on-demand run lets you push a button in the GitHub **Actions** tab and run
the same checks the CI normally runs. It is the fastest way to re-run a single
notebook, validate your work before opening a pull request, or rebuild the
published site, all without committing anything new.

## Start a run

1. Go to your repository on GitHub and open the **Actions** tab.
2. In the left sidebar, click **Notebook CI - On-Demand Actions**.
3. Click the **Run workflow** button on the right.
4. Choose the **branch** to run from, fill in the options below, and click
   **Run workflow**.

The run appears in the list within a few seconds. Click it to watch progress and
read logs, exactly like a PR run.

## Options

| Option | What it is | When you set it |
| --- | --- | --- |
| **Action** (`action_type`) | What to run (see table below) | Always |
| **Single notebook path** (`single_notebook`) | Path like `notebooks/my-analysis/my-analysis.ipynb` | Only for the `*-single` actions |
| **Python version** (`python_version`) | Defaults to `3.11` | Only to override the default |
| **Custom conda environment** (`conda_environment`) | Conda env name, if your repo uses one | Only if your science needs it |
| **Days until deprecation** (`deprecation_days`) | Defaults to `60` | Only for `deprecate-notebook` |
| **Enable debug logging** (`enable_debug`) | Verbose logs for troubleshooting | When a run fails and you want detail |

## What each action does

| Action | Runs | Touches one or all? |
| --- | --- | --- |
| `validate-all` | Structure/validation checks only (no execution) | All notebooks |
| `validate-single` | Validation on one notebook | One (set the path) |
| `execute-all` | Runs notebooks top to bottom in a clean env | All notebooks |
| `execute-single` | Runs one notebook | One (set the path) |
| `security-scan-all` | `bandit` security scan | All notebooks |
| `full-pipeline-all` | Validation + security + execution + storage + HTML build | All notebooks |
| `full-pipeline-single` | The full pipeline on one notebook | One (set the path) |
| `build-html-only` | Rebuilds the docs site without re-executing notebooks | Site |
| `deprecate-notebook` | Starts the deprecation flow for a notebook | One (set the path) |

!!! tip "Single-notebook actions need a path"
    The `validate-single`, `execute-single`, and `full-pipeline-single` actions
    do nothing useful unless you also fill in **Single notebook path**. Copy the
    path from the repo, for example `notebooks/cos_analysis/cos_analysis.ipynb`.

## Common scenarios

| You want to | Action | Also set |
| --- | --- | --- |
| Sanity-check one notebook before opening a PR | `execute-single` | the notebook path |
| Quickly check structure without a slow run | `validate-single` | the notebook path |
| Re-run a notebook that failed in CI, with detail | `execute-single` | the path + **Enable debug logging** |
| Re-run everything after an environment change | `execute-all` | nothing |
| Rebuild the published site after a docs-only edit | `build-html-only` | nothing |
| Retire a notebook | `deprecate-notebook` | the path (coordinate with a maintainer first) |

!!! note "Faster feedback lives on your laptop"
    On-demand runs use real CI runners and take a few minutes. While you are
    actively editing, the local harness is faster: see
    [Local Testing (Cheatsheet)](../local-testing-guide.md). Use on-demand
    runs when you want the real CI environment or to rebuild the site.

## Reading the result

- **Green check** means the action passed. For `build-html-only`, the updated
  site publishes shortly after.
- **Red X** means it failed. Open the run, click the failed job, expand the step,
  and read the error. The same fixes from the [Quick Reference](quick-reference.md)
  apply (declare a missing dependency, restart-and-run-all for ordering, remove a
  hardcoded secret).

---

Need a hand? STScI staff can [submit a ticket to SPB](https://innerspace.stsci.edu/pages/viewpage.action?pageId=637400835&spaceKey=DDP&title=DMD%2BDev%2BPortal%2BHome).

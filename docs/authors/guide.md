# Notebook CI: A Guide for Notebook Authors

This guide is for scientists writing notebooks in a repository that uses the
[`spacetelescope/notebook-ci-actions`](https://github.com/spacetelescope/notebook-ci-actions)
CI system. You do not need to set up or edit the CI itself (a maintainer has
already done that). This explains what the CI does to your notebook, how to make
your notebook pass, and how to catch problems on your laptop before you push.

---

## The one-minute version

When you open a pull request or merge to `main`, the CI automatically runs your
notebooks through some combination of these checks:

1. **Validation** - confirms each notebook is structurally valid and its cells
   produce the expected output (via `pytest` + `nbval`).
2. **Security scan** - flags risky code patterns (via `bandit`).
3. **Execution** - actually runs your notebook top to bottom in a clean
   environment.
4. **Storage** - saves executed outputs to a `gh-storage` branch.
5. **HTML build** - renders the notebooks into a documentation site
   (via JupyterBook).

Which checks run depends on context. Pull requests get fast validation; merges
to `main` get the full treatment including the published docs.

**The single most useful habit:** run the local test script before you push.
It takes about two minutes and saves you the 5-10 minute wait for CI to tell you
something a local run would have caught instantly.

!!! note "Where the test scripts live"
    The local-testing helper scripts (`test-local-ci.sh`, `diagnose-local-ci.sh`) ship in [`notebook-ci-actions/scripts`](https://github.com/spacetelescope/notebook-ci-actions/tree/main/scripts), not in a repo created from the template. Clone `notebook-ci-actions` next to your repo and run them from there (e.g. `../notebook-ci-actions/scripts/test-local-ci.sh`), or copy the scripts in. The `./scripts/...` examples assume one of those.

```bash
./scripts/test-local-ci.sh
```

---

## What "passing CI" actually requires

The checks above boil down to a short contract. If your notebook satisfies these,
it will almost always pass:

### 1. It runs cleanly from top to bottom

The execution check restarts the kernel and runs every cell in order in a fresh
environment. A notebook that only works because you ran cells out of order, or
relied on a variable from an earlier session, will fail here. Before pushing,
do **Kernel → Restart & Run All** locally and confirm it completes.

### 2. Its dependencies are declared

The CI builds a clean environment and installs only what the repository declares.
If your notebook imports a package, that package must be listed somewhere the CI
knows about, typically:

- a `requirements.txt` (pip), or
- a conda environment the repo is configured to use (see below).

A notebook that runs on your machine but imports something you `pip install`ed
months ago and forgot about is the most common cause of a green-locally,
red-in-CI surprise.

### 3. It does not trip the security scanner

`bandit` flags patterns like running shell commands from untrusted input,
hardcoded credentials, or unsafe deserialization. If you get a security failure,
it is usually pointing at something real. Do not paste secrets (passwords, tokens,
API keys) into notebook cells. Use repository secrets instead (see
[Notebooks that need credentials](#notebooks-that-need-credentials)).

### 4. Its data dependencies are handled

If your notebook downloads or depends on external data, that data has to be
available when the CI runs the notebook on a clean machine. Repositories handle
this with a pre-processing hook that runs before validation and execution. If your
repo has one, make sure your notebook's data needs are covered by it rather than
assuming files already exist on disk.

---

## Test locally before you push

There are three local tools, fastest to most thorough. For everyday notebook work
you will mostly use the first two.

### Prerequisites

```bash
python3 --version    # needs 3.9 or newer
git status           # run from inside the repo
```

Docker and [`act`](https://github.com/nektos/act) are optional and only needed
for the full workflow simulation. On macOS: `brew install act`.

### The three tools

| Tool | Time | What it does | When to use |
| --- | --- | --- | --- |
| `./scripts/validate-workflows.sh` | ~30 sec | Checks workflow YAML syntax | Rarely relevant to authors |
| `./scripts/test-local-ci.sh` | 2-5 min | Simulates the CI pipeline on your notebooks | **Before every push** |
| `./scripts/test-with-act.sh pull_request` | 5-10 min | Runs the real GitHub Actions workflow in Docker | Final check before a big PR |

### Useful speed controls

You rarely need the full run while iterating. These environment variables make
local testing faster:

```bash
# Validate only, no execution (fastest useful check, ~1-2 min)
EXECUTION_MODE=validation-only ./scripts/test-local-ci.sh

# Focus on the single notebook you are editing
SINGLE_NOTEBOOK=notebooks/my-analysis.ipynb ./scripts/test-local-ci.sh

# Skip the slow bits while developing
RUN_SECURITY_SCAN=false BUILD_DOCUMENTATION=false ./scripts/test-local-ci.sh
```

`EXECUTION_MODE` accepts `validation-only` (fastest), `quick` (samples the first
few notebooks), and `full` (everything).

### If the local script hangs on "Installing dependencies"

This is almost always large scientific packages (astropy, scipy, numpy)
compiling, slow downloads, or an environment conflict, and it is especially
common on Apple Silicon Macs. Quick escapes:

```bash
# Skip dependency install and reuse what you have
SKIP_DEPS=true ./scripts/test-local-ci.sh

# Or skip execution entirely
EXECUTION_MODE=validation-only ./scripts/test-local-ci.sh

# Kill a stuck run
pkill -f "test-local-ci"

# Run the built-in diagnostic
./scripts/diagnose-local-ci.sh
```

If scripts will not run at all, make them executable: `chmod +x scripts/*.sh`.

---

## Special situations

Most notebooks need none of this. Reach for these only if your science requires it.

### Notebooks that need conda packages

Some domains rely on conda-only tooling rather than pip. The repository is
configured to use a specific conda environment:

| Environment | Use for |
| --- | --- |
| `hstcal` | HST calibration tools |
| `stenv` | JWST / Space Telescope environment |
| `astropy` | General astronomy |

You do not set this yourself, but it tells you which packages are available to
your notebook. To mirror it locally for JWST work, for example:

```bash
export CRDS_SERVER_URL="https://jwst-crds.stsci.edu"
export CRDS_PATH="/tmp/crds_cache"
./scripts/test-local-ci.sh
```

### Notebooks that use CRDS (JWST-style pipelines)

If your notebook needs CRDS reference files, the repository can be configured to
set `CRDS_SERVER_URL`, `CRDS_CONTEXT`, and `CRDS_PATH` during execution. When you
test locally, export the same variables (as shown above) so your local run matches
CI. If you need a pinned context, ask your maintainer to set `crds-context` rather
than hardcoding it in the notebook.

### Notebooks that need credentials

If your notebook accesses a service that needs a login (for example CasJobs), the
credentials live in repository secrets, never in the notebook. The common ones are
`CASJOBS_USERID` and `CASJOBS_PW`. Read them from the environment in your notebook;
do not paste the values into a cell. If you need a new secret added, that is a
maintainer task in the repository settings.

### Notebooks that depend on external data

If your notebook pulls data from an external source, that source has to be
reachable, and ideally stable, when CI runs. Unversioned external data is a common
cause of a notebook that passed last month and fails today through no change of
your own. If you control the data, prefer a versioned, stable location. If you
hit a data-related failure that is not your code, flag it to your maintainer
rather than reworking the notebook.

---

## Reading the results

After a run, the CI posts a summary covering which notebooks were processed,
success and failure counts, and error detail for anything that broke. A few common
failure signatures and what they usually mean:

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `ModuleNotFoundError` in CI but not locally | Dependency not declared | Add it to `requirements.txt` or the conda env |
| Cell fails with `NameError` | Notebook relies on out-of-order execution | Restart kernel and Run All; fix the order |
| Security check fails | `bandit` flagged a real pattern | Remove hardcoded secrets / unsafe calls |
| Passed before, fails now, your code unchanged | External data or dependency drifted | Flag to maintainer; check data source |
| Times out or runs out of memory | Notebook too slow/heavy, or stuck on a download | Reduce work or stage data via the pre-processing hook; if it is genuinely resource-heavy, ask a maintainer to assign a [larger runner](../custom-runner-configuration.md) |

For verbose logs, a maintainer can enable `ACTIONS_STEP_DEBUG` in the repository
variables.

---

## Retiring an old notebook

If a notebook is being phased out, it is not simply deleted. The CI has a
deprecation flow that tags it, adds a visible warning to the rendered docs, and
eventually moves it to a deprecated branch after a grace period (commonly 30-60
days). This is triggered by a maintainer through a manual run, so if you want a
notebook deprecated, ask rather than deleting the file in a PR.

---

## Where to go deeper

These are the canonical maintainer-facing docs. You usually will not need them,
but they are the source of truth:

- **[Quick Start (local testing)](https://github.com/spacetelescope/notebook-ci-actions/blob/main/QUICK_START.md)** - the 5-minute local testing setup
- **[Configuration Reference](https://github.com/spacetelescope/notebook-ci-actions/blob/main/docs/configuration-reference.md)** - every workflow option
- **[Local Testing Guide](https://github.com/spacetelescope/notebook-ci-actions/blob/main/docs/local-testing-guide.md)** - the complete local testing walkthrough
- **[Troubleshooting](https://github.com/spacetelescope/notebook-ci-actions/blob/main/docs/troubleshooting-unified.md)** - common issues and solutions
- **[Main README](https://github.com/spacetelescope/notebook-ci-actions/blob/main/README.md)** - the full system overview

Still stuck? STScI staff can [submit a ticket to SPB](https://innerspace.stsci.edu/pages/viewpage.action?pageId=637400835&spaceKey=DDP&title=DMD%2BDev%2BPortal%2BHome); external contributors should open an issue in the repository.

---

*This guide distills the repository documentation for a notebook-author audience.
If something here disagrees with the linked docs above, the linked docs win.*

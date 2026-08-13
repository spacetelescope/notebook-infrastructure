# Glossary

Plain-language definitions of the terms used across this site.

| Term | What it means |
| --- | --- |
| **CI / CI/CD** | Continuous Integration. Automated checks (validation, execution, security, docs build) that run when you open a pull request or merge. |
| **Unified workflow** | The single reusable workflow, `notebook-ci-unified.yml`, in [`notebook-ci-actions`](https://github.com/spacetelescope/notebook-ci-actions). It is the source of truth for how the CI behaves. |
| **Caller workflow** | A small workflow file in *your* repo (under `.github/workflows/`) that calls the unified workflow and sets its inputs. |
| **`@v1`** | A version tag your caller pins to. `@v1` follows the latest `v1.x.x` release; you can also pin an exact tag (`@v1.2.3`) or a commit SHA. See [Semantic Versioning](semantic-versioning.md). |
| **`main`** | Your repository's default branch, where notebooks are merged and published from. |
| **`gh-pages` branch** | The branch GitHub Pages serves your published notebook HTML from. |
| **`gh-storage` branch** | Where the CI stores *executed* versions of your notebooks; used to build HTML and as a baseline for the weekly scheduled run. |
| **`_toc.yml`** | The JupyterBook table of contents: which notebooks appear in your published docs and in what order. |
| **`_config.yml`** | The JupyterBook configuration: title, author, logo, analytics, and other site settings. |
| **`requirements.txt`** | The list of Python packages your notebooks need. Can be repo-wide or per notebook directory. |
| **nbval** | A pytest plugin the CI uses to validate that a notebook's outputs are consistent. |
| **nbconvert** | The tool the CI uses to execute a notebook top to bottom. |
| **bandit** | A security scanner the CI runs to flag risky code patterns (e.g. hardcoded secrets). |
| **CRDS** | Calibration Reference Data System, used by JWST/HST-style pipelines. Configured via the `crds-*` workflow inputs. |
| **Execution mode** | The workflow input (`pr`, `merge`, `scheduled`, `on-demand`) that tells the unified workflow which scenario it is running. Not to be confused with the local harness's `EXECUTION_MODE` variable. |
| **Pre/post-processing script** | Optional scripts (`pre-processing-script`, `post-processing-script` inputs) that run before or after notebook execution, e.g. to stage data or post-process images. |
| **Selective execution** | Running only the notebook subdirectory that changed instead of the whole repo. See [Selective Execution & Smart Workflows](selective-execution.md). |
| **Smart routing** | Detecting that only docs/config changed and skipping notebook execution. See [Selective Execution & Smart Workflows](selective-execution.md). |
| **Template repository** | [`notebook-ci-template`](https://github.com/spacetelescope/notebook-ci-template), the starting point for a new notebook repo. |
| **SPB** | The STScI team you submit a help ticket to (internal). |

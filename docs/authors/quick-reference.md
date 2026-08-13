# Notebook CI: One-Page Quick Reference

*For scientists writing notebooks in a repo that uses `spacetelescope/notebook-ci-actions`.*

## What runs, and when

| You do this | CI runs | Notebooks deploy to docs? |
| --- | --- | --- |
| Open / update a **pull request** | Validation, security, execution (changed notebooks only) | No (preview only) |
| **Merge** to `main` | Full pipeline + HTML build | Yes |

## Make your notebook pass (the contract)

- [ ] **Runs clean.** Kernel → Restart & Run All completes with no errors, in order.
- [ ] **Deps declared.** Everything you import is in `requirements.txt` or the repo's conda env.
- [ ] **No secrets in cells.** Read credentials from environment variables, never paste them.
- [ ] **Data is reachable.** External data is staged by the repo's pre-processing hook, not assumed on disk.

## Test locally before you push

!!! note "Where the test scripts live"
    The local-testing helper scripts (`test-local-ci.sh`, `diagnose-local-ci.sh`) ship in [`notebook-ci-actions/scripts`](https://github.com/spacetelescope/notebook-ci-actions/tree/main/scripts), not in a repo created from the template. Clone `notebook-ci-actions` next to your repo and run them from there (e.g. `../notebook-ci-actions/scripts/test-local-ci.sh`), or copy the scripts in. The `./scripts/...` examples assume one of those.

```bash
# Fastest useful check while editing (~1-2 min)
EXECUTION_MODE=validation-only ./scripts/test-local-ci.sh

# Full simulation before opening a PR (~2-5 min)
./scripts/test-local-ci.sh

# Just the notebook you're working on
SINGLE_NOTEBOOK=notebooks/my-analysis.ipynb ./scripts/test-local-ci.sh
```

Speed-ups: `SKIP_DEPS=true` (reuse installed packages) ·
`RUN_SECURITY_SCAN=false BUILD_DOCUMENTATION=false` (skip slow steps).
Stuck on "Installing dependencies"? `pkill -f test-local-ci` then rerun with `SKIP_DEPS=true`.
Scripts won't run? `chmod +x scripts/*.sh`.

## Common failures

| Symptom | Cause | Fix |
| --- | --- | --- |
| `ModuleNotFoundError` in CI, fine locally | Dependency not declared | Add to `requirements.txt` / conda env |
| `NameError` on a defined variable | Cells run out of order | Restart & Run All; fix ordering |
| Security check fails | `bandit` hit a real pattern | Remove hardcoded secret / unsafe call |
| Passed last month, fails now, code unchanged | External data or dep drifted | Flag to maintainer |
| Times out | Slow cell or stuck download | Trim work; stage data via pre-processing hook |

## Special cases (only if your science needs them)

- **JWST / CRDS:** export `CRDS_SERVER_URL`, `CRDS_CONTEXT`, `CRDS_PATH` to match CI locally.
- **Conda tooling:** repo uses `hstcal` (HST), `stenv` (JWST), or `astropy` (general).
- **Credentials (e.g. CasJobs):** stored as repo secrets (`CASJOBS_USERID`, `CASJOBS_PW`); ask a maintainer to add new ones.
- **Retiring a notebook:** don't just delete it. Ask a maintainer to run the deprecation flow.

## Need more?

Local testing → `QUICK_START.md` · All options → `docs/configuration-reference.md` ·
Problems → `docs/troubleshooting-unified.md`

Stuck and need a person? STScI staff can [submit a ticket to SPB](https://innerspace.stsci.edu/pages/viewpage.action?pageId=637400835&spaceKey=DDP&title=DMD%2BDev%2BPortal%2BHome).

---
*Workflow files reference a pinned version (e.g. `@v1`). You don't edit these; a maintainer keeps them current.*

# Scheduled Weekly Runs

!!! info "For maintainers"
    This page is reference material for repository maintainers and infrastructure owners. If you just write notebooks, start with the [Quick Reference](authors/quick-reference.md).


*For maintainers: what the weekly scheduled run does, and how to read it.*

Notebooks rot even when nobody touches them. A dependency ships a breaking
release, an external data URL moves, a CRDS context updates, and a notebook that
passed at merge time quietly starts failing. The scheduled run is how you catch
that drift before a user does. It re-runs your notebooks on a timer, so a red
mark means "the world changed," not "someone broke the code."

## What runs, and when

The scheduled workflow (`notebook-scheduled.yml`, shown in the Actions tab as
**Notebook CI - Scheduled**) is driven by a cron trigger:

```yaml
on:
  schedule:
    - cron: '0 2 * * 0'   # Sundays at 02:00 UTC
```

In the standard configuration it **re-executes every notebook** in the repo in a
clean environment (execution only; no PR, no HTML publish):

```yaml
jobs:
  execute-all:
    uses: spacetelescope/notebook-ci-actions/.github/workflows/notebook-ci-unified.yml@v1
    with:
      execution-mode: 'on-demand'
      trigger-event: 'execute'
      enable-execution: true
      # validation / security / storage / html-build left off
    secrets: inherit
```

!!! note "Why `on-demand` and not `scheduled`?"
    The workflow also defines a dedicated `execution-mode: 'scheduled'`. The standard
    template configures the weekly job with `on-demand` + `trigger-event: 'execute'` to
    re-execute notebooks; both are valid. Match whatever your repo's `notebook-scheduled.yml`
    already uses.

!!! note "Scheduled runs only fire on the default branch"
    GitHub runs `schedule` triggers from the workflow file on your **default
    branch** (`main`). Changes to the cron on a feature branch have no effect
    until merged.

## Change the schedule or scope

- **Reschedule:** edit the `cron` expression. `0 2 * * 0` is Sunday 02:00 UTC.
  For example, `0 9 * * 1` is Monday 09:00 UTC. Use [crontab.guru](https://crontab.guru)
  to check an expression.
- **Run more than execution:** flip the `enable-*` flags (for example
  `enable-validation: true` to also re-validate). See the
  [Configuration Reference](configuration-reference.md) for every flag.
- **Run it now:** scheduled runs cannot be forced from the UI unless the workflow
  also has a `workflow_dispatch` trigger. To reproduce a weekly run immediately,
  use the on-demand workflow's `execute-all` action.

## Read the results

1. Repository → **Actions** tab → **Notebook CI - Scheduled** in the left sidebar.
2. Each row is one weekly run. Open the most recent.
3. **Green** = every notebook still executes cleanly. Nothing to do.
4. **Red** = at least one notebook failed. Open the run, click the failed job,
   expand the failing notebook's step, and read the error.

Because the notebook code did not change between a passing run and a failing one,
a scheduled failure points at the environment. Read it that way:

| What you see in the log | Likely cause | What to do |
| --- | --- | --- |
| `ModuleNotFoundError` or a version/`ImportError` | An upstream dependency released a breaking change | Pin or bump it in `requirements.txt` (or the conda env), then re-run |
| Data download `404` / timeout | An external data source moved or went offline | Update the URL or the pre-processing/staging step |
| CRDS or reference-file errors (JWST) | The CRDS context advanced | Pin `crds-context`, or update the notebook's expectations |
| Auth failures (e.g. CasJobs) | A repository secret expired or rotated | Refresh the secret in repo settings |
| Times out | A cell got slower, or a download is hanging | Trim the work, or stage data via the pre-processing hook |

## When it goes red

1. **Reproduce locally** with `test-local-ci.sh` from your `notebook-ci-actions` clone (or the on-demand
   `execute-single` action) to confirm the failure and iterate on a fix.
2. **Fix the drift** (pin a dependency, update a data location, refresh a secret).
3. **Open a PR** with the fix; the PR run confirms the notebook passes again.
4. If the failure is environmental and not yours to fix, flag it. See the
   [Troubleshooting guide](troubleshooting-unified.md).

!!! tip "Stay notified"
    Scheduled failures are reported in the repository's **Actions** tab and to the
    repository-specific **Slack channel** the CI posts to. GitHub also emails the
    maintainer who last edited the workflow file. If that is not the right person,
    configure repository notifications so a weekly failure is not missed.

## Related

- [On-Demand Runs](authors/on-demand-runs.md) - reproduce a weekly run manually
- [Configuration Reference](configuration-reference.md) - every `enable-*` flag and trigger
- [Troubleshooting](troubleshooting-unified.md) - common failures and fixes

---

STScI staff: for help reading or fixing a scheduled failure, [submit a ticket to SPB](https://innerspace.stsci.edu/pages/viewpage.action?pageId=637400835&spaceKey=DDP&title=DMD%2BDev%2BPortal%2BHome).

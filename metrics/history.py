"""
backfill_ci_history.py

One-time backfill for metrics/history.json using historical completed workflow runs.

For each repository in the repo list:
- finds the named workflow
- fetches completed runs (newest first)
- compares each run to the immediately previous completed run
- generates history entries in the same shape used by scheduled_ci_report.py
- writes a populated history.json

Usage:
    python backfill_ci_history.py repos.txt history.json

Optional environment variables:
    GITHUB_TOKEN   - recommended
    WORKFLOW_NAME  - defaults to "Notebook CI - Scheduled"
    MAX_RUNS       - max completed runs to inspect per repo, default 30
"""

import json
import os
import sys
from datetime import datetime, timezone

import requests

TOKEN = os.environ.get("GITHUB_TOKEN", "")
WORKFLOW_NAME = os.environ.get("WORKFLOW_NAME", "Notebook CI - Scheduled")
MAX_RUNS = int(os.environ.get("MAX_RUNS", "30"))
API_BASE = "https://api.github.com"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def gh_get(url, params=None):
    resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json(), resp.headers


def load_repositories(repo_file):
    repos = []
    with open(repo_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            repos.append(line)
    return repos


def get_workflow_id(repo, workflow_name):
    url = f"{API_BASE}/repos/{repo}/actions/workflows"
    data, _ = gh_get(url, params={"per_page": 100})
    for wf in data.get("workflows", []):
        if wf["name"] == workflow_name:
            return wf["id"]
    raise ValueError(f"Workflow '{workflow_name}' not found in {repo}")


def list_workflow_runs(repo, workflow_id, max_runs=30):
    runs = []
    page = 1
    per_page = min(100, max_runs)

    while len(runs) < max_runs:
        url = f"{API_BASE}/repos/{repo}/actions/workflows/{workflow_id}/runs"
        data, _ = gh_get(
            url,
            params={
                "status": "completed",
                "per_page": per_page,
                "page": page,
            },
        )
        batch = data.get("workflow_runs", [])
        if not batch:
            break

        runs.extend(batch)
        if len(batch) < per_page:
            break
        page += 1

    return runs[:max_runs]


def get_notebook_results(repo, run_id):
    """
    Return {notebook_path: conclusion} for a given run.

    Only jobs whose names contain 'process-notebooks' are considered.
    """
    results = {}
    url = f"{API_BASE}/repos/{repo}/actions/runs/{run_id}/jobs"
    params = {"per_page": 100, "filter": "all"}

    while url:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        for job in data.get("jobs", []):
            name = job.get("name", "")
            if "process-notebooks" not in name:
                continue

            if "(" in name and name.endswith(")"):
                nb_path = name[name.index("(") + 1 : -1].strip()
            else:
                nb_path = name

            results[nb_path] = job.get("conclusion", "unknown")

        link = resp.headers.get("Link", "")
        url = None
        params = {}
        for part in link.split(","):
            part = part.strip()
            if 'rel="next"' in part:
                url = part.split(";")[0].strip().strip("<>")

    return results


def compare_results(latest_results, previous_results):
    all_notebooks = sorted(set(latest_results.keys()) | set(previous_results.keys()))

    new_failures = []
    resolved_failures = []
    consistent_failures = []

    for nb in all_notebooks:
        in_latest = nb in latest_results
        in_previous = nb in previous_results

        if not in_latest or not in_previous:
            continue

        prev = previous_results[nb]
        curr = latest_results[nb]

        if prev == "success" and curr == "failure":
            new_failures.append(nb)
        elif prev == "failure" and curr == "success":
            resolved_failures.append(nb)
        elif prev == "failure" and curr == "failure":
            consistent_failures.append(nb)

    return {
        "fail_latest": sum(1 for c in latest_results.values() if c == "failure"),
        "pass_latest": sum(1 for c in latest_results.values() if c == "success"),
        "total_latest": len(latest_results),
        "fail_previous": sum(1 for c in previous_results.values() if c == "failure"),
        "pass_previous": sum(1 for c in previous_results.values() if c == "success"),
        "total_previous": len(previous_results),
        "new_failures": len(new_failures),
        "resolved_failures": len(resolved_failures),
        "consistent_failures": len(consistent_failures),
    }


def build_history_entry(latest_run, previous_run, comp):
    return {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "latest_run_number": latest_run["run_number"],
        "latest_run_created_at": latest_run["created_at"],
        "latest_run_url": latest_run["html_url"],
        "previous_run_number": previous_run["run_number"],
        "previous_run_created_at": previous_run["created_at"],
        "previous_run_url": previous_run["html_url"],
        "fail_latest": comp["fail_latest"],
        "pass_latest": comp["pass_latest"],
        "total_latest": comp["total_latest"],
        "fail_previous": comp["fail_previous"],
        "pass_previous": comp["pass_previous"],
        "total_previous": comp["total_previous"],
        "new_failures": comp["new_failures"],
        "resolved_failures": comp["resolved_failures"],
        "consistent_failures": comp["consistent_failures"],
    }


def main():
    if len(sys.argv) < 3:
        print(
            "Usage: python backfill_ci_history.py repos.txt history.json",
            file=sys.stderr,
        )
        sys.exit(1)

    repo_file = sys.argv[1]
    history_file = sys.argv[2]

    repos = load_repositories(repo_file)
    if not repos:
        print("No repositories found in repo file.", file=sys.stderr)
        sys.exit(1)

    history = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "workflow_name": WORKFLOW_NAME,
        "repos": {},
    }

    errors = []

    for repo in repos:
        try:
            print(f"Backfilling {repo}...", file=sys.stderr)
            workflow_id = get_workflow_id(repo, WORKFLOW_NAME)
            runs = list_workflow_runs(repo, workflow_id, max_runs=MAX_RUNS)

            if len(runs) < 2:
                print(f"Skipping {repo}: fewer than 2 completed runs", file=sys.stderr)
                history["repos"][repo] = []
                continue

            entries = []
            cache = {}

            # Oldest comparable pair first, newest last
            # runs is newest-first, so iterate reversed over pairs:
            # (older previous, newer latest)
            for idx in range(len(runs) - 2, -1, -1):
                latest_run = runs[idx]
                previous_run = runs[idx + 1]

                for run in (latest_run, previous_run):
                    if run["id"] not in cache:
                        cache[run["id"]] = get_notebook_results(repo, run["id"])

                latest_results = cache[latest_run["id"]]
                previous_results = cache[previous_run["id"]]

                comp = compare_results(latest_results, previous_results)
                entry = build_history_entry(latest_run, previous_run, comp)
                entries.append(entry)

            history["repos"][repo] = entries
            print(f"Backfilled {repo}: {len(entries)} history entries", file=sys.stderr)

        except Exception as exc:
            errors.append(f"{repo}: {exc}")
            history["repos"].setdefault(repo, [])

    if errors:
        history["errors"] = errors

    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    print(f"Wrote backfilled history to {history_file}", file=sys.stderr)
    if errors:
        print("Errors encountered:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)


if __name__ == "__main__":
    main()

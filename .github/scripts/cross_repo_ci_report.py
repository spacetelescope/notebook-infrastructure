"""
scheduled_ci_report.py

For each repository in a supplied repo list, compares the latest completed
"Notebook CI - Scheduled" GitHub Actions workflow run with the immediately
previous completed run, then writes a combined Markdown report.

Usage:
    python scheduled_ci_report.py repos.txt [output_file.md]

Repo list format:
    One repo per line, in owner/repo form, e.g.
        spacetelescope/hellouniverse
        spacetelescope/mast_notebooks
        spacetelescope/jdat_notebooks

Required environment variables:
    GITHUB_TOKEN  – optional but recommended, especially to avoid low rate limits
Optional environment variables:
    WORKFLOW_NAME – defaults to "Notebook CI - Scheduled"
"""

import os
import sys
from datetime import datetime, timezone

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
TOKEN = os.environ.get("GITHUB_TOKEN", "")
WORKFLOW_NAME = os.environ.get("WORKFLOW_NAME", "Notebook CI - Scheduled")
API_BASE = "https://api.github.com"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


# ---------------------------------------------------------------------------
# GitHub API helpers
# ---------------------------------------------------------------------------

def gh_get(url, params=None):
    resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json(), resp.headers


def get_workflow_id(repo, workflow_name):
    """Return the numeric workflow ID for a given workflow name."""
    url = f"{API_BASE}/repos/{repo}/actions/workflows"
    data, _ = gh_get(url, params={"per_page": 100})
    for wf in data.get("workflows", []):
        if wf["name"] == workflow_name:
            return wf["id"]
    raise ValueError(f"Workflow '{workflow_name}' not found in {repo}")


def list_workflow_runs(repo, workflow_id, per_page=20):
    """Return completed workflow runs, most-recent first."""
    url = f"{API_BASE}/repos/{repo}/actions/workflows/{workflow_id}/runs"
    data, _ = gh_get(url, params={"status": "completed", "per_page": per_page})
    return data.get("workflow_runs", [])


def get_notebook_results(repo, run_id):
    """Return {notebook_path: conclusion} for a given run.

    Only jobs whose names contain 'process-notebooks' are considered;
    the notebook path is extracted from the parenthesised portion of the
    job name, e.g.
        "execute-all / process-notebooks (notebooks/foo/bar.ipynb)"
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


# ---------------------------------------------------------------------------
# Repo list helpers
# ---------------------------------------------------------------------------

def load_repositories(repo_file):
    repos = []
    with open(repo_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            repos.append(line)
    return repos


# ---------------------------------------------------------------------------
# Comparison + report helpers
# ---------------------------------------------------------------------------

def compare_results(latest_results, previous_results):
    all_notebooks = sorted(set(latest_results.keys()) | set(previous_results.keys()))

    new_failures = []       # success before -> failure now
    resolved_failures = []  # failure before -> success now
    consistent_failures = []
    consistent_successes = []
    changed_other = []      # unknown/cancelled/etc transitions
    only_in_latest = []
    only_in_previous = []

    for nb in all_notebooks:
        in_latest = nb in latest_results
        in_previous = nb in previous_results

        if in_latest and not in_previous:
            only_in_latest.append((nb, latest_results[nb]))
            continue
        if in_previous and not in_latest:
            only_in_previous.append((nb, previous_results[nb]))
            continue

        prev = previous_results[nb]
        curr = latest_results[nb]

        if prev == "success" and curr == "failure":
            new_failures.append(nb)
        elif prev == "failure" and curr == "success":
            resolved_failures.append(nb)
        elif prev == "failure" and curr == "failure":
            consistent_failures.append(nb)
        elif prev == "success" and curr == "success":
            consistent_successes.append(nb)
        elif prev != curr:
            changed_other.append((nb, prev, curr))

    summary = {
        "total_latest": len(latest_results),
        "fail_latest": sum(1 for c in latest_results.values() if c == "failure"),
        "pass_latest": sum(1 for c in latest_results.values() if c == "success"),
        "total_previous": len(previous_results),
        "fail_previous": sum(1 for c in previous_results.values() if c == "failure"),
        "pass_previous": sum(1 for c in previous_results.values() if c == "success"),
        "new_failures": new_failures,
        "resolved_failures": resolved_failures,
        "consistent_failures": consistent_failures,
        "consistent_successes": consistent_successes,
        "changed_other": changed_other,
        "only_in_latest": only_in_latest,
        "only_in_previous": only_in_previous,
    }
    return summary


def build_repo_section(repo, latest_run, previous_run, latest_results, previous_results):
    comp = compare_results(latest_results, previous_results)

    latest_url = latest_run["html_url"]
    latest_date = latest_run["created_at"][:10]
    previous_url = previous_run["html_url"]
    previous_date = previous_run["created_at"][:10]

    lines = [
        f"## `{repo}`",
        "",
        f"| | Run | Date | Pass | Fail | Total |",
        f"|---|---|---|---|---|---|",
        f"| **Latest** | [#{latest_run['run_number']}]({latest_url}) | {latest_date} | {comp['pass_latest']} | {comp['fail_latest']} | {comp['total_latest']} |",
        f"| **Previous** | [#{previous_run['run_number']}]({previous_url}) | {previous_date} | {comp['pass_previous']} | {comp['fail_previous']} | {comp['total_previous']} |",
        "",
        f"- **New failures:** {len(comp['new_failures'])}",
        f"- **Resolved failures:** {len(comp['resolved_failures'])}",
        f"- **Consistent failures:** {len(comp['consistent_failures'])}",
        "",
    ]

    lines.append(f"### 🔴 New Failures ({len(comp['new_failures'])})")
    lines.append("")
    if comp["new_failures"]:
        for nb in comp["new_failures"]:
            lines.append(f"- `{nb}`")
    else:
        lines.append("_No new failures_ ✅")
    lines.append("")

    lines.append(f"### 🟢 Resolved Failures ({len(comp['resolved_failures'])})")
    lines.append("")
    if comp["resolved_failures"]:
        for nb in comp["resolved_failures"]:
            lines.append(f"- `{nb}`")
    else:
        lines.append("_No resolved failures_")
    lines.append("")

    lines.append(f"### 🟡 Consistent Failures ({len(comp['consistent_failures'])})")
    lines.append("")
    if comp["consistent_failures"]:
        for nb in comp["consistent_failures"]:
            lines.append(f"- `{nb}`")
    else:
        lines.append("_No consistent failures_ ✅")
    lines.append("")

    lines.append(f"### ✅ Consistent Successes ({len(comp['consistent_successes'])})")
    lines.append("")
    lines.append("<details>")
    lines.append("<summary>Click to expand</summary>")
    lines.append("")
    if comp["consistent_successes"]:
        for nb in comp["consistent_successes"]:
            lines.append(f"- `{nb}`")
    else:
        lines.append("_None_")
    lines.append("")
    lines.append("</details>")
    lines.append("")

    if comp["changed_other"]:
        lines.append(f"### ⚪ Other Status Changes ({len(comp['changed_other'])})")
        lines.append("")
        for nb, prev, curr in comp["changed_other"]:
            lines.append(f"- `{nb}`: `{prev}` → `{curr}`")
        lines.append("")

    if comp["only_in_latest"]:
        lines.append(f"### ➕ Only in Latest Run ({len(comp['only_in_latest'])})")
        lines.append("")
        for nb, conclusion in comp["only_in_latest"]:
            lines.append(f"- `{nb}` ({conclusion})")
        lines.append("")

    if comp["only_in_previous"]:
        lines.append(f"### ➖ Only in Previous Run ({len(comp['only_in_previous'])})")
        lines.append("")
        for nb, conclusion in comp["only_in_previous"]:
            lines.append(f"- `{nb}` ({conclusion})")
        lines.append("")

    return "\n".join(lines), comp


def build_report(results, errors):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        "# Notebook CI – Latest vs Previous Run Comparison",
        "",
        f"_Generated {now}_",
        "",
        f"Workflow name: `{WORKFLOW_NAME}`",
        "",
    ]

    if results:
        lines.extend([
            "## Summary",
            "",
            "| Repository | Latest Run | Previous Run | New Failures | Resolved | Consistent Failures | Latest Fail Count |",
            "|---|---|---|---:|---:|---:|---:|",
        ])
        for item in results:
            comp = item["comparison"]
            lines.append(
                f"| `{item['repo']}` | "
                f"[#{item['latest_run']['run_number']}]({item['latest_run']['html_url']}) | "
                f"[#{item['previous_run']['run_number']}]({item['previous_run']['html_url']}) | "
                f"{len(comp['new_failures'])} | "
                f"{len(comp['resolved_failures'])} | "
                f"{len(comp['consistent_failures'])} | "
                f"{comp['fail_latest']} |"
            )
        lines.append("")

        lines.append("## Per-Repository Details")
        lines.append("")
        for item in results:
            lines.append(item["section"])
            lines.append("")

    if errors:
        lines.append("## Errors")
        lines.append("")
        for err in errors:
            lines.append(f"- {err}")
        lines.append("")

    if not results and not errors:
        lines.append("_No repositories processed._")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python scheduled_ci_report.py repos.txt [output_file.md]", file=sys.stderr)
        sys.exit(1)

    repo_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    repos = load_repositories(repo_file)
    if not repos:
        print("No repositories found in repo file.", file=sys.stderr)
        sys.exit(1)

    results = []
    errors = []

    for repo in repos:
        try:
            print(f"Fetching workflow runs for '{WORKFLOW_NAME}' in {repo}…", file=sys.stderr)
            workflow_id = get_workflow_id(repo, WORKFLOW_NAME)
            runs = list_workflow_runs(repo, workflow_id)

            if len(runs) < 2:
                errors.append(f"`{repo}`: fewer than 2 completed runs found")
                continue

            latest_run = runs[0]
            previous_run = runs[1]

            print(
                f"{repo}: latest #{latest_run['run_number']} vs previous #{previous_run['run_number']}",
                file=sys.stderr,
            )

            latest_results = get_notebook_results(repo, latest_run["id"])
            previous_results = get_notebook_results(repo, previous_run["id"])

            section, comparison = build_repo_section(
                repo, latest_run, previous_run, latest_results, previous_results
            )

            results.append(
                {
                    "repo": repo,
                    "latest_run": latest_run,
                    "previous_run": previous_run,
                    "comparison": comparison,
                    "section": section,
                }
            )

        except Exception as exc:
            errors.append(f"`{repo}`: {exc}")

    report = build_report(results, errors)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report written to {output_file}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()

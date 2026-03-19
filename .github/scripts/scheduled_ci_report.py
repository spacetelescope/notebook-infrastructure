"""
scheduled_ci_report.py

For each repository in a supplied repo list, compares the latest completed
"Notebook CI - Scheduled" GitHub Actions workflow run with the immediately
previous completed run, writes a combined Markdown report, updates a persistent
history JSON file, generates a dashboard Markdown file with trend tables and
Mermaid charts, and writes a structured details JSON payload for a richer UI.

Usage:
    python scheduled_ci_report.py repos.txt report.md history.json dashboard.md details.json

Repo list format:
    One repo per line, in owner/repo form.

Required environment variables:
    GITHUB_TOKEN  – optional but recommended
Optional environment variables:
    WORKFLOW_NAME – defaults to "Notebook CI - Scheduled"
"""

import json
import os
import sys
from datetime import datetime, timezone

import requests

TOKEN = os.environ.get("GITHUB_TOKEN", "")
WORKFLOW_NAME = os.environ.get("WORKFLOW_NAME", "Notebook CI - Scheduled")
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


def get_workflow_id(repo, workflow_name):
    url = f"{API_BASE}/repos/{repo}/actions/workflows"
    data, _ = gh_get(url, params={"per_page": 100})
    for wf in data.get("workflows", []):
        if wf["name"] == workflow_name:
            return wf["id"]
    raise ValueError(f"Workflow '{workflow_name}' not found in {repo}")


def list_workflow_runs(repo, workflow_id, per_page=20):
    url = f"{API_BASE}/repos/{repo}/actions/workflows/{workflow_id}/runs"
    data, _ = gh_get(url, params={"status": "completed", "per_page": per_page})
    return data.get("workflow_runs", [])


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


def load_repositories(repo_file):
    repos = []
    with open(repo_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            repos.append(line)
    return repos


def compare_results(latest_results, previous_results):
    all_notebooks = sorted(set(latest_results.keys()) | set(previous_results.keys()))

    new_failures = []
    resolved_failures = []
    consistent_failures = []
    consistent_successes = []
    changed_other = []
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

    return {
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


def build_repo_section(repo, latest_run, previous_run, latest_results, previous_results):
    comp = compare_results(latest_results, previous_results)

    latest_url = latest_run["html_url"]
    latest_date = latest_run["created_at"][:10]
    previous_url = previous_run["html_url"]
    previous_date = previous_run["created_at"][:10]

    lines = [
        f"## `{repo}`",
        "",
        "| | Run | Date | Pass | Fail | Total |",
        "|---|---|---|---|---|---|",
        f"| **Latest** | [#{latest_run['run_number']}]({latest_url}) | {latest_date} | {comp['pass_latest']} | {comp['fail_latest']} | {comp['total_latest']} |",
        f"| **Previous** | [#{previous_run['run_number']}]({previous_url}) | {previous_date} | {comp['pass_previous']} | {comp['fail_previous']} | {comp['total_previous']} |",
        "",
        f"- **New failures:** {len(comp['new_failures'])}",
        f"- **Resolved failures:** {len(comp['resolved_failures'])}",
        f"- **Consistent failures:** {len(comp['consistent_failures'])}",
        "",
    ]

    sections = [
        ("### 🔴 New Failures", comp["new_failures"], "_No new failures_ ✅"),
        ("### 🟢 Resolved Failures", comp["resolved_failures"], "_No resolved failures_"),
        ("### 🟡 Consistent Failures", comp["consistent_failures"], "_No consistent failures_ ✅"),
    ]

    for title, items, empty_text in sections:
        lines.append(f"{title} ({len(items)})")
        lines.append("")
        if items:
            for item in items:
                lines.append(f"- `{item}`")
        else:
            lines.append(empty_text)
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

    return "\n".join(lines)


def load_history(history_file):
    if not os.path.exists(history_file):
        return {"generated_at": None, "workflow_name": WORKFLOW_NAME, "repos": {}}
    with open(history_file, "r", encoding="utf-8") as f:
        return json.load(f)


def update_history(history, results):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    history["generated_at"] = now
    history["workflow_name"] = WORKFLOW_NAME
    repos_hist = history.setdefault("repos", {})

    for item in results:
        repo = item["repo"]
        comp = item["comparison"]
        latest_run = item["latest_run"]
        previous_run = item["previous_run"]

        entry = {
            "timestamp": now,
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
            "new_failures": len(comp["new_failures"]),
            "resolved_failures": len(comp["resolved_failures"]),
            "consistent_failures": len(comp["consistent_failures"]),
        }

        repo_entries = repos_hist.setdefault(repo, [])

        if repo_entries and repo_entries[-1].get("latest_run_number") == latest_run["run_number"]:
            repo_entries[-1] = entry
        else:
            repo_entries.append(entry)

        repos_hist[repo] = repo_entries[-26:]

    return history


def render_mermaid_bar_latest_failures(history):
    repos = sorted(history.get("repos", {}).keys())
    if not repos:
        return "_No data yet._"

    labels = []
    values = []

    for repo in repos:
        entries = history["repos"].get(repo, [])
        if not entries:
            continue
        short_name = repo.split("/")[-1]
        labels.append(short_name)
        values.append(entries[-1]["fail_latest"])

    if not labels:
        return "_No data yet._"

    label_str = ", ".join(f'"{x}"' for x in labels)
    value_str = ", ".join(str(v) for v in values)
    upper = max(5, max(values) + 1)

    return "\n".join([
        "```mermaid",
        "xychart-beta",
        '    title "Latest failure count by repository"',
        f'    x-axis [{label_str}]',
        f'    y-axis "Failures" 0 --> {upper}',
        f'    bar [{value_str}]',
        "```",
    ])


def render_mermaid_trend_for_repo(repo, entries):
    short_name = repo.split("/")[-1]
    labels = [e["latest_run_created_at"][:10] for e in entries]
    values = [e["fail_latest"] for e in entries]

    label_str = ", ".join(f'"{x}"' for x in labels)
    value_str = ", ".join(str(v) for v in values)
    ymax = max(values + [1])
    upper = max(5, ymax + 1)

    return "\n".join([
        "```mermaid",
        "xychart-beta",
        f'    title "{short_name} failure trend"',
        f'    x-axis [{label_str}]',
        f'    y-axis "Failures" 0 --> {upper}',
        f'    line [{value_str}]',
        "```",
    ])


def build_dashboard(history):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    repos = sorted(history.get("repos", {}).keys())

    lines = [
        "# Notebook CI Dashboard",
        "",
        f"_Generated {now}_",
        "",
        f"Workflow tracked: `{history.get('workflow_name', WORKFLOW_NAME)}`",
        "",
        "## Executive Summary",
        "",
    ]

    if repos:
        lines.extend([
            "| Repository | Latest Failures | New Failures | Resolved | Consistent Failures | Latest Run |",
            "|---|---:|---:|---:|---:|---|",
        ])
        for repo in repos:
            entries = history["repos"].get(repo, [])
            if not entries:
                continue
            latest = entries[-1]
            lines.append(
                f"| `{repo}` | "
                f"{latest['fail_latest']} | "
                f"{latest['new_failures']} | "
                f"{latest['resolved_failures']} | "
                f"{latest['consistent_failures']} | "
                f"[#{latest['latest_run_number']}]({latest['latest_run_url']}) |"
            )
        lines.append("")
    else:
        lines.append("_No data yet._")
        lines.append("")

    lines.append("## Latest Failure Count by Repository")
    lines.append("")
    lines.append(render_mermaid_bar_latest_failures(history))
    lines.append("")

    lines.append("## Rolling Trend Table")
    lines.append("")

    if repos:
        all_dates = sorted({
            entry["latest_run_created_at"][:10]
            for repo in repos
            for entry in history["repos"].get(repo, [])
        })

        header = "| Repository | " + " | ".join(all_dates) + " |"
        divider = "|---|" + "|".join(["---:" for _ in all_dates]) + "|"
        lines.append(header)
        lines.append(divider)

        for repo in repos:
            entries = history["repos"].get(repo, [])
            by_date = {e["latest_run_created_at"][:10]: e["fail_latest"] for e in entries}
            row = [f"`{repo}`"] + [str(by_date.get(d, "")) for d in all_dates]
            lines.append("| " + " | ".join(row) + " |")
        lines.append("")
    else:
        lines.append("_No trend data yet._")
        lines.append("")

    lines.append("## Per-Repository Trends")
    lines.append("")

    for repo in repos:
        entries = history["repos"].get(repo, [])
        if not entries:
            continue

        lines.append(f"### `{repo}`")
        lines.append("")
        lines.append(render_mermaid_trend_for_repo(repo, entries))
        lines.append("")
        lines.extend([
            "| Date | Failures | New | Resolved | Consistent | Latest Run |",
            "|---|---:|---:|---:|---:|---|",
        ])
        for e in entries:
            lines.append(
                f"| {e['latest_run_created_at'][:10]} | "
                f"{e['fail_latest']} | "
                f"{e['new_failures']} | "
                f"{e['resolved_failures']} | "
                f"{e['consistent_failures']} | "
                f"[#{e['latest_run_number']}]({e['latest_run_url']}) |"
            )
        lines.append("")

    return "\n".join(lines)


def build_details_payload(results, errors):
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    payload = {
        "generated_at": generated_at,
        "workflow_name": WORKFLOW_NAME,
        "repositories": [],
        "errors": errors,
    }

    for item in results:
        comp = item["comparison"]
        latest_run = item["latest_run"]
        previous_run = item["previous_run"]

        payload["repositories"].append(
            {
                "repo": item["repo"],
                "latest_run": {
                    "number": latest_run["run_number"],
                    "url": latest_run["html_url"],
                    "created_at": latest_run["created_at"],
                },
                "previous_run": {
                    "number": previous_run["run_number"],
                    "url": previous_run["html_url"],
                    "created_at": previous_run["created_at"],
                },
                "summary": {
                    "fail_latest": comp["fail_latest"],
                    "pass_latest": comp["pass_latest"],
                    "total_latest": comp["total_latest"],
                    "fail_previous": comp["fail_previous"],
                    "pass_previous": comp["pass_previous"],
                    "total_previous": comp["total_previous"],
                    "new_failures": len(comp["new_failures"]),
                    "resolved_failures": len(comp["resolved_failures"]),
                    "consistent_failures": len(comp["consistent_failures"]),
                    "consistent_successes": len(comp["consistent_successes"]),
                },
                "details": {
                    "new_failures": comp["new_failures"],
                    "resolved_failures": comp["resolved_failures"],
                    "consistent_failures": comp["consistent_failures"],
                    "consistent_successes": comp["consistent_successes"],
                    "changed_other": [
                        {"notebook": nb, "previous": prev, "current": curr}
                        for nb, prev, curr in comp["changed_other"]
                    ],
                    "only_in_latest": [
                        {"notebook": nb, "conclusion": conclusion}
                        for nb, conclusion in comp["only_in_latest"]
                    ],
                    "only_in_previous": [
                        {"notebook": nb, "conclusion": conclusion}
                        for nb, conclusion in comp["only_in_previous"]
                    ],
                },
            }
        )

    return payload


def main():
    if len(sys.argv) < 6:
        print(
            "Usage: python scheduled_ci_report.py repos.txt report.md history.json dashboard.md details.json",
            file=sys.stderr,
        )
        sys.exit(1)

    repo_file = sys.argv[1]
    report_file = sys.argv[2]
    history_file = sys.argv[3]
    dashboard_file = sys.argv[4]
    details_file = sys.argv[5]

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
    history = load_history(history_file)
    history = update_history(history, results)
    dashboard = build_dashboard(history)
    details = build_details_payload(results, errors)

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    with open(dashboard_file, "w", encoding="utf-8") as f:
        f.write(dashboard)

    with open(details_file, "w", encoding="utf-8") as f:
        json.dump(details, f, indent=2)

    print(f"Report written to {report_file}", file=sys.stderr)
    print(f"History written to {history_file}", file=sys.stderr)
    print(f"Dashboard written to {dashboard_file}", file=sys.stderr)
    print(f"Details written to {details_file}", file=sys.stderr)


if __name__ == "__main__":
    main()

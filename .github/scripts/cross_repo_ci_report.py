#!/usr/bin/env python3

from __future__ import annotations

import argparse
import datetime as dt
import os
import sys
from typing import Any, Dict, List, Optional

import requests


API_ROOT = "https://api.github.com"
DEFAULT_TIMEOUT = 30


def gh_session(token: str) -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "cross-repo-ci-report",
        }
    )
    return session


def request_json(session: requests.Session, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    response = session.get(url, params=params, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response.json()


def read_repos(path: str) -> List[str]:
    repos: List[str] = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            repos.append(line)
    return repos


def get_workflow_id(session: requests.Session, repo: str, workflow_name: str) -> Optional[int]:
    url = f"{API_ROOT}/repos/{repo}/actions/workflows"
    data = request_json(session, url)
    for wf in data.get("workflows", []):
        if wf.get("name") == workflow_name:
            return wf["id"]
    return None


def get_failed_runs(
    session: requests.Session,
    repo: str,
    workflow_id: int,
    created_since: str,
) -> List[Dict[str, Any]]:
    url = f"{API_ROOT}/repos/{repo}/actions/workflows/{workflow_id}/runs"
    params = {
        "status": "completed",
        "per_page": 50,
        "created": f">={created_since}",
    }
    data = request_json(session, url, params=params)
    runs = data.get("workflow_runs", [])
    return [run for run in runs if run.get("conclusion") == "failure"]


def get_jobs_for_run(session: requests.Session, repo: str, run_id: int) -> List[Dict[str, Any]]:
    url = f"{API_ROOT}/repos/{repo}/actions/runs/{run_id}/jobs"
    data = request_json(session, url, params={"per_page": 100})
    return data.get("jobs", [])


def summarize_failed_jobs(jobs: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    summaries: List[Dict[str, str]] = []
    for job in jobs:
        if job.get("conclusion") != "failure":
            continue

        failed_steps = []
        for step in job.get("steps", []):
            if step.get("conclusion") == "failure":
                failed_steps.append(step.get("name", "Unnamed step"))

        summaries.append(
            {
                "job_name": job.get("name", "Unnamed job"),
                "failed_steps": ", ".join(failed_steps) if failed_steps else "Unknown failing step",
                "html_url": job.get("html_url", ""),
            }
        )
    return summaries


def render_report(
    workflow_name: str,
    lookback_days: int,
    results: List[Dict[str, Any]],
    errors: List[str],
) -> str:
    lines: List[str] = []
    now_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines.append(f"# Cross-Repo CI Failure Report")
    lines.append("")
    lines.append(f"- **Workflow name:** `{workflow_name}`")
    lines.append(f"- **Lookback window:** last **{lookback_days}** day(s)")
    lines.append(f"- **Generated:** {now_utc}")
    lines.append("")

    if results:
        lines.append("## Summary")
        lines.append("")
        lines.append("| Repository | Latest failed run | Branch | Failed jobs |")
        lines.append("|---|---:|---|---:|")

        for item in results:
            if item["status"] == "failed":
                lines.append(
                    f"| `{item['repo']}` | "
                    f"[#{item['run_number']}]({item['run_url']}) | "
                    f"`{item['branch']}` | "
                    f"{len(item['failed_jobs'])} |"
                )
            else:
                lines.append(
                    f"| `{item['repo']}` | {item['status_label']} | - | - |"
                )
        lines.append("")

        lines.append("## Details")
        lines.append("")
        for item in results:
            lines.append(f"### `{item['repo']}`")
            lines.append("")
            lines.append(f"- **Status:** {item['status_label']}")

            if item["status"] == "failed":
                lines.append(f"- **Run:** [#{item['run_number']}]({item['run_url']})")
                lines.append(f"- **Branch:** `{item['branch']}`")
                lines.append(f"- **Created:** `{item['created_at']}`")
                lines.append("")
                lines.append("| Failed job | Failed step(s) |")
                lines.append("|---|---|")
                for job in item["failed_jobs"]:
                    job_name = job["job_name"]
                    if job["html_url"]:
                        job_name = f"[{job_name}]({job['html_url']})"
                    lines.append(f"| {job_name} | {job['failed_steps']} |")
                lines.append("")
            else:
                lines.append("")

    if errors:
        lines.append("## Errors")
        lines.append("")
        for err in errors:
            lines.append(f"- {err}")
        lines.append("")

    if not results and not errors:
        lines.append("No repositories were processed.")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repos-file", required=True)
    parser.add_argument("--workflow-name", required=True)
    parser.add_argument("--lookback-days", type=int, default=7)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    token = os.getenv("GH_TOKEN")
    if not token:
        print("GH_TOKEN is required", file=sys.stderr)
        return 1

    repos = read_repos(args.repos_file)
    if not repos:
        print("No repositories found in repos file", file=sys.stderr)
        return 1

    created_since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=args.lookback_days)).date().isoformat()
    session = gh_session(token)

    results: List[Dict[str, Any]] = []
    errors: List[str] = []

    for repo in repos:
        try:
            workflow_id = get_workflow_id(session, repo, args.workflow_name)
            if workflow_id is None:
                results.append(
                    {
                        "repo": repo,
                        "status": "missing_workflow",
                        "status_label": f"Workflow `{args.workflow_name}` not found",
                    }
                )
                continue

            failed_runs = get_failed_runs(session, repo, workflow_id, created_since)
            if not failed_runs:
                results.append(
                    {
                        "repo": repo,
                        "status": "no_failures",
                        "status_label": "No failed runs found",
                    }
                )
                continue

            latest = failed_runs[0]
            jobs = get_jobs_for_run(session, repo, latest["id"])
            failed_jobs = summarize_failed_jobs(jobs)

            results.append(
                {
                    "repo": repo,
                    "status": "failed",
                    "status_label": "Failed runs found",
                    "run_number": latest.get("run_number", "?"),
                    "run_url": latest.get("html_url", ""),
                    "branch": latest.get("head_branch", "unknown"),
                    "created_at": latest.get("created_at", "unknown"),
                    "failed_jobs": failed_jobs,
                }
            )

        except requests.HTTPError as exc:
            status_code = exc.response.status_code if exc.response is not None else "unknown"
            errors.append(f"`{repo}`: HTTP {status_code} while querying GitHub API")
        except Exception as exc:
            errors.append(f"`{repo}`: {exc}")

    report = render_report(args.workflow_name, args.lookback_days, results, errors)

    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write(report)

    print(f"Wrote report to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

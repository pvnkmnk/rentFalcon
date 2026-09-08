#!/usr/bin/env python3
"""Close superseded agent-generated PR iterations.

Agent bots (Bolt, Palette, Sentinel, ...) iterate on the same theme again
and again, producing near-duplicate PRs. This repo previously accumulated
70+ stale iterations before a manual cleanup. This script enforces the
policy: **at most one open PR per agent theme**.

It reads the open-PR list from `gh pr list --json ...` on stdin (or runs the
query itself) and closes every PR whose branch matches an agent theme prefix
EXCEPT the newest one in that theme. Closed PRs get a comment linking the
surviving successor.

Safety rails:
  - Only branches matching a known agent theme prefix are ever touched:
    ^(bolt|palette|sentinel)[-/]  (dependabot and human branches are safe).
  - PRs carrying the `no-autoclose` label are never closed.
  - `--dry-run` (default from workflow_dispatch) only prints a plan.
"""

import argparse
import json
import re
import subprocess
import sys

AGENT_THEMES = [
    ("bolt", re.compile(r"^bolt[-/]", re.IGNORECASE)),
    ("palette", re.compile(r"^palette[-/]", re.IGNORECASE)),
    ("sentinel", re.compile(r"^sentinel[-/]", re.IGNORECASE)),
]

POLICY_COMMENT = """This PR is **superseded** by #{successor} — the same agent theme ({theme}) has a newer open iteration.

Per repo policy, superseded agent iterations are auto-closed to keep the PR queue clean (this repo previously accumulated 70+ duplicate iterations). The newer PR is the authoritative version of this work.

If this iteration contains findings the successor lost, comment here or reopen it and they'll be reconciled. To exempt a PR from auto-closing, add the `no-autoclose` label. Policy lives in `.github/workflows/supersede-agent-prs.yml`."""


def gh(*args: str, input_text: str | None = None) -> str:
    """Run `gh` and return stdout; raises on failure."""
    result = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        input=input_text,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def fetch_prs(repo: str) -> list[dict]:
    """Return all open PRs of the repo as a list of dicts."""
    out = gh(
        "pr", "list", "-R", repo, "--state", "open", "--limit", "200",
        "--json", "number,title,headRefName,createdAt,labels",
    )
    return json.loads(out)


def classify(pr: dict) -> str | None:
    """Return the agent theme key for a PR, or None if it isn't agent-iteration."""
    head = pr.get("headRefName") or ""
    for theme, pattern in AGENT_THEMES:
        if pattern.match(head):
            return theme
    return None


def is_exempt(pr: dict) -> bool:
    return any(label.get("name") == "no-autoclose" for label in pr.get("labels", []))


def plan_open_groups(repo: str) -> dict[str, list[dict]]:
    """Group open agent PRs by theme, oldest first, skipping exempt ones."""
    groups: dict[str, list[dict]] = {}
    for pr in fetch_prs(repo):
        theme = classify(pr)
        if theme is None or is_exempt(pr):
            continue
        groups.setdefault(theme, []).append(pr)
    for items in groups.values():
        items.sort(key=lambda p: p["createdAt"])
    return groups


def close_superseded(repo: str, dry_run: bool) -> int:
    closed = 0
    for theme, items in plan_open_groups(repo).items():
        if len(items) <= 1:
            continue
        newest = items[-1]
        for old in items[:-1]:
            body = POLICY_COMMENT.format(successor=newest["number"], theme=theme)
            if dry_run:
                print(f"[dry-run] would close #{old['number']} ({old['title'][:60]!r}) -> successor #{newest['number']}")
                continue
            gh("pr", "close", str(old["number"]), "-R", repo, "--comment", body)
            print(f"closed #{old['number']} ({old['title'][:60]!r}) as superseded by #{newest['number']}")
            closed += 1
    return closed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="owner/name of the repository")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="only print what would be closed (no changes)",
    )
    args = parser.parse_args()

    n = close_superseded(args.repo, dry_run=args.dry_run)
    print(f"{'would close' if args.dry_run else 'closed'} {n} superseded PR(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
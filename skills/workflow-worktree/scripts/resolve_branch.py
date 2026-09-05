#!/usr/bin/env python3
"""Resolve a Git branch and base without creating branches or worktrees."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata


class ResolutionError(ValueError):
    pass


def git(project: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(project), *args], capture_output=True, text=True, check=False)


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not value:
        raise ResolutionError("slug must contain an ASCII letter or digit; use --branch for an exact name")
    return value


def validate_branch(project: Path, branch: str) -> None:
    if branch == "HEAD" or branch.startswith("-") or git(project, "check-ref-format", f"refs/heads/{branch}").returncode:
        raise ResolutionError(f"invalid Git branch name: {branch!r}")


def commit_for(project: Path, revision: str) -> str | None:
    result = git(project, "rev-parse", "--verify", "--quiet", "--end-of-options", f"{revision}^{{commit}}")
    return result.stdout.strip() if result.returncode == 0 else None


def resolve_base(project: Path, explicit: str | None) -> tuple[str, str]:
    if explicit is not None:
        commit = commit_for(project, explicit)
        if not commit:
            raise ResolutionError(f"base does not resolve to a commit: {explicit!r}")
        return explicit, commit
    candidates = [git(project, "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD").stdout.strip(),
                  git(project, "symbolic-ref", "--quiet", "--short", "HEAD").stdout.strip(), "HEAD"]
    for base in candidates:
        if base and (commit := commit_for(project, base)):
            return base, commit
    raise ResolutionError("no base commit exists; provide a repository with a commit")


def resolve(args: argparse.Namespace) -> dict[str, object]:
    project = Path(args.project).expanduser().resolve()
    if git(project, "rev-parse", "--show-toplevel").returncode:
        raise ResolutionError(f"not a Git checkout: {project}")
    if args.branch is not None and (args.prefix is not None or args.type is not None):
        raise ResolutionError("--branch cannot be combined with --prefix or --type")
    prefix = args.prefix if args.prefix is not None else args.type or ""
    branch = args.branch if args.branch is not None else "/".join(part for part in (prefix.rstrip("/"), slugify(args.slug)) if part)
    validate_branch(project, branch)
    base, commit = resolve_base(project, args.base)
    refs_result = git(project, "for-each-ref", "--format=%(refname:strip=2)", "refs/heads/")
    if refs_result.returncode:
        raise ResolutionError(refs_result.stderr.strip() or "could not inspect local branches")
    refs = refs_result.stdout.splitlines()
    conflicts = [ref for ref in refs if ref == branch or ref.startswith(branch + "/") or branch.startswith(ref + "/")]
    if args.require_available and conflicts:
        raise ResolutionError(f"branch {branch!r} conflicts with existing refs: {', '.join(conflicts)}")
    worktrees = git(project, "worktree", "list", "--porcelain", "-z")
    if worktrees.returncode:
        raise ResolutionError(worktrees.stderr.strip() or "could not inspect worktrees")
    checkouts = []
    record = {}
    for field in worktrees.stdout.split("\0"):
        if not field:
            if record.get("branch") == f"refs/heads/{branch}":
                checkouts.append(record.get("worktree", ""))
            record = {}
        else:
            key, _, value = field.partition(" ")
            record[key] = value
    return {"branch": branch, "base": base, "base_commit": commit,
            "branch_exists": branch in refs, "ref_conflicts": conflicts, "checkouts": checkouts}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=".")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--branch", help="Exact branch name, unchanged")
    source.add_argument("--slug", help="Task description normalized to kebab-case")
    parser.add_argument("--prefix", help="Host or project prefix, for example codex")
    parser.add_argument("--type", help="Optional convenience prefix when --prefix is omitted")
    parser.add_argument("--base", help="Base commit, tag, branch, or revision expression")
    parser.add_argument("--require-available", action="store_true")
    try:
        print(json.dumps(resolve(parser.parse_args()), indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError) as error:
        print(json.dumps({"ok": False, "errors": [str(error)]}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

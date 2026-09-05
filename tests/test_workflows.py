from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def run(skill: str, script: str, *args: str | Path, stdin: str | None = None, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SKILLS / skill / "scripts" / script), *map(str, args)],
                          input=stdin, text=True, capture_output=True, check=False, cwd=cwd)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True, check=True)
    return result.stdout.strip()


def prepare_git(root: Path) -> None:
    subprocess.run(["git", "init", "-q", "-b", "trunk", str(root)], check=True)
    git(root, "config", "user.name", "Test")
    git(root, "config", "user.email", "test@example.com")
    git(root, "config", "commit.gpgsign", "false")
    git(root, "config", "core.hooksPath", str(root / "absent-hooks"))
    (root / "README.md").write_text("# Test\n", encoding="utf-8")
    git(root, "add", "README.md")
    git(root, "commit", "-q", "-m", "test: seed")


class PackageTests(unittest.TestCase):
    def test_manifests_and_skill_inventory_align(self) -> None:
        names = sorted(path.name for path in SKILLS.iterdir() if (path / "SKILL.md").is_file())
        self.assertEqual(len(names), 6)
        codex = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        discovery = json.loads((ROOT / "skills.sh.json").read_text())
        self.assertEqual(codex["version"], claude["version"])
        self.assertEqual(codex["name"], "workflows")
        self.assertEqual(sorted(Path(item).name for item in claude["skills"]), names)
        self.assertEqual(sorted(discovery["groupings"][0]["skills"]), names)
        self.assertEqual(codex["author"]["name"], "Henrique Krause")

    def test_distribution_copies_stay_aligned(self) -> None:
        for relative in ("scripts/validate_conventional.py", "references/harness-integration.md"):
            self.assertEqual((SKILLS / "workflow-commit" / relative).read_bytes(),
                             (SKILLS / "workflow-pr" / relative).read_bytes())

    def test_every_skill_runs_when_copied_alone(self) -> None:
        cases = {
            "workflow-commit": ("validate_conventional.py", ["--message", "fix: handle expiry"]),
            "workflow-pr": ("render_pr.py", ["--title", "fix: handle expiry", "--summary", "Reject expired entries."]),
            "workflow-review": ("validate_review.py", ["--format", "json"]),
            "workflow-docs": ("init_docs.py", [".", "--dry-run"]),
            "workflow-artifact": ("create_artifact.py", ["report.html", "--title", "Flow", "--summary", "A flow"]),
            "workflow-worktree": ("resolve_branch.py", ["--slug", "test checkout"]),
        }
        for name, (script, args) in cases.items():
            with self.subTest(skill=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                installed = root / "installed"
                shutil.copytree(SKILLS / name, installed)
                workspace = root / "workspace"
                workspace.mkdir()
                if name == "workflow-worktree":
                    prepare_git(workspace)
                result = subprocess.run([sys.executable, str(installed / "scripts" / script), *args],
                                        cwd=workspace, input="[]", capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                for helper in (installed / "scripts").glob("*.py"):
                    help_result = subprocess.run([sys.executable, str(helper), "--help"],
                                                 cwd=workspace, capture_output=True, text=True)
                    self.assertEqual(help_result.returncode, 0, help_result.stderr)


class WorktreeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "repo"
        prepare_git(self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def resolve(self, *args: str) -> subprocess.CompletedProcess[str]:
        return run("workflow-worktree", "resolve_branch.py", "--project", self.root, *args)

    def test_host_prefix_and_base_are_read_only(self) -> None:
        before = {str(path.relative_to(self.root)): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        result = self.resolve("--prefix", "codex", "--slug", "Repair Cache Expiry", "--require-available")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["branch"], "codex/repair-cache-expiry")
        self.assertEqual(payload["base"], "trunk")
        self.assertEqual(payload["base_commit"], git(self.root, "rev-parse", "HEAD"))
        after = {str(path.relative_to(self.root)): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(before, after)

    def test_exact_unicode_branch_and_commit_base(self) -> None:
        result = self.resolve("--branch", "team/área", "--base", "HEAD^{commit}")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["branch"], "team/área")

    def test_ref_collisions_and_existing_checkout_reported(self) -> None:
        git(self.root, "branch", "codex/task")
        result = self.resolve("--branch", "codex/task/fix", "--require-available")
        self.assertEqual(result.returncode, 2)
        self.assertIn("codex/task", result.stderr)
        result = self.resolve("--branch", "trunk")
        self.assertEqual(json.loads(result.stdout)["checkouts"], [str(self.root.resolve())])

    def test_invalid_base_and_branch_fail_cleanly(self) -> None:
        for args in (("--branch", "codex/bad..name"), ("--branch", "codex/valid", "--base", "missing"),
                     ("--branch", "codex/name", "--prefix", "other"), ("--branch", "HEAD")):
            with self.subTest(args=args):
                result = self.resolve(*args)
                self.assertEqual(result.returncode, 2)
                self.assertFalse(json.loads(result.stderr)["ok"])

    def test_explicit_prefix_overrides_type_without_enforcing_semantics(self) -> None:
        result = self.resolve("--type", "fix", "--prefix", "claude", "--slug", "cache")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["branch"], "claude/cache")

    def test_detached_head_fallback(self) -> None:
        git(self.root, "checkout", "--detach", "-q")
        result = self.resolve("--slug", "task")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["base"], "HEAD")


class CommitTests(unittest.TestCase):
    def validate(self, message: str, *args: str) -> subprocess.CompletedProcess[str]:
        return run("workflow-commit", "validate_conventional.py", "--message", message, "--format", "json", *args)

    def test_breaking_change_and_host_branch(self) -> None:
        result = self.validate("feat(api)!: replace authentication\n\nBREAKING CHANGE: use a refresh token.", "--branch", "codex/auth")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["ok"])

    def test_custom_type_unicode_and_long_header_are_advisory(self) -> None:
        result = self.validate("release: document Café settings " + "a" * 90, "--branch", "custom/branch")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["errors"])
        self.assertTrue(payload["warnings"])

    def test_strict_style_is_opt_in(self) -> None:
        result = self.validate("Fix: correct behavior.", "--strict-style")
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)["errors"])

    def test_structural_errors_and_invalid_git_branch(self) -> None:
        for message, args in (("fix: thing\nBody without separator", []), ("Fix the thing", []),
                              ("fix: thing", ["--branch", "bad..branch"]), ("fix: thing", ["--branch", "HEAD"])):
            with self.subTest(message=message, args=args):
                result = self.validate(message, *args)
                self.assertEqual(result.returncode, 1)
                self.assertTrue(json.loads(result.stdout)["errors"])


class PullRequestTests(unittest.TestCase):
    def render(self, *args: str | Path) -> subprocess.CompletedProcess[str]:
        return run("workflow-pr", "render_pr.py", "--format", "json", *args)

    def test_independent_branch_type_and_optional_sections(self) -> None:
        result = self.render("--title", "fix: reject expired entries", "--branch", "docs/cache", "--summary", "Expired entries are rejected.",
                             "--verification", "Passed regression tests.")
        self.assertEqual(result.returncode, 0, result.stderr)
        body = json.loads(result.stdout)["body"]
        self.assertIn("Passed regression tests.", body)
        self.assertNotIn("## Risks", body)

    def test_preserves_existing_template_exactly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            body = Path(directory) / "body.md"
            expected = "### Why\n\nNeed this.\n\n### Checklist\n\n- [x] Tests passed\n\n"
            body.write_text(expected)
            result = self.render("--title", "fix: correct expiry", "--body-file", body)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["body"], expected)

    def test_explicit_custom_title_allowed(self) -> None:
        result = self.render("--title", "Documentação de acesso", "--allow-nonconventional-title", "--summary", "Updated guide.")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["title"], "Documentação de acesso")

    def test_invalid_structured_item_fails_without_truncation(self) -> None:
        bad = self.render("--title", "docs: route guides", "--summary", "A guide.", "--change", "Missing target")
        self.assertEqual(bad.returncode, 1)
        summary = "Summary " + "x" * 10000
        good = self.render("--title", "docs: route guides", "--summary", summary)
        self.assertEqual(good.returncode, 0)
        self.assertIn(summary, json.loads(good.stdout)["body"])

    def test_template_and_generated_flags_do_not_silently_mix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            body = Path(directory) / "body.md"
            body.write_text("Body")
            result = self.render("--title", "fix: thing", "--body-file", body, "--risk", "A risk")
            self.assertEqual(result.returncode, 1)


class ReviewTests(unittest.TestCase):
    def finding(self) -> dict[str, object]:
        return {"priority": "P2", "title": "Handle empty token", "file": "src/auth.py", "start": 42,
                "evidence": "Empty input reaches decode without a guard.", "impact": "The request fails with an exception.",
                "direction": "Reject empty input before decode."}

    def test_empty_and_evidence_backed_reviews_are_valid(self) -> None:
        for payload in ([], {"findings": [self.finding()]}):
            result = run("workflow-review", "validate_review.py", "--format", "json", stdin=json.dumps(payload))
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_bad_priority_boolean_lines_and_missing_evidence_rejected(self) -> None:
        finding = self.finding()
        finding.update(priority=[], start=True)
        del finding["evidence"]
        result = run("workflow-review", "validate_review.py", "--format", "json", stdin=json.dumps([finding]))
        self.assertEqual(result.returncode, 1)
        self.assertGreaterEqual(len(json.loads(result.stdout)["errors"]), 3)

    def test_invalid_json_is_input_error(self) -> None:
        result = run("workflow-review", "validate_review.py", stdin="{")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)


class DocsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "project"
        self.root.mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def init(self, *args: str) -> subprocess.CompletedProcess[str]:
        return run("workflow-docs", "init_docs.py", self.root, *args)

    def check(self, *args: str) -> subprocess.CompletedProcess[str]:
        return run("workflow-docs", "check_docs.py", self.root, "--format", "json", *args)

    def test_create_only_selected_paths_preserve_and_repeat(self) -> None:
        (self.root / "README.md").write_text("# Existing\n")
        args = ["--file", "README.md", "--file", "documentation/setup.md"]
        first, second = self.init(*args), self.init(*args)
        self.assertEqual(first.returncode, 0)
        self.assertEqual(json.loads(first.stdout)["created"], ["documentation/setup.md"])
        self.assertEqual(json.loads(second.stdout)["created"], [])
        self.assertEqual((self.root / "README.md").read_text(), "# Existing\n")
        self.assertFalse((self.root / "docs").exists())

    def test_preflight_rejects_escape_and_symlink_without_partial_writes(self) -> None:
        (self.root / "outside").symlink_to(self.root.parent, target_is_directory=True)
        for invalid in ("../escape.md", "outside/escape.md"):
            result = self.init("--file", "good.md", "--file", invalid)
            self.assertEqual(result.returncode, 2)
            self.assertFalse((self.root / "good.md").exists())
        self.assertFalse((self.root.parent / "escape.md").exists())

    def test_dry_run_does_not_create_documents(self) -> None:
        result = self.init("--file", "documentation/setup.md", "--dry-run")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["planned"], ["documentation/setup.md"])
        self.assertEqual(list(self.root.iterdir()), [])

    def test_existing_custom_layout_needs_no_baseline(self) -> None:
        folder = self.root / "manual"
        folder.mkdir()
        (folder / "guide.md").write_text("# Guide\n")
        result = self.check("--path", "manual")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)["issues"])
        self.assertFalse((self.root / "docs").exists())

    def test_local_links_images_references_code_and_encoded_paths(self) -> None:
        (self.root / "Target File.md").write_text("# Target\n")
        (self.root / "README.md").write_text('''# Guide
[Valid](Target%20File.md#heading)
[Angle](<Target File.md>)
[Ref][target]
[target]: Target%20File.md
![Missing image](missing.png)
[Unknown][missing]
`[Ignored](missing-code.md)`
```markdown
[Ignored](missing-fence.md)
```
''')
        result = self.check()
        self.assertEqual(result.returncode, 1)
        issues = json.loads(result.stdout)["issues"]
        self.assertEqual(len(issues), 2, issues)
        self.assertTrue(any("missing.png" in issue for issue in issues))
        self.assertTrue(any("undefined link reference" in issue for issue in issues))

    def test_size_threshold_only_when_requested_and_advisory(self) -> None:
        (self.root / "README.md").write_text("line\n" * 250)
        self.assertEqual(self.check().returncode, 0)
        result = self.check("--line-limit", "100")
        self.assertEqual(result.returncode, 0)
        self.assertTrue(json.loads(result.stdout)["warnings"])
        self.assertEqual(self.check("--line-limit", "100", "--strict").returncode, 1)

    def test_explicit_required_path_and_invalid_scope(self) -> None:
        result = self.check("--require", "manual/guide.md")
        self.assertEqual(result.returncode, 1)
        self.assertTrue(json.loads(result.stdout)["issues"])
        self.assertEqual(self.check("--path", "..").returncode, 2)


class ArtifactTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.target = self.root / "reports" / "Flow report.html"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def create(self, *args: str) -> subprocess.CompletedProcess[str]:
        return run("workflow-artifact", "create_artifact.py", self.target, "--title", "Flow & stages", "--summary", "Understand <the flow>", *args)

    def check(self, *args: str | Path) -> subprocess.CompletedProcess[str]:
        return run("workflow-artifact", "check_artifacts.py", self.target, "--format", "json", *args)

    def test_explicit_destination_idempotence_and_no_catalog_requirement(self) -> None:
        result = self.create()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "created")
        self.assertEqual(self.check().returncode, 0)
        self.assertEqual(json.loads(self.create().stdout)["status"], "unchanged")
        self.assertFalse((self.root / "docs").exists())
        self.assertIn("&lt;the flow&gt;", self.target.read_text())

    def test_existing_content_protected_and_replacement_explicit(self) -> None:
        self.create()
        self.target.write_text("User content")
        self.assertEqual(self.create().returncode, 2)
        self.assertEqual(self.target.read_text(), "User content")
        self.assertEqual(json.loads(self.create("--replace").stdout)["status"], "replaced")
        self.assertFalse(list(self.target.parent.glob(".*.tmp")))

    def test_symlink_output_never_overwrites_target(self) -> None:
        self.target.parent.mkdir()
        real = self.root / "original.html"
        real.write_text("Original")
        self.target.symlink_to(real)
        self.assertEqual(self.create("--replace").returncode, 2)
        self.assertEqual(real.read_text(), "Original")

    def test_language_and_embedded_assets_are_accepted(self) -> None:
        self.assertEqual(self.create("--lang", "pt-BR").returncode, 0)
        text = self.target.read_text().replace("</main>", '<img src="data:image/png;base64,AA==" alt=""><svg><use href="#shape"/></svg></main>')
        self.target.write_text(text)
        self.assertEqual(self.check().returncode, 0)

    def test_html_css_module_network_and_svg_dependencies_detected(self) -> None:
        additions = [
            '<script src="app.js"></script>',
            '<style>@import "theme.css"; .x { background: url(icon.svg) }</style>',
            '<div style="background:url(https://example.org/icon.svg)"></div>',
            '<script>fetch("/api")</script>',
            '<script type="module">import { x } from "./module.js";</script>',
            '<svg><image href="photo.png" /></svg>',
            '<img srcset="first.png 1x, second.png 2x" alt="">',
            '<video poster="poster.jpg"></video>',
        ]
        self.create()
        baseline = self.target.read_text()
        for addition in additions:
            with self.subTest(addition=addition):
                self.target.write_text(baseline.replace("</main>", addition + "</main>"))
                result = self.check()
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertTrue(json.loads(result.stdout)["issues"])

    def test_structure_and_image_alt_checked(self) -> None:
        self.target.parent.mkdir()
        self.target.write_text('<html><head><title></title></head><body><img src="data:image/png;base64,AA=="></body></html>')
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertGreaterEqual(len(json.loads(result.stdout)["issues"]), 6)

    def test_optional_catalog_requires_a_real_link(self) -> None:
        self.create()
        index = self.root / "index.md"
        index.write_text("Flow report.html is mentioned but not linked.\n")
        self.assertEqual(self.check("--index", index).returncode, 1)
        index.write_text("[Flow](reports/Flow%20report.html)\n")
        self.assertEqual(self.check("--index", index).returncode, 0)


if __name__ == "__main__":
    unittest.main()

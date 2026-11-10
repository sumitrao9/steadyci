"""SEO landing page generator (problem-first). Produces static Markdown/HTML-ready content.

These pages target real developer problems and funnel to the free scanner.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Page:
    slug: str
    title: str
    problem: str
    fix: str
    cta: str = "Run `steadyci scan .github/workflows` to check your repo."


PAGES = [
    Page(
        "pin-github-actions-to-sha",
        "Pin GitHub Actions to a commit SHA",
        "Tags like `@v4` can be moved by a maintainer. The tj-actions/Trivy incident (Mar 2026) showed how a compromised tag can run attacker code in your CI.",
        "Replace `uses: owner/repo@v4` with `uses: owner/repo@<full-commit-sha>` and keep the version as a comment. Update via Dependabot/Renovate.",
    ),
    Page(
        "github-actions-least-privilege-permissions",
        "GitHub Actions permissions: least privilege",
        "Without explicit `permissions:`, workflows may inherit broad token access. 250k+ misconfigurations were found in starred repos (Kaspersky, Jun 2026).",
        "Set top-level `permissions: contents: read` (or `{}`) and grant only what each job needs.",
    ),
    Page(
        "fix-deprecated-ubuntu-runner",
        "Fix deprecated GitHub Actions runners (ubuntu-20.04)",
        "Deprecated runners (ubuntu-20.04, macOS-11/12) are removed on a schedule and cause CI to fail without warning.",
        "Migrate to supported runners like `ubuntu-24.04` or `ubuntu-latest` and test your workflow.",
    ),
    Page(
        "prevent-script-injection-github-actions",
        "Prevent script injection in GitHub Actions",
        "Interpolating untrusted event data (PR titles, issue bodies) into `run:` via `${{ }}` lets attackers inject shell commands.",
        "Pass untrusted values through `env:` and reference them as quoted shell variables (`\"$VAR\"`).",
    ),
    Page(
        "github-actions-supply-chain-security",
        "GitHub Actions supply chain security checklist",
        "CI pipelines execute third-party code with repo credentials. Unpinned, unverified, or abandoned actions expand your attack surface.",
        "Pin by SHA, restrict permissions, audit untrusted triggers, remove abandoned actions, and monitor with SteadyCI.",
    ),
]


def render_markdown(page: Page) -> str:
    return f"""# {page.title}

## The problem
{page.problem}

## The fix
{page.fix}

## Check your repo
{page.cta}

---
*SteadyCI is an open-source GitHub Actions health scanner. MIT licensed.*
"""


def write_pages(out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for p in PAGES:
        path = out_dir / f"{p.slug}.md"
        path.write_text(render_markdown(p), encoding="utf-8")
        written.append(path)
    return written


if __name__ == "__main__":
    here = Path(__file__).resolve().parents[2] / "docs" / "landing"
    for path in write_pages(here):
        print(path)

"""Builds assets/languages.svg: language mix across my public, non-fork repositories.

Runs daily in GitHub Actions (see .github/workflows/update-stats.yml).
Notebook bytes are excluded because embedded images make them dwarf real code.

Local use:  python scripts/update_languages.py --repos owner/a owner/b
"""
import argparse
import json
import os
import subprocess
import urllib.request
from pathlib import Path

USER = "vrushabh05"
SKIP_REPO = f"{USER}/{USER}"
SKIP_LANG = {"Jupyter Notebook"}
ROOT = Path(__file__).resolve().parent.parent

# Categorical order is fixed, never cycled; anything beyond 6 is folded into "Other".
COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#6250d6"]
OTHER = "#8a8984"


def api(path):
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req = urllib.request.Request(
            f"https://api.github.com/{path}",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    out = subprocess.run(["gh", "api", path], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def list_repos():
    repos, page = [], 1
    while True:
        batch = api(f"users/{USER}/repos?per_page=100&page={page}&type=owner")
        repos += [r["full_name"] for r in batch if not r["fork"] and not r["private"]]
        if len(batch) < 100:
            return repos
        page += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repos", nargs="*")
    args = ap.parse_args()
    repos = [r for r in (args.repos or list_repos()) if r.lower() != SKIP_REPO.lower()]
    totals = {}
    for repo in repos:
        for lang, n in api(f"repos/{repo}/languages").items():
            if lang not in SKIP_LANG:
                totals[lang] = totals.get(lang, 0) + n
    ranked = sorted(totals.items(), key=lambda kv: -kv[1])
    top, rest = ranked[:6], ranked[6:]
    if rest:
        top.append(("Other", sum(n for _, n in rest)))
    total = sum(n for _, n in top) or 1

    W, X0, BAR_W = 640, 24, 592
    rows, x = [], X0
    for i, (lang, n) in enumerate(top):
        w = max(BAR_W * n / total, 2)
        color = OTHER if lang == "Other" else COLORS[i]
        rows.append(f'<rect x="{x:.1f}" y="52" width="{w:.1f}" height="22" fill="{color}" stroke="var(--bg)" stroke-width="2"/>')
        x += w
    legend = []
    for i, (lang, n) in enumerate(top):
        color = OTHER if lang == "Other" else COLORS[i]
        cx, cy = X0 + (i % 2) * 300, 104 + (i // 2) * 24
        legend.append(f'<circle cx="{cx + 6}" cy="{cy - 4}" r="5" fill="{color}"/>'
                      f'<text x="{cx + 18}" y="{cy}" class="t">{lang}</text>'
                      f'<text x="{cx + 270}" y="{cy}" class="t m" text-anchor="end">{100 * n / total:.1f}%</text>')
    height = 104 + ((len(top) + 1) // 2) * 24 + 12
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="Language mix across public repositories">
<style>
:root{{--bg:#fcfcfb;--ink:#0b0b0b;--muted:#52514e}}
@media (prefers-color-scheme: dark){{:root{{--bg:#1a1a19;--ink:#f0efec;--muted:#c3c2b7}}}}
.t{{font:13px -apple-system,Segoe UI,Helvetica,Arial,sans-serif;fill:var(--ink)}}
.m{{fill:var(--muted)}}.h{{font:600 15px -apple-system,Segoe UI,Helvetica,Arial,sans-serif;fill:var(--ink)}}
</style>
<rect width="{W}" height="{height}" rx="10" fill="var(--bg)"/>
<text x="{X0}" y="30" class="h">Language mix across my public repositories</text>
{''.join(rows)}
{''.join(legend)}
</svg>
'''
    out = ROOT / "assets" / "languages.svg"
    out.parent.mkdir(exist_ok=True)
    out.write_text(svg, encoding="utf-8")
    print("wrote", out, "from", len(repos), "repos:", [(l, n) for l, n in top])


if __name__ == "__main__":
    main()

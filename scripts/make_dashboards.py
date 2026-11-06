"""Generate the static SVG dashboards used by the profile README (assets/*.svg).

Every number here is copied from a result file or README in the linked repository.
Run: python scripts/make_dashboards.py
"""
from html import escape

FONT = "-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
HEAD = """<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">
<title>{label}</title>
<style>
:root{{--bg:#fcfcfb;--card:#f3f2ef;--ink:#0b0b0b;--muted:#52514e;--line:#d8d6d0}}
@media (prefers-color-scheme: dark){{:root{{--bg:#1a1a19;--card:#262624;--ink:#f0efec;--muted:#c3c2b7;--line:#3b3a37}}}}
text{{font-family:{font};fill:var(--ink)}}
.h{{font-size:16px;font-weight:600}}.s{{font-size:12px;fill:var(--muted)}}
.big{{font-size:30px;font-weight:700}}.l{{font-size:12.5px}}.r{{font-size:11px;fill:var(--muted)}}
</style>
<rect width="{w}" height="{h}" rx="12" fill="var(--bg)"/>
"""
BLUE, ORANGE, GREEN, AMBER, PINK, PURPLE = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#6250d6"


def svg(w, h, label, body):
    return HEAD.format(w=w, h=h, label=escape(label), font=FONT) + body + "</svg>\n"


def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > n and cur:
            lines.append(cur); cur = wd
        else:
            cur = (cur + " " + wd).strip()
    return lines + [cur]


# ---------------------------------------------------------------- KPI tiles
TILES = [  # repo names below are shortened labels only
    ("98.84%", "LeNet-5 test accuracy on MNIST", "mnist-lenet5-and-naive-bayes", BLUE),
    ("3.71x", "HiFi-GAN on the Mobilint NPU vs CPU (single frame)", "emotional-tts-mobilint-npu", ORANGE),
    ("18.3x", "DenoiseSRNet NPU vs CPU speed-up", "super-resolution-npu-labs", ORANGE),
    ("81.4%", "Fine-tuned DistilBERT, 4-class tweet emotion (zero-shot 52.4%)", "tweet-emotion-transformers", GREEN),
    ("0.89 > 0.97", "RAG context recall with cross-encoder reranking", "llm-prompting-and-rag-wixqa", GREEN),
    ("0.616 > 0.746", "CLIP Recall@1 after partial fine-tuning (Flickr30k)", "clip-blip-multimodal-flickr30k", PURPLE),
    ("402 vs 5,046", "Test perplexity: neural vs count trigram LM", "tweet-emotion-transformers", GREEN),
    ("0.141 vs 0.138", "Bloom filter false-positive rate, measured vs theory", "bloom-filter-hash-quality", AMBER),
]


def kpi():
    W, H, cols = 880, 292, 4
    cw, ch, gx, gy, x0, y0 = 200, 106, 12, 12, 24, 58
    b = ['<text x="24" y="30" class="h">Measured results across my repositories</text>',
         '<text x="24" y="47" class="s">Every figure is reproduced in the linked repository README, with its caveats</text>']
    for i, (big, lab, repo, col) in enumerate(TILES):
        x = x0 + (i % cols) * (cw + gx); y = y0 + (i // cols) * (ch + gy)
        b.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="9" fill="var(--card)"/>')
        b.append(f'<rect x="{x}" y="{y+14}" width="4" height="{ch-28}" rx="2" fill="{col}"/>')
        size = 30 if len(big) <= 7 else 22
        b.append(f'<text x="{x+16}" y="{y+36}" class="big" style="font-size:{size}px">{escape(big)}</text>')
        for j, ln in enumerate(wrap(lab, 27)[:3]):
            b.append(f'<text x="{x+16}" y="{y+56+j*15}" class="l">{escape(ln)}</text>')
        b.append(f'<text x="{x+16}" y="{y+ch-10}" class="r" style="font-size:10px">{escape(repo)}</text>')
    return svg(W, H, "Measured results across my repositories", "\n".join(b))


# ---------------------------------------------------------- coverage matrix
ROLES = [("AI", "Engineering"), ("ML", "Engineering"), ("Data", "Science"), ("Data", "Analytics"), ("Forward", "Deployed")]
ROWS = [  # (project, [AI, ML, DS, DA, FDE]) 2 = main focus, 1 = supporting
    ("MetaTravelGrid (team): microservices, Kafka, EKS", [0, 0, 0, 1, 2]),
    ("Airbnb-style distributed system (Lab 1)", [1, 0, 0, 0, 2]),
    ("Persona RAG + QLoRA (team, in progress)", [2, 2, 1, 0, 1]),
    ("LLM prompting and WixQA RAG", [2, 0, 1, 0, 0]),
    ("NLQuery: text-to-SQL (team)", [2, 0, 0, 1, 0]),
    ("Gemma-2B instruction tuning (QLoRA)", [2, 1, 0, 0, 0]),
    ("MealPilot MCP server", [2, 0, 0, 0, 1]),
    ("Tweet emotion and language models", [1, 2, 1, 0, 0]),
    ("CLIP and BLIP on Flickr30k", [1, 2, 0, 0, 0]),
    ("Emotional TTS, super-resolution, ImageNet-20 (NPU)", [0, 2, 0, 0, 1]),
    ("AlexNet, LeNet-5, Naive Bayes", [0, 2, 1, 0, 0]),
    ("Airline satisfaction, wildfire forecasting", [0, 1, 2, 0, 0]),
    ("ML fundamentals, statistics, PySpark, Bloom filter", [0, 0, 2, 0, 0]),
    ("Power BI and Superstore EDA dashboards", [0, 0, 1, 2, 0]),
]
ROLE_COL = [BLUE, ORANGE, GREEN, AMBER, PURPLE]


def coverage():
    W, rh, y0, lx = 880, 26, 92, 24
    H = y0 + rh * len(ROWS) + 34
    cx0, cw = 450, 94
    b = ['<text x="24" y="30" class="h">Where each project covers my target roles</text>',
         '<text x="24" y="47" class="s">Filled dot = main focus. Ring = supporting skill.</text>']
    for k, r in enumerate(ROLES):
        b.append(f'<text x="{cx0+k*cw}" y="{y0-32}" class="l" text-anchor="middle" font-weight="600">{escape(r[0])}</text>')
        b.append(f'<text x="{cx0+k*cw}" y="{y0-18}" class="l" text-anchor="middle" font-weight="600">{escape(r[1])}</text>')
    for i, (name, vals) in enumerate(ROWS):
        y = y0 + i * rh
        if i % 2 == 0:
            b.append(f'<rect x="12" y="{y-rh/2-4}" width="{W-24}" height="{rh}" rx="6" fill="var(--card)"/>')
        b.append(f'<text x="{lx}" y="{y+1}" class="l">{escape(name)}</text>')
        for k, v in enumerate(vals):
            cx = cx0 + k * cw
            if v == 2:
                b.append(f'<circle cx="{cx}" cy="{y-4}" r="7" fill="{ROLE_COL[k]}"/>')
            elif v == 1:
                b.append(f'<circle cx="{cx}" cy="{y-4}" r="6" fill="none" stroke="{ROLE_COL[k]}" stroke-width="2"/>')
    tot = [sum(1 for r in ROWS if r[1][k] == 2) for k in range(5)]
    ty = y0 + rh * len(ROWS) + 4
    b.append(f'<text x="{lx}" y="{ty}" class="s">Projects with this as the main focus</text>')
    for k, t in enumerate(tot):
        b.append(f'<text x="{cx0+k*cw}" y="{ty}" class="l" text-anchor="middle" font-weight="700">{t}</text>')
    return svg(W, H, "Role coverage matrix: projects against target roles", "\n".join(b))


# ----------------------------------------------------- MetaTravelGrid benchmark
SCEN = [("A  Base", 342.88, 2169), ("B  + Redis cache", 324.41, 2372), ("C  + Kafka", 347.87, 2064), ("D  + gzip (full)", 363.44, 1765)]


def bench():
    W, H = 880, 290
    b = ['<text x="24" y="30" class="h">MetaTravelGrid load test: what each optimisation did</text>',
         '<text x="24" y="47" class="s">400 concurrent users, 12,000 requests per scenario, 0% errors. Source: the repo\'s own performance_report.md</text>']
    # left: throughput
    b.append('<text x="24" y="78" class="l" font-weight="600">Throughput (requests per second, higher is better)</text>')
    bx, bw, base = 24, 190, 0
    for i, (n, t, _) in enumerate(SCEN):
        y = 92 + i * 38
        w = (t / 400) * 330
        col = ORANGE if i == 1 else BLUE
        b.append(f'<text x="{bx}" y="{y+15}" class="l">{escape(n)}</text>')
        b.append(f'<rect x="{bx+130}" y="{y}" width="{w:.1f}" height="22" rx="3" fill="{col}"/>')
        b.append(f'<text x="{bx+130+w+8:.1f}" y="{y+16}" class="l" font-weight="600">{t:.1f}</text>')
    # right: p95
    b.append('<text x="560" y="78" class="l" font-weight="600">P95 latency (ms, lower is better)</text>')
    for i, (n, _, p) in enumerate(SCEN):
        y = 92 + i * 38
        w = (p / 2600) * 200
        col = ORANGE if i == 1 else GREEN
        b.append(f'<text x="560" y="{y+15}" class="l">{n.split("  ")[0]}</text>')
        b.append(f'<rect x="582" y="{y}" width="{w:.1f}" height="22" rx="3" fill="{col}"/>')
        b.append(f'<text x="{582+w+8:.1f}" y="{y+16}" class="l" font-weight="600">{p:,}</text>')
    b.append('<text x="24" y="258" class="s">Redis alone cost 5.4% throughput on these simple indexed queries; the full stack gained 6.0% in throughput.</text>')
    b.append('<text x="24" y="276" class="s">The team\'s report also records 503 errors from the hotel service at 1,000 users.</text>')
    return svg(W, H, "MetaTravelGrid load test results by optimisation scenario", "\n".join(b))


if __name__ == "__main__":
    for name, fn in (("kpi", kpi), ("coverage", coverage), ("benchmark", bench)):
        open(f"assets/{name}.svg", "w", encoding="utf-8").write(fn())
        print("wrote assets/%s.svg" % name)

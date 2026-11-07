"""Builds assets/skills.svg (skill evidence chart) and prints the README skills markdown.

Counts are the number of my own repositories (27 scanned) whose code, notebook code cells or
config import or use the tool. They come from a scan of the repositories, not from self-rating.
Run: python scripts/make_skills.py
"""
from html import escape
from urllib.parse import quote

N_REPOS = 27
BLUE, ORANGE, GREEN, AMBER, PURPLE = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#6250d6"

# (field, colour, [(skill, own repos using it)])
EVIDENCE = [
    ("AI Engineering", BLUE, [("Hugging Face Transformers", 4), ("PEFT / LoRA / QLoRA", 3), ("OpenAI API", 3), ("FAISS", 2), ("sentence-transformers", 2), ("LangChain", 2), ("Pydantic", 2), ("MCP server", 1)]),
    ("ML Engineering", ORANGE, [("PyTorch", 9), ("scikit-learn", 10), ("Mobilint NPU", 4), ("ONNX", 3), ("Optuna", 2), ("XGBoost", 1), ("TensorFlow / Keras", 1), ("CLIP / BLIP", 1)]),
    ("Data Science", GREEN, [("Matplotlib", 22), ("Pandas", 17), ("NumPy", 16), ("Seaborn", 12), ("SciPy / statsmodels", 4), ("PySpark", 1), ("LSTM forecasting", 1)]),
    ("Data Analytics", AMBER, [("Power BI and DAX", 5), ("Plotly", 2), ("SQL in project code", 1)]),
    ("Forward Deployed", PURPLE, [("Docker", 1), ("Kubernetes", 1), ("Kafka", 1), ("MongoDB", 1), ("React", 1), ("FastAPI", 1), ("Streamlit", 1)]),
]

FONT = "-apple-system,Segoe UI,Helvetica,Arial,sans-serif"


def chart():
    W, rh, x_lab, x_bar, bar_w = 880, 21, 24, 250, 520
    y = 76
    body = ['<text x="24" y="30" class="h">Skills, counted from my code</text>',
            f'<text x="24" y="47" class="s">Number of my {N_REPOS} repositories that use each tool. Scanned from code and notebook cells, not self-rated.</text>']
    for field, col, rows in EVIDENCE:
        body.append(f'<text x="{x_lab}" y="{y}" class="g" fill="{col}" style="fill:{col}">{escape(field)}</text>')
        y += 8
        for name, n in rows:
            y += rh
            w = max(bar_w * n / N_REPOS, 4)
            body.append(f'<text x="{x_lab+10}" y="{y}" class="l">{escape(name)}</text>')
            body.append(f'<rect x="{x_bar}" y="{y-12}" width="{w:.1f}" height="14" rx="3" fill="{col}"/>')
            body.append(f'<text x="{x_bar+w+8:.1f}" y="{y}" class="l" font-weight="600">{n}</text>')
        y += 20
    H = y + 6
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Skills counted from my repositories">
<title>Skills counted from my repositories</title>
<style>
:root{{--bg:#fcfcfb;--ink:#0b0b0b;--muted:#52514e}}
@media (prefers-color-scheme: dark){{:root{{--bg:#1a1a19;--ink:#f0efec;--muted:#c3c2b7}}}}
text{{font-family:{FONT};fill:var(--ink)}}
.h{{font-size:16px;font-weight:600}}.s{{font-size:12px;fill:var(--muted)}}.l{{font-size:12.5px}}.g{{font-size:13px;font-weight:700}}
</style>
<rect width="{W}" height="{H}" rx="12" fill="var(--bg)"/>
{chr(10).join(body)}
</svg>
'''
    open("assets/skills.svg", "w", encoding="utf-8").write(svg)


# ----------------------------------------------------------- badge markdown
def badge(label, color, logo=None):
    lab = quote(label.replace("-", "--").replace("_", "__"), safe="")
    url = f"https://img.shields.io/badge/{lab}-{color.lstrip('#')}?style=flat-square"
    if logo:
        url += f"&logo={logo}&logoColor=white"
    return f"![{label}]({url})"


def line(items, color):
    return " ".join(badge(n, color, lg) for n, lg in items)


FIELDS = [
    ("AI Engineering", "2a78d6", "LLMs, retrieval and evaluation",
     [("OpenAI API", "openai"), ("Hugging Face", "huggingface"), ("PEFT, LoRA, QLoRA", None), ("RAG", None), ("FAISS", None), ("sentence-transformers", None),
      ("Cross-encoder reranking", None), ("LangChain", "langchain"), ("MCP (Model Context Protocol)", None), ("Pydantic", "pydantic"),
      ("Prompt engineering", None), ("LLM-as-judge evaluation", None), ("Text-to-SQL", None)],
     [("Ollama", None), ("ChromaDB", None), ("Unsloth", None), ("LightRAG experiments", None), ("Gemini API", "googlegemini")],
     "[LLM prompting and WixQA RAG](https://github.com/vrushabh05/llm-prompting-and-enterprise-rag-wixqa) · [Gemma PEFT](https://github.com/vrushabh05/gemma-instruction-tuning-peft) · [NLQuery](https://github.com/vrushabh05/nlquery-genai) · [MealPilot MCP](https://github.com/vrushabh05/mealpilot-mcp) · [Persona RAG](#persona-rag-qlora-persona-generation-in-progress)"),
    ("ML Engineering", "eb6834", "Training, evaluation and edge deployment",
     [("PyTorch", "pytorch"), ("TensorFlow and Keras", "tensorflow"), ("scikit-learn", "scikitlearn"), ("XGBoost", None), ("Optuna", None), ("ONNX", "onnx"),
      ("Mobilint NPU (compile, quantize, benchmark)", None), ("CNNs", None), ("CLIP and BLIP", None), ("Transfer learning", None), ("Streamlit", "streamlit"), ("FastAPI", "fastapi")],
     [("Airflow", "apacheairflow"), ("Spark pipelines", "apachespark"), ("pytest", "pytest"), ("MinIO", None)],
     "[Emotional TTS on NPU](https://github.com/vrushabh05/emotional-tts-mobilint-npu) · [Super-resolution on NPU](https://github.com/vrushabh05/super-resolution-npu-deep-learning-labs) · [CLIP and BLIP](https://github.com/vrushabh05/clip-blip-multimodal-flickr30k) · [AlexNet](https://github.com/vrushabh05/alexnet-imagenet20-from-scratch) · [LeNet-5](https://github.com/vrushabh05/mnist-lenet5-and-naive-bayes)"),
    ("Data Science", "1baf7a", "Statistics, modelling and forecasting",
     [("Python", "python"), ("pandas", "pandas"), ("NumPy", "numpy"), ("SciPy and statsmodels", "scipy"), ("scikit-learn", "scikitlearn"), ("PySpark", "apachespark"),
      ("Bootstrap and hypothesis tests", None), ("Cross-validation", None), ("LSTM and CNN-LSTM forecasting", None), ("Feature engineering", None), ("NLP (NLTK, spaCy)", None), ("Matplotlib", None), ("Seaborn", None)],
     [("Multiple-test correction", None), ("Seed-stability checks", None)],
     "[ML fundamentals](https://github.com/vrushabh05/ml-fundamentals-from-scratch) · [Statistics](https://github.com/vrushabh05/statistics-fundamentals) · [PySpark](https://github.com/vrushabh05/pyspark-logistic-regression-rdd-vs-dataframe) · [Airline satisfaction](https://github.com/vrushabh05/airline-satisfaction-classification) · [Wildfire](https://github.com/vrushabh05/wildfire-dynamics-prediction)"),
    ("Data Analytics", "eda100", "Dashboards, SQL and storytelling",
     [("Power BI", "powerbi"), ("DAX", None), ("Tableau", "tableau"), ("SQL", "postgresql"), ("Python EDA", "python"), ("Plotly", "plotly"), ("Forecasting and decomposition", None), ("KPI design", None), ("Data cleaning", None), ("Data storytelling", None)],
     [("Admin analytics pages (React)", "react")],
     "[Global sales](https://github.com/vrushabh05/Global_Sales_Insights-and-Future-Forecasting-with-PowerBI) · [Superstore](https://github.com/vrushabh05/PowerBI_Walmart_Sales-_Dashboard) · [Spotify](https://github.com/vrushabh05/Spotify-Dashboard) · [Superstore EDA](https://github.com/vrushabh05/Exploratory_Data_Analysis_on_Walmart_sales_data)"),
    ("Forward Deployed Engineering", "6250d6", "Shipping systems end to end",
     [("React", "react"), ("Redux", "redux"), ("Node.js", "nodedotjs"), ("Express", "express"), ("FastAPI", "fastapi"), ("Kafka", "apachekafka"), ("MongoDB", "mongodb"), ("Docker", "docker"),
      ("Kubernetes", "kubernetes"), ("JMeter", "apachejmeter"), ("REST APIs", None), ("Microservices", None)],
     [("Next.js", "nextdotjs"), ("MySQL", "mysql"), ("Redis", "redis"), ("AWS EKS, ECR, S3", "amazonaws"), ("GitHub Actions", "githubactions"), ("Airflow", "apacheairflow")],
     "[Airbnb-style distributed system](https://github.com/vrushabh05/Lab1_distributed_system) · [MetaTravelGrid](#metatravelgrid-travel-booking-platform-team-project) · [MealPilot MCP](https://github.com/vrushabh05/mealpilot-mcp)"),
]


def markdown():
    out = []
    for i, (name, col, sub, own, team, links) in enumerate(FIELDS):
        out.append(f"<details{' open' if i == 0 else ''}>")
        out.append(f"<summary><b>{name}</b>: {sub}</summary>\n")
        out.append("**Hands-on in my own projects**\n")
        out.append(line(own, col) + "\n")
        out.append("**Used on team projects** (built with teammates; I contributed to parts of the stack)\n")
        out.append(line(team, "8a8984") + "\n")
        out.append(f"**Where to see it:** {links}\n")
        out.append("</details>\n")
    return "\n".join(out)


if __name__ == "__main__":
    chart()
    print(markdown())

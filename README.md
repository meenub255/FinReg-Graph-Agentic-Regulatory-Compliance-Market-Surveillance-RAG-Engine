<div align="center">

# FinReg-Graph: Agentic Regulatory Compliance & Market Surveillance RAG Engine

**Enterprise Data Engineering ETL Pipeline &bull; Qdrant Hybrid (Dense + BM25 RRF) Retrieval &bull; 6-Node LangGraph Self-RAG Compliance Verification for Capital Markets**

[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-0284c7?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-6--Node%20StateGraph-a855f7?style=for-the-badge)](https://github.com/langchain-ai/langgraph)
[![Qdrant](https://img.shields.io/badge/Qdrant-Hybrid%20RRF%20Search-10b981?style=for-the-badge)](https://qdrant.tech/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Enterprise%20REST%20API-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Pytest](https://img.shields.io/badge/Tests-6%2F6%20Passing-22c55e?style=for-the-badge&logo=pytest&logoColor=white)](#testing--quality-assurance)
[![Recall](https://img.shields.io/badge/Context%20Recall-100.0%25-f59e0b?style=for-the-badge)](#quantitative-rag-evaluation--benchmark-results)
[![Citation Precision](https://img.shields.io/badge/Citation%20Precision-99.1%25-ef4444?style=for-the-badge)](#quantitative-rag-evaluation--benchmark-results)

<br />

### Live End-to-End Working Demo (LangGraph 6-Node Execution + Hybrid RRF Lab + Benchmark Suite)

![FinReg-Graph Live Walkthrough Animation](docs/assets/finreg_graph_walkthrough.gif)

> **Video Recording:** Watch the inline animated walkthrough above or [download/view the full HD `.mp4` video (`docs/assets/finreg_graph_demo.mp4`)](docs/assets/finreg_graph_demo.mp4).

</div>

---

## Executive Overview

**FinReg-Graph** is a production-grade **Agentic Retrieval-Augmented Generation (RAG) & Regulatory Surveillance System** engineered to automate compliance verification across complex financial market regulations, exchange listing rules, and public company disclosures.

Built around **Nasdaq**, **SEC**, and **FINRA** regulatory frameworks, **FinReg-Graph** ingests statutory rulebooks into a **hierarchical AST data engineering pipeline**, indexes them in **Qdrant** using **Hybrid Dense + Sparse BM25 Reciprocal Rank Fusion (RRF)** with **Cross-Reference Graph Expansion**, and orchestrates a **6-node LangGraph state machine** that grades retrieved statutory evidence, rewrites ambiguous queries, determines compliance verdicts (`COMPLIANT`, `NON_COMPLIANT`, `CONDITIONAL_REVIEW`, `INFORMATIONAL`), and deterministically audits every cited statute against the vector database to eliminate hallucinations.

---

## Interactive UI Walkthrough (Arrow-Annotated Guide)

### 1. Agentic Compliance Console (`LangGraph 6-Node State Machine + Qdrant Hybrid RRF`)

![Annotated Agentic Compliance Console UI](docs/assets/ui_console_annotated.png)

| Arrow | UI Component | What It Does & How It Works |
| :---: | :--- | :--- |
| 🔴 **`①`** | **One-Click Institutional Scenarios** | Pre-configured real-world audit scenarios covering **SEC Rule 15c3-5** (Naked Sponsored Access), **Reg SHO Rules 203/204** (Short Sale Locate & `T+2` Close-Out), **Nasdaq Rules 5450/5810** (`$1.00` Bid Price Deficiency), **Reg NMS Rule 611** (ISO Order Routing), **SEC Form 8-K Item 1.05** (4-Day Cyber Breach), and **SMARTS / FINRA Rule 3110** (Spoofing & Algo Kill-Switches). |
| 🔵 **`②`** | **Query Analyzer & Jurisdiction Router** | Accepts free-text regulatory questions or structured trade scenarios, lets compliance analysts filter by jurisdiction (`ALL`, `SEC`, `NASDAQ`, `FINRA_NASDAQ`), configure `Top-K` RRF depth, and toggle the **Self-RAG Corrective Query Rewriter**. |
| 🟣 **`③`** | **Live 6-Node LangGraph Execution Trace** | Displays real-time microsecond telemetry for every node in the state machine (`1. query_analyzer` $\rightarrow$ `2. hybrid_retriever` $\rightarrow$ `3. evidence_grader` $\rightarrow$ `4. query_rewriter` $\rightarrow$ `5. compliance_verifier` $\rightarrow$ `6. hallucination_audit`). |
| 🔴 **`④`** | **Compliance Verdict & Guardrail Scores** | Highlights the final determination badge (`NON COMPLIANT`, `COMPLIANT`, `CONDITIONAL REVIEW`, `INFORMATIONAL`), risk severity (`CRITICAL`), and live guardrail metrics (**Faithfulness `99.7%`**, **Citation Precision `100.0%`**, **Evidence Sufficiency `99.0%`**). |
| 🟡 **`⑤`** | **Violated Clauses & Engineering Remediation** | Splits the determination into **Triggered/Violated Statutory Clauses** (red panel citing exact paragraphs like `17 CFR § 240.15c3-5(d)(1)`) and **Mandatory Engineering & Supervisory Remediation Steps** (green panel). |
| 🟢 **`⑥`** | **Node 6 Hallucination Auditor Citation Log** | Deterministic post-generation guardrail that regex-extracts every statute cited by the LLM and cross-checks it against Qdrant payloads (`VERIFIED IN QDRANT` + exact `chunk_id` provenance). |
| 🔵 **`⑦`** | **Qdrant Hybrid RRF Context & Score Breakdown** | Shows every retrieved statutory clause alongside its **Combined RRF Score** (`0.889`) and decomposed **Dense Cosine**, **Sparse BM25**, and **Citation Boost** scores plus statutory hierarchy breadcrumbs. |

---

### 2. Hybrid RRF Retrieval Lab & Live Data Engineering ETL Ingestion

![Annotated Hybrid RRF Retrieval Lab & Live ETL UI](docs/assets/ui_hybrid_lab_annotated.png)

| Arrow | UI Component | What It Does & How It Works |
| :---: | :--- | :--- |
| 🔵 **`①`** | **Multi-Citation Query Input** | Tests complex multi-statute queries (e.g., combining `Rule 15c3-5(c)(1)(ii)` erroneous order collars with `Rule 204(a)` `T+2` close-out rules). |
| 🟢 **`②`** | **3-Way Modality Ranking Comparison** | Side-by-side comparison proving why **Hybrid RRF + Citation Boost** ranks the exact required clauses at `#1` (`0.882`) and `#2`, whereas **Dense Vector Only** or **Sparse BM25 Only** misses cross-domain nuances. |
| 🟡 **`③`** | **Live YAML & Hierarchical AST Editor** | Allows data engineers or compliance officers to paste new regulatory policies with YAML frontmatter (`doc_id`, `jurisdiction`, `citation_prefix`) for live ingestion. |
| 🟢 **`④`** | **Real-Time SHA-256 Qdrant Upsert Telemetry** | Runs the AST chunker, extracts citations/thresholds, computes a deterministic `SHA-256` hash (`UUIDv5`), upserts into Qdrant in `3.4ms`, and confirms idempotent deduplication. |

---

### 3. RAGAS-Style 10-Scenario Golden Evaluation Benchmark Suite

![Annotated RAG Evaluation Benchmark UI](docs/assets/ui_eval_benchmark_annotated.png)

| Arrow | UI Component | What It Does & How It Works |
| :---: | :--- | :--- |
| 🟢 **`①`** | **100.0% Statutory Context Recall & Precision** | Measures whether the ground-truth SEC, Nasdaq, and FINRA statutory clauses appear in the `Top-6` Qdrant Hybrid RRF results across all 10 benchmark cases. |
| 🔵 **`②`** | **99.1% Citation Grounding & 96.8% Faithfulness** | Quantifies hallucination resistance verified by `Node 6 (hallucination_auditor)` across all generated compliance determinations. |
| 🟡 **`③`** | **10/10 Exact Compliance Verdict Matches** | Scenario-by-scenario audit table comparing expected vs. predicted verdicts (`NON_COMPLIANT`, `CONDITIONAL_REVIEW`, `INFORMATIONAL`) with per-query latency (`P50: 12.9ms`). |

---

## Why FinReg-Graph? (Naive RAG vs. FinReg-Graph)

| Engineering Challenge | Naive RAG Pipeline | **FinReg-Graph Architecture** |
| :--- | :--- | :--- |
| **Document Chunking** | Fixed 500-char sliding window; splits exceptions from obligations. | **Hierarchical Statutory AST Chunker** preserving `Document > Section > Subsection` breadcrumbs, obligation strength tags, and numeric thresholds. |
| **Idempotency & Versioning** | Appends duplicate vectors on re-ingestion. | Deterministic **`SHA-256` content hashing** mapped to `UUIDv5` Qdrant point IDs for zero-duplicate incremental ETL updates. |
| **Retrieval Modality** | Dense vector cosine similarity only; misses exact rule citations. | **3-Way Hybrid RRF** fusing **384-dim Dense Embeddings** + **Okapi BM25 Sparse Lexical Search** + **Exact Citation/Threshold Booster**. |
| **Cross-Referenced Rules** | Fails when Rule A says *"pursuant to Rule B"* located in another document. | **Cross-Reference Citation Graph** automatically expands top hits by resolving cited statutes across SEC & Nasdaq documents. |
| **Colloquial Queries** | Single-pass retrieval fails on trader slang (*"naked access"*, *"fat-finger"*). | **LangGraph Self-RAG Loop** grades evidence sufficiency and triggers a **Corrective Query Rewriter** that expands jargon into formal statutory terms. |
| **Hallucination Control** | Relies solely on prompt instructions (*"do not hallucinate"*). | **Deterministic Hallucination Auditor (Node 6)** regex-extracts every emitted citation and verifies its existence against Qdrant payloads (`99.1%` precision). |

---

## System Architecture Diagrams

### 1. Scalable Regulatory Data Engineering ETL Pipeline (`src/pipeline/`)

```mermaid
flowchart LR
    A["📄 SEC / Nasdaq / FINRA\nRulebooks & Filings (.md)"] --> B["⚙️ YAML Frontmatter &\nStatutory AST Parser"]
    B --> C["🧱 Section-Aware Chunker\n(Breadcrumb Context Injection)"]
    C --> D["🔍 Regex Statutory Citation &\nThreshold Extractor"]
    D --> E["🏷️ Obligation Classifier\n(PROHIBITION / MANDATORY / EXEMPTION)"]
    E --> F["🔐 SHA-256 Content Hash &\nUUIDv5 Idempotent Dedup"]
    F --> G[("🗄️ Qdrant Vector Store\n+ BM25 Sparse Index\n+ Cross-Ref Graph")]

    style A fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#f8fafc
    style B fill:#0f172a,stroke:#0ea5e9,stroke-width:2px,color:#f8fafc
    style C fill:#0f172a,stroke:#a855f7,stroke-width:2px,color:#f8fafc
    style D fill:#0f172a,stroke:#f59e0b,stroke-width:2px,color:#f8fafc
    style E fill:#0f172a,stroke:#ec4899,stroke-width:2px,color:#f8fafc
    style F fill:#0f172a,stroke:#10b981,stroke-width:2px,color:#f8fafc
    style G fill:#064e3b,stroke:#34d399,stroke-width:2px,color:#ffffff
```

---

### 2. 6-Node LangGraph Agentic Compliance Workflow (`src/agents/`)

```mermaid
flowchart TD
    START(["🚀 Incoming Query / Trade Audit Scenario"]) --> N1["1️⃣ query_analyzer\nIntent Classification, Jurisdiction Routing & Sub-Query Decomposition"]
    N1 --> N2["2️⃣ hybrid_retriever\nQdrant Dense + Okapi BM25 Sparse + RRF + Cross-Ref Graph"]
    N2 --> N3["3️⃣ evidence_grader\nSelf-RAG Sufficiency Evaluator & Chunk Relevance Grader"]
    N3 -- "Sufficiency < 0.78\n(Colloquial Query)" --> N4["4️⃣ query_rewriter\nStatutory Terminology Expansion Loop"]
    N4 --> N2
    N3 -- "Sufficient Statutory Evidence" --> N5["5️⃣ compliance_verifier\nGrounded Regulatory Synthesis & Verdict Determination"]
    N5 --> N6["6️⃣ hallucination_auditor\nDeterministic Citation Guardrail & Faithfulness Scorer"]
    N6 --> END_NODE(["✅ Structured Compliance Audit Report + Node Telemetry"])

    style START fill:#0284c7,stroke:#38bdf8,stroke-width:2px,color:#ffffff
    style N1 fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#f8fafc
    style N2 fill:#0f172a,stroke:#10b981,stroke-width:2px,color:#f8fafc
    style N3 fill:#0f172a,stroke:#f59e0b,stroke-width:2px,color:#f8fafc
    style N4 fill:#3b0764,stroke:#a855f7,stroke-width:2px,color:#f3e8ff
    style N5 fill:#0f172a,stroke:#ef4444,stroke-width:2px,color:#f8fafc
    style N6 fill:#064e3b,stroke:#34d399,stroke-width:2px,color:#ecfdf5
    style END_NODE fill:#059669,stroke:#34d399,stroke-width:2px,color:#ffffff
```

### Hybrid Reciprocal Rank Fusion ($\text{RRF}$) Mathematical Formulation

To handle both conceptual compliance queries and exact statutory identifiers simultaneously, [`QdrantHybridRetriever`](src/retrieval/qdrant_store.py) computes a weighted Reciprocal Rank Fusion score across three retrieval rankings:

$$\text{RRF}(d) = \frac{w_{\text{dense}}}{k + \text{rank}_{\text{dense}}(d)} + \frac{w_{\text{sparse}}}{k + \text{rank}_{\text{BM25}}(d)} + \frac{w_{\text{citation}}}{k + \text{rank}_{\text{citation}}(d)}$$

where $k = 60$, $w_{\text{dense}} = 0.45$, $w_{\text{sparse}} = 0.40$, and $w_{\text{citation}} = 0.15$, followed by **Cross-Reference Graph Expansion** across linked SEC and Nasdaq rulebooks.

---

## Pre-Loaded Capital Markets Regulatory Corpus (`data/regulations/`)

| Document ID | Jurisdiction | Regulatory Scope & Key Provisions Covered |
| :--- | :---: | :--- |
| **`SEC-15C3-5`** | `SEC` | **17 CFR § 240.15c3-5 (Market Access Rule)**: Prohibition on unfiltered ("naked") sponsored access, pre-trade credit/capital thresholds, erroneous order price/size collars, direct & exclusive broker-dealer control, annual CEO certification. |
| **`SEC-REG-SHO`** | `SEC` | **17 CFR §§ 242.200–204 (Regulation SHO)**: `LONG`/`SHORT`/`SHORT EXEMPT` order marking, Rule 201 `10%` intraday circuit breaker (Alternative Uptick Rule), Rule 203(b)(1) pre-trade locate, Threshold Securities (`10,000 shares` & `0.5%`), Rule 204 `T+2` / `T+4` close-out & Penalty Box. |
| **`SEC-REG-NMS`** | `SEC` | **17 CFR §§ 242.600–613 (Regulation NMS)**: Rule 611 Order Protection (Trade-Through Rule), Intermarket Sweep Orders (`ISO`) simultaneous full-displayed-size routing, Rule 610 access fee caps (`$0.0030` / `30 mils`), Rule 612 Sub-Penny Rule, Rule 613 CAT reporting & `50ms`/`100μs` clock sync. |
| **`NASDAQ-RULE-5000`** | `NASDAQ` | **Nasdaq Equity Rules Series 5000 & Market Surveillance**: Rule 5250 & `IM-5250-1` (`10-minute` prior notice to Nasdaq MarketWatch), Rule 4120 trading halts, Rules 5450/5550 (`$1.00` minimum bid price), Rule 5810 (`30-day` trigger, `180-day` cure period, `$0.10` accelerated delisting, `250:1` reverse split limit), Rule 5605 Audit Committee, SMARTS Spoofing/Layering (`MP-101`). |
| **`SEC-CYBER-10K-8K`** | `SEC` | **SEC Form 8-K Item 1.05, Form 10-K Item 1C & SOX 302/404**: Mandatory `4-business-day` material cybersecurity incident disclosure, U.S. Attorney General national security delay exception, Board/CISO cyber governance, SOX 404 ICFR material weakness reporting. |
| **`FINRA-NASDAQ-SUPERVISION`** | `FINRA_NASDAQ` | **FINRA Rules 3110, 3310, 5310 & RN 15-09**: Algorithmic trading pre-deployment sandbox testing, independent kill-switches, `Series 57` registration, quarterly "regular and rigorous" best-execution & PFOF review, FinCEN `$5,000` SAR reporting (`30 calendar days`) & `25%` beneficial ownership CDD. |

---

## Quantitative RAG Evaluation & Benchmark Results

Evaluated via [`src/evaluation/benchmark.py`](src/evaluation/benchmark.py) across **10 Golden Capital Markets Compliance Scenarios**:

| Metric | Score | Target | Status |
| :--- | :---: | :---: | :---: |
| **Context Recall (Top-6 Statutory Retrieval)** | **100.0%** | `>= 90.0%` | ✅ **PASS** |
| **Context Precision (Hybrid RRF Reranking)** | **100.0%** | `>= 85.0%` | ✅ **PASS** |
| **Statutory Citation Grounding Precision** | **99.1%** | `>= 95.0%` | ✅ **PASS** |
| **Answer Faithfulness (Hallucination Guardrail)** | **96.8%** | `>= 90.0%` | ✅ **PASS** |
| **Compliance Verdict Accuracy** | **100.0%** | `>= 90.0%` | ✅ **PASS** |
| **Pipeline Execution Latency (P50 / P95)** | **12.9 ms / 24.8 ms** | `< 2000 ms` | ✅ **PASS** |

<details>
<summary><strong>📊 Click to Expand Full 10-Scenario Benchmark Breakdown Table</strong></summary>

| Case ID | Regulatory Domain | Expected Verdict | Predicted Verdict | Recall | Precision | Faithfulness | Latency |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `EVAL-01` | SEC Rule 15c3-5 (Unfiltered Sponsored Access) | `NON_COMPLIANT` | `NON_COMPLIANT` | `100%` | `100%` | `100%` | `12.7 ms` |
| `EVAL-02` | SEC Rule 15c3-5 (Direct & Exclusive Control) | `NON_COMPLIANT` | `NON_COMPLIANT` | `100%` | `100%` | `100%` | `20.4 ms` |
| `EVAL-03` | SEC Reg SHO (Locate & Close-Out Rule 203/204) | `NON_COMPLIANT` | `NON_COMPLIANT` | `100%` | `100%` | `94%` | `11.3 ms` |
| `EVAL-04` | SEC Reg SHO (Rule 201 Circuit Breaker) | `INFORMATIONAL` | `INFORMATIONAL` | `100%` | `100%` | `97%` | `14.2 ms` |
| `EVAL-05` | SEC Reg NMS (Rule 611 Intermarket Sweep Orders) | `NON_COMPLIANT` | `NON_COMPLIANT` | `100%` | `100%` | `100%` | `24.8 ms` |
| `EVAL-06` | Nasdaq Listing Rules (Rule 5450/5810 Sub-$1.00 Bid) | `CONDITIONAL_REVIEW` | `CONDITIONAL_REVIEW` | `100%` | `100%` | `93%` | `8.8 ms` |
| `EVAL-07` | Nasdaq Accelerated Delisting ($0.10 & 250:1 Split) | `NON_COMPLIANT` | `NON_COMPLIANT` | `100%` | `100%` | `93%` | `6.0 ms` |
| `EVAL-08` | SEC Form 8-K Item 1.05 & Nasdaq MarketWatch | `NON_COMPLIANT` | `NON_COMPLIANT` | `100%` | `100%` | `100%` | `13.1 ms` |
| `EVAL-09` | Nasdaq SMARTS Surveillance & FINRA Algo Kill-Switch | `NON_COMPLIANT` | `NON_COMPLIANT` | `100%` | `100%` | `92%` | `11.6 ms` |
| `EVAL-10` | FINRA Rule 3310 AML SAR & Rule 5310 Best Execution | `INFORMATIONAL` | `INFORMATIONAL` | `100%` | `100%` | `100%` | `13.6 ms` |

</details>

---

## Repository Structure

```text
FinReg-Graph-Agentic-Regulatory-Compliance-Market-Surveillance-RAG-Engine/
├── docs/
│   └── assets/                             # Annotated UI screenshots, GIF walkthrough & MP4 demo video
│       ├── finreg_graph_walkthrough.gif
│       ├── finreg_graph_demo.mp4
│       ├── ui_console_annotated.png
│       ├── ui_hybrid_lab_annotated.png
│       └── ui_eval_benchmark_annotated.png
├── data/
│   ├── regulations/                        # Curated SEC, Nasdaq & FINRA regulatory markdown corpus
│   │   ├── sec_rule_15c3_5_market_access.md
│   │   ├── sec_reg_sho_short_sales.md
│   │   ├── sec_reg_nms_order_protection.md
│   │   ├── nasdaq_rule_5000_listing_surveillance.md
│   │   ├── sec_10k_8k_cyber_icfr_disclosure.md
│   │   └── finra_nasdaq_algo_supervision_aml.md
│   └── eval_results/                       # Generated JSON & Markdown RAG benchmark reports
│       ├── latest_benchmark_report.json
│       └── latest_benchmark_report.md
├── src/
│   ├── config.py                           # Environment & hyperparameter configuration
│   ├── models/
│   │   └── schemas.py                      # Pydantic v2 schemas for chunks, traces & audit verdicts
│   ├── pipeline/
│   │   ├── chunker.py                      # Hierarchical AST parser, citation & threshold extractor
│   │   └── ingestion.py                    # Idempotent SHA-256 ETL pipeline & telemetry reporter
│   ├── retrieval/
│   │   └── qdrant_store.py                 # Qdrant Hybrid Dense + BM25 Sparse + RRF + Cross-Ref Graph
│   ├── llm/
│   │   └── provider.py                     # Multi-provider LLM router (Gemini / OpenAI / Groq / Offline)
│   ├── agents/
│   │   └── compliance_graph.py             # 6-Node LangGraph Self-RAG & Hallucination Auditor workflow
│   ├── evaluation/
│   │   └── benchmark.py                    # 10-scenario RAGAS-style evaluation benchmark suite
│   ├── api/
│   │   └── main.py                         # FastAPI Enterprise REST API & dashboard server
│   └── frontend/
│       └── index.html                      # Interactive Nasdaq Regulatory Intelligence Web Terminal
├── tests/
│   └── test_compliance_rag.py              # Pytest unit & integration test suite (6/6 passing)
├── Dockerfile                              # Production container image
├── docker-compose.yml                      # Multi-container orchestration (Qdrant + FastAPI API)
├── pyproject.toml                          # Python packaging & pytest configuration
├── requirements.txt                        # Python dependencies
└── .env.example                            # Environment variable template
```

---

## Getting Started

### 1. Clone the Repository & Install Dependencies

```bash
git clone https://github.com/meenub255/FinReg-Graph-Agentic-Regulatory-Compliance-Market-Surveillance-RAG-Engine.git
cd FinReg-Graph-Agentic-Regulatory-Compliance-Market-Surveillance-RAG-Engine
pip install -r requirements.txt
```

### 2. Configure Environment (Optional — Runs Out-of-the-Box!)

Copy `.env.example` to `.env` if you want to connect a live **Google Gemini**, **OpenAI**, or **Groq** API key, or a remote **Qdrant** server. If no API key is set, the system automatically runs using its built-in **Deterministic Institutional Regulatory Engine** and in-memory **Qdrant** index:

```bash
cp .env.example .env
```

### 3. Launch the Enterprise FastAPI Server & Web Terminal

```bash
uvicorn src.api.main:app --host 127.0.0.1 --port 8000 --reload
```

* **Interactive Web Terminal**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **OpenAPI / Swagger Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 4. Run with Docker Compose (FastAPI + Qdrant Server)

```bash
docker compose up --build
```

---

## Testing & Quality Assurance

### Run the Automated Pytest Suite
```bash
pytest -v
```

### Run the 10-Scenario RAG Evaluation Benchmark CLI
```bash
python -m src.evaluation.benchmark
```

---

## REST API Reference

| Method | Endpoint | Description |
| :---: | :--- | :--- |
| `GET` | `/api/v1/health` | Returns ETL pipeline telemetry, Qdrant index stats, and active LLM backend. |
| `POST` | `/api/v1/compliance/query` | Executes the 6-node LangGraph workflow and returns a citation-audited compliance determination. |
| `POST` | `/api/v1/compliance/audit-scenario` | Audits a structured broker-dealer trade or issuer listing scenario. |
| `POST` | `/api/v1/retrieval/compare` | Side-by-side comparison of Hybrid RRF vs. Dense Vector vs. Sparse BM25 rankings. |
| `POST` | `/api/v1/pipeline/ingest` | Ingests custom regulatory Markdown documents into the ETL + Qdrant pipeline at runtime. |
| `GET` | `/api/v1/corpus/documents` | Lists indexed regulatory documents, AST chunks, breadcrumbs, and `SHA-256` hashes. |
| `GET` | `/api/v1/eval/latest` | Returns the latest 10-case RAG evaluation benchmark report. |
| `POST` | `/api/v1/eval/run` | Triggers a live execution of the 10-scenario evaluation benchmark suite. |

### Example API Request (`POST /api/v1/compliance/query`)

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/compliance/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "A quantitative hedge fund routes orders directly to Nasdaq using our broker-dealer MPID via unfiltered sponsored access where credit thresholds are checked post-trade at end-of-day. Is this compliant?",
    "jurisdiction_filter": "ALL",
    "top_k": 6,
    "enable_self_rag_rewrite": true
  }'
```

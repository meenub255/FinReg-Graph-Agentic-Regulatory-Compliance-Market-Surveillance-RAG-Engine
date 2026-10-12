# Nasdaq & SEC Regulatory Compliance RAG — Evaluation Benchmark Report

- **Active LLM Engine:** `Deterministic Institutional Regulatory Engine (Offline Ready)`
- **Qdrant Collection:** `nasdaq_sec_regulatory_corpus`
- **Total Golden Benchmark Scenarios:** `10`

## Aggregate RAG & Compliance Verification Metrics

| Metric | Score | Target Threshold | Status |
| :--- | :---: | :---: | :---: |
| **Context Recall (Top-K Statutory Retrieval)** | `100.0%` | `>= 90.0%` | PASS |
| **Context Precision (Hybrid RRF Reranking)** | `100.0%` | `>= 85.0%` | PASS |
| **Answer Faithfulness (Hallucination Guardrail)** | `96.8%` | `>= 90.0%` | PASS |
| **Statutory Citation Precision** | `99.1%` | `>= 95.0%` | PASS |
| **Compliance Verdict Accuracy** | `100.0%` | `>= 90.0%` | PASS |
| **P50 / P95 Pipeline Latency** | `22.2 ms / 38.1 ms` | `< 2000 ms` | PASS |

## Scenario-by-Scenario Breakdown

| ID | Regulatory Domain | Expected Verdict | Predicted Verdict | Recall | Precision | Faithfulness | Latency (ms) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `EVAL-01` | SEC Rule 15c3-5 (Market Access) | `NON_COMPLIANT` | `NON_COMPLIANT` | `100%` | `100%` | `100%` | `28.4` |
| `EVAL-02` | SEC Rule 15c3-5 (Direct & Exclusive Control) | `NON_COMPLIANT` | `NON_COMPLIANT` | `100%` | `100%` | `100%` | `23.6` |
| `EVAL-03` | SEC Reg SHO (Locate & Close-Out Rule 203/204) | `NON_COMPLIANT` | `NON_COMPLIANT` | `100%` | `100%` | `94%` | `14.3` |
| `EVAL-04` | SEC Reg SHO (Rule 201 Circuit Breaker) | `INFORMATIONAL` | `INFORMATIONAL` | `100%` | `100%` | `97%` | `18.5` |
| `EVAL-05` | SEC Reg NMS (Rule 611 Intermarket Sweep Orders) | `NON_COMPLIANT` | `NON_COMPLIANT` | `100%` | `100%` | `100%` | `46.1` |
| `EVAL-06` | Nasdaq Listing Rules (Rule 5450/5810 Minimum Bid Price) | `CONDITIONAL_REVIEW` | `CONDITIONAL_REVIEW` | `100%` | `100%` | `93%` | `17.6` |
| `EVAL-07` | Nasdaq Accelerated Delisting ($0.10 & Reverse Split Rules) | `NON_COMPLIANT` | `NON_COMPLIANT` | `100%` | `100%` | `93%` | `14.3` |
| `EVAL-08` | SEC Form 8-K Item 1.05 & Nasdaq MarketWatch (Cybersecurity) | `NON_COMPLIANT` | `NON_COMPLIANT` | `100%` | `100%` | `100%` | `24.2` |
| `EVAL-09` | Nasdaq Market Surveillance & FINRA Algo Supervision | `NON_COMPLIANT` | `NON_COMPLIANT` | `100%` | `100%` | `92%` | `23.4` |
| `EVAL-10` | FINRA Rule 3310 AML & Rule 5310 Best Execution | `INFORMATIONAL` | `INFORMATIONAL` | `100%` | `100%` | `100%` | `21.1` |
"""
Comprehensive Pytest Suite for the Nasdaq & SEC Regulatory Compliance Agentic RAG System.

Tests:
1. Hierarchical AST Chunker & Statutory Metadata / Citation / Threshold Extraction
2. Idempotent Data Engineering ETL Pipeline & SHA-256 Deduplication
3. Qdrant Hybrid Dense + BM25 Sparse + RRF Retrieval & Jurisdiction Filtering
4. 6-Node LangGraph Agentic Compliance Verification State Machine
5. Hallucination Auditor & Citation Grounding Verification
6. FastAPI Enterprise REST Endpoints
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from src.agents.compliance_graph import AgenticComplianceWorkflow
from src.api.main import app
from src.evaluation.benchmark import ComplianceRAGEvaluator
from src.models.schemas import (
    ComplianceQueryRequest,
    ComplianceStatus,
    ObligationType,
)
from src.pipeline.chunker import RegulatoryHierarchicalChunker
from src.pipeline.ingestion import RegulatoryETLPipeline


def test_hierarchical_chunker_preserves_statutory_context() -> None:
    """Verify AST chunker extracts frontmatter, hierarchy breadcrumbs, citations, and thresholds."""
    sample_doc = """---
doc_id: "TEST-SEC-15C3-5"
title: "SEC Rule 15c3-5 Test Document"
jurisdiction: "SEC"
citation_prefix: "17 CFR § 240.15c3-5"
effective_date: "2011-07-14"
last_amended: "2024-03-15"
category: "Market Access"
---

# SEC Rule 15c3-5 Market Access

## § 240.15c3-5(c) Risk Management Controls

### § 240.15c3-5(c)(1) Financial Controls
Brokers or dealers shall prevent the entry of orders exceeding pre-set credit thresholds under `17 CFR § 240.15c3-5(c)(1)(i)` and `Nasdaq Rule 4611` within 10 minutes or $5,000 limits. Unfiltered access is strictly prohibited.
"""
    chunker = RegulatoryHierarchicalChunker()
    chunks = chunker.chunk_document(sample_doc, "test_15c3_5.md")

    assert len(chunks) == 1
    ch = chunks[0]
    assert ch.doc_id == "TEST-SEC-15C3-5"
    assert ch.jurisdiction == "SEC"
    assert "§ 240.15c3-5(c) Risk Management Controls" in ch.breadcrumb
    assert "§ 240.15c3-5(c)(1) Financial Controls" in ch.breadcrumb
    assert any("15c3-5" in c for c in ch.citations_extracted)
    assert any("Nasdaq Rule 4611" in c for c in ch.citations_extracted)
    assert ch.obligation_type == ObligationType.PROHIBITION
    assert "10 minutes" in ch.numeric_thresholds or "$5,000" in ch.numeric_thresholds
    assert len(ch.content_hash) == 64


def test_etl_pipeline_idempotent_deduplication() -> None:
    """Verify running directory ingestion twice does not duplicate chunks thanks to SHA-256 hashing."""
    pipeline = RegulatoryETLPipeline()
    report_1 = pipeline.run_directory_ingestion()
    count_1 = report_1.total_chunks_created

    assert report_1.documents_processed == 6
    assert count_1 >= 40
    assert report_1.unique_citations_indexed >= 25

    # Re-run ingestion on same directory; chunk count must remain identical
    report_2 = pipeline.run_directory_ingestion()
    assert report_2.total_chunks_created == count_1


def test_qdrant_hybrid_rrf_retrieval_and_filtering() -> None:
    """Verify Qdrant hybrid search ranks exact regulatory rules at top-1 and respects jurisdiction filters."""
    pipeline = RegulatoryETLPipeline()
    pipeline.run_directory_ingestion()
    retriever = pipeline.retriever

    # Query specifically for Nasdaq $1.00 minimum bid price deficiency
    hits = retriever.search(
        query="Nasdaq Rule 5450 and Rule 5810 minimum bid price below $1.00 for 30 consecutive business days",
        top_k=4,
        jurisdiction_filter="NASDAQ",
    )
    assert len(hits) > 0
    assert all(h.jurisdiction == "NASDAQ" for h in hits)
    assert hits[0].doc_id == "NASDAQ-RULE-5000"
    assert hits[0].rrf_score > 0.35


def test_langgraph_agentic_workflow_audit_verdicts() -> None:
    """Verify the 6-node LangGraph workflow accurately detects violations and audits citations."""
    pipeline = RegulatoryETLPipeline()
    pipeline.run_directory_ingestion()
    workflow = AgenticComplianceWorkflow(retriever=pipeline.retriever)

    # 1. Non-compliant sponsored access scenario
    req_violation = ComplianceQueryRequest(
        query=(
            "A hedge fund client routes orders directly to Nasdaq using our MPID via unfiltered "
            "sponsored access with post-trade credit checks only."
        ),
        jurisdiction_filter="ALL",
        top_k=5,
        enable_self_rag_rewrite=True,
    )
    resp = workflow.run(req_violation)
    assert resp.Compliance_status == ComplianceStatus.NON_COMPLIANT
    assert resp.risk_level == "CRITICAL"
    assert len(resp.agent_trace) >= 5
    assert resp.citation_precision >= 0.90
    assert resp.faithfulness_score >= 0.85

    # 2. Conditional compliance review for Nasdaq sub-$1.00 bid price
    req_cond = ComplianceQueryRequest(
        query="A Nasdaq Global Market company traded below $1.00 for 30 consecutive business days at $0.75.",
        jurisdiction_filter="ALL",
        top_k=5,
    )
    resp_cond = workflow.run(req_cond)
    assert resp_cond.Compliance_status == ComplianceStatus.CONDITIONAL_REVIEW


def test_rag_evaluation_benchmark_suite_scores() -> None:
    """Verify the 10-case golden benchmark achieves >= 95% recall and 100% verdict accuracy."""
    pipeline = RegulatoryETLPipeline()
    pipeline.run_directory_ingestion()
    workflow = AgenticComplianceWorkflow(retriever=pipeline.retriever)
    evaluator = ComplianceRAGEvaluator(workflow=workflow)

    summary = evaluator.run_benchmark(save_artifacts=False)
    assert summary.total_cases == 10
    assert summary.mean_context_recall >= 0.95
    assert summary.mean_context_precision >= 0.95
    assert summary.verdict_accuracy == 1.0


def test_fastapi_endpoints() -> None:
    """Verify all FastAPI enterprise endpoints return 200 OK and valid schemas."""
    client = TestClient(app)

    # 1. Dashboard HTML
    res_home = client.get("/")
    assert res_home.status_code == 200
    assert "NASDAQ & SEC REGULATORY COMPLIANCE" in res_home.text

    # 2. Health endpoint
    res_health = client.get("/api/v1/health")
    assert res_health.status_code == 200
    health_data = res_health.json()
    assert health_data["status"] == "OPERATIONAL"
    assert health_data["etl_telemetry"]["documents_processed"] >= 6

    # 3. Compliance query endpoint
    res_query = client.post(
        "/api/v1/compliance/query",
        json={
            "query": "What is the Form 8-K Item 1.05 filing deadline after a material cybersecurity incident?",
            "jurisdiction_filter": "SEC",
            "top_k": 4,
            "enable_self_rag_rewrite": True,
        },
    )
    assert res_query.status_code == 200
    q_data = res_query.json()
    assert "executive_summary" in q_data
    assert len(q_data["retrieved_chunks"]) > 0

    # 4. Modality comparison endpoint
    res_cmp = client.post(
        "/api/v1/retrieval/compare",
        json={"query": "Rule 204(a) close-out T+2 fail-to-deliver", "top_k": 3},
    )
    assert res_cmp.status_code == 200
    assert "hybrid_rrf_ranking" in res_cmp.json()

    # 5. Corpus explorer endpoint
    res_corpus = client.get("/api/v1/corpus/documents?jurisdiction=NASDAQ")
    assert res_corpus.status_code == 200
    assert res_corpus.json()["filtered_chunks_count"] > 0

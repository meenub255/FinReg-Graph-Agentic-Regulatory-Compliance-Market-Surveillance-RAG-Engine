"""
FastAPI Enterprise Backend for the Nasdaq & SEC Regulatory Compliance Agentic RAG System.

Exposes endpoints for:
- 6-Node LangGraph Agentic Compliance Verification (`POST /api/v1/compliance/query`)
- Trade & Issuer Scenario Compliance Auditing (`POST /api/v1/compliance/audit-scenario`)
- Hybrid vs. Dense vs. Sparse Retrieval Modality Comparison (`POST /api/v1/retrieval/compare`)
- Real-Time Regulatory ETL Document Ingestion (`POST /api/v1/pipeline/ingest`)
- Corpus & Statutory Chunk Explorer (`GET /api/v1/corpus/documents`)
- Automated RAG Evaluation Benchmark Suite (`GET /api/v1/eval/latest`, `POST /api/v1/eval/run`)
"""

from __future__ import annotations

import json
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from src.agents.compliance_graph import AgenticComplianceWorkflow, LANGGRAPH_AVAILABLE
from src.config import settings
from src.evaluation.benchmark import ComplianceRAGEvaluator
from src.models.schemas import (
    ComplianceQueryRequest,
    ComplianceQueryResponse,
    EvalSuiteSummary,
    IngestionReport,
    ScenarioAuditRequest,
)
from src.pipeline.ingestion import RegulatoryETLPipeline
from src.retrieval.qdrant_store import QdrantHybridRetriever


class CustomIngestRequest(BaseModel):
    """Payload for ingesting a new regulatory policy document into the ETL pipeline."""

    filename: str = Field(default="custom_policy.md")
    markdown_content: str = Field(..., min_length=20)


class ModalityCompareRequest(BaseModel):
    """Payload for comparing Dense vs. Sparse BM25 vs. Hybrid RRF retrieval."""

    query: str = Field(..., min_length=3)
    top_k: int = Field(default=5, ge=1, le=10)
    jurisdiction_filter: str = Field(default="ALL")


# Singleton application services initialized on startup
etl_pipeline = RegulatoryETLPipeline()
compliance_workflow = AgenticComplianceWorkflow(retriever=etl_pipeline.retriever)
rag_evaluator = ComplianceRAGEvaluator(workflow=compliance_workflow)


def ensure_pipeline_initialized() -> IngestionReport:
    """Ensure the regulatory corpus has been ingested into Qdrant."""
    if not etl_pipeline.retriever.chunks_list or etl_pipeline.last_report is None:
        return etl_pipeline.run_directory_ingestion()
    return etl_pipeline.last_report


@asynccontextmanager
async def lifespan(_: FastAPI):
    ensure_pipeline_initialized()
    yield


app = FastAPI(
    title="Nasdaq & SEC Regulatory Compliance Agentic RAG API",
    description=(
        "Enterprise Data Engineering Pipeline, Qdrant Hybrid Vector + BM25 RRF Search, "
        "and 6-Node LangGraph Agentic Verification for Financial Market Regulations."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_HTML_PATH = Path(__file__).resolve().parent.parent / "frontend" / "index.html"


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_dashboard() -> HTMLResponse:
    """Serve the interactive Nasdaq Regulatory Compliance Intelligence Dashboard."""
    ensure_pipeline_initialized()
    if FRONTEND_HTML_PATH.exists():
        return HTMLResponse(content=FRONTEND_HTML_PATH.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Dashboard HTML not found</h1>", status_code=404)


@app.get("/api/v1/health")
async def get_system_health() -> Dict[str, Any]:
    """Return system telemetry, ETL pipeline metrics, Qdrant index stats, and active LLM backend."""
    report = ensure_pipeline_initialized()
    return {
        "status": "OPERATIONAL",
        "llm_backend": settings.active_llm_backend(),
        "langgraph_engine": "LangGraph StateGraph (Native)" if LANGGRAPH_AVAILABLE else "LangGraph State Machine",
        "qdrant_backend": etl_pipeline.retriever.qdrant_backend_mode,
        "qdrant_collection": etl_pipeline.retriever.collection_name,
        "embedding_dimension": settings.embedding_dim,
        "etl_telemetry": report.model_dump(),
    }


@app.post("/api/v1/compliance/query", response_model=ComplianceQueryResponse)
async def run_compliance_query(request: ComplianceQueryRequest) -> ComplianceQueryResponse:
    """Execute the 6-node LangGraph Agentic Compliance Verification workflow."""
    ensure_pipeline_initialized()
    return compliance_workflow.run(request)


@app.post("/api/v1/compliance/audit-scenario", response_model=ComplianceQueryResponse)
async def run_scenario_audit(scenario: ScenarioAuditRequest) -> ComplianceQueryResponse:
    """Audit a structured trade, market access, listing, or cybersecurity scenario."""
    ensure_pipeline_initialized()
    param_str = (
        " | Parameters: " + ", ".join(f"{k}={v}" for k, v in scenario.parameters.items())
        if scenario.parameters
        else ""
    )
    composed_query = (
        f"[SCENARIO AUDIT: {scenario.scenario_title} | Entity: {scenario.entity_type}] "
        f"{scenario.scenario_description}{param_str}"
    )
    req = ComplianceQueryRequest(
        query=composed_query,
        jurisdiction_filter=scenario.jurisdiction_filter,
        top_k=6,
        enable_self_rag_rewrite=True,
    )
    return compliance_workflow.run(req)


@app.get("/api/v1/corpus/documents")
async def list_corpus_documents(
    doc_id: Optional[str] = Query(default=None),
    jurisdiction: Optional[str] = Query(default=None),
) -> Dict[str, Any]:
    """Inspect indexed regulatory documents, statutory chunks, obligation tags, and citations."""
    ensure_pipeline_initialized()
    docs = list(etl_pipeline.documents_meta.values())
    chunks = etl_pipeline.retriever.chunks_list

    if doc_id:
        chunks = [c for c in chunks if c.doc_id.upper() == doc_id.upper()]
    if jurisdiction and jurisdiction.upper() != "ALL":
        chunks = [c for c in chunks if c.jurisdiction.upper() == jurisdiction.upper()]

    return {
        "total_documents": len(docs),
        "documents": [d.model_dump() for d in docs],
        "filtered_chunks_count": len(chunks),
        "chunks": [c.model_dump() for c in chunks],
    }


@app.post("/api/v1/retrieval/compare")
async def compare_retrieval_modalities(req: ModalityCompareRequest) -> Dict[str, Any]:
    """
    Compare Dense Semantic Search vs. Sparse Okapi BM25 vs. Hybrid RRF + Citation Boost
    side-by-side for a regulatory query.
    """
    ensure_pipeline_initialized()
    hits = etl_pipeline.retriever.search(
        query=req.query,
        top_k=max(req.top_k, 8),
        jurisdiction_filter=req.jurisdiction_filter,
        expand_cross_references=True,
    )

    dense_sorted = sorted(hits, key=lambda h: h.dense_score, reverse=True)[: req.top_k]
    sparse_sorted = sorted(hits, key=lambda h: h.sparse_bm25_score, reverse=True)[: req.top_k]
    hybrid_sorted = sorted(hits, key=lambda h: h.rrf_score, reverse=True)[: req.top_k]

    return {
        "query": req.query,
        "hybrid_rrf_ranking": [h.model_dump() for h in hybrid_sorted],
        "dense_only_ranking": [h.model_dump() for h in dense_sorted],
        "sparse_bm25_ranking": [h.model_dump() for h in sparse_sorted],
    }


@app.post("/api/v1/pipeline/ingest", response_model=IngestionReport)
async def ingest_custom_document(payload: CustomIngestRequest) -> IngestionReport:
    """Ingest a new Markdown regulatory document or policy manual into Qdrant."""
    ensure_pipeline_initialized()
    try:
        return etl_pipeline.ingest_custom_document(
            raw_markdown=payload.markdown_content,
            filename=payload.filename,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Ingestion failed: {exc}") from exc


@app.get("/api/v1/eval/latest", response_model=EvalSuiteSummary)
async def get_latest_evaluation() -> EvalSuiteSummary:
    """Return the latest saved RAG evaluation benchmark report, or run it if not yet generated."""
    ensure_pipeline_initialized()
    json_path = settings.eval_output_dir / "latest_benchmark_report.json"
    if json_path.exists():
        data = json.loads(json_path.read_text(encoding="utf-8"))
        return EvalSuiteSummary(**data)
    return rag_evaluator.run_benchmark(save_artifacts=True)


@app.post("/api/v1/eval/run", response_model=EvalSuiteSummary)
async def trigger_evaluation_run() -> EvalSuiteSummary:
    """Execute the 10-case golden compliance RAG benchmark suite live."""
    ensure_pipeline_initialized()
    return rag_evaluator.run_benchmark(save_artifacts=True)

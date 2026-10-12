"""
Pydantic v2 data models and schemas for the Regulatory Compliance & Policy Agentic RAG System.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class Jurisdiction(str, Enum):
    """Regulatory bodies covered by the compliance system."""

    SEC = "SEC"
    NASDAQ = "NASDAQ"
    FINRA_NASDAQ = "FINRA_NASDAQ"
    ALL = "ALL"


class ObligationType(str, Enum):
    """Classification of statutory strength within a regulatory clause."""

    MANDATORY_OBLIGATION = "MANDATORY_OBLIGATION"
    PROHIBITION = "PROHIBITION"
    EXEMPTION_SAFE_HARBOR = "EXEMPTION_SAFE_HARBOR"
    REPORTING_DISCLOSURE = "REPORTING_DISCLOSURE"
    DEFINITIONAL = "DEFINITIONAL"


class ComplianceStatus(str, Enum):
    """Outcome determination for a compliance verification query or trade audit."""

    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    CONDITIONAL_REVIEW = "CONDITIONAL_REVIEW"
    INFORMATIONAL = "INFORMATIONAL"


class DocumentMetadata(BaseModel):
    """Structured metadata parsed from regulatory document headers."""

    doc_id: str
    title: str
    jurisdiction: str
    citation_prefix: str
    effective_date: str
    last_amended: str
    category: str
    source_filename: str


class RegulatoryChunk(BaseModel):
    """A hierarchically parsed, context-enriched regulatory chunk indexed in Qdrant."""

    chunk_id: str = Field(..., description="Human-readable identifier e.g. SEC-15C3-5::chunk-03")
    chunk_uuid: str = Field(..., description="Deterministic UUIDv5 derived from content_hash for Qdrant")
    doc_id: str
    doc_title: str
    jurisdiction: str
    category: str
    section_title: str
    subsection_title: str
    breadcrumb: str = Field(..., description="Full statutory hierarchy path")
    primary_citation: str = Field(..., description="Primary statutory citation for this clause")
    citations_extracted: List[str] = Field(default_factory=list, description="All citations and cross-references")
    obligation_type: ObligationType = ObligationType.MANDATORY_OBLIGATION
    numeric_thresholds: List[str] = Field(default_factory=list, description="Extracted numeric/temporal thresholds")
    text: str = Field(..., description="Raw statutory text of the section/clause")
    contextualized_text: str = Field(
        ..., description="Breadcrumb-prefixed text used for dense & sparse indexing"
    )
    content_hash: str = Field(..., description="SHA-256 digest for idempotent ETL deduplication")
    char_count: int = 0
    token_estimate: int = 0
    effective_date: str = ""
    last_amended: str = ""


class IngestionReport(BaseModel):
    """Data engineering pipeline telemetry returned after running regulatory ETL."""

    documents_processed: int
    total_chunks_created: int
    unique_citations_indexed: int
    cross_reference_edges: int
    jurisdiction_breakdown: Dict[str, int]
    obligation_breakdown: Dict[str, int]
    qdrant_collection: str
    qdrant_backend_mode: str
    elapsed_ms: float
    content_hashes: List[str] = Field(default_factory=list)


class RetrievalHit(BaseModel):
    """A single retrieved regulatory clause with Hybrid RRF score decomposition."""

    chunk_id: str
    doc_id: str
    doc_title: str
    jurisdiction: str
    category: str
    breadcrumb: str
    primary_citation: str
    citations_extracted: List[str]
    obligation_type: str
    numeric_thresholds: List[str]
    text: str
    rrf_score: float = Field(..., description="Combined Reciprocal Rank Fusion + Reranker score")
    dense_score: float = Field(..., description="Cosine similarity score from dense embeddings")
    sparse_bm25_score: float = Field(..., description="Normalized Okapi BM25 lexical score")
    citation_match_boost: float = Field(..., description="Exact statutory citation & threshold match boost")
    is_cross_ref_expanded: bool = Field(
        default=False, description="True if pulled via cross-reference graph expansion"
    )
    relevance_grade: str = Field(default="RELEVANT", description="Self-RAG evidence grade")


class AgentNodeTrace(BaseModel):
    """Execution telemetry for a single node in the LangGraph compliance workflow."""

    node_name: str
    status: str = "COMPLETED"
    duration_ms: float
    summary: str
    details: Dict[str, Any] = Field(default_factory=dict)


class CitationAuditItem(BaseModel):
    """Verification record for a statutory citation checked by the Hallucination Auditor."""

    citation: str
    verified_in_corpus: bool
    source_chunk_id: Optional[str] = None
    source_doc_id: Optional[str] = None
    matching_excerpt: Optional[str] = None


class ComplianceQueryRequest(BaseModel):
    """API request payload for compliance query or policy verification."""

    query: str = Field(..., min_length=5, description="Regulatory question or compliance scenario")
    jurisdiction_filter: Optional[str] = Field(
        default="ALL", description="Optional filter: ALL, SEC, NASDAQ, FINRA_NASDAQ"
    )
    top_k: int = Field(default=6, ge=2, le=15)
    enable_self_rag_rewrite: bool = Field(default=True)


class ScenarioAuditRequest(BaseModel):
    """Structured trade or corporate event scenario for automated compliance auditing."""

    scenario_title: str
    entity_type: str = Field(default="Broker-Dealer / Nasdaq Member", description="Entity under review")
    scenario_description: str = Field(..., min_length=10)
    jurisdiction_filter: str = Field(default="ALL")
    parameters: Dict[str, Any] = Field(default_factory=dict)


class ComplianceQueryResponse(BaseModel):
    """Comprehensive response from the LangGraph Agentic Compliance Verification Engine."""

    query: str
    query_intent: str
    compliance_status: ComplianceStatus = Field(..., description="Compliance determination verdict")
    risk_level: str = Field(..., description="CRITICAL, HIGH, MEDIUM, LOW, or INFORMATIONAL")

    @property
    def Compliance_status(self) -> ComplianceStatus:
        return self.compliance_status
    executive_summary: str
    regulatory_analysis: str
    applicable_rules: List[str]
    violated_or_triggered_clauses: List[str]
    remediation_actions: List[str]
    retrieved_chunks: List[RetrievalHit]
    citation_audit: List[CitationAuditItem]
    faithfulness_score: float
    citation_precision: float
    evidence_sufficiency_score: float
    query_rewritten: bool = False
    rewritten_queries: List[str] = Field(default_factory=list)
    agent_trace: List[AgentNodeTrace]
    llm_backend: str
    total_latency_ms: float

    model_config = {"populate_by_name": True}


class EvalCaseResult(BaseModel):
    """Evaluation metrics for a single golden benchmark compliance test case."""

    case_id: str
    category: str
    query: str
    expected_status: str
    predicted_status: str
    status_correct: bool
    expected_citations: List[str]
    retrieved_citations: List[str]
    context_recall: float
    context_precision: float
    faithfulness_score: float
    citation_accuracy: float
    latency_ms: float


class EvalSuiteSummary(BaseModel):
    """Aggregated RAGAS-style evaluation benchmark report."""

    total_cases: int
    mean_context_recall: float
    mean_context_precision: float
    mean_faithfulness: float
    mean_citation_accuracy: float
    verdict_accuracy: float
    p50_latency_ms: float
    p95_latency_ms: float
    llm_backend: str
    qdrant_collection: str
    case_results: List[EvalCaseResult]

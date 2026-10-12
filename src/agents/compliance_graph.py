"""
LangGraph 6-Node Agentic Regulatory Compliance & Policy Verification Engine.

Graph Topology:
    [START]
       │
       ▼
  ┌────────────────────┐
  │ 1. query_analyzer  │  (Intent classification, jurisdiction routing & sub-query decomposition)
  └─────────┬──────────┘
            │
            ▼
  ┌────────────────────┐
  │ 2. hybrid_retriever│◄─────────────────┐ (Qdrant Dense + BM25 Sparse + RRF + Cross-Ref Graph)
  └─────────┬──────────┘                  │
            │                             │
            ▼                             │ (Conditional Corrective Edge if sufficiency < threshold)
  ┌────────────────────┐      ┌───────────┴──────────┐
  │ 3. evidence_grader │─────►│  4. query_rewriter   │ (Colloquial-to-statutory terminology expansion)
  └─────────┬──────────┘      └──────────────────────┘
            │ (Sufficient evidence)
            ▼
  ┌──────────────────────┐
  │5. compliance_verifier│ (Grounded regulatory synthesis & scenario audit determination)
  └─────────┬────────────┘
            │
            ▼
  ┌──────────────────────┐
  │6. hallucination_audit│ (Deterministic citation verification & faithfulness scoring)
  └─────────┬────────────┘
            │
            ▼
          [END]
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, TypedDict

from src.llm.provider import ComplianceLLMProvider
from src.models.schemas import (
    AgentNodeTrace,
    CitationAuditItem,
    ComplianceQueryRequest,
    ComplianceQueryResponse,
    ComplianceStatus,
    RetrievalHit,
)
from src.pipeline.chunker import RegulatoryHierarchicalChunker
from src.retrieval.qdrant_store import QdrantHybridRetriever

try:
    from langgraph.graph import END, START, StateGraph

    LANGGRAPH_AVAILABLE = True
except Exception:
    LANGGRAPH_AVAILABLE = False


# Statutory terminology expansion map for Self-RAG Query Rewriter
REGULATORY_QUERY_EXPANSIONS: List[tuple[List[str], str]] = [
    (
        ["naked access", "unfiltered", "sponsored access", "mpid", "fat finger", "fat-finger", "credit limit", "erroneous order", "price collar", "modify or disable"],
        "17 CFR § 240.15c3-5(b) 15c3-5(c)(1)(i) 15c3-5(c)(1)(ii) 15c3-5(d)(1) pre-trade financial credit thresholds erroneous order collars direct and exclusive control",
    ),
    (
        ["naked short", "fail to deliver", "ftd", "locate", "penalty box", "short sale", "uptick", "mark long"],
        "SEC Regulation SHO 17 CFR § 242.200(g) order marking Rule 201 10% circuit breaker Rule 203(b)(1) locate Rule 204(a) T+2 close-out",
    ),
    (
        ["trade through", "trade-through", "iso", "intermarket sweep", "sub-penny", "access fee", "locked", "cat"],
        "SEC Regulation NMS 17 CFR § 242.611 Order Protection Rule 611(b)(6) ISO full displayed size Rule 610 30 mils Rule 612 Rule 613 CAT",
    ),
    (
        ["under a dollar", "below $1", "bid price", "delisting", "reverse split", "reverse stock split", "180 days", "ten cents"],
        "Nasdaq Rule 5450(a)(1) Rule 5550(a)(2) Rule 5810(c)(3)(A) $1.00 minimum bid price 30 consecutive business days 180 calendar days $0.10 250 shares",
    ),
    (
        ["cyber", "ransomware", "breach", "hack", "incident", "8-k", "10-k", "material weakness", "icfr"],
        "SEC Form 8-K Item 1.05 4 business days materiality determination Attorney General Form 10-K Item 1C Nasdaq IM-5250-1 10 minutes MarketWatch SOX Section 404",
    ),
    (
        ["spoofing", "layering", "wash trade", "kill switch", "kill-switch", "algo", "best execution", "pfof", "aml", "sar"],
        "Nasdaq General 9 Section 1 SMARTS spoofing layering FINRA Rule 3110 RN 15-09 Series 57 FINRA Rule 5310 best execution FINRA Rule 3310 AML SAR $5,000",
    ),
]


class ComplianceGraphState(TypedDict, total=False):
    """Typed state dictionary passed across nodes in the LangGraph compliance state machine."""

    original_query: str
    active_query: str
    sub_queries: List[str]
    jurisdiction_filter: str
    top_k: int
    enable_self_rag_rewrite: bool
    query_intent: str
    detected_citations: List[str]
    retrieved_hits: List[RetrievalHit]
    evidence_sufficiency_score: float
    rewrite_count: int
    query_rewritten: bool
    rewritten_queries: List[str]
    synthesis_output: Dict[str, Any]
    citation_audit: List[CitationAuditItem]
    faithfulness_score: float
    citation_precision: float
    agent_trace: List[AgentNodeTrace]


class AgenticComplianceWorkflow:
    """
    LangGraph-orchestrated 6-node Agentic RAG system for financial regulatory compliance verification.
    """

    def __init__(
        self,
        retriever: QdrantHybridRetriever,
        llm_provider: Optional[ComplianceLLMProvider] = None,
    ) -> None:
        self.retriever = retriever
        self.llm = llm_provider or ComplianceLLMProvider()
        self.compiled_graph = self._build_langgraph() if LANGGRAPH_AVAILABLE else None

    def _build_langgraph(self) -> Any:
        """Construct and compile the LangGraph StateGraph workflow."""
        workflow = StateGraph(ComplianceGraphState)

        workflow.add_node("query_analyzer", self.node_query_analyzer)
        workflow.add_node("hybrid_retriever", self.node_hybrid_retriever)
        workflow.add_node("evidence_grader", self.node_evidence_grader)
        workflow.add_node("query_rewriter", self.node_query_rewriter)
        workflow.add_node("compliance_verifier", self.node_compliance_verifier)
        workflow.add_node("hallucination_auditor", self.node_hallucination_auditor)

        workflow.add_edge(START, "query_analyzer")
        workflow.add_edge("query_analyzer", "hybrid_retriever")
        workflow.add_edge("hybrid_retriever", "evidence_grader")

        workflow.add_conditional_edges(
            "evidence_grader",
            self._should_rewrite_query,
            {
                "rewrite": "query_rewriter",
                "verify": "compliance_verifier",
            },
        )
        workflow.add_edge("query_rewriter", "hybrid_retriever")
        workflow.add_edge("compliance_verifier", "hallucination_auditor")
        workflow.add_edge("hallucination_auditor", END)

        return workflow.compile()

    @staticmethod
    def _should_rewrite_query(state: ComplianceGraphState) -> str:
        """Conditional edge deciding whether to trigger the Self-RAG Query Rewriter loop."""
        if not state.get("enable_self_rag_rewrite", True):
            return "verify"
        if state.get("rewrite_count", 0) >= 1:
            return "verify"
        sufficiency = state.get("evidence_sufficiency_score", 1.0)
        # Trigger corrective rewrite if sufficiency is below 0.78 or no explicit statutory citation was in the query
        if sufficiency < 0.78:
            return "rewrite"
        return "verify"

    # -------------------------------------------------------------------------
    # Node 1: Query Analyzer & Intent Router
    # -------------------------------------------------------------------------
    def node_query_analyzer(self, state: ComplianceGraphState) -> Dict[str, Any]:
        t0 = time.perf_counter()
        query = state["original_query"]
        q_lower = query.lower()

        detected_citations = RegulatoryHierarchicalChunker.extract_citations(query)

        if any(k in q_lower for k in ["violation", "compliant", "audit", "scenario", "allowed", "can a", "if a broker", "without", "failed to"]):
            intent = "TRADE_AND_SCENARIO_COMPLIANCE_AUDIT"
        elif any(k in q_lower for k in ["delist", "bid price", "$1.00", "5450", "5550", "5810", "audit committee", "5605"]):
            intent = "EXCHANGE_LISTING_QUALIFICATION_VERIFICATION"
        elif any(k in q_lower for k in ["8-k", "10-k", "item 1.05", "cyber", "icfr", "sox", "marketwatch"]):
            intent = "ISSUER_FILING_AND_DISCLOSURE_VERIFICATION"
        else:
            intent = "REGULATORY_POLICY_AND_THRESHOLD_LOOKUP"

        # Decompose compound questions into focused sub-queries
        sub_queries = [query]
        if " and " in q_lower and len(query) > 90:
            parts = [p.strip() for p in query.split(" and ") if len(p.strip()) > 25]
            if len(parts) >= 2:
                sub_queries.extend(parts[:2])

        dur_ms = round((time.perf_counter() - t0) * 1000.0, 2)
        trace = list(state.get("agent_trace", []))
        trace.append(
            AgentNodeTrace(
                node_name="1. query_analyzer",
                status="COMPLETED",
                duration_ms=dur_ms,
                summary=f"Classified intent as '{intent}'; extracted {len(detected_citations)} explicit citations and {len(sub_queries)} search query vector(s).",
                details={
                    "intent": intent,
                    "detected_citations": detected_citations,
                    "sub_queries_count": len(sub_queries),
                    "jurisdiction_filter": state.get("jurisdiction_filter", "ALL"),
                },
            )
        )
        return {
            "query_intent": intent,
            "detected_citations": detected_citations,
            "sub_queries": sub_queries,
            "active_query": query,
            "agent_trace": trace,
        }

    # -------------------------------------------------------------------------
    # Node 2: Qdrant Hybrid Retriever (Dense + BM25 Sparse + RRF + Cross-Ref)
    # -------------------------------------------------------------------------
    def node_hybrid_retriever(self, state: ComplianceGraphState) -> Dict[str, Any]:
        t0 = time.perf_counter()
        top_k = state.get("top_k", 6)
        jur_filter = state.get("jurisdiction_filter", "ALL")
        queries_to_run = [state.get("active_query", state["original_query"])] + state.get("sub_queries", [])

        # Deduplicate queries while preserving order
        seen_q = set()
        unique_queries = []
        for q in queries_to_run:
            if q not in seen_q:
                seen_q.add(q)
                unique_queries.append(q)

        merged_hits: Dict[str, RetrievalHit] = {}
        for q in unique_queries:
            hits = self.retriever.search(
                query=q,
                top_k=top_k,
                jurisdiction_filter=jur_filter,
                expand_cross_references=True,
            )
            for h in hits:
                if h.chunk_id not in merged_hits or h.rrf_score > merged_hits[h.chunk_id].rrf_score:
                    merged_hits[h.chunk_id] = h

        sorted_hits = sorted(merged_hits.values(), key=lambda x: x.rrf_score, reverse=True)[:top_k]

        dur_ms = round((time.perf_counter() - t0) * 1000.0, 2)
        cross_ref_count = sum(1 for h in sorted_hits if h.is_cross_ref_expanded)
        trace = list(state.get("agent_trace", []))
        trace.append(
            AgentNodeTrace(
                node_name="2. hybrid_retriever",
                status="COMPLETED",
                duration_ms=dur_ms,
                summary=(
                    f"Retrieved {len(sorted_hits)} statutory chunks via Qdrant Dense + BM25 Sparse RRF "
                    f"(Top RRF: {sorted_hits[0].rrf_score if sorted_hits else 0.0:.3f}, Cross-Ref Expanded: {cross_ref_count})."
                ),
                details={
                    "chunks_retrieved": [h.chunk_id for h in sorted_hits],
                    "top_primary_citations": [h.primary_citation for h in sorted_hits[:3]],
                    "top_rrf_score": sorted_hits[0].rrf_score if sorted_hits else 0.0,
                    "cross_ref_expanded_chunks": cross_ref_count,
                },
            )
        )
        return {
            "retrieved_hits": sorted_hits,
            "agent_trace": trace,
        }

    # -------------------------------------------------------------------------
    # Node 3: Self-RAG / CRAG Evidence Grader
    # -------------------------------------------------------------------------
    def node_evidence_grader(self, state: ComplianceGraphState) -> Dict[str, Any]:
        t0 = time.perf_counter()
        hits = state.get("retrieved_hits", [])
        detected_cits = state.get("detected_citations", [])

        graded_hits: List[RetrievalHit] = []
        high_conf_count = 0
        for h in hits:
            if h.rrf_score >= 0.42 or h.is_cross_ref_expanded:
                h.relevance_grade = "HIGHLY_RELEVANT"
                high_conf_count += 1
            elif h.rrf_score >= 0.25:
                h.relevance_grade = "RELEVANT"
            else:
                h.relevance_grade = "MARGINAL"
            graded_hits.append(h)

        top3_mean = (
            sum(h.rrf_score for h in graded_hits[:3]) / min(3, len(graded_hits))
            if graded_hits
            else 0.0
        )
        # If the user did not supply formal statutory citations on pass 0, trigger Self-RAG expansion if top3_mean < 0.78
        citation_bonus = 0.18 if detected_cits or state.get("rewrite_count", 0) > 0 else 0.0
        sufficiency = round(min(0.99, top3_mean * 1.15 + citation_bonus), 4)

        dur_ms = round((time.perf_counter() - t0) * 1000.0, 2)
        trace = list(state.get("agent_trace", []))
        trace.append(
            AgentNodeTrace(
                node_name="3. evidence_grader",
                status="COMPLETED",
                duration_ms=dur_ms,
                summary=(
                    f"Self-RAG Evidence Sufficiency Score: {sufficiency:.2f} "
                    f"({high_conf_count}/{len(graded_hits)} chunks graded HIGHLY_RELEVANT)."
                ),
                details={
                    "evidence_sufficiency_score": sufficiency,
                    "highly_relevant_chunks": high_conf_count,
                    "decision": "rewrite" if (sufficiency < 0.78 and state.get("rewrite_count", 0) == 0 and state.get("enable_self_rag_rewrite", True)) else "verify",
                },
            )
        )
        return {
            "retrieved_hits": graded_hits,
            "evidence_sufficiency_score": sufficiency,
            "agent_trace": trace,
        }

    # -------------------------------------------------------------------------
    # Node 4: Corrective Query Rewriter (Self-RAG Loop)
    # -------------------------------------------------------------------------
    def node_query_rewriter(self, state: ComplianceGraphState) -> Dict[str, Any]:
        t0 = time.perf_counter()
        orig_q = state["original_query"]
        q_lower = orig_q.lower()

        expansions_applied: List[str] = []
        for triggers, statutory_terms in REGULATORY_QUERY_EXPANSIONS:
            if any(trig in q_lower for trig in triggers):
                expansions_applied.append(statutory_terms)

        if not expansions_applied:
            expansions_applied.append(
                "17 CFR § 240.15c3-5 SEC Regulation SHO Rule 203 Rule 204 Regulation NMS Rule 611 Nasdaq Rule 5000 Form 8-K Item 1.05"
            )

        rewritten_query = f"{orig_q} | Statutory Context: {' ; '.join(expansions_applied)}"
        prev_rewrites = list(state.get("rewritten_queries", []))
        prev_rewrites.append(rewritten_query)

        dur_ms = round((time.perf_counter() - t0) * 1000.0, 2)
        trace = list(state.get("agent_trace", []))
        trace.append(
            AgentNodeTrace(
                node_name="4. query_rewriter",
                status="COMPLETED",
                duration_ms=dur_ms,
                summary=f"Expanded query with {len(expansions_applied)} statutory terminology cluster(s) for corrective retrieval pass.",
                details={
                    "rewritten_query": rewritten_query,
                    "expansions_added": expansions_applied,
                },
            )
        )
        return {
            "active_query": rewritten_query,
            "rewrite_count": state.get("rewrite_count", 0) + 1,
            "query_rewritten": True,
            "rewritten_queries": prev_rewrites,
            "agent_trace": trace,
        }

    # -------------------------------------------------------------------------
    # Node 5: Compliance Verifier & Statutory Synthesizer
    # -------------------------------------------------------------------------
    def node_compliance_verifier(self, state: ComplianceGraphState) -> Dict[str, Any]:
        t0 = time.perf_counter()
        hits = state.get("retrieved_hits", [])
        synthesis = self.llm.synthesize_compliance_decision(
            query=state["original_query"],
            query_intent=state.get("query_intent", "REGULATORY_POLICY_LOOKUP"),
            hits=hits,
        )

        dur_ms = round((time.perf_counter() - t0) * 1000.0, 2)
        trace = list(state.get("agent_trace", []))
        trace.append(
            AgentNodeTrace(
                node_name="5. compliance_verifier",
                status="COMPLETED",
                duration_ms=dur_ms,
                summary=(
                    f"Synthesized compliance verdict '{synthesis.get('compliance_status')}' "
                    f"(Risk: {synthesis.get('risk_level')}) citing {len(synthesis.get('applicable_rules', []))} rules."
                ),
                details={
                    "compliance_status": synthesis.get("compliance_status"),
                    "risk_level": synthesis.get("risk_level"),
                    "llm_backend": self.llm.backend_name,
                },
            )
        )
        return {
            "synthesis_output": synthesis,
            "agent_trace": trace,
        }

    # -------------------------------------------------------------------------
    # Node 6: Hallucination & Statutory Citation Auditor
    # -------------------------------------------------------------------------
    def node_hallucination_auditor(self, state: ComplianceGraphState) -> Dict[str, Any]:
        t0 = time.perf_counter()
        synthesis = state.get("synthesis_output", {})
        hits = state.get("retrieved_hits", [])

        combined_output_text = " ".join(
            [
                str(synthesis.get("executive_summary", "")),
                str(synthesis.get("regulatory_analysis", "")),
                " ".join(synthesis.get("applicable_rules", [])),
                " ".join(synthesis.get("violated_or_triggered_clauses", [])),
                " ".join(synthesis.get("remediation_actions", [])),
            ]
        )

        extracted_output_cits = RegulatoryHierarchicalChunker.extract_citations(combined_output_text)
        audit_items: List[CitationAuditItem] = []
        verified_count = 0

        for cit in extracted_output_cits:
            norm_cit = self.retriever._normalize_citation_key(cit)
            matched_chunk: Optional[RetrievalHit] = None

            # Check against retrieved hits first
            for h in hits:
                all_h_cits = [h.primary_citation] + h.citations_extracted
                if (
                    cit.lower() in h.text.lower()
                    or cit.lower() in h.primary_citation.lower()
                    or any(
                        norm_cit in self.retriever._normalize_citation_key(hc)
                        or self.retriever._normalize_citation_key(hc) in norm_cit
                        for hc in all_h_cits
                    )
                ):
                    matched_chunk = h
                    break

            # Fallback check against global Qdrant citation graph
            if matched_chunk is None:
                linked_ids = self.retriever.citation_to_chunks.get(norm_cit, set())
                if linked_ids:
                    first_cid = next(iter(linked_ids))
                    ch_obj = self.retriever.chunks_by_id.get(first_cid)
                    if ch_obj:
                        verified_count += 1
                        audit_items.append(
                            CitationAuditItem(
                                citation=cit,
                                verified_in_corpus=True,
                                source_chunk_id=ch_obj.chunk_id,
                                source_doc_id=ch_obj.doc_id,
                                matching_excerpt=ch_obj.text[:160] + "...",
                            )
                        )
                        continue

            if matched_chunk is not None:
                verified_count += 1
                audit_items.append(
                    CitationAuditItem(
                        citation=cit,
                        verified_in_corpus=True,
                        source_chunk_id=matched_chunk.chunk_id,
                        source_doc_id=matched_chunk.doc_id,
                        matching_excerpt=matched_chunk.text[:160] + "...",
                    )
                )
            else:
                audit_items.append(
                    CitationAuditItem(
                        citation=cit,
                        verified_in_corpus=False,
                    )
                )

        citation_precision = (
            round(verified_count / len(audit_items), 4) if audit_items else 1.0
        )
        faithfulness = round(
            min(1.0, 0.65 * citation_precision + 0.35 * state.get("evidence_sufficiency_score", 0.9)),
            4,
        )

        dur_ms = round((time.perf_counter() - t0) * 1000.0, 2)
        trace = list(state.get("agent_trace", []))
        trace.append(
            AgentNodeTrace(
                node_name="6. hallucination_auditor",
                status="COMPLETED",
                duration_ms=dur_ms,
                summary=(
                    f"Audited {len(audit_items)} statutory citations: {verified_count}/{len(audit_items)} verified "
                    f"(Citation Precision: {citation_precision * 100:.1f}%, Faithfulness: {faithfulness * 100:.1f}%)."
                ),
                details={
                    "citations_checked": len(audit_items),
                    "citations_verified": verified_count,
                    "citation_precision": citation_precision,
                    "faithfulness_score": faithfulness,
                },
            )
        )
        return {
            "citation_audit": audit_items,
            "citation_precision": citation_precision,
            "faithfulness_score": faithfulness,
            "agent_trace": trace,
        }

    # -------------------------------------------------------------------------
    # Public Execution Entrypoint
    # -------------------------------------------------------------------------
    def run(self, request: ComplianceQueryRequest) -> ComplianceQueryResponse:
        """Execute the 6-node LangGraph compliance workflow and return full audit response."""
        t_start = time.perf_counter()

        initial_state: ComplianceGraphState = {
            "original_query": request.query,
            "active_query": request.query,
            "sub_queries": [request.query],
            "jurisdiction_filter": request.jurisdiction_filter or "ALL",
            "top_k": request.top_k,
            "enable_self_rag_rewrite": request.enable_self_rag_rewrite,
            "rewrite_count": 0,
            "query_rewritten": False,
            "rewritten_queries": [],
            "agent_trace": [],
        }

        if self.compiled_graph is not None:
            final_state = self.compiled_graph.invoke(initial_state)
        else:
            # Sequential execution fallback matching exact LangGraph topology
            state = dict(initial_state)
            state.update(self.node_query_analyzer(state))
            state.update(self.node_hybrid_retriever(state))
            state.update(self.node_evidence_grader(state))
            if self._should_rewrite_query(state) == "rewrite":
                state.update(self.node_query_rewriter(state))
                state.update(self.node_hybrid_retriever(state))
                state.update(self.node_evidence_grader(state))
            state.update(self.node_compliance_verifier(state))
            state.update(self.node_hallucination_auditor(state))
            final_state = state

        synthesis = final_state.get("synthesis_output", {})
        raw_status = str(synthesis.get("compliance_status", "INFORMATIONAL")).upper()
        try:
            comp_status = ComplianceStatus(raw_status)
        except ValueError:
            comp_status = ComplianceStatus.INFORMATIONAL

        total_latency_ms = round((time.perf_counter() - t_start) * 1000.0, 2)

        return ComplianceQueryResponse(
            query=request.query,
            query_intent=final_state.get("query_intent", "REGULATORY_POLICY_LOOKUP"),
            compliance_status=comp_status,
            risk_level=str(synthesis.get("risk_level", "INFORMATIONAL")),
            executive_summary=str(synthesis.get("executive_summary", "")),
            regulatory_analysis=str(synthesis.get("regulatory_analysis", "")),
            applicable_rules=list(synthesis.get("applicable_rules", [])),
            violated_or_triggered_clauses=list(synthesis.get("violated_or_triggered_clauses", [])),
            remediation_actions=list(synthesis.get("remediation_actions", [])),
            retrieved_chunks=final_state.get("retrieved_hits", []),
            citation_audit=final_state.get("citation_audit", []),
            faithfulness_score=float(final_state.get("faithfulness_score", 0.95)),
            citation_precision=float(final_state.get("citation_precision", 1.0)),
            evidence_sufficiency_score=float(final_state.get("evidence_sufficiency_score", 0.90)),
            query_rewritten=bool(final_state.get("query_rewritten", False)),
            rewritten_queries=list(final_state.get("rewritten_queries", [])),
            agent_trace=final_state.get("agent_trace", []),
            llm_backend=self.llm.backend_name,
            total_latency_ms=total_latency_ms,
        )

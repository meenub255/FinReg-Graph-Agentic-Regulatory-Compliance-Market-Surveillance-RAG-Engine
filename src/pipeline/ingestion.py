"""
Scalable Data Engineering ETL Pipeline for Financial Regulatory Documents.

Handles:
1. Automated discovery and ingestion of SEC, Nasdaq, and FINRA regulatory corpora.
2. Structure-aware AST chunking with parent-child statutory breadcrumbs.
3. Idempotent SHA-256 content hashing and deduplication.
4. Qdrant vector + payload indexing and BM25 sparse lexical indexing.
5. Pipeline telemetry & obligation/jurisdiction distribution reporting.
"""

from __future__ import annotations

import time
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional

from src.config import settings
from src.models.schemas import DocumentMetadata, IngestionReport, RegulatoryChunk
from src.pipeline.chunker import RegulatoryHierarchicalChunker
from src.retrieval.qdrant_store import QdrantHybridRetriever


class RegulatoryETLPipeline:
    """End-to-end ETL pipeline for regulatory compliance documents."""

    def __init__(
        self,
        retriever: Optional[QdrantHybridRetriever] = None,
        chunker: Optional[RegulatoryHierarchicalChunker] = None,
    ) -> None:
        self.retriever = retriever or QdrantHybridRetriever()
        self.chunker = chunker or RegulatoryHierarchicalChunker(
            max_chunk_chars=settings.max_chunk_chars,
            overlap_chars=settings.chunk_overlap_chars,
        )
        self.documents_meta: Dict[str, DocumentMetadata] = {}
        self.ingested_hashes: set[str] = set()
        self.last_report: Optional[IngestionReport] = None

    def run_directory_ingestion(self, directory: Optional[Path] = None) -> IngestionReport:
        """Ingest all markdown regulatory files from the target directory into Qdrant."""
        start_time = time.perf_counter()
        target_dir = directory or settings.regulations_dir

        md_files = sorted(target_dir.glob("*.md"))
        all_new_chunks: List[RegulatoryChunk] = []

        for file_path in md_files:
            raw_text = file_path.read_text(encoding="utf-8")
            meta, _ = self.chunker.parse_frontmatter(raw_text, file_path.name)
            self.documents_meta[meta.doc_id] = meta

            doc_chunks = self.chunker.chunk_document(raw_text, file_path.name)
            for ch in doc_chunks:
                if ch.content_hash not in self.ingested_hashes:
                    self.ingested_hashes.add(ch.content_hash)
                    all_new_chunks.append(ch)

        if all_new_chunks:
            self.retriever.index_chunks(all_new_chunks)

        elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
        self.last_report = self._build_report(elapsed_ms)
        return self.last_report

    def ingest_custom_document(
        self,
        raw_markdown: str,
        filename: str = "custom_regulation.md",
    ) -> IngestionReport:
        """Ingest a single custom regulatory document or policy manual at runtime."""
        start_time = time.perf_counter()
        meta, _ = self.chunker.parse_frontmatter(raw_markdown, filename)
        self.documents_meta[meta.doc_id] = meta

        doc_chunks = self.chunker.chunk_document(raw_markdown, filename)
        new_chunks: List[RegulatoryChunk] = []
        for ch in doc_chunks:
            if ch.content_hash not in self.ingested_hashes:
                self.ingested_hashes.add(ch.content_hash)
                new_chunks.append(ch)

        if new_chunks:
            self.retriever.index_chunks(new_chunks)

        elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
        self.last_report = self._build_report(elapsed_ms)
        return self.last_report

    def _build_report(self, elapsed_ms: float) -> IngestionReport:
        """Compile pipeline telemetry metrics across all indexed chunks."""
        all_chunks = self.retriever.chunks_list
        jur_counter = Counter(ch.jurisdiction for ch in all_chunks)
        ob_counter = Counter(ch.obligation_type.value for ch in all_chunks)

        unique_cits = set()
        cross_ref_edges = 0
        for ch in all_chunks:
            unique_cits.add(ch.primary_citation)
            for c in ch.citations_extracted:
                unique_cits.add(c)
                cross_ref_edges += 1

        return IngestionReport(
            documents_processed=len(self.documents_meta),
            total_chunks_created=len(all_chunks),
            unique_citations_indexed=len(unique_cits),
            cross_reference_edges=cross_ref_edges,
            jurisdiction_breakdown=dict(jur_counter),
            obligation_breakdown=dict(ob_counter),
            qdrant_collection=self.retriever.collection_name,
            qdrant_backend_mode=self.retriever.qdrant_backend_mode,
            elapsed_ms=elapsed_ms,
            content_hashes=[ch.content_hash[:16] for ch in all_chunks],
        )

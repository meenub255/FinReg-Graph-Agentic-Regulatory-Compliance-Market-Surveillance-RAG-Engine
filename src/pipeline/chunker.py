"""
Hierarchical Regulatory Document Parser & Section-Aware Chunker.

Implements structure-aware AST splitting for SEC, Nasdaq, and FINRA rulebooks:
1. Parses YAML frontmatter metadata (Jurisdiction, Rule ID, Effective Date, Category).
2. Preserves statutory hierarchy breadcrumbs (Document > Section > Subsection) in every chunk.
3. Extracts statutory citations & cross-references (17 CFR, Nasdaq Rule, Reg SHO/NMS, Form 8-K/10-K, FINRA).
4. Classifies regulatory obligation strength (MANDATORY, PROHIBITION, EXEMPTION, REPORTING, DEFINITIONAL).
5. Extracts numeric/temporal thresholds and computes SHA-256 hashes + UUIDv5 for idempotent Qdrant upserts.
"""

from __future__ import annotations

import hashlib
import re
import uuid
from pathlib import Path
from typing import Dict, List, Tuple
import yaml

from src.models.schemas import DocumentMetadata, ObligationType, RegulatoryChunk


# Regex patterns for statutory citations in financial regulations
CITATION_PATTERNS = [
    r"17\s+CFR\s+§+\s*[\d\.a-zA-Z\-]+(?:\([a-zA-Z0-9]+\))*",
    r"31\s+CFR\s+§+\s*[\d\.a-zA-Z\-]+(?:\([a-zA-Z0-9]+\))*",
    r"§+\s*2\d{2}\.[\d\.a-zA-Z\-]+(?:\([a-zA-Z0-9]+\))*",
    r"Rule\s+(?:15c3-5|15c6-1|10A-3|13a-1[45]|20[0134]|600|61[0123])(?:\([a-zA-Z0-9]+\))*",
    r"Nasdaq\s+(?:Equity\s+\d+,\s+)?Rule\s+\d{4}(?:\([a-zA-Z0-9]+\))*",
    r"IM-\d{4}-\d+",
    r"FINRA\s+Rule\s+\d{4}(?:\.\d+|\([a-zA-Z0-9]+\))*",
    r"FINRA\s+RN\s+\d{2}-\d{2}",
    r"Form\s+(?:8-K(?:/A)?|10-K|10-Q|SHO)\s*(?:Item\s+[\d\.]+[A-Z]?)?",
    r"Item\s+(?:1\.05|1C|9A|106|308)(?:\([a-zA-Z0-9]+\))*",
    r"SOX\s+Section\s+(?:302|404)(?:\([a-z]\))?",
    r"Series\s+57",
]

COMBINED_CITATION_REGEX = re.compile("|".join(f"({p})" for p in CITATION_PATTERNS), re.IGNORECASE)

# Regex patterns for numeric & temporal regulatory thresholds
THRESHOLD_REGEX = re.compile(
    r"(?:\$\d+(?:,\d{3})*(?:\.\d+)?(?:\s*(?:per\s+share|million))?|"
    r"\d+(?:\.\d+)?%|"
    r"\b\d+\s+(?:consecutive\s+)?(?:business|calendar|trading|settlement)\s+days?\b|"
    r"\b\d+\s+(?:minutes?|hours?|milliseconds?|microseconds?|years?|months?)\b|"
    r"\bT\+[1234]\b|"
    r"\bS\+[123]\b|"
    r"\b\d+\s+mils\b|"
    r"\b\d+\s+shares\b)",
    re.IGNORECASE,
)


class RegulatoryHierarchicalChunker:
    """
    Section-aware regulatory document parser and hierarchical chunker.
    Prevents mid-clause truncation and preserves full statutory context.
    """

    def __init__(self, max_chunk_chars: int = 1600, overlap_chars: int = 180) -> None:
        self.max_chunk_chars = max_chunk_chars
        self.overlap_chars = overlap_chars

    @staticmethod
    def parse_frontmatter(raw_content: str, filename: str) -> Tuple[DocumentMetadata, str]:
        """Extract YAML frontmatter metadata and body markdown from a regulatory file."""
        frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw_content, re.DOTALL)
        if frontmatter_match:
            yaml_text, body = frontmatter_match.group(1), frontmatter_match.group(2)
            meta_dict = yaml.safe_load(yaml_text) or {}
        else:
            meta_dict, body = {}, raw_content

        metadata = DocumentMetadata(
            doc_id=str(meta_dict.get("doc_id", Path(filename).stem.upper())),
            title=str(meta_dict.get("title", Path(filename).stem)),
            jurisdiction=str(meta_dict.get("jurisdiction", "SEC")),
            citation_prefix=str(meta_dict.get("citation_prefix", "Rule")),
            effective_date=str(meta_dict.get("effective_date", "2024-01-01")),
            last_amended=str(meta_dict.get("last_amended", "2024-06-01")),
            category=str(meta_dict.get("category", "Financial Regulation")),
            source_filename=filename,
        )
        return metadata, body.strip()

    @staticmethod
    def extract_citations(text: str) -> List[str]:
        """Extract and normalize all unique statutory citations and cross-references in text."""
        found: List[str] = []
        seen = set()
        for match in COMBINED_CITATION_REGEX.finditer(text):
            raw_cit = re.sub(r"\s+", " ", match.group(0).strip())
            norm_key = raw_cit.lower()
            if norm_key not in seen:
                seen.add(norm_key)
                found.append(raw_cit)
        return found

    @staticmethod
    def extract_thresholds(text: str) -> List[str]:
        """Extract quantitative and temporal regulatory thresholds (e.g., $1.00, 180 calendar days, T+2)."""
        found: List[str] = []
        seen = set()
        for match in THRESHOLD_REGEX.finditer(text):
            val = re.sub(r"\s+", " ", match.group(0).strip())
            if val.lower() not in seen:
                seen.add(val.lower())
                found.append(val)
        return found

    @staticmethod
    def classify_obligation(section_heading: str, text: str) -> ObligationType:
        """Classify the statutory obligation type of a regulatory chunk."""
        combined = f"{section_heading} {text}".lower()
        if any(k in section_heading.lower() for k in ["definition", "definitions"]):
            return ObligationType.DEFINITIONAL
        if any(
            k in combined
            for k in [
                "exception",
                "exceptions",
                "exempt",
                "shall not apply",
                "permissible allocation",
                "delay exception",
            ]
        ):
            return ObligationType.EXEMPTION_SAFE_HARBOR
        if any(
            k in combined
            for k in [
                "prohibition",
                "prohibited",
                "may not",
                "shall not",
                "not permitted",
                "strictly prohibited",
                "manipulative",
                "spoofing",
            ]
        ):
            return ObligationType.PROHIBITION
        if any(
            k in combined
            for k in [
                "form 8-k",
                "form 10-k",
                "disclosure",
                "report",
                "certification",
                "notify",
                "notification",
                "consolidated audit trail",
                "suspicious activity report",
            ]
        ):
            return ObligationType.REPORTING_DISCLOSURE
        return ObligationType.MANDATORY_OBLIGATION

    def chunk_document(self, raw_content: str, filename: str) -> List[RegulatoryChunk]:
        """
        Parse a regulatory markdown document into hierarchically contextualized chunks.
        Splits along H2 (##) and H3 (###) boundaries, further subdividing only if a clause
        exceeds `max_chunk_chars`.
        """
        metadata, body = self.parse_frontmatter(raw_content, filename)

        lines = body.splitlines()
        h1_title = metadata.title
        current_h2 = "General Provisions"
        current_h3 = ""
        current_lines: List[str] = []

        sections: List[Tuple[str, str, str]] = []  # (h2, h3, body_text)

        def flush_section() -> None:
            text_block = "\n".join(current_lines).strip()
            if text_block:
                sections.append((current_h2, current_h3, text_block))

        for line in lines:
            if line.startswith("# ") and not line.startswith("## "):
                h1_title = line.lstrip("# ").strip()
            elif line.startswith("## ") and not line.startswith("### "):
                flush_section()
                current_h2 = line.lstrip("# ").strip()
                current_h3 = ""
                current_lines = []
            elif line.startswith("### "):
                flush_section()
                current_h3 = line.lstrip("# ").strip()
                current_lines = []
            else:
                current_lines.append(line)

        flush_section()

        chunks: List[RegulatoryChunk] = []
        chunk_idx = 1

        for h2, h3, section_text in sections:
            sub_blocks = self._split_large_block(section_text)
            for sub_text in sub_blocks:
                breadcrumb_parts = [metadata.jurisdiction, h1_title, h2]
                if h3:
                    breadcrumb_parts.append(h3)
                breadcrumb = " > ".join(breadcrumb_parts)

                heading_context = f"{h2} {h3}".strip()
                extracted_cits = self.extract_citations(f"{heading_context}\n{sub_text}")
                primary_citation = extracted_cits[0] if extracted_cits else metadata.citation_prefix

                thresholds = self.extract_thresholds(sub_text)
                obligation = self.classify_obligation(heading_context, sub_text)

                contextualized_text = (
                    f"[{metadata.jurisdiction} | {metadata.doc_id} | {primary_citation}]\n"
                    f"Hierarchy: {breadcrumb}\n"
                    f"Obligation Type: {obligation.value}\n\n"
                    f"{sub_text}"
                )

                content_hash = hashlib.sha256(contextualized_text.encode("utf-8")).hexdigest()
                chunk_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{metadata.doc_id}::{content_hash}"))
                chunk_id = f"{metadata.doc_id}::chunk-{chunk_idx:02d}"

                chunks.append(
                    RegulatoryChunk(
                        chunk_id=chunk_id,
                        chunk_uuid=chunk_uuid,
                        doc_id=metadata.doc_id,
                        doc_title=metadata.title,
                        jurisdiction=metadata.jurisdiction,
                        category=metadata.category,
                        section_title=h2,
                        subsection_title=h3 or h2,
                        breadcrumb=breadcrumb,
                        primary_citation=primary_citation,
                        citations_extracted=extracted_cits,
                        obligation_type=obligation,
                        numeric_thresholds=thresholds,
                        text=sub_text,
                        contextualized_text=contextualized_text,
                        content_hash=content_hash,
                        char_count=len(sub_text),
                        token_estimate=max(1, len(contextualized_text) // 4),
                        effective_date=metadata.effective_date,
                        last_amended=metadata.last_amended,
                    )
                )
                chunk_idx += 1

        return chunks

    def _split_large_block(self, text: str) -> List[str]:
        """Split a section block along paragraph boundaries if it exceeds max_chunk_chars."""
        if len(text) <= self.max_chunk_chars:
            return [text]

        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        blocks: List[str] = []
        current_block: List[str] = []
        current_len = 0

        for para in paragraphs:
            if current_len + len(para) + 2 > self.max_chunk_chars and current_block:
                blocks.append("\n\n".join(current_block))
                # Keep tail overlap paragraph if short enough
                overlap_seed = [current_block[-1]] if len(current_block[-1]) <= self.overlap_chars * 2 else []
                current_block = overlap_seed + [para]
                current_len = sum(len(x) for x in current_block)
            else:
                current_block.append(para)
                current_len += len(para) + 2

        if current_block:
            blocks.append("\n\n".join(current_block))
        return blocks

"""
Centralized configuration for the Regulatory Compliance & Policy RAG System.
Supports Gemini, OpenAI, Groq, and Offline Institutional Mode out of the box.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


@dataclass
class Settings:
    """Application settings loaded from environment variables with safe defaults."""

    # Project paths
    project_root: Path = PROJECT_ROOT
    regulations_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "data" / "regulations")
    eval_output_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "data" / "eval_results")

    # LLM Provider Configuration ("auto", "gemini", "openai", "groq", "offline")
    llm_provider: str = field(default_factory=lambda: os.getenv("LLM_PROVIDER", "auto").lower())
    gemini_api_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    gemini_model: str = field(default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-2.0-flash"))
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    openai_model: str = field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    groq_api_key: str = field(default_factory=lambda: os.getenv("GROQ_API_KEY", ""))
    groq_model: str = field(default_factory=lambda: os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"))

    # Qdrant Vector Database Configuration
    qdrant_url: str = field(default_factory=lambda: os.getenv("QDRANT_URL", ":memory:"))
    qdrant_api_key: str = field(default_factory=lambda: os.getenv("QDRANT_API_KEY", ""))
    qdrant_collection: str = field(
        default_factory=lambda: os.getenv("QDRANT_COLLECTION", "nasdaq_sec_regulatory_corpus")
    )
    embedding_dim: int = 384

    # Hybrid Retrieval & RRF Parameters
    rrf_k: int = 60
    dense_weight: float = 0.45
    sparse_bm25_weight: float = 0.40
    citation_exact_weight: float = 0.15
    default_top_k: int = 6

    # Chunking Pipeline Parameters
    max_chunk_chars: int = 1600
    chunk_overlap_chars: int = 180

    def active_llm_backend(self) -> str:
        """Resolve which LLM backend is active based on configuration and available API keys."""
        if self.llm_provider == "gemini" and self.gemini_api_key:
            return f"Google Gemini ({self.gemini_model})"
        if self.llm_provider == "openai" and self.openai_api_key:
            return f"OpenAI ({self.openai_model})"
        if self.llm_provider == "groq" and self.groq_api_key:
            return f"Groq ({self.groq_model})"
        if self.llm_provider == "auto":
            if self.gemini_api_key:
                return f"Google Gemini ({self.gemini_model})"
            if self.openai_api_key:
                return f"OpenAI ({self.openai_model})"
            if self.groq_api_key:
                return f"Groq ({self.groq_model})"
        return "Deterministic Institutional Regulatory Engine (Offline Ready)"


settings = Settings()

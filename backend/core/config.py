"""
core/config.py — Centralized configuration for PhishGuard AI.
Uses pydantic-settings for environment variable validation and .env support.
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application-wide settings loaded from environment variables and .env file."""

    # ── General ───────────────────────────────────────────────────────────────
    PROJECT_NAME: str = "PhishGuard AI — Enterprise Threat Intelligence"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    APP_ENV: str = Field(default="development", description="development | staging | production")
    DEBUG: bool = Field(default=True, description="Enable debug mode")

    # ── Security ──────────────────────────────────────────────────────────────
    SECRET_KEY: str = Field(default="phishguard-dev-secret-key-change-in-production")
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000",
        description="Comma-separated list of allowed CORS origins",
    )

    # ── CascadeFlow Routing (Intelligent AI Routing) ────────────────────────────
    NEURALFLOW_PRIMARY_MODEL: str = Field(
        default="phishguard-ensemble-v3",
        description="Primary analysis model for deep-tier routing",
    )
    NEURALFLOW_FALLBACK_MODEL: str = Field(
        default="phishguard-heuristic-v2",
        description="Fallback model when primary is unavailable or times out",
    )
    NEURALFLOW_FAST_TIMEOUT_MS: int = Field(default=50, description="Max latency for fast tier (ms)")
    NEURALFLOW_STANDARD_TIMEOUT_MS: int = Field(default=200, description="Max latency for standard tier (ms)")
    NEURALFLOW_DEEP_TIMEOUT_MS: int = Field(default=1000, description="Max latency for deep tier (ms)")

    # ── Hindsight Memory (Persistent Threat Memory) ───────────────────────
    SENTINEL_DB_URL: str = Field(
        default="sqlite:///./sentinel_memory.db",
        description="Database URL for persistent threat memory",
    )
    SENTINEL_VECTOR_DIM: int = Field(default=64, description="Feature vector dimensionality")
    SENTINEL_MAX_MEMORY: int = Field(default=10000, description="Max threat records in memory")
    SENTINEL_SIMILARITY_THRESHOLD: float = Field(
        default=0.75, description="Minimum cosine similarity for threat matching"
    )

    # ── Rate Limiting ─────────────────────────────────────────────────────────
    RATE_LIMIT_REQUESTS: int = Field(default=100, description="Max requests per window")
    RATE_LIMIT_WINDOW_SECONDS: int = Field(default=60, description="Rate limit window in seconds")

    # ── Redis (optional — for production caching) ─────────────────────────────
    REDIS_URL: Optional[str] = Field(default=None, description="Redis connection URL")
    REDIS_CACHE_TTL: int = Field(default=300, description="Cache TTL in seconds")

    # ── Logging ───────────────────────────────────────────────────────────────
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FILE: str = Field(default="logs/phishguard.log", description="Log file path")
    LOG_JSON: bool = Field(default=False, description="Enable JSON structured logging")

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",
    }


settings = Settings()

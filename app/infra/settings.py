"""Application settings module."""
from __future__ import annotations

from functools import lru_cache
from typing import List, Set

from pydantic import AnyUrl, Field, constr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralised configuration for the DGII service."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=True)

    app_name: str = Field(default="DGII e-CF API")
    environment: constr(strip_whitespace=True) = Field(default="development")

    cors_allow_origins: List[str] = Field(default_factory=lambda: ["https://localhost:3000"])
    rate_limit_per_minute: int = Field(default=120, ge=1)

    jwt_secret: str = Field(default="change-me")
    jwt_access_exp_minutes: int = Field(default=15, ge=5, le=60)

    postgres_dsn: str = Field(default="postgresql+psycopg://postgres:postgres@localhost:5432/dgii")

    dgii_env: constr(strip_whitespace=True) = Field(default="PRECERT")
    dgii_allowed_hosts: Set[str] = Field(default_factory=lambda: {"ecf.dgii.gov.do", "servicios.dgii.gov.do"})
    dgii_token_url: AnyUrl | None = None
    dgii_submission_url: AnyUrl | None = None
    dgii_status_url: AnyUrl | None = None

    dgii_timeout: float = Field(default=5.0, gt=0)
    dgii_conn_timeout: float = Field(default=2.0, gt=0)
    dgii_max_retries: int = Field(default=3, ge=0)
    dgii_circuit_breaker_threshold: int = Field(default=5, ge=1)
    dgii_circuit_breaker_window: int = Field(default=60, ge=1)

    dgii_p12_path: str = Field(default="/secrets/cert.p12")
    dgii_p12_password: str = Field(default="changeit")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

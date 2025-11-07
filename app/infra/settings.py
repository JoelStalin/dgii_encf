"""Application settings module."""
from __future__ import annotations

from functools import lru_cache
from typing import List, Set

from pydantic import AliasChoices, AnyUrl, Field, computed_field, constr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url


class Settings(BaseSettings):
    """Centralised configuration for the DGII service."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=True)

    app_name: str = Field(default="DGII e-CF API")
    environment: constr(strip_whitespace=True) = Field(default="development")

    cors_allow_origins: List[str] = Field(
        default_factory=lambda: [
            "https://api.dgii.getupsoft.do",
            "https://staging.dgii.getupsoft.do",
        ],
        validation_alias=AliasChoices("CORS_ALLOW_ORIGINS", "FRONTEND_ORIGINS"),
    )
    rate_limit_per_minute: int = Field(default=100, ge=1)

    jwt_secret: str = Field(default="change-me")
    jwt_access_exp_minutes: int = Field(default=15, ge=5, le=60)

    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/dgii",
        validation_alias=AliasChoices("DATABASE_URL", "POSTGRES_DSN"),
    )
    redis_url: str = Field(default="redis://localhost:6379/0")
    sentry_dsn: str | None = Field(default=None)
    sentry_traces_sample_rate: float = Field(default=0.0, ge=0.0, le=1.0, alias="SENTRY_TRACES")

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

    @computed_field
    @property
    def sqlalchemy_async_url(self) -> str:
        """Ensure the SQLAlchemy URL uses an async driver."""

        url = make_url(self.database_url)
        if url.drivername.endswith("+asyncpg"):
            return self.database_url

        if "+" in url.drivername:
            dialect, _driver = url.drivername.split("+", 1)
        else:
            dialect = url.drivername

        async_url = url.set(drivername=f"{dialect}+asyncpg")
        return async_url.render_as_string(hide_password=False)

    @field_validator("cors_allow_origins", mode="before")
    @classmethod
    def _parse_origins(cls, value: List[str] | str) -> List[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return [origin.strip() for origin in value]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

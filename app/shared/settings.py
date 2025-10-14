"""Configuración central del proyecto GetUpNet."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Define las variables de entorno y valores por defecto."""

    app_name: str = Field("GetUpNet API", description="Nombre expuesto en OpenAPI")
    environment: str = Field("development", description="Entorno de despliegue actual")
    secret_key: str = Field("dev-secret", env="JWT_SECRET", description="Secreto para firmar JWT")
    hmac_service_secret: str = Field("dev-hmac", env="HMAC_SERVICE_SECRET", description="Secreto compartido entre microservicios")
    access_token_exp_minutes: int = Field(15, ge=5, le=120, description="Duración del access token en minutos")
    refresh_token_exp_minutes: int = Field(60 * 24 * 7, description="Duración del refresh token en minutos")
    database_url: str = Field("sqlite:///:memory:", env="DB_URL", description="Cadena de conexión a PostgreSQL")
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL", description="URL de conexión a Redis")
    log_level: str = Field("INFO", description="Nivel de logs para toda la plataforma")
    cors_allow_origins: List[str] = Field(default_factory=list, description="Orígenes permitidos para CORS")
    tls_enabled: bool = Field(True, description="Indica si el despliegue debe forzar TLS 1.3")
    dgii_env: str = Field("testecf", description="Ambiente DGII por defecto")
    dgii_base_ecf: str = Field("https://ecf.dgii.gov.do", env="DGII_BASE_ECF", description="Base URL para servicios e-CF")
    dgii_base_fc: str = Field("https://fc.dgii.gov.do", env="DGII_BASE_FC", description="Base URL para servicios RFCE")
    tracing_header: str = Field("X-Trace-ID", description="Encabezado utilizado para el tracing distribuido")
    request_id_header: str = Field("X-Request-ID", description="Encabezado de correlación de solicitudes")
    metrics_enabled: bool = Field(True, description="Habilita la exposición de métricas Prometheus")
    sentry_dsn: Optional[str] = Field(None, env="SENTRY_DSN", description="DSN de Sentry opcional")
    storage_bucket: str = Field("local", description="Bucket/espacio para almacenamiento WORM")
    storage_base_path: Path = Field(Path("/var/getupnet/storage"), description="Ruta por defecto para almacenamiento local")

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env.development",
        env_file_encoding="utf-8",
    )

    @field_validator("cors_allow_origins", mode="before")
    @classmethod
    def _split_origins(cls, value: str | List[str]) -> List[str]:
        if isinstance(value, list):
            return value
        return [origin.strip() for origin in value.split(",") if origin.strip()] if value else []


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

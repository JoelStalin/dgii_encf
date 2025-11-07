"""Gunicorn configuration for FastAPI + Uvicorn worker."""
from __future__ import annotations

import multiprocessing
import os

bind = "0.0.0.0:8000"
workers = min(8, multiprocessing.cpu_count() * 2 + 1)
worker_class = "uvicorn.workers.UvicornWorker"
keepalive = 5
timeout = int(os.getenv("GUNICORN_TIMEOUT", "60"))
graceful_timeout = 30
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", "1000"))
max_requests_jitter = int(os.getenv("GUNICORN_MAX_JITTER", "200"))
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")

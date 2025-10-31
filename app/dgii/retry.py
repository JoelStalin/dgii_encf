"""Retry utilities for DGII HTTP calls."""
from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable
from typing import Any, Type

from httpx import HTTPError, HTTPStatusError
from tenacity import AsyncRetrying, RetryCallState, RetryError, retry_if_exception, stop_after_attempt, wait_exponential_jitter

from app.dgii.exceptions import DGIIRetryableError


def _is_retryable(exc: BaseException) -> bool:
    if isinstance(exc, DGIIRetryableError):
        return True
    if isinstance(exc, HTTPStatusError):
        return 500 <= exc.response.status_code < 600
    if isinstance(exc, HTTPError):
        return True
    return False


def async_retry(
    retries: int,
    *,
    base: float = 1.0,
    max_wait: float = 5.0,
) -> AsyncIterator[RetryCallState]:
    """Return an async retry iterator configured for DGII operations."""

    return AsyncRetrying(
        reraise=True,
        stop=stop_after_attempt(max(1, retries)),
        wait=wait_exponential_jitter(exp_base=base, max=max_wait),
        retry=retry_if_exception(_is_retryable),
        before_sleep=_before_sleep_log,
    )


def _before_sleep_log(retry_state: RetryCallState) -> None:
    """Emit structured log before retrying."""

    attempt = retry_state.attempt_number
    exception = retry_state.outcome.exception() if retry_state.outcome else None
    from app.core.logging import bind_request_context

    bind_request_context(retry_attempt=attempt).warning("Reintentando llamada DGII", error=str(exception))

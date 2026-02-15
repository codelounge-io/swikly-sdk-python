from __future__ import annotations

from typing import Any, Dict, Optional, Union

import httpx

from .errors import (
    SwiklyAPIError,
    SwiklyAuthError,
    SwiklyNotFoundError,
    SwiklyRateLimitError,
    SwiklyValidationError,
)
from .utils import _default_base_url, _parse_error_payload, _read_retry_after, _sleep
from .resources.accounts import AccountsResource
from .resources.users import UsersResource
from .resources.requests import RequestsResource
from .resources.advanced import (
    DepositsResource,
    NoShowsResource,
    PaymentsResource,
    ReclaimsResource,
    RefundsResource,
    FilesResource,
    ShortLinksResource,
)

Json = Dict[str, Any]


class _BaseClient:
    def __init__(
        self,
        *,
        token: Optional[str] = None,
        legacy_api_key: Optional[str] = None,
        legacy_api_secret: Optional[str] = None,
        base_url: Optional[str] = None,
        environment: str = "production",
        timeout: float = 30.0,
        max_retries: int = 2,
        user_agent: Optional[str] = None,
        default_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self.base_url = base_url or _default_base_url(environment)
        self.timeout = timeout
        self.max_retries = max_retries

        headers: Dict[str, str] = {"Accept": "application/json"}
        if user_agent:
            headers["User-Agent"] = user_agent
        if default_headers:
            headers.update(default_headers)

        # Auth:
        # - Spec uses Bearer token.
        # - Docs mention legacy api_key/api_secret; support both headers.
        self._token = token
        self._legacy_api_key = legacy_api_key
        self._legacy_api_secret = legacy_api_secret
        self._base_headers = headers

        # Resources (attached in subclasses after http client exists)

    def _auth_headers(self) -> Dict[str, str]:
        headers = dict(self._base_headers)
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        if self._legacy_api_key and self._legacy_api_secret:
            headers["API_KEY"] = self._legacy_api_key
            headers["API_SECRET"] = self._legacy_api_secret
        return headers

    def _raise_for_response(self, resp: httpx.Response) -> None:
        if 200 <= resp.status_code < 300:
            return

        request_id = resp.headers.get("X-Request-Id") or resp.headers.get("Request-Id")
        data: Any = None
        try:
            data = resp.json()
        except Exception:
            data = resp.text

        code, message, context, errors = _parse_error_payload(data)

        if resp.status_code in (401, 403):
            raise SwiklyAuthError(resp.status_code, message, code=code, context=context, errors=errors, request_id=request_id, raw=data)
        if resp.status_code == 404:
            raise SwiklyNotFoundError(resp.status_code, message, code=code, context=context, errors=errors, request_id=request_id, raw=data)
        if resp.status_code == 422:
            raise SwiklyValidationError(resp.status_code, message, code=code, context=context, errors=errors, request_id=request_id, raw=data)
        if resp.status_code == 429:
            e = SwiklyRateLimitError(resp.status_code, message, code=code, context=context, errors=errors, request_id=request_id, raw=data)
            e.retry_after = _read_retry_after(resp.headers)
            raise e

        raise SwiklyAPIError(resp.status_code, message, code=code, context=context, errors=errors, request_id=request_id, raw=data)


class SwiklyClient(_BaseClient):
    """Synchronous Swikly API client."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._http = httpx.Client(base_url=self.base_url, timeout=self.timeout, headers=self._auth_headers())

        # Resources
        self.users = UsersResource(self)
        self.accounts = AccountsResource(self)
        self.requests = RequestsResource(self)

        # Advanced
        self.deposits = DepositsResource(self)
        self.no_shows = NoShowsResource(self)
        self.payments = PaymentsResource(self)
        self.reclaims = ReclaimsResource(self)
        self.refunds = RefundsResource(self)
        self.files = FilesResource(self)
        self.short_links = ShortLinksResource(self)

    def close(self) -> None:
        self._http.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
        files: Any = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        # retry on 429/5xx + transport errors
        attempt = 0
        last_exc: Exception | None = None
        merged_headers = dict(self._auth_headers())
        if headers:
            merged_headers.update(headers)

        while attempt <= self.max_retries:
            try:
                resp = self._http.request(method, path, params=params, json=json, files=files, headers=merged_headers)
                if resp.status_code == 429:
                    retry_after = _read_retry_after(resp.headers)
                    if retry_after is not None and attempt < self.max_retries:
                        _sleep(retry_after)
                        attempt += 1
                        continue
                if 500 <= resp.status_code < 600 and attempt < self.max_retries:
                    attempt += 1
                    continue
                self._raise_for_response(resp)
                return resp
            except (httpx.TimeoutException, httpx.NetworkError) as e:
                last_exc = e
                if attempt >= self.max_retries:
                    raise
                attempt += 1
        # should not happen
        if last_exc:
            raise last_exc
        raise RuntimeError("Unexpected request loop termination")


class AsyncSwiklyClient(_BaseClient):
    """Asynchronous Swikly API client."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._http = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout, headers=self._auth_headers())

        self.users = UsersResource(self)
        self.accounts = AccountsResource(self)
        self.requests = RequestsResource(self)

        self.deposits = DepositsResource(self)
        self.no_shows = NoShowsResource(self)
        self.payments = PaymentsResource(self)
        self.reclaims = ReclaimsResource(self)
        self.refunds = RefundsResource(self)
        self.files = FilesResource(self)
        self.short_links = ShortLinksResource(self)

    async def aclose(self) -> None:
        await self._http.aclose()

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
        files: Any = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        attempt = 0
        merged_headers = dict(self._auth_headers())
        if headers:
            merged_headers.update(headers)

        while attempt <= self.max_retries:
            try:
                resp = await self._http.request(method, path, params=params, json=json, files=files, headers=merged_headers)
                if resp.status_code == 429:
                    retry_after = _read_retry_after(resp.headers)
                    if retry_after is not None and attempt < self.max_retries:
                        _sleep(retry_after)
                        attempt += 1
                        continue
                if 500 <= resp.status_code < 600 and attempt < self.max_retries:
                    attempt += 1
                    continue
                self._raise_for_response(resp)
                return resp
            except (httpx.TimeoutException, httpx.NetworkError):
                if attempt >= self.max_retries:
                    raise
                attempt += 1
        raise RuntimeError("Unexpected request loop termination")

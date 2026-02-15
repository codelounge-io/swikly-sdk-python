from __future__ import annotations

from typing import Optional

from ..models import AccountsListResponse
from .base import ResourceBase

class AccountsResource(ResourceBase):
    def list(self, *, page: int | None = None, per_page: int | None = None) -> AccountsListResponse:
        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        resp = self._client.request("GET", "/accounts", params=params or None)
        return AccountsListResponse.model_validate(resp.json())

    async def alist(self, *, page: int | None = None, per_page: int | None = None) -> AccountsListResponse:
        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        resp = await self._client.request("GET", "/accounts", params=params or None)
        return AccountsListResponse.model_validate(resp.json())

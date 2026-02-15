from __future__ import annotations

from ..models import MeResponse
from .base import ResourceBase

class UsersResource(ResourceBase):
    def me(self) -> MeResponse:
        resp = self._client.request("GET", "/me")
        return MeResponse.model_validate(resp.json())

    async def ame(self) -> MeResponse:
        resp = await self._client.request("GET", "/me")
        return MeResponse.model_validate(resp.json())

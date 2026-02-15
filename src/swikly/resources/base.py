from __future__ import annotations

from typing import Any, Dict, Optional

from ..utils import _coerce_with_param

class ResourceBase:
    def __init__(self, client: Any) -> None:
        self._client = client

    @property
    def _is_async(self) -> bool:
        return hasattr(self._client, "aclose")

    def _with(self, with_: Optional[list[str] | tuple[str, ...] | str]) -> Optional[str]:
        return _coerce_with_param(with_)

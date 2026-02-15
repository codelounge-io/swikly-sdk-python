from __future__ import annotations

from typing import Any, Dict, Optional, Sequence

from ..models import (
    DepositResponse,
    NoShowResponse,
    PaymentResponse,
    RefundResponse,
    ReclaimsListResponse,
    ReclaimResponse,
    RequestsListResponse,
    RequestResponse,
    ShortLinkResponse,
)
from .base import ResourceBase


class DepositsResource(ResourceBase):
    def get(self, *, account_id: str, deposit_id: str, with_: Optional[Sequence[str] | str] = None) -> DepositResponse:
        params: Dict[str, Any] = {}
        w = self._with(with_)
        if w:
            params["with"] = w
        resp = self._client.request("GET", f"/accounts/{account_id}/deposits/{deposit_id}", params=params or None)
        return DepositResponse.model_validate(resp.json())

    def update(self, *, account_id: str, deposit_id: str, startDate: str | None = None, endDate: str | None = None, amount: int | None = None, status: str | None = None) -> DepositResponse:
        payload: Dict[str, Any] = {}
        if startDate is not None:
            payload["startDate"] = startDate
        if endDate is not None:
            payload["endDate"] = endDate
        if amount is not None:
            payload["amount"] = amount
        if status is not None:
            payload["status"] = status
        resp = self._client.request("PATCH", f"/accounts/{account_id}/deposits/{deposit_id}", json=payload)
        return DepositResponse.model_validate(resp.json())


class NoShowsResource(ResourceBase):
    def get(self, *, account_id: str, no_show_id: str, with_: Optional[Sequence[str] | str] = None) -> NoShowResponse:
        params: Dict[str, Any] = {}
        w = self._with(with_)
        if w:
            params["with"] = w
        resp = self._client.request("GET", f"/accounts/{account_id}/no-shows/{no_show_id}", params=params or None)
        return NoShowResponse.model_validate(resp.json())

    def update(self, *, account_id: str, no_show_id: str, status: str | None = None) -> NoShowResponse:
        payload: Dict[str, Any] = {}
        if status is not None:
            payload["status"] = status
        resp = self._client.request("PATCH", f"/accounts/{account_id}/no-shows/{no_show_id}", json=payload)
        return NoShowResponse.model_validate(resp.json())


class PaymentsResource(ResourceBase):
    def get(self, *, account_id: str, payment_id: str, with_: Optional[Sequence[str] | str] = None) -> PaymentResponse:
        params: Dict[str, Any] = {}
        w = self._with(with_)
        if w:
            params["with"] = w
        resp = self._client.request("GET", f"/accounts/{account_id}/payments/{payment_id}", params=params or None)
        return PaymentResponse.model_validate(resp.json())

    def update(self, *, account_id: str, payment_id: str, status: str | None = None) -> PaymentResponse:
        payload: Dict[str, Any] = {}
        if status is not None:
            payload["status"] = status
        resp = self._client.request("PATCH", f"/accounts/{account_id}/payments/{payment_id}", json=payload)
        return PaymentResponse.model_validate(resp.json())


class RefundsResource(ResourceBase):
    def get(self, *, account_id: str, refund_id: str) -> RefundResponse:
        resp = self._client.request("GET", f"/accounts/{account_id}/refunds/{refund_id}")
        return RefundResponse.model_validate(resp.json())

    def refund_payment(self, *, account_id: str, payment_id: str, amount: int, reason: str) -> RefundResponse:
        payload = {"amount": amount, "reason": reason}
        resp = self._client.request("POST", f"/accounts/{account_id}/payments/{payment_id}/refunds", json=payload)
        return RefundResponse.model_validate(resp.json())

    def refund_reclaim(self, *, account_id: str, reclaim_id: str, amount: int, reason: str) -> RefundResponse:
        payload = {"amount": amount, "reason": reason}
        resp = self._client.request("POST", f"/accounts/{account_id}/reclaims/{reclaim_id}/refunds", json=payload)
        return RefundResponse.model_validate(resp.json())


class ReclaimsResource(ResourceBase):
    def list(
        self,
        *,
        account_id: str,
        page: int | None = None,
        per_page: int | None = None,
        with_: Optional[Sequence[str] | str] = None,
        status: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> ReclaimsListResponse:
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        w = self._with(with_)
        if w:
            params["with"] = w
        if status:
            params["status"] = status
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        resp = self._client.request("GET", f"/accounts/{account_id}/reclaims", params=params or None)
        return ReclaimsListResponse.model_validate(resp.json())

    def list_for_request(self, *, account_id: str, request_id: str, with_: Optional[Sequence[str] | str] = None) -> ReclaimsListResponse:
        params: Dict[str, Any] = {}
        w = self._with(with_)
        if w:
            params["with"] = w
        resp = self._client.request("GET", f"/accounts/{account_id}/requests/{request_id}/reclaims", params=params or None)
        return ReclaimsListResponse.model_validate(resp.json())

    def get(self, *, account_id: str, reclaim_id: str, with_: Optional[Sequence[str] | str] = None) -> ReclaimResponse:
        params: Dict[str, Any] = {}
        w = self._with(with_)
        if w:
            params["with"] = w
        resp = self._client.request("GET", f"/accounts/{account_id}/reclaims/{reclaim_id}", params=params or None)
        return ReclaimResponse.model_validate(resp.json())

    def create_from_deposit(self, *, account_id: str, deposit_id: str, amount: int, reason: str) -> ReclaimResponse:
        payload = {"amount": amount, "reason": reason}
        resp = self._client.request("POST", f"/accounts/{account_id}/deposits/{deposit_id}/reclaims", json=payload)
        return ReclaimResponse.model_validate(resp.json())

    def create_from_no_show(self, *, account_id: str, no_show_id: str, amount: int, reason: str) -> ReclaimResponse:
        payload = {"amount": amount, "reason": reason}
        resp = self._client.request("POST", f"/accounts/{account_id}/no-shows/{no_show_id}/reclaims", json=payload)
        return ReclaimResponse.model_validate(resp.json())


class FilesResource(ResourceBase):
    def upload_temporary_file(self, *, account_id: str, file_path: str) -> dict:
        with open(file_path, "rb") as f:
            files = {"file": (file_path.split("/")[-1], f)}
            resp = self._client.request("POST", f"/accounts/{account_id}/files", files=files)
        return resp.json()

    def attach_file_to_reclaim(self, *, account_id: str, reclaim_id: str, file_path: str) -> dict:
        with open(file_path, "rb") as f:
            files = {"file": (file_path.split("/")[-1], f)}
            resp = self._client.request("POST", f"/accounts/{account_id}/reclaims/{reclaim_id}/files", files=files)
        return resp.json()

    def delete_reclaim_file(self, *, account_id: str, reclaim_id: str, file_id: str) -> None:
        self._client.request("DELETE", f"/accounts/{account_id}/reclaims/{reclaim_id}/files/{file_id}")
        return None


class ShortLinksResource(ResourceBase):
    def create(self, *, link: str) -> ShortLinkResponse:
        # Can be query param or JSON; use JSON
        resp = self._client.request("POST", "/shortener/short-links", json={"link": link})
        return ShortLinkResponse.model_validate(resp.json())

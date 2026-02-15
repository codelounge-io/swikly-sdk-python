from __future__ import annotations

from typing import Any, Dict, Optional, Sequence

from ..models import RequestResponse, RequestsListResponse
from .base import ResourceBase

class RequestsResource(ResourceBase):
    # -------- Sync --------
    def list(
        self,
        *,
        account_id: str,
        page: int | None = None,
        per_page: int | None = None,
        with_: Optional[Sequence[str] | str] = None,
        search: str | None = None,
        include_legacy: bool | None = None,
    ) -> RequestsListResponse:
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        w = self._with(with_)
        if w:
            params["with"] = w
        if search:
            params["search"] = search
        if include_legacy is not None:
            params["include_legacy"] = include_legacy
        resp = self._client.request("GET", f"/accounts/{account_id}/requests", params=params or None)
        return RequestsListResponse.model_validate(resp.json())

    def create(
        self,
        *,
        account_id: str,
        description: str,
        language: str,
        custom_id: str | None = None,
        custom_id_must_be_unique: bool | None = None,
        skip_to_payment_page_if_possible: bool | None = None,
        free_text: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        phone_number: str | None = None,
        birth_date: str | None = None,
        redirect_url: str | None = None,
        return_url: str | None = None,
        send_email: bool | None = None,
        send_sms: bool | None = None,
        partner_tag: str | None = None,
        callbacks: dict | None = None,
        deposit: dict | None = None,
        no_show: dict | None = None,
        payment: dict | None = None,
        address: dict | None = None,
    ) -> RequestResponse:
        payload: Dict[str, Any] = {"description": description, "language": language}
        if custom_id is not None:
            payload["customId"] = custom_id
        if custom_id_must_be_unique is not None:
            payload["customIdMustBeUnique"] = custom_id_must_be_unique
        if skip_to_payment_page_if_possible is not None:
            payload["skipToPaymentPageIfPossible"] = skip_to_payment_page_if_possible
        if free_text is not None:
            payload["freeText"] = free_text
        if first_name is not None:
            payload["firstName"] = first_name
        if last_name is not None:
            payload["lastName"] = last_name
        if email is not None:
            payload["email"] = email
        if phone_number is not None:
            payload["phoneNumber"] = phone_number
        if birth_date is not None:
            payload["birthDate"] = birth_date
        if redirect_url is not None:
            payload["redirectUrl"] = redirect_url
        if return_url is not None:
            payload["returnUrl"] = return_url
        if send_email is not None:
            payload["sendEmail"] = send_email
        if send_sms is not None:
            payload["sendSms"] = send_sms
        if partner_tag is not None:
            payload["partnerTag"] = partner_tag
        if callbacks is not None:
            payload["callbacks"] = callbacks
        if deposit is not None:
            payload["deposit"] = deposit
        if no_show is not None:
            payload["noShow"] = no_show
        if payment is not None:
            payload["payment"] = payment
        if address is not None:
            payload["address"] = address

        resp = self._client.request("POST", f"/accounts/{account_id}/requests", json=payload)
        return RequestResponse.model_validate(resp.json())

    def get(self, *, account_id: str, request_id: str, with_: Optional[Sequence[str] | str] = None) -> RequestResponse:
        params: Dict[str, Any] = {}
        w = self._with(with_)
        if w:
            params["with"] = w
        resp = self._client.request("GET", f"/accounts/{account_id}/requests/{request_id}", params=params or None)
        return RequestResponse.model_validate(resp.json())

    def update(
        self,
        *,
        account_id: str,
        request_id: str,
        deposit: dict | None = None,
        no_show: dict | None = None,
        payment: dict | None = None,
    ) -> RequestResponse:
        payload: Dict[str, Any] = {}
        if deposit is not None:
            payload["deposit"] = deposit
        if no_show is not None:
            payload["noShow"] = no_show
        if payment is not None:
            payload["payment"] = payment
        resp = self._client.request("PATCH", f"/accounts/{account_id}/requests/{request_id}", json=payload)
        return RequestResponse.model_validate(resp.json())

    def cancel(self, *, account_id: str, request_id: str) -> RequestResponse:
        resp = self._client.request("POST", f"/accounts/{account_id}/requests/{request_id}/cancel")
        return RequestResponse.model_validate(resp.json())

    def release(self, *, account_id: str, request_id: str) -> RequestResponse:
        resp = self._client.request("POST", f"/accounts/{account_id}/requests/{request_id}/release")
        return RequestResponse.model_validate(resp.json())

    def create_reclaim(
        self,
        *,
        account_id: str,
        request_id: str,
        target: str,
        amount: int,
        reason: str,
        files: list[str] | None = None,
    ) -> RequestResponse:
        payload: Dict[str, Any] = {"target": target, "amount": amount, "reason": reason}
        if files:
            payload["files"] = files
        resp = self._client.request("POST", f"/accounts/{account_id}/requests/{request_id}/create_reclaim", json=payload)
        return RequestResponse.model_validate(resp.json())

    def cancel_reclaim(self, *, account_id: str, request_id: str, target: str) -> RequestResponse:
        payload = {"target": target}
        resp = self._client.request("POST", f"/accounts/{account_id}/requests/{request_id}/cancel_reclaim", json=payload)
        return RequestResponse.model_validate(resp.json())

    def create_refund(self, *, account_id: str, request_id: str, target: str, amount: int, reason: str) -> RequestResponse:
        payload = {"target": target, "amount": amount, "reason": reason}
        resp = self._client.request("POST", f"/accounts/{account_id}/requests/{request_id}/create_refund", json=payload)
        return RequestResponse.model_validate(resp.json())

    # -------- Async --------
    async def alist(self, **kwargs: Any) -> RequestsListResponse:
        resp = await self._client.request("GET", f"/accounts/{kwargs['account_id']}/requests", params=_params_for_list(kwargs))
        return RequestsListResponse.model_validate(resp.json())

    async def acreate(self, **kwargs: Any) -> RequestResponse:
        account_id = kwargs.pop("account_id")
        payload = _payload_for_create(kwargs)
        resp = await self._client.request("POST", f"/accounts/{account_id}/requests", json=payload)
        return RequestResponse.model_validate(resp.json())

    async def aget(self, **kwargs: Any) -> RequestResponse:
        account_id = kwargs["account_id"]
        request_id = kwargs["request_id"]
        params: Dict[str, Any] = {}
        w = self._with(kwargs.get("with_"))
        if w:
            params["with"] = w
        resp = await self._client.request("GET", f"/accounts/{account_id}/requests/{request_id}", params=params or None)
        return RequestResponse.model_validate(resp.json())

    async def aupdate(self, **kwargs: Any) -> RequestResponse:
        account_id = kwargs["account_id"]
        request_id = kwargs["request_id"]
        payload: Dict[str, Any] = {}
        if kwargs.get("deposit") is not None:
            payload["deposit"] = kwargs["deposit"]
        if kwargs.get("no_show") is not None:
            payload["noShow"] = kwargs["no_show"]
        if kwargs.get("payment") is not None:
            payload["payment"] = kwargs["payment"]
        resp = await self._client.request("PATCH", f"/accounts/{account_id}/requests/{request_id}", json=payload)
        return RequestResponse.model_validate(resp.json())

    async def acancel(self, *, account_id: str, request_id: str) -> RequestResponse:
        resp = await self._client.request("POST", f"/accounts/{account_id}/requests/{request_id}/cancel")
        return RequestResponse.model_validate(resp.json())

    async def arelease(self, *, account_id: str, request_id: str) -> RequestResponse:
        resp = await self._client.request("POST", f"/accounts/{account_id}/requests/{request_id}/release")
        return RequestResponse.model_validate(resp.json())

    async def acreate_reclaim(self, *, account_id: str, request_id: str, target: str, amount: int, reason: str, files: list[str] | None = None) -> RequestResponse:
        payload: Dict[str, Any] = {"target": target, "amount": amount, "reason": reason}
        if files:
            payload["files"] = files
        resp = await self._client.request("POST", f"/accounts/{account_id}/requests/{request_id}/create_reclaim", json=payload)
        return RequestResponse.model_validate(resp.json())

    async def acancel_reclaim(self, *, account_id: str, request_id: str, target: str) -> RequestResponse:
        payload = {"target": target}
        resp = await self._client.request("POST", f"/accounts/{account_id}/requests/{request_id}/cancel_reclaim", json=payload)
        return RequestResponse.model_validate(resp.json())

    async def acreate_refund(self, *, account_id: str, request_id: str, target: str, amount: int, reason: str) -> RequestResponse:
        payload = {"target": target, "amount": amount, "reason": reason}
        resp = await self._client.request("POST", f"/accounts/{account_id}/requests/{request_id}/create_refund", json=payload)
        return RequestResponse.model_validate(resp.json())


def _params_for_list(kwargs: Dict[str, Any]) -> Dict[str, Any] | None:
    params: Dict[str, Any] = {}
    if kwargs.get("page") is not None:
        params["page"] = kwargs["page"]
    if kwargs.get("per_page") is not None:
        params["per_page"] = kwargs["per_page"]
    w = kwargs.get("with_")
    if w is not None:
        if isinstance(w, str):
            params["with"] = w
        else:
            params["with"] = ",".join(list(w))
    if kwargs.get("search"):
        params["search"] = kwargs["search"]
    if kwargs.get("include_legacy") is not None:
        params["include_legacy"] = kwargs["include_legacy"]
    return params or None


def _payload_for_create(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    # Map pythonic kwargs to API JSON keys
    payload: Dict[str, Any] = {"description": kwargs["description"], "language": kwargs["language"]}
    mapping = {
        "custom_id": "customId",
        "custom_id_must_be_unique": "customIdMustBeUnique",
        "skip_to_payment_page_if_possible": "skipToPaymentPageIfPossible",
        "free_text": "freeText",
        "first_name": "firstName",
        "last_name": "lastName",
        "email": "email",
        "phone_number": "phoneNumber",
        "birth_date": "birthDate",
        "redirect_url": "redirectUrl",
        "return_url": "returnUrl",
        "send_email": "sendEmail",
        "send_sms": "sendSms",
        "partner_tag": "partnerTag",
        "callbacks": "callbacks",
        "deposit": "deposit",
        "no_show": "noShow",
        "payment": "payment",
        "address": "address",
    }
    for k, api_k in mapping.items():
        if k in kwargs and kwargs[k] is not None:
            payload[api_k] = kwargs[k]
    return payload

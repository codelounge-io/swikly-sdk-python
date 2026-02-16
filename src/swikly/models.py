from __future__ import annotations

from typing import Any, Literal, Optional, Union, List, Dict
from pydantic import BaseModel, Field, ConfigDict


class SwiklyModel(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)


# Common
Id = str
Amount = int
Currency = str
DateStr = str
DateTimeStr = str


class User(SwiklyModel):
    id: Id
    firstName: str
    lastName: str
    email: str
    createdAt: DateTimeStr


class Account(SwiklyModel):
    id: Id
    commercialName: str
    currency: Currency
    createdAt: DateTimeStr
    legacyId: Optional[Id] = None
    managerId: Optional[Id] = None
    reference: Optional[str] = None
    secret: Optional[str] = None


class ResultsMeta(SwiklyModel):
    currentPage: int
    lastPage: int
    perPage: int
    path: str
    total: int


class BaseAddress(SwiklyModel):
    country: str
    region: Optional[str] = None
    postalCode: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None


class Address(BaseAddress):
    postalCode: str
    city: str
    street: str


class Person(SwiklyModel):
    id: Id
    firstName: str
    lastName: str
    address: Address
    email: str
    birthDate: Optional[DateStr] = None
    phone: Optional[str] = None
    createdAt: DateTimeStr


class RefundSummary(SwiklyModel):
    refundableAmount: Amount
    pendingRefundAmount: Amount
    refundedAmount: Amount


class File(SwiklyModel):
    id: Id
    name: str
    url: str
    createdAt: DateTimeStr


class ReclaimSummary(SwiklyModel):
    reclaimableAmount: Optional[Amount] = None
    plannedRequestedAmount: Optional[Amount] = None
    maximumReclaimCreationDate: Optional[DateStr] = None  # <-- allow null
    pendingRequestedAmount: Optional[Amount] = None
    pendingReclaimedAmount: Optional[Amount] = None
    reclaimedAmount: Optional[Amount] = None
    estimatedFinishDate: Optional[DateStr] = None  # <-- allow null
    cancelableAmount: Optional[Amount] = None
    irrecoverableAmount: Optional[Amount] = None
    irrecoverabilityCertificates: Optional[List[File]] = None


class Deposit(SwiklyModel):
    id: Id
    requestId: Id
    amount: Amount
    amountToBeSecured: Amount
    securedAmount: Amount
    status: str
    startDate: DateStr
    endDate: DateStr
    expirationDate: Optional[DateStr] = None  # <-- allow null
    acceptedAt: Optional[DateTimeStr] = None
    releasedAt: Optional[DateTimeStr] = None
    canceledAt: Optional[DateTimeStr] = None
    createdAt: DateTimeStr
    request: Optional["Request"] = None
    reclaimSummary: Optional[ReclaimSummary] = None
    refundSummary: Optional[RefundSummary] = None


class NoShow(SwiklyModel):
    id: Id
    requestId: Id
    reservationDate: DateStr
    amount: Amount
    amountToBeSecured: Amount
    securedAmount: Amount
    status: str
    expirationDate: Optional[DateStr] = None
    acceptedAt: Optional[DateTimeStr] = None
    releasedAt: Optional[DateTimeStr] = None
    expiredAt: Optional[DateTimeStr] = None
    canceledAt: Optional[DateTimeStr] = None
    createdAt: Optional[DateTimeStr] = None
    request: Optional["Request"] = None
    reclaimSummary: Optional[ReclaimSummary] = None
    refundSummary: Optional[RefundSummary] = None


class Payment(SwiklyModel):
    id: Id
    requestId: Id
    amount: Amount
    amountToBePaid: Amount
    amountPaid: Amount
    status: str
    dueDate: Optional[DateStr] = None
    succeededAt: Optional[DateTimeStr] = None
    canceledAt: Optional[DateTimeStr] = None
    createdAt: DateTimeStr
    request: Optional["Request"] = None
    refundSummary: Optional[RefundSummary] = None


class Refund(SwiklyModel):
    id: Id
    refundableType: Literal["Payment", "Reclaim"]
    refundableId: Id
    amount: Amount
    status: str
    finishedAt: Optional[DateTimeStr] = None
    createdAt: DateTimeStr


class BaseReclaim(SwiklyModel):
    id: Id
    reclaimableType: Optional[Literal["Deposit", "NoShow"]] = None
    reclaimableId: Optional[Id] = None
    amount: Amount
    cashedInAmount: Amount
    reason: str
    files: Optional[List[File]] = None
    filesValidated: bool
    guaranteedAmount: Optional[Amount] = None
    createdAt: DateTimeStr


class InitializedReclaim(BaseReclaim):
    status: Literal["Initialized"]
    finishedAt: Optional[DateTimeStr] = None


class FinishedReclaim(BaseReclaim):
    status: Literal["Finished"]
    finishedAt: DateTimeStr


Reclaim = Union[InitializedReclaim, FinishedReclaim]


class Request(SwiklyModel):
    id: Id
    accountId: Id
    link: str
    description: str
    createdAt: DateTimeStr
    legacyId: Optional[Id] = None
    customId: Optional[str] = None
    customIdMustBeUnique: Optional[bool] = None
    skipToPaymentPageIfPossible: Optional[bool] = None
    lastName: Optional[str] = None
    firstName: Optional[str] = None
    email: Optional[str] = None
    phoneNumber: Optional[str] = None
    freeText: Optional[str] = None
    releasable: Optional[bool] = None
    cancelable: Optional[bool] = None
    deposit: Optional[Deposit] = None
    noShow: Optional[NoShow] = None
    payment: Optional[Payment] = None
    endUser: Optional[Any] = None  # union in spec; keep flexible
    redirectUrl: Optional[str] = None
    returnUrl: Optional[str] = None


class ShortLink(SwiklyModel):
    id: Id
    link: str
    shortLink: str
    createdAt: DateTimeStr


# Response wrappers
class MeResponse(SwiklyModel):
    user: User


class AccountsListResponse(SwiklyModel):
    accounts: List[Account]
    meta: Optional[ResultsMeta] = None


class RequestsListResponse(SwiklyModel):
    requests: List[Request]
    meta: Optional[ResultsMeta] = None


class RequestResponse(SwiklyModel):
    request: Request


class DepositResponse(SwiklyModel):
    deposit: Deposit


class NoShowResponse(SwiklyModel):
    no_show: NoShow = Field(alias="no-show")


class PaymentResponse(SwiklyModel):
    payment: Payment


class RefundResponse(SwiklyModel):
    refund: Refund


class ReclaimsListResponse(SwiklyModel):
    reclaims: List[Reclaim]
    meta: Optional[ResultsMeta] = None


class ReclaimResponse(SwiklyModel):
    reclaim: Reclaim


class FileCreateResponse(SwiklyModel):
    file: Any


class ShortLinkResponse(SwiklyModel):
    shortLink: ShortLink

"""Canonical provider request preparation and dispatch authorization contracts.

This module contains no provider adapter and performs no network operation.  It
defines the single byte-level digest grammar used by the B1/B2 amendment and
authority-issued receipts which prove durable preparation and dispatch CAS.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
import re
import unicodedata
from typing import Any, Mapping
from types import MappingProxyType


_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_CREDENTIAL_HEADER_NAMES = frozenset({
    "authorization", "cookie", "proxy-authorization", "set-cookie", "x-api-key",
})


def c_null() -> list[object]:
    return ["null"]


def c_bool(value: bool) -> list[object]:
    if type(value) is not bool:
        raise ValueError("canonical boolean is invalid")
    return ["bool", value]


def c_int(value: int) -> list[object]:
    if type(value) is not int:
        raise ValueError("canonical integer is invalid")
    return ["int", str(value)]


def c_str(value: str) -> list[object]:
    if not isinstance(value, str):
        raise ValueError("canonical string is invalid")
    return ["str", unicodedata.normalize("NFC", value)]


def c_id(value: str) -> list[object]:
    if not isinstance(value, str) or not value or unicodedata.normalize("NFC", value) != value:
        raise ValueError("canonical identifier is invalid")
    return ["id", value]


def c_enum(domain: str, value: str) -> list[object]:
    return ["enum", c_id(domain), c_id(value)]


def c_hex(value: str) -> list[object]:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise ValueError("canonical SHA-256 is invalid")
    return ["hex", value]


def c_bytes(value: bytes) -> list[object]:
    if not isinstance(value, bytes):
        raise ValueError("canonical bytes are invalid")
    return ["bytes", c_int(len(value)), c_hex(hashlib.sha256(value).hexdigest())]


def c_bytes_commitment(byte_length: int, digest: str) -> list[object]:
    if type(byte_length) is not int or byte_length < 0:
        raise ValueError("canonical byte length is invalid")
    return ["bytes", c_int(byte_length), c_hex(digest)]


def c_digest(domain: str, version: int, digest: str) -> list[object]:
    return ["digest", c_id(domain), c_int(version), c_hex(digest)]


def c_tuple(values: tuple[object, ...] | list[object]) -> list[object]:
    return ["tuple", list(values)]


def c_map(value: Mapping[str, object]) -> list[object]:
    pairs = sorted(((unicodedata.normalize("NFC", key), item) for key, item in value.items()), key=lambda pair: pair[0])
    if len({key for key, _ in pairs}) != len(pairs):
        raise ValueError("canonical map key is ambiguous")
    return ["map", [[c_str(key), item] for key, item in pairs]]


def canonical_contract_bytes(domain: str, version: int, ordered_fields: tuple[object, ...]) -> bytes:
    value = c_tuple((c_id("canonical-contract-digest"), c_id(domain), c_int(version), c_tuple(ordered_fields)))
    return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":")).encode("utf-8", "strict")


def canonical_contract_digest(domain: str, version: int, ordered_fields: tuple[object, ...]) -> str:
    return hashlib.sha256(canonical_contract_bytes(domain, version, ordered_fields)).hexdigest()


@dataclass(frozen=True)
class ResolvedTransportSemantics:
    protocol_id: str
    protocol_version: str
    logical_endpoint_id: str
    endpoint_uri_bytes: bytes
    operation_id: str
    method: str
    request_media_type: str
    semantic_headers: tuple[tuple[str, bytes], ...]
    transport_semantics_digest: str = field(init=False)

    def __post_init__(self) -> None:
        headers = tuple(self.semantic_headers)
        names = [name for name, _ in headers]
        if any(not isinstance(name, str) or name.lower() != name or not name.isascii() for name in names):
            raise ValueError("semantic header name must be lowercase ASCII")
        if names != sorted(names, key=lambda item: item.encode("ascii")) or len(names) != len(set(names)):
            raise ValueError("semantic headers are noncanonical")
        if any(not isinstance(value, bytes) for _, value in headers):
            raise ValueError("semantic header value must be exact bytes")
        if any(name in _CREDENTIAL_HEADER_NAMES for name in names):
            raise ValueError("credential-bearing headers cannot be semantic headers")
        fields = (
            c_id(self.protocol_id), c_str(self.protocol_version), c_id(self.logical_endpoint_id),
            c_bytes(self.endpoint_uri_bytes), c_id(self.operation_id), c_str(self.method),
            c_str(self.request_media_type),
            c_tuple(tuple(c_tuple((c_id(name), c_bytes(value))) for name, value in headers)),
        )
        object.__setattr__(self, "semantic_headers", headers)
        object.__setattr__(self, "transport_semantics_digest", canonical_contract_digest("transport-semantics", 1, fields))


def _canonical_setting(value: Any) -> object:
    if value is None:
        return c_null()
    if type(value) is bool:
        return c_bool(value)
    if type(value) is int:
        return c_int(value)
    if isinstance(value, str):
        return c_str(value)
    if isinstance(value, tuple):
        return c_tuple(tuple(_canonical_setting(item) for item in value))
    if isinstance(value, Mapping):
        return c_map({key: _canonical_setting(item) for key, item in value.items()})
    raise ValueError("generation setting is not canonical")


def _freeze_setting(value: Any) -> Any:
    """Detach every semantic value from caller-owned mutable containers."""
    if value is None or type(value) in {bool, int} or isinstance(value, str):
        return value
    if isinstance(value, tuple):
        return tuple(_freeze_setting(item) for item in value)
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze_setting(item) for key, item in value.items()})
    raise ValueError("generation setting is not canonical")


@dataclass(frozen=True)
class GenerationSettings:
    values: Mapping[str, Any]
    settings_digest: str = field(init=False)

    def __post_init__(self) -> None:
        material = c_map({key: _canonical_setting(value) for key, value in self.values.items()})
        object.__setattr__(self, "values", MappingProxyType({key: _freeze_setting(value) for key, value in self.values.items()}))
        object.__setattr__(self, "settings_digest", canonical_contract_digest("generation-settings", 1, (material,)))


@dataclass(frozen=True)
class ModelInputCommitment:
    authorized_payload_digest: str
    runtime_capability_digest: str
    transport_semantics_digest: str
    generation_settings_digest: str
    request_media_type: str
    request_body_bytes: bytes = field(repr=False, compare=False)
    request_body_length: int = field(init=False)
    request_body_digest: str = field(init=False)
    model_input_digest: str = field(init=False)

    def __post_init__(self) -> None:
        body = self.request_body_bytes
        if not isinstance(body, bytes):
            raise ValueError("exact provider request bytes are required")
        for digest in (self.authorized_payload_digest, self.runtime_capability_digest,
                       self.transport_semantics_digest, self.generation_settings_digest):
            if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
                raise ValueError("model input digest reference is invalid")
        body_digest = hashlib.sha256(body).hexdigest()
        fields = (
            c_digest("provider-authorized-payload", 2, self.authorized_payload_digest),
            c_digest("runtime-capability-binding", 2, self.runtime_capability_digest),
            c_digest("transport-semantics", 1, self.transport_semantics_digest),
            c_digest("generation-settings", 1, self.generation_settings_digest),
            c_str(self.request_media_type), c_bytes(body),
        )
        object.__setattr__(self, "request_body_length", len(body))
        object.__setattr__(self, "request_body_digest", body_digest)
        object.__setattr__(self, "model_input_digest", canonical_contract_digest("model-input-commitment", 1, fields))


@dataclass(frozen=True)
class ImmutableRequestBlobReference:
    blob_id: str
    request_body_length: int
    request_body_digest: str
    storage_receipt_digest: str = field(init=False)

    def __post_init__(self) -> None:
        if type(self.request_body_length) is not int or self.request_body_length < 0:
            raise ValueError("request blob length is invalid")
        fields = (c_id(self.blob_id), c_bytes_commitment(self.request_body_length, self.request_body_digest))
        object.__setattr__(self, "storage_receipt_digest", canonical_contract_digest("immutable-request-blob-storage-receipt", 1, fields))


@dataclass(frozen=True)
class PreparationRecord:
    execution_id: str
    attempt_digest: str
    model_input_digest: str
    request_blob: ImmutableRequestBlobReference
    transport_semantics_digest: str
    preparation_record_digest: str = field(init=False)

    def __post_init__(self) -> None:
        if not isinstance(self.request_blob, ImmutableRequestBlobReference):
            raise ValueError("immutable request blob reference is required")
        fields = (
            c_id(self.execution_id), c_digest("provider-execution-attempt", 2, self.attempt_digest),
            c_digest("model-input-commitment", 1, self.model_input_digest),
            c_digest("immutable-request-blob-storage-receipt", 1, self.request_blob.storage_receipt_digest),
            c_digest("transport-semantics", 1, self.transport_semantics_digest),
        )
        object.__setattr__(self, "preparation_record_digest", canonical_contract_digest("model-input-preparation-record", 1, fields))


_PREPARED_MARKER = object()


@dataclass(frozen=True, init=False)
class PreparedModelInputReceipt:
    execution_id: str
    attempt_digest: str
    model_input_digest: str
    preparation_record_digest: str
    storage_receipt_digest: str
    receipt_digest: str
    _marker: object = field(repr=False, compare=False)

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise TypeError("PreparedModelInputReceipt is journal-issued only")

    def is_authority_issued(self) -> bool:
        return getattr(self, "_marker", None) is _PREPARED_MARKER


def _issue_prepared_receipt(record: PreparationRecord) -> PreparedModelInputReceipt:
    fields = (c_id(record.execution_id), c_digest("provider-execution-attempt", 2, record.attempt_digest),
              c_digest("model-input-commitment", 1, record.model_input_digest),
              c_digest("model-input-preparation-record", 1, record.preparation_record_digest),
              c_digest("immutable-request-blob-storage-receipt", 1, record.request_blob.storage_receipt_digest))
    receipt = object.__new__(PreparedModelInputReceipt)
    for name, value in (("execution_id", record.execution_id), ("attempt_digest", record.attempt_digest),
                        ("model_input_digest", record.model_input_digest),
                        ("preparation_record_digest", record.preparation_record_digest),
                        ("storage_receipt_digest", record.request_blob.storage_receipt_digest),
                        ("receipt_digest", canonical_contract_digest("prepared-model-input-receipt", 1, fields)),
                        ("_marker", _PREPARED_MARKER)):
        object.__setattr__(receipt, name, value)
    return receipt


@dataclass(frozen=True)
class DispatchClaimRecord:
    execution_id: str
    attempt_digest: str
    prepared_receipt_digest: str
    model_input_digest: str
    runtime_capability_digest: str
    dispatch_claim_id: str
    dispatch_fence: int
    claim_record_digest: str = field(init=False)

    def __post_init__(self) -> None:
        if type(self.dispatch_fence) is not int or self.dispatch_fence < 1:
            raise ValueError("dispatch fence is invalid")
        fields = (c_id(self.execution_id), c_digest("provider-execution-attempt", 2, self.attempt_digest),
                  c_digest("prepared-model-input-receipt", 1, self.prepared_receipt_digest),
                  c_digest("model-input-commitment", 1, self.model_input_digest),
                  c_digest("runtime-capability-binding", 2, self.runtime_capability_digest),
                  c_id(self.dispatch_claim_id), c_int(self.dispatch_fence))
        object.__setattr__(self, "claim_record_digest", canonical_contract_digest("dispatch-claim-record", 1, fields))


_CLAIM_MARKER = object()


@dataclass(frozen=True, init=False)
class DispatchClaimReceipt:
    record: DispatchClaimRecord
    claim_record_digest: str
    receipt_digest: str
    _marker: object = field(repr=False, compare=False)

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise TypeError("DispatchClaimReceipt is journal-issued only")

    def is_authority_issued(self) -> bool:
        return getattr(self, "_marker", None) is _CLAIM_MARKER


def _issue_dispatch_claim_receipt(record: DispatchClaimRecord) -> DispatchClaimReceipt:
    receipt = object.__new__(DispatchClaimReceipt)
    digest = canonical_contract_digest("dispatch-claim-receipt", 1, (c_digest("dispatch-claim-record", 1, record.claim_record_digest),))
    for name, value in (("record", record), ("claim_record_digest", record.claim_record_digest),
                        ("receipt_digest", digest), ("_marker", _CLAIM_MARKER)):
        object.__setattr__(receipt, name, value)
    return receipt


@dataclass(frozen=True)
class ProviderDispatchBinding:
    prepared_receipt: PreparedModelInputReceipt
    claim_receipt: DispatchClaimReceipt
    dispatch_binding_digest: str = field(init=False)

    def __post_init__(self) -> None:
        if not self.prepared_receipt.is_authority_issued() or not self.claim_receipt.is_authority_issued():
            raise ValueError("authority-issued preparation and claim receipts are required")
        record = self.claim_receipt.record
        if (record.execution_id != self.prepared_receipt.execution_id
                or record.attempt_digest != self.prepared_receipt.attempt_digest
                or record.prepared_receipt_digest != self.prepared_receipt.receipt_digest
                or record.model_input_digest != self.prepared_receipt.model_input_digest):
            raise ValueError("dispatch claim and prepared input mismatch")
        fields = (c_digest("prepared-model-input-receipt", 1, self.prepared_receipt.receipt_digest),
                  c_digest("dispatch-claim-receipt", 1, self.claim_receipt.receipt_digest))
        object.__setattr__(self, "dispatch_binding_digest", canonical_contract_digest("provider-dispatch-binding", 1, fields))


@dataclass(frozen=True)
class DispatchAuthorizationRecord:
    dispatch_binding_digest: str
    claim_record_digest: str
    dispatch_claim_id: str
    dispatch_fence: int
    authorization_record_digest: str = field(init=False)

    def __post_init__(self) -> None:
        fields = (c_digest("provider-dispatch-binding", 1, self.dispatch_binding_digest),
                  c_digest("dispatch-claim-record", 1, self.claim_record_digest),
                  c_id(self.dispatch_claim_id), c_int(self.dispatch_fence))
        object.__setattr__(self, "authorization_record_digest", canonical_contract_digest("dispatch-authorization-record", 1, fields))


_AUTHORIZATION_MARKER = object()


@dataclass(frozen=True, init=False)
class DispatchAuthorizationReceipt:
    record: DispatchAuthorizationRecord
    authorization_record_digest: str
    receipt_digest: str
    _marker: object = field(repr=False, compare=False)

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise TypeError("DispatchAuthorizationReceipt is journal-issued only")

    def is_authority_issued(self) -> bool:
        return getattr(self, "_marker", None) is _AUTHORIZATION_MARKER


def _issue_dispatch_authorization_receipt(record: DispatchAuthorizationRecord) -> DispatchAuthorizationReceipt:
    receipt = object.__new__(DispatchAuthorizationReceipt)
    digest = canonical_contract_digest("dispatch-authorization-receipt", 1, (c_digest("dispatch-authorization-record", 1, record.authorization_record_digest),))
    for name, value in (("record", record), ("authorization_record_digest", record.authorization_record_digest),
                        ("receipt_digest", digest), ("_marker", _AUTHORIZATION_MARKER)):
        object.__setattr__(receipt, name, value)
    return receipt


@dataclass(frozen=True)
class PreparedProviderRequest:
    body: bytes
    media_type: str
    generation_settings: GenerationSettings

    def __post_init__(self) -> None:
        if not isinstance(self.body, bytes) or not isinstance(self.generation_settings, GenerationSettings):
            raise ValueError("prepared provider request is invalid")

"""Protocol models for the GOVQ canonical execution boundary.

This module is transport-only.  It performs schema and size validation and
defines the public error taxonomy; it does not call providers, retrieval,
Qdrant, or the network.
"""

from __future__ import annotations

import json
from enum import Enum
from types import MappingProxyType
from typing import Any, Literal, Mapping

from pydantic import BaseModel, ConfigDict, Field, model_validator


PROTOCOL_VERSION = "1.0"

MAX_MESSAGES = 12
MAX_MESSAGE_CONTENT_UTF8_BYTES = 16_384
MAX_MESSAGES_TOTAL_UTF8_BYTES = 65_536
MAX_CONTEXT_SERIALIZED_UTF8_BYTES = 32_768
# Enforced here after parsing by measuring deterministic compact JSON.
MAX_CANONICAL_REQUEST_UTF8_BYTES = 131_072
# Transport-only limit. The HTTP boundary must enforce this against raw bytes before parsing.
MAX_HTTP_REQUEST_BODY_BYTES = 131_072

IDENTIFIER_PATTERN = r"^[A-Za-z0-9._:@-]+$"

RequestId = str
ServiceId = str
OperationId = str
ProfileId = str
RunId = str


def _json_utf8_size(value: Any) -> int:
    """Return deterministic compact JSON size in UTF-8 bytes."""

    try:
        serialized = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("value must be JSON serializable") from exc
    return len(serialized.encode("utf-8"))


def _utf8_size(value: str) -> int:
    """Return UTF-8 size and turn non-encodable text into validation failure."""

    try:
        return len(value.encode("utf-8"))
    except UnicodeEncodeError as exc:
        raise ValueError("value must contain valid UTF-8 text") from exc


class ProtocolModel(BaseModel):
    """Strict base model shared by every public protocol object."""

    model_config = ConfigDict(extra="forbid")


class Message(ProtocolModel):
    role: Literal["user", "assistant"]
    content: str

    @model_validator(mode="after")
    def validate_content_size(self) -> "Message":
        content_size = _utf8_size(self.content)
        if content_size == 0:
            raise ValueError("message content must be non-empty UTF-8")
        if content_size > MAX_MESSAGE_CONTENT_UTF8_BYTES:
            raise ValueError(
                f"message content exceeds {MAX_MESSAGE_CONTENT_UTF8_BYTES} UTF-8 bytes"
            )
        return self


class ExecutionRequest(ProtocolModel):
    """Canonical non-streaming request for POST /core/v1/executions.

    ``run_id`` and ``stream`` are intentionally absent.  Because extra fields
    are forbidden, either field is rejected for every supplied value.
    """

    protocol_version: Literal[PROTOCOL_VERSION]
    request_id: RequestId = Field(min_length=1, max_length=128, pattern=IDENTIFIER_PATTERN)
    service_id: ServiceId = Field(min_length=1, max_length=64, pattern=IDENTIFIER_PATTERN)
    operation: OperationId = Field(min_length=1, max_length=64, pattern=IDENTIFIER_PATTERN)
    profile_id: ProfileId = Field(min_length=1, max_length=64, pattern=IDENTIFIER_PATTERN)
    messages: list[Message] = Field(min_length=1, max_length=MAX_MESSAGES)
    context: dict[str, Any]

    @model_validator(mode="after")
    def validate_aggregate_sizes(self) -> "ExecutionRequest":
        messages_size = sum(_utf8_size(message.content) for message in self.messages)
        if messages_size > MAX_MESSAGES_TOTAL_UTF8_BYTES:
            raise ValueError(
                f"messages exceed {MAX_MESSAGES_TOTAL_UTF8_BYTES} aggregate UTF-8 bytes"
            )

        context_size = _json_utf8_size(self.context)
        if context_size > MAX_CONTEXT_SERIALIZED_UTF8_BYTES:
            raise ValueError(
                f"context exceeds {MAX_CONTEXT_SERIALIZED_UTF8_BYTES} serialized UTF-8 bytes"
            )

        canonical_size = _json_utf8_size(self.model_dump(mode="json"))
        if canonical_size > MAX_CANONICAL_REQUEST_UTF8_BYTES:
            raise ValueError(
                f"request exceeds {MAX_CANONICAL_REQUEST_UTF8_BYTES} canonical UTF-8 bytes"
            )
        return self


class ExecutionResponse(ProtocolModel):
    protocol_version: Literal[PROTOCOL_VERSION] = PROTOCOL_VERSION
    request_id: RequestId = Field(min_length=1, max_length=128, pattern=IDENTIFIER_PATTERN)
    run_id: RunId = Field(min_length=1, max_length=128, pattern=IDENTIFIER_PATTERN)
    status: Literal["SUCCESS"] = "SUCCESS"
    result: Any
    requested: dict[str, Any]
    resolved: dict[str, Any]
    observed: dict[str, Any]


class ErrorCode(str, Enum):
    AUTH_MISSING = "AUTH_MISSING"
    AUTH_INVALID = "AUTH_INVALID"
    AUTH_EXPIRED = "AUTH_EXPIRED"
    SERVICE_ID_MISMATCH = "SERVICE_ID_MISMATCH"
    PROFILE_FORBIDDEN = "PROFILE_FORBIDDEN"
    OPERATION_FORBIDDEN = "OPERATION_FORBIDDEN"
    PROTOCOL_UNSUPPORTED = "PROTOCOL_UNSUPPORTED"
    REQUEST_INVALID = "REQUEST_INVALID"
    REQUEST_TOO_LARGE = "REQUEST_TOO_LARGE"
    CORE_NOT_READY = "CORE_NOT_READY"
    UPSTREAM_FAILURE = "UPSTREAM_FAILURE"
    TRACE_PERSISTENCE_FAILURE = "TRACE_PERSISTENCE_FAILURE"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class ErrorSpec(ProtocolModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    http_status: int
    message: str
    retryable: bool


ERROR_SPECS: Mapping[ErrorCode, ErrorSpec] = MappingProxyType(
    {
        ErrorCode.AUTH_MISSING: ErrorSpec(http_status=401, message="Service authentication is required.", retryable=False),
        ErrorCode.AUTH_INVALID: ErrorSpec(http_status=401, message="Service authentication failed.", retryable=False),
        ErrorCode.AUTH_EXPIRED: ErrorSpec(http_status=401, message="Service authentication has expired.", retryable=False),
        ErrorCode.SERVICE_ID_MISMATCH: ErrorSpec(http_status=403, message="Service identity does not match the authenticated caller.", retryable=False),
        ErrorCode.PROFILE_FORBIDDEN: ErrorSpec(http_status=403, message="The authenticated service is not allowed to use this profile.", retryable=False),
        ErrorCode.OPERATION_FORBIDDEN: ErrorSpec(http_status=403, message="The authenticated service is not allowed to perform this operation.", retryable=False),
        ErrorCode.PROTOCOL_UNSUPPORTED: ErrorSpec(http_status=400, message="The requested protocol version is not supported.", retryable=False),
        ErrorCode.REQUEST_INVALID: ErrorSpec(http_status=422, message="The request is invalid.", retryable=False),
        ErrorCode.REQUEST_TOO_LARGE: ErrorSpec(http_status=413, message="The request exceeds an allowed size limit.", retryable=False),
        ErrorCode.CORE_NOT_READY: ErrorSpec(http_status=503, message="Core is not ready to execute this request.", retryable=True),
        ErrorCode.UPSTREAM_FAILURE: ErrorSpec(http_status=502, message="An upstream execution dependency failed.", retryable=True),
        ErrorCode.TRACE_PERSISTENCE_FAILURE: ErrorSpec(http_status=503, message="Execution evidence could not be persisted.", retryable=True),
        ErrorCode.INTERNAL_ERROR: ErrorSpec(http_status=500, message="An internal error occurred.", retryable=False),
    }
)


class ErrorDetail(ProtocolModel):
    code: ErrorCode
    message: str
    retryable: bool

    @model_validator(mode="after")
    def enforce_locked_spec(self) -> "ErrorDetail":
        spec = ERROR_SPECS[self.code]
        if self.message != spec.message or self.retryable != spec.retryable:
            raise ValueError("error detail does not match the locked public specification")
        return self


class ErrorResponse(ProtocolModel):
    protocol_version: Literal[PROTOCOL_VERSION] = PROTOCOL_VERSION
    request_id: str = Field(max_length=128, pattern=r"^(?:[A-Za-z0-9._:@-]+)?$")
    run_id: RunId = Field(min_length=1, max_length=128, pattern=IDENTIFIER_PATTERN)
    status: Literal["ERROR"] = "ERROR"
    error: ErrorDetail

    @classmethod
    def from_code(cls, *, code: ErrorCode, request_id: str, run_id: str) -> "ErrorResponse":
        spec = ERROR_SPECS[code]
        return cls(
            request_id=request_id,
            run_id=run_id,
            error=ErrorDetail(code=code, message=spec.message, retryable=spec.retryable),
        )


__all__ = [
    "ERROR_SPECS",
    "IDENTIFIER_PATTERN",
    "MAX_CANONICAL_REQUEST_UTF8_BYTES",
    "MAX_CONTEXT_SERIALIZED_UTF8_BYTES",
    "MAX_HTTP_REQUEST_BODY_BYTES",
    "MAX_MESSAGE_CONTENT_UTF8_BYTES",
    "MAX_MESSAGES",
    "MAX_MESSAGES_TOTAL_UTF8_BYTES",
    "PROTOCOL_VERSION",
    "ErrorCode",
    "ErrorDetail",
    "ErrorResponse",
    "ErrorSpec",
    "ExecutionRequest",
    "ExecutionResponse",
    "Message",
]

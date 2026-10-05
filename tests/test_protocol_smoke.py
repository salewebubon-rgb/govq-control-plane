import pytest
from pydantic import ValidationError

from govq.protocol import ErrorCode, ErrorResponse, ExecutionRequest, PROTOCOL_VERSION


def _valid_request():
    return {
        "protocol_version": PROTOCOL_VERSION,
        "request_id": "request-1",
        "service_id": "service-1",
        "operation": "chat",
        "profile_id": "default",
        "messages": [{"role": "user", "content": "hello"}],
        "context": {},
    }


def test_valid_request_is_accepted():
    request = ExecutionRequest(**_valid_request())
    assert request.protocol_version == PROTOCOL_VERSION
    assert request.request_id == "request-1"


def test_unknown_protocol_field_is_rejected():
    payload = _valid_request()
    payload["stream"] = False
    with pytest.raises(ValidationError):
        ExecutionRequest(**payload)


def test_error_response_uses_locked_public_spec():
    response = ErrorResponse.from_code(
        code=ErrorCode.AUTH_MISSING,
        request_id="request-1",
        run_id="run-1",
    )
    assert response.status == "ERROR"
    assert response.error.code is ErrorCode.AUTH_MISSING
    assert response.error.retryable is False
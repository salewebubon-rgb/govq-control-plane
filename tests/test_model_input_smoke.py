import pytest

from govq.providers.model_input import (
    ResolvedTransportSemantics,
    canonical_contract_digest,
    c_str,
)


def test_canonical_digest_is_deterministic():
    first = canonical_contract_digest("public-test", 1, (c_str("hello"),))
    second = canonical_contract_digest("public-test", 1, (c_str("hello"),))
    assert first == second
    assert len(first) == 64


def test_credential_bearing_semantic_header_is_rejected():
    with pytest.raises(ValueError):
        ResolvedTransportSemantics(
            protocol_id="http",
            protocol_version="1.1",
            logical_endpoint_id="provider",
            endpoint_uri_bytes=b"https://example.invalid",
            operation_id="chat",
            method="POST",
            request_media_type="application/json",
            semantic_headers=(("authorization", b"secret"),),
        )
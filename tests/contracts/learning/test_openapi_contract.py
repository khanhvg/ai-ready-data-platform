from __future__ import annotations

import unittest

from tests.contracts.learning import assert_invalid, fixture


class OpenApiBehaviorTest(unittest.TestCase):
    def test_operation_set(self) -> None:
        assert_invalid(self, "I8-OPENAPI-MATRIX-160", "openapi", fixture("invalid/openapi/orphan-operation.json"), "OPENAPI_OPERATION_SET_MISMATCH")

    def test_authority(self) -> None:
        assert_invalid(self, "I8-OPENAPI-AUTH-161", "openapi", fixture("invalid/openapi/missing-authority.json"), "OPERATION_AUTHORITY_MISSING")

    def test_idempotency(self) -> None:
        assert_invalid(self, "I8-OPENAPI-IDEMPOTENCY-162", "openapi", fixture("invalid/openapi/missing-idempotency.json"), "OPERATION_IDEMPOTENCY_MISSING")

    def test_raw_query(self) -> None:
        assert_invalid(self, "I8-OPENAPI-RAW-163", "openapi", fixture("invalid/openapi/raw-sql-query.json"), "OPENAPI_RAW_QUERY_FORBIDDEN")

    def test_remote_ref(self) -> None:
        assert_invalid(self, "I8-OPENAPI-REF-164", "openapi", fixture("invalid/openapi/remote-ref.json"), "OPENAPI_REF_FORBIDDEN")

    def test_version_header(self) -> None:
        assert_invalid(self, "I8-OPENAPI-VERSION-165", "openapi", fixture("invalid/openapi/missing-version-response.json"), "OPENAPI_VERSION_NEGOTIATION_INCOMPLETE")

    def test_no_asyncapi_without_channel(self) -> None:
        assert_invalid(self, "I8-ASYNCAPI-166", "openapi", fixture("invalid/openapi/orphan-asyncapi.json"), "ASYNCAPI_WITHOUT_CHANNEL")

    def test_request_shape(self) -> None:
        assert_invalid(self, "I8-OPENAPI-REQUEST-173", "openapi", fixture("invalid/openapi/request-shape-drift.json"), "OPENAPI_REQUEST_CONTRACT_MISMATCH")

    def test_response_shape(self) -> None:
        assert_invalid(self, "I8-OPENAPI-RESPONSE-174", "openapi", fixture("invalid/openapi/response-shape-drift.json"), "OPENAPI_RESPONSE_CONTRACT_MISMATCH")

    def test_error_set(self) -> None:
        assert_invalid(self, "I8-OPENAPI-ERROR-175", "openapi", fixture("invalid/openapi/error-set-drift.json"), "OPENAPI_ERROR_CONTRACT_MISMATCH")

    def test_duplicate_yaml_key(self) -> None:
        assert_invalid(self, "I8-OPENAPI-YAML-179", "openapi", fixture("invalid/openapi/duplicate-key.yaml"), "OPENAPI_YAML_DUPLICATE_KEY")

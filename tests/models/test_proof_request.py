import pytest
import json
import logging

from aries_cloudcontroller.models.proof_request import ProofRequest

LOGGER = logging.getLogger(__name__)

pytest.proof_keys = [
    "connection_id",
    "version",
    "name",
    "requested_attributes",
    "requested_predicates",
]

# From sample in https://github.com/hyperledger/aries-cloudagent-python/issues/175
pytest.valid_proof_request = json.dumps(
    {
        "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
        "version": "1.0.0",
        "name": "Proof of Name",
        "requested_attributes": [
            {
                "name": "name",
                "restrictions": [
                    {"cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"},
                    {"value": "Alice Jones"},
                ],
            }
        ],
        "requested_predicates": [],
    }
)

pytest.multi_attrs = json.dumps(
    {
        "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
        "version": "1.0.0",
        "name": "Proof of Name",
        "requested_attributes": [
            {
                "name": "name",
                "restrictions": [
                    {"cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"},
                    {"value": "Alice Jones"},
                ],
            },
            {
                "name": "name",
                "restrictions": [
                    {"cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"},
                    {"value": "Alice Jones"},
                ],
            },
        ],
        "requested_predicates": [],
    }
)

pytest.multi_predicates = json.dumps(
    {
        "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
        "version": "1.0.0",
        "name": "Proof of Name",
        "requested_attributes": [],
        "requested_predicates": [
            {
                "name": "name",
                "restrictions": [
                    {"cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"},
                    {"value": "Alice Jones"},
                ],
            },
            {
                "name": "name",
                "restrictions": [
                    {"cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"},
                    {"value": "Alice Jones"},
                ],
            },
        ],
    }
)

pytest.not_json = 123456

pytest.invalid_proof_request = json.dumps({"abc": "1234"})

pytest.no_requested_attrs = json.dumps(
    {
        "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
        "version": "1.0.0",
        "name": "Proof of Name",
        "requested_attributes": [],
        "requested_predicates": [],
    }
)


def test_init_valid():
    proof = ProofRequest(pytest.valid_proof_request)
    assert proof.json_data == json.loads(pytest.valid_proof_request)


def test_init_invalid():
    with pytest.raises(AssertionError, match="Missing key"):
        ProofRequest(pytest.invalid_proof_request)


def test_init_not_json(caplog):
    error_msg = "the JSON object must be str, bytes or bytearray, not int"
    with pytest.raises(TypeError, match=error_msg):
        ProofRequest(pytest.not_json)
    assert "Failed to load proof request JSON" in caplog.text


# check for each possibly missing key whether the correct error is raised
@pytest.mark.parametrize("key", pytest.proof_keys)
def test_validate_presentation_json(key):
    proof = pytest.valid_proof_request
    proof_obj = ProofRequest(proof)
    with pytest.raises(AssertionError, match=f"Missing key {key}"):
        del proof_obj.json_data[key]
        proof_obj.validate_proof_request_json(json.dumps(proof_obj.json_data))


def test_requested_attributes_empty(caplog):
    requested_attrs = ProofRequest(pytest.no_requested_attrs).get_requested_attributes()
    assert requested_attrs == []


def test_requested_predicates_empty(caplog):
    requested_predicates = ProofRequest(
        pytest.valid_proof_request
    ).get_requested_predicates()
    assert requested_predicates == []


def test_requested_attributes(caplog):
    expected = [
        {
            "name": "name",
            "restrictions": [
                {"cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"},
                {"value": "Alice Jones"},
            ],
        }
    ]
    requested_attrs = ProofRequest(
        pytest.valid_proof_request
    ).get_requested_attributes()
    assert requested_attrs == expected


def test_multi_attributes(caplog):
    expected = [
        {
            "name": "name",
            "restrictions": [
                {"cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"},
                {"value": "Alice Jones"},
            ],
        },
        {
            "name": "name",
            "restrictions": [
                {"cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"},
                {"value": "Alice Jones"},
            ],
        },
    ]
    requested_attrs = ProofRequest(pytest.multi_attrs).get_requested_attributes()
    assert requested_attrs == expected


def test_multi_preds(caplog):
    expected = [
        {
            "name": "name",
            "restrictions": [
                {"cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"},
                {"value": "Alice Jones"},
            ],
        },
        {
            "name": "name",
            "restrictions": [
                {"cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"},
                {"value": "Alice Jones"},
            ],
        },
    ]
    requested_attrs = ProofRequest(pytest.multi_predicates).get_requested_predicates()
    assert requested_attrs == expected


def test_get_connection_id():
    expected = "d965bd54-affb-4e11-ba8e-ea54a3214123"
    connection_id = ProofRequest(pytest.valid_proof_request).get_connection_id()
    assert connection_id == expected


def test_get_version():
    expected = "1.0.0"
    version = ProofRequest(pytest.valid_proof_request).get_version()
    assert version == expected


def test_get_name():
    expected = "Proof of Name"
    name = ProofRequest(pytest.valid_proof_request).get_name()
    assert name == expected

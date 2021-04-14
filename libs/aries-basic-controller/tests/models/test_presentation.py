import pytest
import json
import logging

from aries_cloudcontroller.models.presentation import Presentation

LOGGER = logging.getLogger(__name__)

presentation_keys = [
    "auto_present",
    "connection_id",
    "created_at",
    "error_msg",
    "initiator",
    "presentation",
    "presentation_exchange_id",
    "presentation_proposal_dict",
    "presentation_request",
    "presentation_request_dict",
    "role",
    "state",
    "thread_id",
    "trace",
    "updated_at",
    "verified",
]

# From sample response in Swagger UI
pytest.valid_presentation = json.dumps(
    {
        "auto_present": "false",
        "connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "created_at": "2021-04-08 09:04:01Z",
        "error_msg": "Invalid structure",
        "initiator": "self",
        "presentation": {},
        "presentation_exchange_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "presentation_proposal_dict": {},
        "presentation_request": {},
        "presentation_request_dict": {},
        "role": "prover",
        "state": "verified",
        "thread_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "trace": "true",
        "updated_at": "2021-04-08 09:04:01Z",
        "verified": "true",
    }
)

pytest.unverified_presentation = json.dumps(
    {
        "auto_present": "false",
        "connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "created_at": "2021-04-08 09:04:01Z",
        "error_msg": "Invalid structure",
        "initiator": "self",
        "presentation": {},
        "presentation_exchange_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "presentation_proposal_dict": {},
        "presentation_request": {},
        "presentation_request_dict": {},
        "role": "prover",
        "state": "verified",
        "thread_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "trace": "true",
        "updated_at": "2021-04-08 09:04:01Z",
        "verified": "false",
    }
)

pytest.invalid_presentation = json.dumps({"abc": "1234"})

pytest.not_json = 123456

pytest.self_attested_attrs_json = json.dumps(
    {
        "auto_present": "false",
        "connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "created_at": "2021-04-08 09:04:01Z",
        "error_msg": "Invalid structure",
        "initiator": "self",
        "presentation": {
            "requested_proof": {
                "self_attested_attrs": {
                    "item1": {"raw": "sth"},
                    "item2": {"raw": "sth"},
                    "item3": {"raw": "sth"},
                },
            },
        },
        "presentation_exchange_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "presentation_proposal_dict": {},
        "presentation_request": {},
        "presentation_request_dict": {},
        "role": "prover",
        "state": "verified",
        "thread_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "trace": "true",
        "updated_at": "2021-04-08 09:04:01Z",
        "verified": "true",
    }
)

pytest.revealed_attrs_json = json.dumps(
    {
        "auto_present": "false",
        "connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "created_at": "2021-04-08 09:04:01Z",
        "error_msg": "Invalid structure",
        "initiator": "self",
        "presentation": {
            "requested_proof": {
                "revealed_attrs": {
                    "item1": {"raw": "sth"},
                    "item2": {"raw": "sth"},
                    "item3": {"raw": "sth"},
                },
            },
        },
        "presentation_exchange_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "presentation_proposal_dict": {},
        "presentation_request": {},
        "presentation_request_dict": {},
        "role": "prover",
        "state": "verified",
        "thread_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "trace": "true",
        "updated_at": "2021-04-08 09:04:01Z",
        "verified": "true",
    }
)

pytest.unrevealed_attrs_json = json.dumps(
    {
        "auto_present": "false",
        "connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "created_at": "2021-04-08 09:04:01Z",
        "error_msg": "Invalid structure",
        "initiator": "self",
        "presentation": {
            "requested_proof": {
                "unrevealed_attrs": {
                    "item1": {"raw": "sth"},
                    "item2": {"raw": "sth"},
                    "item3": {"raw": "sth"},
                },
            },
        },
        "presentation_exchange_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "presentation_proposal_dict": {},
        "presentation_request": {},
        "presentation_request_dict": {},
        "role": "prover",
        "state": "verified",
        "thread_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "trace": "true",
        "updated_at": "2021-04-08 09:04:01Z",
        "verified": "true",
    }
)

pytest.predicates_attrs_json = json.dumps(
    {
        "auto_present": "false",
        "connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "created_at": "2021-04-08 09:04:01Z",
        "error_msg": "Invalid structure",
        "initiator": "self",
        "presentation": {
            "requested_proof": {
                "predicates": {
                    "item1": {"raw": "sth"},
                    "item2": {"raw": "sth"},
                    "item3": {"raw": "sth"},
                },
            },
        },
        "presentation_exchange_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "presentation_proposal_dict": {},
        "presentation_request": {},
        "presentation_request_dict": {},
        "role": "prover",
        "state": "verified",
        "thread_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "trace": "true",
        "updated_at": "2021-04-08 09:04:01Z",
        "verified": "true",
    }
)

pytest.identifiers_json = json.dumps(
    {
        "auto_present": "false",
        "connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "created_at": "2021-04-08 09:04:01Z",
        "error_msg": "Invalid structure",
        "initiator": "self",
        "presentation": {
            "identifiers": [
                {
                    "rev_reg_id": "123456789",
                    "cred_def_id": "123456789",
                    "schema_id": "123456789",
                },
                {
                    "rev_reg_id": "987654321",
                    "cred_def_id": "987654321",
                    "schema_id": "987654321",
                },
            ]
        },
        "presentation_exchange_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "presentation_proposal_dict": {},
        "presentation_request": {},
        "presentation_request_dict": {},
        "role": "prover",
        "state": "verified",
        "thread_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "trace": "true",
        "updated_at": "2021-04-08 09:04:01Z",
        "verified": "true",
    }
)


def test_init_valid():
    pres = Presentation(pytest.valid_presentation)
    assert pres.json_data == json.loads(pytest.valid_presentation)


def test_init_invalid():
    with pytest.raises(AssertionError, match="Missing key"):
        Presentation(pytest.invalid_presentation)


def test_init_unverified(caplog):
    error_msg = "Presentation Object Verification not verified"
    with pytest.raises(Exception, match=error_msg):
        Presentation(pytest.unverified_presentation)
    assert error_msg in caplog.text


def test_init_not_json(caplog):
    error_msg = "the JSON object must be str, bytes or bytearray, not int"
    with pytest.raises(TypeError, match=error_msg):
        Presentation(pytest.not_json)
    assert "Failed to load presentation JSON" in caplog.text


# check for each possibly missing key whether the correct error is raised
@pytest.mark.parametrize("key", presentation_keys)
def test_validate_presentation_json(key):
    pres = pytest.valid_presentation
    pres_obj = Presentation(pres)
    with pytest.raises(AssertionError, match=f"Missing key {key}"):
        del pres_obj.json_data[key]
        pres_obj.validate_presentation_json(json.dumps(pres_obj.json_data))


def test_has_no_identifiers(caplog):
    error_msg = "No key 'identifiers' in presentation"
    with pytest.raises(AssertionError, match=error_msg):
        Presentation(pytest.valid_presentation).get_cred_def_ids()
    assert error_msg in caplog.text


def test_get_role():
    expected = "prover"
    result = Presentation(pytest.valid_presentation).get_role()
    assert result == expected


def test_get_threadid():
    expected = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    result = Presentation(pytest.valid_presentation).get_threadid()
    assert result == expected


def test_get_presentation_request():
    expected = {}
    result = Presentation(pytest.valid_presentation).get_presentation_request()
    assert result == expected


def test_get_verified_state():
    expected = "verified"
    result = Presentation(pytest.valid_presentation).get_verified_state()
    assert result == expected


def test_get_presxid():
    expected = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    result = Presentation(pytest.valid_presentation).get_presxid()
    assert result == expected


def test_get_from_conn_id():
    expected = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    result = Presentation(pytest.valid_presentation).get_from_conn_id()
    assert result == expected


def test_get_rev_reg_ids():
    expected = '{"rev_reg_id": ["123456789", "987654321"]}'
    result = Presentation(pytest.identifiers_json).get_rev_reg_ids()
    assert result == expected


def test_get_cred_def_ids():
    expected = '{"cred_def_id": ["123456789", "987654321"]}'
    result = Presentation(pytest.identifiers_json).get_cred_def_ids()
    assert result == expected


def test_get_schemas():
    expected = '{"schema_id": ["123456789", "987654321"]}'
    result = Presentation(pytest.identifiers_json).get_schemas()
    assert result == expected


def test_get_identifiers():
    expected = json.dumps(
        {
            "identifiers": [
                {
                    "rev_reg_id": "123456789",
                    "cred_def_id": "123456789",
                    "schema_id": "123456789",
                },
                {
                    "rev_reg_id": "987654321",
                    "cred_def_id": "987654321",
                    "schema_id": "987654321",
                },
            ]
        }
    )
    result = Presentation(pytest.identifiers_json).get_identifiers()
    assert result == expected


def test_get_predicates():
    expected = json.dumps(
        {
            "item1": "sth",
            "item2": "sth",
            "item3": "sth",
        }
    )
    result = Presentation(pytest.predicates_attrs_json).get_predicates()
    assert expected == result


def test_get_unrevealed_attrs():
    expected = json.dumps(
        {
            "item1": "sth",
            "item2": "sth",
            "item3": "sth",
        }
    )
    result = Presentation(pytest.unrevealed_attrs_json).get_unrevealed_attrs()
    assert expected == result


def test_get_revealed_attrs():
    expected = json.dumps(
        {
            "item1": "sth",
            "item2": "sth",
            "item3": "sth",
        }
    )
    result = Presentation(pytest.revealed_attrs_json).get_revealed_attrs()
    assert expected == result


def test_get_self_attested():
    expected = json.dumps(
        {
            "item1": "sth",
            "item2": "sth",
            "item3": "sth",
        }
    )
    result = Presentation(pytest.self_attested_attrs_json).get_self_attested_attrs()
    assert expected == result

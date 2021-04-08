import pytest
import json
import logging

from ..models.presentation import Presentation

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
                "verified"
            ]

# From sample response in Swagger UI
pytest.valid_presentation = json.dumps({
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
    "verified": "true"
    })

pytest.unverified_presentation = json.dumps({
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
    "verified": "false"
    })

pytest.invalid_presentation = json.dumps({
    "abc": "1234"
    })

pytest.not_json = 123456


def test_init_valid():
    pres = Presentation(pytest.valid_presentation)
    assert pres.json_data == json.loads(pytest.valid_presentation)


def test_init_invalid():
    with pytest.raises(AssertionError,
                       match="Missing key"):
        Presentation(pytest.invalid_presentation)


def test_init_unverified(caplog):
    error_msg = "Presentation Object Verification not verified"
    with pytest.raises(Exception,
                       match=error_msg):
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
    with pytest.raises(AssertionError,
                       match=f"Missing key {key}"):
        del pres_obj.json_data[key]
        pres_obj.validate_presentation_json(json.dumps(pres_obj.json_data))


def test_has_no_identifiers(caplog):
    error_msg = "No key 'identifiers' in presentation"
    with pytest.raises(AssertionError,
                       match=error_msg):
        Presentation(pytest.valid_presentation).get_cred_def_ids()
    assert error_msg in caplog.text

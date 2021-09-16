import pydantic
import pytest
import logging

from aries_cloudcontroller.model.v10_presentation_exchange import (
    V10PresentationExchange,
)

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
valid_presentation = {
    "auto_present": "false",
    "connection_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "created_at": "2021-04-08 09:04:01Z",
    "error_msg": "Invalid structure",
    "initiator": "self",
    "presentation": {},
    "presentation_exchange_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "presentation_proposal_dict": {
        "presentation_proposal": {"attributes": [], "predicates": []}
    },
    "presentation_request": {},
    "presentation_request_dict": {"request_presentations~attach": [{"data": {}}]},
    "role": "prover",
    "state": "verified",
    "thread_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "trace": "true",
    "updated_at": "2021-04-08 09:04:01Z",
    "verified": "true",
}

invalid_presentation = {"abc": "1234"}


def test_init_valid():
    # Should not throw validation errors
    V10PresentationExchange(**valid_presentation)


def test_init_invalid():
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        V10PresentationExchange(role="random")

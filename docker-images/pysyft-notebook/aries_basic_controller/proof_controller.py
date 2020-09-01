from .base_controller import BaseController
from aiohttp import ClientSession
import logging
from typing import List

logger = logging.getLogger("aries_controller.proof")

PRES_PREVIEW = "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0/presentation-preview"

class ProofController(BaseController):

    def __init__(self, admin_url: str, client_session: ClientSession):
        super().__init__(admin_url, client_session)
        self.base_url = "/present-proof"

    def default_handler(self, payload):
        logger.debug("Present Proof Message received", payload)

    async def get_records(self, connection_id: str = None, thread_id: str = None, state: str = None, role: str = None):
        params = {}
        if connection_id:
            params["connection_id"] = connection_id
        if thread_id:
            params["thread_id"] = thread_id
        if state:
            params["state"] = state
        if role:
            params["role"] = role

        return await self.admin_GET(f"{self.base_url}/records", params=params)

    async def get_record_by_id(self, pres_ex_id):
        return await self.admin_GET(f"{self.base_url}/records/{pres_ex_id}")

    # Fetch a single presentation exchange record
    async def get_presentation_credentials(self, pres_ex_id, count: int = None, wql_query: str = None, start: int = None, referent: str = None):
        params = {}
        if count:
            params["count"] = count
        # Not sure what this does
        if wql_query:
            params["extra_query"] = wql_query
        if start:
            params["start"] = start
        # Not sure what this does
        if referent:
            params["referent"] = referent

        return await self.admin_GET(f"{self.base_url}/records/{pres_ex_id}/credentials", params=params)

    # Sends a presentation proposal
    async def send_proposal(self, connection_id, attributes: List = [], predicates: List = [], comment: str = "", auto_present: bool = True, trace: bool = False):
        body = {
            "presentation_proposal": {
                "@type": PRES_PREVIEW,
                "attributes": attributes,
                "predicates": predicates
            },
            "connection_id": connection_id,
            "comment": comment,
            "auto_present": auto_present,
            "trace": trace
        }

        return await self.admin_POST(f"{self.base_url}/send-proposal", data=body)

    # Creates a presentation request not bound to any proposal or existing connection
    async def create_request(self, proof_request, comment: str = "", trace: bool = False):
        # TODO How should proof request object be broken up? Complex.
        #  Do we want user to have to know how to build this object?
        body = {
            "trace": trace,
            "proof_request": proof_request,
            "comment": comment
        }
        return await self.admin_POST(f"{self.base_url}/create-request", data=body)


    # Sends a free presentation request not bound to any proposal
    async def send_request(self, connection_id, proof_request, comment: str = "", trace: bool = False):

        body = {
            "connection_id": connection_id,
            "proof_request": proof_request,
            "comment": comment,
            "trace": trace
        }
        return await self.admin_POST(f"{self.base_url}/send-request", data=body)

    async def send_request_for_proposal(self, connection_id, pres_ex_id, proof_request, comment: str = "", trace: bool = False):
        body = {
            "connection_id": connection_id,
            "proof_request": proof_request,
            "comment": comment,
            "trace": trace
        }
        return await self.admin_POST(f"{self.base_url}/records/{pres_ex_id}/send-request", data=body)

    # Send a proof presentation
    async def send_presentation(self, pres_ex_id, attrs, self_attested_attrs, predicates, trace: bool = False):
        body = {
            "requested_attributes": attrs,
            "self_attested_attributes": self_attested_attrs,
            "requested_predicates": predicates,
            "trace": trace
        }
        return await self.admin_POST(f"{self.base_url}/records/{pres_ex_id}/send-presentation", data=body)

    # Verify a received presentation
    async def verify_presentation(self, pres_ex_id):
        return await self.admin_POST(f"{self.base_url}/records/{pres_ex_id}/verify-presentation")

    async def remove_presentation_record(self, pres_ex_id):
        return await self.admin_POST(f"{self.base_url}/records/{pres_ex_id}/remove")

    # def build_proof_request(self, name, version, requested_attributes, requested_predicates):


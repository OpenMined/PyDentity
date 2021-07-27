from .base import BaseController
from aiohttp import ClientSession
import logging
from ..helpers.utils import extract_did, get_schema_details

logger = logging.getLogger("aries_controller.issuer2")

CRED_PREVIEW = (
    "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/2.0/credential-preview"
)


class IssuerV2Controller(BaseController):
    def __init__(
        self,
        admin_url: str,
        client_session: ClientSession,
        connection_controller,
        wallet_controller,
        definition_controller,
    ):
        super().__init__(admin_url, client_session)
        self.base_url = "/issue-credential-2.0"
        self.connections = connection_controller
        self.wallet = wallet_controller
        self.definitions = definition_controller

    # Fetch all credential exchange records
    async def get_records(
        self,
        connection_id: str = None,
        role: str = None,
        state: str = None,
        thread_id: str = None,
    ):
        params = {}
        if connection_id:
            params["connection_id"] = connection_id
        if role in ["issuer", "holder"]:
            params["role"] = role
        if state in [
            "proposal-sent",
            "proposal-received",
            "offer-sent",
            "offer-received",
            "request-sent",
            "request-received",
            "credential-issued",
            "credential-received",
            "done",
        ]:
            params["state"] = state
        if thread_id:
            params["thread_id"] = thread_id
        return await self.admin_GET(f"{self.base_url}/records", params=params)

    async def get_record_by_id(self, cred_ex_id):
        return await self.admin_GET(f"{self.base_url}/records/{cred_ex_id}")

    async def create_credential(self, body):
        return await self.admin_POST(f"{self.base_url}/create", json_data=body)

    # Send holder a credential, automating the entire flow
    async def send_credential2(
        self,
        connection_id,
        schema_id,
        cred_def_id,
        attributes,
        comment: str = "",
        auto_remove: bool = True,
        trace: bool = False,
    ):

        body = await self.create_credential_body(
            connection_id,
            schema_id,
            cred_def_id,
            attributes,
            comment,
            auto_remove,
            trace,
        )
        return await self.admin_POST(f"{self.base_url}/send", json_data=body)

    # Send Issuer a credential proposal
    async def send_proposal(
        self,
        connection_id,
        schema_id,
        cred_def_id,
        attributes,
        comment: str = "",
        auto_remove: bool = True,
        trace: bool = False,
    ):

        body = await self.create_credential_body(
            connection_id,
            schema_id,
            cred_def_id,
            attributes,
            comment,
            auto_remove,
            trace,
        )
        return await self.admin_POST(f"{self.base_url}/send-proposal", json_data=body)

    async def send_offer(
        self,
        connection_id,
        cred_def_id,
        attributes,
        comment: str = "",
        auto_issue: bool = True,
        auto_remove: bool = True,
        trace: bool = False,
    ):
        await self.connections.is_active(connection_id)
        offer_body = {
            "cred_def_id": cred_def_id,
            "auto_remove": auto_remove,
            "trace": trace,
            "comment": comment,
            "auto_issue": auto_issue,
            "credential_preview": {"@type": CRED_PREVIEW, "attributes": attributes},
            "connection_id": connection_id,
        }
        return await self.admin_POST(
            f"{self.base_url}/send-offer", json_data=offer_body
        )

    # Send holder a credential offer in reference to a proposal with preview
    async def send_offer_for_record(self, cred_ex_id):
        return await self.admin_POST(f"{self.base_url}/records/{cred_ex_id}/send-offer")

    # Send issuer a credential request
    async def send_request_for_record(self, cred_ex_id):
        return await self.admin_POST(
            f"{self.base_url}/records/{cred_ex_id}/send-request"
        )

    # Send holder a credential
    async def issue_credential(self, cred_ex_id: str, comment: str = None):
        body = {}
        if comment:
            body = {
                "comment": comment,
            }
        return await self.admin_POST(
            f"{self.base_url}/records/{cred_ex_id}/issue", json_data=body
        )

    # Store a received credential
    async def store_credential(self, cred_ex_id: str, credential_id: str = None):
        body = {}
        if credential_id:
            body["credential_id"] = credential_id
        return await self.admin_POST(
            f"{self.base_url}/records/{cred_ex_id}/store", json_data=body
        )

    # Remove an existing credential exchange record
    async def remove_record(self, cred_ex_id):
        return await self.admin_DELETE(f"{self.base_url}/records/{cred_ex_id}")

    # Send a problem report for a credential exchange
    async def problem_report(self, cred_ex_id, explanation: str):
        body = {"explain_ltxt": explanation}

        return await self.admin_POST(
            f"{self.base_url}/records/{cred_ex_id}/problem-report", json_data=body
        )

    # Used for both send and send-proposal bodies
    async def create_credential_body(
        self,
        connection_id,
        schema_id,
        cred_def_id,
        attributes,
        comment: str = "",
        auto_remove: bool = True,
        trace: bool = False,
        dif_criterion: str = "",
    ):
        # raises error if connection not active
        await self.connections.is_active(connection_id)

        schema_details = get_schema_details(schema_id)

        issuer_did = extract_did(cred_def_id)

        body = {
            "auto_remove": auto_remove,
            "comment": comment,
            "connection_id": connection_id,
            "credential_preview": {
                "@type": "issue-credential/2.0/credential-preview",
                "attributes": attributes,
            },
            "filter": {
                "indy": {
                    "cred_def_id": cred_def_id,
                    "schema_id": schema_id,
                    "issuer_did": issuer_did,
                },
            },
            "trace": trace,
        }
        credential_body = {**body, **schema_details}
        return credential_body

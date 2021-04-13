from .base import BaseController
from ..models.errors import InputError

from aiohttp import (
    ClientSession,
)
import asyncio


class RevocationController(BaseController):
    def __init__(self, admin_url: str, client_session: ClientSession):
        super().__init__(admin_url, client_session)
        self.base_url = "/revocation"
        self.revocation_states = set(["init", "generated", "posted", "active", "full"])

    async def revoke_credential(
        self,
        cred_ex_id: str = "",
        cred_rev_id: str = "",
        rev_reg_id: str = "",
        publish: bool = False,
    ):
        """
        Revoke an issued credential.

        This method does not publish revocation to the ledger immediately by default - instead, marks it as pending.
        Either (cred_ex_id) OR (cred_rev_id AND rev_reg_id) are required.
        """

        req_body = {"publish": publish}
        if cred_ex_id:
            req_body["cred_ex_id"] = cred_ex_id
        elif cred_rev_id and rev_reg_id:
            req_body["cred_rev_id"] = cred_rev_id
            req_body["rev_reg_id"] = rev_reg_id
        else:
            raise InputError(
                "Either (cred_ex_id) OR (cred_rev_id AND rev_reg_id) are required."
            )

        return await self.admin_POST(f"{self.base_url}/revoke", json_data=req_body)

    async def publish_pending_revocations(self, pending_revs):
        """
        Publish pending revocations to ledger.

        Takes in a list of dicts with str key-values, transforms into the correct
        API schema.

        eg. pending_revs = [{ "sample-rev-reg-id": "sample-cred-rev-id" }]
        """

        req_body = {"rrid2crid": {}}

        for rev in pending_revs:
            # check if revocation registry id already exists in map, if so, simply append to array
            if rev.rev_reg_id in req_body["rrid2crid"]:
                req_body["rrid2crid"][rev.rev_reg_id].append(rev.cred_rev_id)
            else:
                req_body["rrid2crid"][rev.rev_reg_id] = [rev.cred_rev_id]

        return await self.admin_POST(
            f"{self.base_url}/publish-revocations", json_data=req_body
        )

    async def clear_pending_revocations(self, pending_revs):
        """
        Clear pending revocations.

        Takes in a list of dicts with str key-values, transforms into the correct
        API schema.

        eg. pending_revs = [{ "sample-rev-reg-id": "sample-cred-rev-id" }]
        """

        req_body = {"purge": {}}

        for rev in pending_revs:
            # check if revocation registry id already exists in map, if so, simply append to array
            if rev.rev_reg_id in req_body["purge"]:
                req_body["purge"][rev.rev_reg_id].append(rev.cred_rev_id)
            else:
                req_body["purge"][rev.rev_reg_id] = [rev.cred_rev_id]

        return await self.admin_POST(
            f"{self.base_url}/clear-pending-revocations", json_data=req_body
        )

    async def get_credential_revocation_status(
        self, cred_ex_id: str, cred_rev_id: str, rev_reg_id: str
    ):
        """
        Get credential revocation status.
        """

        params = {}
        if cred_ex_id:
            params["cred_ex_id"] = cred_ex_id
        if cred_rev_id:
            params["cred_rev_id"] = cred_rev_id
        if rev_reg_id:
            params["rev_reg_id"] = rev_reg_id

        return await self.admin_GET(f"{self.base_url}/credential-record", params=params)

    async def get_created_revocation_registries(
        self, cred_def_id: str, rev_reg_state: str
    ):
        """
        Search for matching revocation registries that current agnet created.
        """

        params = {}
        if cred_def_id:
            params["cred_def_id"] = cred_def_id
        if rev_reg_state:
            if not self.__validate_revocation_registry_state(rev_reg_state):
                raise InputError("invalid revocation registry state input")
            params["state"] = rev_reg_state

        return await self.admin_GET(
            f"{self.base_url}/registries/created", params=params
        )

    async def get_revocation_registry(self, rev_reg_id: str):
        """
        Get revocation registry by revocation registry id
        """

        return await self.admin_GET(f"{self.base_url}/registry/{rev_reg_id}")

    async def update_revocation_registry_tails_file(
        self, rev_reg_id: str, tail_file_uri: str
    ):
        """
        Update revocation registry by revocation registry id.
        """

        req_body = {"tails_public_uri": tail_file_uri}

        return await self.admin_PATCH(
            f"{self.base_url}/registry/{rev_reg_id}", json_data=req_body
        )

    async def get_active_revocation_registry_by_cred_def(self, cred_def_id: str):
        """
        Get current active revocation registry by credential definition id.
        """

        return await self.admin_GET(f"{self.base_url}/active-registry/{cred_def_id}")

    async def get_num_credentials_issued_by_revocation_registry(self, rev_reg_id: str):
        """
        Get number of credentials issued against revocation registry.
        """

        response = await self.admin_GET(f"{self.base_url}/registry/{rev_reg_id}/issued")
        return response["result"]

    async def create_revocation_registry(self, cred_def_id: str, max_cred_num: int):
        """
        Creates a new revocation registry.
        """

        req_body = {
            "credential_definition_id": cred_def_id,
            "max_cred_num": max_cred_num,
        }

        return await self.admin_POST(
            f"{self.base_url}/create-registry", json_data=req_body
        )

    async def send_revocation_registry_definition(self, rev_reg_id: str):
        """
        Send revocation registry definition to ledger.
        """

        return await self.admin_POST(
            f"{self.base_url}/registry/{rev_reg_id}/definition"
        )

    async def send_revocation_registry_entry(self, rev_reg_id: str):
        """
        Send revocation registry entry to ledger.
        """

        return await self.admin_POST(f"{self.base_url}/registry/{rev_reg_id}/entry")

    async def upload_revocation_registry_tails_file(self, rev_reg_id: str):
        """
        Upload local tails file to server.
        """

        return await self.admin_PUT(f"{self.base_url}/registry/{rev_reg_id}/tails-file")

    """
    TODO: this API call downloads the Tails file as an octet stream. We need to consider if we
    want to build support for this
    """
    # async def get_revocation_registry_tails_file(self, rev_reg_id: str):
    #     """
    #     Download tails file.
    #     """
    #     return await self.admin_GET(f"{self.base_url}/registry/{rev_reg_id}/tails-file")

    async def update_revocation_registry_state(self, rev_reg_id: str, state: str):
        """
        Set revocation registry state manually.
        """

        params = {}
        if state:
            if not self.__validate_revocation_registry_state(state):
                raise InputError("invalid revocation registry state input")
            params["state"] = state

        return await self.admin_PATCH(
            f"{self.base_url}/registry/{rev_reg_id}/set-state", params=params
        )

    """
    Private utility methods.
    """

    def __validate_revocation_registry_state(self, state: str) -> bool:
        """
        Validate if state input is one of init, generated, posted, active, full.
        """

        return state in self.revocation_states

# For usage please consult https://github.com/hyperledger/aries-cloudagent-python/blob/main/Mediation.md

from .base import BaseController
from aiohttp import ClientSession
import logging
from typing import List

logger = logging.getLogger("aries_controller.mediation")


class MediationController(BaseController):

    def __init__(self, admin_url: str, client_session: ClientSession):
        super().__init__(admin_url, client_session)
        self.base_url = "/mediation"

    def default_handler(self, payload):
        logger.debug("Mediation Message received", payload)


    # Get default mediator
    async def get_default_mediator(self):
        return await self.admin_POST(f"{self.base_url}/default-mediator")


    # Clear default mediator
    async def delete_default_mediator(self):
        return await self.admin_DELETE(f"{self.base_url}/default-mediator")


    # Retrieve keylists by connection or role
    async def get_keylists(self, conn_id: str = None, role: str = None):
        params = {}
        if conn_id:
            params["conn_id"] = conn_id
        if role:
            params["role"] = role

        return await self.admin_GET(f"{self.base_url}/keylists", params=params)


    # Send keylist query to mediator
    async def send_keylist_query(self, request, mediation_id: str, paginate_limit: int = -1, paginate_offset: int = 0):
        params = {}
        params["mediation_id"] = mediation_id
        if paginate_limit:
            params["paginate_limit"] = paginate_limit
        if paginate_offset:
            params["paginate_offset"] = paginate_offset

        return await self.admin_POST(f"{self.base_url}/keylists/{mediation_id}/send-keylist-query", params=params, json_data=request)


    # Send keylist update to mediator
    async def send_keylist_update(self, request, mediation_id: str):
        return await self.admin_POST(f"{self.base_url}/keylists/{mediation_id}/send-keylist-update", json_data=request)


    # Request mediation from connection
    async def request_mediation(self, request, conn_id: str):
        return await self.admin_POST(f"{self.base_url}/request/{conn_id}", json_data=request)


    # Query mediation requests, returns list of all mediation records
    async def get_mediation_records(self, mediator_terms: [str], recipient_terms: [str], state: str = None, conn_id: str = None):
        params = {}
        if conn_id:
            params["conn_id"] = conn_id
        if mediator_terms:
            params["mediator_terms"] = mediator_terms
        if recipient_terms:
            params["recipient_terms"] = recipient_terms
        if state:
            params["state"] = state

        return await self.admin_GET(f"{self.base_url}/requests", params=params)


    # Retrieve mediation request record
    async def get_mediation_record_by_id(self, mediation_id: str):
        return await self.admin_GET(f"{self.base_url}/requests/{mediation_id}")


    # Delete mediation request record
    async def delete_mediation_record_by_id(self, mediation_id: str):
        return await self.admin_DELETE(f"{self.base_url}/requests/{mediation_id}")


    # Deny a stored mediation request
    async def deny_mediation_request_by_id(self, request, mediation_id: str):
        return await self.admin_POST(f"{self.base_url}/requests/{mediation_id}/deny", json_data=request)


    # Grant received mediation request
    async def grant_mediation_request_by_id(self, mediation_id: str):
        return await self.admin_POST(f"{self.base_url}/requests/{mediation_id}/grant")


    # Grant received mediation request
    async def set_default_mediator(self, mediation_id: str):
        return await self.admin_PUT(f"{self.base_url}/requests/{mediation_id}/default-mediator")

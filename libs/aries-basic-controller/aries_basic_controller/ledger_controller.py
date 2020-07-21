from .base_controller import BaseController
from aiohttp import ClientSession
import logging

logger = logging.getLogger("aries_controller.ledger")

class LedgerController(BaseController):

    def __init__(self, admin_url: str, client_session: ClientSession):
        super().__init__(admin_url, client_session)
        self.base_url = "/ledger"

    async def get_did_verkey(self, did):
        params = {
            "did": did
        }
        return await self.admin_GET(f"{self.base_url}/did-verkey", params=params)

    async def get_did_endpoint(self, did):
        params = {
            "did": did
        }
        return await self.admin_GET(f"{self.base_url}/did-endpoint", params=params)

    async def get_taa(self):
        return await self.admin_GET(f"{self.base_url}/taa")



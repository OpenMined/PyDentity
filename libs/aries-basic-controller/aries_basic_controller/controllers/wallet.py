from .base import BaseController
from aiohttp import ClientSession
import logging

logger = logging.getLogger("aries_controller.wallet")

class WalletController(BaseController):

    def __init__(self, admin_url: str, client_session: ClientSession):
        super().__init__(admin_url, client_session)
        self.base_url = "/wallet"

    async def get_dids(self):
        return await self.admin_GET(f"{self.base_url}/did")


    async def create_did(self):
        return await self.admin_POST(f"{self.base_url}/did/create")

    async def get_public_did(self):
        return await self.admin_GET(f"{self.base_url}/did/public")

    async def assign_public_did(self, did):
        params = {
            "did": did
        }
        return await self.admin_POST(f"{self.base_url}/did/public", params=params)

    async def get_tag_policy(self, credential_definition_id):
        return await self.admin_GET(f"{self.base_url}/tag-policy/{credential_definition_id}")

    async def set_tag_policy(self, credential_definition_id):
        return await self.admin_POST(f"{self.base_url}/tag-policy/{credential_definition_id}")
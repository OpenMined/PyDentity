# For usage please consult https://github.com/hyperledger/aries-cloudagent-python/blob/main/Mediation.md

from .base import BaseController
from aiohttp import ClientSession
import logging
from typing import List

logger = logging.getLogger("aries_controller.multitenancy")


class MultitenancyController(BaseController):
    def __init__(self, admin_url: str, client_session: ClientSession):
        super().__init__(admin_url, client_session)
        self.base_url = "/multitenancy"

    def default_handler(self, payload):
        logger.debug("Multitenancy Message received", payload)

    # Create a subwallet
    async def create_subwallet(self, request):
        return await self.admin_POST(f"{self.base_url}/wallet", json_data=request)

    # Get a single subwallet
    async def get_single_subwallet_by_id(self, wallet_id: str):
        return await self.admin_GET(f"{self.base_url}/wallet/{wallet_id}")

    # Update a subwallet
    async def update_subwallet_by_id(self, request, wallet_id: str):
        return await self.admin_PUT(
            f"{self.base_url}/wallet/{wallet_id}", json_data=request
        )

    # Remove a subwallet
    async def remove_subwallet_by_id(self, wallet_id: str, request=None):
        return await self.admin_POST(
            f"{self.base_url}/wallet/{wallet_id}/remove", json_data=request
        )

    # Get auth token for a subwallet
    async def get_subwallet_authtoken_by_id(self, wallet_id: str, request=None):
        return await self.admin_POST(
            f"{self.base_url}/wallet/{wallet_id}/token", json_data=request
        )

    # Query subwallets
    async def query_subwallets(self, wallet_name: str = None):
        params = {}
        if wallet_name:
            params["wallet_name"] = wallet_name

        return await self.admin_GET(f"{self.base_url}/wallets")

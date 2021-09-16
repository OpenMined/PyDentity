from uplink import (
    Consumer,
    Path,
    Query,
    Body,
    Header,
    get,
    post,
    patch,
    put,
    delete,
    returns,
    json,
)

from typing import Dict, List, Optional, Union  # noqa: F401

from aries_cloudcontroller.model.create_wallet_request import CreateWalletRequest
from aries_cloudcontroller.model.create_wallet_response import CreateWalletResponse
from aries_cloudcontroller.model.create_wallet_token_request import (
    CreateWalletTokenRequest,
)
from aries_cloudcontroller.model.create_wallet_token_response import (
    CreateWalletTokenResponse,
)
from aries_cloudcontroller.model.remove_wallet_request import RemoveWalletRequest
from aries_cloudcontroller.model.update_wallet_request import UpdateWalletRequest
from aries_cloudcontroller.model.wallet_list import WalletList
from aries_cloudcontroller.model.wallet_record import WalletRecord


class MultitenancyApi(Consumer):
    async def create_wallet(
        self, *, body: Optional[CreateWalletRequest] = None
    ) -> CreateWalletResponse:
        """Create a subwallet"""
        return await self.__create_wallet(
            body=body,
        )

    async def delete_wallet(
        self, *, wallet_id: str, body: Optional[RemoveWalletRequest] = None
    ) -> Dict:
        """Remove a subwallet"""
        return await self.__delete_wallet(
            wallet_id=wallet_id,
            body=body,
        )

    async def get_auth_token(
        self, *, wallet_id: str, body: Optional[CreateWalletTokenRequest] = None
    ) -> CreateWalletTokenResponse:
        """Get auth token for a subwallet"""
        return await self.__get_auth_token(
            wallet_id=wallet_id,
            body=body,
        )

    async def get_wallet(self, *, wallet_id: str) -> WalletRecord:
        """Get a single subwallet"""
        return await self.__get_wallet(
            wallet_id=wallet_id,
        )

    async def get_wallets(self, *, wallet_name: Optional[str] = None) -> WalletList:
        """Query subwallets"""
        return await self.__get_wallets(
            wallet_name=wallet_name,
        )

    async def update_wallet(
        self, *, wallet_id: str, body: Optional[UpdateWalletRequest] = None
    ) -> WalletRecord:
        """Update a subwallet"""
        return await self.__update_wallet(
            wallet_id=wallet_id,
            body=body,
        )

    @returns.json
    @json
    @post("/multitenancy/wallet")
    def __create_wallet(
        self, *, body: Body(type=CreateWalletRequest) = {}
    ) -> CreateWalletResponse:
        """Internal uplink method for create_wallet"""

    @returns.json
    @json
    @post("/multitenancy/wallet/{wallet_id}/remove")
    def __delete_wallet(
        self, *, wallet_id: str, body: Body(type=RemoveWalletRequest) = {}
    ) -> Dict:
        """Internal uplink method for delete_wallet"""

    @returns.json
    @json
    @post("/multitenancy/wallet/{wallet_id}/token")
    def __get_auth_token(
        self, *, wallet_id: str, body: Body(type=CreateWalletTokenRequest) = {}
    ) -> CreateWalletTokenResponse:
        """Internal uplink method for get_auth_token"""

    @returns.json
    @get("/multitenancy/wallet/{wallet_id}")
    def __get_wallet(self, *, wallet_id: str) -> WalletRecord:
        """Internal uplink method for get_wallet"""

    @returns.json
    @get("/multitenancy/wallets")
    def __get_wallets(self, *, wallet_name: Query = None) -> WalletList:
        """Internal uplink method for get_wallets"""

    @returns.json
    @json
    @put("/multitenancy/wallet/{wallet_id}")
    def __update_wallet(
        self, *, wallet_id: str, body: Body(type=UpdateWalletRequest) = {}
    ) -> WalletRecord:
        """Internal uplink method for update_wallet"""

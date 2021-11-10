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

from aries_cloudcontroller.uplink_util import bool_query

from aries_cloudcontroller.model.get_did_endpoint_response import GetDIDEndpointResponse
from aries_cloudcontroller.model.get_did_verkey_response import GetDIDVerkeyResponse
from aries_cloudcontroller.model.get_nym_role_response import GetNymRoleResponse
from aries_cloudcontroller.model.register_ledger_nym_response import (
    RegisterLedgerNymResponse,
)
from aries_cloudcontroller.model.taa_accept import TAAAccept
from aries_cloudcontroller.model.taa_result import TAAResult


class LedgerApi(Consumer):
    async def accept_taa(self, *, body: Optional[TAAAccept] = None) -> Dict:
        """Accept the transaction author agreement"""
        return await self.__accept_taa(
            body=body,
        )

    async def fetch_taa(self) -> TAAResult:
        """Fetch the current transaction author agreement, if any"""
        return await self.__fetch_taa()

    async def get_did_endpoint(
        self, *, did: str, endpoint_type: Optional[str] = None
    ) -> GetDIDEndpointResponse:
        """Get the endpoint for a DID from the ledger."""
        return await self.__get_did_endpoint(
            did=did,
            endpoint_type=endpoint_type,
        )

    async def get_did_nym_role(self, *, did: str) -> GetNymRoleResponse:
        """Get the role from the NYM registration of a public DID."""
        return await self.__get_did_nym_role(
            did=did,
        )

    async def get_did_verkey(self, *, did: str) -> GetDIDVerkeyResponse:
        """Get the verkey for a DID from the ledger."""
        return await self.__get_did_verkey(
            did=did,
        )

    async def register_nym(
        self,
        *,
        did: str,
        verkey: str,
        alias: Optional[str] = None,
        role: Optional[str] = None
    ) -> RegisterLedgerNymResponse:
        """Send a NYM registration to the ledger."""
        return await self.__register_nym(
            did=did,
            verkey=verkey,
            alias=alias,
            role=role,
        )

    async def rotate_public_did_keypair(self) -> Dict:
        """Rotate key pair for public DID."""
        return await self.__rotate_public_did_keypair()

    @returns.json
    @json
    @post("/ledger/taa/accept")
    def __accept_taa(self, *, body: Body(type=TAAAccept) = {}) -> Dict:
        """Internal uplink method for accept_taa"""

    @returns.json
    @get("/ledger/taa")
    def __fetch_taa(self) -> TAAResult:
        """Internal uplink method for fetch_taa"""

    @returns.json
    @get("/ledger/did-endpoint")
    def __get_did_endpoint(
        self, *, did: Query, endpoint_type: Query = None
    ) -> GetDIDEndpointResponse:
        """Internal uplink method for get_did_endpoint"""

    @returns.json
    @get("/ledger/get-nym-role")
    def __get_did_nym_role(self, *, did: Query) -> GetNymRoleResponse:
        """Internal uplink method for get_did_nym_role"""

    @returns.json
    @get("/ledger/did-verkey")
    def __get_did_verkey(self, *, did: Query) -> GetDIDVerkeyResponse:
        """Internal uplink method for get_did_verkey"""

    @returns.json
    @post("/ledger/register-nym")
    def __register_nym(
        self, *, did: Query, verkey: Query, alias: Query = None, role: Query = None
    ) -> RegisterLedgerNymResponse:
        """Internal uplink method for register_nym"""

    @returns.json
    @patch("/ledger/rotate-public-did-keypair")
    def __rotate_public_did_keypair(self) -> Dict:
        """Internal uplink method for rotate_public_did_keypair"""
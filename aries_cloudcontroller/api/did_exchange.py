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

from aries_cloudcontroller.model.conn_record import ConnRecord
from aries_cloudcontroller.model.didx_request import DIDXRequest


class DidExchangeApi(Consumer):
    async def accept_invitation(
        self,
        *,
        conn_id: str,
        my_endpoint: Optional[str] = None,
        my_label: Optional[str] = None
    ) -> ConnRecord:
        """Accept a stored connection invitation"""
        return await self.__accept_invitation(
            conn_id=conn_id,
            my_endpoint=my_endpoint,
            my_label=my_label,
        )

    async def accept_request(
        self,
        *,
        conn_id: str,
        mediation_id: Optional[str] = None,
        my_endpoint: Optional[str] = None
    ) -> ConnRecord:
        """Accept a stored connection request"""
        return await self.__accept_request(
            conn_id=conn_id,
            mediation_id=mediation_id,
            my_endpoint=my_endpoint,
        )

    async def create_request(
        self,
        *,
        their_public_did: str,
        alias: Optional[str] = None,
        mediation_id: Optional[str] = None,
        my_endpoint: Optional[str] = None,
        my_label: Optional[str] = None,
        use_public_did: Optional[bool] = None
    ) -> ConnRecord:
        """Create and send a request against public DID's implicit invitation"""
        return await self.__create_request(
            their_public_did=their_public_did,
            alias=alias,
            mediation_id=mediation_id,
            my_endpoint=my_endpoint,
            my_label=my_label,
            use_public_did=bool_query(use_public_did),
        )

    async def receive_request(
        self,
        *,
        alias: Optional[str] = None,
        auto_accept: Optional[bool] = None,
        mediation_id: Optional[str] = None,
        my_endpoint: Optional[str] = None,
        body: Optional[DIDXRequest] = None
    ) -> ConnRecord:
        """Receive request against public DID's implicit invitation"""
        return await self.__receive_request(
            alias=alias,
            auto_accept=bool_query(auto_accept),
            mediation_id=mediation_id,
            my_endpoint=my_endpoint,
            body=body,
        )

    @returns.json
    @post("/didexchange/{conn_id}/accept-invitation")
    def __accept_invitation(
        self, *, conn_id: str, my_endpoint: Query = None, my_label: Query = None
    ) -> ConnRecord:
        """Internal uplink method for accept_invitation"""

    @returns.json
    @post("/didexchange/{conn_id}/accept-request")
    def __accept_request(
        self, *, conn_id: str, mediation_id: Query = None, my_endpoint: Query = None
    ) -> ConnRecord:
        """Internal uplink method for accept_request"""

    @returns.json
    @post("/didexchange/create-request")
    def __create_request(
        self,
        *,
        their_public_did: Query,
        alias: Query = None,
        mediation_id: Query = None,
        my_endpoint: Query = None,
        my_label: Query = None,
        use_public_did: Query = None
    ) -> ConnRecord:
        """Internal uplink method for create_request"""

    @returns.json
    @json
    @post("/didexchange/receive-request")
    def __receive_request(
        self,
        *,
        alias: Query = None,
        auto_accept: Query = None,
        mediation_id: Query = None,
        my_endpoint: Query = None,
        body: Body(type=DIDXRequest) = {}
    ) -> ConnRecord:
        """Internal uplink method for receive_request"""

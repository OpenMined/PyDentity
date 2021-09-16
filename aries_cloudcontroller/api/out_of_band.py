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

from aries_cloudcontroller.model.conn_record import ConnRecord
from aries_cloudcontroller.model.invitation_create_request import (
    InvitationCreateRequest,
)
from aries_cloudcontroller.model.invitation_message import InvitationMessage
from aries_cloudcontroller.model.invitation_record import InvitationRecord


class OutOfBandApi(Consumer):
    async def create_invitation(
        self,
        *,
        auto_accept: Optional[bool] = None,
        multi_use: Optional[bool] = None,
        body: Optional[InvitationCreateRequest] = None
    ) -> InvitationRecord:
        """Create a new connection invitation"""
        return await self.__create_invitation(
            auto_accept=auto_accept,
            multi_use=multi_use,
            body=body,
        )

    async def receive_invitation(
        self,
        *,
        alias: Optional[str] = None,
        auto_accept: Optional[bool] = None,
        mediation_id: Optional[str] = None,
        use_existing_connection: Optional[bool] = None,
        body: Optional[InvitationMessage] = None
    ) -> ConnRecord:
        """Receive a new connection invitation"""
        return await self.__receive_invitation(
            alias=alias,
            auto_accept=auto_accept,
            mediation_id=mediation_id,
            use_existing_connection=use_existing_connection,
            body=body,
        )

    @returns.json
    @json
    @post("/out-of-band/create-invitation")
    def __create_invitation(
        self,
        *,
        auto_accept: Query = None,
        multi_use: Query = None,
        body: Body(type=InvitationCreateRequest) = {}
    ) -> InvitationRecord:
        """Internal uplink method for create_invitation"""

    @returns.json
    @json
    @post("/out-of-band/receive-invitation")
    def __receive_invitation(
        self,
        *,
        alias: Query = None,
        auto_accept: Query = None,
        mediation_id: Query = None,
        use_existing_connection: Query = None,
        body: Body(type=InvitationMessage) = {}
    ) -> ConnRecord:
        """Internal uplink method for receive_invitation"""

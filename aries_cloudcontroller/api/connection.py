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
from aries_cloudcontroller.model.connection_list import ConnectionList
from aries_cloudcontroller.model.connection_metadata import ConnectionMetadata
from aries_cloudcontroller.model.connection_metadata_set_request import (
    ConnectionMetadataSetRequest,
)
from aries_cloudcontroller.model.connection_static_request import (
    ConnectionStaticRequest,
)
from aries_cloudcontroller.model.connection_static_result import ConnectionStaticResult
from aries_cloudcontroller.model.create_invitation_request import (
    CreateInvitationRequest,
)
from aries_cloudcontroller.model.endpoints_result import EndpointsResult
from aries_cloudcontroller.model.invitation_result import InvitationResult
from aries_cloudcontroller.model.receive_invitation_request import (
    ReceiveInvitationRequest,
)


class ConnectionApi(Consumer):
    async def accept_invitation(
        self,
        *,
        conn_id: str,
        mediation_id: Optional[str] = None,
        my_endpoint: Optional[str] = None,
        my_label: Optional[str] = None
    ) -> ConnRecord:
        """Accept a stored connection invitation"""
        return await self.__accept_invitation(
            conn_id=conn_id,
            mediation_id=mediation_id,
            my_endpoint=my_endpoint,
            my_label=my_label,
        )

    async def accept_request(
        self, *, conn_id: str, my_endpoint: Optional[str] = None
    ) -> ConnRecord:
        """Accept a stored connection request"""
        return await self.__accept_request(
            conn_id=conn_id,
            my_endpoint=my_endpoint,
        )

    async def create_invitation(
        self,
        *,
        alias: Optional[str] = None,
        auto_accept: Optional[bool] = None,
        multi_use: Optional[bool] = None,
        public: Optional[bool] = None,
        body: Optional[CreateInvitationRequest] = None
    ) -> InvitationResult:
        """Create a new connection invitation"""
        return await self.__create_invitation(
            alias=alias,
            auto_accept=bool_query(auto_accept),
            multi_use=bool_query(multi_use),
            public=bool_query(public),
            body=body,
        )

    async def create_static_connection(
        self, *, body: Optional[ConnectionStaticRequest] = None
    ) -> ConnectionStaticResult:
        """Create a new static connection"""
        return await self.__create_static_connection(
            body=body,
        )

    async def delete_connection(self, *, conn_id: str) -> Dict:
        """Remove an existing connection record"""
        return await self.__delete_connection(
            conn_id=conn_id,
        )

    async def establish_inbound(self, *, conn_id: str, ref_id: str) -> Dict:
        """Assign another connection as the inbound connection"""
        return await self.__establish_inbound(
            conn_id=conn_id,
            ref_id=ref_id,
        )

    async def get_connection(self, *, conn_id: str) -> ConnRecord:
        """Fetch a single connection record"""
        return await self.__get_connection(
            conn_id=conn_id,
        )

    async def get_connection_endpoint(self, *, conn_id: str) -> EndpointsResult:
        """Fetch connection remote endpoint"""
        return await self.__get_connection_endpoint(
            conn_id=conn_id,
        )

    async def get_connections(
        self,
        *,
        alias: Optional[str] = None,
        connection_protocol: Optional[str] = None,
        invitation_key: Optional[str] = None,
        my_did: Optional[str] = None,
        state: Optional[str] = None,
        their_did: Optional[str] = None,
        their_role: Optional[str] = None
    ) -> ConnectionList:
        """Query agent-to-agent connections"""
        return await self.__get_connections(
            alias=alias,
            connection_protocol=connection_protocol,
            invitation_key=invitation_key,
            my_did=my_did,
            state=state,
            their_did=their_did,
            their_role=their_role,
        )

    async def get_metadata(
        self, *, conn_id: str, key: Optional[str] = None
    ) -> ConnectionMetadata:
        """Fetch connection metadata"""
        return await self.__get_metadata(
            conn_id=conn_id,
            key=key,
        )

    async def receive_invitation(
        self,
        *,
        alias: Optional[str] = None,
        auto_accept: Optional[bool] = None,
        mediation_id: Optional[str] = None,
        body: Optional[ReceiveInvitationRequest] = None
    ) -> ConnRecord:
        """Receive a new connection invitation"""
        return await self.__receive_invitation(
            alias=alias,
            auto_accept=bool_query(auto_accept),
            mediation_id=mediation_id,
            body=body,
        )

    async def set_metadata(
        self, *, conn_id: str, body: Optional[ConnectionMetadataSetRequest] = None
    ) -> ConnectionMetadata:
        """Set connection metadata"""
        return await self.__set_metadata(
            conn_id=conn_id,
            body=body,
        )

    @returns.json
    @post("/connections/{conn_id}/accept-invitation")
    def __accept_invitation(
        self,
        *,
        conn_id: str,
        mediation_id: Query = None,
        my_endpoint: Query = None,
        my_label: Query = None
    ) -> ConnRecord:
        """Internal uplink method for accept_invitation"""

    @returns.json
    @post("/connections/{conn_id}/accept-request")
    def __accept_request(
        self, *, conn_id: str, my_endpoint: Query = None
    ) -> ConnRecord:
        """Internal uplink method for accept_request"""

    @returns.json
    @json
    @post("/connections/create-invitation")
    def __create_invitation(
        self,
        *,
        alias: Query = None,
        auto_accept: Query = None,
        multi_use: Query = None,
        public: Query = None,
        body: Body(type=CreateInvitationRequest) = {}
    ) -> InvitationResult:
        """Internal uplink method for create_invitation"""

    @returns.json
    @json
    @post("/connections/create-static")
    def __create_static_connection(
        self, *, body: Body(type=ConnectionStaticRequest) = {}
    ) -> ConnectionStaticResult:
        """Internal uplink method for create_static_connection"""

    @returns.json
    @delete("/connections/{conn_id}")
    def __delete_connection(self, *, conn_id: str) -> Dict:
        """Internal uplink method for delete_connection"""

    @returns.json
    @post("/connections/{conn_id}/establish-inbound/{ref_id}")
    def __establish_inbound(self, *, conn_id: str, ref_id: str) -> Dict:
        """Internal uplink method for establish_inbound"""

    @returns.json
    @get("/connections/{conn_id}")
    def __get_connection(self, *, conn_id: str) -> ConnRecord:
        """Internal uplink method for get_connection"""

    @returns.json
    @get("/connections/{conn_id}/endpoints")
    def __get_connection_endpoint(self, *, conn_id: str) -> EndpointsResult:
        """Internal uplink method for get_connection_endpoint"""

    @returns.json
    @get("/connections")
    def __get_connections(
        self,
        *,
        alias: Query = None,
        connection_protocol: Query = None,
        invitation_key: Query = None,
        my_did: Query = None,
        state: Query = None,
        their_did: Query = None,
        their_role: Query = None
    ) -> ConnectionList:
        """Internal uplink method for get_connections"""

    @returns.json
    @get("/connections/{conn_id}/metadata")
    def __get_metadata(self, *, conn_id: str, key: Query = None) -> ConnectionMetadata:
        """Internal uplink method for get_metadata"""

    @returns.json
    @json
    @post("/connections/receive-invitation")
    def __receive_invitation(
        self,
        *,
        alias: Query = None,
        auto_accept: Query = None,
        mediation_id: Query = None,
        body: Body(type=ReceiveInvitationRequest) = {}
    ) -> ConnRecord:
        """Internal uplink method for receive_invitation"""

    @returns.json
    @json
    @post("/connections/{conn_id}/metadata")
    def __set_metadata(
        self, *, conn_id: str, body: Body(type=ConnectionMetadataSetRequest) = {}
    ) -> ConnectionMetadata:
        """Internal uplink method for set_metadata"""

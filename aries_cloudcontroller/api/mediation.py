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

from aries_cloudcontroller.model.admin_mediation_deny import AdminMediationDeny
from aries_cloudcontroller.model.keylist import Keylist
from aries_cloudcontroller.model.keylist_query import KeylistQuery
from aries_cloudcontroller.model.keylist_query_filter_request import (
    KeylistQueryFilterRequest,
)
from aries_cloudcontroller.model.keylist_update import KeylistUpdate
from aries_cloudcontroller.model.keylist_update_request import KeylistUpdateRequest
from aries_cloudcontroller.model.mediation_create_request import MediationCreateRequest
from aries_cloudcontroller.model.mediation_deny import MediationDeny
from aries_cloudcontroller.model.mediation_grant import MediationGrant
from aries_cloudcontroller.model.mediation_list import MediationList
from aries_cloudcontroller.model.mediation_record import MediationRecord


class MediationApi(Consumer):
    async def clear_default_mediator(self) -> MediationRecord:
        """Clear default mediator"""
        return await self.__clear_default_mediator()

    async def delete_record(self, *, mediation_id: str) -> MediationRecord:
        """Delete mediation request by ID"""
        return await self.__delete_record(
            mediation_id=mediation_id,
        )

    async def deny_mediation_request(
        self, *, mediation_id: str, body: Optional[AdminMediationDeny] = None
    ) -> MediationDeny:
        """Deny a stored mediation request"""
        return await self.__deny_mediation_request(
            mediation_id=mediation_id,
            body=body,
        )

    async def get_default_mediator(self) -> MediationRecord:
        """Get default mediator"""
        return await self.__get_default_mediator()

    async def get_record(self, *, mediation_id: str) -> MediationRecord:
        """Retrieve mediation request record"""
        return await self.__get_record(
            mediation_id=mediation_id,
        )

    async def get_records(
        self,
        *,
        conn_id: Optional[str] = None,
        mediator_terms: Optional[List[str]] = None,
        recipient_terms: Optional[List[str]] = None,
        state: Optional[str] = None
    ) -> MediationList:
        """Query mediation requests, returns list of all mediation records"""
        return await self.__get_records(
            conn_id=conn_id,
            mediator_terms=mediator_terms,
            recipient_terms=recipient_terms,
            state=state,
        )

    async def grant_mediation_request(self, *, mediation_id: str) -> MediationGrant:
        """Grant received mediation"""
        return await self.__grant_mediation_request(
            mediation_id=mediation_id,
        )

    async def request_mediation(
        self, *, conn_id: str, body: Optional[MediationCreateRequest] = None
    ) -> MediationRecord:
        """Request mediation from connection"""
        return await self.__request_mediation(
            conn_id=conn_id,
            body=body,
        )

    async def retrieve_keylists(
        self, *, conn_id: Optional[str] = None, role: Optional[str] = "server"
    ) -> Keylist:
        """Retrieve keylists by connection or role"""
        return await self.__retrieve_keylists(
            conn_id=conn_id,
            role=role,
        )

    async def send_keylist_query(
        self,
        *,
        mediation_id: str,
        paginate_limit: Optional[int] = -1,
        paginate_offset: Optional[int] = 0,
        body: Optional[KeylistQueryFilterRequest] = None
    ) -> KeylistQuery:
        """Send keylist query to mediator"""
        return await self.__send_keylist_query(
            mediation_id=mediation_id,
            paginate_limit=paginate_limit,
            paginate_offset=paginate_offset,
            body=body,
        )

    async def send_keylist_update(
        self, *, mediation_id: str, body: Optional[KeylistUpdateRequest] = None
    ) -> KeylistUpdate:
        """Send keylist update to mediator"""
        return await self.__send_keylist_update(
            mediation_id=mediation_id,
            body=body,
        )

    async def set_default_mediator(self, *, mediation_id: str) -> MediationRecord:
        """Set default mediator"""
        return await self.__set_default_mediator(
            mediation_id=mediation_id,
        )

    @returns.json
    @delete("/mediation/default-mediator")
    def __clear_default_mediator(self) -> MediationRecord:
        """Internal uplink method for clear_default_mediator"""

    @returns.json
    @delete("/mediation/requests/{mediation_id}")
    def __delete_record(self, *, mediation_id: str) -> MediationRecord:
        """Internal uplink method for delete_record"""

    @returns.json
    @json
    @post("/mediation/requests/{mediation_id}/deny")
    def __deny_mediation_request(
        self, *, mediation_id: str, body: Body(type=AdminMediationDeny) = {}
    ) -> MediationDeny:
        """Internal uplink method for deny_mediation_request"""

    @returns.json
    @get("/mediation/default-mediator")
    def __get_default_mediator(self) -> MediationRecord:
        """Internal uplink method for get_default_mediator"""

    @returns.json
    @get("/mediation/requests/{mediation_id}")
    def __get_record(self, *, mediation_id: str) -> MediationRecord:
        """Internal uplink method for get_record"""

    @returns.json
    @get("/mediation/requests")
    def __get_records(
        self,
        *,
        conn_id: Query = None,
        mediator_terms: Query = None,
        recipient_terms: Query = None,
        state: Query = None
    ) -> MediationList:
        """Internal uplink method for get_records"""

    @returns.json
    @post("/mediation/requests/{mediation_id}/grant")
    def __grant_mediation_request(self, *, mediation_id: str) -> MediationGrant:
        """Internal uplink method for grant_mediation_request"""

    @returns.json
    @json
    @post("/mediation/request/{conn_id}")
    def __request_mediation(
        self, *, conn_id: str, body: Body(type=MediationCreateRequest) = {}
    ) -> MediationRecord:
        """Internal uplink method for request_mediation"""

    @returns.json
    @get("/mediation/keylists")
    def __retrieve_keylists(
        self, *, conn_id: Query = None, role: Query = "server"
    ) -> Keylist:
        """Internal uplink method for retrieve_keylists"""

    @returns.json
    @json
    @post("/mediation/keylists/{mediation_id}/send-keylist-query")
    def __send_keylist_query(
        self,
        *,
        mediation_id: str,
        paginate_limit: Query = -1,
        paginate_offset: Query = 0,
        body: Body(type=KeylistQueryFilterRequest) = {}
    ) -> KeylistQuery:
        """Internal uplink method for send_keylist_query"""

    @returns.json
    @json
    @post("/mediation/keylists/{mediation_id}/send-keylist-update")
    def __send_keylist_update(
        self, *, mediation_id: str, body: Body(type=KeylistUpdateRequest) = {}
    ) -> KeylistUpdate:
        """Internal uplink method for send_keylist_update"""

    @returns.json
    @put("/mediation/{mediation_id}/default-mediator")
    def __set_default_mediator(self, *, mediation_id: str) -> MediationRecord:
        """Internal uplink method for set_default_mediator"""

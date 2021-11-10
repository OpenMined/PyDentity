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

from aries_cloudcontroller.model.action_menu_fetch_result import ActionMenuFetchResult
from aries_cloudcontroller.model.perform_request import PerformRequest
from aries_cloudcontroller.model.send_menu import SendMenu


class ActionMenuApi(Consumer):
    async def close_active_menu(self, *, conn_id: str) -> Dict:
        """Close the active menu associated with a connection"""
        return await self.__close_active_menu(
            conn_id=conn_id,
        )

    async def fetch_active_menu(self, *, conn_id: str) -> ActionMenuFetchResult:
        """Fetch the active menu"""
        return await self.__fetch_active_menu(
            conn_id=conn_id,
        )

    async def perform_action(
        self, *, conn_id: str, body: Optional[PerformRequest] = None
    ) -> Dict:
        """Perform an action associated with the active menu"""
        return await self.__perform_action(
            conn_id=conn_id,
            body=body,
        )

    async def request_active_menu(self, *, conn_id: str) -> Dict:
        """Request the active menu"""
        return await self.__request_active_menu(
            conn_id=conn_id,
        )

    async def send_menu(self, *, conn_id: str, body: Optional[SendMenu] = None) -> Dict:
        """Send an action menu to a connection"""
        return await self.__send_menu(
            conn_id=conn_id,
            body=body,
        )

    @returns.json
    @post("/action-menu/{conn_id}/close")
    def __close_active_menu(self, *, conn_id: str) -> Dict:
        """Internal uplink method for close_active_menu"""

    @returns.json
    @post("/action-menu/{conn_id}/fetch")
    def __fetch_active_menu(self, *, conn_id: str) -> ActionMenuFetchResult:
        """Internal uplink method for fetch_active_menu"""

    @returns.json
    @json
    @post("/action-menu/{conn_id}/perform")
    def __perform_action(
        self, *, conn_id: str, body: Body(type=PerformRequest) = {}
    ) -> Dict:
        """Internal uplink method for perform_action"""

    @returns.json
    @post("/action-menu/{conn_id}/request")
    def __request_active_menu(self, *, conn_id: str) -> Dict:
        """Internal uplink method for request_active_menu"""

    @returns.json
    @json
    @post("/action-menu/{conn_id}/send-menu")
    def __send_menu(self, *, conn_id: str, body: Body(type=SendMenu) = {}) -> Dict:
        """Internal uplink method for send_menu"""
